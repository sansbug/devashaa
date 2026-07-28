/**
 * Sky wheel — the horoscope as the sky actually stood, around the native.
 *
 * The native is at the centre. The lagna (ascendant) — the ecliptic degree
 * rising on the EASTERN horizon at birth — is pinned to the LEFT, and the
 * horizon is the horizontal diameter (east rising on the left, west setting on
 * the right). The twelve rāśis each cast their 30° counter-clockwise from there,
 * subdivided into their nakṣatras and pādas, and every graha sits at its exact
 * ecliptic degree, its ray reaching in to the centre.
 *
 * WHY THIS IS ASTRONOMICALLY HONEST, AND WHERE IT STOPS
 * ----------------------------------------------------
 * With the ascendant degree on the horizon and points placed by true ecliptic
 * longitude, higher-longitude points fall BELOW the eastern horizon (not yet
 * risen) and lower-longitude points ABOVE it (already climbing) — the real sky.
 * The horizon (Ascendant→Descendant) is therefore an exact diameter, and the sky
 * above / earth below are shaded accordingly. The vertical is NOT drawn as a
 * meridian: the true MC is not 90° from the ascendant along the ecliptic except
 * at the equator, so drawing one would be a quiet lie. Houses are whole-sign, so
 * a bhāva is a whole rāśi; the ascendant degree marks the true rising point, so
 * the lagna sign straddles the horizon.
 *
 * The nakṣatra (13°20′) and pāda (3°20′) grids share the same degree axis: a
 * pāda boundary lands on every sign boundary (9 pādas/sign) and every nakṣatra
 * boundary (4 pādas/nakṣatra). Real-sky, so it plots D1 ecliptic longitudes.
 */

import { useState } from 'react'

const SIZE = 520
const C = SIZE / 2
const R_PLANET = 156       // base radius for graha glyphs
const R_SIGN_IN = 186
const R_SIGN_OUT = 232
const R_SIGN_LABEL = 210
const R_BHAVA = 196
const R_NAK_IN = 232
const R_NAK_OUT = 298
const R_NAK_LABEL = 270     // curved nakṣatra names run along this radius
const R_PADA_NUM = 244
const R_MAX = 298
const HALF = 332           // viewBox half-extent
const STEP = 30            // radial stagger for a crowded cluster
const NAK_ARC = 40 / 3     // 13°20′
const PADA_ARC = 10 / 3    // 3°20′
const DEG = Math.PI / 180

// Distinct graha colours — medium saffron-to-indigo hues that read on both the
// light and dark themes (traditional-flavoured: Sun warm, Saturn cold, …).
const GRAHA_COLOR = {
  sun: '#e8663a', moon: '#6f8fb0', mars: '#e04343', mercury: '#2fa06a',
  jupiter: '#d3a028', venus: '#d268a8', saturn: '#5566b8', rahu: '#8f8a97',
  ketu: '#a1785f',
}
// Rāśi element, for a faint sector tint: fire, earth, air, water repeating.
const ELEMENT = ['fire', 'earth', 'air', 'water']
const ELEMENT_COLOR = { fire: '#d9663a', earth: '#3f9f5f', air: '#c9a83e', water: '#4f86c6' }
// Compact nakṣatra marks (full name is in the tooltip). Fixed to avoid the
// Pūrva-/Uttara- collisions a naive slice would make.
const NAK_ABBR = ['Aśv', 'Bha', 'Kṛt', 'Roh', 'Mṛg', 'Ārd', 'Pun', 'Puṣ', 'Āśl',
  'Mag', 'PPh', 'UPh', 'Has', 'Cit', 'Svā', 'Viś', 'Anu', 'Jye', 'Mūl', 'PĀṣ',
  'UĀṣ', 'Śra', 'Dha', 'Śat', 'PBh', 'UBh', 'Rev']

