/**
 * "Summary, area by area": the life areas told as a few plain paragraphs, the way a reader expects a reading to
 * sound (owner, 2026-11-26, after comparing another site's summary of their own chart: "Yes, build it").
 *
 * The other summary read well because it said more than its texts do: it named BPHS for things BPHS does not say,
 * gave ages, gave money advice and softened hard verses into "delay". This one keeps the plain voice and none of
 * that. Every paragraph is one of four kinds, and the page labels which:
 *   chart   what is calculated: the area's house, its sign, who sits in it, where its lord sits;
 *   text    the classical text's own words: the BPHS ch.24 verse for this house's lord in the house it occupies,
 *           quoted whole (a SENSITIVE verse is never quoted here; the summary says it is held and where it is);
 *   timing  when the area's planets run their periods (the same dates as "Your life, area by area");
 *   ours    how the factors lean, in our words and labelled ours. It never predicts an event, never gives an age,
 *           never gives medical, legal or financial instructions.
 * Nothing here is new doctrine. It is built from buildLifeAreas and buildFindings, which carry the rules.
 */
import { makeNamer } from './naming.js'
import { HOUSE } from './walkthrough.js'
import { buildLifeAreas } from './lifeareas.js'

const SIGN_LORD = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'saturn', 'jupiter']
const EN_ORD = (n) => `${n}${n % 10 === 1 && n !== 11 ? 'st' : n % 10 === 2 && n !== 12 ? 'nd' : n % 10 === 3 && n !== 13 ? 'rd' : 'th'}`
const HI_ORD = ['', 'पहले', 'दूसरे', 'तीसरे', 'चौथे', 'पाँचवें', 'छठे', 'सातवें', 'आठवें', 'नौवें', 'दसवें', 'ग्यारहवें', 'बारहवें']
const list = (xs, l) => (xs.length < 2 ? xs.join('') : `${xs.slice(0, -1).join(', ')} ${l === 'hi' ? 'और' : 'and'} ${xs[xs.length - 1]}`)
// A finding's factor ("Counted a benefic …", "In an enemy's sign …", "Mangal, a benefic …, looks at this house
// fully") made into a clause about the lord. "This house" in a finding is the house the planet sits in.
const plain = (s, l) => {
  if (l === 'hi') return String(s).replace('इस भाव को पूर्ण दृष्टि से देखते हैं', 'उसके भाव को पूर्ण दृष्टि से देखते हैं')
  const x = String(s).replace('looks at this house fully', 'fully aspects the house it sits in')
  if (/^(Counted|In |Combust|Exalted|Debilitated|Retrograde|Strong|Weak)/.test(x)) return 'it is ' + x[0].toLowerCase() + x.slice(1)
  if (/^Sits /.test(x)) return 'it s' + x.slice(1)
  return x
}

/** The order of the summary: the areas a reader asks about first. */
export const ORDER = ['career', 'marriage', 'children', 'wealth', 'home', 'self']
export const KIND = {
  chart: { en: 'From your chart', hi: 'आपकी कुंडली से' },
  text: { en: 'What the classical text says', hi: 'शास्त्र क्या कहता है' },
  timing: { en: 'When', hi: 'कब' },
  ours: { en: 'Our reading, not a text’s', hi: 'हमारी व्याख्या, किसी ग्रंथ की नहीं' },
}

/**
 * @returns [{ key, label, paras: [{ kind, en, hi, cite? }] }] in ORDER
 */
