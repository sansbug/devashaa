/**
 * The daśā reading (src/dashareading.js): what it may and may not say.
 *
 *   node web/test_dashareading.mjs [chart.json]
 */
import fs from 'node:fs'
import { buildDashaReading, HOW } from './src/dashareading.js'
import { makeNamer } from './src/naming.js'

let fail = 0

// The owner's style for every sentence of ours (2026-11-16, after ASD-STE100): one idea a sentence, at most 25
// words, no semicolon and no dash. A passage quoted from a text is the text's and is not checked. A yoga's name
// is the engine's key and may carry a dash.
const styleBreak = (lines, names = []) => {
  for (const raw of lines.flat(Infinity).filter(Boolean)) {
    const s = names.reduce((x, n) => x.split(n).join('X'), String(raw))
    for (const q of s.split(/(?<=[.?])\s+/)) {
      if (q.split(/\s+/).length > 25) return `too long: ${q}`
      if (/[;—–]/.test(q)) return `semicolon or dash: ${q}`
    }
  }
  return null
}
const ok = (name, cond, extra = '') => { console.log(`  ${cond ? 'OK' : 'FAIL'} ${name} ${cond ? '' : extra}`); if (!cond) fail++ }

console.log('How to read a daśā:')
ok('the explanation is given in both languages, line for line', HOW.en.length >= 3 && HOW.en.length === HOW.hi.length && HOW.hi.every(Boolean))
ok('a chart without a daśā yields no reading', buildDashaReading({ grahas: [], lagna_rasi: 0 }) === null)

async function loadChart() {
  if (process.argv[2]) return JSON.parse(fs.readFileSync(process.argv[2], 'utf8'))
  try {
    const r = await fetch('http://127.0.0.1:5174/api/chart', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date: '1990-01-01', time: '12:00', latitude: 28.6214, longitude: 77.2148, timezone: 'Asia/Kolkata' }),
    })
    return r.ok ? await r.json() : null
  } catch { return null }
}

const chart = await loadChart()
if (!chart) {
  console.log('\n(no chart payload: pass a file or start the local API to check a real chart)')
} else {
  console.log('\nThe reference chart:')
  const R = buildDashaReading(chart, makeNamer('common'), Date.now())
  ok('there is a reading', !!R)
  const roles = R.rows.map((r) => r.role)
  ok('it has the running main period and sub-period', roles.includes('maha') && roles.includes('antar'))
  ok('it has what comes next', roles.includes('nextAntar') || roles.includes('nextMaha'))
  ok('every row is written in both languages', R.rows.every((r) => r.title.en && r.title.hi && r.span.en && r.span.hi && r.brings.en && r.brings.hi && r.verdict.line.en && r.verdict.line.hi))
  ok('every row carries one of the four verdict states', R.rows.every((r) => ['favourable', 'adverse', 'contested', 'not_stated'].includes(r.verdict.state)))
  ok('the next sub-period starts when the running one ends', (() => {
    const a = R.rows.find((r) => r.role === 'antar'), n = R.rows.find((r) => r.role === 'nextAntar')
    return !a || !n || a.end === n.start
  })())
  ok('the next main period starts when the running one ends', (() => {
    const a = R.rows.find((r) => r.role === 'maha'), n = R.rows.find((r) => r.role === 'nextMaha')
    return !n || a.end === n.start
  })())
  ok('the rule is the text’s verse, with its locus', R.rule && R.rule.verse.length > 40 && /ch\.47/.test(R.rule.cite))
  ok('“what changes” and the notes are in both languages', R.changes.en.length && R.changes.en.length === R.changes.hi.length && R.notes.en.length && R.notes.en.length === R.notes.hi.length)
  ok('the notes carry what they rest on', R.basis.en.length >= 3)
  const ours = [...R.rows.flatMap((r) => [r.brings.en, r.verdict.line.en]), ...R.changes.en, ...R.notes.en, ...HOW.en]
  ok('none of our lines predicts ("will …")', !ours.some((s) => /\bwill\b/i.test(s)), ours.find((s) => /\bwill\b/i.test(s)))
  ok('none of our lines names a book', !ours.some((s) => /BPHS|Parāśara|Santhanam|Phaladīpikā/.test(s)))
  ok('no line prescribes a ritual, a gem, a charity or a remedy', !ours.some((s) => /\b(mantra|recit\w*|chant\w*|puja|pūjā|havan|homa|gem\w*|donat\w*|charit\w*|fast(ing)?|worship\w*|yantra|remed\w*)\b/i.test(s)))
  ok('no line gives medical, legal or investment instructions', !ours.some((s) => /\b(doctor|medic\w*|treatment|lawyer|invest\w*|buy|sell|stocks?|loan)\b/i.test(s)))
  ok('no line speaks of a death or a lifespan', !ours.some((s) => /\b(death|die|dead|lifespan|longevity|short-lived)\b/i.test(s)))
  ok('every date named is a month and a year', [...R.changes.en, ...R.rows.map((r) => r.span.en)].every((s) => !/\d{4}/.test(s) || /(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (19|20|21)\d\d/.test(s)))
  // the owner's complaint, 2026-11-16: "moves from (courage and siblings; career and status) to (career and status)"
  // — a sentence that names the same area on both sides of a change says nothing. An area is named once per sentence.
  const AREA = ['yourself', 'money', 'initiative', 'home', 'children', 'rivals', 'partnership', 'inheritance', 'fortune', 'career', 'income', 'expenses']
  const sentences = [...R.changes.en, ...R.notes.en].flatMap((s) => s.split(/(?<=\.)\s+/))
  const repeated = sentences.find((s) => AREA.some((w) => (s.toLowerCase().match(new RegExp(`\\b${w}\\b`, 'g')) || []).length > 1))
  ok('no sentence names the same area twice', !repeated, repeated)
  ok('no line uses the jargon "lean" or "the text’s rule"', !ours.some((s) => /\blean\b|text’s rule|stated verdict/i.test(s)), ours.find((s) => /\blean\b|text’s rule|stated verdict/i.test(s)))
  ok('a period’s verdict is said in plain words', R.rows.every((r) => /counts as (un)?favourable, because|is neutral\.|is mixed\./.test(r.verdict.line.en)))
  const br = styleBreak([HOW.en, R.basis.en, R.changes.en, R.notes.en, R.rows.map((r) => [r.span.en, r.brings.en, r.verdict.line.en])])
  ok('every sentence of ours is short and carries one idea', !br, br)
  ok('no change line says the same clause twice', R.changes.en.every((s) => { const parts = s.split(/(?<=\.)\s+/).map((x) => x.replace(/\([^)]*\)/g, '').replace(/^(The sub-period running now|The next one)\s*/, '')); return new Set(parts).size === parts.length }))
  console.log('')
  R.rows.forEach((r) => console.log(`  ${r.title.en} · ${r.span.en} · ${r.verdict.state}`))
  console.log('\n  changes:'); R.changes.en.forEach((s) => console.log('   ·', s))
  console.log('  notes:'); R.notes.en.forEach((s) => console.log('   ·', s))
}

console.log(fail ? `\n${fail} FAILED` : '\nALL PASS ✓')
process.exit(fail ? 1 : 0)
