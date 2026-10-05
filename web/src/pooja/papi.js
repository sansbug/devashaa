/**
 * Devashaa Pūjā — the client for the Worker's /api/pooja and the session a
 * pandit or admin signs in with.
 *
 * Sign-in reuses the site's accounts (see ../account.js): the password never
 * leaves the browser; what the Worker checks is a verifier derived from it.
 * The session lives in memory only — a reload signs you out, the same stance
 * the chart store takes. A family booking a pūjā needs no account at all: the
 * booking's id, which only they hold, is their key to it and to the room.
 */
import { API_BASE, deriveAccount, register, login } from '../account.js'
import { API } from '../config.js'

const BASE = `${API_BASE}/api/pooja`
let session = null           // { userid, authId }
const listeners = new Set()
const emit = () => listeners.forEach((f) => f(session))

export const getSession = () => session
export const onSession = (f) => { listeners.add(f); return () => listeners.delete(f) }
export function signOut() { session = null; emit() }
export async function signIn(userid, password, create) {
  const a = await deriveAccount(userid, password)
  if (create) await register(a.userid, a.authId)
  else await login(a.userid, a.authId)
  session = { userid: a.userid, authId: a.authId }
  emit()
  return session
}

async function call(path, { method = 'GET', body, blob, type } = {}) {
  const headers = {}
  if (session) { headers['X-User'] = session.userid; headers['X-Auth'] = session.authId }
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  if (blob) headers['Content-Type'] = type || 'video/webm'
  const r = await fetch(BASE + path, { method, headers, body: blob || (body !== undefined ? JSON.stringify(body) : undefined) })
  const j = await r.json().catch(() => ({}))
  if (!r.ok) throw new Error(j.error || `HTTP ${r.status}`)
  return j
}

export const api = {
  priests: () => call('/priests'),
  apply: (profile) => call('/priests/apply', { method: 'POST', body: profile }),
  vet: (userid, decision) => call(`/priests/${encodeURIComponent(userid)}/vet`, { method: 'POST', body: { decision } }),
  me: () => call('/me'),
  claim: (code) => call('/admin/claim', { method: 'POST', body: { code } }),
  desk: () => call('/desk'),
  book: (b) => call('/bookings', { method: 'POST', body: b }),
  booking: (id) => call(`/bookings/${id}`),
  accept: (id) => call(`/bookings/${id}/accept`, { method: 'POST', body: {} }),
  complete: (id) => call(`/bookings/${id}/complete`, { method: 'POST', body: {} }),
  cancel: (id) => call(`/bookings/${id}/cancel`, { method: 'POST', body: {} }),
  recInfo: (id) => call(`/rec/${id}`),
  putChunk: (id, seq, blob) => call(`/rec/${id}/${seq}`, { method: 'PUT', blob }),
  playUrl: (id) => `${BASE}/rec/${id}/play`,
  /** The chant library: which mantras a pandit has recorded, and their audio. */
  chants: () => call('/chants').then((j) => j.chants || {}).catch(() => ({})),
  chantUrl: (step) => `${BASE}/chant/${step}`,
  putChant: (step, blob) => call(`/chant/${step}`, { method: 'PUT', blob, type: (blob.type || 'audio/webm').split(';')[0] }),
  delChant: (step) => call(`/chant/${step}`, { method: 'DELETE' }),
  wsUrl: (id, peer, name, role) => {
    const origin = API_BASE || (typeof location !== 'undefined' ? location.origin : 'https://devashaa.com')
    return `${origin.replace(/^http/, 'ws')}/api/pooja/room/${id}/ws?peer=${peer}&name=${encodeURIComponent(name)}&role=${role}`
  },
  /** A month of the religious calendar for a place — the pañcāṅga engine, no birth chart. */
  observances: async (place, year, month) => {
    const r = await fetch(`${API}/api/panchang/observances`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ latitude: place.latitude, longitude: place.longitude, timezone: place.timezone, year, month }),
    })
    const j = await r.json().catch(() => ({}))
    if (!r.ok) throw new Error(j.error || `HTTP ${r.status}`)
    return j
  },
  /** The day's time-windows at a place for a ceremony — the muhūrta engine, no birth chart. */
  muhurta: async (place, date, ritual) => {
    const r = await fetch(`${API}/api/muhurta`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ latitude: place.latitude, longitude: place.longitude, timezone: place.timezone, date, ritual }),
    })
    const j = await r.json().catch(() => ({}))
    if (!r.ok) throw new Error(j.error || `HTTP ${r.status}`)
    return j
  },
  places: async (q) => {
    const r = await fetch(`${API}/api/places?q=${encodeURIComponent(q)}`)
    const j = await r.json().catch(() => ({}))
    return j.places || []
  },
}

export const DEFAULT_PLACE = { name: 'New Delhi, Delhi, India', latitude: 28.6139, longitude: 77.209, timezone: 'Asia/Kolkata' }
export const loadPlace = () => { try { return JSON.parse(localStorage.getItem('pooja.place')) || DEFAULT_PLACE } catch { return DEFAULT_PLACE } }
export const savePlace = (p) => { try { localStorage.setItem('pooja.place', JSON.stringify(p)) } catch { /* private mode */ } }
