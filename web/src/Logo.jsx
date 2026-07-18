/**
 * Devashaa mark: a glowing orb ringed by the zodiac, with grahas around it.
 *
 * This is literally what the app draws — a luminary at the centre, the ring
 * divided into the 12 rāśis, and lit points placed around it. The ring's 12
 * ticks are not decoration: they are the twelve signs.
 *
 * The glow is constructed, not implied: a radial halo behind everything, a
 * gaussian bloom merged under the crisp shapes, and a lit-sphere gradient on
 * the orb. Everything keys off --accent and --logo-hi, so the mark re-lights
 * itself per theme rather than being a fixed asset.
 *
 * ids are prefixed dv- because SVG defs share ONE document-wide namespace — a
 * generic id like "glow" would collide with any other inline SVG on the page.
 */

const R_RING = 20.5

// Twelve rāśi ticks. Angles start at -90° so the first division sits at the top.
const TICKS = Array.from({ length: 12 }, (_, i) => {
  const a = ((i * 30 - 90) * Math.PI) / 180
  return {
    x1: 32 + Math.cos(a) * (R_RING - 2.6),
    y1: 32 + Math.sin(a) * (R_RING - 2.6),
    x2: 32 + Math.cos(a) * (R_RING + 2.6),
    y2: 32 + Math.sin(a) * (R_RING + 2.6),
  }
})

// Grahas riding the ring. Uneven spacing and sizes so it reads as a sky, not a dial.
const GRAHAS = [
  { deg: -90, r: 3.1 },
  { deg: -18, r: 2.2 },
  { deg: 52, r: 2.7 },
  { deg: 133, r: 2.0 },
  { deg: 205, r: 2.4 },
]

export function LogoMark({ size = 48, className = '' }) {
  return (
    <svg
      className={`logo-mark ${className}`}
      width={size} height={size} viewBox="0 0 64 64"
      role="img" aria-label="Devashaa"
    >
      <defs>
        <radialGradient id="dvHalo" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="var(--accent)" stopOpacity=".42" />
          <stop offset="42%" stopColor="var(--accent)" stopOpacity=".14" />
          <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
        </radialGradient>

        {/* off-centre highlight so the orb reads as a lit sphere, not a disc */}
        <radialGradient id="dvOrb" cx="36%" cy="32%" r="72%">
          <stop offset="0%" stopColor="var(--logo-hi, #ffffff)" />
          <stop offset="58%" stopColor="var(--accent)" />
          <stop offset="100%" stopColor="var(--accent)" stopOpacity=".72" />
        </radialGradient>

        <filter id="dvBloom" x="-70%" y="-70%" width="240%" height="240%">
          <feGaussianBlur stdDeviation="1.7" result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="b" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>
      </defs>

      <circle cx="32" cy="32" r="31" fill="url(#dvHalo)" />

      {/* zodiac ring + its twelve divisions */}
      <g stroke="var(--accent)" fill="none" strokeLinecap="round">
        <circle cx="32" cy="32" r={R_RING} strokeWidth="1.2" opacity=".62" />
        {TICKS.map((t, i) => (
          <line key={i} x1={t.x1} y1={t.y1} x2={t.x2} y2={t.y2}
                strokeWidth="1.2" opacity=".5" />
        ))}
      </g>

      <g filter="url(#dvBloom)">
        {/* the luminary */}
        <circle cx="32" cy="32" r="7.6" fill="url(#dvOrb)" />
        {/* grahas around it */}
        {GRAHAS.map((g, i) => {
          const a = (g.deg * Math.PI) / 180
          return (
            <circle key={i} r={g.r} fill="var(--logo-hi, #ffffff)"
                    cx={32 + Math.cos(a) * R_RING}
                    cy={32 + Math.sin(a) * R_RING} />
          )
        })}
      </g>

      {/* distant stars */}
      <circle cx="9" cy="15" r=".9" fill="var(--accent)" opacity=".75" />
      <circle cx="56" cy="48" r="1.1" fill="var(--accent)" opacity=".6" />
      <circle cx="52" cy="11" r=".7" fill="var(--accent)" opacity=".5" />
    </svg>
  )
}

export default function Logo() {
  return (
    <div className="logo">
      <LogoMark />
      <div className="logo-text">
        <span className="logo-word">devashaa</span>
        <span className="logo-tag">Jyotiṣa · Vedic birth charts</span>
      </div>
    </div>
  )
}
