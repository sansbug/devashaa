/**
 * The daśā reading — how to read a period, what is running now, what changes
 * next, and what that means for the reader.
 *
 * Built from the chart payload alone:
 *   - the Viṁśottarī tree (which periods run, and their dates) — calculated;
 *   - which houses each period's planet rules and sits in — calculated; the
 *     method line "a period brings forward the matters of the houses its planet
 *     rules and sits in" is the one the walkthrough already uses;
 *   - the text's own rule for judging a period, BPHS Vol II ch.47 vv.5-6, as the
 *     backend evaluated it (`dasha.verdicts`): favourable / unfavourable /
 *     both / no stated verdict, with the conditions that were met. The VERSE is
 *     the text's; our lines only report which of its conditions this chart meets.
 *
 * `changes` and `notes` are OURS (derived; `basis` says what they rest on), under
 * the same rules as the life-area notes: attention, planning and timing — never
 * what will happen, never a ritual or a remedy, never medical / legal / financial
 * instructions, never a death or a lifespan. An unfavourable verdict is "a reason
 * to prepare, not a reason to worry". test_dashareading.mjs pins this.
 *
 * The sub-period chapters (ch.52-60) are NOT built here: DashaReading.jsx fetches
 * them from /api/antardasa/plain (api/antardasa_plain.py) for the running and the
 * next sub-period and shows the branches that apply, as the text's own lists.
 * They carry no verdict, and neither "what changes" nor the notes draw on them.
 */
import { makeNamer } from './naming.js'
import { HOUSE } from './walkthrough.js'
import { dashaTree } from './findings.js'

const SIGN_LORD = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'saturn', 'jupiter']
const EN_ORD = (n) => `${n}${n % 10 === 1 && n !== 11 ? 'st' : n % 10 === 2 && n !== 12 ? 'nd' : n % 10 === 3 && n !== 13 ? 'rd' : 'th'}`
const HI_ORD = ['', 'पहले', 'दूसरे', 'तीसरे', 'चौथे', 'पाँचवें', 'छठे', 'सातवें', 'आठवें', 'नौवें', 'दसवें', 'ग्यारहवें', 'बारहवें']
const MONTHS = { en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], hi: ['जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'] }
const monthYear = (s, l) => { const m = /^(\d{4})-(\d{2})/.exec(String(s || '')); return m ? `${MONTHS[l][+m[2] - 1]} ${m[1]}` : '' }
const when = (s) => new Date(String(s).replace(' ', 'T')).getTime()
const list = (xs, l) => (xs.length < 2 ? xs.join('') : `${xs.slice(0, -1).join(', ')} ${l === 'hi' ? 'और' : 'and'} ${xs[xs.length - 1]}`)

export const HOW = {
  en: [
    'A daśā is a planetary period. This system (Viṁśottarī) divides 120 years among the nine planets, starting from the star the Moon was in at your birth, so everyone’s periods fall at different ages.',
    'Periods nest: a main period (mahādaśā) of several years holds nine sub-periods (antardaśā), each of months to a few years. The main period sets the background; the sub-period is what is in the foreground now.',
    'To read a period, look at its planet in your chart. The houses that planet rules and the house it sits in are the areas of life the period brings forward.',
    'Whether a period leans favourable or not is judged, by the text’s own rule, from where its planet stands: in the ascendant, exalted, in its own or a friend’s sign on one side; in the 6th, 8th or 12th house, debilitated or in an enemy’s sign on the other.',
  ],
  hi: [
    'दशा ग्रह की एक अवधि है। यह पद्धति (विंशोत्तरी) 120 वर्षों को नौ ग्रहों में बाँटती है, और गिनती उस नक्षत्र से शुरू होती है जिसमें जन्म के समय चन्द्र था — इसलिए हर व्यक्ति की दशाएँ अलग-अलग आयु पर आती हैं।',
    'दशाएँ एक-दूसरे के भीतर चलती हैं: कई वर्षों की महादशा के भीतर नौ अन्तर्दशाएँ होती हैं, हर एक कुछ महीनों से कुछ वर्षों की। महादशा पृष्ठभूमि तय करती है; अन्तर्दशा वह है जो अभी सामने है।',
    'दशा पढ़ने के लिए कुंडली में उसके ग्रह को देखें। वह ग्रह जिन भावों का स्वामी है और जिस भाव में बैठा है, जीवन के वही क्षेत्र उस दशा में आगे आते हैं।',
    'दशा अनुकूल ओर झुकती है या नहीं, यह ग्रंथ के अपने नियम से, उसके ग्रह की स्थिति से आँका जाता है: लग्न में, उच्च, स्वराशि या मित्र राशि में — एक ओर; छठे, आठवें या बारहवें भाव में, नीच या शत्रु राशि में — दूसरी ओर।',
  ],
}

