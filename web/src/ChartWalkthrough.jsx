/**
 * "Watch it explained" — the chart walked through, step by step, on its own
 * animated North Indian chart: the house being spoken of is outlined (never
 * tinted), its grahas glow, the lagna's lord and the aspects are drawn as
 * lines, while the caption says what is being shown.
 *
 * Everything said comes from walkthrough.js, which builds it from this chart's
 * own payload — facts and method, never a verdict (see there). The caption is
 * the narration; a device voice reads it only if the reader turns that on, and
 * it is labelled as a machine's. The script can be copied as plain text, one
 * paragraph a step, for a narrator or a presenter to read.
 */
import { useEffect, useMemo, useRef, useState } from 'react'
import { useLang } from './LangContext.jsx'
import { NORTH_REGIONS } from './RasiChart.jsx'
import { buildWalkthrough, spokenScript, readSeconds } from './walkthrough.js'
import { refsOn } from './refs.js'

const ABBR = {
  en: { sun: 'Su', moon: 'Mo', mars: 'Ma', mercury: 'Me', jupiter: 'Ju', venus: 'Ve', saturn: 'Sa', rahu: 'Ra', ketu: 'Ke' },
  hi: { sun: 'सू', moon: 'चं', mars: 'मं', mercury: 'बु', jupiter: 'गु', venus: 'शु', saturn: 'श', rahu: 'रा', ketu: 'के' },
}
const TAGS = { en: ['en-IN', 'en-GB', 'en-US'], hi: ['hi-IN'] }
const pickVoice = (lang) => {
  const all = (typeof speechSynthesis !== 'undefined' && speechSynthesis.getVoices()) || []
  const ok = all.filter((v) => TAGS[lang].some((t) => String(v.lang).replace('_', '-').toLowerCase().startsWith(t.toLowerCase())))
  return ok.find((v) => /natural|neural/i.test(v.name)) || ok.find((v) => /google/i.test(v.name)) || ok[0] || null
}

/** The chart, with the step's focus drawn on it. Keyed by step, so every step's lines draw afresh. */
function TourChart({ chart, step, lang }) {
  const lagna = chart.lagna_rasi
  const f = step.focus
  const on = new Set(f.houses), lit = new Set(f.grahas)
  const byHouse = Array.from({ length: 12 }, () => [])
  for (const g of chart.grahas) byHouse[g.bhava - 1].push(g)
  const C = (h) => NORTH_REGIONS[h - 1]
  return (
    <svg className={`wt-chart${f.sweep ? ' sweep' : ''}${on.size || lit.size || f.lines.length ? ' focused' : ''}`} viewBox="-6 -6 412 412" role="img"
         aria-label={lang === 'hi' ? 'उत्तर भारतीय कुंडली' : 'North Indian chart'}>
      <defs>
        <marker id="wt-head" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
          <path d="M0,0 L10,5 L0,10 z" className="wt-head" />
        </marker>
      </defs>
      <rect x="0" y="0" width="400" height="400" className="wt-line" />
      <line x1="0" y1="0" x2="400" y2="400" className="wt-line" />
      <line x1="400" y1="0" x2="0" y2="400" className="wt-line" />
      <polygon points="200,0 400,200 200,400 0,200" className="wt-line" />
      {NORTH_REGIONS.map((r, i) => (
        <polygon key={i} points={r.pts} className={`wt-house${on.has(i + 1) ? ' on' : ''}`} style={{ '--d': `${i * 0.28}s` }} />
      ))}
      {f.lines.map((ln, k) => {
        const a = C(ln.from), b = C(ln.to)
        // stop short of the centres, so a line never sits on the labels it joins
        const dx = b.cx - a.cx, dy = b.cy - a.cy, len = Math.hypot(dx, dy) || 1, s = 26 / len
        return (
          <line key={k} x1={a.cx + dx * s} y1={a.cy + dy * s} x2={b.cx - dx * s} y2={b.cy - dy * s}
                className={`wt-ray ${ln.kind}`} style={{ '--d': `${0.25 + k * 0.18}s` }}
                markerEnd={ln.kind === 'part' ? undefined : 'url(#wt-head)'} pathLength="1" />
        )
      })}
      {NORTH_REGIONS.map((r, i) => {
        const occ = byHouse[i]
        const rows = 1 + occ.length, top = r.cy - (rows - 1) * 7.5
        return (
          <g key={i} className="wt-cell">
            <text x={r.cx} y={top} className={`wt-sign${i === 0 ? ' lagna' : ''}`}>{((lagna + i) % 12) + 1}</text>
            {occ.map((g, k) => (
              <text key={g.key} x={r.cx} y={top + (k + 1) * 15} className={`wt-graha${lit.has(g.key) ? ' on' : ''}`}
                    style={{ '--g': `var(--pc-${g.key})` }}>
                {ABBR[lang][g.key]}{g.retrograde ? 'ᴿ' : ''}<tspan className="wt-deg"> {g.degree}°</tspan>
              </text>
            ))}
          </g>
        )
      })}
    </svg>
  )
}

