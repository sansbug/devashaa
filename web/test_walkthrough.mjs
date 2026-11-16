/**
 * "Explain my chart" — the plain-words, topic-by-topic script (src/walkthrough.js).
 *
 * What it must never do: put a lord-in-house rule or any care-sensitive verdict (a
 * death, a lost child, childlessness, a vice) in the plain lines; name a book in
 * what is spoken (references stay behind the switch); carry a birth detail.
 * What it must do: follow the chart — every house, graha and line it lights is the
 * chart's own, the lord it names is the house's lord, sitting where it sits — in
 * both languages, one topic per house.
 *
 * Run:  node test_walkthrough.mjs   (with the local API on :5174 it also walks the reference chart)
 */
import { buildWalkthrough, spokenScript, readSeconds, CARE, HOUSE, NATURE, OURS } from './src/walkthrough.js'
import { makeNamer, yogaName } from './src/naming.js'
import { snapshotOf } from './src/shareCodec.js'

let failed = 0
const ok = (name, cond, detail = '') => { console.log(`  ${cond ? 'OK ' : 'XX '}${name} ${detail}`); if (!cond) failed += 1 }
const KEYS = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu']
const SIGN_LORD = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'saturn', 'jupiter']
const EN_ORD = (n) => `${n}${n % 10 === 1 && n !== 11 ? 'st' : n % 10 === 2 && n !== 12 ? 'nd' : n % 10 === 3 && n !== 13 ? 'rd' : 'th'}`
const BOOKS = /BPHS|Par[āa][śs]ara|S[āa]r[āa]val[īi]|J[āa]taka|Santhanam|Cint[āa]ma[ṇn]i|\bch\.\s*\d|\bvv?\.\s*\d|sloka|śloka/i
const VERDICT = /death|\bdies?\b|short-lived|\blose\b|loss of|childless|bereft|deprived|poverty|widow|thie(f|ves)|longevity|मृत्यु|अल्पायु|नाश|वंचित|दरिद्र|चोर|आयु/i
const P = (o, l) => (o ? o[l] : null)

