/**
 * "What would you like to understand?" — the chart's findings in reading order,
 * each one opening into: what the chart shows · what the classical texts say ·
 * why each rule applies · what else must be considered · the exact references ·
 * and, labelled as ours, an inference with its chain. See findings.js for what a
 * finding may say. A topic re-sorts the same findings; the chart does not change.
 *
 * References (Settings › References) decide whether the book, the translator and
 * the chapter-and-verse are printed beside each passage. Off — the default — a
 * passage is still marked as a classical text's statement, never as ours; on, it
 * carries its exact source, the tiers are named and the references are listed.
 */
import { useMemo, useState } from 'react'
import { useLang } from './LangContext.jsx'
import { buildFindings, rankFindings, TOPICS, TAGS } from './findings.js'
import { HOUSE } from './walkthrough.js'

const TOP = 5
const pad2 = (n) => String(n).padStart(2, '0')
const TIER = {
  sloka: { en: 'Bṛhat Parāśara Horā Śāstra', hi: 'बृहत् पाराशर होरा शास्त्र' },
  jaimini: { en: 'Jaimini', hi: 'जैमिनि' },
  classical: { en: 'Other classical texts', hi: 'अन्य शास्त्रीय ग्रंथ' },
  modern: { en: 'Modern authors (kept apart)', hi: 'आधुनिक लेखक (अलग रखे गए)' },
}
const TIER_ORDER = ['sloka', 'jaimini', 'classical', 'modern']

function Group({ title, items, tone }) {
  if (!items.length) return null
  return (
    <div className={`fd-group ${tone || ''}`}>
      <h6>{title}</h6>
      <ul>{items.map((s, i) => <li key={i}>{s}</li>)}</ul>
    </div>
  )
}

/** "Sārāvalī 30.11 — Kalyāṇa Varma, tr. R. Santhanam" */
const attribution = (t) => [t.cite || (t.source && t.source.text), t.source && [t.source.author, t.source.translator && `tr. ${t.source.translator}`].filter(Boolean).join(', ')].filter(Boolean).join(' — ')

export function Passage({ t, L, refs }) {
  const W = (en, hi) => (L === 'hi' ? hi : en)
  // A passage that also speaks of a loss, a death or a partner's fidelity is shown only when the reader asks for
  // it — and then whole, never with the hard clause cut out (a verse's good and bad halves belong together).
  const [asked, setAsked] = useState(false)
  const body = t.says || (asked ? t.full : null)
  return (
    <div className="fd-passage">
      {body
        ? <blockquote>{body}</blockquote>
        : (
          <p className="fd-held">
            {W('This passage matches your chart. Part of it speaks of a death, a lifespan, a bereavement or a partner’s fidelity, so it is not shown unasked. It is an old text’s statement about a placement, not a forecast for you.', 'यह पाठ आपकी कुंडली पर लागू होता है। इसका एक अंश मृत्यु, आयु, वियोग या जीवनसाथी की निष्ठा की बात करता है, इसलिए बिना पूछे नहीं दिखाया जाता। यह एक पुराने ग्रंथ का एक स्थिति पर कथन है, आपके लिए भविष्यवाणी नहीं।')}
            {t.full && <> <button type="button" className="sv-link" onClick={() => setAsked(true)}>{W('Show the whole passage', 'पूरा पाठ दिखाएँ')}</button></>}
          </p>
        )}
      {refs && (
      <p className="fd-attr">
        <b>{attribution(t)}</b>
        {body && <span>{t.kind === 'rendering' ? W(' · our rendering of the cited passage', ' · उद्धृत पाठ का हमारा भावार्थ') : W(' · the translator’s words', ' · अनुवादक के शब्द')}</span>}
      </p>
      )}
      <p className="fd-applies"><i>{W('Why it applies:', 'यह क्यों लागू है:')}</i> {t.applies[L]}</p>
      {t.qualifier && t.qualifier[L] && <p className="fd-applies"><i>{W('Which part applies:', 'कौन-सा भाग लागू है:')}</i> {t.qualifier[L]}</p>}
      {t.exception && <p className="fd-applies"><i>{W('The text’s own exception for this ascendant:', 'इस लग्न के लिए पाठ का अपना अपवाद:')}</i> {t.exception}</p>}
    </div>
  )
}

