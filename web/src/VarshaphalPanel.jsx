/**
 * Varṣaphala — the Tājika annual chart.
 *
 * Everything shown is geometry with its rule and its page: the praveśa, the
 * year chart, Muntha, the office-bearers and the year-lord, the pañcavargīya
 * and harṣa strengths, the Tājika aspects, the sixteen yogas, the fifty
 * sahams, and the Mudda periods. Beside each Mudda period stand two things,
 * never blended: this site's own projection (synthesis) and what K.S. Charak
 * (1996) STATES for the period lord's house and strength in the year chart —
 * cited gists, adapted per docs/classical-sources-policy.md §5 (modern tier).
 * See api/varshaphal.py, api/tajika.py, api/charak_annual_rules.py.
 */
import { useEffect, useState } from 'react'
import { API } from './config.js'
import { useLang } from './LangContext.jsx'
import { SouthIndianChart, NorthIndianChart } from './RasiChart.jsx'
import Glyph from './DashaGlyphs.jsx'

const SEVEN = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn']
const fmtD = (s) => (s || '').slice(0, 10)
const sv = (v) => (v == null ? '—' : (v >= 0 ? '+' : '') + v.toFixed(2))
const n1 = (v) => (v == null ? '—' : Number(v).toFixed(1))
const n2 = (v) => (v == null ? '—' : Number(v).toFixed(2))
const dms = (deg) => { const d = Math.floor(deg); const m = Math.round((deg - d) * 60); return `${d}°${String(m).padStart(2, '0')}′` }

const ITH_TYPE = { vartamana: 'vartamāna', purna: 'pūrṇa', bhavishyat: 'bhaviṣyat' }
const YOGA_TONE = {
  itthasala: 'good', isarapha: 'bad', nakta: 'help', yamaya: 'help', manau: 'bad', kambula: 'good',
  gairi_kambula: 'good', khallasara: 'bad', rudda: 'bad', duphalikuttha: 'good', dutthottha: 'help',
  tambira: 'help', kuttha: 'good', durpha: 'bad',
}

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
                      title={`${namer.grahaKey(p.lord)} — ${fmtD(p.start)} → ${fmtD(p.end)} (${p.days} d${p.kind !== 'full' ? ', ' + p.kind : ''})`}>
                <Glyph lord={p.lord} size={18} className="dt-band-glyph" />
                <span className="dt-band-lord">{namer.grahaKey(p.lord)}</span>
                <span className="dt-band-vert" aria-hidden="true">{namer.grahaKey(p.lord)}</span>
                <span className="dt-band-dur">{Math.round(p.days)}{t('dtl.unit.d', 'd')}</span>
              </button>
            )
          })}
          {nowIn && <span className="dt-now" style={{ left: `${pct(nowJd)}%` }}><span className="dt-now-label">{t('dtl.now')}</span></span>}
        </div>
        <div className="dt-axis">
          {ps.map((p, i) => i % 2 === 0 && <span key={i} className="dt-tick" style={{ left: `${pct(p.start_jd)}%` }}>{fmtD(p.start).slice(0, 7)}</span>)}
        </div>
      </div>
    </div>
  )
}

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
  return { overall, best, bestV: mean[best], worst, worstV: mean[worst] }
}

/** A §5 handling badge: which content classes the gist touched and how. */
function Adapted({ a, t }) {
  const cls = (a?.classes || []).filter(Boolean)
  if (!cls.length) return null
  return (
    <span className="cl-hist vp-ph-adapt" title={`${a.action}. ${a.note}`}>
      ⧗ {t('vp.phala.handled', 'handled')} — {cls.map((c) => t('vp.phala.cls.' + c, c)).join(' · ')}
    </span>
  )
}

/** One cited line of what the text states. Attribution first, then the gist. */
function Stated({ e, lead, t }) {
  if (!e) return null
  return (
    <div className="vp-ph-block">
      <div className="vp-ph-src"><span className="cl-tier">modern</span> <b>{e.citation}</b>{lead && <span> — {lead}</span>}</div>
      <p className="vp-ph-gist">{e.gist}</p>
      <Adapted a={e.adaptation} t={t} />
    </div>
  )
}

/** The per-period readings: the lord's house and strength in the year chart,
 *  Charak's stated results for both, the hints that apply as flags, the yogas
 *  it takes part in, and — separately labelled — this site's own projection. */
