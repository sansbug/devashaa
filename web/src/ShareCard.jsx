/**
 * The share card: a link that opens this chart, the card it will look like,
 * and the ways to send it. The link is made on demand (see share.js) — what
 * is shared is encrypted before it leaves this browser, and the key rides in
 * the fragment, so neither our server nor anyone reading a log can open it;
 * only the person you send the whole link to can.
 *
 * By default the link carries the FINISHED CHART and not the birth details:
 * the other person sees the chart, its strengths, yogas and readings, but the
 * date, the time and the place of birth are not in the link at all. Ticking
 * "include the birth details" shares those instead, which gives the other
 * person the whole site for this chart — timelines included.
 */
import { useEffect, useState } from 'react'
import { useLang } from './LangContext.jsx'
import { Bubble } from './DashaGlyphs.jsx'
import { makeShareLink } from './share.js'

export default function ShareCard({ chart, name, date, time, place, namer, onClose }) {
  const { t, lang } = useLang()
  const [details, setDetails] = useState(false)
  const [link, setLink] = useState('')
  const [err, setErr] = useState('')
  const [copied, setCopied] = useState(false)
  useEffect(() => {
    let dead = false
    setLink(''); setErr('')
    makeShareLink({ name, date, time, place, chart, lang }, { details })
      .then((l) => { if (!dead) setLink(l) })
      .catch((e) => { if (!dead) setErr(e.message || String(e)) })
    return () => { dead = true }
  }, [name, date, time, place, chart, lang, details])
  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  const sun = chart.grahas.find((g) => g.key === 'sun')
  const moon = chart.grahas.find((g) => g.key === 'moon')
  const title = `${name || t('share.untitled', 'A birth chart')} — Devashaa`
  const text = `${title}: ${t('share.text', 'lagna')} ${namer.rasi(chart.lagna_rasi)} · ${t('share.moon', 'Moon')} ${namer.rasi(moon.rasi)} · ${t('share.sun', 'Sun')} ${namer.rasi(sun.rasi)}`
  const copy = async () => {
    try { await navigator.clipboard.writeText(link); setCopied(true); setTimeout(() => setCopied(false), 1800) } catch { /* fall back to selecting */ }
  }
  const en = namer.style !== 'english'
  const rasi = (i) => `${namer.rasi(i)}${en ? ` (${namer.rasiEnglish(i)})` : ''}`

  return (
    <div className="sh-backdrop" onClick={onClose} role="presentation">
      <div className="sh-modal dk-card" role="dialog" aria-modal="true" aria-label={t('share.title', 'Share this chart')} onClick={(e) => e.stopPropagation()}>
        <h4 className="dk-head"><span>{t('share.title', 'Share this chart')}</span><button type="button" className="sh-x" onClick={onClose} aria-label={t('share.close', 'Close')}>×</button></h4>
        <div className="dk-body">
          <div className="sh-card">
            <div className="sh-card-head">
              <span className="sh-card-brand">devashaa</span>
              <span className="sh-card-name">{name || t('share.untitled', 'A birth chart')}</span>
              <span className="sh-card-when">{details
                ? `${date} · ${time} · ${place.name.split(',')[0]}`
                : t('share.hidden', 'birth details not included')}</span>
            </div>
            <div className="sh-card-rows">
              <div><span className="dk-rbub">{chart.lagna_rasi + 1}</span><b>{t('deck.ascendant', 'Ascendant (Lagna)')}</b><span>{rasi(chart.lagna_rasi)}</span></div>
              <div><Bubble lord="moon" size="m" /><b>{t('deck.moonsign', 'Moon Sign (Rāśi)')}</b><span>{rasi(moon.rasi)} · {namer.nakshatra(moon.nakshatra)}</span></div>
              <div><Bubble lord="sun" size="m" /><b>{t('deck.sunsign', 'Sun Sign')}</b><span>{rasi(sun.rasi)}</span></div>
            </div>
            <div className="sh-card-foot">{t('share.foot', 'Verified positions · cited readings · nothing sold')}</div>
          </div>

          <label className="sh-details">
            <input type="checkbox" checked={details} onChange={(e) => setDetails(e.target.checked)} />
            <span>
              <b>{t('share.details', 'Include the birth details (date, time, place)')}</b>
              <i>{details
                ? t('share.details.on', 'They will see the date, time and place, and get the whole site for this chart — daśā, projection and yearly charts included.')
                : t('share.details.off', 'Off: they get the finished chart — positions, strengths, yogas and readings. The date, time and place are not in the link.')}</i>
            </span>
          </label>

          {err ? (
            <p className="acct-err">{t('share.err', 'The link could not be made:')} {err}</p>
          ) : (
            <>
              <label className="sh-linklabel" htmlFor="sh-link">{t('share.link', 'Link')}</label>
              <div className="sh-linkrow">
                <input id="sh-link" readOnly value={link || t('share.making', 'making the link…')} onFocus={(e) => e.target.select()} />
                <button type="button" className="go sh-copy" disabled={!link} onClick={copy}>{copied ? t('share.copied', 'Copied') : t('share.copy', 'Copy')}</button>
              </div>
              <div className="sh-send">
                <a className="sh-btn" href={link ? `https://wa.me/?text=${encodeURIComponent(text + '\n' + link)}` : '#'} target="_blank" rel="noreferrer" aria-disabled={!link}>WhatsApp</a>
                <a className="sh-btn" href={link ? `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(link)}` : '#'} target="_blank" rel="noreferrer" aria-disabled={!link}>X</a>
                <a className="sh-btn" href={link ? `mailto:?subject=${encodeURIComponent(title)}&body=${encodeURIComponent(text + '\n\n' + link)}` : '#'} aria-disabled={!link}>{t('share.email', 'Email')}</a>
                {typeof navigator !== 'undefined' && navigator.share && (
                  <button type="button" className="sh-btn" disabled={!link} onClick={() => navigator.share({ title, text, url: link }).catch(() => {})}>{t('share.more', 'More…')}</button>
                )}
              </div>
              <p className="sh-note">{details
                ? t('share.note', 'The birth details are encrypted in this browser before the link is made; the key is in the link itself, after the #, which no server ever receives. Only someone with the whole link can open the chart — we cannot.')
                : t('share.note.snap', 'This link carries the chart, not what it was cast from: no date, no time, no place, no dated periods. It is encrypted in this browser, and the key is in the link itself, after the #, which no server receives. One thing to know: a chart is a picture of the sky at a moment, so someone who studies the positions closely could still work out the date.')}</p>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
