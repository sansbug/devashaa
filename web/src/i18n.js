/**
 * UI string table for the interface chrome (headings, labels, buttons, notes).
 *
 * This is Phase 1 of full Hindi: the *static* interface. The generated chart
 * READINGS (śloka effects, bhāva/yoga/dignity/daśā verdicts) are backend-served
 * cited content and get their own later phase with a language path + review.
 *
 * Keys are dotted and grouped by surface. Every key MUST have `en`; `hi` is
 * added as translated (falls back to English until then, so nothing breaks).
 */
import { CHROME } from './i18n-chrome.js'

const MANUAL = {
  // ── birth-data form + header ──────────────────────────────────────────────
  'header.sub': {
    en: 'Sidereal · Lahiri ayanāṁśa · whole-sign bhāvas · Swiss Ephemeris',
    hi: 'निरयन · लाहिरी अयनांश · पूर्ण-राशि भाव · स्विस एफ़ेमेरिस',
  },
  'header.after': { en: 'after', hi: 'आधार' },
  'form.name': { en: 'Name', hi: 'नाम' },
  'form.name.ph': { en: 'optional', hi: 'वैकल्पिक' },
  'form.date': { en: 'Birth date', hi: 'जन्म तिथि' },
  'form.time': { en: 'Birth time (24h, local)', hi: 'जन्म समय (24 घंटे, स्थानीय)' },
  'form.place.label': { en: 'Birth place', hi: 'जन्म स्थान' },
  'form.place': { en: 'City, region, country', hi: 'शहर, क्षेत्र, देश' },
  'form.searching': { en: 'searching…', hi: 'खोजा जा रहा है…' },
  'form.cast': { en: 'Cast chart', hi: 'कुंडली बनाएँ' },
  'form.casting': { en: 'Casting…', hi: 'बन रही है…' },

  // ── appearance bar ────────────────────────────────────────────────────────
  'appearance.language': { en: 'Language', hi: 'भाषा' },
  'appearance.theme': { en: 'Theme', hi: 'रंग-रूप' },
  'appearance.names': { en: 'Names', hi: 'नाम-शैली' },

  // ── saved charts / account ────────────────────────────────────────────────
  'saved.title': { en: 'Save your charts', hi: 'अपनी कुंडलियाँ सहेजें' },
  'saved.here': { en: 'in this browser, or to an account', hi: 'इस ब्राउज़र में, या किसी खाते में' },

  // ── ephemeris status ──────────────────────────────────────────────────────
  'ephem.ok': { en: '● ephemeris verified — reading .se1 (JPL DE431)', hi: '● एफ़ेमेरिस सत्यापित — .se1 (JPL DE431) पढ़ा जा रहा है' },
  // Full-phrase toggle labels (word order differs by language — verb trails in Hindi).
  'ref.rao.showFull': { en: 'Show the K.N. Rao (modern) pointers', hi: 'K.N. Rao (आधुनिक) संकेत दिखाएँ' },
  'ref.rao.hideFull': { en: 'Hide the K.N. Rao (modern) pointers', hi: 'K.N. Rao (आधुनिक) संकेत छिपाएँ' },

  // ── result sections the catalog missed ────────────────────────────────────
  'ref.grahaSignals.title': { en: 'What BPHS says about each graha', hi: 'BPHS प्रत्येक ग्रह के बारे में क्या कहता है' },
  'ref.grahaTable.title': { en: 'Grahas', hi: 'ग्रह' },
  'ref.varga.title': { en: 'Ṣoḍaśavarga — all sixteen divisions', hi: 'षोडशवर्ग — सोलहों विभाजन' },
  'ref.varga.caption': { en: 'Hover a column heading for what each division is read for.', hi: 'प्रत्येक विभाजन किसके लिए पढ़ा जाता है, यह जानने के लिए स्तंभ-शीर्ष पर कर्सर ले जाएँ।' },
  'grahaTable.graha': { en: 'Graha', hi: 'ग्रह' },
  'grahaTable.rasi': { en: 'Rāśi', hi: 'राशि' },
  'grahaTable.degree': { en: 'Degree', hi: 'अंश' },
  'grahaTable.bhava': { en: 'Bhāva', hi: 'भाव' },
  'grahaTable.nakshatra': { en: 'Nakṣatra', hi: 'नक्षत्र' },
  'grahaTable.pada': { en: 'Pada', hi: 'पाद' },
  'grahaTable.deity': { en: 'Deity', hi: 'देवता' },
  'grahaTable.rasiLord': { en: 'Rāśi lord', hi: 'राशि स्वामी' },
  'grahaTable.speed': { en: 'Speed', hi: 'गति' },

  // ── classical concordance panel ───────────────────────────────────────────
  'classical.title': { en: 'Classical sources', hi: 'शास्त्रीय स्रोत' },
  'classical.in': { en: 'in', hi: 'में' },
  'classical.houseTitle': { en: 'Planet-in-house (bhāva)', hi: 'भाव में ग्रह (भाव-फल)' },
  'classical.bhava': { en: 'bhāva', hi: 'भाव' },
  'classical.hist.prefix': { en: 'historical', hi: 'ऐतिहासिक' },
  'classical.class.caste': { en: 'caste', hi: 'जाति' },
  'classical.class.gender': { en: 'gender & marriage', hi: 'लिंग एवं विवाह' },
  'classical.class.slavery': { en: 'servitude', hi: 'सेवावृत्ति' },
  'classical.class.occupation': { en: 'occupation', hi: 'व्यवसाय' },
  'classical.class.health': { en: 'illness', hi: 'रोग' },
  'classical.class.archaic': { en: 'archaic terms', hi: 'पुरातन संदर्भ' },
  'classical.hist.detailLead': { en: 'Historical material', hi: 'ऐतिहासिक सामग्री' },
  'classical.hist.detailTouches': { en: 'This reading touches:', hi: 'यह पाठ इनसे संबंधित है:' },
  'classical.hist.detailNote': {
    en: 'Shown for completeness, not as a judgement — handled per our adaptation policy:',
    hi: 'पूर्णता हेतु दर्शाया गया, निर्णय के रूप में नहीं — हमारी अनुकूलन नीति के अनुसार नियंत्रित:',
  },
}

// Chrome (the 482 extracted panel strings) plus the hand-written entry-experience
// entries above, which win on any key overlap.
export const STRINGS = { ...CHROME, ...MANUAL }

export function t(lang, key, fallback) {
  const s = STRINGS[key]
  if (!s) return fallback ?? key
  return s[lang] ?? s.en ?? fallback ?? key
}
