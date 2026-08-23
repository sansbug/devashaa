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
import { useLang } from './LangContext.jsx'
import { BhavaHoverCard, useBhavaHover } from './RasiChart.jsx'

const SIZE = 520
const C = SIZE / 2
const R_PLANET = 156       // base radius for graha glyphs
const R_TRANSIT = 116      // inner "ghost ring" for transiting grahas
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
const CODE = { sun: 'Su', moon: 'Mo', mars: 'Ma', mercury: 'Me', jupiter: 'Ju',
  venus: 'Ve', saturn: 'Sa', rahu: 'Ra', ketu: 'Ke' }
// Devanāgarī graha codes (the standard Hindi-jyotiṣa abbreviations) for the
// Devanāgarī name style; the wheel's glyph slot is too small for full names.
const CODE_DEV = { sun: 'सू', moon: 'चं', mars: 'मं', mercury: 'बु', jupiter: 'गु',
  venus: 'शु', saturn: 'श', rahu: 'रा', ketu: 'के' }
const ordinal = (n) => {
  const s = ['th', 'st', 'nd', 'rd'], v = n % 100
  return n + (s[(v - 20) % 10] || s[v] || s[0])
}
// The "return" (a graha back on its own natal degree) is a Western frame with no
// BPHS transit doctrine behind it, so the natal-degree offset is shown only for
// the slow grahas whose long cycle makes it worth noticing — never the fast ones.
const SLOW_RETURN = new Set(['saturn', 'jupiter', 'rahu', 'ketu'])
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
  exalted: 'sw.dword.exalted', debilitated: 'sw.dword.debilitated', moolatrikona: 'sw.dword.moolatrikona',
  own: 'sw.dword.own', friend: 'sw.dword.friend',
  neutral: 'sw.dword.neutral', enemy: 'sw.dword.enemy',
}
const dignityPhrase = (d, t) => (d ? ` — ${t(DIGNITY_WORD[d.state] ?? d.state)}` : '')

// Dignity as a categorical STATE (BPHS ch.3 vv.49–55): seven distinct hues,
// deliberately NOT a green→red strength ramp — BPHS never numbers dignity, so
// the states jump across the wheel (teal / green / periwinkle / olive / grey /
// amber / crimson) rather than shading smoothly. Chosen to sit clear of the
// GRAHA_COLOR identity hues so a state ring is never mistaken for a planet's own
// colour (e.g. exalted is teal, NOT Mercury's green). Tooltip carries the word.
const DIGNITY_COLOR = {
  exalted: '#1ec7cf', moolatrikona: '#3fb06e', own: '#7d92e8',
  friend: '#93a544', neutral: '#9aa0ab', enemy: '#d68a34', debilitated: '#cf3f5e',
}
// Legend follows BPHS's own listing (uccha → nīcha). friend/neutral/enemy are the
// ch.3 v.55 NATURAL (permanent) relationship — friend-and-enemy resolves to neutral.
const DIGNITY_LEGEND = [
  ['exalted', 'sw.dig.exalted'], ['moolatrikona', 'sw.dig.moolatrikona'], ['own', 'sw.dig.own'],
  ['friend', 'sw.dig.friend'], ['neutral', 'sw.dig.neutral'], ['enemy', 'sw.dig.enemy'],
  ['debilitated', 'sw.dig.debilitated'],
]

function Toggle({ on, set, children }) {
  return (
    <button type="button" className={`sw-toggle${on ? ' on' : ''}`}
            aria-pressed={on} onClick={() => set((v) => !v)}>{children}</button>
  )
}

