/**
 * Devashaa Pūjā & Havan — a separate section of the site, for devotion rather
 * than for charts.
 *
 * THE PROPOSITION: practice your traditions, wherever your family lives. A
 * family chooses a ceremony, reads what it is for, sees what to keep ready,
 * finds its day and hour (the muhūrta, for its own city), and then KEEPS it —
 * on its own with the guide (each mantra with what is happening and why,
 * read aloud in the language it chooses), with relatives in other homes in
 * one room, or with a vetted pandit leading it live. A pandit is one way to
 * keep a ceremony here, not the only one.
 *
 * It shares nothing with the astrology side but the pañcāṅga engine (for the
 * calendar and the muhūrta) and the account sign-in (for pandits). No ceremony
 * here is prescribed from a horoscope, and nothing is promised of one.
 *
 * Routes, all under /pooja:
 *   /pooja                       home
 *   /pooja/rituals               the catalogue
 *   /pooja/ritual/<key>          one ceremony: purpose, steps, sāmagrī, muhūrta, ways to keep it
 *   /pooja/ritual/<key>/guide    the guided ceremony, step by step
 *   /pooja/calendar              the months' observances for a place
 *   /pooja/pandits               the roster · /pooja/join  apply as a pandit
 *   /pooja/b/<id>                a gathering or booking (the id is the family's key)
 *   /pooja/room/<id>             the live room
 *   /pooja/desk                  a pandit's / admin's desk
 */
import { useEffect, useMemo, useRef, useState } from 'react'
import { passwordProblem, USERID_RE, normaliseUserid } from '../account.js'
import { api, getSession, onSession, signIn, signOut } from './papi.js'
import { RITUALS, KIND_LABEL, ritualByKey, ritualsFor, samagriFor, durationLabel } from './rituals.js'
import { ABOUT, HERO_SHLOKA, scriptFor, plainRoman } from './guide.js'
import Guide from './Guide.jsx'
import Muhurta, { PlacePicker, usePlace } from './Muhurta.jsx'
import VoiceStudio from './Chants.jsx'
import Room from './Room.jsx'
import './pooja.css'

const SUPPORT_URL = (import.meta.env.VITE_SUPPORT_URL || '').trim()
const UPI_ID = (import.meta.env.VITE_UPI_ID || '').trim()
const HEX32 = /^[0-9a-f]{32}$/
const pad = (n) => String(n).padStart(2, '0')
const today = () => { const d = new Date(); return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}` }
const fmtWhen = (iso, tz, lang) => {
  const [d, t] = String(iso).split('T')
  const dt = new Date(`${d}T${t || '00:00'}`)
  const day = dt.toLocaleDateString(lang === 'hi' ? 'hi-IN' : 'en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
  return `${day} · ${(t || '').slice(0, 5)}${tz ? ` (${tz})` : ''}`
}

function useSession() {
  const [s, setS] = useState(getSession())
  useEffect(() => onSession(setS), [])
  return s
}

function Card({ title, right, children, className = '' }) {
  return (
    <section className={`dk-card pu-card ${className}`}>
      {title && <h4 className="dk-head"><span>{title}</span>{right && <span className="dk-head-right">{right}</span>}</h4>}
      <div className="dk-body">{children}</div>
    </section>
  )
}

/** Sign in or create an account — the site's own accounts. */
function SignIn({ L, create: createDefault = false, lead }) {
  const [create, setCreate] = useState(createDefault)
  const [userid, setUserid] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const idBad = userid && !USERID_RE.test(normaliseUserid(userid))
  const pwBad = create && password ? passwordProblem(password) : null
  const go = async () => {
    setBusy(true); setErr('')
    try { await signIn(userid, password, create) } catch (e) { setErr(e.message || String(e)) } finally { setBusy(false) }
  }
  return (
    <div className="pu-signin">
      {lead && <p className="pu-lead">{lead}</p>}
      <div className="dt-view-btns pu-tabs">
        <button type="button" className={!create ? 'on' : ''} onClick={() => setCreate(false)}>{L('Sign in', 'साइन इन')}</button>
        <button type="button" className={create ? 'on' : ''} onClick={() => setCreate(true)}>{L('Create account', 'खाता बनाएँ')}</button>
      </div>
      <label>{L('Email (your sign-in id)', 'ईमेल (आपकी साइन-इन आईडी)')}
        <input value={userid} onChange={(e) => setUserid(e.target.value)} autoComplete="username" spellCheck={false} placeholder="you@example.com" /></label>
      {idBad && <p className="pu-err">{L('Use your email address.', 'अपना ईमेल पता लिखें।')}</p>}
      <label>{L('Password', 'पासवर्ड')}
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} autoComplete={create ? 'new-password' : 'current-password'}
               onKeyDown={(e) => e.key === 'Enter' && userid && password && !idBad && !pwBad && go()} /></label>
      {pwBad && <p className="pu-err">{pwBad}</p>}
      {create && <p className="pu-note">{L('There is no password reset — we never send mail. Keep this password safe.', 'पासवर्ड रीसेट नहीं है — हम कभी मेल नहीं भेजते। यह पासवर्ड सुरक्षित रखें।')}</p>}
      <button type="button" className="go" disabled={busy || !userid || !password || idBad || !!pwBad} onClick={go}>{busy ? L('working…', 'कार्य चल रहा है…') : create ? L('Create account', 'खाता बनाएँ') : L('Sign in', 'साइन इन')}</button>
      {err && <p className="pu-err">{err}</p>}
    </div>
  )
}

/** Pay-what-you-wish: nothing is charged for a pūjā; a donation keeps this running. */
function Donate({ L }) {
  const upi = UPI_ID ? `upi://pay?pa=${encodeURIComponent(UPI_ID)}&pn=${encodeURIComponent('Devashaa')}&cu=INR` : ''
  return (
    <Card title={L('Dakṣiṇā — as you wish', 'दक्षिणा — स्वेच्छा से')} className="pu-donate">
      <p className="pu-lead">{L('No fee is set for a pūjā here. If the ceremony was of value to your family, give what you wish — it keeps the pandits and this service going.', 'यहाँ पूजा का कोई शुल्क तय नहीं है। यदि अनुष्ठान आपके परिवार के लिए मूल्यवान रहा, तो जो इच्छा हो दें — इसी से पंडित जी और यह सेवा चलती है।')}</p>
      <div className="pu-donate-btns">
        {SUPPORT_URL
          ? <a className="sup-btn" href={SUPPORT_URL} target="_blank" rel="noopener noreferrer">♥ {L('Give by card (Stripe)', 'कार्ड से दें (Stripe)')}</a>
          : <button type="button" className="sup-btn sup-btn-off" disabled>{L('Card giving opening soon', 'कार्ड से दान शीघ्र')}</button>}
        {upi
          ? <a className="sup-btn pu-upi" href={upi}>₹ {L('Give by UPI', 'UPI से दें')} · {UPI_ID}</a>
          : <button type="button" className="sup-btn sup-btn-off" disabled>₹ {L('UPI (India) opening soon', 'UPI (भारत) शीघ्र')}</button>}
      </div>
      <p className="pu-note">{L('Payments go through Stripe or your UPI app; we never see your card or bank details.', 'भुगतान Stripe या आपके UPI ऐप से होता है; आपके कार्ड या बैंक का विवरण हम कभी नहीं देखते।')}</p>
    </Card>
  )
}

