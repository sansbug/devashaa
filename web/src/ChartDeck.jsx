/**
 * The chart deck — the cards that stand beside and beneath the rāśi chart:
 * planetary positions, key highlights, casts (graha dṛṣṭi), housewise planets,
 * and aspects (rāśi dṛṣṭi plus what the subject receives).
 *
 * Doctrine carried over from the ledger this replaces. Graha dṛṣṭi (BPHS ch.26
 * vv.2-5) is graded in four slabs and renders as a metered row with a written
 * fraction. Rāśi dṛṣṭi (ch.8 vv.1-5) is NOT graded and renders as bare chips —
 * no count, no meter, no number of any kind. The two are different element
 * types on purpose: there is no shared component with a `graded` flag that a
 * later edit could flip. The citations live in the card headers' tooltips, not
 * in the body — the deck is a figure, not a footnote.
 */
import { useState } from 'react'
import { useLang } from './LangContext.jsx'
import { Bubble } from './DashaGlyphs.jsx'
import { BhavaHoverCard } from './RasiChart.jsx'
import { lordPlacement } from './LordMark.jsx'

/** Written out, never as ¼ ½ ¾ — the vulgar-fraction glyphs draw their
 *  numerals at half height, and ¼ vs ¾ is the one thing a reader must tell apart. */
const FRACTION = { 0.25: '1/4', 0.5: '1/2', 0.75: '3/4', 1: 'drishti.fraction.full' }
const ORDINAL = ['', 'ordinal.1st', 'ordinal.2nd', 'ordinal.3rd', 'ordinal.4th',
                 'ordinal.5th', 'ordinal.6th', 'ordinal.7th', 'ordinal.8th',
                 'ordinal.9th', 'ordinal.10th', 'ordinal.11th', 'ordinal.12th']
/** Special full aspects, ch.26 vv.4-5 — named in the Casts header's tooltip. */
const SPECIAL = { saturn: [3, 10], jupiter: [5, 9], mars: [4, 8] }
const ORDER = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu']

const pad2 = (n) => String(n).padStart(2, '0')
/** Inclusive house distance, matching drishti.house_distance on the backend.
 *  Used ONLY to label a row we were given — never to decide an aspect. */
const houseDistance = (from, to) => ((to - from + 12) % 12) + 1
const bhavaOf = (sign, lagna) => ((sign - lagna + 12) % 12) + 1
const degOf = (g) => `${g.degree}°${pad2(g.minute)}′`

/** Four discrete blocks, never a continuous bar: BPHS gives four slabs. */
function Meter({ value }) {
  const filled = Math.round(value * 4)
  return (
    <span className="dk-meter" aria-hidden="true">
      {[1, 2, 3, 4].map((i) => <span key={i} className={`dk-sb${i <= filled ? ' on' : ''}`} />)}
    </span>
  )
}

function Card({ title, right, tip, children, className = '' }) {
  return (
    <section className={`dk-card ${className}`}>
      <h4 className="dk-head" title={tip}>
        <span>{title}</span>
        {right && <span className="dk-head-right">{right}</span>}
      </h4>
      <div className="dk-body">{children}</div>
    </section>
  )
}

function Planet({ g, namer, deg = false, size = 'm' }) {
  return (
    <span className="dk-planet">
      <Bubble lord={g.key} size={size} />
      <span>{namer.graha(g)}</span>
      {deg && <span className={`dk-deg${g.retrograde ? ' rx' : ''}`}> {deg === 'whole' ? `${g.degree}°` : degOf(g)}{g.retrograde ? ' ℞' : ''}</span>}
    </span>
  )
}

/** A nakṣatra's muhūrta class (the chart payload's `quality`, from api/nakshatra_attrs.py) grouped for colour. The
 *  classes are the tradition's; this three-way grouping is ours. It describes the nakṣatra, not the planet in it. */
const NAK_TONE = { Soft: 'good', Light: 'good', Fixed: 'good', Mixed: 'mixed', Mutable: 'mixed', Fierce: 'hard', Sharp: 'hard' }
const ORDER_KEY = 'deck.positions.order'
const loadOrder = () => { try { return localStorage.getItem(ORDER_KEY) === 'houses' ? 'houses' : 'planets' } catch { return 'planets' } }
/** Rounded to the minute with the carry, as a graha's degree in its sign is. */
const degMin = (d) => { const m = Math.round(d * 60); return `${Math.floor(m / 60)}°${pad2(m % 60)}′` }

