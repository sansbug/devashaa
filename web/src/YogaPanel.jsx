/**
 * Yogas — the named BPHS combinations the chart forms. A yoga is shown only when
 * its geometric condition is met. Strength-gated yogas (Kahala, Sankha, Bheri,
 * Adhi, the strong-vargottama Moon) are now RESOLVED against the Ṣaḍbala engine:
 * "fructifies" when the gating graha is strong, "does not fructify" when the
 * geometry is present but that strength is lacking — and Adhi shows the office's
 * balakramat (strength order). When the Ṣaḍbala is unavailable a yoga falls back
 * to the honest "strength unverified" flag. Each card shows the cited śloka
 * effect, never asserted as fate.
 */
const FAMILY = {
  nabhasa: 'Nābhasa', mahapurusha: 'Mahāpuruṣa', lunar: 'Lunar',
  solar: 'Solar', other: 'ch.36', raja: 'Rāja',
}
// Long provenance string → the chapter/verse tail for the chip.
const shortCite = (c) => {
  const m = (c || '').match(/Ch\.\s?\d+.*/i) || (c || '').match(/ch\.\s?\d+.*/i)
  return m ? m[0].replace(/\s*\(printed[^)]*\)/g, '').trim() : c
}
// Drop a leading verse-number label ("20-22. ") the extraction sometimes keeps.
const effectText = (t) => (t || '').replace(/^\d+\s*[-–]?\s*\d*\.\s*/, '')

// The Ṣaḍbala resolution of a strength-gated yoga: the verdict chip, the gating
// role, and each gating graha with its rūpa and strong/weak mark.
function Strength({ s, namer }) {
  const isAdhi = /balakramat/.test(s.role || '')
  return (
    <div className="yoga-strength">
      <span className={`yoga-str ${s.fructifies ? 'ok' : 'no'}`} title={s.basis}>
        {isAdhi ? 'strength ranked' : s.fructifies ? 'fructifies' : 'does not fructify'}
      </span>
      <span className="yoga-str-role">{s.role}</span>
      {(s.grahas || []).map((gr) => (
        <span key={gr.graha} className={`yoga-str-g ${gr.strong ? 'strong' : 'weak'}`}
              title={`${gr.rupa} rūpa vs minimum ${gr.min} → ${gr.strong ? 'strong' : 'weak'}`}>
          {namer ? namer.grahaKey(gr.graha) : gr.graha} {gr.rupa}r {gr.strong ? '✓' : '✕'}
        </span>
      ))}
    </div>
  )
}

export default function YogaPanel({ data, namer }) {
  if (!data || data.error || !data.detected) return null
  const dt = data.detected
  return (
    <section className="table-panel yoga-panel" id="rg-yoga">
      <h3>Yogas — the combinations your chart forms</h3>
      <p className="rc-note">
        {dt.length} of {data.catalogued} catalogued BPHS yogas are present. A yoga is
        listed only when its geometric condition is met; the effect is the cited
        śloka, not a fated prediction, and there is no per-yoga score.{' '}
        {data.strength_resolved
          ? 'Strength-gated yogas are resolved against the Ṣaḍbala engine — whether the gating graha is strong enough for the result to fructify.'
          : 'Strength-gated yogas carry an unverified flag (Ṣaḍbala was unavailable for this chart).'}
      </p>
      {dt.length === 0 ? (
        <p className="yoga-none">None of the catalogued yogas' conditions are met in this chart.</p>
      ) : (
        <div className="yoga-list">
          {dt.map((y) => (
            <div key={y.name}
                 className={`yoga-card fam-${y.family}`
                   + (y.strength && !y.strength.fructifies ? ' yoga-dormant' : '')}>
              <div className="yoga-head">
                <span className="yoga-name">{y.name}</span>
                <span className="yoga-fam">{FAMILY[y.family] || y.family}</span>
                {y.computability === 'strength_gated' && !y.strength && (
                  <span className="yoga-sg" title={y.strength_note || 'BPHS gates this result on a strength this engine does not compute'}>
                    strength unverified
                  </span>
                )}
              </div>
              <p className="yoga-effect">{effectText(y.effect)}</p>
              {y.strength && <Strength s={y.strength} namer={namer} />}
              <span className="src">{shortCite(y.citation)}</span>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}
