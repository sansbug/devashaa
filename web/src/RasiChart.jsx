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

import { useEffect, useRef, useState } from 'react'
import CellRuler, { useRulerMode } from './CellRuler'
import { useLang } from './LangContext.jsx'

/**
 * Hover/tap state for the bhāva card. Mouse (or pen) hover previews transiently;
 * a tap/click PINS the card (sticky) — tap the same house again, or anywhere
 * outside the chart, to close. Touch never drives the transient path: on touch,
 * pointerenter fires on tap but pointerleave fires the instant the finger lifts,
 * so a hover-only card would flash and vanish on phones.
 */
function useBhavaHover(hoverable) {
  const [hov, setHov] = useState(null)          // { sign, sticky } | null
  const rootRef = useRef(null)
  useEffect(() => {
    if (!hov || !hov.sticky) return undefined
    const onDoc = (e) => {
      if (rootRef.current && !rootRef.current.contains(e.target)) setHov(null)
    }
    document.addEventListener('pointerdown', onDoc)
    return () => document.removeEventListener('pointerdown', onDoc)
  }, [hov])
  const enter = (sign) => (e) => {
    if (!hoverable || (e.pointerType !== 'mouse' && e.pointerType !== 'pen')) return
    setHov((h) => (h && h.sticky ? h : { sign, sticky: false }))
  }
  const leave = () => hoverable && setHov((h) => (h && h.sticky ? h : null))
  const tap = (sign) => () => {
    if (!hoverable) return
    setHov((h) => (h && h.sign === sign && h.sticky ? null : { sign, sticky: true }))
  }
  return { hovSign: hov ? hov.sign : null, sticky: !!(hov && hov.sticky), rootRef, enter, leave, tap }
}

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

// Rāśi index -> its lord's graha key, for the hover card's lord line.
const RASI_LORD = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury',
                   'venus', 'mars', 'jupiter', 'saturn', 'saturn', 'jupiter']

// Ch.26 vv.2-5 graded graha dṛṣṭi, sign-to-sign — the same table the server's
// drishti chart uses. Needed client-side ONLY for varga frames, where the D1
// aspect data would be the wrong frame; the seven planets cast, the nodes don't
// (matching the server default).
const DRISHTI_SPECIAL = { mars: [4, 8], jupiter: [5, 9], saturn: [3, 10] }
function drishtiFrac(graha, from, to) {
  const d = ((to - from + 12) % 12) + 1
  if (d === 7 || (DRISHTI_SPECIAL[graha] || []).includes(d)) return 1
  if (d === 4 || d === 8) return 0.75
  if (d === 5 || d === 9) return 0.5
  if (d === 3 || d === 10) return 0.25
  return 0
}
const DRISHTI_CASTERS = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn']

/**
 * Hover card for a bhāva on any chart. Everywhere: the house's BPHS ch.11
 * significations (house-generic), its nature, and its lord located in the SAME
 * varga. D1 additionally shows each occupant's dignity and cited classical
 * reading plus the server-computed ch.26 dṛṣṭi (rāśi-chart facts). Vargas show
 * occupants plainly and a sign-count dṛṣṭi recomputed in the varga's own frame,
 * labelled as an engine extension. Pointer-events none; never steals the hover.
 */
