/**
 * "Watch it explained" — a chart explained topic by topic, in plain words.
 *
 * The format follows the simple explainers people already read: one topic at a
 * time ("Marriage and partnership"), the houses that matter in one line, then
 * numbered lines that say what THIS chart has — which sign the house holds,
 * where its lord sits and how strong it is there, which planets sit in it or
 * look at it, and its natural significator. "Signs, not promises."
 *
 * Built ONLY from the chart the API returned; nothing is generated and no
 * reading is invented. The plain lines state the chart's facts and the method
 * that reads them (a house is read through where its lord sits — BPHS ch.24).
 * What a house stands for is drawn from BPHS ch.11's significations, shortened;
 * longevity and one's own death are deliberately left out of the plain labels.
 *
 * What the classical text says about the placement (BPHS ch.24's lord-in-house
 * rule) is NOT in the plain lines: it is behind a click (`text`), in the text's
 * own words, and only when it carries no care-sensitive verdict (a death, a lost
 * child or parent, childlessness, a vice); otherwise the click says where to read
 * it. Nothing in `say` names a book; `cite` shows only with references switched on.
 *
 * Each step: { key, title, chips, lines, text, cite, focus, say } — title, chips,
 * lines and text are per language ({ en, hi }); `say` is the narration (title +
 * lines) for a voice or a presenter; `focus` is what the animated chart lights.
 */
import { makeNamer } from './naming.js'

// sign index 0-11 → its lord (graha key)
const SIGN_LORD = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'saturn', 'jupiter']
const EN_ORD = (n) => `${n}${n % 10 === 1 && n !== 11 ? 'st' : n % 10 === 2 && n !== 12 ? 'nd' : n % 10 === 3 && n !== 13 ? 'rd' : 'th'}`
const HI_ORD = ['', 'पहले', 'दूसरे', 'तीसरे', 'चौथे', 'पाँचवें', 'छठे', 'सातवें', 'आठवें', 'नौवें', 'दसवें', 'ग्यारहवें', 'बारहवें']
const HI_ORD_N = ['', 'पहला', 'दूसरा', 'तीसरा', 'चौथा', 'पाँचवाँ', 'छठा', 'सातवाँ', 'आठवाँ', 'नौवाँ', 'दसवाँ', 'ग्यारहवाँ', 'बारहवाँ']

/** What each house stands for, shortened from BPHS ch.11 (vv.2-13). Longevity (8th) and one's own death (12th) are
 *  left out on purpose; "wife" is the spouse. `of` completes "the house of …"; `chip` is the one-line meaning. */
export const HOUSE = {
  1: { title: { en: 'You: body and nature', hi: 'आप: शरीर और स्वभाव' }, of: { en: 'self and body', hi: 'स्वयं और शरीर' }, chip: { en: 'body, looks, nature, happiness', hi: 'शरीर, रूप, स्वभाव, सुख' } },
  2: { title: { en: 'Wealth and family', hi: 'धन और परिवार' }, of: { en: 'wealth and family', hi: 'धन और परिवार' }, chip: { en: 'wealth, food, family, gems', hi: 'धन, अन्न, परिवार, रत्न' } },
  3: { title: { en: 'Courage and siblings', hi: 'पराक्रम और भाई-बहन' }, of: { en: 'courage and siblings', hi: 'पराक्रम और भाई-बहन' }, chip: { en: 'courage, brothers and sisters, helpers, journeys', hi: 'पराक्रम, भाई-बहन, सहायक, यात्रा' } },
  4: { title: { en: 'Home and mother', hi: 'घर और माता' }, of: { en: 'home and mother', hi: 'घर और माता' }, chip: { en: 'home, mother, vehicles, land, happiness', hi: 'घर, माता, वाहन, भूमि, सुख' } },
  5: { title: { en: 'Children and learning', hi: 'संतान और विद्या' }, of: { en: 'children and learning', hi: 'संतान और विद्या' }, chip: { en: 'children, learning, mantras, authority', hi: 'संतान, विद्या, मंत्र, अधिकार' } },
  6: { title: { en: 'Rivals and health', hi: 'शत्रु और स्वास्थ्य' }, of: { en: 'rivals and health', hi: 'शत्रु और स्वास्थ्य' }, chip: { en: 'rivals, illness, maternal uncle', hi: 'शत्रु, रोग, मामा' } },
  7: { title: { en: 'Marriage and partnership', hi: 'विवाह और साझेदारी' }, of: { en: 'marriage and partnership', hi: 'विवाह और साझेदारी' }, chip: { en: 'spouse, partnership, trade, travel', hi: 'जीवनसाथी, साझेदारी, व्यापार, यात्रा' } },
  8: { title: { en: 'Inheritance and hidden matters', hi: 'विरासत और गूढ़ बातें' }, of: { en: 'inheritance and hidden matters', hi: 'विरासत और गूढ़ बातें' }, chip: { en: 'inheritance, struggles, hidden matters', hi: 'विरासत, संघर्ष, गूढ़ बातें' } },
  9: { title: { en: 'Fortune and faith', hi: 'भाग्य और धर्म' }, of: { en: 'fortune and faith', hi: 'भाग्य और धर्म' }, chip: { en: 'fortune, religion, pilgrimage', hi: 'भाग्य, धर्म, तीर्थ' } },
  10: { title: { en: 'Career and status', hi: 'कर्म और प्रतिष्ठा' }, of: { en: 'career and status', hi: 'कर्म और प्रतिष्ठा' }, chip: { en: 'profession, authority, honour, father, living abroad', hi: 'आजीविका, अधिकार, सम्मान, पिता, विदेश-वास' } },
  11: { title: { en: 'Income and gains', hi: 'आय और लाभ' }, of: { en: 'income and gains', hi: 'आय और लाभ' }, chip: { en: 'income, gains, prosperity', hi: 'आय, लाभ, समृद्धि' } },
  12: { title: { en: 'Expenses', hi: 'व्यय' }, of: { en: 'expenses', hi: 'व्यय' }, chip: { en: 'expenses', hi: 'व्यय, खर्च' } },
}

