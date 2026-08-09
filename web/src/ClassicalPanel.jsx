/**
 * Classical concordance — readings from classical Sanskrit texts OTHER than BPHS
 * (pilot: Sārāvalī), on their own `classical` provenance tier and NEVER blended
 * with Parāśara. Each is a cited, dated, adaptation-classified rendering — not a
 * fated prediction. See docs/classical-sources-policy.md.
 *
 * The `sources` list per placement is the concordance: when Jātaka Pārijāta /
 * Bṛhat Jātaka are added, each simply appends another cited line here.
 */
import Cite from './Cite.jsx'
import { useLang } from './LangContext.jsx'

// The §5 content-classes that make a reading carry historical-context adaptation.
const CLASS_LABEL = {
  caste: 'caste', gender: 'gender & marriage', slavery: 'servitude',
  occupation: 'occupation', health: 'illness', archaic: 'archaic terms',
}

/** The historical-context badge (policy §5): flags a reading that touches dated
 *  social content, and on tap explains how it was handled. */
function HistoricalBadge({ adaptation, date }) {
  const cls = (adaptation?.classes || []).filter((c) => c && c !== 'clean')
  if (!cls.length) return null
  const labels = cls.map((c) => CLASS_LABEL[c] || c).join(' · ')
  const detail =
    `Historical material (${date}). This reading touches: ${labels}. ` +
    `Shown for completeness, not as a judgement — handled per our adaptation policy: ` +
    `${adaptation.action}. ${adaptation.note || ''}`
  return <Cite className="src cl-hist" detail={detail}>⧗ historical — {labels}</Cite>
}

export default function ClassicalPanel({ data, namer }) {
  const { t } = useLang()
  if (!data || data.error || !data.readings || !data.readings.length) return null
  return (
    <section className="table-panel classical-panel" id="rg-classical">
      <h3>{t('classical.title', 'Classical sources')}</h3>
      <p className="rc-note">{data.note}</p>
      {data.readings.map((r) => (
        <div className="cl-reading" key={`${r.graha}-${r.sign}`}>
          <h4 className="cl-place">
            {namer.grahaKey(r.graha)} {t('classical.in', 'in')} {namer.rasi(r.sign)}
          </h4>
          {r.sources.map((s, i) => (
            <div className="cl-source" key={i}>
              <div className="cl-src-head">
                <span className="cl-tier">{s.source.tier}</span>
                <strong className="cl-src-name">{s.source.text}</strong>
                <span className="cl-src-meta">{s.source.author} · {s.source.date}</span>
                <Cite
                  className="src"
                  detail={`${s.source.text} — ${s.source.author} (${s.source.date}); ` +
                          `tr. ${s.source.translator}. ${s.citation}. Confidence: ${s.confidence}.`}
                >{s.citation}</Cite>
              </div>
              <p className="cl-gist">{s.gist}</p>
              <HistoricalBadge adaptation={s.adaptation} date={s.source.date} />
            </div>
          ))}
        </div>
      ))}
      {data.coverage && <p className="cl-coverage">{data.coverage}</p>}
    </section>
  )
}
