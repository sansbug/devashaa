import { useState, useEffect, useRef } from 'react'
import { SouthIndianChart, NorthIndianChart } from './RasiChart.jsx'
import DashaTree from './DashaTree.jsx'
import Appearance from './Appearance.jsx'
import { makeNamer } from './naming.js'
import { API } from './config.js'
import './App.css'

const VARGA_LABELS = [
  ['D1', 'Rāśi'], ['D2', 'Horā'], ['D3', 'Drekkāṇa'], ['D4', 'Chaturthāṁśa'],
  ['D7', 'Saptāṁśa'], ['D9', 'Navāṁśa'], ['D10', 'Daśāṁśa'], ['D12', 'Dvādaśāṁśa'],
  ['D16', 'Ṣoḍaśāṁśa'], ['D20', 'Viṁśāṁśa'], ['D24', 'Chaturviṁśāṁśa'],
  ['D27', 'Saptaviṁśāṁśa'], ['D30', 'Triṁśāṁśa'], ['D40', 'Khavedāṁśa'],
  ['D45', 'Akṣavedāṁśa'], ['D60', 'Ṣaṣṭiāṁśa'],
]

// Names come from the active name style (see naming.js) — full, never abbreviated.
// The ṣoḍaśavarga matrix is wider than the page as a result and scrolls
// horizontally, with the graha column pinned so rows keep their labels.

const pad = (n) => String(n).padStart(2, '0')
const fmtDeg = (g) => `${g.degree}°${pad(g.minute)}'${pad(g.second)}"`
const fmtAyan = (v) => {
  const d = Math.floor(v)
  const m = Math.floor((v - d) * 60)
  const s = ((v - d) * 60 - m) * 60
  return `${d}°${pad(m)}'${s.toFixed(2)}"`
}

function PlaceField({ onPick, place }) {
  const [q, setQ] = useState('')
  const [hits, setHits] = useState([])
  const [busy, setBusy] = useState(false)
  const timer = useRef(null)

  useEffect(() => {
    if (!q.trim() || (place && q === place.name)) { setHits([]); return }
    clearTimeout(timer.current)
    // Short debounce: the lookup is a local SQLite query (~0.05 ms), so this only
    // needs to coalesce keystrokes. (It was 600 ms to respect Nominatim's
    // 1 req/sec policy back when place search hit the network.)
    timer.current = setTimeout(async () => {
      setBusy(true)
      try {
        const r = await fetch(`${API}/api/places?q=${encodeURIComponent(q)}`)
        const j = await r.json()
        setHits(j.places || [])
      } catch {
        setHits([])
      } finally {
        setBusy(false)
      }
    }, 150)
    return () => clearTimeout(timer.current)
  }, [q, place])

  return (
    <div className="field place-field">
      <label htmlFor="place">Birth place</label>
      <input
        id="place" type="text" value={q} autoComplete="off"
        placeholder="City, region, country"
        onChange={(e) => setQ(e.target.value)}
      />
      {busy && <div className="hint">searching…</div>}
      {hits.length > 0 && (
        <ul className="hits">
          {hits.map((p, i) => (
            <li key={i}>
              <button type="button" onClick={() => { onPick(p); setQ(p.name); setHits([]) }}>
                <strong>{p.name.split(',')[0]}</strong>
                <span>{p.name.split(',').slice(1).join(',').trim()}</span>
                <em>{p.latitude.toFixed(4)}, {p.longitude.toFixed(4)} · {p.timezone}</em>
              </button>
            </li>
          ))}
        </ul>
      )}
      {place && (
        <div className="picked">
          {place.latitude.toFixed(4)}, {place.longitude.toFixed(4)} · {place.timezone}
        </div>
      )}
    </div>
  )
}

