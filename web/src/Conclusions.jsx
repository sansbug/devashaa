/**
 * "What this means for you" — the first thing under the chart (and in the report): the chart's conclusions in
 * a few plain sentences, each with the readings it rests on. See conclusions.js for the rule: a conclusion is
 * stated only when the separate readings agree.
 *
 * The site's own weighted projection is one of the voices. It is fetched from /api/matrix when the birth
 * details are on the page; without them (a chart shared without its birth details) the other voices decide.
 */
import { useEffect, useMemo, useState } from 'react'
import { useLang } from './LangContext.jsx'
import { buildConclusions, GROUP_OF } from './conclusions.js'
import { buildDashaReading } from './dashareading.js'
import { API } from './config.js'

const TONE = { good: 'good', care: 'hard', mixed: 'mixed', quiet: 'plain' }

export default function Conclusions({ chart, namer, date, time, place, onArea, open = false }) {
  const { lang } = useLang()
  const L = lang === 'hi' ? 'hi' : 'en'
  const W = (en, hi) => (L === 'hi' ? hi : en)
  const [matrix, setMatrix] = useState(null)
  const lat = place && place.latitude, lon = place && place.longitude, tz = place && place.timezone
  useEffect(() => {
    setMatrix(null)
    if (!date || !time || lat == null || lon == null) return undefined
    let dead = false
    fetch(`${API}/api/matrix`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ date, time, latitude: lat, longitude: lon, timezone: tz }),
    })
      .then((r) => (r.ok ? r.json() : null))
      .then((j) => { if (!dead && j && !j.error && Array.isArray(j.bhavas)) setMatrix({ bhavas: j.bhavas.map((b) => ({ house: b.house, net: b.net })) }) })
      .catch(() => { /* the other readings stand without it */ })
    return () => { dead = true }
  }, [date, time, lat, lon, tz])

  const C = useMemo(() => {
    try {
      let dasha = null
      try { dasha = buildDashaReading(chart, namer) } catch { dasha = null }
      return buildConclusions(chart, matrix, dasha)
    } catch { return null }
  }, [chart, matrix, namer.style])  // eslint-disable-line react-hooks/exhaustive-deps
  if (!C) return null

  const Group = ({ v, title }) => (C.groups[v].length === 0 ? null : (
    <div className={`cn-group cn-${TONE[v]}`}>
      <h6>{title}</h6>
      {C.groups[v].map((x) => (
        <div className="cn-item" key={x.key}>
          <p className="cn-head">
            {onArea ? <button type="button" className="cn-link" onClick={() => onArea(x.key)}>{x.head[L]}</button> : x.head[L]}
          </p>
          {x.reasons[L].length > 0 && <ul>{x.reasons[L].map((s, i) => <li key={i}>{s}</li>)}</ul>}
        </div>
      ))}
    </div>
  ))

  return (
    <section className="dk-card cn-card" id="conclusions">
      <h4 className="dk-head"><span>{W('What this means for you', 'आपके लिए इसका अर्थ')}</span></h4>
      <div className="dk-body">
        <p className="cn-summary">{C.summary[L]}</p>
        <div className="cn-grid">
          <Group v="good" title={W('Your strengths', 'आपके बल')} />
          <Group v="care" title={W('Where to take care', 'जहाँ सावधानी चाहिए')} />
          <Group v="mixed" title={W('Where the chart is mixed', 'जहाँ कुंडली मिली-जुली है')} />
          <Group v="quiet" title={W('Where the chart says little', 'जहाँ कुंडली कम कहती है')} />
        </div>
        <details className="cn-houses" open={open}>
          <summary>{W('House by house: all twelve', 'भाव-दर-भाव: सभी बारह')}</summary>
          <div className="cn-hgrid">
            {C.houses.map((x) => (
              <div className={`cn-house cn-${TONE[GROUP_OF[x.verdict]]}`} key={x.key}>
                <p className="cn-head">{x.head[L]}</p>
                {x.reasons[L].length > 0 && <ul>{x.reasons[L].map((s, i) => <li key={i}>{s}</li>)}</ul>}
                {x.note && <p className="fd-held">{x.note[L]}</p>}
              </div>
            ))}
          </div>
        </details>
        {C.now && C.now[L].length > 0 && (
          <div className="cn-now">
            <h6>{W('Now and next', 'अभी और आगे')}</h6>
            <ul>{C.now[L].map((s, i) => <li key={i}>{s}</li>)}</ul>
          </div>
        )}
        {C.act[L].length > 0 && (
          <div className="cn-now la-notes">
            <h6>{W('What you can do (our notes, not from any text)', 'आप क्या कर सकते हैं (हमारे सुझाव, किसी ग्रंथ के नहीं)')}</h6>
            <ul>{C.act[L].map((s, i) => <li key={i}>{s}</li>)}</ul>
          </div>
        )}
        <p className="fd-held">{C.rule[L]}{C.usedProjection ? '' : ` ${W('Our weighted projection is not part of this summary for this chart.', 'इस कुंडली के इस सार में हमारा भारित प्रक्षेपण शामिल नहीं है।')}`}</p>
      </div>
    </section>
  )
}
