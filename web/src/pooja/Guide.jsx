/**
 * The guided ceremony — purpose first, then the chanting, one step at a time.
 *
 * Each step shows the mantra as chanted (Devanāgarī, and a plain roman reading
 * to say it from), then WHAT IS HAPPENING and WHY. Three depths of explanation:
 * detailed, short, or the mantras alone. The family chooses the language of
 * the explanation (the chant is always Sanskrit) and a male or a female voice.
 *
 * WHOSE VOICE.
 *   A chant is a person's. The mantra is played from the voice library — a
 *   pandit of the roster chanting it — in the voice asked for where there is
 *   one. Where no pandit has recorded a mantra yet it is NOT read out by a
 *   machine: it is shown, to be chanted from the text. (A device-voice reading
 *   can be switched on as a pronunciation aid; it is off unless asked for.)
 *   The explanation is likewise the pandit's own recording where he has made
 *   one. The device's own voice — a machine's — is used for neither unless the
 *   family asks for it, and then it is labelled as what it is. If the family
 *   asked for a man's voice and the device has only a woman's (or the reverse),
 *   the wrong one is not played: the panel says the device has none.
 *
 *   Live — the pandit chants in the room and moves everyone's screen to the
 *   step he is on; this panel then only explains (aloud too, if asked — for
 *   someone on headphones who wants it in another language).
 */
import { useEffect, useMemo, useRef, useState } from 'react'
import { MODES, VOICE_LANGS, scriptFor, explain, romanOf, narration, mantraClip, explainClip } from './guide.js'
import { api } from './papi.js'
import { deviceVoice } from './voices.js'

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
const sentences = (text) => (String(text).match(/[^.!?।॥\n]+[.!?।॥]*/g) || []).map((x) => x.replace(/[।॥]+/g, '').trim()).filter(Boolean)

let clipsCache = null
function useClips() {
  const [c, setC] = useState(clipsCache || {})
  useEffect(() => { if (!clipsCache) api.chants().then((j) => { clipsCache = j; setC(j) }) }, [])
  return c
}
const blobUrls = new Map()

function Seg({ label, options, value, set }) {
  return (
    <div className="pg-set">
      <span className="pg-set-l">{label}</span>
      <span className="pg-seg" role="group" aria-label={label}>
        {options.map(([k, text]) => <button type="button" key={k} className={value === k ? 'on' : ''} aria-pressed={value === k} onClick={() => set(k)}>{text}</button>)}
      </span>
    </div>
  )
}

