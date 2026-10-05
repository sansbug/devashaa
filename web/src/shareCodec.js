/**
 * What a share link carries, and how it is packed. No imports, so it can be
 * tested on its own.
 *
 * TWO KINDS OF SHARE
 *   details  (v1) — the four things the form needs to cast the chart again:
 *                   name, date, time, place. The recipient gets the whole
 *                   site for that chart, and can read the birth details.
 *   snapshot (v2) — the FINISHED CHART and nothing it was cast from. The
 *                   recipient sees the chart, the strengths, the yogas and the
 *                   readings; the date, the clock time and the place of birth
 *                   are not in the link at all, so there is nothing to find.
 *                   Timelines (daśā, projection, varṣaphala, transits) are
 *                   computed from the birth details, so they are not sent.
 *
 * HONESTY ABOUT A SNAPSHOT. A chart is a picture of the sky at one moment:
 * someone who studies the positions closely can work the date back out of
 * them, and with effort the hour. What a snapshot withholds is everything
 * that would TELL them — the date, the time, the place, the time zone, the
 * Julian day, the ayanāṁśa to eight places, and every dated period.
 */

/** The top-level parts of a cast chart that describe the chart and not the birth. Anything new is left out until it is listed here. */
export const SNAPSHOT_KEYS = [
  'analysis', 'ayanamsa', 'bhava_system', 'gandanta', 'grahas', 'lagna_longitude', 'lagna_nakshatra',
  'lagna_rasi', 'lagna_vargas', 'landmarks', 'motion', 'navamsa', 'shadbala', 'warnings', 'zodiac',
]
/** Never carried, however deep they sit. Only names that can mean nothing else: a graha has a `longitude` and a
 *  `latitude` too (on the ecliptic), and a cited text has a `date` — those must stay. */
export const BIRTH_KEYS = new Set([
  'jd_ut', 'julian_day', 'utc', 'local_time', 'timezone', 'utc_offset_hours',
  'birth', 'birth_date', 'birth_time', 'birthplace', 'sunrise', 'sunset', 'ayanamsa_value', 'dasha',
])

const strip = (v) => {
  if (Array.isArray(v)) return v.map(strip)
  if (v && typeof v === 'object') {
    const out = {}
    for (const [k, x] of Object.entries(v)) if (!BIRTH_KEYS.has(k)) out[k] = strip(x)
    return out
  }
  // Belt and braces: a value that reads like a date, a clock time or a time zone is not carried under any name.
  return looksLikeBirthDetail(v) ? null : v
}

/** The chart with everything it was cast from taken out. */
export function snapshotOf(chart) {
  const out = {}
  for (const k of SNAPSHOT_KEYS) if (chart[k] !== undefined) out[k] = strip(chart[k])
  out.snapshot = true
  return out
}

function looksLikeBirthDetail(v) {
  if (typeof v === 'string') {
    // not \b: in "1975-06-25T22:30" the T is a word character, and the date would slip through
    if (/(^|\D)(1[6-9]|20|21)\d{2}-\d{2}-\d{2}(\D|$)/.test(v)) return 'a date'
    if (/^\d{1,2}:\d{2}(:\d{2})?$/.test(v)) return 'a clock time'
    if (/^(Africa|America|Antarctica|Asia|Atlantic|Australia|Europe|Indian|Pacific)\/[A-Za-z_]+/.test(v)) return 'a time zone'
  } else if (typeof v === 'number' && v > 2300000 && v < 2600000 && !Number.isInteger(v)) return 'a Julian day'
  return null
}

/** Paths in a value that still look like a birth detail — a date, a clock time, a time zone, a Julian day. Empty is the goal. */
export function birthTraces(value) {
  const found = []
  const walk = (v, path) => {
    if (found.length > 50) return
    if (v && typeof v === 'object') { for (const [k, x] of Object.entries(v)) walk(x, `${path}.${k}`); return }
    const why = looksLikeBirthDetail(v)
    if (why) found.push(`${path} (${why})`)
  }
  walk(value, '')
  return found
}

export function detailsPayload({ name, date, time, place }) {
  return {
    v: 1, name: name || '', date, time,
    place: { name: place.name, latitude: place.latitude, longitude: place.longitude, timezone: place.timezone },
  }
}
export function snapshotPayload({ name, lang, chart }) {
  return { v: 2, kind: 'snapshot', name: name || '', lang: lang || 'en', chart: snapshotOf(chart) }
}
/** What kind of share this is, or a thrown 'bad share'. */
export function checkPayload(p) {
  if (p && p.kind === 'snapshot' && p.chart && Array.isArray(p.chart.grahas) && Number.isInteger(p.chart.lagna_rasi)) return 'snapshot'
  if (p && p.date && p.time && p.place) return 'details'
  throw new Error('bad share')
}

// ── packing: JSON → gzip → AES-GCM → base64url ────────────────────────────────
const enc = new TextEncoder()
const dec = new TextDecoder()
/** base64url, in pieces: a chart is far too long to spread into one call. */
export function b64u(buf) {
  const u = new Uint8Array(buf)
  let s = ''
  for (let i = 0; i < u.length; i += 0x6000) s += String.fromCharCode.apply(null, u.subarray(i, i + 0x6000))
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
}
export const unb64u = (s) => Uint8Array.from(atob(s.replace(/-/g, '+').replace(/_/g, '/') + '==='.slice((s.length + 3) % 4)), (c) => c.charCodeAt(0))

async function pipe(bytes, stream) {
  const w = stream.writable.getWriter()
  w.write(bytes); w.close()
  return new Uint8Array(await new Response(stream.readable).arrayBuffer())
}
const isGzip = (u) => u.length > 2 && u[0] === 0x1f && u[1] === 0x8b

/** → { blob: "<iv>.<ciphertext>", key: "<base64url raw key>" } */
export async function seal(payload) {
  let plain = enc.encode(JSON.stringify(payload))
  // A chart is ~130 KB of JSON and squeezes to a fifth; the four birth details are not worth squeezing.
  if (plain.length > 2048 && typeof CompressionStream !== 'undefined') plain = await pipe(plain, new CompressionStream('gzip'))
  const key = await crypto.subtle.generateKey({ name: 'AES-GCM', length: 256 }, true, ['encrypt'])
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, plain)
  return { blob: `${b64u(iv)}.${b64u(ct)}`, key: b64u(await crypto.subtle.exportKey('raw', key)) }
}

export async function unseal(blob, keyB64) {
  const [ivS, ctS] = String(blob).split('.')
  const key = await crypto.subtle.importKey('raw', unb64u(keyB64), { name: 'AES-GCM' }, false, ['decrypt'])
  let plain = new Uint8Array(await crypto.subtle.decrypt({ name: 'AES-GCM', iv: unb64u(ivS) }, key, unb64u(ctS)))
  if (isGzip(plain)) plain = await pipe(plain, new DecompressionStream('gzip'))
  const p = JSON.parse(dec.decode(plain))
  checkPayload(p)
  return p
}
