/**
 * Chart findings — the handful of things in a chart worth reading first, each
 * with its reasoning laid out: the calculated fact, what the tradition makes of
 * it, what supports it, what counts against it, and what is still to be checked.
 *
 * Built ONLY from what /api/chart already computed (placements, dignity, house
 * lordship, graded aspects, the ascendant's functional natures, Viṁśopaka, the
 * detected yogas, the daśā tree, the classical concordance). Nothing is generated
 * and no rule is invented. The owner's provenance rules (2026-11-15):
 *
 *  1. DIRECT — a traditional interpretation is shown when its passage is in the
 *     registered library, its condition matches the calculated chart, and its
 *     source (text, translator, locus) is named. It is always presented as what
 *     the TEXT says (`texts`), never as a fact about the person.
 *  2. DERIVED — a synthesis is shown only with its chain of cited steps, its
 *     conflicting factors, and the label "our inference" (`inference`).
 *  3. MODERN — only with a registered author and passage, on its own tier.
 *  4. UNSUPPORTED — left out. No trait is attached to a planet or a node that a
 *     registered passage does not attach.
 *
 * Our own lines (`fact`, `why`, `supports`, `cautions`) state placements and the
 * method that reads them; they never say what will happen. A passage that speaks
 * of a death, a lifespan, a bereavement or a partner's fidelity is not shown
 * here (SENSITIVE) — the site's standing rule for those readings; the finding
 * says where the passage can be read.
 *
 * THE ORDER IS OURS (synthesis tier). The texts do not rank placements; `weight`
 * is a reading order, not a strength and not a prediction. A topic re-sorts the
 * same findings by how directly each one touches that topic's houses.
 */
import { makeNamer } from './naming.js'
import { HOUSE } from './walkthrough.js'

const SIGN_LORD = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'saturn', 'jupiter']
const EN_ORD = (n) => `${n}${n % 10 === 1 && n !== 11 ? 'st' : n % 10 === 2 && n !== 12 ? 'nd' : n % 10 === 3 && n !== 13 ? 'rd' : 'th'}`
const HI_ORD = ['', 'पहले', 'दूसरे', 'तीसरे', 'चौथे', 'पाँचवें', 'छठे', 'सातवें', 'आठवें', 'नौवें', 'दसवें', 'ग्यारहवें', 'बारहवें']
const NODES = ['rahu', 'ketu']
const HARD_HOUSES = [6, 8, 12]
const KENDRA = [1, 4, 7, 10]

/** Passages the findings do not put in front of a reader: a death or a lifespan, a bereavement, a partner's
 *  fidelity. (Narrower than the walkthrough's CARE: wealth, family, character and standing ARE shown, attributed.) */
