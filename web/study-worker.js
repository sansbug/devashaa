/**
 * /api/study — the owner's study view, gated here and answered by the Python API.
 *
 * The page itself (/study) is part of the public bundle, but it shows nothing
 * without this route. This route answers only a signed-in account whose role in
 * `pooja_roles` is "admin" (the same role the Pūjā desk uses). It then forwards
 * the request to the Render API with the shared secret STUDY_KEY, which the API
 * requires (api/app.py `_study_allowed`). Nothing about the request is stored.
 *
 * Configuration (the owner's step):
 *   wrangler secret put STUDY_KEY          (the same value as Render's STUDY_KEY)
 *   optional var STUDY_API                 (default https://devashaa-api.onrender.com)
 */

const USERID = /^(?:[a-z0-9][a-z0-9._-]{2,31}|[a-z0-9._%+-]{1,64}@[a-z0-9-]+(?:\.[a-z0-9-]+)*\.[a-z]{2,24})$/

const reply = (body, status) => new Response(JSON.stringify(body), {
  status,
  headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex' },
})

export async function handleStudy(request, env, authorise) {
  const url = new URL(request.url)
  if (!['GET', 'POST'].includes(request.method)) return reply({ error: 'not found' }, 404)
  if (!['/api/study', '/api/study/gaps', '/api/study/whoami'].includes(url.pathname)) return reply({ error: 'not found' }, 404)
  const db = env.DB
  if (!db) return reply({ error: 'account storage is not configured' }, 503)

  const userid = (request.headers.get('X-User') || '').toLowerCase().trim()
  const authed = USERID.test(userid) ? await authorise(db, userid, request) : false
  if (!authed) return reply({ error: 'sign in first' }, 401)
  const role = (await db.prepare('SELECT role FROM pooja_roles WHERE userid = ?').bind(userid).first())?.role
  if (role !== 'admin') return reply({ error: 'This page is for the site owner.' }, 403)
  if (url.pathname === '/api/study/whoami') return reply({ ok: true, role }, 200)

  if (!env.STUDY_KEY) return reply({ error: 'The study API key is not configured on the Worker.' }, 503)
  const base = env.STUDY_API || 'https://devashaa-api.onrender.com'
  const init = { method: request.method, headers: { 'X-Study-Key': env.STUDY_KEY } }
  if (request.method === 'POST') {
    init.headers['Content-Type'] = 'application/json'
    init.body = await request.text()
  }
  const r = await fetch(base + url.pathname, init)
  return new Response(r.body, {
    status: r.status,
    headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store', 'X-Robots-Tag': 'noindex' },
  })
}