function NakCells({ g, namer }) {
  const { t } = useLang()
  const n = g.nakshatra
  return (
    <>
      <td className={`dk-nak ${NAK_TONE[n.quality] || ''}`}>
        {namer.nakshatra(n)}
        {n.quality && <small>{t(`deck.nak.${n.quality}`, n.quality)}</small>}
      </td>
      <td className="dk-num">{n.pada}</td>
      <td className="dk-num">{degMin(n.degrees_in)}</td>
    </>
  )
}

function SignCell({ sign, namer, rowSpan }) {
  return (
    <td rowSpan={rowSpan}>
      {namer.rasi(sign)}
      {namer.style !== 'english' && <span className="dk-en">{namer.rasiEnglish(sign)}</span>}
    </td>
  )
}

/** Planetary positions: by planet, or by house from the 1st to the 12th (empty houses included, so it always starts
 *  at the 1st). A house's planets stand in the order they fall in its sign. */
function PositionsCard({ ordered, lagna, namer, onHoverSign }) {
  const { t } = useLang()
  const [order, setOrderState] = useState(loadOrder)
  const setOrder = (k) => { setOrderState(k); try { localStorage.setItem(ORDER_KEY, k) } catch { /* private mode */ } }
  const hover = (sign) => ({ onPointerEnter: () => onHoverSign?.(sign), onPointerLeave: () => onHoverSign?.(null) })
  const degree = (x) => <td className={`dk-num${x.retrograde ? ' rx' : ''}`}>{degOf(x)}{x.retrograde ? ' ℞' : ''}</td>
  const nakHead = <><th>{t('deck.nakshatra', 'Nakṣatra')}</th><th>{t('deck.pada.head', 'Pāda')}</th><th>{t('deck.nakdeg', 'In nak.')}</th></>
  const toggle = (
    <span className="dk-order" role="group" aria-label={t('deck.order', 'Start the table with')}>
      {[['planets', t('deck.order.planets', 'Planets')], ['houses', t('deck.order.houses', 'Houses 1–12')]].map(([k, label]) => (
        <button type="button" key={k} className={order === k ? 'on' : ''} aria-pressed={order === k} onClick={() => setOrder(k)}>{label}</button>
      ))}
    </span>
  )
  return (
    <Card title={t('deck.positions', 'Planetary Positions')} right={toggle} tip={t('deck.positions.tip', 'Sidereal (Lahiri) longitudes; houses are whole-sign bhāvas from the lagna. Nakṣatra classes: the muhūrta tradition’s seven (traditional tier).')}>
      <table className="dk-table dk-pos">
        {order === 'planets' ? (
          <>
            <thead><tr><th>{t('deck.planet', 'Planet')}</th><th>{t('deck.sign', 'Sign (Rāśi)')}</th><th>{t('deck.degree', 'Degree')}</th><th>{t('deck.house', 'House')}</th>{nakHead}</tr></thead>
            <tbody>
              {ordered.map((x) => (
                <tr key={x.key} {...hover(x.rasi)}>
                  <td><Planet g={x} namer={namer} size="s" /></td>
                  <SignCell sign={x.rasi} namer={namer} />
                  {degree(x)}
                  <td className="dk-num">{t(ORDINAL[bhavaOf(x.rasi, lagna)])}</td>
                  <NakCells g={x} namer={namer} />
                </tr>
              ))}
            </tbody>
          </>
        ) : (
          <>
            <thead><tr><th>{t('deck.house', 'House')}</th><th>{t('deck.sign', 'Sign (Rāśi)')}</th><th>{t('deck.planet', 'Planet')}</th><th>{t('deck.degree', 'Degree')}</th>{nakHead}</tr></thead>
            <tbody>
              {Array.from({ length: 12 }, (_, i) => {
                const h = i + 1, sign = (lagna + i) % 12
                const occ = ordered.filter((x) => bhavaOf(x.rasi, lagna) === h).sort((a, b) => a.longitude - b.longitude)
                if (!occ.length) {
                  return (
                    <tr key={h} className="dk-empty" {...hover(sign)}>
                      <td className="dk-num dk-h">{t(ORDINAL[h])}</td>
                      <SignCell sign={sign} namer={namer} />
                      <td colSpan={5}>—</td>
                    </tr>
                  )
                }
                return occ.map((x, k) => (
                  <tr key={x.key} {...hover(sign)}>
                    {k === 0 && <td className="dk-num dk-h" rowSpan={occ.length}>{t(ORDINAL[h])}</td>}
                    {k === 0 && <SignCell sign={sign} namer={namer} rowSpan={occ.length} />}
                    <td><Planet g={x} namer={namer} size="s" /></td>
                    {degree(x)}
                    <NakCells g={x} namer={namer} />
                  </tr>
                ))
              })}
            </tbody>
          </>
        )}
      </table>
      <p className="dk-note dk-nak-key">
        <span className="dk-nak good">{t('deck.nak.good', 'Soft, light or fixed')}</span>
        {' · '}<span className="dk-nak mixed">{t('deck.nak.mixed', 'Mixed or mutable')}</span>
        {' · '}<span className="dk-nak hard">{t('deck.nak.hard', 'Fierce or sharp')}</span>
        <small>{t('deck.nak.note', 'The colour is the class of the nakṣatra itself in the muhūrta tradition, not of the planet standing in it.')}</small>
      </p>
    </Card>
  )
}

