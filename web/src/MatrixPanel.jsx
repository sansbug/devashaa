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

// Near-future timeline — a daśā ribbon over a themes×months heatmap + flagged windows.
function MatrixTimeline({ timeline, themeName, nm, t }) {
  const steps = timeline.steps || []
  const order = timeline.themeOrder || []
  if (!steps.length) return null
  const ym = (d) => d.slice(0, 7)
  const segs = []
  let cur = null
  steps.forEach((s) => {
    const k = `${s.maha}|${s.antar}`
    if (!cur || cur.k !== k) { if (cur) segs.push(cur); cur = { k, maha: s.maha, antar: s.antar, n: 1 } }
    else cur.n++
  })
  if (cur) segs.push(cur)
  const rowCells = (get) => steps.map((s, i) => {
    const v = get(s)
    return <td key={i} className="mx-tl-cell" style={{ background: netColor(v) }}
               title={`${ym(s.date)} · ${sv(v)}`} />
  })
  return (
    <div className="mx-tlwrap">
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
            <tr className="mx-tl-overall-row"><td className="mx-tl-name"><b>{t('matrix.overall', 'Overall')}</b></td>{rowCells((s) => s.overall)}</tr>
            {order.map((tk) => (
              <tr key={tk}><td className="mx-tl-name">{t('matrix.theme.' + tk, themeName[tk] || tk)}</td>{rowCells((s) => s.themes[tk])}</tr>
            ))}
          </tbody>
        </table>
      </div>
      {timeline.windows && timeline.windows.length > 0 && (
        <ul className="mx-tl-windows">
          {timeline.windows.map((w, i) => (
            <li key={i} className={w.good ? 'good' : 'bad'}>
              <span className="mx-tl-dir">{w.good ? '▲' : '▼'}</span>
              <span className="mx-tl-wname">{t('matrix.theme.' + w.key, w.name)}</span>
              <span className="mx-tl-wdate">{ym(w.from)}{w.from !== w.to ? ' – ' + ym(w.to) : ''}</span>
              <span className="mx-tl-wdrv">{nm(w.maha)}–{nm(w.antar)}</span>
            </li>
          ))}
        </ul>
      )}
      <p className="mx-prov">{timeline.note}</p>
    </div>
  )
}

export default function MatrixPanel({ date, time, place, namer }) {
  const { t } = useLang()
  const [data, setData] = useState(null)
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const [open, setOpen] = useState(null)

  useEffect(() => {
    if (!date || !time || !place) return
    let alive = true
    setBusy(true); setErr(''); setData(null); setOpen(null)
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
              <MatrixTimeline
                timeline={data.timeline}
                themeName={Object.fromEntries((data.themes || []).map((th) => [th.key, th.name]))}
                nm={nm}
                t={t}
              />
            </>
          )}

          <p className="mx-prov">{data.provenance?.note}</p>
        </>
      )}
    </section>
  )
}
