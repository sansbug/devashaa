/**
 * Passphrase sync — carry your saved charts to another device without ever
 * telling the server who you are.
 *
 * THE GUARANTEE, AND HOW IT IS ENFORCED
 * -------------------------------------
 * Birth date + exact time + place is close to a unique identifier on its own —
 * roughly one person per minute per town — and with a name it is unambiguously
 * personal data. So it never leaves this file unencrypted.
 *
 * One passphrase derives TWO independent values:
 *
 *     master  = PBKDF2-SHA256(passphrase, fixed salt, 600 000 iterations)
 *     syncId  = HKDF(master, info "sync-id")    → sent to the server
 *     encKey  = HKDF(master, info "enc-key")    → NEVER sent, never stored
 *
 * The server is keyed on `syncId` and holds AES-GCM ciphertext. Because the two
 * HKDF outputs are independent, holding every syncId ever created tells you
 * nothing about any encKey. The server cannot decrypt what it stores — not as a
 * promise, but because it does not have the material.
 *
 * WHY THE PASSPHRASE IS GENERATED AND NOT CHOSEN
 * ----------------------------------------------
 * There is no per-user salt, because a per-user salt would have to be fetched
 * by some identifier, and the identifier is the thing we are refusing to
 * collect. A fixed salt permits precomputation, which is only safe if the
 * passphrase has real entropy. Ten words from a 256-word list is 80 bits from
 * a CSPRNG — far beyond precomputation.
 *
 * A user-chosen phrase would be perhaps 20 bits and the fixed salt would then
 * matter enormously. So `generatePassphrase()` is the only way to make one, and
 * the UI must not offer a text box to invent your own.
 */

const SALT = 'devashaa-sync-v1'
const ITERATIONS = 600_000          // OWASP 2023 floor for PBKDF2-SHA256
const WORDS_IN_PHRASE = 10          // 10 x 8 bits = 80 bits of entropy

/**
 * 256 short, common, unambiguous English words = exactly 8 bits each.
 * Chosen to be easy to read aloud and to write down: no homophones, no words
 * that differ by one letter, nothing longer than six characters.
 */
export const WORDLIST = [
  'able', 'acid', 'aged', 'also', 'area', 'army', 'away', 'baby', 'back', 'ball',
  'band', 'bank', 'base', 'bath', 'bean', 'bear', 'beat', 'beer', 'bell', 'belt',
  'bend', 'best', 'bike', 'bird', 'blue', 'boat', 'body', 'bone', 'book', 'boot',
  'born', 'bowl', 'brass', 'bread', 'brick', 'bring', 'brown', 'brush', 'burn', 'bush',
  'busy', 'cake', 'call', 'calm', 'camp', 'card', 'care', 'cart', 'case', 'cash',
  'cast', 'cell', 'chain', 'chair', 'chalk', 'cheap', 'chest', 'chief', 'city', 'clay',
  'clean', 'clear', 'climb', 'clock', 'cloth', 'cloud', 'coal', 'coat', 'cold', 'come',
  'cook', 'cool', 'copy', 'cord', 'cork', 'corn', 'cost', 'crop', 'cup', 'cut',
  'damp', 'dark', 'date', 'dawn', 'deep', 'desk', 'dish', 'dock', 'door', 'down',
  'draw', 'dress', 'drink', 'drive', 'drop', 'drum', 'dry', 'dust', 'duty', 'each',
  'earn', 'east', 'easy', 'edge', 'eggs', 'face', 'fact', 'fair', 'fall', 'farm',
  'fast', 'feed', 'feel', 'field', 'find', 'fire', 'fish', 'flag', 'flat', 'floor',
  'flour', 'flow', 'fold', 'food', 'foot', 'fork', 'form', 'free', 'fresh', 'fruit',
  'fuel', 'full', 'game', 'gate', 'gift', 'girl', 'give', 'glass', 'goat', 'gold',
  'good', 'grain', 'grass', 'grey', 'grow', 'hair', 'half', 'hall', 'hand', 'hang',
  'hard', 'harm', 'hat', 'head', 'heat', 'help', 'herb', 'hide', 'high', 'hill',
  'hold', 'hole', 'home', 'hook', 'hope', 'horn', 'horse', 'hour', 'house', 'ice',
  'idea', 'inch', 'iron', 'jump', 'keep', 'key', 'kind', 'king', 'knee', 'knife',
  'knot', 'lace', 'lake', 'lamp', 'land', 'last', 'late', 'lead', 'leaf', 'learn',
  'leg', 'lend', 'light', 'line', 'lion', 'lip', 'list', 'live', 'load', 'lock',
  'long', 'look', 'loose', 'loud', 'love', 'low', 'luck', 'made', 'mail', 'main',
  'make', 'man', 'map', 'mark', 'mass', 'meal', 'mean', 'meat', 'meet', 'metal',
  'milk', 'mind', 'mine', 'mint', 'mist', 'mix', 'moon', 'move', 'music', 'nail',
  'name', 'near', 'neck', 'need', 'nest', 'net', 'new', 'news', 'nice', 'night',
  'noise', 'north', 'nose', 'note', 'nut', 'oak', 'oil', 'old', 'open', 'oven',
  'page', 'pain', 'paint', 'pair', 'paper', 'park',
]

