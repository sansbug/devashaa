/**
 * "Watch it explained" — the walkthrough script (src/walkthrough.js).
 *
 * What it must never do: read out a verdict (a lord-in-house rule, a planet-in-
 * house reading — they can state a death or a lost child), name a book in the
 * spoken line (references stay behind the switch), or carry a birth detail.
 * What it must do: follow the chart — every house, graha and line it lights is
 * the chart's own — in both languages.
 *
 * Run:  node test_walkthrough.mjs   (with the local API on :5174 it also walks the reference chart)
 */
import { buildWalkthrough, spokenScript, readSeconds } from './src/walkthrough.js'
import { makeNamer } from './src/naming.js'
import { snapshotOf } from './src/shareCodec.js'

let failed = 0
const ok = (name, cond, detail = '') => { console.log(`  ${cond ? 'OK ' : 'XX '}${name} ${detail}`); if (!cond) failed += 1 }
const KEYS = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu']
const SIGN_LORD = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'saturn', 'jupiter']
const BOOKS = /BPHS|Par[āa][śs]ara|S[āa]r[āa]val[īi]|J[āa]taka|Santhanam|Cint[āa]ma[ṇn]i|\bch\.\s*\d|\bvv?\.\s*\d|sloka|śloka/i
const VERDICT = /death|\bdies?\b|short-lived|lose|loss of|child|progeny|poverty|disease|widow|मृत्यु|अल्पायु|संतान|रोग|दरिद्र/i

function checks(label, chart, namer) {
  const { steps } = buildWalkthrough(chart, namer)
  const keys = steps.map((s) => s.key)
  const has = new Set(keys)
  ok(`${label}: opens on the frame and closes on the close`, keys[0] === 'frame' && keys[keys.length - 1] === 'close', keys.join(' → '))
  ok(`${label}: every step is said in English and in Hindi`, steps.every((s) => s.say.en && s.say.hi && s.say.en !== s.say.hi))
  ok(`${label}: the Hindi is all Devanāgarī — no roman name slips into it`, steps.every((s) => !/[A-Za-z]/.test(s.say.hi)), steps.filter((s) => /[A-Za-z]/.test(s.say.hi)).map((s) => s.key).join(' '))
  ok(`${label}: no book is named in what is spoken — references stay behind the switch`, steps.every((s) => !BOOKS.test(s.say.en) && !BOOKS.test(s.say.hi)), steps.filter((s) => BOOKS.test(s.say.en)).map((s) => s.key).join(' '))
  ok(`${label}: nothing spoken reads as a verdict (death, a child lost, a short life…)`, steps.every((s) => !VERDICT.test(s.say.en) && !VERDICT.test(s.say.hi)), steps.filter((s) => VERDICT.test(s.say.en) || VERDICT.test(s.say.hi)).map((s) => s.key).join(' '))
  const a = chart.analysis || {}
  const rules = ((a.bhava_phala && a.bhava_phala.bhavas) || []).map((b) => b.lord_rule && b.lord_rule.effect).filter(Boolean)
  const gists = [...((a.classical && a.classical.readings) || []), ...((a.classical && a.classical.house_readings) || [])].flatMap((r) => (r.sources || []).map((s) => s.gist)).filter(Boolean)
  const script = spokenScript(steps, 'en') + spokenScript(steps, 'hi')
  ok(`${label}: no lord-in-house rule and no planet reading is in the spoken script`, [...rules, ...gists].every((x) => !script.includes(String(x).slice(0, 40))), `${rules.length} rules · ${gists.length} readings checked`)
  ok(`${label}: a quote (a yoga's cited effect) is on screen only, and only on the yogas step`, steps.every((s) => !s.quote || !s.quote.length || s.key === 'yogas') && steps.every((s) => !(s.quote || []).some((q) => s.say.en.includes(q.effect.slice(0, 30)))))
  const grahas = new Set(chart.grahas.map((x) => x.key))
  ok(`${label}: every house it lights is a house, every graha the chart's, every line joins two houses`,
    steps.every((s) => s.focus.houses.every((h) => h >= 1 && h <= 12) && s.focus.grahas.every((k) => KEYS.includes(k) && grahas.has(k)) && s.focus.lines.every((l) => l.from >= 1 && l.from <= 12 && l.to >= 1 && l.to <= 12 && l.from !== l.to)))
  const lord = chart.grahas.find((x) => x.key === SIGN_LORD[chart.lagna_rasi])
  const ll = steps.find((s) => s.key === 'lagnaLord')
  ok(`${label}: the lagna's lord is the sign's lord, and its line runs from the 1st house to where it sits`,
    !!ll && ll.focus.grahas[0] === lord.key && (lord.bhava === 1 ? ll.focus.lines.length === 0 : ll.focus.lines[0].from === 1 && ll.focus.lines[0].to === lord.bhava))
  const casts = a.drishti && a.drishti.graha && a.drishti.graha.casts && a.drishti.graha.casts.jupiter
  if (casts) {
    const asp = steps.find((s) => s.key === 'aspects')
    const want = Object.keys(casts.signs).map((sg) => ((+sg - chart.lagna_rasi + 12) % 12) + 1).sort((x, y) => x - y)
    ok(`${label}: Jupiter's lines are exactly its casts, full ones drawn full`, !!asp && asp.focus.lines.map((l) => l.to).join() === want.join() &&
      asp.focus.lines.every((l) => (l.kind === 'full') === (casts.signs[String((chart.lagna_rasi + l.to - 1) % 12)] >= 1)))
  }
  ok(`${label}: the daśā step is there exactly when the chart has a daśā`, has.has('dasha') === !!(chart.dasha && chart.dasha.variants))
  ok(`${label}: a step stays at least six seconds on screen`, steps.every((s) => readSeconds(s.say.en) >= 6))
  return steps
}

