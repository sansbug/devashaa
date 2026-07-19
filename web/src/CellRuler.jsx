/**
 * Cell ruler — a 0°→30° axis for one rāśi, drawn at the foot of a South Indian
 * cell so that a graha's DEGREE stops being a number in a list and becomes a
 * position you can compare by eye.
 *
 * What the position is actually good for, in the order that matters:
 *
 *   1. RĀŚI SANDHI. A graha at 29°50′ is one arc-minute of birth-time error
 *      from a different sign — and, for the lagna, from a different chart.
 *      The end caps are that junction.
 *   2. PADA / NAKṢATRA. The tick a graha sits next to is what every one of the
 *      eight daśās on this site is computed from, and what D9 is cut on.
 *   3. DISTANCE TO UCCHA. BPHS puts peak strength at a POINT (ch.3 vv.49-50),
 *      not across a whole sign. The chevron is that point; `uccha_bala` is how
 *      far along you are.
 *   4. MŪLATRIKOṆA vs plain own-sign — an arc inside a sign (vv.51-54), so it
 *      can only be shown against a degree scale.
 *
 * What it is deliberately NOT for: "conjunction tightness". Orbs are Western.
 * In BPHS yuti is RĀŚI membership — two grahas in the same sign are conjunct
 * whether they are 0°30′ or 28° apart. Two pins close together on this ruler
 * mean nothing beyond what the sign already said. That spread is a side effect
 * of drawing degrees honestly; it is not a claim.
 *
 * D1 ONLY. In D9 or D30 the cell's sign is a DERIVED sign — the graha does not
 * have a longitude "within" it — so a 0-30° ruler under a varga cell would be
 * a fabrication. Other vargas render exactly as they did before.
 */

import { useEffect, useState } from 'react'

/* x is degrees ×10 in both viewBoxes, so this is the only x code path. */
const x = (deg) => deg * 10

/* Wide y-geometry. Narrow multiplies every y by NARROW_SY to keep the rendered
   band ~12 CSS px tall while the cell itself has shrunk to ~2.16 px/degree. */
const Y = {
  pinTop: 4, pinTopRx: 1, pinFoot: 12, axis: 14, lagnaTop: 2,
  padaFoot: 18, nakFoot: 21, chevronFoot: 22, connector: 16,
  mtTop: 23, mtFoot: 26, capTop: 10, capFoot: 18, gandantaH: 4,
}
const NARROW_SY = 56 / 26

/**
 * Below this the cell is under 2 px/degree and the ruler resolves nothing —
 * so it is removed rather than shown as decoration.
 */
const FLOOR_PX = 356
/** At six occupants the tag list plus a ruler overflows the cell in the
    561-694px band. The list wins: it carries the names. */
const MAX_OCCUPANTS = 5

/**
 * matchMedia, not a `resize` listener on innerWidth: the listener fires on
 * every pixel of a drag (re-rendering twelve SVGs each time) and, worse, is
 * not reliably delivered when the viewport is changed programmatically rather
 * than by the user. A media query fires once, on the threshold crossing, and
 * uses the same mechanism as the CSS breakpoint it has to agree with.
 */
function useMedia(query) {
  const [hit, setHit] = useState(
    () => typeof window !== 'undefined' && window.matchMedia(query).matches,
  )
  useEffect(() => {
    const mq = window.matchMedia(query)
    const on = () => setHit(mq.matches)
    on()                              // catch a change that landed before mount
    mq.addEventListener('change', on)
    return () => mq.removeEventListener('change', on)
  }, [query])
  return hit
}

/* Must track the 560px breakpoint in App.css, where .tag-deg is hidden. */
const NARROW_Q = '(max-width: 560px)'
const FLOOR_Q = `(max-width: ${FLOOR_PX - 1}px)`

export function useRulerMode(occupantCount) {
  const narrow = useMedia(NARROW_Q)
  const belowFloor = useMedia(FLOOR_Q)
  if (belowFloor || occupantCount > MAX_OCCUPANTS) return null
  return narrow ? 'narrow' : 'wide'
}

/**
 * @param sign        0-11, the rāśi this cell holds
 * @param occupants   grahas in it (each carries .dignity, null for the nodes)
 * @param landmarks   sign_landmarks(sign) from the API — no BPHS numbers here
 * @param lagnaDegree degrees into THIS sign, or null if the lagna is elsewhere
 * @param mode        'wide' | 'narrow'
 * @param active      key of the graha being hovered/tapped in the tag list
 */
