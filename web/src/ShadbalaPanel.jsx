/**
 * Ṣaḍbala — the six-fold strength of the grahas (B. V. Raman's codification of
 * Parāśara's method). Every formula is validated to the virūpa against Raman's
 * own worked "Standard Horoscope" (see api/test_shadbala.py).
 *
 * Unlike the Tier-0 signal stack — which BPHS states as separate judgements and
 * this site refuses to fuse — Ṣaḍbala IS an explicit, cited numeric method, so
 * here a single per-graha total and a strong/weak verdict are legitimate. Two
 * honest caveats travel on the payload and are surfaced below: Cheṣṭā uses
 * modern secular mean longitudes (the "Seeghrocha" the śāstra never tabulated),
 * and Ayana follows Raman's β=0 / 24° kranti, not the true declination.
 */
const CODE = { sun: 'Su', moon: 'Mo', mars: 'Ma', mercury: 'Me', jupiter: 'Ju',
  venus: 'Ve', saturn: 'Sa' }

// The five always-positive balas, in stacking order, + the signed Dṛk.
const PARTS = [
  { key: 'sthana', label: 'Sthāna', en: 'positional' },
  { key: 'dik', label: 'Dik', en: 'directional' },
  { key: 'kala', label: 'Kāla', en: 'temporal' },
  { key: 'cheshta', label: 'Cheṣṭā', en: 'motional' },
  { key: 'naisargika', label: 'Naisargika', en: 'natural' },
]
const KALA_PARTS = ['nathonnatha', 'paksha', 'thribhaga', 'abda', 'masa', 'vara', 'hora', 'ayana', 'yuddha']
const STHANA_PARTS = ['ochcha', 'saptavargaja', 'ojayugma', 'kendra', 'drekkana']

const v1 = (x) => (x == null ? '—' : x.toFixed(1))         // one decimal (Raman's precision)
const RUPA = (x) => x.toFixed(2)
// Truncate, not round, so a weak graha just under 1 never displays "1.00×".
const RATIO = (x) => (Math.floor(x * 100) / 100).toFixed(2)

/** Horizontal stacked-composition bars: each graha's six balas summed to its
    Ṣaḍbala Piṇḍa, with a marker at its minimum requirement and a verdict. Shows
    not just how strong a graha is, but which bala makes it so. */
function StrengthBars({ grahas, namer }) {
  const rows = Object.entries(grahas)
    .map(([key, v]) => ({ key, ...v }))
    .sort((a, b) => b.ratio - a.ratio)     // strongest first, as Raman ranks them
  const grossOf = (v) => PARTS.reduce((s, p) => s + (v[p.key] || 0), 0)
  const maxEnd = Math.max(...rows.map((v) => Math.max(grossOf(v), v.min_required_rupa * 60))) * 1.06
  const W = 720, LABEL = 62, RIGHT = 96, plotW = W - LABEL - RIGHT
  const x = (virupa) => LABEL + (virupa / maxEnd) * plotW
  const rowH = 30, top = 8
  const H = top + rows.length * rowH + 4

  return (
    <div className="sb-bars-wrap">
      <svg viewBox={`0 0 ${W} ${H}`} className="sb-bars" role="img"
           aria-label="Each graha's six-fold strength, composed, against its minimum requirement">
        {rows.map((v, i) => {
          const y = top + i * rowH
          const gross = grossOf(v)
          const net = v.total_virupa
          const minV = v.min_required_rupa * 60
          let cx = LABEL
          return (
            <g key={v.key} className={`sb-row${v.strong ? ' strong' : ' weak'}`}>
              <text className="sb-glyph" x={LABEL - 8} y={y + rowH / 2} textAnchor="end"
                    dominantBaseline="central">{CODE[v.key]}</text>
              {/* the five positive balas, stacked */}
              {PARTS.map((p) => {
                const w = ((v[p.key] || 0) / maxEnd) * plotW
                const seg = <rect key={p.key} className={`sb-seg sb-${p.key}`} x={cx} y={y + 5}
                                  width={Math.max(0, w)} height={rowH - 12} rx="1">
                  <title>{`${namer.grahaKey(v.key)} · ${p.label} (${p.en}): ${v1(v[p.key])} virūpa`}</title>
                </rect>
                cx += w
                return seg
              })}
              {/* Dṛk: green extension if it helps, red pull-back if it hurts */}
              {v.drik >= 0 ? (
                <rect className="sb-seg sb-drik-pos" x={cx} y={y + 5}
                      width={(v.drik / maxEnd) * plotW} height={rowH - 12} rx="1">
                  <title>{`Dṛk (aspect): +${v1(v.drik)} virūpa`}</title>
                </rect>
              ) : (
                <rect className="sb-seg sb-drik-neg" x={x(net)} y={y + 5}
                      width={x(gross) - x(net)} height={rowH - 12}>
                  <title>{`Dṛk (aspect): ${v1(v.drik)} virūpa`}</title>
                </rect>
              )}
              {/* minimum-required marker */}
              <line className="sb-min" x1={x(minV)} y1={y + 2} x2={x(minV)} y2={y + rowH - 2} />
              {/* net total + verdict */}
              <text className="sb-total" x={x(Math.max(net, gross)) + 8} y={y + rowH / 2}
                    dominantBaseline="central">
                {RUPA(v.total_rupa)}
                <tspan className={`sb-verdict ${v.strong ? 'is-strong' : 'is-weak'}`}>
                  {v.strong ? ' ✓' : ' ✕'}
                </tspan>
              </text>
            </g>
          )
        })}
      </svg>
      <div className="sb-legend">
        {PARTS.map((p) => (
          <span key={p.key} className="sb-leg"><i className={`sb-sw sb-${p.key}`} />{p.label}</span>
        ))}
        <span className="sb-leg"><i className="sb-sw sb-drik-pos" />Dṛk ±</span>
        <span className="sb-leg"><i className="sb-sw sb-minmark" />min. required</span>
      </div>
    </div>
  )
}

