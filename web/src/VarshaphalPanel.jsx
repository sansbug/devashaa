/**
 * Varṣaphala — the Tājika annual chart, calculation layer only.
 *
 * What is shown is geometry: the moment the Sun returns to its natal place,
 * the chart cast for it, the Muntha, and the nine Mudda periods laid over the
 * year. What is NOT shown is listed on the panel itself, with the reason —
 * the year-lord, the sahams, the Tājika yogas and every line of phala wait on
 * a registered source (Tājika-Nīlakaṇṭhī). The readings beside each Mudda
 * period are this site's own projection, labelled synthesis, never a Tājika
 * verdict. See api/varshaphal.py.
 */
import { useEffect, useState } from 'react'
import { API } from './config.js'
import { useLang } from './LangContext.jsx'
import { SouthIndianChart, NorthIndianChart } from './RasiChart.jsx'
import Glyph from './DashaGlyphs.jsx'

const fmtD = (s) => (s || '').slice(0, 10)
const sv = (v) => (v == null ? '—' : (v >= 0 ? '+' : '') + v.toFixed(2))

/** Nine Mudda periods on one proportional rail, in the daśā navigator's idiom. */
function MuddaRail({ mudda, namer, t }) {
  const ps = mudda.periods
  const t0 = ps[0].start_jd, t1 = ps[ps.length - 1].end_jd
  const pct = (x) => ((x - t0) / (t1 - t0)) * 100
  const nowJd = 2440587.5 + Date.now() / 86400000
  const nowIn = nowJd >= t0 && nowJd <= t1
  return (
    <div className="dasha-timeline vp-rail">
      <div className="dt-rail">
        <div className="dt-rail-head">
          <span className="dt-step" aria-hidden="true">M</span>
          <span className="dt-rail-titles">
            <span className="dt-rail-label">{t('vp.mudda.title', 'Mudda daśā')}</span>
            <span className="dt-rail-sub">{t('vp.mudda.sub', 'Viṁśottarī proportions over the solar year')}</span>
          </span>
          <span className="dt-rail-span">{fmtD(ps[0].start)} → {fmtD(ps[ps.length - 1].end)}</span>
        </div>
        <div className="dt-track">
          {ps.map((p, i) => {
            const w = pct(p.end_jd) - pct(p.start_jd)
            return (
              <button type="button" key={i}
                      className={`dt-band${p.is_current ? ' running' : ''}${p.end_jd < nowJd ? ' past' : ''}${w < 5 ? ' tight' : ''}`}
                      style={{ left: `${pct(p.start_jd)}%`, width: `${w}%`, '--g': `var(--gr-${p.lord})` }}
                      title={`${namer.grahaKey(p.lord)} — ${fmtD(p.start)} → ${fmtD(p.end)} (${p.days} d)`}>
                <Glyph lord={p.lord} size={18} className="dt-band-glyph" />
                <span className="dt-band-lord">{namer.grahaKey(p.lord)}</span>
                <span className="dt-band-vert" aria-hidden="true">{namer.grahaKey(p.lord)}</span>
                <span className="dt-band-dur">{Math.round(p.days)}{t('dtl.unit.d', 'd')}</span>
              </button>
            )
          })}
          {nowIn && (
            <span className="dt-now" style={{ left: `${pct(nowJd)}%` }}>
              <span className="dt-now-label">{t('dtl.now')}</span>
            </span>
          )}
        </div>
        <div className="dt-axis">
          {ps.map((p, i) => i % 2 === 0 && (
            <span key={i} className="dt-tick" style={{ left: `${pct(p.start_jd)}%` }}>{fmtD(p.start).slice(0, 7)}</span>
          ))}
        </div>
      </div>
    </div>
  )
}

/** The site's own reading for a span: mean overall + best/worst theme over the
 *  monthly steps that fall inside it (or the nearest step for a short period). */
