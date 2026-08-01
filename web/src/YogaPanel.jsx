/**
 * Yogas — the named BPHS combinations the chart forms. A yoga is shown only when
 * its geometric condition is met; strength-gated yogas carry a "strength
 * unverified" flag (BPHS gates the result on a Ṣaḍbala the engine won't fake).
 * Each card shows the cited śloka effect, never asserted as fate.
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

export default function YogaPanel({ data }) {
  if (!data || data.error || !data.detected) return null
  const dt = data.detected
  return (
    <section className="table-panel yoga-panel" id="rg-yoga">
      <h3>Yogas — the combinations your chart forms</h3>
      <p className="rc-note">
        {dt.length} of {data.catalogued} catalogued BPHS yogas are present. A yoga is
        listed only when its geometric condition is met; the effect is the cited
        śloka, not a fated prediction, and there is no per-yoga score.
      </p>
      {dt.length === 0 ? (
        <p className="yoga-none">None of the catalogued yogas' conditions are met in this chart.</p>
      ) : (
        <div className="yoga-list">
          {dt.map((y) => (
            <div key={y.name} className={`yoga-card fam-${y.family}`}>
              <div className="yoga-head">
                <span className="yoga-name">{y.name}</span>
                <span className="yoga-fam">{FAMILY[y.family] || y.family}</span>
                {y.computability === 'strength_gated' && (
                  <span className="yoga-sg" title={y.strength_note || 'BPHS gates this result on a strength this engine does not compute'}>
                    strength unverified
                  </span>
                )}
              </div>
              <p className="yoga-effect">{effectText(y.effect)}</p>
              <span className="src">{shortCite(y.citation)}</span>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}