console.log('\na chart drawn for the test')
{
  const G = (key, rasi, lagna, dig = 'neutral', extra = {}) => ({ key, rasi, bhava: ((rasi - lagna + 12) % 12) + 1, degree: 10, minute: 0, retrograde: false,
    dignity: { state: dig }, nakshatra: { index: 1, name: 'Bharani', name_iast: 'Bharaṇī', pada: 2 }, ...extra })
  const lagna = 4   // Siṁha: its lord, the Sun
  const chart = {
    lagna_rasi: lagna, lagna_nakshatra: { index: 9, name: 'Magha', name_iast: 'Maghā', pada: 3 },
    grahas: [G('sun', 0, lagna, 'exalted'), G('moon', 3, lagna, 'own'), G('mars', 9, lagna, 'exalted'), G('mercury', 5, lagna, 'own'),
      G('jupiter', 8, lagna, 'own'), G('venus', 11, lagna, 'exalted'), G('saturn', 6, lagna, 'exalted'), G('rahu', 2, lagna), G('ketu', 8, lagna)],
    analysis: {
      drishti: { graha: { citation: 'BPHS Vol I ch.26 vv.2-5', casts: { jupiter: { from_sign: 8, signs: { 0: 1, 2: 1, 4: 1, 11: 0.75 }, grahas: { sun: 1 } } } } },
      yogas: { checked: 85, detected: [{ name: 'Hamsa', effect: 'A test effect.', citation: 'BPHS ch.75' }, { name: 'Moon–Venus mutual 3rd/11th', effect: 'A second test effect, never spoken.', citation: 'BPHS ch.39' }] },
      karakas: { atmakaraka: 'saturn', citation: 'BPHS Vol I ch.32' },
      bhava_phala: { bhavas: [{ house: 1, lord_rule: { citation: 'BPHS I ch.24 v.9', effect: 'the native will lose his first child' } }] },
      grahas: { sun: [{ name: 'dignity', citation: 'BPHS Vol I ch.3 vv.49-55' }] },
    },
  }
  const steps = checks('drawn', chart, makeNamer('common'))
  ok('drawn: three dignities at most, strongest kind first', steps.find((s) => s.key === 'dignity').focus.grahas.join() === 'sun,mars,venus')
  const yo = steps.find((s) => s.key === 'yogas')
  ok('drawn: a yoga with a proper name is spoken; a description of one is counted, not read out',
    yo.say.en.includes('Hamsa') && yo.say.en.includes('1 more') && !yo.say.en.includes('mutual') && yo.focus.names.length === 2)
  ok('drawn: in English a Sanskrit name carries its English one', steps.find((s) => s.key === 'lagnaLord').say.en.includes('Surya (Sun)'))
  ok('drawn: in the English name style, no doubled names', !buildWalkthrough(chart, makeNamer('english')).steps.some((s) => /Sun \(Sun\)/.test(s.say.en)))
  ok('drawn: the spoken script is one paragraph a step', spokenScript(steps, 'hi').split('\n\n').length === steps.length)
}

console.log('\nthe reference chart (from the local API)')
try {
  const r = await fetch('http://127.0.0.1:5174/api/chart', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: 'Reference', date: '1975-06-25', time: '22:30', lang: 'en', latitude: 26.4609, longitude: 80.3218, timezone: 'Asia/Kolkata' }),
  })
  const real = await r.json()
  for (const style of ['common', 'iast', 'english', 'devanagari']) checks(`reference/${style}`, real, makeNamer(style))
  const snapSteps = checks('reference, shared without birth details', snapshotOf(real), makeNamer('common'))
  const s = spokenScript(snapSteps, 'en') + spokenScript(snapSteps, 'hi')
  ok('a shared chart\'s script carries no date, time or place of birth', !['1975', '22:30', 'Kanpur', 'Kolkata', '26.46', '80.32'].some((x) => s.includes(x)))
} catch (e) {
  console.log(`  --  skipped: the local API is not running (${e.cause?.code || e.message})`)
}

console.log(failed ? `\n${failed} FAILED ✗` : '\nALL PASS ✓')
process.exit(failed ? 1 : 0)
