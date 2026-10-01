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
import { useLang } from './LangContext.jsx'
import { Bubble } from './DashaGlyphs.jsx'

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

export default function ChartDeck({
  chart, drishti, grahas, namer, subject, onPickSubject, onHoverSign, varga,
}) {
  const { t } = useLang()
  const lagna = chart.lagna_rasi
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
                className={`dk-pick${subject === x.key ? ' on' : ''}`} style={{ '--g': `var(--gr-${x.key})` }}
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
        <Card title={t('deck.positions', 'Planetary Positions')} tip={t('deck.positions.tip', 'Sidereal (Lahiri) longitudes; houses are whole-sign bhāvas from the lagna.')}>
          <table className="dk-table">
            <thead><tr><th>{t('deck.planet', 'Planet')}</th><th>{t('deck.sign', 'Sign (Rāśi)')}</th><th>{t('deck.degree', 'Degree')}</th><th>{t('deck.house', 'House')}</th></tr></thead>
            <tbody>
              {ordered.map((x) => (
                <tr key={x.key} onPointerEnter={() => onHoverSign?.(x.rasi)} onPointerLeave={() => onHoverSign?.(null)}>
                  <td><Planet g={x} namer={namer} /></td>
                  <td>{namer.rasi(x.rasi)}{namer.style !== 'english' && <span className="dk-en"> ({namer.rasiEnglish(x.rasi)})</span>}</td>
                  <td className={`dk-num${x.retrograde ? ' rx' : ''}`}>{degOf(x)}{x.retrograde ? ' ℞' : ''}</td>
                  <td className="dk-num">{t(ORDINAL[bhavaOf(x.rasi, lagna)])}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </Card>

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
        {/* ── Housewise planets ─────────────────────────────────── */}
        <Card title={t('deck.housewise', 'Housewise Planets')}>
          <table className="dk-table dk-housewise">
            <thead><tr><th>{t('deck.house', 'House')}</th><th>{t('deck.sign', 'Sign')}</th><th>{t('deck.planets', 'Planet(s)')}</th></tr></thead>
            <tbody>
              {Array.from({ length: 12 }, (_, i) => {
                const sign = (lagna + i) % 12
                const occ = bySign[sign] ?? []
                return (
                  <tr key={i} onPointerEnter={() => onHoverSign?.(sign)} onPointerLeave={() => onHoverSign?.(null)}>
                    <td className="dk-num">{t(ORDINAL[i + 1])}</td>
                    <td>{namer.rasi(sign)}{namer.style !== 'english' && <span className="dk-en"> ({namer.rasiEnglish(sign)})</span>}</td>
                    <td className="dk-occ">{occ.length ? occ.map((x) => <Planet key={x.key} g={x} namer={namer} deg="whole" size="s" />) : <span className="dk-en">—</span>}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
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
