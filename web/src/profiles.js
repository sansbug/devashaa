/**
 * Saved birth profiles.
 *
 * PRIVACY: these live in localStorage and nowhere else. Birth data is personal,
 * and this app has no accounts and no user database — nothing here is ever sent
 * to the backend. The backend only ever receives a chart request; it stores
 * nothing. Clearing site data removes every profile.
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
