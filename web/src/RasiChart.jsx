/**
 * Rāśi chart, drawn in either traditional style.
 *
 *  - South Indian: the twelve signs sit in FIXED cells; the lagna is marked.
 *  - North Indian:  the twelve BHĀVAS are fixed (house 1 always top-centre) and
 *                   the signs rotate to suit the lagna.
 *
 * Both render the same data — only the frame differs.
 */

const GRAHA_FULL = {
  sun: 'Sūrya', moon: 'Candra', mars: 'Maṅgala', mercury: 'Budha',
  jupiter: 'Guru', venus: 'Śukra', saturn: 'Śani', rahu: 'Rāhu', ketu: 'Ketu',
}

const RASI_FULL = [
  'Meṣa', 'Vṛṣabha', 'Mithuna', 'Karka', 'Siṁha', 'Kanyā',
  'Tulā', 'Vṛścika', 'Dhanu', 'Makara', 'Kumbha', 'Mīna',
]

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

function GrahaTag({ g }) {
  return (
    <span className={`tag${g.retrograde ? ' rx' : ''}`}
          title={`${g.name_en} — ${g.rasi_name_en} ${g.degree}°${g.minute}'`}>
      {GRAHA_FULL[g.key]}
      {g.retrograde && <sup>℞</sup>}
    </span>
  )
}

export function SouthIndianChart({ grahas, lagnaRasi, vargaKey, lagnaVargaSign }) {
  const bySign = groupBySign(grahas, vargaKey)
  const lagna = vargaKey === 'D1' ? lagnaRasi : lagnaVargaSign

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
                  <div className="centre-sub">Lagna {RASI_FULL[lagna]}</div>
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
              <div className="cell-sign">{RASI_FULL[sign]}</div>
              {sign === lagna && <div className="asc-mark">Lagna</div>}
              <div className="cell-grahas">
                {bySign[sign].map((g) => <GrahaTag g={g} key={g.key} />)}
              </div>
            </div>
          )
        }),
      )}
    </div>
  )
}

export function NorthIndianChart({ grahas, lagnaRasi, vargaKey, lagnaVargaSign }) {
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
        const top = r.cy - 14 - (lines > 1 ? (lines - 1) * (LEAD / 2) : 0)

        return (
          <g key={bhava}>
            <text x={r.cx} y={top} className="north-sign">
              <title>{`Bhāva ${bhava} — ${RASI_FULL[sign]}`}</title>
              {RASI_FULL[sign]}
            </text>
            {occupants.map((g, k) => (
              <text
                key={g.key}
                x={r.cx}
                y={top + 15 + k * LEAD}
                className={`north-graha${g.retrograde ? ' rx' : ''}`}
              >
                <title>{`${g.name_en} — ${g.degree}°${g.minute}'`}</title>
                {GRAHA_FULL[g.key]}{g.retrograde ? ' ℞' : ''}
              </text>
            ))}
          </g>
        )
      })}
    </svg>
  )
}
