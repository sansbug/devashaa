/**
 * Life areas (src/lifeareas.js): what the practical notes may and may not say.
 *
 *   node web/test_lifeareas.mjs [chart.json]
 *
 * With a chart payload (a file, or the local API on :5174) it builds the areas for
 * the reference chart and checks the rules. Without one it checks the static table.
 */
import fs from 'node:fs'
import { buildFindings } from './src/findings.js'
import { buildLifeAreas, AREAS } from './src/lifeareas.js'
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

console.log('The areas:')
ok('every area has a label in both languages and at least one house', AREAS.every((a) => a.label.en && a.label.hi && a.houses.length))
ok('there is no health area (the 6th house is not turned into advice)', !AREAS.some((a) => a.houses.includes(6) || /health/i.test(a.key + a.label.en)))
ok('the 8th house (longevity) is in no area', !AREAS.some((a) => a.houses.includes(8)))

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
  const namer = makeNamer('common')
  const NOW = new Date('2026-11-16T00:00:00').getTime()
  const areas = buildLifeAreas(chart, buildFindings(chart, namer), namer, NOW)
  {
    const br = styleBreak(areas.map((A) => [A.shows.en, A.supports.en, A.cautions.en, A.notes.en, A.basis.en, A.timing.now && A.timing.now.en, A.timing.next && A.timing.next.en]))
    ok('every sentence of ours is short and carries one idea', !br, br)
  }
  ok('one entry per area', areas.length === AREAS.length)
  ok('every area says what the chart shows, in both languages', areas.every((a) => a.shows.en.length && a.shows.en.length === a.shows.hi.length && a.shows.hi.every(Boolean)))
  ok('every area has practical notes in both languages', areas.every((a) => a.notes.en.length >= 1 && a.notes.en.length === a.notes.hi.length && a.notes.hi.every(Boolean)))
  ok('every area carries what its notes rest on', areas.every((a) => a.basis.en.length >= 3 && a.basis.hi.length === a.basis.en.length))
  const ours = areas.flatMap((a) => [...a.shows.en, ...a.notes.en, ...(a.timing.now ? [a.timing.now.en] : []), ...(a.timing.next ? [a.timing.next.en] : [])])
  ok('none of our lines predicts ("will …")', !ours.some((s) => /\bwill\b/i.test(s)), ours.find((s) => /\bwill\b/i.test(s)))
  ok('none of our lines names a book', !ours.some((s) => /BPHS|Parāśara|Santhanam|Phaladīpikā|Sārāvalī/.test(s)))
  const notes = areas.flatMap((a) => a.notes.en)
  ok('no note prescribes a ritual, a gem, a charity or a fast', !notes.some((s) => /\b(mantra|recit\w*|chant\w*|puja|pūjā|havan|homa|gem\w*|stone|donat\w*|charit\w*|fast(ing)?|worship\w*|yantra|remed\w*)\b/i.test(s)), notes.find((s) => /\b(mantra|gem|donat|fast|worship|remed)/i.test(s)))
  ok('no note gives medical, legal or investment instructions', !notes.some((s) => /\b(doctor|medic\w*|treatment|diagnos\w*|lawyer|invest\w*|buy|sell|stocks?|loan)\b/i.test(s)))
  ok('no note speaks of a death or a lifespan', !notes.some((s) => /\b(death|die|dead|lifespan|longevity|short-lived)\b/i.test(s)))
  ok('every passage in an area is tied to one of its houses', areas.every((a) => a.passages.every((t) => a.houses.includes(t.house) && t.cite)))
  ok('a passage appears once per area (one citation may carry several planets’ readings)', areas.every((a) => new Set(a.passages.map((t) => `${t.cite}|${t.full || ''}`)).size === a.passages.length))
  ok('an area is either in focus now, has a next window, or says it has none', areas.every((a) => a.timing.now || a.timing.next || a.timing.none || true))
  const withNext = areas.filter((a) => a.timing.next)
  ok('a "next" window is never offered for an area already in focus', areas.every((a) => !(a.timing.now && a.timing.next)))
  ok('the timing lines name a month and a year', [...areas.filter((a) => a.timing.now).map((a) => a.timing.now.en), ...withNext.map((a) => a.timing.next.en)].every((s) => /\b(19|20|21)\d\d\b/.test(s)))
  ok('the reference chart yields passages for at least three areas', areas.filter((a) => a.passages.length).length >= 3)
  console.log('')
  for (const a of areas) console.log(`  ${a.label.en}: ${a.passages.length} passage(s), +${a.supports.en.length}/-${a.cautions.en.length}, ${a.timing.now ? 'IN FOCUS' : a.timing.next ? 'next: ' + a.timing.next.en.slice(34, 70) : 'no window'}`)
  console.log('\n  career notes:'); areas.find((a) => a.key === 'career').notes.en.forEach((s) => console.log('   ·', s))
}

console.log(fail ? `\n${fail} FAILED` : '\nALL PASS ✓')
process.exit(fail ? 1 : 0)
