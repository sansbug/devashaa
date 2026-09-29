/**
 * Chart-analysis matrix — per-chart domain verdicts, in three views.
 *
 *   Overview  — the natal balance: twelve life domains on a wheel, each opening
 *               to its cited, weighted ledger; the bhāva decomposition and the
 *               planetary-aspect grid underneath.
 *   Forecast  — the near future month by month: a domain × month heatmap under
 *               the running daśā ribbon, the strongest windows, projected
 *               events and typed changes, and the calibration harness.
 *   Life arc  — the whole trajectory from birth with its turning points, the
 *               transit-strength strip and the birth-time confidence band.
 *
 * Every number is an iṣṭa/kaṣṭa balance in [-1,+1]; a band is a tint over a
 * visible ledger, never a black box — an indication from classical measures,
 * not a fated verdict. The graphics changed in this revision; the numbers, the
 * citations and the refusals did not.
 */
import { useState, useEffect, useMemo } from 'react'
import { API } from './config.js'
import { useLang } from './LangContext.jsx'
import DomainIcon from './ProjectionIcons.jsx'
import Glyph from './DashaGlyphs.jsx'

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
const polColor = (p) => (p === 1 ? _mix(NEUTRAL, ISTA, 1) : p === -1 ? _mix(NEUTRAL, KASTA, 1) : `rgb(${NEUTRAL.join(',')})`)
const signColor = (v) => (v == null ? 'var(--dim)' : v > 0.02 ? BAND_C.thriving : v < -0.02 ? BAND_C.afflicted : BAND_C.mixed)
const pct = (w) => (w == null ? '' : Math.round(w * 100) + '%')
const sv = (v) => (v == null ? '—' : (v >= 0 ? '+' : '') + v.toFixed(2))
const ym = (d) => (d || '').slice(0, 7)

const GRAHAS = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn', 'rahu', 'ketu']
const THEME_KEYS = ['self', 'wealth', 'career', 'marriage', 'children', 'health',
  'education', 'home', 'fortune', 'enemies', 'foreign', 'longevity']
const CLOCK_LABEL = { vims: 'Viṁśottarī', goch: 'gochara', chara: 'chara daśā', trig: 'double transit' }
const CHANGE_DIR = { up: '▲', down: '▼', shift: '↻', care: '♥' }

const YEAR_MS = 365.2425 * 86400000
const DAY = 86400000

function BphsQuote({ b, t }) {
  if (!b) return null
  const tag = b.kind === 'house' ? t('matrix.bhps.house', 'BPHS · house') : t('matrix.bhps.dasha', 'BPHS · daśā')
  return (
    <div className="mx-bhps">
      <span className="mx-bhps-tag">{tag}</span>
      <span className="mx-bhps-txt">{b.text} <span className="mx-bhps-cite">— {b.cite}</span></span>
    </div>
  )
}

// ════════════════════════════════════════════════════════════════════════════
//  Overview
// ════════════════════════════════════════════════════════════════════════════

/** Twelve domains on a wheel. Bars rise from the −1 ring, so a value of 0 is
 *  the middle ring and +1 the rim; the fill is the band, the same tint the
 *  ledger uses. Sector order is house order, clockwise from the top. The
 *  geometry fills the card: the wheel is the picture, the labels sit just
 *  outside the rim, and the number badges ride on the rim itself. */
const WHEEL_C = { thriving: '#1f8a5f', supported: '#6dbb8c', mixed: '#d9a83c', stressed: '#e0806a', afflicted: '#c23f36' }
const wheelSign = (v) => (v == null ? '#8a8f99' : v > 0.02 ? WHEEL_C.thriving : v < -0.02 ? WHEEL_C.afflicted : WHEEL_C.mixed)