function checks(label, chart, namer) {
  const { steps } = buildWalkthrough(chart, namer)
  const keys = steps.map((s) => s.key)
  const bh = (chart.analysis && chart.analysis.bhava_phala && chart.analysis.bhava_phala.bhavas) || []
  ok(`${label}: the basics first, then one topic per house in order, then the close`,
    keys[0] === 'basics' && keys[keys.length - 1] === 'close' && keys.filter((k) => k.startsWith('house')).join() === bh.map((b) => `house${b.house}`).join(), keys.join(' → '))
  ok(`${label}: every topic has a title and numbered lines, in English and in Hindi`,
    steps.every((s) => s.title.en && s.title.hi && s.lines.en.length && s.lines.en.length === s.lines.hi.length))
  const devOnly = (s) => [s.title.hi, ...s.lines.hi, ...s.chips.hi.flatMap((c) => [c.label, c.text]), s.text && s.text.hi.note].filter(Boolean).every((x) => !/[A-Za-z]/.test(x))
  ok(`${label}: the Hindi is all Devanāgarī — no roman name slips into it`, steps.every(devOnly), steps.filter((s) => !devOnly(s)).map((s) => s.key).join(' '))
  ok(`${label}: no book is named in what is spoken — references stay behind the switch`, steps.every((s) => !BOOKS.test(s.say.en) && !BOOKS.test(s.say.hi)), steps.filter((s) => BOOKS.test(s.say.en)).map((s) => s.key).join(' '))
  ok(`${label}: nothing spoken or shown plainly reads as a verdict (a death, a lost child, a short life…)`,
    steps.every((s) => !VERDICT.test(s.say.en) && !VERDICT.test(s.say.hi) && ![...s.chips.en, ...s.chips.hi].some((c) => VERDICT.test(c.text))),
    steps.filter((s) => VERDICT.test(s.say.en) || VERDICT.test(s.say.hi)).map((s) => s.key).join(' '))
  const rules = bh.map((b) => b.lord_rule && b.lord_rule.effect).filter(Boolean)
  const script = spokenScript(steps, 'en') + spokenScript(steps, 'hi')
  ok(`${label}: no lord-in-house rule is in the plain lines — it is behind the click`, rules.every((x) => !script.includes(String(x).slice(0, 40))), `${rules.length} rules`)
  const shown = steps.filter((s) => s.text && s.text.en.quote)
  ok(`${label}: a rule shown behind the click is the chart's own rule, word for word, and carries no care-sensitive verdict`,
    shown.every((s) => { const b = bh.find((x) => `house${x.house}` === s.key); return b && s.text.en.quote === b.lord_rule.effect && !CARE.en.test(s.text.en.quote) && !CARE.hi.test(s.text.en.quote) }),
    `${shown.length} of ${rules.length} shown`)
  ok(`${label}: a rule held back says where to read it`, steps.filter((s) => s.text && !s.text.en.quote).every((s) => /Bhaavs/.test(s.text.en.note) && /भाव व योग/.test(s.text.hi.note)))
  const grahas = new Set(chart.grahas.map((x) => x.key))
  ok(`${label}: every house it lights is a house, every graha the chart's, every line joins two houses`,
    steps.every((s) => s.focus.houses.every((h) => h >= 1 && h <= 12) && s.focus.grahas.every((k) => KEYS.includes(k) && grahas.has(k))
      && s.focus.lines.every((l) => l.from >= 1 && l.from <= 12 && l.to >= 1 && l.to <= 12 && l.from !== l.to) && (s.focus.main == null || s.focus.houses.includes(s.focus.main))))
  const g = (k) => chart.grahas.find((x) => x.key === k)
  ok(`${label}: each house names its sign's lord, says where the lord sits, and draws the line there`,
    bh.every((b) => {
      const s = steps.find((x) => x.key === `house${b.house}`)
      const lord = SIGN_LORD[b.sign], at = g(lord).bhava
      return b.lord === lord && b.lord_in_house === at && s.focus.main === b.house && s.focus.grahas[0] === lord
        && s.lines.en[1].includes(at === b.house ? 'sits in this house' : `sits in your ${EN_ORD(at)} house`)
        && (at === b.house || s.focus.lines.some((l) => l.kind === 'lord' && l.from === b.house && l.to === at))
    }))
  ok(`${label}: the planets it says sit in a house are the ones that do`,
    bh.every((b) => {
      const s = steps.find((x) => x.key === `house${b.house}`)
      const occ = chart.grahas.filter((x) => x.bhava === b.house)
      return occ.length ? occ.every((x) => s.lines.hi.some((ln) => ln.includes(makeNamer('devanagari').grahaKey(x.key)))) && occ.every((x) => s.lines.en.flatMap((ln) => ln.split(/(?<=\.)\s+/)).filter((q) => /\bsits? in this house\.$/.test(q) && q.includes(namer.grahaKey(x.key))).length === 1)
        : s.lines.en.includes('No planet sits in this house.')
    }))
  ok(`${label}: only the full and three-quarter aspects are named, and they are the chart's`,
    bh.every((b) => {
      const s = steps.find((x) => x.key === `house${b.house}`)
      const want = (b.aspects_in || []).filter((x) => x.strength >= 0.75).map((x) => x.graha)
      const line = s.lines.en.find((ln) => /looks? at this house with|^No planet looks/.test(ln))
      const E = makeNamer('english'), C = namer
      return want.length ? want.every((k) => line.includes(C.grahaKey(k))) : line === 'No planet looks at this house fully.'
    }))
  // the planet topics: fixed sentence patterns, every slot from the chart (the owner's brief, 2026-11-16)
  const ps = steps.filter((s) => s.key.startsWith('graha_'))
  const lagnaLord = SIGN_LORD[chart.lagna_rasi]
  ok(`${label}: one topic per planet, the Lagna's lord first, between the basics and the houses`,
    ps.length === chart.grahas.length && ps[0].key === `graha_${lagnaLord}` && keys.indexOf(ps[0].key) === 1 && keys.indexOf(ps[ps.length - 1].key) < keys.indexOf('house1'), ps.map((s) => s.key).join(' '))
  // the style holds for EVERY topic (the houses, the opening, the timing and the close too)
  const sent = steps.flatMap((s) => s.lines.en.flatMap((ln) => ln.split(/(?<=\.)\s+/)))
  const long = sent.find((x) => x.split(/\s+/).length > 25)
  ok(`${label}: a sentence has at most 25 words`, !long, long)
  const joined = sent.find((x) => /[;—–]|\band\b.*\bbut\b|, which\b/.test(x))
  ok(`${label}: a sentence carries one idea — no semicolon, no dash, no trailing clause`, !joined, joined)
  // one line a planet is OURS and says so; outside it no sentence states a trait, and nowhere a prediction
  const oursOf = (s, l) => s.lines[l].filter((x) => x.startsWith(OURS[l]))
  ok(`${label}: each planet has exactly one line of ours, labelled as ours, in both languages`, ps.every((s) => oursOf(s, 'en').length === 1 && oursOf(s, 'hi').length === 1))
  ok(`${label}: every sentence of ours carries "usually" and names the planet's own house`,
    ps.every((s) => { const x = g(s.key.slice(6)), parts = oursOf(s, 'en')[0].split(/(?<=\.)\s+/); return parts.length === 2 && parts.every((p) => /\busually\b/.test(p)) && parts[1].includes(`In your ${EN_ORD(x.bhava)} house`) && parts[0].includes(NATURE[x.key].en) }))
  const rest = ps.flatMap((s) => s.lines.en.filter((x) => !x.startsWith(OURS.en)).flatMap((ln) => ln.split(/(?<=\.)\s+/)))
  const trait = rest.find((x) => /\b(usually|shows|stands for|tends?|personality|mind)\b/i.test(x))
  ok(`${label}: outside the line of ours, no planet sentence states a trait`, !trait, trait)
  // a topic never says the same sentence twice (one planet running both periods is described once)
  const twice = steps.find((s) => { const q = s.lines.en.flatMap((ln) => ln.split(/(?<=\.)\s+/)); return new Set(q).size !== q.length })
  ok(`${label}: no topic says the same sentence twice`, !twice, twice && twice.key)
  const will = sent.find((x) => /\bwill\b/i.test(x))
  ok(`${label}: no sentence predicts ("will …")`, !will, will)
  ok(`${label}: each planet topic states the chart's own sign, house and degree`,
    ps.every((s) => { const x = g(s.key.slice(6)); return s.focus.main === x.bhava && s.lines.en[0].includes(`in your ${EN_ORD(x.bhava)} house`) && s.title.en.includes(`${Math.floor(x.degree)}°`) && s.lines.en[0].includes(namer.rasi(x.rasi)) }))
  const sig = (k) => ((chart.analysis.grahas && chart.analysis.grahas[k]) || []).find((x) => x.name === 'baladi')
  // the owner's spellings (docs/spelling-list.md, 2026-11-16): Bal, Kumar, and "Passive" for the last stage
  const STAGES = { bala: 'Bal', kumara: 'Kumar', yuva: 'Yuva', vriddha: 'Vriddha', mrita: 'Passive' }
  ok(`${label}: the stage named is the engine's, and there is none where the chart carries none`,
    ps.every((s) => { const v = sig(s.key.slice(6)), ln = s.lines.en.find((x) => /stage/.test(x)); return v ? !!ln && ln.includes(`the ${STAGES[v.value]} stage`) : !ln }))
  ok(`${label}: a node gets no sign-strength line and no yoga line`,
    ps.filter((s) => /rahu|ketu/.test(s.key)).every((s) => !s.lines.en.some((x) => /sign (of|for)|exalted in|debilitated in|\bYog\b/.test(x))))
  const det = (chart.analysis.yogas && chart.analysis.yogas.detected) || []
  ok(`${label}: a planet is said to form a yoga only when the engine detected it`,
    ps.every((s) => s.lines.en.filter((x) => / forms [A-Z]\w+ Yog\b/.test(x)).every((x) => det.some((y) => x.includes(yogaName(String(y.name).split(' ')[0]))))))
  ok(`${label}: the timing topic is there exactly when the chart has a daśā`, keys.includes('now') === !!(chart.dasha && chart.dasha.variants))
  ok(`${label}: a topic stays at least eight seconds on screen`, steps.every((s) => readSeconds(s.say.en) >= 8))
  ok(`${label}: the spoken script is one paragraph a topic`, spokenScript(steps, 'en').split('\n\n').length === steps.length && spokenScript(steps, 'hi').split('\n\n').length === steps.length)
  return steps
}

