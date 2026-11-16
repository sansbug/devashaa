/**
 * "What this means for you" (src/conclusions.js): a conclusion is stated only when the readings agree.
 *
 *   node web/test_conclusions.mjs        (with the local API on :5174 it also reads two real charts)
 */
import { buildConclusions, RULE, PROJECTION_EDGE, PRIMARY, GROUP_OF } from './src/conclusions.js'
import { buildDashaReading } from './src/dashareading.js'
import { makeNamer } from './src/naming.js'

let fail = 0
const ok = (name, cond, extra = '') => { console.log(`  ${cond ? 'OK' : 'FAIL'} ${name} ${cond ? '' : extra}`); if (!cond) fail++ }
const styleBreak = (lines) => {
  for (const raw of lines.flat(Infinity).filter(Boolean)) for (const q of String(raw).split(/(?<=[.?])\s+/)) {
    if (q.split(/\s+/).length > 25) return `too long: ${q}`
    if (/[;—–]/.test(q)) return `semicolon or dash: ${q}`
  }
  return null
}

// ── a chart drawn for the test: Leo rising ─────────────────────────────────────────────────────
const lagna = 4
const G = (key, rasi, dig) => ({ key, rasi, bhava: ((rasi - lagna + 12) % 12) + 1, dignity: dig ? { state: dig } : null })
const base = (grahas, extra = {}) => ({ lagna_rasi: lagna, grahas, analysis: { lagna_profile: { grahas: [], yogakarakas: [] }, ...extra } })
const all = (over = {}) => ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu'].map((k) => over[k] || G(k, 0, 'neutral'))
const area = (C, key) => C.areas.find((x) => x.key === key)

console.log('The rule:')
{
  // Leo rising: the 10th is Taurus (Venus). Taurus is rasi 1 → the 10th house; Aquarius (rasi 10) is the 7th; Pisces (11) the 8th.
  const fav = { bhava_effects: { matches: [{ house: 10, clauses: [{ polarity: 'favourable' }] }] } }
  const adv = { bhava_effects: { matches: [{ house: 10, clauses: [{ polarity: 'adverse' }] }] } }
  const strong = base(all({ venus: G('venus', 1, 'own') }), fav)           // strong by sign, in the 10th, a favourable verse
  ok('two or more of the three readings in favour, none against: a strength', area(buildConclusions(strong), 'career').verdict === 'strength')
  ok('one reading in favour alone is a lean, never a strength', area(buildConclusions(base(all({ venus: G('venus', 2, 'own') }))), 'career').verdict === 'leanGood')
  const split = area(buildConclusions(base(all({ venus: G('venus', 1, 'own') }), adv)), 'career')
  ok('readings that disagree make it mixed, with every side given', split.verdict === 'mixed' && split.reasons.en.length >= 2)
  ok('two or more against, none in favour: an area to take care with', area(buildConclusions(base(all({ venus: G('venus', 11, 'debilitated') }), adv)), 'career').verdict === 'care')
  ok('none of the three speaks: the area is quiet', area(buildConclusions(base(all({ venus: G('venus', 2, 'neutral') }))), 'career').verdict === 'quiet')
  // the two readings reported beside the verdict never decide it
  const mx = (net) => ({ bhavas: [{ house: 10, net }] })
  const tempered = area(buildConclusions(strong, mx(-0.6)), 'career')
  ok('the projection going the other way does not change a strength; it is said on the other side', tempered.verdict === 'strength' && tempered.reasons.en.some((x) => x.startsWith('On the other side:') && /projection/.test(x)))
  ok('the projection alone never makes a conclusion', area(buildConclusions(base(all({ venus: G('venus', 2, 'neutral') })), mx(0.9)), 'career').verdict === 'quiet')
  ok('a projection score near the middle is not reported', area(buildConclusions(strong, mx(PROJECTION_EDGE - 0.01)), 'career').voices.projection === null)
  const mal = { ...strong, analysis: { ...strong.analysis, lagna_profile: { grahas: [{ graha: 'venus', nature: 'malefic' }], yogakarakas: [] } } }
  const m = area(buildConclusions(mal), 'career')
  ok('a ruler that counts as a difficult planet does not change a strength; it is said on the other side', m.verdict === 'strength' && m.reasons.en.some((x) => x.startsWith('On the other side:') && /difficult planet/.test(x)))
  ok('a verse that states both results counts on both sides', area(buildConclusions(base(all({ venus: G('venus', 2, 'neutral') }), { bhava_effects: { matches: [{ house: 10, clauses: [{ polarity: 'favourable' }, { polarity: 'adverse' }] }] } })), 'career').verdict === 'mixed')
  ok('the rule is said in both languages', RULE.en.length > 40 && RULE.hi.length > 40 && !/[A-Za-z]/.test(RULE.hi))
}

