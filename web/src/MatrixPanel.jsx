/**
 * Chart-analysis matrix — per-chart domain verdicts (v1: bhāva + kāraka).
 *
 * Fetches /api/matrix for the loaded chart and shows two views: expandable
 * life-theme cards (each opening to its cited, weighted ledger) and a bhāva
 * decomposition heatmap (12 houses × the four contributors + net). Every number
 * is an iṣṭa/kaṣṭa balance in [-1,+1]; the band is a tint over a visible ledger,
 * never a black box — an indication from classical measures, not a fated verdict.
 */
import { useState, useEffect } from 'react'
import { API } from './config.js'
import { useLang } from './LangContext.jsx'

const BAND_C = {
  thriving: '#2b8a6f', supported: '#5aa07f', mixed: '#a9791f',
  stressed: '#c06a55', afflicted: '#b03f36',
}
const NEUTRAL = [122, 127, 140], ISTA = [43, 138, 111], KASTA = [176, 63, 54]
const _mix = (a, b, t) => `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(',')})`
// signed net → diverging tint (−1 sindoor · 0 neutral · +1 jade)
function netColor(v) {
  const t = Math.max(-1, Math.min(1, v || 0))
  return t >= 0 ? _mix(NEUTRAL, ISTA, t) : _mix(NEUTRAL, KASTA, -t)
}
const pct = (w) => (w == null ? '' : Math.round(w * 100) + '%')
const sv = (v) => (v == null ? '—' : (v >= 0 ? '+' : '') + v.toFixed(2))

function Ledger({ comps, nm, t }) {
  const label = (c) => {
    if (c.factor === 'bhava') return `${t('matrix.house', 'House')} ${c.house}`
    if (c.factor === 'lord') return `${t('matrix.lord', 'Lord')} · ${nm(c.graha)}`
    if (c.factor === 'occupants') return t('matrix.occ', 'Occupants') + (c.grahas && c.grahas.length ? ' · ' + c.grahas.map(nm).join(', ') : '')
    if (c.factor === 'aspects') return t('matrix.asp', 'Aspects in')
    if (c.factor === 'karaka' || c.factor === 'sthira_karaka') return `${t('matrix.karaka', 'Kāraka')} · ${nm(c.graha)}`
    if (c.factor === 'chara_karaka') return `${c.role} · ${c.graha ? nm(c.graha) : '—'}`
    if (c.factor === 'yoga') return `${t('matrix.yoga', 'Yoga')} · ${c.slot}`
    if (c.factor === 'varga') return `${t('matrix.varga', 'Varga')} · ${c.chart}`
    return c.factor
  }
  return (
    <div className="mx-ledger">
      {comps.map((c, i) => (
        <div className="mx-lrow" key={i} title={c.detail || ''}>
          <span className="mx-lw">{pct(c.effWeight != null ? c.effWeight : c.weight)}</span>
          <span className="mx-ll">{label(c)}</span>
          <span className="mx-lv" style={{ color: c.value == null ? 'var(--muted)' : c.value >= 0 ? BAND_C.thriving : BAND_C.afflicted }}>{sv(c.value)}</span>
          <span className="mx-lt">{c.tier}</span>
        </div>
      ))}
    </div>
  )
}

const GRAHA_ABBR = { sun: 'Su', moon: 'Mo', mars: 'Ma', mercury: 'Me', jupiter: 'Ju', venus: 'Ve', saturn: 'Sa', rahu: 'Ra', ketu: 'Ke' }
const RASI_ABBR = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi']
const polColor = (p) => (p === 1 ? _mix(NEUTRAL, ISTA, 1) : p === -1 ? _mix(NEUTRAL, KASTA, 1) : `rgb(${NEUTRAL.join(',')})`)

