/**
 * Daśā navigator — a life laid out end to end, with today marked.
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
 *   MAHĀ        [────Sūrya────][──────Chandra──────][───Maṅgala───] …  120 yrs
 *   ANTAR         the selected mahā, re-spread across the full width
 *   PRATYANTAR    the selected antar, re-spread across the full width
 *
 * Every rail is internally proportional and honest; what changes between rails
 * is only which span the width represents. A funnel under each rail shows which
 * band was expanded, so the zoom is never implicit.
 *
 * ON COLOUR
 * ---------
 * A band's FILL is its graha — nine fixed hues, the same on every rail, so the
 * eye learns them once. The VERDICT (BPHS ch.47) is the coloured edge along the
 * band's foot: favourable, adverse, both stated, or none — supplied by the
 * caller with its citation. The two never share a channel, so neither can be
 * mistaken for the other. A band with no verdict has a plain foot, and that is
 * a real state here, not a fallback.
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

/** Duration as the almanacs write it: "16y" on the life rail, "2y 1m 18d" below. */
function fmtDur(ms, level, t) {
  const d0 = Math.max(0, Math.round(ms / DAY))
  const y = Math.floor(d0 / 365.25)
  const rem = d0 - Math.round(y * 365.25)
  const m = Math.floor(rem / 30.44)
  const d = Math.max(0, rem - Math.round(m * 30.44))
  const Y = t('dtl.unit.y', 'y'), M = t('dtl.unit.m', 'm'), D = t('dtl.unit.d', 'd')
  if (level === 0) return `${y}${Y}`
  const parts = []
  if (y) parts.push(`${y}${Y}`)
  if (m) parts.push(`${m}${M}`)
  if (level === 2 || !y) parts.push(`${d}${D}`)
  return parts.join(' ') || `${d}${D}`
}

/** Long form, for the "time remaining" readout: "2 years 4 months", "17 days". */
function longSpan(ms, t) {
  if (ms <= 0) return t('dtl.rem.ended', 'ended')
  const d = Math.floor(ms / DAY)
  const y = Math.floor(d / 365.25)
  const m = Math.floor((d - y * 365.25) / 30.44)
  const dd = Math.max(0, Math.floor(d - y * 365.25 - m * 30.44))
  const parts = []
  if (y) parts.push(`${y} ${t(y === 1 ? 'dtl.long.year' : 'dtl.long.years', y === 1 ? 'year' : 'years')}`)
  if (m) parts.push(`${m} ${t(m === 1 ? 'dtl.long.month' : 'dtl.long.months', m === 1 ? 'month' : 'months')}`)
  if (!y && dd) parts.push(`${dd} ${t(dd === 1 ? 'dtl.long.day' : 'dtl.long.days', dd === 1 ? 'day' : 'days')}`)
  return parts.join(' ')
}

