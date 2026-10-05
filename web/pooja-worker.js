/**
 * Devashaa Pūjā — the Worker side.
 *
 * A separate service from the astrology site that happens to share its Worker:
 * a vetted roster of pandits, bookings, a live room, recordings, and the voice
 * library.
 *
 *   /api/pooja/where                   GET   the visitor's approximate city, from the edge (not stored)
 *   /api/pooja/priests                 GET   the approved roster (public fields)
 *   /api/pooja/priests/apply           POST  apply / update own profile     (auth)
 *   /api/pooja/priests/<pid>/vet       POST  approve | reject an applicant  (auth: approved pandit or admin)
 *   /api/pooja/me                      GET   own role + profile             (auth)
 *   /api/pooja/admin/claim             POST  become admin with the one-time code (auth)
 *   /api/pooja/desk                    GET   applicants + bookings for a pandit / admin (auth)
 *   /api/pooja/bookings                POST  request a pūjā, or open a family gathering (public)
 *   /api/pooja/bookings/<id>           GET   one booking — the id IS the secret
 *   /api/pooja/bookings/<id>/accept    POST  a pandit takes it              (auth)
 *   /api/pooja/bookings/<id>/complete  POST                                   (auth)
 *   /api/pooja/bookings/<id>/cancel    POST  by whoever holds the id
 *   /api/pooja/room/<id>/ws            WS    signalling for the live room (Durable Object)
 *   /api/pooja/room/<id>/ice           GET   STUN + short-lived TURN relay credentials for the room
 *   /api/pooja/rec/<id>/<seq>          PUT   one recorded chunk             (auth: the booking's pandit or admin)
 *   /api/pooja/rec/<id>                GET   how much is recorded
 *   /api/pooja/rec/<id>/play           GET   the recording, chunks streamed in order
 *   /api/pooja/chants                  GET   which clips are recorded, by whom, in which voice
 *   /api/pooja/chant/<clip>            PUT   a pandit's own recording of that clip (auth: approved pandit)
 *   /api/pooja/chant/<clip>/<pid>      GET   that recording · DELETE (auth: its pandit, or admin)
 *
 * WHAT IS STORED, AND WHY IT IS NOT ENCRYPTED LIKE THE CHARTS
 * A booking carries a name and a contact, in the clear, because the pandit has
 * to be able to reach the family; the contact is shown only to the pandit who
 * has taken the booking and to admins. A pandit's profile is public by design
 * — but never the id he signs in with, which may be his email: everything
 * public names a pandit by a random `pid`. Nothing here touches the chart
 * store, and a chart is never attached to a booking.
 *
 * A FAMILY GATHERING ('self') is a room a family opens to keep a ceremony on
 * its own with the guide: no pandit, no contact stored, never shown on a
 * pandit's desk.
 *
 * VETTING. The roster starts with pandits the owner knows (they apply, an
 * admin approves) and grows by application: any approved pandit can vet a
 * joiner. The first admin is made with a one-time code held as a Worker
 * secret (POOJA_ADMIN_CODE).
 *
 * THE ROOM is a WebRTC mesh; this Worker only relays the handshake. Media goes
 * peer to peer where the two networks allow it. Where they do not (strict
 * NATs, office and hotel firewalls) it goes through a TURN relay: Cloudflare
 * Realtime TURN, with credentials minted here per room and valid for hours,
 * not for ever. The relay is on when the Worker has TURN_KEY_ID and
 * TURN_KEY_API_TOKEN; without them the room is STUN-only and says so.
 * The recording is made in the pandit's browser and uploaded here in chunks,
 * so the family can watch later from their booking page.
 *
 * THE VOICE LIBRARY. The guided ceremony is voiced by people, not by a
 * machine: a pandit on the roster records each mantra — and, if he will, each
 * explanation in English or Hindi — once, in his own voice. A clip is named by
 * what it is and by a hash of its text (see web/src/pooja/guide.js clipId), so
 * a recording can never be played over a text it was not read from. One
 * recording per pandit per clip; only he (or an admin) can replace or remove
 * it. The pandit's voice (male / female) comes from his profile, so a family
 * can ask for either.
 */