// Aspect web — grahas placed on the zodiac by longitude; dṛṣṭi as edges coloured
// by the aspecting graha's benefic/malefic nature, node fill = disposition.
function MatrixGraph({ nodes, edges, nm, t }) {
  const cx = 200, cy = 200, Rr = 158, Rn = 128
  const at = (L, r) => [cx + r * Math.cos(L * Math.PI / 180), cy - r * Math.sin(L * Math.PI / 180)]
  const pos = {}
  Object.entries(nodes).forEach(([k, v]) => { pos[k] = at(v.longitude, Rn) })
  return (
    <div className="mx-graphwrap">
      <svg viewBox="0 0 400 400" className="mx-graph" role="img"
           aria-label="Aspect web: grahas placed by longitude on the zodiac ring, dṛṣṭi drawn as edges coloured by the aspecting graha's benefic or malefic nature.">
        <circle cx={cx} cy={cy} r={Rr} className="mx-ring" />
        {Array.from({ length: 12 }, (_, s) => {
          const [bx, by] = at(s * 30, Rr)
          const [lx, ly] = at(s * 30 + 15, Rr + 14)
          return (
            <g key={s}>
              <line x1={cx} y1={cy} x2={bx.toFixed(1)} y2={by.toFixed(1)} className="mx-spoke" />
              <text x={lx.toFixed(1)} y={(ly + 3).toFixed(1)} className="mx-rlbl" textAnchor="middle">{RASI_ABBR[s]}</text>
            </g>
          )
        })}
        {edges.map((e, i) => {
          const a = pos[e.from], b = pos[e.to]
          if (!a || !b) return null
          return (
            <line key={i} x1={a[0].toFixed(1)} y1={a[1].toFixed(1)} x2={b[0].toFixed(1)} y2={b[1].toFixed(1)}
                  stroke={polColor(nodes[e.from]?.polarity)} strokeWidth={(0.5 + e.strength * 1.6).toFixed(1)}
                  strokeOpacity={(0.12 + e.strength * 0.33).toFixed(2)}>
              <title>{nm(e.from)} → {nm(e.to)} · {Math.round(e.strength * 100)}%</title>
            </line>
          )
        })}
        {Object.entries(nodes).map(([k, v]) => {
          const [x, y] = pos[k]
          const r = 6 + (v.strength ? Math.min(v.strength, 1.5) * 3.5 : 2)
          return (
            <g key={k}>
              <circle cx={x.toFixed(1)} cy={y.toFixed(1)} r={r.toFixed(1)} fill={netColor(v.disp)}
                      stroke={polColor(v.polarity)} strokeWidth="1.6">
                <title>{nm(k)} · {v.state} · disp {sv(v.disp)} · bhāva {v.bhava}{v.retro ? ' · retro' : ''}</title>
              </circle>
              <text x={x.toFixed(1)} y={(y + 3).toFixed(1)} className="mx-nlbl" textAnchor="middle">{GRAHA_ABBR[k] || k.slice(0, 2)}</text>
            </g>
          )
        })}
      </svg>
      <div className="mx-legend">
        <span className="mx-leg"><i style={{ background: polColor(1) }} />{t('matrix.benefic', 'benefic dṛṣṭi')}</span>
        <span className="mx-leg"><i style={{ background: polColor(-1) }} />{t('matrix.malefic', 'malefic dṛṣṭi')}</span>
        <span className="mx-leg">{t('matrix.nodenote', 'node fill = disposition · ring size = strength')}</span>
      </div>
    </div>
  )
}

// Sarvāṣṭakavarga strip — natal bindus per sign (0..56), the transit-strength map
// that grades the timeline's gochara. High bindus support a transit, low afflict.
const RASI_AB = ['Ar', 'Ta', 'Ge', 'Cn', 'Le', 'Vi', 'Li', 'Sc', 'Sg', 'Cp', 'Aq', 'Pi']
function MatrixAvStrip({ av, t }) {
  const sav = av.sarva || []
  if (!sav.length) return null
  const peak = Math.max(...sav)
  return (
    <div className="mx-av">
      <div className="mx-av-lbl">{t('matrix.av', 'Sarvāṣṭakavarga · transit strength')}</div>
      <div className="mx-av-row">
        {sav.map((b, i) => (
          <span key={i} className={'mx-av-cell' + (b === peak ? ' peak' : '')}
                style={{ background: netColor(Math.max(-1, Math.min(1, (b - 28) / 12))) }}
                title={`${RASI_AB[i]} · ${b} bindus`}>
            <b>{b}</b><i>{RASI_AB[i]}</i>
          </span>
        ))}
      </div>
      <div className="mx-av-note">{t('matrix.avnote', 'bindus per sign (0–56); Σ = 337 — a graha transiting a bindu-rich sign supports, a bindu-poor one afflicts')}</div>
    </div>
  )
}

const CLOCK_LABEL = { vims: 'Viṁśottarī', goch: 'gochara', chara: 'chara', trig: 'trigger' }

