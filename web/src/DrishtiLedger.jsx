/**
 * Dṛṣṭi ledger — what one graha aspects, and what aspects it.
 *
 * WHY THIS IS A PANEL AND NOT AN OVERLAY ON THE CHART
 * ---------------------------------------------------
 * Four renderings were designed and measured. Chords lose because seven arcs
 * leaving one cell are mutually tangent at the origin, so the 4th-house quarter
 * and the 5th-house three-quarters separate by about half a pixel at the chart's
 * full 620px. Cell-marks lose because the grading has to be read as a
 * fill-vs-empty distinction between --accent and --ruler-line, which is 1.66:1
 * in one theme and 1.54:1 in another, and inverts polarity between the dark and
 * light sets. A whole-graph matrix loses because its most-read cell lands at
 * 1.06:1.
 *
 * A nine-graha chart has roughly sixty graha-to-sign relationships in a figure
 * with twelve cells. The chart is the wrong surface for a graph that dense, and
 * a legible ledger beats an illegible overlay.
 *
 * THE TWO DOCTRINES ARE SEPARATED BY ELEMENT TYPE, NOT BY STYLING
 * ---------------------------------------------------------------
 * Graha dṛṣṭi (ch.26 vv.2-5) is graded — a quarter, a half, three quarters,
 * full — and renders as metered rows carrying a house count and a written
 * fraction. Rāśi dṛṣṭi (ch.8 vv.1-5) is NOT graded, and renders as bare chips
 * with no count, no meter and no number of any kind.
 *
 * That separation is structural on purpose. There is no shared component with a
 * `graded` flag that a later edit could flip; to grade a rāśi aspect you would
 * have to build a different component. BPHS grades one of these doctrines and
 * not the other, and any ¼-½-¾ on a rāśi aspect is an import from ch.26.
 */

import { useState } from 'react'

/** Written out, never as ¼ ½ ¾. Vulgar-fraction glyphs draw their numerals at
 *  roughly half digit height, so at this size ¼ and ¾ differ only in a ~3.5px
 *  mark — the one part a reader must actually distinguish. */
const FRACTION = { 0.25: '1/4', 0.5: '1/2', 0.75: '3/4', 1: 'full' }
const ORDINAL = ['', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th',
                 '8th', '9th', '10th', '11th', '12th']

/** Special full aspects, for the explanatory second line. ch.26 vv.4-5. */
const SPECIAL = {
  saturn: [3, 10], jupiter: [5, 9], mars: [4, 8],
}
const SPECIAL_WORD = {
  saturn: 'Śani', jupiter: 'Guru', mars: 'Maṅgala',
}

/** Inclusive house distance, matching drishti.house_distance on the backend.
 *  Used ONLY for labelling a row we were given — never to decide an aspect. */
const houseDistance = (from, to) => ((to - from + 12) % 12) + 1

/** Four discrete boxes, never a continuous bar: BPHS gives four slabs, and a
 *  bar would assert an interpolation between them that the text does not make. */
function Meter({ value }) {
  const filled = Math.round(value * 4)
  return (
    <span className="dr-meter" aria-hidden="true">
      {[1, 2, 3, 4].map((i) => (
        <span key={i} className={`dr-box${i <= filled ? ' on' : ''}`} />
      ))}
    </span>
  )
}

function Flag({ text }) {
  const [open, setOpen] = useState(false)
  return (
    <>
      <button type="button" className="sig-flag" aria-expanded={open}
              title="The text does not settle this" onClick={() => setOpen(!open)}>⚑</button>
      {open && <p className="sig-flag-body">{text}</p>}
    </>
  )
}

function Row({ count, countLabel, value, target, extra, onHoverSign, sign }) {
  return (
    <div className="dr-row"
         onPointerEnter={() => onHoverSign?.(sign)}
         onPointerLeave={() => onHoverSign?.(null)}>
      <span className="dr-count">{countLabel ?? ORDINAL[count]}</span>
      <Meter value={value} />
      <span className="dr-target">
        {target}
        {extra && <span className="dr-extra"> {extra}</span>}
      </span>
      <span className="dr-frac">{FRACTION[value] ?? value}</span>
    </div>
  )
}