function RitualCard({ r, lang, L, go }) {
  return (
    <a className="pu-ritual" href={`/pooja/ritual/${r.key}`} onClick={(e) => { e.preventDefault(); go(`/pooja/ritual/${r.key}`) }}>
      <span className={`pu-kind k-${r.kind}`}>{KIND_LABEL[r.kind][lang] || KIND_LABEL[r.kind].en}</span>
      <b>{r.name[lang] || r.name.en}</b>
      <span className="pu-ritual-purpose">{r.purpose[lang] || r.purpose.en}</span>
      <span className="pu-ritual-meta">{durationLabel(r.minutes, lang === 'hi')}{r.havan ? ` · ${L('with havan', 'हवन सहित')}` : ''}</span>
    </a>
  )
}

/** The next observances at a place, from the pañcāṅga engine. */
function useObservances(place, months = 2) {
  const [days, setDays] = useState(null)
  const [err, setErr] = useState('')
  useEffect(() => {
    let dead = false
    setDays(null); setErr('')
    const now = new Date()
    const reqs = Array.from({ length: months }, (_, i) => {
      const d = new Date(now.getFullYear(), now.getMonth() + i, 1)
      return api.observances(place, d.getFullYear(), d.getMonth() + 1)
    })
    Promise.all(reqs).then((rs) => { if (!dead) setDays(rs.flatMap((r) => r.days || [])) }).catch((e) => { if (!dead) setErr(e.message || String(e)) })
    return () => { dead = true }
  }, [place.latitude, place.longitude, place.timezone, months])
  return { days, err }
}

