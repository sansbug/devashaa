/**
 * The signal stack — what BPHS actually says about one graha.
 *
 * NOT a score. BPHS contains at least seven partially overlapping judgements of
 * a graha and never combines them, so each row keeps its own scale, its own
 * citation, and its own availability. A single red/green verdict would be our
 * arithmetic wearing Parāśara's authority.
 *
 * Three rules this component exists to enforce:
 *
 *  1. Every row shows its citation. A row without one cannot render.
 *  2. UNAVAILABLE is a first-class state, shown with its reason — never hidden,
 *     never replaced by a proxy. The row saying "BPHS does not tabulate
 *     Seeghrocha" is doing more for the reader's trust than any number here.
 *  3. A flagged value is never drawn as settled. Flags mean the text is damaged,
 *     ambiguous, or the translator's rather than the sage's, and the mark that
 *     says so is not decorative.
 *
 * Row order is FIXED across grahas — doctrinal weight, not value — so the eye
 * can compare straight down a column when switching between grahas.
 */

import { useState } from 'react'
import { useLang } from './LangContext.jsx'

const ORDER = [
  'vimsopaka', 'dignity', 'uccha_bala', 'baladi', 'jagradadi',
  'functional', 'shadbala', 'ishta_kashta',
]

const TITLE = {
  vimsopaka: 'signalstack.title.vimsopaka',
  dignity: 'signalstack.title.dignity',
  uccha_bala: 'signalstack.title.uccha_bala',
  baladi: 'signalstack.title.baladi',
  jagradadi: 'signalstack.title.jagradadi',
  functional: 'signalstack.title.functional',
  shadbala: 'signalstack.title.shadbala',
  ishta_kashta: 'signalstack.title.ishta_kashta',
}

/** Rows that carry a 0-1 proportion we can draw as a bar. Everything else is
    categorical and gets a word, because inventing a scale for a category is
    exactly the kind of quiet fabrication this whole panel exists to avoid. */
const BAR = {
  vimsopaka: (s) => (typeof s.value === 'number' ? s.value / 20 : null),
  uccha_bala: (s) => (typeof s.value === 'number' ? s.value : null),
}

const pretty = (v) =>
  typeof v === 'number' ? (Number.isInteger(v) ? v : v.toFixed(2)) : String(v ?? '')

function Flag({ text }) {
  const [open, setOpen] = useState(false)
  const { t } = useLang()
  return (
    <>
      <button type="button" className="sig-flag" title={t('signalstack.flag.title')}
              aria-expanded={open} onClick={() => setOpen(!open)}>⚑</button>
      {open && <p className="sig-flag-body">{text}</p>}
    </>
  )
}

function Row({ sig }) {
  const [open, setOpen] = useState(false)
  const { t } = useLang()
  const frac = BAR[sig.name]?.(sig)

  if (!sig.available) {
    return (
      <div className="sig-row unavailable">
        <div className="sig-head">
          <span className="sig-mark" aria-hidden="true">⊘</span>
          <span className="sig-name">{TITLE[sig.name] ? t(TITLE[sig.name]) : sig.name}</span>
          <span className="sig-cite">{sig.citation}</span>
        </div>
        {/* The reason is the content of this row. It tells the reader exactly
            what the text does not supply — and, where a book would close the
            gap, that is a far more useful answer than a fabricated number. */}
        <p className="sig-reason">{sig.reason}</p>
      </div>
    )
  }

  return (
    <div className={`sig-row${sig.flags.length ? ' flagged' : ''}`}>
      <div className="sig-head">
        {frac !== null && frac !== undefined ? (
          <span className="sig-bar" aria-hidden="true">
            <span className="sig-bar-fill" style={{ width: `${Math.max(0, Math.min(1, frac)) * 100}%` }} />
          </span>
        ) : <span className="sig-mark" aria-hidden="true">·</span>}
        <span className="sig-value">{pretty(sig.value)}</span>
        <span className="sig-name">{TITLE[sig.name] ? t(TITLE[sig.name]) : sig.name}</span>
        <span className="sig-cite">{sig.citation}</span>
        {sig.detail && (
          <button type="button" className="sig-more" onClick={() => setOpen(!open)}
                  aria-expanded={open} title={t('signalstack.more.title')}>
            {open ? '−' : '+'}
          </button>
        )}
      </div>
      {sig.label && <p className="sig-label">{sig.label}</p>}
      {sig.flags.map((f, i) => <Flag key={i} text={f} />)}
      {open && sig.detail?.rows && (
        // Viṁśopaka's own working, laid out the way the book prints it on p.99 —
        // so the total is checkable rather than asserted.
        <table className="sig-working">
          <thead>
            <tr><th>{t('signalstack.working.varga')}</th><th>{t('signalstack.working.relationship')}</th><th className="num">{t('signalstack.working.swamsa')}</th>
                <th className="num">{t('signalstack.working.varga_viswa')}</th><th className="num">{t('signalstack.working.points')}</th></tr>
          </thead>
          <tbody>
            {sig.detail.rows.map((r) => (
              <tr key={r.varga}>
                <td>{r.varga}</td><td>{r.relationship}</td>
                <td className="num">{r.swaviswa}</td>
                <td className="num">{r.varga_viswa}</td>
                <td className="num">{pretty(r.points)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}

export default function SignalStack({ signals, namer, graha }) {
  const { t } = useLang()
  if (!signals) return null
  const byName = Object.fromEntries(signals.map((s) => [s.name, s]))
  const ordered = ORDER.map((n) => byName[n]).filter(Boolean)
  const extra = signals.filter((s) => !ORDER.includes(s.name))

  return (
    <div className="signal-stack">
      <h4 className="sig-title">{graha ? namer.graha(graha) : ''}</h4>
      {[...ordered, ...extra].map((s) => <Row key={s.name} sig={s} />)}
      <p className="sig-foot">{t('signalstack.foot')}</p>
    </div>
  )
}
