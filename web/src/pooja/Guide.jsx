/**
 * The guided ceremony — purpose first, then the chanting, one step at a time.
 *
 * Each step shows the mantra as chanted (Devanāgarī, and a plain roman reading
 * to say it from), then WHAT IS HAPPENING and WHY. Three depths of explanation:
 * detailed, short, or the mantras alone. The explanation is read in the
 * language the family chooses.
 *
 * WHO CHANTS.
 *   Live      — the pandit, in the room. He moves everyone's screen to the step
 *               he is on; this panel then only explains (aloud too, if asked —
 *               for someone on headphones who wants it in another language).
 *   Guided    — on your own. The explanation is read by the device's voice.
 *               For the mantra itself: a pandit's recorded chant where the
 *               roster has recorded one; otherwise the device voice reads it
 *               slowly, AS AN AID TO PRONUNCIATION — it is not a chant, and
 *               the panel says so.
 */
import { useEffect, useMemo, useRef, useState } from 'react'
import { ABOUT, MODES, VOICE_LANGS, scriptFor, explain, plainRoman } from './guide.js'
import { api } from './papi.js'

const PREFS = 'pooja.guide'
const loadPrefs = () => { try { return JSON.parse(localStorage.getItem(PREFS)) || {} } catch { return {} } }
const savePrefs = (p) => { try { localStorage.setItem(PREFS, JSON.stringify(p)) } catch { /* private mode */ } }
const synth = () => (typeof window !== 'undefined' && 'speechSynthesis' in window ? window.speechSynthesis : null)
const wait = (ms) => new Promise((r) => setTimeout(r, ms))

function useVoices() {
  const [v, setV] = useState([])
  useEffect(() => {
    const s = synth()
    if (!s) return undefined
    const read = () => setV(s.getVoices() || [])
    read()
    s.addEventListener && s.addEventListener('voiceschanged', read)
    return () => { s.removeEventListener && s.removeEventListener('voiceschanged', read) }
  }, [])
  return v
}
/** The best voice a device has for one of these language tags — a natural one if there is one. */
function voiceFor(voices, tags) {
  for (const tag of tags) {
    const hits = voices.filter((v) => (v.lang || '').replace('_', '-').toLowerCase().startsWith(tag.toLowerCase()))
    if (hits.length) return hits.find((v) => /natural|neural|google/i.test(v.name)) || hits[0]
  }
  return null
}
const sentences = (text) => (String(text).match(/[^.!?।॥\n]+[.!?।॥]*/g) || []).map((x) => x.replace(/[।॥]+/g, '').trim()).filter(Boolean)

let chantsCache = null
function useChants() {
  const [c, setC] = useState(chantsCache || {})
  useEffect(() => { if (!chantsCache) api.chants().then((j) => { chantsCache = j; setC(j) }) }, [])
  return c
}

