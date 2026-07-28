/**
 * "How to read this chart" — an interactive, chart-AWARE walkthrough.
 *
 * The doctrine of this site is cite-or-refuse: show the signals, never a
 * fabricated verdict. So this guide teaches the METHOD, step by step, on the
 * reader's OWN cast chart — each step names what BPHS actually does, points at
 * the live panel that shows it, and highlights the relevant piece. It never says
 * "your Sun in Leo means…"; it says "here is how strength / function / aspect /
 * timing are read, and here is where the app shows yours."
 *
 * The last step is the point: a reading is you weighing the cited signals, and
 * "the text is silent" is a real answer — that is the difference between reading
 * a chart and being told a story.
 */

import { useState, useEffect, useRef, useMemo } from 'react'

const DIGNITY_WORD = {
  exalted: 'exalted — its strongest', debilitated: 'debilitated — its weakest',
  moolatrikona: 'in its mūlatrikoṇa (very strong)', own: 'in its own sign (strong)',
  friend: "in a friend's sign", neutral: "in a neutral's sign",
  enemy: "in an enemy's sign (strained)",
}

function buildCtx(chart, namer) {
  const g = (k) => chart.grahas.find((x) => x.key === k)
  const lagna = chart.lagna_rasi
  const seventh = (lagna + 6) % 12
  // A graha with a striking dignity makes the strength step concrete.
  let dign = null
  for (const st of ['exalted', 'debilitated', 'moolatrikona', 'own']) {
    dign = chart.grahas.find((x) => x.dignity?.state === st)
    if (dign) break
  }
  dign = dign || g('sun')
  const dv = chart.dasha && chart.dasha.variants
  const tree = dv ? (dv['360'] || Object.values(dv)[0]) : null
  const curMaha = tree && tree.mahadashas && tree.mahadashas.find((m) => m.is_current)
  const curAntar = curMaha && curMaha.sub && curMaha.sub.find((a) => a.is_current)
  const navamsa = chart.navamsa && !chart.navamsa.error ? chart.navamsa : null
  return { chart, namer, g, lagna, moon: g('moon'), sun: g('sun'), seventh, dign, curMaha, curAntar, navamsa }
}

