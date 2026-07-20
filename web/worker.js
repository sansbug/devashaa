/**
 * devashaa.com — static site + the account and profile store.
 *
 * THIS SERVER CANNOT READ THE PROFILES IT STORES, and that is architectural
 * rather than a promise. The AES key is derived on the client from a password
 * this server never receives; what arrives is a verifier derived from the same
 * password by a *different* HKDF branch, plus ciphertext. Holding every row in
 * the database reveals no name, birth date, birth time or place.
 *
 * The account exists only to give people a login instead of a written-down
 * phrase. It buys convenience, NOT recovery: with no email on file a forgotten
 * password is unrecoverable, and the UI says so before registration.
 *
 * WHY D1 AND NOT KV, AND NOT THE PYTHON API
 * ------------------------------------------
 * Uniqueness of a userid needs a real constraint. KV has no atomic
 * check-and-set, so two simultaneous registrations could both observe "free"
 * and both write. D1's PRIMARY KEY makes that a database error instead of a
 * silent account collision.
 *
 * And not Render: its free plan has an ephemeral filesystem, so anything
 * written there is destroyed on the next deploy.
 */

const HEX64 = /^[0-9a-f]{64}$/
// Deliberately narrow: lowercase, digits and a separator. No unicode, so two
// userids cannot look identical while differing in codepoints (homograph
// confusion is an account-takeover vector, not a cosmetic issue).
const USERID = /^[a-z0-9][a-z0-9._-]{2,31}$/
const MAX_BLOB = 64 * 1024
const MAX_PROFILES = 200

function corsHeaders(request) {
  const origin = request.headers.get('Origin') || ''
  const ok = /^https:\/\/(www\.)?devashaa\.com$/.test(origin)
    || /^http:\/\/localhost:\d+$/.test(origin)
  return ok
    ? {
        'Access-Control-Allow-Origin': origin,
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,X-Auth',
        'Access-Control-Max-Age': '86400',
        Vary: 'Origin',
      }
    : {}
}

const json = (body, status, request) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      'Content-Type': 'application/json',
      // User data, never cacheable — an intermediary copy would outlive the
      // user's own delete.
      'Cache-Control': 'no-store',
      ...corsHeaders(request),
    },
  })

async function sha256Hex(s) {
  const buf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s))
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('')
}

/** Constant-time compare, so a timing signal cannot confirm a partial guess. */
function timingSafeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false
  let diff = 0
  for (let i = 0; i < a.length; i++) diff |= a.charCodeAt(i) ^ b.charCodeAt(i)
  return diff === 0
}

