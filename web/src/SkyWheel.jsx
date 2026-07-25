/**
 * Sky wheel — the horoscope as the sky actually stood, around the native.
 *
 * The native is at the centre. The lagna (ascendant) — the ecliptic degree
 * rising on the EASTERN horizon at birth — is pinned to the LEFT, and the
 * horizon is the horizontal diameter (east rising on the left, west setting on
 * the right). The twelve rāśis each cast their 30° counter-clockwise from there,
 * and every graha sits at its exact ecliptic degree, its ray reaching in to the
 * centre.
 *
 * WHY THIS IS ASTRONOMICALLY HONEST, AND WHERE IT STOPS
 * ----------------------------------------------------
 * With the ascendant degree on the horizon and points placed by true ecliptic
 * longitude, higher-longitude points fall BELOW the eastern horizon (not yet
 * risen) and lower-longitude points ABOVE it (already climbing) — which is the
 * real sky. The horizon (Ascendant→Descendant) is therefore an exact diameter.
 * The vertical is NOT drawn as a meridian: the true MC is not 90° from the
 * ascendant along the ecliptic except at the equator, so drawing a vertical
 * "meridian" would be a quiet lie. Houses are whole-sign (the site's frame), so
 * a bhāva is a whole rāśi; the ascendant degree marks the true rising point
 * within the lagna sign, which is why the lagna sign straddles the horizon.
 *
 * This is a REAL-SKY view, so it plots D1 ecliptic longitudes only — a varga is
 * a re-mapping of signs with no "degree within", so the wheel shows the rāśi.
 */

const SIZE = 520
const C = SIZE / 2
const R_OUT = 250          // outer edge of the sign ring
const R_IN = 202           // inner edge of the sign ring
const R_LABEL = 226        // rāśi name sits mid-band
const R_BHAVA = 190        // bhāva number just inside the ring
const R_TICK = R_IN        // a graha's exact-degree tick sits on the inner edge
const R_PLANET = 168       // base radius for graha glyphs
const STEP = 30            // radial stagger for a crowded cluster
const PAD_X = 50           // viewBox padding so edge labels (Lagna, signs) have room
const PAD_Y = 28
const DEG = Math.PI / 180

// Unambiguous 2-letter graha marks (common-name initials collide: Shukra/Shani).
const GLYPH = {
  sun: 'Su', moon: 'Mo', mars: 'Ma', mercury: 'Me', jupiter: 'Ju',
  venus: 'Ve', saturn: 'Sa', rahu: 'Ra', ketu: 'Ke',
}

const pad2 = (n) => String(n).padStart(2, '0')
const lonOf = (g) => (g.longitude != null
  ? g.longitude
  : g.rasi * 30 + (g.degree || 0) + (g.minute || 0) / 60 + (g.second || 0) / 3600)

const DIGNITY_WORD = {
  exalted: 'exalted', debilitated: 'debilitated', moolatrikona: 'in mūlatrikoṇa',
  own: 'in its own sign', friend: "in a friend's sign",
  neutral: "in a neutral's sign", enemy: "in an enemy's sign",
}
function dignityPhrase(d) {
  if (!d) return ''
  const word = DIGNITY_WORD[d.state] ?? d.state
  return ` — ${word}`
}

