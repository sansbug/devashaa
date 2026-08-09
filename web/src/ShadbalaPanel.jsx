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
import Cite from './Cite.jsx'
import { useLang } from './LangContext.jsx'
const CODE = { sun: 'Su', moon: 'Mo', mars: 'Ma', mercury: 'Me', jupiter: 'Ju',
  venus: 'Ve', saturn: 'Sa' }

// The five always-positive balas, in stacking order, + the signed Dṛk.
const PARTS = [
  { key: 'sthana', label: 'Sthāna', en: 'shadbala.gloss.positional' },
  { key: 'dik', label: 'Dik', en: 'shadbala.gloss.directional' },
  { key: 'kala', label: 'Kāla', en: 'shadbala.gloss.temporal' },
  { key: 'cheshta', label: 'Cheṣṭā', en: 'shadbala.gloss.motional' },
  { key: 'naisargika', label: 'Naisargika', en: 'shadbala.gloss.natural' },
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
  const { t } = useLang()
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
           aria-label={t('shadbala.bars.aria')}>
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
                  <title>{`${namer.grahaKey(v.key)} · ${p.label} (${t(p.en)}): ${v1(v[p.key])} virūpa`}</title>
                </rect>
                cx += w
                return seg
              })}
              {/* Dṛk: green extension if it helps, red pull-back if it hurts */}
              {v.drik >= 0 ? (
                <rect className="sb-seg sb-drik-pos" x={cx} y={y + 5}
                      width={(v.drik / maxEnd) * plotW} height={rowH - 12} rx="1">
                  <title>{`Dṛk (${t('shadbala.gloss.aspect')}): +${v1(v.drik)} virūpa`}</title>
                </rect>
              ) : (
                <rect className="sb-seg sb-drik-neg" x={x(net)} y={y + 5}
                      width={x(gross) - x(net)} height={rowH - 12}>
                  <title>{`Dṛk (${t('shadbala.gloss.aspect')}): ${v1(v.drik)} virūpa`}</title>
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
        <span className="sb-leg"><i className="sb-sw sb-minmark" />{t('shadbala.legend.minRequired')}</span>
      </div>
    </div>
  )
}

export default function ShadbalaPanel({ data, namer }) {
  const { t } = useLang()
  if (!data || data.error || !data.grahas) return null
  const { grahas, kala_components: kc, sthana_components: sc, method } = data
  const order = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn']

  return (
    <section className="table-panel shadbala-panel" aria-label={t('shadbala.aria')}>
      <h3>{t('shadbala.title')}</h3>
      <p className="rc-note">{t('shadbala.note')}</p>

      <details className="sb-explain">
        <summary>{t('shadbala.explain.summary', 'What the six strengths mean')}</summary>
        <p className="sb-explain-lead">
          {t('shadbala.explain.lead',
            'Ṣaḍbala ("six strengths") gauges how much capacity each graha has to deliver its results. Parāśara’s six components (BPHS ch.27), computed here by B. V. Raman’s method, are summed in virūpa (60 virūpa = 1 rūpa) and weighed against a minimum requirement to give each graha a strong / weak verdict.')}
        </p>
        <dl className="sb-explain-list">
          <dt>Sthāna <span>({t('shadbala.gloss.positional', 'positional')})</span></dt>
          <dd>{t('shadbala.explain.sthana',
            'Strength from placement — exaltation and own-sign dignity, standing across the seven divisional charts (saptavargaja), odd/even sign, a kendra, and the decanate (drekkāṇa).')}</dd>
          <dt>Dik <span>({t('shadbala.gloss.directional', 'directional')})</span></dt>
          <dd>{t('shadbala.explain.dik',
            'Strength from direction — Jupiter and Mercury are strong in the east (Ascendant), the Sun and Mars in the south (10th), Saturn in the west (7th), the Moon and Venus in the north (4th).')}</dd>
          <dt>Kāla <span>({t('shadbala.gloss.temporal', 'temporal')})</span></dt>
          <dd>{t('shadbala.explain.kala',
            'Strength from the time of birth — day vs night, the waxing/waning Moon (pakṣa), the day- and night-thirds, the lords of the year/month/day/hour, the Sun’s northward/southward course (ayana), and planetary war (yuddha).')}</dd>
          <dt>Cheṣṭā <span>({t('shadbala.gloss.motional', 'motional')})</span></dt>
          <dd>{t('shadbala.explain.cheshta',
            'Strength from motion — chiefly retrogression (vakra); the Sun and Moon draw theirs from ayana and pakṣa instead.')}</dd>
          <dt>Naisargika <span>({t('shadbala.gloss.natural', 'natural')})</span></dt>
          <dd>{t('shadbala.explain.naisargika',
            'A fixed, intrinsic ranking — Sun (strongest) › Moon › Venus › Jupiter › Mercury › Mars › Saturn (weakest).')}</dd>
          <dt>Dṛk <span>({t('shadbala.gloss.aspect', 'aspectual')})</span></dt>
          <dd>{t('shadbala.explain.drik',
            'Strength from aspects received — benefic aspects add, malefic aspects subtract. It is the only component that can be negative.')}</dd>
        </dl>
        <p className="sb-explain-foot">
          {t('shadbala.explain.nodes',
            'The result is each graha’s potency — its capacity to deliver. Rāhu and Ketu are assigned no Ṣaḍbala.')}
        </p>
      </details>

      <StrengthBars grahas={grahas} namer={namer} />

      <div className="sb-scroll">
        <table className="sb-table">
          <thead>
            <tr>
              <th>{t('shadbala.th.graha')}</th>
              <th className="num" title={t('shadbala.gloss.positional')}>Sthāna</th>
              <th className="num" title={t('shadbala.gloss.directional')}>Dik</th>
              <th className="num" title={t('shadbala.gloss.temporal')}>Kāla</th>
              <th className="num" title={t('shadbala.gloss.motional')}>Cheṣṭā</th>
              <th className="num" title={t('shadbala.gloss.natural')}>Naisargika</th>
              <th className="num" title={t('shadbala.gloss.aspectualSigned')}>Dṛk</th>
              <th className="num">{t('shadbala.th.total')}</th>
              <th className="num" title={t('shadbala.th.rupaTitle')}>rūpa</th>
              <th>{t('shadbala.th.vsmin')}</th>
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
                      {v.strong ? t('shadbala.badge.strong') : t('shadbala.badge.weak')} · {RATIO(v.ratio)}×
                    </span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      <p className="sb-foot">
        {t('shadbala.foot.lead')}{' '}
        <Cite className="src" detail={method?.cheshta_note}>{t('shadbala.foot.cite1')}</Cite>{' '}
        {t('shadbala.foot.and')} <Cite className="src" detail={method?.ayana_note}>{t('shadbala.foot.cite2')}</Cite>{' '}
        {t('shadbala.foot.tail')}
      </p>
    </section>
  )
}
