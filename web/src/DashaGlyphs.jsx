/**
 * Graha glyphs for the daśā rails.
 *
 * Drawn as inline SVG rather than the Unicode astrological codepoints (☉ ☾ ♂ …)
 * because those render as a system-font grab-bag: some platforms have no glyph
 * for Rāhu/Ketu at all, several draw the planets as emoji, and none of them
 * inherit stroke weight. These are a single consistent set that takes its
 * colour from `currentColor`, so a band tints them with the theme.
 *
 * Geometry only — no per-planet colour lives here. Colour is the VERDICT's job
 * (see DashaTimeline), and a glyph that carried its own hue would quietly
 * compete with it.
 */

const P = { fill: 'none', stroke: 'currentColor', strokeWidth: 1.6, strokeLinecap: 'round', strokeLinejoin: 'round' }

const SHAPES = {
  // Sūrya — disc with a centre point
  sun: <><circle cx="8" cy="8" r="5.2" {...P} /><circle cx="8" cy="8" r="1.1" fill="currentColor" /></>,
  // Candra — crescent
  moon: <path d="M10.6 3.1a5.6 5.6 0 1 0 0 9.8 6.6 6.6 0 0 1 0-9.8Z" {...P} />,
  // Maṅgala — shield and spear
  mars: <><circle cx="6.6" cy="9.4" r="3.9" {...P} /><path d="M9.6 6.5 13.4 2.7M10.4 2.7h3v3" {...P} /></>,
  // Budha — winged disc
  mercury: <><circle cx="8" cy="8.1" r="3.3" {...P} /><path d="M8 11.4v3.1M6.3 13h3.4M5.6 3.3a3.4 3.4 0 0 0 4.8 0" {...P} /></>,
  // Guru — the numeral-4 hook
  jupiter: <path d="M4.6 4.6c2.2 0 3.3 1.5 3.3 3.6v5.3M3.6 13.5h8.8M9.9 2.6v7.1" {...P} />,
  // Śukra — disc over a cross
  venus: <><circle cx="8" cy="6.3" r="3.5" {...P} /><path d="M8 9.8v4.2M6.1 12.2h3.8" {...P} /></>,
  // Śani — the scythe
  saturn: <path d="M3.4 4.1h4M5.4 2.6v7.6c0 2 1 3.2 2.6 3.2 1.5 0 2.6-1.1 2.6-2.6 0-1.3-.8-2.2-1.9-2.2-.7 0-1.3.3-1.7.8" {...P} />,
  // Rāhu — the ascending node
  rahu: <><path d="M4.6 12.4V8a3.4 3.4 0 0 1 6.8 0v4.4" {...P} /><circle cx="4.6" cy="13.4" r="1.5" {...P} /><circle cx="11.4" cy="13.4" r="1.5" {...P} /></>,
  // Ketu — the descending node (Rāhu inverted)
  ketu: <><path d="M4.6 3.6V8a3.4 3.4 0 0 0 6.8 0V3.6" {...P} /><circle cx="4.6" cy="2.6" r="1.5" {...P} /><circle cx="11.4" cy="2.6" r="1.5" {...P} /></>,
}

/** `size` is in px; the glyph inherits colour from its parent. */
export default function Glyph({ lord, size = 16, className = '' }) {
  const shape = SHAPES[lord]
  if (!shape) return null
  return (
    <svg
      className={`dt-glyph ${className}`}
      width={size}
      height={size}
      viewBox="0 0 16 16"
      aria-hidden="true"
      focusable="false"
    >
      {shape}
    </svg>
  )
}

export const HAS_GLYPH = (lord) => Boolean(SHAPES[lord])