function readingFor(p, proj) {
  const steps = proj?.steps || []
  if (!steps.length) return null
  const s0 = fmtD(p.start), s1 = fmtD(p.end)
  let inside = steps.filter((s) => s.date >= s0 && s.date < s1)
  if (!inside.length) {
    const mid = new Date(s0).getTime() + (new Date(s1).getTime() - new Date(s0).getTime()) / 2
    inside = [steps.reduce((a, b) => (Math.abs(new Date(b.date) - mid) < Math.abs(new Date(a.date) - mid) ? b : a))]
  }
  const n = inside.length
  const overall = inside.reduce((a, s) => a + (s.overall || 0), 0) / n
  const keys = Object.keys(inside[0].themes)
  const mean = Object.fromEntries(keys.map((k) => [k, inside.reduce((a, s) => a + (s.themes[k] || 0), 0) / n]))
  const best = keys.reduce((a, b) => (mean[b] > mean[a] ? b : a))
  const worst = keys.reduce((a, b) => (mean[b] < mean[a] ? b : a))
  return { overall, best, bestV: mean[best], worst, worstV: mean[worst], n }
}

export default function VarshaphalPanel({ date, time, place, namer, chartStyle = 'north' }) {
  const { t } = useLang()
  const [year, setYear] = useState(null)          // null = the varṣa running now
  const [data, setData] = useState(null)
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')

  useEffect(() => {
    if (!date || !time || !place) return
    let alive = true
    setBusy(true); setErr('')
    fetch(`${API}/api/varshaphal`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, time, latitude: place.latitude, longitude: place.longitude,
                             timezone: place.timezone, year }),
    })
      .then((r) => r.json())
      .then((j) => { if (!alive) return; if (j.error) setErr(j.error); else setData(j) })
      .catch((e) => alive && setErr(String(e)))
      .finally(() => alive && setBusy(false))
    return () => { alive = false }
  }, [date, time, place, year])

  if (!date || !time || !place) return null
  const nm = (k) => namer.grahaKey(k)
  const Chart = chartStyle === 'south' ? SouthIndianChart : NorthIndianChart
  const themeName = (k) => t('matrix.theme.' + k, (data?.projection?.themeNames?.[k] || k).split(' · ')[0])

  return (
    <section className="table-panel vp-panel" id="rg-varshaphal">
      <h3>{t('vp.title', 'Varṣaphala — the annual chart')}</h3>
      <p className="rc-note">{t('vp.sub', 'The Tājika year: the chart cast for the moment the Sun returns to its natal place, the Muntha, and the nine Mudda periods. Calculation only — what is not shown, and why, is listed below.')}</p>
      {busy && <p className="rc-note">{t('vp.loading', 'Casting the year…')}</p>}
      {err && <p className="rc-note pc-err">{err}</p>}

      {data && (
        <>
          <div className="dt-chips vp-chips">
            <div className="dt-chip">
              <span className="dt-chip-k">{t('vp.chip.year', 'Varṣa')}</span>
              <span className="dt-chip-v vp-year">
                <button type="button" onClick={() => setYear(data.year - 1)} aria-label="previous year">‹</button>
                {data.year}–{data.year + 1}
                <button type="button" onClick={() => setYear(data.year + 1)} aria-label="next year">›</button>
                <span className="dt-rail-dur"> · {t('vp.chip.age', 'age')} {data.age}</span>
              </span>
            </div>
            <div className="dt-chip">
              <span className="dt-chip-k">{t('vp.chip.pravesha', 'Varṣa-praveśa')}</span>
              <span className="dt-chip-v">{data.pravesha.local} <span className="dt-rail-dur">({data.pravesha.timezone})</span></span>
            </div>
            <div className="dt-chip">
              <span className="dt-chip-k">{t('vp.chip.lagna', 'Varṣa lagna')}</span>
              <span className="dt-chip-v">{namer.rasi ? namer.rasi(data.varsha_lagna.sign) : data.varsha_lagna.sign + 1} <span className="dt-rail-dur">· {t('vp.lord', 'lord')} {nm(data.varsha_lagna.lord)}</span></span>
            </div>
            <div className="dt-chip">
              <span className="dt-chip-k">{t('vp.chip.muntha', 'Muntha')}</span>
              <span className="dt-chip-v">{namer.rasi ? namer.rasi(data.muntha.sign) : data.muntha.sign + 1} <span className="dt-rail-dur">· {t('vp.bhava', 'bhāva')} {data.muntha.house_from_varsha_lagna} · {t('vp.lord', 'lord')} {nm(data.muntha.lord)}</span></span>
            </div>
          </div>

          <div className="vp-body">
            <div className="vp-chart">
              <h4>{t('vp.chart.title', 'Varṣa kuṇḍalī')}</h4>
              <p className="rc-note">{t('vp.chart.sub', 'Cast for the praveśa instant at the birth place.')} {data.pravesha.utc} UTC</p>
              <Chart grahas={data.chart.grahas} lagnaRasi={data.chart.lagna_rasi} vargaKey="D1"
                     lagnaLongitude={data.chart.lagna_longitude} namer={namer} />
            </div>
            <aside className="dt-side">
              <div className="dt-card">
                <h4>{t('vp.adhikari.title', 'Office-bearers (pañcādhikārī)')}</h4>
                {[['muntha_lord', t('vp.adhikari.muntha', 'Muntha lord')],
                  ['varsha_lagna_lord', t('vp.adhikari.vlagna', 'Varṣa-lagna lord')],
                  ['janma_lagna_lord', t('vp.adhikari.jlagna', 'Janma-lagna lord')],
                  ['trirasi_lord', t('vp.adhikari.trirasi', 'Tri-rāśi lord')],
                  ['dinaratri_lord', t('vp.adhikari.dinaratri', 'Dina-rātri lord')]].map(([k, l]) => (
                  <div key={k} className="dt-rem-row">
                    <span className="dt-rem-k">{l}</span>
                    <span className="dt-rem-v">{data.panchadhikari[k] ? <><Glyph lord={data.panchadhikari[k]} size={14} /> {nm(data.panchadhikari[k])}</> : <span className="vp-refused">{t('vp.refused.short', 'not computed')}</span>}</span>
                  </div>
                ))}
                <p className="dt-now-lvl" style={{ marginTop: '.4rem' }}>{t('vp.adhikari.note', 'The year-lord (varṣeśa) is chosen among these five by the pañcavargīya bala — which needs the text. It is not chosen here.')}</p>
              </div>
              <div className="dt-card vp-refused-card">
                <h4>{t('vp.refused.title', 'Not shown — and why')}</h4>
                <ul>
                  {data.refused.map((r, i) => <li key={i}><b>{r.what}</b><span>{r.why}</span></li>)}
                </ul>
              </div>
            </aside>
          </div>

          <MuddaRail mudda={data.mudda} namer={namer} t={t} />

          <div className="dt-table-wrap">
            <table className="dt-table vp-table">
              <thead>
                <tr>
                  <th>{t('vp.tbl.period', 'Mudda period')}</th>
                  <th>{t('vp.tbl.from', 'From')}</th><th>{t('vp.tbl.to', 'To')}</th><th>{t('vp.tbl.days', 'Days')}</th>
                  <th>{t('vp.tbl.reading', 'This site’s reading (synthesis)')}</th>
                </tr>
              </thead>
              <tbody>
                {data.mudda.periods.map((p, i) => {
                  const r = readingFor(p, data.projection)
                  return (
                    <tr key={i} className={p.is_current ? 'running' : ''} style={{ '--g': `var(--gr-${p.lord})` }}>
                      <td className="dt-tbl-lord"><Glyph lord={p.lord} size={16} />{nm(p.lord)}{p.is_current && <span className="dt-badge">{t('dtl.side.current_badge')}</span>}</td>
                      <td>{fmtD(p.start)}</td><td>{fmtD(p.end)}</td><td>{Math.round(p.days)}</td>
                      <td className="vp-reading">
                        {r ? (
                          <>
                            <span className="vp-ov" style={{ color: r.overall > 0.02 ? 'var(--ok-ink)' : r.overall < -0.02 ? 'var(--err-ink)' : 'var(--dim)' }}>{sv(r.overall)}</span>
                            <span className="vp-th up">▲ {themeName(r.best)} {sv(r.bestV)}</span>
                            <span className="vp-th down">▼ {themeName(r.worst)} {sv(r.worstV)}</span>
                          </>
                        ) : '—'}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
          <p className="mx-prov">{t('vp.mudda.rule', 'Rule')}: {data.mudda.rule}. {data.mudda.validation}.</p>
          <p className="mx-prov">{data.note}</p>
        </>
      )}
    </section>
  )
}
