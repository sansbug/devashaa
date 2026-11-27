/**
 * "Summary, area by area" — the life areas as a few plain paragraphs (areasummary.js has the rules). Each
 * paragraph carries a small label saying what it is: from the chart, the text's own words, timing, or ours.
 */
import { useMemo, useState } from 'react'
import { useLang } from './LangContext.jsx'
import { buildFindings } from './findings.js'
import { buildAreaSummary, KIND } from './areasummary.js'

const FIRST = 3

export default function AreaSummary({ chart, namer, refs, report = false }) {
  const { lang } = useLang()
  const L = lang === 'hi' ? 'hi' : 'en'
  const W = (en, hi) => (L === 'hi' ? hi : en)
  const [all, setAll] = useState(false)
  const areas = useMemo(() => {
    try { return buildAreaSummary(chart, buildFindings(chart, namer), namer) } catch { return null }
  }, [chart, namer.style])  // eslint-disable-line react-hooks/exhaustive-deps
  if (!areas || !areas.length) return null
  const shown = all || report ? areas : areas.slice(0, FIRST)

  return (
    <section className="dk-card as-card">
      <h4 className="dk-head">
        <span>{W('Summary, area by area', 'सारांश, क्षेत्र-दर-क्षेत्र')}</span>
        <span className="dk-head-right">{W('each line says where it comes from', 'हर पंक्ति बताती है कि वह कहाँ से है')}</span>
      </h4>
      <div className="dk-body">
        {shown.map((A) => (
          <div className="as-area" key={A.key}>
            <h5>{A.label[L]}{A.now ? <span className="as-now">{W('in focus now', 'अभी केंद्र में')}</span> : null}</h5>
            {A.paras.map((p, i) => (
              <p key={i} className={'as-p as-' + p.kind}>
                <span className="as-kind">{KIND[p.kind][L]}</span>
                {p[L]}
                {(p.kind === 'text' || p.kind === 'rendered') && p.cite && refs ? <small className="as-cite"> {p.cite}{p.source && p.source.translator ? (p.kind === 'text' ? `, tr. ${p.source.translator}` : `; ${p.source.translator}`) : ''}</small> : null}
              </p>
            ))}
          </div>
        ))}
        {!report && areas.length > FIRST && (
          <button type="button" className="sv-link" onClick={() => setAll((x) => !x)}>
            {all ? W('Show less', 'कम दिखाएँ') : W(`Show the other ${areas.length - FIRST} areas`, `बाकी ${areas.length - FIRST} क्षेत्र दिखाएँ`)}
          </button>
        )}
        <p className="fd-held">{W('A chart shows tendencies, not fixed events. The texts’ words are theirs; how the factors lean is our reading.', 'कुंडली प्रवृत्ति दिखाती है, तय घटनाएँ नहीं। ग्रंथों के शब्द उनके हैं; बातें किस ओर झुकती हैं, यह हमारी व्याख्या है।')}</p>
      </div>
    </section>
  )
}
