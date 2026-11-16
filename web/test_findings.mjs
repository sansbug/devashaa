/**
 * Chart findings (src/findings.js): what they may and may not say.
 *
 *   node web/test_findings.mjs [chart.json]
 *
 * With a chart payload (a file, or the local API on :5174 if it is up) it builds the
 * findings for the reference chart and checks the rules the page relies on. Without
 * one it checks only the static tables.
 */
import fs from 'node:fs'
import { buildFindings, rankFindings, TOPICS, TAGS, SENSITIVE } from './src/findings.js'
import { makeNamer } from './src/naming.js'

let fail = 0
const ok = (name, cond, extra = '') => { console.log(`  ${cond ? 'OK' : 'FAIL'} ${name} ${cond ? '' : extra}`); if (!cond) fail++ }

console.log('Static tables:')
ok('every topic has both languages', TOPICS.every((t) => t.label.en && t.label.hi && t.sub.en && t.sub.hi))
ok('every tag has both languages', Object.values(TAGS).every((t) => t.en && t.hi && t.tone))

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
  const built = buildFindings(chart, makeNamer('common'))
  const { findings } = built
  ok('one finding per graha', findings.filter((f) => f.kind === 'graha').length === chart.grahas.length)
  ok('the ascendant lord leads the overall order', rankFindings(built, 'overall')[0].f.role === 'lagnaLord')
  const all = (f, l) => [f.title[l], f.sub[l], ...f.fact[l], ...f.why[l], ...f.supports[l], ...f.cautions[l], ...f.measured[l], ...f.check.map((c) => c.label[l])]
  const shownTexts = (f) => f.texts.filter((t) => t.says)
  ok('every finding is written in both languages', findings.every((f) => all(f, 'en').every(Boolean) && all(f, 'hi').every(Boolean)))
  ok('every finding has a fact and a tag', findings.every((f) => f.fact.en.length && TAGS[f.tag]))
  // OUR lines (not the texts') never predict and never speak for a book
  const plain = findings.flatMap((f) => [...f.fact.en, ...f.why.en, ...f.supports.en, ...f.cautions.en,
    ...(f.inference ? [f.inference.conclusion.en, ...f.inference.chain.map((c) => c.line.en)] : [])])
  ok('none of our own lines predicts ("will …")', !plain.some((s) => /\bwill\b/i.test(s.replace(/“[^”]*”/g, ''))), plain.find((s) => /\bwill\b/i.test(s)))
  ok('none of our own lines names a book', !plain.some((s) => /BPHS|Parāśara|Santhanam|Phaladīpikā|Sārāvalī/.test(s)))
  // rule 1 — a direct interpretation carries its text, its locus and why it applies
  const texts = findings.flatMap((f) => f.texts)
  ok('the reference chart has passages to show', texts.filter((t) => t.says).length > 5, String(texts.length))
  ok('every passage names its source text and its locus', texts.every((t) => t.source && t.source.text && t.cite), JSON.stringify(texts.find((t) => !(t.source && t.source.text && t.cite))))
  ok('every passage says why it applies, in both languages', texts.every((t) => t.applies && t.applies.en && t.applies.hi))
  ok('every passage is on a known tier', texts.every((t) => ['sloka', 'jaimini', 'classical', 'modern'].includes(t.tier)))
  ok('a passage is marked as the translator’s words or as our rendering', texts.every((t) => ['translation', 'rendering'].includes(t.kind)))
  ok('a death, a lifespan, a bereavement or a partner’s fidelity is never shown',
    texts.every((t) => !t.says || (!SENSITIVE.en.test(t.says) && !SENSITIVE.hi.test(t.says))))
  ok('a held-back passage is still listed with its reference', texts.filter((t) => t.held).every((t) => t.cite && !t.says))
  // rule 2 — a derived reading shows its chain and is only offered where there are passages to weigh
  const inf = findings.filter((f) => f.inference)
  ok('an inference is offered only where a passage is shown', inf.every((f) => f.texts.some((t) => t.says)))
  ok('every inference has a chain and a conclusion in both languages', inf.every((f) => f.inference.chain.length >= 2 && f.inference.conclusion.en && f.inference.conclusion.hi))
  ok('every measured step of a chain is cited', inf.every((f) => f.inference.chain.slice(1).every((c) => c.cite)), JSON.stringify(inf.flatMap((f) => f.inference.chain.slice(1)).find((c) => !c.cite)))
  // rule 3 — nothing modern is mixed in unless it is registered as modern
  ok('no modern-tier passage is mixed into a finding', texts.every((t) => t.tier !== 'modern'))
  for (const t of TOPICS.filter((x) => x.houses.length)) {
    const ranked = rankFindings(built, t.key)
    ok(`${t.key}: every listed finding says why it is there`, ranked.length > 0 && ranked.every((r) => r.because && r.because.en && r.because.hi))
    const lordKey = chart.analysis.bhava_phala.bhavas.find((b) => b.house === t.houses[0]).lord
    ok(`${t.key}: the lord of the ${t.houses[0]}th house comes first or shares first place`,
      ranked[0].f.touch(t.houses[0]) === 4 || ranked.some((r) => r.f.graha === lordKey))
  }
  const timing = rankFindings(built, 'timing')
  ok('timing lists only the running lords (or nothing, for a chart with no daśā)', timing.every((r) => [built.running.maha, built.running.antar].includes(r.f.graha)))
  console.log('\nOverall order:')
  rankFindings(built, 'overall').slice(0, 7).forEach(({ f }, i) => console.log(`  ${i + 1}. [${TAGS[f.tag].en}] ${f.title.en} — ${shownTexts(f).length} passage(s), ${f.texts.length - shownTexts(f).length} held back`))
  const first = rankFindings(built, 'overall')[0].f
  console.log('\nFirst finding, passages:')
  first.texts.forEach((t) => console.log(`  · [${t.tier}] ${t.cite} — ${t.says ? t.says.slice(0, 110) : '(held back)'}`))
  if (first.inference) console.log('  inference:', first.inference.conclusion.en)
}

console.log(fail ? `\n${fail} FAILED` : '\nALL PASS ✓')
process.exit(fail ? 1 : 0)