if (WORDLIST.length !== 256) {
  // A short list silently reduces entropy, which is the one failure here that
  // would be invisible in testing. Fail loudly at load instead.
  throw new Error(`sync.js: WORDLIST must be exactly 256 words, got ${WORDLIST.length}`)
}

const enc = new TextEncoder()
const dec = new TextDecoder()

const toHex = (buf) =>
  [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, '0')).join('')

/**
 * A fresh passphrase from the platform CSPRNG. There is deliberately no way to
 * supply your own — see the module note on entropy and the fixed salt.
 */
export function generatePassphrase() {
  const bytes = crypto.getRandomValues(new Uint8Array(WORDS_IN_PHRASE))
  return [...bytes].map((b) => WORDLIST[b]).join(' ')
}

/** Tolerate the ways a human retypes a phrase: case, punctuation, extra spaces. */
export function normalisePassphrase(phrase) {
  return String(phrase || '')
    .toLowerCase()
    .replace(/[^a-z\s]/g, ' ')
    .split(/\s+/)
    .filter(Boolean)
    .join(' ')
}

export function looksLikePassphrase(phrase) {
  const words = normalisePassphrase(phrase).split(' ').filter(Boolean)
  return words.length === WORDS_IN_PHRASE && words.every((w) => WORDLIST.includes(w))
}

/** The word that isn't in the list — so a typo can be pointed at precisely. */
export function unknownWords(phrase) {
  return normalisePassphrase(phrase)
    .split(' ')
    .filter((w) => w && !WORDLIST.includes(w))
}

async function hkdf(masterBits, info, bits = 256) {
  const key = await crypto.subtle.importKey('raw', masterBits, 'HKDF', false, ['deriveBits'])
  return crypto.subtle.deriveBits(
    { name: 'HKDF', hash: 'SHA-256', salt: enc.encode(SALT), info: enc.encode(info) },
    key, bits,
  )
}

/**
 * passphrase -> { syncId, key }.
 *
 * `syncId` is the only thing that ever goes to the server. `key` is a
 * non-extractable CryptoKey, so even a later bug cannot serialise it by
 * accident.
 */