function LifeWheel({ themes, open, onOpen, t }) {
  const W = 880, H = 704, CX = 440, CY = 344
  const RH = 72          // hub
  const R0 = 88          // the −1 ring, where every bar starts
  const R1 = 232         // the +1 ring
  const RR = 244         // the rim the number badges ride on
  const RL = 268         // where the labels begin
  const N = themes.length
  const arc = 360 / N
  const rad = (deg) => (deg * Math.PI) / 180
  const rOf = (v) => R0 + ((Math.max(-1, Math.min(1, v)) + 1) / 2) * (R1 - R0)
  const pt = (r, deg) => [CX + r * Math.cos(rad(deg)), CY + r * Math.sin(rad(deg))]
  const wedge = (r0, r1, a0, a1) => {
    const [x0, y0] = pt(r1, a0), [x1, y1] = pt(r1, a1)
    const [x2, y2] = pt(r0, a1), [x3, y3] = pt(r0, a0)
    const large = a1 - a0 > 180 ? 1 : 0
    return `M${x0.toFixed(1)},${y0.toFixed(1)} A${r1},${r1} 0 ${large} 1 ${x1.toFixed(1)},${y1.toFixed(1)} `
         + `L${x2.toFixed(1)},${y2.toFixed(1)} A${r0},${r0} 0 ${large} 0 ${x3.toFixed(1)},${y3.toFixed(1)} Z`
  }
  const mean = themes.reduce((s, th) => s + (th.net || 0), 0) / N
  // ring labels sit on the spoke between sectors 1 and 2, clear of any bar
  const ringA = -90 + arc / 2
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="pj-wheel" role="img" aria-label={t('pj.wheel.title', 'Life wheel')}>
      {/* rim + sector washes: the halves read before any bar does */}
      <circle cx={CX} cy={CY} r={RR} className="rim" />
      {themes.map((th, i) => {
        const a0 = -90 - arc / 2 + i * arc, a1 = a0 + arc
        return <path key={'w' + i} d={wedge(R0, RR, a0, a1)} fill={wheelSign(th.net)} fillOpacity="0.09" />
      })}
      {[-1, 0, 0.5, 1].map((v) => (
        <circle key={v} cx={CX} cy={CY} r={rOf(v)} className={'ring' + (v === 0 ? ' zero' : '')} />
      ))}
      {themes.map((_, i) => {
        const a = -90 - arc / 2 + i * arc
        const [x0, y0] = pt(R0, a), [x1, y1] = pt(RR, a)
        return <line key={'s' + i} x1={x0} y1={y0} x2={x1} y2={y1} className="spoke" />
      })}
      {[-1, 0, 0.5, 1].map((v) => {
        const [x, y] = pt(rOf(v) + (v === 1 ? -9 : 7), ringA)
        return <text key={'l' + v} x={x + 4} y={y + 4} className="ringlbl">{v > 0 ? '+' : ''}{v.toFixed(1)}</text>
      })}
      {themes.map((th, i) => {
        const mid = -90 + i * arc
        const a0 = mid - arc * 0.32, a1 = mid + arc * 0.32
        const on = open === th.key
        const c = Math.cos(rad(mid)), sn = Math.sin(rad(mid))
        const anchor = c > 0.3 ? 'start' : c < -0.3 ? 'end' : 'middle'
        const [nx, ny] = pt(RR, mid)
        const [lx, ly] = pt(RL, mid)
        // three stacked lines: icon, name, value — nudged so top/bottom labels
        // stack away from the rim and side labels centre on the spoke
        const dy = sn < -0.3 ? -64 : sn > 0.3 ? 6 : -20
        const ix = anchor === 'start' ? lx : anchor === 'end' ? lx - 18 : lx - 9
        return (
          <g key={th.key} className={'sector' + (on ? ' on' : '')} onClick={() => onOpen(on ? null : th.key)}
             role="button" tabIndex={0} onKeyDown={(e) => (e.key === 'Enter' || e.key === ' ') && onOpen(on ? null : th.key)}>
            <title>{th.name} · {sv(th.net)}</title>
            <path d={wedge(R0, RR, mid - arc / 2, mid + arc / 2)} fill="transparent" />
            <path className="bar" d={wedge(R0 + 2, rOf(th.net), a0, a1)} fill={WHEEL_C[th.band] || wheelSign(th.net)} />
            <circle cx={nx} cy={ny} r="13" className="lbl-numc" />
            <text x={nx} y={ny + 4} textAnchor="middle" className="lbl-num">{i + 1}</text>
            <g transform={`translate(${ix.toFixed(1)},${(ly + dy).toFixed(1)})`} className="lbl-ico">
              <DomainIcon k={th.key} size={18} />
            </g>
            <text x={lx} y={ly + dy + 34} textAnchor={anchor} className="lbl-name">{th.name.split(' · ')[0]}</text>
            {th.name.includes(' · ') && (
              <text x={lx} y={ly + dy + 48} textAnchor={anchor} className="lbl-name2">{th.name.split(' · ').slice(1).join(' · ')}</text>
            )}
            <text x={lx} y={ly + dy + (th.name.includes(' · ') ? 66 : 52)} textAnchor={anchor} className="lbl-val" fill={wheelSign(th.net)}>{sv(th.net)}</text>
          </g>
        )
      })}
      <circle cx={CX} cy={CY} r={RH} className="hub" />
      <text x={CX} y={CY - 10} textAnchor="middle" className="hub-t">{t('pj.wheel.centre', 'Natal balance')}</text>
      <rect x={CX - 30} y={CY + 2} width="60" height="24" rx="7" fill={wheelSign(mean)} />
      <text x={CX} y={CY + 19} textAnchor="middle" className="hub-v" fill="#fff">{sv(mean)}</text>
      <text x={CX} y={CY + 44} textAnchor="middle" className="hub-n">{t('pj.wheel.centre.note', 'mean of the twelve')}</text>
    </svg>
  )
}

function factorLabel(c, nm, t) {
  switch (c.factor) {
    case 'bhava': return `${t('matrix.hcol', 'House')} (${c.house})`
    case 'lord': return t('matrix.lord', 'Lord') + (c.graha ? ` · ${nm(c.graha)}` : '')
    case 'occupants': return t('matrix.occ', 'Occupancy')
    case 'aspects': return t('matrix.asp', 'Aspects')
    case 'karaka':
    case 'sthira_karaka': return t('matrix.karaka', 'Kāraka') + (c.graha ? ` · ${nm(c.graha)}` : '')
    default: return c.factor
  }
}

