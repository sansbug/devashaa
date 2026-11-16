/**
 * The site's sentence style, over the whole interface string table (src/i18n.js + src/i18n-chrome.js).
 *
 * The owner's rule (2026-11-16, after ASD-STE100): one idea a sentence, at most 25 words, no semicolon and no
 * dash. A range of numbers ("0–56", "Ch.XVI–XX") is not a dash in a sentence. A few entries are fragments that
 * a panel joins to something else, or a name; they are listed in FRAGMENTS and are not checked.
 *
 *   node web/test_style.mjs
 */
import { STRINGS } from './src/i18n.js'

let fail = 0
const ok = (name, cond, extra = '') => { console.log(`  ${cond ? 'OK' : 'FAIL'} ${name} ${cond ? '' : extra}`); if (!cond) fail++ }

const FRAGMENTS = new Set([
  'footer.ephem', 'footer.privacyNote',        // "Powered by … —" + a link; "Privacy" + "— no cookies …"
  'sw.tip.sits_on_it', 'sw.tip.on_it_now',     // tooltip tails after a graha's name
  'matrix.trig.doubletransit',                 // "Jup–Sat double transit": a name
])
const breakOf = (s) => {
  const t = String(s).replace(/(\d)[–—](\d)/g, '$1-$2').replace(/([IVXL])[–—](?=[IVXL])/g, '$1-')
  for (const q of t.split(/(?<=[.?!])\s+/)) {
    if (q.split(/\s+/).length > 25) return `too long: ${q}`
    if (/[;—–]/.test(q)) return `semicolon or dash: ${q}`
  }
  return null
}

const entries = Object.entries(STRINGS).filter(([k, v]) => v && typeof v.en === 'string' && !FRAGMENTS.has(k))
ok('the string table is loaded', entries.length > 1000, String(entries.length))
const bad = entries.map(([k, v]) => [k, breakOf(v.en)]).filter(([, b]) => b)
ok('every English interface string is short and carries one idea', bad.length === 0, `${bad.length} break it, e.g. ${bad.slice(0, 5).map(([k, b]) => `${k} — ${b}`).join(' | ')}`)
ok('every fragment on the exemption list still exists', [...FRAGMENTS].every((k) => STRINGS[k]), [...FRAGMENTS].filter((k) => !STRINGS[k]).join(' '))
// a placeholder that the English carries must be in the Hindi too, or the panel prints a hole
const holes = entries.filter(([, v]) => v.hi).filter(([, v]) => (v.en.match(/\{[a-z_]+\}/g) || []).some((p) => !v.hi.includes(p)))
ok('every placeholder in an English string is in its Hindi string', holes.length === 0, holes.slice(0, 5).map(([k]) => k).join(' '))

console.log(fail ? `\n${fail} FAILED` : '\nALL PASS ✓')
process.exit(fail ? 1 : 0)