export default function App() {
  const [name, setName] = useState('')
  const [date, setDate] = useState('')
  const [time, setTime] = useState('')
  const [place, setPlace] = useState(null)
  const [chart, setChart] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [varga, setVarga] = useState('D1')
  const [style, setStyle] = useState('south')
  const [health, setHealth] = useState(null)

  // Appearance, remembered across visits.
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'ember')
  const [nameStyle, setNameStyle] = useState(
    () => localStorage.getItem('nameStyle') || 'common',
  )
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('theme', theme)
  }, [theme])
  useEffect(() => { localStorage.setItem('nameStyle', nameStyle) }, [nameStyle])
  const namer = makeNamer(nameStyle)

  useEffect(() => {
    fetch(`${API}/api/health`)
      .then((r) => r.json())
      .then(setHealth)
      .catch(() => setHealth({ status: 'unreachable' }))
  }, [])

  async function submit(e) {
    e.preventDefault()
    setError(''); setBusy(true); setChart(null)
    try {
      const r = await fetch(`${API}/api/chart`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name, date, time,
          latitude: place?.latitude, longitude: place?.longitude,
          timezone: place?.timezone,
        }),
      })
      const j = await r.json()
      if (!r.ok) throw new Error(j.error || `HTTP ${r.status}`)
      setChart(j)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  const ready = date && time && place
  const Chart = style === 'south' ? SouthIndianChart : NorthIndianChart

  return (
    <div className="page">
      <Appearance
        theme={theme} setTheme={setTheme}
        nameStyle={nameStyle} setNameStyle={setNameStyle}
      />
      <header>
        <h1>Jyotiṣa</h1>
        <p className="sub">
          Sidereal · Lahiri ayanāṁśa · whole-sign bhāvas · Swiss Ephemeris
          <br />after <em>Bṛhat Parāśara Horā Śāstra</em>
        </p>
        {health && (
          <div className={`health ${health.status}`}>
            {health.status === 'ok'
              ? '● ephemeris verified — reading .se1 (JPL DE431)'
              : `● ephemeris ${health.status} — charts refused`}
          </div>
        )}
      </header>

      <form onSubmit={submit} className="birth-form">
        <div className="field">
          <label htmlFor="name">Name</label>
          <input id="name" value={name} onChange={(e) => setName(e.target.value)}
                 placeholder="optional" />
        </div>
        <div className="field">
          <label htmlFor="date">Birth date</label>
          <input id="date" type="date" value={date} required
                 onChange={(e) => setDate(e.target.value)} />
        </div>
        <div className="field">
          <label htmlFor="time">Birth time (24h, local)</label>
          <input id="time" type="time" value={time} required
                 onChange={(e) => setTime(e.target.value)} />
        </div>
        <PlaceField onPick={setPlace} place={place} />
        <button type="submit" className="go" disabled={!ready || busy}>
          {busy ? 'Calculating…' : 'Cast chart'}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {chart && (
        <main className="result">
          <section className="meta">
            <h2>{chart.name || 'Chart'}</h2>
            <dl>
              <div><dt>Local</dt><dd>{chart.local_time}</dd></div>
              <div><dt>Zone</dt><dd>{chart.timezone} ({chart.utc_offset_hours >= 0 ? '+' : ''}{chart.utc_offset_hours}h)</dd></div>
              <div><dt>UTC</dt><dd>{chart.utc}</dd></div>
              <div><dt>Julian day</dt><dd>{chart.jd_ut.toFixed(6)}</dd></div>
              <div><dt>Ayanāṁśa</dt><dd>{fmtAyan(chart.ayanamsa_value)}</dd></div>
              <div><dt>Lagna</dt><dd>{namer.rasi(chart.lagna_rasi)} · {namer.nakshatra(chart.lagna_nakshatra)} pada {chart.lagna_nakshatra.pada}</dd></div>
            </dl>
          </section>

          <section className="chart-panel">
            <div className="controls">
              <div className="styles">
                <button type="button" className={style === 'south' ? 'on' : ''}
                        onClick={() => setStyle('south')}>South Indian</button>
                <button type="button" className={style === 'north' ? 'on' : ''}
                        onClick={() => setStyle('north')}>North Indian</button>
              </div>
              <div className="vargas">
                {VARGA_LABELS.map(([k, label]) => (
                  <button type="button" key={k} title={label}
                          className={varga === k ? 'on' : ''}
                          onClick={() => setVarga(k)}>{k}</button>
                ))}
              </div>
              <div className="varga-name">
                {VARGA_LABELS.find(([k]) => k === varga)[1]}
              </div>
            </div>
            <Chart
              grahas={chart.grahas}
              lagnaRasi={chart.lagna_rasi}
              lagnaVargaSign={chart.lagna_vargas[varga]}
              vargaKey={varga}
              namer={namer}
            />
          </section>

          <section className="table-panel">
            <h3>Daśā</h3>
            <DashaTree
              dasha={chart.dasha}
              chartMeta={{
                jd_ut: chart.jd_ut,
                moon_nakshatra_index: chart.grahas.find((g) => g.key === 'moon').nakshatra.index,
                moon_nakshatra_fraction: chart.grahas.find((g) => g.key === 'moon').nakshatra.fraction,
                moon_longitude: chart.grahas.find((g) => g.key === 'moon').longitude,
                timezone: chart.timezone,
              }}
              nameOf={(key) => namer.graha(chart.grahas.find((g) => g.key === key))}
            />
          </section>

          <section className="table-panel">
            <h3>Grahas</h3>
            <div className="scroll">
              <table>
                <thead>
                  <tr>
                    <th>Graha</th><th>Rāśi</th><th>Degree</th><th>Bhāva</th>
                    <th>Nakṣatra</th><th>Pada</th><th>Deity</th><th>Rāśi lord</th><th>Speed</th>
                  </tr>
                </thead>
                <tbody>
                  {chart.grahas.map((g) => (
                    <tr key={g.key}>
                      <td className="graha-name">
                        {namer.graha(g)}
                        {/* the English gloss is redundant once names ARE English */}
                        {nameStyle !== 'english' &&
                          <span className="en"> {g.name_en}</span>}
                      </td>
                      <td>
                        {namer.grahaRasi(g)}
                        {nameStyle !== 'english' &&
                          <span className="en"> {g.rasi_name_en}</span>}
                      </td>
                      <td className="num">
                        {fmtDeg(g)}{g.retrograde && <span className="rx-mark">℞</span>}
                      </td>
                      <td className="num">{g.bhava}</td>
                      <td>{namer.nakshatra(g.nakshatra)}</td>
                      <td className="num">{g.nakshatra.pada}</td>
                      <td className="deity">{namer.deity(g.nakshatra)}</td>
                      <td>{namer.rasiLord(g)}</td>
                      <td className="num">{g.speed.toFixed(4)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="table-panel">
            <h3>Ṣoḍaśavarga — all sixteen divisions</h3>
            <div className="scroll">
              <table className="varga-table">
                <thead>
                  <tr>
                    <th>Graha</th>
                    {VARGA_LABELS.map(([k]) => <th key={k}>{k}</th>)}
                  </tr>
                </thead>
                <tbody>
                  <tr className="lagna-row">
                    <td className="graha-name">Lagna</td>
                    {VARGA_LABELS.map(([k]) => (
                      <td key={k}>{namer.rasi(chart.lagna_vargas[k])}</td>
                    ))}
                  </tr>
                  {chart.grahas.map((g) => (
                    <tr key={g.key}>
                      <td className="graha-name">{namer.graha(g)}</td>
                      {VARGA_LABELS.map(([k]) => (
                        <td key={k}>{namer.rasi(g.vargas[k])}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </main>
      )}

      <footer>
        <p>
          Positions from the Swiss Ephemeris <code>.se1</code> files (JPL DE431).
          Divisional rules follow BPHS. Powered by the AGPL Swiss Ephemeris —{' '}
          <a href={import.meta.env.VITE_SOURCE_URL || '#'} rel="noreferrer">
            source code
          </a>.
        </p>
        <p>
          Place data from{' '}
          <a href="https://www.geonames.org" rel="noreferrer">GeoNames</a>,
          licensed{' '}
          <a href="https://creativecommons.org/licenses/by/4.0/" rel="noreferrer">
            CC BY 4.0
          </a>.
        </p>
      </footer>
    </div>
  )
}