function ObservanceList({ days, lang, L, go, limit, fromToday = true }) {
  const t0 = today()
  const rows = (days || []).filter((d) => d.festivals && d.festivals.length && (!fromToday || d.date >= t0))
  const shown = limit ? rows.slice(0, limit) : rows
  if (!days) return <p className="pu-note">{L('reading the pañcāṅga…', 'पंचांग पढ़ा जा रहा है…')}</p>
  if (!shown.length) return <p className="pu-note">{L('No observances in this span.', 'इस अवधि में कोई पर्व नहीं।')}</p>
  return (
    <div className="dk-table-wrap">
      <table className="dk-table pu-cal">
        <thead><tr><th>{L('Date', 'तिथि')}</th><th>{L('Observance', 'पर्व / व्रत')}</th><th>{L('Tithi · Nakṣatra', 'तिथि · नक्षत्र')}</th><th>{L('Ceremonies kept on it', 'इस दिन के अनुष्ठान')}</th></tr></thead>
        <tbody>
          {shown.map((d) => {
            const sugg = [...new Map(d.festivals.flatMap((f) => ritualsFor(f.key)).map((r) => [r.key, r])).values()].slice(0, 3)
            const dt = new Date(`${d.date}T12:00`)
            return (
              <tr key={d.date} className={d.festivals.some((f) => f.importance === 'major') ? 'major' : ''}>
                <td className="dk-num"><b>{dt.toLocaleDateString(lang === 'hi' ? 'hi-IN' : 'en-GB', { day: 'numeric', month: 'short' })}</b><span className="dk-en"> {lang === 'hi' ? d.vara_hi : d.vara}</span></td>
                <td>{d.festivals.map((f) => (
                  <div key={f.key} className={`pu-fest ${f.importance}`}><b>{lang === 'hi' ? (f.name_hi || f.name) : f.name}</b>{(lang === 'hi' ? f.significance_hi : f.significance) && <span className="dk-en"> — {lang === 'hi' ? f.significance_hi : f.significance}</span>}</div>
                ))}</td>
                <td>{lang === 'hi' ? d.tithi_hi : d.tithi}<span className="dk-en"> · {lang === 'hi' ? d.nakshatra_hi : d.nakshatra}</span></td>
                <td className="pu-sugg">{sugg.length ? sugg.map((r) => (
                  <a key={r.key} href={`/pooja/ritual/${r.key}?date=${d.date}`} onClick={(e) => { e.preventDefault(); go(`/pooja/ritual/${r.key}?date=${d.date}`) }}>{r.name[lang] || r.name.en}</a>
                )) : <span className="dk-en">—</span>}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}

function Home({ lang, L, go }) {
  const [place, setPlace] = usePlace()
  const { days, err } = useObservances(place, 2)
  const featured = ['satyanarayan', 'ganesh', 'rudrabhishek', 'griha-pravesh', 'durga', 'gayatri-havan'].map(ritualByKey)
  const link = (path) => ({ href: path, onClick: (e) => { e.preventDefault(); go(path) } })
  return (
    <>
      <section className="pu-hero dk-card">
        <div className="dk-body">
          <div className="pu-hero-mark" aria-hidden="true">🪔</div>
          <h1>{L('Bring authentic Sanatan rituals into the home', 'प्रामाणिक सनातन अनुष्ठान — आपके घर में')}</h1>
          <blockquote className="pu-shloka">
            <p lang="sa">{HERO_SHLOKA.dev[0]} <span>{HERO_SHLOKA.dev[1]}</span><br />{HERO_SHLOKA.dev[2]} <span>{HERO_SHLOKA.dev[3]}</span></p>
            <footer>{plainRoman(HERO_SHLOKA.iast)}</footer>
          </blockquote>
          <p className="pu-tagline">{L('Practice your traditions, wherever your family lives.', 'अपनी परंपराएँ निभाइए — आपका परिवार जहाँ भी रहता हो।')}</p>
          <p className="pu-lead">{L('Choose a pūjā or havan and understand it first — what it is for, each mantra with what is happening and why. Find its day and hour for your own city. Then keep it at home: guided step by step, with relatives joining from their homes, or led live by a pandit.', 'पूजा या हवन चुनें और पहले उसे समझें — वह किसलिए है, हर मंत्र के साथ क्या हो रहा है और क्यों। अपने ही शहर के लिए उसका दिन और मुहूर्त देखें। फिर उसे घर पर कीजिए: चरण-दर-चरण मार्गदर्शन के साथ, दूसरे घरों से जुड़े स्वजनों के साथ, या पंडित जी के लाइव संचालन में।')}</p>
          <div className="pu-hero-btns">
            <a className="go" {...link('/pooja/rituals')}>{L('Begin a ceremony', 'अनुष्ठान आरंभ करें')}</a>
            <a className="pu-ghost" {...link('/pooja/calendar')}>{L('The calendar for my city', 'मेरे शहर का पंचांग')}</a>
          </div>
        </div>
      </section>
      <div className="pu-ways">
        <section className="dk-card pu-way">
          <h4 className="dk-head"><span>{L('On your own, guided', 'स्वयं, मार्गदर्शन के साथ')}</span></h4>
          <div className="dk-body"><p>{L('The purpose first, then every step: the mantra as it is chanted, what is happening, and why. Detailed, short, or the mantras alone — read aloud in English or Hindi.', 'पहले उद्देश्य, फिर हर चरण: मंत्र जैसा बोला जाता है, क्या हो रहा है, और क्यों। विस्तार से, संक्षेप में, या केवल मंत्र — हिन्दी या अंग्रेज़ी में पढ़कर सुनाया जाता है।')}</p></div>
        </section>
        <section className="dk-card pu-way">
          <h4 className="dk-head"><span>{L('With the family, wherever they are', 'परिवार के साथ, वे जहाँ भी हों')}</span></h4>
          <div className="dk-body"><p>{L('Open one room and send the link. Grandparents, children and cousins join from their own homes and follow the same step on their screens.', 'एक कक्ष खोलिए और लिंक भेजिए। दादा-दादी, बच्चे और भाई-बहन अपने-अपने घर से जुड़ते हैं और अपनी स्क्रीन पर वही चरण देखते हैं।')}</p></div>
        </section>
        <section className="dk-card pu-way">
          <h4 className="dk-head"><span>{L('With a pandit, live', 'पंडित जी के साथ, लाइव')}</span></h4>
          <div className="dk-body"><p>{L('When you want it led: a pandit we know, or one vetted by them, chants in the room while each of you reads what the step is and why, in your own language. Recorded, to watch again.', 'जब आप चाहें कि कोई कराए: हमारे परिचित, या उनके परखे हुए पंडित जी कक्ष में मंत्रोच्चार करते हैं, और आप में से हर कोई अपनी भाषा में पढ़ता है कि चरण क्या है और क्यों। रिकॉर्ड होता है, फिर देखने के लिए।')}</p></div>
        </section>
      </div>
      <Card title={L('Begin with one of these', 'इनमें से किसी से आरंभ करें')} right={<a {...link('/pooja/rituals')}>{L('all sixteen →', 'सभी सोलह →')}</a>}>
        <div className="pu-rituals">{featured.map((r) => <RitualCard key={r.key} r={r} lang={lang} L={L} go={go} />)}</div>
      </Card>
      <Card title={L('Coming up in the calendar', 'पंचांग में आगे')} right={<a {...link('/pooja/calendar')}>{L('full calendar →', 'पूरा पंचांग →')}</a>}>
        <PlacePicker place={place} setPlace={setPlace} L={L} />
        {err ? <p className="pu-err">{err}</p> : <ObservanceList days={days} lang={lang} L={L} go={go} limit={5} />}
      </Card>
      <Card title={L('What this section stands on', 'यह सेवा किस पर टिकी है')}>
        <ul className="pu-points">
          <li>{L('Understanding before ritual. Every ceremony is explained before it is chanted — and the explanation says what a step is and why it is done; it does not pass off a paraphrase as a translation of the Sanskrit.', 'पहले समझ, फिर विधि। हर अनुष्ठान मंत्रोच्चार से पहले समझाया जाता है — और व्याख्या बताती है कि चरण क्या है और क्यों किया जाता है; वह किसी भावार्थ को संस्कृत का अनुवाद बताकर नहीं परोसती।')}</li>
          <li>{L('The day and the hour are computed for your own city from its sunrise and sunset, with the reason shown.', 'दिन और मुहूर्त आपके ही शहर के सूर्योदय और सूर्यास्त से गणित होते हैं, कारण सहित।')}</li>
          <li>{L('Every pandit here is known to us or vetted by a pandit who is. Any pandit may apply to join.', 'यहाँ हर पंडित जी हमारे परिचित हैं या किसी परिचित पंडित द्वारा परखे गए हैं। कोई भी पंडित जुड़ने के लिए आवेदन कर सकते हैं।')} <a {...link('/pooja/join')}>{L('Join as a pandit →', 'पंडित के रूप में जुड़ें →')}</a></li>
          <li>{L('No fee is set. Give what you wish.', 'कोई शुल्क तय नहीं। स्वेच्छा से दें।')}</li>
          <li>{L('A pūjā is an act of devotion. Nothing here is prescribed from a horoscope, and nothing is promised of a ceremony.', 'पूजा भक्ति का कार्य है। यहाँ कुछ भी कुंडली देखकर नहीं बताया जाता, और किसी अनुष्ठान का कोई फल वादा नहीं किया जाता।')}</li>
        </ul>
      </Card>
    </>
  )
}

function Rituals({ lang, L, go }) {
  const [kind, setKind] = useState('all')
  const list = RITUALS.filter((r) => kind === 'all' || r.kind === kind)
  return (
    <Card title={L('The ceremonies', 'अनुष्ठान')} right={(
      <span className="pu-filter">
        {['all', 'puja', 'havan', 'path', 'samskara'].map((k) => (
          <button type="button" key={k} className={kind === k ? 'on' : ''} onClick={() => setKind(k)}>{k === 'all' ? L('All', 'सभी') : (KIND_LABEL[k][lang] || KIND_LABEL[k].en)}</button>
        ))}
      </span>
    )}>
      <div className="pu-rituals">{list.map((r) => <RitualCard key={r.key} r={r} lang={lang} L={L} go={go} />)}</div>
      <p className="pu-note">{L('Rites differ by region and family custom. The outline and list on each page are a starting point — your pandit confirms both before the day.', 'विधि क्षेत्र और कुल-परंपरा से बदलती है। हर पृष्ठ की रूपरेखा और सूची आरंभ-बिंदु है — पंडित जी दिन से पहले दोनों की पुष्टि करते हैं।')}</p>
    </Card>
  )
}

/** The ways to keep a ceremony: on your own, with the family in a room, or led by a pandit. */
function Keep({ r, lang, L, go, when, place }) {
  const [tab, setTab] = useState('self')
  const [priests, setPriests] = useState([])
  const [f, setF] = useState({ priest: '', name: '', contact: '', family: 2, notes: '' })
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  useEffect(() => { api.priests().then((j) => setPriests(j.priests || [])).catch(() => {}) }, [])
  const set = (k) => (e) => setF((x) => ({ ...x, [k]: e.target.value }))
  const timed = when.date && when.time
  const city = place.name.split(',')[0]
  const send = async (self) => {
    setBusy(true); setErr('')
    try {
      const j = await api.book({ ritual: r.key, starts_at: `${when.date}T${when.time}`, tz: place.timezone, city, lang, self,
        ...(self ? { name: f.name } : { priest: f.priest || null, name: f.name, contact: f.contact, family: f.family, notes: f.notes }) })
      go(`/pooja/b/${j.id}`)
    } catch (e2) { setErr(e2.message || String(e2)) } finally { setBusy(false) }
  }
  const whenLine = timed
    ? <p className="pu-when">{fmtWhen(`${when.date}T${when.time}`, '', lang)} · {city}</p>
    : <p className="pu-note">{L('Choose the date and the time above first.', 'पहले ऊपर दिनांक और समय चुनें।')}</p>
  return (
    <div className="pu-keep">
      <div className="dt-view-btns pu-tabs">
        <button type="button" className={tab === 'self' ? 'on' : ''} onClick={() => setTab('self')}>{L('On our own, guided', 'स्वयं, मार्गदर्शन के साथ')}</button>
        <button type="button" className={tab === 'pandit' ? 'on' : ''} onClick={() => setTab('pandit')}>{L('Invite a pandit to lead it', 'पंडित जी को आमंत्रित करें')}</button>
      </div>
      {tab === 'self' ? (
        <div className="pu-form">
          <p className="pu-lead">{L('Keep it yourselves with the guide: the purpose first, then each step with its mantra, what is happening and why.', 'मार्गदर्शन के साथ स्वयं कीजिए: पहले उद्देश्य, फिर हर चरण — मंत्र, क्या हो रहा है और क्यों।')}</p>
          <div className="pu-bk-actions">
            <a className="go" href={`/pooja/ritual/${r.key}/guide`} onClick={(e) => { e.preventDefault(); go(`/pooja/ritual/${r.key}/guide`) }}>▶ {L('Begin now, guided', 'अभी आरंभ करें')}</a>
          </div>
          <h5 className="pu-sub">{L('Relatives in other homes?', 'स्वजन दूसरे घरों में हैं?')}</h5>
          <p className="pu-note">{L('Open a family room for the day. Everyone joins by video from their own home and follows the same step. Nothing but a name for the gathering is stored.', 'उस दिन के लिए परिवार-कक्ष खोलिए। सब अपने घर से वीडियो पर जुड़ते हैं और वही चरण देखते हैं। सभा के नाम के अतिरिक्त कुछ भी संग्रहीत नहीं होता।')}</p>
          {whenLine}
          <div className="pu-form-row">
            <label>{L('A name for the gathering', 'सभा का नाम')}<input value={f.name} onChange={set('name')} placeholder={L('e.g. the Sharma family', 'जैसे शर्मा परिवार')} /></label>
            <button type="button" className="pu-ghost pu-rowbtn" disabled={!timed || busy} onClick={() => send(true)}>{busy ? L('opening…', 'खुल रहा है…') : L('Open a family room', 'परिवार-कक्ष खोलें')}</button>
          </div>
        </div>
      ) : (
        <form className="pu-form" onSubmit={(e) => { e.preventDefault(); send(false) }}>
          <p className="pu-lead">{L('A pandit chants and leads in the live room; every home follows the step on its own screen, in its own language. The ceremony is recorded for you to watch again.', 'पंडित जी लाइव कक्ष में मंत्रोच्चार और संचालन करते हैं; हर घर अपनी स्क्रीन पर, अपनी भाषा में चरण देखता है। अनुष्ठान रिकॉर्ड होता है ताकि आप फिर देख सकें।')}</p>
          {whenLine}
          <div className="pu-form-row">
            <label>{L('Pandit', 'पंडित जी')}
              <select value={f.priest} onChange={set('priest')}>
                <option value="">{L('Any available pandit', 'कोई भी उपलब्ध पंडित जी')}</option>
                {priests.map((p) => <option key={p.id} value={p.id}>{p.name}{p.city ? ` — ${p.city}` : ''}{p.languages ? ` · ${p.languages}` : ''}</option>)}
              </select></label>
            <label>{L('Homes joining', 'कितने घर जुड़ेंगे')}<input type="number" min="1" max="50" value={f.family} onChange={set('family')} /></label>
          </div>
          <div className="pu-form-row">
            <label>{L('Your name', 'आपका नाम')}<input value={f.name} onChange={set('name')} required /></label>
            <label>{L('Phone / WhatsApp or email', 'फ़ोन / व्हाट्सऐप या ईमेल')}<input value={f.contact} onChange={set('contact')} required /></label>
          </div>
          <label>{L('Anything the pandit should know (gotra, occasion, language, tradition)', 'पंडित जी के लिए जानकारी (गोत्र, अवसर, भाषा, परंपरा)')}<textarea rows="3" value={f.notes} onChange={set('notes')} /></label>
          <p className="pu-note">{L('Your name and contact are shown only to the pandit who takes your request, so they can reach you. No fee is set — give what you wish afterwards.', 'आपका नाम और संपर्क केवल उन पंडित जी को दिखता है जो आपका अनुरोध लेते हैं, ताकि वे आपसे संपर्क कर सकें। कोई शुल्क तय नहीं — बाद में स्वेच्छा से दें।')}</p>
          <button type="submit" className="go" disabled={!timed || busy || f.name.trim().length < 2 || f.contact.trim().length < 5}>{busy ? L('sending…', 'भेजा जा रहा है…') : L('Request a pandit', 'पंडित जी का अनुरोध करें')}</button>
        </form>
      )}
      {err && <p className="pu-err">{err}</p>}
    </div>
  )
}

function RitualDetail({ rkey, lang, L, go, query }) {
  const r = ritualByKey(rkey)
  const [place, setPlace] = usePlace()
  const [date, setDate] = useState(query.get('date') || '')
  const [time, setTime] = useState('')
  const hourRef = useRef(null)
  if (!r) return <Card title={L('Not found', 'नहीं मिला')}><p>{L('That ceremony is not in the catalogue.', 'यह अनुष्ठान सूची में नहीं है।')}</p></Card>
  const hi = lang === 'hi'
  const steps = scriptFor(r.key)
  const about = ABOUT[r.key]
  const guide = `/pooja/ritual/${r.key}/guide`
  return (
    <>
      <section className="pu-ritual-head dk-card">
        <div className="dk-body">
          <span className={`pu-kind k-${r.kind}`}>{KIND_LABEL[r.kind][lang] || KIND_LABEL[r.kind].en}</span>
          <h1>{r.name[lang] || r.name.en}</h1>
          <p className="pu-lead">{r.purpose[lang] || r.purpose.en}</p>
          <p className="pu-ritual-meta">{L('About', 'लगभग')} {durationLabel(r.minutes, hi)}{r.havan ? ` · ${L('with havan', 'हवन सहित')}` : ''} · {steps.length} {L('steps', 'चरण')}</p>
          <div className="pu-hero-btns">
            <a className="go" href={guide} onClick={(e) => { e.preventDefault(); go(guide) }}>▶ {L('Begin — guided, step by step', 'आरंभ करें — चरण-दर-चरण')}</a>
            <button type="button" className="pu-ghost" onClick={() => hourRef.current && hourRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })}>{L('Choose the day and hour', 'दिन और मुहूर्त चुनें')}</button>
          </div>
        </div>
      </section>
      {about && (
        <Card title={L('Why this ceremony is kept', 'यह अनुष्ठान क्यों किया जाता है')}>
          <p className="pu-about">{about[lang] || about.en}</p>
        </Card>
      )}
      <div className="pu-two">
        <Card title={L('The steps, and why each is done', 'चरण, और हर एक क्यों')} right={<a href={guide} onClick={(e) => { e.preventDefault(); go(guide) }}>{L('with the mantras →', 'मंत्रों सहित →')}</a>}>
          <ol className="pu-outline">{steps.map((s) => <li key={s.id}><b>{s.title[lang] || s.title.en}</b><span>{s.why[lang] || s.why.en}</span></li>)}</ol>
        </Card>
        <Card title={L('What to keep ready (sāmagrī)', 'क्या तैयार रखें (सामग्री)')}>
          <ul className="pu-samagri">{samagriFor(r).map((s, i) => <li key={i}>{s[lang] || s.en}</li>)}</ul>
          <p className="pu-note">{L('A starting list — rites differ by region and family; where a pandit leads, he confirms the exact sāmagrī. Kit delivery is coming.', 'आरंभिक सूची — विधि क्षेत्र और कुल से बदलती है; जहाँ पंडित जी करा रहे हों, सटीक सामग्री वे बताते हैं। किट डिलीवरी शीघ्र।')}</p>
        </Card>
      </div>
      <div ref={hourRef} className="pu-anchor">
        <Card title={L('The day and the hour — muhūrta for your city', 'दिन और समय — आपके शहर का मुहूर्त')}>
          <Muhurta ritual={r} place={place} setPlace={setPlace} date={date} setDate={setDate} time={time} setTime={setTime} lang={lang} L={L} />
        </Card>
      </div>
      <Card title={L('Keep this ceremony', 'यह अनुष्ठान कीजिए')}>
        <Keep r={r} lang={lang} L={L} go={go} when={{ date, time }} place={place} />
      </Card>
    </>
  )
}

/** The guided ceremony on its own page. */
function GuidePage({ rkey, lang, L, go }) {
  const r = ritualByKey(rkey)
  if (!r) return <Card title={L('Not found', 'नहीं मिला')}><p>{L('That ceremony is not in the catalogue.', 'यह अनुष्ठान सूची में नहीं है।')}</p></Card>
  const back = `/pooja/ritual/${r.key}`
  return (
    <Card title={r.name[lang] || r.name.en} right={<a href={back} onClick={(e) => { e.preventDefault(); go(back) }}>{L('← sāmagrī, muhūrta, invite a pandit', '← सामग्री, मुहूर्त, पंडित जी')}</a>} className="pu-guide-card">
      <Guide ritual={r} lang={lang} L={L} />
    </Card>
  )
}

function Calendar({ lang, L, go }) {
  const [place, setPlace] = usePlace()
  const { days, err } = useObservances(place, 3)
  return (
    <Card title={L('The religious calendar — next three months', 'धार्मिक पंचांग — अगले तीन माह')}>
      <PlacePicker place={place} setPlace={setPlace} L={L} />
      <p className="pu-note">{L('Computed for your city: an observance falls on the day its tithi holds at sunrise there, so dates can differ by a day between countries.', 'आपके शहर के लिए गणना: पर्व उस दिन पड़ता है जिस दिन वहाँ सूर्योदय पर उसकी तिथि हो, अतः देशों के बीच एक दिन का अंतर संभव है।')}</p>
      {err ? <p className="pu-err">{err}</p> : <ObservanceList days={days} lang={lang} L={L} go={go} />}
    </Card>
  )
}

function Pandits({ L, go }) {
  const [list, setList] = useState(null)
  useEffect(() => { api.priests().then((j) => setList(j.priests || [])).catch(() => setList([])) }, [])
  return (
    <Card title={L('The pandits', 'पंडित जी')} right={<a href="/pooja/join" onClick={(e) => { e.preventDefault(); go('/pooja/join') }}>{L('Join as a pandit →', 'पंडित के रूप में जुड़ें →')}</a>}>
      {!list ? <p className="pu-note">{L('loading…', 'लोड हो रहा है…')}</p> : !list.length ? (
        <p className="pu-lead">{L('The first pandits are being added. You can request a ceremony now — it goes to the first available pandit as soon as they join.', 'पहले पंडित जी जोड़े जा रहे हैं। आप अभी अनुरोध कर सकते हैं — वह पहले उपलब्ध पंडित जी के पास जाएगा।')}</p>
      ) : (
        <div className="pu-pandits">
          {list.map((p) => (
            <div key={p.id} className="pu-pandit">
              <b>{p.name}</b>
              <span className="dk-en">{[p.city, p.country].filter(Boolean).join(', ')}{p.years ? ` · ${p.years} ${L('years', 'वर्ष')}` : ''}</span>
              {p.voice && <span><i>{L('Voice', 'स्वर')}:</i> {p.voice === 'f' ? L('female', 'स्त्री') : L('male', 'पुरुष')}</span>}
              {p.languages && <span><i>{L('Languages', 'भाषाएँ')}:</i> {p.languages}</span>}
              {p.traditions && <span><i>{L('Tradition', 'परंपरा')}:</i> {p.traditions}</span>}
              {p.rituals && <span><i>{L('Ceremonies', 'अनुष्ठान')}:</i> {p.rituals}</span>}
              {p.bio && <p>{p.bio}</p>}
            </div>
          ))}
        </div>
      )}
      <p className="pu-note">{L('Every pandit listed is known to us or was vetted by one who is.', 'सूची के हर पंडित जी हमारे परिचित हैं या किसी परिचित पंडित द्वारा परखे गए हैं।')}</p>
    </Card>
  )
}

function Join({ L }) {
  const s = useSession()
  const [me, setMe] = useState(null)
  const [f, setF] = useState({ name: '', voice: '', city: '', country: '', languages: '', traditions: '', rituals: '', years: '', bio: '', contact: '' })
  const [msg, setMsg] = useState('')
  const [err, setErr] = useState('')
  useEffect(() => {
    if (!s) { setMe(null); return }
    api.me().then((j) => { setMe(j); if (j.priest) setF((x) => ({ ...x, ...Object.fromEntries(Object.keys(x).map((k) => [k, j.priest[k] ?? ''])) })) }).catch((e) => setErr(e.message))
  }, [s])
  const set = (k) => (e) => setF((x) => ({ ...x, [k]: e.target.value }))
  const submit = async (e) => {
    e.preventDefault(); setErr(''); setMsg('')
    try { const j = await api.apply(f); setMsg(j.status === 'approved' ? L('Profile updated.', 'प्रोफ़ाइल अद्यतन हुई।') : L('Application received. A pandit on the roster will review it.', 'आवेदन प्राप्त हुआ। सूची के कोई पंडित जी इसे देखेंगे।')); setMe(await api.me()) } catch (e2) { setErr(e2.message || String(e2)) }
  }
  return (
    <Card title={L('Join as a pandit', 'पंडित के रूप में जुड़ें')}>
      <p className="pu-lead">{L('Tell families who you are and which ceremonies you lead. A pandit already on the roster reviews every application before it is listed.', 'परिवारों को बताइए आप कौन हैं और कौन-से अनुष्ठान कराते हैं। सूची में आने से पहले हर आवेदन को सूची के कोई पंडित जी देखते हैं।')}</p>
      {!s ? <SignIn L={L} create lead={L('First, an account to sign in with:', 'पहले, साइन-इन के लिए एक खाता:')} /> : (
        <form className="pu-form" onSubmit={submit}>
          {me?.priest && <p className={`pu-status s-${me.priest.status}`}>{L('Status', 'स्थिति')}: <b>{me.priest.status}</b></p>}
          <div className="pu-form-row">
            <label>{L('Name as families should see it', 'नाम जैसा परिवार देखें')}<input value={f.name} onChange={set('name')} required /></label>
            <label>{L('City', 'शहर')}<input value={f.city} onChange={set('city')} /></label>
            <label>{L('Country', 'देश')}<input value={f.country} onChange={set('country')} /></label>
          </div>
          <div className="pu-form-row">
            <label>{L('Languages', 'भाषाएँ')}<input value={f.languages} onChange={set('languages')} placeholder="Hindi, Sanskrit, English" /></label>
            <label>{L('Tradition / śākhā', 'परंपरा / शाखा')}<input value={f.traditions} onChange={set('traditions')} /></label>
            <label>{L('Years of practice', 'अनुभव (वर्ष)')}<input type="number" min="0" max="90" value={f.years} onChange={set('years')} /></label>
            <label>{L('Your voice (families choose a male or a female voice)', 'आपकी आवाज़ (परिवार पुरुष या स्त्री स्वर चुनते हैं)')}
              <select value={f.voice} onChange={set('voice')} required>
                <option value="">{L('choose…', 'चुनें…')}</option>
                <option value="m">{L('Male', 'पुरुष')}</option>
                <option value="f">{L('Female', 'स्त्री')}</option>
              </select></label>
          </div>
          <label>{L('Ceremonies you lead', 'आप कौन-से अनुष्ठान कराते हैं')}<input value={f.rituals} onChange={set('rituals')} placeholder="Satyanārāyaṇa, Rudrābhiṣeka, Gṛha praveśa…" /></label>
          <label>{L('About you (training, guru, where you have served)', 'आपके बारे में (शिक्षा, गुरु, सेवा-स्थान)')}<textarea rows="4" value={f.bio} onChange={set('bio')} /></label>
          <label>{L('Phone / WhatsApp (seen only by those who vet you)', 'फ़ोन / व्हाट्सऐप (केवल परखने वालों को दिखेगा)')}<input value={f.contact} onChange={set('contact')} /></label>
          <button type="submit" className="go">{me?.priest ? L('Update', 'अद्यतन करें') : L('Apply', 'आवेदन करें')}</button>
          {msg && <p className="pu-ok">{msg}</p>}{err && <p className="pu-err">{err}</p>}
        </form>
      )}
    </Card>
  )
}

function BookingPage({ id, lang, L, go }) {
  const s = useSession()
  const [b, setB] = useState(null)
  const [err, setErr] = useState('')
  const [copied, setCopied] = useState(false)
  const load = () => api.booking(id).then(setB).catch((e) => setErr(e.message || String(e)))
  useEffect(() => { load() }, [id, s])  // eslint-disable-line react-hooks/exhaustive-deps
  if (err) return <Card title={L('Booking', 'बुकिंग')}><p className="pu-err">{err}</p></Card>
  if (!b) return <Card title={L('Booking', 'बुकिंग')}><p className="pu-note">{L('loading…', 'लोड हो रहा है…')}</p></Card>
  const r = ritualByKey(b.ritual)
  const here = `${location.origin}/pooja/b/${b.id}`
  const mine = !!(s && b.mine)
  const self = b.status === 'self'
  const STATUS = { self: L('Family gathering — self-guided', 'परिवार की सभा — स्वयं, मार्गदर्शन के साथ'), requested: L('Requested — waiting for a pandit', 'अनुरोध भेजा गया — पंडित जी की प्रतीक्षा'), confirmed: L('Confirmed', 'पुष्टि हो गई'), completed: L('Completed', 'संपन्न'), cancelled: L('Cancelled', 'रद्द') }
  const act = (fn) => async () => { try { await fn(b.id); await load() } catch (e) { setErr(e.message || String(e)) } }
  return (
    <>
      <Card title={r ? (r.name[lang] || r.name.en) : b.ritual} right={<span className={`pu-status s-${b.status}`}>{STATUS[b.status] || b.status}</span>}>
        <table className="dk-table pu-bk">
          <tbody>
            <tr><th>{L('When', 'कब')}</th><td>{fmtWhen(b.starts_at, b.tz, lang)}</td></tr>
            <tr><th>{L('For', 'किसके लिए')}</th><td>{b.name}{b.city ? ` — ${b.city}` : ''}{self ? '' : ` · ${b.family} ${L('home(s) joining', 'घर जुड़ेंगे')}`}</td></tr>
            {self
              ? <tr><th>{L('Led by', 'संचालन')}</th><td>{L('The family, with the guide — anyone in the room can move the step for all.', 'परिवार स्वयं, मार्गदर्शन के साथ — कक्ष में कोई भी सबके लिए चरण आगे बढ़ा सकता है।')}</td></tr>
              : <tr><th>{L('Pandit', 'पंडित जी')}</th><td>{b.priest ? b.priest.name : L('not yet assigned', 'अभी निर्धारित नहीं')}</td></tr>}
            {b.notes && <tr><th>{L('Notes', 'टिप्पणी')}</th><td>{b.notes}</td></tr>}
            {b.contact && <tr><th>{L('Reach the family', 'परिवार से संपर्क')}</th><td>{b.contact}</td></tr>}
          </tbody>
        </table>
        <div className="pu-bk-actions">
          {b.status !== 'cancelled' && <a className="go" href={`/pooja/room/${b.id}`} onClick={(e) => { e.preventDefault(); go(`/pooja/room/${b.id}`) }}>{L('Enter the room', 'कक्ष में प्रवेश')}</a>}
          {r && <a className="pu-ghost" href={`/pooja/ritual/${r.key}/guide`} onClick={(e) => { e.preventDefault(); go(`/pooja/ritual/${r.key}/guide`) }}>{L('Read the steps beforehand', 'चरण पहले पढ़ लें')}</a>}
          <button type="button" className="pu-ghost" onClick={() => { try { navigator.clipboard.writeText(here); setCopied(true); setTimeout(() => setCopied(false), 1600) } catch { /* no clipboard */ } }}>{copied ? L('Copied', 'कॉपी हुआ') : L('Copy this link', 'यह लिंक कॉपी करें')}</button>
          <a className="pu-ghost" href={`https://wa.me/?text=${encodeURIComponent(`${r ? r.name.en : b.ritual} — ${fmtWhen(b.starts_at, b.tz, 'en')}\n${location.origin}/pooja/room/${b.id}`)}`} target="_blank" rel="noreferrer">{L('Send the room to family (WhatsApp)', 'परिवार को कक्ष भेजें (व्हाट्सऐप)')}</a>
          {s && !mine && !self && b.status === 'requested' && <button type="button" className="go" onClick={act(api.accept)}>{L('Accept as pandit', 'पंडित के रूप में स्वीकार करें')}</button>}
          {mine && b.status === 'confirmed' && <button type="button" className="pu-ghost" onClick={act(api.complete)}>{L('Mark completed', 'संपन्न चिह्नित करें')}</button>}
          {b.status !== 'completed' && b.status !== 'cancelled' && <button type="button" className="pu-ghost danger" onClick={act(api.cancel)}>{L('Cancel', 'रद्द करें')}</button>}
        </div>
        <p className="pu-note">{self
          ? L('Keep this link — it is your key to the room. Anyone you send the room link to can join. A family gathering is not recorded; a ceremony led by a pandit is.', 'यह लिंक सँभालकर रखें — यही कक्ष की कुंजी है। जिसे भी कक्ष का लिंक भेजेंगे वह जुड़ सकता है। परिवार की सभा रिकॉर्ड नहीं होती; पंडित जी द्वारा कराया अनुष्ठान होता है।')
          : L('Keep this link — it is your key to the request, the room and the recording. Anyone you send the room link to can join.', 'यह लिंक सँभालकर रखें — यही अनुरोध, कक्ष और रिकॉर्डिंग की कुंजी है। जिसे भी कक्ष का लिंक भेजेंगे वह जुड़ सकता है।')}</p>
      </Card>
      {b.recording && b.recording.available && (
        <Card title={L('The recording', 'रिकॉर्डिंग')}>
          <video className="pu-video" controls preload="metadata" src={api.playUrl(b.id)} />
          <p className="pu-note">{L('Recorded in the room and kept for your family. Seeking may be limited while it loads.', 'कक्ष में रिकॉर्ड किया गया और आपके परिवार के लिए सुरक्षित। लोड होते समय आगे-पीछे करना सीमित हो सकता है।')}</p>
        </Card>
      )}
      {r && (
        <Card title={L('What to keep ready', 'क्या तैयार रखें')}>
          <ul className="pu-samagri">{samagriFor(r).map((x, i) => <li key={i}>{x[lang] || x.en}</li>)}</ul>
        </Card>
      )}
      <Donate L={L} />
    </>
  )
}

function RoomGate({ id, lang, L, go }) {
  const s = useSession()
  const [b, setB] = useState(null)
  const [name, setName] = useState('')
  const [inRoom, setInRoom] = useState(false)
  const [err, setErr] = useState('')
  useEffect(() => { api.booking(id).then(setB).catch((e) => setErr(e.message || String(e))) }, [id, s])
  if (err) return <Card title={L('The room', 'कक्ष')}><p className="pu-err">{err}</p></Card>
  if (!b) return <Card title={L('The room', 'कक्ष')}><p className="pu-note">{L('loading…', 'लोड हो रहा है…')}</p></Card>
  const isPriest = !!(s && b.mine)
  const r = ritualByKey(b.ritual)
  const selfLed = b.status === 'self'
  if (inRoom) return <Room bookingId={id} name={name.trim() || (isPriest ? b.priest.name : L('Family', 'परिवार'))} role={isPriest ? 'priest' : 'family'} canRecord={isPriest} ritual={r} selfLed={selfLed} lang={lang} L={L} onLeave={() => { setInRoom(false); go(`/pooja/b/${id}`) }} />
  return (
    <Card title={`${r ? r.name.en : b.ritual} — ${L('the room', 'कक्ष')}`}>
      <p className="pu-lead">{fmtWhen(b.starts_at, b.tz, 'en')}{b.priest ? ` · ${L('with', 'पंडित जी')} ${b.priest.name}` : ''}</p>
      <div className="pu-form">
        <label>{L('Your name, as the others will see it', 'आपका नाम, जैसा दूसरों को दिखेगा')}<input value={name} onChange={(e) => setName(e.target.value)} placeholder={isPriest ? b.priest.name : L('e.g. the Sharma family, Pune', 'जैसे शर्मा परिवार, पुणे')} /></label>
        <button type="button" className="go" onClick={() => setInRoom(true)}>{L('Join with camera and microphone', 'कैमरा और माइक के साथ जुड़ें')}</button>
        <p className="pu-note">{selfLed
          ? L('Your browser will ask for the camera and microphone. The steps of the ceremony are beside the video; whoever moves the step moves it for everyone.', 'ब्राउज़र कैमरा और माइक की अनुमति माँगेगा। अनुष्ठान के चरण वीडियो के साथ दिखते हैं; जो भी चरण बढ़ाता है, वह सबके लिए बढ़ता है।')
          : L('Your browser will ask for the camera and microphone. The pandit may record the ceremony; you will see when it is on. Beside the video, each step is explained in the language you choose.', 'ब्राउज़र कैमरा और माइक की अनुमति माँगेगा। पंडित जी अनुष्ठान रिकॉर्ड कर सकते हैं; चालू होने पर आपको दिखेगा। वीडियो के साथ हर चरण आपकी चुनी भाषा में समझाया जाता है।')}</p>
        {!isPriest && !s && !selfLed && <p className="pu-note">{L('Leading this ceremony?', 'क्या आप यह अनुष्ठान करा रहे हैं?')} <a href="/pooja/desk" onClick={(e) => { e.preventDefault(); go('/pooja/desk') }}>{L('Sign in as the pandit', 'पंडित के रूप में साइन इन')}</a></p>}
      </div>
    </Card>
  )
}

function Desk({ lang, L, go }) {
  const s = useSession()
  const [d, setD] = useState(null)
  const [code, setCode] = useState('')
  const [err, setErr] = useState('')
  const load = () => api.desk().then(setD).catch((e) => setErr(e.message || String(e)))
  useEffect(() => { if (s) load(); else setD(null) }, [s])  // eslint-disable-line react-hooks/exhaustive-deps
  if (!s) return <Card title={L('The pandit’s desk', 'पंडित जी की डेस्क')}><SignIn L={L} lead={L('Sign in to see the bookings waiting for you.', 'आपकी प्रतीक्षा कर रही बुकिंग देखने के लिए साइन इन करें।')} /></Card>
  const act = (fn, ...a) => async () => { setErr(''); try { await fn(...a); await load() } catch (e) { setErr(e.message || String(e)) } }
  return (
    <>
      <Card title={L('The pandit’s desk', 'पंडित जी की डेस्क')} right={<span>{s.userid} · <a href="#out" onClick={(e) => { e.preventDefault(); signOut() }}>{L('sign out', 'साइन आउट')}</a></span>}>
        {err && <p className="pu-err">{err}</p>}
        {!d ? <p className="pu-note">{L('loading…', 'लोड हो रहा है…')}</p> : !d.role ? (
          <>
            <p className="pu-lead">{d.priest ? L(`Your application is ${d.priest.status}. Once a pandit on the roster approves it, your bookings appear here.`, `आपका आवेदन ${d.priest.status} है। सूची के पंडित जी की स्वीकृति के बाद आपकी बुकिंग यहाँ दिखेंगी।`) : L('You are not on the roster yet.', 'आप अभी सूची में नहीं हैं।')} <a href="/pooja/join" onClick={(e) => { e.preventDefault(); go('/pooja/join') }}>{L('Apply / edit profile →', 'आवेदन / प्रोफ़ाइल →')}</a></p>
            <div className="pu-claim">
              <label>{L('Admin code (the owner only)', 'एडमिन कोड (केवल स्वामी)')}<input value={code} onChange={(e) => setCode(e.target.value)} /></label>
              <button type="button" className="pu-ghost" disabled={!code} onClick={act(api.claim, code)}>{L('Claim', 'दावा करें')}</button>
            </div>
          </>
        ) : (
          <p className="pu-lead">{L('Signed in as', 'साइन इन')}: <b>{d.role === 'admin' ? L('admin', 'एडमिन') : L('pandit', 'पंडित')}</b>{d.priest ? ` · ${d.priest.name}` : ''} · <a href="/pooja/join" onClick={(e) => { e.preventDefault(); go('/pooja/join') }}>{L('edit profile', 'प्रोफ़ाइल बदलें')}</a></p>
        )}
      </Card>
      {d && d.role && (
        <>
          <Card title={`${L('Applications to vet', 'परखने हेतु आवेदन')} (${d.applicants.length})`}>
            {!d.applicants.length ? <p className="pu-note">{L('None waiting.', 'कोई प्रतीक्षा में नहीं।')}</p> : d.applicants.map((p) => (
              <div key={p.id} className="pu-applicant">
                <div><b>{p.name}</b> <span className="dk-en">{[p.city, p.country].filter(Boolean).join(', ')}{p.years ? ` · ${p.years}y` : ''}{p.voice === 'f' ? ` · ${L('female voice', 'स्त्री स्वर')}` : p.voice === 'm' ? ` · ${L('male voice', 'पुरुष स्वर')}` : ''}</span>
                  <p>{[p.languages, p.traditions, p.rituals].filter(Boolean).join(' · ')}</p>{p.bio && <p>{p.bio}</p>}{p.contact && <p className="dk-en">{p.contact}</p>}</div>
                <div className="pu-applicant-btns">
                  <button type="button" className="go" onClick={act(api.vet, p.id, 'approve')}>{L('Approve', 'स्वीकृत')}</button>
                  <button type="button" className="pu-ghost danger" onClick={act(api.vet, p.id, 'reject')}>{L('Decline', 'अस्वीकृत')}</button>
                </div>
              </div>
            ))}
          </Card>
          <Card title={`${L('Bookings', 'बुकिंग')} (${d.bookings.length})`}>
            {!d.bookings.length ? <p className="pu-note">{L('No bookings yet.', 'अभी कोई बुकिंग नहीं।')}</p> : (
              <div className="dk-table-wrap">
                <table className="dk-table pu-desk">
                  <thead><tr><th>{L('When', 'कब')}</th><th>{L('Ceremony', 'अनुष्ठान')}</th><th>{L('Family', 'परिवार')}</th><th>{L('Status', 'स्थिति')}</th><th /></tr></thead>
                  <tbody>
                    {d.bookings.map((b) => {
                      const r = ritualByKey(b.ritual)
                      return (
                        <tr key={b.id}>
                          <td className="dk-num">{String(b.starts_at).replace('T', ' ')}<span className="dk-en"> {b.tz}</span></td>
                          <td>{r ? (r.name[lang] || r.name.en) : b.ritual}</td>
                          <td>{b.name}<span className="dk-en">{b.contact ? ` · ${b.contact}` : ''}{b.city ? ` · ${b.city}` : ''}</span>{b.notes && <div className="dk-en">{b.notes}</div>}</td>
                          <td><span className={`pu-status s-${b.status}`}>{b.status}</span>{b.priest_name && !b.mine && <span className="dk-en"> {b.priest_name}</span>}</td>
                          <td className="pu-desk-btns">
                            {b.status === 'requested' && <button type="button" className="go" onClick={act(api.accept, b.id)}>{L('Accept', 'स्वीकार')}</button>}
                            {b.status === 'confirmed' && <button type="button" className="pu-ghost" onClick={act(api.complete, b.id)}>{L('Completed', 'संपन्न')}</button>}
                            <a className="pu-ghost" href={`/pooja/b/${b.id}`} onClick={(e) => { e.preventDefault(); go(`/pooja/b/${b.id}`) }}>{L('Open', 'खोलें')}</a>
                          </td>
                        </tr>
                      )
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </Card>
          <VoiceStudio lang={lang} L={L} me={d} go={go} />
        </>
      )}
    </>
  )
}

export default function PoojaApp({ route, go, lang = 'en', setLang }) {
  const L = (en, hi) => (lang === 'hi' ? hi : en)
  const [path, qs] = useMemo(() => { const i = route.indexOf('?'); return i < 0 ? [route, ''] : [route.slice(0, i), route.slice(i + 1)] }, [route])
  const query = useMemo(() => new URLSearchParams(qs || (typeof location !== 'undefined' ? location.search : '')), [qs])
  const seg = path.split('/').filter(Boolean)          // pooja, ...
  const view = seg[1] || 'home'
  const nav = [['home', '/pooja', L('Home', 'मुख्य')], ['rituals', '/pooja/rituals', L('Ceremonies', 'अनुष्ठान')], ['calendar', '/pooja/calendar', L('Calendar', 'पंचांग')], ['pandits', '/pooja/pandits', L('Pandits', 'पंडित जी')]]
  const active = view === 'ritual' ? 'rituals' : view === 'join' ? 'pandits' : view
  useEffect(() => { document.title = `${L('Pūjā & Havan', 'पूजा एवं हवन')} — Devashaa` ; return () => { document.title = 'Devashaa — Vedic Birth Chart (Jyotiṣa)' } }, [lang])  // eslint-disable-line react-hooks/exhaustive-deps
  let body
  if (view === 'home') body = <Home lang={lang} L={L} go={go} />
  else if (view === 'rituals') body = <Rituals lang={lang} L={L} go={go} />
  else if (view === 'ritual' && seg[3] === 'guide') body = <GuidePage rkey={seg[2]} lang={lang} L={L} go={go} />
  else if (view === 'ritual') body = <RitualDetail key={seg[2]} rkey={seg[2]} lang={lang} L={L} go={go} query={query} />
  else if (view === 'calendar') body = <Calendar lang={lang} L={L} go={go} />
  else if (view === 'pandits') body = <Pandits L={L} go={go} />
  else if (view === 'join') body = <Join L={L} />
  else if (view === 'desk') body = <Desk lang={lang} L={L} go={go} />
  else if (view === 'b' && HEX32.test(seg[2] || '')) body = <BookingPage id={seg[2]} lang={lang} L={L} go={go} />
  else if (view === 'room' && HEX32.test(seg[2] || '')) body = <RoomGate id={seg[2]} lang={lang} L={L} go={go} />
  else body = <Card title={L('Not found', 'नहीं मिला')}><p><a href="/pooja" onClick={(e) => { e.preventDefault(); go('/pooja') }}>{L('Back to Pūjā & Havan', 'पूजा एवं हवन पर वापस')}</a></p></Card>
  return (
    <div className="page pu-page" lang={lang}>
      <header className="pu-top">
        <a className="pu-brand" href="/pooja" onClick={(e) => { e.preventDefault(); go('/pooja') }}>
          <span className="pu-brand-mark" aria-hidden="true">🪔</span>
          <span><b>devashaa</b><i>{L('Pūjā & Havan', 'पूजा एवं हवन')}</i></span>
        </a>
        <nav className="pu-nav" aria-label={L('Sections', 'अनुभाग')}>
          {nav.map(([k, p, label]) => <a key={k} className={active === k ? 'on' : ''} href={p} onClick={(e) => { e.preventDefault(); go(p) }}>{label}</a>)}
        </nav>
        <div className="pu-top-right">
          {setLang && (
            <span className="pu-lang">
              <button type="button" className={lang === 'en' ? 'on' : ''} onClick={() => setLang('en')}>EN</button>
              <button type="button" className={lang === 'hi' ? 'on' : ''} onClick={() => setLang('hi')}>हिं</button>
            </span>
          )}
          <a className="pu-back" href="/pooja/desk" onClick={(e) => { e.preventDefault(); go('/pooja/desk') }}>{L('For pandits', 'पंडित जी हेतु')}</a>
          <a className="pu-back" href="/" onClick={(e) => { e.preventDefault(); go('/') }}>{L('Jyotiṣa charts →', 'ज्योतिष कुंडली →')}</a>
        </div>
      </header>
      <main className="pu-main">{body}</main>
      <footer className="pu-foot">
        <p><b>{L('Practice your traditions, wherever your family lives.', 'अपनी परंपराएँ निभाइए — आपका परिवार जहाँ भी रहता हो।')}</b></p>
        <p>{L('Devashaa Pūjā & Havan — a separate service from the chart reference. Ceremonies are acts of devotion; nothing here is prescribed from a horoscope.', 'देवाशा पूजा एवं हवन — कुंडली-सन्दर्भ से अलग सेवा। अनुष्ठान भक्ति के कार्य हैं; यहाँ कुछ भी कुंडली देखकर नहीं बताया जाता।')}</p>
      </footer>
    </div>
  )
}
