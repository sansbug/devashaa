/**
 * "Your periods (daśā): now, next, and what it means" — the simple view's daśā
 * reading. See dashareading.js for what each part may say: the verse is the
 * text's; the changes and the practical notes are ours and are labelled so.
 *
 * The running and the next sub-period also carry the text's own result lists
 * (BPHS Vol II chs 52-60), fetched from /api/antardasa/plain: only the branches
 * whose conditions this chart meets, shown as the text's words. A list that
 * speaks of a death, a lifespan or a bereavement is shown only on request, whole.
 */
import { useEffect, useMemo, useState } from 'react'
import { useLang } from './LangContext.jsx'
import { Bubble } from './DashaGlyphs.jsx'
import { buildDashaReading } from './dashareading.js'
import { SENSITIVE } from './findings.js'
import { API } from './config.js'

const sensitive = (s) => SENSITIVE.en.test(String(s || '')) || SENSITIVE.hi.test(String(s || ''))

/** One branch of the text's sub-period section that this chart meets. */
function Branch({ b, L }) {
  const W = (en, hi) => (L === 'hi' ? hi : en)
  const [asked, setAsked] = useState(false)
  const held = sensitive(b.results)
  return (
    <div className="dsr-branch">
      {held && !asked ? (
        <p className="fd-held">
          {W('The text’s list for this branch speaks of a death, a lifespan or a bereavement, so it is not shown unasked.', 'इस शाखा की सूची मृत्यु, आयु या वियोग की बात करती है, इसलिए बिना पूछे नहीं दिखाई जाती।')}
          {' '}<button type="button" className="sv-link" onClick={() => setAsked(true)}>{W('Show the whole list', 'पूरी सूची दिखाएँ')}</button>
        </p>
      ) : <blockquote>{b.results}</blockquote>}
      <p className="fd-applies">
        <i>{W('Applies because the sub-period’s planet is', 'लागू है क्योंकि अन्तर्दशा का ग्रह')}</i>{' '}
        {b.met.map((m) => m.predicate).join(W('; and ', '; और '))}.
        {b.polarity_word ? <> {W('The text’s own word for this branch:', 'इस शाखा के लिए ग्रंथ का अपना शब्द:')} “{b.polarity_word}”.</> : null}
      </p>
    </div>
  )
}

function SubResults({ cell, L, refs }) {
  const W = (en, hi) => (L === 'hi' ? hi : en)
  if (!cell) return null
  const c = cell.counts
  return (
    <div className="dsr-sub">
      <h6>{W('What the text lists for this sub-period', 'इस अन्तर्दशा के लिए ग्रंथ क्या गिनाता है')}</h6>
      {cell.applies.length === 0 && (
        <p className="fd-held">{W('None of the branches the text lists for this sub-period could be confirmed for your chart.', 'इस अन्तर्दशा के लिए ग्रंथ की कोई शाखा आपकी कुंडली पर पक्की नहीं हो सकी।')}</p>
      )}
      {cell.applies.map((b, i) => <Branch key={i} b={b} L={L} />)}
      {refs && <p className="fd-attr"><b>{cell.citation} — Parāśara, tr. R. Santhanam</b></p>}
      <p className="fd-held">
        {W(`Of the ${c.branches} branches the text gives here, ${c.apply} ${c.apply === 1 ? 'applies' : 'apply'} to your chart`, `ग्रंथ की ${c.branches} शाखाओं में से ${c.apply} आपकी कुंडली पर लागू`)}
        {c.not_met ? W(`, ${c.not_met} ${c.not_met === 1 ? 'does' : 'do'} not`, `, ${c.not_met} नहीं`) : ''}
        {c.undetermined ? W(`, and ${c.undetermined} could not be checked (they turn on a navāṁśa, an aspect or a house the text counts from no stated point)`, `, और ${c.undetermined} जाँची नहीं जा सकीं (वे नवांश, दृष्टि या ऐसे भाव पर टिकी हैं जिसकी गिनती का आधार ग्रंथ नहीं बताता)`) : ''}
        {W('. These are the text’s lists of what such a period can bring, not a verdict and not a forecast.', '। ये ग्रंथ की सूचियाँ हैं कि ऐसी दशा क्या ला सकती है — निर्णय या भविष्यवाणी नहीं।')}
      </p>
    </div>
  )
}

export default function DashaReading({ chart, namer, refs, goFull }) {
  const { lang } = useLang()
  const L = lang === 'hi' ? 'hi' : 'en'
  const W = (en, hi) => (L === 'hi' ? hi : en)
  const [how, setHow] = useState(false)
  const [cells, setCells] = useState({})
  const R = useMemo(() => {
    try { return buildDashaReading(chart, namer) } catch { return null }
  }, [chart, namer.style])  // eslint-disable-line react-hooks/exhaustive-deps

  // the text's result lists for the running and the next sub-period
  const pairs = useMemo(() => (R ? R.rows.filter((r) => (r.role === 'antar' || r.role === 'nextAntar') && r.within).map((r) => ({ role: r.role, maha: r.within, antar: r.lord })) : []), [R])
  const pairKey = pairs.map((p) => `${p.maha}-${p.antar}`).join('|')
  useEffect(() => {
    if (!pairs.length) { setCells({}); return undefined }
    let dead = false
    const positions = Object.fromEntries((chart.grahas || []).map((g) => [g.key, { rasi: g.rasi, longitude: g.longitude }]))
    fetch(`${API}/api/antardasa/plain`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pairs: pairs.map(({ maha, antar }) => ({ maha, antar })), positions, lagna: chart.lagna_rasi }),
    })
      .then((r) => (r.ok ? r.json() : null))
      .then((j) => {
        if (dead || !j || !Array.isArray(j.cells)) return
        setCells(Object.fromEntries(pairs.map((p, i) => [p.role, j.cells[i]]).filter(([, c]) => c)))
      })
      .catch(() => { /* the reading stands without the lists */ })
    return () => { dead = true }
  }, [pairKey, lang, refs])  // eslint-disable-line react-hooks/exhaustive-deps

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
      <SubResults cell={cells[r.role]} L={L} refs={refs} />
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
            <h6>{W('The classical rule for judging a period', 'दशा आँकने का शास्त्रीय नियम')}</h6>
            <div className="fd-passage">
              <blockquote>{R.rule.verse}</blockquote>
              {refs && <p className="fd-attr"><b>{R.rule.cite} — Parāśara, tr. R. Santhanam</b></p>}
              <p className="fd-applies">{W('It is read from where each period’s planet stood at your birth. It says whether a period counts as favourable or not. It does not say what happens in it.', 'इसे जन्म के समय हर दशा के ग्रह की स्थिति से पढ़ा जाता है। यह बताता है कि दशा अनुकूल गिनी जाए या नहीं; उसमें क्या घटता है, यह नहीं बताता।')}</p>
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
          {W('The full analysis has every sub-period of every main period, with each condition the text lists and whether it could be evaluated.', 'पूरे विश्लेषण में हर महादशा की हर अन्तर्दशा है — ग्रंथ की हर शर्त के साथ, और यह भी कि वह जाँची जा सकी या नहीं।')}
          {' '}<button type="button" className="sv-link" onClick={goFull}>{W('Open the full daśā timeline →', 'पूरी दशा समय-रेखा खोलें →')}</button>
        </p>
      </div>
    </section>
  )
}
