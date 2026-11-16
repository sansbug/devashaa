/**
 * "What this means for you" — the chart's conclusions, in a few plain sentences.
 *
 * The owner (2026-11-16): a reader does not come for calculations; they want to know what the chart says for
 * them. The danger is that the site's separate readings can disagree (the weighted projection scores a planet
 * down for the houses it rules while a classical verse for the same planet speaks well of it).
 *
 * Each life area (lifeareas.js AREAS) is judged by THREE readings of its own houses, each saying +, − or nothing:
 *   sign    the planets that rule the area's houses are strong by sign (exalted, mūlatrikoṇa, own) or weak
 *           (debilitated, in an enemy's sign)                                              — BPHS dignity
 *   place   those rulers sit in an angle or a trine (1, 4, 5, 7, 9, 10), or in the 6th, 8th or 12th
 *                                                                                          — the house-lord method
 *   texts   the registered verses whose own condition this chart meets for those houses and which state a
 *           favourable or an adverse result (BPHS ch.13; chs 12, 14-18, 20-23)             — the texts
 *
 *   strength  : two or more of the three say +, none says −
 *   leanGood  : one says +, none says −          (said as a lean, never as a strength)
 *   care      : two or more say −, none says +
 *   leanCare  : one says −, none says +
 *   mixed     : at least one + and at least one −   (both sides are given)
 *   quiet     : none of the three speaks — the block says exactly that
 *
 * Two more readings are REPORTED BESIDE the verdict and never decide it:
 *   nature      the ruler counts as a benefic, a yogakāraka or a malefic for this ascendant (BPHS ch.34). That
 *               verdict is about the planet's own periods, not about the houses it rules.
 *   projection  the site's own weighted score for those houses (/api/matrix) — OURS, and largely built on
 *               `nature`, so letting both vote would count one signal twice. (The first version of this file
 *               did, and two real charts came out "0 strengths, 4 mixed": honest, and useless.)
 * Where one of these two goes the other way, the conclusion says so under "On the other side".
 *
 * Nothing here is new doctrine and no weight is hidden: it is a count of agreements, shown with its reasons.
 * The lines follow the site's sentence style and the life-area notes' rules: tendencies, not events; no
 * "will"; no ritual, gem or charity; no medical, legal or financial instruction. test_conclusions.mjs pins it.
 */
import { AREAS } from './lifeareas.js'

const SIGN_LORD = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'saturn', 'jupiter']
const GOOD = ['exalted', 'moolatrikona', 'own'], BAD = ['debilitated', 'enemy']
const STRONG_HOUSES = [1, 4, 5, 7, 9, 10], HARD = [6, 8, 12]
/** the projection's score for a house is reported only when it is clearly off the middle */
export const PROJECTION_EDGE = 0.25
export const PRIMARY = ['sign', 'place', 'texts'], BESIDE = ['nature', 'projection']

