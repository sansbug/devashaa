/**
 * Ask your chart — search-driven, chart-tailored explanation (full scope).
 *
 * A free-text query POSTs to /api/explain and renders one of four intents:
 *   • placement — graha in a house/sign: cited reading + bhāva verdict + life arc
 *   • yoga      — a named yoga: its cited BPHS effect + present-in-chart + life arc
 *   • theme     — a life-area: verdict + ledger + significators + events + life arc
 *   • house     — a bhāva: verdict + every occupant's cited reading + life arc
 * Every line is an indication tied to a cited source or a visible ledger, not a fate.
 */
import { useState, useEffect, useRef } from 'react'
import { API } from './config.js'
import { useLang } from './LangContext.jsx'

const EXAMPLES = ['Jupiter in the 2nd house', 'Gajakesari yoga', 'How is September 2026 looking?', 'Chance of marriage next year', 'When did my career rise?']
const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
const monLabel = (ym) => { if (!ym) return ''; const [y, m] = String(ym).split('-').map(Number); return m ? `${MON[m - 1]} ${y}` : String(ym) }
const ORD = ['', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']
const NEUTRAL = [122, 127, 140], ISTA = [43, 138, 111], KASTA = [176, 63, 54]
const _mix = (a, b, t) => `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(',')})`
const netColor = (v) => { const t = Math.max(-1, Math.min(1, v || 0)); return t >= 0 ? _mix(NEUTRAL, ISTA, t) : _mix(NEUTRAL, KASTA, -t) }
const sv = (v) => (v == null ? '—' : (v >= 0 ? '+' : '') + Number(v).toFixed(2))
const BAND_C = { thriving: '#2b8a6f', supported: '#5aa07f', mixed: '#a9791f', stressed: '#c06a55', afflicted: '#b03f36' }
const FACTOR_KEY = { lord: 'matrix.lord', occupants: 'matrix.occ', aspects: 'matrix.asp', karaka: 'matrix.karaka', sthira_karaka: 'matrix.karaka' }
const FACTOR_EN = { lord: 'Lord', occupants: 'Occupants', aspects: 'Aspects in', karaka: 'Kāraka', sthira_karaka: 'Kāraka', bhava: 'House', chara_karaka: 'Kāraka', yoga: 'Yoga', varga: 'Varga' }

// A compact life-arc line of one facet (or overall), with the graha windows shaded.
function Spark({ series, windows }) {
  if (!series || series.length < 2) return null
  const W = 620, H = 92, pad = 6
  const yrs = series.map((p) => p.year)
  const x0 = Math.min(...yrs), x1 = Math.max(...yrs)
  const yMax = Math.max(0.3, ...series.map((p) => Math.abs(p.value || 0)))
  const X = (yr) => pad + ((yr - x0) / Math.max(1, x1 - x0)) * (W - 2 * pad)
  const Y = (v) => (H / 2) - ((v || 0) / yMax) * (H / 2 - pad)
  const line = series.map((p, i) => `${i ? 'L' : 'M'}${X(p.year).toFixed(1)},${Y(p.value).toFixed(1)}`).join(' ')
  return (
    <svg className="xp-spark" viewBox={`0 0 ${W} ${H}`} preserveAspectRatio="none" role="img">
      {(windows || []).map((w, i) => (
        <rect key={i} x={X(w.from)} y="0" width={Math.max(2, X(w.to) - X(w.from))} height={H} className="xp-spark-win" />
      ))}
      <line x1="0" y1={H / 2} x2={W} y2={H / 2} className="xp-spark-zero" />
      <path d={line} className="xp-spark-line" fill="none" />
      {series.filter((p) => p.inWindow).map((p, i) => (
        <circle key={i} cx={X(p.year)} cy={Y(p.value)} r="2.4" fill={netColor(p.value)} />
      ))}
    </svg>
  )
}

export default function ExplainPanel({ date, time, place, namer, initialQuery }) {
  const { t, lang } = useLang()
  const nm = (k) => (namer && namer.grahaKey ? namer.grahaKey(k) : k)
  const rasiName = (i) => (namer && namer.rasi ? namer.rasi(i) : i)
  const facetName = (f) => t('matrix.facet.' + f, f)

  const [q, setQ] = useState('')
  const [data, setData] = useState(null)
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const panelRef = useRef(null)
  const [flash, setFlash] = useState(false)

  const ask = (query) => {
    const text = (query != null ? query : q).trim()
    if (!text || !date || !time || !place) return
    setQ(text); setBusy(true); setErr(''); setData(null)
    fetch(`${API}/api/explain`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, time, latitude: place.latitude, longitude: place.longitude, timezone: place.timezone, query: text, lang }),
    })
      .then((r) => r.json())
      .then((j) => { if (j.error) setErr(j.error); else setData(j) })
      .catch((e) => setErr(String(e)))
      .finally(() => setBusy(false))
  }

  // the chart-side "Ask" box feeds a { q, nonce } object; run it, then bring the
  // panel into view with a brief highlight so the answer is obviously "here" — the
  // result renders in this section, well below the chart it was asked from.
  useEffect(() => {
    if (!initialQuery || !initialQuery.q) return
    ask(initialQuery.q)
    const el = panelRef.current
    if (!el) return
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    setFlash(true)
    const id = setTimeout(() => setFlash(false), 1200)
    return () => clearTimeout(id)
  }, [initialQuery])  // eslint-disable-line react-hooks/exhaustive-deps

  // ── shared renderers ──
  const Reading = ({ reading }) => (
    <div className="xp-block">
      <h4>{t('explain.reading', 'The reading')} <span className="xp-tier">classical</span></h4>
      {reading && reading.available ? (
        <ul className="xp-sources">
          {reading.sources.map((s, i) => (<li key={i}><span className="xp-cite">{s.citation}</span> {s.text}</li>))}
        </ul>
      ) : <p className="xp-refuse">{(reading && reading.note) || ''}</p>}
    </div>
  )

  const Verdict = ({ bhava }) => (
    <>
      <div className="xp-verdict">
        <span className="xp-net" style={{ background: netColor(bhava.net), color: '#fff' }}>{sv(bhava.net)}</span>
        <span className="xp-band" style={{ color: BAND_C[bhava.band] }}>{t('matrix.band.' + bhava.band, bhava.band)}</span>
        <span className="xp-lord">{ORD[bhava.house]} {t('explain.house', 'house')} · {t('matrix.lord', 'Lord')} {nm(bhava.lord)}</span>
      </div>
      <ul className="xp-ledger">
        {bhava.ledger.map((c, i) => (
          <li key={i}>
            <span className="xp-lf">{t(FACTOR_KEY[c.factor] || 'x', FACTOR_EN[c.factor] || c.factor)}</span>
            <span className="xp-lv" style={{ color: netColor(c.value) }}>{sv(c.value)}</span>
            <span className="xp-ld">{c.detail}</span>
            {c.citation && <span className="xp-lc">{c.citation}</span>}
          </li>
        ))}
      </ul>
    </>
  )

  const Life = ({ life, subjectGrahas }) => {
    if (!life) return null
    const hasWin = life.windows && life.windows.length
    return (
      <div className="xp-block">
        <h4>{t('explain.life', 'Over your life')}</h4>
        {hasWin ? (
          <>
            <p className="xp-aside">
              {(subjectGrahas || []).map(nm).join(' · ')} {t('explain.ranMaha', 'ran its mahādaśā')} {life.windows.map((w) => w.from === w.to ? w.from : `${w.from}–${w.to}`).join(', ')}
              {life.primaryFacet && life.tone !== 'none' && (<> · {facetName(life.primaryFacet)} {t('explain.tone.' + life.tone, life.tone)}</>)}.
            </p>
            <Spark series={life.series} windows={life.windows} />
            {life.relevantFacets && life.relevantFacets.length > 0 && (
              <div className="xp-deltas">
                {life.relevantFacets.map((fk) => {
                  const d = life.facetDeltas[fk]
                  return (<div key={fk} className="xp-delta">
                    <span className="xp-dn">{facetName(fk)}</span>
                    <span className="xp-dv">{t('explain.during', 'during')} <b style={{ color: netColor(d.during) }}>{sv(d.during)}</b> {t('explain.vsLife', 'vs life')} {sv(d.lifetime)}</span>
                  </div>)
                })}
              </div>
            )}
          </>
        ) : <p className="xp-aside">{(subjectGrahas || []).map(nm).join(' · ')} {t('explain.noMaha', 'has not run a mahādaśā within the span shown.')}</p>}
      </div>
    )
  }

  const CHARA = { 'Ātmakāraka': 'Ātmakāraka', AmK: 'Amātyakāraka', DK: 'Dārakāraka', PK: 'Putrakāraka', BK: 'Bhrātṛkāraka', MK: 'Mātṛkāraka', GK: 'Gnātikāraka' }
  const houseList = (hs) => (hs || []).map((h) => ORD[h] || h).join(', ')

  const GrahaFacets = ({ gf, graha, asOf }) => {
    const a = gf.aspects || {}, tr = gf.transit, ro = gf.role || {}
    const casts = (a.castsHouses && a.castsHouses.length) || (a.castsGrahas && a.castsGrahas.length)
    return (
      <div className="xp-block">
        <h4>{t('explain.related', 'Everything else about')} {nm(graha)}</h4>
        <div className="xp-facets">
          <div className="xp-facet"><span className="xp-facet-k">{t('explain.drishti', 'Dṛṣṭi · aspects')}</span>
            <span className="xp-facet-v">
              {casts ? <>{t('explain.castsOn', 'casts on')} {houseList(a.castsHouses)}{a.castsGrahas && a.castsGrahas.length ? ` · ${a.castsGrahas.map(nm).join(', ')}` : ''}</> : t('explain.noAspect', 'casts no full aspect')}
              {a.receivedFrom && a.receivedFrom.length ? <> · {t('explain.aspectedBy', 'aspected by')} {a.receivedFrom.map(nm).join(', ')}</> : null}
            </span></div>
          {tr && <div className="xp-facet"><span className="xp-facet-k">{asOf ? `${t('explain.gocharaOf', 'Gochara')} · ${monLabel(asOf)}` : t('explain.gochara', 'Gochara · transit now')}</span>
            <span className="xp-facet-v">{asOf ? t('explain.thenIn', 'then in') : t('explain.todayIn', 'today in')} {rasiName(tr.sign)} · {ORD[tr.houseFromLagna]} {t('explain.fromLagna', 'from lagna')}{tr.houseFromMoon ? `, ${ORD[tr.houseFromMoon]} ${t('explain.fromMoon', 'from the Moon')}` : ''}{tr.bindu != null ? <> · <b className={'xp-tone-' + tr.tone}>{t('explain.tone.' + tr.tone, tr.tone)}</b> ({tr.bindu}/8 {t('explain.bindu', 'bindu')})</> : ''}</span></div>}
          <div className="xp-facet"><span className="xp-facet-k">{t('explain.role', 'Role')}</span>
            <span className="xp-facet-v">
              {ro.charaRoles && ro.charaRoles.length ? <><b>{ro.charaRoles.map((r) => CHARA[r] || r).join(', ')}</b>; </> : null}
              {ro.rules && ro.rules.length ? <>{t('explain.rules', 'rules')} {houseList(ro.rules)}; </> : null}
              {ro.karakaHouses && ro.karakaHouses.length ? <>{t('explain.karakaOf', 'natural kāraka of')} {houseList(ro.karakaHouses)}; </> : null}
              {ro.dispositor ? <>{t('explain.dispositor', 'dispositor')} {nm(ro.dispositor)}; </> : null}
              {ro.conjunct && ro.conjunct.length ? <>{t('explain.with', 'with')} {ro.conjunct.map(nm).join(', ')}; </> : <>{t('explain.alone', 'alone in its house')}; </>}
              {ro.state ? <span className="xp-state">{ro.state}{ro.retro ? ' ℞' : ''}</span> : null}
              {ro.yogas && ro.yogas.length ? <> · {t('explain.forms', 'forms')} {ro.yogas.join(', ')}</> : null}
            </span></div>
        </div>
        <p className="xp-cite-line">BPHS I ch.26 (dṛṣṭi) · gochara + aṣṭakavarga</p>
      </div>
    )
  }

  const foot = <p className="xp-foot">{t('explain.foot', 'Classical readings are cited, dated renderings on their own tier — never blended with BPHS. The chart verdict opens a weighted ledger; the life arc is a broad shape, not a record of events.')}</p>

  // ── per-intent results ──
  const renderResult = () => {
    if (!data || data.parsed === null) return null
    if (data.kind === 'placement') {
      const label = data.axis === 'sign' ? `${nm(data.graha)} · ${rasiName(data.sign)}` : `${nm(data.graha)} · ${t('explain.house', 'house')} ${ORD[data.house] || data.house}`
      return (<div className="xp-result">
        <div className="xp-head"><span className="xp-q">{label}</span>
          <span className={'xp-inchart ' + (data.inChart ? 'yes' : 'no')}>{data.inChart ? t('explain.inchart', 'in your chart') : t('explain.notinchart', 'not in your chart')}</span></div>
        <Reading reading={data.reading} />
        {data.bhava && (<div className="xp-block"><h4>{t('explain.inchartH', 'In your chart')}</h4>
          {data.axis === 'house' && !data.inChart && (<p className="xp-aside">{t('explain.actualHouse', 'Your')} {nm(data.graha)} {t('explain.sits', 'sits in the')} {ORD[data.placement.house] || data.placement.house} {t('explain.house', 'house')}{data.occupants && data.occupants.length ? ` · ${ORD[data.house]} ${t('explain.houseOcc', 'house holds')}: ${data.occupants.map(nm).join(', ')}` : ` · ${ORD[data.house]} ${t('explain.houseEmpty', 'house is empty')}`}.</p>)}
          {data.axis === 'sign' && (<p className="xp-aside">{rasiName(data.sign)} {t('explain.isYour', 'is your')} {ORD[data.signHouse] || data.signHouse} {t('explain.house', 'house')}.</p>)}
          <Verdict bhava={data.bhava} /></div>)}
        {data.grahaFacets && <GrahaFacets gf={data.grahaFacets} graha={data.graha} asOf={data.transitAsOf} />}
        <Life life={data.life} subjectGrahas={[data.graha]} />{foot}
      </div>)
    }
    if (data.kind === 'yoga') {
      const y = data.yoga
      return (<div className="xp-result">
        <div className="xp-head"><span className="xp-q">{y.name}</span>
          <span className={'xp-inchart ' + (y.present ? 'yes' : 'no')}>{y.present ? t('explain.present', 'present in your chart') : t('explain.notpresent', 'not in your chart')}</span>
          {y.family && <span className="xp-fam">{y.family}</span>}</div>
        <div className="xp-block"><h4>{t('explain.whatItMeans', 'What it means')} <span className="xp-tier">śloka</span></h4>
          <p className="xp-effect">{y.effect}</p>
          {y.citation && <p className="xp-cite-line">{y.citation}</p>}
          {y.present && y.strength && y.strength.role && (<p className="xp-aside">{t('explain.formedBy', 'formed by')} {(y.strength.grahas || []).map((g) => nm(g.graha)).join(', ')}{y.strength.fructifies != null ? ` · ${y.strength.fructifies ? t('explain.fructifies', 'fructifies') : t('explain.weakStrength', 'strength not confirmed')}` : ''}.</p>)}
          {y.present && y.grahas && y.grahas.length > 0 && (!y.strength || !y.strength.role) && (<p className="xp-aside">{t('explain.formedBy', 'formed by')} {y.grahas.map(nm).join(', ')}.</p>)}
        </div>
        <Life life={data.life} subjectGrahas={y.grahas} />{foot}
      </div>)
    }
    if (data.kind === 'theme') {
      const v = data.verdict
      return (<div className="xp-result">
        <div className="xp-head"><span className="xp-q">{t('matrix.theme.' + data.theme, v ? v.name : data.theme)}</span>
          {v && <span className="xp-band" style={{ color: BAND_C[v.band] }}>{t('matrix.band.' + v.band, v.band)} {sv(v.net)}</span>}</div>
        {v && (<div className="xp-block"><h4>{t('explain.themeVerdict', 'Where it stands')}</h4>
          <ul className="xp-ledger">{v.ledger.filter((c) => c.value != null).slice(0, 8).map((c, i) => (
            <li key={i}><span className="xp-lf">{c.factor === 'bhava' ? `${t('explain.house', 'house')} ${c.house}` : c.graha ? nm(c.graha) : t(FACTOR_KEY[c.factor] || 'x', FACTOR_EN[c.factor] || c.factor)}</span>
              <span className="xp-lv" style={{ color: netColor(c.value) }}>{sv(c.value)}</span>
              <span className="xp-ld">{c.detail || (c.chart ? c.chart : '')}</span></li>))}</ul>
          <p className="xp-aside">{t('explain.significators', 'Significators')}: {t('explain.houses', 'houses')} {data.houses.join(', ')}{data.karakas.length ? ` · ${t('explain.karakas', 'kārakas')} ${data.karakas.map(nm).join(', ')}` : ''}.</p></div>)}
        {data.events && data.events.length > 0 && (<div className="xp-block"><h4>{t('explain.nearFuture', 'Near future')}</h4>
          <ul className="xp-events">{data.events.map((e, i) => (
            <li key={i}><span className={'xp-ev ' + (e.good ? 'up' : 'down')}>{e.good ? '▲' : '▼'}</span> {e.from}{e.to !== e.from ? `–${e.to}` : ''}<span className="xp-ev-d"> · {nm(e.maha)}–{nm(e.antar)}</span></li>))}</ul></div>)}
        <Life life={data.life} subjectGrahas={data.karakas} />{foot}
      </div>)
    }
    if (data.kind === 'dasha') {
      return (<div className="xp-result">
        <div className="xp-head"><span className="xp-q">{nm(data.graha)} {t('matrix.dashaword', 'daśā')}</span></div>
        {data.current && (<p className="xp-aside">{t('explain.nowRunning', 'Now running')}: {nm(data.current.maha)} {t('matrix.dashaword', 'daśā')} {t('explain.until', 'until')} {data.current.mahaEnd}{data.current.antar ? ` · ${nm(data.current.antar)} ${t('explain.antarWord', 'antardaśā')} ${t('explain.until', 'until')} ${data.current.antarEnd}` : ''}.</p>)}
        <div className="xp-block"><h4>{nm(data.graha)} — {t('explain.mahaSpans', 'mahādaśā spans')}</h4>
          {data.periods.length ? (<ul className="xp-events">
            {data.periods.map((p, i) => (<li key={i}><span className="xp-ev up">{p.current ? '●' : '○'}</span> {p.from} → {p.to} <span className="xp-ev-d">({p.years}y{p.current ? ` · ${t('explain.runningNow', 'running now')}` : ''})</span></li>))}
          </ul>) : (<p className="xp-aside">{t('explain.noDashaSpan', 'This graha runs no mahādaśā inside the 120-year cycle shown.')}</p>)}
          <p className="xp-cite-line">Viṁśottarī · {data.yearSystem}</p></div>
        {foot}
      </div>)
    }
    if (data.kind === 'period' && data.preBirth) {
      return (<div className="xp-result">
        <div className="xp-head"><span className="xp-q">{monLabel(data.window.from)}{data.window.to !== data.window.from ? ` — ${monLabel(data.window.to)}` : ''}</span></div>
        <p className="xp-refuse">{t('explain.preBirth', 'This window falls before the birth')} ({monLabel(data.birth)}) — {t('explain.preBirthNote', 'a natal chart reads a life, so nothing is projected before it begins.')}</p>
        {foot}
      </div>)
    }
    if (data.kind === 'period') {
      const w = data.window
      const label = monLabel(w.from) + (w.to !== w.from ? ` — ${monLabel(w.to)}` : '')
      const pc = data.panchang
      return (<div className="xp-result">
        <div className="xp-head"><span className="xp-q">{label}</span>
          <span className="xp-net" style={{ background: netColor(data.overall), color: '#fff' }}>{sv(data.overall)}</span></div>
        {data.dasha && data.dasha.length > 0 && (
          <p className="xp-aside">{t('explain.dashaThen', 'Running daśā')}: {data.dasha.map((d, i) => `${nm(d.maha)}–${nm(d.antar)}${data.dasha.length > 1 ? ` (${monLabel(d.month)}→)` : ''}`).join(' · ')}</p>)}
        <div className="xp-block"><h4>{t('explain.themesWindow', 'Life-areas in this window')}</h4>
          <div className="xp-thchips">
            {data.themes.best.map((a) => (<span key={a.key} className="xp-thchip up">▲ {t('matrix.theme.' + a.key, a.name)} <b>{sv(a.v)}</b></span>))}
            {data.themes.strain.map((a) => (<span key={a.key} className="xp-thchip down">▼ {t('matrix.theme.' + a.key, a.name)} <b>{sv(a.v)}</b></span>))}
            {!data.themes.best.length && !data.themes.strain.length && <span className="xp-aside">{t('explain.quietWindow', 'No life-area stands out — a quiet window.')}</span>}
          </div></div>
        {(data.events.length > 0 || data.changes.length > 0) && (
          <div className="xp-block"><h4>{t('explain.inWindow', 'Marked in this window')}</h4>
            <ul className="xp-events">
              {data.events.map((e, i) => (<li key={'e' + i}><span className={'xp-ev ' + (e.good ? 'up' : 'down')}>{e.good ? '▲' : '▼'}</span> {e.name} · {monLabel(e.from.slice(0, 7))}{e.to.slice(0, 7) !== e.from.slice(0, 7) ? `–${monLabel(e.to.slice(0, 7))}` : ''}</li>))}
              {data.changes.map((e, i) => (<li key={'c' + i}><span className="xp-ev">↻</span> {e.label} · {monLabel((e.date || '').slice(0, 7))}<span className="xp-ev-d"> · {t('matrix.trig.' + e.triggerType, e.triggerType)}</span></li>))}
            </ul></div>)}
        <div className="xp-block"><h4>{t('explain.transitsThen', 'Slow transits then')}</h4>
          {data.transits.map((tr) => tr.sign != null && (
            <p className="xp-aside" key={tr.graha}>{nm(tr.graha)} {t('explain.todayIn', 'in')} {rasiName(tr.sign)} · {ORD[tr.houseFromLagna]} {t('explain.fromLagna', 'from lagna')} · <b className={'xp-tone-' + tr.tone}>{t('explain.tone.' + tr.tone, tr.tone)}</b>{tr.bindu != null ? ` (${tr.bindu}/8)` : ''}</p>))}</div>
        {pc && (<div className="xp-block"><h4>{t('explain.auspicious', 'Auspicious days')} <span className="xp-tier">pañcāṅga</span></h4>
          <p className="xp-aside">{pc.auspicious} {t('explain.auspN', 'auspicious')} · {pc.mixed} {t('explain.mixedN', 'mixed')} · {pc.inauspicious} {t('explain.inauspN', 'inauspicious')} {t('explain.of', 'of')} {pc.days} — {t('explain.bestDays', 'best')}: {pc.best.map((b) => `${Number(b.date.slice(8, 10))} ${MON[Number(b.date.slice(5, 7)) - 1]} (${b.score})`).join(', ')}</p></div>)}
        {foot}
      </div>)
    }
    if (data.kind === 'when') {
      if (data.care) {
        return (<div className="xp-result">
          <div className="xp-head"><span className="xp-q">{t('matrix.theme.' + data.theme, data.themeName)}</span><span className="xp-inchart no">♥</span></div>
          <p className="xp-refuse">{data.refusal}</p>{foot}
        </div>)
      }
      const past = data.direction === 'past'
      const winLabel = (x) => past ? (x.from === x.to ? String(x.from) : `${x.from}–${x.to}`) : (x.from === x.to ? monLabel(x.from) : `${monLabel(x.from)}–${monLabel(x.to)}`)
      return (<div className="xp-result">
        <div className="xp-head"><span className="xp-q">{t('matrix.theme.' + data.theme, data.themeName)}</span>
          <span className="xp-fam">{past ? t('explain.lookingBack', 'looking back') : t('explain.ahead', 'ahead')}</span></div>
        {data.ageFloor > 0 && (<p className="xp-aside">{t('explain.ageFloorNote', 'Considered from age')} {data.ageFloor} {t('explain.ageFloorTail', 'on — earlier ages aren’t sensible for this question.')}</p>)}
        {data.focus && (<div className="xp-block"><h4>{monLabel(data.focus.from)}{data.focus.to !== data.focus.from ? ` — ${monLabel(data.focus.to)}` : ''}</h4>
          <p className="xp-aside"><b className={'xp-tone-' + (data.focus.tone === 'supportive' ? 'supportive' : data.focus.tone === 'challenging' ? 'straining' : 'neutral')}>{t('explain.focus.' + data.focus.tone, data.focus.tone)}</b> · {sv(data.focus.v)} ({t('explain.agreement', 'agreement')} {Math.round((data.focus.cf || 0) * 100)}%)
            {data.focus.delta != null && <> · {sv(data.focus.delta)} {t('explain.vsLifeMean', 'vs its life average')}</>}
            {data.focus.changesInWindow && data.focus.changesInWindow.length > 0 && (<> — {data.focus.changesInWindow.map((c) => `${c.label} · ${monLabel((c.date || '').slice(0, 7))}`).join('; ')}</>)}</p></div>)}
        <div className="xp-block"><h4>{past ? t('explain.strongWindowsPast', 'When it ran strongest') : t('explain.strongWindows', 'The stronger windows ahead')}</h4>
          {data.windows.length ? (<ul className="xp-events">
            {data.windows.map((x, i) => (<li key={i}><span className="xp-ev up">▲</span> {winLabel(x)}{x.peak !== x.from || x.peak !== x.to ? ` · ${t('explain.peak', 'peak')} ${past ? x.peak : monLabel(x.peak)}` : ''}<span className="xp-ev-d">{x.age != null ? ` · ${t('explain.ageWord', 'age')} ${x.age}` : ''} · {nm(x.maha)}{x.antar ? `–${nm(x.antar)}` : ''} {t('matrix.dashaword', 'daśā')} · +{(x.delta ?? x.v).toFixed ? (x.delta ?? x.v).toFixed(2) : x.delta} {t('explain.aboveMean', 'above its life average')}</span>
              {x.bhps && (<div className="xp-wq"><span className="xp-wq-tag">{x.bhps.general ? t('explain.bhpsPeriodTag', 'BPHS · this period') : 'BPHS'}</span> “{x.bhps.text}” <span className="xp-wq-cite">— {x.bhps.cite}</span></div>)}
            </li>))}
          </ul>) : (<p className="xp-aside">{past ? t('explain.noPastWin', 'No years stood clearly above this axis’s own life average.') : t('explain.noFutWin', 'No standout windows in the 3-year horizon — the marked signals below carry the answer.')}</p>)}</div>
        {!past && data.changes.length > 0 && (<div className="xp-block"><h4>{t('explain.markedSignals', 'Marked signals')}</h4>
          <ul className="xp-events">{data.changes.map((e, i) => (
            <li key={i}><span className={'xp-ev ' + (e.direction === 'down' ? 'down' : 'up')}>{e.direction === 'down' ? '▼' : e.direction === 'shift' ? '↻' : '▲'}</span> {e.label} · {monLabel((e.date || '').slice(0, 7))}<span className="xp-ev-d"> · {t('matrix.trig.' + e.triggerType, e.triggerType)} · {Math.round((e.cf || 0) * 100)}%</span>
              {e.bhps && (<div className="xp-wq"><span className="xp-wq-tag">{e.bhps.general ? t('explain.bhpsPeriodTag', 'BPHS · this period') : 'BPHS'}</span> “{e.bhps.text}” <span className="xp-wq-cite">— {e.bhps.cite}</span></div>)}
            </li>))}</ul></div>)}
        {data.indications && data.indications.length > 0 && (<div className="xp-block"><h4>{t('explain.indications', 'Standing yoga indications')} <span className="xp-tier">śloka</span></h4>
          {data.indications.map((ind, i) => (<div key={i} className="xp-wq xp-wq-yoga"><span className="xp-wq-tag">{ind.yoga}</span> “{ind.effect}” <span className="xp-wq-cite">— {ind.citation}</span>
            {ind.windows && ind.windows.length > 0 && (<span className="xp-ev-d"> · {t('explain.likelyIn', 'most likely to fructify in')} {ind.windows.map((w) => `${nm(w.lord)} ${t('matrix.dashaword', 'daśā')} ${w.from}–${w.to}`).join(', ')}</span>)}</div>))}</div>)}
        <p className="xp-aside">{past ? t('explain.pastNote', 'The chart cannot know what happened — these are the windows where this axis was most activated, read the same way the future is projected.') : t('explain.futNote', 'Percentages are the clocks’ agreement (conviction), not a probability of a real event — an indication, never a promise.')}</p>
        {foot}
      </div>)
    }
    if (data.kind === 'house') {
      return (<div className="xp-result">
        <div className="xp-head"><span className="xp-q">{ORD[data.house] || data.house} {t('explain.house', 'house')}</span>
          {data.bhava && <span className="xp-band" style={{ color: BAND_C[data.bhava.band] }}>{t('matrix.band.' + data.bhava.band, data.bhava.band)} {sv(data.bhava.net)}</span>}</div>
        {data.focus && (<p className="xp-aside">{monLabel(data.focus.from)}{data.focus.to !== data.focus.from ? `—${monLabel(data.focus.to)}` : ''} · {t('matrix.theme.' + data.focus.theme, data.focus.themeName)}: <b className={'xp-tone-' + (data.focus.tone === 'supportive' ? 'supportive' : data.focus.tone === 'challenging' ? 'straining' : 'neutral')}>{t('explain.focus.' + data.focus.tone, data.focus.tone)}</b> {sv(data.focus.v)} ({t('explain.agreement', 'agreement')} {Math.round((data.focus.cf || 0) * 100)}%)</p>)}
        {data.bhava && (<div className="xp-block"><h4>{t('explain.inchartH', 'In your chart')}</h4>
          <p className="xp-aside">{data.occupants && data.occupants.length ? `${t('explain.houseHolds', 'Holds')}: ${data.occupants.map(nm).join(', ')}` : t('explain.houseEmptyFull', 'No graha occupies this house.')}</p>
          <Verdict bhava={data.bhava} /></div>)}
        {data.occupantReadings && data.occupantReadings.length > 0 && (<div className="xp-block"><h4>{t('explain.occReadings', 'The occupants, classically')} <span className="xp-tier">classical</span></h4>
          {data.occupantReadings.map((o, i) => (<div key={i} className="xp-occ"><span className="xp-occ-g">{nm(o.graha)}</span>
            <ul className="xp-sources">{o.sources.map((s, j) => (<li key={j}><span className="xp-cite">{s.citation}</span> {s.text}</li>))}</ul></div>))}</div>)}
        <Life life={data.life} subjectGrahas={data.bhava ? [data.bhava.lord] : []} />{foot}
      </div>)
    }
    return null
  }

  return (
    <section ref={panelRef} className={'table-panel mx-panel xp-panel' + (flash ? ' xp-flash' : '')} id="rg-explain">
      <h3>{t('explain.title', 'Ask your chart')}</h3>
      <p className="rc-note">{t('explain.sub', 'Ask about any placement, yoga, life-area or house. You get the cited classical reading, your own chart’s verdict for it, and when it has run across your life. An indication, not a fated reading.')}</p>

      <form className="xp-search" onSubmit={(e) => { e.preventDefault(); ask() }}>
        <input type="text" value={q} onChange={(e) => setQ(e.target.value)}
               placeholder={t('explain.placeholder', 'e.g. Jupiter in the 2nd house · Gajakesari yoga · my career')} aria-label={t('explain.title', 'Ask your chart')} />
        <button type="submit" disabled={busy || !q.trim()}>{busy ? t('explain.asking', 'Reading…') : t('explain.ask', 'Ask')}</button>
      </form>
      <div className="xp-eg">{EXAMPLES.map((ex) => (<button type="button" key={ex} className="xp-chip" onClick={() => ask(ex)}>{ex}</button>))}</div>

      {err && <p className="rc-err">{err}</p>}
      {data && data.parsed === null && (
        <div className="xp-none"><p>{t('explain.noparse', 'I couldn’t read that. Try a placement, a yoga, a life-area, or a house — for example:')}</p>
          <div className="xp-eg">{(data.suggestions || []).map((s) => (<button type="button" key={s} className="xp-chip" onClick={() => ask(s)}>{s}</button>))}</div></div>
      )}
      {renderResult()}
    </section>
  )
}