console.log('\nthe plain labels')
ok('twelve houses, each with a title, a meaning and a chip, in both languages', Object.keys(HOUSE).length === 12 && Object.values(HOUSE).every((h) => ['title', 'of', 'chip'].every((f) => h[f].en && h[f].hi)))
ok('no house is labelled with longevity or death', Object.values(HOUSE).every((h) => !VERDICT.test(h.chip.en) && !VERDICT.test(h.chip.hi) && !VERDICT.test(h.of.en)))

ok('what each planet stands for is in both languages, and holds no verdict, remedy or prediction', Object.keys(NATURE).length === 9
  && Object.values(NATURE).every((n) => n.en && n.hi && !/[A-Za-z]/.test(n.hi) && !VERDICT.test(n.en) && !VERDICT.test(n.hi) && !/\b(will|illness|disease|divorce|wealthy|poor|mantra|gem)\b/i.test(n.en)))

{
  // "courage … shows in courage and siblings" says nothing: a planet's words never repeat a house's
  const words = (s) => s.toLowerCase().split(/[^a-zऀ-ॿ]+/).filter((w) => w.length > 2 && w !== 'and' && w !== 'और')
  const clash = ['en', 'hi'].flatMap((l) => Object.values(NATURE).flatMap((n) => Object.values(HOUSE).flatMap((h) => words(n[l]).filter((w) => words(h.of[l]).includes(w)))))
  ok('no planet word repeats a house word', clash.length === 0, clash.join(' '))
}

