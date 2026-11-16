import { useState, useEffect, useRef, useMemo, lazy, Suspense } from 'react'
import { SouthIndianChart, NorthIndianChart } from './RasiChart.jsx'
import SkyWheelChart from './SkyWheel.jsx'
import NavamsaPanel from './NavamsaPanel.jsx'
import MotionPanel from './MotionPanel.jsx'
import ShadbalaPanel from './ShadbalaPanel.jsx'
import BhavaPanel from './BhavaPanel.jsx'
import YogaPanel from './YogaPanel.jsx'
import ClassicalPanel from './ClassicalPanel.jsx'
import PanchangHeatmap from './PanchangHeatmap.jsx'
import MatrixPanel from './MatrixPanel.jsx'
import PlanetMatrix from './PlanetMatrix.jsx'
import ExplainPanel from './ExplainPanel.jsx'
import ReadingGuide, { NAVAMSA_STEP } from './ReadingGuide.jsx'
import DashaTree from './DashaTree.jsx'
import VarshaphalPanel from './VarshaphalPanel.jsx'
import CharaDashaTimeline from './CharaDashaTimeline.jsx'
import Appearance from './Appearance.jsx'
import Logo from './Logo.jsx'
import { makeNamer } from './naming.js'
import { validTheme, DEFAULT_THEME, OLD_DEFAULT_THEME, OLD_DEFAULT_THEME_2 } from './themes.js'
import Profiles from './Profiles.jsx'
import Account from './Account.jsx'
import References from './References.jsx'
import Support from './Support.jsx'
import ComparePage from './ComparePage.jsx'
import ShareCard from './ShareCard.jsx'
import Report from './Report.jsx'
import Conclusions from './Conclusions.jsx'
import { SHARE_ID_RE, openShare } from './share.js'
import { REFS_KEY, refsOn, applyRefs, scrubProse } from './refs.js'
import Privacy from './Privacy.jsx'
import Methodology from './Methodology.jsx'
import ValidationPage from './ValidationPage.jsx'
import { LangContext, useLang } from './LangContext.jsx'
import { t as tFn } from './i18n.js'
import { profileIdFor, removeProfile as removeFromAccount } from './account.js'
import SignalStack from './SignalStack.jsx'
import RasiCard from './RasiCard.jsx'
import NakshatraCard from './NakshatraCard.jsx'
import ModernNotes from './ModernNotes.jsx'
import ChartDeck, { HighlightsCard } from './ChartDeck.jsx'
import FindingsPanel from './Findings.jsx'
import LifeAreas from './LifeAreas.jsx'
import DashaReading from './DashaReading.jsx'
import { LandingHero, RunningCard, ChartSummary, WhoCard, HouseExplorer, useStory, FullCta, ModeSwitch, useSlow } from './SimpleView.jsx'
import NorthDeckChart from './NorthDeckChart.jsx'
import SouthDeckChart from './SouthDeckChart.jsx'
import { listProfiles, saveProfile, deleteProfile, replaceAll } from './profiles.js'
import { API } from './config.js'
import './App.css'

// Pūjā & Havan is its own section with its own bundle — nothing of it loads with a chart.
const PoojaApp = lazy(() => import('./pooja/PoojaApp.jsx'))
const ChartWalkthrough = lazy(() => import('./ChartWalkthrough.jsx'))

const VARGA_LABELS = [
  ['D1', 'Raashi'], ['D2', 'Horā'], ['D3', 'Drekkāṇa'], ['D4', 'Chaturthāṁśa'],
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
  D9: 'spouse, marriage & dharma, and a graha’s inner strength',
  D10: 'career, karma & status',
  D12: 'parents & lineage',
  D16: 'vehicles, comforts & pleasures',
  D20: 'spiritual practice & worship',
  D24: 'education & learning',
  D27: 'overall strengths & weaknesses',
  D30: 'misfortunes, ariṣṭa & character',
  D40: 'auspicious & inauspicious effects (matrilineal)',
  D45: 'conduct & all indications (patrilineal)',
  D60: 'all matters & past-life karma (the finest, heavily weighted)',
}
const VARGA_SIG_NOTE = 'BPHS ch.6 gives the sixteen divisions’ calculation and '
  + 'names. The life-area each is read for is classical / traditional usage, not '
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
  const { t } = useLang()
  const [q, setQ] = useState(place?.name || '')
  const [hits, setHits] = useState([])
  const [busy, setBusy] = useState(false)
  const timer = useRef(null)
  const slow = useSlow(busy)

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
      <label htmlFor="place">{t('form.place.label')}</label>
      <input
        id="place" type="text" value={q} autoComplete="off"
        placeholder={t('form.place')}
        onChange={(e) => setQ(e.target.value)}
      />
      {busy && <div className="hint">{slow ? t('form.waking', 'Waking the server. The first search can take up to a minute…') : t('form.searching')}</div>}
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
        </Swatch> 0°→30° of the rāśi. Caps are the sandhi</span>
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

