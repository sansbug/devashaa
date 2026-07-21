"""Jaimini Chara Daśā — the length engine.

TIER: jaimini. This is NOT Parāśara and must never be labelled as BPHS. It is a
SIGN-based daśā from the Jaimini school; every other daśā in this project is a
nakṣatra daśā of the Viṁśottarī family.

SOURCE: K.N. Rao, *Predicting Through Jaimini's Chara Daśā* (Vani Publications),
Chapter 6 "Calculation of Jaimini Chara Daśā" (book pp.40-45). The length rule,
the two fixed counting groups, the own-sign exception, the dual-lord tie-break
and the two method rejections are all taken from that chapter as an algorithm.
Validated against the book's three worked illustration tables (see the tests).

WHAT IS COMPLETE HERE, AND THE ONE THING THAT IS NOT
---------------------------------------------------
COMPLETE — the per-sign daśā LENGTH. This is the whole substance of the method:
the inclusive count to the sign's lord, the direction of that count fixed by the
sign's group, minus one year, with the own-sign 12-year exception and the
dual-lord strength test. All sourced, all validated.

NOT IN THE SOURCE — the daśā ORDER's DIRECTION. Chara Daśā runs the twelve signs
in a sequence that is "direct" (zodiacally forward from a starting sign) in some
charts and "reverse" in others. The rule that decides forward vs reverse lives
in the book's Chapter 3, which is not in the scanned copy available. Both of the
book's worked examples happen to run direct from the lagna, but the selection
criterion is not shown. So this engine will NOT guess it: `chara_dasha()` takes
the direction as an explicit argument and refuses to invent one. Substituting a
remembered "standard" rule here would be exactly the fabrication this project
refuses.

A TRAP THE SOURCE ITSELF WARNS ABOUT: the word "direct/indirect" names TWO
different things in this method, and only one is defined in the available pages.
The GROUP a sign belongs to fixes the direction you count FROM the sign TO its
lord (§ COUNTING_GROUPS). That is NOT the same as the daśā SEQUENCE direction.
The book's Virgo-lagna example runs its sequence "direct" while Virgo sits in the
*indirect* counting group. The two must never be conflated — see
`sequence_direction_unavailable`.
"""

from __future__ import annotations

import dignity

# ch.6. Signs whose distance-to-lord is counted FORWARD vs BACKWARD. This is the
# lord-counting direction only — NOT the daśā sequence direction.
DIRECT_GROUP = frozenset({0, 1, 2, 6, 7, 8})     # Aries,Taurus,Gemini,Libra,Scorpio,Sag
INDIRECT_GROUP = frozenset({3, 4, 5, 9, 10, 11})  # Cancer,Leo,Virgo,Cap,Aquarius,Pisces

# The two signs with two lords, and their pair. Every other sign uses
# dignity.RASI_LORD. Scorpio counts forward (direct group), Aquarius backward.
DUAL_LORDS = {7: ("mars", "ketu"), 10: ("saturn", "rahu")}

CITATION = "K.N. Rao, Predicting Through Jaimini's Chara Daśā, ch.6 (jaimini, NOT BPHS)"

SEQUENCE_DIRECTION_UNAVAILABLE = (
    "The rule that decides whether the daśā sequence runs forward or reverse "
    "from the lagna is stated in the book's Chapter 3, which is not in the "
    "available source. This engine computes the correct per-sign LENGTHS for "
    "any chart, but will not guess the sequence direction — pass it explicitly. "
    "The book's own worked examples all run 'direct' from the lagna."
)

REJECTIONS = (
    "Rao rejects the commentators' rule of adding/deducting a year for an "
    "exalted/debilitated lord (it can zero out a sign, and 'no rashi can ever "
    "have zero years'), and rejects fractional/expired-portion lengths (P.S. "
    "Sastri's method) — full years only, minimum 1, maximum 12.",
)