function fmtDate(t) {
  const d = new Date(t)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

/**
 * Axis ticks that suit the rail's own span. The life rail wants decades; a
 * two-year antardaśā wants quarters. One fixed granularity makes two of the
 * three rails useless.
 */
function ticks(t0, t1) {
  const years = (t1 - t0) / YEAR
  const out = []
  const push = (d) => { const x = d.getTime(); if (x > t0 && x < t1) out.push(x) }
  if (years > 40) {
    for (let y = Math.ceil(yearOf(t0) / 10) * 10; y <= yearOf(t1); y += 10) push(new Date(y, 0, 1))
  } else if (years > 12) {
    for (let y = Math.ceil(yearOf(t0) / 5) * 5; y <= yearOf(t1); y += 5) push(new Date(y, 0, 1))
  } else if (years > 4) {
    for (let y = yearOf(t0); y <= yearOf(t1); y += 2) push(new Date(y, 0, 1))
  } else if (years > 1.5) {
    for (let y = yearOf(t0); y <= yearOf(t1); y += 1) push(new Date(y, 0, 1))
  } else {
    const d = new Date(t0); d.setDate(1); d.setMonth(Math.ceil(d.getMonth() / 3) * 3)
    while (d.getTime() < t1) { push(new Date(d)); d.setMonth(d.getMonth() + 3) }
  }
  return out
}
function tickLabel(x, years) {
  const d = new Date(x)
  if (years > 1.5) return String(d.getFullYear())
  return d.toLocaleString(undefined, { month: 'short' }) + ' ' + d.getFullYear()
}

/** One rail. Bands are proportional within [t0, t1] — the rail's own span. */
function Rail({ nodes, level, namer, verdictOf, conditionsOf, now, selected, onSelect, label, sub, step }) {
  const { t } = useLang()
  if (!nodes?.length) return null
  const t0 = parse(nodes[0].start)
  const t1 = parse(nodes[nodes.length - 1].end)
  const years = (t1 - t0) / YEAR
  const pct = (x) => ((x - t0) / (t1 - t0)) * 100
  const nowInRail = now >= t0 && now <= t1
  // the rail's pixel width, so a band can be judged tight in absolute terms
  // (a 6-year mahādaśā is 5% of the life rail: 55px on a desktop, 18px on a phone)
  const [trackPx, setTrackPx] = useState(0)
  const trackRef = (el) => { if (el && el.clientWidth !== trackPx) setTrackPx(el.clientWidth) }

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
          <span className="dt-rail-dur"> ({fmtDur(t1 - t0, level, t)})</span>
        </span>
      </div>

      <div className="dt-track" ref={trackRef}>
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
                + (w < 5 || (trackPx && (w / 100) * trackPx < 52) ? ' tight' : '')}
              style={{ left: `${pct(a)}%`, width: `${w}%`, '--g': `var(--gr-${n.lord})` }}
              onClick={() => onSelect?.(i)}
              aria-pressed={selected === i}
              /* The tooltip carries the CONDITIONS, not just the verdict. A
                 reader must be able to check the label against the verse
                 rather than take it on trust — and for `contested` both sides
                 have to be visible, since the whole point is that BPHS states
                 both and arbitrates neither. */
              title={`${namer.grahaKey(n.lord)} — ${fmtDate(a)} → ${fmtDate(b)} (${fmtDur(b - a, level, t)})`
                     + (v ? `\n\n${v.label.toUpperCase()} — ${v.citation}`
                          + (v.favourable?.length ? `\n${t('dtl.tip.favourable')} ${v.favourable.map((c) => c.condition).join('; ')}` : '')
                          + (v.adverse?.length ? `\n${t('dtl.tip.adverse')} ${v.adverse.map((c) => c.condition).join('; ')}` : '')
                          + (v.silent ? '\n' + t('dtl.tip.silent') : '')
                        : '')
                     + (cond
                        ? `\n\n${cond.chapter} — ${cond.counts.fired} ${t('dtl.tip.of')} ${cond.counts.total} ${t('dtl.tip.conditions_fire')}`
                          + (cond.counts.unavailable ? `, ${cond.counts.unavailable} cannot be evaluated` : '')
                          + (cond.fired?.length ? '\n' + cond.fired.map((f) => '· ' + (f.reading || f.predicate)).join('\n') : '')
                        : '')}
            >
              <Glyph lord={n.lord} size={18} className="dt-band-glyph" />
              <span className="dt-band-lord">{namer.grahaKey(n.lord)}</span>
              <span className="dt-band-vert" aria-hidden="true">{namer.grahaKey(n.lord)}</span>
              <span className="dt-band-dur">{fmtDur(b - a, level, t)}</span>
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
        {/* Today: a pill above the track and a dashed line through it, on
            every rail it falls inside, so the eye can carry the same instant
            down through the zoom levels. */}
        {nowInRail && (
          <span className="dt-now" style={{ left: `${pct(now)}%` }}>
            <span className="dt-now-label">{t('dtl.now')}</span>
          </span>
        )}
      </div>

      <div className="dt-axis">
        {ticks(t0, t1).map((x) => (
          <span key={x} className="dt-tick" style={{ left: `${pct(x)}%` }}>{tickLabel(x, years)}</span>
        ))}
      </div>
    </div>
  )
}

/** The funnel between two rails: the selected band's footprint above, opening
 *  to the full width below, washed in that graha's own colour. */
