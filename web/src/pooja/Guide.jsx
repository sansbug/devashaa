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
 *   one, and only otherwise the device's voice, labelled as such.
 *
 *   Live — the pandit chants in the room and moves everyone's screen to the
 *   step he is on; this panel then only explains (aloud too, if asked — for
 *   someone on headphones who wants it in another language).
 */
import { useEffect, useMemo, useRef, useState } from 'react'
import { MODES, VOICE_LANGS, scriptFor, explain, plainRoman, narration, mantraClip, explainClip } from './guide.js'
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
// A device does not say whether a voice is a man's or a woman's; the common ones are known by name.
const FEMALE = /female|swara|neerja|heera|kalpana|ananya|aditi|lekha|veena|zira|aria|jenny|sonia|libby|samantha|karen|moira|tessa|nicky|google हिन्दी|google us english/i
const MALE = /(^|[^e])male|madhur|prabhat|ravi|hemant|rishi|david|mark|guy|ryan|daniel|alex|aaron|george|james/i
const genderOf = (v) => (FEMALE.test(v.name) ? 'f' : MALE.test(v.name) ? 'm' : '')
/** The best device voice for these language tags: of the gender asked for if the device has one, natural if it has one. */
function voiceFor(voices, tags, gender) {
  for (const tag of tags) {
    const hits = voices.filter((v) => (v.lang || '').replace('_', '-').toLowerCase().startsWith(tag.toLowerCase()))
    if (!hits.length) continue
    const pool = hits.filter((v) => genderOf(v) === gender)
    const from = pool.length ? pool : hits
    return from.find((v) => /natural|neural/i.test(v.name)) || from.find((v) => /google/i.test(v.name)) || from[0]
  }
  return null
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
  const [aid, setAid] = useState(!!prefs.aid)    // let the device voice read a mantra no pandit has recorded
  const [voice, setVoice] = useState(false)      // read aloud — always starts off; a tap turns it on
  const [i, setI] = useState(0)
  const [speaking, setSpeaking] = useState('')   // '' | 'explain' | 'mantra'
  const run = useRef(0)
  const audio = useRef(null)
  const voices = useVoices()
  const clips = useClips()
  const exVoice = useMemo(() => voiceFor(voices, VOICE_LANGS.find((v) => v.key === glang).bcp, gender), [voices, glang, gender])
  const mantraVoice = useMemo(() => voiceFor(voices, ['sa', 'hi-IN', 'hi'], gender), [voices, gender])
  const G = (o) => (o ? (o[glang] || o.en) : '')
  const T = (en, hi) => (glang === 'hi' ? hi : en)

  useEffect(() => { savePrefs({ mode, glang, gender, auto, aid }) }, [mode, glang, gender, auto, aid])
  // The pandit moved on: follow him.
  useEffect(() => { if (remote != null && remote >= 0 && remote < total) setI(remote) }, [remote, total])

  const step = i > 0 ? steps[i - 1] : null
  const told = narration(ritual, step, mode, glang)           // what is read to explain this step
  const parts = step ? explain(step, mode, glang) : []
  // A recording in the voice asked for; failing that, whoever has recorded it.
  const pick = (id) => { const list = clips[id] || []; return list.find((c) => c.voice === gender) || list[0] || null }
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
    if (alive(token)) await say(token, step ? told : `${T('The purpose of this ceremony', 'इस अनुष्ठान का उद्देश्य')}. ${told}`, exVoice, 0.95, 'explain')
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
  }, [voice, i, mode, glang, gender, aid, exVoice, mantraVoice, chant && chant.id, toldBy && toldBy.id])  // eslint-disable-line react-hooks/exhaustive-deps
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
      <p className="pg-langs">{L('The chant is always in Sanskrit; the explanation is in the language you choose.', 'मंत्रोच्चार सदा संस्कृत में है; व्याख्या आपकी चुनी भाषा में।')}</p>
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
            <p className="pg-dev" lang="sa">{step.mantra.dev}</p>
            <p className="pg-roman">{plainRoman(step.mantra.iast)}</p>
            {!live && (
              <p className="pg-src">
                {chant
                  ? <><button type="button" className="pg-hear" onClick={hearMantra}>▶ {T('Hear the chant', 'मंत्रोच्चार सुनें')}</button> ♪ {T('chanted by', 'स्वर')} <b>{chant.by}</b></>
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
            ? <>♪ {T('explained by', 'व्याख्या')} <b>{toldBy.by}</b></>
            : exVoice
              ? T('Read by your device’s voice. A pandit’s own voice replaces it as each explanation is recorded.', 'आपके उपकरण की आवाज़ में। जैसे-जैसे हर व्याख्या रिकॉर्ड होगी, पंडित जी की अपनी आवाज़ इसकी जगह लेगी।')
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

      {!live && (
        <label className="pg-aid"><input type="checkbox" checked={aid} onChange={(e) => setAid(e.target.checked)} /> {L(
          'Where no pandit has recorded a mantra, let my device’s voice read it as a pronunciation aid (it is a machine reading, not a chant).',
          'जहाँ किसी पंडित जी ने मंत्र रिकॉर्ड नहीं किया, वहाँ मेरे उपकरण की आवाज़ उसे उच्चारण-सहायता के रूप में पढ़े (यह मशीन का पाठ है, मंत्रोच्चार नहीं)।')}</label>
      )}
      <p className="pu-note pg-note">{L(
        'The explanations say what each step is and why it is done; they are not word-for-word translations of the Sanskrit. Rites differ by region and family — where a pandit leads, his order of steps stands above this one.',
        'व्याख्या बताती है कि हर चरण क्या है और क्यों किया जाता है; यह संस्कृत का शब्दशः अनुवाद नहीं है। विधि क्षेत्र और कुल से बदलती है — जहाँ पंडित जी करा रहे हों, वहाँ उनका क्रम ही मान्य है।')}</p>
    </div>
  )
}
