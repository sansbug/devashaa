/**
 * The voice library — where a pandit's voice is recorded.
 *
 * The guided ceremony is voiced by people. Each mantra is recorded once
 * (Sanskrit), and — if he will — each explanation in English or in Hindi,
 * short or detailed. A family keeping a ceremony on its own then hears him:
 * the explanation, then the chant, with his name.
 *
 * WHO RECORDS. A pandit on the roster, at his own desk. And the admin, for a
 * pandit he knows who will never sign in to a website: the admin adds him as a
 * "voice" (a name, male or female — no account) and records him in person on
 * this device, or uploads an audio file he sent.
 *
 * One recording per voice per clip. Each take is heard before it is saved, and
 * can be replaced or removed. The take is cleaned up in the browser before it
 * is saved (see chantAudio.js): mono, the silence at both ends trimmed, every
 * voice at the same level.
 */
import { useEffect, useMemo, useRef, useState } from 'react'
import { api } from './papi.js'
import { RITUALS } from './rituals.js'
import { MANTRA_STEPS, ALL_STEPS, romanOf, narration, mantraClip, explainClip } from './guide.js'
import { toWav } from './chantAudio.js'

const MAX_SECONDS = 150
const mmss = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`

function Recorder({ item, forPid, who, L, onSaved, onClose }) {
  const [phase, setPhase] = useState('ready')     // ready | recording | working | review | saving
  const [secs, setSecs] = useState(0)
  const [take, setTake] = useState(null)           // { blob, url, seconds }
  const [err, setErr] = useState('')
  const rec = useRef(null)
  const stream = useRef(null)
  const tick = useRef(null)
  const raf = useRef(0)
  const actx = useRef(null)
  const meter = useRef(null)
  const box = useRef(null)
  const file = useRef(null)

  const release = () => {
    clearInterval(tick.current)
    cancelAnimationFrame(raf.current)
    try { stream.current && stream.current.getTracks().forEach((t) => t.stop()) } catch { /* stopped */ }
    try { actx.current && actx.current.close() } catch { /* closed */ }
    stream.current = null; actx.current = null
  }
  useEffect(() => { box.current && box.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' }) }, [item.id])
  useEffect(() => () => { try { rec.current && rec.current.state !== 'inactive' && rec.current.stop() } catch { /* stopped */ } release() }, [])
  useEffect(() => () => { if (take) URL.revokeObjectURL(take.url) }, [take])

  /** Whatever was recorded or uploaded → the cleaned take, ready to hear. */
  const prepare = async (blob) => {
    setPhase('working'); setErr('')
    try {
      const w = await toWav(blob)
      if (w.seconds > MAX_SECONDS + 5) throw new Error('long')
      setTake({ blob: w.blob, url: URL.createObjectURL(w.blob), seconds: w.seconds })
      setPhase('review')
    } catch (e) {
      setErr(e && e.message === 'silent'
        ? L('Nothing was heard in it — check the microphone, or the file, and try again.', 'उसमें कुछ सुनाई नहीं दिया — माइक या फ़ाइल जाँचकर फिर प्रयास करें।')
        : e && e.message === 'long'
          ? L('That is longer than two and a half minutes — one mantra, or one explanation, at a time.', 'यह ढाई मिनट से लंबा है — एक बार में एक मंत्र, या एक व्याख्या।')
          : L('That audio could not be read — try another take or another file (m4a, mp3, wav, ogg).', 'वह ऑडियो पढ़ा नहीं जा सका — दूसरी रिकॉर्डिंग या दूसरी फ़ाइल (m4a, mp3, wav, ogg) आज़माएँ।'))
      setPhase('ready')
    }
  }

  const start = async () => {
    setErr(''); setTake(null)
    try {
      // The browser's speech clean-up is tuned for talk and eats a held "Oṁ": leave the voice as it is.
      const s = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: false, noiseSuppression: false, autoGainControl: false, channelCount: 1 } })
      stream.current = s
      const mime = ['audio/webm;codecs=opus', 'audio/webm', 'audio/mp4'].find((m) => window.MediaRecorder && MediaRecorder.isTypeSupported(m))
      const r = new MediaRecorder(s, mime ? { mimeType: mime, audioBitsPerSecond: 128000 } : undefined)
      const parts = []
      r.ondataavailable = (e) => { if (e.data && e.data.size) parts.push(e.data) }
      r.onstop = () => { release(); prepare(new Blob(parts, { type: r.mimeType || 'audio/webm' })) }
      // a level bar, so he can see the microphone hears him
      const AC = window.AudioContext || window.webkitAudioContext
      const ctx = new AC()
      actx.current = ctx
      const an = ctx.createAnalyser()
      an.fftSize = 1024
      ctx.createMediaStreamSource(s).connect(an)
      const buf = new Float32Array(an.fftSize)
      const draw = () => {
        an.getFloatTimeDomainData(buf)
        let sum = 0
        for (let k = 0; k < buf.length; k++) sum += buf[k] * buf[k]
        if (meter.current) meter.current.style.width = `${Math.min(100, Math.round(Math.sqrt(sum / buf.length) * 420))}%`
        raf.current = requestAnimationFrame(draw)
      }
      draw()
      const t0 = Date.now()
      setSecs(0)
      tick.current = setInterval(() => {
        const el = (Date.now() - t0) / 1000
        setSecs(el)
        if (el >= MAX_SECONDS) { try { r.stop() } catch { /* stopped */ } }
      }, 250)
      r.start()
      rec.current = r
      setPhase('recording')
    } catch (e) {
      release()
      setErr(e && e.name === 'NotAllowedError'
        ? L('The browser was not allowed to use the microphone. Allow it for this site and try again — or upload a recording made on a phone.', 'ब्राउज़र को माइक की अनुमति नहीं मिली। इस साइट के लिए अनुमति देकर फिर प्रयास करें — या फ़ोन पर बनी रिकॉर्डिंग अपलोड करें।')
        : L('No microphone could be opened on this device — upload a recording instead.', 'इस उपकरण पर माइक नहीं खुल सका — इसके स्थान पर रिकॉर्डिंग अपलोड करें।'))
    }
  }
  const stop = () => { try { rec.current && rec.current.stop() } catch { /* stopped */ } }
  const save = async () => {
    setPhase('saving'); setErr('')
    try { await api.putChant(item.id, take.blob, forPid); onSaved() } catch (e) { setErr(e.message || String(e)); setPhase('review') }
  }
  const pickFile = (e) => {
    const f = e.target.files && e.target.files[0]
    e.target.value = ''
    if (f) { setTake(null); prepare(f) }
  }

  return (
    <section className="vs-rec" ref={box} aria-label={L('Recording', 'रिकॉर्डिंग')}>
      <header>
        <b>{item.title}</b>
        <span>{item.sa ? (item.tongue === 'awa' ? L('Awadhi — the verses', 'अवधी — छंद') : L('Sanskrit — the mantra', 'संस्कृत — मंत्र')) : item.kind}{who ? ` · ${L('voice', 'स्वर')}: ${who}` : ''}</span>
        <button type="button" className="vs-x" onClick={onClose} disabled={phase === 'recording' || phase === 'saving'} aria-label={L('Close', 'बंद करें')}>×</button>
      </header>
      <p className={`vs-text${item.sa ? ' sa' : ''}${item.sa && item.text.split('\n').length > 5 ? ' long' : ''}`} lang={item.sa ? item.tongue : item.lang}>{item.text}</p>
      {item.roman && <p className="vs-roman">{item.roman}</p>}
      <input ref={file} type="file" accept="audio/*,.m4a,.mp3,.wav,.ogg,.opus,.aac" hidden onChange={pickFile} />
      {phase === 'ready' && (
        <div className="vs-actions">
          <button type="button" className="go" onClick={start}>● {L('Record now', 'अभी रिकॉर्ड करें')}</button>
          <button type="button" className="pu-ghost" onClick={() => file.current && file.current.click()}>⬆ {L('Upload an audio file', 'ऑडियो फ़ाइल अपलोड करें')}</button>
          <span className="pu-note">{item.sa
            ? L('A quiet room; the microphone a hand’s width away. Chant it as you would lead a family through it. A voice note sent by phone can be uploaded as it is.', 'शांत कमरा; माइक एक बित्ता दूर। वैसे ही बोलें जैसे किसी परिवार से करा रहे हों। फ़ोन से भेजा गया वॉइस नोट जैसा है वैसा अपलोड हो सकता है।')
            : L('Read it as you would explain it to a family in front of you — the sense must stay the same.', 'वैसे पढ़ें जैसे सामने बैठे परिवार को समझा रहे हों — भाव वही रहे।')}</span>
        </div>
      )}
      {phase === 'recording' && (
        <div className="vs-actions">
          <span className="vs-live"><i /> {mmss(secs)}</span>
          <span className="vs-meter"><span ref={meter} /></span>
          <button type="button" className="go" onClick={stop}>■ {L('Stop', 'रोकें')}</button>
        </div>
      )}
      {phase === 'working' && <p className="pu-note">{L('preparing the take…', 'रिकॉर्डिंग तैयार हो रही है…')}</p>}
      {(phase === 'review' || phase === 'saving') && take && (
        <div className="vs-actions">
          <audio controls src={take.url} />
          <span className="pu-note">{mmss(take.seconds)} · {Math.round(take.blob.size / 1024)} KB</span>
          <button type="button" className="go" disabled={phase === 'saving'} onClick={save}>{phase === 'saving' ? L('saving…', 'सहेजा जा रहा है…') : L('Save this take', 'यह रिकॉर्डिंग सहेजें')}</button>
          <button type="button" className="pu-ghost" disabled={phase === 'saving'} onClick={start}>● {L('Record again', 'फिर रिकॉर्ड करें')}</button>
          <button type="button" className="pu-ghost" disabled={phase === 'saving'} onClick={() => file.current && file.current.click()}>⬆ {L('Another file', 'दूसरी फ़ाइल')}</button>
        </div>
      )}
      {(phase === 'review') && <p className="pu-note">{L('Listen before saving: this is exactly what a family will hear.', 'सहेजने से पहले सुन लें: परिवार ठीक यही सुनेगा।')}</p>}
      {err && <p className="pu-err">{err}</p>}
    </section>
  )
}

export default function VoiceStudio({ lang, L, me, go, reload }) {
  const priest = me && me.priest && me.priest.status === 'approved' ? me.priest : null
  const admin = !!(me && me.role === 'admin')
  const voices = (admin && me.voices) || []
  // Whose voice is being recorded: one's own, or — for the admin — a voice he keeps.
  const people = [
    ...(priest ? [{ id: priest.pid, name: `${priest.name} (${L('you', 'आप')})`, voice: priest.voice, self: true }] : []),
    ...voices,
  ]
  const [as, setAs] = useState('')
  const current = people.find((p) => p.id === as) || people[0] || null
  const [clips, setClips] = useState({})
  const [tab, setTab] = useState('m')            // m | en | hi
  const [depth, setDepth] = useState('short')
  const [active, setActive] = useState(null)
  const [err, setErr] = useState('')
  const [nv, setNv] = useState({ name: '', voice: '' })
  const [busy, setBusy] = useState(false)
  const load = () => api.chants().then(setClips)
  useEffect(() => { load() }, [])

  const items = useMemo(() => {
    if (tab === 'm') {
      return MANTRA_STEPS.map((s) => ({ id: mantraClip(s), sa: true, tongue: s.mantra.lang || 'sa', title: s.title[lang] || s.title.en, text: s.mantra.dev, roman: romanOf(s.mantra) }))
    }
    const kindP = tab === 'hi' ? 'उद्देश्य' : 'Purpose', kindS = tab === 'hi' ? 'चरण' : 'Step'
    return [
      ...RITUALS.map((r) => ({ id: explainClip(r, null, depth, tab), lang: tab, kind: kindP, title: r.name[tab] || r.name.en, text: narration(r, null, depth, tab) })),
      ...ALL_STEPS.map((s) => ({ id: explainClip(null, s, depth, tab), lang: tab, kind: kindS, title: s.title[tab] || s.title.en, text: narration(null, s, depth, tab) })),
    ]
  }, [tab, depth, lang])
  const has = (id) => !!(current && (clips[id] || []).some((c) => c.id === current.id))
  const done = items.filter((x) => has(x.id)).length

  const play = (id, c) => fetch(api.chantUrl(id, c.id, c.at)).then((r) => r.blob()).then((b) => new Audio(URL.createObjectURL(b)).play()).catch((e) => setErr(e.message || String(e)))
  const remove = async (id, c) => { setErr(''); try { await api.delChant(id, c.id); await load() } catch (e) { setErr(e.message || String(e)) } }
  const addVoice = async (e) => {
    e.preventDefault(); setErr(''); setBusy(true)
    try { const j = await api.addVoice(nv.name, nv.voice); setNv({ name: '', voice: '' }); if (reload) await reload(); setAs(j.id) } catch (e2) { setErr(e2.message || String(e2)) } finally { setBusy(false) }
  }
  const dropVoice = async (v) => {
    if (typeof window !== 'undefined' && !window.confirm(L(`Remove ${v.name} and every recording in that voice?`, `${v.name} और उस स्वर की हर रिकॉर्डिंग हटाएँ?`))) return
    setErr('')
    try { await api.delVoice(v.id); if (reload) await reload(); await load(); setAs('') } catch (e) { setErr(e.message || String(e)) }
  }
  const TABS = [['m', L('Mantras and verses', 'मंत्र और छंद')], ['en', L('Explanations — English', 'व्याख्या — अंग्रेज़ी')], ['hi', L('Explanations — Hindi', 'व्याख्या — हिन्दी')]]
  const sex = (v) => (v === 'f' ? L('female', 'स्त्री') : v === 'm' ? L('male', 'पुरुष') : '')

  return (
    <section className="dk-card pu-card vs">
      <h4 className="dk-head"><span>{L('The voice library', 'स्वर-संग्रह')}</span>{current && <span className="dk-head-right">{done} / {items.length} {L('recorded in this voice', 'इस स्वर में रिकॉर्ड')}</span>}</h4>
      <div className="dk-body">
        <p className="pu-lead">{L(
          'The guided ceremony is voiced by pandits, not by a machine. Each mantra is recorded once; a family keeping the ceremony on its own then hears it chanted, with the pandit’s name. The explanations can be recorded too, in English or Hindi.',
          'मार्गदर्शित अनुष्ठान पंडित जी की आवाज़ में है, मशीन की नहीं। हर मंत्र एक बार रिकॉर्ड होता है; जो परिवार स्वयं अनुष्ठान करता है, वह उसे पंडित जी के नाम के साथ सुनता है। व्याख्या भी रिकॉर्ड की जा सकती है — हिन्दी या अंग्रेज़ी में।')}</p>

        {admin && (
          <div className="vs-voices">
            <p className="vs-voices-h">{L('Voices you record for', 'जिन स्वरों के लिए आप रिकॉर्ड करते हैं')}</p>
            <p className="pu-note">{L(
              'For a pandit you know who will not sign in himself: add his name here, then record him in person on this device, or upload the audio he sends you. He needs no account, and he is not listed for booking.',
              'उन परिचित पंडित जी के लिए जो स्वयं साइन-इन नहीं करेंगे: उनका नाम यहाँ जोड़ें, फिर इसी उपकरण पर सामने बैठाकर रिकॉर्ड करें, या उनका भेजा ऑडियो अपलोड करें। उन्हें खाते की आवश्यकता नहीं, और वे बुकिंग सूची में नहीं आते।')}</p>
            {voices.length > 0 && (
              <ul className="vs-voice-list">
                {voices.map((v) => <li key={v.id}><b>{v.name}</b> <span className="dk-en">· {sex(v.voice)}</span> <button type="button" className="vs-del" onClick={() => dropVoice(v)}>{L('remove', 'हटाएँ')}</button></li>)}
              </ul>
            )}
            <form className="vs-addvoice" onSubmit={addVoice}>
              <input value={nv.name} onChange={(e) => setNv((x) => ({ ...x, name: e.target.value }))} placeholder={L('Name, as families should see it', 'नाम, जैसा परिवार देखें')} aria-label={L('Name', 'नाम')} />
              <select value={nv.voice} onChange={(e) => setNv((x) => ({ ...x, voice: e.target.value }))} aria-label={L('Voice', 'स्वर')}>
                <option value="">{L('voice…', 'स्वर…')}</option>
                <option value="m">{L('Male', 'पुरुष')}</option>
                <option value="f">{L('Female', 'स्त्री')}</option>
              </select>
              <button type="submit" className="pu-ghost" disabled={busy || nv.name.trim().length < 2 || !nv.voice}>+ {L('Add this voice', 'यह स्वर जोड़ें')}</button>
            </form>
          </div>
        )}

        {!current && <p className="pu-note">{admin
          ? L('Add a voice above to begin recording. You can also hear and remove any recording below.', 'रिकॉर्डिंग आरंभ करने के लिए ऊपर एक स्वर जोड़ें। नीचे की कोई भी रिकॉर्डिंग आप सुन और हटा सकते हैं।')
          : L('Recording opens once your application is approved.', 'आवेदन स्वीकृत होते ही रिकॉर्डिंग खुल जाएगी।')}</p>}
        {priest && !priest.voice && (
          <p className="pu-note vs-warn">{L('Your profile does not yet say whether your voice is male or female — families choose by it.', 'आपकी प्रोफ़ाइल में अभी नहीं लिखा कि आपकी आवाज़ पुरुष की है या स्त्री की — परिवार इसी से चुनते हैं।')} <a href="/pooja/join" onClick={(e) => { e.preventDefault(); go('/pooja/join') }}>{L('Set it in your profile →', 'प्रोफ़ाइल में भरें →')}</a></p>
        )}

        <div className="vs-bar">
          {people.length > 1 && (
            <label className="vs-as">{L('Recording as', 'किसका स्वर')}
              <select value={current ? current.id : ''} onChange={(e) => { setAs(e.target.value); setActive(null) }}>
                {people.map((p) => <option key={p.id} value={p.id}>{p.name}{p.voice ? ` — ${sex(p.voice)}` : ''}</option>)}
              </select></label>
          )}
          <div className="dt-view-btns pu-tabs">{TABS.map(([k, label]) => <button type="button" key={k} className={tab === k ? 'on' : ''} onClick={() => { setTab(k); setActive(null) }}>{label}</button>)}</div>
          {tab !== 'm' && (
            <span className="pg-seg" role="group" aria-label={L('Depth', 'गहराई')}>
              {[['short', L('Short', 'संक्षेप')], ['detailed', L('Detailed', 'विस्तार')]].map(([k, label]) => <button type="button" key={k} className={depth === k ? 'on' : ''} onClick={() => { setDepth(k); setActive(null) }}>{label}</button>)}
            </span>
          )}
        </div>
        {err && <p className="pu-err">{err}</p>}
        {active && current && (
          <Recorder key={`${active.id}|${current.id}`} item={active} forPid={current.self ? undefined : current.id} who={current.self ? '' : current.name} L={L}
                    onClose={() => setActive(null)} onSaved={async () => { setActive(null); await load() }} />
        )}
        <div className="dk-table-wrap">
          <table className="dk-table vs-table">
            <thead><tr><th>{tab === 'm' ? L('Mantra or verses', 'मंत्र या छंद') : L('To be read', 'पढ़ने हेतु')}</th><th>{L('Recorded by', 'किसने रिकॉर्ड किया')}</th><th /></tr></thead>
            <tbody>
              {items.map((x) => {
                const list = clips[x.id] || []
                return (
                  <tr key={x.id} className={active && active.id === x.id ? 'on' : ''}>
                    <td><b>{x.title}</b>{x.kind && <span className="dk-en"> · {x.kind}</span>}<div className={`vs-prev${x.sa ? ' sa' : ''}`} lang={x.sa ? 'sa' : x.lang}>{x.text}</div></td>
                    <td className="vs-by">
                      {list.length ? list.map((c) => (
                        <div key={c.id}>
                          <button type="button" className="vs-play" onClick={() => play(x.id, c)} aria-label={`${L('Hear', 'सुनें')} — ${c.by}`}>▶</button> {c.by}
                          <span className="dk-en">{sex(c.voice) ? ` · ${sex(c.voice)}` : ''}</span>
                          {(admin || (priest && c.id === priest.pid)) && <button type="button" className="vs-del" onClick={() => remove(x.id, c)}>{L('remove', 'हटाएँ')}</button>}
                        </div>
                      )) : <span className="dk-en">—</span>}
                    </td>
                    <td className="pu-desk-btns">
                      {current && <button type="button" className={has(x.id) ? 'pu-ghost' : 'go'} disabled={!!active} onClick={() => setActive(x)}>● {has(x.id) ? L('Record again', 'फिर रिकॉर्ड करें') : L('Record / upload', 'रिकॉर्ड / अपलोड')}</button>}
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
        <p className="pu-note">{L(
          'A recording belongs to the exact text it was read from. If a mantra or an explanation is ever corrected, its recording is set aside until it is read again.',
          'रिकॉर्डिंग ठीक उसी पाठ की है जिससे वह पढ़ी गई। यदि किसी मंत्र या व्याख्या में कभी सुधार होता है, तो उसकी रिकॉर्डिंग दोबारा पढ़े जाने तक अलग रख दी जाती है।')}</p>
      </div>
    </section>
  )
}
