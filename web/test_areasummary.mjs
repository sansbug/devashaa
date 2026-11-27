// node web/test_areasummary.mjs — needs the local API on :5174.
// Pins the summary's rules (areasummary.js): every paragraph says what it is; the text paragraphs quote only
// BPHS ch.24 lord-in-house verses, whole; a SENSITIVE verse is never quoted; "ours" never predicts or advises.
import { buildFindings, SENSITIVE } from './src/findings.js'
import { buildAreaSummary, KIND, ORDER } from './src/areasummary.js'
import { makeNamer } from './src/naming.js'

const CHARTS = [
  ['1975-06-25', '23:45', 28.6519, 77.2315, 'Asia/Kolkata'],  // Kumbh Lagn, 7th lord in the 5th: the source note
  ['1960-08-15', '10:00', 28.6519, 77.2315, 'Asia/Kolkata'],  // meets BPHS 16.19, a dated verse (a child at 30 or 36)
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
  const rendered = paras.filter((p) => p.kind === 'rendered')
  ok('rendered readings carry a citation and are not held ones', rendered.every((p) => p.cite && !SENSITIVE.en.test(p.en)), rendered.map((p) => p.cite).join())
  ok('rendered readings are the other classical texts, never BPHS', rendered.every((p) => !/BPHS/.test(p.cite)))
  const ours = paras.filter((p) => p.kind === 'ours')
  // owner's rule 2026-11-26: guidance is allowed when it states its basis; only a remedy for sale and fear are out
  ok('"ours" states its basis in the chart', ours.every((p) => /Basis:|factors? against it/.test(p.en)), ours.map((p) => p.en).join(' | '))
  ok('"ours" sells nothing and prescribes no remedy', ours.every((p) => !/\b(gem|gemstone|ritual|puja|mantra|charity|donat\w*|wear|buy|consult us|book a)\b/i.test(p.en)))
  ok('"ours" does not frighten', ours.every((p) => !/\b(danger|doom\w*|disaster|death|die|curse\w*|ruin\w*)\b/i.test(p.en)))
  const dated = paras.filter((p) => p.kind === 'dated')
  ok('a dated verse is BPHS, cited, and gives its age in this native’s calendar dates',
    dated.every((p) => /^BPHS I ch\.(15|16|20|22) /.test(p.cite) && /in your dates/.test(p.en) && /\b(19|20)\d\d\b/.test(p.en)), dated.map((p) => p.cite).join())
  ok('no dated paragraph speaks of a death, a disease or a danger', dated.every((p) => !SENSITIVE.en.test(p.en) && !/\b(disease|danger|fatal|fever)\b/i.test(p.en)))
  if (date === '1960-08-15') ok('this chart shows BPHS 16.19 under children', S.find((A) => A.key === 'children').paras.some((p) => p.kind === 'dated' && /ch\.16 v\.19/.test(p.cite)))
  const notes = paras.filter((p) => p.kind === 'note')
  ok('a source note never claims BPHS teaches the love-marriage rule', notes.every((p) => /did not find that rule in BPHS/.test(p.en)))
  ok('no planet name is lower-cased in a factor line', paras.every((p) => !/[;:] (surya|chandra|mangal|budh|guru|shukr|shani|rahu|ketu)\b/.test(p.en)))
}
console.log(failed ? `\n${failed} FAILED` : '\nall passed')
process.exit(failed ? 1 : 0)