function MuddaReadings({ mudda, phala, projection, nm, rs, G, themeName, t }) {
  const lag = phala.lagna
  return (
    <Card
      className="vp-ph"
      title={t('vp.phala.title', 'Period readings — what the text states')}
      sub={<>{t('vp.phala.sub', 'For each Mudda period: its lord’s house in the year chart and its pañcavargīya band, with the stated results for that placement — in this site’s words, never a verdict, never blended with this site’s own reading.')} <span className="src">{t('vp.phala.subref', '')}</span></>}
      cite={`${phala.source.text} — ${phala.source.author} (${phala.source.date}). ${phala.caveat.citation}: ${phala.caveat.gist} ${phala.source.verification}.`}
    >
      {lag && (
        <p className="vp-ph-lagna">
          <b>{t('vp.phala.lagna', 'The year’s lagna')}</b> — <span className={`vp-cat vp-cat-${lag.lord_category}`}>{t('vp.phala.band.' + lag.band, lag.band)}</span>
          <span className="vp-ph-src"> · {t('vp.phala.lagnaby', 'read through its lord’s band')} ({t('vp.pv.' + lag.lord_category, lag.lord_category)}) · <b>{lag.citation}</b>:</span> {lag.gist} <Adapted a={lag.adaptation} t={t} />
        </p>
      )}
      {mudda.periods.map((p, i) => {
        const r = p.reading
        if (!r) return null
        const syn = readingFor(p, projection)
        return (
          <details key={i} className={`vp-ph-period ${p.is_current ? 'running' : ''}`} open={p.is_current} style={{ '--g': `var(--gr-${p.lord})` }}>
            <summary>
              <span className="vp-ph-lord"><G k={p.lord} s={16} /></span>
              <span className="vp-ph-dates">{fmtD(p.start)} → {fmtD(p.end)} · {Math.round(p.days)} {t('vp.phala.days', 'd')}</span>
              {p.kind !== 'full' && <span className="dt-rail-dur">{t('vp.mudda.' + p.kind, p.kind)}</span>}
              {p.is_current && <span className="dt-badge">{t('dtl.side.current_badge')}</span>}
              <span className="vp-ph-place">{t('vp.phala.inhouse', 'in the')} {r.house_ordinal} · {rs(r.sign)}</span>
              {r.band && <span className={`vp-cat vp-cat-${r.category}`}>{t('vp.pv.' + r.category, r.category)} · VB {n1(r.vishwa_bala)}</span>}
              {r.house_flag && <span className={`vp-ph-flag ${r.house_flag}`}>{t('vp.phala.' + r.house_flag, r.house_flag === 'favourable' ? 'a house the text calls favourable for it' : 'a house the text calls adverse for it')}</span>}
            </summary>
            <Stated e={r.in_house} lead={`${nm(p.lord)} ${t('vp.phala.inhouse', 'in the')} ${r.house_ordinal}`} t={t} />
            {r.by_strength
              ? <Stated e={r.by_strength} lead={`${t('vp.phala.bystrength', 'by strength')}: ${t('vp.pv.' + r.category, r.category)} (VB ${n1(r.vishwa_bala)})`} t={t} />
              : <Stated e={r.strength_note} lead={t('vp.phala.nostrength', 'no strength result for the nodes')} t={t} />}
            {r.modifiers.length > 0 && (
              <div className="vp-ph-mods">
                <span className="vp-ph-src">{t('vp.phala.hints', 'Charak’s hints that apply here')}:</span>
                {r.modifiers.map((m) => (
                  <span key={m.hint} className="vp-yoga help" title={`${m.citation}: ${m.gist}`}>
                    §{m.hint} {t('vp.phala.flag.' + m.hint, m.flag)}{m.bodies?.length ? ` — ${m.bodies.map(nm).join(', ')}` : ''}
                  </span>
                ))}
              </div>
            )}
            {r.yogas.length > 0 && (
              <div className="vp-ph-mods">
                <span className="vp-ph-src">{t('vp.phala.yogas', 'yogas this lord takes part in')}:</span>
                {r.yogas.map((y, j) => (
                  <span key={j} className={`vp-yoga ${YOGA_TONE[y.yoga] || 'help'}`} title={r.fructification ? `${r.fructification.citation}: ${r.fructification.gist}` : ''}>
                    {y.yoga === 'itthasala' ? 'Itthaśāla' : 'Īśarāpha'}{y.type ? ` ${ITH_TYPE[y.type] || y.type}` : ''} · {nm(y.with)}
                  </span>
                ))}
              </div>
            )}
            {syn && (
              <p className="vp-ph-syn">
                <span className="cl-tier vp-tier-syn">synthesis</span> {t('vp.phala.synth', 'this site’s own projection for the period')}:{' '}
                <span className="vp-ov" style={{ color: syn.overall > 0.02 ? 'var(--ok-ink)' : syn.overall < -0.02 ? 'var(--err-ink)' : 'var(--dim)' }}>{sv(syn.overall)}</span>{' '}
                <span className="vp-th up">▲ {themeName(syn.best)} {sv(syn.bestV)}</span>{' '}
                <span className="vp-th down">▼ {themeName(syn.worst)} {sv(syn.worstV)}</span>
              </p>
            )}
          </details>
        )
      })}
      <details className="vp-details">
        <summary>{t('vp.phala.allhints', 'The eight interpretation hints')} <span className="src">pp. 106–107</span></summary>
        <ol className="vp-ph-hints">
          {Object.entries(phala.hints).map(([k, h]) => <li key={k}><span className="vp-ph-src">{h.citation}</span> {h.gist}</li>)}
        </ol>
      </details>
    </Card>
  )
}

