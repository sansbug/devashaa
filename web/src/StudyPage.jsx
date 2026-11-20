/**
 * /study — the owner's study view. Not linked from the site and marked noindex.
 *
 * It shows, for one chart, every cited relation that fires across D1-D60 (and a
 * transit date), the gap map of what the registered texts cover, and what they are
 * silent on. All of it comes from api/study.py; this page adds no rule or weight.
 *
 * Access: on devashaa.com the Worker answers /api/study only for a signed-in account
 * with the admin role (web/study-worker.js). In local development the page talks to
 * the Python API directly, which answers callers on this machine only.
 */
import { useEffect, useMemo, useState } from 'react'
import { API } from './config.js'
import { signIn, getSession, onSession, signOut } from './pooja/papi.js'

const DEV = import.meta.env.DEV
const RASI = ['Mesh', 'Vrishabh', 'Mithun', 'Kark', 'Simha', 'Kanya', 'Tula', 'Vrishchik', 'Dhanu', 'Makar', 'Kumbh', 'Meen']
const VARGAS = ['D1', 'D2', 'D3', 'D4', 'D7', 'D9', 'D10', 'D12', 'D16', 'D20', 'D24', 'D27', 'D30', 'D40', 'D45', 'D60', 'D1-D60']
const TIER = { sloka: '#7a4b00', classical: '#174f86', modern: '#5b5b5b', traditional: '#2d6a3e', note: '#6b3fa0' }

async function call(path, body) {
  const s = getSession()
  const headers = {}
  if (!DEV && s) { headers['X-User'] = s.userid; headers['X-Auth'] = s.authId }
  if (body) headers['Content-Type'] = 'application/json'
  const r = await fetch((DEV ? API : '') + path, { method: body ? 'POST' : 'GET', headers, body: body ? JSON.stringify(body) : undefined })
  const j = await r.json().catch(() => ({}))
  if (!r.ok) throw new Error(j.error || `HTTP ${r.status}`)
  return j
}

const factors = (f = {}) => [
  f.graha && f.graha[0].toUpperCase() + f.graha.slice(1),
  f.rashi != null && RASI[f.rashi],
  f.bhaav != null && `Bhaav ${f.bhaav}`,
  f.nakshatra != null && `Nakshatr ${f.nakshatra}`,
  f.degree != null && `${Number(f.degree).toFixed(2)}°`,
].filter(Boolean).join(' · ')

function Tier({ t }) {
  return <span className="stv-tier" style={{ background: TIER[t] || '#444' }}>{t}</span>
}

