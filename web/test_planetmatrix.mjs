// The planet and house matrix: the words (planetmatrix.js) and the payload they are laid over.
import { CARRIES, NATURE, RELATION, RELATION_ORDER, WHY, OURS, FRACTION, notes, houseLine, nakshatraLord, lordState, SIGN_STATE, parts, partsLine, lordEffect, effectLine, EFFECT } from './src/planetmatrix.js'
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
  ok('the rules name the Nakshatr lord teaching as later than the texts', E.some((s) => /A later teaching says a Nakshatr takes its strength from its own lord/.test(s)) && E.some((s) => /do not state this teaching/.test(s)))
  ok('the rules say the lord does not change the benefic and malefic columns', E.some((s) => /does not change the benefic and malefic columns/.test(s)))
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

console.log('\nThe state of a Nakshatr lord:')
{
  const P = {
    jupiter: { graha: 'jupiter', sign: 11, house: 2, natural: 'benefic', functional: 'malefic', in_chart: { mercury: { compound: 'satru' } } },
    mercury: { graha: 'mercury', sign: 9, house: 12, natural: 'malefic', functional: 'benefic', in_chart: { jupiter: { compound: 'sama' } } },
    rahu: { graha: 'rahu', sign: 9, house: 12, natural: 'malefic', functional: null },
  }
  const G = { mercury: { dignity: { state: 'friend' } }, jupiter: { dignity: { state: 'own' } }, rahu: { dignity: null } }
  const s = lordState('jupiter', 'mercury', P, G)
  ok('Guru in Revati: the lord is Budh, with its own house and sign', s.lord === 'mercury' && s.house === 12 && s.sign === 9)
  ok('the lord\'s strength by sign and its two natures are its own', s.dignity === 'friend' && s.natural === 'malefic' && s.functional === 'benefic')
  ok('the two directions of the relation are kept apart', s.towards === 'satru' && s.back === 'sama')
  ok('a planet in its own Nakshatr is its own lord', lordState('jupiter', 'jupiter', P, G).towards === 'own' && lordState('jupiter', 'jupiter', P, G).back === 'own')
  ok('a node as the lord gives a place and a nature, no strength by sign, no relation', (() => { const r = lordState('jupiter', 'rahu', P, G); return r.house === 12 && r.natural === 'malefic' && r.dignity === null && r.towards === null && r.back === null })())
  ok('a lord in the planet\'s own house is marked', lordState('rahu', 'mercury', P, G).same_house === true && s.same_house === false)
  ok('no lord, no state', lordState('jupiter', null, P, G) === null)
  ok('every strength by sign has both languages', Object.values(SIGN_STATE).every((x) => x.en && x.hi && x.tone))
}

console.log('\nThe two parts behind a relation (Guru and Budh):')
{
  // Guru in Meen, Budh in Vrishabh: Budh is in the 3rd from Guru, Guru in the 11th from Budh: friends by place.
  const P = {
    jupiter: { friends: ['sun', 'moon', 'mars'], neutrals: ['saturn'], enemies: ['mercury', 'venus'], in_chart: { mercury: { temporary: 'friend', compound: 'sama' } } },
    mercury: { friends: ['sun', 'venus'], neutrals: ['mars', 'jupiter', 'saturn'], enemies: ['moon'], in_chart: { jupiter: { temporary: 'friend', compound: 'mitra' } } },
    rahu: {},
  }
  const a = parts('jupiter', 'mercury', P), b = parts('mercury', 'jupiter', P)
  ok('Guru counts Budh an enemy by nature and a friend by place', a.natural === 'enemy' && a.temporary === 'friend')
  ok('Budh counts Guru neutral by nature: the two directions differ', b.natural === 'neutral' && b.temporary === 'friend')
  ok('the line says both parts', partsLine(a, 'en') === 'enemy by nature, friend by place', partsLine(a, 'en'))
  ok('the Hindi line too', partsLine(a, 'hi') === 'स्वभाव से शत्रु, स्थान से मित्र')
  ok('no parts for a node or for a planet towards itself', parts('jupiter', 'rahu', P) === null && parts('rahu', 'jupiter', P) === null && parts('jupiter', 'jupiter', P) === null)
}

