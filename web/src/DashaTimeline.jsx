/**
 * Daśā timeline — a life laid out end to end, with today marked.
 *
 * THE SCALE PROBLEM, AND WHY THIS IS A ZOOM STACK
 * -----------------------------------------------
 * A Viṁśottarī cycle is 120 years. A pratyantardaśā inside it can be ten weeks.
 * That is a ratio of about 600:1, so a single proportional axis cannot hold
 * both — at any width where the whole life is legible, a pratyantar is a
 * sub-pixel sliver, and at any width where the pratyantar is legible the life
 * is metres long.
 *
 * So there are three rails, each one a full-width expansion of a single band
 * from the rail above:
 *
 *   MAHĀ        [────Sūrya────][──────Chandra──────][───Maṅgala───] …  118 yrs
 *   ANTAR         the selected mahā, re-spread across the full width
 *   PRATYANTAR    the selected antar, re-spread across the full width
 *
 * Every rail is internally proportional and honest; what changes between rails
 * is only which span the width represents. A funnel under each rail shows which
 * band was expanded, so the zoom is never implicit.
 *
 * ON COLOUR
 * ---------
 * The colouring is supplied by the caller, per lord, and each entry must carry
 * its own citation. This component deliberately owns no opinion about whether a
 * daśā is good or bad — see the legend text in DashaTimeline's parent. A band
 * with no verdict renders neutral, and neutral is a real state here rather than
 * a fallback.
 *
 * Planet identity therefore rides on the GLYPH, never on the fill. Tinting
 * bands by graha would look livelier and would quietly overwrite the only thing
 * the fill is allowed to mean.
 *
 * ON AGE
 * ------
 * Age is computed from the BIRTH instant, never from `mahadashas[0].start`.
 * The first mahādaśā's start is *notional* — it precedes birth by the elapsed
 * part of the janma nakṣatra (see vimshottari.build_vimshottari), here by about
 * three years. Reading age off the rail's left edge overstates it by exactly
 * that much, on every age shown.
 */

import { useEffect, useMemo, useState } from 'react'
import { useLang } from './LangContext.jsx'
import Glyph from './DashaGlyphs.jsx'

const DAY = 86400000
const YEAR = 365.2425 * DAY

const parse = (s) => new Date(s.replace(' ', 'T')).getTime()
const yearOf = (t) => new Date(t).getFullYear()

/** Duration in a form that stays readable from decades down to weeks. */
function span(ms) {
  const d = ms / DAY
  if (d >= 365) return `${(d / 365.25).toFixed(d / 365.25 < 10 ? 1 : 0)}y`
  if (d >= 31) return `${Math.round(d / 30.44)}m`
  return `${Math.round(d)}d`
}

/** Long form, for the "time remaining" readout: "2 years 4 months", "17 days". */
function longSpan(ms, t) {
  if (ms <= 0) return t('dtl.rem.ended')
  const d = Math.floor(ms / DAY)
  const y = Math.floor(d / 365.25)
  const m = Math.floor((d - y * 365.25) / 30.44)
  const parts = []
  if (y) parts.push(`${y}${t('dtl.unit.y')}`)
  if (m) parts.push(`${m}${t('dtl.unit.m')}`)
  if (!y && !m) parts.push(`${d}${t('dtl.unit.d')}`)
  return parts.join(' ')
}

