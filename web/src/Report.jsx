/**
 * The full report: one page that carries everything the simple view says about a chart — the two charts, the
 * key facts and positions, "who you are", the chart explained planet by planet and house by house, the daśā
 * reading, every life area and every finding — laid out to be read, printed or saved as a PDF.
 *
 * It is made in this browser from the chart already on the page: nothing is sent anywhere and nothing new is
 * written. Every line comes from the same builders the simple view uses (walkthrough.js, dashareading.js,
 * lifeareas.js, findings.js), so the report says exactly what the site says and obeys the same rules: a
 * passage that speaks of a death, a lifespan, a bereavement or a partner's fidelity is not shown unasked, and
 * references appear only when the reader has them switched on.
 *
 * "Save as PDF" is the browser's own print dialog (destination: Save as PDF). The print stylesheet (App.css,
 * `.rp`) hides the rest of the site and the toolbar. With "birth details and dated periods" unticked the report
 * carries no date, time or place of birth and no dated period — the same line the share link draws.
 */
import { useEffect, useMemo, useState } from 'react'
import { createPortal } from 'react-dom'
import { useLang } from './LangContext.jsx'
import NorthDeckChart from './NorthDeckChart.jsx'
import SouthDeckChart from './SouthDeckChart.jsx'
import { HighlightsCard } from './ChartDeck.jsx'
import { WhoCard } from './SimpleView.jsx'
import DashaReading from './DashaReading.jsx'
import { Passage } from './Findings.jsx'
import { buildWalkthrough } from './walkthrough.js'
import { buildFindings, rankFindings, TAGS } from './findings.js'
import { buildLifeAreas } from './lifeareas.js'

const EN_ORD = (n) => `${n}${n % 10 === 1 && n !== 11 ? 'st' : n % 10 === 2 && n !== 12 ? 'nd' : n % 10 === 3 && n !== 13 ? 'rd' : 'th'}`
const pad2 = (n) => String(n).padStart(2, '0')