// Overall projection curve — value line (coloured by iṣṭa/kaṣṭa height) over a
// confidence band (clock disagreement) and, once refined, an outer birth-time
// (Monte-Carlo) envelope shown separately.
function MatrixCurve({ steps, t, envelope }) {
  if (!steps.length) return null
  const W = 660, H = 150, PX = 28, PYt = 12, PYb = 18
  const n = steps.length
  const x = (i) => PX + (i / Math.max(1, n - 1)) * (W - PX - 8)
  const y = (v) => PYt + (1 - (v + 1) / 2) * (H - PYt - PYb)
  const bandOf = (s) => s.overallBand || [s.overall, s.overall]
  const vpts = steps.map((s, i) => `${x(i)},${y(s.overall)}`).join(' ')
  const band = [
    ...steps.map((s, i) => `${x(i)},${y(bandOf(s)[1])}`),
    ...steps.map((s, i) => `${x(i)},${y(bandOf(s)[0])}`).reverse(),
  ].join(' ')
  const env = envelope && envelope.length === n ? [
    ...envelope.map((e, i) => `${x(i)},${y(e.p90)}`),
    ...envelope.map((e, i) => `${x(i)},${y(e.p10)}`).reverse(),
  ].join(' ') : null
  return (
    <div className="mx-cvwrap">
      <div className="mx-tl-lbl">{t('matrix.curve', 'Overall projection · confidence band')}</div>
      <svg viewBox={`0 0 ${W} ${H}`} className="mx-curve" role="img" aria-label="overall projection curve">
        <defs>
          <linearGradient id="mxcv" gradientUnits="userSpaceOnUse" x1="0" y1={y(1)} x2="0" y2={y(-1)}>
            <stop offset="0%" className="mx-cv-g0" />
            <stop offset="50%" className="mx-cv-g1" />
            <stop offset="100%" className="mx-cv-g2" />
          </linearGradient>
        </defs>
        <line x1={PX} y1={y(0.5)} x2={W - 8} y2={y(0.5)} className="mx-cv-grid" />
        <line x1={PX} y1={y(-0.5)} x2={W - 8} y2={y(-0.5)} className="mx-cv-grid" />
        <line x1={PX} y1={y(0)} x2={W - 8} y2={y(0)} className="mx-cv-zero" />
        <text x="2" y={y(1) + 3} className="mx-cv-yl">+1</text>
        <text x="8" y={y(0) + 3} className="mx-cv-yl">0</text>
        <text x="2" y={y(-1) + 3} className="mx-cv-yl">−1</text>
        {env && <polygon points={env} className="mx-cv-env" />}
        <polygon points={band} className="mx-cv-band" />
        <polyline points={vpts} className="mx-cv-line" stroke="url(#mxcv)" />
        {steps.map((s, i) => (i % 6 === 0
          ? <text key={i} x={x(i)} y={H - 3} className="mx-cv-xl">{s.date.slice(2, 7)}</text> : null))}
      </svg>
    </div>
  )
}