export default function ChartWalkthrough({ chart, namer, onClose }) {
  const { lang: uiLang, t } = useLang()
  const lang = uiLang === 'hi' ? 'hi' : 'en'
  const { steps } = useMemo(() => buildWalkthrough(chart, namer), [chart, namer])
  const [i, setI] = useState(0)
  const [playing, setPlaying] = useState(false)
  const [voiceOn, setVoiceOn] = useState(false)
  const [copied, setCopied] = useState(false)
  const [, setVoicesReady] = useState(0)   // a browser lists its voices late; re-render when it does
  const timer = useRef(null)
  useEffect(() => {
    if (typeof speechSynthesis === 'undefined') return undefined
    const f = () => setVoicesReady((n) => n + 1)
    speechSynthesis.addEventListener('voiceschanged', f)
    return () => speechSynthesis.removeEventListener('voiceschanged', f)
  }, [])
  const step = steps[Math.min(i, steps.length - 1)]
  const text = step.say[lang] || step.say.en
  const refs = refsOn()
  const L = (en, hi) => (lang === 'hi' ? hi : en)

  // Play: speak the step (if asked) or give it a reading pace, then move on; stop after the last.
  useEffect(() => {
    clearTimeout(timer.current)
    if (typeof speechSynthesis !== 'undefined') speechSynthesis.cancel()
    if (!playing) return undefined
    let done = false
    const next = () => {
      if (done) return
      done = true
      timer.current = setTimeout(() => (i < steps.length - 1 ? setI(i + 1) : setPlaying(false)), 700)
    }
    const v = voiceOn ? pickVoice(lang) : null
    if (v) {
      const u = new SpeechSynthesisUtterance(text)
      u.voice = v; u.lang = v.lang; u.rate = 0.95
      u.onend = next; u.onerror = next
      speechSynthesis.speak(u)
    } else {
      timer.current = setTimeout(next, readSeconds(text) * 1000)
    }
    return () => { done = true; clearTimeout(timer.current) }
  }, [playing, i, voiceOn, lang, text, steps.length])

  useEffect(() => () => { clearTimeout(timer.current); if (typeof speechSynthesis !== 'undefined') speechSynthesis.cancel() }, [])

  const go = (k) => setI(Math.max(0, Math.min(steps.length - 1, k)))
  const onKey = (e) => {
    if (e.key === 'ArrowRight') { e.preventDefault(); go(i + 1) }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); go(i - 1) }
    else if (e.key === 'Escape') onClose()
  }
  const copy = async () => {
    try { await navigator.clipboard.writeText(spokenScript(steps, lang)); setCopied(true); setTimeout(() => setCopied(false), 2500) } catch { /* no clipboard */ }
  }
  const noVoice = voiceOn && !pickVoice(lang)

  return (
    <section className="wt" aria-label={L('The chart, explained', 'कुंडली की व्याख्या')} onKeyDown={onKey}>
      <header className="wt-top">
        <h3>{L('The chart, explained', 'कुंडली की व्याख्या')}</h3>
        <span className="wt-count">{i + 1} / {steps.length}</span>
        <button type="button" className="wt-x" onClick={onClose} aria-label={t('common.close', 'Close')}>×</button>
      </header>
      <div className="wt-body">
        <div className="wt-stage"><TourChart key={i} chart={chart} step={step} lang={lang} /></div>
        <div className="wt-cap" aria-live="polite">
          <p className="wt-say">{text}</p>
          {step.focus.names && step.focus.names.length > 0 && (
            <ul className="wt-names">{step.focus.names.map((n) => <li key={n}>{n}</li>)}</ul>
          )}
          {step.quote && step.quote.length > 0 && (
            <div className="wt-quotes">
              {step.quote.map((q) => (
                <p key={q.name} className="wt-quote"><b>{q.name}</b> — {L('the text reads', 'ग्रंथ के शब्द')}: “{q.effect}”</p>
              ))}
            </div>
          )}
          {refs && step.cite && <p className="wt-cite">{step.cite}</p>}
        </div>
      </div>
      <div className="wt-bar">
        <button type="button" className="wt-btn" onClick={() => go(i - 1)} disabled={i === 0} aria-label={L('Previous step', 'पिछला चरण')}>◀</button>
        <button type="button" className="wt-btn wt-play" onClick={() => { if (!playing && i === steps.length - 1) setI(0); setPlaying(!playing) }}
                aria-pressed={playing}>
          {playing ? `❚❚ ${L('Pause', 'रोकें')}` : `▶ ${L('Play', 'चलाएँ')}`}
        </button>
        <button type="button" className="wt-btn" onClick={() => go(i + 1)} disabled={i === steps.length - 1} aria-label={L('Next step', 'अगला चरण')}>▶</button>
        <ol className="wt-dots">
          {steps.map((s, k) => (
            <li key={s.key}><button type="button" className={k === i ? 'on' : k < i ? 'done' : ''} onClick={() => go(k)}
                                    aria-label={`${k + 1}`} aria-current={k === i ? 'step' : undefined} /></li>
          ))}
        </ol>
        <label className="wt-voice">
          <input type="checkbox" checked={voiceOn} onChange={(e) => setVoiceOn(e.target.checked)} />
          {L('Read aloud — this device’s machine voice', 'पढ़कर सुनाएँ — इस उपकरण की मशीनी आवाज़')}
        </label>
        <button type="button" className="wt-copy" onClick={copy} title={L('Plain text, one paragraph a step', 'सादा पाठ, हर चरण का एक अनुच्छेद')}>
          {copied ? L('Copied ✓', 'कॉपी हो गया ✓') : L('Copy the script', 'पटकथा कॉपी करें')}
        </button>
      </div>
      {noVoice && <p className="wt-note">{L('This device has no voice for English — the captions carry it.', 'इस उपकरण में हिन्दी की कोई आवाज़ नहीं है — कैप्शन पढ़ें।')}</p>}
    </section>
  )
}