export const SENSITIVE = {
  en: /\b(destr(oy|oyed|uction)\w* (at once )?(of |both )?(the )?(coborn|co-born|preborn|afterborn|later born|wife|children|mother|father)|(preborn|afterborn|coborn|co-born|wife|children) will be destroyed|no offspring|no children|quit the world|death|die[sd]?|dying|dead|kill\w*|short-lived|short life|longevity|life-?span|widow\w*|bereave\w*|bereft of (his |her |a |the )?(child\w*|sons?|daughters?|wife|husband|spouse|father|mother|parents?|progeny|issue)|childless|issueless|adulter\w*|unchaste|los(e|es|ing|s) (of )?(his |her |a |the |one's )?(child\w*|sons?|daughters?|wife|husband|spouse|father|mother|parents?|brothers?|sisters?)|other(s'|'s)? (wives|women|men)|another('s)? (wife|woman))\b/i,
  hi: /मृत्यु|मरण|अल्पायु|आयु क्षीण|विधवा|विधुर|निःसंतान|संतानहीन|व्यभिचार|परस्त्री|परपुरुष|(पुत्र|संतान|पत्नी|पति|पिता|माता)[^।]{0,12}(नाश|हानि|वियोग)/,
}
/** Why a ch.13 clause applies to this chart — our words for the verse's own condition (api/dhana_bhava.py). */
const DHANA_WHY = {
  lord2_well_placed: (l, n, o, c) => (l === 'hi' ? `आपके दूसरे भाव के स्वामी ${n(c.grahas[0])} ${o(c.houses[0])} भाव में हैं — श्लोक की शर्त: दूसरे भाव में, या केन्द्र/त्रिकोण में।` : `Your 2nd lord, ${n(c.grahas[0])}, is in your ${o(c.houses[0])} house — the verse’s condition: in the 2nd, or in an angle or a trine.`),
  lord2_in_6_8_12: (l, n, o, c) => (l === 'hi' ? `आपके दूसरे भाव के स्वामी ${n(c.grahas[0])} ${o(c.houses[0])} भाव में हैं — श्लोक की शर्त: छठे, आठवें या बारहवें में।` : `Your 2nd lord, ${n(c.grahas[0])}, is in your ${o(c.houses[0])} house — the verse’s condition: in the 6th, 8th or 12th.`),
  benefic_in_2nd: (l, n, o, c) => (l === 'hi' ? `दूसरे भाव में नैसर्गिक शुभ ग्रह: ${c.grahas.map(n).join(', ')}।` : `A natural benefic is in your 2nd house: ${c.grahas.map(n).join(', ')}.`),
  malefic_in_2nd: (l, n, o, c) => (l === 'hi' ? `दूसरे भाव में नैसर्गिक पाप ग्रह: ${c.grahas.map(n).join(', ')}।` : `A natural malefic is in your 2nd house: ${c.grahas.map(n).join(', ')}.`),
  jupiter_lord2_in_2nd: (l, n) => (l === 'hi' ? `${n('jupiter')} आपके दूसरे भाव के स्वामी हैं और दूसरे ही भाव में हैं।` : `${n('jupiter')} rules your 2nd house and is in your 2nd house.`),
  jupiter_with_mars: (l, n, o, c) => (l === 'hi' ? `${n('jupiter')} और ${n('mars')} एक ही राशि में हैं (${o(c.houses[0])} भाव)।` : `${n('jupiter')} is with ${n('mars')}, in your ${o(c.houses[0])} house.`),
  lords_2_11_exchange: (l, n, o, c) => (l === 'hi' ? `दूसरे भाव के स्वामी ${n(c.grahas[0])} ग्यारहवें में और ग्यारहवें के स्वामी ${n(c.grahas[1])} दूसरे में हैं।` : `Your 2nd lord ${n(c.grahas[0])} is in the 11th and your 11th lord ${n(c.grahas[1])} is in the 2nd.`),
  lords_2_11_join_kendra_kona: (l, n, o, c) => (l === 'hi' ? `दूसरे और ग्यारहवें भाव के स्वामी (${c.grahas.map(n).join(', ')}) ${o(c.houses[0])} भाव में साथ हैं — एक केन्द्र/त्रिकोण।` : `Your 2nd and 11th lords (${c.grahas.map(n).join(', ')}) are together in your ${o(c.houses[0])} house — an angle or a trine.`),
  lord2_kendra_lord11_trine_from_it: (l, n, o, c) => (l === 'hi' ? `दूसरे भाव के स्वामी ${n(c.grahas[0])} केन्द्र (${o(c.houses[0])} भाव) में हैं और ग्यारहवें के स्वामी ${n(c.grahas[1])} उनसे त्रिकोण में।` : `Your 2nd lord ${n(c.grahas[0])} is in an angle (your ${o(c.houses[0])} house) and your 11th lord ${n(c.grahas[1])} is in a trine from it.`),
  lords_in_evil_houses_malefic_in_2nd: (l, n, o, c) => (l === 'hi' ? `दूसरे और ग्यारहवें भाव के स्वामी दोनों छठे/आठवें/बारहवें में हैं और दूसरे भाव में पाप ग्रह है (${c.grahas.map(n).join(', ')})।` : `Your 2nd and 11th lords are both in the 6th, 8th or 12th and a malefic is in your 2nd house (${c.grahas.map(n).join(', ')}).`),
  lords_2_11_with_malefics: (l, n, o, c) => (l === 'hi' ? `दूसरे और ग्यारहवें भाव के स्वामी दोनों पाप ग्रहों के साथ हैं (${c.grahas.map(n).join(', ')})।` : `Your 2nd and 11th lords are both with malefics (${c.grahas.map(n).join(', ')}).`),
}
const DHANA_NOT = {
  one_planet_rules_both: { en: 'Verses 4–5 describe a relation between the 2nd lord and the 11th lord. In this chart one planet rules both houses, so they are not applied.', hi: 'श्लोक 4–5 दूसरे और ग्यारहवें भाव के स्वामियों के आपसी संबंध की बात करते हैं। इस कुंडली में दोनों भावों का स्वामी एक ही ग्रह है, इसलिए वे लागू नहीं किए गए।' },
  alternative_ambiguous: { en: 'Verse 5’s alternative (aspect or conjunction of Jupiter and Venus) is ambiguous in the translation and is not evaluated.', hi: 'श्लोक 5 का विकल्प (गुरु और शुक्र की दृष्टि या युति) अनुवाद में अस्पष्ट है; उसे नहीं जाँचा गया।' },
  combustion_has_no_orb_in_the_text: { en: 'Verse 7’s “combust” is not evaluated: the text gives no orb for combustion.', hi: 'श्लोक 7 का “अस्त” नहीं जाँचा गया: ग्रंथ अस्त की कोई अंश-सीमा नहीं देता।' },
}
const sensitive = (s) => SENSITIVE.en.test(String(s || '')) || SENSITIVE.hi.test(String(s || ''))
const BPHS = { text: 'Bṛhat Parāśara Horā Śāstra', author: 'Parāśara', translator: 'R. Santhanam', tier: 'sloka' }
const withBook = (c) => (c && !/BPHS|Parāśara/.test(c) ? `BPHS ${c}` : c)

const DIG = {
  exalted: { en: 'exalted', hi: 'उच्च का', gloss: { en: 'at its strongest', hi: 'अपनी सबसे बलवान स्थिति में' }, w: 82, good: true },
  moolatrikona: { en: 'in its mūlatrikoṇa sign', hi: 'मूलत्रिकोण में', gloss: { en: 'very strong', hi: 'बहुत बलवान' }, w: 78, good: true },
  own: { en: 'in its own sign', hi: 'स्वराशि में', gloss: { en: 'strong', hi: 'बलवान' }, w: 74, good: true },
  friend: { en: 'in a friend’s sign', hi: 'मित्र की राशि में', gloss: { en: 'comfortable', hi: 'सहज' } },
  neutral: { en: 'in a neutral sign', hi: 'सम राशि में', gloss: null },
  enemy: { en: 'in an enemy’s sign', hi: 'शत्रु की राशि में', gloss: { en: 'uncomfortable', hi: 'असहज' }, bad: true },
  debilitated: { en: 'debilitated', hi: 'नीच का', gloss: { en: 'at its weakest', hi: 'अपनी सबसे दुर्बल स्थिति में' }, w: 80, bad: true },
}

export const TAGS = {
  key: { en: 'Key placement', hi: 'मुख्य स्थिति', tone: 'key' },
  strong: { en: 'Favourable dignity', hi: 'अनुकूल बल', tone: 'good' },
  weak: { en: 'Weak by sign', hi: 'राशि से दुर्बल', tone: 'hard' },
  mixed: { en: 'Mixed — read closely', hi: 'मिश्रित — ध्यान से पढ़ें', tone: 'mixed' },
  context: { en: 'Needs context', hi: 'संदर्भ चाहिए', tone: 'mixed' },
  named: { en: 'Named combination', hi: 'नामित योग', tone: 'key' },
  plain: { en: 'Placement', hi: 'स्थिति', tone: 'plain' },
}

