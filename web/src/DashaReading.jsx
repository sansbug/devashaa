/**
 * "Your periods (daśā): now, next, and what it means" — the simple view's daśā
 * reading. See dashareading.js for what each part may say: the verse is the
 * text's; the changes and the practical notes are ours and are labelled so.
 */
import { useMemo, useState } from 'react'
import { useLang } from './LangContext.jsx'
import { Bubble } from './DashaGlyphs.jsx'
import { buildDashaReading } from './dashareading.js'

export default function DashaReading({ chart, namer, refs, goFull }) {
  const { lang } = useLang()
  const L = lang === 'hi' ? 'hi' : 'en'
  const W = (en, hi) => (L === 'hi' ? hi : en)
  const [how, setHow] = useState(false)
  const R = useMemo(() => {
    try { return buildDashaReading(chart, namer) } catch { return null }
  }, [chart, namer.style])  // eslint-disable-line react-hooks/exhaustive-deps
  if (!R) return null
  const now = R.rows.filter((r) => r.role === 'maha' || r.role === 'antar')
  const next = R.rows.filter((r) => r.role === 'nextAntar' || r.role === 'nextMaha')
  const Row = ({ r }) => (
    <div className={`dsr-row dsr-${r.verdict.tone}`}>
      <div className="dsr-row-head">
        <Bubble lord={r.lord} size="m" />
        <span><b>{r.title[L]}</b><small>{r.span[L]}</small></span>
      </div>
      <p>{r.brings[L]}</p>
      <p className="dsr-verdict">{r.verdict.line[L]}</p>
    </div>
  )

  return (
    <section className="dk-card sv-dasha">
      <h4 className="dk-head">
        <span>{W('Your periods (daśā): now, next, and what it means', 'आपकी दशाएँ: अभी, आगे, और इसका अर्थ')}</span>
      </h4>
      <div className="dk-body">
        <div className="la-step">
          <h6>{W('How to read a daśā', 'दशा कैसे पढ़ें')}</h6>
          <p>{R.how[L][0]}</p>
          {how && R.how[L].slice(1).map((s, i) => <p key={i}>{s}</p>)}
          <button type="button" className="sv-link" onClick={() => setHow((x) => !x)}>{how ? W('Show less', 'कम दिखाएँ') : W('How periods nest, and how one is judged', 'दशाएँ कैसे चलती हैं और कैसे आँकी जाती हैं')}</button>
        </div>

        <div className="dsr-grid">
          <div className="la-step">
            <h6>{W('Running now', 'अभी चल रही')}</h6>
            {now.map((r) => <Row key={r.role} r={r} />)}
          </div>
          <div className="la-step">
            <h6>{W('What comes next', 'आगे क्या आता है')}</h6>
            {next.map((r) => <Row key={r.role} r={r} />)}
            {!next.length && <p className="fd-held">{W('No later period falls within the calculated span.', 'गणना की अवधि में कोई आगामी दशा नहीं है।')}</p>}
          </div>
        </div>

        {R.rule && (
          <div className="la-step">
            <h6>{W('The text’s rule for judging a period', 'दशा आँकने का ग्रंथ का नियम')}</h6>
            <div className="fd-passage">
              <blockquote>{R.rule.verse}</blockquote>
              {refs && <p className="fd-attr"><b>{R.rule.cite} — Parāśara, tr. R. Santhanam</b></p>}
              <p className="fd-applies">{W('It is read from where each period’s planet stood at your birth. It judges the lean of a period, not what happens in it.', 'इसे जन्म के समय हर दशा के ग्रह की स्थिति से पढ़ा जाता है। यह दशा का झुकाव आँकता है, उसमें क्या घटता है, यह नहीं।')}</p>
            </div>
          </div>
        )}

        <div className="dsr-grid">
          <div className="la-step">
            <h6>{W('What is going to change', 'क्या बदलने वाला है')}</h6>
            <ul className="sv-lines">{R.changes[L].map((s, i) => <li key={i}>{s}</li>)}</ul>
          </div>
          <div className="la-step la-notes">
            <h6>{W('How it affects you — practical notes (ours, not from any text)', 'आप पर इसका असर — व्यावहारिक सुझाव (हमारे, किसी ग्रंथ के नहीं)')}</h6>
            <ul>{R.notes[L].map((s, i) => <li key={i}>{s}</li>)}</ul>
            <details className="la-basis">
              <summary>{W('What these notes rest on', 'ये सुझाव किस पर टिके हैं')}</summary>
              <ol>{R.basis[L].map((s, i) => <li key={i}>{s}</li>)}</ol>
              <p>{W('They are about attention, planning and timing. They are not medical, legal or financial advice, and this site prescribes no ritual, gem or charity.', 'ये ध्यान, योजना और समय के बारे में हैं। ये चिकित्सा, कानूनी या वित्तीय सलाह नहीं हैं, और यह साइट कोई अनुष्ठान, रत्न या दान नहीं बताती।')}</p>
            </details>
          </div>
        </div>

        <p className="fd-foot">
          {W('The texts also list detailed results for each sub-period. Those are conditions that fire one by one and carry no overall verdict, so they are kept in the full analysis.', 'ग्रंथ हर अन्तर्दशा के विस्तृत फल भी देते हैं। वे एक-एक करके लागू होने वाली शर्तें हैं और उनका कोई समग्र निर्णय नहीं होता, इसलिए वे पूरे विश्लेषण में रखे गए हैं।')}
          {' '}<button type="button" className="sv-link" onClick={goFull}>{W('Open the full daśā timeline →', 'पूरी दशा समय-रेखा खोलें →')}</button>
        </p>
      </div>
    </section>
  )
}