export default function Report({ chart, name, date, time, place, namer, refs, snap, onClose }) {
  const { lang } = useLang()
  const L = lang === 'hi' ? 'hi' : 'en'
  const W = (en, hi) => (L === 'hi' ? hi : en)
  const hasBirth = !snap && !!(chart.dasha && chart.dasha.variants)
  const [dated, setDated] = useState(hasBirth)
  // with the birth details left out, the builders are given a chart with no periods: no dated line can be written
  const shown = useMemo(() => (dated ? chart : { ...chart, dasha: undefined }), [chart, dated])
  const data = useMemo(() => {
    const built = buildFindings(shown, namer)
    return {
      steps: buildWalkthrough(shown, namer).steps,
      areas: buildLifeAreas(shown, built, namer),
      findings: rankFindings(built, 'overall'),
    }
  }, [shown, namer.style])  // eslint-disable-line react-hooks/exhaustive-deps

  const who = name || W('A birth chart', 'एक जन्म कुंडली')
  useEffect(() => {
    const was = document.title
    document.title = `${who} · Devashaa`   // the browser offers this as the PDF's file name
    document.body.classList.add('rp-open')
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => { document.title = was; document.body.classList.remove('rp-open'); window.removeEventListener('keydown', onKey) }
  }, [who, onClose])

  const today = new Date()
  const made = `${today.getFullYear()}-${pad2(today.getMonth() + 1)}-${pad2(today.getDate())}`
  const planets = data.steps.filter((s) => s.key.startsWith('graha_'))
  const houses = data.steps.filter((s) => s.key.startsWith('house'))
  const basics = data.steps.find((s) => s.key === 'basics')
  const Step = ({ s }) => (
    <div className="rp-step">
      <h5>{s.key.startsWith('house') ? `${s.key.slice(5)} · ` : ''}{s.title[L]}</h5>
      <ol className="sv-lines">{s.lines[L].map((x, i) => <li key={i}>{x}</li>)}</ol>
      {s.text && s.text[L].quote && (
        <p className="rp-quote"><i>{W('What the classical text says:', 'शास्त्र क्या कहता है:')}</i> “{s.text[L].quote}”</p>
      )}
      {refs && s.cite && <p className="fd-attr"><b>{s.cite}</b></p>}
    </div>
  )

  return createPortal(
    <div className="rp" role="document" aria-label={W('Full report', 'पूरी रिपोर्ट')}>
      <div className="rp-bar">
        <button type="button" className="go" onClick={() => window.print()}>{W('Save as PDF / Print', 'PDF सहेजें / प्रिंट करें')}</button>
        {hasBirth && (
          <label className="rp-check">
            <input type="checkbox" checked={dated} onChange={(e) => setDated(e.target.checked)} />
            {W('Include the birth details and the dated periods', 'जन्म-विवरण और तिथि वाली दशाएँ शामिल करें')}
          </label>
        )}
        <span className="rp-hint">{W('In the print window, choose “Save as PDF”. The report is made in this browser. Nothing is uploaded.', 'प्रिंट विंडो में “PDF के रूप में सहेजें” चुनें। रिपोर्ट इसी ब्राउज़र में बनती है। कुछ भी अपलोड नहीं होता।')}</span>
        <button type="button" className="rp-x" onClick={onClose}>{W('Close', 'बंद करें')}</button>
      </div>

      <article className="rp-page">
        <header className="rp-head">
          <span className="rp-brand">devashaa</span>
          <h1>{who}</h1>
          {dated && date && place ? <p>{date} · {time} · {place.name}</p> : <p>{W('Birth details not included.', 'जन्म-विवरण शामिल नहीं।')}</p>}
          <p className="rp-sub">{W('Vedic birth chart report', 'वैदिक जन्म कुंडली रिपोर्ट')} · {W('made on', 'तिथि')} {made} · devashaa.com</p>
        </header>

        <section className="rp-sec">
          <h2>{W('The chart', 'कुंडली')}</h2>
          <div className="rp-charts">
            <figure>
              <NorthDeckChart grahas={chart.grahas} lagnaRasi={chart.lagna_rasi} lagnaVargaSign={chart.lagna_vargas?.D1} vargaKey="D1" namer={namer} title={who} />
              <figcaption>{W('North Indian style', 'उत्तर भारतीय शैली')}</figcaption>
            </figure>
            <figure>
              <SouthDeckChart grahas={chart.grahas} lagnaRasi={chart.lagna_rasi} lagnaVargaSign={chart.lagna_vargas?.D1} vargaKey="D1" namer={namer}
                landmarks={chart.landmarks} lagnaLongitude={chart.lagna_longitude} gandanta={chart.gandanta} onHover={() => {}} title={who} />
              <figcaption>{W('South Indian style', 'दक्षिण भारतीय शैली')}</figcaption>
            </figure>
          </div>
          <div className="rp-two">
            <HighlightsCard chart={chart} grahas={chart.grahas} namer={namer} />
            <div className="dk-card">
              <h4 className="dk-head"><span>{W('Planetary positions', 'ग्रहों की स्थिति')}</span></h4>
              <div className="dk-body">
                <table className="rp-table">
                  <thead><tr><th>{W('Planet', 'ग्रह')}</th><th>{W('Sign', 'राशि')}</th><th>{W('Degree', 'अंश')}</th><th>{W('House', 'भाव')}</th><th>{W('Star · quarter', 'नक्षत्र · चरण')}</th></tr></thead>
                  <tbody>
                    {chart.grahas.map((g) => (
                      <tr key={g.key}>
                        <td>{(L === 'hi' ? namer : namer).grahaKey(g.key)}{g.retrograde ? ' ℞' : ''}</td>
                        <td>{namer.rasiFull(g.rasi)}</td>
                        <td>{g.degree}°{pad2(g.minute ?? 0)}′</td>
                        <td>{L === 'hi' ? g.bhava : EN_ORD(g.bhava)}</td>
                        <td>{g.nakshatra ? `${namer.nakshatra(g.nakshatra)} · ${g.nakshatra.pada}` : ''}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </section>

        <section className="rp-sec"><WhoCard chart={chart} namer={namer} refs={refs} /></section>

        <section className="rp-sec">
          <h2>{W('Your chart, explained simply', 'आपकी कुंडली, सरल शब्दों में')}</h2>
          {basics && <Step s={basics} />}
          <h3>{W('The nine planets', 'नौ ग्रह')}</h3>
          <div className="rp-cols">{planets.map((s) => <Step key={s.key} s={s} />)}</div>
          <h3>{W('The twelve houses', 'बारह भाव')}</h3>
          <div className="rp-cols">{houses.map((s) => <Step key={s.key} s={s} />)}</div>
        </section>

        {dated && hasBirth && (
          <section className="rp-sec"><DashaReading chart={chart} namer={namer} refs={refs} goFull={() => {}} report /></section>
        )}

        <section className="rp-sec">
          <h2>{W('Your life, area by area', 'आपका जीवन, क्षेत्र-दर-क्षेत्र')}</h2>
          {data.areas.map((A) => (
            <div className="rp-area" key={A.key}>
              <h3>{A.label[L]}</h3>
              <h6>{W('What your chart shows', 'आपकी कुंडली क्या दिखाती है')}</h6>
              {A.shows[L].map((s, i) => <p key={i}>{s}</p>)}
              {A.passages.length > 0 && <h6>{W('What the classical texts say', 'शास्त्रीय ग्रंथ क्या कहते हैं')}</h6>}
              {A.passages.map((t, i) => <Passage key={`${A.key}-${i}`} t={t} L={L} refs={refs} />)}
              {(A.supports[L].length > 0 || A.cautions[L].length > 0) && (
                <div className="fd-cols">
                  {A.supports[L].length > 0 && <div className="fd-group good"><h6>{W('Supporting', 'समर्थन में')}</h6><ul>{A.supports[L].map((s, i) => <li key={i}>{s}</li>)}</ul></div>}
                  {A.cautions[L].length > 0 && <div className="fd-group hard"><h6>{W('Counting against', 'विपरीत')}</h6><ul>{A.cautions[L].map((s, i) => <li key={i}>{s}</li>)}</ul></div>}
                </div>
              )}
              {(A.timing.now || A.timing.next) && (
                <>
                  <h6>{W('When it comes forward', 'यह कब आगे आता है')}</h6>
                  {A.timing.now && <p>{A.timing.now[L]}</p>}
                  {A.timing.next && <p>{A.timing.next[L]}</p>}
                </>
              )}
              <div className="la-notes">
                <h6>{W('What you can do: practical notes (ours, not from any text)', 'आप क्या कर सकते हैं: व्यावहारिक सुझाव (हमारे, किसी ग्रंथ के नहीं)')}</h6>
                <ul>{A.notes[L].map((s, i) => <li key={i}>{s}</li>)}</ul>
              </div>
            </div>
          ))}
        </section>

        <section className="rp-sec">
          <h2>{W('The findings, most important first', 'मुख्य बातें, सबसे महत्त्वपूर्ण पहले')}</h2>
          <p className="fd-held">{W('The texts’ statements are reported as theirs, not as facts about a life. The order is ours.', 'ग्रंथों के कथन उन्हीं के कथन के रूप में दिए गए हैं, जीवन के तथ्य के रूप में नहीं। क्रम हमारा है।')}</p>
          {data.findings.map(({ f }, i) => (
            <div className="rp-finding" key={f.key}>
              <h3>{i + 1}. {f.title[L]} <small>{TAGS[f.tag] ? TAGS[f.tag][L] : ''}</small></h3>
              <h6>{W('What your chart shows', 'आपकी कुंडली क्या दिखाती है')}</h6>
              {f.fact[L].map((s, k) => <p key={k}>{s}</p>)}
              {f.texts.length > 0 && <h6>{W('What the classical texts say', 'शास्त्रीय ग्रंथ क्या कहते हैं')}</h6>}
              {f.texts.map((t, k) => <Passage key={k} t={t} L={L} refs={refs} />)}
              {f.why[L].length > 0 && <h6>{W('How the placement is read', 'इस स्थिति को कैसे पढ़ा जाता है')}</h6>}
              {f.why[L].map((s, k) => <p key={k}>{s}</p>)}
              {(f.supports[L].length > 0 || f.cautions[L].length > 0 || f.measured[L].length > 0) && (
                <div className="fd-cols">
                  {f.supports[L].length > 0 && <div className="fd-group good"><h6>{W('Supporting', 'समर्थन में')}</h6><ul>{f.supports[L].map((s, k) => <li key={k}>{s}</li>)}</ul></div>}
                  {f.cautions[L].length > 0 && <div className="fd-group hard"><h6>{W('Counting against', 'विपरीत')}</h6><ul>{f.cautions[L].map((s, k) => <li key={k}>{s}</li>)}</ul></div>}
                  {f.measured[L].length > 0 && <div className="fd-group"><h6>{W('Measured', 'मापा गया')}</h6><ul>{f.measured[L].map((s, k) => <li key={k}>{s}</li>)}</ul></div>}
                </div>
              )}
              {f.inference && (
                <div className="rp-infer">
                  <h6>{W('Our inference, not a statement of any text', 'हमारा अनुमान, किसी ग्रंथ का कथन नहीं')}</h6>
                  <ol>{f.inference.chain.map((c, k) => <li key={k}>{c.line[L]}{refs && c.cite ? ` (${c.cite})` : ''}</li>)}</ol>
                  <p>{f.inference.conclusion[L]}</p>
                </div>
              )}
            </div>
          ))}
        </section>

        <footer className="rp-foot">
          <p>{W('A chart shows tendencies, not fixed events. This report prescribes no ritual, gem or charity, and it is not medical, legal or financial advice.', 'कुंडली प्रवृत्ति दिखाती है, तय घटनाएँ नहीं। यह रिपोर्ट कोई अनुष्ठान, रत्न या दान नहीं बताती, और यह चिकित्सा, कानूनी या वित्तीय सलाह नहीं है।')}</p>
          <p>devashaa.com · {made}</p>
        </footer>
      </article>
    </div>,
    document.body,
  )
}
