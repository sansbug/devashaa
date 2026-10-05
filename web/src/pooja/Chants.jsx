/**
 * The voice library — where a pandit records.
 *
 * The guided ceremony is voiced by people. A pandit on the roster records each
 * mantra once (Sanskrit), and — if he will — each explanation in English or in
 * Hindi, short or detailed. A family keeping a ceremony on its own then hears
 * him: the explanation, then the chant, with his name.
 *
 * One recording per pandit per clip. He hears each take before it is saved,
 * and can replace or remove his own at any time; an admin can remove any.
 * The take is cleaned up in the browser before it is saved (see chantAudio.js):
 * mono, the silence at both ends trimmed, every pandit at the same level.
 */
import { useEffect, useMemo, useRef, useState } from 'react'
import { api } from './papi.js'
import { RITUALS } from './rituals.js'
import { MANTRA_STEPS, ALL_STEPS, plainRoman, narration, mantraClip, explainClip } from './guide.js'
import { toWav } from './chantAudio.js'

const MAX_SECONDS = 150
const mmss = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`

function Recorder({ item, L, onSaved, onClose }) {
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
      r.onstop = async () => {
        release()
        setPhase('working')
        try {
          const w = await toWav(new Blob(parts, { type: r.mimeType || 'audio/webm' }))
          setTake({ blob: w.blob, url: URL.createObjectURL(w.blob), seconds: w.seconds })
          setPhase('review')
        } catch (e) {
          setErr(e && e.message === 'silent'
            ? L('Nothing was heard in that take — check the microphone and try again.', 'उस रिकॉर्डिंग में कुछ सुनाई नहीं दिया — माइक जाँचकर फिर प्रयास करें।')
            : L('That take could not be read — try again.', 'वह रिकॉर्डिंग पढ़ी नहीं जा सकी — फिर प्रयास करें।'))
          setPhase('ready')
        }
      }
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
        ? L('The browser was not allowed to use the microphone. Allow it for this site and try again.', 'ब्राउज़र को माइक की अनुमति नहीं मिली। इस साइट के लिए अनुमति देकर फिर प्रयास करें।')
        : L('No microphone could be opened on this device.', 'इस उपकरण पर माइक नहीं खुल सका।'))
    }
  }
  const stop = () => { try { rec.current && rec.current.stop() } catch { /* stopped */ } }
  const save = async () => {
    setPhase('saving'); setErr('')
    try { await api.putChant(item.id, take.blob); onSaved() } catch (e) { setErr(e.message || String(e)); setPhase('review') }
  }

  return (
    <section className="vs-rec" ref={box} aria-label={L('Recording', 'रिकॉर्डिंग')}>
      <header>
        <b>{item.title}</b>
        <span>{item.sa ? L('Sanskrit — the mantra', 'संस्कृत — मंत्र') : item.kind}</span>
        <button type="button" className="vs-x" onClick={onClose} disabled={phase === 'recording' || phase === 'saving'} aria-label={L('Close', 'बंद करें')}>×</button>
      </header>
      <p className={`vs-text${item.sa ? ' sa' : ''}`} lang={item.sa ? 'sa' : item.lang}>{item.text}</p>
      {item.roman && <p className="vs-roman">{item.roman}</p>}
      {phase === 'ready' && (
        <div className="vs-actions">
          <button type="button" className="go" onClick={start}>● {L('Start recording', 'रिकॉर्डिंग आरंभ करें')}</button>
          <span className="pu-note">{item.sa
            ? L('A quiet room; the microphone a hand’s width away. Chant it as you would lead a family through it.', 'शांत कमरा; माइक एक बित्ता दूर। वैसे ही बोलें जैसे किसी परिवार से करा रहे हों।')
            : L('Read it as you would explain it to a family in front of you — your own words of greeting are welcome, the sense must stay the same.', 'वैसे पढ़ें जैसे सामने बैठे परिवार को समझा रहे हों — अभिवादन के अपने शब्द जोड़ सकते हैं, भाव वही रहे।')}</span>
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
        </div>
      )}
      {(phase === 'review') && <p className="pu-note">{L('Listen before saving: this is exactly what a family will hear.', 'सहेजने से पहले सुन लें: परिवार ठीक यही सुनेगा।')}</p>}
      {err && <p className="pu-err">{err}</p>}
    </section>
  )
}

export default function VoiceStudio({ lang, L, me, go }) {
  const priest = me && me.priest && me.priest.status === 'approved' ? me.priest : null
  const admin = !!(me && me.role === 'admin')
  const [clips, setClips] = useState({})
  const [tab, setTab] = useState('m')            // m | en | hi
  const [depth, setDepth] = useState('short')
  const [active, setActive] = useState(null)
  const [err, setErr] = useState('')
  const load = () => api.chants().then(setClips)
  useEffect(() => { load() }, [])

  const items = useMemo(() => {
    if (tab === 'm') {
      return MANTRA_STEPS.map((s) => ({ id: mantraClip(s), sa: true, title: s.title[lang] || s.title.en, text: s.mantra.dev, roman: plainRoman(s.mantra.iast) }))
    }
    const kindP = tab === 'hi' ? 'उद्देश्य' : 'Purpose', kindS = tab === 'hi' ? 'चरण' : 'Step'
    return [
      ...RITUALS.map((r) => ({ id: explainClip(r, null, depth, tab), lang: tab, kind: kindP, title: r.name[tab] || r.name.en, text: narration(r, null, depth, tab) })),
      ...ALL_STEPS.map((s) => ({ id: explainClip(null, s, depth, tab), lang: tab, kind: kindS, title: s.title[tab] || s.title.en, text: narration(null, s, depth, tab) })),
    ]
  }, [tab, depth, lang])
  const mine = (id) => !!(priest && (clips[id] || []).some((c) => c.id === priest.pid))
  const done = items.filter((x) => mine(x.id)).length

  const play = (id, c) => fetch(api.chantUrl(id, c.id, c.at)).then((r) => r.blob()).then((b) => new Audio(URL.createObjectURL(b)).play()).catch((e) => setErr(e.message || String(e)))
  const remove = async (id, c) => { setErr(''); try { await api.delChant(id, c.id); await load() } catch (e) { setErr(e.message || String(e)) } }
  const TABS = [['m', L('Mantras (Sanskrit)', 'मंत्र (संस्कृत)')], ['en', L('Explanations — English', 'व्याख्या — अंग्रेज़ी')], ['hi', L('Explanations — Hindi', 'व्याख्या — हिन्दी')]]

  return (
    <section className="dk-card pu-card vs">
      <h4 className="dk-head"><span>{L('The voice library', 'स्वर-संग्रह')}</span>{priest && <span className="dk-head-right">{done} / {items.length} {L('recorded by you here', 'यहाँ आपने रिकॉर्ड किए')}</span>}</h4>
      <div className="dk-body">
        <p className="pu-lead">{L(
          'The guided ceremony is voiced by pandits, not by a machine. Record each mantra once in your own voice; a family keeping the ceremony on its own then hears you chant it, with your name. The explanations can be recorded too, in English or Hindi.',
          'मार्गदर्शित अनुष्ठान पंडित जी की आवाज़ में है, मशीन की नहीं। हर मंत्र एक बार अपनी आवाज़ में रिकॉर्ड कीजिए; जो परिवार स्वयं अनुष्ठान करता है, वह आपका मंत्रोच्चार, आपके नाम के साथ, सुनता है। व्याख्या भी रिकॉर्ड की जा सकती है — हिन्दी या अंग्रेज़ी में।')}</p>
        {!priest && <p className="pu-note">{admin
          ? L('You are the admin: you can hear every recording and remove any. Recording is done by the pandits of the roster, signed in to their own desk.', 'आप एडमिन हैं: हर रिकॉर्डिंग सुन और हटा सकते हैं। रिकॉर्डिंग सूची के पंडित जी अपनी डेस्क से करते हैं।')
          : L('Recording opens once your application is approved.', 'आवेदन स्वीकृत होते ही रिकॉर्डिंग खुल जाएगी।')}</p>}
        {priest && !priest.voice && (
          <p className="pu-note vs-warn">{L('Your profile does not yet say whether your voice is male or female — families choose by it.', 'आपकी प्रोफ़ाइल में अभी नहीं लिखा कि आपकी आवाज़ पुरुष की है या स्त्री की — परिवार इसी से चुनते हैं।')} <a href="/pooja/join" onClick={(e) => { e.preventDefault(); go('/pooja/join') }}>{L('Set it in your profile →', 'प्रोफ़ाइल में भरें →')}</a></p>
        )}
        <div className="vs-bar">
          <div className="dt-view-btns pu-tabs">{TABS.map(([k, label]) => <button type="button" key={k} className={tab === k ? 'on' : ''} onClick={() => { setTab(k); setActive(null) }}>{label}</button>)}</div>
          {tab !== 'm' && (
            <span className="pg-seg" role="group" aria-label={L('Depth', 'गहराई')}>
              {[['short', L('Short', 'संक्षेप')], ['detailed', L('Detailed', 'विस्तार')]].map(([k, label]) => <button type="button" key={k} className={depth === k ? 'on' : ''} onClick={() => { setDepth(k); setActive(null) }}>{label}</button>)}
            </span>
          )}
        </div>
        {err && <p className="pu-err">{err}</p>}
        {active && <Recorder key={active.id} item={active} L={L} onClose={() => setActive(null)} onSaved={async () => { setActive(null); await load() }} />}
        <div className="dk-table-wrap">
          <table className="dk-table vs-table">
            <thead><tr><th>{tab === 'm' ? L('Mantra', 'मंत्र') : L('To be read', 'पढ़ने हेतु')}</th><th>{L('Recorded by', 'किसने रिकॉर्ड किया')}</th><th /></tr></thead>
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
                          <span className="dk-en">{c.voice === 'f' ? ` · ${L('female', 'स्त्री')}` : c.voice === 'm' ? ` · ${L('male', 'पुरुष')}` : ''}</span>
                          {(admin || (priest && c.id === priest.pid)) && <button type="button" className="vs-del" onClick={() => remove(x.id, c)}>{L('remove', 'हटाएँ')}</button>}
                        </div>
                      )) : <span className="dk-en">—</span>}
                    </td>
                    <td className="pu-desk-btns">
                      {priest && <button type="button" className={mine(x.id) ? 'pu-ghost' : 'go'} disabled={!!active} onClick={() => setActive(x)}>● {mine(x.id) ? L('Record again', 'फिर रिकॉर्ड करें') : L('Record', 'रिकॉर्ड करें')}</button>}
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