function Finding({ n, f, because, L, open, onToggle, goFull, refs }) {
  const W = (en, hi) => (L === 'hi' ? hi : en)
  const tag = TAGS[f.tag] || TAGS.plain
  const byTier = TIER_ORDER.map((tier) => [tier, f.texts.filter((t) => t.tier === tier)]).filter(([, xs]) => xs.length)
  const refList = [...new Set([...f.texts.map(attribution), ...(f.inference ? f.inference.chain.map((c) => c.cite) : [])].filter(Boolean))]
  return (
    <li className={`fd-item${open ? ' open' : ''}`}>
      <button type="button" className="fd-row" aria-expanded={open} onClick={onToggle}>
        <span className="fd-n">{pad2(n)}</span>
        <span className="fd-main">
          <b>{f.title[L]}</b>
          <small>{because ? `${f.sub[L]} · ${because[L]}` : f.sub[L]}</small>
        </span>
        <span className={`fd-tag ${tag.tone}`}>{tag[L]}</span>
        <span className="fd-caret" aria-hidden="true">{open ? '−' : '+'}</span>
      </button>
      {open && (
        <div className="fd-body">
          <div className="fd-step">
            <h6>{W('What your chart shows', 'आपकी कुंडली क्या दिखाती है')}</h6>
            {f.fact[L].map((s, i) => <p key={i}>{s}</p>)}
          </div>

          <div className="fd-step">
            <h6>{W('What the classical texts say', 'शास्त्रीय ग्रंथ क्या कहते हैं')}</h6>
            {byTier.length === 0 && (
              <p className="fd-held">{W('No passage in the registered library speaks of this placement directly, so none is offered.', 'पंजीकृत ग्रंथों में इस स्थिति पर सीधे कोई पाठ नहीं है, इसलिए कोई नहीं दिया गया।')}</p>
            )}
            {byTier.map(([tier, xs]) => (
              <div key={tier} className={`fd-tier fd-tier--${tier}`}>
                {refs && <div className="fd-tier-name">{TIER[tier][L]}</div>}
                {xs.map((t, i) => <Passage key={i} t={t} L={L} refs={refs} />)}
              </div>
            ))}
            {byTier.length > 0 && (
              <p className="fd-held">{W('These are the texts’ statements, some of them many centuries old. They are reported here as what each text says about this placement, not as facts about your life.', 'ये ग्रंथों के कथन हैं, जिनमें कुछ सदियों पुराने हैं। इन्हें यहाँ इस रूप में दिया गया है कि हर ग्रंथ इस स्थिति के बारे में क्या कहता है, आपके जीवन के तथ्य के रूप में नहीं।')}</p>
            )}
          </div>

          <div className="fd-step">
            <h6>{W('How the placement is read', 'यह स्थिति कैसे पढ़ी जाती है')}</h6>
            {f.why[L].map((s, i) => <p key={i}>{s}</p>)}
          </div>

          <div className="fd-step">
            <h6>{W('What other factors must be considered', 'और किन बातों पर विचार ज़रूरी है')}</h6>
            <div className="fd-cols">
              <Group tone="good" title={W('Supporting', 'समर्थन में')} items={f.supports[L]} />
              <Group tone="hard" title={W('Counting against', 'विपरीत')} items={f.cautions[L]} />
              <Group title={W('Measured', 'मापा गया')} items={f.measured[L]} />
            </div>
            <div className="fd-check-row">
              <span className="fd-check-label">{W('Still to evaluate:', 'अभी जाँचना बाकी:')}</span>
              {f.check.map((c, i) => (
                <button type="button" key={i} onClick={() => goFull(c.go)}>{c.label[L]} →</button>
              ))}
            </div>
          </div>

          {f.inference && (
            <div className="fd-step fd-infer">
              <h6>{W('Our inference, not a statement of any text', 'हमारा अनुमान, किसी ग्रंथ का कथन नहीं')}</h6>
              <ol>
                {f.inference.chain.map((c, i) => <li key={i}>{c.line[L]}{refs && c.cite ? <span className="fd-cite"> [{c.cite}]</span> : null}</li>)}
              </ol>
              <p><b>{W('Therefore:', 'इसलिए:')}</b> {f.inference.conclusion[L]}</p>
            </div>
          )}

          {refs && refList.length > 0 && (
            <div className="fd-step fd-refs">
              <h6>{W('Exact textual references', 'सटीक ग्रंथ-संदर्भ')}</h6>
              <ul>{refList.map((r, i) => <li key={i}>{r}</li>)}</ul>
            </div>
          )}
        </div>
      )}
    </li>
  )
}