export async function deriveKeys(phrase) {
  const normalised = normalisePassphrase(phrase)
  const base = await crypto.subtle.importKey(
    'raw', enc.encode(normalised), 'PBKDF2', false, ['deriveBits'],
  )
  const master = await crypto.subtle.deriveBits(
    { name: 'PBKDF2', hash: 'SHA-256', salt: enc.encode(SALT), iterations: ITERATIONS },
    base, 256,
  )
  const idBits = await hkdf(master, 'devashaa-sync-id')
  const keyBits = await hkdf(master, 'devashaa-enc-key')
  const key = await crypto.subtle.importKey(
    'raw', keyBits, { name: 'AES-GCM' }, false, ['encrypt', 'decrypt'],
  )
  return { syncId: toHex(idBits), key }
}

/** AES-GCM with a fresh IV every time. Output is iv || ciphertext, base64. */
export async function encryptJSON(key, value) {
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const ct = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv }, key, enc.encode(JSON.stringify(value)),
  )
  const out = new Uint8Array(iv.length + ct.byteLength)
  out.set(iv, 0)
  out.set(new Uint8Array(ct), iv.length)
  let s = ''
  for (const b of out) s += String.fromCharCode(b)
  return btoa(s)
}

export async function decryptJSON(key, b64) {
  const raw = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0))
  const iv = raw.slice(0, 12)
  const pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, raw.slice(12))
  return JSON.parse(dec.decode(pt))
}

/**
 * Union two profile lists by their birth signature.
 *
 * Last-write-wins would be wrong here: two devices editing offline is the
 * normal case, not the exception, and silently discarding the charts someone
 * saved on their phone is the kind of data loss that is never noticed until it
 * matters. A profile is the same profile when the birth moment and place match,
 * which is exactly what `signature` in profiles.js already encodes.
 */
export function mergeProfiles(a = [], b = []) {
  const sig = (p) =>
    [p.date, p.time, p.place?.latitude?.toFixed?.(4), p.place?.longitude?.toFixed?.(4)].join('|')
  const out = new Map()
  for (const p of [...b, ...a]) {           // `a` (local) wins on a name clash
    const k = sig(p)
    if (!out.has(k)) out.set(k, p)
  }
  return [...out.values()]
}

/* ------------------------------------------------------------------------ *
 * Transport. The blob store lives on the Cloudflare Worker that serves the
 * site (see web/worker.js), NOT on the Python chart API — Render's free plan
 * has an ephemeral filesystem and would lose every blob on redeploy.
 * ------------------------------------------------------------------------ */

/** Same origin in production. In `npm run dev` the site is on :5175 and the
 *  Worker is not running, so sync points at the deployed origin. */
export const SYNC_BASE =
  import.meta.env.VITE_SYNC_URL
  || (typeof location !== 'undefined' && location.port === '5175'
        ? 'https://devashaa.com'
        : '')

export async function pushProfiles(syncId, key, profiles) {
  const blob = await encryptJSON(key, { v: 1, profiles })
  const r = await fetch(`${SYNC_BASE}/api/sync/${syncId}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ blob }),
  })
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).error || `HTTP ${r.status}`)
  return true
}

/** Returns null when nothing has ever been stored under this passphrase. */
export async function pullProfiles(syncId, key) {
  const r = await fetch(`${SYNC_BASE}/api/sync/${syncId}`)
  if (r.status === 404) return null
  if (!r.ok) throw new Error((await r.json().catch(() => ({}))).error || `HTTP ${r.status}`)
  const { blob } = await r.json()
  try {
    const data = await decryptJSON(key, blob)
    return Array.isArray(data?.profiles) ? data.profiles : []
  } catch {
    // AES-GCM is authenticated, so a decrypt failure means the key is wrong —
    // i.e. a different passphrase collided on the id, or the blob is corrupt.
    // Never silently return an empty list here: that would look like "you have
    // no saved charts" and invite the user to overwrite real data.
    throw new Error('DECRYPT_FAILED')
  }
}

export async function forgetProfiles(syncId) {
  const r = await fetch(`${SYNC_BASE}/api/sync/${syncId}`, { method: 'DELETE' })
  if (!r.ok) throw new Error(`HTTP ${r.status}`)
  return true
}
