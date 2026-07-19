/**
 * Rāśi chart, drawn in either traditional style.
 *
 *  - South Indian: the twelve signs sit in FIXED cells; the lagna is marked.
 *  - North Indian:  the twelve BHĀVAS are fixed (house 1 always top-centre) and
 *                   the signs rotate to suit the lagna.
 *
 * Both render the same data — only the frame differs.
 */

/* Names are supplied by the `namer` prop (see naming.js) so the chart follows the
   selected name style. Nothing here is abbreviated — the cells have room. */

import { useState } from 'react'
import CellRuler, { useRulerMode } from './CellRuler'

/** Wrapper so the viewport hook lives in its own component and can therefore
    return "no ruler at all" without breaking the rules of hooks. */
function SignRuler({ occupants, ...rest }) {
  const mode = useRulerMode(occupants.length)
  if (!mode) return null
  return <CellRuler occupants={occupants} mode={mode} {...rest} />
}

// South Indian: signs are fixed in this layout, Aries at row0/col1, going clockwise.
const SOUTH_CELLS = [
  [11, 0, 1, 2],
  [10, null, null, 3],
  [9, null, null, 4],
  [8, 7, 6, 5],
]

// North Indian: 12 regions of a square cut by its diagonals and inner diamond.
// Listed as bhāva 1..12 in the conventional arrangement.
const NORTH_REGIONS = [
  { pts: '200,0 300,100 200,200 100,100', cx: 200, cy: 100 }, // 1  top diamond
  { pts: '0,0 200,0 100,100', cx: 100, cy: 35 },              // 2
  { pts: '0,0 100,100 0,200', cx: 35, cy: 100 },              // 3
  { pts: '0,200 100,100 200,200 100,300', cx: 100, cy: 200 }, // 4  left diamond
  { pts: '0,200 100,300 0,400', cx: 35, cy: 300 },            // 5
  { pts: '0,400 100,300 200,400', cx: 100, cy: 365 },         // 6
  { pts: '200,400 100,300 200,200 300,300', cx: 200, cy: 300 },// 7 bottom diamond
  { pts: '200,400 300,300 400,400', cx: 300, cy: 365 },       // 8
  { pts: '400,400 300,300 400,200', cx: 365, cy: 300 },       // 9
  { pts: '400,200 300,300 200,200 300,100', cx: 300, cy: 200 },// 10 right diamond
  { pts: '400,200 300,100 400,0', cx: 365, cy: 100 },         // 11
  { pts: '400,0 300,100 200,0', cx: 300, cy: 35 },            // 12
]

/** Group grahas by the sign they occupy in the chosen varga. */
function groupBySign(grahas, vargaKey) {
  const bySign = Array.from({ length: 12 }, () => [])
  for (const g of grahas) bySign[g.vargas[vargaKey]].push(g)
  return bySign
}

const pad2 = (n) => String(n).padStart(2, '0')

/** Bhāva of a sign, counted from the lagna's sign. Whole-sign, so rāśi = bhāva. */
const bhavaOf = (sign, lagna) => ((sign - lagna + 12) % 12) + 1

/**
 * Bhāva typology, marked on the numeral rather than by colour so it survives
 * every theme and colour blindness.
 *   kendra  1,4,7,10  — boxed
 *   trikoṇa 1,5,9     — underlined  (house 1 is both)
 *   duḥsthāna 6,8,12  — struck through
 * Houses 2,3,11 are deliberately unmarked — "bare" does NOT mean duḥsthāna.
 */
function bhavaClass(b) {
  const c = ['bhava-num']
  if ([1, 4, 7, 10].includes(b)) c.push('kendra')
  if ([1, 5, 9].includes(b)) c.push('trikona')
  if ([6, 8, 12].includes(b)) c.push('duhsthana')
  return c.join(' ')
}

/** Dignity as one clause of prose, for the tag's tooltip. `null` for the nodes:
    BPHS assigns Rāhu and Ketu no exaltation, so absence here is a finding, not
    a gap. */
const DIGNITY_WORD = {
  exalted: 'exalted', debilitated: 'debilitated', moolatrikona: 'in mūlatrikoṇa',
  own: 'in its own sign', friend: "in a friend's sign",
  neutral: "in a neutral's sign", enemy: "in an enemy's sign",
}
function dignityPhrase(d) {
  if (!d) return ''
  const word = DIGNITY_WORD[d.state] ?? d.state
  // uccha_distance is signed: negative means the graha has not yet reached its
  // deep-exaltation point.
  const arc = Math.abs(d.uccha_distance).toFixed(2)
  const side = d.uccha_distance < 0 ? 'short of' : 'past'
  return ` — ${word}; ${arc}° ${side} its exaltation point (uccha bala ${d.uccha_bala})`
}

function GrahaTag({ g, namer, active, onActivate }) {
  return (
    <span className={`tag${g.retrograde ? ' rx' : ''}${active ? ' active' : ''}`}
          onPointerEnter={() => onActivate?.(g.key)}
          onPointerLeave={() => onActivate?.(null)}
          onClick={() => onActivate?.(active ? null : g.key)}
          title={`${g.name_en} — ${g.rasi_name_en} ${g.degree}°${pad2(g.minute)}'${pad2(g.second)}"` +
                 `${g.retrograde ? ' (retrograde)' : ''}${dignityPhrase(g.dignity)}`}>
      <span className="tag-name">
        {namer.graha(g)}
        {g.retrograde && <sup>℞</sup>}
      </span>
      {/* Degree is the datum everything else is verifiable against — dignity,
          combustion, varga placement all follow from it. */}
      <span className="tag-deg">{g.degree}°{pad2(g.minute)}′</span>
    </span>
  )
}

