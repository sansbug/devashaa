/**
 * Saved birth profiles.
 *
 * PRIVACY: these live in localStorage. Birth data is personal — a date, an
 * exact time and a place is roughly one person per minute per town.
 *
 * NOTE, and keep this accurate: profiles ARE transmitted in two cases. Casting
 * or re-opening one sends its birth details to the chart API (which stores
 * nothing). Saving one to an account sends it ENCRYPTED to the accounts server,
 * which has no key for it. Neither is automatic; both follow a user action.
 *
 * This comment was wrong for a while after accounts shipped, and the error
 * propagated onto the public privacy page. If you change what leaves this file,
 * /privacy is part of the change — see web/src/Privacy.jsx.
 */

const KEY = 'devashaa.profiles'
const LIMIT = 60

const read = () => {
  try {
    const raw = JSON.parse(localStorage.getItem(KEY) || '[]')
    return Array.isArray(raw) ? raw : []
  } catch {
    return []   // corrupt storage must not break the whole app
  }
}

const write = (list) => {
  try {
    localStorage.setItem(KEY, JSON.stringify(list.slice(0, LIMIT)))
  } catch {
    /* quota or private mode — saving is a convenience, never block casting */
  }
}

/** Identity of a birth: the same moment and place is the same person, whatever
 *  they typed as a name. Prevents a duplicate every time a chart is recast. */
const signature = (p) =>
  [p.date, p.time, p.place?.latitude?.toFixed(4), p.place?.longitude?.toFixed(4)].join('|')

export const listProfiles = () => read()

/**
 * Save (or refresh) a profile. Returns the updated list.
 * An unnamed chart is still worth saving — it is keyed by its birth data.
 */
export function saveProfile({ name, date, time, place }) {
  if (!date || !time || !place) return read()
  const entry = {
    id: signature({ date, time, place }),
    name: (name || '').trim(),
    date,
    time,
    place,
    savedAt: Date.now(),
  }
  const rest = read().filter((p) => p.id !== entry.id)
  // If the user recasts an existing birth and NOW gives it a name, keep the name.
  const prior = read().find((p) => p.id === entry.id)
  if (!entry.name && prior?.name) entry.name = prior.name
  const list = [entry, ...rest]
  write(list)
  return list
}

export function deleteProfile(id) {
  const list = read().filter((p) => p.id !== id)
  write(list)
  return list
}

/** Label for the chooser: name if given, else the birth details themselves. */
export function profileLabel(p) {
  const city = (p.place?.name || '').split(',')[0]
  return p.name || `${city || 'Chart'} · ${p.date}`
}

export function profileDetail(p) {
  const city = (p.place?.name || '').split(',')[0]
  return `${p.date} ${p.time}${city ? ` · ${city}` : ''}`
}

/**
 * Replace the whole list — used only by passphrase sync after a merge.
 *
 * Deliberately separate from saveProfile(): that one is for a chart someone
 * just cast, and enforces the newest-first ordering and the LIMIT. This takes
 * an already-merged list and writes it wholesale, so a restore cannot be
 * reordered or silently truncated mid-merge.
 */
export const replaceAll = (list) => {
  write(Array.isArray(list) ? list : [])
  return read()
}
