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
 * is only which span the width represents. A connector under each rail shows
 * which band was expanded, so the zoom is never implicit.
 *
 * ON COLOUR
 * ---------
 * The colouring is supplied by the caller, per lord, and each entry must carry
 * its own citation. This component deliberately owns no opinion about whether a
 * daśā is good or bad — see the legend text in DashaTimeline's parent. A band
 * with no verdict renders neutral, and neutral is a real state here rather than
 * a fallback.
 */

import { useEffect, useMemo, useState } from 'react'

const DAY = 86400000

const parse = (s) => new Date(s.replace(' ', 'T')).getTime()
const yearOf = (t) => new Date(t).getFullYear()

/** Duration in a form that stays readable from decades down to weeks. */
function span(ms) {
  const d = ms / DAY
  if (d >= 365) return `${(d / 365.25).toFixed(d / 365.25 < 10 ? 1 : 0)}y`
  if (d >= 31) return `${Math.round(d / 30.44)}m`
  return `${Math.round(d)}d`
}

function fmtDate(t) {
  const d = new Date(t)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

/**
 * One rail. Bands are proportional within [t0, t1] — the rail's own span, not
 * the whole life — which is what makes a ten-week pratyantar readable.
 */
function Rail({ nodes, level, namer, verdictOf, conditionsOf, now, selected, onSelect, label }) {
  if (!nodes?.length) return null
  const t0 = parse(nodes[0].start)
  const t1 = parse(nodes[nodes.length - 1].end)
  const pct = (t) => ((t - t0) / (t1 - t0)) * 100
  const nowInRail = now >= t0 && now <= t1

  return (
    <div className="dt-rail">
      <div className="dt-rail-head">
        <span className="dt-rail-label">{label}</span>
        <span className="dt-rail-span">{fmtDate(t0)} → {fmtDate(t1)}</span>
      </div>
      <div className="dt-track">
        {nodes.map((n, i) => {
          const a = parse(n.start), b = parse(n.end)
          const v = verdictOf?.(n.lord)
          const cond = conditionsOf?.(n.lord)
          const past = b < now
          const running = a <= now && now < b
          return (
            <button
              type="button"
              key={i}
              className={`dt-band${running ? ' running' : ''}${past ? ' past' : ''}`
                + (selected === i ? ' selected' : '')
                + (v ? ` v-${v.state}` : '')}
              style={{ left: `${pct(a)}%`, width: `${pct(b) - pct(a)}%` }}
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
                              ? `\nfavourable: ${v.favourable.map((c) => c.condition).join('; ')}`
                              : '')
                          + (v.adverse?.length
                              ? `\nadverse: ${v.adverse.map((c) => c.condition).join('; ')}`
                              : '')
                          + (v.silent
                              ? '\nNeither branch of the verse names this placement.'
                              : '')
                        : '')
                     + (cond
                        ? `\n\n${cond.chapter} — ${cond.counts.fired} of ${cond.counts.total}`
                          + ' conditions fire'
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
            <span className="dt-now-label">now</span>
          </span>
        )}
      </div>
      {/* Decade ticks only on the life rail; the lower rails are too short. */}
      {level === 0 && (
        <div className="dt-axis">
          {decades(t0, t1).map((t) => (
            <span key={t} className="dt-tick" style={{ left: `${pct(t)}%` }}>
              {yearOf(t)}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

function decades(t0, t1) {
  const out = []
  let y = Math.ceil(yearOf(t0) / 10) * 10
  while (new Date(y, 0, 1).getTime() < t1) {
    const t = new Date(y, 0, 1).getTime()
    if (t > t0) out.push(t)
    y += 10
  }
  return out
}

export default function DashaTimeline({
  dasha, namer, verdictOf, conditionsOf, onMahaChange, legend, showChain = false,
}) {
  const now = Date.now()
  const maha = dasha?.mahadashas
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

  if (!maha?.length) return null

  return (
    <div className="dasha-timeline">
      {showChain && chain.length > 0 && (
        <p className="dt-chain">
          Running now:{' '}
          {chain.map((n, i) => (
            <span key={i}>
              {i > 0 && <span className="dt-sep"> › </span>}
              <strong>{namer.grahaKey(n.lord)}</strong>
              <span className="dt-chain-end"> to {fmtDate(parse(n.end))}</span>
            </span>
          ))}
        </p>
      )}

      <Rail nodes={maha} level={0} label="Mahādaśā — the whole life"
            namer={namer} verdictOf={verdictOf} now={now}
            selected={mi} onSelect={pickMaha} />

      <p className="dt-zoom">
        ↳ inside <strong>{namer.grahaKey(maha[mi].lord)}</strong>’s mahādaśā
      </p>
      {/* Rail 2 takes conditionsOf but NOT verdictOf: ch.47's mahādaśā verse
          does not reach down here, and ch.52-60 label too few branches to
          colour one. */}
      <Rail nodes={antars} level={1} label="Antardaśā"
            namer={namer} conditionsOf={conditionsOf} now={now}
            selected={ai} onSelect={setAi} />

      {pratys?.length > 0 && (
        <>
          <p className="dt-zoom">
            ↳ inside <strong>{namer.grahaKey(antars[ai].lord)}</strong>’s antardaśā
          </p>
          <Rail nodes={pratys} level={2} label="Pratyantardaśā"
                namer={namer} verdictOf={verdictOf} now={now} />
        </>
      )}

      {legend}
    </div>
  )
}
