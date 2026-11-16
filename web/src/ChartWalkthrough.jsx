/**
 * "Watch it explained" — the chart explained topic by topic, in plain words, on
 * its own animated North Indian chart. One topic a screen (the basics, each of
 * the twelve houses, what is running now): the house in question is outlined —
 * never tinted — the house its lord sits in is outlined lighter, a line runs to
 * the lord, the grahas that matter glow and the aspects are drawn in.
 *
 * Everything shown comes from walkthrough.js, built from this chart's own
 * payload: the chart's facts and the method that reads them, in the format of
 * the simple explainers people already read — the houses that matter, then
 * numbered lines about THIS chart. The classical rule behind a placement is a
 * click away, in the text's own words (or, when it carries a care-sensitive
 * verdict, a pointer to the Bhāvas panel). A device voice reads the lines only
 * if the reader turns it on, labelled as a machine's; "Copy the script" gives
 * one paragraph a topic, for a narrator or a presenter to read.
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
        <polygon key={i} points={r.pts} className={`wt-house${on.has(i + 1) ? ' on' : ''}${f.main === i + 1 ? ' main' : ''}`} style={{ '--d': `${i * 0.28}s` }} />
      ))}
      {f.lines.map((ln, k) => {
        const a = C(ln.from), b = C(ln.to)
        // stop short of the centres, so a line never sits on the labels it joins
        const dx = b.cx - a.cx, dy = b.cy - a.cy, len = Math.hypot(dx, dy) || 1, s = 26 / len
        // an aspect runs a little to one side, so it never lies on top of the lord's line between the same two houses
        const o = ln.kind === 'lord' ? 0 : 6, ox = (-dy / len) * o, oy = (dx / len) * o
        return (
          <line key={k} x1={a.cx + dx * s + ox} y1={a.cy + dy * s + oy} x2={b.cx - dx * s + ox} y2={b.cy - dy * s + oy}
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
  const P = (o) => (o ? (o[lang] || o.en) : null)
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

  // keep the current topic in view in the topic row (sideways only — the page itself does not move)
  const topics = useRef(null)
  useEffect(() => {
    const row = topics.current, b = row && row.querySelector('button.on')
    if (b) row.scrollTo({ left: b.offsetLeft - (row.clientWidth - b.offsetWidth) / 2, behavior: 'smooth' })
  }, [i])

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
    <section className="wt" aria-label={L('Your chart, explained simply', 'आपकी कुंडली, सरल शब्दों में')} onKeyDown={onKey}>
      <header className="wt-top">
        <h3>{L('Your chart, explained simply', 'आपकी कुंडली, सरल शब्दों में')}</h3>
        <span className="wt-count">{i + 1} / {steps.length}</span>
        <button type="button" className="wt-x" onClick={onClose} aria-label={t('common.close', 'Close')}>×</button>
      </header>
      <ol className="wt-topics" ref={topics} aria-label={L('Topics', 'विषय')}>
        {steps.map((s, k) => (
          <li key={s.key}>
            <button type="button" className={k === i ? 'on' : ''} aria-current={k === i ? 'step' : undefined} onClick={() => go(k)}>
              {s.key.startsWith('house') ? `${s.key.slice(5)} · ` : ''}{P(s.title)}
            </button>
          </li>
        ))}
      </ol>
      <div className="wt-body">
        <div className="wt-stage"><TourChart key={i} chart={chart} step={step} lang={lang} /></div>
        <div className="wt-cap" aria-live="polite">
          <h4 className="wt-title">{P(step.title)}</h4>
          {P(step.chips).length > 0 && (
            <ul className="wt-chips" aria-label={L('What matters here', 'यहाँ क्या मायने रखता है')}>
              {P(step.chips).map((c) => <li key={c.label}><b>{c.label}</b> = {c.text}</li>)}
            </ul>
          )}
          <ol className={`wt-lines${P(step.lines).length > 1 ? '' : ' one'}`}>
            {P(step.lines).map((x, k) => <li key={k}>{x}</li>)}
          </ol>
          {step.text && (
            <details className="wt-text" key={step.key}>
              <summary>{L('What the classical text says', 'शास्त्र क्या कहता है')}</summary>
              {P(step.text).quote
                ? <p>“{P(step.text).quote}” <small>{P(step.text).note}</small></p>
                : <p><small>{P(step.text).note}</small></p>}
            </details>
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
        <label className="wt-voice">
          <input type="checkbox" checked={voiceOn} onChange={(e) => setVoiceOn(e.target.checked)} />
          {L('Read aloud: this device’s machine voice', 'पढ़कर सुनाएँ: इस उपकरण की मशीनी आवाज़')}
        </label>
        <button type="button" className="wt-copy" onClick={copy} title={L('Plain text, one paragraph a step', 'सादा पाठ, हर चरण का एक अनुच्छेद')}>
          {copied ? L('Copied ✓', 'कॉपी हो गया ✓') : L('Copy the script', 'पटकथा कॉपी करें')}
        </button>
      </div>
      {noVoice && <p className="wt-note">{L('This device has no voice for English. The captions carry it.', 'इस उपकरण में हिन्दी की कोई आवाज़ नहीं है। कैप्शन पढ़ें।')}</p>}
    </section>
  )
}