export default function ChartDeck({
  chart, drishti, grahas, namer, subject, onPickSubject, onHoverSign, varga, analysis, vargaSig,
}) {
  const { t } = useLang()
  const lagna = chart.lagna_rasi
  // The frame's own lagna: D1's, or the varga's derived one.
  const vLagna = varga === 'D1' ? lagna : (chart.lagna_vargas?.[varga] ?? lagna)
  const ordered = [...grahas].sort((a, b) => ORDER.indexOf(a.key) - ORDER.indexOf(b.key))
  const bySign = {}
  for (const x of grahas) (bySign[x.rasi] ||= []).push(x)
  const sun = grahas.find((x) => x.key === 'sun')
  const moon = grahas.find((x) => x.key === 'moon')
  const lagnaDeg = chart.lagna_longitude != null ? chart.lagna_longitude % 30 : null

  const d1 = varga === 'D1' && drishti
  const g = d1 ? drishti.graha : null
  const r = d1 ? drishti.rasi : null
  const casts = g ? g.casts[subject] : null
  // The subject's sign comes from the chart, not from the casts table — the
  // nodes are absent there as ASPECTORS but still stand in a sign.
  const subjSign = grahas.find((x) => x.key === subject)?.rasi ?? casts?.from_sign
  const received = g ? (g.received?.signs?.[String(subjSign)] ?? {}) : {}
  const isNode = subject === 'rahu' || subject === 'ketu'
  const subjName = namer.grahaKey(subject)

  const castsTip = [g?.citation, SPECIAL[subject] && `${subjName}: ${t('deck.special', 'special full aspect on the')} ${SPECIAL[subject].map((h) => t(ORDINAL[h])).join(' & ')}`].filter(Boolean).join(' · ')
  const aspectsTip = [r?.citation, r?.ungraded_note, ...(r?.notes || [])].filter(Boolean).join(' · ')

  const unavailable = (
    <p className="dk-note">{t('deck.unavailable', 'Dṛṣṭi is counted from the sign a graha actually stands in — switch to D1.')}</p>
  )

  const picker = (
    <div className="dk-picker" role="tablist" aria-label={t('deck.casts', 'Casts (Strengths)')}>
      {ordered.map((x) => (
        <button type="button" key={x.key} role="tab" aria-selected={subject === x.key}
                className={`dk-pick${subject === x.key ? ' on' : ''}`} style={{ '--g': `var(--pc-${x.key})` }}
                onClick={() => onPickSubject(x.key)} title={namer.graha(x)}>
          <Bubble lord={x.key} size="m" />
          <span className="dk-pick-name">{namer.graha(x)}</span>
        </button>
      ))}
    </div>
  )

  return (
    <>
      <div className="deck-side">
        {/* ── Planetary positions ─────────────────────────────────── */}
        <PositionsCard ordered={ordered} lagna={lagna} namer={namer} onHoverSign={onHoverSign} />

        {/* ── Key highlights — placements only; no trait sentences (uncited) ── */}
        <Card title={t('deck.highlights', 'Key Highlights')} className="dk-hl-card">
          <div className="dk-hl">
            <span className="dk-rbub" aria-hidden="true">{lagna + 1}</span>
            <span className="dk-hl-title">{t('deck.ascendant', 'Ascendant (Lagna)')}</span>
            <span className="dk-hl-text">
              <b>{namer.rasi(lagna)}</b>{namer.style !== 'english' && <span className="dk-en"> ({namer.rasiEnglish(lagna)})</span>}{lagnaDeg != null && <> — {Math.floor(lagnaDeg)}°{pad2(Math.floor((lagnaDeg % 1) * 60))}′</>}
              {chart.lagna_nakshatra && <i>{namer.nakshatra(chart.lagna_nakshatra)} · {t('deck.pada', 'pada')} {chart.lagna_nakshatra.pada}</i>}
            </span>
          </div>
          {moon && (
            <div className="dk-hl">
              <span className="dk-rbub" aria-hidden="true">{moon.rasi + 1}</span>
              <span className="dk-hl-title">{t('deck.moonsign', 'Moon Sign (Rāśi)')}</span>
              <span className="dk-hl-text">
                <b>{namer.rasi(moon.rasi)}</b>{namer.style !== 'english' && <span className="dk-en"> ({namer.rasiEnglish(moon.rasi)})</span>} — <Planet g={moon} namer={namer} deg size="s" />
                {moon.nakshatra && <i>{namer.nakshatra(moon.nakshatra)} · {t('deck.pada', 'pada')} {moon.nakshatra.pada}</i>}
              </span>
            </div>
          )}
          {sun && (
            <div className="dk-hl">
              <span className="dk-rbub" aria-hidden="true">{sun.rasi + 1}</span>
              <span className="dk-hl-title">{t('deck.sunsign', 'Sun Sign')}</span>
              <span className="dk-hl-text">
                <b>{namer.rasi(sun.rasi)}</b>{namer.style !== 'english' && <span className="dk-en"> ({namer.rasiEnglish(sun.rasi)})</span>} — <Planet g={sun} namer={namer} deg size="s" />
                {sun.nakshatra && <i>{namer.nakshatra(sun.nakshatra)} · {t('deck.pada', 'pada')} {sun.nakshatra.pada}</i>}
              </span>
            </div>
          )}
        </Card>

        {/* ── Casts — ch.26, GRADED ──────────────────────────────── */}
        <Card title={t('deck.casts', 'Casts (Strengths)')} tip={castsTip || undefined}
              right={(
                <span className="dk-legend" aria-hidden="true">
                  {[[0.25, '1/4'], [0.5, '1/2'], [0.75, '3/4'], [1, t('drishti.fraction.full', 'Full')]].map(([v, l]) => (
                    <span key={l}><Meter value={v} /> = {l}</span>
                  ))}
                </span>
              )}>
          {d1 ? (
            <>
              {picker}
              {isNode ? (
                <p className="dk-note">{t('deck.nodeNote', 'No graha dṛṣṭi is cast by')} {subjName}.</p>
              ) : (
                <table className="dk-table dk-casts">
                  <thead><tr><th>{t('deck.house', 'House')}</th><th>{t('deck.planet', 'Planet')}</th><th>{t('deck.strength', 'Strength')}</th></tr></thead>
                  <tbody>
                    {Object.entries(casts?.signs ?? {})
                      .map(([s, v]) => [Number(s), v])
                      .sort((a, b) => houseDistance(subjSign, a[0]) - houseDistance(subjSign, b[0]))
                      .map(([s, v]) => {
                        const occ = (bySign[s] ?? []).map((o) => {
                          const back = g.casts[o.key]?.grahas?.[subject]
                          return `${namer.graha(o)}${back ? ` (${t('deck.returns', 'returns')} ${t(FRACTION[back])})` : ''}`
                        })
                        return (
                          <tr key={s} onPointerEnter={() => onHoverSign?.(s)} onPointerLeave={() => onHoverSign?.(null)}>
                            <td className="dk-num">{t(ORDINAL[houseDistance(subjSign, s)])}</td>
                            <td><b>{namer.rasi(s)}</b>{occ.length ? <span className="dk-en"> · {occ.join(', ')}</span> : null}</td>
                            <td><span className="dk-strength"><Meter value={v} /><b>{t(FRACTION[v] ?? String(v))}</b></span></td>
                          </tr>
                        )
                      })}
                  </tbody>
                </table>
              )}
            </>
          ) : unavailable}
        </Card>
      </div>

      <div className="deck-under">
        {/* ── Houses — the bhāva texts that used to be the chart's hover card ── */}
        <Card title={t('deck.houses', 'Houses (Bhāvas)')} className="dk-houses"
              tip={t('deck.houses.tip', 'BPHS ch.11 significations, the lord’s place, each occupant’s dignity and cited reading, and the dṛṣṭi on the house (ch.26).')}>
          {Array.from({ length: 12 }, (_, i) => {
            const sign = (vLagna + i) % 12
            const occ = grahas.filter((x) => x.vargas?.[varga] === sign)
            const lp = lordPlacement(sign, grahas, varga, vLagna)
            return (
              <details key={i} className="dk-house" open={i === 0}
                       onPointerEnter={() => onHoverSign?.(sign)} onPointerLeave={() => onHoverSign?.(null)}>
                <summary>
                  <span className="dk-house-n">{t(ORDINAL[i + 1])}</span>
                  <b>{namer.rasi(sign)}</b>{namer.style !== 'english' && <span className="dk-en"> ({namer.rasiEnglish(sign)})</span>}
                  <span className="dk-house-occ">{occ.length ? occ.map((x) => <Bubble key={x.key} lord={x.key} size="s" />) : <span className="dk-en">—</span>}</span>
                  {lp.at != null && <span className="dk-house-lord" style={{ '--g': `var(--pc-${lp.lord})` }}><Bubble lord={lp.lord} size="s" /> {lp.own ? t('deck.own', 'own') : `→ ${lp.bhava}`}</span>}
                </summary>
                {analysis ? (
                  <BhavaHoverCard sign={sign} lagna={vLagna} grahas={grahas} vargaKey={varga} analysis={analysis} namer={namer} vargaSig={vargaSig} sticky={false} />
                ) : <p className="dk-note">{t('deck.houses.none', 'The analysis is not available for this chart.')}</p>}
              </details>
            )
          })}
        </Card>

        {/* ── Aspects — rāśi dṛṣṭi (ch.8, UNGRADED) + what the subject receives ── */}
        <Card title={t('deck.aspects', 'Aspects (Drishti)')} tip={aspectsTip || undefined}>
          {d1 ? (
            <>
              <div className="dk-asp-row">
                <Bubble lord={subject} size="m" />
                <span className="dk-asp-text">
                  <b>{namer.rasi(subjSign)}</b> ↔{' '}
                  {(r.sign_table?.[String(subjSign)] ?? []).map((s) => (
                    <span key={s} className="dk-chip"
                          onPointerEnter={() => onHoverSign?.(s)} onPointerLeave={() => onHoverSign?.(null)}>
                      {namer.rasi(s)}
                    </span>
                  ))}
                  <i className="dk-mutual">{t('drishti.rasi.alwaysMutual', 'always mutual')}</i>
                </span>
              </div>
              {Object.keys(received).length === 0 ? (
                <p className="dk-note">{t('deck.noneReceived', 'No graha aspects')} {namer.rasi(subjSign)}.</p>
              ) : (
                Object.entries(received).map(([k, v]) => {
                  const from = g.casts[k]?.from_sign
                  // The count MUST be the aspector's, labelled as theirs: Śani's
                  // 3rd counted backwards is an 11th, and ch.26 has no 11th aspect.
                  const h = from === undefined ? null : houseDistance(from, subjSign)
                  return (
                    <div key={k} className="dk-asp-row" onPointerEnter={() => onHoverSign?.(from)} onPointerLeave={() => onHoverSign?.(null)}>
                      <Bubble lord={k} size="m" />
                      <span className="dk-asp-text">
                        <b>{namer.grahaKey(k)}{h ? `’s ${t(ORDINAL[h])}` : ''}</b> → {t('deck.from', 'from')} {namer.rasi(from)} <span className="dk-strength dk-inline"><Meter value={v} /><b>{t(FRACTION[v] ?? String(v))}</b></span>
                      </span>
                    </div>
                  )
                })
              )}
              <p className="dk-note dk-asym">{t('drishti.received.asymNote')}</p>
            </>
          ) : unavailable}
        </Card>
      </div>
    </>
  )
}
