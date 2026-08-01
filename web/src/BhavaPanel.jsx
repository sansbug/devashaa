/**
 * Bhāva-phala — the house-by-house reading. Each house is a card that shows the
 * cited rules that FIRE (lord-in-house effect ch.24, significations ch.11, kāraka
 * ch.32), never a synthesised verdict. Occupants are shown for context with the
 * sourced "BPHS is silent on graha-in-bhāva" refusal.
 */
import { useState } from 'react'

const ORD = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th']
const ord = (n) => ORD[n - 1] || `${n}th`
// The extraction keeps the śloka's "…FIRST HOUSE:" / "SECOND HOUSE:" prefix
// (the card already shows the house number); drop everything up to it.
const sig = (t) => (t || '').replace(/^.*?HOUSE:\s*/i, '')

export default function BhavaPanel({ data, namer }) {
  if (!data || data.error || !data.bhavas) return null
  return (
    <section className="table-panel bhava-panel" id="rg-bhava">
      <h3>Bhāva-phala — the twelve houses</h3>
      <p className="rc-note">
        A house-by-house reading assembled from the relationships already in the
        chart, each line a cited BPHS rule — the lord's placement (ch.24), the
        house significations (ch.11) and its kāraka (ch.32). No per-house verdict
        or score: Parāśara states these separately and never fuses them.
      </p>
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
  const r = b.lord_rule
  return (
    <div className="bhava-card">
      <button type="button" className="bhava-head" aria-expanded={open} onClick={() => setOpen((o) => !o)}>
        <span className="bhava-num">{ord(b.house)}</span>
        <span className="bhava-sign">{namer.rasi(b.sign)}</span>
        <span className="bhava-lordline">
          lord <strong>{namer.grahaKey(b.lord)}</strong> in the {ord(b.lord_in_house)}
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
              <em>Exception:</em> {r.lagna_exception}{' '}
              <span className={`src conf conf-${r.exception_source === 'sloka' ? 'sloka' : 'note'}`}>
                {r.exception_source === 'sloka' ? 'in the śloka' : "Santhanam's note"}
              </span>
            </p>
          )}
        </div>
      )}

      {b.combination_applies && (
        <p className="bhava-combo">
          Its lord also rules the {b.lord_also_rules.map(ord).join(' &amp; ')} — by ch.24
          vv.145–148 both lordships apply (contrary results nullify).
        </p>
      )}

      {open && (
        <div className="bhava-detail">
          <div className="bhava-meta">
            <span><em>Kāraka</em> {namer.grahaKey(b.karaka)} <span className="src">ch.32</span></span>
            <span><em>Occupants</em> {b.occupants.length
              ? b.occupants.map((g) => namer.grahaKey(g)).join(', ') : '—'}</span>
            {b.aspects_in.length > 0 && (
              <span><em>Aspected by</em> {b.aspects_in.map((a) => namer.grahaKey(a.graha)).join(', ')}</span>
            )}
          </div>
          {b.occupants.length > 0 && (
            <p className="bhava-occ-note">
              Occupancy carries no cited effect — BPHS Vol I has no graha-in-bhāva
              rule for the seven grahas. See each graha's signal stack for its state.
            </p>
          )}
          {r && r.notes_caveat && (
            <p className="bhava-notes"><em>Santhanam's note</em> {r.notes_caveat}</p>
          )}
          {b.combination_applies && combo && (
            <p className="bhava-combo-rule"><em>ch.24 vv.145–148</em> {combo}</p>
          )}
        </div>
      )}
    </div>
  )
}
