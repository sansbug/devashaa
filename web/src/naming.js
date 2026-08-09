/**
 * Name styles. The API returns every name in three Latin forms; this picks one,
 * or renders a fourth — Devanāgarī — from tables here.
 *
 *   common      — ordinary English spelling people actually write: Chandra, Mesha
 *   iast        — scholarly transliteration with diacritics:       Candra, Meṣa
 *   english     — plain English equivalents:                       Moon, Aries
 *   devanagari  — Devanāgarī script (the Hindi/Sanskrit default):  चन्द्र, मेष
 *
 * Nakṣatras and their deities have no English equivalents, so those fall back to
 * the common spelling under the "english" style. The API carries no Devanāgarī
 * field, so the "devanagari" style maps from the stable key / index / common
 * spelling to the tables below — falling back to the Latin value if unmapped, so
 * nothing ever renders blank.
 */

export const NAME_STYLES = [
  { key: 'common', label: 'Sanskrit', example: 'Chandra · Mesha' },
  { key: 'iast', label: 'Sanskrit (IAST)', example: 'Candra · Meṣa' },
  { key: 'english', label: 'English', example: 'Moon · Aries' },
  { key: 'devanagari', label: 'देवनागरी', example: 'चन्द्र · मेष' },
]

const RASIS = {
  common: ['Mesha', 'Vrishabha', 'Mithuna', 'Karka', 'Simha', 'Kanya',
           'Tula', 'Vrishchika', 'Dhanu', 'Makara', 'Kumbha', 'Meena'],
  iast: ['Meṣa', 'Vṛṣabha', 'Mithuna', 'Karka', 'Siṁha', 'Kanyā',
         'Tulā', 'Vṛścika', 'Dhanu', 'Makara', 'Kumbha', 'Mīna'],
  english: ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'],
  devanagari: ['मेष', 'वृषभ', 'मिथुन', 'कर्क', 'सिंह', 'कन्या',
               'तुला', 'वृश्चिक', 'धनु', 'मकर', 'कुम्भ', 'मीन'],
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
  devanagari: { sun: 'सूर्य', moon: 'चन्द्र', mars: 'मङ्गल', mercury: 'बुध',
                jupiter: 'गुरु', venus: 'शुक्र', saturn: 'शनि',
                rahu: 'राहु', ketu: 'केतु' },
}

/** Nakṣatra Devanāgarī by the API's common spelling (vedic.py NAKSHATRAS[·][0]). */
const NAK_DEV = {
  'Ashwini': 'अश्विनी', 'Bharani': 'भरणी', 'Krittika': 'कृत्तिका', 'Rohini': 'रोहिणी',
  'Mrigashira': 'मृगशिरा', 'Ardra': 'आर्द्रा', 'Punarvasu': 'पुनर्वसु', 'Pushya': 'पुष्य',
  'Ashlesha': 'आश्लेषा', 'Magha': 'मघा', 'Purva Phalguni': 'पूर्वाफल्गुनी',
  'Uttara Phalguni': 'उत्तराफल्गुनी', 'Hasta': 'हस्त', 'Chitra': 'चित्रा', 'Swati': 'स्वाती',
  'Vishakha': 'विशाखा', 'Anuradha': 'अनुराधा', 'Jyeshtha': 'ज्येष्ठा', 'Mula': 'मूल',
  'Purva Ashadha': 'पूर्वाषाढा', 'Uttara Ashadha': 'उत्तराषाढा', 'Shravana': 'श्रवण',
  'Dhanishta': 'धनिष्ठा', 'Shatabhisha': 'शतभिषा', 'Purva Bhadrapada': 'पूर्वाभाद्रपदा',
  'Uttara Bhadrapada': 'उत्तराभाद्रपदा', 'Revati': 'रेवती',
}

/** Deity Devanāgarī by the API's common deity string (vedic.py NAKSHATRAS[·][2]),
 *  parentheticals preserved so the rendered value matches the Latin one. */
