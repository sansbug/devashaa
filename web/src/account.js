/**
 * Account + per-profile encrypted storage.
 *
 * Replaces the passphrase sync. Same cryptographic guarantee, nicer front door:
 * a user id and a password instead of ten words to write down.
 *
 * THE DERIVATION
 * --------------
 *     master    = PBKDF2-SHA256(password, salt = "devashaa-acct-v1:" + userid,
 *                               600 000 iterations)
 *     authId    = HKDF(master, "auth")        → sent; the server stores sha256 of it
 *     encKey    = HKDF(master, "enc")         → NEVER sent
 *     idKey     = HKDF(master, "profile-id")  → NEVER sent
 *
 * THE USERID IS THE SALT, and that is the point of having one. With a single
 * fixed salt, one precomputed table attacks every account at once; with the
 * userid mixed in, an attacker must spend the full 600 000 iterations per guess
 * *per account*. That is what turns a cheap mass spray into a slow targeted
 * attack, and it is why a self-chosen password is defensible here where it
 * would not have been under the old scheme.
 *
 * The three HKDF branches are independent, so the server holding every authId
 * ever registered learns nothing about any encKey.
 *
 * PROFILE IDS MUST BE OPAQUE
 * --------------------------
 * Each profile is stored separately so it can be saved and removed on its own.
 * Its key is HMAC(idKey, birth-signature) — never the signature itself. A birth
 * signature is date|time|latitude|longitude, which is close to a unique
 * identifier for a real person; storing it as a database key in the clear would
 * defeat the entire design while the blob beside it stayed encrypted.
 *
 * THERE IS NO RECOVERY. No email is collected, so a forgotten password cannot
 * be reset — the data is unreachable, including by us. That is the same
 * property that stops us reading it, and the UI states it before registration
 * rather than after.
 */

const SALT_PREFIX = 'devashaa-acct-v1:'
const ITERATIONS = 600_000            // OWASP 2023 floor for PBKDF2-SHA256

/** Mirrors the Worker's USERID regex. Kept in sync deliberately: the client
 *  gives a helpful message, the server is what actually enforces. */
export const USERID_RE = /^[a-z0-9][a-z0-9._-]{2,31}$/

export const API_BASE =
  import.meta.env.VITE_SYNC_URL
  || (typeof location !== 'undefined' && location.port === '5175'
        ? 'https://devashaa.com'
        : '')

const enc = new TextEncoder()
const dec = new TextDecoder()
const toHex = (b) =>
  [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, '0')).join('')

export const normaliseUserid = (s) => String(s || '').toLowerCase().trim()

/**
 * Password strength floor.
 *
 * A minimum, not a suggestion. The data behind it is a name plus a birth
 * moment and place, which identifies a real person, and there is no reset if
 * it is guessed. Length does most of the work — an 8-character password is
 * brute-forceable regardless of which symbols it contains.
 */
export function passwordProblem(pw) {
  const s = String(pw || '')
  if (s.length < 12) return 'Use at least 12 characters — length matters far more than symbols.'
  if (/^\d+$/.test(s)) return 'Digits alone are guessed almost instantly.'
  if (/^(.)\1+$/.test(s)) return 'That is a single repeated character.'
  const weak = ['password', 'qwerty', '123456', 'letmein', 'welcome', 'admin',
                'iloveyou', 'astrology', 'horoscope', 'devashaa', 'jyotish']
  const low = s.toLowerCase()
  if (weak.some((w) => low.includes(w))) return 'That contains a very common word.'
  if (new Set(s).size < 5) return 'Use a few more distinct characters.'
  return null
}

