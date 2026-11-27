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
 *   rendered  the other classical texts (Sārāvalī 30, Phaladīpikā 8, Bṛhat Jātaka 20, Chamatkāra) on each planet
 *           sitting in the area's houses, as the site renders them (classical tier; not quoted, the words are ours);
 *   dated   a BPHS verse naming an age for a good event (chs 15, 16, 20, 22; api/bhava_effects.py) whose condition
 *           this chart meets: quoted whole, the clause met, and the age as this native's calendar months (agewindow.js);
 *   note    a source note: the modern 5th–7th "love marriage" rule, which other readings attribute to BPHS. BPHS
 *           (24.77) does not say it and no classical text we hold does, so it is named as modern and not stated;
 *   timing  when the area's planets run their periods, with dates (the same dates as "Your life, area by area");
 *   ours    how the factors lean, in our words and labelled ours, ALWAYS with its basis in the chart. Owner's rule
 *           2026-11-26: guidance from the chart is welcome ("avoid speculation" when Rahu is weak in a house of
 *           money), dated periods are fine; only selling a remedy and fear are out. No gem, ritual or charity.
 * Nothing here is new doctrine. It is built from buildLifeAreas and buildFindings, which carry the rules.
 */
import { makeNamer } from './naming.js'
import { HOUSE } from './walkthrough.js'
import { buildLifeAreas } from './lifeareas.js'
import { ageSentence } from './agewindow.js'

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

/** Where a dated verse is told: by the house its chapter is about (the 9th, fortunes, goes with wealth). */
const DATED_AREA = { 4: 'home', 5: 'children', 9: 'wealth', 11: 'wealth' }

