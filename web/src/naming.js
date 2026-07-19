/**
 * Name styles. The API already returns every name in three forms; this picks one.
 *
 *   common  — ordinary English spelling people actually write:  Chandra, Meṣa→Mesha
 *   iast    — scholarly transliteration with diacritics:        Candra, Meṣa
 *   english — plain English equivalents:                        Moon, Aries
 *
 * Nakṣatras and their deities have no English equivalents, so those fall back to
 * the common spelling under the "english" style.
 */

export const NAME_STYLES = [
  { key: 'common', label: 'Sanskrit', example: 'Chandra · Mesha' },
  { key: 'iast', label: 'Sanskrit (IAST)', example: 'Candra · Meṣa' },
  { key: 'english', label: 'English', example: 'Moon · Aries' },
]

const RASIS = {
  common: ['Mesha', 'Vrishabha', 'Mithuna', 'Karka', 'Simha', 'Kanya',
           'Tula', 'Vrishchika', 'Dhanu', 'Makara', 'Kumbha', 'Meena'],
  iast: ['Meṣa', 'Vṛṣabha', 'Mithuna', 'Karka', 'Siṁha', 'Kanyā',
         'Tulā', 'Vṛścika', 'Dhanu', 'Makara', 'Kumbha', 'Mīna'],
  english: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'],
}

/** Graha display names by KEY. The chart endpoint returns whole graha objects
 *  carrying all three spellings, but the analysis and rāśi endpoints return
 *  bare keys ("sun", "saturn") because they are citing BPHS rules rather than
 *  describing a placement — so those need this table. Order is the canonical
 *  Sūrya→Ketu, not alphabetical. */
const GRAHAS = {
  common: { sun: 'Surya', moon: 'Chandra', mars: 'Mangala', mercury: 'Budha',
            jupiter: 'Guru', venus: 'Shukra', saturn: 'Shani',
            rahu: 'Rahu', ketu: 'Ketu' },
  iast: { sun: 'Sūrya', moon: 'Candra', mars: 'Maṅgala', mercury: 'Budha',
          jupiter: 'Guru', venus: 'Śukra', saturn: 'Śani',
          rahu: 'Rāhu', ketu: 'Ketu' },
  english: { sun: 'Sun', moon: 'Moon', mars: 'Mars', mercury: 'Mercury',
             jupiter: 'Jupiter', venus: 'Venus', saturn: 'Saturn',
             rahu: 'Rāhu', ketu: 'Ketu' },   // the nodes have no English names
}

/** Field suffix on the API objects for a given style. */
const SUFFIX = { common: '', iast: '_iast', english: '_en' }

export function makeNamer(style = 'common') {
  const s = SUFFIX[style] === undefined ? '' : SUFFIX[style]
  const pick = (obj, base) => (obj ? (obj[base + s] ?? obj[base]) : undefined)

  return {
    style,
    /** Graha display name, e.g. Chandra / Candra / Moon. */
    graha: (g) => pick(g, 'name'),
    /** The rāśi a graha occupies. */
    grahaRasi: (g) => pick(g, 'rasi_name'),
    /** Lord of the rāśi a graha occupies. */
    rasiLord: (g) => pick(g, 'rasi_lord'),
    /** Rāśi by zodiac index 0-11 (charts index by sign, not by graha). */
    rasi: (i) => (RASIS[style] || RASIS.common)[i],
    /** Graha by KEY — for the analysis and rāśi endpoints, which cite rules
     *  rather than describe placements and so return keys, not objects. */
    grahaKey: (k) => (GRAHAS[style] || GRAHAS.common)[k] ?? k,
    /** Nakṣatra — no English form exists, so english falls back to common. */
    nakshatra: (n) => (style === 'iast' ? n?.name_iast : n?.name),
    deity: (n) => (style === 'iast' ? n?.deity_iast : n?.deity),
  }
}