const HEX32 = /^[0-9a-f]{32}$/
const PID = /^[0-9a-f]{16}$/
const USERID = /^(?:[a-z0-9][a-z0-9._-]{2,31}|[a-z0-9._%+-]{1,64}@[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,24})$/
const CLIP_ID = /^[a-z](?:[A-Za-z0-9-]|\.(?!\.)){2,90}$/      // m.ganesha.1a2b3c · x.ganesha.en.short.1a2b3c · p.griha-pravesh.hi.detailed.1a2b3c
const MAX_CHUNK = 24 * 1024 * 1024
const MAX_CHANT = 6 * 1024 * 1024
const CHANT_TYPES = ['audio/wav', 'audio/x-wav', 'audio/webm', 'audio/mp4', 'audio/ogg', 'audio/mpeg']
const TURN_TTL = 12 * 3600                   // seconds a minted relay credential lives
const STUN = [{ urls: ['stun:stun.cloudflare.com:3478', 'stun:stun.l.google.com:19302'] }]

function cors(request) {
  const origin = request.headers.get('Origin') || ''
  const ok = /^https:\/\/(www\.)?devashaa\.com$/.test(origin) || /^http:\/\/localhost:\d+$/.test(origin)
  return ok
    ? {
        'Access-Control-Allow-Origin': origin,
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type,X-Auth,X-User,X-Refs',
        'Access-Control-Max-Age': '86400',
        Vary: 'Origin',
      }
    : {}
}
const json = (body, status, request) =>
  new Response(JSON.stringify(body), {
    status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', ...cors(request) },
  })
const clip = (v, n) => String(v ?? '').trim().slice(0, n)
const hex = (n) => [...crypto.getRandomValues(new Uint8Array(n))].map((x) => x.toString(16).padStart(2, '0')).join('')
const rid = () => hex(16)
const newPid = () => hex(8)
function tsEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string' || a.length !== b.length) return false
  let d = 0
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i)
  return d === 0
}

let ready = false
async function ensure(db) {
  if (ready) return
  await db.exec('CREATE TABLE IF NOT EXISTS pooja_roles (userid TEXT PRIMARY KEY, role TEXT NOT NULL, created_at INTEGER NOT NULL)')
  await db.exec('CREATE TABLE IF NOT EXISTS pooja_priests (userid TEXT PRIMARY KEY, pid TEXT, voice TEXT, name TEXT NOT NULL, city TEXT, country TEXT, languages TEXT, traditions TEXT, rituals TEXT, years INTEGER, bio TEXT, contact TEXT, status TEXT NOT NULL, vetted_by TEXT, created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL)')
  await db.exec('CREATE TABLE IF NOT EXISTS pooja_bookings (id TEXT PRIMARY KEY, ritual TEXT NOT NULL, starts_at TEXT NOT NULL, tz TEXT, priest TEXT, name TEXT NOT NULL, contact TEXT NOT NULL, city TEXT, family INTEGER, notes TEXT, lang TEXT, status TEXT NOT NULL, created_at INTEGER NOT NULL, updated_at INTEGER NOT NULL)')
  await db.exec('CREATE INDEX IF NOT EXISTS pooja_bookings_priest ON pooja_bookings(priest, status)')
  // `pid` (the public name of a pandit) and `voice` came later: a table made before them gets the columns here.
  for (const col of ['pid', 'voice']) {
    try { await db.exec(`ALTER TABLE pooja_priests ADD COLUMN ${col} TEXT`) } catch { /* the column is already there */ }
  }
  const bare = (await db.prepare('SELECT userid FROM pooja_priests WHERE pid IS NULL').all()).results || []
  for (const r of bare) await db.prepare('UPDATE pooja_priests SET pid = ? WHERE userid = ?').bind(newPid(), r.userid).run()
  await db.exec('CREATE UNIQUE INDEX IF NOT EXISTS pooja_priests_pid ON pooja_priests(pid)')
  ready = true
}