const VOICE = {
  sign: {
    '+': { en: 'The planet that rules it is strong by sign.', hi: 'इसका स्वामी ग्रह राशि से बलवान है।' },
    '-': { en: 'The planet that rules it is weak by sign.', hi: 'इसका स्वामी ग्रह राशि से दुर्बल है।' },
    '±': { en: 'Its two rulers differ. One is strong by sign and one is weak.', hi: 'इसके दो स्वामी अलग हैं। एक राशि से बलवान है और एक दुर्बल।' },
  },
  place: {
    '+': { en: 'Its ruler sits in a strong house of the chart.', hi: 'इसका स्वामी कुंडली के बलवान भाव में बैठा है।' },
    '-': { en: 'Its ruler sits in a difficult house (the 6th, 8th or 12th).', hi: 'इसका स्वामी कठिन भाव में बैठा है (छठा, आठवाँ या बारहवाँ)।' },
    '±': { en: 'Its two rulers differ. One sits in a strong house and one in a difficult house.', hi: 'इसके दो स्वामी अलग हैं। एक बलवान भाव में बैठा है और एक कठिन भाव में।' },
  },
  texts: {
    '+': { en: 'The classical verses that match it are favourable.', hi: 'इस पर लागू शास्त्रीय श्लोक अनुकूल हैं।' },
    '-': { en: 'The classical verses that match it are unfavourable.', hi: 'इस पर लागू शास्त्रीय श्लोक प्रतिकूल हैं।' },
    '±': { en: 'The classical verses that match it point both ways.', hi: 'इस पर लागू शास्त्रीय श्लोक दोनों ओर जाते हैं।' },
  },
  nature: {
    '+': { en: 'Its ruler counts as a helpful planet for this ascendant.', hi: 'इसका स्वामी इस लग्न के लिए शुभ ग्रह गिना जाता है।' },
    '-': { en: 'Its ruler counts as a difficult planet for this ascendant.', hi: 'इसका स्वामी इस लग्न के लिए पाप ग्रह गिना जाता है।' },
    '±': { en: 'Its two rulers differ for this ascendant. One counts as helpful and one as difficult.', hi: 'इस लग्न के लिए इसके दो स्वामी अलग हैं। एक शुभ गिना जाता है और एक पाप।' },
  },
  projection: {
    '+': { en: 'Our own weighted projection supports it.', hi: 'हमारा अपना भारित प्रक्षेपण इसका समर्थन करता है।' },
    '-': { en: 'Our own weighted projection goes against it.', hi: 'हमारा अपना भारित प्रक्षेपण इसके विपरीत जाता है।' },
  },
}
const HEAD = {
  strength: { en: (a) => `${a} is a strength in this chart.`, hi: (a) => `${a} इस कुंडली में एक बल है।` },
  leanGood: { en: (a) => `${a} leans favourable. One reading supports it.`, hi: (a) => `${a} अनुकूल ओर झुकता है। एक पठन इसका समर्थन करता है।` },
  care: { en: (a) => `${a} is an area to take care with.`, hi: (a) => `${a} ऐसा क्षेत्र है जहाँ सावधानी चाहिए।` },
  leanCare: { en: (a) => `${a} leans difficult. One reading goes against it.`, hi: (a) => `${a} कठिन ओर झुकता है। एक पठन इसके विपरीत जाता है।` },
  mixed: { en: (a) => `${a} is mixed. The readings do not agree.`, hi: (a) => `${a} मिला-जुला है। पठन आपस में सहमत नहीं हैं।` },
  quiet: { en: (a) => `${a}: the chart says little either way.`, hi: (a) => `${a}: कुंडली किसी भी ओर बहुत कम कहती है।` },
}
const OTHER = { en: 'On the other side:', hi: 'दूसरी ओर:' }
/** when none of the three main readings speaks, what the two side readings say is given as just that */
const SILENT = { en: 'The three main readings are silent.', hi: 'तीनों मुख्य पठन मौन हैं।' }
/** "You is a strength" is not a sentence: in a conclusion the first area is named by what its house holds */
const NAME = { self: { en: 'Self and body', hi: 'स्वयं और शरीर' } }
const DO = {
  good: { en: 'Build on your strengths. Effort put there is well placed.', hi: 'अपने बलों पर आगे बढ़ें। वहाँ लगाया गया प्रयास सही जगह लगा है।' },
  care: { en: 'Go steadily where care is needed, and keep a margin. This is a reason to prepare, not a reason to worry.', hi: 'जहाँ सावधानी चाहिए वहाँ धीरे और स्थिर चलें, और गुंजाइश रखें। यह तैयारी का कारण है, चिंता का नहीं।' },
  mixed: { en: 'For a mixed area, read both sides below before you decide anything on it.', hi: 'मिले-जुले क्षेत्र में कुछ तय करने से पहले नीचे दोनों पक्ष पढ़ें।' },
}
export const RULE = {
  en: 'Each conclusion rests on three readings of the area: its ruler’s strength by sign, where that ruler sits, and the classical verses that match. It is stated firmly only when they agree. These are tendencies, not fixed events.',
  hi: 'हर निष्कर्ष क्षेत्र के तीन पठनों पर टिका है: स्वामी का राशि-बल, स्वामी कहाँ बैठा है, और लागू शास्त्रीय श्लोक। यह दृढ़ता से तभी कहा जाता है जब वे सहमत हों। ये प्रवृत्तियाँ हैं, तय घटनाएँ नहीं।',
}
/** which group a verdict is shown under */
export const GROUP_OF = { strength: 'good', leanGood: 'good', care: 'care', leanCare: 'care', mixed: 'mixed', quiet: 'quiet' }

/** One voice's word from a tally of + and − */
const say = (p, n) => (p && n ? '±' : p ? '+' : n ? '-' : null)

/**
 * @param chart   the /api/chart payload
 * @param matrix  the /api/matrix payload (only `bhavas[].house` and `.net` are read), or null
 * @param dasha   buildDashaReading(chart, namer) or null
 * @returns { areas:[{key,label,houses,verdict,voices,head,reasons}], groups:{good,care,mixed,quiet}, summary, act, now, rule, usedProjection }
 */
