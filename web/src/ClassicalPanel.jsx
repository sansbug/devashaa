/**
 * Classical concordance — readings from classical Sanskrit texts OTHER than BPHS,
 * on their own `classical` provenance tier and NEVER blended with Parāśara. Each is
 * a cited, dated, adaptation-classified rendering — not a fated prediction. See
 * docs/classical-sources-policy.md.
 *
 * Two axes, each a concordance whose `sources` list is the point of comparison:
 *   • planet-in-sign  (data.readings)       — Sārāvalī + Bṛhat Jātaka
 *   • planet-in-house (data.house_readings)  — Sārāvalī Ch.30 + Bṛhat Jātaka Ch.20
 *                                              + Phaladīpikā + Chamatkāra Cintāmaṇi
 */
import Cite from './Cite.jsx'
import { useLang } from './LangContext.jsx'

// The §5 content-classes → i18n key for the badge label (docs/classical-sources-policy.md).
const CLASS_KEY = {
  caste: 'classical.class.caste', gender: 'classical.class.gender',
  slavery: 'classical.class.slavery', occupation: 'classical.class.occupation',
  health: 'classical.class.health', archaic: 'classical.class.archaic',
}

/** The historical-context badge (policy §5): flags a reading that touches dated
 *  social content, and on tap explains how it was handled. Chrome is localized;
 *  the adaptation action/note come pre-localized from the API (ADAPT_HI). */
function HistoricalBadge({ adaptation, date }) {
  const { t } = useLang()
  const cls = (adaptation?.classes || []).filter((c) => c && c !== 'clean')
  if (!cls.length) return null
  const labels = cls.map((c) => (CLASS_KEY[c] ? t(CLASS_KEY[c], c) : c)).join(' · ')
  const detail =
    `${t('classical.hist.detailLead', 'Historical material')} (${date}). ` +
    `${t('classical.hist.detailTouches', 'This reading touches:')} ${labels}. ` +
    `${t('classical.hist.detailNote', 'Shown for completeness, not as a judgement — handled per our adaptation policy:')} ` +
    `${adaptation.action}. ${adaptation.note || ''}`
  return (
    <Cite className="src cl-hist" detail={detail}>
      ⧗ {t('classical.hist.prefix', 'historical')} — {labels}
    </Cite>
  )
}

/** One source's cited, adapted line — shared by the sign and house axes. */
function SourceLine({ s }) {
  return (
    <div className="cl-source">
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
  )
}

export default function ClassicalPanel({ data, namer }) {
  const { t } = useLang()
  const signReadings = (data && !data.error && data.readings) || []
  const houseReadings = (data && !data.error && data.house_readings) || []
  if (!signReadings.length && !houseReadings.length) return null
  return (
    <section className="table-panel classical-panel" id="rg-classical">
      <h3>{t('classical.title', 'Classical sources')}</h3>

      {signReadings.length > 0 && (
        <>
          {data.note && <p className="rc-note">{data.note}</p>}
          {signReadings.map((r) => (
            <div className="cl-reading" key={`sign-${r.graha}-${r.sign}`}>
              <h4 className="cl-place">
                {namer.grahaKey(r.graha)} {t('classical.in', 'in')} {namer.rasi(r.sign)}
              </h4>
              {r.sources.map((s, i) => <SourceLine key={i} s={s} />)}
            </div>
          ))}
          {data.coverage && <p className="cl-coverage">{data.coverage}</p>}
        </>
      )}

      {houseReadings.length > 0 && (
        <div className="cl-house-axis">
          <h4 className="cl-axis-title">{t('classical.houseTitle', 'Planet-in-house (bhāva)')}</h4>
          {data.house_note && <p className="rc-note">{data.house_note}</p>}
          {houseReadings.map((r) => (
            <div className="cl-reading" key={`house-${r.graha}-${r.house}`}>
              <h4 className="cl-place">
                {namer.grahaKey(r.graha)} · {t('classical.bhava', 'bhāva')} {r.house}
              </h4>
              {r.sources.map((s, i) => <SourceLine key={i} s={s} />)}
            </div>
          ))}
        </div>
      )}
    </section>
  )
}
