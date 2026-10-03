/**
 * The South Indian chart as the deck draws it — the fixed 4×4 grid in the
 * same construction as NorthDeckChart: gold grid, banner on the card's top
 * edge, serif sign labels with the English name beneath, planets as colour
 * discs with the glyph knocked out, the rāśi symbol where a cell is empty,
 * the lord's mark under every sign. Signs are fixed in this frame (Meṣa at
 * row 0 / col 1, clockwise); the lagna cell carries the traditional corner
 * stroke and a label, never a fill. The degree ruler stays at each cell's
 * floor on D1 — it is what this frame is for. No hover card: the bhāva texts
 * live in the deck's Houses card. Planet rows and lord marks select that
 * graha in the Casts card.
 */
import { SOUTH_CELLS, SignRuler } from './RasiChart.jsx'
import Glyph from './DashaGlyphs.jsx'
import LordMark, { lordPlacement } from './LordMark.jsx'

const RASI_SYMBOL = ['♈', '♉', '♊', '♋', '♌', '♍', '♎', '♏', '♐', '♑', '♒', '♓']

function groupBySign(grahas, vargaKey) {
  const bySign = Array.from({ length: 12 }, () => [])
  for (const g of grahas) bySign[g.vargas[vargaKey]].push(g)
  return bySign
}

export default function SouthDeckChart({
  grahas, lagnaRasi, vargaKey, lagnaVargaSign, namer, landmarks, lagnaLongitude, gandanta,
  active, onHover, onPick, highlightSign, title, subtitle, titleTip,
}) {
  const bySign = groupBySign(grahas, vargaKey)
  const lagna = vargaKey === 'D1' ? lagnaRasi : lagnaVargaSign
  const en = namer.style !== 'english'
  const ruled = vargaKey === 'D1' && !!landmarks
  const lagnaWord = namer.style === 'devanagari' ? 'लग्न' : 'Lagna'

  return (
    <div className="rc-card">
      <div className="rc-banner" title={titleTip}>
        <div className="rc-banner-title">{title}</div>
        {subtitle && <div className="rc-banner-sub">{subtitle}</div>}
      </div>
      <div className="sc-grid rasi-chart" role="img" aria-label="South Indian rāśi chart">
        <span className="rc-corner tl" aria-hidden="true" /><span className="rc-corner tr" aria-hidden="true" />
        <span className="rc-corner bl" aria-hidden="true" /><span className="rc-corner br" aria-hidden="true" />
        {SOUTH_CELLS.map((row, ri) =>
          row.map((sign, ci) => {
            if (sign === null) {
              if (ri === 1 && ci === 1) {
                return (
                  <div className="sc-centre" key="centre">
                    <div className="sc-centre-varga">{vargaKey}</div>
                    <div className="sc-centre-sub">{lagnaWord} {namer.rasi(lagna)}{en && <small> ({namer.rasiEnglish(lagna)})</small>}</div>
                  </div>
                )
              }
              return null
            }
            const occupants = bySign[sign]
            const lp = lordPlacement(sign, grahas, vargaKey, lagna)
            const bhava = ((sign - lagna + 12) % 12) + 1
            return (
              <div key={`${ri}-${ci}`}
                   className={`sc-cell${sign === lagna ? ' is-lagna' : ''}${highlightSign === sign ? ' dr-locate' : ''}${lp.own ? ' own' : ''}${occupants.length ? '' : ' empty'}`}
                   style={{ gridRow: ri + 1, gridColumn: ci + 1, '--g': `var(--pc-${lp.lord})` }}>
                {sign === lagna && <span className="sc-lagna" aria-hidden="true" />}
                {sign === lagna && <span className="sc-lagna-word">{lagnaWord}</span>}
                <div className="house-sign" title={`${namer.rasi(sign)} — rāśi ${sign + 1} · bhāva ${bhava}`}>
                  {sign + 1} · {namer.rasi(sign)}
                  {en && <small>({namer.rasiEnglish(sign)})</small>}
                </div>
                <LordMark sign={sign} grahas={grahas} vargaKey={vargaKey} lagna={lagna} namer={namer} size="n"
                          onClick={onPick ? () => onPick(lp.lord) : undefined} />
                <div className="sc-planets">
                  {occupants.map((g) => (
                    <div key={g.key} className={`planet${onPick ? ' pick' : ''}${active === g.key ? ' active' : ''}`}
                         style={{ '--g': `var(--pc-${g.key})` }}
                         title={`${g.name_en} — ${g.degree}°${String(g.minute).padStart(2, '0')}′${g.retrograde ? ' (retrograde)' : ''}`}
                         onPointerEnter={() => onHover?.(g.key)} onPointerLeave={() => onHover?.(null)}
                         onClick={onPick ? () => onPick(g.key) : undefined}>
                      <span className="planet-icon"><Glyph lord={g.key} size={16} /></span>
                      <span className="planet-name">{namer.graha(g)}</span>
                      {g.retrograde && <span className="retrograde">R</span>}
                      <span className="planet-deg">{g.degree}°</span>
                    </div>
                  ))}
                </div>
                {!occupants.length && (
                  <span className="house-glyph" aria-hidden="true">{RASI_SYMBOL[sign]}&#xFE0E;</span>
                )}
                {ruled && (
                  <SignRuler
                    sign={sign}
                    occupants={occupants}
                    landmarks={landmarks[sign]}
                    lagnaDegree={sign === lagna ? lagnaLongitude % 30 : null}
                    gandanta={gandanta}
                    active={active}
                    onHover={onHover}
                    onPin={onPick}
                  />
                )}
              </div>
            )
          }),
        )}
      </div>
    </div>
  )
}
