"""Bhāva-phala — a house-by-house reading, as a stack of CITED rules that fire.

This is the interpretive layer: it takes the relationships the chart already
computes (whole-sign house placement, rāśi lordship, graha dṛṣṭi) and attaches
the BPHS rules that speak to each house — WITHOUT synthesising a verdict.

Per house it assembles:
  · the LORD-IN-HOUSE effect — where this house's lord sits (BPHS ch.24, one
    cited verse per (lord, house)); if the lord rules two houses, the ch.24
    vv.145-148 combination rule is flagged (both lordships apply; contrary →
    nullify) — the ONLY licensed way to combine, quoted, never gone beyond;
  · the house's SIGNIFICATIONS (ch.11) and its KĀRAKA (ch.32);
  · the OCCUPANTS — listed for context with NO asserted effect, because BPHS
    Vol I gives no systematic seven-graha-in-bhāva table (a sourced refusal);
  · the grahas ASPECTING the house (graha dṛṣṭi, ch.26) — a fact.

There is deliberately NO composite score and NO per-house verdict: BPHS states
these judgements separately and never says how to fuse them (the same stance the
signal stack and daśā-effects engines take). The reader does the synthesis; this
engine supplies the cited evidence, organised by life-area.
"""

from __future__ import annotations

from dignity import RASI_LORD
from drishti import graha_drishti_chart
import bhava_phala_rules as R

PLANET_IN_HOUSE_NOTE = (
    "BPHS Vol I gives no systematic seven-graha-in-bhāva table (chs 12-23 are "
    "organised by house-matter, not by planet). So a graha's occupancy of a "
    "house carries no cited effect here — occupants are shown for context, with "
    "their own dignity/state, never asserted as a rule."
)
NO_COMPOSITE_NOTE = (
    "No per-house verdict or score. BPHS states the lord-effect, significations "
    "and kāraka separately and never fuses them; any single summary would be our "
    "arithmetic, not Parāśara's. The only combination it licenses is ch.24 "
    "vv.145-148, applied when a lord rules two houses."
)


def _house_of(rasi: int, lagna: int) -> int:
    """Whole-sign house (1-12) of a sign, counted from the lagna sign."""
    return (rasi - lagna) % 12 + 1


def bhava_phala(positions: dict, lagna: int, lang: str = "en") -> dict:
    """`positions` maps graha key -> {"rasi": int, ...}; `lagna` is the lagna sign
    (0-11). ``lang='hi'`` serves the Hindi renderings (bhava_phala_rules_hi) for
    every string that has one, falling back to English otherwise."""
    H = None
    if lang == "hi":
        try:
            import bhava_phala_rules_hi as H
        except Exception:
            H = None
    rasi = {g: p["rasi"] for g, p in positions.items()}

    # Which houses each graha lords (a graha owns two rāśis, so two houses).
    lords_of: dict[str, list[int]] = {}
    for h in range(1, 13):
        sign = (lagna + h - 1) % 12
        lords_of.setdefault(RASI_LORD[sign], []).append(h)

    # Grahas aspecting each sign (graha dṛṣṭi, ch.26). Nodes cast none, per the
    # natal engine's default.
    received = graha_drishti_chart(rasi)["received"]["signs"]

    bhavas = []
    for h in range(1, 13):
        sign = (lagna + h - 1) % 12
        lord = RASI_LORD[sign]
        lord_house = _house_of(rasi[lord], lagna) if lord in rasi else None

        rule = R.LORD_IN_HOUSE.get((h, lord_house)) if lord_house else None
        lord_rule = None
        if rule:
            k = (h, lord_house)
            lord_rule = {
                "verse": rule["verse"],
                "citation": f"BPHS I ch.24 v.{rule['verse']}",
                "effect": H.EFFECTS_HI.get(k, rule["effect"]) if H else rule["effect"],
                "lagna_exception": (H.EXCEPTIONS_HI.get(k, rule["lagna_exception"])
                                    if H else rule["lagna_exception"]),
                "exception_source": rule["exception_source"],
                "notes_caveat": (H.CAVEATS_HI.get(k, rule["notes_caveat"])
                                 if H else rule["notes_caveat"]),
            }

        # Dual lordship: this lord also rules these OTHER houses → ch.24 vv.145-148.
        also_rules = [x for x in lords_of.get(lord, []) if x != h]

        occupants = sorted(g for g, r in rasi.items() if _house_of(r, lagna) == h)
        aspects_in = sorted(
            ({"graha": g, "strength": round(f, 3)} for g, f in received.get(sign, {}).items()),
            key=lambda a: -a["strength"],
        )

        bhavas.append({
            "house": h,
            "sign": sign,
            "lord": lord,
            "lord_in_house": lord_house,             # where the lord sits (1-12)
            "lord_rule": lord_rule,                  # cited ch.24 effect
            "lord_also_rules": also_rules,           # other houses this lord owns
            "combination_applies": bool(also_rules), # ch.24 vv.145-148 in play
            "significations": ({**R.HOUSE_SIGNIFICATIONS[h], "text": H.SIGNIF_HI[h]}
                               if H and h in H.SIGNIF_HI else R.HOUSE_SIGNIFICATIONS[h]),   # ch.11
            "karaka": R.HOUSE_KARAKA[h],             # graha key; join to its signal-stack state
            "karaka_citation": "BPHS I ch.32 vv.31-34",
            "occupants": occupants,                  # context only — no cited effect (see note)
            "aspects_in": aspects_in,                # grahas aspecting the house (ch.26)
        })

    return {
        "bhavas": bhavas,
        "combination_rule": (H.COMBINATION_RULE_HI if H and H.COMBINATION_RULE_HI
                             else R.COMBINATION_RULE),      # ch.24 vv.145-148, verbatim
        "planet_in_house": (H.PLANET_IN_HOUSE_NOTE_HI if H and H.PLANET_IN_HOUSE_NOTE_HI
                            else PLANET_IN_HOUSE_NOTE),     # the sourced refusal
        "no_composite": (H.NO_COMPOSITE_HI if H and H.NO_COMPOSITE_HI
                         else NO_COMPOSITE_NOTE),
        "source": "BPHS Vol I (Santhanam): ch.24 lord-in-house, ch.11 significations, ch.32 kārakas.",
    }