const PUBLIC_PRIEST = 'pid AS id, name, voice, city, country, languages, traditions, rituals, years, bio'
const publicBooking = (b, priest, rec) => ({
  id: b.id, ritual: b.ritual, starts_at: b.starts_at, tz: b.tz, status: b.status, city: b.city,
  family: b.family, name: b.name, lang: b.lang, notes: b.notes,
  priest: priest ? { id: priest.pid, name: priest.name } : null,
  recording: rec,
})

async function recInfo(env, id) {
  if (!env.REC) return { available: false, chunks: 0, bytes: 0, storage: false }
  let chunks = 0, bytes = 0, cursor
  do {
    const l = await env.REC.list({ prefix: `rec/${id}/`, cursor })
    for (const o of l.objects) { chunks += 1; bytes += o.size }
    cursor = l.truncated ? l.cursor : undefined
  } while (cursor)
  return { available: chunks > 0, chunks, bytes, storage: true }
}

/**
 * The ICE servers for a room: STUN always, and a TURN relay when the Worker
 * holds a Cloudflare Realtime TURN key. The relay credential is short-lived and
 * minted server-side — the key itself never reaches a browser. Port 53 URLs are
 * dropped: browsers block that port and the candidate only times out.
 */
export async function mintIce(env, f = fetch) {
  const base = { iceServers: STUN, turn: false }
  const id = env && env.TURN_KEY_ID, token = env && env.TURN_KEY_API_TOKEN
  if (!id || !token) return base
  try {
    const r = await f(`https://rtc.live.cloudflare.com/v1/turn/keys/${id}/credentials/generate-ice-servers`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ ttl: TURN_TTL }),
    })
    if (!r.ok) return { ...base, reason: `the relay answered ${r.status}` }
    const j = await r.json()
    const servers = (Array.isArray(j.iceServers) ? j.iceServers : [])
      .map((s) => ({ ...s, urls: [].concat(s.urls || []).filter((u) => typeof u === 'string' && !/:53(\?|$)/.test(u)) }))
      .filter((s) => s.urls.length)
    const turn = servers.some((s) => s.username && s.credential && s.urls.some((u) => /^turns?:/.test(u)))
    return turn ? { iceServers: servers, turn: true } : { ...base, reason: 'the relay gave no TURN server' }
  } catch {
    return { ...base, reason: 'the relay could not be reached' }
  }
}

/**
 * A pandit has deleted his account: take him out of the Pūjā service too. His
 * roster entry and any role go; his voice recordings are removed; a booking he
 * had taken and not yet led goes back to the families' queue for another
 * pandit, and one already completed keeps its record without his name.
 */
export async function forgetPandit(env, userid) {
  const db = env.DB
  if (!db) return
  await ensure(db)
  const me = await db.prepare('SELECT pid FROM pooja_priests WHERE userid = ?').bind(userid).first()
  await db.batch([
    db.prepare("UPDATE pooja_bookings SET priest = NULL, status = 'requested', updated_at = ? WHERE priest = ? AND status IN ('requested', 'confirmed')").bind(Date.now(), userid),
    db.prepare('UPDATE pooja_bookings SET priest = NULL WHERE priest = ?').bind(userid),
    db.prepare('DELETE FROM pooja_priests WHERE userid = ?').bind(userid),
    db.prepare('DELETE FROM pooja_roles WHERE userid = ?').bind(userid),
  ])
  if (!me?.pid || !env.REC) return
  let cursor
  do {
    const l = await env.REC.list({ prefix: 'chant/', cursor })
    const mine = l.objects.map((o) => o.key).filter((k) => k.endsWith(`/${me.pid}`))
    if (mine.length) await env.REC.delete(mine)
    cursor = l.truncated ? l.cursor : undefined
  } while (cursor)
}

