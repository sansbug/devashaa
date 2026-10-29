/**
 * The chart walkthrough — the script a narrated, animated tour of one chart
 * plays from.
 *
 * Built ONLY from the chart the API returned: no free text is generated and no
 * reading is invented. Each step is
 *
 *   say    { en, hi } — what is spoken (and captioned): the chart's own facts
 *          and the method that reads them. It names no book (references stay
 *          behind the switch, as everywhere on the site), and it never reads out
 *          a verdict — a lord-in-house rule or a planet-in-house reading can
 *          state a death, a lost child, a short life, and those stay on the
 *          panels, as the text's dated view, where they are read in context.
 *   quote  — on screen only, never spoken: a yoga's cited effect, exactly as the
 *          Yogas panel shows it.
 *   cite   — the locus of the rule the step leans on; shown only with
 *          references switched on.
 *   focus  — what the chart lights up: houses (1–12, outlined — never tinted),
 *          grahas, lines from one house to another (the lagna lord, aspects).
 *
 * The order follows the reading guide's method — lagna, its lord, the Moon,
 * dignity, aspects, yogas, the kāraka of the self, timing — told on THIS
 * chart. A chart shared without its birth details has no daśā, and that step
 * is left out. The spoken script (`spokenScript`) is plain text, one paragraph
 * a step, for a narrator or a presenter (an avatar) to read.
 */
import { makeNamer } from './naming.js'

// sign index 0-11 → its lord (graha key)
const SIGN_LORD = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'saturn', 'jupiter']
const EN_ORD = (n) => `${n}${n % 10 === 1 && n !== 11 ? 'st' : n % 10 === 2 && n !== 12 ? 'nd' : n % 10 === 3 && n !== 13 ? 'rd' : 'th'}`
// oblique ordinals, as in "पाँचवें भाव में"
const HI_ORD = ['', 'पहले', 'दूसरे', 'तीसरे', 'चौथे', 'पाँचवें', 'छठे', 'सातवें', 'आठवें', 'नौवें', 'दसवें', 'ग्यारहवें', 'बारहवें']
const DIGNITY = {
  exalted: { en: 'exalted — at its strongest', hi: 'उच्च के हैं — अपनी सबसे बलवान स्थिति में' },
  debilitated: { en: 'debilitated — at its weakest', hi: 'नीच के हैं — अपनी सबसे दुर्बल स्थिति में' },
  moolatrikona: { en: 'in its mūlatrikoṇa sign — very strong', hi: 'मूलत्रिकोण में हैं — बहुत बलवान' },
  own: { en: 'in its own sign — strong', hi: 'स्वराशि के हैं — बलवान' },
}
const DIGNITY_ORDER = ['exalted', 'debilitated', 'moolatrikona', 'own']
// "a, b and c" / "क, ख और ग"
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
  const antar = (maha.sub || []).find((a) => a.is_current) || null
  return { maha, antar, cite: tree.citation || null }
}

/**
 * @param chart  the /api/chart payload (a snapshot works too)
 * @param namer  the reader's name style (naming.js) for the English script; Hindi is always in Devanāgarī
 * @returns      { steps: [{ key, say: {en, hi}, quote, cite, focus: {houses, grahas, lines, sweep} }] }
 */
