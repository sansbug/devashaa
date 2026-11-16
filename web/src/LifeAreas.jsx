/**
 * "Your life, area by area" — the simple view's reading by area of life, ending in
 * practical notes (see lifeareas.js for what each part may say). The notes are
 * OURS and are labelled so; the passages are the texts' and are labelled so.
 */
import { useMemo, useState } from 'react'
import { useLang } from './LangContext.jsx'
import { buildFindings } from './findings.js'
import { buildLifeAreas } from './lifeareas.js'
import { Passage } from './Findings.jsx'

const SHOWN = 3

export default function LifeAreas({ chart, namer, refs, onHouse, goFull }) {
  const { lang } = useLang()
  const L = lang === 'hi' ? 'hi' : 'en'
  const W = (en, hi) => (L === 'hi' ? hi : en)
  const [key, setKey] = useState('career')
  const [more, setMore] = useState(false)
  const areas = useMemo(() => {
    try { return buildLifeAreas(chart, buildFindings(chart, namer), namer) } catch { return null }
  }, [chart, namer.style])  // eslint-disable-line react-hooks/exhaustive-deps
  if (!areas || !areas.length) return null
  const A = areas.find((a) => a.key === key) || areas[0]
  const pick = (a) => { setKey(a.key); setMore(false); if (onHouse) onHouse(a.houses[0]) }
  const passages = more ? A.passages : A.passages.slice(0, SHOWN)

  return (
    <section className="dk-card sv-areas">
      <h4 className="dk-head">
        <span>{W('Your life, area by area', 'आपका जीवन, क्षेत्र-दर-क्षेत्र')}</span>
        <span className="dk-head-right">{W('what the chart shows, what the texts say, and what you can do', 'कुंडली क्या दिखाती है, ग्रंथ क्या कहते हैं, और आप क्या कर सकते हैं')}</span>
      </h4>
      <div className="dk-body">
        <div className="la-tabs" role="tablist">
          {areas.map((a) => (
            <button type="button" key={a.key} role="tab" aria-selected={a.key === A.key}
                    className={a.key === A.key ? 'on' : ''} onClick={() => pick(a)}>
              {a.label[L]}{a.timing.now && <span className="la-now" title={W('in focus now', 'अभी केन्द्र में')} />}
              <small>{a.timing.now ? W('in focus now', 'अभी केन्द्र में') : a.houses.map((h) => W(`house ${h}`, `भाव ${h}`)).join(' · ')}</small>
            </button>
          ))}
        </div>

        <div className="la-grid">
          <div>
            <div className="la-step">
              <h6>{W('What your chart shows', 'आपकी कुंडली क्या दिखाती है')}</h6>
              {A.shows[L].map((s, i) => <p key={i}>{s}</p>)}
            </div>

            <div className="la-step">
              <h6>{W('What the classical texts say', 'शास्त्रीय ग्रंथ क्या कहते हैं')}</h6>
              {A.passages.length === 0 && (
                <p className="fd-held">{W('No registered passage speaks of these houses for this chart, so none is offered.', 'इस कुंडली के इन भावों पर कोई पंजीकृत पाठ लागू नहीं होता, इसलिए कोई नहीं दिया गया।')}</p>
              )}
              {passages.map((t, i) => <Passage key={`${A.key}-${i}`} t={t} L={L} refs={refs} />)}
              {A.passages.length > SHOWN && (
                <button type="button" className="sv-link" onClick={() => setMore((x) => !x)}>
                  {more ? W('Show fewer', 'कम दिखाएँ') : W(`Show all ${A.passages.length} passages`, `सभी ${A.passages.length} पाठ दिखाएँ`)}
                </button>
              )}
              {A.passages.length > 0 && (
                <p className="fd-held">{W('These are the texts’ statements about a placement, some many centuries old. They are not facts about your life.', 'ये एक स्थिति पर ग्रंथों के कथन हैं, कुछ सदियों पुराने। ये आपके जीवन के तथ्य नहीं हैं।')}</p>
              )}
            </div>
          </div>

          <div>
            <div className="la-step">
              <h6>{W('The balance of factors', 'बातों का संतुलन')}</h6>
              <div className="fd-cols">
                {A.supports[L].length > 0 && (
                  <div className="fd-group good"><h6>{W('Supporting', 'समर्थन में')}</h6><ul>{A.supports[L].map((s, i) => <li key={i}>{s}</li>)}</ul></div>
                )}
                {A.cautions[L].length > 0 && (
                  <div className="fd-group hard"><h6>{W('Counting against', 'विपरीत')}</h6><ul>{A.cautions[L].map((s, i) => <li key={i}>{s}</li>)}</ul></div>
                )}
              </div>
              {!A.supports[L].length && !A.cautions[L].length && (
                <p className="fd-held">{W('Nothing notable on either side.', 'किसी भी ओर कोई विशेष बात नहीं।')}</p>
              )}
            </div>

            <div className="la-step">
              <h6>{W('When it comes forward', 'यह कब आगे आता है')}</h6>
              <div className="la-when">
                {A.timing.now && <p>{A.timing.now[L]}</p>}
                {A.timing.next && <p>{A.timing.next[L]}</p>}
                {A.timing.none && <p>{W('This chart was shared without its birth details, so its periods cannot be shown.', 'यह कुंडली जन्म-विवरण के बिना साझा हुई है, इसलिए इसकी दशाएँ नहीं दिखाई जा सकतीं।')}</p>}
                {!A.timing.now && !A.timing.next && !A.timing.none && <p>{W('No upcoming period in the calculated span is tied to this area.', 'गणना की अवधि में इस क्षेत्र से जुड़ी कोई आगामी दशा नहीं है।')}</p>}
                {!A.timing.none && <button type="button" className="sv-link" onClick={goFull}>{W('See the whole timeline →', 'पूरी समय-रेखा देखें →')}</button>}
              </div>
            </div>

            <div className="la-step la-notes">
              <h6>{W('What you can do: practical notes (ours, not from any text)', 'आप क्या कर सकते हैं: व्यावहारिक सुझाव (हमारे, किसी ग्रंथ के नहीं)')}</h6>
              <ul>{A.notes[L].map((s, i) => <li key={i}>{s}</li>)}</ul>
              <details className="la-basis">
                <summary>{W('What these notes rest on', 'ये सुझाव किस पर टिके हैं')}</summary>
                <ol>{A.basis[L].map((s, i) => <li key={i}>{s}</li>)}</ol>
                <p>{W('They are about attention, planning and timing. They are not medical, legal or financial advice, and this site prescribes no ritual, gem or charity.', 'ये ध्यान, योजना और समय के बारे में हैं। ये चिकित्सा, कानूनी या वित्तीय सलाह नहीं हैं, और यह साइट कोई अनुष्ठान, रत्न या दान नहीं बताती।')}</p>
              </details>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