export function buildAreaSummary(chart, built, namer = makeNamer('common'), now = Date.now()) {
  const areas = buildLifeAreas(chart, built, namer, now)
  const N = { en: namer, hi: makeNamer('devanagari') }
  const nm = (l, k) => N[l].grahaKey(k)
  const lagna = chart.lagna_rasi
  const grahas = chart.grahas || []
  const g = (k) => grahas.find((x) => x.key === k)
  const lordOf = (h) => SIGN_LORD[(lagna + h - 1) % 12]
  const occ = (h) => grahas.filter((x) => x.bhava === h).map((x) => x.key)
  const both = (f) => ({ en: f('en'), hi: f('hi') })

  return ORDER.map((key) => areas.find((a) => a.key === key)).filter(Boolean).map((A) => {
    const paras = []

    // ── chart: the house, who sits in it, where its lord sits ──
    paras.push({ kind: 'chart', ...both((l) => A.houses.map((h) => {
      const s = (lagna + h - 1) % 12, lo = lordOf(h), lg = g(lo), o = occ(h)
      const hn = HOUSE[h].of[l]
      if (l === 'hi') {
        return `${hn} आपके ${HI_ORD[h]} भाव से देखे जाते हैं, जो ${N.hi.rasi(s)} राशि है।`
          + (o.length ? ` इसमें ${list(o.map((k) => nm(l, k)), l)} बैठे हैं।` : ' इसमें कोई ग्रह नहीं बैठा।')
          + (lg ? (lg.bhava === h ? ` इसके स्वामी ${nm(l, lo)} इसी भाव में हैं।` : ` इसके स्वामी ${nm(l, lo)} आपके ${HI_ORD[lg.bhava]} भाव (${HOUSE[lg.bhava].of.hi}) में बैठे हैं।`) : '')
      }
      return `${hn[0].toUpperCase() + hn.slice(1)} ${hn.includes(' and ') ? 'are' : 'is'} read from your ${EN_ORD(h)} house, ${N.en.rasi(s)}.`
        + (o.length ? ` ${list(o.map((k) => nm(l, k)), l)} ${o.length > 1 ? 'sit' : 'sits'} in it.` : ' No planet sits in it.')
        + (lg ? (lg.bhava === h ? ` Its lord, ${nm(l, lo)}, sits in the same house.` : ` Its lord, ${nm(l, lo)}, sits in your ${EN_ORD(lg.bhava)} house, the house of ${HOUSE[lg.bhava].of.en}.`) : '')
    }).join(' ')) })

    // ── text: the lord-in-house verse(s) of BPHS ch.24, whole ──
    const lordVerses = A.passages.filter((t) => t.cite && /ch\.24\b/.test(t.cite))
    for (const t of lordVerses) {
      if (t.says) paras.push({ kind: 'text', en: `“${t.says}”`, hi: `“${t.says}”`, cite: t.cite, note: t.applies })
    }
    const rest = A.passages.filter((t) => !lordVerses.includes(t) || !t.says)
    const held = rest.filter((t) => t.held).length
    if (rest.length) {
      paras.push({ kind: 'text', ...both((l) => (l === 'hi'
        ? `इस क्षेत्र पर ${rest.length === 1 ? 'एक और पाठ लागू होता है' : `${rest.length} और पाठ लागू होते हैं`}।${held ? ` ${held === 1 ? 'उनमें से एक' : `उनमें से ${held}`} किसी हानि या वियोग की बात करता है, इसलिए यहाँ नहीं दिखाया गया।` : ''} ${rest.length === 1 ? 'वह' : 'सब'} नीचे “आपका जीवन, क्षेत्र-दर-क्षेत्र” में पूरे दिए हैं।`
        : `${rest.length === 1 ? 'One more passage applies' : `${rest.length} more passages apply`} to this area.${held ? ` ${held === 1 ? 'One of them speaks' : `${held} of them speak`} of a loss or a separation, so it is not shown here.` : ''} ${rest.length === 1 ? 'It is' : 'All of them are'} given whole below, under “Your life, area by area”.`)) })
    }

    // ── chart: the lords' condition, both sides ──
    const lords = [...new Set(A.houses.map(lordOf))]
    for (const k of lords) {
      const f = built.findings.find((x) => x.graha === k)
      if (!f) continue
      const s = f.supports, c = f.cautions
      if (!s.en.length && !c.en.length) continue
      paras.push({ kind: 'chart', ...both((l) => {
        const pro = s[l].map((x) => plain(x, l)), con = c[l].map((x) => plain(x, l))
        if (l === 'hi') {
          return (pro.length ? `स्वामी ${nm(l, k)} के पक्ष में: ${pro.join('; ')}।` : `स्वामी ${nm(l, k)} के पक्ष में कोई विशेष बात नहीं।`)
            + (con.length ? ` विपक्ष में: ${con.join('; ')}।` : ' विपक्ष में कोई विशेष बात नहीं।')
        }
        return (pro.length ? `What helps the lord, ${nm(l, k)}: ${pro.join('; ')}.` : `Nothing notable helps the lord, ${nm(l, k)}.`)
          + (con.length ? ` What weighs on it: ${con.join('; ')}.` : ' Nothing notable weighs on it.')
      }) })
    }

    // ── timing ──
    if (A.timing.now) paras.push({ kind: 'timing', ...A.timing.now })
    else if (A.timing.next) paras.push({ kind: 'timing', ...A.timing.next })

    // ── ours: how it leans, in a sentence ──
    const S = lords.reduce((n, k) => n + ((built.findings.find((x) => x.graha === k) || { supports: { en: [] } }).supports.en.length), 0)
    const C = lords.reduce((n, k) => n + ((built.findings.find((x) => x.graha === k) || { cautions: { en: [] } }).cautions.en.length), 0)
    const lean = S && !C ? 'up' : C && !S ? 'down' : S && C ? 'mixed' : null
    if (lean) {
      paras.push({ kind: 'ours', ...both((l) => (l === 'hi'
        ? { up: 'स्वामी की स्थिति समर्थन की ओर झुकती है। यह आगे बढ़ाने का क्षेत्र है।',
          down: 'स्वामी की स्थिति विपरीत ओर झुकती है। इस क्षेत्र को मानकर न चलें। धीरे और तैयारी के साथ चलें।',
          mixed: 'स्वामी की स्थिति में दोनों ओर की बातें हैं। रास्ता मिला-जुला मानें: समर्थन वाली बातों पर टिकें, विपरीत बातों के लिए पहले से तैयार रहें।' }[lean]
        : { up: 'The lord’s condition leans to the supporting side. This is an area to build on.',
          down: 'The lord’s condition leans against. Do not take this area for granted. Move steadily and prepare.',
          mixed: 'The lord’s condition has factors on both sides. Expect a mixed road: lean on what supports it, and prepare for what counts against it.' }[lean])) })
    }

    return { key: A.key, label: A.label, houses: A.houses, now: !!A.timing.now, paras }
  })
}
