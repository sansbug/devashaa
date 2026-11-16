/**
 * Life areas — the chart read one area of life at a time (you · career · wealth ·
 * marriage · home · children and learning), ending in practical notes.
 *
 * Each area gathers, from what findings.js already built:
 *   shows     what the chart has in the area's house(s) — placements only;
 *   passages  the registered classical passages tied to those houses (whole; a
 *             sensitive one only on request) — the TEXTS' statements;
 *   supports / cautions   the factors for and against the house lords;
 *   timing    whether a running period's planet rules or sits in the area, and
 *             when the next such period begins — dates read off the daśā tree;
 *   notes     PRACTICAL NOTES, OURS. The owner's choice (2026-11-16): "what you
 *             can do" is practical notes in our own words, not the texts'
 *             remedies — the site prescribes no ritual, gem or charity.
 *
 * Rules for the notes (test_lifeareas.mjs pins them):
 *   - they are derived, so each area carries its `basis` (what they rest on);
 *   - they speak of attention, planning and timing — never of what will happen,
 *     never medical, legal or financial instructions, never a ritual;
 *   - an unfavourable factor is "a reason to prepare, not a reason to worry";
 *   - there is no health area: the 6th house is not turned into advice.
 */
import { makeNamer } from './naming.js'
import { HOUSE } from './walkthrough.js'
import { dashaTree } from './findings.js'

const SIGN_LORD = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'saturn', 'jupiter']
const EN_ORD = (n) => `${n}${n % 10 === 1 && n !== 11 ? 'st' : n % 10 === 2 && n !== 12 ? 'nd' : n % 10 === 3 && n !== 13 ? 'rd' : 'th'}`
const HI_ORD = ['', 'पहले', 'दूसरे', 'तीसरे', 'चौथे', 'पाँचवें', 'छठे', 'सातवें', 'आठवें', 'नौवें', 'दसवें', 'ग्यारहवें', 'बारहवें']
const HI_ORD_N = ['', 'पहला', 'दूसरा', 'तीसरा', 'चौथा', 'पाँचवाँ', 'छठा', 'सातवाँ', 'आठवाँ', 'नौवाँ', 'दसवाँ', 'ग्यारहवाँ', 'बारहवाँ']
const MONTHS = { en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], hi: ['जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'] }
const monthYear = (s, l) => { const m = /^(\d{4})-(\d{2})/.exec(String(s || '')); return m ? `${MONTHS[l][+m[2] - 1]} ${m[1]}` : '' }
const when = (s) => new Date(String(s).replace(' ', 'T')).getTime()
const list = (xs, l) => (xs.length < 2 ? xs.join('') : `${xs.slice(0, -1).join(', ')} ${l === 'hi' ? 'और' : 'and'} ${xs[xs.length - 1]}`)

export const AREAS = [
  { key: 'self', houses: [1], label: { en: 'You', hi: 'आप स्वयं' } },
  { key: 'career', houses: [10], label: { en: 'Career and standing', hi: 'कर्म और प्रतिष्ठा' } },
  { key: 'wealth', houses: [2, 11], label: { en: 'Wealth and income', hi: 'धन और आय' } },
  { key: 'marriage', houses: [7], label: { en: 'Marriage and partnership', hi: 'विवाह और साझेदारी' } },
  { key: 'home', houses: [4], label: { en: 'Home and family', hi: 'घर और परिवार' } },
  { key: 'children', houses: [5], label: { en: 'Children and learning', hi: 'संतान और विद्या' } },
]

const BASIS = {
  en: ['Which planets rule and sit in this area’s houses (calculated).',
    'Which periods are running and when they change (calculated). A period brings forward the matters of the houses its planet rules and sits in.',
    'The supporting and opposing factors listed in this section.'],
  hi: ['इस क्षेत्र के भावों के स्वामी और उनमें बैठे ग्रह (गणना से)।',
    'कौन-सी दशाएँ चल रही हैं और कब बदलती हैं (गणना से)। दशा उन भावों की बातों को आगे लाती है जिनका उसका ग्रह स्वामी है और जिसमें वह बैठा है।',
    'इस खंड में दी गई समर्थक और विपरीत बातें।'],
}

/**
 * @param chart  the /api/chart payload
 * @param built  buildFindings(chart, namer) — the findings already computed for this chart
 * @param namer  the reader's name style (English lines); Hindi is always Devanāgarī
 * @param now    "today", for the timing (a Date or a ms timestamp); defaults to the clock
 */
