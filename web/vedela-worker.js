/**
 * /vedela/* — Vedela (Kitchen, Shop, and the owner's Wellness), shown as a tab of devashaa.com.
 *
 * Vedela is not part of this site's code. It is its own two small apps on their own server
 * (repo sansbug/vidveda: `shop/` is the front door, `api/` + `web/` are Wellness and Kitchen),
 * and that server already serves everything under the path /vedela/. This passes a request
 * for /vedela/... straight through to it and hands the answer back, so to a visitor it is
 * one more section of devashaa.com.
 *
 * Nothing is decided here. Who may see Wellness (the owner's account only, for now) is
 * enforced on Vedela's own server, which is also reachable at its own address; a rule kept
 * only in this file would not hold there.
 *
 * Two things this file must keep true:
 *   - devashaa's own account headers (X-Auth, X-User) are never sent on: Vedela's sign-in is
 *     separate and has no business seeing them.
 *   - public/sw.js leaves /vedela/ alone (it does): a service-worker cache is keyed by address,
 *     not by who is signed in, and it would also save a Vedela page as this site's home page.
 *
 * Configuration: var VEDELA_ORIGIN in wrangler.jsonc (where Vedela's server is).
 */

const DOWN = '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
  + '<title>Vedela</title><body style="font:16px/1.6 system-ui,sans-serif;color:#2c4630;background:#fafaf4;padding:48px">'
  + '<p>Vedela is not reachable right now. Please try again in a moment.</p>'
  + '<p><a href="/" style="color:#2c4630">Back to devashaa.com</a></p>'

export async function handleVedela(request, env) {
  const url = new URL(request.url)
  // Vedela's pages ask for their files relative to this folder, so the bare name gets its slash.
  if (url.pathname === '/vedela') return Response.redirect(`${url.origin}/vedela/${url.search}`, 302)

  const origin = String(env.VEDELA_ORIGIN || '').replace(/\/+$/, '')
  if (!origin) return new Response(DOWN, { status: 503, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' } })

  const headers = new Headers(request.headers)
  headers.delete('X-Auth')
  headers.delete('X-User')
  headers.set('X-Forwarded-Host', url.host)
  headers.set('X-Forwarded-Proto', 'https')
  const init = { method: request.method, headers, redirect: 'manual' }
  if (!['GET', 'HEAD'].includes(request.method)) init.body = request.body

  let r
  try {
    r = await fetch(origin + url.pathname + url.search, init)
  } catch {
    return new Response(DOWN, { status: 502, headers: { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store' } })
  }
  const out = new Response(r.body, r)
  // A redirect that names Vedela's own server would take the visitor off this site: keep the path.
  const loc = out.headers.get('Location')
  if (loc && loc.startsWith(origin + '/')) out.headers.set('Location', loc.slice(origin.length))
  return out
}