function BhavaHoverCard({ sign, lagna, grahas, vargaKey, analysis, namer, vargaSig, sticky }) {
  const { t } = useLang()
  if (sign == null || !analysis) return null
  const isD1 = vargaKey === 'D1'
  const bhava = bhavaOf(sign, lagna)
  const occ = grahas.filter((g) => g.vargas[vargaKey] === sign)
  const bp = analysis.bhava_phala && !analysis.bhava_phala.error
    ? (analysis.bhava_phala.bhavas || []).find((b) => b.house === bhava) : null
  const signif = bp && bp.significations
  let sigText = (signif && signif.text) || ''
  sigText = sigText.replace(/^[^:]*HOUSE[^:]*:\s*/i, '')
  const readings = (analysis.classical && analysis.classical.house_readings) || []
  let aspects
  if (isD1) {
    const recv = ((analysis.drishti || {}).graha || {}).received
    aspects = Object.entries((recv && recv.signs && recv.signs[sign]) || {})
      .sort((a, b) => b[1] - a[1])
  } else {
    // varga frame: same ch.26 sign-count, applied to THIS varga's signs.
    aspects = grahas
      .filter((g) => DRISHTI_CASTERS.includes(g.key) && g.vargas[vargaKey] !== sign)
      .map((g) => [g.key, drishtiFrac(g.key, g.vargas[vargaKey], sign)])
      .filter(([, f]) => f > 0)
      .sort((a, b) => b[1] - a[1])
  }
  const lordKey = RASI_LORD[sign]
  const lord = grahas.find((g) => g.key === lordKey)
  const kind = [[1, 4, 7, 10].includes(bhava) && 'kendra', [1, 5, 9].includes(bhava) && 'trikoṇa',
                [6, 8, 12].includes(bhava) && 'duḥsthāna'].filter(Boolean).join(' · ')
  const frac = (f) => (f >= 0.99 ? t('chart.full', 'full') : f >= 0.74 ? '¾' : f >= 0.49 ? '½' : '¼')
  const gistOf = (g) => {
    const r = readings.find((x) => x.graha === g.key && x.house === bhava)
    if (!r || !r.sources || !r.sources.length) return null
    const s = r.sources[0]
    let txt = (s.gist || '').replace(/^.*?bhava as\s*/i, '')
    if (txt.length > 200) txt = txt.slice(0, 200).replace(/[,;][^,;]*$/, '') + '…'
    const book = (s.source || {}).text || ''
    const cite = (s.citation || '').startsWith(book) ? (s.citation || '')
      : `${book} ${s.citation || ''}`.trim()
    return { txt, cite }
  }
  return (
    <div className="bhava-hover-card" aria-hidden="true">
      <div className="bhc-head"><b>{t('chart.bhava', 'Bhāva')} {bhava}</b> · {namer.rasi(sign)}
        {kind && <span className="bhc-kind"> · {kind}</span>}</div>
      {!isD1 && vargaSig && (
        <div className="bhc-line bhc-dim">{vargaKey} · {t('chart.readFor', 'read for')} {vargaSig}</div>
      )}
      {lord && <div className="bhc-line">{t('chart.lord', 'Lord')} {namer.grahaKey(lordKey)} — {t('chart.inBhava', 'in bhāva')} {bhavaOf(lord.vargas[vargaKey], lagna)}{!isD1 ? ` (${vargaKey})` : ''}</div>}
      {sigText && <div className="bhc-sig">{sigText} <span className="bhc-cite">— {(signif || {}).citation}</span></div>}
      {occ.length > 0 ? (
        <div className="bhc-sec">
          <div className="bhc-h">{t('chart.occupants', 'Occupants')}</div>
          {occ.map((g) => {
            const r = isD1 ? gistOf(g) : null
            return (
              <div key={g.key} className="bhc-occ">
                <b>{namer.graha(g)}{g.retrograde ? ' ℞' : ''}</b>
                {isD1 && g.dignity && DIGNITY_WORD[g.dignity.state] ? ` — ${DIGNITY_WORD[g.dignity.state]}` : ''}
                {r && <div className="bhc-gist">“{r.txt}” <span className="bhc-cite">— {r.cite}</span></div>}
              </div>
            )
          })}
        </div>
      ) : <div className="bhc-line bhc-dim">{t('chart.emptyHouse', 'No graha occupies this bhāva.')}</div>}
      {aspects.length > 0 && (
        <div className="bhc-sec">
          <div className="bhc-h">{t('chart.drishtiOn', 'Dṛṣṭi on this bhāva')}{!isD1 && <span className="bhc-kind"> · {vargaKey}</span>}</div>
          <div className="bhc-line">{aspects.map(([g, f]) => `${namer.grahaKey(g)} (${frac(f)})`).join(' · ')}</div>
          {!isD1 && <div className="bhc-cite">{t('chart.vargaDrishtiNote', 'ch.26 sign-count applied within this varga — an engine extension, not stated by the text')}</div>}
        </div>
      )}
      {sticky && <div className="bhc-cite">{t('chart.tapClose', 'tap the bhāva again — or anywhere outside — to close')}</div>}
      <div className="bhc-cite bhc-foot">BPHS ch.11 · ch.26 dṛṣṭi · {t('chart.hoverFoot', 'an indication, not fate')}</div>
    </div>
  )
}