export function buildConclusions(chart, matrix = null, dasha = null) {
  const lagna = chart.lagna_rasi
  const g = (k) => (chart.grahas || []).find((x) => x.key === k)
  const a = chart.analysis && !chart.analysis.error ? chart.analysis : {}
  const prof = (a.lagna_profile && a.lagna_profile.grahas) || []
  const nature = (k) => (prof.find((p) => p.graha === k) || {}).nature
  const yks = ((a.lagna_profile && a.lagna_profile.yogakarakas) || []).map((y) => (typeof y === 'string' ? y : y && (y.graha || y.key))).filter(Boolean)
  const lordOf = (h) => SIGN_LORD[(lagna + h - 1) % 12]
  const verses = [
    ...(((a.bhava_effects && !a.bhava_effects.error && a.bhava_effects.matches) || []).map((m) => ({ house: m.house, clauses: m.clauses || [] }))),
    ...(((a.dhana_bhava && !a.dhana_bhava.error && a.dhana_bhava.matches) || []).map((m) => ({ house: 2, clauses: m.clauses || [] }))),
  ]
  const net = (h) => { const b = matrix && (matrix.bhavas || []).find((x) => x.house === h); return b && typeof b.net === 'number' ? b.net : null }
  const both = (f) => ({ en: f('en'), hi: f('hi') })
  const count = (xs, f) => xs.filter(f).length

  const areas = AREAS.map((A) => {
    const lords = [...new Set(A.houses.map(lordOf))].map(g).filter(Boolean)
    const cl = verses.filter((v) => A.houses.includes(v.house)).flatMap((v) => v.clauses)
    const nets = A.houses.map(net).filter((x) => x != null)
    const mean = nets.length ? nets.reduce((s, x) => s + x, 0) / nets.length : null
    const voices = {
      sign: say(count(lords, (x) => x.dignity && GOOD.includes(x.dignity.state)), count(lords, (x) => x.dignity && BAD.includes(x.dignity.state))),
      place: say(count(lords, (x) => STRONG_HOUSES.includes(x.bhava)), count(lords, (x) => HARD.includes(x.bhava))),
      texts: say(count(cl, (c) => c.polarity === 'favourable'), count(cl, (c) => c.polarity === 'adverse')),
      nature: say(count(lords, (x) => nature(x.key) === 'benefic' || yks.includes(x.key)), count(lords, (x) => nature(x.key) === 'malefic')),
      projection: mean == null ? null : mean >= PROJECTION_EDGE ? '+' : mean <= -PROJECTION_EDGE ? '-' : null,
    }
    const prim = PRIMARY.map((v) => voices[v])
    const pos = count(prim, (w) => w === '+' || w === '±'), neg = count(prim, (w) => w === '-' || w === '±')
    const verdict = pos && neg ? 'mixed' : pos >= 2 ? 'strength' : pos === 1 ? 'leanGood' : neg >= 2 ? 'care' : neg === 1 ? 'leanCare' : 'quiet'
    const side = GROUP_OF[verdict]                       // good | care | mixed | quiet
    const line = (l, v) => VOICE[v][voices[v]][l]
    const reasons = both((l) => {
      const mine = PRIMARY.filter((v) => voices[v])
      if (side === 'quiet') { const b = BESIDE.filter((v) => voices[v]); return b.length ? [`${SILENT[l]} ${b.map((v) => line(l, v)).join(' ')}`] : [] }
      if (side === 'mixed') return [...mine, ...BESIDE.filter((v) => voices[v])].map((v) => line(l, v))
      const want = side === 'good' ? '+' : '-'
      const withIt = BESIDE.filter((v) => voices[v] === want), against = BESIDE.filter((v) => voices[v] && voices[v] !== want)
      return [...mine, ...withIt].map((v) => line(l, v)).concat(against.length ? [`${OTHER[l]} ${against.map((v) => line(l, v)).join(' ')}`] : [])
    })
    return { key: A.key, label: A.label, houses: A.houses, verdict, voices, head: both((l) => HEAD[verdict][l]((NAME[A.key] || A.label)[l])), reasons }
  })

  const groups = { good: [], care: [], mixed: [], quiet: [] }
  for (const x of areas) groups[GROUP_OF[x.verdict]].push(x)
  const n = (k) => groups[k].length
  const summary = both((l) => (l === 'hi'
    ? `छह क्षेत्रों में से ${n('good')} अनुकूल ओर ${n('good') === 1 ? 'है' : 'हैं'}, ${n('care')} में सावधानी चाहिए, ${n('mixed')} ${n('mixed') === 1 ? 'मिला-जुला है' : 'मिले-जुले हैं'} और ${n('quiet')} पर कुंडली कम कहती है।`
    : `Of six areas of life, ${n('good')} ${n('good') === 1 ? 'is' : 'are'} on the favourable side, ${n('care')} ${n('care') === 1 ? 'needs' : 'need'} care, ${n('mixed')} ${n('mixed') === 1 ? 'is' : 'are'} mixed and ${n('quiet')} ${n('quiet') === 1 ? 'is' : 'are'} quiet.`))
  const act = both((l) => ['good', 'care', 'mixed'].filter((k) => n(k)).map((k) => DO[k][l]))
  // now and next: the daśā reading's own first two notes (the running period, then the coming one)
  const now = dasha ? both((l) => (dasha.notes[l] || []).slice(0, 2)) : null
  return { areas, groups, summary, act, now, rule: RULE, usedProjection: !!matrix }
}
