/**
 * Devashaa mark — the Sky wheel in miniature.
 *
 * This is the app's own SkyWheel chart distilled to a mark: the two concentric
 * rings (rāśis outside, nakṣatra ticks on the rim), the horizontal HORIZON with
 * the sky faintly lit above and the earth shaded below, a few grahas raying in
 * to the native at the centre, and — the signature — the luminous lagna cresting
 * the EASTERN horizon on the left, exactly where SkyWheel pins the ascendant.
 *
 * The glow is constructed, not implied: a radial halo behind everything, a
 * gaussian bloom under the rising orb, and a lit-sphere gradient on the orb.
 * Everything keys off --accent, --logo-hi, --line and --dim, so the mark
 * re-lights itself per theme rather than being a fixed asset.
 *
 * ids are prefixed dv- because SVG defs share ONE document-wide namespace — a
 * generic id like "glow" would collide with any other inline SVG on the page.
 */

const R_OUT = 26   // rāśi ring (outer)
const R_IN = 19    // inner ring — grahas sit inside it
const R_GRAHA = 12

// Point on a circle of radius r at angle deg (0 = east/right, CCW), in the 64 box.
const P = (r, deg) => {
  const a = (deg * Math.PI) / 180
  return [32 + r * Math.cos(a), 32 - r * Math.sin(a)]
}

// Twelve rāśi divisions, as spokes spanning the ring band.
const SPOKES = Array.from({ length: 12 }, (_, i) => {
  const [x1, y1] = P(R_OUT, i * 30)
  const [x2, y2] = P(R_IN, i * 30)
  return { x1, y1, x2, y2 }
})

// Twenty-seven nakṣatra ticks on the outer rim.
const NAKS = Array.from({ length: 27 }, (_, i) => {
  const d = (i * 360) / 27
  const [x1, y1] = P(R_OUT, d)
  const [x2, y2] = P(R_OUT - 2.1, d)
  return { x1, y1, x2, y2 }
})

// A few grahas riding inside the ring, each raying in to the centre. One is
// lit in --logo-hi for a cool/warm tonal lift; the rest ride in --accent.
const GRAHAS = [{ deg: 58, hi: false }, { deg: 128, hi: true }, { deg: 312, hi: false }]

const [LX, LY] = P(R_IN, 180) // the lagna, on the eastern horizon (left)

export function LogoMark({ size = 48, className = '' }) {
  return (
    <svg
      className={`logo-mark ${className}`}
      width={size} height={size} viewBox="0 0 64 64"
      role="img" aria-label="Devashaa"
    >
      <defs>
        <radialGradient id="dvHalo" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="var(--accent)" stopOpacity=".34" />
          <stop offset="45%" stopColor="var(--accent)" stopOpacity=".11" />
          <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
        </radialGradient>

        {/* off-centre highlight so the rising orb reads as a lit sphere */}
        <radialGradient id="dvOrb" cx="36%" cy="32%" r="72%">
          <stop offset="0%" stopColor="var(--logo-hi, #ffffff)" />
          <stop offset="55%" stopColor="var(--accent)" />
          <stop offset="100%" stopColor="var(--accent)" stopOpacity=".7" />
        </radialGradient>

        <filter id="dvBloom" x="-80%" y="-80%" width="260%" height="260%">
          <feGaussianBlur stdDeviation="1.4" result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>

        <clipPath id="dvDisc"><circle cx="32" cy="32" r={R_OUT} /></clipPath>
      </defs>

      <circle cx="32" cy="32" r="31" fill="url(#dvHalo)" />

      {/* sky above the horizon, earth below — clipped to the wheel */}
      <g clipPath="url(#dvDisc)">
        <rect x="0" y="0" width="64" height="32" fill="var(--accent)" opacity=".07" />
        <rect x="0" y="32" width="64" height="32" fill="#000" opacity=".2" />
      </g>

      {/* the two rings */}
      <g fill="none" stroke="var(--line)">
        <circle cx="32" cy="32" r={R_OUT} strokeWidth="1.1" />
        <circle cx="32" cy="32" r={R_IN} strokeWidth="1" />
      </g>

      {/* twelve rāśi spokes */}
      <g stroke="var(--line)" strokeWidth=".9" opacity=".55" strokeLinecap="round">
        {SPOKES.map((s, i) => <line key={i} x1={s.x1} y1={s.y1} x2={s.x2} y2={s.y2} />)}
      </g>

      {/* twenty-seven nakṣatra ticks */}
      <g stroke="var(--line)" strokeWidth=".7" opacity=".32">
        {NAKS.map((s, i) => <line key={i} x1={s.x1} y1={s.y1} x2={s.x2} y2={s.y2} />)}
      </g>

      {/* the horizon — Ascendant→Descendant diameter */}
      <line x1="4" y1="32" x2="60" y2="32" stroke="var(--dim)"
            strokeWidth="1.1" strokeDasharray="4 3" opacity=".7" />

      {/* grahas, each raying in to the native */}
      {GRAHAS.map((g, i) => {
        const [gx, gy] = P(R_GRAHA, g.deg)
        const col = g.hi ? 'var(--logo-hi, #ffffff)' : 'var(--accent)'
        return (
          <g key={i}>
            <line x1={gx} y1={gy} x2="32" y2="32" stroke={col} strokeWidth=".8" opacity=".5" />
            <circle cx={gx} cy={gy} r="1.7" fill={col} />
          </g>
        )
      })}
      <circle cx="32" cy="32" r="1.5" fill="var(--logo-hi, #ffffff)" />

      {/* the lagna, luminous on the eastern horizon */}
      <g filter="url(#dvBloom)">
        <circle cx={LX} cy={LY} r="4.3" fill="url(#dvOrb)" />
      </g>
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
