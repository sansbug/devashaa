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
  // ── Panchāṅga ──
  'panchang.tab': { en: 'Pañcāṅga', hi: 'पञ्चाङ्ग' },
  'panchang.title': { en: 'Pañcāṅga — auspicious days', hi: 'पञ्चाङ्ग — शुभ दिन' },
  'panchang.limbs': { en: 'Pañcāṅga', hi: 'पञ्चाङ्ग' },
  'panchang.foryou': { en: 'For this chart', hi: 'इस कुंडली हेतु' },
  'panchang.windows': { en: 'Windows', hi: 'कालखण्ड' },
  'panchang.tithi': { en: 'Tithi', hi: 'तिथि' },
  'panchang.vara': { en: 'Vāra', hi: 'वार' },
  'panchang.nakshatra': { en: 'Nakṣatra', hi: 'नक्षत्र' },
  'panchang.yoga': { en: 'Yoga', hi: 'योग' },
  'panchang.tarabala': { en: 'Tārā-bala', hi: 'तारा-बल' },
  'panchang.candrabala': { en: 'Candra-bala', hi: 'चन्द्र-बल' },
  'panchang.transit': { en: 'Moon transit', hi: 'चन्द्र-गोचर' },
  'panchang.dayquality': { en: 'Day quality', hi: 'दिन की गुणवत्ता' },
  'panchang.dasha': { en: 'Daśā fit', hi: 'दशा-अनुकूलता' },
  'panchang.masa': { en: 'Lunar month', hi: 'चांद्र मास' },
  'panchang.festivals': { en: 'Festivals & observances', hi: 'पर्व एवं व्रत' },
  'panchang.monthFestivals': { en: 'Special days this month', hi: 'इस माह के विशेष दिन' },
  'panchang.drikSrc': { en: 'Date per DrikPanchang (bhadrā-adjusted muhūrta)', hi: 'तिथि DrikPanchang अनुसार (भद्रा-समायोजित मुहूर्त)' },
  // ── chart-analysis matrix ──
  'matrix.title': { en: 'Chart matrix — domain verdicts', hi: 'कुंडली मैट्रिक्स — क्षेत्र-निर्णय' },
  'matrix.sub': {
    en: 'Each life-domain read as a weighted, cited composite of the natal factor web. A balance from −1 to +1; the band tints a ledger you can open — an indication, not a fated verdict.',
    hi: 'प्रत्येक जीवन-क्षेत्र जन्म-कुंडली के कारक-जाल का भारित, प्रमाणित संयोजन। −1 से +1 तक संतुलन; बैंड एक बहीखाता रंगता है जिसे आप खोल सकते हैं — संकेत, नियति नहीं।',
  },
  'matrix.loading': { en: 'Computing the matrix…', hi: 'मैट्रिक्स गणना हो रही है…' },
  'matrix.themes': { en: 'Life themes', hi: 'जीवन-क्षेत्र' },
  'matrix.bhavas': { en: 'Bhāva decomposition', hi: 'भाव-विश्लेषण' },
  'matrix.house': { en: 'House', hi: 'भाव' }, 'matrix.hcol': { en: 'House', hi: 'भाव' },
  'matrix.lord': { en: 'Lord', hi: 'स्वामी' }, 'matrix.lcol': { en: 'Lord', hi: 'स्वामी' },
  'matrix.occ': { en: 'Occ.', hi: 'ग्रह' }, 'matrix.asp': { en: 'Asp.', hi: 'दृष्टि' },
  'matrix.karaka': { en: 'Kāraka', hi: 'कारक' }, 'matrix.yoga': { en: 'Yoga', hi: 'योग' },
  'matrix.varga': { en: 'Varga', hi: 'वर्ग' },
  'matrix.net': { en: 'Net', hi: 'निवल' },
  'matrix.band.thriving': { en: 'thriving', hi: 'समृद्ध' },
  'matrix.band.supported': { en: 'supported', hi: 'समर्थित' },
  'matrix.band.mixed': { en: 'mixed', hi: 'मिश्र' },
  'matrix.band.stressed': { en: 'stressed', hi: 'तनावग्रस्त' },
  'matrix.band.afflicted': { en: 'afflicted', hi: 'पीड़ित' },
  'matrix.web': { en: 'Aspect web', hi: 'दृष्टि-जाल' },
  'matrix.benefic': { en: 'benefic dṛṣṭi', hi: 'शुभ दृष्टि' },
  'matrix.malefic': { en: 'malefic dṛṣṭi', hi: 'पाप दृष्टि' },
  'matrix.nodenote': { en: 'node fill = disposition · ring size = strength', hi: 'बिंदु रंग = स्वभाव · आकार = बल' },
  'matrix.timeline': { en: 'Near future', hi: 'निकट भविष्य' },
  'matrix.overall': { en: 'Overall', hi: 'समग्र' },
  'matrix.theme.self': { en: 'Self · vitality · mind', hi: 'स्वयं · प्राण · मन' },
  'matrix.theme.wealth': { en: 'Wealth · finances', hi: 'धन · वित्त' },
  'matrix.theme.career': { en: 'Career · status', hi: 'कर्म · प्रतिष्ठा' },
  'matrix.theme.marriage': { en: 'Marriage · partner', hi: 'विवाह · जीवनसाथी' },
  'matrix.theme.children': { en: 'Children · progeny', hi: 'संतान · संतति' },
  'matrix.theme.health': { en: 'Health · body', hi: 'स्वास्थ्य · शरीर' },
  'matrix.theme.education': { en: 'Education · learning', hi: 'शिक्षा · विद्या' },
  'matrix.theme.home': { en: 'Home · property', hi: 'गृह · संपत्ति' },
  'matrix.theme.fortune': { en: 'Fortune · dharma · father', hi: 'भाग्य · धर्म · पिता' },
  'matrix.theme.enemies': { en: 'Enemies · disease · debt', hi: 'शत्रु · रोग · ऋण' },
  'matrix.theme.foreign': { en: 'Foreign · loss · mokṣa', hi: 'विदेश · हानि · मोक्ष' },
  'matrix.theme.longevity': { en: 'Longevity', hi: 'आयु' },
  'panchang.house': { en: 'house', hi: 'भाव' },
  'panchang.bhava': { en: 'bhāva', hi: 'भाव' },
  'panchang.sunrise': { en: 'Sunrise · sunset', hi: 'सूर्योदय · सूर्यास्त' },
  'panchang.rahu': { en: 'Rāhu-kāla', hi: 'राहु-काल' },
  'panchang.yama': { en: 'Yama-gaṇḍa', hi: 'यम-गण्ड' },
  'panchang.gulika': { en: 'Gulika', hi: 'गुलिक' },
  'panchang.abhijit': { en: 'Abhijit', hi: 'अभिजित्' },
  'panchang.brahma': { en: 'Brahma-muhūrta', hi: 'ब्रह्म-मुहूर्त' },
  'panchang.band.auspicious': { en: 'auspicious', hi: 'शुभ' },
  'panchang.band.mixed': { en: 'mixed', hi: 'मिश्र' },
  'panchang.band.inauspicious': { en: 'inauspicious', hi: 'अशुभ' },
  'panchang.verdict.favourable': { en: 'favourable', hi: 'अनुकूल' },
  'panchang.verdict.unfavourable': { en: 'unfavourable', hi: 'प्रतिकूल' },
  'panchang.verdict.mixed': { en: 'mixed', hi: 'मिश्र' },
  'panchang.verdict.clean': { en: 'clean', hi: 'निर्दोष' },
  'panchang.verdict.weak': { en: 'weak', hi: 'दुर्बल' },
  'panchang.śukla': { en: 'śukla', hi: 'शुक्ल' },
  'panchang.kṛṣṇa': { en: 'kṛṣṇa', hi: 'कृष्ण' },
  'panchang.birthline': { en: 'Scored for your chart — birth Moon in', hi: 'आपकी कुंडली हेतु — जन्म-चन्द्र' },
  'panchang.loading': { en: 'Computing the month…', hi: 'माह की गणना हो रही है…' },
  'panchang.discl': {
    en: 'Auspiciousness of the day for this chart — a muhūrta guide from classical measures, not a fated verdict. Rāhu-kāla / Yama-gaṇḍa / Gulika are inauspicious; Abhijit / Brahma-muhūrta are auspicious.',
    hi: 'इस कुंडली हेतु दिन की शुभता — शास्त्रीय मापों पर आधारित एक मुहूर्त-मार्गदर्शन, कोई नियति-कथन नहीं। राहु-काल / यम-गण्ड / गुलिक अशुभ हैं; अभिजित् / ब्रह्म-मुहूर्त शुभ हैं।',
  },
  'month.1': { en: 'January', hi: 'जनवरी' }, 'month.2': { en: 'February', hi: 'फ़रवरी' },
  'month.3': { en: 'March', hi: 'मार्च' }, 'month.4': { en: 'April', hi: 'अप्रैल' },
  'month.5': { en: 'May', hi: 'मई' }, 'month.6': { en: 'June', hi: 'जून' },
  'month.7': { en: 'July', hi: 'जुलाई' }, 'month.8': { en: 'August', hi: 'अगस्त' },
  'month.9': { en: 'September', hi: 'सितंबर' }, 'month.10': { en: 'October', hi: 'अक्तूबर' },
  'month.11': { en: 'November', hi: 'नवंबर' }, 'month.12': { en: 'December', hi: 'दिसंबर' },
  'wd.Su': { en: 'Su', hi: 'रवि' }, 'wd.Mo': { en: 'Mo', hi: 'सोम' }, 'wd.Tu': { en: 'Tu', hi: 'मं' },
  'wd.We': { en: 'We', hi: 'बु' }, 'wd.Th': { en: 'Th', hi: 'गु' }, 'wd.Fr': { en: 'Fr', hi: 'शु' },
  'wd.Sa': { en: 'Sa', hi: 'शनि' },
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