export default function SkyWheelChart({
  grahas, lagnaRasi, lagnaLongitude, vargaKey, namer, nakNames,
  active, onHover, onPin, highlightSign, drishti, dashaLords, runningDasha, combust, analysis,
  transit, transitOn, setTransitOn, transitDate, setTransitDate, transitBusy, transitErr,
}) {
  const [shade, setShade] = useState(true)
  const [colors, setColors] = useState(true)
  const [naks, setNaks] = useState(true)
  const [padas, setPadas] = useState(true)
  const [drishtiOn, setDrishtiOn] = useState(true)
  const [dashaOn, setDashaOn] = useState(true)
  const [dignityOn, setDignityOn] = useState(true)
  const [ucchaOn, setUcchaOn] = useState(true)
  // Which transit graha's aspect lines to show — hover (mouse) or pin (tap).
  const [hoverT, setHoverT] = useState(null)
  const [pinT, setPinT] = useState(null)
  const markedT = pinT ?? hoverT
  const { t } = useLang()

  // Bhava hover/tap card — the wheel plots D1 ecliptic longitudes, so D1 only.
  const cardable = vargaKey === 'D1' && analysis && !analysis.error
  const { hovSign, sticky, rootRef, enter, leave, tap } = useBhavaHover(cardable)

  const todayStr = new Date().toISOString().slice(0, 10)
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

  // A small triangle at a longitude on the sign rim, apex pointing radially
  // (outward for an exaltation tick, inward for a fall tick).
  const radialTri = (lon, rBase, len, half, outward) => {
    const a = ang(lon)
    const ux = Math.cos(a), uy = Math.sin(a)      // radial unit
    const tx = -Math.sin(a), ty = Math.cos(a)     // tangent unit
    const rA = rBase + (outward ? len : -len)
    const apex = `${(C + rA * ux).toFixed(1)},${(C + rA * uy).toFixed(1)}`
    const b1 = `${(C + rBase * ux + half * tx).toFixed(1)},${(C + rBase * uy + half * ty).toFixed(1)}`
    const b2 = `${(C + rBase * ux - half * tx).toFixed(1)},${(C + rBase * uy - half * ty).toFixed(1)}`
    return `${apex} ${b1} ${b2}`
  }

  // A concentric arc (sampled) for curved text to follow along the ring.
  const arcPath = (lonA, lonB, r) => {
    const n = 12
    let d = ''
    for (let i = 0; i <= n; i++) { const [x, y] = pt(lonA + (lonB - lonA) * i / n, r); d += (i ? 'L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1) }
    return d
  }
  // An arc hugging radius r, from `fromLon` by a SIGNED `span` (degrees) — a
  // negative span traces backward (increasing/decreasing longitude both work),
  // which is what keeps a retrograde body's arc on the side it actually crossed.
  const ringArc = (fromLon, span, r) => {
    const n = Math.max(6, Math.round(Math.abs(span) / 5))
    let d = ''
    for (let i = 0; i <= n; i++) { const [x, y] = pt(fromLon + span * i / n, r); d += (i ? 'L' : 'M') + x.toFixed(1) + ',' + y.toFixed(1) }
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

  // Transiting grahas share the wheel's geometry but ride an inner "ghost" ring;
  // a crowded cluster staggers inward the same way the natal grahas do.
  const placedTransit = (transitOn && isD1 && transit && !transit.error && transit.grahas)
    ? transit.grahas
        .map((t) => ({ t, lon: t.longitude, a: ((180 - (t.longitude - ascLon)) % 360 + 360) % 360 }))
        .sort((p, q) => p.a - q.a)
    : []
  {
    let tLastA = -99, tLevel = 0
    for (const p of placedTransit) {
      const gap = Math.min(Math.abs(p.a - tLastA), 360 - Math.abs(p.a - tLastA))
      tLevel = gap < 10 ? Math.min(tLevel + 1, 3) : 0
      p.r = R_TRANSIT - tLevel * 22
      tLastA = p.a
    }
  }

  // Where each natal point sits, so a hovered transit's aspect line can land on
  // the actual natal graha (or the lagna) it aspects, not just the sign.
  const natalPos = {}
  for (const p of placed) natalPos[p.g.key] = [p.lon, p.r]
  natalPos.lagna = [ascLon, R_SIGN_IN]
  const hoverTransit = markedT ? placedTransit.find((p) => p.t.key === markedT) : null
  // The natal-degree arc only shows for slow grahas; when it does, the aspect
  // fan steps back so the two overlays establish a hierarchy instead of competing.
  const returnShowing = !!(hoverTransit && hoverTransit.t.return && SLOW_RETURN.has(hoverTransit.t.key))
  const [ascX, ascY] = pt(ascLon, R_SIGN_IN)

  // Exaltation (uccha) and fall (nīca) landmarks: the exact BPHS ch.3 vv.49–50
  // degree points, one pair per non-node graha. A graha near its own tick is
  // near deep exaltation/fall — the point the whole-sign dignity ring can't show.
  const dignityPoints = (ucchaOn && isD1)
    ? grahas.flatMap((g) => {
        const d = g.dignity
        if (!d) return []   // nodes carry no dignity → no tick
        const ex = d.exaltation, de = d.debilitation
        return [
          { key: g.key, kind: 'uccha', lon: ex.sign * 30 + ex.degree, sign: ex.sign, deg: ex.degree, dist: d.uccha_distance },
          { key: g.key, kind: 'nica', lon: de.sign * 30 + de.degree, sign: de.sign, deg: de.degree, dist: d.nica_distance },
        ]
      })
    : []

  // Dṛṣṭi lines for the selected graha (its graded ch.26 casts to each sign).
  // Nodes are excluded as aspectors, matching the ledger's refusal.
  const isNode = active === 'rahu' || active === 'ketu'
  const activePlaced = active && placed.find((p) => p.g.key === active)
  const drishtiCasts = (drishtiOn && isD1 && active && !isNode && activePlaced
    && drishti && drishti.graha && drishti.graha.casts[active])
    ? drishti.graha.casts[active].signs : null

  return (
    <div className="sw-wrap" ref={rootRef} onPointerLeave={leave}>
      <div className="sw-toggles">
        <Toggle on={shade} set={setShade}>{t('sw.toggle.horizon')}</Toggle>
        <Toggle on={colors} set={setColors}>{t('sw.toggle.graha_colours')}</Toggle>
        <Toggle on={naks} set={setNaks}>{t('sw.toggle.nakshatras')}</Toggle>
        <Toggle on={padas} set={setPadas}>{t('sw.toggle.padas')}</Toggle>
        <Toggle on={drishtiOn} set={setDrishtiOn}>{t('sw.toggle.drishti')}</Toggle>
        <Toggle on={dashaOn} set={setDashaOn}>{t('sw.toggle.dasha')}</Toggle>
        <Toggle on={dignityOn} set={setDignityOn}>{t('sw.toggle.dignity')}</Toggle>
        <Toggle on={ucchaOn} set={setUcchaOn}>{t('sw.toggle.uccha_nica')}</Toggle>
        {setTransitOn && <Toggle on={transitOn} set={setTransitOn}>{t('sw.toggle.transits')}</Toggle>}
      </div>
      {transitOn && isD1 && (
        <div className="sw-transit-bar">
          <label className="sw-tb-date">
            {t('sw.transit.as_of')}
            <input type="date" value={transitDate || todayStr}
                   onChange={(e) => setTransitDate(e.target.value)} />
          </label>
          {transitDate && (
            <button type="button" className="sw-tb-now" onClick={() => setTransitDate('')}>{t('sw.transit.now')}</button>
          )}
          <span className="sw-transit-status">
            {transitBusy ? t('sw.transit.loading')
              : transitErr ? `⚠ ${transitErr}`
              : transit && transit.transit_utc ? `${transit.grahas.length} grahas · ${transit.transit_utc}`
              : ''}
          </span>
        </div>
      )}
      {dignityOn && isD1 && (
        <div className="sw-dig-legend" aria-label={t('sw.dig.aria')}>
          {DIGNITY_LEGEND.map(([k, label]) => (
            <span key={k} className="sw-dig-key">
              <span className="sw-dig-sw" style={{ background: DIGNITY_COLOR[k] }} />{t(label)}
            </span>
          ))}
          <span className="sw-dig-note">
            {t('sw.dig.note')}
          </span>
        </div>
      )}
      <svg viewBox={`${C - HALF} ${C - HALF} ${2 * HALF} ${2 * HALF}`}
           className="sky-wheel" role="img"
           aria-label={t('sw.aria.title')}>
        {/* above / below the horizon */}
        {shade && (
          <>
            <path className="sw-sky" d={`M ${C - R_MAX},${C} A ${R_MAX},${R_MAX} 0 0 1 ${C + R_MAX},${C} Z`} />
            <path className="sw-earth" d={`M ${C - R_MAX},${C} A ${R_MAX},${R_MAX} 0 0 0 ${C + R_MAX},${C} Z`} />
          </>
        )}

        {/* invisible full-sector hit areas (under everything): hover/tap a sign's
            empty space raises the bhava card without touching glyph interactions */}
        {cardable && Array.from({ length: 12 }, (_, s) => (
          <path key={`hit${s}`} d={band(s * 30, 30, 48, R_MAX)} fill="transparent"
                pointerEvents="all" onPointerEnter={enter(s)} onClick={tap(s)} />
        ))}

        {/* rāśi bands (faint element tint) + boundaries */}
        {Array.from({ length: 12 }, (_, s) => {
          const lagnaBand = s === lagnaRasi
          const hi = s === highlightSign
          const el = ELEMENT[s % 4]
          return (
            <path key={`b${s}`} d={band(s * 30, 30, R_SIGN_IN, R_SIGN_OUT)}
                  onPointerEnter={cardable ? enter(s) : undefined}
                  onClick={cardable ? tap(s) : undefined}
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

        {/* rāśi names + rāśi numbers (Meṣa 1 … Mīna 12); the bhāva is named in
            the tooltip. */}
        {Array.from({ length: 12 }, (_, s) => {
          const [lx, ly] = pt(s * 30 + 15, R_SIGN_LABEL)
          const [bx, by] = pt(s * 30 + 15, R_BHAVA)
          return (
            <g key={`l${s}`}>
              <text x={lx} y={ly} className="sw-sign" textAnchor="middle" dominantBaseline="middle">{namer.rasi(s)}</text>
              <text x={bx} y={by} className="sw-bhava" textAnchor="middle" dominantBaseline="middle">
                <title>{`${namer.rasi(s)} — rāśi ${s + 1} · bhāva ${bhavaOf(s)}`}</title>{s + 1}
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

        {/* the lagna, pinned to the eastern horizon */}
        <g className="sw-asc">
          <polygon points={`${ascX - 12},${ascY - 6} ${ascX - 12},${ascY + 6} ${ascX - 2},${ascY}`} />
          <text x={ascX - 16} y={ascY - 8} textAnchor="end">
            <title>{`Lagna — ${namer.rasi(lagnaRasi)} ${(ascLon % 30).toFixed(2)}°`}</title>
            {namer.style === 'devanagari' ? 'लग्न' : 'Lagna'} {Math.floor(ascLon % 30)}°
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
              <title>{`${namer.grahaKey(active)} aspects ${namer.rasi(Number(s))} — ${{ 0.25: '¼', 0.5: '½', 0.75: '¾', 1: t('sw.drishti.full') }[v] ?? v}`}</title>
            </line>
          )
        })}

        {/* uccha / nīca landmarks: each graha's exact deep-exaltation and fall
            degrees (ch.3 vv.49–50), as rim ticks — uccha ▲ outward, nīca ▽ inward */}
        {dignityPoints.map((p, i) => {
          const isU = p.kind === 'uccha'
          const col = colors ? GRAHA_COLOR[p.key] : null
          const [cx, cy] = pt(p.lon, R_SIGN_IN - 11)
          const near = Math.abs(p.dist) < 1
          return (
            <g key={`uc${i}`} className={`sw-uccha ${isU ? 'up' : 'dn'}${near ? ' near' : ''}`}>
              <title>
                {`${namer.grahaKey(p.key)} — ${isU ? t('sw.tip.exaltation') : t('sw.tip.debilitation')} · ${namer.rasi(p.sign)} ${p.deg}°`}
                {near ? t('sw.tip.sits_on_it') : ''}
              </title>
              <polygon points={radialTri(p.lon, R_SIGN_IN, 6, 3.1, isU)}
                       style={col ? (isU ? { fill: col } : { stroke: col }) : undefined} />
              <text x={cx} y={cy} className="sw-uccha-code" textAnchor="middle" dominantBaseline="central"
                    style={col ? { fill: col } : undefined}>{CODE[p.key]}</text>
            </g>
          )
        })}

        {/* transit (gochara) overlay: an inner ghost ring of where the grahas
            stand now / at the chosen date, against the birth chart. Facts only —
            the good/bad transit reading is a separate, not-yet-built layer. */}
        {transitOn && isD1 && placedTransit.length > 0 && (
          <>
            <circle cx={C} cy={C} r={R_TRANSIT} className="sw-transit-ring" />

            {/* aspect lines for the hovered/pinned transit graha: from its inner-
                ring glyph to each natal point it aspects, weighted by ch.26 strength.
                Dimmed as a group while the natal-degree arc shares the hover. */}
            {hoverTransit && (
              <g className={`sw-taspect-group${returnShowing ? ' dim' : ''}`}>
                {hoverTransit.t.aspects_natal.map((a) => {
                  const dst = natalPos[a.target]
                  if (!dst) return null
                  const [ax, ay] = pt(hoverTransit.lon, hoverTransit.r)
                  const [bx, by] = pt(dst[0], dst[1])
                  const col = colors ? GRAHA_COLOR[hoverTransit.t.key] : null
                  return (
                    <line key={`ta${a.target}`} x1={ax} y1={ay} x2={bx} y2={by}
                          className={`sw-taspect${a.special ? ' special' : ''}`}
                          style={{ strokeOpacity: 0.25 + a.strength * 0.6, strokeWidth: 0.7 + a.strength * 1.9, ...(col ? { stroke: col } : {}) }}>
                      <title>
                        {`Transit ${namer.grahaKey(hoverTransit.t.key)}'s ${ordinal(a.house)} aspect`}
                        {a.special ? t('sw.tip.special_full') : ''}
                        {` on ${a.target === 'lagna' ? t('sw.tip.the_lagna') : namer.grahaKey(a.target)}`}
                      </title>
                    </line>
                  )
                })}
              </g>
            )}

            {/* conjunction highlight: the transit graha shares a sign with these
                natal points (yuti) — a connector ties them and the natal graha is
                ringed. Kept at full opacity, distinct from the graded aspect fan. */}
            {hoverTransit && hoverTransit.t.conjunct_natal.map((c) => {
              const dst = natalPos[c.key]
              if (!dst) return null
              const [ax, ay] = pt(hoverTransit.lon, hoverTransit.r)
              const [bx, by] = pt(dst[0], dst[1])
              const col = colors ? GRAHA_COLOR[hoverTransit.t.key] : null
              const isLagna = c.key === 'lagna'
              return (
                <g key={`tc${c.key}`} className="sw-tconj" style={{ pointerEvents: 'none' }}>
                  <title>
                    {`Transit ${namer.grahaKey(hoverTransit.t.key)} conjoins ${isLagna ? t('sw.tip.the_lagna') : namer.grahaKey(c.key)}`}
                    {c.arc != null ? ` — ${Math.abs(Math.round(c.arc))}° apart` : t('sw.tip.same_sign')}
                  </title>
                  <line x1={ax} y1={ay} x2={bx} y2={by} className="sw-tconj-line"
                        style={col ? { stroke: col } : undefined} />
                  {!isLagna && <circle cx={bx} cy={by} r="20" className="sw-tconj-ring"
                                       style={col ? { stroke: col } : undefined} />}
                </g>
              )
            })}

            {/* natal-degree offset (the Western "return", flagged as geometry not
                BPHS): the hovered slow graha's shortest-arc distance from its OWN
                natal degree, marker at the birth degree, arc ending at the glyph.
                Uses the SIGNED shortest arc so a retrograde body (the nodes always)
                draws the side it truly crossed, and never wraps a full circle. */}
            {hoverTransit && hoverTransit.t.return && SLOW_RETURN.has(hoverTransit.t.key) && (() => {
              const ret = hoverTransit.t.return
              const dist = ret.distance   // signed shortest arc, |dist| ≤ 180
              const col = colors ? GRAHA_COLOR[hoverTransit.t.key] : null
              const nr = ((ret.natal_longitude % 360) + 360) % 360
              const [nx, ny] = pt(nr, hoverTransit.r)
              const onIt = Math.abs(dist) < 2
              return (
                <g className={`sw-return${onIt ? ' near' : ''}`} style={{ pointerEvents: 'none' }}>
                  <path d={ringArc(nr, dist, hoverTransit.r)} className="sw-return-arc"
                        style={col ? { stroke: col } : undefined}>
                    <title>
                      {`Transit ${namer.grahaKey(hoverTransit.t.key)} — ${Math.round(Math.abs(dist))}° from its natal degree (${namer.rasi(Math.floor(nr / 30))} ${Math.floor(nr % 30)}°)`}
                      {onIt ? t('sw.tip.on_it_now') : ''}
                      {'\n' + t('sw.tip.return_geometry')}
                    </title>
                  </path>
                  <circle cx={nx} cy={ny} r="4.8" className="sw-return-natal"
                          style={col ? { stroke: col } : undefined} />
                </g>
              )
            })()}

            {placedTransit.map(({ t, lon, r }) => {
              const [px, py] = pt(lon, r)
              const col = colors ? GRAHA_COLOR[t.key] : null
              const combustT = t.combustion && t.combustion.combust
              const on = markedT === t.key
              const conj = (t.conjunct_natal || []).map((c) => c.key === 'lagna' ? 'the lagna' : namer.grahaKey(c.key))
              const asp = (t.aspects_natal || []).map((a) => a.target === 'lagna' ? 'the lagna' : namer.grahaKey(a.target))
              return (
                <g key={`t${t.key}`} className={`sw-tgraha${t.retrograde ? ' rx' : ''}${on ? ' on' : ''}`}
                   onPointerEnter={(e) => { if (e.pointerType !== 'touch') setHoverT(t.key) }}
                   onPointerLeave={(e) => { if (e.pointerType !== 'touch') setHoverT(null) }}
                   onClick={() => setPinT((cur) => cur === t.key ? null : t.key)}>
                  <title>
                    {`Transit ${namer.grahaKey(t.key)} — ${namer.rasi(t.rasi)} ${t.degree}°${pad2(t.minute)}'`}
                    {t.retrograde ? ' ℞' : ''}
                    {` · ${ordinal(t.house_from_moon)} from the natal Moon, ${ordinal(t.house_from_lagna)} from the lagna`}
                    {combustT ? ' · combust' : ''}
                    {conj.length ? ` · conjoins ${conj.join(', ')}` : ''}
                    {asp.length ? ` · aspects ${asp.join(', ')}` : ''}
                  </title>
                  {combustT && <circle cx={px} cy={py} r="11.5" className="sw-tcombust" />}
                  <circle cx={px} cy={py} r="9" className="sw-tdot" style={col ? { stroke: col } : undefined} />
                  <text x={px} y={py} className="sw-tglyph" textAnchor="middle" dominantBaseline="central"
                        style={col ? { fill: col } : undefined}>
                    {CODE[t.key]}{t.retrograde ? '℞' : ''}
                  </text>
                </g>
              )
            })}
          </>
        )}

        {/* grahas: ray to centre, exact-degree tick, staggered glyph */}
        {isD1 && placed.map(({ g, lon, r }) => {
          const [tx, ty] = pt(lon, R_SIGN_IN)
          const [tx2, ty2] = pt(lon, R_SIGN_IN - 7)
          const [px, py] = pt(lon, r)
          const on = active === g.key
          const col = colors ? GRAHA_COLOR[g.key] : null
          const combustSep = combust ? combust[g.key] : undefined
          const isCombust = combustSep != null
          return (
            <g key={g.key}
               className={`sw-graha${g.retrograde ? ' rx' : ''}${on ? ' active' : ''}`}
               onPointerEnter={() => onHover?.(g.key)}
               onPointerLeave={() => onHover?.(null)}
               onClick={() => onPin?.(g.key)}>
              <title>
                {`${g.name_en} — ${namer.rasi(g.rasi)} ${g.degree}°${pad2(g.minute)}'${pad2(g.second)}"`}
                {g.retrograde ? t('sw.tip.retrograde') : ''}{dignityPhrase(g.dignity, t)}
                {isCombust ? ` · combust (${combustSep}° from the Sun)` : ''}
              </title>
              <line x1={px} y1={py} x2={C} y2={C} className="sw-ray" style={col ? { stroke: col } : undefined} />
              <line x1={tx} y1={ty} x2={tx2} y2={ty2} className="sw-gtick" style={col ? { stroke: col } : undefined} />
              <line x1={tx2} y1={ty2} x2={px} y2={py} className="sw-glink" />
              {dignityOn && g.dignity && DIGNITY_COLOR[g.dignity.state] && (
                <circle cx={px} cy={py} r="15.5" className="sw-dignity"
                        style={{ fill: DIGNITY_COLOR[g.dignity.state] }} />
              )}
              {isCombust && <circle cx={px} cy={py} r="16.5" className="sw-combust" />}
              <circle cx={px} cy={py} r="13" className="sw-gdot" style={col ? { stroke: col } : undefined} />
              <text x={px} y={py} className="sw-gglyph" textAnchor="middle" dominantBaseline="central" style={col ? { fill: col } : undefined}>
                {((namer.style === 'devanagari' ? CODE_DEV[g.key] : CODE[g.key]) || g.name_en.slice(0, 2))}{g.retrograde ? '℞' : ''}
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
              <title>{md ? t('sw.dasha.md_lord') : t('sw.dasha.ad_lord')}</title>
              <circle cx={px} cy={py} r="18" className="sw-dasha-ring" />
              <text x={px} y={py - 21} className="sw-dasha-lbl" textAnchor="middle">{lbl}</text>
            </g>
          )
        })}

        {/* the native, at the centre */}
        <circle cx={C} cy={C} r="4" className="sw-center" />
        <text x={C} y={C + 20} className="sw-center-label" textAnchor="middle">{t('sw.center.native')}</text>

        {!isD1 && (
          <text x={C} y={C - 20} className="sw-note" textAnchor="middle">{t('sw.note.real_sky')}</text>
        )}
      </svg>
      {cardable && hovSign != null && (
        <BhavaHoverCard sign={hovSign} lagna={lagnaRasi} grahas={grahas} sticky={sticky}
                        vargaKey="D1" analysis={analysis} namer={namer}
                        transitHere={(transitOn && placedTransit.length ? placedTransit : [])
                          .filter((p) => Math.floor((((p.lon % 360) + 360) % 360) / 30) === hovSign)
                          .map((p) => (namer.grahaKey ? namer.grahaKey(p.t.key) : p.t.key) + (p.t.retrograde ? ' ℞' : ''))} />
      )}
      {dashaOn && isD1 && runningDasha && (
        <div className="sw-dasha-now" role="note">
          <span className="sw-dn-head">{t('sw.dn.head')}</span>
          <div className="sw-dn-rows">
            {runningDasha.levels.map((l) => (
              <span key={l.code} className="sw-dn-row">
                <span className="sw-dn-code" title={
                  l.code === 'MD' ? t('sw.dn.title.md') : l.code === 'AD' ? t('sw.dn.title.ad') : t('sw.dn.title.pd')
                }>{l.code}</span>
                <strong className="sw-dn-lord">{namer.grahaKey(l.lord)}</strong>
                <span className="sw-dn-rem" title={`${l.remaining} left`}>ends {l.ends}</span>
              </span>
            ))}
          </div>
          <span className="sw-dn-note">
            {t('sw.dn.note')}
          </span>
        </div>
      )}
    </div>
  )
}
