/**
 * Devashaa mark: a glowing crescent moon with a sparkle in its notch.
 *
 * Chandra is the right symbol for this app specifically — the janma nakṣatra is
 * set by the Moon's position, and every daśā system here is computed from it.
 *
 * The glow is real, not implied: a radial halo behind the shapes, a gaussian
 * bloom merged under the originals, and a light-edge gradient across the
 * crescent. All of it keys off --accent (plus --logo-hi for the lit limb), so
 * the mark re-lights itself per theme rather than being a fixed asset.
 *
 * ids are prefixed dv- because SVG defs share one document-wide namespace —
 * a generic id like "glow" would collide with any other inline SVG on the page.
 */
export function LogoMark({ size = 48, className = '' }) {
  return (
    <svg
      className={`logo-mark ${className}`}
      width={size} height={size} viewBox="0 0 64 64"
      role="img" aria-label="Devashaa"
    >
      <defs>
        <radialGradient id="dvHalo" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor="var(--accent)" stopOpacity=".50" />
          <stop offset="45%" stopColor="var(--accent)" stopOpacity=".16" />
          <stop offset="100%" stopColor="var(--accent)" stopOpacity="0" />
        </radialGradient>

        <linearGradient id="dvLimb" x1="0" y1="1" x2="1" y2="0">
          <stop offset="0%" stopColor="var(--accent)" />
          <stop offset="100%" stopColor="var(--logo-hi, #ffffff)" />
        </linearGradient>

        {/* bloom: blur a copy and lay the crisp shape back on top */}
        <filter id="dvBloom" x="-70%" y="-70%" width="240%" height="240%">
          <feGaussianBlur stdDeviation="2" result="b" />
          <feMerge>
            <feMergeNode in="b" />
            <feMergeNode in="b" />
            <feMergeNode in="SourceGraphic" />
          </feMerge>
        </filter>

        {/* crescent = disc minus an offset, slightly larger disc */}
        <mask id="dvCrescent">
          <rect width="64" height="64" fill="#000" />
          <circle cx="30" cy="33" r="19" fill="#fff" />
          <circle cx="38" cy="29.5" r="20.7" fill="#000" />
        </mask>
      </defs>

      <circle cx="30" cy="32" r="31" fill="url(#dvHalo)" />

      <g filter="url(#dvBloom)">
        <circle cx="30" cy="33" r="19" fill="url(#dvLimb)" mask="url(#dvCrescent)" />
        {/* sparkle, sitting in the crescent's notch */}
        <g transform="translate(45 20)">
          <path
            d="M0,-9 C1,-3.8 3.8,-1 9,0 C3.8,1 1,3.8 0,9 C-1,3.8 -3.8,1 -9,0 C-3.8,-1 -1,-3.8 0,-9 Z"
            fill="url(#dvLimb)"
          />
        </g>
      </g>

      {/* scattered stars, for depth */}
      <circle cx="13" cy="16" r="1.15" fill="var(--accent)" opacity=".9" />
      <circle cx="54" cy="40" r="1.4" fill="var(--accent)" opacity=".75" />
      <circle cx="19" cy="52" r=".95" fill="var(--accent)" opacity=".6" />
      <circle cx="49" cy="52" r=".7" fill="var(--accent)" opacity=".5" />
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
