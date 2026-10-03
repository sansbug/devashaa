/**
 * The North Indian chart as the deck draws it — HTML house blocks positioned
 * over an SVG of gold lines, after the design's own stylesheet (.rasi-chart /
 * .house / .house-sign / .planet / .planet-icon). Type and icons scale with the
 * chart's width (container query units), so the proportions hold at any size.
 *
 * Same geometry and the same hover card as RasiChart's NorthIndianChart: the
 * SVG wedge polygons are the hit areas (the house blocks let pointer events
 * through), NORTH_REGIONS gives the centres, and a bhāva hover opens the same
 * BhavaHoverCard. The numeral in each house is the RĀŚI number; the bhāva is
 * the region's fixed position.
 */
import { NORTH_REGIONS, BhavaHoverCard, useBhavaHover } from './RasiChart.jsx'
import Glyph from './DashaGlyphs.jsx'
import LordMark, { lordPlacement } from './LordMark.jsx'

/** Per-region block width (% of the square) and a nudge for the side wedges,
 *  whose text anchor sits a little too close to the edge for an HTML block. */
const BLOCK = [
  { w: 38 }, { w: 30 }, { w: 19, cx: 40 }, { w: 38 }, { w: 19, cx: 40 }, { w: 30 },
  { w: 38 }, { w: 30 }, { w: 19, cx: 360 }, { w: 38 }, { w: 19, cx: 360 }, { w: 30 },
]
const RASI_SYMBOL = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓']

function groupBySign(grahas, vargaKey) {
  const bySign = Array.from({ length: 12 }, () => [])
  for (const g of grahas) bySign[g.vargas[vargaKey]].push(g)
  return bySign
}

export default function NorthDeckChart({
  grahas, lagnaRasi, vargaKey, lagnaVargaSign, namer, highlightSign, analysis, vargaSig,
  title, subtitle, titleTip,
}) {
  const bySign = groupBySign(grahas, vargaKey)
  const lagna = vargaKey === 'D1' ? lagnaRasi : lagnaVargaSign
  const hoverable = analysis && !analysis.error
  const { hovSign, sticky, rootRef, enter, leave, tap } = useBhavaHover(hoverable)
  const en = namer.style !== 'english'

  return (
    <div className="rc-card">
      <div className="rc-banner" title={titleTip}>
        <div className="rc-banner-title">{title}</div>
        {subtitle && <div className="rc-banner-sub">{subtitle}</div>}
      </div>
      <div className="rasi-chart north-wrap" ref={rootRef} onPointerLeave={leave}>
        <span className="rc-corner tl" aria-hidden="true" /><span className="rc-corner tr" aria-hidden="true" />
        <span className="rc-corner bl" aria-hidden="true" /><span className="rc-corner br" aria-hidden="true" />
        <svg viewBox="0 0 400 400" role="img" aria-label="North Indian bhāva chart">
          <rect x="1" y="1" width="398" height="398" className="chart-line" />
          <line x1="0" y1="0" x2="400" y2="400" className="chart-line" />
          <line x1="400" y1="0" x2="0" y2="400" className="chart-line" />
          <polygon points="200,0 400,200 200,400 0,200" className="chart-line" />
          {NORTH_REGIONS.map((r, i) => {
            const sign = (lagna + i) % 12
            const lp = lordPlacement(sign, grahas, vargaKey, lagna)
            return (
              <g key={i} onPointerEnter={hoverable ? enter(sign) : undefined} onClick={hoverable ? tap(sign) : undefined}>
                {/* The lord at home: the wedge takes a wash of the lord's colour. */}
                {lp.own && <polygon points={r.pts} className="own-fill" style={{ '--g': `var(--pc-${lp.lord})` }} />}
                <polygon points={r.pts} fill="transparent" pointerEvents="all" />
                {highlightSign === sign && <polygon points={r.pts} className="north-locate" />}
              </g>
            )
          })}
        </svg>
        {NORTH_REGIONS.map((r, i) => {
          const bhava = i + 1
          const sign = (lagna + i) % 12
          const occupants = bySign[sign]
          const b = BLOCK[i]
          const cx = b.cx ?? r.cx
          const lp = lordPlacement(sign, grahas, vargaKey, lagna)
          return (
            <div key={i} className={`house h${bhava}${occupants.length ? '' : ' empty'}`}
                 style={{ left: `${cx / 4}%`, top: `${r.cy / 4}%`, width: `${b.w}%` }}
                 title={`${namer.rasi(sign)} — rāśi ${sign + 1} · bhāva ${bhava}`}>
              <div className="house-sign">
                {sign + 1} · {namer.rasi(sign)}
                {en && <small>({namer.rasiEnglish(sign)})</small>}
              </div>
              <LordMark sign={sign} grahas={grahas} vargaKey={vargaKey} lagna={lagna} namer={namer} size="n" />
              {occupants.map((g) => (
                <div key={g.key} className="planet" style={{ '--g': `var(--pc-${g.key})` }}>
                  <span className="planet-icon"><Glyph lord={g.key} size={16} /></span>
                  <span className="planet-name">{namer.graha(g)}</span>
                  {g.retrograde && <span className="retrograde">R</span>}
                  <span className="planet-deg">{g.degree}°</span>
                </div>
              ))}
              {!occupants.length && (
                <span className="house-glyph" style={{ '--g': `var(--pc-${lp.lord})` }} aria-hidden="true">
                  {RASI_SYMBOL[sign]}&#xFE0E;
                </span>
              )}
            </div>
          )
        })}
        {hoverable && hovSign != null && (
          <BhavaHoverCard sign={hovSign} lagna={lagna} grahas={grahas} sticky={sticky}
                          vargaKey={vargaKey} analysis={analysis} namer={namer} vargaSig={vargaSig} />
        )}
      </div>
    </div>
  )
}