console.log('\na chart drawn for the test')
{
  const lagna = 4   // Siṁha: its lord, the Sun
  const G = (key, rasi, dig = 'neutral') => ({ key, rasi, bhava: ((rasi - lagna + 12) % 12) + 1, degree: 10, minute: 0, retrograde: false, longitude: rasi * 30 + 10,
    dignity: { state: dig }, nakshatra: { index: 1, name: 'Bharani', name_iast: 'Bharaṇī', pada: 2, quality: 'Fierce' } })
  const grahas = [G('sun', 0, 'exalted'), G('moon', 3, 'own'), G('mars', 9, 'exalted'), G('mercury', 5, 'own'), G('jupiter', 8, 'own'),
    G('venus', 11, 'exalted'), G('saturn', 6, 'exalted'), G('rahu', 2), G('ketu', 8)]
  const bhavas = Array.from({ length: 12 }, (_, i) => {
    const h = i + 1, sign = (lagna + i) % 12, lord = SIGN_LORD[sign]
    return { house: h, sign, lord, lord_in_house: grahas.find((x) => x.key === lord).bhava, occupants: grahas.filter((x) => x.bhava === h).map((x) => x.key),
      karaka: 'jupiter', aspects_in: h === 7 ? [{ graha: 'saturn', strength: 1 }, { graha: 'moon', strength: 0.75 }, { graha: 'mars', strength: 0.25 }] : [],
      significations: { citation: `BPHS Vol I, Ch.11 v.${h + 1}` },
      lord_rule: { citation: `BPHS I ch.24 v.${h}`, effect: h === 1 ? 'If the ascendant lord is in the 9th, the native will lose his first child.' : `If the ${h} lord is placed so, the native will be wealthy and happy.` } }
  })
  const chart = {
    lagna_rasi: lagna, lagna_nakshatra: { index: 9, name: 'Magha', name_iast: 'Maghā', pada: 3, quality: 'Fierce' }, grahas,
    analysis: { bhava_phala: { bhavas }, karakas: { atmakaraka: 'saturn' } },
  }
  const steps = checks('drawn', chart, makeNamer('common'))
  const h1 = steps.find((s) => s.key === 'house1'), h2 = steps.find((s) => s.key === 'house2'), h7 = steps.find((s) => s.key === 'house7')
  ok('drawn: a rule that speaks of a lost child is held back; a clean one is shown', h1.text.en.quote === null && h2.text.en.quote.startsWith('If the 2 lord'))
  ok('drawn: the 7th names its full and three-quarter aspects, not the quarter one', h7.lines.en.some((ln) => ln === 'Shani looks at this house with a full aspect. Chandra looks at this house with a three-quarter aspect.'))
  ok('drawn: in English a Sanskrit name carries its English one', h1.lines.en[0].includes('Surya (Sun)'))
  ok('drawn: no doubled names — not in the English style, not for the nodes', !buildWalkthrough(chart, makeNamer('english')).steps.some((s) => /Sun \(Sun\)/.test(s.lines.en.join(' '))) && !steps.some((s) => /Rahu \(R/.test(s.lines.en.join(' '))))
}

console.log('\nthe reference chart (from the local API)')
try {
  const body = (lang) => JSON.stringify({ name: 'Reference', date: '1975-06-25', time: '22:30', lang, latitude: 26.4609, longitude: 80.3218, timezone: 'Asia/Kolkata' })
  const get = (lang) => fetch('http://127.0.0.1:5174/api/chart', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: body(lang) }).then((r) => r.json())
  const [en, hi] = await Promise.all([get('en'), get('hi')])
  for (const style of ['common', 'iast', 'english', 'devanagari']) checks(`reference/${style}`, en, makeNamer(style))
  checks('reference, cast in Hindi', hi, makeNamer('common'))
  const a = buildWalkthrough(en, makeNamer('common')).steps, b = buildWalkthrough(hi, makeNamer('common')).steps
  ok('the same rules are held back in English and in Hindi', a.every((s, k) => !s.text || (!!s.text.en.quote) === (!!b[k].text.en.quote)),
    a.filter((s) => s.text && s.text.en.quote).map((s) => s.key).join(' '))
  const snapSteps = checks('reference, shared without birth details', snapshotOf(en), makeNamer('common'))
  const s = spokenScript(snapSteps, 'en') + spokenScript(snapSteps, 'hi')
  ok('a shared chart\'s script carries no date, time or place of birth', !['1975', '22:30', 'Kanpur', 'Kolkata', '26.46', '80.32'].some((x) => s.includes(x)))
} catch (e) {
  console.log(`  --  skipped: the local API is not running (${e.cause?.code || e.message})`)
}

console.log(failed ? `\n${failed} FAILED ✗` : '\nALL PASS ✓')
process.exit(failed ? 1 : 0)