def _sign(longitude: float) -> int:
    return int(longitude % 360 // 30)


def _deg_in_sign(longitude: float) -> float:
    return longitude % 30


def _count(start: int, target: int, forward: bool) -> int:
    """Inclusive whole-sign count from `start` to `target`. Start itself is 1."""
    return ((target - start) % 12 + 1) if forward else ((start - target) % 12 + 1)


def _operative_lord(sign: int, positions: dict[str, int], degrees: dict[str, float]):
    """Which lord governs a sign's length, and whether it sits in the sign.

    Single-lord signs: the rāśi lord. Dual-lord signs (Scorpio, Aquarius) apply
    Rao's ch.6 tie-break verbatim:

      (a) one lord in the sign, the other elsewhere -> count to the OTHER (the
          one in the sign is ignored);
      (b) mirror of (a);
      (c) both lords in the sign -> own-sign (full 12 years);
      (d) both elsewhere -> the STRONGER lord, where:
            (i)   a lord sharing its sign with another graha beats a solitary one;
            (ii)  both associated  -> higher degree-within-sign wins;
            (iii) both solitary    -> higher degree-within-sign wins;
            (iv)  a degree+minute tie -> higher seconds wins
          — i.e. association first, else the higher longitude-within-sign, which
          subsumes the degree/minute/second ordering into one float compare.

    Returns (lord_key, is_own): is_own True means the operative lord sits in the
    sign, so the length is the flat 12 years with no deduction.
    """
    if sign not in DUAL_LORDS:
        lord = dignity.RASI_LORD[sign]
        return lord, positions.get(lord) == sign

    a, b = DUAL_LORDS[sign]
    in_a = positions.get(a) == sign
    in_b = positions.get(b) == sign
    if in_a and in_b:
        return a, True                      # (c) both here -> own-sign, 12y
    if in_a:
        return b, False                     # (a) A here -> count to B
    if in_b:
        return a, False                     # (b) B here -> count to A

    # (d) both elsewhere -> strength test.
    occ = {}
    for g, s in positions.items():
        occ.setdefault(s, []).append(g)
    assoc_a = len(occ.get(positions[a], [])) > 1
    assoc_b = len(occ.get(positions[b], [])) > 1
    if assoc_a and not assoc_b:
        return a, False                     # (d)(i)
    if assoc_b and not assoc_a:
        return b, False                     # (d)(i)
    # both associated or both solitary -> higher longitude-within-sign wins.
    # A missing degree defaults to 0: a real chart always supplies them, and a
    # test that does not is not exercising this tie, so it must not crash here.
    return (a if degrees.get(a, 0.0) >= degrees.get(b, 0.0) else b), False


def sign_lengths(positions: dict[str, int], degrees: dict[str, float] | None = None):
    """The Chara Daśā length, in whole years, of every rāśi for one chart.

    `positions` maps a graha key (sun..ketu) to the rāśi index 0-11 it occupies.
    `degrees` maps the same keys to degrees-within-sign 0-30, needed only to
    break a dual-lord strength tie; may be omitted if no such tie arises.

    Returns a 12-element list, index 0 = Aries, each entry a dict with the
    length and the full working so the number is checkable, never asserted.
    """
    degrees = degrees or {}
    out = []
    for sign in range(12):
        forward = sign in DIRECT_GROUP
        lord, is_own = _operative_lord(sign, positions, degrees)
        if is_own:
            years, counted = 12, None       # own-sign exception, no deduction
        else:
            counted = _count(sign, positions[lord], forward)
            years = max(1, min(12, counted - 1))
        out.append({
            "sign": sign,
            "years": years,
            "lord": lord,
            "lord_sign": positions.get(lord),
            "counted": counted,
            "count_direction": "forward" if forward else "backward",
            "group": "direct" if forward else "indirect",
            "own_sign": is_own,
            "dual": sign in DUAL_LORDS,
        })
    return out


def chara_dasha(positions, degrees=None, *, lagna=None, direction=None):
    """Chara Daśā periods for one chart.

    Always returns the per-sign lengths. If `direction` ("direct"|"reverse") and
    `lagna` are supplied, also returns the ordered sequence of signs with their
    cumulative year offsets from birth. `direction` is NEVER defaulted: the rule
    that picks it is not in the available source, so the caller must state it.

    The order, once a direction is given, is the twelve signs walked from the
    lagna sign — zodiacally forward for "direct", backward for "reverse".
    """
    lengths = sign_lengths(positions, degrees)
    result = {
        "lengths": lengths,
        "total_years": sum(x["years"] for x in lengths),
        "citation": CITATION,
        "rejections": list(REJECTIONS),
        "tier": "jaimini",
    }
    if direction is None or lagna is None:
        result["sequence"] = None
        result["sequence_note"] = SEQUENCE_DIRECTION_UNAVAILABLE
        return result

    if direction not in ("direct", "reverse"):
        raise ValueError("direction must be 'direct', 'reverse', or None")

    step = 1 if direction == "direct" else -1
    order = [(lagna + step * k) % 12 for k in range(12)]
    by_sign = {x["sign"]: x for x in lengths}
    seq, cursor = [], 0.0
    for s in order:
        yrs = by_sign[s]["years"]
        seq.append({"sign": s, "years": yrs,
                    "start_offset": cursor, "end_offset": cursor + yrs})
        cursor += yrs
    result["sequence"] = seq
    result["direction"] = direction
    result["direction_caveat"] = (
        "'direction' was supplied by the caller. The rule that selects direct "
        "vs reverse is not in the available source (book ch.3); it is not "
        "inferred here."
    )
    return result