/** The topics a reader can ask about, each read from its own houses (the houses' meanings are HOUSE's). */
export const TOPICS = [
  { key: 'overall', label: { en: 'Overall chart', hi: 'पूरी कुंडली' }, sub: { en: 'the most important findings', hi: 'सबसे महत्त्वपूर्ण बातें' }, houses: [] },
  { key: 'career', label: { en: 'Career', hi: 'आजीविका' }, sub: { en: 'profession and status', hi: 'कर्म और प्रतिष्ठा' }, houses: [10] },
  { key: 'wealth', label: { en: 'Wealth', hi: 'धन' }, sub: { en: 'resources and gains', hi: 'धन और लाभ' }, houses: [2, 11] },
  { key: 'marriage', label: { en: 'Marriage', hi: 'विवाह' }, sub: { en: 'partnership', hi: 'साझेदारी' }, houses: [7] },
  { key: 'timing', label: { en: 'Periods and timing', hi: 'दशा और समय' }, sub: { en: 'what is running now', hi: 'अभी क्या चल रहा है' }, houses: [] },
]

const list = (xs, l) => (xs.length < 2 ? xs.join('') : `${xs.slice(0, -1).join(', ')} ${l === 'hi' ? 'और' : 'and'} ${xs[xs.length - 1]}`)
const year = (s) => (/^(\d{4})/.exec(String(s || '')) || [])[1] || ''

export function dashaTree(chart) {
  const dv = chart.dasha && chart.dasha.variants
  if (!dv) return null
  return dv[String(chart.dasha.default_year_days)] || dv[String(chart.dasha.default_year_days).replace('.0', '')] || dv['360'] || Object.values(dv)[0] || null
}

/**
 * @param chart  the /api/chart payload (a snapshot works; it simply has no daśā)
 * @param namer  the reader's name style, for English; Hindi is always Devanāgarī
 * @returns      { findings, running }  — findings unsorted; rank them with rankFindings()
 */