export function buildLifeAreas(chart, built, namer = makeNamer('common'), now = Date.now()) {
  const N = { en: namer, hi: makeNamer('devanagari') }
  const plainEn = namer.style === 'english'
  const lagna = chart.lagna_rasi
  const grahas = chart.grahas || []
  const g = (k) => grahas.find((x) => x.key === k)
  const nm = (l, k) => N[l].grahaKey(k)
  const sign = (l, i) => (l === 'en' && !plainEn ? `${namer.rasi(i)} (${namer.rasiEnglish(i)})` : N[l].rasi(i))
  const both = (f) => ({ en: f('en'), hi: f('hi') })
  const lordOf = (h) => SIGN_LORD[(lagna + h - 1) % 12]
  const occupants = (h) => grahas.filter((x) => x.bhava === h).map((x) => x.key)
  const ruled = (k) => Array.from({ length: 12 }, (_, i) => i + 1).filter((h) => lordOf(h) === k)
  const T = +now
  const tree = dashaTree(chart)
  const mahas = (tree && tree.mahadashas) || []
  const mi = mahas.findIndex((m) => m.is_current)
  const maha = mi >= 0 ? mahas[mi] : null
  const antar = maha ? (maha.sub || []).find((x) => x.is_current) : null

  return AREAS.map((A) => {
    const lords = [...new Set(A.houses.map(lordOf))]
    const inIt = [...new Set(A.houses.flatMap(occupants))]
    const tied = [...new Set([...lords, ...inIt])]
    // how a graha is tied to this area, in words
    const tie = (l, k) => {
      const r = A.houses.filter((h) => lordOf(h) === k), s = A.houses.filter((h) => g(k) && g(k).bhava === h)
      const parts = []
      if (r.length) parts.push(l === 'hi' ? `आपके ${list(r.map((h) => HI_ORD[h]), l)} भाव के स्वामी हैं` : `rules your ${list(r.map(EN_ORD), l)} ${r.length > 1 ? 'houses' : 'house'}`)
      if (s.length) parts.push(l === 'hi' ? `आपके ${list(s.map((h) => HI_ORD[h]), l)} भाव में बैठे हैं` : `sits in your ${list(s.map(EN_ORD), l)} ${s.length > 1 ? 'houses' : 'house'}`)
      return parts.join(l === 'hi' ? ' और ' : ' and ')
    }

    // ── what the chart shows ──
    const shows = both((l) => A.houses.flatMap((h) => {
      const s = (lagna + h - 1) % 12, lo = lordOf(h), lg = g(lo), occ = occupants(h)
      return [
        l === 'hi'
          ? `आपका ${HI_ORD_N[h]} भाव (${HOUSE[h].chip.hi}) ${sign(l, s)} राशि है।${lg ? ` इसके स्वामी ${nm(l, lo)} आपके ${HI_ORD[lg.bhava]} भाव में बैठे हैं।${lg.bhava === h ? '' : ` ${HI_ORD_N[lg.bhava]} भाव ${HOUSE[lg.bhava].of.hi} का भाव है।`}` : ''}`
          : `Your ${EN_ORD(h)} house (${HOUSE[h].chip.en}) is ${sign(l, s)}.${lg ? ` Its lord, ${nm(l, lo)}, sits in your ${EN_ORD(lg.bhava)} house.${lg.bhava === h ? '' : ` The ${EN_ORD(lg.bhava)} house is the house of ${HOUSE[lg.bhava].of.en}.`}` : ''}`,
        occ.length
          ? (l === 'hi' ? `इस भाव में बैठे ग्रह: ${list(occ.map((k) => nm(l, k)), l)}।` : `Planets in this house: ${list(occ.map((k) => nm(l, k)), l)}.`)
          : (l === 'hi' ? 'इस भाव में कोई ग्रह नहीं बैठा।' : 'No planet sits in this house.'),
      ]
    }))

    // ── what the texts say: every registered passage tied to these houses, once each ──
    const seen = new Set(), passages = []
    for (const f of built.findings) {
      for (const t of (f.texts || [])) {
        if (!A.houses.includes(t.house) || seen.has(t.cite)) continue
        seen.add(t.cite); passages.push(t)
      }
    }

    // ── the factors on the house lords ──
    const lordF = lords.map((k) => built.findings.find((f) => f.graha === k)).filter(Boolean)
    const tagged = (l, f, xs) => xs.map((s) => `${nm(l, f.graha)}: ${s}`)
    const supports = both((l) => lordF.flatMap((f) => tagged(l, f, f.supports[l])))
    const cautions = both((l) => lordF.flatMap((f) => tagged(l, f, f.cautions[l])))

    // ── timing: is the area in focus now, and when is it next ──
    const nowItems = []
    if (maha && tied.includes(maha.lord)) nowItems.push({ lord: maha.lord, kind: 'maha', end: maha.end })
    if (antar && tied.includes(antar.lord) && !(maha && antar.lord === maha.lord && nowItems.length)) nowItems.push({ lord: antar.lord, kind: 'antar', end: antar.end })
    let next = null
    if (maha && !nowItems.length) {
      outer: for (let i = mi; i < mahas.length; i++) {
        for (const a of (mahas[i].sub || [])) {
          if (!(when(a.start) > T)) continue
          const viaMaha = i > mi && tied.includes(mahas[i].lord)
          if (tied.includes(a.lord) || viaMaha) { next = { lord: viaMaha ? mahas[i].lord : a.lord, kind: viaMaha ? 'maha' : 'antar', start: viaMaha ? mahas[i].start : a.start, end: viaMaha ? mahas[i].end : a.end, within: viaMaha ? null : mahas[i].lord }; break outer }
        }
      }
    }
    const kindWord = (l, k) => (k === 'maha' ? (l === 'hi' ? 'महादशा' : 'main period') : (l === 'hi' ? 'अन्तर्दशा' : 'sub-period'))
    const timing = {
      now: nowItems.length ? both((l) => nowItems.map((x) => (l === 'hi'
        ? `अभी ${nm(l, x.lord)} की ${kindWord(l, x.kind)} चल रही है, ${monthYear(x.end, l)} तक। ${nm(l, x.lord)} ${tie(l, x.lord)}।`
        : `${nm(l, x.lord)}’s ${kindWord(l, x.kind)} is running now, until ${monthYear(x.end, l)}. ${nm(l, x.lord)} ${tie(l, x.lord)}.`)).join(' ')) : null,
      next: next ? both((l) => (l === 'hi'
        ? `अगली बार यह क्षेत्र ${monthYear(next.start, l)} से आगे आता है। तब ${nm(l, next.lord)} की ${kindWord(l, next.kind)} शुरू होती है${next.within ? ` (${nm(l, next.within)} की महादशा के भीतर)` : ''}। यह ${monthYear(next.end, l)} तक चलती है। ${nm(l, next.lord)} ${tie(l, next.lord)}।`
        : `This area next comes forward from ${monthYear(next.start, l)}. ${nm(l, next.lord)}’s ${kindWord(l, next.kind)} begins then${next.within ? ` (within ${nm(l, next.within)}’s main period)` : ''}. It runs until ${monthYear(next.end, l)}. ${nm(l, next.lord)} ${tie(l, next.lord)}.`)) : null,
      none: !maha,
    }

    // ── practical notes, ours ──
    const S = supports.en.length, C = cautions.en.length
    const hard = passages.some((t) => t.held)
    const notes = both((l) => [
      nowItems.length && (l === 'hi'
        ? 'यह क्षेत्र अभी केन्द्र में है। परंपरा इस खिड़की को इस क्षेत्र के निर्णयों और नई शुरुआत से जोड़ती है। जो आप टाल रहे हैं, उस पर अभी ध्यान दें।'
        : 'This area is in focus now. The tradition ties this window to decisions and new starts in it. If you have been putting one off, give it your attention now.'),
      !nowItems.length && next && (l === 'hi'
        ? `यह क्षेत्र अभी केन्द्र में नहीं है। अगली खिड़की ${monthYear(next.start, l)} से है। बड़ी योजनाओं की तैयारी उसी की ओर रखें। तब तक नींव का काम करें।`
        : `This area is not in focus right now. Its next window opens in ${monthYear(next.start, l)}. Aim the larger plans at that window. Use the time until then for groundwork.`),
      S > 0 && C === 0 && (l === 'hi'
        ? 'ऊपर की बातें समर्थन की ओर हैं। यह आगे बढ़ाने का क्षेत्र है। यहाँ लगाया गया प्रयास सही जगह लगा है।'
        : 'The factors above are on the supporting side. This is an area to build on. Effort put here is well placed.'),
      C > 0 && S === 0 && (l === 'hi'
        ? 'ऊपर की बातें इस क्षेत्र के विपरीत जाती हैं। इसे मानकर न चलें। धीरे और स्थिर चलें, और गुंजाइश रखें। बड़े कदम से पहले दूसरी राय लें।'
        : 'The factors above count against this area. Do not take it for granted. Move steadily and keep a margin. Get a second opinion before a large step.'),
      C > 0 && S > 0 && (l === 'hi'
        ? 'यहाँ दोनों ओर की बातें हैं, इसलिए रास्ता मिला-जुला मानें। जो समर्थन में है (पहली सूची) उस पर टिकें। जो विपरीत है (दूसरी सूची) उसके लिए पहले से तैयारी रखें।'
        : 'There are factors on both sides here, so expect a mixed road. Lean on what supports it (the first list). Prepare in advance for what counts against it (the second list).'),
      (hard || passages.some((t) => /adverse|प्रतिकूल/.test((t.qualifier && t.qualifier.en) || ''))) && (l === 'hi'
        ? 'इस क्षेत्र पर ग्रंथों के कुछ कथन प्रतिकूल हैं। वे स्थिति की प्रवृत्ति बताते हैं, तय परिणाम नहीं। वे तैयारी का कारण हैं, चिंता का नहीं।'
        : 'Some of the texts’ statements on this area are unfavourable. They describe a tendency of the placement, not a fixed outcome. They are a reason to prepare, not a reason to worry.'),
      l === 'hi'
        ? 'कुंडली प्रवृत्ति दिखाती है। आप उसका क्या करते हैं, वह आपके हाथ में है। प्रयास और चुनाव सदा मायने रखते हैं।'
        : 'A chart shows tendencies. What you do with them is yours. Effort and choices always matter.',
    ].filter(Boolean))

    return { key: A.key, label: A.label, houses: A.houses, tied, shows, passages, supports, cautions, timing, notes, basis: BASIS }
  })
}