/** A nakṣatra's muhūrta class (chart payload `quality`, api/nakshatra_attrs.py), in a word. */
const NAK_CLASS = {
  Soft: { en: 'soft', hi: 'मृदु' }, Light: { en: 'light, swift', hi: 'क्षिप्र' }, Fixed: { en: 'fixed', hi: 'ध्रुव' },
  Mutable: { en: 'moving', hi: 'चर' }, Mixed: { en: 'mixed', hi: 'मिश्र' }, Fierce: { en: 'fierce', hi: 'उग्र' }, Sharp: { en: 'sharp', hi: 'तीक्ष्ण' },
}
const STRONG = ['exalted', 'moolatrikona', 'own']

/** A planet's standing in its sign, one idea a sentence (the planet topics). P = planet, S = sign. */
const SIGN_STANDING = {
  exalted: { en: (P, S) => `${P} is exalted in ${S}. This is its strongest sign.`, hi: (P, S) => `${P} ${S} में उच्च के हैं। यह उनकी सबसे बलवान राशि है।` },
  moolatrikona: { en: (P, S) => `${P} is in its mūlatrikoṇa part of ${S}. This is a very strong position.`, hi: (P, S) => `${P} ${S} में अपने मूलत्रिकोण में हैं। यह बहुत बलवान स्थिति है।` },
  own: { en: (P, S) => `${S} is the own sign of ${P}. This is a strong position.`, hi: (P, S) => `${S} ${P} की अपनी राशि है। यह बलवान स्थिति है।` },
  friend: { en: (P, S) => `${S} is a friend’s sign for ${P}. This is a comfortable position.`, hi: (P, S) => `${S} ${P} के मित्र की राशि है। यह सहज स्थिति है।` },
  neutral: { en: (P, S) => `${S} is a neutral sign for ${P}.`, hi: (P, S) => `${S} ${P} के लिए सम राशि है।` },
  enemy: { en: (P, S) => `${S} is an enemy’s sign for ${P}. This is an uncomfortable position.`, hi: (P, S) => `${S} ${P} के शत्रु की राशि है। यह असहज स्थिति है।` },
  debilitated: { en: (P, S) => `${P} is debilitated in ${S}. This is its weakest sign.`, hi: (P, S) => `${P} ${S} में नीच के हैं। यह उनकी सबसे दुर्बल राशि है।` },
}
/** The five Bālādi stages, in the order the text names them (BPHS ch.45 v.3). */
const STAGE = {
  bala: { en: 'Bala', hi: 'बाल', nth: { en: 'first', hi: 'पहली' } },
  kumara: { en: 'Kumara', hi: 'कुमार', nth: { en: 'second', hi: 'दूसरी' } },
  yuva: { en: 'Yuva', hi: 'युवा', nth: { en: 'third', hi: 'तीसरी' } },
  vriddha: { en: 'Vriddha', hi: 'वृद्ध', nth: { en: 'fourth', hi: 'चौथी' } },
  mrita: { en: 'Mrita', hi: 'मृत', nth: { en: 'last', hi: 'अंतिम' } },
}
/** The grade of results the text gives each stage (ch.45 v.4), in its own words: "a planet in this stage gives …". */
const GRADE = {
  one_fourth: { en: 'one fourth of its results', hi: 'चौथाई फल देता है' },
  half: { en: 'half of its results', hi: 'आधा फल देता है' },
  full: { en: 'its full results', hi: 'पूरा फल देता है' },
  negligible: { en: 'negligible results', hi: 'नगण्य फल देता है' },
  nil: { en: 'no results', hi: 'कोई फल नहीं देता' },
}
/** What each planet usually stands for — OUR words (synthesis), the owner's choice of 2026-11-16 ("Our words,
 *  labelled"). It is from no registered text, so the line that uses it always opens by saying so and every claim
 *  carries "usually". Qualities only: never an event, a date, a person's fate or anything the CARE list holds back. */
