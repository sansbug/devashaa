/**
 * Share a chart by link — without the server, or the link's path, ever
 * holding the birth details in the clear.
 *
 *   link = https://devashaa.com/c/<id>#<key>
 *
 * The chart's details (name, date, time, place) are encrypted here with a
 * random AES-GCM key; the ciphertext goes to the Worker under a random id;
 * the KEY travels only in the URL fragment, which browsers never send to any
 * server and which never appears in a log. Whoever holds the whole link can
 * open the chart; the server holds a blob it cannot read; the path alone
 * (what analytics and referrer headers see) says nothing.
 *
 * A birth moment and place is close to a unique identifier for a person —
 * the same reason the account store is designed the way it is.
 */
import { API_BASE } from './account.js'

const enc = new TextEncoder()
const dec = new TextDecoder()
const b64u = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
const unb64u = (s) => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((s.length + 3) % 4)), (c) => c.charCodeAt(0))

export const SHARE_ID_RE = /^\/c\/([0-9a-f]{32})$/

/** The payload a share carries: exactly what the form needs to cast again. */
export function sharePayload({ name, date, time, place }) {
  return {
    v: 1, name: name || '', date, time,
    place: { name: place.name, latitude: place.latitude, longitude: place.longitude, timezone: place.timezone },
  }
}

export async function makeShareLink(profile) {
  const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt'])
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, enc.encode(JSON.stringify(sharePayload(profile))))
  const blob = b64u(iv) + '.' + b64u(ct)
  const r = await fetch(`${API_BASE}/api/share`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ blob }),
  })
  const j = await r.json().catch(() => ({}))
  if (!r.ok || !j.id) throw new Error(j.error || `HTTP ${r.status}`)
  const raw = await crypto.subtle.exportKey('raw', key)
  const origin = typeof location !== 'undefined' ? location.origin : 'https://devashaa.com'
  return `${origin}/c/${j.id}#${b64u(raw)}`
}

export async function openShare(id, keyB64) {
  const r = await fetch(`${API_BASE}/api/share/${id}`)
  const j = await r.json().catch(() => ({}))
  if (!r.ok || !j.blob) throw new Error(j.error || `HTTP ${r.status}`)
  const [ivS, ctS] = String(j.blob).split('.')
  const key = await crypto.subtle.importKey('raw', unb64u(keyB64), { name: 'AES-GCM' }, false, ['decrypt'])
  const pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: unb64u(ivS) }, key, unb64u(ctS))
  const p = JSON.parse(dec.decode(pt))
  if (!p || !p.date || !p.time || !p.place) throw new Error('bad share')
  return p
}
