/**
 * Chara Daśā timeline — Jaimini, sign-based, laid out as a life.
 *
 * This is deliberately NOT the Viṁśottarī DashaTimeline. That one is graha-lord
 * shaped and coloured by BPHS ch.47's verdict verse; Chara Daśā bands are RĀŚIS,
 * from a different school, and ch.47 does not reach them — so this is its own,
 * quieter instrument with no verdict colouring.
 *
 * THE ONE HONEST COMPROMISE, MADE VISIBLE
 * ---------------------------------------
 * The per-sign LENGTHS are validated against the source's worked examples. The
 * ORDER is not: the rule that decides whether the signs run zodiacally forward
 * ("direct") or backward ("reverse") from the lagna lives in the book's Ch.3,
 * which is not in the available scan. So the direction is a TOGGLE the reader
 * sets, never a sourced result — the caveat says so, plainly, above the toggle.
 * The book's own worked examples all happen to run direct, so that is the
 * default, but it is labelled as the reader's assumption.
 *
 * THE AXIS IS AGE, NOT A CALENDAR. The lengths are in years; age is exact from
 * them and needs no daśā day-count convention (which is itself unsettled here).
 * Calendar years are shown alongside as a plain birth + N-years convenience,
 * computed from the chart's own Julian day.
 */

import { useState } from 'react'

const DAY = 86400000
const YEAR = 365.2425 * DAY               // a calendar year, for age↔date only
const jdToMs = (jd) => (jd - 2440587.5) * DAY

const fmtAge = (y) => (Number.isInteger(y) ? `${y}` : y.toFixed(1))
const yearOfMs = (ms) => new Date(ms).getUTCFullYear()

export default function CharaDashaTimeline({ chara, lagna, jdUt, namer }) {
  const [direction, setDirection] = useState('direct')
  if (!chara?.lengths?.length || lagna === undefined || lagna === null) return null

  const bySign = Object.fromEntries(chara.lengths.map((l) => [l.sign, l]))
  const step = direction === 'direct' ? 1 : -1
  const total = chara.total_years || chara.lengths.reduce((s, l) => s + l.years, 0)

  // Walk the twelve signs from the lagna in the chosen direction, accumulating
  // each sign's own length as an age offset — the same order the engine builds
  // server-side when a direction is supplied, done here so the toggle is instant.
  let cursor = 0
  const bands = Array.from({ length: 12 }, (_, k) => {
    const sign = (((lagna + step * k) % 12) + 12) % 12
    const l = bySign[sign]
    const start = cursor
    cursor += l.years
    return { sign, years: l.years, lord: l.lord, own: l.own_sign, start, end: cursor }
  })

  const birthMs = jdUt ? jdToMs(jdUt) : null
  const nowAge = birthMs != null ? (Date.now() - birthMs) / YEAR : null
  const withinLife = nowAge != null && nowAge >= 0 && nowAge <= total
  const current = withinLife ? bands.find((b) => nowAge >= b.start && nowAge < b.end) : null

  const pct = (y) => (y / total) * 100
  const calYear = (y) => (birthMs != null ? yearOfMs(birthMs + y * YEAR) : null)

  const tickStep = total > 72 ? 24 : total > 36 ? 12 : 6
  const ticks = []
  for (let a = tickStep; a < total - tickStep / 2; a += tickStep) ticks.push(a)

  return (
    <div className="chara-dasha">
      <p className="cd-caveat">
        <strong>Sequence direction is not in the available source.</strong> The
        rule that decides whether the twelve signs run zodiacally forward
        (“direct”) or backward (“reverse”) from the lagna is in the book’s
        Chapter 3, absent from the scanned copy. The per-sign <em>lengths</em>
        here are validated against the book’s worked examples; the <em>order</em>
        is the direction you choose below. The book’s own examples all run
        direct, so that is the default — but it is your assumption, not a sourced
        result.
      </p>

      <div className="cd-controls">
        <span className="d-label">Direction</span>
        <button type="button" className={direction === 'direct' ? 'on' : ''}
                onClick={() => setDirection('direct')}
                title="Signs run zodiacally forward from the lagna">direct</button>
        <button type="button" className={direction === 'reverse' ? 'on' : ''}
                onClick={() => setDirection('reverse')}
                title="Signs run backward from the lagna">reverse</button>
        <span className="cd-total">{total}-year cycle · from lagna {namer.rasi(lagna)}</span>
      </div>

      {current && (
        <p className="dt-chain">
          Running now: <strong>{namer.rasi(current.sign)}</strong> daśā
          {' '}(lord {namer.grahaKey(current.lord)}) — age{' '}
          {fmtAge(current.start)}–{fmtAge(current.end)}
          {birthMs != null && <span className="dt-chain-end"> · to {calYear(current.end)}</span>}
        </p>
      )}

      <div className="dt-rail">
        <div className="dt-track">
          {bands.map((b, i) => {
            const past = nowAge != null && b.end <= nowAge
            const running = current && current.sign === b.sign
            return (
              <div key={i}
                   className={`dt-band${running ? ' running' : ''}${past ? ' past' : ''}`}
                   style={{ left: `${pct(b.start)}%`, width: `${pct(b.years)}%` }}
                   title={`${namer.rasi(b.sign)} — ${b.years}y (age ${fmtAge(b.start)}–${fmtAge(b.end)})`
                     + (b.own ? ' · own sign → full 12 years' : '')
                     + ` · Chara lord ${namer.grahaKey(b.lord)}`}>
                <span className="dt-band-lord">{namer.rasi(b.sign)}</span>
                <span className="dt-band-dur">{b.years}y</span>
              </div>
            )
          })}
          {withinLife && (
            <span className="dt-now" style={{ left: `${pct(nowAge)}%` }}>
              <span className="dt-now-label">now</span>
            </span>
          )}
        </div>
        <div className="dt-axis">
          <span className="dt-tick" style={{ left: '0%' }}>
            birth{birthMs != null && ` · ${yearOfMs(birthMs)}`}
          </span>
          {ticks.map((a) => (
            <span key={a} className="dt-tick" style={{ left: `${pct(a)}%` }}>
              age {a}{birthMs != null && ` · ${calYear(a)}`}
            </span>
          ))}
        </div>
      </div>

      <div className="scroll cd-list">
        <table>
          <thead>
            <tr>
              <th>#</th><th>Rāśi</th><th>Chara lord</th><th>Years</th><th>Age</th>
              {birthMs != null && <th>Calendar</th>}
            </tr>
          </thead>
          <tbody>
            {bands.map((b, i) => (
              <tr key={i} className={current && current.sign === b.sign ? 'cd-cur' : ''}>
                <td>{i + 1}</td>
                <td>{namer.rasi(b.sign)}{b.own && <span className="cd-own" title="own sign → full 12 years"> ∗</span>}</td>
                <td>{namer.grahaKey(b.lord)}</td>
                <td>{b.years}</td>
                <td>{fmtAge(b.start)}–{fmtAge(b.end)}</td>
                {birthMs != null && <td>{calYear(b.start)}–{calYear(b.end)}</td>}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="dasha-note">
        Jaimini Chara Daśā · {chara.citation}. Lengths validated against the
        source’s worked examples; the sequence direction is user-selected, not
        sourced (book Ch.3). {chara.rejections?.[0]}
      </p>
    </div>
  )
}
