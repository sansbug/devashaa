// The planet and house matrix: the words (planetmatrix.js) and the payload they are laid over.
import { CARRIES, NATURE, RELATION, RELATION_ORDER, WHY, OURS, FRACTION, notes, houseLine, nakshatraLord } from './src/planetmatrix.js'
import { makeNamer } from './src/naming.js'

let fails = 0
const ok = (label, cond, detail) => { if (!cond) fails++; console.log(`  ${cond ? 'PASS' : '**FAIL**'}  ${label}${!cond && detail ? `  → ${detail}` : ''}`) }
const styleBreak = (lines) => {
  for (const raw of lines.flat(Infinity).filter(Boolean)) for (const q of String(raw).split(/(?<=[.?।])\s+/)) {
    if (q.split(/\s+/).length > 25) return `too long: ${q}`
    if (/[;—–]/.test(q)) return `semicolon or dash: ${q}`
  }
  return null
}
const NINE = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu']
const en = makeNamer('common'), hi = makeNamer('devanagari')

console.log('The words:')
{
  const E = notes((k) => en.grahaKey(k), 'en', ['sun']), H = notes((k) => hi.grahaKey(k), 'hi', ['sun'])
  ok('the rules are short sentences with one idea each', !styleBreak(E), styleBreak(E))
  ok('the Hindi rules too', !styleBreak(H), styleBreak(H))
  ok('English and Hindi carry the same number of rules', E.length === H.length)
  ok('the conjunction note shows only when planets share a sign', notes((k) => k, 'en', []).length === E.length - 1)
  ok('the rules use the owner\'s spellings', E.join(' ').includes('Mangal') && E.join(' ').includes('Guru') && E.join(' ').includes('Shani') && E.join(' ').includes('Lagn'))
  ok('the Hindi rules are all Devanāgarī', H.every((s) => !/[A-Za-z]/.test(s)), H.find((s) => /[A-Za-z]/.test(s)))
  ok('the rules say the count does not make an aspect good or bad', E.some((s) => /does not make the aspect good or bad/.test(s)))
  ok('the rules say no result is stated for the Nakshatr lord relation', E.some((s) => /state no result for that relation/.test(s)))
  ok('the rules say the nodes are given no aspect', E.some((s) => /names no aspect for Rahu and Ketu/.test(s)))
  ok('no rule predicts ("will …")', !E.some((s) => /\bwill\b/i.test(s)))
  ok('no book is named in the rules', !E.some((s) => /BPHS|Parāśara|Santhanam/.test(s)))
  ok('all nine planets have what they carry, in both languages', NINE.every((g) => CARRIES[g] && CARRIES[g].good.en && CARRIES[g].good.hi && CARRIES[g].hard.en && CARRIES[g].hard.hi))
  ok('what a planet carries is labelled as ours', /Our words/.test(OURS.en) && OURS.hi.length > 0)
  ok('the five relations have a mark and both names', RELATION_ORDER.length === 5 && RELATION_ORDER.every((k) => RELATION[k].mark && RELATION[k].en && RELATION[k].hi))
  ok('every nature and reason has both languages', [...Object.values(NATURE), ...Object.values(WHY)].every((x) => x.en && x.hi))
  ok('the three part aspects have a sign', FRACTION[0.25] === '¼' && FRACTION[0.5] === '½' && FRACTION[0.75] === '¾')
}

console.log('\nThe lord of a Nakshatr:')
{
  ok('Ashwini (1), Magha (10) and Mula (19) belong to Ketu', [1, 10, 19].every((i) => nakshatraLord(i) === 'ketu'))
  ok('Revati (27) belongs to Budh, not to Guru (the lord of its Raashi)', nakshatraLord(27) === 'mercury')
  ok('Punarvasu (7), Vishakha (16) and Purva Bhadrapada (25) belong to Guru', [7, 16, 25].every((i) => nakshatraLord(i) === 'jupiter'))
  ok('each of the nine lords holds three', ['ketu', 'venus', 'sun', 'moon', 'mars', 'rahu', 'jupiter', 'saturn', 'mercury'].every((g) => Array.from({ length: 27 }, (_, i) => nakshatraLord(i + 1)).filter((x) => x === g).length === 3))
  ok('no number, no lord', nakshatraLord(undefined) === null && nakshatraLord(0) === null && nakshatraLord(28) === null)
}