/** password + userid -> the three derived values. */
export async function deriveAccount(userid, password) {
  const id = normaliseUserid(userid)
  const base = await crypto.subtle.importKey(
    'raw', enc.encode(String(password)), 'PBKDF2', false, ['deriveBits'],
  )
  const master = await crypto.subtle.deriveBits(
    {
      name: 'PBKDF2', hash: 'SHA-256',
      salt: enc.encode(SALT_PREFIX + id),        // <- the userid IS the salt
      iterations: ITERATIONS,
    },
    base, 256,
  )
  const hk = await crypto.subtle.importKey('raw', master, 'HKDF', false, ['deriveBits'])
  const branch = (info) => crypto.subtle.deriveBits(
    { name: 'HKDF', hash: 'SHA-256', salt: enc.encode(SALT_PREFIX + id), info: enc.encode(info) },
    hk, 256,
  )
  const [authBits, encBits, idBits] = await Promise.all([
    branch('auth'), branch('enc'), branch('profile-id'),
  ])
  return {
    userid: id,
    authId: toHex(authBits),
    // Non-extractable, so no later bug can serialise it by accident.
    key: await crypto.subtle.importKey('raw', encBits, { name: 'AES-GCM' }, false,
                                       ['encrypt', 'decrypt']),
    idKey: await crypto.subtle.importKey('raw', idBits, { name: 'HMAC', hash: 'SHA-256' },
                                         false, ['sign']),
  }
}

/** Stable, opaque, per-account id for one profile. */
export async function profileIdFor(idKey, profile) {
  const sig = [profile.date, profile.time,
               profile.place?.latitude?.toFixed?.(4),
               profile.place?.longitude?.toFixed?.(4)].join('|')
  return toHex(await crypto.subtle.sign('HMAC', idKey, enc.encode(sig)))
}

export async function encryptJSON(key, value) {
  const iv = crypto.getRandomValues(new Uint8Array(12))
  const ct = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key,
                                         enc.encode(JSON.stringify(value)))
  const out = new Uint8Array(12 + ct.byteLength)
  out.set(iv, 0); out.set(new Uint8Array(ct), 12)
  let s = ''
  for (const b of out) s += String.fromCharCode(b)
  return btoa(s)
}

export async function decryptJSON(key, b64) {
  const raw = Uint8Array.from(atob(b64), (c) => c.charCodeAt(0))
  const pt = await crypto.subtle.decrypt({ name: 'AES-GCM', iv: raw.slice(0, 12) },
                                         key, raw.slice(12))
  return JSON.parse(dec.decode(pt))
}

/* --------------------------------- API ---------------------------------- */

async function call(path, { method = 'GET', authId, body } = {}) {
  const r = await fetch(`${API_BASE}/api/account${path}`, {
    method,
    headers: {
      ...(body ? { 'Content-Type': 'application/json' } : {}),
      ...(authId ? { 'X-Auth': authId } : {}),
    },
    ...(body ? { body: JSON.stringify(body) } : {}),
  })
  const data = await r.json().catch(() => ({}))
  if (!r.ok) throw new Error(data.error || `HTTP ${r.status}`)
  return data
}

/** Availability for the signup form. NOT authoritative — the PRIMARY KEY is. */
export const isTaken = (userid) =>
  call(`/${normaliseUserid(userid)}`).then((d) => d.exists)

export const register = (userid, authId) =>
  call('', { method: 'POST', body: { userid: normaliseUserid(userid), authId } })

export const login = (userid, authId) =>
  call(`/${normaliseUserid(userid)}/login`, { method: 'POST', body: { authId } })

export const deleteAccount = (userid, authId) =>
  call(`/${normaliseUserid(userid)}`, { method: 'DELETE', authId })

export const putProfile = (acct, profileId, blob) =>
  call(`/${acct.userid}/profiles/${profileId}`,
       { method: 'PUT', authId: acct.authId, body: { blob } })

export const removeProfile = (acct, profileId) =>
  call(`/${acct.userid}/profiles/${profileId}`, { method: 'DELETE', authId: acct.authId })

/**
 * Every stored profile, decrypted.
 *
 * A row that will not decrypt is reported rather than dropped. Silently
 * skipping it would render as "you have fewer charts than you saved", which is
 * the kind of loss nobody notices until it matters.
 */
export async function fetchProfiles(acct) {
  const { profiles } = await call(`/${acct.userid}/profiles`, { authId: acct.authId })
  const out = [], broken = []
  for (const row of profiles || []) {
    try {
      out.push({ ...(await decryptJSON(acct.key, row.blob)), _pid: row.profile_id })
    } catch {
      broken.push(row.profile_id)
    }
  }
  return { profiles: out, broken }
}

/** Push one profile. Per-profile by design, so saving is never all-or-nothing. */
export async function saveProfile(acct, profile) {
  const pid = await profileIdFor(acct.idKey, profile)
  await putProfile(acct, pid, await encryptJSON(acct.key, profile))
  return pid
}