export default function ShadbalaPanel({ data, namer }) {
  if (!data || data.error || !data.grahas) return null
  const { grahas, kala_components: kc, sthana_components: sc, method } = data
  const order = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn']

  return (
    <section className="table-panel shadbala-panel" aria-label="Ṣaḍbala — six-fold strength">
      <h3>Ṣaḍbala — the six-fold strength</h3>
      <p className="rc-note">
        Parāśara's six strengths — positional, directional, temporal, motional,
        natural and aspectual — after <strong>B. V. Raman</strong>. Every formula is
        validated to the virūpa (60 virūpa = 1 rūpa) against Raman's own worked
        chart. This is a cited numeric method, so — unlike the signal stack — a
        per-graha total and a strong/weak verdict are shown.
      </p>

      <StrengthBars grahas={grahas} namer={namer} />

      <div className="sb-scroll">
        <table className="sb-table">
          <thead>
            <tr>
              <th>Graha</th>
              <th className="num" title="positional">Sthāna</th>
              <th className="num" title="directional">Dik</th>
              <th className="num" title="temporal">Kāla</th>
              <th className="num" title="motional">Cheṣṭā</th>
              <th className="num" title="natural">Naisargika</th>
              <th className="num" title="aspectual (signed)">Dṛk</th>
              <th className="num">Total</th>
              <th className="num" title="Ṣaḍbala Piṇḍa in rūpa">rūpa</th>
              <th>vs min.</th>
            </tr>
          </thead>
          <tbody>
            {order.filter((k) => grahas[k]).map((k) => {
              const v = grahas[k]
              const kalaTip = KALA_PARTS.map((p) => `${p}: ${v1(kc?.[p]?.[k] ?? 0)}`).join('\n')
              const sthanaTip = STHANA_PARTS.map((p) => `${p}: ${v1(sc?.[k]?.[p] ?? 0)}`).join('\n')
              return (
                <tr key={k} className={v.strong ? 'sb-strong' : 'sb-weak'}>
                  <td className="sb-graha">{namer.grahaKey(k)}</td>
                  <td className="num" title={sthanaTip}>{v1(v.sthana)}</td>
                  <td className="num">{v1(v.dik)}</td>
                  <td className="num" title={kalaTip}>{v1(v.kala)}</td>
                  <td className="num">{v.cheshta == null ? '—' : v1(v.cheshta)}</td>
                  <td className="num">{v1(v.naisargika)}</td>
                  <td className={`num sb-drik ${v.drik < 0 ? 'neg' : 'pos'}`}>
                    {v.drik >= 0 ? '+' : ''}{v1(v.drik)}
                  </td>
                  <td className="num sb-vir">{v1(v.total_virupa)}</td>
                  <td className="num sb-rupa">{RUPA(v.total_rupa)}</td>
                  <td>
                    <span className={`sb-badge ${v.strong ? 'ok' : 'no'}`}
                          title={`${RUPA(v.total_rupa)} rūpa vs minimum ${v.min_required_rupa} · ratio ${v.ratio.toFixed(3)}`}>
                      {v.strong ? 'strong' : 'weak'} · {RATIO(v.ratio)}×
                    </span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      <p className="sb-foot">
        Cheṣṭā is blank for the Sun and Moon (their motional strength rides in Ayana
        and Pakṣa). Hover Sthāna or Kāla for the sub-components. Two method notes:{' '}
        <span className="src" title={method?.cheshta_note}>Cheṣṭā mean-elements</span>{' '}
        and <span className="src" title={method?.ayana_note}>Ayana kranti</span>{' '}
        follow modern astronomy / Raman's β=0 table respectively — stated, not hidden.
      </p>
    </section>
  )
}