function GrahaTag({ g, namer, active, onHover, onPin }) {
  return (
    <span className={`tag${g.retrograde ? ' rx' : ''}${active ? ' active' : ''}`}
          onPointerEnter={() => onHover?.(g.key)}
          onPointerLeave={() => onHover?.(null)}
          onClick={() => onPin?.(g.key)}
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
  gandanta, active, onHover, onPin, highlightSign, analysis, vargaSig,
}) {
  const bySign = groupBySign(grahas, vargaKey)
  const lagna = vargaKey === 'D1' ? lagnaRasi : lagnaVargaSign
  // House hover card on every varga; the card itself gates what is honest per frame.
  const hoverable = analysis && !analysis.error
  const { hovSign, sticky, rootRef, enter, leave, tap } = useBhavaHover(hoverable)

  // The ruler measures longitude WITHIN a sign, so it is meaningful only where
  // the cell's sign is the sign the graha is actually standing in — i.e. D1.
  // A varga sign is derived; there is no "degree into D9 Kanyā".
  const ruled = vargaKey === 'D1' && !!landmarks

  return (
    <div className="south-chart" role="img" aria-label="South Indian rāśi chart"
         ref={rootRef} onPointerLeave={leave}>
      {SOUTH_CELLS.map((row, ri) =>
        row.map((sign, ci) => {
          if (sign === null) {
            // The 2x2 hole in the middle — render once, as the label block.
            if (ri === 1 && ci === 1) {
              return (
                <div className="south-centre" key="centre">
                  <div className="centre-varga">{vargaKey}</div>
                  <div className="centre-sub">{namer.style === 'devanagari' ? 'लग्न' : 'Lagna'} {namer.rasi(lagna)}</div>
                </div>
              )
            }
            return null
          }
          return (
            <div
              className={`south-cell${sign === lagna ? ' is-lagna' : ''}`
                         + (highlightSign === sign ? ' dr-locate' : '')}
              key={`${ri}-${ci}`}
              style={{ gridRow: ri + 1, gridColumn: ci + 1 }}
              onPointerEnter={enter(sign)} onClick={tap(sign)}
            >
              {/* The numeral is the RĀŚI number (Meṣa 1 … Mīna 12), a fixed
                  property of the sign — not the bhāva. The bhāva (and its
                  kendra/trikoṇa/duḥsthāna nature) still decorates the numeral
                  and is named in the tooltip. */}
              <div className="cell-sign"
                   title={`${namer.rasi(sign)} — rāśi ${sign + 1} · bhāva ${bhavaOf(sign, lagna)}`}>
                <span className={bhavaClass(bhavaOf(sign, lagna))}>
                  {sign + 1}
                </span>
                <span className="cell-sep">·</span>
                {namer.rasi(sign)}
              </div>
              {sign === lagna && <div className="asc-mark">{namer.style === 'devanagari' ? 'लग्न' : 'Lagna'}</div>}
              <div className="cell-grahas">
                {bySign[sign].map((g) => (
                  <GrahaTag g={g} namer={namer} key={g.key}
                            active={active === g.key}
                            onHover={onHover} onPin={onPin} />
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
                  onHover={onHover}
                  onPin={onPin}
                />
              )}
            </div>
          )
        }),
      )}
      {hoverable && hovSign != null && (
        <BhavaHoverCard sign={hovSign} lagna={lagna} grahas={grahas} sticky={sticky}
                        vargaKey={vargaKey} analysis={analysis} namer={namer} vargaSig={vargaSig} />
      )}
    </div>
  )
}

export function NorthIndianChart({
  grahas, lagnaRasi, vargaKey, lagnaVargaSign, namer, highlightSign, analysis, vargaSig,
}) {
  const bySign = groupBySign(grahas, vargaKey)
  const lagna = vargaKey === 'D1' ? lagnaRasi : lagnaVargaSign
  const hoverable = analysis && !analysis.error
  const { hovSign, sticky, rootRef, enter, leave, tap } = useBhavaHover(hoverable)

  return (
    <div className="north-wrap" ref={rootRef} onPointerLeave={leave}>
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
          <g key={bhava} onPointerEnter={enter(sign)} onClick={tap(sign)}>
            {/* Invisible hit area so the whole wedge (not just painted glyphs)
                triggers the bhāva hover card. First child: text stays on top. */}
            {hoverable && (
              <polygon points={r.pts} fill="transparent" pointerEvents="all" />
            )}
            {/* Drawn AFTER the frame and BEFORE the text, so the locator can
                never overprint a graha name. No chords here, deliberately: the
                interior is already a rect plus both diagonals plus an inner
                diamond, and NORTH_REGIONS' cx/cy ARE the text anchors — a chord
                between centres would terminate on a label. */}
            {highlightSign === sign && (
              <polygon points={r.pts} className="north-locate" />
            )}
            <text x={r.cx} y={top} className="north-sign">
              {/* The numeral is the RĀŚI number (Meṣa 1 … Mīna 12); the bhāva is
                  given by the region's fixed position and named in the tooltip. */}
              <title>{`${namer.rasi(sign)} — rāśi ${sign + 1} · bhāva ${bhava}`}</title>
              <tspan className="north-bhava">{sign + 1}</tspan>
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
      {hoverable && hovSign != null && (
        <BhavaHoverCard sign={hovSign} lagna={lagna} grahas={grahas} sticky={sticky}
                        vargaKey={vargaKey} analysis={analysis} namer={namer} vargaSig={vargaSig} />
      )}
    </div>
  )
}