export default function StudyPage({ onBack, birth }) {
  const [session, setSession] = useState(getSession())
  const [owner, setOwner] = useState(DEV)
  const [err, setErr] = useState('')
  const [busy, setBusy] = useState(false)
  const [cred, setCred] = useState({ userid: '', password: '' })
  const [f, setF] = useState(() => ({
    date: birth?.date || '', time: birth?.time || '',
    latitude: birth?.place?.latitude ?? '', longitude: birth?.place?.longitude ?? '',
    timezone: birth?.place?.timezone || '', transit_date: new Date().toISOString().slice(0, 10),
  }))
  const [sensitive, setSensitive] = useState(false)
  const [gaps, setGaps] = useState(null)
  const [led, setLed] = useState(null)
  const [tab, setTab] = useState('chart')
  const [axis, setAxis] = useState('')

  useEffect(() => onSession(setSession), [])
  useEffect(() => {
    const m = document.querySelector('meta[name="robots"]')
    const was = m?.getAttribute('content')
    m?.setAttribute('content', 'noindex, nofollow')
    return () => { if (m && was) m.setAttribute('content', was) }
  }, [])
  useEffect(() => {
    if (DEV || !session) return
    call('/api/study/whoami').then(() => setOwner(true)).catch((e) => { setOwner(false); setErr(e.message) })
  }, [session])

  const doSignIn = async (e) => {
    e.preventDefault(); setErr(''); setBusy(true)
    try { await signIn(cred.userid, cred.password, false) } catch (x) { setErr(x.message) }
    setBusy(false)
  }
  const build = async (e) => {
    e?.preventDefault(); setErr(''); setBusy(true)
    try {
      const body = { ...f, latitude: Number(f.latitude), longitude: Number(f.longitude), show_sensitive: sensitive }
      if (!body.timezone) delete body.timezone
      const [g, l] = await Promise.all([gaps ? Promise.resolve(gaps) : call('/api/study/gaps'), call('/api/study', body)])
      setGaps(g); setLed(l)
    } catch (x) { setErr(x.message) }
    setBusy(false)
  }

  const axes = useMemo(() => [...new Set((led?.rows || []).map((r) => r.axis))].sort(), [led])
  const shown = (led?.rows || []).filter((r) => !axis || r.axis === axis)

  return (
    <div className="page stv">
      <style>{CSS}</style>
      <p><a href="/" onClick={(e) => { e.preventDefault(); onBack() }}>← devashaa</a></p>
      <h1>Study view</h1>
      <p className="sub">Owner only. Every line is one source's cited reading. Lines are never added, netted or ranked. Silence means the registered texts do not cover it.</p>

      {!owner && !session && (
        <form className="stv-card" onSubmit={doSignIn}>
          <b>Sign in with the owner account</b>
          <input placeholder="User id" value={cred.userid} onChange={(e) => setCred({ ...cred, userid: e.target.value })} autoComplete="username" />
          <input placeholder="Password" type="password" value={cred.password} onChange={(e) => setCred({ ...cred, password: e.target.value })} autoComplete="current-password" />
          <button disabled={busy}>Sign in</button>
        </form>
      )}
      {!DEV && session && !owner && (
        <div className="stv-card">Signed in as {session.userid}. {err || 'Checking access…'} <button onClick={signOut}>Sign out</button></div>
      )}

      {owner && (
        <>
          <form className="stv-card stv-form" onSubmit={build}>
            <label>Date <input type="date" value={f.date} onChange={(e) => setF({ ...f, date: e.target.value })} required /></label>
            <label>Time <input type="time" value={f.time} onChange={(e) => setF({ ...f, time: e.target.value })} required /></label>
            <label>Latitude <input value={f.latitude} onChange={(e) => setF({ ...f, latitude: e.target.value })} required /></label>
            <label>Longitude <input value={f.longitude} onChange={(e) => setF({ ...f, longitude: e.target.value })} required /></label>
            <label>Time zone <input placeholder="e.g. Asia/Kolkata" value={f.timezone} onChange={(e) => setF({ ...f, timezone: e.target.value })} /></label>
            <label>Transit date <input type="date" value={f.transit_date} onChange={(e) => setF({ ...f, transit_date: e.target.value })} /></label>
            <label className="stv-check"><input type="checkbox" checked={sensitive} onChange={(e) => setSensitive(e.target.checked)} /> Show sensitive passages</label>
            <button disabled={busy}>{busy ? 'Working…' : 'Build the study'}</button>
            {birth?.date && <span className="stv-muted">Filled from the chart open on the site.</span>}
          </form>
          {err && <p className="stv-err">{err}</p>}

          {led && (
            <>
              <p>{led.counts.rows} cited lines · {led.counts.silences} silences · {led.counts.sensitive_withheld} sensitive passages withheld</p>
              <div className="stv-tabs">
                {[['chart', 'This chart'], ['silent', 'Where the texts are silent'], ['gaps', 'Gap map'], ['uses', 'What each division is for']].map(([k, l]) => (
                  <button key={k} className={tab === k ? 'on' : ''} onClick={() => setTab(k)}>{l}</button>
                ))}
              </div>

              {tab === 'chart' && (
                <>
                  <select value={axis} onChange={(e) => setAxis(e.target.value)}>
                    <option value="">All relations</option>
                    {axes.map((a) => <option key={a} value={a}>{a} ({led.counts.by_axis[a]})</option>)}
                  </select>
                  {VARGAS.map((v) => {
                    const rows = shown.filter((r) => r.varga === v)
                    if (!rows.length) return null
                    return (
                      <section key={v}>
                        <h3>{v}{led.uses?.[v] ? <span className="stv-muted"> · read for {led.uses[v].topic}</span> : null}</h3>
                        <table><tbody>
                          {rows.map((r, i) => (
                            <tr key={i}>
                              <td>{r.axis}{r.transit ? ' (transit)' : ''}</td>
                              <td>{factors(r.factors)}</td>
                              <td><Tier t={r.tier} /> {r.source}<div className="stv-muted">{r.citation}{r.confidence ? ` · ${r.confidence}` : ''}</div></td>
                              <td>
                                {r.polarity && <b>[{r.polarity}] </b>}
                                {r.text ?? <i className="stv-muted">Sensitive passage, withheld.</i>}
                                {r.why && <div className="stv-muted">Why: {r.why.replace(/\{g:(\w+)\}/g, (_, g) => g[0].toUpperCase() + g.slice(1))}</div>}
                                {r.use && <div className="stv-muted">{r.use}</div>}
                                {r.adaptation?.note && <div className="stv-muted">Adapted: {r.adaptation.note}</div>}
                              </td>
                            </tr>
                          ))}
                        </tbody></table>
                      </section>
                    )
                  })}
                </>
              )}

              {tab === 'silent' && (
                <table><tbody>
                  {led.silences.map((s, i) => (
                    <tr key={i}>
                      <td>{s.axis}</td><td>{s.varga}</td>
                      <td>{s.factors?.placements
                        ? Object.entries(s.factors.placements).filter(([, x]) => x != null).map(([k, x]) => `${k} ${RASI[x]}`).join(', ')
                        : factors(s.factors)}</td>
                      <td className="stv-muted">{s.reason}</td>
                    </tr>
                  ))}
                </tbody></table>
              )}

              {tab === 'gaps' && gaps && (
                <>
                  <p className="stv-muted">{gaps.summary.covered} covered · {gaps.summary.partial} partial · {gaps.summary.listed} listed · {gaps.summary.silent} silent. {gaps.note}</p>
                  <table><tbody>
                    {gaps.axes.map((r) => (
                      <tr key={r.axis}>
                        <td>{r.axis}{r.note && <div className="stv-muted">{r.note}</div>}</td>
                        <td className={`stv-${r.status}`}>{r.status}</td>
                        <td>{r.possible ?? 'n/a'}</td>
                        <td>{r.sources.length ? r.sources.map((s, i) => <div key={i}><Tier t={s.tier} /> {s.source}: {s.cells}{s.note && <span className="stv-muted"> {s.note}</span>}</div>) : '—'}</td>
                        <td className="stv-muted">{r.candidates.join(', ')}</td>
                      </tr>
                    ))}
                  </tbody></table>
                </>
              )}

              {tab === 'uses' && (
                <table><tbody>
                  {Object.entries(led.uses || {}).map(([v, u]) => (
                    <tr key={v}><td>{v}</td><td>{u.topic}</td><td className="stv-muted">{u.words}</td><td className="stv-muted">{u.citation}</td></tr>
                  ))}
                </tbody></table>
              )}
            </>
          )}
        </>
      )}
    </div>
  )
}

const CSS = `
.stv table{border-collapse:collapse;width:100%;margin:6px 0 18px;font-size:14px}
.stv td{border:1px solid var(--line,#ddd);padding:4px 6px;vertical-align:top}
.stv-tier{color:#fff;border-radius:3px;padding:0 5px;font-size:12px}
.stv-muted{opacity:.7;font-size:13px}
.stv-card{border:1px solid var(--line,#ddd);border-radius:8px;padding:12px;margin:12px 0;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.stv-form label{display:flex;flex-direction:column;font-size:13px;gap:2px}
.stv-check{flex-direction:row!important;align-items:center;gap:6px!important}
.stv-tabs{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
.stv-tabs button.on{font-weight:700;text-decoration:underline}
.stv-err{color:#b3261e}
.stv-silent{color:#b3261e}.stv-covered{color:#2d6a3e}.stv-partial,.stv-listed{color:#7a4b00}
@media (max-width:640px){.stv table{display:block;overflow-x:auto}}
`