const VIEWS_KEY = 'profileViews'
const readViews = () => { try { return JSON.parse(localStorage.getItem(VIEWS_KEY) || '{}') } catch { return {} } }
const bumpViews = (id) => { try { const v = readViews(); v[id] = (v[id] || 0) + 1; localStorage.setItem(VIEWS_KEY, JSON.stringify(v)) } catch { /* private mode */ } }

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
  // A share link: /c/<id>#<key>. Fetch the blob, decrypt it with the key from
  // the fragment, load the form and cast — then offer to keep the chart.
  useEffect(() => {
    const m = SHARE_ID_RE.exec(location.pathname)
    const key = location.hash.slice(1)
    if (!m || !key) return
    let dead = false
    openShare(m[1], key)
      .then((p) => {
        if (dead) return
        setSharedIn(true)
        if (p.kind === 'snapshot') openSnapshot(p)
        else useProfile(p)
      })
      .catch((e) => { if (!dead) setError(`${t('share.openErr', 'This shared chart could not be opened:')} ${e.message || e}`) })
    return () => { dead = true }
  }, [])  // eslint-disable-line react-hooks/exhaustive-deps

  const [name, setName] = useState('')
  const [date, setDate] = useState('')
  const [time, setTime] = useState('')
  const [place, setPlace] = useState(null)
  const [chart, setChart] = useState(null)
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [varga, setVarga] = useState('D1')
  const [style, setStyle] = useState('north')
  const [section, setSection] = useState('projection')
  // Simple (the default: the chart, three placements, what is running now) or the
  // full analysis. The choice is remembered in this browser.
  const [mode, setModeState] = useState(() => {
    try { return localStorage.getItem('viewMode') === 'full' ? 'full' : 'simple' } catch { return 'simple' }
  })
  const setMode = (m) => { setModeState(m); try { localStorage.setItem('viewMode', m) } catch { /* private mode */ } }
  const simple = mode === 'simple'
  // The rāśi / nakṣatra reference, opened from the landing page or the simple view.
  const [refOpen, setRefOpen] = useState(false)
  // In the simple view the birth form folds away once a chart is showing.
  const [formOpen, setFormOpen] = useState(false)
  // The house the reader picked in the simple view (on the chart, or in the list under it).
  const [houseSel, setHouseSel] = useState(1)
  const pickHouse = (h) => {
    setHouseSel(h)
    setTimeout(() => document.querySelector('.sv-houses')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 40)
  }
  const [explainQuery, setExplainQuery] = useState(null)
  const [health, setHealth] = useState(null)
  // Transit (gochara) overlay: fetched lazily from /api/gochara only while the
  // overlay is on, so nobody pays the round-trip who hasn't asked. '' = now.
  const [transitOn, setTransitOn] = useState(true)
  const [transitDate, setTransitDate] = useState('')
  const [transit, setTransit] = useState(null)
  const [transitBusy, setTransitBusy] = useState(false)
  const [transitErr, setTransitErr] = useState('')
  const [profiles, setProfiles] = useState(() => listProfiles())
  const [activeProfile, setActiveProfile] = useState(null)
  const [shareOpen, setShareOpen] = useState(false)
  const [reportOpen, setReportOpen] = useState(false)   // the full report page (read, print, save as PDF)
  const [sharedIn, setSharedIn] = useState(false)   // this chart arrived by a share link
  // …and it arrived WITHOUT its birth details: the finished chart is all there
  // is. Nothing that is computed from a date, a time or a place can be shown,
  // because this browser was never given them.
  const [snap, setSnap] = useState(false)
  // The most-viewed saved chart is the one that comes up by default. Views
  // are counted per profile id in this browser; ties go to the newer chart.
  const restored = useRef(false)
  useEffect(() => {
    if (restored.current || route !== '/' || !profiles.length) return
    restored.current = true
    const views = readViews()
    const best = [...profiles].sort((a, b) => (views[b.id] || 0) - (views[a.id] || 0))[0]
    if (best) useProfile(best)
  }, [profiles])  // eslint-disable-line react-hooks/exhaustive-deps
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
  // "Watch it explained" — the chart walked through on its own animated chart.
  const [watchOpen, setWatchOpen] = useState(false)
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
  const openGuide = () => { setMode('full'); setGuideStep(0); setGuideOpen(true); dismissNudge() }
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
  // Section a scroll target lives in, so the guide can open its tab before scrolling.
  const SECTION_OF = { '#rg-signals': 'overview', '#rg-dasha': 'dasha' }
  const guideActions = {
    setStyle, setVarga, selectGraha, highlightSign: setRowSign,
    scrollTo: (sel) => {
      const sec = SECTION_OF[sel]
      if (sec) setSection(sec)
      setTimeout(() => document.querySelector(sel)?.scrollIntoView({ behavior: 'smooth', block: 'center' }), sec ? 80 : 0)
    },
  }

  // Appearance, remembered across visits. validTheme guards a stale saved key
  // (e.g. the retired "parchment") from leaving the page themeless.
  const [theme, setTheme] = useState(() => {
    const stored = localStorage.getItem('theme')
    // One-time move to the new default. The theme has always been written back
    // on load, so a browser holding the OLD default may simply never have been
    // asked. Move it once; any pick made after this (Midnight included) stays.
    // (v3: the default moved again, Tulasi → Clean. A Midnight picked after the
    // v2 move was a real choice and is kept.)
    if (!localStorage.getItem('themeDefault_v3')) {
      const askedBefore = localStorage.getItem('themeDefault_v2')
      localStorage.setItem('themeDefault_v3', '1')
      localStorage.setItem('themeDefault_v2', '1')
      if ((stored === OLD_DEFAULT_THEME && !askedBefore) || stored === OLD_DEFAULT_THEME_2) return DEFAULT_THEME
    }
    return validTheme(stored ?? DEFAULT_THEME)
  })
  const [nameStyle, setNameStyle] = useState(() => {
    const stored = localStorage.getItem('nameStyle')
    // One-time migration: Devanāgarī is the natural default name style for the
    // Hindi UI, but visitors who chose Hindi BEFORE it shipped are stuck on the
    // legacy Latin 'common' default — the language→style auto-switch only fires
    // on an explicit toggle, not on load. Move those users to Devanāgarī once;
    // any later explicit pick persists (the flag stops this from re-running).
    if (!localStorage.getItem('nameStyleHiMigrated_v1')) {
      localStorage.setItem('nameStyleHiMigrated_v1', '1')
      if (localStorage.getItem('lang') === 'hi' && (!stored || stored === 'common')) {
        return 'devanagari'
      }
    }
    return stored || 'common'
  })
  // UI language — persisted, and set on <html lang> for accessibility. Currently
  // drives the methodology page; the rest of the UI follows in later passes.
  const [lang, setLang] = useState(() => {
    const s = localStorage.getItem('lang')
    return s === 'hi' || s === 'en' ? s : 'en'
  })
  useEffect(() => {
    document.documentElement.dataset.theme = theme
    localStorage.setItem('theme', theme)
  }, [theme])
  useEffect(() => { localStorage.setItem('nameStyle', nameStyle) }, [nameStyle])
  useEffect(() => {
    localStorage.setItem('lang', lang)
    document.documentElement.lang = lang
  }, [lang])
  const namer = makeNamer(nameStyle)

  // Switching the UI language also moves the NAME style to that language's
  // natural default — Hindi → Devanāgarī, English → the Latin "common" spelling —
  // while staying switchable: the dropdown can still pick any style, and a manual
  // pick holds until the next language switch. Fires only on a real user toggle
  // (not on mount), so a persisted manual choice survives a reload.
  const changeLang = (next) => {
    setLang(next)
    setNameStyle((cur) => (next === 'hi' ? 'devanagari'
                          : next === 'en' && cur === 'devanagari' ? 'common'
                          : cur))
  }
  // Bound translator + shared context value for the UI chrome (Phase-1 i18n).
  // References off (the default): the UI's own sentences lose the book as
  // their subject too, through the same rules the API applies (refs.js).
  const [refs, setRefs] = useState(refsOn)
  useEffect(() => { setRefs(refsOn()) }, [route])
  useEffect(() => { applyRefs(refs) }, [refs])
  const langValue = useMemo(() => ({
    lang,
    t: refs ? (k, f) => tFn(lang, k, f) : (k, f) => scrubProse(tFn(lang, k, f)),
  }), [lang, refs])
  const { t } = langValue
  const watchButton = (
    <button type="button" className="rg-open" onClick={() => setWatchOpen(true)}>{t('wt.open', '▶ Explain my chart')}</button>
  )

  // Re-cast when the language changes so the generated readings switch too
  // (the birth params are unchanged; only `lang` on the request differs).
  // Every chart is stamped with the language it was asked for (`_lang`). A chart that
  // arrives in the other language is cast again: the reader changed the language while
  // the first cast was still on its way, and no chart was on the page to re-cast then.
  const langSeen = useRef({ lang, refs })
  const castLang = chart && !chart.error ? chart._lang : null
  useEffect(() => {
    const changed = langSeen.current.lang !== lang || langSeen.current.refs !== refs
    langSeen.current = { lang, refs }
    if (!changed && (!castLang || castLang === lang)) return
    if (!chart || chart.error || !place || !date || !time) return
    let cancelled = false
    ;(async () => {
      try {
        const r = await fetch(`${API}/api/chart`, {
          method: 'POST', headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, date, time, lang,
            latitude: place.latitude, longitude: place.longitude, timezone: place.timezone }),
        })
        const j = await r.json()
        if (!cancelled && r.ok) setChart({ ...j, _lang: lang })
      } catch { /* keep the current chart on a failed re-cast */ }
    })()
    return () => { cancelled = true }
  }, [lang, refs, castLang])  // eslint-disable-line react-hooks/exhaustive-deps

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
    setSnap(false)
    setError(''); setBusy(true); setChart(null)
    try {
      const r = await fetch(`${API}/api/chart`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name, date, time, lang,
          latitude: place?.latitude, longitude: place?.longitude,
          timezone: place?.timezone,
        }),
      })
      const j = await r.json()
      if (!r.ok) throw new Error(j.error || `HTTP ${r.status}`)
      setChart({ ...j, _lang: lang })
      setFormOpen(false)
      // Only remember births that actually produced a chart — saving on submit
      // would fill the list with typos and out-of-range dates.
      const saved = saveProfile({ name, date, time, place })
      setProfiles(saved)
      setActiveProfile(saved[0]?.id ?? null)
      if (saved[0]?.id) bumpViews(saved[0].id)
    } catch (err) {
      setError(err.message)
    } finally {
      setBusy(false)
    }
  }

  /** Load a saved chart back into the form and cast it straight away. */
  function openSnapshot(p) {
    setName(p.name || ''); setDate(''); setTime(''); setPlace(null); setActiveProfile(null)
    setError(''); setTransitOn(false); setTransit(null)
    setSection('overview')
    setStyle((st) => (st === 'panchang' ? 'north' : st))
    setSnap(true)
    setChart({ ...p.chart, name: p.name || '' })
  }

  async function useProfile(p) {
    setSnap(false)
    if (p.id) bumpViews(p.id)
    setName(p.name || ''); setDate(p.date); setTime(p.time); setPlace(p.place)
    setActiveProfile(p.id)
    setError(''); setBusy(true); setChart(null)
    try {
      const r = await fetch(`${API}/api/chart`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: p.name, date: p.date, time: p.time, lang,
          latitude: p.place.latitude, longitude: p.place.longitude,
          timezone: p.place.timezone,
        }),
      })
      const j = await r.json()
      if (!r.ok) throw new Error(j.error || `HTTP ${r.status}`)
      setChart({ ...j, _lang: lang })
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

  // Fetch the transit geometry whenever the overlay is on and the birth data or
  // chosen moment changes. Cancels in-flight fetches so a fast date change can't
  // land its stale result after a newer one.
  useEffect(() => {
    if (!transitOn || !chart || !place) return
    let cancelled = false
    setTransitBusy(true); setTransitErr('')
    fetch(`${API}/api/gochara`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        date, time,
        latitude: place.latitude, longitude: place.longitude, timezone: place.timezone,
        ...(transitDate ? { transit_date: transitDate } : {}),
      }),
    })
      .then((r) => r.json().then((j) => { if (!r.ok) throw new Error(j.error || `HTTP ${r.status}`); return j }))
      .then((j) => { if (!cancelled) setTransit(j) })
      .catch((e) => { if (!cancelled) { setTransitErr(e.message); setTransit(null) } })
      .finally(() => { if (!cancelled) setTransitBusy(false) })
    return () => { cancelled = true }
  }, [transitOn, transitDate, chart, date, time, place])

  const ready = date && time && place
  const slowCast = useSlow(busy)
  // The landing page: nothing cast, nothing loading.
  const landing = !chart && !busy
  const formHidden = simple && !formOpen && !error && (chart || busy)
  // In the simple view no analysis section is open.
  const sec = simple ? null : section
  const simpleStyle = style === 'south' ? 'south' : 'north'
  const story = useStory(simple ? chart : null, namer)
  const Chart = style === 'south' ? SouthIndianChart
    : style === 'north' ? NorthIndianChart
    : SkyWheelChart

  // The grahas ruling the running mahā and antar daśā — for the wheel's daśā
  // overlay. Time isn't spatial, but WHERE the ruling graha sits is.
  const dashaLords = (() => {
    const dv = chart && chart.dasha && chart.dasha.variants
    const dk = chart && chart.dasha ? String(chart.dasha.default_year_days).replace('.0', '') : null
    const tree = dv ? (dv[dk] || dv['360'] || Object.values(dv)[0]) : null
    const maha = tree && tree.mahadashas && tree.mahadashas.find((m) => m.is_current)
    const antar = maha && maha.sub && maha.sub.find((a) => a.is_current)
    return { maha: maha && maha.lord, antar: antar && antar.lord }
  })()
  // The running daśā chain (mahā → antar → pratyantar) with the time remaining
  // in each level, for the wheel's daśā readout. is_current is marked as-of now
  // on the backend, and each node's `end` is the boundary we count down to.
  const runningDasha = (() => {
    const dv = chart && chart.dasha && chart.dasha.variants
    const dk = chart && chart.dasha ? String(chart.dasha.default_year_days).replace('.0', '') : null
    const tree = dv ? (dv[dk] || dv['360'] || Object.values(dv)[0]) : null
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
    // The period that follows `node` among its siblings; at the end of a parent's
    // run, the first period of the parent's own successor.
    const after = (list, node, parentNext) => {
      const i = list ? list.indexOf(node) : -1
      if (i >= 0 && list[i + 1]) return list[i + 1]
      return (parentNext && parentNext.sub && parentNext.sub[0]) || null
    }
    const mahaNext = after(tree.mahadashas, maha, null)
    const antarNext = antar ? after(maha.sub, antar, mahaNext) : null
    const pratyNext = praty ? after(antar.sub, praty, antarNext) : null
    const level = (node, code, nxt) => (node && node.end
      ? { code, lord: node.lord, ends: fmtEnd(node.end), remaining: remain(node.end),
          next: nxt && nxt.end ? { lord: nxt.lord, ends: fmtEnd(nxt.end) } : null } : null)
    const levels = [level(maha, 'MD', mahaNext), level(antar, 'AD', antarNext), level(praty, 'PD', pratyNext)].filter(Boolean)
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

  if (route === '/pooja' || route.startsWith('/pooja/') || route.startsWith('/pooja?')) {
    return <Suspense fallback={<div className="page"><p className="sub">…</p></div>}><PoojaApp route={route} go={go} lang={lang} setLang={changeLang} /></Suspense>
  }
  if (route === '/privacy') return <Privacy onBack={() => go('/')} />
  if (route === '/references') return <References lang={lang} onBack={() => go('/')} />
  if (route === '/support') return <Support lang={lang} onBack={() => go('/')} />
  if (route === '/compare') return <ComparePage lang={lang} onBack={() => go('/')} />
  if (route === '/methodology') return <Methodology lang={lang} setLang={changeLang} onBack={() => go('/')} />
  if (route === '/validation') return <ValidationPage lang={lang} setLang={changeLang} onBack={() => go('/')} />

  return (
    <LangContext.Provider value={langValue}>
    <div className="page">
      {/* One bar: the name on the left, the two sections of the site beside it,
          language and settings on the right. */}
      <div className="topbar">
        <h1 className="visually-hidden">Devashaa — Jyotiṣa birth charts</h1>
        <a className="topbar-logo" href="/" onClick={(e) => { e.preventDefault(); go('/') }}><Logo /></a>
        <nav className="site-tabs" aria-label={t('site.sections', 'Sections of the site')}>
          <a className="on" href="/" aria-current="page">{t('site.jyotisha', 'Jyotiṣa charts')}</a>
          <a href="/pooja" onClick={(e) => { e.preventDefault(); go('/pooja') }}>{t('site.pooja', 'Pūjā & Havan')}</a>
        </nav>
        <Appearance
          theme={theme} setTheme={setTheme}
          nameStyle={nameStyle} setNameStyle={setNameStyle}
          lang={lang} setLang={changeLang}
          refs={refs}
          setRefs={(on) => { try { localStorage.setItem(REFS_KEY, on ? '1' : '0') } catch { /* private mode */ } setRefs(on) }}
        />
        {/* Opens the account panel under the bar (sign in, create an account, sync). */}
        <button type="button" className="topbar-signin" aria-expanded={savedOpen}
                onClick={() => {
                  setSavedOpen(true)
                  setTimeout(() => document.querySelector('.saved')?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 60)
                }}>
          {acct ? acct.userid : t('topbar.signin', 'Sign in')}
        </button>
      </div>
      <nav className="trust trust--top" aria-label={t('trust.aria', 'What this site stands on')}>
        <a href="/validation" onClick={(e) => { e.preventDefault(); go('/validation') }}><i>✓</i>{t('trust.verified', 'Positions verified against JPL')}</a>
        <a href="/references" onClick={(e) => { e.preventDefault(); go('/references') }}><i>§</i>{t('trust.cited', 'Every reading cited to its text')}</a>
        <a href="/methodology" onClick={(e) => { e.preventDefault(); go('/methodology') }}><i>∅</i>{t('trust.nothingSold', 'No remedies · no fear · nothing sold')}</a>
        <a href={import.meta.env.VITE_SOURCE_URL || 'https://github.com/sansbug/devashaa'} target="_blank" rel="noreferrer"><i>{'</>'}</i>{t('trust.open', 'Open source')}</a>
        <a href="/compare" onClick={(e) => { e.preventDefault(); go('/compare') }}><i>≠</i>{t('trust.compare', 'Why charts differ between apps')}</a>
      </nav>
      {health && health.status !== 'ok' && (
        <header className="hdr-meta">
          <div className={`health ${health.status}`}>{`● ephemeris ${health.status}: charts refused`}</div>
        </header>
      )}

      <section className={`saved${landing ? ' saved--landing' : ''}`}>
        <div className="saved-bar">
          <button type="button" className="saved-toggle" aria-expanded={savedOpen}
                  onClick={() => setSavedOpen((o) => !o)}>
            <span className="saved-caret" aria-hidden="true">{savedOpen ? '−' : '+'}</span>
            {t('saved.title')}
            <span className="saved-hint">
              {acct
                ? `signed in as ${acct.userid}`
                : profiles.length
                  ? `${profiles.length} in this browser`
                  : t('saved.here')}
            </span>
          </button>
          <Profiles
            profiles={profiles}
            activeId={activeProfile}
            onPick={useProfile}
            onDelete={removeProfile}
          />
          {simple && chart && !error && (
            <button type="button" className="saved-toggle sv-new" aria-expanded={formOpen}
                    onClick={() => setFormOpen((o) => !o)}>
              <span className="saved-caret" aria-hidden="true">{formOpen ? '−' : '+'}</span>
              {t('sv.new', 'New chart')}
            </button>
          )}
        </div>
        {savedOpen && (
          <Account
            profiles={profiles}
            onAccount={setAcct}
            onMerged={(merged) => setProfiles(replaceAll(merged))}
          />
        )}
      </section>

      {landing && <LandingHero namer={namer} nakNames={NAK_NAMES} />}

      {formHidden && busy && <p className="hint sv-casting">{slowCast ? t('form.wakingCast', 'Waking the server. The first chart can take up to a minute…') : t('form.casting')}</p>}
      {!formHidden && (
      <form onSubmit={submit} className={`birth-form${landing ? ' birth-form--landing' : ''}`}>
        {landing && (
          <div className="sv-form-head">
            <b>{t('sv.form.title', 'Create your chart')}</b>
            <span>{t('sv.form.note', 'Your birth time and place are used to calculate the planetary positions.')}</span>
          </div>
        )}
        <div className="field field-name">
          <label htmlFor="name">{t('form.name')}</label>
          <input id="name" value={name} onChange={(e) => setName(e.target.value)}
                 placeholder={t('form.name.ph')} />
        </div>
        <div className="field">
          <label htmlFor="date">{t('form.date')}</label>
          <input id="date" type="date" value={date} required
                 onChange={(e) => setDate(e.target.value)} />
        </div>
        <div className="field">
          <label htmlFor="time">{t('form.time')}</label>
          <input id="time" type="time" value={time} required
                 onChange={(e) => setTime(e.target.value)} />
        </div>
        <PlaceField onPick={setPlace} place={place} />
        <button type="submit" className="go" disabled={!ready || busy}>
          {busy ? t('form.casting') : landing ? t('sv.form.go', 'Create my birth chart →') : t('form.cast')}
        </button>
        {busy && slowCast && <div className="hint sv-form-wait">{t('form.wakingCast', 'Waking the server. The first chart can take up to a minute…')}</div>}
      </form>
      )}

      {!chart && (
        <p className="sv-ref-link">
          <button type="button" className="sv-link" aria-expanded={refOpen} onClick={() => setRefOpen((o) => !o)}>
            {refOpen ? t('sv.ref.hide', 'Hide the reference') : t('sv.ref.show', 'Browse the 12 rāśis and 27 nakṣatras')}
          </button>
        </p>
      )}
      {error && <div className="error">{error}</div>}
      {sharedIn && chart && (
        <div className="shared-note" role="note">
          <span>↗ {t('share.shared', 'A chart shared with you')}{chart.name ? ` — ${chart.name}` : ''}.
            {snap && <> {t('share.shared.snap', 'It was shared without its birth details: the chart, its strengths, yogas and readings are here; the timelines (daśā, projection, yearly charts, transits) are computed from the date, time and place, which were not sent.')}</>}</span>
          {!snap && (
            <button type="button" className="profile-x sh-save" onClick={() => {
              const saved = saveProfile({ name, date, time, place }); setProfiles(saved); setActiveProfile(saved[0]?.id ?? null); setSharedIn(false)
            }}>{t('share.save', 'Save to my charts')}</button>
          )}
        </div>
      )}
      {reportOpen && chart && (
        <Report chart={chart} name={name} date={date} time={time} place={place} namer={namer} refs={refs} snap={snap}
                onClose={() => setReportOpen(false)} />
      )}
      {shareOpen && chart && place && (
        <ShareCard chart={chart} name={name} date={date} time={time} place={place} namer={namer} onClose={() => setShareOpen(false)}
                   onReport={() => { setShareOpen(false); setReportOpen(true) }} />
      )}

      {chart && (
        <main className="result">
          {guideOpen && (
            <ReadingGuide chart={chart} namer={namer} actions={guideActions}
                          initialStep={guideStep}
                          onClose={() => setGuideOpen(false)} />
          )}
          {watchOpen && (
            <Suspense fallback={null}>
              <ChartWalkthrough chart={chart} namer={namer} onClose={() => setWatchOpen(false)} />
            </Suspense>
          )}
          {!simple && (
          <section className="meta" id="rg-positions">
            <div className="meta-head">
              <h2>{chart.name || t('sv.chart', 'Your chart')}</h2>
              {snap && <div className="rg-open-wrap">{watchButton}<ModeSwitch mode={mode} setMode={setMode} /></div>}
              {!snap && (
              <div className="rg-open-wrap">
                {!simple && watchButton}
                <button type="button" className="rg-open sh-open" onClick={() => setShareOpen(true)}>
                  ↗ {t('share.open', 'Share')}
                </button>
                {!simple && (
                <button type="button" className="rg-open" onClick={openGuide}>
                  How to read this chart →
                </button>
                )}
                <ModeSwitch mode={mode} setMode={setMode} />
                {!simple && !nudgeSeen && !guideOpen && (
                  <div className="rg-nudge" role="note">
                    <button type="button" className="rg-nudge-x" onClick={dismissNudge}
                            aria-label="Dismiss">×</button>
                    <p>New here? A quick walkthrough reads your chart <em>with</em> you,
                      one step at a time.</p>
                    <button type="button" className="rg-nudge-go" onClick={openGuide}>
                      Start the walkthrough →
                    </button>
                  </div>
                )}
              </div>
              )}
            </div>
            {!simple && (
            <div className="dk-table-wrap meta-table-wrap">
              {snap ? (
              <table className="dk-table meta-table">
                <thead><tr><th>Lagn</th><th>{t('share.meta.birth', 'Date · time · place of birth')}</th><th>Ayanāṁśa</th></tr></thead>
                <tbody><tr>
                  <td className="mc-lagna">{namer.rasiFull(chart.lagna_rasi)} · {namer.nakshatra(chart.lagna_nakshatra)} p{chart.lagna_nakshatra.pada}</td>
                  <td>{t('share.meta.hidden', 'not shared by the sender')}</td>
                  <td>{chart.ayanamsa}</td>
                </tr></tbody>
              </table>
              ) : (
              <table className="dk-table meta-table">
                <thead><tr><th>Lagn</th><th>Local</th><th>Zone</th><th>UTC</th><th>JD</th><th>Ayanāṁśa</th></tr></thead>
                <tbody><tr>
                  <td className="mc-lagna">{namer.rasiFull(chart.lagna_rasi)} · {namer.nakshatra(chart.lagna_nakshatra)} p{chart.lagna_nakshatra.pada}</td>
                  <td className="dk-num">{chart.local_time}</td>
                  <td>{chart.timezone} ({chart.utc_offset_hours >= 0 ? '+' : ''}{chart.utc_offset_hours}h)</td>
                  <td className="dk-num">{chart.utc}</td>
                  <td className="dk-num">{chart.jd_ut.toFixed(4)}</td>
                  <td className="dk-num">{fmtAyan(chart.ayanamsa_value)}</td>
                </tr></tbody>
              </table>
              )}
            </div>
            )}
          </section>
          )}

          {simple && (
          <section className="chart-panel chart-panel--deck sv-panel">
            {/* One row: whose chart it is, the way in for a newcomer, then the chart
                style, sharing, and the simple / full switch. */}
            <div className="controls sv-bar">
              <div className="sv-explain-row">
                <button type="button" className="go" onClick={() => setWatchOpen(true)}>{t('wt.open', '▶ Explain my chart')}</button>
                <span>
                  <b>{t('sv.explain.title', 'New to this? Start here.')}</b>
                  <small>{t('sv.explain.body', 'Your chart, one topic at a time, in plain words.')}</small>
                </span>
              </div>
              <div className="styles">
                <button type="button" className={simpleStyle === 'north' ? 'on' : ''}
                        onClick={() => setStyle('north')}>{t('sv.north', 'North')}</button>
                <button type="button" className={simpleStyle === 'south' ? 'on' : ''}
                        onClick={() => setStyle('south')}>{t('sv.south', 'South')}</button>
              </div>
              {!snap && (
                <button type="button" className="rg-open sh-open" onClick={() => setShareOpen(true)}>
                  ↗ {t('share.open', 'Share')}
                </button>
              )}
              <button type="button" className="rg-open sh-open" onClick={() => setReportOpen(true)}>
                ⎙ {t('report.open', 'PDF')}
              </button>
              <ModeSwitch mode={mode} setMode={setMode} />
            </div>
            <div className="chart-figure">
              {simpleStyle === 'south' ? (
                <SouthDeckChart grahas={chart.grahas} lagnaRasi={chart.lagna_rasi}
                  lagnaVargaSign={chart.lagna_vargas.D1} vargaKey="D1" namer={namer}
                  landmarks={chart.landmarks} lagnaLongitude={chart.lagna_longitude}
                  gandanta={chart.gandanta} active={marked} onHover={setHovered}
                  highlightSign={(chart.lagna_rasi + houseSel - 1) % 12} title={chart.name} onHouse={pickHouse} />
              ) : (
                <NorthDeckChart grahas={chart.grahas} lagnaRasi={chart.lagna_rasi}
                  lagnaVargaSign={chart.lagna_vargas.D1} vargaKey="D1" namer={namer}
                  highlightSign={(chart.lagna_rasi + houseSel - 1) % 12} title={chart.name} onHouse={pickHouse} />
              )}
            </div>
            <div className="deck-side sv-side">
              <ChartSummary story={story} />
              <WhoCard chart={chart} namer={namer} refs={refs} />
              <HighlightsCard chart={chart} grahas={chart.grahas} namer={namer} />
              {!snap && <RunningCard running={runningDasha} namer={namer}
                                     onMore={() => { setMode('full'); setSection('dasha') }} />}
              {!snap && (
              <form className="ask-inline sv-ask" role="search"
                    onSubmit={(e) => {
                      e.preventDefault()
                      const v = e.target.elements.q.value.trim()
                      if (v) setExplainQuery({ q: v, nonce: Date.now() })
                    }}>
                <span className="ask-inline-ic" aria-hidden="true">✦</span>
                <input name="q" type="text"
                       placeholder={t('sv.ask.place', 'Ask a question: “my career”, “Jupiter”…')}
                       aria-label={t('explain.title', 'Ask your chart')} />
                <button type="submit">{t('explain.ask', 'Ask')}</button>
              </form>
              )}
            </div>
            <div className="deck-under sv-under">
              <HouseExplorer story={story} house={houseSel} setHouse={setHouseSel}
                             onFull={() => { setMode('full'); setSection('bhava'); window.scrollTo(0, 0) }} />
            </div>
          </section>
          )}
          {simple && <Conclusions chart={chart} namer={namer} date={snap ? null : date} time={snap ? null : time} place={snap ? null : place} />}
          {simple && !snap && explainQuery && (
            <ExplainPanel date={date} time={time} place={place} namer={namer} initialQuery={explainQuery} />
          )}
          {simple && !snap && <DashaReading chart={chart} namer={namer} refs={refs}
                                       goFull={() => { setMode('full'); setSection('dasha'); window.scrollTo(0, 0) }} />}
          {simple && <LifeAreas chart={chart} namer={namer} refs={refs} onHouse={setHouseSel}
                               goFull={() => { setMode('full'); if (!snap) setSection('dasha'); window.scrollTo(0, 0) }} />}
          {simple && (
            <FindingsPanel chart={chart} namer={namer} refs={refs} onHouse={setHouseSel}
              goFull={(to) => {
                setMode('full')
                if (to === 'navamsa') setVarga('D9')
                else if (['strength', 'dasha', 'classical', 'bhava'].includes(to) && !(snap && to === 'dasha')) setSection(to)
                window.scrollTo(0, 0)
              }} />
          )}
          {simple && <FullCta onFull={() => { setMode('full'); window.scrollTo(0, 0) }} />}

          {!simple && (<>
          <section className={`chart-panel${style === 'north' || style === 'south' ? ' chart-panel--deck' : ''}`}>
            <div className="controls">
              <div className="styles">
                <button type="button" className={style === 'south' ? 'on' : ''}
                        onClick={() => setStyle('south')}>South Indian</button>
                <button type="button" className={style === 'north' ? 'on' : ''}
                        onClick={() => setStyle('north')}>North Indian</button>
                <button type="button" className={style === 'wheel' ? 'on' : ''}
                        onClick={() => setStyle('wheel')}>Sky wheel</button>
                {!snap && (
                  <button type="button" className={style === 'panchang' ? 'on' : ''}
                          onClick={() => setStyle('panchang')}>{t('panchang.tab', 'Pañcāṅga')}</button>
                )}
              </div>
              {style !== 'panchang' && (
                <div className="vargas">
                  {VARGA_LABELS.map(([k, label]) => (
                    <button type="button" key={k} title={`${label} — ${VARGA_SIG[k]}`}
                            className={varga === k ? 'on' : ''}
                            onClick={() => setVarga(k)}>{k}</button>
                  ))}
                </div>
              )}
              {style !== 'panchang' && (
                <div className="varga-name">
                  <strong>{VARGA_LABELS.find(([k]) => k === varga)[1]}</strong>
                  <span className="varga-sig"> — read for {VARGA_SIG[varga]}</span>
                  <span className="varga-tier" title={VARGA_SIG_NOTE}>traditional</span>
                </div>
              )}
              {!snap && (
              <form className="ask-inline" role="search"
                    onSubmit={(e) => {
                      e.preventDefault()
                      const v = e.target.elements.q.value.trim()
                      if (v) { setExplainQuery({ q: v, nonce: Date.now() }); setSection('explain') }
                    }}>
                <span className="ask-inline-ic" aria-hidden="true">✦</span>
                <input name="q" type="text"
                       placeholder={t('explain.askPlace', 'Ask this chart: “Jupiter”, “Gajakesari yoga”, “my career”…')}
                       aria-label={t('explain.title', 'Ask your chart')} />
                <button type="submit">{t('explain.ask', 'Ask')}</button>
              </form>
              )}
            </div>
            <div className="chart-figure">
              {style === 'panchang' ? (
                <PanchangHeatmap date={date} time={time} place={place} />
              ) : (<>
              {style === 'south' ? (
                <SouthDeckChart
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
                  onPick={pinGraha}
                  highlightSign={rowSign}
                />
              ) : style === 'north' ? (
                <NorthDeckChart
                  grahas={chart.grahas}
                  lagnaRasi={chart.lagna_rasi}
                  lagnaVargaSign={chart.lagna_vargas[varga]}
                  vargaKey={varga}
                  namer={namer}
                  highlightSign={rowSign}
                  onPick={pinGraha}
                />
              ) : (
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
                analysis={chart.analysis && !chart.analysis.error ? chart.analysis : null}
                vargaSig={VARGA_SIG[varga]}
                noHover={style === 'south'}
                drishti={chart.analysis && !chart.analysis.error ? chart.analysis.drishti : null}
                dashaLords={dashaLords}
                runningDasha={runningDasha}
                combust={combust}
                transit={transit}
                transitOn={transitOn}
                setTransitOn={snap ? () => {} : setTransitOn}
                transitDate={transitDate}
                setTransitDate={setTransitDate}
                transitBusy={transitBusy}
                transitErr={transitErr}
              />
              )}
              {style === 'south' && varga === 'D1' && <RulerLegend />}
              {style === 'wheel' && (
                <p className="frame-note">
                  The sky as it stood around the native: the lagna rises on the
                  eastern horizon (left), each rāśi casts its 30°, and every graha
                  sits at its exact degree. A real-sky view, so it plots the D1
                  ecliptic — the horizon is exact, but no meridian is drawn (the
                  true MC is not 90° from the lagna along the ecliptic).
                </p>
              )}
              </>)}
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
            {style !== 'panchang' && (
              <ChartDeck
                chart={chart}
                drishti={chart.analysis && !chart.analysis.error ? chart.analysis.drishti : null}
                grahas={chart.grahas}
                namer={namer}
                varga={varga}
                subject={subject}
                onPickSubject={pinGraha}
                onHoverSign={setRowSign}
                analysis={chart.analysis && !chart.analysis.error ? chart.analysis : null}
                vargaSig={VARGA_SIG[varga]}
              />
            )}
          </section>

          <nav className="sec-nav" role="tablist">
            {[['projection', t('sec.projection', 'Projection')],
              ['explain', t('sec.explain', 'Ask')],
              ['overview', t('sec.overview', 'Overview')],
              ['strength', t('sec.strength', 'Strength')],
              ['bhava', t('sec.bhava', 'Bhāvas & Yogas')],
              ['dasha', t('sec.dasha', 'Daśā')],
              ['varsha', t('sec.varsha', 'Varṣaphala')],
              ['classical', t('sec.classical', 'Classical')],
              ['reference', t('sec.reference', 'Reference')]]
              // a chart shared without its birth details has no timelines to show
              .filter(([id]) => !snap || !['projection', 'explain', 'dasha', 'varsha'].includes(id))
              .map(([id, label]) => (
              <button type="button" key={id} role="tab" aria-selected={section === id}
                      className={'sec-pill' + (section === id ? ' on' : '')}
                      onClick={() => setSection(id)}>{label}</button>
            ))}
          </nav>
          </>)}

          {sec === 'overview' && chart.analysis && !chart.analysis.error && (
            <PlanetMatrix data={chart.analysis.planet_matrix} namer={namer} grahas={chart.grahas} />
          )}

          {sec === 'overview' && chart.analysis && !chart.analysis.error && (
            <section className="table-panel" id="rg-signals">
              <h3>{t('ref.grahaSignals.title')}</h3>
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

          {sec === 'strength' && chart.shadbala && !chart.shadbala.error && chart.shadbala.grahas && (
            <ShadbalaPanel data={chart.shadbala} namer={namer} />
          )}

          {sec === 'strength' && chart.motion && !chart.motion.error && (
            <MotionPanel data={chart.motion} namer={namer} />
          )}

          {sec === 'bhava' && chart.analysis && chart.analysis.bhava_phala && !chart.analysis.bhava_phala.error && (
            <BhavaPanel data={chart.analysis.bhava_phala} namer={namer} />
          )}

          {sec === 'bhava' && chart.analysis && chart.analysis.yogas && !chart.analysis.yogas.error && (
            <YogaPanel data={chart.analysis.yogas} namer={namer} />
          )}

          {sec === 'classical' && chart.analysis && chart.analysis.classical && (
            <ClassicalPanel data={chart.analysis.classical} namer={namer} />
          )}

          {!snap && sec === 'projection' && <MatrixPanel date={date} time={time} place={place} namer={namer} />}

          {!snap && sec === 'explain' && <ExplainPanel date={date} time={time} place={place} namer={namer} initialQuery={explainQuery} />}

          {!snap && sec === 'varsha' && (
            <VarshaphalPanel date={date} time={time} place={place} namer={namer} chartStyle={style} />
          )}

          {!snap && sec === 'dasha' && (
          <section className="table-panel" id="rg-dasha">
            <h3>{t('dasha.title')}</h3>
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
                  {t('dasha.chara.title')} <span className="chara-tag">{t('dasha.chara.tag')}</span>
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
          )}

          {sec === 'overview' && (
          <section className="table-panel">
            <h3>{t('ref.grahaTable.title')}</h3>
            <div className="scroll">
              <table>
                <thead>
                  <tr>
                    <th>{t('grahaTable.graha')}</th><th>{t('grahaTable.rasi')}</th><th>{t('grahaTable.degree')}</th><th>{t('grahaTable.bhava')}</th>
                    <th>{t('grahaTable.nakshatra')}</th><th>{t('grahaTable.pada')}</th><th>{t('grahaTable.deity')}</th><th>{t('grahaTable.rasiLord')}</th><th>{t('grahaTable.speed')}</th>
                  </tr>
                </thead>
                <tbody>
                  {chart.grahas.map((g) => (
                    <tr key={g.key}>
                      <td className="graha-name">
                        {namer.graha(g)}
                        {/* English gloss: an aid for the Latin transliteration
                            styles. Redundant once names ARE English — or already
                            Indic (Devanāgarī). */}
                        {nameStyle !== 'english' && nameStyle !== 'devanagari' &&
                          <span className="en"> {g.name_en}</span>}
                      </td>
                      <td>
                        {namer.grahaRasi(g)}
                        {nameStyle !== 'english' && nameStyle !== 'devanagari' &&
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
          )}

          {sec === 'reference' && (
          <section className="table-panel">
            <h3>{t('ref.varga.title')}</h3>
            <p className="rc-note varga-caption">
              {t('ref.varga.caption')} {VARGA_SIG_NOTE}
            </p>
            <div className="scroll">
              <table className="varga-table">
                <thead>
                  <tr>
                    <th>Graha</th>
                    {VARGA_LABELS.map(([k, label]) => (
                      <th key={k} title={`${label}: read for ${VARGA_SIG[k]} (traditional)`}>{k}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <tr className="lagna-row">
                    <td className="graha-name">Lagn</td>
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
          )}
        </main>
      )}

      {/* Rāśi / nakṣatra / Rao reference — shown standalone on the landing page (no
          chart) and inside the Reference tab once a chart is cast. */}
      {(refOpen || sec === 'reference') && (<>
      <section className="table-panel rasi-section">
        <h3>{t('ref.rasi.title')}</h3>
        <p className="rc-note rasi-intro">{t('ref.rasi.intro')}</p>
        <div className="rasi-picker">
          {Array.from({ length: 12 }, (_, i) => (
            <button type="button" key={i}
                    className={openRasi === i ? 'on' : ''}
                    onClick={() => setOpenRasi(openRasi === i ? null : i)}>
              {namer.rasiFull(i)}
            </button>
          ))}
        </div>
        {openRasi !== null && !rasis && <p className="hint">{t('ref.loading')}</p>}
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
        <h3>{t('ref.nak.title')}</h3>
        <p className="rc-note rasi-intro">{t('ref.nak.intro')}</p>
        <div className="rasi-picker">
          {NAK_NAMES.map((nm, i) => (
            <button type="button" key={i}
                    className={openNak === i ? 'on' : ''}
                    onClick={() => setOpenNak(openNak === i ? null : i)}>
              {namer.nakshatra(nm)}
            </button>
          ))}
        </div>
        {openNak !== null && !nakAttrs && <p className="hint">{t('ref.loading')}</p>}
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
        <h3>{t('ref.rao.title')}</h3>
        <p className="rc-note rasi-intro">{t('ref.rao.intro')}</p>
        <button type="button" className="rc-toggle"
                aria-expanded={raoOpen}
                onClick={() => setRaoOpen((o) => !o)}>
          {raoOpen ? t('ref.rao.hideFull') : t('ref.rao.showFull')}
        </button>
        {raoOpen && !raoData && <p className="hint">{t('ref.loading')}</p>}
        {raoOpen && raoData?.error && (
          <p className="hint">{t('ref.rao.loadError')}</p>
        )}
        {raoOpen && raoData && !raoData.error && <ModernNotes data={raoData} />}
      </section>
      </>)}

      <footer>
        <p>
          {t('footer.ephem')}{' '}
          <a href={import.meta.env.VITE_SOURCE_URL || '#'} rel="noreferrer">
            {t('footer.source')}
          </a>.
        </p>
        <p>
          <a href="/methodology"
             onClick={(e) => { e.preventDefault(); go('/methodology') }}>
            {lang === 'hi' ? 'देवाशा किस तरह अलग है' : 'How Devashaa is different'}
          </a>
          {'  ·  '}
          <a href="/validation"
             onClick={(e) => { e.preventDefault(); go('/validation') }}>
            {lang === 'hi' ? 'हम गणित की जाँच कैसे करते हैं' : 'How we check the math'}
          </a>
          {'  ·  '}
          <a href="/compare"
             onClick={(e) => { e.preventDefault(); go('/compare') }}>
            {lang === 'hi' ? 'ऐप-ऐप में कुंडली क्यों भिन्न' : 'Why charts differ between apps'}
          </a>
        </p>
        <p>
          <a href="/privacy"
             onClick={(e) => { e.preventDefault(); go('/privacy') }}>{t('footer.privacy')}</a>
          {' '}{t('footer.privacyNote')}
          {'  ·  '}
          <a href="/support" className="footer-support"
             onClick={(e) => { e.preventDefault(); go('/support') }}>
            ♥ {t('support.badge', 'Support us')}
          </a>
          {'  ·  '}
          <a href="/references" className="footer-refs"
             onClick={(e) => { e.preventDefault(); go('/references') }}>
            {lang === 'hi' ? 'संदर्भ' : 'References'}
          </a>
        </p>
        <p>
          {t('footer.placeFrom')}{' '}
          <a href="https://www.geonames.org" rel="noreferrer">GeoNames</a>,
          {' '}{t('footer.licensed')}{' '}
          <a href="https://creativecommons.org/licenses/by/4.0/" rel="noreferrer">
            CC BY 4.0
          </a>.
        </p>
      </footer>
    </div>
    </LangContext.Provider>
  )
}
