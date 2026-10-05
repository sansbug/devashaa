/**
 * Share a chart by link — without the server, or the link's path, ever
 * holding what is shared in the clear.
 *
 *   link = https://devashaa.com/c/<id>#<key>
 *
 * What is shared is encrypted here with a random AES-GCM key; the ciphertext
 * goes to the Worker under a random id; the KEY travels only in the URL
 * fragment, which browsers never send to any server and which never appears
 * in a log. Whoever holds the whole link can open it; the server holds a blob
 * it cannot read; the path alone (what analytics and referrer headers see)
 * says nothing.
 *
 * Two kinds of share (see shareCodec.js): the finished chart WITHOUT the birth
 * details — the default — or the birth details themselves, when the sender
 * wants the other person to have the whole site for that chart.
 *
 * A birth moment and place is close to a unique identifier for a person —
 * the same reason the account store is designed the way it is.
 */
import { API_BASE } from './account.js'
import { detailsPayload, snapshotPayload, seal, unseal } from './shareCodec.js'

export const SHARE_ID_RE = /^\/c\/([0-9a-f]{32})$/

/**
 * Make the link. `details: true` shares the birth details (name, date, time,
 * place); otherwise only the finished chart is shared and the birth details
 * never leave this browser.
 */
export async function makeShareLink({ name, date, time, place, chart, lang }, { details = false } = {}) {
  const { blob, key } = await seal(details ? detailsPayload({ name, date, time, place }) : snapshotPayload({ name, lang, chart }))
  const r = await fetch(`${API_BASE}/api/share`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ blob }),
  })
  const j = await r.json().catch(() => ({}))
  if (!r.ok || !j.id) throw new Error(j.error || `HTTP ${r.status}`)
  const origin = typeof location !== 'undefined' ? location.origin : 'https://devashaa.com'
  return `${origin}/c/${j.id}#${key}`
}

/** → the payload: `{ kind: 'snapshot', name, chart }`, or the birth details `{ name, date, time, place }`. */
export async function openShare(id, keyB64) {
  const r = await fetch(`${API_BASE}/api/share/${id}`)
  const j = await r.json().catch(() => ({}))
  if (!r.ok || !j.blob) throw new Error(j.error || `HTTP ${r.status}`)
  return unseal(j.blob, keyB64)
}