function checks(label, chart, matrix) {
  const namer = makeNamer('common')
  let dasha = null
  try { dasha = buildDashaReading(chart, namer) } catch { dasha = null }
  const C = buildConclusions(chart, matrix, dasha)
  ok(`${label}: six areas, each in exactly one group`, C.areas.length === 6 && Object.values(C.groups).flat().length === 6 && C.areas.every((x) => C.groups[GROUP_OF[x.verdict]].includes(x)))
  const prim = (x) => PRIMARY.map((v) => x.voices[v])
  const P = (x) => prim(x).filter((w) => w === '+' || w === '±').length, N = (x) => prim(x).filter((w) => w === '-' || w === '±').length
  ok(`${label}: a strength has two or more of the three readings in favour and none against`, C.areas.filter((x) => x.verdict === 'strength').every((x) => P(x) >= 2 && N(x) === 0))
  ok(`${label}: an area to take care with has two or more against and none in favour`, C.areas.filter((x) => x.verdict === 'care').every((x) => N(x) >= 2 && P(x) === 0))
  ok(`${label}: a lean has exactly one reading, on one side`, C.areas.filter((x) => /^lean/.test(x.verdict)).every((x) => P(x) + N(x) === 1))
  ok(`${label}: a mixed area has a reading on each side`, C.groups.mixed.every((x) => P(x) >= 1 && N(x) >= 1))
  ok(`${label}: a quiet area has none of the three`, C.groups.quiet.every((x) => P(x) + N(x) === 0))
  const ours = [C.summary.en, C.act.en, C.areas.map((x) => [x.head.en, x.reasons.en]), C.now ? C.now.en : []].flat(Infinity)
  const br = styleBreak(ours)
  ok(`${label}: every sentence is short and carries one idea`, !br, br)
  ok(`${label}: no line predicts ("will …")`, !ours.some((s) => /\bwill\b/i.test(s)), ours.find((s) => /\bwill\b/i.test(s)))
  ok(`${label}: no ritual, gem, charity or remedy`, !ours.some((s) => /\b(mantra|recit\w*|chant\w*|puja|pūjā|havan|gem\w*|donat\w*|charit\w*|fast(ing)?|worship\w*|remed\w*)\b/i.test(s)))
  ok(`${label}: no medical, legal or investment instruction, no death or lifespan`, !ours.some((s) => /\b(doctor|medic\w*|treatment|lawyer|invest\w*|buy|sell|stocks?|loan|death|die|dead|lifespan|longevity)\b/i.test(s)))
  ok(`${label}: no book is named`, !ours.some((s) => /BPHS|Parāśara|Santhanam|Phaladīpikā/.test(s)))
  const hi = [C.summary.hi, C.act.hi, C.areas.map((x) => [x.head.hi, x.reasons.hi])].flat(Infinity)
  ok(`${label}: the Hindi is all Devanāgarī`, hi.every((s) => !/[A-Za-z]/.test(s)), hi.find((s) => /[A-Za-z]/.test(s)))
  ok(`${label}: the summary's counts are the groups' sizes`, ['good', 'care', 'mixed', 'quiet'].every((v) => C.summary.en.includes(String(C.groups[v].length))))
  console.log(`     ${C.summary.en}`)
  for (const x of C.areas) console.log(`     ${x.verdict.padEnd(9)} ${x.label.en.padEnd(26)} ${Object.entries(x.voices).map(([k, v]) => `${k}:${v || '·'}`).join(' ')}`)
  return C
}

console.log('\nReal charts (from the local API):')
try {
  const post = (path, body) => fetch('http://127.0.0.1:5174' + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) }).then((r) => r.json())
  for (const [label, b] of [['sample', { date: '1990-01-01', time: '12:00', latitude: 28.6214, longitude: 77.2148, timezone: 'Asia/Kolkata' }],
    ['reference', { date: '1975-06-25', time: '22:30', latitude: 26.4499, longitude: 80.3319, timezone: 'Asia/Kolkata' }]]) {
    const [chart, matrix] = await Promise.all([post('/api/chart', b), post('/api/matrix', b)])
    checks(`${label}, with the projection`, chart, matrix)
    checks(`${label}, without it`, chart, null)
  }
} catch (e) {
  console.log(`  --  skipped: the local API is not running (${e.cause?.code || e.message})`)
}

console.log(fail ? `\n${fail} FAILED` : '\nALL PASS ✓')
process.exit(fail ? 1 : 0)