export default function Guide({ ritual, lang = 'en', L, live = false, canLead = true, remote = null, onStep, className = '' }) {
  const steps = useMemo(() => scriptFor(ritual.key), [ritual.key])
  const total = steps.length + 1                 // step 0 is the purpose
  const prefs = useMemo(loadPrefs, [])
  const [mode, setMode] = useState(MODES.some((m) => m.key === prefs.mode) ? prefs.mode : 'short')
  const [glang, setGlang] = useState(VOICE_LANGS.some((v) => v.key === prefs.glang) ? prefs.glang : (lang === 'hi' ? 'hi' : 'en'))
  const [auto, setAuto] = useState(!!prefs.auto)
  const [voice, setVoice] = useState(false)      // read aloud — always starts off; a tap turns it on
  const [i, setI] = useState(0)
  const [speaking, setSpeaking] = useState('')   // '' | 'explain' | 'mantra' | 'chant'
  const run = useRef(0)
  const audio = useRef(null)
  const voices = useVoices()
  const chants = useChants()
  const exVoice = useMemo(() => voiceFor(voices, VOICE_LANGS.find((v) => v.key === glang).bcp), [voices, glang])
  const mantraVoice = useMemo(() => voiceFor(voices, ['sa', 'hi-IN', 'hi']), [voices])
  const G = (o) => (o ? (o[glang] || o.en) : '')
  const T = (en, hi) => (glang === 'hi' ? hi : en)

  useEffect(() => { savePrefs({ mode, glang, auto }) }, [mode, glang, auto])
  // The pandit moved on: follow him.
  useEffect(() => { if (remote != null && remote >= 0 && remote < total) setI(remote) }, [remote, total])

  const hush = () => {
    run.current += 1
    const s = synth()
    try { s && s.cancel() } catch { /* nothing speaking */ }
    try { audio.current && audio.current.pause() } catch { /* nothing playing */ }
    audio.current = null
    setSpeaking('')
  }
  const move = (k) => {
    const n = Math.max(0, Math.min(total - 1, k))
    setI(n)
    if (live && canLead && onStep) onStep(n)
  }

  const step = i > 0 ? steps[i - 1] : null
  const purpose = mode === 'detailed' ? G(ABOUT[ritual.key]) || G(ritual.purpose) : G(ritual.purpose)
  const parts = step ? explain(step, mode, glang) : []
  const chant = step && step.mantra && chants[step.id] ? chants[step.id] : null

  // Read the step aloud whenever the voice is on and the step, depth or language changes.
  useEffect(() => {
    if (!voice) return undefined
    const token = ++run.current
    const alive = () => run.current === token
    const s = synth()
    const say = async (text, v, rate, what) => {
      if (!s || !v || !text) return
      setSpeaking(what)
      for (const chunk of sentences(text)) {
        if (!alive()) return
        await new Promise((res) => {
          const u = new SpeechSynthesisUtterance(chunk)
          u.voice = v; u.lang = v.lang; u.rate = rate
          u.onend = res; u.onerror = res
          s.speak(u)
        })
      }
    }
    const playChant = async (id) => {
      setSpeaking('chant')
      try {
        const blob = await fetch(api.chantUrl(id)).then((r) => (r.ok ? r.blob() : null))
        if (!blob || !alive()) return false
        const a = new Audio(URL.createObjectURL(blob))
        audio.current = a
        await new Promise((res) => { a.onended = res; a.onerror = res; a.onpause = res; a.play().catch(res) })
        return true
      } catch { return false }
    }
    ;(async () => {
      await wait(250)
      if (!alive()) return
      if (!step) {
        if (mode !== 'none') await say(`${T('The purpose of this ceremony', 'इस अनुष्ठान का उद्देश्य')}. ${purpose}`, exVoice, 0.95, 'explain')
      } else {
        if (mode !== 'none') await say(`${G(step.title)}. ${parts.map((p) => `${p.label}: ${p.text}`).join(' ')}`, exVoice, 0.95, 'explain')
        if (alive() && !live && step.mantra) {
          const played = chant ? await playChant(step.id) : false
          if (alive() && !played) await say(step.mantra.dev, mantraVoice, 0.78, 'mantra')
        }
      }
      if (!alive()) return
      setSpeaking('')
      if (auto && !live && i < total - 1) { await wait(1800); if (alive()) setI(i + 1) }
    })()
    return () => { run.current += 1; try { s && s.cancel() } catch { /* idle */ } try { audio.current && audio.current.pause() } catch { /* idle */ } }
  }, [voice, i, mode, glang, exVoice, mantraVoice, chant])  // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => () => hush(), [])  // eslint-disable-line react-hooks/exhaustive-deps

  const canSpeak = !!synth()
  const behind = live && !canLead && remote != null && remote !== i

  return (
    <div className={`pg${live ? ' live' : ''} ${className}`} lang={glang}>
      <div className="pg-bar">
        <div className="pg-set">
          <span className="pg-set-l">{L('Explanation', 'व्याख्या')}</span>
          <span className="pg-seg" role="group" aria-label={L('Depth of explanation', 'व्याख्या की गहराई')}>
            {MODES.map((m) => <button type="button" key={m.key} className={mode === m.key ? 'on' : ''} aria-pressed={mode === m.key} onClick={() => setMode(m.key)}>{lang === 'hi' ? m.hi : m.en}</button>)}
          </span>
        </div>
        <div className="pg-set">
          <span className="pg-set-l">{L('Explain in', 'व्याख्या की भाषा')}</span>
          <span className="pg-seg" role="group" aria-label={L('Language of the explanation', 'व्याख्या की भाषा')}>
            {VOICE_LANGS.map((v) => <button type="button" key={v.key} className={glang === v.key ? 'on' : ''} aria-pressed={glang === v.key} onClick={() => setGlang(v.key)}>{v.label}</button>)}
          </span>
        </div>
        {canSpeak && (
          <div className="pg-set pg-voice">
            <button type="button" className={`pg-play${voice ? ' on' : ''}`} aria-pressed={voice} onClick={() => { if (voice) { hush(); setVoice(false) } else setVoice(true) }}>
              {voice ? `❚❚ ${L('Voice off', 'आवाज़ बंद')}` : live ? `🔊 ${L('Read the explanation to me', 'व्याख्या पढ़कर सुनाएँ')}` : `▶ ${L('Guide me by voice', 'आवाज़ से मार्गदर्शन')}`}
            </button>
            {!live && <label className="pg-auto"><input type="checkbox" checked={auto} onChange={(e) => setAuto(e.target.checked)} /> {L('move on by itself', 'स्वयं आगे बढ़े')}</label>}
          </div>
        )}
      </div>
      {voice && !exVoice && mode !== 'none' && <p className="pu-note pg-warn">{L('This device has no voice for that language — the explanation is shown, not read.', 'इस उपकरण में उस भाषा की आवाज़ नहीं है — व्याख्या दिखाई जा रही है, पढ़ी नहीं जा रही।')}</p>}
      {voice && live && <p className="pu-note pg-warn">{L('Use headphones, so the voice does not carry into the room. Only the explanation is read — the pandit chants.', 'हेडफ़ोन लगाएँ, ताकि आवाज़ कक्ष में न जाए। केवल व्याख्या पढ़ी जाती है — मंत्रोच्चार पंडित जी करते हैं।')}</p>}

      <ol className="pg-rail" aria-label={L('The steps', 'चरण')}>
        {Array.from({ length: total }, (_, k) => {
          const st = k > 0 ? steps[k - 1] : null
          const label = st ? G(st.title) : T('Purpose', 'उद्देश्य')
          const lockd = live && !canLead
          return (
            <li key={k} className={`${k === i ? 'on' : ''}${k < i ? ' done' : ''}${remote === k ? ' at' : ''}`}>
              <button type="button" onClick={() => (lockd ? setI(k) : move(k))} aria-current={k === i ? 'step' : undefined} title={label}>
                <b>{k === 0 ? '◈' : k}</b><span>{label}</span>
              </button>
            </li>
          )
        })}
      </ol>

      <article className="pg-step" aria-live="polite">
        <header>
          <span className="dk-rbub">{i === 0 ? '◈' : i}</span>
          <h3>{step ? G(step.title) : T('The purpose of this ceremony', 'इस अनुष्ठान का उद्देश्य')}</h3>
          <span className="pg-count">{i === 0 ? T('before you begin', 'आरंभ से पहले') : `${i} / ${total - 1}`}</span>
        </header>

        {!step && <p className="pg-purpose">{purpose}</p>}

        {step && step.mantra && (
          <div className={`pg-mantra${speaking === 'mantra' || speaking === 'chant' ? ' sounding' : ''}`}>
            <p className="pg-dev" lang="sa">{step.mantra.dev}</p>
            <p className="pg-roman">{plainRoman(step.mantra.iast)}</p>
            {!live && (chant || voice) && (
              <p className="pg-src">
                {chant
                  ? `♪ ${T('Chanted by', 'मंत्रोच्चार')} ${chant.by || T('a pandit of the roster', 'सूची के पंडित जी')}`
                  : mantraVoice
                    ? T('Read by your device’s voice as an aid to pronunciation — it is not a chant.', 'आपके उपकरण की आवाज़ में, उच्चारण की सहायता के लिए — यह मंत्रोच्चार नहीं है।')
                    : T('Your device has no Hindi voice to read this — say it from the text.', 'इस उपकरण में इसे पढ़ने के लिए हिन्दी आवाज़ नहीं है — पाठ देखकर बोलें।')}
              </p>
            )}
          </div>
        )}
        {step && !step.mantra && (
          <p className="pg-nomantra">{live
            ? T('The pandit recites this part.', 'यह भाग पंडित जी पढ़ते हैं।')
            : T('No single fixed mantra is given for this step — do it as described, or as your family keeps it.', 'इस चरण का कोई एक निश्चित मंत्र नहीं दिया गया — जैसा बताया है, या जैसी आपकी कुल-रीति हो, वैसे करें।')}</p>
        )}

        {parts.length > 0 && (
          <dl className={`pg-ex${speaking === 'explain' ? ' sounding' : ''}`}>
            {parts.map((p) => (<div key={p.k} className={`pg-${p.k}`}><dt>{p.label}</dt><dd>{p.text}</dd></div>))}
          </dl>
        )}

        <footer>
          <button type="button" className="pu-ghost" disabled={i === 0} onClick={() => (live && !canLead ? setI(i - 1) : move(i - 1))}>← {L('Back', 'पीछे')}</button>
          {behind && <button type="button" className="pu-ghost pg-follow" onClick={() => setI(remote)}>↻ {L('Go to the pandit’s step', 'पंडित जी के चरण पर जाएँ')}</button>}
          {i < total - 1
            ? <button type="button" className="go" onClick={() => (live && !canLead ? setI(i + 1) : move(i + 1))}>{i === 0 ? L('Begin the ceremony', 'अनुष्ठान आरंभ करें') : L('Next step', 'अगला चरण')} →</button>
            : <span className="pg-end">॥ {T('The ceremony is complete', 'अनुष्ठान संपन्न')} ॥</span>}
        </footer>
      </article>

      <p className="pu-note pg-note">{L(
        'The explanations say what each step is and why it is done; they are not word-for-word translations of the Sanskrit. Rites differ by region and family — where a pandit leads, his order of steps stands above this one.',
        'व्याख्या बताती है कि हर चरण क्या है और क्यों किया जाता है; यह संस्कृत का शब्दशः अनुवाद नहीं है। विधि क्षेत्र और कुल से बदलती है — जहाँ पंडित जी करा रहे हों, वहाँ उनका क्रम ही मान्य है।')}</p>
    </div>
  )
}