const BASIS = {
  en: ['Which periods are running and the dates they change (calculated from the Moon’s position at birth).',
    'Which houses each period’s planet rules and sits in (calculated). A period brings forward the matters of those houses.',
    'The text’s rule for judging a period by where its planet stands, and which of its conditions your chart meets.'],
  hi: ['कौन-सी दशाएँ चल रही हैं और किस तिथि को बदलती हैं (जन्म के समय चन्द्र की स्थिति से गणना)।',
    'हर दशा का ग्रह किन भावों का स्वामी है और किस भाव में बैठा है (गणना से)। दशा उन्हीं भावों की बातों को आगे लाती है।',
    'ग्रह की स्थिति से दशा आँकने का ग्रंथ का नियम, और आपकी कुंडली उसकी कौन-सी शर्तें पूरी करती है।'],
}

const STATE = {
  favourable: { en: 'on the favourable side', hi: 'अनुकूल ओर', tone: 'good' },
  adverse: { en: 'on the unfavourable side', hi: 'प्रतिकूल ओर', tone: 'hard' },
  contested: { en: 'on both sides at once', hi: 'दोनों ओर', tone: 'mixed' },
  not_stated: { en: 'without a stated verdict', hi: 'बिना किसी कथित निर्णय के', tone: 'plain' },
}

/**
 * @returns null for a chart with no daśā (one shared without its birth details), else
 *   { how, rows:[{role, lord, start, end, title, span, brings, verdict:{state,tone,line}}], rule:{verse,cite}, changes, notes, basis }
 */