// Near-future timeline — a daśā ribbon over a themes×months heatmap + flagged windows.
function MatrixTimeline({ timeline, themeName, nm, t, mc, onRefine, mcBusy, mcMin, setMcMin }) {
  const steps = timeline.steps || []
  const order = timeline.themeOrder || []
  if (!steps.length) return null
  const ym = (d) => d.slice(0, 7)
  const survOf = {}
  if (mc && mc.events) mc.events.forEach((e) => { survOf[e.key + '|' + e.from] = e.survival })
  const segs = []
  let cur = null
  steps.forEach((s) => {
    const k = `${s.maha}|${s.antar}`
    if (!cur || cur.k !== k) { if (cur) segs.push(cur); cur = { k, maha: s.maha, antar: s.antar, n: 1 } }
    else cur.n++
  })
  if (cur) segs.push(cur)
  const rowCells = (vget, cfget) => steps.map((s, i) => {
    const v = vget(s)
    const cf = cfget ? cfget(s) : 1
    return <td key={i} className="mx-tl-cell" style={{ background: netColor(v), opacity: 0.4 + 0.6 * cf }}
               title={`${ym(s.date)} · ${sv(v)} · ${t('matrix.conviction', 'conviction')} ${Math.round(cf * 100)}%`} />
  })
  return (
    <div className="mx-tlwrap">
      <MatrixCurve steps={steps} t={t} envelope={mc && mc.envelope} />
      <div className="mx-mc-ctl">
        <button type="button" className="mx-mc-btn" onClick={() => onRefine && onRefine(mcMin)} disabled={mcBusy}>
          {mcBusy ? t('matrix.refining', 'Refining…') : t('matrix.refine', 'Refine · birth-time')}
        </button>
        <select className="mx-mc-min" value={mcMin} onChange={(e) => setMcMin && setMcMin(+e.target.value)} disabled={mcBusy}>
          {[4, 8, 15, 30].map((m) => <option key={m} value={m}>±{m} min</option>)}
        </select>
        {mc && (
          <span className={'mx-mc-sum' + (mc.lagnaStability < 0.85 ? ' warn' : '')}>
            {t('matrix.lagnastab', 'lagna stable')} {Math.round(mc.lagnaStability * 100)}% · {mc.samples} {t('matrix.runs', 'runs')}
          </span>
        )}
      </div>
      <div className="mx-tl-ribbon">
        {segs.map((sg, i) => (
          <span key={i} className="mx-tl-seg" style={{ flexGrow: sg.n }} title={`${nm(sg.maha)} – ${nm(sg.antar)}`}>{nm(sg.antar)}</span>
        ))}
      </div>
      <div className="mx-heatwrap">
        <table className="mx-heat mx-tl-table">
          <thead>
            <tr><th className="mx-tl-name" />{steps.map((s, i) => <th key={i} className="mx-tl-mh">{i % 3 === 0 ? ym(s.date).slice(2) : ''}</th>)}</tr>
          </thead>
          <tbody>
            <tr className="mx-tl-overall-row"><td className="mx-tl-name"><b>{t('matrix.overall', 'Overall')}</b></td>{rowCells((s) => s.overall, (s) => s.overallCf ?? 1)}</tr>
            {order.map((tk) => (
              <tr key={tk}><td className="mx-tl-name">{t('matrix.theme.' + tk, themeName[tk] || tk)}</td>{rowCells((s) => s.themes[tk], (s) => (s.conv ? s.conv[tk] : 1))}</tr>
            ))}
          </tbody>
        </table>
      </div>
      {timeline.events && timeline.events.length > 0 && (
        <div className="mx-events">
          <div className="mx-tl-lbl">{t('matrix.events', 'Projected events')}</div>
          <ul className="mx-ev-list">
            {timeline.events.map((e, i) => (
              <li key={i} className={e.good ? 'good' : 'bad'}>
                <span className="mx-ev-dir">{e.good ? '▲' : '▼'}</span>
                <div className="mx-ev-body">
                  <div className="mx-ev-top">
                    <span className="mx-ev-label">{t('matrix.event.' + e.key + '.' + (e.good ? 'good' : 'bad'), themeName[e.key] || e.key)}</span>
                    <span className="mx-ev-date">{ym(e.from)}{e.from !== e.to ? ' – ' + ym(e.to) : ''}</span>
                  </div>
                  <div className="mx-ev-meta">
                    <span className="mx-ev-int" title={`${t('matrix.intensity', 'intensity')} ${Math.round(e.intensity * 100)}%`}>
                      <i style={{ width: `${Math.round(Math.min(1, e.intensity / 0.4) * 100)}%` }} />
                    </span>
                    {e.cf != null && <span className="mx-ev-cf" title={t('matrix.conviction', 'conviction')}>{Math.round(e.cf * 100)}%</span>}
                    {survOf[e.key + '|' + e.from] != null && (
                      <span className="mx-ev-surv" title={t('matrix.survival', 'birth-time survival')}>
                        {Math.round(survOf[e.key + '|' + e.from] * 100)}%↻
                      </span>
                    )}
                    <span className="mx-ev-drv">{e.driver ? t('matrix.clock.' + e.driver, CLOCK_LABEL[e.driver]) + ' · ' : ''}{nm(e.maha)}–{nm(e.antar)}</span>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
      <p className="mx-prov">{timeline.note}</p>
    </div>
  )
}

const THEME_KEYS = ['self', 'wealth', 'career', 'marriage', 'children', 'health',
  'education', 'home', 'fortune', 'enemies', 'foreign', 'longevity']

const CHANGE_DIR = { up: '↑', down: '↓', shift: '↻', care: '♥' }

// Projected changes — typed transition-windows grouped by the three motives, with
// the two sensitive care-signals (♥) behind an opt-in toggle.
function MatrixChanges({ changes, nm, t }) {
  const [showCare, setShowCare] = useState(false)
  if (!changes) return null
  const ym = (d) => d.slice(0, 7)
  const groups = [
    ['health', t('matrix.motive.health', 'Health')],
    ['wealthCareer', t('matrix.motive.wealthCareer', 'Wealth & Career')],
    ['relationships', t('matrix.motive.relationships', 'Relationships')],
  ]
  const visible = (g) => (changes[g] || []).filter((e) => showCare || !e.care)
  const anyCare = groups.some(([g]) => (changes[g] || []).some((e) => e.care))
  const total = groups.reduce((n, [g]) => n + visible(g).length, 0)
  return (
    <div className="mx-chg">
      <h4 className="mx-h">{t('matrix.changesTitle', 'Projected changes')}</h4>
      <p className="rc-note">{t('matrix.changesSub', 'Where a life-area is about to turn — from daśā junctions, transits and sharp swings landing on its significators. A window and a direction, not a fated event.')}</p>
      {groups.map(([g, label]) => visible(g).length > 0 && (
        <div key={g} className="mx-chg-group">
          <div className="mx-chg-gh">{label}</div>
          <ul className="mx-chg-list">
            {visible(g).map((e, i) => (
              <li key={i} className={'dir-' + e.direction + (e.care ? ' care' : '')}>
                <span className="mx-chg-dir">{CHANGE_DIR[e.direction]}</span>
                <div className="mx-chg-body">
                  <div className="mx-chg-top">
                    <span className="mx-chg-label">{t('matrix.change.' + e.key + '.' + e.direction, e.label)}</span>
                    <span className="mx-chg-date">{ym(e.from)}{e.from !== e.to ? ' – ' + ym(e.to) : ''}</span>
                  </div>
                  <div className="mx-chg-note">{t('matrix.changenote.' + e.key, e.note)}</div>
                  <div className="mx-chg-meta">
                    <span className="mx-ev-cf">{Math.round(e.cf * 100)}%</span>
                    <span className="mx-chg-drv">{t('matrix.trig.' + e.triggerType, e.triggerType)} · {nm(e.maha)}–{nm(e.antar)}</span>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      ))}
      {total === 0 && <p className="rc-note">{t('matrix.nochanges', 'No notable changes flagged in the next three years.')}</p>}
      {anyCare && (
        <label className="mx-chg-care">
          <input type="checkbox" checked={showCare} onChange={(e) => setShowCare(e.target.checked)} />
          <span>{t('matrix.showcare', 'Show sensitive relationship & wellbeing signals (♥) — offered as care and attention, never as verdicts about another person or a forecast of loss.')}</span>
        </label>
      )}
      <p className="mx-prov">{changes.note}</p>
    </div>
  )
}

// Calibration — log real past events, backtest the projection against them for a
// personal hit-rate. Events persist in localStorage keyed to the chart.
function MatrixCalibration({ date, time, place, t }) {
  const storeKey = `dvz-cal-${date}|${time}|${place && place.latitude}|${place && place.longitude}`
  const [events, setEvents] = useState(() => {
    try { return JSON.parse(localStorage.getItem(storeKey) || '[]') } catch { return [] }
  })
  const [month, setMonth] = useState('')
  const [theme, setTheme] = useState('career')
  const [pol, setPol] = useState(1)
  const [bt, setBt] = useState(null)
  const [busy, setBusy] = useState(false)

  const persist = (list) => {
    setEvents(list); setBt(null)
    try { localStorage.setItem(storeKey, JSON.stringify(list)) } catch { /* private mode */ }
  }
  const add = () => {
    if (!/^\d{4}-\d{2}$/.test(month)) return
    persist([...events, { date: month, key: theme, polarity: pol }])
    setMonth('')
  }
  const run = () => {
    if (!events.length || busy) return
    setBusy(true)
    fetch(`${API}/api/matrix/backtest`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, time, latitude: place.latitude, longitude: place.longitude, timezone: place.timezone, events }),
    })
      .then((r) => r.json()).then((j) => { if (!j.error) setBt(j) })
      .catch(() => {}).finally(() => setBusy(false))
  }

  return (
    <div className="mx-cal">
      <h4 className="mx-h">{t('matrix.calib', 'Calibration · your events')}</h4>
      <p className="rc-note">{t('matrix.calibsub', 'Log real events to backtest the projection against your own life — a personal hit-rate, kept on this device. An honest track record, not proof.')}</p>
      <div className="mx-cal-form">
        <input type="month" className="mx-cal-in" value={month} onChange={(e) => setMonth(e.target.value)} aria-label={t('matrix.calmonth', 'Month')} />
        <select className="mx-cal-sel" value={theme} onChange={(e) => setTheme(e.target.value)}>
          {THEME_KEYS.map((k) => <option key={k} value={k}>{t('matrix.theme.' + k, k)}</option>)}
        </select>
        <div className="mx-cal-pol">
          <button type="button" className={pol > 0 ? 'on' : ''} onClick={() => setPol(1)}>{t('matrix.went.good', 'went well')}</button>
          <button type="button" className={pol < 0 ? 'on' : ''} onClick={() => setPol(-1)}>{t('matrix.went.bad', 'went badly')}</button>
        </div>
        <button type="button" className="mx-cal-add" onClick={add}>{t('matrix.addevent', 'Add')}</button>
      </div>
      {events.length > 0 && (
        <ul className="mx-cal-list">
          {events.map((e, i) => (
            <li key={i}>
              <span className={e.polarity > 0 ? 'good' : 'bad'}>{e.polarity > 0 ? '▲' : '▼'}</span>
              <span className="mx-cal-d">{e.date}</span>
              <span className="mx-cal-t">{t('matrix.theme.' + e.key, e.key)}</span>
              <button type="button" className="mx-cal-x" onClick={() => persist(events.filter((_, j) => j !== i))} aria-label="remove">×</button>
            </li>
          ))}
        </ul>
      )}
      {events.length > 0 && (
        <button type="button" className="mx-mc-btn" onClick={run} disabled={busy}>
          {busy ? t('matrix.backtesting', 'Backtesting…') : t('matrix.dobacktest', 'Backtest')}
        </button>
      )}
      {bt && bt.summary.n > 0 && (
        <div className="mx-cal-out">
          <div className="mx-cal-score">
            <b>{Math.round(bt.summary.hitRate * 100)}%</b> {t('matrix.matched', 'matched')} ({bt.summary.n}) ·
            {' '}{t('matrix.timingagree', 'timing')} {Math.round(bt.summary.timingHitRate * 100)}%
          </div>
          <ul className="mx-cal-res">
            {bt.events.map((e, i) => (
              <li key={i} className={e.hit ? 'hit' : 'miss'}>
                <span className="mx-cal-d">{e.date}</span>
                <span className="mx-cal-t">{t('matrix.theme.' + e.key, e.key)}</span>
                <span>{e.polarity > 0 ? '▲' : '▼'}</span>
                <span className="mono mx-cal-v">{e.v >= 0 ? '+' : ''}{e.v}</span>
                <span className="mx-cal-hit">{e.hit ? '✓' : '✗'}</span>
              </li>
            ))}
          </ul>
          <p className="mx-prov">{bt.note}</p>
        </div>
      )}
    </div>
  )
}

export default function MatrixPanel({ date, time, place, namer }) {
  const { t } = useLang()
  const [data, setData] = useState(null)
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const [open, setOpen] = useState(null)
  const [mc, setMc] = useState(null)
  const [mcBusy, setMcBusy] = useState(false)
  const [mcMin, setMcMin] = useState(4)

  useEffect(() => {
    if (!date || !time || !place) return
    let alive = true
    setBusy(true); setErr(''); setData(null); setOpen(null); setMc(null)
    fetch(`${API}/api/matrix`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, time, latitude: place.latitude, longitude: place.longitude, timezone: place.timezone }),
    })
      .then((r) => r.json())
      .then((j) => { if (!alive) return; if (j.error) setErr(j.error); else setData(j) })
      .catch((e) => alive && setErr(String(e)))
      .finally(() => alive && setBusy(false))
    return () => { alive = false }
  }, [date, time, place])

  const runMc = (minutes) => {
    if (!date || !time || !place || mcBusy) return
    setMcBusy(true)
    fetch(`${API}/api/matrix/montecarlo`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, time, latitude: place.latitude, longitude: place.longitude, timezone: place.timezone, minutes }),
    })
      .then((r) => r.json())
      .then((j) => { if (!j.error) setMc(j) })
      .catch(() => {})
      .finally(() => setMcBusy(false))
  }

  if (!date || !time || !place) return null
  const nm = (k) => (namer && namer.grahaKey ? namer.grahaKey(k) : k)
  const bandLbl = (b) => t('matrix.band.' + b, b)

  return (
    <section className="table-panel mx-panel" id="rg-matrix" style={{ '--tf-accent': '#a9791f' }}>
      <h3>{t('matrix.title', 'Chart matrix — domain verdicts')}</h3>
      <p className="rc-note">{t('matrix.sub', 'Each life-domain read as a weighted, cited composite of the natal factor web. A balance from −1 to +1; the band tints a ledger you can open — an indication, not a fated verdict.')}</p>
      {busy && <p className="rc-note">{t('matrix.loading', 'Computing the matrix…')}</p>}
      {err && <p className="rc-note pc-err">{err}</p>}

      {data && (
        <>
          <h4 className="mx-h">{t('matrix.themes', 'Life themes')}</h4>
          <div className="mx-themes">
            {data.themes.map((th) => {
              const on = open === 't:' + th.key
              return (
                <div className={'mx-card' + (on ? ' on' : '')} key={th.key}>
                  <button type="button" className="mx-card-h" aria-expanded={on} onClick={() => setOpen(on ? null : 't:' + th.key)}>
                    <span className="mx-band" style={{ background: BAND_C[th.band] }}>{sv(th.net)}</span>
                    <span className="mx-card-name">{t('matrix.theme.' + th.key, th.name)}</span>
                    <span className="mx-bandlbl">{bandLbl(th.band)}</span>
                    <span className="mx-caret">{on ? '−' : '+'}</span>
                  </button>
                  {on && <Ledger comps={th.components} nm={nm} t={t} />}
                </div>
              )
            })}
          </div>

          <h4 className="mx-h">{t('matrix.bhavas', 'Bhāva decomposition')}</h4>
          <div className="mx-heatwrap">
            <table className="mx-heat">
              <thead>
                <tr>
                  <th>{t('matrix.hcol', 'House')}</th><th>{t('matrix.lcol', 'Lord')}</th>
                  <th>{t('matrix.lord', 'Lord')}<small>.40</small></th>
                  <th>{t('matrix.occ', 'Occ.')}<small>.25</small></th>
                  <th>{t('matrix.asp', 'Asp.')}<small>.20</small></th>
                  <th>{t('matrix.karaka', 'Kār.')}<small>.15</small></th>
                  <th>{t('matrix.net', 'Net')}</th>
                </tr>
              </thead>
              <tbody>
                {data.bhavas.map((b) => {
                  const cell = (factor) => {
                    const c = b.components.find((x) => x.factor === factor)
                    const v = c ? c.value : null
                    return <td className="mx-cell" style={{ background: v == null ? 'transparent' : netColor(v) }}>{v == null ? '·' : sv(v)}</td>
                  }
                  return (
                    <tr key={b.house}>
                      <td className="mx-hnum">{b.house}</td>
                      <td className="mx-hlord">{nm(b.lord)}</td>
                      {cell('lord')}{cell('occupants')}{cell('aspects')}{cell('karaka')}
                      <td className="mx-net" style={{ background: BAND_C[b.band] }} title={bandLbl(b.band)}>{sv(b.net)}</td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>

          <div className="mx-legend">
            {['thriving', 'supported', 'mixed', 'stressed', 'afflicted'].map((bd) => (
              <span key={bd} className="mx-leg"><i style={{ background: BAND_C[bd] }} />{bandLbl(bd)}</span>
            ))}
          </div>
          <h4 className="mx-h">{t('matrix.web', 'Aspect web')}</h4>
          {data.nodes && data.edges && (
            <MatrixGraph nodes={data.nodes} edges={data.edges.aspects || []} nm={nm} t={t} />
          )}

          {data.timeline && (
            <>
              <h4 className="mx-h">{t('matrix.timeline', 'Near future')}</h4>
              {data.ashtakavarga && <MatrixAvStrip av={data.ashtakavarga} t={t} />}
              <MatrixTimeline
                timeline={data.timeline}
                themeName={Object.fromEntries((data.themes || []).map((th) => [th.key, th.name]))}
                nm={nm}
                t={t}
                mc={mc}
                onRefine={runMc}
                mcBusy={mcBusy}
                mcMin={mcMin}
                setMcMin={setMcMin}
              />
              {data.changes && <MatrixChanges changes={data.changes} nm={nm} t={t} />}
              <MatrixCalibration date={date} time={time} place={place} t={t} />
            </>
          )}

          <p className="mx-prov">{data.provenance?.note}</p>
        </>
      )}
    </section>
  )
}