export function buildWalkthrough(chart, namer = makeNamer('common')) {
  const H = makeNamer('devanagari'), E = makeNamer('english')
  const N = { en: namer, hi: H }
  const lagna = chart.lagna_rasi
  const g = (k) => (chart.grahas || []).find((x) => x.key === k)
  // in English, a Sanskrit name carries its English one on first mention: "Guru (Jupiter)"
  const name = (lang, k) => N[lang].grahaKey(k)
  const named = (lang, k) => (lang === 'en' && namer.style !== 'english' ? `${namer.grahaKey(k)} (${E.grahaKey(k)})` : name(lang, k))
  const sign = (lang, i) => (lang === 'en' && namer.style !== 'english' ? `${namer.rasi(i)} (${namer.rasiEnglish(i)})` : N[lang].rasi(i))
  const a = chart.analysis && !chart.analysis.error ? chart.analysis : {}
  const citeOf = (k, field) => ((a.grahas && a.grahas[k]) || []).find((e) => e.name === field)?.citation || null
  const both = (f) => ({ en: f('en'), hi: f('hi') })
  const steps = []

  // 1 — the frame
  steps.push({
    key: 'frame',
    say: {
      en: 'This is the rāśi chart, drawn in the North Indian style. Its twelve compartments are the twelve houses — the bhāvas. The top diamond is the 1st house; the others follow it anticlockwise, and the number in each is the sign that falls in it.',
      hi: 'यह उत्तर भारतीय शैली में बनी राशि-कुंडली है। इसके बारह खाने बारह भाव हैं। ऊपर बीच का खाना पहला भाव है; बाकी भाव उसके बाद वामावर्त — घड़ी की उलटी दिशा में — चलते हैं, और हर खाने का अंक उसमें पड़ी राशि का है।',
    },
    quote: null, cite: null,
    focus: { houses: [], grahas: [], lines: [], sweep: true },
  })

  // 2 — the lagna
  const nk = chart.lagna_nakshatra
  steps.push({
    key: 'lagna',
    say: both((l) => (l === 'hi'
      ? `पहला भाव लग्न है — जन्म के क्षण पूर्व में उदित होती राशि। यहाँ लग्न ${sign(l, lagna)} है${nk ? `, ${N.hi.nakshatra(nk)} नक्षत्र में (पाद ${nk.pada})` : ''}। भाव इसी से गिने जाते हैं, और शास्त्र के नियम लग्न से बँधे हैं — "सूर्य राशि" से नहीं।`
      : `The 1st house is the lagna — the sign rising in the east at the moment of birth. Here it is ${sign(l, lagna)}${nk ? `, in pāda ${nk.pada} of the nakṣatra ${namer.nakshatra(nk)}` : ''}. The houses are counted from it, and the classical rules are keyed to it — not to a "sun sign".`)),
    quote: null, cite: 'BPHS Vol I, ch.34',
    focus: { houses: [1], grahas: [], lines: [] },
  })

  // 3 — the lagna's lord
  const L = SIGN_LORD[lagna], gl = g(L)
  if (gl) {
    const rule = ((a.bhava_phala && a.bhava_phala.bhavas) || []).find((b) => b.house === 1)?.lord_rule
    steps.push({
      key: 'lagnaLord',
      say: both((l) => (l === 'hi'
        ? `${sign(l, lagna)} के स्वामी ${name(l, L)} हैं, और ${name(l, L)} ${gl.bhava === 1 ? 'स्वयं लग्न में' : `${HI_ORD[gl.bhava]} भाव में`}, ${sign(l, gl.rasi)} राशि में बैठे हैं। लग्नेश जिस भाव में हो, शास्त्र उसका अलग नियम देते हैं — बारहों भावों के लिए; इस कुंडली का नियम ‘भाव व योग’ खंड में है।`
        : `${sign(l, lagna)} is ruled by ${named(l, L)}, and ${name(l, L)} sits ${gl.bhava === 1 ? 'in the lagna itself' : `in the ${EN_ORD(gl.bhava)} house`}, in ${sign(l, gl.rasi)}. The classical texts give a rule for the lagna's lord in each of the twelve houses; this chart's is in the Bhāvas & Yogas section.`)),
      quote: null, cite: rule ? rule.citation : null,
      focus: { houses: gl.bhava === 1 ? [1] : [1, gl.bhava], grahas: [L], lines: gl.bhava === 1 ? [] : [{ from: 1, to: gl.bhava, kind: 'lord' }] },
    })
  }

  // 4 — the Moon and the Sun
  const mo = g('moon'), su = g('sun'), dsh = currentDasha(chart)
  if (mo && su) {
    steps.push({
      key: 'luminaries',
      say: both((l) => (l === 'hi'
        ? `चन्द्र ${sign(l, mo.rasi)} राशि में, ${HI_ORD[mo.bhava]} भाव में, ${N.hi.nakshatra(mo.nakshatra)} नक्षत्र में है। चन्द्र की राशि जन्म-राशि कहलाती है, और उसका नक्षत्र तय करता है कि विंशोत्तरी दशा किस ग्रह से आरंभ होती है। सूर्य ${sign(l, su.rasi)} राशि में, ${HI_ORD[su.bhava]} भाव में है।`
        : `${named(l, 'moon')} is in ${sign(l, mo.rasi)}, in the ${EN_ORD(mo.bhava)} house, in the nakṣatra ${namer.nakshatra(mo.nakshatra)}. Its sign is the janma rāśi, and its nakṣatra sets the graha with which the Viṁśottarī daśā begins. ${named(l, 'sun')} is in ${sign(l, su.rasi)}, in the ${EN_ORD(su.bhava)} house.`)),
      quote: null, cite: dsh ? dsh.cite : null,
      focus: { houses: [...new Set([mo.bhava, su.bhava])], grahas: ['moon', 'sun'], lines: [] },
    })
  }

  // 5 — dignity
  const strong = DIGNITY_ORDER.flatMap((st) => (chart.grahas || []).filter((x) => x.dignity && x.dignity.state === st)).slice(0, 3)
  if (strong.length) {
    steps.push({
      key: 'dignity',
      say: both((l) => {
        const items = strong.map((x) => (l === 'hi'
          ? `${sign(l, x.rasi)} राशि में ${name(l, x.key)} ${DIGNITY[x.dignity.state].hi}`
          : `${named(l, x.key)}, in ${sign(l, x.rasi)}, is ${DIGNITY[x.dignity.state].en}`))
        return l === 'hi'
          ? `ग्रह की राशि उसका बल बदलती है: उच्च, मूलत्रिकोण, स्वराशि, मित्र या शत्रु की राशि, नीच। इस कुंडली में: ${items.join('; ')}। गरिमा उन बलों में से एक है जिन्हें शास्त्र गिनते हैं।`
          : `The sign a graha stands in changes its strength — exalted, mūlatrikoṇa, its own sign, a friend's or an enemy's, debilitated. In this chart: ${items.join('; ')}. Dignity is one of the strengths the classical texts count.`
      }),
      quote: null, cite: citeOf(strong[0].key, 'dignity'),
      focus: { houses: [...new Set(strong.map((x) => x.bhava))], grahas: strong.map((x) => x.key), lines: [] },
    })
  }

  // 6 — aspects: Jupiter's, the graha with special full aspects of the kindest repute
  const casts = a.drishti && a.drishti.graha && a.drishti.graha.casts
  const jc = casts && casts.jupiter, ju = g('jupiter')
  if (jc && ju) {
    const hj = ju.bhava
    const aspects = Object.entries(jc.signs || {}).map(([s, v]) => ({ to: houseOf(+s, lagna), s: v })).sort((x, y) => x.to - y.to)
    const full = aspects.filter((x) => x.s >= 1).map((x) => x.to)
    const onto = Object.entries(jc.grahas || {}).filter(([, v]) => v >= 1).map(([k]) => k)
    steps.push({
      key: 'aspects',
      say: both((l) => (l === 'hi'
        ? `ग्रह दृष्टि डालते हैं। हर ग्रह अपने से सातवें भाव को पूर्ण दृष्टि से देखता है; ${list(['mars', 'jupiter', 'saturn'].map((k) => name(l, k)), l)} की कुछ विशेष पूर्ण दृष्टियाँ भी हैं। ${name(l, 'jupiter')}, ${HI_ORD[hj]} भाव से, ${list(full.map((h) => HI_ORD[h]), l)} भाव को पूर्ण दृष्टि से देखते हैं${onto.length ? ` — और वहाँ बैठे ${list(onto.map((k) => name(l, k)), l)} को` : ''}। हल्की रेखाएँ आंशिक दृष्टि हैं।`
        : `Grahas cast aspects — dṛṣṭi. Every graha looks fully at the 7th house from itself, and ${list(['mars', 'jupiter', 'saturn'].map((k) => name(l, k)), l)} have special full aspects too. ${named(l, 'jupiter')}, from the ${EN_ORD(hj)} house, looks fully on the ${list(full.map(EN_ORD), l)} houses${onto.length ? ` — and on ${list(onto.map((k) => name(l, k)), l)}, who sit there` : ''}. The fainter lines are its partial aspects.`)),
      quote: null, cite: a.drishti.graha.citation || null,
      focus: { houses: [hj, ...full], grahas: ['jupiter', ...onto], lines: aspects.map((x) => ({ from: hj, to: x.to, kind: x.s >= 1 ? 'full' : 'part' })) },
    })
  }

  // 7 — yogas: on screen all of them, with the first two's cited effects; spoken, only the ones with a
  // proper name ("Parvata Yoga" — not a description like "Moon–Venus mutual 3rd/11th"), and in Hindi
  // none (the catalogue names them in roman only) — the count, and the names are on screen
  const yg = a.yogas
  if (yg && Array.isArray(yg.detected)) {
    const ys = yg.detected
    const proper = ys.map((y) => y.name).filter((n) => /^[A-Z][a-zāīūṛṝṣṇṭḍśñṅṁḥ]+( Yoga)?$/.test(n))
    const rest = ys.length - proper.length
    steps.push({
      key: 'yogas',
      say: both((l) => (ys.length
        ? (l === 'hi'
          ? `शास्त्र ग्रहों के कुछ विशेष मेलों को योग कहते हैं। जाँचे गए ${yg.checked} योगों में से ${ys.length} इस कुंडली में बनते हैं — उनके नाम स्क्रीन पर हैं। हर योग का शास्त्र-वर्णित फल ‘भाव व योग’ खंड में है — शास्त्र के शब्दों में, भविष्यवाणी के रूप में नहीं।`
          : `The classical texts name certain combinations — yogas. Of the ${yg.checked} checked, ${ys.length} ${ys.length === 1 ? 'is' : 'are'} formed in this chart${proper.length ? `: ${list([...proper, ...(rest ? [`${rest} more`] : [])], l)}` : ' — their names are on screen'}. Each yoga's effect is in the Bhāvas & Yogas section, in the text's own words — not as a forecast.`)
        : (l === 'hi'
          ? `शास्त्र ग्रहों के कुछ विशेष मेलों को योग कहते हैं। जाँचे गए ${yg.checked} योगों में से कोई इस कुंडली में नहीं बनता — जहाँ शास्त्र मौन है, वहाँ यह पृष्ठ भी मौन है।`
          : `The classical texts name certain combinations — yogas. None of the ${yg.checked} checked is formed in this chart — where the texts are silent, so is this page.`))),
      quote: ys.slice(0, 2).map((y) => ({ name: y.name, effect: String(y.effect || '').replace(/^\d+\s*[-–]?\s*\d*\.\s*/, '') })).filter((q) => q.effect),
      cite: ys.slice(0, 2).map((y) => y.citation).filter(Boolean).join(' · ') || null,
      focus: { houses: [], grahas: [], lines: [], names: ys.map((y) => y.name) },
    })
  }

  // 8 — the kāraka of the self
  const ak = a.karakas && a.karakas.atmakaraka
  if (ak && g(ak)) {
    steps.push({
      key: 'atmakaraka',
      say: both((l) => (l === 'hi'
        ? `चर-कारक पद्धति में जो ग्रह अपनी राशि में सबसे अधिक अंश पर हो, वह आत्मकारक — आत्मा का कारक — कहलाता है। इस कुंडली में वह ${name(l, ak)} है, ${HI_ORD[g(ak).bhava]} भाव में।`
        : `In the chara-kāraka scheme, the graha furthest advanced in its sign is the ātmakāraka — the significator of the self. In this chart it is ${named(l, ak)}, in the ${EN_ORD(g(ak).bhava)} house.`)),
      quote: null, cite: a.karakas.citation || null,
      focus: { houses: [g(ak).bhava], grahas: [ak], lines: [] },
    })
  }

  // 9 — timing (not for a chart shared without its birth details: it has no daśā)
  if (dsh) {
    const { maha, antar } = dsh
    steps.push({
      key: 'dasha',
      say: both((l) => (l === 'hi'
        ? `समय दशाओं से पढ़ा जाता है। विंशोत्तरी पद्धति में अभी ${name(l, maha.lord)} की महादशा है — ${monthYear(maha.start, l)} से ${monthYear(maha.end, l)} तक${antar ? `; उसके भीतर ${name(l, antar.lord)} की अंतर्दशा ${monthYear(antar.end, l)} तक है` : ''}। दशा अपने ग्रह की इस कुंडली में स्थिति से पढ़ी जाती है — वह एक खिड़की खोलती है, कोई घटना तय नहीं करती।`
        : `Timing is read from the daśās. In the Viṁśottarī system this is the period of ${named(l, maha.lord)}, from ${monthYear(maha.start, l)} to ${monthYear(maha.end, l)}${antar ? `; within it, the sub-period of ${named(l, antar.lord)} runs until ${monthYear(antar.end, l)}` : ''}. A period is read from where its graha stands in this chart — it opens a window; it does not fix an event.`)),
      quote: null, cite: dsh.cite,
      focus: { houses: [...new Set([g(maha.lord)?.bhava, antar && g(antar.lord)?.bhava].filter(Boolean))], grahas: [maha.lord, antar && antar.lord].filter(Boolean), lines: [] },
    })
  }

  // 10 — the close
  steps.push({
    key: 'close',
    say: {
      en: 'That is the frame of a reading: the lagna and its lord, the Moon, dignity, aspects, yogas and timing. Every reading on this page traces to a cited text — and where the texts are silent, so is this page.',
      hi: 'यही एक पाठ का ढाँचा है: लग्न और उसका स्वामी, चन्द्र, ग्रहों की गरिमा, दृष्टि, योग और समय। इस पृष्ठ का हर पाठ किसी उद्धृत ग्रंथ से आता है — और जहाँ ग्रंथ मौन हैं, वहाँ यह पृष्ठ भी मौन है।',
    },
    quote: null, cite: null,
    focus: { houses: [], grahas: [], lines: [] },
  })

  return { steps }
}

/** The spoken script as plain text — one paragraph a step — for a narrator or a presenter to read. */
export const spokenScript = (steps, lang = 'en') => steps.map((s) => s.say[lang] || s.say.en).join('\n\n')

/** Seconds a step stays on screen when nothing is speaking it: a calm reading pace, never under six. */
export const readSeconds = (text) => Math.max(6, Math.round(String(text || '').split(/\s+/).length / 2.4))