export default function DrishtiLedger({
  drishti, grahas, namer, subject, onPickSubject, onHoverSign, varga,
}) {
  // The engine counts from the sign a graha actually stands in. A varga sign is
  // derived, so there is no aspect "from D9 Kanyā" in Parāśara — the panel
  // refuses rather than counting from a sign the graha does not occupy.
  if (varga !== 'D1') {
    return (
      <div className="drishti-ledger">
        <h4 className="sig-title">Dṛṣṭi</h4>
        <div className="sig-row unavailable">
          <div className="sig-head">
            <span className="sig-mark" aria-hidden="true">⊘</span>
            <span className="sig-name">Unavailable in {varga}</span>
          </div>
          <p className="sig-reason">
            Ch.26 vv.2-5 and ch.8 vv.1-5 both count from the sign a graha
            actually stands in. A varga sign is derived — there is no aspect
            “from {varga} Kanyā” in Parāśara. Switch to D1.
          </p>
        </div>
      </div>
    )
  }
  if (!drishti) return null

  const g = drishti.graha
  const r = drishti.rasi
  const casts = g.casts[subject]
  const subjName = namer.grahaKey(subject)
  const bySign = {}
  for (const x of grahas) (bySign[x.rasi] ||= []).push(x)

  // NOT from `casts` — the nodes are absent there by design (they are excluded
  // as ASPECTORS), but they still stand in a sign, still receive aspects, and
  // their sign still casts rāśi dṛṣṭi. Reading the sign from the chart rather
  // than from the casts table keeps those two halves independent, which is
  // exactly the distinction ch.26-vs-ch.8 requires.
  const subjSign = grahas.find((x) => x.key === subject)?.rasi ?? casts?.from_sign

  const received = g.received?.signs?.[String(subjSign)] ?? {}
  const isNode = subject === 'rahu' || subject === 'ketu'

  return (
    <div className="drishti-ledger">
      <div className="graha-picker">
        {grahas.map((x) => (
          <button type="button" key={x.key}
                  className={subject === x.key ? 'on' : ''}
                  onClick={() => onPickSubject(x.key)}>
            {namer.graha(x)}
          </button>
        ))}
      </div>
      <p className="dr-context">
        {subjName} — {namer.rasi(subjSign)}
      </p>

      {/* ---------------- CASTS — ch.26, graded ---------------- */}
      <h4 className="sig-title">
        Casts <span className="sig-cite">{g.citation}</span>
      </h4>

      {isNode ? (
        // An empty block would read as "Rāhu aspects nothing", which is a
        // different and false claim. The refusal has to be stated.
        <div className="sig-row unavailable">
          <div className="sig-head">
            <span className="sig-mark" aria-hidden="true">⊘</span>
            <span className="sig-name">No graha dṛṣṭi for {subjName}</span>
          </div>
          <p className="sig-reason">
            Ch.26 never names Rāhu or Ketu among the aspecting grahas. Their
            graha dṛṣṭi rests on Santhanam’s note, not on the mūla, so it is not
            computed here. What aspects <em>them</em> is not in doubt and is
            listed below.
          </p>
        </div>
      ) : (
        <>
          {Object.entries(casts?.signs ?? {})
            .map(([s, v]) => [Number(s), v])
            .sort((a, b) => houseDistance(subjSign, a[0]) - houseDistance(subjSign, b[0]))
            .map(([s, v]) => {
              const occ = (bySign[s] ?? []).map((o) => {
                // The one place the asymmetry is visible on a single line:
                // what that occupant sends back to the subject.
                const back = g.casts[o.key]?.grahas?.[subject]
                return `${namer.graha(o)}${back ? ` (returns ${FRACTION[back]})` : ''}`
              })
              return (
                <Row key={s} sign={s} count={houseDistance(subjSign, s)} value={v}
                     target={namer.rasi(s)}
                     extra={occ.length ? `· ${occ.join(', ')}` : null}
                     onHoverSign={onHoverSign} />
              )
            })}
          {SPECIAL[subject] && (
            <p className="dr-note">
              {SPECIAL_WORD[subject]}’s special aspect — full on the{' '}
              {SPECIAL[subject].map((h) => ORDINAL[h]).join(' and the ')}, where
              the general rule would give less.
            </p>
          )}
        </>
      )}

      {/* ---------------- RECEIVED ---------------- */}
      <h4 className="sig-title">Received</h4>
      {Object.keys(received).length === 0 ? (
        <p className="dr-note">No graha aspects {namer.rasi(subjSign)} in this chart.</p>
      ) : (
        Object.entries(received).map(([k, v]) => {
          const from = g.casts[k]?.from_sign
          // The count MUST be the aspector's, labelled as theirs. Counting back
          // would print a house number that is not in the table at all: Śani's
          // 3rd, counted in reverse, is an 11th, and ch.26 gives no 11th aspect.
          const h = from === undefined ? null : houseDistance(from, subjSign)
          return (
            <Row key={k} sign={from} value={v}
                 countLabel={h ? `${namer.grahaKey(k)}’s ${ORDINAL[h]}` : namer.grahaKey(k)}
                 target={`from ${namer.rasi(from)}`}
                 onHoverSign={onHoverSign} />
          )
        })
      )}
      <p className="dr-note">
        Asymmetric. The 3rd and the 8th are one-way. The 4th and the 10th are
        mutual but unequal — a graha’s 4th is three quarters and what comes back
        is a quarter. Only the 5th, 9th and 7th return what they send.
      </p>

      {/* ---------------- RĀŚI DṚṢṬI — ch.8, UNGRADED ----------------
          A different element type on purpose. No count, no meter, no fraction:
          there is nothing here to grade, and rendering one would be an import
          from the chapter above. */}
      <h4 className="sig-title">
        Rāśi dṛṣṭi <span className="sig-cite">{r.citation}</span>
      </h4>
      <p className="dr-chips-line">
        <strong>{namer.rasi(subjSign)}</strong> ⟷{' '}
        {(r.sign_table?.[String(subjSign)] ?? []).map((s) => (
          <span key={s} className="dr-chip"
                onPointerEnter={() => onHoverSign?.(s)}
                onPointerLeave={() => onHoverSign?.(null)}>
            {namer.rasi(s)}
          </span>
        ))}
        <span className="dr-mutual">always mutual</span>
      </p>
      <p className="dr-note">{r.ungraded_note}</p>
      {r.notes?.map((n, i) => <Flag key={i} text={n} />)}

      <p className="dr-note dr-legend">
        The meter shows the four slabs BPHS gives — a quarter, a half, three
        quarters, full. Both doctrines here are counted <strong>from the
        sign</strong>, not from the degree: the ruler in each cell measures
        longitude, and no number on it is used here. Ch.26’s finer
        degree-counted layer (vv.6-12, in virūpas) is a different instrument and
        is not shown on this panel.
      </p>
    </div>
  )
}