export function buildFindings(chart, namer = makeNamer('common')) {
  const H = makeNamer('devanagari'), E = makeNamer('english')
  const N = { en: namer, hi: H }
  const plainEn = namer.style === 'english'
  const lagna = chart.lagna_rasi
  const grahas = chart.grahas || []
  const g = (k) => grahas.find((x) => x.key === k)
  const a = chart.analysis && !chart.analysis.error ? chart.analysis : {}
  const bh = (a.bhava_phala && a.bhava_phala.bhavas) || []
  const B = (h) => bh.find((b) => b.house === h) || null
  const prof = (a.lagna_profile && a.lagna_profile.grahas) || []
  const P = (k) => prof.find((p) => p.graha === k) || null
  const cls = a.classical || {}
  /** Registered passages on a graha in a house / in a sign (other classical texts; our renderings of them). */
  const concordance = (k, h, s) => [
    ...((cls.house_readings || []).filter((r) => r.graha === k && r.house === h).flatMap((r) => (r.sources || []).map((src) => ({ src, on: 'house' })))),
    ...((cls.readings || []).filter((r) => r.graha === k && r.sign === s).flatMap((r) => (r.sources || []).map((src) => ({ src, on: 'sign' })))),
  ]
  /** One passage, as the finding carries it. `says` is null when the passage is SENSITIVE. */
  const passage = ({ says, source, cite, kind, applies }) => ({
    says: says && !sensitive(says) ? says : null, held: !!says && sensitive(says),
    // the whole passage, for a reader who asks to see it: shown entire or not at all, never with a clause cut out
    full: says || null,
    source, cite: cite || null, kind, tier: (source && source.tier) || 'classical', applies,
  })
  // BPHS ch.13 vv.1-7 — the 2nd-house verses whose own conditions this chart meets (api/dhana_bhava.py)
  const dhana = a.dhana_bhava && !a.dhana_bhava.error ? a.dhana_bhava : null
  // BPHS chs 12, 14-18, 20-23 — the other house-effect verses this chart meets (api/bhava_effects.py)
  const bhe = a.bhava_effects && !a.bhava_effects.error ? a.bhava_effects : null
  const bheFor = (k) => (bhe ? (bhe.matches || []).filter((m) => m.clauses.some((c) => c.grahas.includes(k))) : [])
  /** the payload's "{g:jupiter}" placeholders → the reader's name for that graha */
  const fill = (l, s) => String(s || '').replace(/\{g:([a-z]+)\}/g, (_, key) => nm(l, key))
  const dhanaFor = (k) => (dhana ? (dhana.matches || []).filter((m) => m.clauses.some((c) => c.grahas.includes(k))) : [])
  const yks = ((a.lagna_profile && a.lagna_profile.yogakarakas) || []).map((y) => (typeof y === 'string' ? y : y && (y.graha || y.key))).filter(Boolean)
  const fold = (s) => String(s).normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
  const nm = (l, k) => N[l].grahaKey(k)
  const named = (l, k) => (l === 'en' && !plainEn && fold(namer.grahaKey(k)) !== fold(E.grahaKey(k)) ? `${namer.grahaKey(k)} (${E.grahaKey(k)})` : nm(l, k))
  const sign = (l, i) => (l === 'en' && !plainEn ? `${namer.rasi(i)} (${namer.rasiEnglish(i)})` : N[l].rasi(i))
  const ord = (l, h) => (l === 'hi' ? HI_ORD[h] : EN_ORD(h))
  const of = (l, h) => HOUSE[h].of[l]
  const ruled = (k) => Array.from({ length: 12 }, (_, i) => i + 1).filter((h) => SIGN_LORD[(lagna + h - 1) % 12] === k)
  const houseOfSign = (s) => ((s - lagna + 12) % 12) + 1
  const signal = (k, name) => (((a.grahas || {})[k]) || []).find((s) => s.name === name && s.available) || null
  const combust = (() => {
    const out = {}
    const m = chart.motion
    if (m && !m.error) for (const r of (m.grahas || [])) if (r.combustion && r.combustion.applies && r.combustion.combust) out[r.key] = true
    return out
  })()
  const tree = dashaTree(chart)
  const maha = tree && (tree.mahadashas || []).find((m) => m.is_current)
  const antar = maha && (maha.sub || []).find((x) => x.is_current)
  const running = { maha: maha ? maha.lord : null, antar: antar ? antar.lord : null }
  const period = (k) => (tree ? (tree.mahadashas || []).filter((m) => m.lord === k).map((m) => `${year(m.start)}–${year(m.end)}`) : [])

  const both = (f) => ({ en: f('en'), hi: f('hi') })
  const findings = []

  // ── one finding per graha: its most important role names it ────────────────
  const lagnaLord = B(1) ? B(1).lord : SIGN_LORD[lagna]
  for (const x of grahas) {
    const k = x.key, h = x.bhava, isNode = NODES.includes(k)
    const d = x.dignity && DIG[x.dignity.state] ? DIG[x.dignity.state] : null
    const r = ruled(k)
    const p = P(k)
    const here = B(h)
    const fullOn = here ? (here.aspects_in || []).filter((s) => s.strength >= 1 && s.graha !== k).map((s) => s.graha) : []
    const dispositor = SIGN_LORD[x.rasi], disp = g(dispositor)
    const vim = signal(k, 'vimsopaka')

    let role = 'plain', weight = 30
    if (k === lagnaLord) { role = 'lagnaLord'; weight = 100 }
    else if (d && d.w) { role = 'dignity'; weight = d.w }
    else if (yks.includes(k)) { role = 'yogakaraka'; weight = 77 }
    else if (isNode && KENDRA.includes(h)) { role = 'node'; weight = 60 }
    else if (k === 'moon') { role = 'moon'; weight = 45 }
    else if (HARD_HOUSES.includes(h) && r.length) { weight = 40 }

    const title = both((l) => {
      const n = nm(l, k)
      if (role === 'lagnaLord') return l === 'hi' ? `लग्नेश ${n} आपके ${HI_ORD[h]} भाव में` : `Ascendant lord ${n} in your ${EN_ORD(h)} house`
      if (role === 'dignity') return l === 'hi' ? `${n} ${d.hi}, आपके ${HI_ORD[h]} भाव में` : `${n} ${d.en} in your ${EN_ORD(h)} house`
      if (role === 'yogakaraka') return l === 'hi' ? `योगकारक ${n} आपके ${HI_ORD[h]} भाव में` : `Yogakāraka ${n} in your ${EN_ORD(h)} house`
      return l === 'hi' ? `${n} आपके ${HI_ORD[h]} भाव में` : `${n} in your ${EN_ORD(h)} house`
    })
    const sub = both((l) => of(l, h))

    const fact = both((l) => [
      isNode
        ? (l === 'hi'
          ? `${nm(l, k)} किसी राशि के स्वामी नहीं; वे ${sign(l, x.rasi)} राशि में, आपके ${HI_ORD[h]} भाव में हैं — ${of(l, h)} का भाव।`
          : `${named(l, k)} rules no sign. It sits in ${sign(l, x.rasi)}, your ${EN_ORD(h)} house — the house of ${of(l, h)}.`)
        : (l === 'hi'
          ? `${nm(l, k)} आपके ${list(r.map((n) => HI_ORD[n]), l)} भाव (${r.map((n) => of(l, n)).join('; ')}) के स्वामी हैं और ${sign(l, x.rasi)} राशि में, आपके ${HI_ORD[h]} भाव में बैठे हैं — ${of(l, h)} का भाव।`
          : `${named(l, k)} rules your ${list(r.map(EN_ORD), l)} ${r.length > 1 ? 'houses' : 'house'} (${r.map((n) => of(l, n)).join('; ')}) and sits in ${sign(l, x.rasi)}, your ${EN_ORD(h)} house — the house of ${of(l, h)}.`),
      d && (l === 'hi'
        ? `वहाँ ${nm(l, k)} ${d.hi} हैं${d.gloss ? ` (${d.gloss.hi})` : ''}${x.retrograde ? ', वक्री' : ''}।`
        : `${nm(l, k)} there is ${d.en}${d.gloss ? ` — ${d.gloss.en}` : ''}${x.retrograde ? ', and retrograde' : ''}.`),
    ].filter(Boolean))

    const why = both((l) => [
      role === 'lagnaLord' && (l === 'hi'
        ? `भाव को उसके स्वामी की स्थिति से पढ़ा जाता है। आपका पहला भाव — आप स्वयं — इसलिए ${HI_ORD[h]} भाव (${of(l, h)}) से पढ़ा जाता है। यह पूरी कुंडली की नींव है।`
        : `A house is read through where its lord sits. Your 1st house — you — is therefore read through your ${EN_ORD(h)} house: ${of(l, h)}. This is the foundation of the whole chart.`),
      !isNode && role !== 'lagnaLord' && r.length > 0 && (l === 'hi'
        ? `जिन भावों के ${nm(l, k)} स्वामी हैं (${r.map((n) => of(l, n)).join('; ')}), वे इसी स्थिति से पढ़े जाते हैं${r.includes(h) ? '' : ` — यानी ${of(l, h)} से जुड़कर`}।`
        : `The houses ${nm(l, k)} rules (${r.map((n) => of(l, n)).join('; ')}) are read through this placement${r.includes(h) ? '' : ` — that is, through ${of(l, h)}`}.`),
      isNode && disp && (l === 'hi'
        ? `राहु-केतु की अपनी कोई राशि नहीं; इन्हें उस राशि के स्वामी से पढ़ा जाता है जिसमें वे बैठे हैं — यहाँ ${nm(l, dispositor)}, जो आपके ${HI_ORD[disp.bhava]} भाव में हैं${disp.dignity && DIG[disp.dignity.state] ? ` (${DIG[disp.dignity.state].hi})` : ''}।`
        : `The nodes own no sign; a node is read through the lord of the sign it sits in — here ${nm(l, dispositor)}, in your ${EN_ORD(disp.bhava)} house${disp.dignity && DIG[disp.dignity.state] ? ` (${DIG[disp.dignity.state].en})` : ''}.`),
      role === 'yogakaraka' && (l === 'hi'
        ? `इस लग्न के लिए ${nm(l, k)} योगकारक हैं — एक केन्द्र और एक त्रिकोण, दोनों के स्वामी।`
        : `For this ascendant ${nm(l, k)} is the yogakāraka — it rules both an angle and a trine.`),
    ].filter(Boolean))

    const supports = both((l) => [
      d && d.good && (l === 'hi' ? `${d.hi} — ${d.gloss.hi}` : `${d.en[0].toUpperCase()}${d.en.slice(1)} — ${d.gloss.en}`),
      yks.includes(k) && (l === 'hi' ? 'इस लग्न के लिए योगकारक — एक केन्द्र और एक त्रिकोण के स्वामी' : 'The yogakāraka for this ascendant — lord of an angle and a trine'),
      p && p.nature === 'benefic' && (l === 'hi' ? 'इस लग्न के लिए शुभ ग्रह गिने जाते हैं (स्वामित्व से)' : 'Counted a benefic for this ascendant, by the houses it rules'),
      ...fullOn.filter((o) => P(o) && P(o).nature === 'benefic').map((o) => (l === 'hi' ? `${nm(l, o)} (इस लग्न के शुभ ग्रह) इस भाव को पूर्ण दृष्टि से देखते हैं` : `${nm(l, o)}, a benefic for this ascendant, looks at this house fully`)),
      !isNode && r.includes(h) && !(d && d.good) && (l === 'hi' ? 'अपने ही भाव में बैठे हैं' : 'Sits in a house it rules'),
    ].filter(Boolean))

    const cautions = both((l) => [
      d && d.bad && (l === 'hi' ? `${d.hi}${d.gloss ? ` — ${d.gloss.hi}` : ''}` : `${d.en[0].toUpperCase()}${d.en.slice(1)}${d.gloss ? ` — ${d.gloss.en}` : ''}`),
      HARD_HOUSES.includes(h) && (l === 'hi' ? `${HI_ORD[h]} भाव में — छठा, आठवाँ और बारहवाँ वे तीन भाव हैं जिन्हें परंपरा कठिन गिनती है` : `Sits in the ${EN_ORD(h)} house — one of the three houses (6th, 8th, 12th) the tradition counts as difficult`),
      p && p.nature === 'malefic' && (l === 'hi' ? 'इस लग्न के लिए पाप ग्रह गिने जाते हैं (स्वामित्व से)' : 'Counted a malefic for this ascendant, by the houses it rules'),
      combust[k] && (l === 'hi' ? 'सूर्य के बहुत निकट — अस्त' : 'Very close to the Sun — combust'),
      ...fullOn.filter((o) => P(o) && P(o).nature === 'malefic').map((o) => (l === 'hi' ? `${nm(l, o)} (इस लग्न के पाप ग्रह) इस भाव को पूर्ण दृष्टि से देखते हैं` : `${nm(l, o)}, a malefic for this ascendant, looks at this house fully`)),
    ].filter(Boolean))

    const measured = both((l) => [
      ...(dhana && k === dhana.lord2 ? (dhana.not_applied || []).filter((x) => x.reason !== 'combustion_has_no_orb_in_the_text' && DHANA_NOT[x.reason]).map((x) => DHANA_NOT[x.reason][l]) : []),
      vim && (l === 'hi'
        ? `सोलह वर्ग-कुंडलियों में बल (विंशोपक): 20 में से ${vim.value}`
        : `Strength across the sixteen divisional charts (Viṁśopaka): ${vim.value} of 20 — “${vim.label}”`),
      x.retrograde && !d && (l === 'hi' ? 'वक्री' : 'Retrograde'),
      fullOn.length > 0 && (l === 'hi' ? `इस भाव पर पूर्ण दृष्टि: ${list(fullOn.map((o) => nm(l, o)), l)}` : `Looking at this house fully: ${list(fullOn.map((o) => nm(l, o)), l)}`),
    ].filter(Boolean))

    const pr = period(k)
    const check = [
      { go: 'navamsa', label: both((l) => (l === 'hi' ? `नवांश (D9) में ${nm(l, k)} की राशि` : `${nm(l, k)}’s sign in the navāṁśa (D9)`)) },
      { go: 'strength', label: both((l) => (l === 'hi' ? `${nm(l, k)} का पूरा बल` : `${nm(l, k)}’s full strength`)) },
      ...(pr.length ? [{ go: 'dasha', label: both((l) => (l === 'hi' ? `${nm(l, k)} की महादशा: ${pr.join(', ')}` : `When ${nm(l, k)}’s main period runs: ${pr.join(', ')}`)) }] : []),
      { go: 'classical', label: both((l) => (l === 'hi' ? 'इस स्थिति के शास्त्रीय पाठ' : 'The classical readings for this placement')) },
    ]

    const texts = []
    // BPHS: the lord of each house this graha rules, in the house it sits in
    for (const rh of (isNode ? [] : r)) {
      const b = B(rh)
      if (!b || !b.lord_rule || !b.lord_rule.effect) continue
      texts.push(passage({
        says: b.lord_rule.effect, source: BPHS, cite: withBook(b.lord_rule.citation), kind: 'translation',
        applies: both((l) => (l === 'hi'
          ? `${nm(l, k)} आपके ${HI_ORD[rh]} भाव के स्वामी हैं और ${HI_ORD[h]} भाव में बैठे हैं — यह ${HI_ORD[rh]} भाव के स्वामी के ${HI_ORD[h]} भाव में होने का नियम है।`
          : `${nm(l, k)} rules your ${EN_ORD(rh)} house and sits in your ${EN_ORD(h)}: this is the text’s statement for the ${EN_ORD(rh)} lord in the ${EN_ORD(h)} house.`)),
      }))
      texts[texts.length - 1].house = rh
      if (b.lord_rule.lagna_exception) {
        // the text's own exception for this ascendant qualifies the rule
        texts[texts.length - 1].exception = b.lord_rule.lagna_exception
      }
    }
    // BPHS ch.13: the wealth verses this graha is part of — the WHOLE verse, with the clause that matched
    for (const m of dhanaFor(k)) {
      const mine = m.clauses.filter((c) => c.grahas.includes(k))
      const t = passage({
        says: m.text, source: BPHS, cite: m.citation, kind: 'translation',
        applies: both((l) => mine.map((c) => (DHANA_WHY[c.code] ? DHANA_WHY[c.code](l, (g) => nm(l, g), (hh) => ord(l, hh), c) : c.code)).join(' ')),
      })
      // vv.1-2 and vv.6-7 each state a favourable and an adverse outcome: say which this chart meets
      if (m.verse === '1-2') {
        const all = m.clauses
        const fav = all.some((c) => c.polarity === 'favourable'), adv = all.some((c) => c.polarity === 'adverse')
        t.qualifier = both((l) => (fav && adv
          ? (l === 'hi' ? 'यह कुंडली इस श्लोक की अनुकूल और प्रतिकूल, दोनों शर्तें पूरी करती है।' : 'This chart meets both a favourable and an adverse condition of this verse.')
          : fav ? (l === 'hi' ? 'यह कुंडली इस श्लोक की अनुकूल शर्तें पूरी करती है; प्रतिकूल शर्तें (स्वामी छठे/आठवें/बारहवें में, दूसरे भाव में पाप ग्रह) नहीं।' : 'This chart meets the verse’s favourable conditions. Its adverse ones (the lord in the 6th, 8th or 12th; a malefic in the 2nd) are not met.')
            : (l === 'hi' ? 'यह कुंडली इस श्लोक की प्रतिकूल शर्तें पूरी करती है; अनुकूल शर्तें नहीं।' : 'This chart meets the verse’s adverse conditions, not its favourable ones.')))
      } else if (m.verse === '6-7') {
        t.qualifier = both((l) => DHANA_NOT.combustion_has_no_orb_in_the_text[l])
      }
      t.house = 2
      texts.push(t)
    }
    // BPHS chs 12, 14-18, 20-23: the house-effect verses this graha is part of — whole, with the clause that fired
    for (const m of bheFor(k)) {
      const t = passage({
        says: m.text, source: BPHS, cite: m.citation, kind: 'translation',
        applies: both((l) => m.clauses.map((c) => fill(l, c.why[l] || c.why.en)).join(' ')),
      })
      const fav = m.clauses.some((c) => c.polarity === 'favourable'), adv = m.clauses.some((c) => c.polarity === 'adverse')
      t.qualifier = both((l) => [
        fav && adv ? (l === 'hi' ? 'यह कुंडली इस श्लोक की अनुकूल और प्रतिकूल, दोनों शर्तें पूरी करती है।' : 'This chart meets both a favourable and an adverse condition of this verse.')
          : fav ? (l === 'hi' ? 'यह कुंडली इस श्लोक की अनुकूल शर्त पूरी करती है।' : 'This chart meets a favourable condition of this verse.')
            : (l === 'hi' ? 'यह कुंडली इस श्लोक की प्रतिकूल शर्त पूरी करती है।' : 'This chart meets an adverse condition of this verse.'),
        ...((m.notes && (m.notes[l] || m.notes.en)) || []),
      ].join(' '))
      t.house = m.house
      texts.push(t)
    }
    // BPHS Vol II ch.47 vv.5-6: the text's verdict on a daśā, for the lords whose periods are running now
    const dv = chart.dasha && chart.dasha.verdicts ? chart.dasha.verdicts[k] : null
    if (dv && dv.verse && (k === running.maha || k === running.antar)) {
      const fav = (dv.favourable || []).map((c) => c.condition), adv = (dv.adverse || []).map((c) => c.condition)
      const t = passage({
        says: dv.verse, source: BPHS, cite: withBook(dv.citation), kind: 'translation',
        applies: both((l) => {
          const which = k === running.maha ? (l === 'hi' ? 'महादशा' : 'main period (mahādaśā)') : (l === 'hi' ? 'अन्तर्दशा' : 'sub-period (antardaśā)')
          return l === 'hi' ? `अभी ${nm(l, k)} की ${which} चल रही है; यह श्लोक दशा के स्वामी की स्थिति से दशा का फल बताता है।` : `${nm(l, k)}’s ${which} is running now; this verse judges a period by where its lord stands.`
        }),
      })
      t.qualifier = both((l) => {
        const head = fav.length && adv.length
          ? (l === 'hi' ? `श्लोक की दोनों ओर की शर्तें पूरी होती हैं — अनुकूल: ${fav.join('; ')}; प्रतिकूल: ${adv.join('; ')}। ग्रंथ यह नहीं बताता कि दोनों हों तो क्या माना जाए।` : `Conditions on both sides are met — favourable: ${fav.join('; ')}; unfavourable: ${adv.join('; ')}. The text does not say how to weigh the two.`)
          : fav.length ? (l === 'hi' ? `श्लोक की अनुकूल शर्त पूरी होती है: ${fav.join('; ')}।` : `The favourable condition is met: ${fav.join('; ')}.`)
            : adv.length ? (l === 'hi' ? `श्लोक की प्रतिकूल शर्त पूरी होती है: ${adv.join('; ')}।` : `The unfavourable condition is met: ${adv.join('; ')}.`)
              : (l === 'hi' ? 'श्लोक की कोई शर्त पूरी नहीं होती: इस दशा पर ग्रंथ कोई निर्णय नहीं देता।' : 'None of the verse’s conditions is met either way: the text states no verdict for this period.')
        return [head, ...((dv.caveats || []).slice(0, 2))].join(' ')
      })
      texts.push(t)
    }
    // BPHS: how the text classes this graha for this ascendant
    if (p && p.quote && !isNode && p.source === 'sloka') {
      texts.push(passage({
        says: p.quote, source: BPHS, cite: withBook(p.citation), kind: 'translation',
        applies: both((l) => (l === 'hi'
          ? `यह ${sign(l, lagna)} लग्न के लिए ग्रहों के शुभ-पाप होने का श्लोक है; आपका लग्न यही है।`
          : `This is the verse on which planets are favourable for a ${sign(l, lagna)} ascendant, which is yours.`)),
      }))
    }
    // the other classical texts: this graha in this house, and in this sign
    for (const { src, on } of concordance(k, h, x.rasi)) {
      if (!src || !src.gist) continue
      texts.push(passage({
        says: src.gist, source: src.source || null, cite: src.citation, kind: 'rendering',
        applies: both((l) => (on === 'house'
          ? (l === 'hi' ? `${nm(l, k)} आपके ${HI_ORD[h]} भाव में हैं।` : `${nm(l, k)} is in your ${EN_ORD(h)} house.`)
          : (l === 'hi' ? `${nm(l, k)} ${sign(l, x.rasi)} राशि में हैं।` : `${nm(l, k)} is in ${sign(l, x.rasi)}.`))),
      }))
    }

    const hasGood = supports.en.length > 0, hasBad = cautions.en.length > 0
    // DERIVED: how the passages above are to be weighed — every step cited, both sides disclosed
    const dig = signal(k, 'dignity')
    const shown = texts.filter((t) => t.says).length
    let inference = shown ? {
      chain: [
        { line: both((l) => (l === 'hi' ? `${shown} पंजीकृत पाठ इस स्थिति के बारे में कहते हैं (ऊपर)।` : `${shown} registered passage${shown > 1 ? 's speak' : ' speaks'} of this placement (above).`)), cite: null },
        d && { line: both((l) => (l === 'hi' ? `राशि-बल: ${nm(l, k)} ${d.hi} हैं।` : `Dignity by sign: ${nm(l, k)} is ${d.en}.`)), cite: dig ? withBook(dig.citation) : null },
        vim && { line: both((l) => (l === 'hi' ? `वर्ग-बल (विंशोपक): 20 में से ${vim.value}।` : `Strength across the divisional charts (Viṁśopaka): ${vim.value} of 20 — the text’s band for this is “${vim.label}”.`)), cite: withBook(vim.citation) },
        p && p.nature && { line: both((l) => (l === 'hi' ? `इस लग्न के लिए: ${p.nature === 'benefic' ? 'शुभ' : p.nature === 'malefic' ? 'पाप' : 'सम'} ग्रह।` : `For this ascendant it is counted ${p.nature === 'benefic' ? 'a benefic' : p.nature === 'malefic' ? 'a malefic' : 'neutral'}.`)), cite: withBook(p.citation) },
      ].filter(Boolean),
      conclusion: both((l) => {
        const s = supports[l].length, c = cautions[l].length
        if (l === 'hi') {
          return s && !c ? `इस ग्रह की अपनी स्थिति पाठों के कथन का समर्थन करती है (${s} समर्थक बात, विपरीत कोई नहीं)।`
            : !s && c ? `इस ग्रह की अपनी स्थिति पाठों के कथन को कमज़ोर करती है (${c} विपरीत बात, समर्थक कोई नहीं)।`
              : s && c ? `दोनों ओर की बातें हैं (${s} समर्थक, ${c} विपरीत): पाठों के कथन को इन्हीं शर्तों के साथ पढ़ें।`
                : 'न समर्थक, न विपरीत कोई विशेष बात मिली: पाठों का कथन जैसा है वैसा पढ़ें।'
        }
        return s && !c ? `The planet’s own condition supports what the passages say (${s} supporting factor${s > 1 ? 's' : ''}, none against).`
          : !s && c ? `The planet’s own condition weakens what the passages say (${c} factor${c > 1 ? 's' : ''} against, none supporting).`
            : s && c ? `There are factors on both sides (${s} supporting, ${c} against): read the passages as qualified by them.`
              : 'Nothing notable supports or counts against it: read the passages as they stand.'
      }),
    } : null
    // with nothing measured to weigh the passages by (the nodes), there is no chain, so no inference
    if (inference && inference.chain.length < 2) inference = null
    const tag = role === 'lagnaLord' ? 'key'
      : d && d.good && !hasBad ? 'strong'
        : d && d.bad && !hasGood ? 'weak'
          : hasGood && hasBad ? 'mixed'
            : role === 'node' ? 'context'
              : d && d.good ? 'strong' : d && d.bad ? 'weak' : 'plain'

    findings.push({
      key: `graha-${k}`, kind: 'graha', graha: k, house: h, weight, role, tag,
      title, sub, fact, why, supports, cautions, measured, check, texts, inference,
      cite: [p && p.citation, signal(k, 'dignity') && signal(k, 'dignity').citation].filter(Boolean).join(' · ') || null,
      // how directly this graha touches a house: lord 4 · occupant 3 · kāraka 2 · full aspect 1
      touch: (th) => Math.max(
        r.includes(th) ? 4 : 0, h === th ? 3 : 0,
        B(th) && B(th).karaka === k ? 2 : 0,
        B(th) && (B(th).aspects_in || []).some((s) => s.graha === k && s.strength >= 1) ? 1 : 0),
      touchWord: (th, l) => (r.includes(th) ? (l === 'hi' ? `${HI_ORD[th]} भाव के स्वामी` : `rules your ${EN_ORD(th)} house`)
        : h === th ? (l === 'hi' ? `${HI_ORD[th]} भाव में बैठे हैं` : `sits in your ${EN_ORD(th)} house`)
          : B(th) && B(th).karaka === k ? (l === 'hi' ? `${HI_ORD[th]} भाव के नैसर्गिक कारक` : `natural significator of your ${EN_ORD(th)} house`)
            : (l === 'hi' ? `${HI_ORD[th]} भाव को पूर्ण दृष्टि से देखते हैं` : `looks at your ${EN_ORD(th)} house fully`)),
    })
  }

  // ── two or more house-lords together ────────────────────────────────────────
  for (let h = 1; h <= 12; h++) {
    const occ = grahas.filter((x) => x.bhava === h && !NODES.includes(x.key))
    if (occ.length < 2) continue
    const keys = occ.map((x) => x.key)
    const withLagnaLord = keys.includes(lagnaLord)
    findings.push({
      key: `together-${h}`, kind: 'together', house: h, grahas: keys, weight: withLagnaLord ? 55 : 42, tag: 'context',
      title: both((l) => (l === 'hi' ? `${list(keys.map((k) => nm(l, k)), l)} साथ-साथ, आपके ${HI_ORD[h]} भाव में` : `${list(keys.map((k) => nm(l, k)), l)} together in your ${EN_ORD(h)} house`)),
      sub: both((l) => of(l, h)),
      fact: both((l) => [l === 'hi'
        ? `${keys.map((k) => `${nm(l, k)} (${list(ruled(k).map((n) => HI_ORD[n]), l)} भाव के स्वामी)`).join(', ')} — सब ${sign(l, occ[0].rasi)} राशि में, आपके ${HI_ORD[h]} भाव में हैं।`
        : `${keys.map((k) => `${nm(l, k)} (lord of your ${list(ruled(k).map(EN_ORD), l)})`).join(', ')} all sit in ${sign(l, occ[0].rasi)}, your ${EN_ORD(h)} house.`]),
      why: both((l) => [l === 'hi'
        ? `जब दो भावों के स्वामी एक ही भाव में बैठते हैं, तो उन भावों की बातें (${[...new Set(keys.flatMap(ruled))].map((n) => of(l, n)).join('; ')}) ${of(l, h)} के भाव में मिलती हैं। यह अच्छा है या कठिन, यह हर ग्रह के बल और अंश-दूरी से तय होता है।`
        : `When the lords of different houses share one house, the matters of those houses (${[...new Set(keys.flatMap(ruled))].map((n) => of(l, n)).join('; ')}) meet in the house of ${of(l, h)}. Whether that helps or strains depends on each planet’s strength and how close they stand.`]),
      supports: both(() => []), cautions: both(() => []),
      measured: both((l) => occ.map((x) => `${nm(l, x.key)} ${x.degree}°${x.dignity && DIG[x.dignity.state] ? ` · ${DIG[x.dignity.state][l]}` : ''}`)),
      check: [
        { go: 'strength', label: both((l) => (l === 'hi' ? 'हर ग्रह का बल' : 'Each planet’s strength')) },
        { go: 'bhava', label: both((l) => (l === 'hi' ? 'इस भाव के योग और शास्त्रीय पाठ' : 'The yogas and classical readings for this house')) },
      ],
      texts: [], inference: null, cite: null,
      touch: (th) => Math.max(h === th ? 3 : 0, keys.some((k) => ruled(k).includes(th)) ? 2 : 0),
      touchWord: (th, l) => (h === th ? (l === 'hi' ? `${HI_ORD[th]} भाव में` : `in your ${EN_ORD(th)} house`) : (l === 'hi' ? `${HI_ORD[th]} भाव के स्वामी शामिल` : `includes the lord of your ${EN_ORD(th)} house`)),
    })
  }

  // ── the named combinations the engine detected ──────────────────────────────
  const yogas = (a.yogas && !a.yogas.error && a.yogas.detected) || []
  yogas.forEach((y, i) => {
    findings.push({
      key: `yoga-${i}`, kind: 'yoga', house: null, weight: 44 - i, tag: 'named',
      title: both(() => y.name),
      sub: both((l) => (l === 'hi' ? 'योग' : 'yoga')),
      fact: both((l) => [l === 'hi' ? `इस कुंडली में ${y.name} की शर्तें पूरी होती हैं।` : `This chart meets the conditions of ${y.name}.`]),
      why: both((l) => [l === 'hi'
        ? 'योग ग्रहों की एक नामित स्थिति है। शर्तें पूरी होना एक बात है; वह कितना फल देगा, यह उसे बनाने वाले ग्रहों के बल और उनकी दशा पर निर्भर है।'
        : 'A yoga is a named arrangement of planets. Meeting its conditions is one thing; how much it gives depends on the strength of the planets that form it and on their periods.']),
      supports: both(() => []), cautions: both(() => []),
      measured: both(() => (y.strength_note ? [y.strength_note] : [])),
      check: [{ go: 'bhava', label: both((l) => (l === 'hi' ? 'इसे बनाने वाले ग्रह और पूरा योग-पाठ' : 'The planets that form it, and the full yoga reading')) }],
      texts: y.effect ? [passage({
        says: y.effect, source: { ...BPHS, tier: y.tier || 'sloka' }, cite: y.citation, kind: 'translation',
        applies: both((l) => (l === 'hi' ? `इस कुंडली में ${y.name} की शर्तें पूरी होती हैं।` : `This chart meets the conditions the text gives for ${y.name}.`)),
      })] : [],
      inference: null, cite: y.citation || null,
      touch: () => 0, touchWord: () => '',
    })
  })

  return { findings, running }
}