export function buildDashaReading(chart, namer = makeNamer('common'), now = Date.now()) {
  const tree = dashaTree(chart)
  const mahas = (tree && tree.mahadashas) || []
  const mi = mahas.findIndex((m) => m.is_current)
  if (mi < 0) return null
  const maha = mahas[mi]
  const subs = maha.sub || []
  const ai = subs.findIndex((x) => x.is_current)
  const antar = ai >= 0 ? subs[ai] : null
  const nextMaha = mahas[mi + 1] || null
  const nextAntar = antar ? (subs[ai + 1] || (nextMaha && nextMaha.sub && nextMaha.sub[0]) || null) : null
  const nextAntarIn = antar && subs[ai + 1] ? maha : nextMaha

  const N = { en: namer, hi: makeNamer('devanagari') }
  const lagna = chart.lagna_rasi
  const g = (k) => (chart.grahas || []).find((x) => x.key === k)
  const nm = (l, k) => N[l].grahaKey(k)
  const both = (f) => ({ en: f('en'), hi: f('hi') })
  const ruled = (k) => Array.from({ length: 12 }, (_, i) => i + 1).filter((h) => SIGN_LORD[(lagna + h - 1) % 12] === k)
  const housesOf = (k) => [...new Set([...ruled(k), ...(g(k) ? [g(k).bhava] : [])])]
  const areas = (l, k) => housesOf(k).map((h) => HOUSE[h].of[l]).join('; ')
  const verdicts = (chart.dasha && chart.dasha.verdicts) || {}
  const T = +now

  const brings = (k) => both((l) => {
    const r = ruled(k), x = g(k)
    if (!x) return ''
    return l === 'hi'
      ? `${nm(l, k)} ${r.length ? `आपके ${list(r.map((h) => HI_ORD[h]), l)} भाव के स्वामी हैं और ` : 'किसी राशि के स्वामी नहीं; वे '}${HI_ORD[x.bhava]} भाव में बैठे हैं। इसलिए यह दशा इन बातों को आगे लाती है: ${areas(l, k)}।`
      : `${nm(l, k)} ${r.length ? `rules your ${list(r.map(EN_ORD), l)} ${r.length > 1 ? 'houses' : 'house'} and ` : 'rules no sign; it '}sits in your ${EN_ORD(x.bhava)} house. So this period brings forward: ${areas(l, k)}.`
  })
  const verdict = (k) => {
    const v = verdicts[k]
    const state = v && STATE[v.state] ? v.state : 'not_stated'
    const fav = v ? (v.favourable || []).map((c) => c.condition) : [], adv = v ? (v.adverse || []).map((c) => c.condition) : []
    return {
      state, tone: STATE[state].tone,
      line: both((l) => {
        const why = [...fav, ...adv].join('; ')
        if (state === 'not_stated') return l === 'hi' ? `ग्रंथ के नियम से इस दशा पर कोई निर्णय नहीं बनता: ${nm(l, k)} उसकी कोई शर्त पूरी नहीं करते।` : `By the text’s rule this period is ${STATE[state].en}: ${nm(l, k)} meets none of its conditions either way.`
        if (state === 'contested') return l === 'hi' ? `ग्रंथ के नियम से यह दशा दोनों ओर है (${why}); ग्रंथ यह नहीं बताता कि दोनों हों तो क्या माना जाए।` : `By the text’s rule this period is ${STATE[state].en} (${why}); the text does not say how to weigh the two.`
        return l === 'hi' ? `ग्रंथ के नियम से यह दशा ${STATE[state].hi} है: ${nm(l, k)} — ${why}।` : `By the text’s rule this period is ${STATE[state].en}: ${nm(l, k)} is ${why}.`
      }),
    }
  }
  const row = (role, node, within) => ({
    role, lord: node.lord, within: within ? within.lord : null, start: node.start, end: node.end,
    title: both((l) => {
      const w = { maha: ['Main period (mahādaśā)', 'महादशा'], antar: ['Sub-period (antardaśā)', 'अन्तर्दशा'], nextAntar: ['Next sub-period', 'अगली अन्तर्दशा'], nextMaha: ['Next main period', 'अगली महादशा'] }[role]
      return `${l === 'hi' ? w[1] : w[0]}: ${nm(l, node.lord)}${within && within.lord !== node.lord && role !== 'maha' && role !== 'nextMaha' ? (l === 'hi' ? ` (${nm(l, within.lord)} की महादशा में)` : ` (within ${nm(l, within.lord)}’s main period)`) : ''}`
    }),
    span: both((l) => (role === 'maha' || role === 'antar'
      ? (l === 'hi' ? `${monthYear(node.start, l)} से ${monthYear(node.end, l)} तक — अभी चल रही है` : `${monthYear(node.start, l)} to ${monthYear(node.end, l)} — running now`)
      : (l === 'hi' ? `${monthYear(node.start, l)} से ${monthYear(node.end, l)} तक` : `${monthYear(node.start, l)} to ${monthYear(node.end, l)}`))),
    brings: brings(node.lord), verdict: verdict(node.lord),
  })

  const rows = [row('maha', maha, maha)]
  if (antar) rows.push(row('antar', antar, maha))
  if (nextAntar) rows.push(row('nextAntar', nextAntar, nextAntarIn))
  if (nextMaha) rows.push(row('nextMaha', nextMaha, nextMaha))

  const SHORT = { favourable: { en: 'the favourable side', hi: 'अनुकूल ओर' }, adverse: { en: 'the unfavourable side', hi: 'प्रतिकूल ओर' }, contested: { en: 'both sides at once', hi: 'दोनों ओर' }, not_stated: { en: 'no stated verdict', hi: 'कोई कथित निर्णय नहीं' } }
  const side = (l, st) => SHORT[st][l]
  const va = antar ? verdict(antar.lord).state : null, vna = nextAntar ? verdict(nextAntar.lord).state : null
  const vm = verdict(maha.lord).state, vnm = nextMaha ? verdict(nextMaha.lord).state : null
  const yearsTo = (s) => (when(s) - T) / (365.25 * 86400000)

  // ── what is going to change (ours: dates and emphasis, read off the rows above) ──
  const changes = both((l) => [
    antar && nextAntar && (l === 'hi'
      ? `${monthYear(nextAntar.start, l)} में अन्तर्दशा ${nm(l, antar.lord)} से ${nm(l, nextAntar.lord)} की हो जाती है। सामने की बातें ${areas(l, antar.lord)} से हटकर ${areas(l, nextAntar.lord)} पर आती हैं।`
      : `In ${monthYear(nextAntar.start, l)} the sub-period passes from ${nm(l, antar.lord)} to ${nm(l, nextAntar.lord)}. The foreground moves from (${areas(l, antar.lord)}) to (${areas(l, nextAntar.lord)}).`),
    antar && nextAntar && va !== vna && (l === 'hi'
      ? `ग्रंथ के नियम से अन्तर्दशा का झुकाव बदलता है: पहले — ${side(l, va)}; आगे — ${side(l, vna)}।`
      : `By the text’s rule the lean of the sub-period changes: ${side(l, va)} now, ${side(l, vna)} next.`),
    antar && nextAntar && va === vna && (l === 'hi'
      ? `ग्रंथ के नियम से अन्तर्दशा का झुकाव वही रहता है: ${side(l, vna)}।`
      : `By the text’s rule the lean of the sub-period stays the same: ${side(l, vna)}.`),
    nextMaha && (!nextAntar || nextAntarIn === maha) && (l === 'hi'
      ? `महादशा ${monthYear(maha.end, l)} तक ${nm(l, maha.lord)} की ही रहती है, इसलिए उसकी बातें (${areas(l, maha.lord)}) पृष्ठभूमि में बनी रहती हैं।`
      : `The main period stays ${nm(l, maha.lord)}’s until ${monthYear(maha.end, l)}, so its matters (${areas(l, maha.lord)}) remain the background.`),
    nextMaha && (l === 'hi'
      ? `${monthYear(nextMaha.start, l)} में महादशा स्वयं बदलती है: ${nm(l, maha.lord)} से ${nm(l, nextMaha.lord)} (${Math.round(nextMaha.years)} वर्ष)। यह बड़ा मोड़ है — पृष्ठभूमि ${areas(l, maha.lord)} से ${areas(l, nextMaha.lord)} पर जाती है${vm !== vnm ? `; ग्रंथ के नियम से झुकाव: पहले — ${side(l, vm)}, आगे — ${side(l, vnm)}` : ''}।`
      : `In ${monthYear(nextMaha.start, l)} the main period itself changes, from ${nm(l, maha.lord)} to ${nm(l, nextMaha.lord)} (${Math.round(nextMaha.years)} years). This is the larger turn: the background moves from (${areas(l, maha.lord)}) to (${areas(l, nextMaha.lord)})${vm !== vnm ? `; by the text’s rule its lean is ${side(l, vm)} now and ${side(l, vnm)} next` : ''}.`),
  ].filter(Boolean))

  // ── how it affects you: practical notes, ours ──
  const notes = both((l) => [
    antar && (l === 'hi'
      ? `अभी ध्यान देने के क्षेत्र: ${areas(l, antar.lord)} (अन्तर्दशा), ${areas(l, maha.lord)} की पृष्ठभूमि में (महादशा)। इन्हीं में निर्णय और प्रयास इस समय सबसे अधिक मायने रखते हैं।`
      : `The areas to give your attention to now: ${areas(l, antar.lord)} (the sub-period), against a background of ${areas(l, maha.lord)} (the main period). Decisions and effort in these count most at present.`),
    nextAntar && vna === 'adverse' && (l === 'hi'
      ? `आने वाली अन्तर्दशा को ग्रंथ का नियम प्रतिकूल ओर गिनता है। ${monthYear(nextAntar.start, l)} से पहले के महीनों में जो खुला है उसे पूरा करें, और ${areas(l, nextAntar.lord)} के लिए गुंजाइश बना लें। यह तैयारी का कारण है, चिंता का नहीं।`
      : `The coming sub-period is one the text’s rule counts on the unfavourable side. Use the months before ${monthYear(nextAntar.start, l)} to finish what is open, and build a margin around ${areas(l, nextAntar.lord)}. It is a reason to prepare, not a reason to worry.`),
    nextAntar && vna === 'favourable' && (l === 'hi'
      ? `आने वाली अन्तर्दशा को ग्रंथ का नियम अनुकूल ओर गिनता है। ${areas(l, nextAntar.lord)} से जुड़ी जो बातें रुकी हैं, उनकी तैयारी अभी करें ताकि ${monthYear(nextAntar.start, l)} से उन्हें आगे बढ़ा सकें।`
      : `The coming sub-period is one the text’s rule counts on the favourable side. Prepare now whatever has been waiting in ${areas(l, nextAntar.lord)}, so that it can be moved forward from ${monthYear(nextAntar.start, l)}.`),
    nextAntar && (vna === 'not_stated' || vna === 'contested') && (l === 'hi'
      ? `आने वाली अन्तर्दशा पर ग्रंथ का नियम कोई स्पष्ट निर्णय नहीं देता। ${monthYear(nextAntar.start, l)} से ${areas(l, nextAntar.lord)} पर नज़र रखें — किसी पूर्वानुमान पर नहीं।`
      : `The text’s rule gives no clear verdict on the coming sub-period. From ${monthYear(nextAntar.start, l)}, watch ${areas(l, nextAntar.lord)} — the area, not a forecast.`),
    nextMaha && yearsTo(nextMaha.start) <= 3 && (l === 'hi'
      ? `महादशा ${monthYear(nextMaha.start, l)} में बदलती है — अब दूर नहीं। लंबी प्रतिबद्धताएँ (जो कई वर्ष चलेंगी) इस तिथि को ध्यान में रखकर तय करें, क्योंकि उसके बाद पृष्ठभूमि ${areas(l, nextMaha.lord)} की होगी।`
      : `The main period changes in ${monthYear(nextMaha.start, l)}, which is not far off. Weigh long commitments (ones that run for years) with that date in view, since the background after it is ${areas(l, nextMaha.lord)}.`),
    l === 'hi'
      ? 'दशा समय की खिड़की है, घटना नहीं। वह बताती है कि किस ओर ध्यान जाएगा; उसमें क्या होता है, यह आपके प्रयास और चुनाव पर भी निर्भर है।'
      : 'A period is a window of time, not an event. It says where attention goes; what happens in it also depends on your own effort and choices.',
  ].filter(Boolean))

  const any = verdicts[maha.lord] || Object.values(verdicts)[0] || null
  return {
    how: HOW, rows, changes, notes, basis: BASIS,
    rule: any && any.verse ? { verse: any.verse, cite: any.citation && !/BPHS/.test(any.citation) ? `BPHS ${any.citation}` : any.citation } : null,
  }
}