function fmtDate(t) {
  const d = new Date(t)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

/**
 * Axis ticks that suit the rail's own span. The life rail wants decades; a
 * two-year antardaśā wants quarters. One fixed granularity makes two of the
 * three rails useless, which is why the old build only ticked the top one.
 */
function ticks(t0, t1) {
  const years = (t1 - t0) / YEAR
  const out = []
  const push = (d) => {
    const t = d.getTime()
    if (t > t0 && t < t1) out.push(t)
  }
  if (years > 40) {
    for (let y = Math.ceil(yearOf(t0) / 10) * 10; y <= yearOf(t1); y += 10) push(new Date(y, 0, 1))
  } else if (years > 12) {
    for (let y = Math.ceil(yearOf(t0) / 5) * 5; y <= yearOf(t1); y += 5) push(new Date(y, 0, 1))
  } else if (years > 4) {
    for (let y = yearOf(t0); y <= yearOf(t1); y += 2) push(new Date(y, 0, 1))
  } else if (years > 1.5) {
    for (let y = yearOf(t0); y <= yearOf(t1); y += 1) push(new Date(y, 0, 1))
  } else {
    const d = new Date(t0)
    d.setDate(1)
    d.setMonth(Math.ceil(d.getMonth() / 3) * 3)
    while (d.getTime() < t1) {
      push(new Date(d))
      d.setMonth(d.getMonth() + 3)
    }
  }
  return out
}

/** Short tick label: a bare year where the span is years, else "Mon YYYY". */
function tickLabel(t, years) {
  const d = new Date(t)
  if (years > 1.5) return String(d.getFullYear())
  return d.toLocaleString(undefined, { month: 'short' }) + ' ' + d.getFullYear()
}

/**
 * One rail. Bands are proportional within [t0, t1] — the rail's own span, not
 * the whole life — which is what makes a ten-week pratyantar readable.
 */
function Rail({
  nodes, level, namer, verdictOf, conditionsOf, now, selected, onSelect, label, sub, step,
}) {
  const { t } = useLang()
  if (!nodes?.length) return null
  const t0 = parse(nodes[0].start)
  const t1 = parse(nodes[nodes.length - 1].end)
  const years = (t1 - t0) / YEAR
  const pct = (x) => ((x - t0) / (t1 - t0)) * 100
  const nowInRail = now >= t0 && now <= t1

  return (
    <div className="dt-rail">
      <div className="dt-rail-head">
        <span className="dt-step" aria-hidden="true">{step}</span>
        <span className="dt-rail-titles">
          <span className="dt-rail-label">{label}</span>
          {sub && <span className="dt-rail-sub">{sub}</span>}
        </span>
        <span className="dt-rail-span">
          {fmtDate(t0)} → {fmtDate(t1)}
          <span className="dt-rail-dur"> ({span(t1 - t0)})</span>
        </span>
      </div>

      <div className="dt-track">
        {nodes.map((n, i) => {
          const a = parse(n.start), b = parse(n.end)
          const v = verdictOf?.(n.lord)
          const cond = conditionsOf?.(n.lord)
          const past = b < now
          const running = a <= now && now < b
          const w = pct(b) - pct(a)
          return (
            <button
              type="button"
              key={i}
              className={`dt-band${running ? ' running' : ''}${past ? ' past' : ''}`
                + (selected === i ? ' selected' : '')
                + (v ? ` v-${v.state}` : '')
                + (w < 4 ? ' narrow' : '')}
              style={{ left: `${pct(a)}%`, width: `${w}%` }}
              onClick={() => onSelect?.(i)}
              aria-pressed={selected === i}
              /* The tooltip carries the CONDITIONS, not just the verdict. A
                 reader must be able to check the label against the verse
                 rather than take it on trust — and for `contested` both sides
                 have to be visible, since the whole point is that BPHS states
                 both and arbitrates neither. */
              title={`${namer.grahaKey(n.lord)} — ${fmtDate(a)} → ${fmtDate(b)} (${span(b - a)})`
                     + (v ? `\n\n${v.label.toUpperCase()} — ${v.citation}`
                          + (v.favourable?.length
                              ? `\n${t('dtl.tip.favourable')} ${v.favourable.map((c) => c.condition).join('; ')}`
                              : '')
                          + (v.adverse?.length
                              ? `\n${t('dtl.tip.adverse')} ${v.adverse.map((c) => c.condition).join('; ')}`
                              : '')
                          + (v.silent
                              ? '\n' + t('dtl.tip.silent')
                              : '')
                        : '')
                     + (cond
                        ? `\n\n${cond.chapter} — ${cond.counts.fired} ${t('dtl.tip.of')} ${cond.counts.total}`
                          + ' ' + t('dtl.tip.conditions_fire')
                          + (cond.counts.unavailable
                              ? `, ${cond.counts.unavailable} cannot be evaluated`
                              : '')
                          + (cond.fired?.length
                              ? '\n' + cond.fired
                                  .map((f) => '· ' + (f.reading || f.predicate))
                                  .join('\n')
                              : '')
                        : '')}
            >
              <Glyph lord={n.lord} size={15} />
              <span className="dt-band-lord">{namer.grahaKey(n.lord)}</span>
              <span className="dt-band-dur">{span(b - a)}</span>
              {/* Presence, not verdict. ch.52-60 name conditions that fire in
                  this cell; the count says how many, and how many could not be
                  evaluated at all. It is never a colour. */}
              {cond && (cond.counts.fired > 0 || cond.counts.unavailable > 0) && (
                <span className="dt-cond" aria-hidden="true">
                  {cond.counts.fired > 0 && <span className="dt-cond-n">{cond.counts.fired}</span>}
                  {cond.counts.unavailable > 0 && <span className="dt-cond-u">⊘</span>}
                </span>
              )}
            </button>
          )
        })}
        {/* Today. Drawn on every rail it falls inside, so the eye can carry the
            same instant down through the zoom levels. */}
        {nowInRail && (
          <span className="dt-now" style={{ left: `${pct(now)}%` }}>
            <span className="dt-now-label">{t('dtl.now')}</span>
          </span>
        )}
      </div>

      <div className="dt-axis">
        {ticks(t0, t1).map((x) => (
          <span key={x} className="dt-tick" style={{ left: `${pct(x)}%` }}>
            {tickLabel(x, years)}
          </span>
        ))}
      </div>
    </div>
  )
}

/**
 * The funnel between two rails: the selected band's footprint above, opening to
 * the full width below. It is the only thing that says *which* band the next
 * rail expands — without it the zoom is a claim the reader has to take on faith.
 */
function Funnel({ nodes, index, namer, label }) {
  if (!nodes?.length || nodes[index] === undefined) return null
  const t0 = parse(nodes[0].start)
  const t1 = parse(nodes[nodes.length - 1].end)
  const a = parse(nodes[index].start), b = parse(nodes[index].end)
  const l = ((a - t0) / (t1 - t0)) * 100
  const r = ((b - t0) / (t1 - t0)) * 100
  return (
    <div className="dt-funnel">
      <svg viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">
        <polygon points={`${l},0 ${r},0 100,100 0,100`} />
      </svg>
      <span className="dt-funnel-label">
        <Glyph lord={nodes[index].lord} size={14} />
        {label} <strong>{namer.grahaKey(nodes[index].lord)}</strong>
      </span>
    </div>
  )
}

export default function DashaTimeline({
  dasha, namer, verdictOf, conditionsOf, onMahaChange, legend, showChain = false,
  birthMs,
}) {
  const now = Date.now()
  const maha = dasha?.mahadashas
  const { t } = useLang()
  const [view, setView] = useState('timeline')

  // Open on the running chain: a timeline whose first view is someone's
  // infancy answers a question nobody asked.
  const currentIdx = (list) => {
    const i = (list ?? []).findIndex((n) => n.is_current)
    return i === -1 ? 0 : i
  }
  const [mi, setMi] = useState(() => currentIdx(maha))
  const [ai, setAi] = useState(() => currentIdx(maha?.[currentIdx(maha)]?.sub))

  const antars = maha?.[mi]?.sub
  const pratys = antars?.[ai]?.sub

  // Re-point the antar when the mahā changes, so drilling never lands on a
  // stale index from a different (and differently-sized) parent.
  const pickMaha = (i) => {
    setMi(i)
    setAi(currentIdx(maha[i].sub))
    onMahaChange?.(maha[i].lord)
  }

  // The tree can be REPLACED under us: DashaTree mounts with variant '360' and
  // an effect then flips it to the chart's default (365.25), and the user can
  // switch year-length or daśā system at any time. The arrays are the same
  // LENGTH across those trees but the periods are not, so a retained index
  // silently points at the wrong period — which is how rail 3 came to open on
  // Rahu while the running antardaśā was Maṅgala. Re-derive the opened chain
  // whenever the tree identity changes rather than trusting the old index.
  useEffect(() => {
    const m = currentIdx(maha)
    setMi(m)
    setAi(currentIdx(maha?.[m]?.sub))
  }, [maha])

  // Tell the parent which mahādaśā's conditions to fetch, including the one we
  // open on, so rail 2 is annotated before the user touches anything.
  useEffect(() => {
    if (maha?.[mi]) onMahaChange?.(maha[mi].lord)
  }, [maha, mi, onMahaChange])

  const chain = useMemo(() => {
    const m = maha?.find((n) => n.is_current)
    const a = m?.sub?.find((n) => n.is_current)
    const p = a?.sub?.find((n) => n.is_current)
    return [m, a, p].filter(Boolean)
  }, [maha])

  // Age from the birth instant, NOT from the rail's left edge. See the note at
  // the top of this file — the difference is about three years.
  const age = birthMs ? Math.floor((now - birthMs) / YEAR) : null
  const ageAt = (ms) => (birthMs ? Math.floor((ms - birthMs) / YEAR) : null)

  if (!maha?.length) return null

  const levelName = [t('dtl.rail.maha'), t('dtl.rail.antar'), t('dtl.rail.pratyantar')]

  return (
    <div className="dasha-timeline">
      {/* ── header: the facts a reader wants before any bar is read ───────── */}
      <div className="dt-chips">
        {dasha.balance_at_birth && (
          <div className="dt-chip">
            <span className="dt-chip-k">{t('dtl.chip.balance')}</span>
            <span className="dt-chip-v">
              {dasha.starting_lord_name} — {dasha.balance_at_birth}
            </span>
          </div>
        )}
        {chain.length > 0 && (
          <div className="dt-chip">
            <span className="dt-chip-k">{t('dtl.chip.current')}</span>
            <span className="dt-chip-v dt-chain-v">
              {chain.map((n, i) => (
                <span key={i}>
                  {i > 0 && <span className="dt-sep">›</span>}
                  <Glyph lord={n.lord} size={13} />
                  {namer.grahaKey(n.lord)}
                </span>
              ))}
            </span>
          </div>
        )}
        {age !== null && (
          <div className="dt-chip">
            <span className="dt-chip-k">{t('dtl.chip.age')}</span>
            <span className="dt-chip-v">{age} {t('dtl.chip.years')}</span>
          </div>
        )}
        <div className="dt-view" role="group" aria-label={t('dtl.view.label')}>
          <span className="dt-chip-k">{t('dtl.view.label')}</span>
          <div className="dt-view-btns">
            <button type="button" className={view === 'timeline' ? 'on' : ''}
                    onClick={() => setView('timeline')} aria-pressed={view === 'timeline'}>
              {t('dtl.view.timeline')}
            </button>
            <button type="button" className={view === 'table' ? 'on' : ''}
                    onClick={() => setView('table')} aria-pressed={view === 'table'}>
              {t('dtl.view.table')}
            </button>
          </div>
        </div>
      </div>

      {view === 'timeline' ? (
        <div className="dt-body">
          <div className="dt-rails">
            <Rail nodes={maha} level={0} step="1"
                  label={t('dtl.rail.maha')} sub={t('dtl.rail.maha.sub')}
                  namer={namer} verdictOf={verdictOf} now={now}
                  selected={mi} onSelect={pickMaha} />

            <Funnel nodes={maha} index={mi} namer={namer} label={t('dtl.funnel.inside')} />

            {/* Rail 2 takes conditionsOf but NOT verdictOf: ch.47's mahādaśā verse
                does not reach down here, and ch.52-60 label too few branches to
                colour one. */}
            <Rail nodes={antars} level={1} step="2"
                  label={t('dtl.rail.antar')}
                  sub={t('dtl.rail.antar.sub').replace('{lord}', namer.grahaKey(maha[mi].lord))}
                  namer={namer} conditionsOf={conditionsOf} now={now}
                  selected={ai} onSelect={setAi} />

            {pratys?.length > 0 && (
              <>
                <Funnel nodes={antars} index={ai} namer={namer} label={t('dtl.funnel.inside')} />
                <Rail nodes={pratys} level={2} step="3"
                      label={t('dtl.rail.pratyantar')}
                      sub={t('dtl.rail.pratyantar.sub').replace('{lord}', namer.grahaKey(antars[ai].lord))}
                      namer={namer} verdictOf={verdictOf} now={now} />
              </>
            )}
          </div>

          {/* ── sidebar: where the reader is standing right now ───────────── */}
          {chain.length > 0 && (
            <aside className="dt-side">
              <div className="dt-card dt-card-now">
                <h4>{t('dtl.side.current')}</h4>
                {chain.map((n, i) => (
                  <div key={i} className={`dt-now-row${i === chain.length - 1 ? ' is-last' : ''}`}>
                    <Glyph lord={n.lord} size={22} />
                    <div className="dt-now-txt">
                      <div className="dt-now-lord">
                        {namer.grahaKey(n.lord)}
                        {i === chain.length - 1 && (
                          <span className="dt-badge">{t('dtl.side.current_badge')}</span>
                        )}
                      </div>
                      <div className="dt-now-lvl">{levelName[i]}</div>
                      <div className="dt-now-dates">
                        {fmtDate(parse(n.start))} → {fmtDate(parse(n.end))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="dt-card">
                <h4>{t('dtl.side.remaining')}</h4>
                {chain.map((n, i) => (
                  <div key={i} className="dt-rem-row">
                    <span className="dt-rem-k">
                      {namer.grahaKey(n.lord)} <span className="dt-rem-lvl">({levelName[i]})</span>
                    </span>
                    <span className="dt-rem-v">{longSpan(parse(n.end) - now, t)}</span>
                  </div>
                ))}
              </div>

              {age !== null && (
                <div className="dt-card">
                  <h4>{t('dtl.side.ages')}</h4>
                  <div className="dt-rem-row">
                    <span className="dt-rem-k">{t('dtl.side.age_now')}</span>
                    <span className="dt-rem-v">{age}</span>
                  </div>
                  <div className="dt-rem-row">
                    <span className="dt-rem-k">
                      {t('dtl.side.age_start').replace('{lord}', namer.grahaKey(chain[0].lord))}
                    </span>
                    <span className="dt-rem-v">{ageAt(parse(chain[0].start))}</span>
                  </div>
                  <div className="dt-rem-row">
                    <span className="dt-rem-k">
                      {t('dtl.side.age_end').replace('{lord}', namer.grahaKey(chain[0].lord))}
                    </span>
                    <span className="dt-rem-v">{ageAt(parse(chain[0].end))}</span>
                  </div>
                </div>
              )}
            </aside>
          )}
        </div>
      ) : (
        /* ── table view: the same sequence, exact dates, nothing to scale ── */
        <div className="dt-table-wrap">
          <table className="dt-table">
            <thead>
              <tr>
                <th>{t('dtl.tbl.planet')}</th>
                <th>{t('dtl.tbl.period')}</th>
                <th>{t('dtl.tbl.start')}</th>
                <th>{t('dtl.tbl.end')}</th>
                {birthMs && <th>{t('dtl.tbl.age')}</th>}
              </tr>
            </thead>
            <tbody>
              {maha.map((m, i) => {
                const a = parse(m.start), b = parse(m.end)
                const running = a <= now && now < b
                const v = verdictOf?.(m.lord)
                return (
                  <tr key={i} className={(running ? 'running' : '') + (v ? ` v-${v.state}` : '')}>
                    <td className="dt-tbl-lord">
                      <Glyph lord={m.lord} size={15} />
                      {namer.grahaKey(m.lord)}
                      {running && <span className="dt-badge">{t('dtl.side.current_badge')}</span>}
                    </td>
                    <td>{m.years} {t('dtl.tbl.years')}</td>
                    <td>{fmtDate(a)}</td>
                    <td>{fmtDate(b)}</td>
                    {birthMs && <td>{ageAt(a)} → {ageAt(b)}</td>}
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}

      {legend}
    </div>
  )
}