/** Verifies X-Auth against the stored hash. Returns true/false, never throws. */
async function authorise(db, userid, request) {
  const authId = request.headers.get('X-Auth') || ''
  if (!HEX64.test(authId)) return false
  const row = await db.prepare('SELECT auth_hash FROM users WHERE userid = ?')
    .bind(userid).first()
  if (!row) return false
  return timingSafeEqual(row.auth_hash, await sha256Hex(authId))
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url)
    const path = url.pathname

    if (!path.startsWith('/api/account')) return env.ASSETS.fetch(request)
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(request) })
    }

    const db = env.DB
    if (!db) return json({ error: 'account storage is not configured' }, 503, request)

    const seg = path.split('/').filter(Boolean)      // api, account, ...
    const userid = (seg[2] || '').toLowerCase()
    const body = ['POST', 'PUT'].includes(request.method)
      ? await request.json().catch(() => null)
      : null

    // --- POST /api/account  { userid, authId }  → register
    if (seg.length === 2 && request.method === 'POST') {
      const id = String(body?.userid || '').toLowerCase().trim()
      const authId = String(body?.authId || '')
      if (!USERID.test(id)) {
        return json({
          error: 'A user id is 3–32 characters: lowercase letters, digits, '
               + 'and . _ - after the first character.',
        }, 400, request)
      }
      if (!HEX64.test(authId)) return json({ error: 'bad authId' }, 400, request)
      try {
        await db.prepare(
          'INSERT INTO users (userid, auth_hash, created_at) VALUES (?, ?, ?)',
        ).bind(id, await sha256Hex(authId), Date.now()).run()
      } catch {
        // The PRIMARY KEY is what actually enforces uniqueness. The availability
        // check below is a courtesy for the UI and is NOT authoritative — two
        // registrations racing the same id both see "free" and one loses here.
        return json({ error: 'That user id is taken.' }, 409, request)
      }
      return json({ ok: true, userid: id }, 201, request)
    }

    if (!USERID.test(userid)) return json({ error: 'bad user id' }, 400, request)

    // --- GET /api/account/<id>  → availability, for the signup form only
    if (seg.length === 3 && request.method === 'GET') {
      const row = await db.prepare('SELECT 1 AS x FROM users WHERE userid = ?')
        .bind(userid).first()
      return json({ exists: !!row }, 200, request)
    }

    // --- DELETE /api/account/<id>  → remove the account and every profile
    if (seg.length === 3 && request.method === 'DELETE') {
      if (!await authorise(db, userid, request)) {
        return json({ error: 'unauthorised' }, 401, request)
      }
      // Deletion must always work: it is the user's data and there is no
      // support channel to appeal to.
      await db.batch([
        db.prepare('DELETE FROM profiles WHERE userid = ?').bind(userid),
        db.prepare('DELETE FROM users WHERE userid = ?').bind(userid),
      ])
      return json({ ok: true }, 200, request)
    }

    // --- POST /api/account/<id>/login  { authId }
    if (seg.length === 4 && seg[3] === 'login' && request.method === 'POST') {
      const authId = String(body?.authId || '')
      if (!HEX64.test(authId)) return json({ error: 'unauthorised' }, 401, request)
      const row = await db.prepare('SELECT auth_hash FROM users WHERE userid = ?')
        .bind(userid).first()
      // Same answer whether the account is missing or the password is wrong, so
      // login cannot be used to enumerate which userids exist.
      const ok = row && timingSafeEqual(row.auth_hash, await sha256Hex(authId))
      return ok
        ? json({ ok: true }, 200, request)
        : json({ error: 'Wrong user id or password.' }, 401, request)
    }

    // --- /api/account/<id>/profiles ...
    if (seg[3] === 'profiles') {
      if (!await authorise(db, userid, request)) {
        return json({ error: 'unauthorised' }, 401, request)
      }

      if (seg.length === 4 && request.method === 'GET') {
        const { results } = await db.prepare(
          'SELECT profile_id, blob, updated_at FROM profiles WHERE userid = ?',
        ).bind(userid).all()
        return json({ profiles: results || [] }, 200, request)
      }

      const profileId = seg[4] || ''
      if (!HEX64.test(profileId)) return json({ error: 'bad profile id' }, 400, request)

      if (request.method === 'PUT') {
        const blob = body?.blob
        if (typeof blob !== 'string' || !blob) {
          return json({ error: 'expected {blob: string}' }, 400, request)
        }
        if (blob.length > MAX_BLOB) return json({ error: 'blob too large' }, 413, request)
        const { count } = await db.prepare(
          'SELECT COUNT(*) AS count FROM profiles WHERE userid = ? AND profile_id != ?',
        ).bind(userid, profileId).first()
        if (count >= MAX_PROFILES) {
          return json({ error: `at most ${MAX_PROFILES} charts per account` }, 409, request)
        }
        // Opaque in, opaque out. Nothing here parses or indexes the value.
        await db.prepare(
          'INSERT INTO profiles (userid, profile_id, blob, updated_at) VALUES (?,?,?,?) '
          + 'ON CONFLICT(userid, profile_id) DO UPDATE SET blob = excluded.blob, '
          + 'updated_at = excluded.updated_at',
        ).bind(userid, profileId, blob, Date.now()).run()
        return json({ ok: true }, 200, request)
      }

      if (request.method === 'DELETE') {
        await db.prepare('DELETE FROM profiles WHERE userid = ? AND profile_id = ?')
          .bind(userid, profileId).run()
        return json({ ok: true }, 200, request)
      }
    }

    return json({ error: 'not found' }, 404, request)
  },
}
