/**
 * devashaa.com — static site + the passphrase-sync blob store.
 *
 * This Worker holds encrypted profile blobs and CANNOT READ THEM. That is
 * architectural, not a policy: the AES key is derived on the client from a
 * passphrase this server never receives, and the key it stores under is a
 * separate HKDF output from the same passphrase. Holding every key in this
 * namespace tells you nothing about any plaintext.
 *
 * So there is no user table, no email, no account, and nothing here that
 * identifies a person. A blob is a 64-hex name and a base64 string.
 *
 * WHY THE STORE LIVES HERE AND NOT ON THE PYTHON BACKEND
 * ------------------------------------------------------
 * The chart API runs on Render's free plan, whose filesystem is ephemeral —
 * anything written there is destroyed on the next deploy. KV is persistent and
 * on the same origin as the site, so sync needs no CORS in production and adds
 * no cost.
 */

const ID_RE = /^[0-9a-f]{64}$/          // the client sends a SHA-256-sized hex id
const MAX_BYTES = 256 * 1024            // a generous ceiling on one person's charts

/** Same-origin in production; localhost is allowed so `npm run dev` can sync. */
function corsHeaders(request) {
  const origin = request.headers.get('Origin') || ''
  const ok = /^https:\/\/(www\.)?devashaa\.com$/.test(origin)
    || /^http:\/\/localhost:\d+$/.test(origin)
  return ok
    ? {
        'Access-Control-Allow-Origin': origin,
        'Access-Control-Allow-Methods': 'GET,PUT,DELETE,OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
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
      // A blob is user data, not a cacheable asset — and an intermediary
      // caching it would outlive the user's own delete.
      'Cache-Control': 'no-store',
      ...corsHeaders(request),
    },
  })

export default {
  async fetch(request, env) {
    const url = new URL(request.url)

    if (!url.pathname.startsWith('/api/sync/')) {
      // Everything else is the React app.
      return env.ASSETS.fetch(request)
    }

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(request) })
    }

    const id = url.pathname.slice('/api/sync/'.length)
    // Reject anything that is not exactly a derived id. This also means the
    // route can never be walked, listed or path-traversed.
    if (!ID_RE.test(id)) {
      return json({ error: 'bad sync id' }, 400, request)
    }
    if (!env.SYNC) {
      return json({ error: 'sync storage is not configured' }, 503, request)
    }

    if (request.method === 'GET') {
      const blob = await env.SYNC.get(id)
      if (blob === null) return json({ error: 'not found' }, 404, request)
      return json({ blob }, 200, request)
    }

    if (request.method === 'PUT') {
      let body
      try {
        body = await request.json()
      } catch {
        return json({ error: 'expected JSON' }, 400, request)
      }
      const blob = body?.blob
      if (typeof blob !== 'string' || !blob) {
        return json({ error: 'expected {blob: string}' }, 400, request)
      }
      if (blob.length > MAX_BYTES) {
        return json({ error: 'blob too large' }, 413, request)
      }
      // Opaque in, opaque out. This Worker never parses, inspects or indexes
      // the value — it could not decrypt it if it tried.
      await env.SYNC.put(id, blob)
      return json({ ok: true }, 200, request)
    }

    if (request.method === 'DELETE') {
      // Deletion must work without an account, because there is no account to
      // authenticate. Knowing the id means knowing the passphrase.
      await env.SYNC.delete(id)
      return json({ ok: true }, 200, request)
    }

    return json({ error: 'method not allowed' }, 405, request)
  },
}