export const NATURE = {
  sun: { en: 'authority, confidence and recognition', hi: 'अधिकार, आत्मविश्वास और मान' },
  moon: { en: 'feelings, care and peace of mind', hi: 'भावना, स्नेह और मन की शांति' },
  mars: { en: 'energy, drive and action', hi: 'ऊर्जा, जोश और पहल' },
  mercury: { en: 'thinking, speech and skill', hi: 'सोच, वाणी और कौशल' },
  jupiter: { en: 'knowledge, guidance and growth', hi: 'ज्ञान, मार्गदर्शन और वृद्धि' },
  venus: { en: 'comfort, affection and art', hi: 'सुख, स्नेह और कला' },
  saturn: { en: 'discipline, patience and slow, steady work', hi: 'अनुशासन, धैर्य और धीमे, स्थिर काम' },
  rahu: { en: 'ambition, restlessness and unusual paths', hi: 'महत्वाकांक्षा, बेचैनी और अलग राह' },
  ketu: { en: 'detachment, inward focus and letting go', hi: 'विरक्ति, अंतर्मुखता और त्याग' },
}
export const OURS = { en: 'Our reading, not from a classical text:', hi: 'हमारा पाठ, किसी ग्रंथ का नहीं:' }

/** The five "great person" yogas: a planet in its own or exalted sign, in a kendra (BPHS ch.75 vv.1-2). */
const MAHA = {
  mars: { en: 'Ruchaka', hi: 'रुचक' }, mercury: { en: 'Bhadra', hi: 'भद्र' }, jupiter: { en: 'Hamsa', hi: 'हंस' },
  venus: { en: 'Malavya', hi: 'मालव्य' }, saturn: { en: 'Sasa', hi: 'शश' },
}

/** A lord-in-house rule that speaks of a death, a lost child or parent, childlessness, many wives or a vice is not
 *  put in front of a reader in a plain summary; the Bhāvas panel carries it, in the text's own words. Both languages. */
export const CARE = {
  en: /\b(death|die[sd]?|dead|lose[sr]?|loss|deprived|bereft|devoid|childless|progeny|sons?|wives|wife|thie(f|ves)|tortur\w*|vices?|short-lived|poverty|disease|widow\w*|betray\w*|wicked|females?)\b/i,
  hi: /संतान|पुत्र|पत्नी|पत्नि|मृत्यु|मरण|नाश|वंचित|रहित|चोर|पीड़|दुर्व्यसन|अल्पायु|रोग|दरिद्र|विश्वासघात|स्त्रियों/,
}

const list = (xs, lang) => (xs.length < 2 ? xs.join('') : `${xs.slice(0, -1).join(', ')} ${lang === 'hi' ? 'और' : 'and'} ${xs[xs.length - 1]}`)
const MONTHS_HI = ['जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर']
const MONTHS_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
// "2012-10-25 20:25" → "Oct 2012" / "अक्टूबर 2012" (read off the string: no time zone can shift it)
const monthYear = (s, lang) => {
  const m = /^(\d{4})-(\d{2})/.exec(String(s || ''))
  return m ? `${(lang === 'hi' ? MONTHS_HI : MONTHS_EN)[+m[2] - 1]} ${m[1]}` : ''
}
const houseOf = (sign, lagna) => ((sign - lagna + 12) % 12) + 1

/** The current Viṁśottarī mahādaśā and antardaśā, from the variant the chart reckons by default. */
function currentDasha(chart) {
  const dv = chart.dasha && chart.dasha.variants
  if (!dv) return null
  const tree = dv[String(chart.dasha.default_year_days)] || dv['360'] || Object.values(dv)[0]
  const maha = tree && (tree.mahadashas || []).find((m) => m.is_current)
  if (!maha) return null
  const antar = (maha.sub || []).find((x) => x.is_current) || null
  return { maha, antar, cite: tree.citation || null }
}

/**
 * @param chart  the /api/chart payload (a snapshot works too)
 * @param namer  the reader's name style (naming.js) for English; Hindi is always in Devanāgarī
 * @returns      { steps }
 */