/** The order of the summary: the areas a reader asks about first. */
export const ORDER = ['career', 'marriage', 'children', 'wealth', 'home', 'self']
export const KIND = {
  chart: { en: 'From your chart', hi: 'आपकी कुंडली से' },
  text: { en: 'What the classical text says', hi: 'शास्त्र क्या कहता है' },
  timing: { en: 'When', hi: 'कब' },
  dated: { en: 'An age in the text', hi: 'ग्रंथ में दी गई आयु' },
  rendered: { en: 'A classical text, in our words', hi: 'शास्त्र, हमारे शब्दों में' },
  note: { en: 'A note on sources', hi: 'स्रोतों पर एक बात' },
  ours: { en: 'Our reading, not a text’s', hi: 'हमारी व्याख्या, किसी ग्रंथ की नहीं' },
}
/** Ours: what to do with an area whose lord leans against or is mixed. Plain steps, no remedy, nothing sold. */
const GUIDE = {
  career: { en: 'Expect progress through steady work more than sudden leaps.', hi: 'तरक्की अचानक छलाँग से कम, लगातार काम से अधिक आने की उम्मीद रखें।' },
  marriage: { en: 'Give the partnership time and plain talk, and do not leave friction unspoken.', hi: 'साझेदारी को समय और खुली बातचीत दें, और खटपट को अनकहा न छोड़ें।' },
  children: { en: 'If children come later than hoped, the chart leans that way; it is a reason for patience and planning, not worry.', hi: 'अगर संतान उम्मीद से देर से हो, तो कुंडली उसी ओर झुकती है; यह धैर्य और योजना का कारण है, चिंता का नहीं।' },
  wealth: { en: 'Prefer steady earnings and savings over money that depends on luck.', hi: 'भाग्य पर टिके पैसे से अधिक, नियमित कमाई और बचत को चुनें।' },
  home: { en: 'Look twice at property and vehicle decisions.', hi: 'घर, ज़मीन और वाहन के फ़ैसलों को दो बार परखें।' },
  self: { en: 'A steady routine serves you better than bursts of effort.', hi: 'थोड़े-थोड़े ज़ोर से अधिक, नियमित दिनचर्या आपके काम आती है।' },
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
  // the renderings name the planet in English, sometimes lower-case ("with jupiter in the 2nd"): the reader's name instead
  const named = (s) => String(s).replace(/\bwith (the )?(sun|moon|mars|mercury|jupiter|venus|saturn|rahu|ketu)\b/gi, (_, _t, k) => `with ${nm('en', k.toLowerCase())}`)

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
      if (t.says) paras.push({ kind: 'text', en: `“${t.says}”`, hi: `“${t.says}”`, cite: t.cite, source: t.source, note: t.applies })
    }
    // ── rendered: the other classical texts on each planet sitting in the area's houses (Sārāvalī, Phaladīpikā,
    //    Bṛhat Jātaka, Chamatkāra), shown as the site renders them — not quoted, since the words are ours ──
    const rendered = A.passages.filter((t) => t.kind === 'rendering' && t.says)
    for (const t of rendered) paras.push({ kind: 'rendered', en: named(t.says), hi: named(t.says), cite: t.cite, source: t.source })

    // ── dated: a BPHS verse that names an age for a good event, and this chart meets its condition (owner,
    //    2026-11-26: "dated event is fine"). Quoted whole, with the clause met and the age in this native's dates.
    //    The 9th house (fortunes) is read with wealth here. A verse dating a death or a disease is not registered.
    const bhe = chart.analysis && chart.analysis.bhava_effects
    const datedHere = ((bhe && !bhe.error && bhe.matches) || []).filter((m) => m.dated && DATED_AREA[m.house] === A.key)
    const fillG = (l, s) => String(s || '').replace(/\{g:([a-z]+)\}/g, (_, k) => nm(l, k))
    for (const m of datedHere) {
      paras.push({ kind: 'dated', cite: m.citation, source: { translator: 'R. Santhanam' }, ...both((l) => [
        `“${m.text}”`,
        ...m.clauses.filter((c) => c.age).map((c) => `${l === 'hi' ? 'आपकी कुंडली यह शर्त पूरी करती है।' : 'Your chart meets this.'} ${fillG(l, c.why[l] || c.why.en)} ${ageSentence(c.age, chart, l, now)}`),
      ].join(' ')) })
    }

    // ── note: the modern 5th–7th "love marriage" rule, which readers meet everywhere attributed to BPHS ──
    if (A.key === 'marriage') {
      const l5 = lordOf(5), l7 = lordOf(7), g5 = g(l5), g7 = g(l7)
      const link = g5 && g7 && l5 !== l7 && (g7.bhava === 5 || g5.bhava === 7 || g5.bhava === g7.bhava)
      if (link) {
        paras.push({ kind: 'note', ...both((l) => (l === 'hi'
          ? `आपके पाँचवें और सातवें भाव के स्वामी (${nm(l, l5)}, ${nm(l, l7)}) आपस में जुड़े हैं। बहुत-सी आधुनिक व्याख्याएँ इसे प्रेम-विवाह का संकेत मानती हैं और अक्सर इसे BPHS का नियम बताती हैं। हमें यह नियम BPHS में नहीं मिला, न सारावली, फलदीपिका, जातक पारिजात या होरा सार में। यह आधुनिक परंपरा की बात है, इसलिए हम इसे यहाँ फल के रूप में नहीं लिखते।`
          : `The lords of your 5th and 7th houses (${nm(l, l5)} and ${nm(l, l7)}) are linked. Many modern readings take this as a sign of a love marriage, and often say BPHS teaches it. We did not find that rule in BPHS, nor in Sārāvalī, Phaladīpikā, Jātaka Pārijāta or Horā Sāra. It is modern teaching, so we do not state it here as a result.`)) })
      }
    }

    const rest = A.passages.filter((t) => !(lordVerses.includes(t) && t.says) && !(rendered.includes(t)) && !datedHere.some((m) => m.citation === t.cite))
    const held = rest.filter((t) => t.held).length
    if (rest.length) {
      paras.push({ kind: 'text', ...both((l) => (l === 'hi'
        ? `इस क्षेत्र पर ${rest.length === 1 ? 'एक और पाठ लागू होता है' : `${rest.length} और पाठ लागू होते हैं`}।${held ? ` ${held === 1 ? (rest.length === 1 ? 'वह किसी हानि या वियोग की बात करता है, इसलिए यहाँ नहीं दिखाया गया।' : 'उनमें से एक किसी हानि या वियोग की बात करता है, इसलिए यहाँ नहीं दिखाया गया।') : `उनमें से ${held} किसी हानि या वियोग की बात करते हैं, इसलिए यहाँ नहीं दिखाए गए।`}` : ''} ${rest.length === 1 ? 'वह नीचे “आपका जीवन, क्षेत्र-दर-क्षेत्र” में पूरा दिया है।' : 'सब नीचे “आपका जीवन, क्षेत्र-दर-क्षेत्र” में पूरे दिए हैं।'}`
        : `${rest.length === 1 ? 'One more passage applies' : `${rest.length} more passages apply`} to this area.${held ? ` ${held === 1 ? (rest.length === 1 ? 'It speaks' : 'One of them speaks') : `${held} of them speak`} of a loss or a separation, so it is not shown here.` : ''} ${rest.length === 1 ? 'It is' : 'All of them are'} given whole below, under “Your life, area by area”.`)) })
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
      // the basis first (owner, 2026-11-26: guidance from the chart is welcome when it says what it rests on)
      const basis = (l) => (l === 'hi'
        ? `आधार: स्वामी ${list(lords.map((k) => nm(l, k)), l)} के पक्ष में ${S}, विपक्ष में ${C} बातें (ऊपर)।`
        : `Basis: ${S} factor${S === 1 ? '' : 's'} for and ${C} against the lord${lords.length > 1 ? 's' : ''}, ${list(lords.map((k) => nm(l, k)), l)} (above).`)
      const lead = (l) => (l === 'hi'
        ? { up: 'स्वामी की स्थिति समर्थन की ओर झुकती है। यह आगे बढ़ाने का क्षेत्र है।',
          down: 'स्वामी की स्थिति विपरीत ओर झुकती है। इस क्षेत्र को मानकर न चलें। धीरे और तैयारी के साथ चलें।',
          mixed: 'स्वामी की स्थिति में दोनों ओर की बातें हैं। रास्ता मिला-जुला मानें: समर्थन वाली बातों पर टिकें, विपरीत बातों के लिए पहले से तैयार रहें।' }[lean]
        : { up: 'The lord’s condition leans to the supporting side. This is an area to build on.',
          down: 'The lord’s condition leans against. Do not take this area for granted. Move steadily and prepare.',
          mixed: 'The lord’s condition has factors on both sides. Expect a mixed road: lean on what supports it, and prepare for what counts against it.' }[lean])
      const guide = lean === 'up' ? null : GUIDE[A.key]
      paras.push({ kind: 'ours', ...both((l) => `${lead(l)}${guide ? ' ' + guide[l] : ''} ${basis(l)}`) })
    }

    // ── ours: Rahu in a house of money with more against it than for it → careful with speculation ──
    const ra = g('rahu'), rf = built.findings.find((x) => x.graha === 'rahu')
    if (A.key === 'wealth' && ra && rf && [2, 5, 11].includes(ra.bhava) && rf.cautions.en.length > rf.supports.en.length) {
      const c = rf.cautions.en.length, s = rf.supports.en.length
      paras.push({ kind: 'ours', ...both((l) => (l === 'hi'
        ? `${nm(l, 'rahu')} आपके ${HI_ORD[ra.bhava]} भाव में हैं, और उनके विपक्ष में ${c}, पक्ष में ${s} बातें हैं। हम इसे सट्टे और जल्दी मुनाफ़े वाले सौदों, जैसे उधार लेकर शेयर का व्यापार, से सावधान रहने का कारण मानते हैं।`
        : `${nm(l, 'rahu')} sits in your ${EN_ORD(ra.bhava)} house with ${c} factor${c === 1 ? '' : 's'} against it and ${s} for it. We read that as a reason to be careful with speculation and quick-profit deals, such as trading shares on borrowed money.`)) })
    }

    return { key: A.key, label: A.label, houses: A.houses, now: !!A.timing.now, paras }
  })
}
