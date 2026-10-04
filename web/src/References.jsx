/**
 * /references — the source registry and the one switch that puts the
 * chapter-and-verse references back on the site.
 *
 * The readings on the site are drawn from named texts and every one of them
 * still carries its locus in the data — cite-or-refuse is unchanged. What
 * changed is the default view: the references are hidden unless this switch
 * is on, so a reader meets the reading, not the footnote. The switch is a
 * per-browser preference (localStorage "refs"); nothing is sent anywhere.
 */
import { useEffect, useState } from 'react'

export const REFS_KEY = 'refs'
export const refsOn = () => { try { return localStorage.getItem(REFS_KEY) === '1' } catch { return false } }
export const applyRefs = (on) => { document.documentElement.dataset.refs = on ? '1' : '0' }

const SOURCES = [
  ['Bṛhat Parāśara Horā Śāstra', 'Parāśara', 'received text', 'R. Santhanam (Ranjan)', 'the backbone — chapter and verse'],
  ['Sārāvalī', 'Kalyāṇa Varma', '~9th–10th c.', 'R. Santhanam (Ranjan)', 'planets in signs (pilot)'],
  ['Bṛhat Jātaka', 'Varāhamihira', '~550 CE', 'B. Suryanarain Row, 1919', 'planets in signs'],
  ['Jātaka Pārijāta', 'Vaidyanātha Dīkṣita', '~15th c.', 'V. Subramanya Sastri, 1932', 'planned'],
  ['Bṛhat Saṁhitā', 'Varāhamihira', '~550 CE', 'Sastri & Bhat, 1947', 'planned (nakṣatra)'],
  ['Phaladīpikā', 'Mantreśvara', '~13th–15th c.', 'Sanskrit e-text; Ojha (Hindi artha)', 'yoga indications'],
  ['Tājika-Nīlakaṇṭhī', 'Nīlakaṇṭha Daivajña', '1587 CE', 'D.P. Saxena (Ranjan)', 'the annual chart — calculation rules'],
  ['A Textbook of Varshaphala', 'K.S. Charak', '1996', '—', 'the annual chart — worked examples; period results'],
  ['Varshaphal', 'B.V. Raman', '2nd ed.', '—', 'the annual chart — corroboration'],
  ['Jaimini Chara Daśā', 'K.N. Rao (method)', 'modern', '—', 'the chara daśā lengths and sequence'],
  ['Navāṁśa', 'C.S. Patel (method)', 'modern', '—', 'vargottama, puṣkara, khara, bhāva-sūcaka'],
]

export default function References({ onBack, lang = 'en' }) {
  const [on, setOn] = useState(refsOn)
  useEffect(() => {
    applyRefs(on)
    try { localStorage.setItem(REFS_KEY, on ? '1' : '0') } catch { /* private mode */ }
  }, [on])
  const hi = lang === 'hi'
  return (
    <div className="page privacy methodology references" lang={lang}>
      <div className="method-top">
        <button type="button" className="privacy-back" onClick={onBack}>{hi ? '← कुंडली पर वापस' : '← back to the chart'}</button>
      </div>
      <h1>{hi ? 'सन्दर्भ' : 'References'}</h1>
      <p className="privacy-lede">
        {hi
          ? 'साइट का हर पठन किसी नामित ग्रन्थ के किसी स्थान से आता है; वह स्थान आँकड़ों में सदा रहता है। यहाँ उन्हें पृष्ठ पर दिखाने का स्विच है, और ग्रन्थों की सूची।'
          : 'Every reading on the site is drawn from a named text and keeps its locus in the data. This page lists the texts, and holds the one switch that shows those references beside the readings.'}
      </p>
      <section>
        <h2>{hi ? 'सन्दर्भ पृष्ठ पर दिखाएँ' : 'Show references on the site'}</h2>
        <label className="refs-switch">
          <input type="checkbox" checked={on} onChange={(e) => setOn(e.target.checked)} />
          <span>{hi ? 'हर पठन के पास अध्याय-श्लोक / पृष्ठ के सन्दर्भ दिखाएँ (केवल इस ब्राउज़र में)' : 'Show chapter-and-verse / page references beside every reading (this browser only)'}</span>
        </label>
        <p>{hi ? 'बंद होने पर पाठक को पठन मिलता है, पाद-टिप्पणी नहीं। चालू होने पर स्रोत-चिप, तल-पंक्तियाँ और ग्रन्थ-पृष्ठ फिर दिखते हैं।' : 'Off, the reader meets the reading, not the footnote. On, the source chips, provenance lines and page references come back everywhere.'}</p>
      </section>
      <section>
        <h2>{hi ? 'ग्रन्थ' : 'The texts'}</h2>
        <div className="dk-table-wrap">
          <table className="dk-table refs-table">
            <thead><tr><th>{hi ? 'ग्रन्थ' : 'Text'}</th><th>{hi ? 'लेखक' : 'Author'}</th><th>{hi ? 'काल' : 'Date'}</th><th>{hi ? 'संस्करण / अनुवाद' : 'Edition / translation'}</th><th>{hi ? 'यहाँ उपयोग' : 'Used for'}</th></tr></thead>
            <tbody>
              {SOURCES.map((r) => <tr key={r[0]}>{r.map((c, i) => <td key={i}>{c}</td>)}</tr>)}
            </tbody>
          </table>
        </div>
        <p>{hi ? 'नीति: उद्धृत करो या मना करो; प्रमाण-स्तर कभी मिश्रित नहीं; संस्कृत का स्व-अनुवाद कभी नहीं। विवरण “देवाशा किस तरह अलग है” पृष्ठ पर।' : 'The working rules — cite or refuse, provenance tiers never blended, no self-translation of Sanskrit — are on “How Devashaa is different”.'}</p>
      </section>
    </div>
  )
}
