import { useState, useEffect, useRef } from 'react'
import { SouthIndianChart, NorthIndianChart } from './RasiChart.jsx'
import DashaTree from './DashaTree.jsx'
import CharaDashaTimeline from './CharaDashaTimeline.jsx'
import Appearance from './Appearance.jsx'
import Logo from './Logo.jsx'
import { makeNamer } from './naming.js'
import { validTheme, DEFAULT_THEME } from './themes.js'
import Profiles from './Profiles.jsx'
import Account from './Account.jsx'
import Privacy from './Privacy.jsx'
import { profileIdFor, removeProfile as removeFromAccount } from './account.js'
import SignalStack from './SignalStack.jsx'
import RasiCard from './RasiCard.jsx'
import NakshatraCard from './NakshatraCard.jsx'
import DrishtiLedger from './DrishtiLedger.jsx'
import { listProfiles, saveProfile, deleteProfile, replaceAll } from './profiles.js'
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
  const [q, setQ] = useState(place?.name || '')
  const [hits, setHits] = useState([])
  const [busy, setBusy] = useState(false)
  const timer = useRef(null)

  // Loading a saved profile sets `place` from outside; without this the input
  // would sit empty while a place was in fact selected. The search effect below
  // then no-ops, because q === place.name.
  useEffect(() => {
    if (place?.name) setQ(place.name)
  }, [place])

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

/** A swatch drawn with the ruler's own classes, so the key cannot drift from
    the marks it explains. */
function Swatch({ children }) {
  return <svg className="lg-swatch" viewBox="0 0 20 14" aria-hidden="true">{children}</svg>
}

/**
 * Without this the ruler is decoration. Two clauses are load-bearing:
 *
 *  - the whole-sign caveat. A pin hard against an end cap under a cell headed
 *    "3 · Mithuna" reads as "nearly in the 4th" to any chart-literate eye. That
 *    is Placidus thinking, and it is the likeliest way this graphic misleads.
 *  - the nodes. Rāhu and Ketu having no dignity marks is a FINDING (BPHS gives
 *    them none), not a rendering gap.
 */
function RulerLegend() {
  return (
    <div className="ruler-legend">
      <div className="lg-row">
        <span><Swatch><line x1="1" y1="9" x2="19" y2="9" className="rl-axis" />
          <line x1="1.5" y1="5" x2="1.5" y2="13" className="rl-axis" />
          <line x1="18.5" y1="5" x2="18.5" y2="13" className="rl-axis" />
        </Swatch> 0°→30° of the rāśi; caps are the sandhi</span>
        <span><Swatch><line x1="10" y1="9" x2="10" y2="2" className="rl-pin" /></Swatch> graha</span>
        <span><Swatch><line x1="9" y1="12" x2="9" y2="1" className="rl-lagna" />
          <line x1="11" y1="12" x2="11" y2="1" className="rl-lagna" /></Swatch> lagna</span>
        <span><Swatch><line x1="10" y1="9" x2="10" y2="2" className="rl-pin rx" />
          <line x1="10" y1="2" x2="6" y2="2" className="rl-barb" /></Swatch> retrograde</span>
      </div>
      <div className="lg-row">
        <span><Swatch><line x1="10" y1="4" x2="10" y2="13" className="rl-nak" /></Swatch> nakṣatra start</span>
        <span><Swatch><line x1="10" y1="6" x2="10" y2="12" className="rl-pada" /></Swatch> pada</span>
        <span><Swatch><path d="M 6,13 L 10,5 L 14,13" className="rl-uccha" /></Swatch> exact exaltation</span>
        <span><Swatch><path d="M 6,5 L 10,13 L 14,5" className="rl-nica" /></Swatch> exact debilitation</span>
        <span><Swatch><path d="M 3,13 L 3,7 L 17,7 L 17,13" className="rl-mt" /></Swatch> mūlatrikoṇa arc</span>
      </div>
      <p className="lg-note">
        Whole-sign bhāvas: a graha at 29° is <em>wholly</em> in its own house — the
        ruler measures position in the <strong>sign</strong>, not distance to the next
        house. Rāhu and Ketu carry no dignity marks; BPHS assigns them none.
        Two pins close together mean nothing beyond the sign they share —
        yuti here is rāśi membership, not orb.
      </p>
    </div>
  )
}