export default function FindingsPanel({ chart, namer, onHouse, goFull, refs }) {
  const { lang } = useLang()
  const L = lang === 'hi' ? 'hi' : 'en'
  const W = (en, hi) => (L === 'hi' ? hi : en)
  const [topic, setTopic] = useState('overall')
  const [open, setOpen] = useState(null)
  const [all, setAll] = useState(false)
  const built = useMemo(() => {
    try { return buildFindings(chart, namer) } catch { return null }
  }, [chart, namer.style])  // eslint-disable-line react-hooks/exhaustive-deps
  const ranked = useMemo(() => (built ? rankFindings(built, topic) : []), [built, topic])
  if (!built || !built.findings.length) return null
  const T = TOPICS.find((t) => t.key === topic)
  const shown = all ? ranked : ranked.slice(0, TOP)
  const bh = (chart.analysis && chart.analysis.bhava_phala && chart.analysis.bhava_phala.bhavas) || []
  const pick = (t) => { setTopic(t); setOpen(null); setAll(false) }
  const toggle = (f) => {
    const next = open === f.key ? null : f.key
    setOpen(next)
    if (next && f.house && onHouse) onHouse(f.house)
  }

  return (
    <section className="dk-card sv-find">
      <h4 className="dk-head">
        <span>{W('What would you like to understand?', 'आप क्या समझना चाहेंगे?')}</span>
      </h4>
      <div className="dk-body">
        <div className="fd-topics" role="tablist">
          {TOPICS.map((t) => (
            <button type="button" key={t.key} role="tab" aria-selected={topic === t.key}
                    className={topic === t.key ? 'on' : ''} onClick={() => pick(t.key)}>
              <b>{t.label[L]}</b><small>{t.sub[L]}</small>
            </button>
          ))}
          <button type="button" className="fd-full" onClick={() => goFull('full')}>
            <b>{W('Complete technical analysis', 'पूरा तकनीकी विश्लेषण')}</b><small>{W('every table and timeline →', 'हर तालिका और समय-रेखा →')}</small>
          </button>
        </div>

        <div className="fd-headline">
          <h5>
            {topic === 'overall' ? W('Findings worth exploring', 'देखने योग्य मुख्य बातें')
              : topic === 'timing' ? W('The planets whose periods are running', 'जिन ग्रहों की दशा चल रही है')
                : `${T.label[L]}: ${W('what touches it in your chart', 'आपकी कुंडली में इससे जुड़ी बातें')}`}
          </h5>
          <span className="sv-tag">{W('in reading order', 'पढ़ने के क्रम में')}</span>
        </div>
        {T.houses.length > 0 && (
          <p className="sv-note">
            {T.houses.map((h) => {
              const b = bh.find((x) => x.house === h)
              return W(
                `Your ${h}${h === 1 ? 'st' : h === 2 ? 'nd' : h === 3 ? 'rd' : 'th'} house (${HOUSE[h].chip.en})${b ? ` is ${namer.rasiFull ? namer.rasiFull(b.sign) : namer.rasi(b.sign)}, ruled by ${namer.grahaKey(b.lord)}` : ''}.`,
                `आपका ${h}वाँ भाव (${HOUSE[h].chip.hi})${b ? ` ${namer.rasi(b.sign)} राशि है; इसके स्वामी ${namer.grahaKey(b.lord)} हैं` : ''}।`)
            }).join(' ')}
          </p>
        )}
        {topic === 'timing' && ranked.length > 0 && (
          <p className="sv-note">
            {W('Each running lord’s finding includes the text’s verdict on its period (BPHS Vol II ch.47). The text’s detailed results for each sub-period (chs 52 to 60) are in the full analysis.', 'हर चल रहे दशा-स्वामी की बात में उसकी दशा पर ग्रंथ का निर्णय (बृहत् पाराशर, खंड 2, अध्याय 47) शामिल है। हर अन्तर्दशा के विस्तृत फल (अध्याय 52 से 60) पूरे विश्लेषण में हैं।')}
            {' '}<button type="button" className="sv-link" onClick={() => goFull('dasha')}>{W('Open the daśā results →', 'दशा-फल खोलें →')}</button>
          </p>
        )}
        {topic === 'timing' && !ranked.length && (
          <p className="sv-note">{W('This chart was shared without its birth details, so it has no periods to show.', 'यह कुंडली जन्म-विवरण के बिना साझा हुई है, इसलिए इसमें दशा नहीं है।')}</p>
        )}

        <ol className="fd-list">
          {shown.map(({ f, because }, i) => (
            <Finding key={f.key} n={i + 1} f={f} because={because} L={L}
                     open={open === f.key} onToggle={() => toggle(f)} goFull={goFull} refs={!!refs} />
          ))}
        </ol>
        {ranked.length > TOP && (
          <button type="button" className="sv-link" onClick={() => setAll((x) => !x)}>
            {all ? W('Show the first five', 'पहली पाँच दिखाएँ') : W(`Show all ${ranked.length}`, `सभी ${ranked.length} दिखाएँ`)}
          </button>
        )}
        {!refs && (
          <p className="fd-foot">{W('Book names, chapter-and-verse and page numbers are hidden. Turn on References in Settings to see the exact source of every passage.', 'ग्रंथों के नाम, अध्याय-श्लोक और पृष्ठ संख्या छिपी हैं। हर पाठ का सटीक स्रोत देखने के लिए सेटिंग में “संदर्भ” चालू करें।')}</p>
        )}
        <p className="fd-foot">
          {W('Each finding gives what your chart shows, what the registered classical texts say about it, and the factors that qualify it. The texts’ statements are reported as theirs, not as facts about a life. The order is ours, a way to decide what to read first. The texts do not rank placements.',
            'हर बात में दिया है कि आपकी कुंडली क्या दिखाती है, पंजीकृत शास्त्रीय ग्रंथ उस पर क्या कहते हैं, और कौन-सी बातें उसे सीमित करती हैं। ग्रंथों के कथन उन्हीं के कथन के रूप में दिए गए हैं, जीवन के तथ्य के रूप में नहीं। क्रम हमारा है। यह तय करने का तरीका है कि पहले क्या पढ़ें। शास्त्र स्थितियों को क्रम नहीं देते।')}
        </p>
      </div>
    </section>
  )
}
