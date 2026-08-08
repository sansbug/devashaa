/**
 * Planetary motion (gati) & combustion.
 *
 * Facts first: speed, direction (retrograde), near-stationary and the distance
 * to the Sun come straight from the ephemeris. The gati NAMES and the combustion
 * ORBS are the classical scheme, shown on a `traditional` footing — NOT BPHS
 * (whose combustion is a proportional rule, not a fixed orb). Cheṣṭā bala — the
 * numeric motion-strength — is not derived here (BPHS gives no Seeghrocha); it is
 * computed in the Ṣaḍbala panel by Raman's method, and this panel links there.
 */
import Cite from './Cite.jsx'
import { useLang } from './LangContext.jsx'

// Direction is the sign of the speed; the near-stationary state (which can occur
// on either side of a station) is carried by the gati label (vikala) beside it.
const DIR_LABEL = (m) => (m.retrograde ? 'motion.dir.retrograde' : 'motion.dir.direct')

const CODE = { sun: 'Su', moon: 'Mo', mars: 'Ma', mercury: 'Me', jupiter: 'Ju',
  venus: 'Ve', saturn: 'Sa', rahu: 'Ra', ketu: 'Ke' }
// The spectrum axis is signed speed÷mean: 0 = station, negative = retrograde,
// 1 = the graha's own mean. The five regions ARE the gati classification.
const DOM_LO = -1.6, DOM_HI = 2.4
const BANDS = [
  { lo: DOM_LO, hi: -0.15, iast: 'vakra', en: 'motion.band.retrograde' },
  { lo: -0.15, hi: 0.15, iast: 'vikala', en: 'motion.band.stationary' },
  { lo: 0.15, hi: 0.9, iast: 'manda', en: 'motion.band.slow' },
  { lo: 0.9, hi: 1.1, iast: 'sama', en: 'motion.band.average' },
  { lo: 1.1, hi: DOM_HI, iast: 'atichāra', en: 'motion.band.swift' },
]

/** The gati spectrum: each graha at its speed÷mean, over the five traditional
    bands. Facts (speed, direction) drive the position; the bands and combustion
    ring are the traditional layer. */
function MotionSpectrum({ grahas, namer }) {
  const { t } = useLang()
  const W = 700, PADL = 12, PADR = 12, plotW = W - PADL - PADR
  const top = 20, bot = 92
  const x = (r) => PADL + (Math.max(DOM_LO, Math.min(DOM_HI, r)) - DOM_LO) / (DOM_HI - DOM_LO) * plotW
  const ROWS = [34, 56, 78]

  const pts = grahas.map((row) => {
    const m = row.motion
    const sr = m.retrograde ? -m.ratio : m.ratio
    return {
      key: row.key, px: x(sr), retro: m.retrograde,
      combust: row.combustion.applies && row.combustion.combust, m, c: row.combustion,
    }
  }).sort((a, b) => a.px - b.px)
  // Spread markers over up to three rows so near-equal speeds don't collide.
  const lastX = ROWS.map(() => -999)
  pts.forEach((p) => {
    let r = ROWS.findIndex((_, i) => p.px - lastX[i] >= 26)
    if (r < 0) r = lastX.indexOf(Math.min(...lastX))
    p.y = ROWS[r]; lastX[r] = p.px
  })

  return (
    <div className="ms-wrap">
      <svg viewBox={`0 0 ${W} 138`} className="ms-svg" role="img"
           aria-label={t('motion.spectrum.aria')}>
        {BANDS.map((b, i) => (
          <rect key={i} className={`ms-band ms-b-${b.iast.replace('ā', 'a')}`}
                x={x(b.lo)} y={top} width={x(b.hi) - x(b.lo)} height={bot - top} />
        ))}
        <line className="ms-axis" x1={x(0)} y1={top} x2={x(0)} y2={bot} />
        <line className="ms-axis" x1={x(1)} y1={top} x2={x(1)} y2={bot} />
        <text className="ms-axis-lbl" x={x(0)} y={top - 4} textAnchor="middle">{t('motion.axis.station')}</text>
        <text className="ms-axis-lbl" x={x(1)} y={top - 4} textAnchor="middle">{t('motion.axis.mean')}</text>
        {BANDS.map((b, i) => {
          const cx = (x(b.lo) + x(b.hi)) / 2
          return (
            <g key={`l${i}`}>
              <text className="ms-band-iast" x={cx} y={bot + 14} textAnchor="middle">{b.iast}</text>
              <text className="ms-band-en" x={cx} y={bot + 25} textAnchor="middle">{t(b.en)}</text>
            </g>
          )
        })}
        {pts.map((p) => (
          <g key={p.key} className={`ms-mk${p.retro ? ' retro' : ''}`}>
            <title>
              {`${namer.grahaKey(p.key)} — ${p.m.direction}, ${p.m.gati.iast} (${p.m.gati.en})`}
              {`\n${p.m.speed}°/day · ${Math.round(p.m.ratio * 100)}% of its mean (${p.m.mean}°/day)`}
              {p.c.applies ? `\ncombustion: ${p.c.combust ? 'combust' : 'free'} · ${p.c.separation}° from the Sun` : ''}
            </title>
            {p.combust && <circle className="ms-burn" cx={p.px} cy={p.y} r="12" />}
            <circle className="ms-dot" cx={p.px} cy={p.y} r="9" />
            <text className="ms-code" x={p.px} y={p.y} textAnchor="middle" dominantBaseline="central">{CODE[p.key]}</text>
          </g>
        ))}
      </svg>
      <p className="ms-cap">{t('motion.spectrum.caption')}</p>
    </div>
  )
}