export async function handlePooja(request, env, ctx, authorise) {
  const url = new URL(request.url)
  const seg = url.pathname.split('/').filter(Boolean)        // api, pooja, ...
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: cors(request) })

  // --- where the visitor roughly is, so the calendar opens on their own city ---
  // Cloudflare's edge already knows the city an address resolves to. It is read
  // here, sent back to the same visitor, and stored nowhere.
  if (seg[2] === 'where' && request.method === 'GET') {
    const cf = request.cf || {}
    const lat = parseFloat(cf.latitude), lon = parseFloat(cf.longitude)
    if (!cf.city || !Number.isFinite(lat) || !Number.isFinite(lon)) return json({}, 200, request)
    return json({ name: [cf.city, cf.region, cf.country].filter(Boolean).join(', '), latitude: lat, longitude: lon, timezone: cf.timezone || null }, 200, request)
  }

  const db = env.DB
  if (!db) return json({ error: 'storage is not configured' }, 503, request)
  await ensure(db)

  // --- the live room: only a real, uncancelled booking has one -----------------
  if (seg[2] === 'room' && (seg[4] === 'ws' || seg[4] === 'ice')) {
    if (!HEX32.test(seg[3] || '')) return json({ error: 'bad room' }, 400, request)
    if (!env.ROOMS) return json({ error: 'rooms are not configured' }, 503, request)
    const bk = await db.prepare('SELECT status FROM pooja_bookings WHERE id = ?').bind(seg[3]).first()
    if (!bk || bk.status === 'cancelled') return json({ error: 'There is no such room.' }, 404, request)
    const room = env.ROOMS.get(env.ROOMS.idFromName(seg[3]))
    if (seg[4] === 'ws') return room.fetch(request)        // hand the socket to the room's Durable Object
    if (request.method !== 'GET') return json({ error: 'not found' }, 404, request)
    const r = await room.fetch(new Request('https://room/ice'))
    return json(await r.json(), 200, request)
  }

  const userid = (request.headers.get('X-User') || '').toLowerCase().trim()
  const authed = USERID.test(userid) ? await authorise(db, userid, request) : false
  const body = ['POST', 'PUT'].includes(request.method) && seg[2] !== 'rec' && seg[2] !== 'chant'
    ? await request.json().catch(() => null) : null
  const roleOf = async (id) => (await db.prepare('SELECT role FROM pooja_roles WHERE userid = ?').bind(id).first())?.role || null
  const priestOf = async (id) => db.prepare('SELECT * FROM pooja_priests WHERE userid = ?').bind(id).first()
  const need = () => json({ error: 'sign in first' }, 401, request)

  // --- the roster -----------------------------------------------------------
  if (seg[2] === 'priests' && seg.length === 3 && request.method === 'GET') {
    const { results } = await db.prepare(`SELECT ${PUBLIC_PRIEST} FROM pooja_priests WHERE status = 'approved' ORDER BY name`).all()
    return json({ priests: results || [] }, 200, request)
  }
  if (seg[2] === 'priests' && seg[3] === 'apply' && request.method === 'POST') {
    if (!authed) return need()
    const name = clip(body?.name, 80)
    if (name.length < 2) return json({ error: 'A name is needed.' }, 400, request)
    const now = Date.now()
    const cur = await priestOf(userid)
    const status = cur?.status === 'approved' ? 'approved' : 'pending'
    const voice = body?.voice === 'f' ? 'f' : body?.voice === 'm' ? 'm' : ''
    await db.prepare(
      'INSERT INTO pooja_priests (userid, pid, voice, name, city, country, languages, traditions, rituals, years, bio, contact, status, vetted_by, created_at, updated_at) '
      + 'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(userid) DO UPDATE SET voice=excluded.voice, name=excluded.name, city=excluded.city, country=excluded.country, '
      + 'languages=excluded.languages, traditions=excluded.traditions, rituals=excluded.rituals, years=excluded.years, bio=excluded.bio, '
      + 'contact=excluded.contact, status=excluded.status, updated_at=excluded.updated_at',
    ).bind(userid, cur?.pid || newPid(), voice, name, clip(body?.city, 80), clip(body?.country, 60), clip(body?.languages, 160), clip(body?.traditions, 160),
           clip(body?.rituals, 400), Math.max(0, Math.min(90, parseInt(body?.years, 10) || 0)), clip(body?.bio, 1200),
           clip(body?.contact, 120), status, cur?.vetted_by || null, cur?.created_at || now, now).run()
    return json({ ok: true, status }, 200, request)
  }
  if (seg[2] === 'priests' && seg[4] === 'vet' && request.method === 'POST') {
    if (!authed) return need()
    const me = await priestOf(userid)
    const admin = (await roleOf(userid)) === 'admin'
    if (!admin && me?.status !== 'approved') return json({ error: 'Only an approved pandit or an admin can vet.' }, 403, request)
    const decision = body?.decision === 'approve' ? 'approved' : body?.decision === 'reject' ? 'rejected' : null
    if (!PID.test(seg[3] || '') || !decision) return json({ error: 'expected {decision: approve|reject}' }, 400, request)
    if (me?.pid === seg[3] && !admin) return json({ error: 'You cannot vet yourself.' }, 403, request)
    const r = await db.prepare('UPDATE pooja_priests SET status = ?, vetted_by = ?, updated_at = ? WHERE pid = ?')
      .bind(decision, userid, Date.now(), seg[3]).run()
    return json({ ok: true, changed: r.meta?.changes || 0 }, 200, request)
  }

  // --- who am I --------------------------------------------------------------
  if (seg[2] === 'me' && request.method === 'GET') {
    if (!authed) return need()
    return json({ userid, role: await roleOf(userid), priest: await priestOf(userid) || null }, 200, request)
  }
  if (seg[2] === 'admin' && seg[3] === 'claim' && request.method === 'POST') {
    if (!authed) return need()
    const code = String(env.POOJA_ADMIN_CODE || '')
    if (!code || !tsEqual(String(body?.code || ''), code)) return json({ error: 'That code is not right.' }, 403, request)
    await db.prepare('INSERT INTO pooja_roles (userid, role, created_at) VALUES (?, ?, ?) ON CONFLICT(userid) DO UPDATE SET role = excluded.role')
      .bind(userid, 'admin', Date.now()).run()
    return json({ ok: true, role: 'admin' }, 200, request)
  }

  // --- the desk: what a pandit or an admin has to act on ----------------------
  if (seg[2] === 'desk' && request.method === 'GET') {
    if (!authed) return need()
    const me = await priestOf(userid)
    const admin = (await roleOf(userid)) === 'admin'
    if (!admin && me?.status !== 'approved') return json({ role: null, priest: me || null, applicants: [], bookings: [] }, 200, request)
    const applicants = (await db.prepare("SELECT pid AS id, name, voice, city, country, languages, traditions, rituals, years, bio, contact, created_at FROM pooja_priests WHERE status = 'pending' ORDER BY created_at").all()).results || []
    const rows = admin
      ? (await db.prepare('SELECT * FROM pooja_bookings ORDER BY starts_at DESC LIMIT 200').all()).results || []
      : (await db.prepare("SELECT * FROM pooja_bookings WHERE priest = ? OR (priest IS NULL AND status = 'requested') ORDER BY starts_at").bind(userid).all()).results || []
    const names = Object.fromEntries(((await db.prepare('SELECT userid, name FROM pooja_priests').all()).results || []).map((p) => [p.userid, p.name]))
    // A family's contact goes only to the pandit who has taken the booking, and to admins.
    const bookings = rows.map((b) => ({
      id: b.id, ritual: b.ritual, starts_at: b.starts_at, tz: b.tz, status: b.status, name: b.name, city: b.city,
      family: b.family, notes: b.notes, lang: b.lang,
      contact: admin || b.priest === userid ? b.contact : null,
      mine: b.priest === userid, priest_name: b.priest ? (names[b.priest] || '') : null,
    }))
    return json({ role: admin ? 'admin' : 'priest', priest: me || null, applicants, bookings }, 200, request)
  }

  // --- bookings ----------------------------------------------------------------
  if (seg[2] === 'bookings' && seg.length === 3 && request.method === 'POST') {
    const ritual = clip(body?.ritual, 60), starts = clip(body?.starts_at, 40)
    const self = body?.self === true          // a family keeping it on its own: no pandit, no contact
    const name = clip(body?.name, 80) || (self ? 'Family' : ''), contact = self ? '' : clip(body?.contact, 120)
    if (!ritual || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(starts)) return json({ error: 'A ritual, a date and a time are needed.' }, 400, request)
    if (!self && (name.length < 2 || contact.length < 5)) return json({ error: 'A name and a way to reach you are needed.' }, 400, request)
    let priest = null
    const want = self ? '' : clip(body?.priest, 40).toLowerCase()
    if (PID.test(want)) {
      const p = await db.prepare("SELECT userid FROM pooja_priests WHERE pid = ? AND status = 'approved'").bind(want).first()
      priest = p?.userid || null
    }
    const id = rid(), now = Date.now()
    await db.prepare('INSERT INTO pooja_bookings (id, ritual, starts_at, tz, priest, name, contact, city, family, notes, lang, status, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)')
      .bind(id, ritual, starts, clip(body?.tz, 60), priest, name, contact, clip(body?.city, 80),
            Math.max(1, Math.min(50, parseInt(body?.family, 10) || 1)), self ? '' : clip(body?.notes, 1200), clip(body?.lang, 20), self ? 'self' : 'requested', now, now).run()
    return json({ id }, 201, request)
  }
  if (seg[2] === 'bookings' && HEX32.test(seg[3] || '')) {
    const b = await db.prepare('SELECT * FROM pooja_bookings WHERE id = ?').bind(seg[3]).first()
    if (!b) return json({ error: 'not found' }, 404, request)
    if (seg.length === 4 && request.method === 'GET') {
      const out = publicBooking(b, b.priest ? await priestOf(b.priest) : null, await recInfo(env, b.id))
      out.mine = !!(authed && b.priest === userid)
      // the pandit who has taken it, and admins, also see how to reach the family
      if (authed && (b.priest === userid || (await roleOf(userid)) === 'admin')) out.contact = b.contact
      return json(out, 200, request)
    }
    if (request.method === 'POST' && seg[4] === 'cancel') {
      if (b.status === 'completed') return json({ error: 'It is already completed.' }, 409, request)
      await db.prepare("UPDATE pooja_bookings SET status = 'cancelled', updated_at = ? WHERE id = ?").bind(Date.now(), b.id).run()
      return json({ ok: true, status: 'cancelled' }, 200, request)
    }
    if (request.method === 'POST' && (seg[4] === 'accept' || seg[4] === 'complete')) {
      if (!authed) return need()
      const me = await priestOf(userid)
      const admin = (await roleOf(userid)) === 'admin'
      if (!admin && me?.status !== 'approved') return json({ error: 'Only an approved pandit can do that.' }, 403, request)
      if (seg[4] === 'accept') {
        if (b.priest && b.priest !== userid && !admin) return json({ error: 'Another pandit has this booking.' }, 409, request)
        if (b.status === 'cancelled') return json({ error: 'It was cancelled.' }, 409, request)
        if (b.status === 'self') return json({ error: 'This family is keeping the ceremony on its own.' }, 409, request)
        await db.prepare("UPDATE pooja_bookings SET priest = ?, status = 'confirmed', updated_at = ? WHERE id = ?")
          .bind(me?.status === 'approved' ? userid : (b.priest || userid), Date.now(), b.id).run()
        return json({ ok: true, status: 'confirmed' }, 200, request)
      }
      if (b.priest !== userid && !admin) return json({ error: 'This is not your booking.' }, 403, request)
      await db.prepare("UPDATE pooja_bookings SET status = 'completed', updated_at = ? WHERE id = ?").bind(Date.now(), b.id).run()
      return json({ ok: true, status: 'completed' }, 200, request)
    }
  }

  // --- recordings --------------------------------------------------------------
  if (seg[2] === 'rec' && HEX32.test(seg[3] || '')) {
    if (!env.REC) return json({ error: 'recording storage is not configured' }, 503, request)
    const id = seg[3]
    if (request.method === 'PUT' && /^\d{1,6}$/.test(seg[4] || '')) {
      if (!authed) return need()
      const b = await db.prepare('SELECT priest FROM pooja_bookings WHERE id = ?').bind(id).first()
      if (!b) return json({ error: 'not found' }, 404, request)
      if (b.priest !== userid && (await roleOf(userid)) !== 'admin') return json({ error: 'Only the pandit of this booking records it.' }, 403, request)
      const len = parseInt(request.headers.get('Content-Length') || '0', 10)
      if (!len || len > MAX_CHUNK) return json({ error: 'bad chunk size' }, 413, request)
      await env.REC.put(`rec/${id}/${String(seg[4]).padStart(6, '0')}.webm`, request.body, { httpMetadata: { contentType: 'video/webm' } })
      return json({ ok: true }, 200, request)
    }
    if (request.method === 'GET' && seg.length === 4) return json(await recInfo(env, id), 200, request)
    if (request.method === 'GET' && seg[4] === 'play') {
      const keys = []
      let cursor
      do {
        const l = await env.REC.list({ prefix: `rec/${id}/`, cursor })
        for (const o of l.objects) keys.push(o.key)
        cursor = l.truncated ? l.cursor : undefined
      } while (cursor)
      if (!keys.length) return json({ error: 'no recording yet' }, 404, request)
      keys.sort()
      const { readable, writable } = new TransformStream()
      ctx.waitUntil((async () => {
        try {
          for (const k of keys) {
            const o = await env.REC.get(k)
            if (o) await o.body.pipeTo(writable, { preventClose: true })
          }
          await writable.close()
        } catch { try { await writable.abort() } catch { /* the viewer went away */ } }
      })())
      return new Response(readable, { status: 200, headers: { 'Content-Type': 'video/webm', 'Cache-Control': 'private, no-store', ...cors(request) } })
    }
  }

  // --- the voice library: each pandit's own voice for each mantra and explanation ---
  if (seg[2] === 'chants' && request.method === 'GET') {
    const clips = {}
    if (env.REC) {
      // Who a recording is by, and in which voice, comes from the roster — so it is always current,
      // and a recording by someone no longer on the roster is not offered.
      const who = Object.fromEntries(((await db.prepare("SELECT pid, name, voice FROM pooja_priests WHERE status = 'approved'").all()).results || []).map((p) => [p.pid, p]))
      let cursor
      do {
        const l = await env.REC.list({ prefix: 'chant/', cursor })
        for (const o of l.objects) {
          const [, id, pid] = o.key.split('/')
          const p = who[pid]
          if (!p || !CLIP_ID.test(id || '')) continue
          ;(clips[id] = clips[id] || []).push({ id: pid, by: p.name, voice: p.voice || '', at: o.uploaded ? new Date(o.uploaded).getTime() : 0 })
        }
        cursor = l.truncated ? l.cursor : undefined
      } while (cursor)
      for (const k of Object.keys(clips)) clips[k].sort((a, b) => a.at - b.at)     // the first to record a clip is heard by default
    }
    return json({ clips }, 200, request)
  }
  if (seg[2] === 'chant' && CLIP_ID.test(seg[3] || '')) {
    if (!env.REC) return json({ error: 'recording storage is not configured' }, 503, request)
    const id = seg[3]
    if (request.method === 'GET' && PID.test(seg[4] || '')) {
      const o = await env.REC.get(`chant/${id}/${seg[4]}`)
      if (!o) return json({ error: 'not recorded yet' }, 404, request)
      // The client adds ?v=<when it was recorded>, so a re-recording is a new URL and this can be cached for long.
      return new Response(o.body, { status: 200, headers: { 'Content-Type': o.httpMetadata?.contentType || 'audio/wav', 'Content-Length': String(o.size), 'Cache-Control': 'public, max-age=86400', ...cors(request) } })
    }
    if (request.method !== 'PUT' && request.method !== 'DELETE') return json({ error: 'not found' }, 404, request)
    if (!authed) return need()
    const me = await priestOf(userid)
    const admin = (await roleOf(userid)) === 'admin'
    if (request.method === 'DELETE') {
      if (!PID.test(seg[4] || '')) return json({ error: 'not found' }, 404, request)
      const own = me?.status === 'approved' && me.pid === seg[4]
      if (!own && !admin) return json({ error: 'Only the pandit who recorded it, or an admin, removes a recording.' }, 403, request)
      await env.REC.delete(`chant/${id}/${seg[4]}`)
      return json({ ok: true }, 200, request)
    }
    if (seg.length !== 4) return json({ error: 'not found' }, 404, request)
    if (me?.status !== 'approved' || !me.pid) return json({ error: 'Only a pandit on the roster records for the library.' }, 403, request)
    const len = parseInt(request.headers.get('Content-Length') || '0', 10)
    if (!len || len > MAX_CHANT) return json({ error: 'The recording is empty or too long.' }, 413, request)
    const type = (request.headers.get('Content-Type') || '').split(';')[0].trim().toLowerCase()
    await env.REC.put(`chant/${id}/${me.pid}`, request.body, { httpMetadata: { contentType: CHANT_TYPES.includes(type) ? type : 'audio/wav' } })
    return json({ ok: true, id: me.pid }, 200, request)
  }

  return json({ error: 'not found' }, 404, request)
}