export default function SkyWheelChart({
  grahas, lagnaRasi, lagnaLongitude, vargaKey, namer,
  active, onHover, onPin, highlightSign,
}) {
  const ascLon = lagnaLongitude ?? lagnaRasi * 30

  // Screen angle for an ecliptic longitude: ascendant → left (180°), and higher
  // longitude runs clockwise-down from there, so the horizon is horizontal and
  // the sky above the horizon is genuinely above.
  const ang = (lon) => (180 - (lon - ascLon)) * DEG
  const pt = (lon, r) => [C + r * Math.cos(ang(lon)), C + r * Math.sin(ang(lon))]

  // Annular sector for one 30° rāśi, sampled so we never fight SVG arc flags.
  const band = (lon1, ri, ro) => {
    const n = 12
    let d = ''
    for (let i = 0; i <= n; i++) {
      const [x, y] = pt(lon1 + (30 * i) / n, ro)
      d += (i ? 'L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1)
    }
    for (let i = n; i >= 0; i--) {
      const [x, y] = pt(lon1 + (30 * i) / n, ri)
      d += 'L' + x.toFixed(1) + ',' + y.toFixed(1)
    }
    return d + 'Z'
  }

  const bhavaOf = (sign) => ((sign - lagnaRasi + 12) % 12) + 1

  // Place grahas at their true angle; stagger radius for tight clusters so glyphs
  // don't collide, with a connector back to the exact-degree tick.
  const placed = grahas
    .map((g) => {
      const lon = lonOf(g)
      let a = ((180 - (lon - ascLon)) % 360 + 360) % 360
      return { g, lon, a }
    })
    .sort((p, q) => p.a - q.a)
  let lastA = -99, level = 0
  for (const p of placed) {
    const gap = Math.min(Math.abs(p.a - lastA), 360 - Math.abs(p.a - lastA))
    level = gap < 10 ? Math.min(level + 1, 3) : 0
    p.r = R_PLANET - level * STEP
    lastA = p.a
  }

  const isD1 = vargaKey === 'D1'
  const [ascX, ascY] = pt(ascLon, R_IN)

  return (
    <svg viewBox={`${-PAD_X} ${-PAD_Y} ${SIZE + 2 * PAD_X} ${SIZE + 2 * PAD_Y}`}
         className="sky-wheel" role="img"
         aria-label="Sky wheel — the sky around the native at birth">
      {/* above / below the horizon, faintly distinguished */}
      <path className="sw-sky" d={`M ${C - R_OUT},${C} A ${R_OUT},${R_OUT} 0 0 1 ${C + R_OUT},${C} Z`} />

      {/* rāśi bands + boundaries */}
      {Array.from({ length: 12 }, (_, s) => {
        const lagnaBand = s === lagnaRasi
        const hi = s === highlightSign
        return (
          <path key={`b${s}`} d={band(s * 30, R_IN, R_OUT)}
                className={`sw-band${s % 2 ? ' alt' : ''}${lagnaBand ? ' lagna' : ''}${hi ? ' locate' : ''}`} />
        )
      })}
      {Array.from({ length: 12 }, (_, s) => {
        const [x1, y1] = pt(s * 30, R_IN)
        const [x2, y2] = pt(s * 30, R_OUT)
        return <line key={`bd${s}`} x1={x1} y1={y1} x2={x2} y2={y2} className="sw-bound" />
      })}
      <circle cx={C} cy={C} r={R_OUT} className="sw-ring" />
      <circle cx={C} cy={C} r={R_IN} className="sw-ring" />

      {/* 10° / 20° ticks inside each sign, to show the 30° cast */}
      {Array.from({ length: 36 }, (_, k) => {
        const lon = k * 10
        const major = k % 3 === 0
        const [x1, y1] = pt(lon, R_IN)
        const [x2, y2] = pt(lon, R_IN + (major ? 0 : 5))
        return major ? null
          : <line key={`t${k}`} x1={x1} y1={y1} x2={x2} y2={y2} className="sw-tick" />
      })}

      {/* rāśi names + bhāva numbers */}
      {Array.from({ length: 12 }, (_, s) => {
        const [lx, ly] = pt(s * 30 + 15, R_LABEL)
        const [bx, by] = pt(s * 30 + 15, R_BHAVA)
        return (
          <g key={`l${s}`}>
            <text x={lx} y={ly} className="sw-sign" dominantBaseline="middle">{namer.rasi(s)}</text>
            <text x={bx} y={by} className="sw-bhava" dominantBaseline="middle">
              <title>{`Bhāva ${bhavaOf(s)} — ${namer.rasi(s)}`}</title>
              {bhavaOf(s)}
            </text>
          </g>
        )
      })}

      {/* horizon: the Ascendant→Descendant diameter (exactly horizontal) */}
      <line x1={C - R_OUT} y1={C} x2={C + R_OUT} y2={C} className="sw-horizon" />
      <text x={C - R_OUT + 4} y={C - 8} className="sw-horizon-label">East · rising</text>
      <text x={C + R_OUT - 4} y={C - 8} className="sw-horizon-label" textAnchor="end">West · setting</text>

      {/* the lagna, pinned to the eastern horizon */}
      <g className="sw-asc">
        <polygon points={`${ascX - 12},${ascY - 6} ${ascX - 12},${ascY + 6} ${ascX - 2},${ascY}`} />
        <text x={ascX - 16} y={ascY - 8} textAnchor="end">
          <title>{`Lagna — ${namer.rasi(lagnaRasi)} ${(ascLon % 30).toFixed(2)}°`}</title>
          Lagna {Math.floor(ascLon % 30)}°
        </text>
      </g>

      {/* grahas: ray to centre, exact-degree tick, staggered glyph */}
      {isD1 && placed.map(({ g, lon, r }) => {
        const [tx, ty] = pt(lon, R_TICK)
        const [tx2, ty2] = pt(lon, R_TICK - 7)
        const [px, py] = pt(lon, r)
        const on = active === g.key
        return (
          <g key={g.key}
             className={`sw-graha${g.retrograde ? ' rx' : ''}${on ? ' active' : ''}`}
             onPointerEnter={() => onHover?.(g.key)}
             onPointerLeave={() => onHover?.(null)}
             onClick={() => onPin?.(g.key)}>
            <title>
              {`${g.name_en} — ${namer.rasi(g.rasi)} ${g.degree}°${pad2(g.minute)}'${pad2(g.second)}"`}
              {g.retrograde ? ' (retrograde)' : ''}{dignityPhrase(g.dignity)}
            </title>
            <line x1={px} y1={py} x2={C} y2={C} className="sw-ray" />
            <line x1={tx} y1={ty} x2={tx2} y2={ty2} className="sw-gtick" />
            <line x1={tx2} y1={ty2} x2={px} y2={py} className="sw-glink" />
            <circle cx={px} cy={py} r="13" className="sw-gdot" />
            <text x={px} y={py} className="sw-gglyph" textAnchor="middle" dominantBaseline="central">
              {GLYPH[g.key] || g.name_en.slice(0, 2)}{g.retrograde ? '℞' : ''}
            </text>
            <text x={px} y={py + 22} className="sw-gdeg" textAnchor="middle">
              {g.degree}°{pad2(g.minute)}′
            </text>
          </g>
        )
      })}

      {/* the native, at the centre */}
      <circle cx={C} cy={C} r="4" className="sw-center" />
      <text x={C} y={C + 20} className="sw-center-label" textAnchor="middle">the native</text>

      {!isD1 && (
        <text x={C} y={C - 20} className="sw-note" textAnchor="middle">
          real-sky view — shows the D1 rāśi
        </text>
      )}
    </svg>
  )
}