// The grahas that can be combust (the Sun is the source; the nodes are shadow
// points), in a fixed display order.
const COMBUST_ORDER = ['moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn']

/** The combustion strip: one row per combust-eligible graha, its OWN orb drawn
    as a faint "burn reach" bar from the Sun, and a dot at its actual separation.
    A dot inside its bar is combust. Separation is a fact; the orbs are traditional. */
function CombustionStrip({ grahas, namer }) {
  const { t } = useLang()
  const rows = COMBUST_ORDER.map((k) => grahas.find((g) => g.key === k))
    .filter((g) => g && g.combustion.applies)
  if (!rows.length) return null
  const W = 700, X0 = 16, X1 = 680, plotW = X1 - X0, DMAX = 60
  const x = (d) => X0 + Math.min(Math.max(d, 0), DMAX) / DMAX * plotW
  const rowH = 20, y0 = 30
  const H = y0 + rows.length * rowH + 4
  const TICKS = [0, 15, 30, 45, 60]
  return (
    <div className="cs-wrap">
      <svg viewBox={`0 0 ${W} ${H}`} className="cs-svg" role="img"
           aria-label={t('motion.strip.aria')}>
        {TICKS.map((t) => (
          <g key={t}>
            <line className="cs-grid" x1={x(t)} y1="20" x2={x(t)} y2={H - 2} />
            <text className="cs-tick" x={x(t)} y="13" textAnchor="middle">{t}°</text>
          </g>
        ))}
        <text className="cs-sun" x={x(0)} y="13" textAnchor="middle">☉</text>
        {rows.map((g, i) => {
          const c = g.combustion, y = y0 + i * rowH, over = c.separation > DMAX
          return (
            <g key={g.key} className={`cs-row${c.combust ? ' combust' : ''}`}>
              <title>
                {`${namer.grahaKey(g.key)} — ${c.separation}° from the Sun · own orb ${c.orb}° → ${c.combust ? 'combust' : 'free'}`}
                {c.confidence === 'uncertain' ? '\n' + t('motion.strip.uncertainNote') : ''}
              </title>
              <rect className="cs-orb" x={x(0)} y={y - 7} width={x(c.orb) - x(0)} height="14" />
              {over && <text className="cs-over" x={X1 - 1} y={y - 10} textAnchor="end">›{Math.round(c.separation)}°</text>}
              <circle className="cs-dot" cx={x(c.separation)} cy={y} r="9" />
              <text className="cs-code" x={x(c.separation)} y={y} textAnchor="middle" dominantBaseline="central">{CODE[g.key]}</text>
            </g>
          )
        })}
      </svg>
      <p className="cs-cap">{t('motion.strip.caption')}</p>
    </div>
  )
}

export default function MotionPanel({ data, namer }) {
  const { t } = useLang()
  if (!data || data.error) return null
  const cb = data.cheshta_bala

  return (
    <section className="table-panel motion-panel" aria-label={t('motion.panel.aria')}>
      <h3>{t('motion.title')}</h3>
      <p className="rc-note">{t('motion.rcNote')}</p>

      {cb && !cb.available && (
        <p className="mp-cheshta">
          <Cite className="src conf conf-corroborated" detail={`${cb.reason}\n\n${cb.citation}`}>
            {t('motion.cheshta.cite')}
          </Cite>
          <span className="mp-cheshta-why">{t('motion.cheshta.why')}</span>
        </p>
      )}

      <h4 className="mp-sub">{t('motion.sub.speed')}</h4>
      <MotionSpectrum grahas={data.grahas} namer={namer} />

      <h4 className="mp-sub">{t('motion.sub.combustion')}</h4>
      <CombustionStrip grahas={data.grahas} namer={namer} />

      <div className="mp-scroll">
        <table className="mp-table">
          <thead>
            <tr>
              <th>{t('motion.table.graha')}</th>
              <th>{t('motion.table.motion')}</th>
              <th className="num">°/day</th>
              <th>{t('motion.table.combustion')}</th>
            </tr>
          </thead>
          <tbody>
            {data.grahas.map(({ key, motion: m, combustion: c }) => (
              <tr key={key}>
                <td className="mp-graha">{namer.grahaKey(key)}</td>
                <td>
                  <span className={`mp-dir mp-${m.retrograde ? 'retro' : 'direct'}`}>
                    {t(DIR_LABEL(m))}
                  </span>
                  <span className="mp-gati" title={`${m.gati.en} — ${t('motion.gati.tradTooltip')}`}>
                    {m.gati.iast}{m.pace ? ` · ${m.pace}` : ''}
                  </span>
                </td>
                <td className="num mp-speed"
                    title={`mean ${m.mean}°/day · ${Math.round(m.ratio * 100)}% of mean`}>
                  {m.speed.toFixed(3)}
                </td>
                <td>
                  {!c.applies ? (
                    <span className="mp-na" title={c.reason}>—</span>
                  ) : (
                    <span className={`mp-comb${c.combust ? ' is-combust' : ''}`}
                          title={`${c.separation}° from the Sun · orb ${c.orb}°\n\n${c.note}`}>
                      {c.combust ? t('motion.status.combust') : t('motion.status.free')} · {c.separation}°
                      <span className={`src mp-tier mp-${c.confidence === 'uncertain' ? 'uncertain' : 'trad'}`}>
                        {c.confidence === 'uncertain' ? t('motion.status.uncertain') : t('motion.status.traditional')}
                      </span>
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