/** The opened domain: value and band, the weighted ledger as bars, the cites. */
function DomainDetail({ th, nm, t, bandLbl, onClose }) {
  const [tab, setTab] = useState('breakdown')
  if (!th) {
    return (
      <div className="pj-card pj-detail">
        <p className="pj-sub" style={{ margin: 0 }}>{t('pj.detail.hint', 'Select a domain on the wheel to see how its number is built.')}</p>
      </div>
    )
  }
  const cites = []
  const seen = new Set()
  for (const c of th.components) {
    const k = (c.citation || '') + '|' + (c.detail || '')
    if (c.citation && !seen.has(k)) { seen.add(k); cites.push(c) }
  }
  return (
    <div className="pj-card pj-detail">
      <div className="pj-detail-head">
        <DomainIcon k={th.key} size={20} />
        <h4>{th.name}</h4>
        <button type="button" className="pj-detail-x" onClick={onClose} aria-label={t('pj.detail.close', 'Close')}>×</button>
      </div>
      <div className="pj-detail-pills">
        <span className="pj-val" style={{ background: BAND_C[th.band] || netColor(th.net) }}>{sv(th.net)}</span>
        <span className="pj-bandpill">{bandLbl(th.band)}</span>
      </div>
      <div className="pj-detail-tabs">
        <button type="button" className={tab === 'breakdown' ? 'on' : ''} onClick={() => setTab('breakdown')}>{t('pj.detail.breakdown', 'Breakdown')}</button>
        <button type="button" className={tab === 'sources' ? 'on' : ''} onClick={() => setTab('sources')}>{t('pj.detail.sources', 'Classical basis')}</button>
      </div>
      {tab === 'breakdown' ? (
        <>
          <table className="pj-ledger">
            <thead><tr><th>{t('pj.detail.factor', 'Factor')}</th><th>{t('pj.detail.contrib', 'Contribution')}</th><th /><th>{t('pj.detail.weight', 'Weight')}</th></tr></thead>
            <tbody>
              {th.components.map((c, i) => (
                <tr key={i} title={c.detail || ''}>
                  <td>{factorLabel(c, nm, t)}</td>
                  <td className="n" style={{ color: signColor(c.value) }}>{sv(c.value)}</td>
                  <td>
                    <div className="pj-bar"><i style={{ width: `${Math.round(Math.abs(c.value || 0) * 100)}%`, background: signColor(c.value) }} /></div>
                  </td>
                  <td className="n">{pct(c.effWeight != null ? c.effWeight : c.weight)}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <div className="pj-net">
            <div><b>{t('pj.detail.net', 'Net indication')}</b><small>{t('pj.detail.net.sub', 'weighted composite')}</small></div>
            <span className="pj-val" style={{ background: BAND_C[th.band] || netColor(th.net) }}>{sv(th.net)}</span>
          </div>
        </>
      ) : (
        <ul className="pj-cites">
          {cites.map((c, i) => (
            <li key={i}><b>{factorLabel(c, nm, t)}</b> — <span className="c">{c.citation}</span>{c.detail ? ` · ${c.detail}` : ''} <span className="c">[{c.tier}]</span></li>
          ))}
        </ul>
      )}
    </div>
  )
}

function BhavaMatrix({ bhavas, nm, t, bandLbl }) {
  return (
    <div className="pj-card">
      <h4>{t('pj.bhava.title', 'Bhāva decomposition')}</h4>
      <p className="pj-sub">{t('pj.bhava.sub', 'Each house from its four cited contributors, −1 to +1.')}</p>
      <div className="mx-heatwrap">
        <table className="pj-heat">
          <thead>
            <tr>
              <th>{t('matrix.hcol', 'House')}</th><th>{t('matrix.lcol', 'Lord')}</th>
              <th>{t('matrix.lord', 'Lord')}</th><th>{t('matrix.occ', 'Occ.')}</th>
              <th>{t('matrix.asp', 'Asp.')}</th><th>{t('matrix.karaka', 'Kār.')}</th><th>{t('matrix.net', 'Net')}</th>
            </tr>
          </thead>
          <tbody>
            {bhavas.map((b) => {
              const cell = (factor) => {
                const c = b.components.find((x) => x.factor === factor)
                const v = c ? c.value : null
                return <td key={factor} className={'v' + (v == null ? ' faint' : '')} style={v == null ? undefined : { background: netColor(v) }} title={c?.detail || ''}>{v == null ? '·' : sv(v)}</td>
              }
              return (
                <tr key={b.house}>
                  <td className="hn">{b.house}</td>
                  <td className="lord">{nm(b.lord)}</td>
                  {cell('lord')}{cell('occupants')}{cell('aspects')}{cell('karaka')}
                  <td className="v" style={{ background: BAND_C[b.band] }} title={bandLbl(b.band)}>{sv(b.net)}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      <div className="pj-legend">
        {['thriving', 'supported', 'mixed', 'stressed', 'afflicted'].map((bd) => (
          <span key={bd}><i style={{ background: BAND_C[bd] }} />{bandLbl(bd)}</span>
        ))}
      </div>
    </div>
  )
}

function AspectMatrix({ edges, nodes, nm, t }) {
  const by = {}
  for (const e of edges) by[e.from + '|' + e.to] = e
  const ab = (k) => nm(k).slice(0, 2)
  return (
    <div className="pj-card">
      <h4>{t('pj.asp.title', 'Planetary aspects')}</h4>
      <p className="pj-sub">{t('pj.asp.sub', 'Rows aspect columns.')}</p>
      <div className="mx-heatwrap">
        <table className="pj-asp">
          <thead>
            <tr><th />{GRAHAS.map((g) => <th key={g}><Glyph lord={g} size={13} />{ab(g)}</th>)}</tr>
          </thead>
          <tbody>
            {GRAHAS.map((a) => (
              <tr key={a}>
                <td className="rh"><Glyph lord={a} size={13} /> {nm(a)}</td>
                {GRAHAS.map((b) => {
                  if (a === b) return <td key={b} className="self">–</td>
                  const e = by[a + '|' + b]
                  if (!e) return <td key={b} title={`${nm(a)} → ${nm(b)} · ${t('pj.asp.none', 'No aspect')}`}><span className="dot none" /></td>
                  const s = (0.45 + e.strength * 0.4).toFixed(2)
                  return (
                    <td key={b} title={`${nm(a)} → ${nm(b)} · ${Math.round(e.strength * 100)}%`}>
                      <span className="dot" style={{ width: s + 'rem', height: s + 'rem', background: polColor(nodes[a]?.polarity) }} />
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="pj-legend">
        <span><i className="dot" style={{ background: polColor(1) }} />{t('pj.asp.benefic', 'Benefic dṛṣṭi')}</span>
        <span><i className="dot" style={{ background: polColor(-1) }} />{t('pj.asp.malefic', 'Malefic dṛṣṭi')}</span>
        <span><i className="dot" style={{ border: '1.5px solid var(--line)' }} />{t('pj.asp.none', 'No aspect')}</span>
        <span>– {t('pj.asp.self', 'Self')}</span>
      </div>
    </div>
  )
}

function Overview({ data, nm, t, bandLbl, open, setOpen }) {
  const themes = data.themes
  const sorted = [...themes].sort((a, b) => b.net - a.net)
  const strong = sorted.slice(0, 3)
  const weak = sorted.slice(-3).reverse()
  const near = [...themes].sort((a, b) => Math.abs(a.net) - Math.abs(b.net)).slice(0, 3)
  const names = (l) => l.map((x) => x.name.split(' · ')[0].toLowerCase()).join(', ')
  const nearNames = themes.filter((x) => Math.abs(x.net) < 0.12).map((x) => x.name.split(' · ')[0].toLowerCase())
  const prose = (nearNames.length
    ? t('pj.balance.prose', 'The chart shows support for {up}, with pressure around {down}. {near} sit near balance.')
    : t('pj.balance.prose.nonear', 'The chart shows support for {up}, with pressure around {down}.'))
    .replace('{up}', names(strong)).replace('{down}', names(weak))
    .replace('{near}', nearNames.join(', ').replace(/^./, (c) => c.toUpperCase()))
  const openTheme = themes.find((x) => x.key === open)
  // open on the most challenged domain: an empty detail panel next to a wheel
  // answers a question nobody asked
  useEffect(() => { if (open == null && weak.length) setOpen(weak[0].key) }, [])  // eslint-disable-line react-hooks/exhaustive-deps
  const Kpi = ({ title, glyph, color, list }) => (
    <div className="pj-card pj-kpi">
      <h5><span className="pj-kpi-dot" style={{ background: color }}>{glyph}</span>{title}</h5>
      {list.map((x) => (
        <div className="pj-kpi-row" key={x.key}>
          <span><DomainIcon k={x.key} size={13} />{x.name.split(' · ')[0]}</span>
          <b style={{ color: signColor(x.net) }}>{sv(x.net)}</b>
        </div>
      ))}
    </div>
  )
  return (
    <>
      <div className="pj-balance">
        <div className="pj-card pj-balance-prose">
          <h4>{t('pj.balance.title', 'Your natal balance')}</h4>
          {prose}
        </div>
        <Kpi title={t('pj.balance.strong', 'Strongest support')} glyph="↑" color={WHEEL_C.thriving} list={strong} />
        <Kpi title={t('pj.balance.near', 'Near balance')} glyph="≈" color={WHEEL_C.mixed} list={near} />
        <Kpi title={t('pj.balance.weak', 'Most challenged')} glyph="↓" color={WHEEL_C.afflicted} list={weak} />
      </div>

      <div className="pj-wheel-row">
        <div className="pj-card">
          <h4>{t('pj.wheel.title', 'Life wheel')}</h4>
          <p className="pj-sub">{t('pj.wheel.sub', 'Twelve life domains from the natal chart. Tap a domain to open its ledger.')}</p>
          <LifeWheel themes={themes} open={open} onOpen={setOpen} t={t} />
          <div className="pj-wheel-legend">
            {['thriving', 'supported', 'mixed', 'stressed', 'afflicted'].map((bd) => (
              <span key={bd}><i style={{ background: WHEEL_C[bd] }} />{bandLbl(bd)}</span>
            ))}
          </div>
        </div>
        <DomainDetail th={openTheme} nm={nm} t={t} bandLbl={bandLbl} onClose={() => setOpen(null)} />
      </div>

      <div className="pj-grid2">
        <BhavaMatrix bhavas={data.bhavas} nm={nm} t={t} bandLbl={bandLbl} />
        {data.nodes && data.edges && <AspectMatrix edges={data.edges.aspects || []} nodes={data.nodes} nm={nm} t={t} />}
      </div>
    </>
  )
}

// ════════════════════════════════════════════════════════════════════════════
//  Forecast
// ════════════════════════════════════════════════════════════════════════════

function Heatmap({ steps, themes, nm, t }) {
  // year header spans + daśā ribbon segments (by antardaśā, the finer clock)
  const years = []
  for (const s of steps) {
    const y = s.date.slice(0, 4)
    if (years.length && years[years.length - 1].y === y) years[years.length - 1].n++
    else years.push({ y, n: 1 })
  }
  const segs = []
  for (const s of steps) {
    const last = segs[segs.length - 1]
    if (last && last.maha === s.maha && last.antar === s.antar) last.n++
    else segs.push({ maha: s.maha, antar: s.antar, n: 1 })
  }
  const cell = (v, cf, i) => (
    <td key={i} className="c" style={{ background: netColor(v), opacity: (0.32 + 0.68 * (cf ?? 1)).toFixed(2) }}
        title={`${steps[i].date.slice(0, 7)} · ${sv(v)}`} />
  )
  return (
    <div className="pj-card">
      <h4>{t('pj.heat.title', 'Monthly forecast')}</h4>
      <p className="pj-sub">{t('pj.heat.sub', 'Relative strength across the domains, month by month.')}</p>
      <div className="pj-heatwrap">
        <table className="pj-hm">
          <thead>
            <tr><th /><td colSpan={steps.length} style={{ padding: 0 }}>
              <table style={{ width: '100%', borderCollapse: 'separate', borderSpacing: '1.5px 0' }}><tbody><tr>
                {segs.map((sg, i) => (
                  <td key={i} className="rib" colSpan={sg.n} title={`${nm(sg.maha)} – ${nm(sg.antar)}`}>{nm(sg.antar)}</td>
                ))}
              </tr></tbody></table>
            </td></tr>
            <tr><th />{years.map((yr) => <th key={yr.y} className="yr" colSpan={yr.n}>{yr.y}</th>)}</tr>
            <tr><th style={{ textAlign: 'left' }}>{t('pj.heat.domain', 'Life domain')}</th>
              {steps.map((s, i) => <th key={i}>{i % 3 === 0 ? s.date.slice(5, 7) : ''}</th>)}</tr>
          </thead>
          <tbody>
            <tr className="overall"><td className="name">{t('matrix.overall', 'Overall')}</td>
              {steps.map((s, i) => cell(s.overall, s.overallCf, i))}</tr>
            {themes.map((th) => (
              <tr key={th.key}>
                <td className="name"><DomainIcon k={th.key} size={13} />{t('matrix.theme.' + th.key, th.name)}</td>
                {steps.map((s, i) => cell(s.themes[th.key], s.conv ? s.conv[th.key] : 1, i))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="pj-hm-legend">
        <span><i style={{ background: netColor(0.8) }} />{t('pj.heat.supportive', 'Supportive')}</span>
        <span><i style={{ background: netColor(0) }} />{t('pj.heat.neutral', 'Neutral')}</span>
        <span><i style={{ background: netColor(-0.8) }} />{t('pj.heat.challenging', 'Challenging')}</span>
      </div>
    </div>
  )
}

function confLabel(cf, t) {
  if (cf >= 0.75) return t('pj.events.conf.high', 'High confidence')
  if (cf >= 0.45) return t('pj.events.conf.mod', 'Moderate')
  return t('pj.events.conf.low', 'Low')
}

function Forecast({ data, nm, t, themeName, mc, runMc, mcBusy, mcMin, setMcMin, date, time, place }) {
  const tl = data.timeline
  const steps = tl.steps
  const first = steps[0], last = steps[steps.length - 1]
  const nextMaha = steps.find((s) => s.maha !== first.maha)
  const nextAntar = steps.find((s) => s.antar !== first.antar || s.maha !== first.maha)
  const meanOverall = steps.reduce((a, s) => a + (s.overall || 0), 0) / steps.length
  const tone = meanOverall > 0.12 ? 'supportive' : meanOverall < -0.12 ? 'challenging' : 'mixed'
  const toneColor = tone === 'supportive' ? BAND_C.thriving : tone === 'challenging' ? BAND_C.afflicted : BAND_C.mixed
  const events = [...(tl.events || [])].sort((a, b) => b.intensity - a.intensity)
  const survOf = {}
  for (const e of (mc?.events || [])) survOf[e.key + '|' + e.from] = e.survival
  const evLabel = (e) => t('matrix.event.' + e.key + '.' + (e.good ? 'good' : 'bad'), themeName[e.key] || e.key)
  const Chip = ({ ico, k, v, s }) => (
    <div className="pj-chip">
      <span className="pj-chip-ico">{ico}</span>
      <div style={{ minWidth: 0 }}>
        <div className="pj-chip-k">{k}</div>
        <div className="pj-chip-v">{v}</div>
        {s && <div className="pj-chip-s">{s}</div>}
      </div>
    </div>
  )
  return (
    <>
      <div className="pj-chips">
        <Chip ico="▦" k={t('pj.fc.range', 'Time range')} v={`${first.date.slice(0, 4)} – ${last.date.slice(0, 4)}`} />
        <div className="pj-chip">
          <span className="pj-chip-ico">◷</span>
          <div style={{ minWidth: 0 }}>
            <div className="pj-chip-k">{t('pj.fc.refine', 'Refine birth time')}</div>
            <div className="pj-chip-v">
              <select value={mcMin} onChange={(e) => setMcMin(+e.target.value)} disabled={mcBusy} aria-label={t('pj.fc.refine', 'Refine birth time')}>
                {[2, 4, 8, 15, 30].map((m) => <option key={m} value={m}>±{m} min</option>)}
              </select>
              <button type="button" onClick={() => runMc(mcMin)} disabled={mcBusy}>
                {mcBusy ? t('pj.la.conf.running', 'Computing…') : t('pj.la.conf.run', 'Compute band')}
              </button>
            </div>
          </div>
        </div>
        <Chip ico={<Glyph lord={first.maha} size={16} />} k={t('pj.fc.current', 'Current daśā')}
              v={<>{nm(first.maha)} <span className="pj-chip-s">→</span> {nm(first.antar)}</>} />
        {(nextMaha || nextAntar) && (
          <Chip ico={<Glyph lord={(nextMaha || nextAntar)[nextMaha ? 'maha' : 'antar']} size={16} />}
                k={nextMaha ? t('pj.fc.next', 'Next daśā') : t('pj.fc.next.antar', 'Next antardaśā')}
                v={nm((nextMaha || nextAntar)[nextMaha ? 'maha' : 'antar'])}
                s={ym((nextMaha || nextAntar).date)} />
        )}
        <Chip ico={<span style={{ color: toneColor }}>●</span>} k={t('pj.fc.tone', 'Overall tone')}
              v={<span style={{ color: toneColor }}>{t('pj.fc.tone.' + tone, tone)}</span>} s={t('pj.fc.tone.note', 'mean of the monthly overall reading')} />
      </div>

      <div className="pj-fc-row">
        <Heatmap steps={steps} themes={data.themes} nm={nm} t={t} />
        <div className="pj-card pj-watch">
          <h4>{t('pj.watch.title', 'Key watch windows')}</h4>
          <p className="pj-sub">{t('pj.watch.sub', 'The strongest windows in the projection — indications, not appointments.')}</p>
          <ul>
            {events.slice(0, 6).map((e, i) => (
              <li key={i}>
                <span className={'d ' + (e.good ? 'up' : 'down')}>{e.good ? '▲' : '▼'}</span>
                <span className="l">{evLabel(e)}<span className="s">{nm(e.maha)}–{nm(e.antar)}{e.house ? ` · ${t('matrix.hcol', 'House')} ${e.house}` : ''}</span></span>
                <span className={'w ' + (e.good ? 'up' : 'down')}>{ym(e.from)}{e.from !== e.to ? ` – ${ym(e.to)}` : ''}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {events.length > 0 && (
        <div className="pj-card" style={{ marginBottom: '.8rem' }}>
          <h4>{t('pj.events.title', 'Projected events')}</h4>
          <p className="pj-sub">{t('pj.events.sub', 'Where a domain crests or dips. Confidence is the clocks’ agreement.')}</p>
          <div className="pj-events">
            {events.slice(0, 4).map((e, i) => (
              <div className="pj-ev" key={i}>
                <span className={'d ' + (e.good ? 'up' : 'down')}>{e.good ? '▲' : '▼'}</span>
                <div>
                  <div className="pj-ev-top">
                    <b>{evLabel(e)}</b>
                    <span className="pj-conf">{confLabel(e.cf ?? 0, t)} {Math.round((e.cf ?? 0) * 100)}%</span>
                    {survOf[e.key + '|' + e.from] != null && <span className="pj-conf" title={t('matrix.survival', 'birth-time survival')}>{Math.round(survOf[e.key + '|' + e.from] * 100)}%↻</span>}
                    <span className="date">{ym(e.from)}{e.from !== e.to ? ` – ${ym(e.to)}` : ''}</span>
                  </div>
                  <div className="pj-ev-meta">{e.driver ? t('matrix.clock.' + e.driver, CLOCK_LABEL[e.driver]) + ' · ' : ''}{nm(e.maha)} → {nm(e.antar)}{e.bhps ? ` · ${t('pj.events.source', 'Source')}: ${e.bhps.cite}` : ''}</div>
                  {e.bhps && <div className="pj-ev-txt">{e.bhps.text}</div>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {data.changes && <Changes changes={data.changes} nm={nm} t={t} />}
      <Calibration date={date} time={time} place={place} t={t} />
    </>
  )
}

// Projected changes — typed transition-windows grouped by the three motives, with
// the two sensitive care-signals (♥) behind an opt-in toggle.
function Changes({ changes, nm, t }) {
  const [showCare, setShowCare] = useState(false)
  const groups = [
    ['health', t('matrix.motive.health', 'Health'), 'health'],
    ['wealthCareer', t('matrix.motive.wealthCareer', 'Wealth & Career'), 'wealth'],
    ['relationships', t('matrix.motive.relationships', 'Relationships'), 'marriage'],
  ]
  const visible = (g) => (changes[g] || []).filter((e) => showCare || !e.care)
  const anyCare = groups.some(([g]) => (changes[g] || []).some((e) => e.care))
  const total = groups.reduce((n, [g]) => n + visible(g).length, 0)
  return (
    <div className="pj-card" style={{ marginBottom: '.8rem' }}>
      <h4>{t('matrix.changesTitle', 'Projected changes')}</h4>
      <p className="pj-sub">{t('matrix.changesSub', 'Where a life-area is about to turn — a window and a direction, not a fated event.')}</p>
      <div className="pj-changes">
        {groups.map(([g, label, ico]) => visible(g).length > 0 && (
          <div key={g} className="pj-chg-card">
            <h5><DomainIcon k={ico} size={15} />{label}</h5>
            <ul>
              {visible(g).map((e, i) => (
                <li key={i} className={e.care ? 'care' : ''}>
                  <span className={e.direction === 'up' ? 'up' : e.direction === 'down' ? 'down' : ''}>{CHANGE_DIR[e.direction]}</span>
                  <span className="l">
                    <b>{t('matrix.change.' + e.key + '.' + e.direction, e.label)}</b>
                    <span>{t('matrix.changenote.' + e.key, e.note)} <span className="cf">· {Math.round(e.cf * 100)}%</span></span>
                  </span>
                  <span className="trig">{t('matrix.trig.' + e.triggerType, e.triggerType)}</span>
                  <span className="dt">{ym(e.from || e.date)}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
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
function Calibration({ date, time, place, t }) {
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
    <div className="pj-card mx-cal">
      <h4>{t('matrix.calib', 'Calibration · your events')}</h4>
      <p className="pj-sub">{t('matrix.calibsub', 'Log real events to backtest the projection against your own life — a personal hit-rate, kept on this device. An honest track record, not proof.')}</p>
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

// ════════════════════════════════════════════════════════════════════════════
//  Life arc
// ════════════════════════════════════════════════════════════════════════════

const ASPECT_DEFS = [
  ['wealth', ['wealthEarned', 'wealthReceived']],
  ['health', ['healthPhysical', 'healthMental']],
  ['relationships', ['relFamily', 'relOthers']],
]

/** Overall projection with its birth-time envelope, change markers on top. */
function ConfidenceCurve({ steps, t, envelope, events }) {
  const W = 680, H = 150, PX = 30, PY = 14
  const y = (v) => PY + (1 - (Math.max(-1, Math.min(1, v)) + 1) / 2) * (H - 2 * PY - 22)
  const x = (i) => PX + (i / Math.max(1, steps.length - 1)) * (W - PX - 8)
  const vpts = steps.map((s, i) => `${x(i).toFixed(1)},${y(s.overall).toFixed(1)}`).join(' ')
  const envMap = {}
  for (const e of (envelope || [])) envMap[e.date] = e
  const envPts = steps.map((s, i) => ({ i, e: envMap[s.date] })).filter((p) => p.e)
  const env = envPts.length > 1
    ? envPts.map((p) => `${x(p.i).toFixed(1)},${y(p.e.p90).toFixed(1)}`).join(' ') + ' '
      + [...envPts].reverse().map((p) => `${x(p.i).toFixed(1)},${y(p.e.p10).toFixed(1)}`).join(' ')
    : null
  const idxOf = (d) => steps.findIndex((s) => s.date >= d)
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="mx-curve" role="img" aria-label="overall projection curve">
      <line x1={PX} y1={y(0.5)} x2={W - 8} y2={y(0.5)} className="mx-cv-grid" />
      <line x1={PX} y1={y(-0.5)} x2={W - 8} y2={y(-0.5)} className="mx-cv-grid" />
      <line x1={PX} y1={y(0)} x2={W - 8} y2={y(0)} className="mx-cv-zero" />
      <text x="2" y={y(1) + 3} className="mx-cv-yl">+1</text>
      <text x="8" y={y(0) + 3} className="mx-cv-yl">0</text>
      <text x="2" y={y(-1) + 3} className="mx-cv-yl">−1</text>
      {env && <polygon points={env} className="mx-cv-env" />}
      <polyline points={vpts} className="mx-cv-line" style={{ stroke: 'var(--accent)' }} />
      {steps.map((s, i) => (s.date.endsWith('-01-01') || i === 0) && (
        <text key={i} x={x(i)} y={H - 4} className="mx-cv-xl" textAnchor="middle">{s.date.slice(0, 4)}</text>
      ))}
      {(events || []).map((ev, k) => {
        const i = idxOf(ev.date); if (i < 0) return null
        const ex = x(i), c = ev.dir === 'up' ? BAND_C.thriving : ev.dir === 'down' ? BAND_C.afflicted : BAND_C.mixed
        const ly = 10 + (k % 2) * 11
        const anchor = ex < PX + 30 ? 'start' : ex > W - 60 ? 'end' : 'middle'
        return (
          <g key={k}>
            <line x1={ex} y1={ly + 3} x2={ex} y2={y(steps[i].overall)} className="mx-cv-evline" style={{ stroke: c }} />
            <circle cx={ex} cy={y(steps[i].overall)} r="3" fill={c} />
            <text x={ex} y={ly} className="mx-cv-evlbl" style={{ fill: c }} textAnchor={anchor}>{ev.dir === 'up' ? '▲ ' : ev.dir === 'down' ? '▼ ' : '↻ '}{ev.label} · {ev.date.slice(0, 7)}</text>
          </g>
        )
      })}
    </svg>
  )
}

function LifeArc({ data, nm, t, namer, date, time, place, mc, runMc, mcBusy, mcMin }) {
  const [la, setLa] = useState(null)
  const [busy, setBusy] = useState(false)
  useEffect(() => {
    if (!date || !time || !place) return
    let alive = true
    setBusy(true); setLa(null)
    fetch(`${API}/api/matrix/lifearc`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, time, latitude: place.latitude, longitude: place.longitude, timezone: place.timezone }),
    }).then((r) => r.json()).then((j) => { if (alive && !j.error) setLa(j) })
      .catch(() => {}).finally(() => alive && setBusy(false))
    return () => { alive = false }
  }, [date, time, place])

  const themes = data.themes
  const sorted = [...themes].sort((a, b) => b.net - a.net)
  const strong = sorted.slice(0, 3), weak = sorted.slice(-3).reverse()
  const birthMs = date && time ? new Date(`${date}T${time}`).getTime() : null
  const ageNow = birthMs ? (Date.now() - birthMs) / YEAR_MS : null
  const cur = la ? la.ribbon.find((r) => la.nowYear >= r.from && la.nowYear <= r.to) : null
  const sarva = data.ashtakavarga?.sarva || []
  const smean = sarva.length ? sarva.reduce((a, b) => a + b, 0) / sarva.length : 28
  const av = (v) => netColor(Math.max(-1, Math.min(1, (v - smean) / 8)))
  const curveEvents = data.changes ? [
    ...(data.changes.health || []), ...(data.changes.wealthCareer || []), ...(data.changes.relationships || []),
  ].filter((e) => !e.care).sort((a, b) => b.cf - a.cf).slice(0, 5)
    .map((e) => ({ date: e.from || e.date, dir: e.direction, label: t('matrix.change.' + e.key + '.' + e.direction, e.label) })) : []

  const Chip = ({ ico, k, s, children }) => (
    <div className="pj-chip">
      <span className="pj-chip-ico">{ico}</span>
      <div style={{ minWidth: 0, flex: 1 }}>
        <div className="pj-chip-k">{k}</div>
        <div className="pj-chip-v" style={{ display: 'block' }}>{children}</div>
        {s && <div className="pj-chip-s">{s}</div>}
      </div>
    </div>
  )
  const rows = (list) => list.map((x) => (
    <div className="pj-kpi-row" key={x.key}><span><DomainIcon k={x.key} size={13} />{x.name.split(' · ')[0]}</span><b style={{ color: signColor(x.net) }}>{sv(x.net)}</b></div>
  ))

  // chart geometry (kept from the previous build; adds today's marker)
  let chart = null, tps = []
  if (la && la.points && la.points.length) {
    const pts = la.points
    const maxAge = pts[pts.length - 1].age
    const yMax = Math.min(0.6, Math.max(0.3, ...pts.flatMap((p) => Object.values(p.facets).map((v) => Math.abs(v)))))
    const W = 680, PX = 62, PR = 10, chH = 62, gap = 16, ribH = 22, top = 32
    const chartTop = (i) => top + i * (chH + gap)
    const x = (age) => PX + (age / Math.max(1, maxAge)) * (W - PX - PR)
    const yv = (v, i) => chartTop(i) + (1 - (Math.max(-yMax, Math.min(yMax, v)) + yMax) / (2 * yMax)) * chH
    const line = (f, i) => pts.map((p) => `${x(p.age)},${yv(p.facets[f], i)}`).join(' ')
    const ribbonY = chartTop(3)
    const totalH = ribbonY + ribH + 26
    const ageOfYear = (yr) => (pts.find((p) => p.year === yr) || {}).age
    tps = la.turningPoints.map((tp) => ({ ...tp, ageShown: tp.kind === 'yoga' ? ageOfYear(tp.year) : tp.age }))
    const tx = ageNow != null ? x(Math.min(maxAge, ageNow)) : null
    chart = (
      <svg viewBox={`0 0 ${W} ${totalH}`} className="mx-lifesvg" role="img" aria-label="life arc chart">
        {ASPECT_DEFS.map(([akey, facets], i) => (
          <g key={akey}>
            <line x1={PX} y1={yv(yMax, i)} x2={W - PR} y2={yv(yMax, i)} className="mx-cv-grid" />
            <line x1={PX} y1={yv(0, i)} x2={W - PR} y2={yv(0, i)} className="mx-cv-zero" />
            <g transform={`translate(4,${chartTop(i) + chH / 2 - 16})`} className="lbl-ico" style={{ color: 'var(--dim)' }}><DomainIcon k={akey === 'relationships' ? 'marriage' : akey} size={14} /></g>
            <text x="4" y={chartTop(i) + chH / 2 + 10} className="mx-life-alabel">{t('matrix.aspect.' + akey, akey)}</text>
            <polyline points={line(facets[0], i)} className="mx-life-line a" />
            <polyline points={line(facets[1], i)} className="mx-life-line b" />
            <text x={W - PR} y={chartTop(i) + 9} className="mx-life-flbl a" textAnchor="end">{t('matrix.facet.' + facets[0], facets[0])}</text>
            <text x={W - PR} y={chartTop(i) + chH - 2} className="mx-life-flbl b" textAnchor="end">{t('matrix.facet.' + facets[1], facets[1])}</text>
          </g>
        ))}
        {tps.map((tp, k) => {
          const tx2 = x(tp.ageShown)
          const ly = 12 + (k % 2) * 14
          const anchor = tx2 < PX + 24 ? 'start' : tx2 > W - 40 ? 'end' : 'middle'
          const dcls = tp.kind === 'yoga' ? 'yoga' : tp.direction
          const label = (tp.kind === 'yoga'
            ? '★ ' + tp.yoga
            : (tp.direction === 'rise' ? '▲ ' : '▼ ') + t('matrix.turn.' + tp.facet + '.' + tp.direction, t('matrix.facet.' + tp.facet, tp.facet))) + ' · ' + tp.year
          return (
            <g key={'tp' + k}>
              <line x1={tx2} y1={ly + 3} x2={tx2} y2={ribbonY} className={'mx-life-tp ' + dcls} />
              <text x={tx2} y={ly} className={'mx-life-tplbl ' + dcls} textAnchor={anchor}>{label}</text>
            </g>
          )
        })}
        {tx != null && (
          <g>
            <line x1={tx} y1={top - 4} x2={tx} y2={ribbonY + ribH} className="pj-la-today" />
            <text x={tx} y={top - 8} textAnchor="middle" className="pj-la-todaylbl">{t('pj.la.today', 'Today')} ▾</text>
          </g>
        )}
        {la.ribbon.map((r, i) => {
          const x1 = x(r.from - la.birthYear), x2 = x(Math.min(maxAge, r.to - la.birthYear + 1))
          return (
            <g key={i}>
              <rect x={x1} y={ribbonY} width={Math.max(2, x2 - x1)} height={ribH} className="mx-life-seg" />
              {x2 - x1 > 26 && <text x={(x1 + x2) / 2} y={ribbonY + 14} className="mx-life-seglbl" textAnchor="middle">{nm(r.lord)}</text>}
            </g>
          )
        })}
        {[0, 10, 20, 30, 40, 50, 60, 70, 80, 90].filter((a) => a <= maxAge).map((a) => (
          <g key={a}>
            <text x={x(a)} y={totalH - 12} className="mx-cv-xl">{t('matrix.age', 'age')} {a}</text>
            <text x={x(a)} y={totalH - 2} className="mx-cv-xl yr">{la.birthYear + a}</text>
          </g>
        ))}
      </svg>
    )
  }

  return (
    <>
      <div className="pj-chips">
        <Chip ico={<DomainIcon k="fortune" size={16} />} k={t('pj.la.strong', 'Strongest themes')} s={t('pj.la.strong.sub', 'sustained support across the arc')}>{rows(strong)}</Chip>
        <Chip ico={cur ? <Glyph lord={cur.lord} size={16} /> : '◔'} k={t('pj.la.period', 'Current period')}
              s={cur ? t('pj.la.period.age', 'age {a}–{b}').replace('{a}', cur.from - la.birthYear).replace('{b}', cur.to - la.birthYear) + ` · ${cur.from} – ${cur.to}` : ''}>
          {cur ? `${nm(cur.lord)} ${t('pj.la.dasha', 'daśā')}` : '…'}
        </Chip>
        <Chip ico={<DomainIcon k="enemies" size={16} />} k={t('pj.la.watch', 'Near-future watch')} s={t('pj.la.watch.sub', 'domains under most pressure')}>{rows(weak)}</Chip>
      </div>

      <div className="pj-la-row">
        <div className="pj-card">
          <h4>{t('pj.la.title', 'Life arc')}</h4>
          <p className="pj-sub">{t('pj.la.sub', 'The trajectory across wealth, health and relationships from birth onward.')}</p>
          {busy && <p className="rc-note">{t('matrix.lifeloading', 'Tracing the life arc…')}</p>}
          {chart && <div className="mx-heatwrap">{chart}</div>}
          {chart && (
            <div className="mx-life-leg">
              <span><i className="a" />{t('matrix.facet.wealthEarned', 'Earned')} / {t('matrix.facet.healthPhysical', 'Physical')} / {t('matrix.facet.relFamily', 'Family')}</span>
              <span><i className="b" />{t('matrix.facet.wealthReceived', 'Received')} / {t('matrix.facet.healthMental', 'Mental')} / {t('matrix.facet.relOthers', 'Others')}</span>
              <span className="mx-life-star">★ {t('matrix.turnyoga', 'yoga turning point')}</span>
            </div>
          )}
          {la && <p className="mx-prov">{la.note}</p>}
        </div>
        <div className="pj-card pj-turn">
          <h4>{t('pj.la.turning', 'Key turning points')}</h4>
          <p className="pj-sub">{t('pj.la.turning.sub', 'Where the arc bends. Indications, not a record of events.')}</p>
          <ul>
            {tps.map((tp, i) => (
              <li key={i}>
                <span className={tp.kind === 'yoga' ? 'mx-life-star' : tp.direction === 'rise' ? 'up' : 'down'}>{tp.kind === 'yoga' ? '★' : tp.direction === 'rise' ? '▲' : '▼'}</span>
                <span className="l">
                  <b>{tp.kind === 'yoga' ? tp.yoga : t('matrix.turn.' + tp.facet + '.' + tp.direction, t('matrix.facet.' + tp.facet, tp.facet))}</b>
                  <span>{t('matrix.age', 'age')} {tp.ageShown} · {nm(tp.maha)} {t('pj.la.dasha', 'daśā')}</span>
                </span>
                <span className={'y ' + (tp.kind === 'yoga' ? '' : tp.direction === 'rise' ? 'up' : 'down')}>{tp.year}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="pj-grid2">
        <div className="pj-card">
          <h4>{t('pj.la.transit', 'Near future · transit strength')}</h4>
          <p className="pj-sub">{t('pj.la.transit.sub', 'Sarvāṣṭakavarga bindus per sign (0–56).')}</p>
          <div className="pj-av">
            {sarva.map((v, s) => (
              <div key={s} className="pj-av-tile" style={{ background: av(v) }}>
                <b>{v}</b><span>{namer && namer.rasiAbbr ? namer.rasiAbbr(s) : s + 1}</span>
              </div>
            ))}
          </div>
          <div className="pj-av-scale">
            <span className="down">● {t('pj.la.more.challenging', 'More challenging')}</span>
            <span className="up">{t('pj.la.more.supportive', 'More supportive')} ●</span>
          </div>
        </div>
        <div className="pj-card">
          <h4>{t('pj.la.conf', 'Projection confidence')}</h4>
          <p className="pj-sub">{t('pj.la.conf.sub', 'The overall projection with its birth-time band.')}</p>
          <ConfidenceCurve steps={data.timeline.steps} t={t} envelope={mc?.envelope} events={curveEvents} />
          <div style={{ display: 'flex', gap: '.5rem', alignItems: 'center', marginTop: '.4rem' }}>
            <button type="button" className="mx-mc-btn" onClick={() => runMc(mcMin)} disabled={mcBusy}>
              {mcBusy ? t('pj.la.conf.running', 'Computing…') : t('pj.la.conf.run', 'Compute band')} (±{mcMin} min)
            </button>
            {mc && <span className="pj-chip-s">{mc.samples} × · lagna {Math.round((mc.lagnaStability ?? 0) * 100)}%</span>}
          </div>
        </div>
      </div>
    </>
  )
}

// ════════════════════════════════════════════════════════════════════════════

export default function MatrixPanel({ date, time, place, namer }) {
  const { t } = useLang()
  const [data, setData] = useState(null)
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const [open, setOpen] = useState(null)
  const [view, setView] = useState('overview')
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

  const themeName = useMemo(() => Object.fromEntries((data?.themes || []).map((th) => [th.key, th.name])), [data])

  if (!date || !time || !place) return null
  const nm = (k) => (namer && namer.grahaKey ? namer.grahaKey(k) : k)
  const bandLbl = (b) => t('matrix.band.' + b, b)

  return (
    <section className="table-panel mx-panel" id="rg-matrix">
      <h3>{t('matrix.title', 'Chart matrix — domain verdicts')}</h3>
      <p className="rc-note">{t('matrix.sub', 'Each life-domain read as a weighted, cited composite of the natal factor web. A balance from −1 to +1; the band tints a ledger you can open — an indication, not a fated verdict.')}</p>
      {busy && <p className="rc-note">{t('matrix.loading', 'Computing the matrix…')}</p>}
      {err && <p className="rc-note pc-err">{err}</p>}

      {data && (
        <>
          <div className="pj-tabs" role="tablist">
            {[['overview', t('pj.tab.overview', 'Overview')], ['forecast', t('pj.tab.forecast', 'Forecast')], ['lifearc', t('pj.tab.lifearc', 'Life arc')]].map(([k, l]) => (
              <button key={k} type="button" role="tab" aria-selected={view === k} className={view === k ? 'on' : ''} onClick={() => setView(k)}>{l}</button>
            ))}
          </div>

          {view === 'overview' && <Overview data={data} nm={nm} t={t} bandLbl={bandLbl} open={open} setOpen={setOpen} />}
          {view === 'forecast' && data.timeline && (
            <Forecast data={data} nm={nm} t={t} themeName={themeName} mc={mc} runMc={runMc} mcBusy={mcBusy}
                      mcMin={mcMin} setMcMin={setMcMin} date={date} time={time} place={place} />
          )}
          {view === 'lifearc' && data.timeline && (
            <LifeArc data={data} nm={nm} t={t} namer={namer} date={date} time={time} place={place}
                     mc={mc} runMc={runMc} mcBusy={mcBusy} mcMin={mcMin} />
          )}

          <p className="mx-prov">{data.provenance?.note}</p>
        </>
      )}
    </section>
  )
}