// Static nakṣatra names, for the picker buttons — they must render before the
// (lazy) attribute payload arrives. Order is canonical, Aśvinī = 1.
const NAK_NAMES = [
  { name: 'Ashwini', name_iast: 'Aśvinī' }, { name: 'Bharani', name_iast: 'Bharaṇī' },
  { name: 'Krittika', name_iast: 'Kṛttikā' }, { name: 'Rohini', name_iast: 'Rohiṇī' },
  { name: 'Mrigashira', name_iast: 'Mṛgaśira' }, { name: 'Ardra', name_iast: 'Ārdrā' },
  { name: 'Punarvasu', name_iast: 'Punarvasu' }, { name: 'Pushya', name_iast: 'Puṣya' },
  { name: 'Ashlesha', name_iast: 'Āśleṣā' }, { name: 'Magha', name_iast: 'Maghā' },
  { name: 'Purva Phalguni', name_iast: 'Pūrva Phalgunī' },
  { name: 'Uttara Phalguni', name_iast: 'Uttara Phalgunī' },
  { name: 'Hasta', name_iast: 'Hasta' }, { name: 'Chitra', name_iast: 'Citrā' },
  { name: 'Swati', name_iast: 'Svātī' }, { name: 'Vishakha', name_iast: 'Viśākhā' },
  { name: 'Anuradha', name_iast: 'Anurādhā' }, { name: 'Jyeshtha', name_iast: 'Jyeṣṭhā' },
  { name: 'Mula', name_iast: 'Mūla' }, { name: 'Purva Ashadha', name_iast: 'Pūrva Āṣāḍhā' },
  { name: 'Uttara Ashadha', name_iast: 'Uttara Āṣāḍhā' },
  { name: 'Shravana', name_iast: 'Śravaṇa' }, { name: 'Dhanishta', name_iast: 'Dhaniṣṭhā' },
  { name: 'Shatabhisha', name_iast: 'Śatabhiṣā' },
  { name: 'Purva Bhadrapada', name_iast: 'Pūrva Bhādrapadā' },
  { name: 'Uttara Bhadrapada', name_iast: 'Uttara Bhādrapadā' },
  { name: 'Revati', name_iast: 'Revatī' },
]