console.log('\nA house line:')
{
  const h = { benefic: { occupants: ['venus'], aspects: ['jupiter'] }, malefic: { occupants: [], aspects: ['mars', 'saturn'] } }
  const l = houseLine(h, (k) => en.grahaKey(k), 'en')
  ok('names the planet in it and the planet that aspects it', l.benefic === 'Shukr (in it), Guru (aspect)', l.benefic)
  ok('malefic side likewise', l.malefic === 'Mangal, Shani (aspect)', l.malefic)
  ok('an empty side is empty', houseLine({ benefic: { occupants: [], aspects: [] }, malefic: { occupants: [], aspects: [] } }, (k) => k, 'en').benefic === '')
}

console.log('\nA real chart (from the local API):')
try {
  const chart = await fetch('http://127.0.0.1:5174/api/chart', { method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ date: '1990-01-01', time: '12:00', latitude: 28.6214, longitude: 77.2148, timezone: 'Asia/Kolkata' }) }).then((r) => r.json())
  const m = chart.analysis.planet_matrix
  ok('the chart carries the matrix', m && !m.error && m.planets.length === 9 && m.houses.length === 12, m && m.error)
  ok('each planet sits in the house the chart gives it', m.planets.every((p) => chart.grahas.find((g) => g.key === p.graha).bhava === p.house))
  ok('every full aspect in a house is one its planet casts', m.houses.every((h) => h.full_aspects.every((g) => m.planets.find((p) => p.graha === g).aspect_houses.includes(h.house))))
  ok('the nodes cast none', m.planets.filter((p) => p.is_node).every((p) => p.aspect_houses.length === 0))
  ok('every planet has a Nakshatr and a Nakshatr lord', m.planets.every((p) => Number.isInteger(p.nakshatra) && p.nakshatra_lord))
  ok('the Nakshatr index is the one the chart gives the planet', m.planets.every((p) => chart.grahas.find((g) => g.key === p.graha).nakshatra.index - 1 === p.nakshatra),
    m.planets.map((p) => `${p.graha}:${p.nakshatra}/${chart.grahas.find((g) => g.key === p.graha).nakshatra.index}`).join(' '))
  ok('a relation to the Nakshatr lord is given only between the seven planets', m.planets.every((p) => (p.is_node || ['rahu', 'ketu'].includes(p.nakshatra_lord)) === (p.to_nakshatra_lord == null)))
  ok('the page\'s own lord table agrees with the server for every planet', m.planets.every((p) => nakshatraLord(chart.grahas.find((g) => g.key === p.graha).nakshatra.index) === p.nakshatra_lord))
  ok('every relation to a Nakshatr lord has a word', m.planets.every((p) => !p.to_nakshatra_lord || RELATION[p.to_nakshatra_lord]))
  ok('every nature and relation the chart uses has a word', m.planets.every((p) => (!p.natural || NATURE[p.natural]) && (!p.functional || NATURE[p.functional])
    && Object.values(p.in_chart || {}).every((c) => !c.compound || RELATION[c.compound])) && m.houses.every((h) => h.occupants.every((o) => !o.to_lord || RELATION[o.to_lord])))
  for (const h of m.houses) console.log(`     ${String(h.house).padStart(2)}  in: ${h.occupants.map((o) => o.graha).join(',') || '·'}  full: ${h.full_aspects.join(',') || '·'}  + ${houseLine(h, (k) => en.grahaKey(k), 'en').benefic || '·'}  − ${houseLine(h, (k) => en.grahaKey(k), 'en').malefic || '·'}`)
} catch (e) { ok('the local API answers (start astrodev-api)', false, String(e)) }

console.log(fails ? `\n${fails} FAILED` : '\nALL PASS ✓')
process.exit(fails ? 1 : 0)
