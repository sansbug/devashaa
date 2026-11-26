// node web/test_areasummary.mjs — needs the local API on :5174.
// Pins the summary's rules (areasummary.js): every paragraph says what it is; the text paragraphs quote only
// BPHS ch.24 lord-in-house verses, whole; a SENSITIVE verse is never quoted; "ours" never predicts or advises.
import { buildFindings, SENSITIVE } from './src/findings.js'
import { buildAreaSummary, KIND, ORDER } from './src/areasummary.js'
import { makeNamer } from './src/naming.js'

const CHARTS = [
  ['1990-01-01', '12:00', 28.6519, 77.2315, 'Asia/Kolkata'],
  ['1985-08-15', '06:30', 19.076, 72.8777, 'Asia/Kolkata'],
  ['1974-07-01', '02:00', 28.6519, 77.2315, 'Asia/Kolkata'],
  ['2001-03-21', '18:45', 51.5074, -0.1278, 'Europe/London'],
]
let failed = 0
const ok = (name, cond, why = '') => { if (!cond) failed++; console.log(`  ${cond ? 'PASS' : '**FAIL**'}  ${name}${cond ? '' : `  → ${why}`}`) }

for (const [date, time, latitude, longitude, timezone] of CHARTS) {
  const r = await fetch('http://127.0.0.1:5174/api/chart', { method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ date, time, latitude, longitude, timezone }) })
  const c = await r.json()
  const namer = makeNamer('common')
  const S = buildAreaSummary(c, buildFindings(c, namer), namer)
  console.log(`\n${date} ${time}`)
  const paras = S.flatMap((A) => A.paras)
  ok('the areas come in the summary order', S.map((A) => A.key).join() === ORDER.join(), S.map((A) => A.key).join())
  ok('every paragraph has a known kind and both languages', paras.every((p) => KIND[p.kind] && p.en && p.hi))
  const quotes = paras.filter((p) => p.kind === 'text' && p.cite)
  ok('quoted verses are BPHS ch.24 only', quotes.every((p) => /ch\.24\b/.test(p.cite)), quotes.map((p) => p.cite).join())
  ok('no quoted verse is a sensitive one', quotes.every((p) => !SENSITIVE.en.test(p.en)))
  ok('each area has a chart paragraph first', S.every((A) => A.paras[0].kind === 'chart'))
  const ours = paras.filter((p) => p.kind === 'ours')
  ok('"ours" gives no age, no event and no instruction on money, health or law',
    ours.every((p) => !/\b(age|aged|years old|will (marry|have|get|lose|be))\b|invest|loan|doctor|medic|lawyer|share market/i.test(p.en)),
    ours.map((p) => p.en).join(' | '))
  ok('no planet name is lower-cased in a factor line', paras.every((p) => !/[;:] (surya|chandra|mangal|budh|guru|shukr|shani|rahu|ketu)\b/.test(p.en)))
}
console.log(failed ? `\n${failed} FAILED` : '\nall passed')
process.exit(failed ? 1 : 0)
