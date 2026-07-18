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
    /** Nakṣatra — no English form exists, so english falls back to common. */
    nakshatra: (n) => (style === 'iast' ? n?.name_iast : n?.name),
    deity: (n) => (style === 'iast' ? n?.deity_iast : n?.deity),
  }
}