/** The findings in reading order for a topic. Overall: by weight. A house topic: by how directly each finding touches
 *  the topic's houses, then weight (findings that do not touch it are left out). Timing: the running lords first. */
export function rankFindings({ findings, running }, topicKey = 'overall') {
  const topic = TOPICS.find((t) => t.key === topicKey) || TOPICS[0]
  const byWeight = (x, y) => y.weight - x.weight
  if (topic.key === 'overall') return [...findings].sort(byWeight).map((f) => ({ f, because: null }))
  if (topic.key === 'timing') {
    const order = [running.maha, running.antar].filter(Boolean)
    return findings.filter((f) => f.kind === 'graha' && order.includes(f.graha))
      .sort((x, y) => order.indexOf(x.graha) - order.indexOf(y.graha))
      .map((f) => ({ f, because: { en: f.graha === running.maha ? 'lord of the main period running now' : 'lord of the sub-period running now', hi: f.graha === running.maha ? 'अभी चल रही महादशा के स्वामी' : 'अभी चल रही अन्तर्दशा के स्वामी' } }))
  }
  return findings
    .map((f) => {
      const scored = topic.houses.map((h) => [f.touch(h), h]).sort((x, y) => y[0] - x[0])[0]
      return { f, score: scored[0], h: scored[1] }
    })
    .filter((x) => x.score > 0)
    .sort((x, y) => y.score - x.score || byWeight(x.f, y.f))
    .map(({ f, h }) => ({ f, because: { en: f.touchWord(h, 'en'), hi: f.touchWord(h, 'hi') } }))
}