export function SouthIndianChart({
  grahas, lagnaRasi, vargaKey, lagnaVargaSign, namer, landmarks, lagnaLongitude,
  gandanta,
}) {
  const bySign = groupBySign(grahas, vargaKey)
  const lagna = vargaKey === 'D1' ? lagnaRasi : lagnaVargaSign
  const [active, setActive] = useState(null)

  // The ruler measures longitude WITHIN a sign, so it is meaningful only where
  // the cell's sign is the sign the graha is actually standing in — i.e. D1.
  // A varga sign is derived; there is no "degree into D9 Kanyā".
  const ruled = vargaKey === 'D1' && !!landmarks

  return (
    <div className="south-chart" role="img" aria-label="South Indian rāśi chart">
      {SOUTH_CELLS.map((row, ri) =>
        row.map((sign, ci) => {
          if (sign === null) {
            // The 2x2 hole in the middle — render once, as the label block.
            if (ri === 1 && ci === 1) {
              return (
                <div className="south-centre" key="centre">
                  <div className="centre-varga">{vargaKey}</div>
                  <div className="centre-sub">Lagna {namer.rasi(lagna)}</div>
                </div>
              )
            }
            return null
          }
          return (
            <div
              className={`south-cell${sign === lagna ? ' is-lagna' : ''}`}
              key={`${ri}-${ci}`}
              style={{ gridRow: ri + 1, gridColumn: ci + 1 }}
            >
              <div className="cell-sign">
                <span className={bhavaClass(bhavaOf(sign, lagna))}>
                  {bhavaOf(sign, lagna)}
                </span>
                <span className="cell-sep">·</span>
                {namer.rasi(sign)}
              </div>
              {sign === lagna && <div className="asc-mark">Lagna</div>}
              <div className="cell-grahas">
                {bySign[sign].map((g) => (
                  <GrahaTag g={g} namer={namer} key={g.key}
                            active={active === g.key} onActivate={setActive} />
                ))}
              </div>
              {ruled && (
                <SignRuler
                  sign={sign}
                  occupants={bySign[sign]}
                  landmarks={landmarks[sign]}
                  lagnaDegree={sign === lagna ? lagnaLongitude % 30 : null}
                  gandanta={gandanta}
                  active={active}
                  onActivate={setActive}
                />
              )}
            </div>
          )
        }),
      )}
    </div>
  )
}

export function NorthIndianChart({ grahas, lagnaRasi, vargaKey, lagnaVargaSign, namer }) {
  const bySign = groupBySign(grahas, vargaKey)
  const lagna = vargaKey === 'D1' ? lagnaRasi : lagnaVargaSign

  return (
    <svg viewBox="-2 -2 404 404" className="north-chart" role="img"
         aria-label="North Indian bhāva chart">
      <rect x="0" y="0" width="400" height="400" className="frame" />
      <line x1="0" y1="0" x2="400" y2="400" className="frame" />
      <line x1="400" y1="0" x2="0" y2="400" className="frame" />
      <polygon points="200,0 400,200 200,400 0,200" className="frame" />

      {NORTH_REGIONS.map((r, i) => {
        const bhava = i + 1
        // In North Indian style the house is fixed and the SIGN rotates with it.
        const sign = (lagna + i) % 12
        const occupants = bySign[sign]
        // Stack the sign label plus its occupants around the region's centre so
        // a busy house grows symmetrically instead of running out of its wedge.
        // LEAD must exceed the 10px font's ~13.7 line box or stacked names crowd.
        const LEAD = 13
        const lines = occupants.length
        // Clamp: region 2 has cy=35, so five occupants would centre the stack
        // at y=-5 and print the sign label off the top of the viewBox.
        const top = Math.max(10, r.cy - 14 - (lines > 1 ? (lines - 1) * (LEAD / 2) : 0))

        // The wedges have a hard ~70-unit horizontal ceiling and text-anchor
        // middle grows BOTH ways across the frame diagonal, so degrees only
        // appear in an uncrowded house, and then whole degrees only.
        const showDeg = occupants.length <= 2

        return (
          <g key={bhava}>
            <text x={r.cx} y={top} className="north-sign">
              <title>{`Bhāva ${bhava} — ${namer.rasi(sign)}`}</title>
              <tspan className="north-bhava">{bhava}</tspan>
              {` · ${namer.rasi(sign)}`}
            </text>
            {occupants.map((g, k) => (
              <text
                key={g.key}
                x={r.cx}
                y={top + 15 + k * LEAD}
                className={`north-graha${g.retrograde ? ' rx' : ''}`}
              >
                <title>{`${g.name_en} — ${g.degree}°${pad2(g.minute)}'`}</title>
                {namer.graha(g)}{g.retrograde ? ' ℞' : ''}
                {showDeg && <tspan className="north-deg">{` ${g.degree}°`}</tspan>}
              </text>
            ))}
          </g>
        )
      })}
    </svg>
  )
}