function Funnel({ nodes, index, namer, label }) {
  if (!nodes?.length || nodes[index] === undefined) return null
  const t0 = parse(nodes[0].start), t1 = parse(nodes[nodes.length - 1].end)
  const a = parse(nodes[index].start), b = parse(nodes[index].end)
  const l = ((a - t0) / (t1 - t0)) * 100, r = ((b - t0) / (t1 - t0)) * 100
  return (
    <div className="dt-funnel" style={{ '--g': `var(--gr-${nodes[index].lord})` }}>
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

/** The whole cycle as a strip — nine columns, exact dates, nothing to scale. */
function MahaStrip({ maha, namer, now, t, ageAt }) {
  return (
    <div className="dt-strip">
      <div className="dt-strip-title">{t('dtl.strip.title', 'All mahādaśās')} <span>· {t('dtl.rail.maha.sub')}</span></div>
      <div className="dt-table-wrap">
        <table className="dt-strip-t">
          <thead>
            <tr>
              <th>{t('dtl.tbl.planet')}</th>
              {maha.map((m, i) => {
                const a = parse(m.start), b = parse(m.end)
                const running = a <= now && now < b
                return (
                  <th key={i} className={running ? 'running' : ''} style={{ '--g': `var(--gr-${m.lord})` }}>
                    <Glyph lord={m.lord} size={18} />
                    <span>{namer.grahaKey(m.lord)}</span>
                  </th>
                )
              })}
            </tr>
          </thead>
          <tbody>
            <tr><td>{t('dtl.tbl.period')}</td>{maha.map((m, i) => <td key={i}>{m.years} {t('dtl.tbl.years')}</td>)}</tr>
            <tr><td>{t('dtl.tbl.start')}</td>{maha.map((m, i) => <td key={i}>{fmtDate(parse(m.start))}</td>)}</tr>
            <tr><td>{t('dtl.tbl.end')}</td>{maha.map((m, i) => <td key={i}>{fmtDate(parse(m.end))}</td>)}</tr>
            {ageAt && <tr><td>{t('dtl.tbl.age')}</td>{maha.map((m, i) => <td key={i}>{ageAt(parse(m.start))} → {ageAt(parse(m.end))}</td>)}</tr>}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default function DashaTimeline({
  dasha, namer, verdictOf, conditionsOf, onMahaChange, legend, birthMs,
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
  // A period that begins before birth (the notional start of the first
  // mahādaśā) is shown as "birth", never as a negative age.
  const ageAt = birthMs
    ? (ms) => (ms < birthMs ? t('dtl.age.birth', 'birth') : Math.floor((ms - birthMs) / YEAR))
    : null

  if (!maha?.length) return null

  const levelName = [t('dtl.rail.maha'), t('dtl.rail.antar'), t('dtl.rail.pratyantar')]
  const cycle = `${dasha.system || ''} · ${dasha.total_years || 120}-${t('dtl.strip.yearcycle', 'year cycle')}`

  return (
    <div className="dasha-timeline">
      {/* ── header: name, the facts a reader wants before any bar is read ── */}
      <div className="dt-head">
        <div className="dt-title">
          <h4>{t('dtl.title', 'Daśā navigator')}</h4>
          <span className="dt-title-sub">{cycle}</span>
        </div>
        <div className="dt-chips">
          {dasha.balance_at_birth && (
            <div className="dt-chip">
              <span className="dt-chip-k">{t('dtl.chip.balance')}</span>
              <span className="dt-chip-v">{dasha.starting_lord_name} — {dasha.balance_at_birth}</span>
            </div>
          )}
          {chain.length > 0 && (
            <div className="dt-chip">
              <span className="dt-chip-k">{t('dtl.chip.current')}</span>
              <span className="dt-chip-v dt-chain-v">
                {chain.map((n, i) => (
                  <span key={i} style={{ '--g': `var(--gr-${n.lord})` }} className="dt-chain-lord">
                    {i > 0 && <span className="dt-sep">›</span>}
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
              <button type="button" className={view === 'timeline' ? 'on' : ''} onClick={() => setView('timeline')} aria-pressed={view === 'timeline'}>{t('dtl.view.timeline')}</button>
              <button type="button" className={view === 'table' ? 'on' : ''} onClick={() => setView('table')} aria-pressed={view === 'table'}>{t('dtl.view.table')}</button>
            </div>
          </div>
        </div>
      </div>

      {view === 'timeline' ? (
        <>
          <div className="dt-body">
            <div className="dt-rails">
              <Rail nodes={maha} level={0} step="1" label={t('dtl.rail.maha')} sub={t('dtl.rail.maha.sub')}
                    namer={namer} verdictOf={verdictOf} now={now} selected={mi} onSelect={pickMaha} />
              <Funnel nodes={maha} index={mi} namer={namer} label={t('dtl.funnel.inside')} />
              {/* Rail 2 takes conditionsOf but NOT verdictOf: ch.47's mahādaśā verse
                  does not reach down here, and ch.52-60 label too few branches to
                  colour one. */}
              <Rail nodes={antars} level={1} step="2" label={t('dtl.rail.antar')}
                    sub={t('dtl.rail.antar.sub').replace('{lord}', namer.grahaKey(maha[mi].lord))}
                    namer={namer} conditionsOf={conditionsOf} now={now} selected={ai} onSelect={setAi} />
              {pratys?.length > 0 && (
                <>
                  <Funnel nodes={antars} index={ai} namer={namer} label={t('dtl.funnel.inside')} />
                  <Rail nodes={pratys} level={2} step="3" label={t('dtl.rail.pratyantar')}
                        sub={t('dtl.rail.pratyantar.sub').replace('{lord}', namer.grahaKey(antars[ai].lord))}
                        namer={namer} verdictOf={verdictOf} now={now} />
                </>
              )}
              <MahaStrip maha={maha} namer={namer} now={now} t={t} ageAt={ageAt} />
            </div>

            {/* ── sidebar: where the reader is standing right now ─────────── */}
            {chain.length > 0 && (
              <aside className="dt-side">
                <div className="dt-card dt-card-now">
                  <h4>{t('dtl.side.current')}</h4>
                  {chain.map((n, i) => (
                    <div key={i}>
                      {i > 0 && <div className="dt-arrow" aria-hidden="true">↓</div>}
                      <div className={`dt-now-row${i === chain.length - 1 ? ' is-last' : ''}`} style={{ '--g': `var(--gr-${n.lord})` }}>
                        <Glyph lord={n.lord} size={30} />
                        <div className="dt-now-txt">
                          <div className="dt-now-lord">
                            {namer.grahaKey(n.lord)}
                            {i === chain.length - 1 && <span className="dt-badge">{t('dtl.side.current_badge')}</span>}
                          </div>
                          <div className="dt-now-lvl">{levelName[i]}</div>
                          <div className="dt-now-dates">{fmtDate(parse(n.start))} → {fmtDate(parse(n.end))}</div>
                          <div className="dt-now-dur">{fmtDur(parse(n.end) - parse(n.start), i, t)}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="dt-card">
                  <h4>{t('dtl.side.remaining')}</h4>
                  {chain.map((n, i) => (
                    <div key={i} className="dt-rem-row">
                      <span className="dt-rem-k">{t('dtl.side.in', 'In')} {namer.grahaKey(n.lord)} <span className="dt-rem-lvl">({levelName[i]})</span></span>
                      <span className="dt-rem-v">{longSpan(parse(n.end) - now, t)}</span>
                    </div>
                  ))}
                </div>

                {age !== null && (
                  <div className="dt-card">
                    <h4>{t('dtl.side.ages')}</h4>
                    <div className="dt-rem-row"><span className="dt-rem-k">{t('dtl.side.age_now')}</span><span className="dt-rem-v">{age} {t('dtl.chip.years')}</span></div>
                    <div className="dt-rem-row"><span className="dt-rem-k">{t('dtl.side.age_start').replace('{lord}', namer.grahaKey(chain[0].lord))}</span><span className="dt-rem-v">{ageAt(parse(chain[0].start))} {t('dtl.chip.years')}</span></div>
                    <div className="dt-rem-row"><span className="dt-rem-k">{t('dtl.side.age_end').replace('{lord}', namer.grahaKey(chain[0].lord))}</span><span className="dt-rem-v">{ageAt(parse(chain[0].end))} {t('dtl.chip.years')}</span></div>
                  </div>
                )}
              </aside>
            )}
          </div>
        </>
      ) : (
        /* ── table view: the same sequence, exact dates, nothing to scale ── */
        <div className="dt-table-wrap">
          <table className="dt-table">
            <thead>
              <tr>
                <th>{t('dtl.tbl.planet')}</th><th>{t('dtl.tbl.period')}</th>
                <th>{t('dtl.tbl.start')}</th><th>{t('dtl.tbl.end')}</th>
                {ageAt && <th>{t('dtl.tbl.age')}</th>}
              </tr>
            </thead>
            <tbody>
              {maha.map((m, i) => {
                const a = parse(m.start), b = parse(m.end)
                const running = a <= now && now < b
                const v = verdictOf?.(m.lord)
                return (
                  <tr key={i} className={(running ? 'running' : '') + (v ? ` v-${v.state}` : '')} style={{ '--g': `var(--gr-${m.lord})` }}>
                    <td className="dt-tbl-lord">
                      <Glyph lord={m.lord} size={16} />
                      {namer.grahaKey(m.lord)}
                      {running && <span className="dt-badge">{t('dtl.side.current_badge')}</span>}
                    </td>
                    <td>{m.years} {t('dtl.tbl.years')}</td>
                    <td>{fmtDate(a)}</td>
                    <td>{fmtDate(b)}</td>
                    {ageAt && <td>{ageAt(a)} → {ageAt(b)}</td>}
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