export default function CellRuler({
  sign, occupants, landmarks, lagnaDegree, gandanta, mode, active, onActivate,
}) {
  const narrow = mode === 'narrow'
  const sy = narrow ? NARROW_SY : 1
  const y = (v) => +(v * sy).toFixed(2)
  const H = narrow ? 56 : 26

  const present = new Set(occupants.map((g) => g.key))
  const degIn = (g) => g.longitude % 30

  /* Only the grahas actually standing here get their dignity landmarks drawn.
     A cell is not a reference card for the whole zodiac. */
  const uccha = (landmarks?.exaltation_points ?? []).filter((p) => present.has(p.graha))
  const nica = (landmarks?.debilitation_points ?? []).filter((p) => present.has(p.graha))
  const mt = narrow
    ? []
    : (landmarks?.moolatrikona_arcs ?? []).filter((a) => present.has(a.graha))

  /* A gaṇḍānta straddles a sign boundary, so the zone has to be clipped to
     this cell's own 0-30° window. The Mīna|Meṣa junction is at 360°/0°, hence
     testing the junction at both +360 and -360. */
  let gandantaBand = null
  if (gandanta && present.has('moon')) {
    const base = sign * 30
    for (const j of [gandanta.junction, gandanta.junction + 360, gandanta.junction - 360]) {
      const lo = Math.max(base, j - gandanta.half_width) - base
      const hi = Math.min(base + 30, j + gandanta.half_width) - base
      if (hi > lo) { gandantaBand = { from: lo, to: hi }; break }
    }
  }

  /* Where a graha sits, for the dashed connector to its own uccha point. */
  const posOf = (key) => {
    const g = occupants.find((o) => o.key === key)
    return g ? degIn(g) : null
  }

  return (
    <svg
      className="cell-ruler"
      viewBox={`0 0 300 ${H}`}
      preserveAspectRatio="none"
      aria-hidden="true"
    >
      {/* Each cell is its own <svg>, so the pattern id must be per-sign or the
          document carries twelve duplicates. */}
      {!narrow && (
        <defs>
          <pattern id={`rl-hatch-${sign}`} width="5" height="5"
                   patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <line x1="0" y1="0" x2="0" y2="5" className="rl-hatch-line" />
          </pattern>
        </defs>
      )}

      {/* --- axis and the two rāśi sandhi caps --- */}
      <line x1="0" y1={y(Y.axis)} x2="300" y2={y(Y.axis)} className="rl-axis" />
      <line x1="0.5" y1={y(Y.capTop)} x2="0.5" y2={y(Y.capFoot)} className="rl-axis" />
      <line x1="299.5" y1={y(Y.capTop)} x2="299.5" y2={y(Y.capFoot)} className="rl-axis" />

      {/* --- pada ticks; every 4th pada boundary starts a nakṣatra ---
          Exactly two nakṣatras begin inside any sign, always: 9 padas per sign
          against 4 padas per nakṣatra. On a phone the 8 pada ticks sit 7px
          apart and read as texture, so only the nakṣatra pair survives. */}
      {Array.from({ length: 8 }, (_, i) => i + 1).map((k) => {
        const isNak = (9 * sign + k) % 4 === 0
        if (narrow && !isNak) return null
        return (
          <line
            key={k}
            x1={x(k * (30 / 9))} y1={y(Y.axis)}
            x2={x(k * (30 / 9))} y2={y(isNak ? Y.nakFoot : Y.padaFoot)}
            className={isNak ? 'rl-nak' : 'rl-pada'}
          />
        )
      })}

      {/* --- gaṇḍānta (BPHS Vol II ch.92 v.3) ---
          Almost always absent. Ariṣṭa doctrine about the birth MOMENT, not a
          dignity and not a hazard zone any graha can stand in — Parāśara's
          three kinds are tithi, nakṣatra and lagna — so this is Candra's zone
          only, drawn only in the cell she occupies.
          Deliberately NARROW: two ghaṭikās of her motion is ~26 arc-minutes,
          not the 3°20' navāṁśa later authors quote. At 4.7px/° that is ~2px,
          so it takes a minimum width to stay findable. */}
      {gandantaBand && (
        <rect
          x={x(gandantaBand.from)} y={y(Y.axis)}
          width={Math.max(3, x(gandantaBand.to - gandantaBand.from))}
          height={y(Y.gandantaH)}
          fill={narrow ? undefined : `url(#rl-hatch-${sign})`}
          className={narrow ? 'rl-gandanta-solid' : 'rl-gandanta'}
        />
      )}

      {/* --- mūlatrikoṇa arcs (v.51-54) --- */}
      {mt.map((a) => {
        const g = occupants.find((o) => o.key === a.graha)
        const unverified = g?.dignity?.moolatrikona_verified === false
        return (
          <path
            key={a.graha}
            d={`M ${x(a.from)},${y(Y.mtFoot)} L ${x(a.from)},${y(Y.mtTop)} ` +
               `L ${x(a.to)},${y(Y.mtTop)} L ${x(a.to)},${y(Y.mtFoot)}`}
            className={`rl-mt${unverified ? ' unverified' : ''}`}
          />
        )
      })}

      {/* --- exaltation / debilitation points ---
          Apex up vs apex down, plus a dash on the debilitation form: the
          distinction never rests on hue alone. */}
      {uccha.map((p) => {
        const at = posOf(p.graha)
        return (
          <g key={`u${p.graha}`}>
            {!narrow && at !== null && (
              <line x1={x(at)} y1={y(Y.connector)} x2={x(p.degree)} y2={y(Y.connector)}
                    className="rl-connector" />
            )}
            <path
              d={`M ${x(p.degree) - 4},${y(Y.chevronFoot)} L ${x(p.degree)},${y(Y.axis)} ` +
                 `L ${x(p.degree) + 4},${y(Y.chevronFoot)}`}
              className="rl-uccha"
            />
          </g>
        )
      })}
      {nica.map((p) => (
        <path
          key={`n${p.graha}`}
          d={`M ${x(p.degree) - 4},${y(Y.axis)} L ${x(p.degree)},${y(Y.chevronFoot)} ` +
             `L ${x(p.degree) + 4},${y(Y.axis)}`}
          className="rl-nica"
        />
      ))}

      {/* --- graha pins ---
          Anonymous by design. Identity lives in the labelled list directly
          above; hovering or tapping a row raises its pin and vice versa. Two
          grahas half a degree apart merge into one mark and are NOT nudged
          apart — the ruler is a comparison instrument, not a readout, and the
          exact figure is in the tag and in the table below. */}
      {occupants.map((g) => (
        <g key={g.key}
           onPointerEnter={() => onActivate?.(g.key)}
           onPointerLeave={() => onActivate?.(null)}
           onClick={() => onActivate?.(active === g.key ? null : g.key)}>
          <line
            x1={x(degIn(g))} y1={y(Y.pinFoot)}
            x2={x(degIn(g))} y2={y(g.retrograde ? Y.pinTopRx : Y.pinTop)}
            className={`rl-pin${g.retrograde ? ' rx' : ''}${active === g.key ? ' active' : ''}`}
          />
          {/* Retrograde carries THREE channels — hue, extra height, and a
              backward barb — but deliberately NOT a dash: at 4.7px/° the pin is
              under 4px tall and a dash pattern erases it entirely. Height is
              free here, and legible where a dash is not. */}
          {g.retrograde && (
            <line x1={x(degIn(g))} y1={y(Y.pinTopRx)} x2={x(degIn(g)) - 5} y2={y(Y.pinTopRx)}
                  className="rl-barb" />
          )}
          <rect x={x(degIn(g)) - 6} y={0} width="12" height={H} className="rl-hit" />
        </g>
      ))}

      {/* --- lagna ---
          Two parallel strokes and extra height, so it stays distinguishable
          from a retrograde pin even in the theme where --accent and --rx sit
          close together. In a whole-sign chart this degree fixes every bhāva
          in the figure; it belongs on any graphic claiming to show degree. */}
      {lagnaDegree !== null && (
        <g>
          <line x1={x(lagnaDegree) - 1} y1={y(Y.axis)} x2={x(lagnaDegree) - 1} y2={y(Y.lagnaTop)}
                className="rl-lagna" />
          <line x1={x(lagnaDegree) + 1} y1={y(Y.axis)} x2={x(lagnaDegree) + 1} y2={y(Y.lagnaTop)}
                className="rl-lagna" />
        </g>
      )}
    </svg>
  )
}
