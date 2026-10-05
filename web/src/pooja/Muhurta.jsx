/**
 * Choosing the day and the hour — the muhūrta for one ceremony at one place.
 *
 * Everything here is computed for the family's own city from its sunrise and
 * sunset (api/muhurta.py): the five limbs of the day, the kāla this ceremony
 * is traditionally kept in and why, the clear windows (tap one to take it),
 * the three spans the almanac avoids, and the day's cautions. Whatever time
 * is chosen is then read back against all of it, so the reason is on screen.
 * Almanac practice — never a judgement from anyone's horoscope.
 */
import { useEffect, useState } from 'react'
import { api, loadPlace, savePlace } from './papi.js'

const mins = (hhmm) => { const [h, m] = String(hhmm).split(':'); return (+h) * 60 + (+m) }
const inside = (t, w) => w && !w.next_day && mins(t) >= mins(w.start) && mins(t) < mins(w.end)
export const todayIso = () => { const d = new Date(), p = (n) => String(n).padStart(2, '0'); return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}` }

/**
 * The place everything is computed for. A city the family chose is kept; until
 * they choose one, it is wherever the browser is — the city its address
 * resolves to at the edge, asked once per visit and stored nowhere but here.
 */
export function usePlace() {
  const [place, set] = useState(loadPlace)
  useEffect(() => {
    if (place.chosen) return undefined
    let dead = false
    api.where().then((w) => {
      if (dead || !w || !Number.isFinite(w.latitude) || !Number.isFinite(w.longitude) || !w.timezone) return
      const p = { name: w.name, latitude: w.latitude, longitude: w.longitude, timezone: w.timezone, auto: true }
      savePlace(p); set(p)
    })
    return () => { dead = true }
  }, [])  // eslint-disable-line react-hooks/exhaustive-deps
  const setPlace = (p) => { const q = { name: p.name, latitude: p.latitude, longitude: p.longitude, timezone: p.timezone, chosen: true }; savePlace(q); set(q) }
  return [place, setPlace]
}

/** One small line: the city in use, and a way to choose another. */
export function PlacePicker({ place, setPlace, L }) {
  const [open, setOpen] = useState(false)
  const [q, setQ] = useState('')
  const [hits, setHits] = useState([])
  const [note, setNote] = useState('')
  useEffect(() => {
    if (q.trim().length < 2) { setHits([]); return undefined }
    const h = setTimeout(() => api.places(q).then(setHits).catch(() => setHits([])), 200)
    return () => clearTimeout(h)
  }, [q])
  const close = () => { setOpen(false); setQ(''); setHits([]); setNote('') }
  const exact = () => {
    if (!navigator.geolocation) { setNote(L('This browser cannot give its location.', 'यह ब्राउज़र स्थान नहीं बता सकता।')); return }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        let tz = place.timezone
        try { tz = Intl.DateTimeFormat().resolvedOptions().timeZone || tz } catch { /* keep the one in use */ }
        setPlace({ name: L('My location', 'मेरा स्थान'), latitude: +pos.coords.latitude.toFixed(4), longitude: +pos.coords.longitude.toFixed(4), timezone: tz })
        close()
      },
      () => setNote(L('The browser did not share its location — choose a city instead.', 'ब्राउज़र ने स्थान साझा नहीं किया — शहर चुन लें।')),
      { maximumAge: 600000, timeout: 10000 },
    )
  }
  return (
    <div className={`pu-place${open ? ' open' : ''}`}>
      <span className="pu-place-cur"><span aria-hidden="true">📍</span> <b>{place.name.split(',')[0]}</b></span>
      {!open
        ? <button type="button" className="pu-link" onClick={() => setOpen(true)}>{L('choose city', 'शहर चुनें')}</button>
        : (
          <>
            <input autoFocus value={q} onChange={(e) => setQ(e.target.value)} placeholder={L('type a city…', 'शहर लिखें…')} aria-label={L('City', 'शहर')} onKeyDown={(e) => e.key === 'Escape' && close()} />
            <button type="button" className="pu-link" onClick={exact}>{L('use my exact location', 'मेरा सटीक स्थान')}</button>
            <button type="button" className="pu-link" onClick={close} aria-label={L('Close', 'बंद करें')}>×</button>
            {note && <span className="pu-place-note">{note}</span>}
            {hits.length > 0 && (
              <ul className="hits">
                {hits.slice(0, 6).map((p, i) => (
                  <li key={i}><button type="button" onClick={() => { setPlace(p); close() }}><strong>{p.name.split(',')[0]}</strong><span>{p.name.split(',').slice(1).join(',').trim()}</span></button></li>
                ))}
              </ul>
            )}
          </>
        )}
    </div>
  )
}

export default function Muhurta({ ritual, place, setPlace, date, setDate, time, setTime, lang, L }) {
  const [m, setM] = useState(null)
  const [err, setErr] = useState('')
  const hi = lang === 'hi'
  const N = (o, k = 'name') => (o ? (hi ? (o[`${k}_hi`] || o[k]) : o[k]) : '')
  useEffect(() => {
    if (!date) { setM(null); return undefined }
    let dead = false
    setM(null); setErr('')
    api.muhurta(place, date, ritual.key).then((j) => { if (!dead) setM(j) }).catch((e) => { if (!dead) setErr(e.message || String(e)) })
    return () => { dead = true }
  }, [place.latitude, place.longitude, place.timezone, date, ritual.key])

  const Win = ({ w, label, star }) => (
    <button type="button" className={`pm-win${time && inside(time, w) ? ' on' : ''}${w.quality === 1 ? ' good' : ''}`} onClick={() => setTime(w.start)} aria-pressed={!!(time && inside(time, w))}>
      <b>{w.start}–{w.end}</b>{label && <span>{label}</span>}{star && <i>★ {L('Abhijit', 'अभिजित्')}</i>}
    </button>
  )

  // The tithi named is the one at sunrise; say when it gives way, if that is today.
  const tEnd = m && String(m.panchang.tithi.end || '')
  const tithiEnds = tEnd && tEnd.slice(0, 10) === m.date ? tEnd.slice(11, 16) : ''

  // Read the chosen time back against the day.
  let verdict = null
  if (m && time) {
    const bad = m.avoid.find((a) => inside(time, a))
    const clear = m.clear.find((c) => inside(time, c))
    const pref = m.preferred && inside(time, m.preferred)
    const chog = [...m.choghadiya.day, ...m.choghadiya.night].find((c) => inside(time, c))
    if (bad) verdict = { cls: 'bad', text: L(`${time} falls in ${bad.name} (${bad.start}–${bad.end}), which the almanac avoids for beginning a ceremony.`, `${time} ${bad.name_hi} (${bad.start}–${bad.end}) में पड़ता है, जिसे पंचांग अनुष्ठान के आरंभ के लिए टालता है।`) }
    else if (pref) verdict = { cls: 'good', text: L(`${time} is within ${m.preferred.name} — the kāla this ceremony is traditionally kept in.`, `${time} ${m.preferred.name_hi} के भीतर है — जिस काल में यह अनुष्ठान परंपरा से किया जाता है।`) }
    else if (clear) verdict = { cls: 'good', text: L(`${time} is in a clear window — ${clear.choghadiya} choghaḍiyā${clear.abhijit ? ', touching Abhijit muhūrta' : ''}, outside rāhu kāla, yama-gaṇḍa and gulika.`, `${time} शुद्ध अवधि में है — ${clear.choghadiya_hi} चौघड़िया${clear.abhijit ? ', अभिजित् मुहूर्त को छूता हुआ' : ''}; राहु काल, यमगण्ड और गुलिक से बाहर।`) }
    else if (chog && chog.quality < 0) verdict = { cls: 'warn', text: L(`${time} is in ${chog.name} choghaḍiyā, which the almanac counts as harsh.`, `${time} ${chog.name_hi} चौघड़िया में है, जिसे पंचांग कठोर मानता है।`) }
    else verdict = { cls: 'plain', text: L(`${time} is outside the three avoided spans, but not in one of the day’s clear windows.`, `${time} तीनों वर्जित कालों से बाहर है, पर दिन की शुद्ध अवधियों में नहीं।`) }
  }

  return (
    <div className="pm">
      <div className="pm-pick">
        <PlacePicker place={place} setPlace={setPlace} L={L} />
        <label>{L('Date', 'दिनांक')}<input type="date" min={todayIso()} value={date} onChange={(e) => setDate(e.target.value)} /></label>
        <label>{L('Time', 'समय')}<input type="time" value={time} onChange={(e) => setTime(e.target.value)} /></label>
      </div>
      {!date && <p className="pu-note">{L('Choose a date to see its muhūrta — the hours the almanac favours and avoids, computed for your city.', 'मुहूर्त देखने के लिए दिनांक चुनें — पंचांग जिन घड़ियों को शुभ और वर्जित मानता है, आपके शहर के लिए गणना सहित।')}</p>}
      {err && <p className="pu-err">{err}</p>}
      {date && !m && !err && <p className="pu-note">{L('computing the muhūrta…', 'मुहूर्त की गणना हो रही है…')}</p>}
      {m && (
        <>
          <div className="dk-table-wrap">
            <table className="dk-table pm-table">
              <tbody>
                <tr>
                  <th>{L('The day', 'दिन')}</th>
                  <td>
                    <b>{N(m.panchang.vara)}</b> · {N(m.masa)}{m.masa.purnimanta && <span className="dk-en"> ({L('amānta', 'अमान्त')}; {hi ? m.masa.purnimanta_hi : m.masa.purnimanta} {L('by pūrṇimānta', 'पूर्णिमान्त से')})</span>} · {N(m.panchang.tithi)} <span className="dk-en">({m.panchang.tithi.paksha === 'śukla' ? L('śukla', 'शुक्ल') : L('kṛṣṇa', 'कृष्ण')}{tithiEnds ? `, ${L('until', 'समाप्ति')} ${tithiEnds}` : ''})</span> · {N(m.panchang.nakshatra)}
                    <span className="dk-en"> · {L('sunrise', 'सूर्योदय')} {m.sunrise} · {L('sunset', 'सूर्यास्त')} {m.sunset}</span>
                    {m.festivals && m.festivals.length > 0 && <div className="pm-fests">{m.festivals.map((f) => <span key={f.key} className={`pu-fest ${f.importance}`}><b>{hi ? (f.name_hi || f.name) : f.name}</b></span>)}</div>}
                  </td>
                </tr>
                {m.preferred && (
                  <tr className="pm-pref">
                    <th>{L('Kept in', 'किस काल में')}</th>
                    <td>
                      <b>{N(m.preferred)}</b> <span className="dk-num">{m.preferred.start}–{m.preferred.end}</span>
                      <div className="pm-why">{hi ? m.preferred.why_hi : m.preferred.why}</div>
                      <div className="pm-wins">
                        {m.preferred.clear_within.length
                          ? m.preferred.clear_within.map((w, k) => <Win key={k} w={w} label={w.choghadiya ? (hi ? w.choghadiya_hi : w.choghadiya) : N(m.preferred)} star={w.abhijit} />)
                          : <span className="dk-en">{L('No clear window falls inside it on this day — the whole kāla is shown above; your pandit decides.', 'इस दिन इसके भीतर कोई शुद्ध अवधि नहीं — पूरा काल ऊपर दिया है; निर्णय पंडित जी का।')}</span>}
                      </div>
                    </td>
                  </tr>
                )}
                <tr>
                  <th>{L('Clear windows', 'शुद्ध अवधियाँ')}</th>
                  <td>
                    <div className="pm-wins">
                      {m.clear.length ? m.clear.map((w, k) => <Win key={k} w={w} label={hi ? w.choghadiya_hi : w.choghadiya} star={w.abhijit} />) : <span className="dk-en">—</span>}
                    </div>
                    <div className="pm-why">{L('Tap a window to take its start. These are the good and fair choghaḍiyās of the day, with the avoided spans cut out.', 'किसी अवधि को छूकर उसका आरंभ-समय लें। ये दिन के शुभ और सामान्य चौघड़िये हैं, वर्जित कालों को हटाकर।')}</div>
                  </td>
                </tr>
                <tr className="pm-avoid">
                  <th>{L('Avoided', 'वर्जित')}</th>
                  <td>{m.avoid.map((a) => <span key={a.key} className={`pm-av${time && inside(time, a) ? ' hit' : ''}`}><b>{N(a)}</b> {a.start}–{a.end}</span>)}</td>
                </tr>
                {m.cautions.length > 0 && (
                  <tr className={`pm-caut${m.cautions_apply ? ' apply' : ''}`}>
                    <th>{L('The day itself', 'दिन की बात')}</th>
                    <td>
                      {m.cautions.map((c) => <div key={c.key}>{hi ? c.text_hi : c.text}</div>)}
                      <div className="pm-why">{m.cautions_apply
                        ? L('This ceremony is a beginning, so these apply — consider another day, or ask your pandit.', 'यह अनुष्ठान एक शुभारंभ है, अतः ये लागू होते हैं — दूसरा दिन देखें, या पंडित जी से पूछें।')
                        : L('These are cautions for beginning something new; they are not held against this ceremony.', 'ये नए आरंभ के लिए सावधानियाँ हैं; इस अनुष्ठान पर लागू नहीं मानी जातीं।')}</div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
          {verdict && <p className={`pm-verdict ${verdict.cls}`}>{verdict.text}</p>}
          <p className="pu-note">{L(
            `Times are local to ${place.name.split(',')[0]} (${m.timezone}). Almanac practice, computed from that city’s sunrise and sunset — not read from anyone’s horoscope. Where a pandit leads, he confirms the hour.`,
            `समय ${place.name.split(',')[0]} (${m.timezone}) के स्थानीय हैं। पंचांग-परंपरा, उस शहर के सूर्योदय और सूर्यास्त से गणित — किसी की कुंडली से नहीं। जहाँ पंडित जी करा रहे हों, समय की पुष्टि वे करते हैं।`)}</p>
        </>
      )}
    </div>
  )
}