export default function App() {
  const [route, setRoute] = useState(
    () => (typeof location !== 'undefined' ? location.pathname : '/'),
  )
  useEffect(() => {
    const on = () => setRoute(location.pathname)
    window.addEventListener('popstate', on)
    return () => window.removeEventListener('popstate', on)
  }, [])
  const go = (path) => {
    history.pushState({}, '', path)
    setRoute(path)
    window.scrollTo(0, 0)
  }

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
  const [profiles, setProfiles] = useState(() => listProfiles())
  const [activeProfile, setActiveProfile] = useState(null)
  // Which graha the analysis panel is showing. Sūrya is the conventional
  // first entry, so it is the least surprising default.
  const [picked, setPicked] = useState('sun')
  // The twelve rasi reference cards. Fetched once, lazily — they are
  // static reference, independent of any chart.
  const [rasis, setRasis] = useState(null)
  const [openRasi, setOpenRasi] = useState(null)
  // The 27 nakṣatra reference cards — traditional-tier attributes (gaṇa, yoni,
  // …) BPHS itself does not carry. Fetched once, lazily, like the rāśis. The
  // picker labels come from a static name list so it can render before the
  // (larger) attribute payload has loaded.
  const [nakAttrs, setNakAttrs] = useState(null)
  const [openNak, setOpenNak] = useState(null)
  // The signed-in account, lifted out of <Account> so that deleting a chart
  // here can also delete the server copy. Without this the × removed the
  // local copy and the encrypted one silently returned on the next sign-in,
  // which reverses the user's delete rather than merely half-doing it.
  const [acct, setAcct] = useState(null)
  // The account controls are collapsed by default. Most visitors never make an
  // account, and the charts already in this browser are what they came back
  // for — so those stay visible and the rest folds away.
  const [savedOpen, setSavedOpen] = useState(false)
  // Dṛṣṭi selection. `hovered` is transient (pointer), `pinned` is sticky
  // (click/tap). The ledger always needs a subject, so it falls back to Sūrya;
  // the CHART highlights only a real selection, so it stays quiet at rest and
  // the ledger's default does not permanently mark a graha in the figure.
  const [hovered, setHovered] = useState(null)
  const [pinned, setPinned] = useState(null)
  const [rowSign, setRowSign] = useState(null)
  const subject = hovered ?? pinned ?? 'sun'
  const marked = hovered ?? pinned
  const pinGraha = (k) => { setPinned((p) => (p === k ? null : k)); setHovered(null) }

  // Appearance, remembered across visits. validTheme guards a stale saved key
  // (e.g. the retired "parchment") from leaving the page themeless.
  const [theme, setTheme] = useState(
    () => validTheme(localStorage.getItem('theme') ?? DEFAULT_THEME),
  )
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

  // Rāśi cards are static reference and do not depend on a chart, so they load
  // once on demand rather than with every cast.
  useEffect(() => {
    if (openRasi === null || rasis) return
    fetch(`${API}/api/rasis`)
      .then((r) => r.json())
      .then((j) => setRasis(j.rasis))
      .catch(() => setRasis([]))
  }, [openRasi, rasis])

  // Nakṣatra attribute table — same lazy-once pattern as the rāśis.
  useEffect(() => {
    if (openNak === null || nakAttrs) return
    fetch(`${API}/api/nakshatra-attributes`)
      .then((r) => r.json())
      .then((j) => setNakAttrs(j))
      .catch(() => setNakAttrs({ nakshatras: [] }))
  }, [openNak, nakAttrs])

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
      // Only remember births that actually produced a chart — saving on submit
      // would fill the list with typos and out-of-range dates.
      const saved = saveProfile({ name, date, time, place })
      setProfiles(saved)
      setActiveProfile(saved[0]?.id ?? null)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  /** Load a saved chart back into the form and cast it straight away. */
  async function useProfile(p) {
    setName(p.name || ''); setDate(p.date); setTime(p.time); setPlace(p.place)
    setActiveProfile(p.id)
    setError(''); setBusy(true); setChart(null)
    try {
      const r = await fetch(`${API}/api/chart`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: p.name, date: p.date, time: p.time,
          latitude: p.place.latitude, longitude: p.place.longitude,
          timezone: p.place.timezone,
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

  async function removeProfile(id) {
    const gone = profiles.find((p) => p.id === id)
    setProfiles(deleteProfile(id))
    if (activeProfile === id) setActiveProfile(null)
    // Delete the account copy too, or signing in would restore what was just
    // removed. Failure here is not surfaced as an error — the local delete has
    // already succeeded and is what the user asked for — but it is not silent
    // either: the Account panel still lists the server copy.
    if (acct && gone) {
      try {
        await removeFromAccount(acct, await profileIdFor(acct.idKey, gone))
      } catch { /* the account panel remains the source of truth for the server */ }
    }
  }

  const ready = date && time && place
  const Chart = style === 'south' ? SouthIndianChart : NorthIndianChart

  if (route === '/privacy') return <Privacy onBack={() => go('/')} />

  return (
    <div className="page">
      <Appearance
        theme={theme} setTheme={setTheme}
        nameStyle={nameStyle} setNameStyle={setNameStyle}
      />
      <header>
        <h1 className="visually-hidden">Devashaa — Jyotiṣa birth charts</h1>
        <Logo />
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

      <section className="saved">
        <div className="saved-bar">
          <button type="button" className="saved-toggle" aria-expanded={savedOpen}
                  onClick={() => setSavedOpen((o) => !o)}>
            <span className="saved-caret" aria-hidden="true">{savedOpen ? '−' : '+'}</span>
            Save your charts
            <span className="saved-hint">
              {acct
                ? `signed in as ${acct.userid}`
                : profiles.length
                  ? `${profiles.length} in this browser`
                  : 'in this browser, or to an account'}
            </span>
          </button>
          <Profiles
            profiles={profiles}
            activeId={activeProfile}
            onPick={useProfile}
            onDelete={removeProfile}
          />
        </div>
        {savedOpen && (
          <Account
            profiles={profiles}
            onAccount={setAcct}
            onMerged={(merged) => setProfiles(replaceAll(merged))}
          />
        )}
      </section>

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
            <div className="chart-figure">
              <Chart
                grahas={chart.grahas}
                lagnaRasi={chart.lagna_rasi}
                lagnaVargaSign={chart.lagna_vargas[varga]}
                vargaKey={varga}
                namer={namer}
                landmarks={chart.landmarks}
                lagnaLongitude={chart.lagna_longitude}
                gandanta={chart.gandanta}
                active={marked}
                onHover={setHovered}
                onPin={pinGraha}
                highlightSign={rowSign}
              />
              {style === 'south' && varga === 'D1' && <RulerLegend />}
              {style === 'north' && (
                <p className="frame-note">
                  The North Indian frame is a <em>bhāva</em> diagram — it discards sign
                  geometry by design. For degree behaviour, use the South Indian frame.
                </p>
              )}
            </div>
            {chart.analysis && !chart.analysis.error && (
              <DrishtiLedger
                drishti={chart.analysis.drishti}
                grahas={chart.grahas}
                namer={namer}
                varga={varga}
                subject={subject}
                onPickSubject={pinGraha}
                onHoverSign={setRowSign}
              />
            )}
          </section>

          {chart.analysis && !chart.analysis.error && (
            <section className="table-panel">
              <h3>What BPHS says about each graha</h3>
              <div className="graha-picker">
                {chart.grahas.map((g) => (
                  <button type="button" key={g.key}
                          className={picked === g.key ? 'on' : ''}
                          onClick={() => setPicked(g.key)}>
                    {namer.graha(g)}
                  </button>
                ))}
              </div>
              <SignalStack
                signals={chart.analysis.grahas[picked]}
                graha={chart.grahas.find((g) => g.key === picked)}
                namer={namer}
              />
            </section>
          )}

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
              verdicts={chart.dasha?.verdicts}
              positions={Object.fromEntries(chart.grahas.map((g) => [g.key, g.rasi]))}
              lagna={chart.lagna_rasi}
            />

            {/* Jaimini Chara Daśā — a sign-based daśā, a different school from
                the nakṣatra daśās above. Its own quieter timeline (no ch.47
                verdict colour) with the sequence-direction toggle, since that
                rule is not in the available source. */}
            {chart.dasha?.chara?.lengths?.length > 0 && (
              <div className="chara-block">
                <h4 className="chara-h">
                  Chara Daśā <span className="chara-tag">Jaimini · sign-based</span>
                </h4>
                <CharaDashaTimeline
                  chara={chart.dasha.chara}
                  lagna={chart.lagna_rasi}
                  jdUt={chart.jd_ut}
                  namer={namer}
                />
              </div>
            )}
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

      {/* Rāśi reference. Deliberately outside the chart block: these are
          reference pages about the twelve signs, not a reading, and they work
          with no birth data at all. */}
      <section className="table-panel rasi-section">
        <h3>The twelve rāśis</h3>
        <p className="rc-note rasi-intro">
          Reference pages, not sun-signs — and with no date ranges, because BPHS
          has none. There is not one statement in either volume of the form
          “one born with the Sun in …”; ch.34, the closest thing to “what your
          sign means”, is keyed to the <strong>lagna</strong> throughout. Cast a
          chart above and it will tell you your lagna, your janma rāśi (Moon)
          and your Sūrya rāśi — all three, computed.
        </p>
        <div className="rasi-picker">
          {Array.from({ length: 12 }, (_, i) => (
            <button type="button" key={i}
                    className={openRasi === i ? 'on' : ''}
                    onClick={() => setOpenRasi(openRasi === i ? null : i)}>
              {namer.rasi(i)}
            </button>
          ))}
        </div>
        {openRasi !== null && !rasis && <p className="hint">loading…</p>}
        {openRasi !== null && rasis && rasis[openRasi] && (
          <RasiCard
            r={rasis[openRasi]}
            namer={namer}
            names={Array.from({ length: 12 }, (_, i) => namer.rasi(i))}
          />
        )}
      </section>

      {/* The twenty-seven nakṣatras. The complement to the rāśi cards: this is
          exactly the gaṇa/yoni/nāḍī material BPHS lacks, filled from named
          sources on its own tier rather than left for a reader to invent. */}
      <section className="table-panel rasi-section">
        <h3>The twenty-seven nakṣatras</h3>
        <p className="rc-note rasi-intro">
          The muhūrta-tradition attributes of each nakṣatra — gaṇa, yoni, śakti
          and the rest — that <strong>BPHS itself does not carry.</strong> Shown
          on a <strong>traditional</strong> tier beside the BPHS deity and
          Viṁśottarī lord, never blended into them, with every cell citing its
          source and how sure we are of it. Nāḍī is left an explicit gap: it is
          in neither source book.
        </p>
        <div className="rasi-picker">
          {NAK_NAMES.map((nm, i) => (
            <button type="button" key={i}
                    className={openNak === i ? 'on' : ''}
                    onClick={() => setOpenNak(openNak === i ? null : i)}>
              {namer.nakshatra(nm)}
            </button>
          ))}
        </div>
        {openNak !== null && !nakAttrs && <p className="hint">loading…</p>}
        {openNak !== null && nakAttrs?.nakshatras?.[openNak] && (
          <NakshatraCard
            n={nakAttrs.nakshatras[openNak]}
            fieldMeta={nakAttrs.field_meta}
            namer={namer}
          />
        )}
      </section>

      <footer>
        <p>
          Positions from the Swiss Ephemeris <code>.se1</code> files (JPL DE431).
          Divisional rules follow BPHS. Powered by the AGPL Swiss Ephemeris —{' '}
          <a href={import.meta.env.VITE_SOURCE_URL || '#'} rel="noreferrer">
            source code
          </a>.
        </p>
        <p>
          <a href="/privacy"
             onClick={(e) => { e.preventDefault(); go('/privacy') }}>Privacy</a>
          {' '}— no cookies, no trackers, and your charts are encrypted before
          they leave your device.
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