console.log('\nThe Nakshatr lord\'s effect on the planet (the owner\'s rule):')
{
  const P = {
    jupiter: { friends: ['sun', 'moon', 'mars'], neutrals: ['saturn'], enemies: ['mercury', 'venus'], in_chart: { mercury: { temporary: 'friend', compound: 'sama' } } },
    mercury: { friends: ['sun', 'venus'], neutrals: ['mars', 'jupiter', 'saturn'], enemies: ['moon'] },
    sun: {}, saturn: {}, rahu: { is_node: true }, ketu: { is_node: true },
  }
  ok('Guru in Revati: the lord Budh is its enemy by nature, so it reduces Guru', lordEffect('jupiter', 'mercury', P) === 'reduce')
  ok('the place in the chart does not soften it (the sum there is neutral)', P.jupiter.in_chart.mercury.compound === 'sama' && lordEffect('jupiter', 'mercury', P) === 'reduce')
  ok('a lord that is a friend by nature supports', lordEffect('jupiter', 'sun', P) === 'support')
  ok('a lord that is neutral by nature changes nothing', lordEffect('jupiter', 'saturn', P) === 'none')
  ok('the other direction is its own: Budh in a Nakshatr of Guru is not reduced', lordEffect('mercury', 'jupiter', P) === 'none')
  ok('a planet in its own Nakshatr is supported', lordEffect('jupiter', 'jupiter', P) === 'support')
  ok('nothing is said when the planet or the lord is a node', lordEffect('jupiter', 'rahu', P) === null && lordEffect('rahu', 'jupiter', P) === null && lordEffect('ketu', 'ketu', P) === null)
  const lines = [effectLine('reduce', false, 'Guru', 'Budh', 'en'), effectLine('support', false, 'Guru', 'Surya', 'en'), effectLine('support', true, 'Guru', 'Guru', 'en')]
  ok('the house line says who and what', lines[0] === 'Budh is an enemy of Guru by nature. This reduces the strength of Guru here.', lines[0])
  ok('the lines are short sentences', !styleBreak(lines) && !styleBreak([effectLine('reduce', false, 'गुरु', 'बुध', 'hi'), effectLine('support', true, 'गुरु', 'गुरु', 'hi')]))
  ok('no line for no change', effectLine('none', false, 'Guru', 'Shani', 'en') === '')
  ok('the three effects have both languages', Object.values(EFFECT).every((x) => x.en && x.hi && x.tone))
  ok('the rules state the effect and that it uses the fixed friendship', notes((k) => k, 'en').some((s) => /reduces its strength/.test(s)) && notes((k) => k, 'en').some((s) => /fixed friendship only/.test(s)))
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
  {
    const P = Object.fromEntries(m.planets.map((p) => [p.graha, p])), G = Object.fromEntries(chart.grahas.map((g) => [g.key, g]))
    const states = m.planets.map((p) => [p, lordState(p.graha, p.nakshatra_lord, P, G)])
    ok('every planet\'s Nakshatr lord has a state', states.every(([, s]) => s && s.house >= 1 && s.house <= 12))
    ok('the lord\'s house and sign are the lord\'s own row', states.every(([p, s]) => s.house === P[p.nakshatra_lord].house && s.sign === P[p.nakshatra_lord].sign))
    ok('every strength by sign the chart uses has a word', states.every(([, s]) => !s.dignity || SIGN_STATE[s.dignity]), states.map(([, s]) => s.dignity).join(' '))
    ok('the planet-to-lord relation is the one the server gives', states.every(([p, s]) => (s.towards || null) === (p.to_nakshatra_lord || null)))
    const SUM = { 'friend+friend': 'adhimitra', 'neutral+friend': 'mitra', 'enemy+friend': 'sama', 'friend+enemy': 'sama', 'neutral+enemy': 'satru', 'enemy+enemy': 'adhisatru' }
    const seven = m.planets.filter((p) => !p.is_node)
    ok('every relation in the chart is the sum of its two parts, as the verse gives it', seven.every((a) => seven.every((b) => {
      if (a === b) return true
      const pt = parts(a.graha, b.graha, P)
      return pt && SUM[`${pt.natural}+${pt.temporary}`] === a.in_chart[b.graha].compound
    })))
    ok('every effect in the chart follows the planet\'s fixed friendship towards the lord', states.every(([p, s]) => {
      if (p.is_node || P[s.lord].is_node) return s.effect === null
      if (s.lord === p.graha) return s.effect === 'support'
      return s.effect === (p.friends.includes(s.lord) ? 'support' : p.enemies.includes(s.lord) ? 'reduce' : 'none')
    }), states.map(([p, s]) => `${p.graha}:${s.effect}`).join(' '))
    ok('the Nakshatr lord rows carry the parts wherever they carry a relation', states.every(([, s]) => (s.towards && s.towards !== 'own') ? !!s.towards_parts : true))
    ok('the lord never moves a planet between the benefic and malefic columns', m.houses.every((h) => [...h.benefic.occupants, ...h.benefic.aspects].every((g) => P[g].natural === 'benefic') && [...h.malefic.occupants, ...h.malefic.aspects].every((g) => P[g].natural === 'malefic')))
    for (const [p, s] of states) console.log(`     ${p.graha.padEnd(8)} lord ${s.lord.padEnd(8)} house ${String(s.house).padStart(2)}  ${String(s.dignity).padEnd(12)} ${String(s.natural).padEnd(8)} → ${s.towards || '·'}  ← ${s.back || '·'}`)
  }
  ok('every relation to a Nakshatr lord has a word', m.planets.every((p) => !p.to_nakshatra_lord || RELATION[p.to_nakshatra_lord]))
  ok('every nature and relation the chart uses has a word', m.planets.every((p) => (!p.natural || NATURE[p.natural]) && (!p.functional || NATURE[p.functional])
    && Object.values(p.in_chart || {}).every((c) => !c.compound || RELATION[c.compound])) && m.houses.every((h) => h.occupants.every((o) => !o.to_lord || RELATION[o.to_lord])))
  for (const h of m.houses) console.log(`     ${String(h.house).padStart(2)}  in: ${h.occupants.map((o) => o.graha).join(',') || '·'}  full: ${h.full_aspects.join(',') || '·'}  + ${houseLine(h, (k) => en.grahaKey(k), 'en').benefic || '·'}  − ${houseLine(h, (k) => en.grahaKey(k), 'en').malefic || '·'}`)
} catch (e) { ok('the local API answers (start astrodev-api)', false, String(e)) }

console.log(fails ? `\n${fails} FAILED` : '\nALL PASS ✓')
process.exit(fails ? 1 : 0)