/**
 * One live room. It holds the sockets of everyone in the room (the pandit and
 * each family location) and relays the WebRTC handshake between them: who is
 * here, offers, answers, ICE candidates, the step the ceremony is on. It never
 * sees media. It also keeps the room's relay credential, so a room mints one
 * and every home in it shares it, however often they reconnect.
 * Hibernatable WebSockets, so an idle room costs nothing.
 */
export class PoojaRoom {
  constructor(state, env) { this.state = state; this.env = env }

  async ice() {
    const now = Date.now()
    const cur = await this.state.storage.get('ice')
    // Hand out a credential only while at least half its life is left — longer than any ceremony.
    if (cur && cur.exp - now > TURN_TTL * 500) return cur.body
    const body = await mintIce(this.env)
    if (body.turn) await this.state.storage.put('ice', { body, exp: now + TURN_TTL * 1000 })
    return body
  }

  async fetch(request) {
    const url = new URL(request.url)
    if (url.pathname === '/ice') return Response.json(await this.ice())
    if (request.headers.get('Upgrade') !== 'websocket') return new Response('expected a websocket', { status: 426 })
    const peer = clip(url.searchParams.get('peer'), 40)
    if (!/^[a-z0-9]{8,40}$/.test(peer)) return new Response('bad peer', { status: 400 })
    if (this.state.getWebSockets().length >= 12) return new Response('the room is full', { status: 409 })
    const me = { peer, name: clip(url.searchParams.get('name'), 60) || 'Guest', role: url.searchParams.get('role') === 'priest' ? 'priest' : 'family' }
    const pair = new WebSocketPair()
    const client = pair[0], server = pair[1]
    this.state.acceptWebSocket(server, [peer])
    server.serializeAttachment(me)
    const others = this.state.getWebSockets().filter((ws) => ws !== server).map((ws) => ws.deserializeAttachment()).filter(Boolean)
    server.send(JSON.stringify({ t: 'hello', you: me, peers: others }))
    this.broadcast({ t: 'join', peer: me }, server)
    return new Response(null, { status: 101, webSocket: client })
  }

  webSocketMessage(ws, raw) {
    let m
    try { m = JSON.parse(typeof raw === 'string' ? raw : new TextDecoder().decode(raw)) } catch { return }
    const from = ws.deserializeAttachment()
    if (!from || !m || typeof m.t !== 'string' || raw.length > 64 * 1024) return
    if (m.t === 'ping') { try { ws.send('{"t":"pong"}') } catch { /* gone */ } return }
    const out = JSON.stringify({ ...m, from: from.peer })
    if (m.to) { for (const o of this.state.getWebSockets(String(m.to))) { try { o.send(out) } catch { /* gone */ } } }
    else this.broadcast({ ...m, from: from.peer }, ws)
  }

  webSocketClose(ws) { this.left(ws) }
  webSocketError(ws) { this.left(ws) }
  left(ws) {
    const a = ws.deserializeAttachment()
    try { ws.close() } catch { /* already closed */ }
    if (a) this.broadcast({ t: 'leave', peer: a.peer }, ws)
  }

  broadcast(obj, except) {
    const s = JSON.stringify(obj)
    for (const ws of this.state.getWebSockets()) { if (ws !== except) { try { ws.send(s) } catch { /* gone */ } } }
  }
}
