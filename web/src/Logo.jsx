/**
 * Devashaa mark: the North Indian kuṇḍalī — a square cut by its diagonals with
 * an inner diamond. Chosen because it is unique to Jyotiṣa (Western charts are
 * round) and it is already this app's visual language.
 *
 * The filled top diamond is bhāva 1, the lagna — the point every chart is
 * anchored to. Geometry matches RasiChart's bhāva-1 region exactly, scaled 400→64.
 *
 * Strokes use currentColor so the mark inherits the theme; the lagna uses
 * --accent. Nothing here is a raster asset, so it stays sharp at any size.
 */
export function LogoMark({ size = 34, className = '' }) {
  return (
    <svg
      className={`logo-mark ${className}`}
      width={size} height={size} viewBox="0 0 64 64"
      role="img" aria-label="Devashaa"
    >
      <g fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinejoin="round">
        <rect x="4" y="4" width="56" height="56" rx="2" />
        <path d="M4 4 L60 60 M60 4 L4 60" />
        <path d="M32 4 L60 32 L32 60 L4 32 Z" />
      </g>
      {/* bhāva 1 — the lagna */}
      <path d="M32 4 L46 18 L32 32 L18 18 Z" fill="var(--accent)" />
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