const pad2 = (n) => String(n).padStart(2, '0')
const lonOf = (g) => (g.longitude != null
  ? g.longitude
  : g.rasi * 30 + (g.degree || 0) + (g.minute || 0) / 60 + (g.second || 0) / 3600)

const DIGNITY_WORD = {
  exalted: 'exalted', debilitated: 'debilitated', moolatrikona: 'in mūlatrikoṇa',
  own: 'in its own sign', friend: "in a friend's sign",
  neutral: "in a neutral's sign", enemy: "in an enemy's sign",
}
const dignityPhrase = (d) => (d ? ` — ${DIGNITY_WORD[d.state] ?? d.state}` : '')

function Toggle({ on, set, children }) {
  return (
    <button type="button" className={`sw-toggle${on ? ' on' : ''}`}
            aria-pressed={on} onClick={() => set((v) => !v)}>{children}</button>
  )
}

export default function SkyWheelChart({
  grahas, lagnaRasi, lagnaLongitude, vargaKey, namer, nakNames,
  active, onHover, onPin, highlightSign, drishti, dashaLords, runningDasha,
}) {
  const [shade, setShade] = useState(true)
  const [colors, setColors] = useState(true)
  const [naks, setNaks] = useState(true)
  const [padas, setPadas] = useState(true)
  const [drishtiOn, setDrishtiOn] = useState(true)
  const [dashaOn, setDashaOn] = useState(true)

  const ascLon = lagnaLongitude ?? lagnaRasi * 30
  const ang = (lon) => (180 - (lon - ascLon)) * DEG
  const pt = (lon, r) => [C + r * Math.cos(ang(lon)), C + r * Math.sin(ang(lon))]

  const band = (lon1, span, ri, ro) => {
    const n = 12
    let d = ''
    for (let i = 0; i <= n; i++) { const [x, y] = pt(lon1 + (span * i) / n, ro); d += (i ? 'L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1) }
    for (let i = n; i >= 0; i--) { const [x, y] = pt(lon1 + (span * i) / n, ri); d += 'L' + x.toFixed(1) + ',' + y.toFixed(1) }
    return d + 'Z'
  }
  const bhavaOf = (sign) => ((sign - lagnaRasi + 12) % 12) + 1

  // A concentric arc (sampled) for curved text to follow along the ring.
  const arcPath = (lonA, lonB, r) => {
    const n = 12
    let d = ''
    for (let i = 0; i <= n; i++) { const [x, y] = pt(lonA + (lonB - lonA) * i / n, r); d += (i ? 'L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1) }
    return d
  }
  // Purva → P, Uttara → U (both common and IAST spellings).
  const abbr = (s) => s.replace(/^(Pūrva|Purva)\s+/, 'P ').replace(/^Uttara\s+/, 'U ')

  const placed = grahas
    .map((g) => { const lon = lonOf(g); return { g, lon, a: ((180 - (lon - ascLon)) % 360 + 360) % 360 } })
    .sort((p, q) => p.a - q.a)
  let lastA = -99, level = 0
  for (const p of placed) {
    const gap = Math.min(Math.abs(p.a - lastA), 360 - Math.abs(p.a - lastA))
    level = gap < 10 ? Math.min(level + 1, 3) : 0
    p.r = R_PLANET - level * STEP
    lastA = p.a
  }

  const isD1 = vargaKey === 'D1'
  const [ascX, ascY] = pt(ascLon, R_SIGN_IN)

  // Dṛṣṭi lines for the selected graha (its graded ch.26 casts to each sign).
  // Nodes are excluded as aspectors, matching the ledger's refusal.
  const isNode = active === 'rahu' || active === 'ketu'
  const activePlaced = active && placed.find((p) => p.g.key === active)
  const drishtiCasts = (drishtiOn && isD1 && active && !isNode && activePlaced
    && drishti && drishti.graha && drishti.graha.casts[active])
    ? drishti.graha.casts[active].signs : null

  return (
    <div className="sw-wrap">
      <div className="sw-toggles">
        <Toggle on={shade} set={setShade}>Horizon</Toggle>
        <Toggle on={colors} set={setColors}>Graha colours</Toggle>
        <Toggle on={naks} set={setNaks}>Nakṣatras</Toggle>
        <Toggle on={padas} set={setPadas}>Pādas</Toggle>
        <Toggle on={drishtiOn} set={setDrishtiOn}>Dṛṣṭi</Toggle>
        <Toggle on={dashaOn} set={setDashaOn}>Daśā</Toggle>
      </div>
      <svg viewBox={`${C - HALF} ${C - HALF} ${2 * HALF} ${2 * HALF}`}
           className="sky-wheel" role="img"
           aria-label="Sky wheel — the sky around the native at birth">
        {/* above / below the horizon */}
        {shade && (
          <>
            <path className="sw-sky" d={`M ${C - R_MAX},${C} A ${R_MAX},${R_MAX} 0 0 1 ${C + R_MAX},${C} Z`} />
            <path className="sw-earth" d={`M ${C - R_MAX},${C} A ${R_MAX},${R_MAX} 0 0 0 ${C + R_MAX},${C} Z`} />
          </>
        )}

        {/* rāśi bands (faint element tint) + boundaries */}
        {Array.from({ length: 12 }, (_, s) => {
          const lagnaBand = s === lagnaRasi
          const hi = s === highlightSign
          const el = ELEMENT[s % 4]
          return (
            <path key={`b${s}`} d={band(s * 30, 30, R_SIGN_IN, R_SIGN_OUT)}
                  className={`sw-band${lagnaBand ? ' lagna' : ''}${hi ? ' locate' : ''}`}
                  style={colors && !lagnaBand && !hi ? { fill: ELEMENT_COLOR[el], fillOpacity: 0.14 } : undefined}>
              <title>{`${namer.rasi(s)} — ${el}`}</title>
            </path>
          )
        })}
        {Array.from({ length: 12 }, (_, s) => {
          const [x1, y1] = pt(s * 30, R_SIGN_IN)
          const [x2, y2] = pt(s * 30, R_SIGN_OUT)
          return <line key={`bd${s}`} x1={x1} y1={y1} x2={x2} y2={y2} className="sw-bound" />
        })}
        <circle cx={C} cy={C} r={R_SIGN_OUT} className="sw-ring" />
        <circle cx={C} cy={C} r={R_SIGN_IN} className="sw-ring" />

        {/* rāśi names + bhāva numbers */}
        {Array.from({ length: 12 }, (_, s) => {
          const [lx, ly] = pt(s * 30 + 15, R_SIGN_LABEL)
          const [bx, by] = pt(s * 30 + 15, R_BHAVA)
          return (
            <g key={`l${s}`}>
              <text x={lx} y={ly} className="sw-sign" textAnchor="middle" dominantBaseline="middle">{namer.rasi(s)}</text>
              <text x={bx} y={by} className="sw-bhava" textAnchor="middle" dominantBaseline="middle">
                <title>{`Bhāva ${bhavaOf(s)} — ${namer.rasi(s)}`}</title>{bhavaOf(s)}
              </text>
            </g>
          )
        })}

        {/* nakṣatra ring: 27 sectors, boundaries + compact marks */}
        {naks && (
          <>
            <circle cx={C} cy={C} r={R_NAK_OUT} className="sw-ring" />
            {Array.from({ length: 27 }, (_, n) => {
              const [x1, y1] = pt(n * NAK_ARC, R_NAK_IN)
              const [x2, y2] = pt(n * NAK_ARC, R_NAK_OUT)
              return <line key={`nb${n}`} x1={x1} y1={y1} x2={x2} y2={y2} className="sw-nakbound" />
            })}
            {Array.from({ length: 27 }, (_, n) => {
              // Curved: the name runs ALONG the ring at a constant radius, so it
              // never sticks out over the pādas. Reversed on the bottom half so it
              // reads right-side-up. Purva/Uttara abbreviate to P/U to keep the
              // long names within their sector.
              const lon1 = n * NAK_ARC, lon2 = (n + 1) * NAK_ARC
              const midLon = (lon1 + lon2) / 2
              const td = ((180 - (midLon - ascLon)) % 360 + 360) % 360
              // Reverse the guide arc on the TOP half so the text travels
              // left-to-right (upright) there; the bottom half already does.
              const flip = td > 180 && td < 360
              const d = flip ? arcPath(lon2, lon1, R_NAK_LABEL) : arcPath(lon1, lon2, R_NAK_LABEL)
              const full = nakNames ? namer.nakshatra(nakNames[n]) : NAK_ABBR[n]
              const id = `nkp${n}`
              return (
                <g key={`nn${n}`}>
                  <path id={id} d={d} className="sw-nakpath" />
                  <text className="sw-nak" dominantBaseline="central">
                    <title>{`${n + 1}. ${full}`}</title>
                    <textPath href={`#${id}`} startOffset="50%" textAnchor="middle">{abbr(full)}</textPath>
                  </text>
                </g>
              )
            })}
          </>
        )}

        {/* pāda grid: 108 ticks + the pāda number 1-4 inside each nakṣatra */}
        {naks && padas && Array.from({ length: 108 }, (_, p) => {
          const lon = p * PADA_ARC
          const isNakBound = p % 4 === 0
          const [x1, y1] = pt(lon, R_NAK_IN)
          const [x2, y2] = pt(lon, R_NAK_IN + (isNakBound ? 0 : 7))
          const [nx, ny] = pt(lon + PADA_ARC / 2, R_PADA_NUM)
          return (
            <g key={`p${p}`}>
              {!isNakBound && <line x1={x1} y1={y1} x2={x2} y2={y2} className="sw-padatick" />}
              <text x={nx} y={ny} className="sw-pada" textAnchor="middle" dominantBaseline="middle">{(p % 4) + 1}</text>
            </g>
          )
        })}

        {/* horizon: the Ascendant→Descendant diameter (exactly horizontal) */}
        <line x1={C - R_MAX} y1={C} x2={C + R_MAX} y2={C} className="sw-horizon" />
        <text x={C - R_MAX + 4} y={C - 8} className="sw-horizon-label">East · rising</text>
        <text x={C + R_MAX - 4} y={C - 8} className="sw-horizon-label" textAnchor="end">West · setting</text>

        {/* the lagna, pinned to the eastern horizon */}
        <g className="sw-asc">
          <polygon points={`${ascX - 12},${ascY - 6} ${ascX - 12},${ascY + 6} ${ascX - 2},${ascY}`} />
          <text x={ascX - 16} y={ascY - 8} textAnchor="end">
            <title>{`Lagna — ${namer.rasi(lagnaRasi)} ${(ascLon % 30).toFixed(2)}°`}</title>
            Lagna {Math.floor(ascLon % 30)}°
          </text>
        </g>

        {/* dṛṣṭi: the selected graha's graded aspects to each sign (ch.26).
            Drawn under the dots; opacity & width track the ¼/½/¾/full strength. */}
        {drishtiCasts && Object.entries(drishtiCasts).map(([s, v]) => {
          const [ax, ay] = pt(activePlaced.lon, activePlaced.r)
          const [bx, by] = pt(Number(s) * 30 + 15, R_SIGN_IN - 4)
          const col = colors ? GRAHA_COLOR[active] : null
          return (
            <line key={`dr${s}`} x1={ax} y1={ay} x2={bx} y2={by} className="sw-drishti"
                  style={{ strokeOpacity: 0.22 + v * 0.6, strokeWidth: 0.8 + v * 1.7, ...(col ? { stroke: col } : {}) }}>
              <title>{`${namer.grahaKey(active)} aspects ${namer.rasi(Number(s))} — ${{ 0.25: '¼', 0.5: '½', 0.75: '¾', 1: 'full' }[v] ?? v}`}</title>
            </line>
          )
        })}

        {/* grahas: ray to centre, exact-degree tick, staggered glyph */}
        {isD1 && placed.map(({ g, lon, r }) => {
          const [tx, ty] = pt(lon, R_SIGN_IN)
          const [tx2, ty2] = pt(lon, R_SIGN_IN - 7)
          const [px, py] = pt(lon, r)
          const on = active === g.key
          const col = colors ? GRAHA_COLOR[g.key] : null
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
              <line x1={px} y1={py} x2={C} y2={C} className="sw-ray" style={col ? { stroke: col } : undefined} />
              <line x1={tx} y1={ty} x2={tx2} y2={ty2} className="sw-gtick" style={col ? { stroke: col } : undefined} />
              <line x1={tx2} y1={ty2} x2={px} y2={py} className="sw-glink" />
              <circle cx={px} cy={py} r="13" className="sw-gdot" style={col ? { stroke: col } : undefined} />
              <text x={px} y={py} className="sw-gglyph" textAnchor="middle" dominantBaseline="central" style={col ? { fill: col } : undefined}>
                {(GRAHA_COLOR[g.key] ? { sun: 'Su', moon: 'Mo', mars: 'Ma', mercury: 'Me', jupiter: 'Ju', venus: 'Ve', saturn: 'Sa', rahu: 'Ra', ketu: 'Ke' }[g.key] : g.name_en.slice(0, 2))}{g.retrograde ? '℞' : ''}
              </text>
              <text x={px} y={py + 22} className="sw-gdeg" textAnchor="middle">{g.degree}°{pad2(g.minute)}′</text>
            </g>
          )
        })}

        {/* daśā: ring the graha ruling the running mahā (and antar) — the time
            sequence isn't spatial, but WHERE the ruling graha sits is. */}
        {dashaOn && isD1 && dashaLords && placed.map(({ g, lon, r }) => {
          const md = g.key === dashaLords.maha
          const ad = g.key === dashaLords.antar
          if (!md && !ad) return null
          const [px, py] = pt(lon, r)
          const lbl = md && ad ? 'MD·AD' : md ? 'MD' : 'AD'
          return (
            <g key={`dl${g.key}`} className={`sw-dasha-mark${md ? ' md' : ' ad'}`} style={{ pointerEvents: 'none' }}>
              <title>{md ? 'running mahādaśā lord' : 'running antardaśā lord'}</title>
              <circle cx={px} cy={py} r="18" className="sw-dasha-ring" />
              <text x={px} y={py - 21} className="sw-dasha-lbl" textAnchor="middle">{lbl}</text>
            </g>
          )
        })}

        {/* the native, at the centre */}
        <circle cx={C} cy={C} r="4" className="sw-center" />
        <text x={C} y={C + 20} className="sw-center-label" textAnchor="middle">the native</text>

        {!isD1 && (
          <text x={C} y={C - 20} className="sw-note" textAnchor="middle">real-sky view — shows the D1 rāśi</text>
        )}
      </svg>
      {dashaOn && isD1 && runningDasha && (
        <div className="sw-dasha-now" role="note">
          <span className="sw-dn-head">Running daśā · time remaining</span>
          <div className="sw-dn-rows">
            {runningDasha.levels.map((l) => (
              <span key={l.code} className="sw-dn-row">
                <span className="sw-dn-code" title={
                  l.code === 'MD' ? 'mahādaśā' : l.code === 'AD' ? 'antardaśā' : 'pratyantardaśā'
                }>{l.code}</span>
                <strong className="sw-dn-lord">{namer.grahaKey(l.lord)}</strong>
                <span className="sw-dn-rem">{l.remaining} left</span>
              </span>
            ))}
          </div>
          <span className="sw-dn-note">
            A daśā is a span of time, not a place — the rings mark where its lords
            sit; this is how much of each is left.
          </span>
        </div>
      )}
    </div>
  )
}