const DEITY_DEV = {
  'Dastra (Ashwini Kumara)': 'दस्र (अश्विनीकुमार)', 'Yama': 'यम', 'Agni': 'अग्नि',
  'Brahma': 'ब्रह्मा', 'Chandra': 'चन्द्र', 'Isha (Rudra)': 'ईश (रुद्र)', 'Aditi': 'अदिति',
  'Jiva (Brihaspati)': 'जीव (बृहस्पति)', 'Ahi (Sarpa)': 'अहि (सर्प)', 'Pitara': 'पितर',
  'Bhaga': 'भग', 'Aryama': 'अर्यमा', 'Surya': 'सूर्य', 'Tvashta': 'त्वष्टा', 'Marut': 'मरुत्',
  'Shakragni': 'शक्राग्नि', 'Mitra': 'मित्र', 'Vasava (Indra)': 'वासव (इन्द्र)',
  'Rakshasa (Nirriti)': 'राक्षस (निरृति)', 'Varuna': 'वरुण', 'Vishvadeva': 'विश्वदेव',
  'Govinda (Vishnu)': 'गोविन्द (विष्णु)', 'Vasu': 'वसु', 'Ajapa': 'अजैकपाद',
  'Ahirbudhanya': 'अहिर्बुध्न्य', 'Pusha': 'पूषा',
}

/** Reverse lookups: from the API's common spelling to Devanāgarī, built from the
 *  tables above so there is a single source of truth. */
const RASI_DEV_BY_COMMON = Object.fromEntries(
  RASIS.common.map((n, i) => [n, RASIS.devanagari[i]]))
const GRAHA_DEV_BY_COMMON = Object.fromEntries(
  Object.entries(GRAHAS.common).map(([k, n]) => [n, GRAHAS.devanagari[k]]))

/** Field suffix on the API objects for a given style (Devanāgarī has no field). */
const SUFFIX = { common: '', iast: '_iast', english: '_en' }

export function makeNamer(style = 'common') {
  const dev = style === 'devanagari'
  const s = SUFFIX[style] === undefined ? '' : SUFFIX[style]
  const pick = (obj, base) => (obj ? (obj[base + s] ?? obj[base]) : undefined)

  return {
    style,
    /** Graha display name, e.g. Chandra / Candra / Moon / चन्द्र. */
    graha: (g) => (dev ? (GRAHAS.devanagari[g?.key] ?? GRAHA_DEV_BY_COMMON[g?.name] ?? pick(g, 'name'))
                       : pick(g, 'name')),
    /** The rāśi a graha occupies. */
    grahaRasi: (g) => (dev ? (RASIS.devanagari[g?.rasi] ?? RASI_DEV_BY_COMMON[g?.rasi_name] ?? pick(g, 'rasi_name'))
                           : pick(g, 'rasi_name')),
    /** Lord of the rāśi a graha occupies. */
    rasiLord: (g) => (dev ? (GRAHA_DEV_BY_COMMON[g?.rasi_lord] ?? pick(g, 'rasi_lord'))
                          : pick(g, 'rasi_lord')),
    /** Rāśi by zodiac index 0-11 (charts index by sign, not by graha). */
    rasi: (i) => (RASIS[style] || RASIS.common)[i],
    /** Graha by KEY — for the analysis and rāśi endpoints, which cite rules
     *  rather than describe placements and so return keys, not objects. */
    grahaKey: (k) => (GRAHAS[style] || GRAHAS.common)[k] ?? k,
    /** Nakṣatra — no English form exists, so english falls back to common. */
    nakshatra: (n) => (dev ? (NAK_DEV[n?.name] ?? n?.name)
                           : (style === 'iast' ? n?.name_iast : n?.name)),
    deity: (n) => (dev ? (DEITY_DEV[n?.deity] ?? n?.deity)
                       : (style === 'iast' ? n?.deity_iast : n?.deity)),
  }
}