const STEPS = [
  {
    title: 'Start with three points',
    cite: 'BPHS Vol I, ch.34',
    enter: (a, c) => { a.scrollTo('#rg-positions'); a.highlightSign(c.lagna) },
    body: (c) => (
      <>A reading hangs on the <strong>lagna</strong> — the sign rising in the
        east at the moment of birth. Yours is <strong>{c.namer.rasi(c.lagna)}</strong>.
        Your Moon sits in <strong>{c.namer.rasi(c.moon.rasi)}</strong> (the janma
        rāśi) and your Sun in <strong>{c.namer.rasi(c.sun.rasi)}</strong>. BPHS
        keys its rules to the <em>lagna</em> — that is the anchor, not a "sun sign".</>
    ),
  },
  {
    title: 'Every sign is a house',
    cite: 'whole-sign bhāvas',
    enter: (a, c) => { a.setStyle('south'); a.scrollTo('.chart-panel'); a.highlightSign(c.seventh) },
    body: (c) => (
      <>Because <strong>{c.namer.rasi(c.lagna)}</strong> rises, it is your{' '}
        <strong>1st bhāva</strong>, and each following sign is the next house. So
        your 7th house — partnership — is <strong>{c.namer.rasi(c.seventh)}</strong>{' '}
        (highlighted). Every sign in the chart carries its bhāva number.</>
    ),
  },
  {
    title: 'How strong is each graha',
    cite: 'BPHS Vol I, ch.3',
    enter: (a, c) => { a.selectGraha(c.dign.key); a.scrollTo('#rg-signals') },
    body: (c) => (
      <>A graha's power turns on the sign it occupies — its own, exalted, a
        friend's, an enemy's, or fallen. Take <strong>{c.namer.graha(c.dign)}</strong>:
        it is in <strong>{c.namer.rasi(c.dign.rasi)}</strong>,{' '}
        <strong>{DIGNITY_WORD[c.dign.dignity?.state] ?? c.dign.dignity?.state ?? 'placed'}</strong>.
        The signal-stack below names this for every graha, each line cited.</>
    ),
  },
  {
    title: 'Friend or foe depends on your lagna',
    cite: 'BPHS Vol I, ch.34 / ch.44',
    enter: (a) => { a.scrollTo('#rg-signals') },
    body: (c) => (
      <>The same graha helps one lagna and harms another — a{' '}
        <strong>functional</strong> benefic or malefic, set by the houses it rules
        from <em>your</em> ascendant, and sometimes a <strong>māraka</strong> (a
        "killer" by lordship). The panel reads this for{' '}
        <strong>{c.namer.graha(c.dign)}</strong> and the rest — and keeps it
        strictly apart from a graha's natural nature, as ch.34 insists.</>
    ),
  },
  {
    title: 'Where each graha casts its gaze',
    cite: 'BPHS Vol I, ch.26',
    enter: (a) => { a.setStyle('wheel'); a.scrollTo('.chart-panel') },
    body: () => (
      <>Every graha aspects the <strong>7th</strong> sign from itself; Mars also
        the 4th &amp; 8th, Jupiter the 5th &amp; 9th, Saturn the 3rd &amp; 10th —
        this is <strong>dṛṣṭi</strong>. The dṛṣṭi ledger lists who aspects whom,
        and the <strong>Sky wheel</strong> (now shown) draws each graha's rays in
        to the centre.</>
    ),
  },
  {
    title: 'When it happens: the daśā',
    cite: 'BPHS Vol II, ch.46-47',
    enter: (a) => { a.scrollTo('#rg-dasha') },
    body: (c) => (
      <>The chart shows <em>what</em>; the Viṁśottarī <strong>daśā</strong> shows{' '}
        <em>when</em>.{' '}
        {c.curMaha
          ? <>You are running <strong>{c.namer.graha(c.g(c.curMaha.lord)) || c.curMaha.lord_name}</strong>'s
            mahādaśā{c.curAntar ? <> (the <strong>{c.namer.graha(c.g(c.curAntar.lord)) || c.curAntar.lord_name}</strong> antardaśā)</> : ''}.</>
          : <>Your running period is on the timeline.</>}{' '}
        BPHS names a daśā favourable or adverse only for specific placements
        (ch.47), so most periods it stays silent — which the timeline marks
        honestly rather than inventing a verdict.</>
    ),
  },
  {
    title: 'Go deeper: the divisional charts',
    cite: 'ṣoḍaśavarga',
    enter: (a) => { a.setVarga('D9'); a.setStyle('south'); a.scrollTo('.chart-panel') },
    body: () => (
      <>The rāśi (<strong>D1</strong>) is the body; the sixteen divisions refine
        each area — the <strong>D9 (navāṁśa)</strong>, shown now, for marriage and
        dharma; D10 for career; and so on. The same grahas fall into new signs,
        and a graha strong in D1 but weak across the vargas is a different story
        from one strong in both.</>
    ),
  },
  {
    title: 'The navāṁśa has its own reading',
    cite: 'C. S. Patel · modern',
    enter: (a) => {
      a.setVarga('D9'); a.setStyle('south')
      // The D9 panel mounts on the varga switch; scroll once it exists.
      setTimeout(() => a.scrollTo('.nv-panel'), 260)
    },
    body: (c) => {
      const nm = (k) => (k === 'lagna' ? 'Lagna' : c.namer.grahaKey(k))
      const vg = c.navamsa ? c.navamsa.vargottama.items : []
      const tally = c.navamsa ? c.navamsa.bhava_suchaka.tally : null
      return (
        <>The <strong>D9 panel</strong> below reads the navāṁśa itself — on a{' '}
          <strong>modern</strong> tier (C. S. Patel), kept apart from BPHS, which is
          silent here. A graha in the <em>same sign in D1 and D9</em> is{' '}
          <strong>vargottama</strong> — strong, its results amplified.{' '}
          {vg.length
            ? <>Yours: <strong>{vg.map((v) => nm(v.key)).join(', ')}</strong>.</>
            : <>Your chart has none — common, and the panel says so plainly.</>}{' '}
          It also marks the <strong>64th navāṁśa</strong>, a classical sensitive
          point{tally ? <>, and tallies each navāṁśa-sign by house
            ({tally.prosperous} favourable, {tally.difficult} difficult)</> : ''}.
          Every line names its source and stays a pointer — never a verdict.</>
      )
    },
  },
  {
    title: 'Reading, not guessing',
    cite: 'the whole point',
    enter: (a) => { a.setVarga('D1') },
    body: () => (
      <>A reading is <em>you</em> weighing these cited signals together —
        strength, function, aspect, timing, and their echo across the vargas. This
        site shows no single "score", and where the text is silent it says so.
        That refusal to guess is the difference between reading a chart and being
        told a story.</>
    ),
  },
]

// The index of the navāṁśa step, so callers can open the guide straight to it
// without hardcoding a position that reordering the steps would break.
export const NAVAMSA_STEP = STEPS.findIndex((s) => s.title.startsWith('The navāṁśa'))

export default function ReadingGuide({ chart, namer, actions, onClose, initialStep = 0 }) {
  const [step, setStep] = useState(initialStep)
  const ctx = useMemo(() => buildCtx(chart, namer), [chart, namer])
  const aRef = useRef(actions)
  aRef.current = actions

  // Run the step's panel action (scroll + highlight) when the step changes.
  useEffect(() => { STEPS[step]?.enter?.(aRef.current, ctx) }, [step, ctx])

  const s = STEPS[step]
  const last = STEPS.length - 1

  return (
    <div className="reading-guide" role="dialog" aria-label="How to read this chart">
      <div className="rg-head">
        <span className="rg-count">Reading a chart · {step + 1}/{STEPS.length}</span>
        <button type="button" className="rg-close" onClick={onClose} aria-label="Close guide">×</button>
      </div>
      <h4 className="rg-title">
        {s.title}
        <span className="rg-cite" title={`Cited to ${s.cite}`}>{s.cite}</span>
      </h4>
      <p className="rg-body">{s.body(ctx)}</p>
      <div className="rg-dots" aria-hidden="true">
        {STEPS.map((_, i) => (
          <span key={i} className={`rg-dot${i === step ? ' on' : ''}`} onClick={() => setStep(i)} />
        ))}
      </div>
      <div className="rg-nav">
        <button type="button" onClick={() => setStep((v) => Math.max(0, v - 1))} disabled={step === 0}>
          ‹ Back
        </button>
        {step < last
          ? <button type="button" className="rg-next" onClick={() => setStep((v) => v + 1)}>Next ›</button>
          : <button type="button" className="rg-next" onClick={onClose}>Done</button>}
      </div>
    </div>
  )
}
