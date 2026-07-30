import { useState, useEffect, useRef } from 'react'
import { SouthIndianChart, NorthIndianChart } from './RasiChart.jsx'
import SkyWheelChart from './SkyWheel.jsx'
import NavamsaPanel from './NavamsaPanel.jsx'
import MotionPanel from './MotionPanel.jsx'
import ReadingGuide, { NAVAMSA_STEP } from './ReadingGuide.jsx'
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
import ModernNotes from './ModernNotes.jsx'
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

// The life-area each varga is read for. IMPORTANT PROVENANCE: BPHS ch.6 gives the
// divisions' calculation and names only (see docs/bphs-rules.md) — the life-area
// each governs is CLASSICAL / TRADITIONAL usage, not a BPHS śloka. Shown labelled
// "traditional" so it is never mistaken for Parāśara's own words.
const VARGA_SIG = {
  D1: 'the body & the whole life',
  D2: 'wealth & resources',
  D3: 'siblings & courage',
  D4: 'fortune, property & the home',
  D7: 'children & progeny',
  D9: 'spouse, marriage & dharma — and a graha’s inner strength',
  D10: 'career, karma & status',
  D12: 'parents & lineage',
  D16: 'vehicles, comforts & pleasures',
  D20: 'spiritual practice & worship',
  D24: 'education & learning',
  D27: 'overall strengths & weaknesses',
  D30: 'misfortunes, ariṣṭa & character',
  D40: 'auspicious & inauspicious effects (matrilineal)',
  D45: 'conduct & all indications (patrilineal)',
  D60: 'all matters & past-life karma — the finest, heavily weighted',
}
const VARGA_SIG_NOTE = 'BPHS ch.6 gives the sixteen divisions’ calculation and '
  + 'names; the life-area each is read for is classical / traditional usage, not '
  + 'a BPHS śloka.'

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
  // The adjacent "K.N. Rao (modern)" pointer bucket (§3b) — not nakṣatra-based,
  // its own reference block, lazy-loaded on first open.
  const [raoData, setRaoData] = useState(null)
  const [raoOpen, setRaoOpen] = useState(false)
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

  // "How to read this chart" interactive walkthrough.
  const [guideOpen, setGuideOpen] = useState(false)
  // First-time nudge toward the walkthrough — shown once, then remembered.
  const [nudgeSeen, setNudgeSeen] = useState(
    () => localStorage.getItem('rg-nudge-seen') === '1',
  )
  const dismissNudge = () => {
    setNudgeSeen(true)
    try { localStorage.setItem('rg-nudge-seen', '1') } catch { /* private mode */ }
  }
  // Which step the guide opens on (0 for the header button; the navāṁśa step
  // when reached from the D9 nudge). The guide reads it once, on mount.
  const [guideStep, setGuideStep] = useState(0)
  const openGuide = () => { setGuideStep(0); setGuideOpen(true); dismissNudge() }
  // A second first-time nudge, toward the navāṁśa (D9) reading — shown once, when
  // the reader first opens the D9, then remembered separately from the main one.
  const [nvNudgeSeen, setNvNudgeSeen] = useState(
    () => localStorage.getItem('nv-nudge-seen') === '1',
  )
  const dismissNvNudge = () => {
    setNvNudgeSeen(true)
    try { localStorage.setItem('nv-nudge-seen', '1') } catch { /* private mode */ }
  }
  const openGuideAtNavamsa = () => {
    setGuideStep(NAVAMSA_STEP); setGuideOpen(true); dismissNvNudge()
  }
  // Guide steps drive the real panels: select a graha (signal-stack + chart +
  // dṛṣṭi subject), switch style/varga, highlight a sign, and scroll into view.
  const selectGraha = (k) => { setPicked(k); setPinned(k); setHovered(null) }
  const guideActions = {
    setStyle, setVarga, selectGraha, highlightSign: setRowSign,
    scrollTo: (sel) => document.querySelector(sel)?.scrollIntoView({ behavior: 'smooth', block: 'center' }),
  }

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

  // K.N. Rao (modern) pointers — lazy-loaded on first open.
  useEffect(() => {
    if (!raoOpen || raoData) return
    fetch(`${API}/api/modern-pointers`)
      .then((r) => r.json())
      .then((j) => setRaoData(j))
      .catch(() => setRaoData({ error: true }))
  }, [raoOpen, raoData])

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
  const Chart = style === 'south' ? SouthIndianChart
    : style === 'north' ? NorthIndianChart
    : SkyWheelChart

  // The grahas ruling the running mahā and antar daśā — for the wheel's daśā
  // overlay. Time isn't spatial, but WHERE the ruling graha sits is.
  const dashaLords = (() => {
    const dv = chart && chart.dasha && chart.dasha.variants
    const tree = dv ? (dv['360'] || Object.values(dv)[0]) : null
    const maha = tree && tree.mahadashas && tree.mahadashas.find((m) => m.is_current)
    const antar = maha && maha.sub && maha.sub.find((a) => a.is_current)
    return { maha: maha && maha.lord, antar: antar && antar.lord }
  })()
  // The running daśā chain (mahā → antar → pratyantar) with the time remaining
  // in each level, for the wheel's daśā readout. is_current is marked as-of now
  // on the backend, and each node's `end` is the boundary we count down to.
  const runningDasha = (() => {
    const dv = chart && chart.dasha && chart.dasha.variants
    const tree = dv ? (dv['360'] || Object.values(dv)[0]) : null
    const maha = tree && tree.mahadashas && tree.mahadashas.find((m) => m.is_current)
    if (!maha) return null
    const antar = maha.sub && maha.sub.find((a) => a.is_current)
    const praty = antar && antar.sub && antar.sub.find((p) => p.is_current)
    const remain = (endISO) => {
      const ms = new Date(String(endISO).replace(' ', 'T')).getTime() - Date.now()
      if (!(ms > 0)) return 'ending now'
      const days = ms / 86400000
      const y = Math.floor(days / 365.25)
      const m = Math.floor((days - y * 365.25) / 30.4375)
      const d = Math.floor(days - y * 365.25 - m * 30.4375)
      if (y > 0) return `${y}y ${m}m`
      if (m > 0) return `${m}m ${d}d`
      if (d > 0) return `${d}d`
      return `${Math.max(1, Math.floor(ms / 3600000))}h`
    }
    const fmtEnd = (endISO) => {
      const d = new Date(String(endISO).replace(' ', 'T'))
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
    }
    const level = (node, code) => (node && node.end
      ? { code, lord: node.lord, ends: fmtEnd(node.end), remaining: remain(node.end) } : null)
    const levels = [level(maha, 'MD'), level(antar, 'AD'), level(praty, 'PD')].filter(Boolean)
    return levels.length ? { levels } : null
  })()
  // Combust grahas (within their own orb of the Sun) → their separation, for the
  // wheel's combust marker. From the motion module; degrades to null.
  const combust = (() => {
    const m = chart && chart.motion
    if (!m || m.error) return null
    const out = {}
    for (const r of m.grahas) {
      if (r.combustion.applies && r.combustion.combust) out[r.key] = r.combustion.separation
    }
    return Object.keys(out).length ? out : null
  })()

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
          {guideOpen && (
            <ReadingGuide chart={chart} namer={namer} actions={guideActions}
                          initialStep={guideStep}
                          onClose={() => setGuideOpen(false)} />
          )}
          <section className="meta" id="rg-positions">
            <div className="meta-head">
              <h2>{chart.name || 'Chart'}</h2>
              <div className="rg-open-wrap">
                <button type="button" className="rg-open" onClick={openGuide}>
                  How to read this chart →
                </button>
                {!nudgeSeen && !guideOpen && (
                  <div className="rg-nudge" role="note">
                    <button type="button" className="rg-nudge-x" onClick={dismissNudge}
                            aria-label="Dismiss">×</button>
                    <p>New here? A quick walkthrough reads your chart <em>with</em> you —
                      cited to BPHS at every step.</p>
                    <button type="button" className="rg-nudge-go" onClick={openGuide}>
                      Start the walkthrough →
                    </button>
                  </div>
                )}
              </div>
            </div>
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
                <button type="button" className={style === 'wheel' ? 'on' : ''}
                        onClick={() => setStyle('wheel')}>Sky wheel</button>
              </div>
              <div className="vargas">
                {VARGA_LABELS.map(([k, label]) => (
                  <button type="button" key={k} title={`${label} — ${VARGA_SIG[k]}`}
                          className={varga === k ? 'on' : ''}
                          onClick={() => setVarga(k)}>{k}</button>
                ))}
              </div>
              <div className="varga-name">
                <strong>{VARGA_LABELS.find(([k]) => k === varga)[1]}</strong>
                <span className="varga-sig"> — read for {VARGA_SIG[varga]}</span>
                <span className="varga-tier" title={VARGA_SIG_NOTE}>traditional</span>
              </div>
            </div>
            <div className="chart-figure">
              <Chart
                grahas={chart.grahas}
                lagnaRasi={chart.lagna_rasi}
                lagnaVargaSign={chart.lagna_vargas[varga]}
                vargaKey={varga}
                namer={namer}
                nakNames={NAK_NAMES}
                landmarks={chart.landmarks}
                lagnaLongitude={chart.lagna_longitude}
                gandanta={chart.gandanta}
                active={marked}
                onHover={setHovered}
                onPin={pinGraha}
                highlightSign={rowSign}
                drishti={chart.analysis && !chart.analysis.error ? chart.analysis.drishti : null}
                dashaLords={dashaLords}
                runningDasha={runningDasha}
                combust={combust}
              />
              {style === 'south' && varga === 'D1' && <RulerLegend />}
              {style === 'north' && (
                <p className="frame-note">
                  The North Indian frame is a <em>bhāva</em> diagram — it discards sign
                  geometry by design. For degree behaviour, use the South Indian frame.
                </p>
              )}
              {style === 'wheel' && (
                <p className="frame-note">
                  The sky as it stood around the native: the lagna rises on the
                  eastern horizon (left), each rāśi casts its 30°, and every graha
                  sits at its exact degree. A real-sky view, so it plots the D1
                  ecliptic — the horizon is exact, but no meridian is drawn (the
                  true MC is not 90° from the lagna along the ecliptic).
                </p>
              )}
            </div>
            {varga === 'D9' && chart.navamsa && !chart.navamsa.error && (
              <>
                {!nvNudgeSeen && !guideOpen && (
                  <div className="rg-nudge nv-nudge" role="note">
                    <button type="button" className="rg-nudge-x" onClick={dismissNvNudge}
                            aria-label="Dismiss">×</button>
                    <p>The navāṁśa reads differently — vargottama, the 64th navāṁśa
                      and the bhāva-sūchaka tally, on a <em>modern</em> tier kept
                      apart from BPHS. The guide has a step that walks it on your
                      chart.</p>
                    <button type="button" className="rg-nudge-go" onClick={openGuideAtNavamsa}>
                      Show me the navāṁśa step →
                    </button>
                  </div>
                )}
                <NavamsaPanel data={chart.navamsa} namer={namer} />
              </>
            )}
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
            <section className="table-panel" id="rg-signals">
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

          {chart.motion && !chart.motion.error && (
            <MotionPanel data={chart.motion} namer={namer} />
          )}

          <section className="table-panel" id="rg-dasha">
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
            <p className="rc-note varga-caption">
              Hover a column heading for what each division is read for. {VARGA_SIG_NOTE}
            </p>
            <div className="scroll">
              <table className="varga-table">
                <thead>
                  <tr>
                    <th>Graha</th>
                    {VARGA_LABELS.map(([k, label]) => (
                      <th key={k} title={`${label} — read for ${VARGA_SIG[k]} (traditional)`}>{k}</th>
                    ))}
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

      {/* The adjacent "K.N. Rao (modern)" bucket (§3b) — not nakṣatra-based, so
          its own reference block rather than a card. Collapsed by default. */}
      <section className="table-panel rasi-section">
        <h3>Modern method notes — K.N. Rao</h3>
        <p className="rc-note rasi-intro">
          Not nakṣatra-based and <strong>not BPHS</strong> — one modern author's
          method pointers (how he assesses the Gajakesari yoga; notes on his
          <em> Astrology Lessons</em>), kept in their own bucket, attributed and
          never presented as a verdict on any chart.
        </p>
        <button type="button" className="rc-toggle"
                aria-expanded={raoOpen}
                onClick={() => setRaoOpen((o) => !o)}>
          {raoOpen ? 'Hide' : 'Show'} the K.N. Rao (modern) pointers
        </button>
        {raoOpen && !raoData && <p className="hint">loading…</p>}
        {raoOpen && raoData?.error && (
          <p className="hint">Could not load — the backend may be waking.</p>
        )}
        {raoOpen && raoData && !raoData.error && <ModernNotes data={raoData} />}
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
