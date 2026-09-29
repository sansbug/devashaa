/**
 * Life-domain icons for the projection views — one per theme key.
 *
 * Inline SVG on `currentColor`, for the same reason DashaGlyphs.jsx is: emoji
 * and dingbats render as a per-platform grab-bag and cannot take the theme's
 * ink. These are geometry only; the colour comes from the band, never from
 * the icon.
 */

const P = { fill: 'none', stroke: 'currentColor', strokeWidth: 1.5, strokeLinecap: 'round', strokeLinejoin: 'round' }

const SHAPES = {
  // self · vitality · mind — a rising flame
  self: <path d="M8 2.5c1.6 2.2 3.4 3.6 3.4 6.4A3.4 3.4 0 0 1 8 12.3 3.4 3.4 0 0 1 4.6 8.9c0-1.3.5-2.2 1.2-3 .1 1 .5 1.7 1.2 2.1C7.4 6.2 7.3 4.3 8 2.5Z" {...P} />,
  // wealth · finances — stacked coins
  wealth: <><ellipse cx="8" cy="4.6" rx="4.6" ry="1.9" {...P} /><path d="M3.4 4.6v2.8c0 1 2.1 1.9 4.6 1.9s4.6-.9 4.6-1.9V4.6M3.4 7.4v2.8c0 1 2.1 1.9 4.6 1.9s4.6-.9 4.6-1.9V7.4" {...P} /></>,
  // career · status — briefcase
  career: <><rect x="2.4" y="5.2" width="11.2" height="7.6" rx="1.4" {...P} /><path d="M6 5.2V4a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v1.2M2.4 8.6h11.2" {...P} /></>,
  // marriage · partner — two linked rings
  marriage: <><circle cx="6" cy="8.6" r="3.3" {...P} /><circle cx="10" cy="8.6" r="3.3" {...P} /></>,
  // children · progeny — two figures
  children: <><circle cx="5.4" cy="4.6" r="1.7" {...P} /><circle cx="10.6" cy="5.4" r="1.4" {...P} /><path d="M2.6 13c.2-2.6 1.3-4 2.8-4s2.6 1.4 2.8 4M8.6 13c.1-2 1-3.2 2-3.2s1.9 1.2 2 3.2" {...P} /></>,
  // health · body — heart
  health: <path d="M8 13.2 3.3 8.6a2.9 2.9 0 0 1 4.1-4.1L8 5.1l.6-.6a2.9 2.9 0 0 1 4.1 4.1Z" {...P} />,
  // education · learning — open book
  education: <path d="M8 4.4c-1.4-1-3.2-1.2-5.2-.8v8.6c2-.4 3.8-.2 5.2.8 1.4-1 3.2-1.2 5.2-.8V3.6c-2-.4-3.8-.2-5.2.8Zm0 0v8.6" {...P} />,
  // home · property — house
  home: <path d="M2.6 8 8 3.2 13.4 8M4.2 6.9v5.9h7.6V6.9M6.8 12.8V9.6h2.4v3.2" {...P} />,
  // fortune · dharma · father — lotus
  fortune: <path d="M8 12.6c-2.2 0-4.2-1.3-5.2-3.3 1.4-.2 2.6.2 3.6.9-.4-1.9 0-3.8 1.6-5.4 1.6 1.6 2 3.5 1.6 5.4 1-.7 2.2-1.1 3.6-.9-1 2-3 3.3-5.2 3.3Z" {...P} />,
  // enemies · disease · debt — shield
  enemies: <path d="M8 2.8 3.4 4.4v3.7c0 2.6 1.9 4.5 4.6 5.4 2.7-.9 4.6-2.8 4.6-5.4V4.4Z" {...P} />,
  // foreign · loss · mokṣa — globe
  foreign: <><circle cx="8" cy="8" r="5.3" {...P} /><path d="M2.7 8h10.6M8 2.7c1.7 1.6 2.5 3.3 2.5 5.3S9.7 11.7 8 13.3M8 2.7C6.3 4.3 5.5 6 5.5 8s.8 3.7 2.5 5.3" {...P} /></>,
  // longevity — infinity
  longevity: <path d="M8 8c-1-1.6-2-2.6-3.2-2.6a2.6 2.6 0 0 0 0 5.2C6 10.6 7 9.6 8 8c1-1.6 2-2.6 3.2-2.6a2.6 2.6 0 0 1 0 5.2C10 10.6 9 9.6 8 8Z" {...P} />,
}

export default function DomainIcon({ k, size = 16, className = '' }) {
  const shape = SHAPES[k]
  if (!shape) return null
  return (
    <svg className={`pj-ico ${className}`} width={size} height={size} viewBox="0 0 16 16"
         aria-hidden="true" focusable="false">
      {shape}
    </svg>
  )
}