function Card({ title, sub, cite, children, className = '' }) {
  return (
    <div className={`dt-card vp-card ${className}`}>
      <h4>{title}</h4>
      {sub && <p className="vp-sub">{sub}</p>}
      {children}
      {cite && <p className="mx-prov vp-cite">{cite}</p>}
    </div>
  )
}

export default function VarshaphalPanel({ date, time, place, namer, chartStyle = 'north' }) {
  const { t } = useLang()
  const [year, setYear] = useState(null)
  const [data, setData] = useState(null)
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const [muddaVar, setMuddaVar] = useState('prorated')
  const [allSahams, setAllSahams] = useState(false)

  useEffect(() => {
    if (!date || !time || !place) return
    let alive = true
    setBusy(true); setErr('')
    fetch(`${API}/api/varshaphal`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, time, latitude: place.latitude, longitude: place.longitude, timezone: place.timezone, year }),
    })
      .then((r) => r.json())
      .then((j) => { if (!alive) return; if (j.error) setErr(j.error); else { setData(j); setMuddaVar(j.mudda?.default || 'prorated') } })
      .catch((e) => alive && setErr(String(e)))
      .finally(() => alive && setBusy(false))
    return () => { alive = false }
  }, [date, time, place, year])

  if (!date || !time || !place) return null
  const nm = (k) => (k ? namer.grahaKey(k) : '—')
  const rs = (i) => (namer.rasi ? namer.rasi(i) : i + 1)
  const Chart = chartStyle === 'south' ? SouthIndianChart : NorthIndianChart
  const themeName = (k) => t('matrix.theme.' + k, (data?.projection?.themeNames?.[k] || k).split(' · ')[0])
  const G = ({ k, s = 14 }) => <><Glyph lord={k} size={s} /> {nm(k)}</>

  const mudda = data?.mudda?.variants?.[muddaVar]
  const pv = data?.pancha_vargiya?.grahas
  const ha = data?.harsha?.grahas
  const vl = data?.varshesha
  const yg = data?.yogas
  const CORE = new Set(['punya', 'vidya', 'yasha', 'mitra', 'mahatmya', 'samarthya', 'bhratri', 'gaurava', 'rajya', 'pitri', 'matri', 'putra', 'jiva', 'karma', 'roga', 'vivaha', 'mrityu', 'dhana', 'vyapara', 'karyasiddhi', 'pardesha', 'santapa', 'shatru', 'bandhana'])

  return (
    <section className="table-panel vp-panel" id="rg-varshaphal">
      <h3>{t('vp.title', 'Varṣaphala — the annual chart')}</h3>
      <p className="rc-note">{t('vp.sub2', 'The Tājika year, calculated from the texts on hand: the praveśa, the year chart, Muntha, the office-bearers and year-lord, the five-fold and harṣa strengths, the aspects, the sixteen yogas, the fifty sahams and the Mudda periods. Rules and pages travel with every figure; no prediction sentence ships.')}</p>
      {busy && <p className="rc-note">{t('vp.loading', 'Casting the year…')}</p>}
      {err && <p className="rc-note pc-err">{err}</p>}

      {data && (
        <>
          {/* ── chips ─────────────────────────────────────────────────────── */}
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
              <span className="dt-chip-v">{data.pravesha.local} <span className="dt-rail-dur">· {data.is_day ? t('vp.day', 'day') : t('vp.night', 'night')}</span></span>
            </div>
            <div className="dt-chip">
              <span className="dt-chip-k">{t('vp.chip.lagna', 'Varṣa lagna')}</span>
              <span className="dt-chip-v">{rs(data.varsha_lagna.sign)} <span className="dt-rail-dur">· {t('vp.lord', 'lord')} {nm(data.varsha_lagna.lord)}</span></span>
            </div>
            <div className="dt-chip">
              <span className="dt-chip-k">{t('vp.chip.muntha', 'Muntha')}</span>
              <span className="dt-chip-v">{rs(data.muntha.sign)} <span className="dt-rail-dur">· {t('vp.bhava', 'bhāva')} {data.muntha.house_from_varsha_lagna} · {nm(data.muntha.lord)}</span></span>
            </div>
            {vl && (
              <div className="dt-chip vp-chip-lord" style={{ '--g': `var(--gr-${vl.lord})` }}>
                <span className="dt-chip-k">{t('vp.chip.varshesha', 'Year-lord (varṣeśa)')}</span>
                <span className="dt-chip-v"><G k={vl.lord} s={16} /></span>
              </div>
            )}
          </div>

          {/* ── chart + year-lord ─────────────────────────────────────────── */}
          <div className="vp-body">
            <div className="vp-chart">
              <h4>{t('vp.chart.title', 'Varṣa kuṇḍalī')}</h4>
              <p className="rc-note">{t('vp.chart.sub', 'Cast for the praveśa instant at the birth place.')} {data.pravesha.utc} UTC</p>
              <Chart grahas={data.chart.grahas} lagnaRasi={data.chart.lagna_rasi} vargaKey="D1" lagnaLongitude={data.chart.lagna_longitude} namer={namer} />
            </div>
            <aside className="dt-side">
              <Card title={t('vp.varshesha.title', 'The five office-bearers → the year-lord')} cite={vl?.rule}>
                <div className="dt-table-wrap">
                <table className="dt-table vp-t">
                  <thead><tr><th>{t('vp.varshesha.role', 'Office')}</th><th>{t('vp.varshesha.planet', 'Graha')}</th><th>{t('vp.varshesha.vb', 'Viśva-bala')}</th><th>{t('vp.varshesha.aspects', 'Aspects lagna')}</th></tr></thead>
                  <tbody>
                    {[['muntha', t('vp.adhikari.muntha', 'Muntha lord')], ['janma_lagna', t('vp.adhikari.jlagna', 'Janma-lagna lord')],
                      ['varsha_lagna', t('vp.adhikari.vlagna', 'Varṣa-lagna lord')], ['trirasi', t('vp.adhikari.trirasi', 'Tri-rāśi lord')],
                      ['dinaratri', t('vp.adhikari.dinaratri', 'Dina-rātri lord')]].map(([role, label]) => {
                      const p = data.panchadhikari[role + '_lord']
                      const c = vl?.contenders.find((x) => x.planet === p)
                      const win = vl?.lord === p
                      return (
                        <tr key={role} className={win ? 'running' : ''} style={{ '--g': `var(--gr-${p})` }}>
                          <td>{label}</td>
                          <td className="dt-tbl-lord"><G k={p} /> {win && <span className="dt-badge">{t('vp.varshesha.winner', 'year-lord')}</span>}</td>
                          <td>{c ? n2(c.vishwa_bala) : '—'}</td>
                          <td title={c ? `${t('vp.varshesha.lagnain', 'lagna is its')} ${c.aspect_house}${t('vp.th', 'th')} · ${c.aspect_kind || t('vp.drishti.none', 'no aspect')} · ${c.aspect_value}` : ''}>{c ? (c.aspects_lagna ? `✓ ${c.aspect_house}` : `✗ ${c.aspect_house}`) : '—'}</td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
                </div>
                <ul className="vp-steps">{vl?.steps.map((s, i) => <li key={i}>{s}</li>)}{vl?.moon_note && <li>{vl.moon_note}</li>}</ul>
              </Card>
              <Card title={t('vp.refused.title', 'Not shown — and why')}>
                <ul className="vp-refused-list">{data.refused.map((r, i) => <li key={i}><b>{r.what}</b><span>{r.why}</span></li>)}</ul>
              </Card>
            </aside>
          </div>

          {/* ── strengths ─────────────────────────────────────────────────── */}
          {pv && ha && (<div className="vp-grid2">
            <Card title={t('vp.pv.title', 'Pañcavargīya bala — the five-fold strength')}
                  sub={t('vp.pv.sub', 'Units by the graha’s relation to the lord of its sign, hadda, drekkāṇa and navāṁśa (own 30/15/10/5 · friend ¾ · neutral ½ · enemy ¼), plus the distance from debilitation ÷ 9. Viśva-bala = total ÷ 4.')}
                  cite={data.pancha_vargiya.rule}>
              <div className="dt-table-wrap">
                <table className="dt-table vp-t vp-num">
                  <thead><tr><th>{t('vp.graha', 'Graha')}</th><th>Kṣetra</th><th>Uccha</th><th>Hadda</th><th>Drekkāṇa</th><th>Navāṁśa</th><th>{t('vp.total', 'Total')}</th><th>VB</th><th>{t('vp.pv.cat', 'Class')}</th></tr></thead>
                  <tbody>
                    {SEVEN.map((p) => {
                      const r = pv[p]
                      const cell = (c) => <td title={`${t('vp.lordof', 'lord')} ${nm(r[c].lord)} · ${r[c].relation}`}>{n2(r[c].units)}</td>
                      return (
                        <tr key={p} style={{ '--g': `var(--gr-${p})` }}>
                          <td className="dt-tbl-lord"><G k={p} /></td>
                          {cell('kshetra')}<td title={`${t('vp.pv.deb', 'debilitation at')} ${dms(r.uchcha.debilitation_point % 30)} · ${t('vp.pv.dist', 'distance')} ${n1(r.uchcha.distance)}°`}>{n2(r.uchcha.units)}</td>
                          {cell('hadda')}{cell('drekkana')}{cell('navamsa')}
                          <td><b>{n2(r.total)}</b></td><td><b>{n2(r.vishwa_bala)}</b></td>
                          <td><span className={`vp-cat vp-cat-${r.category}`}>{t('vp.pv.' + r.category, r.category)}</span></td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </Card>
            <Card title={t('vp.harsha.title', 'Harṣa bala — the four joys')}
                  sub={t('vp.harsha.sub', 'Five units each: the graha’s own house of joy; exaltation or own sign; a house of its own sex (female 1-2-3, 7-8-9; male 4-5-6, 10-11-12); male by day, female by night.')}
                  cite={data.harsha.rule}>
              <div className="dt-table-wrap">
                <table className="dt-table vp-t vp-num">
                  <thead><tr><th>{t('vp.graha', 'Graha')}</th><th>{t('vp.harsha.sthana', 'Joy-house')}</th><th>{t('vp.harsha.uccha', 'Exalt./own')}</th><th>{t('vp.harsha.sex', 'Sex')}</th><th>{t('vp.harsha.dn', 'Day/night')}</th><th>{t('vp.total', 'Total')}</th></tr></thead>
                  <tbody>
                    {SEVEN.map((p) => {
                      const r = ha[p]
                      return (
                        <tr key={p} style={{ '--g': `var(--gr-${p})` }}>
                          <td className="dt-tbl-lord"><G k={p} /> <span className="dt-rail-dur">({data.harsha.sthana[p]})</span></td>
                          <td>{r.sthana}</td><td>{r.uchcha_swakshetra}</td><td>{r.stri_purusha}</td><td>{r.dina_ratri}</td>
                          <td><b>{r.total}</b> <span className={`vp-cat vp-cat-${r.category}`}>{t('vp.harsha.' + r.category, r.category)}</span></td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            </Card>
          </div>)}

          {/* ── aspects ───────────────────────────────────────────────────── */}
          {data.drishti && <Card title={t('vp.drishti.title', 'Tājika dṛṣṭi — aspects')}
                sub={t('vp.drishti.sub', 'Row aspects column. 5th/9th ¾ (45) open friends · 3rd ⅔ (40) and 11th ⅙ (10) secret friends · 4th/10th ¼ (15) secret enemies · same sign and 7th full (60) open enemies · 2/6/8/12 none. Values interpolate by the degrees within the sign.')}
                cite={data.drishti.rule} className="vp-drishti-card">
            <div className="dt-table-wrap">
              <table className="dt-table vp-t vp-num vp-drishti">
                <thead><tr><th /><th>{t('vp.drishti.orb', 'Orb')}</th>{SEVEN.map((q) => <th key={q}><Glyph lord={q} size={13} /></th>)}</tr></thead>
                <tbody>
                  {SEVEN.map((p) => (
                    <tr key={p} style={{ '--g': `var(--gr-${p})` }}>
                      <td className="dt-tbl-lord"><G k={p} /></td>
                      <td className="dt-rail-dur">{data.drishti.deeptamsa[p]}°</td>
                      {SEVEN.map((q) => {
                        if (p === q) return <td key={q} className="vp-self">–</td>
                        const a = data.drishti.matrix[p][q]
                        const tone = a.value === 0 ? 'none' : (a.kind || '').includes('friend') ? 'friend' : 'enemy'
                        return <td key={q} className={`vp-asp vp-asp-${tone}`} title={`${nm(p)} → ${nm(q)}: ${a.kind || t('vp.drishti.none', 'no aspect')} (${a.house}${t('vp.th', 'th')})`}>{a.value === 0 ? '·' : n1(a.value)}</td>
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>}

          {/* ── yogas ─────────────────────────────────────────────────────── */}
          {yg && (
            <Card title={t('vp.yogas.title', 'The sixteen Tājika yogas')}
                  sub={t('vp.yogas.sub', 'Read between the lagneśa and the lord of each house, as the annual chart allows (Charak p.110). Itthaśāla: the faster graha behind the slower, in mutual aspect, within the mean of their orbs. Every other yoga is a variation or a negation of it.')}
                  cite={yg.rule}>
              <div className="vp-yoga-global">
                <span className={`vp-yoga ${yg.ikkavala.present ? 'good' : 'off'}`}>Ikkavāla {yg.ikkavala.present ? '✓' : '✗'}</span>
                <span className={`vp-yoga ${yg.induvara.present ? 'bad' : yg.induvara.partial ? 'help' : 'off'}`}>Induvāra {yg.induvara.present ? '✓' : yg.induvara.partial ? t('vp.yogas.partial', 'partial') : '✗'} <span className="dt-rail-dur">({yg.induvara.in_apoklimas}/7 {t('vp.yogas.inapo', 'in apoklimas')})</span></span>
                <span className="vp-yoga off">{t('vp.yogas.lagnesha', 'lagneśa')} <G k={yg.lagnesha} /></span>
              </div>
              <div className="dt-table-wrap">
                <table className="dt-table vp-t vp-yogat">
                  <thead><tr><th>{t('vp.bhava', 'bhāva')}</th><th>{t('vp.yogas.karyesha', 'kāryeśa')}</th><th>{t('vp.yogas.found', 'Yogas with the lagneśa')}</th></tr></thead>
                  <tbody>
                    {Object.entries(yg.houses).map(([k, h]) => {
                      const chips = []
                      if (h.same_lord) chips.push(['same', t('vp.yogas.samelord', 'lagneśa is also kāryeśa'), 'off'])
                      if (h.itthasala) chips.push(['itthasala', `Itthaśāla · ${h.itthasala.type}${h.itthasala.variant ? ' *' : ''} (${nm(h.itthasala.fast)} ${n1(h.itthasala.gap)}° ${t('vp.yogas.behind', 'behind')} ${nm(h.itthasala.slow)}, ${t('vp.yogas.orb', 'orb')} ${h.itthasala.orb})`, 'good'])
                      if (h.isarapha) chips.push(['isarapha', `Īśarāpha (${nm(h.isarapha.fast)} ${n1(h.isarapha.separation)}° ${t('vp.yogas.ahead', 'ahead')})`, 'bad'])
                      if (h.nakta) chips.push(['nakta', `Nakta ${t('vp.yogas.via', 'via')} ${h.nakta.via.map(nm).join(', ')}`, 'help'])
                      if (h.yamaya) chips.push(['yamaya', `Yamayā ${t('vp.yogas.via', 'via')} ${h.yamaya.via.map(nm).join(', ')}`, 'help'])
                      if (h.manau) chips.push(['manau', `Manau (${h.manau.map(nm).join(', ')})`, 'bad'])
                      if (h.kambula) chips.push(['kambula', `Kambūla ${h.kambula.label} (${t('vp.yogas.moonwith', 'Moon with')} ${nm(h.kambula.with)})`, 'good'])
                      if (h.gairi_kambula) chips.push(['gairi', `Gairi-Kambūla (${h.gairi_kambula.with.map(nm).join(', ')})`, 'good'])
                      if (h.khallasara) chips.push(['khallasara', 'Khallāsara', 'bad'])
                      if (h.rudda) chips.push(['rudda', `Rudda (${Object.entries(h.rudda.weak).map(([p, f]) => `${nm(p)}: ${f.join(', ')}`).join('; ')})`, 'bad'])
                      if (h.duphalikuttha) chips.push(['duphali', `Duphāli-kuttha (${nm(h.duphalikuttha.fast)} ${t('vp.yogas.weaker', 'the weaker')})`, 'good'])
                      if (h.dutthottha) chips.push(['dutthottha', `Dutthottha-dāvīra ${t('vp.yogas.via', 'via')} ${h.dutthottha.via.map(nm).join(', ')}`, 'help'])
                      if (h.tambira) chips.push(['tambira', `Tambīra (${h.tambira.with.map(nm).join(', ')})`, 'help'])
                      if (h.kuttha) chips.push(['kuttha', 'Kuttha', 'good'])
                      if (h.durpha) chips.push(['durpha', 'Durpha', 'bad'])
                      return (
                        <tr key={k}>
                          <td>{k}</td>
                          <td className="dt-tbl-lord" style={{ '--g': `var(--gr-${h.karyesha})` }}><G k={h.karyesha} /></td>
                          <td className="vp-chips-cell">{chips.length ? chips.map(([id, label, tone]) => <span key={id} className={`vp-yoga ${tone}`}>{label}</span>) : <span className="dt-rail-dur">{t('vp.yogas.none', 'none — the two lords are not in aspect, or no yoga forms')}</span>}</td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
              {yg.pairs.length > 0 && (
                <details className="vp-details">
                  <summary>{t('vp.yogas.allpairs', 'Every itthaśāla / īśarāpha between the seven')}</summary>
                  <ul className="vp-pairs">
                    {yg.pairs.map((pr, i) => (
                      <li key={i}>
                        <G k={pr.a} /> · <G k={pr.b} />
                        {pr.itthasala && <span className="vp-yoga good">Itthaśāla {pr.itthasala.type} — {nm(pr.itthasala.fast)} {n1(pr.itthasala.gap)}° {t('vp.yogas.behind', 'behind')} {nm(pr.itthasala.slow)} ({t('vp.yogas.orb', 'orb')} {pr.itthasala.orb}){pr.itthasala.variant ? ` — ${pr.itthasala.variant}` : ''}</span>}
                        {pr.isarapha && <span className="vp-yoga bad">Īśarāpha — {nm(pr.isarapha.fast)} {n1(pr.isarapha.separation)}° {t('vp.yogas.ahead', 'ahead')}</span>}
                      </li>
                    ))}
                  </ul>
                </details>
              )}
            </Card>
          )}

          {/* ── sahams ────────────────────────────────────────────────────── */}
          {Array.isArray(data.sahams) && <Card title={t('vp.sahams.title', 'Sahams — the fifty sensitive points')}
                sub={t('vp.sahams.sub', 'Each is a − b + c on the year’s longitudes, +30° when c does not lie in the arc from b forward to a; by day or by night as the text states. Strength follows the saham’s lord; timing = (saham − lord) × the rising time of its sign ÷ 300. House cusps are equal houses from the lagna degree (a convention).')}
                cite="TN p.93-107; Charak ch.XI">
            <div className="dt-table-wrap">
              <table className="dt-table vp-t vp-sahams">
                <thead><tr><th>Saham</th><th>{t('vp.sahams.formula', 'Formula')}</th><th>{t('vp.sahams.point', 'Point')}</th><th>{t('vp.bhava', 'bhāva')}</th><th>{t('vp.lord', 'lord')}</th><th>{t('vp.sahams.strength', 'Strength')}</th><th>{t('vp.sahams.timing', 'Timing')}</th></tr></thead>
                <tbody>
                  {data.sahams.filter((s) => allSahams || CORE.has(s.key)).map((s) => (
                    <tr key={s.key} className={`vp-sah-${s.strength.verdict}`}>
                      <td><b>{s.key}</b><span className="dt-rail-dur"> · {s.gloss}{s.strength.inverted ? ` · ${t('vp.sahams.inverted', 'better weak')}` : ''}</span></td>
                      <td className="dt-rail-dur">{s.formula.replace('saham:', '')}</td>
                      <td>{rs(s.sign)} {dms(s.deg)}</td>
                      <td>{s.house}</td>
                      <td className="dt-tbl-lord" style={{ '--g': `var(--gr-${s.lord})` }}><G k={s.lord} /> <span className="dt-rail-dur">{n1(s.lord_vishwa_bala)}</span></td>
                      <td title={[...s.strength.strong.map((x) => '+ ' + x), ...s.strength.weak.map((x) => '− ' + x)].join('\n')}>
                        <span className={`vp-cat vp-sv-${s.strength.verdict}`}>{t('vp.sahams.' + s.strength.verdict, s.strength.verdict)}</span>
                      </td>
                      <td>{s.timing ? `${Math.round(s.timing.days)} d · ${s.timing.date}` : '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <button type="button" className="vp-more" onClick={() => setAllSahams((v) => !v)}>
              {allSahams ? t('vp.sahams.core', 'Show the commonly used ones') : t('vp.sahams.all', 'Show all fifty')}
            </button>
          </Card>}

          {/* ── mudda ─────────────────────────────────────────────────────── */}
          {mudda && (
            <>
              <div className="vp-mudda-head">
                <span className="dt-chip-k">{t('vp.mudda.variant', 'First period')}</span>
                <div className="dt-view-btns">
                  <button type="button" className={muddaVar === 'prorated' ? 'on' : ''} onClick={() => setMuddaVar('prorated')}>{t('vp.mudda.prorated', 'prorated by the janma nakṣatra (Charak)')}</button>
                  <button type="button" className={muddaVar === 'unprorated' ? 'on' : ''} onClick={() => setMuddaVar('unprorated')}>{t('vp.mudda.unprorated', 'unprorated (some software)')}</button>
                </div>
              </div>
              <MuddaRail mudda={mudda} namer={namer} t={t} />
              <div className="dt-table-wrap">
                <table className="dt-table vp-table">
                  <thead><tr><th>{t('vp.tbl.period', 'Mudda period')}</th><th>{t('vp.tbl.from', 'From')}</th><th>{t('vp.tbl.to', 'To')}</th><th>{t('vp.tbl.days', 'Days')}</th><th>{t('vp.tbl.reading', 'This site’s reading (synthesis)')}</th></tr></thead>
                  <tbody>
                    {mudda.periods.map((p, i) => {
                      const r = readingFor(p, data.projection)
                      return (
                        <tr key={i} className={p.is_current ? 'running' : ''} style={{ '--g': `var(--gr-${p.lord})` }}>
                          <td className="dt-tbl-lord"><G k={p.lord} s={16} />{p.kind !== 'full' && <span className="dt-rail-dur"> · {t('vp.mudda.' + p.kind, p.kind)}</span>}{p.is_current && <span className="dt-badge">{t('dtl.side.current_badge')}</span>}</td>
                          <td>{fmtD(p.start)}</td><td>{fmtD(p.end)}</td><td>{Math.round(p.days)}</td>
                          <td className="vp-reading">
                            {r ? (<>
                              <span className="vp-ov" style={{ color: r.overall > 0.02 ? 'var(--ok-ink)' : r.overall < -0.02 ? 'var(--err-ink)' : 'var(--dim)' }}>{sv(r.overall)}</span>
                              <span className="vp-th up">▲ {themeName(r.best)} {sv(r.bestV)}</span>
                              <span className="vp-th down">▼ {themeName(r.worst)} {sv(r.worstV)}</span>
                            </>) : '—'}
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
              <p className="mx-prov">{t('vp.mudda.rule', 'Rule')}: {data.mudda.rule}. {data.mudda.validation}. {data.mudda.note}</p>
              {data.phala && mudda.periods[0]?.reading && (
                <MuddaReadings mudda={mudda} phala={data.phala} projection={data.projection} nm={nm} rs={rs} G={G} themeName={themeName} t={t} />
              )}
            </>
          )}
          <p className="mx-prov">{data.note}</p>
        </>
      )}
    </section>
  )
}