export default function Guide({ ritual, lang = 'en', L, live = false, canLead = true, remote = null, onStep, className = '' }) {
  const steps = useMemo(() => scriptFor(ritual.key), [ritual.key])
  const total = steps.length + 1                 // step 0 is the purpose
  const prefs = useMemo(loadPrefs, [])
  const [mode, setMode] = useState(MODES.some((m) => m.key === prefs.mode) ? prefs.mode : 'short')
  const [glang, setGlang] = useState(VOICE_LANGS.some((v) => v.key === prefs.glang) ? prefs.glang : (lang === 'hi' ? 'hi' : 'en'))
  const [gender, setGender] = useState(prefs.gender === 'f' ? 'f' : 'm')
  const [auto, setAuto] = useState(!!prefs.auto)
  const [machine, setMachine] = useState(!!prefs.machine)  // let the device voice read an explanation no pandit has recorded
  const [aid, setAid] = useState(!!prefs.aid)    // …and a mantra, as a pronunciation aid
  const [voice, setVoice] = useState(false)      // read aloud — always starts off; a tap turns it on
  const [i, setI] = useState(0)
  const [speaking, setSpeaking] = useState('')   // '' | 'explain' | 'mantra'
  const run = useRef(0)
  const audio = useRef(null)
  const voices = useVoices()
  const clips = useClips()
  const ex = useMemo(() => deviceVoice(voices, VOICE_LANGS.find((v) => v.key === glang).bcp, gender), [voices, glang, gender])
  const mv = useMemo(() => deviceVoice(voices, ['sa', 'hi-IN', 'hi'], gender), [voices, gender])
  const exVoice = ex.voice, mantraVoice = mv.voice
  const G = (o) => (o ? (o[glang] || o.en) : '')
  const T = (en, hi) => (glang === 'hi' ? hi : en)

  useEffect(() => { savePrefs({ mode, glang, gender, auto, machine, aid }) }, [mode, glang, gender, auto, machine, aid])
  // The pandit moved on: follow him.
  useEffect(() => { if (remote != null && remote >= 0 && remote < total) setI(remote) }, [remote, total])

  const step = i > 0 ? steps[i - 1] : null
  const told = narration(ritual, step, mode, glang)           // what is read to explain this step
  const parts = step ? explain(step, mode, glang) : []
  // A recording in the voice asked for; failing that, whoever has recorded it.
  const pick = (id) => { const list = clips[id] || []; return list.find((c) => c.voice === gender) || list[0] || null }
  // A person's chant in the other voice is still offered — a real chant beats silence — but never unannounced.
  const otherVoice = (rec) => (rec && rec.voice && rec.voice !== gender
    ? (gender === 'm'
      ? T(' — no man’s voice has recorded this yet', ' — इसे अभी किसी पुरुष स्वर ने रिकॉर्ड नहीं किया')
      : T(' — no woman’s voice has recorded this yet', ' — इसे अभी किसी स्त्री स्वर ने रिकॉर्ड नहीं किया'))
    : '')
  const chantId = step && step.mantra ? mantraClip(step) : null
  const chant = chantId ? pick(chantId) : null
  const toldId = told ? explainClip(ritual, step, mode, glang) : null
  const toldBy = toldId ? pick(toldId) : null

  const alive = (token) => run.current === token
  const hush = () => {
    run.current += 1
    const s = synth()
    try { s && s.cancel() } catch { /* nothing speaking */ }
    try { audio.current && audio.current.pause() } catch { /* nothing playing */ }
    audio.current = null
    setSpeaking('')
  }
  const say = async (token, text, v, rate, what) => {
    const s = synth()
    if (!s || !v || !text) return false
    setSpeaking(what)
    for (const chunk of sentences(text)) {
      if (!alive(token)) return true
      await new Promise((res) => {
        const u = new SpeechSynthesisUtterance(chunk)
        u.voice = v; u.lang = v.lang; u.rate = rate
        u.onend = res; u.onerror = res
        s.speak(u)
      })
    }
    return true
  }
  /** Play a pandit's recording. False if it could not be played, so the caller can fall back. */
  const playClip = async (token, id, rec, what) => {
    setSpeaking(what)
    try {
      const src = api.chantUrl(id, rec.id, rec.at)
      if (!blobUrls.has(src)) {
        const blob = await fetch(src).then((r) => (r.ok ? r.blob() : null))
        if (!blob) return false
        blobUrls.set(src, URL.createObjectURL(blob))
      }
      if (!alive(token)) return true
      const a = new Audio(blobUrls.get(src))
      audio.current = a
      return await new Promise((res) => { a.onended = () => res(true); a.onpause = () => res(true); a.onerror = () => res(false); a.play().catch(() => res(false)) })
    } catch { return false }
  }
  const soundExplanation = async (token) => {
    if (!told) return
    if (toldBy && await playClip(token, toldId, toldBy, 'explain')) return
    if (machine && alive(token)) await say(token, step ? told : `${T('The purpose of this ceremony', 'इस अनुष्ठान का उद्देश्य')}. ${told}`, exVoice, 0.95, 'explain')
  }
  /** The mantra: a pandit's chant; else — only if asked for — the device voice as a pronunciation aid. True if anything sounded. */
  const soundMantra = async (token) => {
    if (!step || !step.mantra) return false
    if (chant && await playClip(token, chantId, chant, 'mantra')) return true
    if (aid && alive(token)) return say(token, step.mantra.dev, mantraVoice, 0.78, 'mantra')
    return false
  }
  const hearMantra = async () => {
    hush()
    const token = ++run.current
    await soundMantra(token)
    if (alive(token)) setSpeaking('')
  }
  const move = (k) => {
    const n = Math.max(0, Math.min(total - 1, k))
    setI(n)
    if (live && canLead && onStep) onStep(n)
  }

  // Voice on: sound the step whenever the step, the depth, the language or the voice changes.
  useEffect(() => {
    if (!voice) return undefined
    const token = ++run.current
    ;(async () => {
      await wait(250)
      if (!alive(token)) return
      await soundExplanation(token)
      let chanted = true
      if (alive(token) && !live && step && step.mantra) chanted = await soundMantra(token)
      if (!alive(token)) return
      setSpeaking('')
      if (auto && !live && i < total - 1) {
        // No recording of this mantra: leave the family time to chant it themselves.
        await wait(chanted ? 1800 : Math.min(25000, 4000 + (step && step.mantra ? step.mantra.dev.length * 90 : 0)))
        if (alive(token)) setI(i + 1)
      }
    })()
    return () => { run.current += 1; const s = synth(); try { s && s.cancel() } catch { /* idle */ } try { audio.current && audio.current.pause() } catch { /* idle */ } }
  }, [voice, i, mode, glang, gender, machine, aid, exVoice, mantraVoice, chant && chant.id, toldBy && toldBy.id])  // eslint-disable-line react-hooks/exhaustive-deps
  useEffect(() => () => hush(), [])  // eslint-disable-line react-hooks/exhaustive-deps

  const behind = live && !canLead && remote != null && remote !== i

  return (
    <div className={`pg${live ? ' live' : ''} ${className}`} lang={glang}>
      <div className="pg-bar">
        <Seg label={L('Explanation', 'व्याख्या')} options={MODES.map((m) => [m.key, lang === 'hi' ? m.hi : m.en])} value={mode} set={setMode} />
        <Seg label={L('Explain in', 'व्याख्या की भाषा')} options={VOICE_LANGS.map((v) => [v.key, v.label])} value={glang} set={setGlang} />
        <Seg label={L('Voice', 'आवाज़')} options={[['m', L('Male', 'पुरुष')], ['f', L('Female', 'स्त्री')]]} value={gender} set={setGender} />
        <div className="pg-set pg-voice">
          <button type="button" className={`pg-play${voice ? ' on' : ''}`} aria-pressed={voice} onClick={() => { if (voice) { hush(); setVoice(false) } else setVoice(true) }}>
            {voice ? `❚❚ ${L('Voice off', 'आवाज़ बंद')}` : live ? `🔊 ${L('Read the explanation to me', 'व्याख्या पढ़कर सुनाएँ')}` : `▶ ${L('Guide me by voice', 'आवाज़ से मार्गदर्शन')}`}
          </button>
          {!live && <label className="pg-auto"><input type="checkbox" checked={auto} onChange={(e) => setAuto(e.target.checked)} /> {L('move on by itself', 'स्वयं आगे बढ़े')}</label>}
        </div>
      </div>
      <p className="pg-langs">{steps.some((s) => s.mantra && s.mantra.lang === 'awa')
        ? L('The verses are Tulasīdāsa’s own, in Awadhi — given in Hindi letters and in roman; the explanation is in the language you choose.', 'छंद गोस्वामी तुलसीदास के अपने हैं, अवधी में — हिन्दी और रोमन अक्षरों में दिए गए; व्याख्या आपकी चुनी भाषा में।')
        : L('The chant is always in Sanskrit; the explanation is in the language you choose.', 'मंत्रोच्चार सदा संस्कृत में है; व्याख्या आपकी चुनी भाषा में।')}</p>
      {voice && live && <p className="pu-note pg-warn">{L('Use headphones, so the voice does not carry into the room. Only the explanation is read — the pandit chants.', 'हेडफ़ोन लगाएँ, ताकि आवाज़ कक्ष में न जाए। केवल व्याख्या पढ़ी जाती है — मंत्रोच्चार पंडित जी करते हैं।')}</p>}

      <ol className="pg-rail" aria-label={L('The steps', 'चरण')}>
        {Array.from({ length: total }, (_, k) => {
          const st = k > 0 ? steps[k - 1] : null
          const label = st ? G(st.title) : T('Purpose', 'उद्देश्य')
          const lockd = live && !canLead
          return (
            <li key={k} className={`${k === i ? 'on' : ''}${k < i ? ' done' : ''}${remote === k ? ' at' : ''}`}>
              <button type="button" onClick={() => (lockd ? setI(k) : move(k))} aria-current={k === i ? 'step' : undefined}>
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

        {!step && <p className={`pg-purpose${speaking === 'explain' ? ' sounding' : ''}`}>{told || G(ritual.purpose)}</p>}

        {step && step.mantra && (
          <div className={`pg-mantra${speaking === 'mantra' ? ' sounding' : ''}`}>
            <p className={`pg-dev${step.mantra.dev.split('\n').length > 5 ? ' long' : ''}`} lang={step.mantra.lang || 'sa'}>{step.mantra.dev}</p>
            <p className={`pg-roman${step.mantra.dev.split('\n').length > 5 ? ' long' : ''}`}>{romanOf(step.mantra)}</p>
            {!live && (
              <p className="pg-src">
                {chant
                  ? <><button type="button" className="pg-hear" onClick={hearMantra}>▶ {T('Hear the chant', 'मंत्रोच्चार सुनें')}</button> ♪ {T('chanted by', 'स्वर')} <b>{chant.by}</b>{otherVoice(chant)}</>
                  : <>{T('No pandit has recorded this mantra yet — chant it from the text.', 'इस मंत्र का उच्चारण अभी किसी पंडित जी ने रिकॉर्ड नहीं किया — पाठ देखकर स्वयं बोलें।')}
                      {aid && mantraVoice && <> <button type="button" className="pg-hear" onClick={hearMantra}>▶ {T('Pronunciation aid', 'उच्चारण सहायता')}</button></>}</>}
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
        {voice && told && (
          <p className="pg-src pg-toldby">{toldBy
            ? <>♪ {T('explained by', 'व्याख्या')} <b>{toldBy.by}</b>{otherVoice(toldBy)}</>
            : !machine
              ? T('No pandit has recorded this explanation yet — it is shown, not read. (A machine voice can be switched on below.)', 'यह व्याख्या अभी किसी पंडित जी ने रिकॉर्ड नहीं की — यह दिखाई जा रही है, पढ़ी नहीं जा रही। (मशीन की आवाज़ नीचे चालू की जा सकती है।)')
              : ex.how === 'exact'
                ? `${T('A machine voice, from your device', 'मशीन की आवाज़, आपके उपकरण से')}: ${exVoice.name}.`
                : ex.how === 'unknown'
                  ? `${T('A machine voice, from your device', 'मशीन की आवाज़, आपके उपकरण से')}: ${exVoice.name}. ${T('This device does not say whether its voices are a man’s or a woman’s, so the choice above cannot be applied to it.', 'यह उपकरण नहीं बताता कि उसकी आवाज़ें पुरुष की हैं या स्त्री की, अतः ऊपर का चुनाव इस पर लागू नहीं हो सकता।')}`
                  : ex.how === 'other'
                    ? (gender === 'm'
                      ? T('This device has no male voice for this language, only a female one — so nothing is read. Choose Female above, or read from the screen.', 'इस उपकरण में इस भाषा की पुरुष आवाज़ नहीं है, केवल स्त्री की — इसलिए कुछ पढ़ा नहीं जा रहा। ऊपर "स्त्री" चुनें, या स्क्रीन से पढ़ें।')
                      : T('This device has no female voice for this language, only a male one — so nothing is read. Choose Male above, or read from the screen.', 'इस उपकरण में इस भाषा की स्त्री आवाज़ नहीं है, केवल पुरुष की — इसलिए कुछ पढ़ा नहीं जा रहा। ऊपर "पुरुष" चुनें, या स्क्रीन से पढ़ें।'))
                    : T('This device has no voice for that language — the explanation is shown, not read.', 'इस उपकरण में उस भाषा की आवाज़ नहीं है — व्याख्या दिखाई जा रही है, पढ़ी नहीं जा रही।')}</p>
        )}

        <footer>
          <button type="button" className="pu-ghost" disabled={i === 0} onClick={() => (live && !canLead ? setI(i - 1) : move(i - 1))}>← {L('Back', 'पीछे')}</button>
          {behind && <button type="button" className="pu-ghost pg-follow" onClick={() => setI(remote)}>↻ {L('Go to the pandit’s step', 'पंडित जी के चरण पर जाएँ')}</button>}
          {i < total - 1
            ? <button type="button" className="go" onClick={() => (live && !canLead ? setI(i + 1) : move(i + 1))}>{i === 0 ? L('Begin the ceremony', 'अनुष्ठान आरंभ करें') : L('Next step', 'अगला चरण')} →</button>
            : <span className="pg-end">॥ {T('The ceremony is complete', 'अनुष्ठान संपन्न')} ॥</span>}
        </footer>
      </article>

      <fieldset className="pg-machine">
        <legend>{L('Where no pandit has recorded yet', 'जहाँ अभी किसी पंडित जी ने रिकॉर्ड नहीं किया')}</legend>
        <label className="pg-aid"><input type="checkbox" checked={machine} onChange={(e) => setMachine(e.target.checked)} /> {L(
          'let my device’s voice read the explanation — a machine voice, off unless you ask for it',
          'व्याख्या मेरे उपकरण की आवाज़ में पढ़ी जाए — यह मशीन की आवाज़ है, माँगे बिना चालू नहीं होती')}</label>
        {!live && (
          <label className="pg-aid"><input type="checkbox" checked={aid} onChange={(e) => setAid(e.target.checked)} /> {L(
            'and let it read the mantra as a pronunciation aid — a machine reading, not a chant',
            'और मंत्र को उच्चारण-सहायता के रूप में पढ़े — यह मशीन का पाठ है, मंत्रोच्चार नहीं')}</label>
        )}
      </fieldset>
      <p className="pu-note pg-note">{L(
        'The explanations say what each step is and why it is done; they are not word-for-word translations of the Sanskrit. Rites differ by region and family — where a pandit leads, his order of steps stands above this one.',
        'व्याख्या बताती है कि हर चरण क्या है और क्यों किया जाता है; यह संस्कृत का शब्दशः अनुवाद नहीं है। विधि क्षेत्र और कुल से बदलती है — जहाँ पंडित जी करा रहे हों, वहाँ उनका क्रम ही मान्य है।')}</p>
    </div>
  )
}
