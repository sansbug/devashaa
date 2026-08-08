/**
 * Bhāva-phala — the house-by-house reading. Each house is a card that shows the
 * cited rules that FIRE (lord-in-house effect ch.24, significations ch.11, kāraka
 * ch.32), never a synthesised verdict. Occupants are shown for context with the
 * sourced "BPHS is silent on graha-in-bhāva" refusal.
 */
import { useState } from 'react'
import { useLang } from './LangContext.jsx'

const ORD = ['bhava.ord.1', 'bhava.ord.2', 'bhava.ord.3', 'bhava.ord.4', 'bhava.ord.5', 'bhava.ord.6', 'bhava.ord.7', 'bhava.ord.8', 'bhava.ord.9', 'bhava.ord.10', 'bhava.ord.11', 'bhava.ord.12']
const ord = (n) => ORD[n - 1] || `${n}th`
// The extraction keeps the śloka's "…FIRST HOUSE:" / "SECOND HOUSE:" prefix
// (the card already shows the house number); drop everything up to it.
const sig = (t) => (t || '').replace(/^.*?HOUSE:\s*/i, '')

export default function BhavaPanel({ data, namer }) {
  const { t } = useLang()
  if (!data || data.error || !data.bhavas) return null
  return (
    <section className="table-panel bhava-panel" id="rg-bhava">
      <h3>{t('bhava.title')}</h3>
      <p className="rc-note">{t('bhava.note')}</p>
      <div className="bhava-list">
        {data.bhavas.map((b) => (
          <BhavaCard key={b.house} b={b} namer={namer} combo={data.combination_rule} />
        ))}
      </div>
      <p className="bhava-refusal">{data.planet_in_house}</p>
    </section>
  )
}

function BhavaCard({ b, namer, combo }) {
  const [open, setOpen] = useState(false)
  const { t } = useLang()
  const r = b.lord_rule
  return (
    <div className="bhava-card">
      <button type="button" className="bhava-head" aria-expanded={open} onClick={() => setOpen((o) => !o)}>
        <span className="bhava-num">{t(ord(b.house))}</span>
        <span className="bhava-sign">{namer.rasi(b.sign)}</span>
        <span className="bhava-lordline">
          {t('bhava.lordline.lord')} <strong>{namer.grahaKey(b.lord)}</strong> {t('bhava.lordline.in')} {t(ord(b.lord_in_house))}
        </span>
        <span className="bhava-caret" aria-hidden="true">{open ? '−' : '+'}</span>
      </button>

      <p className="bhava-sig">{sig(b.significations.text)}</p>

      {r && (
        <div className="bhava-rule">
          <p className="bhava-effect">{r.effect}</p>
          <span className="src">{r.citation}</span>
          {r.lagna_exception && (
            <p className="bhava-exc">
              <em>{t('bhava.exception.label')}</em> {r.lagna_exception}{' '}
              <span className={`src conf conf-${r.exception_source === 'sloka' ? 'sloka' : 'note'}`}>
                {r.exception_source === 'sloka' ? t('bhava.exception.sloka') : t('bhava.exception.note')}
              </span>
            </p>
          )}
        </div>
      )}

      {b.combination_applies && (
        <p className="bhava-combo">
          {t('bhava.combo.pre')} {b.lord_also_rules.map((n) => t(ord(n))).join(' &amp; ')} {t('bhava.combo.post')}
        </p>
      )}

      {open && (
        <div className="bhava-detail">
          <div className="bhava-meta">
            <span><em>{t('bhava.meta.karaka')}</em> {namer.grahaKey(b.karaka)} <span className="src">ch.32</span></span>
            <span><em>{t('bhava.meta.occupants')}</em> {b.occupants.length
              ? b.occupants.map((g) => namer.grahaKey(g)).join(', ') : '—'}</span>
            {b.aspects_in.length > 0 && (
              <span><em>{t('bhava.meta.aspectedBy')}</em> {b.aspects_in.map((a) => namer.grahaKey(a.graha)).join(', ')}</span>
            )}
          </div>
          {b.occupants.length > 0 && (
            <p className="bhava-occ-note">{t('bhava.occNote')}</p>
          )}
          {r && r.notes_caveat && (
            <p className="bhava-notes"><em>{t('bhava.santhanamNote')}</em> {r.notes_caveat}</p>
          )}
          {b.combination_applies && combo && (
            <p className="bhava-combo-rule"><em>ch.24 vv.145–148</em> {combo}</p>
          )}
        </div>
      )}
    </div>
  )
}