export function buildWalkthrough(chart, namer = makeNamer('common')) {
  const H = makeNamer('devanagari'), E = makeNamer('english')
  const N = { en: namer, hi: H }
  const plainEn = namer.style === 'english'
  const lagna = chart.lagna_rasi
  const g = (k) => (chart.grahas || []).find((x) => x.key === k)
  const a = chart.analysis && !chart.analysis.error ? chart.analysis : {}
  const bhavas = (a.bhava_phala && a.bhava_phala.bhavas) || []
  const name = (l, k) => N[l].grahaKey(k)
  // in English a Sanskrit name carries its English one the first time a step uses it: "Guru (Jupiter)"
  const fold = (s) => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
  const named = (l, k) => (l === 'en' && !plainEn && fold(namer.grahaKey(k)) !== fold(E.grahaKey(k)) ? `${namer.grahaKey(k)} (${E.grahaKey(k)})` : name(l, k))
  const sign = (l, i) => (l === 'en' && !plainEn ? `${namer.rasi(i)} (${namer.rasiEnglish(i)})` : N[l].rasi(i))
  const nak = (l, x) => N[l].nakshatra(x.nakshatra)
  const cls = (l, x) => (x.nakshatra && NAK_CLASS[x.nakshatra.quality] ? NAK_CLASS[x.nakshatra.quality][l] : '')
  const ord = (l, h) => (l === 'hi' ? HI_ORD[h] : EN_ORD(h))
  const ruled = (k) => Array.from({ length: 12 }, (_, i) => i + 1).filter((h) => SIGN_LORD[(lagna + h - 1) % 12] === k)
  const steps = []
  const push = (key, build, focus, cite = null) => {
    const per = { en: build('en'), hi: build('hi') }
    steps.push({
      key, focus, cite,
      title: { en: per.en.title, hi: per.hi.title },
      chips: { en: per.en.chips || [], hi: per.hi.chips || [] },
      lines: { en: per.en.lines, hi: per.hi.lines },
      text: per.en.text ? { en: per.en.text, hi: per.hi.text } : null,
      say: { en: [per.en.title, ...per.en.lines].join('. ').replace(/\.\./g, '.'), hi: [per.hi.title, ...per.hi.lines].join('। ').replace(/।।/g, '।') },
    })
  }
  /** A planet's standing where it sits, a sentence an idea: sign strength, retrograde, its nakṣatra and the nakṣatra's class. */
  const standing = (l, x) => {
    const P = name(l, x.key), S = N[l].rasi(x.rasi), c = cls(l, x)
    const st = x.dignity && SIGN_STANDING[x.dignity.state]
    return [
      st ? st[l](P, S) : (l === 'hi' ? `${P} ${S} राशि में हैं।` : `${P} is in ${S}.`),
      x.retrograde && x.key !== 'rahu' && x.key !== 'ketu' && (l === 'hi' ? `${P} वक्री हैं।` : `${P} is retrograde.`),
      x.nakshatra && (l === 'hi' ? `${P} ${nak(l, x)} नक्षत्र में हैं।` : `${P} is in the nakṣatra ${nak(l, x)}.`),
      x.nakshatra && c && (l === 'hi' ? `यह ${c} नक्षत्र है।` : `This is a ${c} nakṣatra.`),
    ].filter(Boolean).join(' ')
  }
  const strongWord = {
    exalted: { en: 'is exalted', hi: 'उच्च के हैं' }, moolatrikona: { en: 'is in its mūlatrikoṇa', hi: 'अपने मूलत्रिकोण में हैं' }, own: { en: 'is in its own sign', hi: 'अपनी राशि में हैं' },
  }

  // ── 1. the chart in one minute ──────────────────────────────────────────────
  const mo = g('moon'), su = g('sun'), nk = chart.lagna_nakshatra
  const strong = STRONG.flatMap((st) => (chart.grahas || []).filter((x) => x.dignity && x.dignity.state === st))
  const weak = (chart.grahas || []).filter((x) => x.dignity && x.dignity.state === 'debilitated')
  push('basics', (l) => ({
    title: l === 'hi' ? 'एक मिनट में आपकी कुंडली' : 'Your chart in one minute',
    chips: [
      { label: l === 'hi' ? 'लग्न' : 'Lagna', text: l === 'hi' ? 'आप, पहला भाव' : 'you, the 1st house' },
      { label: name(l, 'moon'), text: l === 'hi' ? 'मन' : 'the mind' },
      { label: name(l, 'sun'), text: l === 'hi' ? 'आत्मा' : 'the soul' },
    ],
    lines: [
      l === 'hi'
        ? `आपका लग्न ${sign(l, lagna)} है। लग्न वह राशि है जो आपके जन्म के समय पूर्व में उदित थी। यह आपका पहला भाव है। बाकी भाव इसी से गिने जाते हैं।${nk ? ` लग्न ${N.hi.nakshatra(nk)} नक्षत्र में है।` : ''}`
        : `Your Lagna is ${sign(l, lagna)}. The Lagna is the sign that was rising at your birth. It is your 1st house. The other houses are counted from it.${nk ? ` The Lagna is in the nakṣatra ${namer.nakshatra(nk)}.` : ''}`,
      mo && (l === 'hi'
        ? `आपका चन्द्र ${sign(l, mo.rasi)} राशि में, ${nak(l, mo)} नक्षत्र में है। ये आपकी जन्म-राशि और आपका जन्म-नक्षत्र हैं।`
        : `Your ${named(l, 'moon')} is in ${sign(l, mo.rasi)}, in the nakṣatra ${nak(l, mo)}. These are your birth sign and your birth nakṣatra.`),
      su && (l === 'hi' ? `आपका सूर्य ${sign(l, su.rasi)} राशि में, आपके ${HI_ORD[su.bhava]} भाव में है।` : `Your ${named(l, 'sun')} is in ${sign(l, su.rasi)}, in your ${EN_ORD(su.bhava)} house.`),
      strong.length > 0 && (l === 'hi'
        ? `${strong.length > 1 ? 'ये ग्रह अपनी राशि से बलवान हैं।' : 'एक ग्रह अपनी राशि से बलवान है।'} ${strong.map((x) => `${name(l, x.key)} ${strongWord[x.dignity.state].hi}।`).join(' ')}`
        : `${strong.length > 1 ? 'These planets are strong by sign.' : 'One planet is strong by sign.'} ${strong.map((x) => `${name(l, x.key)} ${strongWord[x.dignity.state].en}.`).join(' ')}`),
      weak.length > 0 && (l === 'hi'
        ? weak.map((x) => `${name(l, x.key)} नीच के हैं। यह उनकी सबसे दुर्बल राशि है।`).join(' ')
        : weak.map((x) => `${name(l, x.key)} is debilitated. This is its weakest sign.`).join(' ')),
    ].filter(Boolean),
  }), { houses: [1, mo && mo.bhava, su && su.bhava].filter(Boolean), main: 1, grahas: ['moon', 'sun', ...strong.map((x) => x.key)], lines: [] })

  // ── 1b. the nine planets, one topic each ────────────────────────────────────
  // Written to fixed sentence patterns (the owner's brief, 2026-11-16, after ASD-STE100): one idea a sentence, at
  // most 25 words, each term used one way, a line left out when the chart gives no value for it. Every slot is
  // filled from the payload. The placement is read the way the house topics read it (what the planet rules is
  // tied to where it sits). ONE line is ours and says so (OURS + NATURE): what the planet usually stands for and
  // the area of life its house holds — no registered text gives a trait for these lines. The stage (Bālādi) and its grade are the engine's, from analysis.grahas.
  const lagnaLord = SIGN_LORD[lagna]
  const ORDER = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu']
  const stageOf = (k) => {
    const s = ((a.grahas && a.grahas[k]) || []).find((x) => x && x.name === 'baladi' && x.available !== false)
    return s && STAGE[s.value] ? { state: s.value, grade: (s.detail && s.detail.grade) || s.scale, cite: s.citation } : null
  }
  const detected = (a.yogas && a.yogas.detected) || null
  for (const k of [lagnaLord, ...ORDER.filter((x) => x !== lagnaLord)]) {
    const x = g(k)
    if (!x || !HOUSE[x.bhava]) continue
    const h = x.bhava, r = ruled(k), others = r.filter((q) => q !== h)
    const mates = (chart.grahas || []).filter((y) => y.bhava === h && y.key !== k).map((y) => y.key)
    const st = stageOf(k)
    const node = k === 'rahu' || k === 'ketu'   // the nodes rule no sign and carry no sign strength
    const dg = !node && x.dignity && SIGN_STANDING[x.dignity.state] ? x.dignity.state : null
    const yoga = MAHA[k] && detected ? { ...MAHA[k], on: detected.some((y) => String(y.name || '').startsWith(MAHA[k].en)), cite: (detected.find((y) => String(y.name || '').startsWith(MAHA[k].en)) || {}).citation } : null
    const kendra = [1, 4, 7, 10].includes(h), strong = STRONG.includes(dg)
    const deg = Math.floor(Number(x.degree) || 0)
    push(`graha_${k}`, (l) => {
      const P = name(l, k), S = N[l].rasi(x.rasi), hi = l === 'hi'
      const yogaLine = !yoga ? null
        : yoga.on
          ? (hi ? `${P} ${yoga.hi} योग बनाते हैं। वे अपनी या उच्च राशि में हैं, और केंद्र भाव में हैं।` : `${P} forms ${yoga.en} Yoga. It is in its own or exalted sign, in a Kendra house.`)
          : strong && !kendra
            ? (hi ? `${P} ${yoga.hi} योग नहीं बनाते। इस योग के लिए केंद्र भाव चाहिए: पहला, चौथा, सातवाँ या दसवाँ।` : `${P} forms no ${yoga.en} Yoga. That yoga needs a Kendra house: the 1st, 4th, 7th or 10th.`)
            : kendra && !strong && dg
              ? (hi ? `${P} ${yoga.hi} योग नहीं बनाते। इस योग के लिए ग्रह अपनी या उच्च राशि में चाहिए।` : `${P} forms no ${yoga.en} Yoga. That yoga needs the planet in its own or exalted sign.`)
              : null
      return {
        title: hi ? `${P} · ${deg}° ${S}, ${HI_ORD_N[h]} भाव` : `${named(l, k)} · ${deg}° ${S}, ${EN_ORD(h)} house`,
        chips: st ? [{ label: hi ? 'अवस्था' : 'Stage', text: hi ? 'राशि में ग्रह के अंश से तय होती है' : 'set by the planet’s degree in its sign' }] : [],
        lines: [
          hi ? `${P} ${sign(l, x.rasi)} राशि में, आपके ${HI_ORD[h]} भाव में हैं। ${HI_ORD_N[h]} भाव ${HOUSE[h].of.hi} का भाव है।`
            : `${named(l, k)} is in ${sign(l, x.rasi)} in your ${EN_ORD(h)} house. The ${EN_ORD(h)} house is the house of ${HOUSE[h].of.en}.`,
          [
            r.length
              ? (hi ? `${P} आपके ${list(r.map((q) => HI_ORD[q]), l)} भाव के स्वामी हैं।` : `${P} rules your ${r.map((q) => `${EN_ORD(q)} house`).join(' and your ')}.`)
              : (hi ? `${P} किसी राशि के स्वामी नहीं हैं।` : `${P} rules no sign.`),
            k === lagnaLord && (hi ? `पहला भाव आपका लग्न है, इसलिए ${P} आपके लग्न के स्वामी हैं।` : `The 1st house is your Lagna, so ${P} is the lord of your Lagna.`),
            r.includes(h) && (hi ? `${P} अपने ही भाव में बैठे हैं।` : `${P} sits in a house that it rules.`),
            ...others.map((q, i) => (hi
              ? (i === 0 ? `यह स्थिति ${HOUSE[q].of.hi} को ${HOUSE[h].of.hi} से जोड़ती है।` : `यह ${HOUSE[q].of.hi} को भी ${HOUSE[h].of.hi} से जोड़ती है।`)
              : (i === 0 ? `This placement ties ${HOUSE[q].of.en} to ${HOUSE[h].of.en}.` : `It also ties ${HOUSE[q].of.en} to ${HOUSE[h].of.en}.`))),
          ].filter(Boolean).join(' '),
          NATURE[k] && (hi
            ? `${OURS.hi} ${P} प्रायः ${NATURE[k].hi} के सूचक हैं। आपके ${HI_ORD[h]} भाव में यह प्रायः ${HOUSE[h].of.hi} में दिखता है।`
            : `${OURS.en} ${P} usually stands for ${NATURE[k].en}. In your ${EN_ORD(h)} house, this usually shows in ${HOUSE[h].of.en}.`),
          dg && SIGN_STANDING[dg][l](P, S),
          !node && x.retrograde && (hi ? `${P} वक्री हैं।` : `${P} is retrograde.`),
          st && [
            hi ? `${P} ${S} के ${deg} अंश पर हैं। यह ${STAGE[st.state].hi} अवस्था है, पाँच अवस्थाओं में ${STAGE[st.state].nth.hi}।`
              : `${P} is at ${deg} degrees of ${S}. This is the ${STAGE[st.state].en} stage, the ${STAGE[st.state].nth.en} of the five stages.`,
            GRADE[st.grade] && (hi ? `शास्त्रीय नियम के अनुसार इस अवस्था का ग्रह ${GRADE[st.grade].hi}। बल के और भी माप हैं।`
              : `By the classical rule, a planet in this stage gives ${GRADE[st.grade].en}. Strength has other measures too.`),
          ].filter(Boolean).join(' '),
          mates.length > 0 && (hi ? `${P} इस भाव में ${list(mates.map((m) => name(l, m)), l)} के साथ बैठे हैं।` : `${P} sits with ${list(mates.map((m) => name(l, m)), l)} in this house.`),
          yogaLine,
        ].filter(Boolean),
      }
    }, {
      main: h,
      houses: [...new Set([h, ...r])],
      grahas: [k, ...mates],
      lines: others.map((q) => ({ from: q, to: h, kind: 'lord' })),
    }, [st && st.cite, yoga && yoga.on && yoga.cite].filter(Boolean).join(' · ') || null)
  }

  // ── 2. the twelve houses, one topic each ────────────────────────────────────
  for (const b of bhavas) {
    const h = b.house, T = HOUSE[h]
    if (!T) continue
    const lord = g(b.lord), lh = b.lord_in_house
    const occ = (b.occupants || []).map(g).filter(Boolean)
    const rest = occ.filter((x) => !(lh === h && x.key === b.lord))
    // fully and three-quarters only: the lighter graded aspects (½, ¼) are on the Aspects card, not in a plain summary
    const full = (b.aspects_in || []).filter((x) => x.strength >= 1).map((x) => x.graha)
    const part = (b.aspects_in || []).filter((x) => x.strength >= 0.75 && x.strength < 1).map((x) => x.graha)
    const kar = b.karaka && b.karaka !== b.lord ? g(b.karaka) : null
    const rule = b.lord_rule && b.lord_rule.effect
    const clean = rule && !CARE.en.test(rule) && !CARE.hi.test(rule)
    push(`house${h}`, (l) => ({
      title: T.title[l],
      chips: [
        { label: l === 'hi' ? `${HI_ORD_N[h]} भाव` : `${EN_ORD(h)} house`, text: T.chip[l] },
        ...(b.karaka ? [{ label: name(l, b.karaka), text: l === 'hi' ? 'इसका नैसर्गिक कारक' : 'its natural significator' }] : []),
      ],
      lines: [
        l === 'hi'
          ? `आपका ${HI_ORD_N[h]} भाव ${sign(l, b.sign)} राशि है। इसके स्वामी ${name(l, b.lord)} हैं।`
          : `Your ${EN_ORD(h)} house is ${sign(l, b.sign)}. ${named(l, b.lord)} rules this sign.`,
        lh === h
          ? (l === 'hi' ? `${name(l, b.lord)} इसी भाव में बैठे हैं। भाव का स्वामी अपने ही घर में है।` : `${name(l, b.lord)} sits in this house. The lord of the house is in its own house.`)
          : (l === 'hi'
            ? `${name(l, b.lord)} आपके ${HI_ORD[lh]} भाव में बैठे हैं। ${HI_ORD_N[lh]} भाव ${HOUSE[lh].of.hi} का भाव है। यह ${T.of.hi} को ${HOUSE[lh].of.hi} से जोड़ता है।`
            : `${name(l, b.lord)} sits in your ${EN_ORD(lh)} house. The ${EN_ORD(lh)} house is the house of ${HOUSE[lh].of.en}. This ties ${T.of.en} to ${HOUSE[lh].of.en}.`),
        lord && standing(l, lord),
        // the lord at home was just named: it is not said twice
        rest.length
          ? (l === 'hi'
            ? `${list(rest.map((x) => name(l, x.key)), l)} ${lh === h ? 'भी ' : ''}इस भाव में बैठे हैं।`
            : `${list(rest.map((x) => name(l, x.key)), l)} ${lh === h ? 'also ' : ''}${rest.length > 1 ? 'sit' : 'sits'} in this house.`)
          : lh === h
            ? (l === 'hi' ? 'इस भाव में और कोई ग्रह नहीं बैठा।' : 'No other planet sits in this house.')
            : (l === 'hi' ? 'इस भाव में कोई ग्रह नहीं बैठा।' : 'No planet sits in this house.'),
        full.length || part.length
          ? [
            full.length && (l === 'hi' ? `${list(full.map((k) => name(l, k)), l)} इस भाव को पूर्ण दृष्टि से देखते हैं।` : `${list(full.map((k) => name(l, k)), l)} ${full.length > 1 ? 'look' : 'looks'} at this house with a full aspect.`),
            part.length && (l === 'hi' ? `${list(part.map((k) => name(l, k)), l)} इस भाव को तीन-चौथाई दृष्टि से देखते हैं।` : `${list(part.map((k) => name(l, k)), l)} ${part.length > 1 ? 'look' : 'looks'} at this house with a three-quarter aspect.`),
          ].filter(Boolean).join(' ')
          : (l === 'hi' ? 'कोई ग्रह इस भाव को पूर्ण दृष्टि से नहीं देखता।' : 'No planet looks at this house fully.'),
        kar && (l === 'hi'
          ? `${name(l, kar.key)} इस भाव के नैसर्गिक कारक हैं। वे आपके ${HI_ORD[kar.bhava]} भाव में, ${sign(l, kar.rasi)} राशि में हैं।`
          : `${named(l, kar.key)} is the natural significator of this house. It sits in your ${EN_ORD(kar.bhava)} house, in ${sign(l, kar.rasi)}.`),
      ].filter(Boolean),
      text: rule
        ? (clean
          ? { quote: rule, note: l === 'hi' ? 'शास्त्र के अपने (पुराने) शब्द — भविष्यवाणी नहीं।' : 'The text’s own, dated words.' }
          : { quote: null, note: l === 'hi' ? 'इस स्थिति का शास्त्रीय नियम ‘भाव व योग’ खंड में है, शास्त्र के अपने शब्दों में।' : 'The classical rule for this placement is in the Bhāvas & Yogas section, in the text’s own words.' })
        : null,
    }), {
      main: h,
      houses: [...new Set([h, lh])],
      grahas: [...new Set([b.lord, ...occ.map((x) => x.key), ...(kar ? [kar.key] : [])])],
      lines: [
        ...(lh && lh !== h ? [{ from: h, to: lh, kind: 'lord' }] : []),
        // one line per house an aspect comes from (two grahas in one house cast along the same line)
        ...[...new Map([...part, ...full].map((k) => [g(k) && g(k).bhava, { from: g(k) && g(k).bhava, to: h, kind: full.includes(k) ? 'full' : 'part' }])).values()]
          .filter((x) => x.from && x.from !== h),
      ],
    }, [b.significations && b.significations.citation, b.lord_rule && b.lord_rule.citation].filter(Boolean).join(' · ') || null)
  }

  // ── 3. what is running now (not for a chart shared without its birth details: it has no daśā) ──
  const dsh = currentDasha(chart)
  if (dsh) {
    const { maha, antar } = dsh
    const about = (l, k) => {
      const x = g(k), r = ruled(k)
      if (!x) return ''
      return l === 'hi'
        ? (r.length
          ? `${name(l, k)} आपके ${list(r.map((h) => HI_ORD[h]), l)} भाव के स्वामी हैं। वे आपके ${HI_ORD[x.bhava]} भाव में बैठे हैं।`
          : `${name(l, k)} किसी राशि के स्वामी नहीं हैं। वे आपके ${HI_ORD[x.bhava]} भाव में बैठे हैं।`)
        : (r.length
          ? `${name(l, k)} rules your ${r.map((h) => `${EN_ORD(h)} house`).join(' and your ')}. It sits in your ${EN_ORD(x.bhava)} house.`
          : `${name(l, k)} rules no sign. It sits in your ${EN_ORD(x.bhava)} house.`)
    }
    push('now', (l) => ({
      title: l === 'hi' ? 'अभी क्या चल रहा है' : 'What is running now',
      chips: [{ label: l === 'hi' ? 'दशा' : 'Daśā', text: l === 'hi' ? 'समय की खिड़की, घटना नहीं' : 'a window of time, not an event' }],
      lines: [
        l === 'hi'
          ? `आप ${name(l, maha.lord)} की महादशा में हैं। यह ${monthYear(maha.start, l)} से ${monthYear(maha.end, l)} तक चलती है।`
          : `You are in the main period (mahādaśā) of ${named(l, maha.lord)}. It runs from ${monthYear(maha.start, l)} to ${monthYear(maha.end, l)}.`,
        about(l, maha.lord),
        antar && (l === 'hi'
          ? `उसके भीतर ${name(l, antar.lord)} की अंतर्दशा ${monthYear(antar.end, l)} तक है।${antar.lord === maha.lord ? '' : ` ${about(l, antar.lord)}`}`
          : `Within it, the sub-period of ${named(l, antar.lord)} runs until ${monthYear(antar.end, l)}.${antar.lord === maha.lord ? '' : ` ${about(l, antar.lord)}`}`),
        l === 'hi'
          ? 'दशा अपने ग्रह के भावों की बातों को आगे लाती है। ये वे भाव हैं जिनका वह स्वामी है और जिसमें वह बैठा है।'
          : 'A period brings forward the matters of the houses that its planet rules and sits in.',
      ].filter(Boolean),
    }), {
      main: g(maha.lord)?.bhava,
      houses: [...new Set([g(maha.lord)?.bhava, ...ruled(maha.lord), antar && g(antar.lord)?.bhava].filter(Boolean))],
      grahas: [maha.lord, antar && antar.lord].filter(Boolean),
      lines: [],
    }, dsh.cite)
  }

  // ── 4. the close ────────────────────────────────────────────────────────────
  push('close', (l) => ({
    title: l === 'hi' ? 'संकेत, वादे नहीं' : 'Signs, not promises',
    lines: l === 'hi'
      ? ['यह आपकी कुंडली थी, भाव-दर-भाव। हर पंक्ति इस पर टिकी है कि आपके ग्रह कहाँ बैठे हैं।', 'उनके पीछे के शास्त्रीय नियम ‘भाव व योग’ खंड में हैं, शास्त्र के अपने शब्दों में। समय दशाओं से आता है। प्रयास सदा मायने रखता है।']
      : ['That is your chart, house by house. Every line rests on where your planets stand.', 'The classical rules behind them are in the Bhāvas & Yogas section, in the words of the texts. Timing comes from the daśās. Effort always matters.'],
  }), { houses: [], grahas: [], lines: [] })

  return { steps }
}

/** The spoken script as plain text — one paragraph a step — for a narrator or a presenter to read. */
export const spokenScript = (steps, lang = 'en') => steps.map((s) => s.say[lang] || s.say.en).join('\n\n')

/** Seconds a step stays on screen when nothing is speaking it: a calm reading pace, never under eight. */
export const readSeconds = (text) => Math.max(8, Math.round(String(text || '').split(/\s+/).length / 2.4))
