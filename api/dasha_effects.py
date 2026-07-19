"""Daśā verdicts — BPHS Vol II ch.47 vv.5-6.

WHY THIS EXISTS WHEN THE GRAHA SCORE DOES NOT
----------------------------------------------
This project refuses to put an uncited good/bad score on a GRAHA, because BPHS
supplies seven overlapping judgements of a graha and never combines them.

The daśā chapters are genuinely different. Parāśara here states a NAMED verdict
and names the inputs that drive it, in one verse, and it survived eight
independent adversarial audits without a challenge:

    5-6. "The effects are favourable if, at the commencernent [commencement]
    of the Dasa, the Dasa lord be in the Ascendant, in his sign of exaltation,
    in his own sign or in a friend's sign. The results are unfavourable if the
    Dasa lord be in the 6th, the 8th, or the l2th [12th] house, in his sign of
    debilitation or in an inimical .sign."
                    — Vol II ch.47 vv.5-6, PDFPAGE 87, mūla

Every condition it names is something this engine already computes. That is a
verdict on results, not a description of results, and it is why a daśā band may
carry a state where a graha may not.

WHAT THIS IS NOT
----------------
NOT a heatmap. There is no gradient here and there must not be, for reasons the
text itself supplies:

  * THERE IS NO MIDDLE BAND. "Medium effects" occurs exactly ONCE in the whole
    265-page effects section (ch.52 vv.1-3) and is scoped to a single cell —
    the Sun's antardaśā in the Sun's own daśā. No carrier clause generalises it,
    and all eight remaining antardaśā chapters open with two branches and no
    residual. So a chart matching neither branch has NO STATED VERDICT. That is
    `not_stated`, not "medium". Filling it as medium would be the uncited score
    wearing a new costume.

  * THERE IS NO RANK. "Extremely favourable" and "extremely beneficial" each
    occur once, both describing the same configuration. Two hapax intensifiers
    are not a scale.

  * THERE IS NO COMBINATION RULE. Nothing says what happens when a favourable
    and an adverse condition BOTH fire — exalted and in the 8th. So that case is
    reported as `contested` and left unarbitrated, because the text leaves it
    unarbitrated. The only combination rule in the volume is under "Notes :",
    which is Santhanam, not Parāśara.

`not_stated` will be the most common outcome on most charts. That is correct,
and it is the point.
"""

from __future__ import annotations

import dignity

# ch.47 v.5-6, the two named house sets. Whole-sign bhāvas throughout.
FAVOURABLE_HOUSES = (1,)
ADVERSE_HOUSES = (6, 8, 12)

CITATION = "BPHS Vol II ch.47 vv.5-6"

FAVOURABLE = "favourable"
ADVERSE = "adverse"
CONTESTED = "contested"
NOT_STATED = "not_stated"

# "at the commencement of the Dasa" — we read this as the daśā lord's NATAL
# placement, which is the standard reading and the only one this engine can
# support: BPHS supplies no transit machinery in these chapters, and a graha's
# natal position is what does not change across the daśā. Flagged rather than
# assumed silently, because a transit reading would give different answers.
FRAME_NOTE = (
    "Read from the daśā lord's NATAL placement. The verse says 'at the "
    "commencement of the Dasa'; BPHS gives no transit rule in these chapters, "
    "so the natal position is used. A transit reading would differ."
)

# The nodes own no rāśi and BPHS gives them no dignity (ch.3 v.50), so four of
# the six conditions cannot be evaluated for them at all. The two HOUSE
# conditions still can. We therefore evaluate them partially and say so, rather
# than either inventing a dignity or refusing a verdict the verse can support.
NODE_NOTE = (
    "Rāhu and Ketu own no rāśi and BPHS assigns them no exaltation, "
    "debilitation or natural relationships (ch.3 v.50). Only the two HOUSE "
    "conditions of ch.47 vv.5-6 are evaluable for them; the four sign "
    "conditions are not."
)

MOOLATRIKONA_NOTE = (
    "ch.47 vv.5-6 names exaltation, own sign, friend's sign, debilitation and "
    "inimical sign — it does NOT name mūlatrikoṇa. A graha in mūlatrikoṇa is "
    "tested on whether that sign is its own or a friend's, which is not always "
    "the case: Candra's mūlatrikoṇa is Vṛṣabha, which belongs to Śukra."
)


def _bhava(sign: int, lagna: int) -> int:
    """Whole-sign bhāva of a rāśi counted from the lagna. 1-12."""
    return (sign - lagna) % 12 + 1


def verdict(graha: str, sign: int, lagna: int) -> dict:
    """ch.47 vv.5-6 applied to one daśā lord.

    `sign` is the rāśi the lord occupies natally; `lagna` the ascendant's rāśi.

    Returns the state plus EVERY condition that fired, each quoting the clause
    of the verse it came from — so a reader can check the verdict against the
    śloka rather than trusting it.
    """
    bhava = _bhava(sign, lagna)
    lord_of_sign = dignity.RASI_LORD[sign]
    is_node = graha not in dignity.EXALTATION

    fav, adv, caveats = [], [], []

    # --- the two house conditions. These hold for every graha, nodes included.
    if bhava in FAVOURABLE_HOUSES:
        fav.append({"condition": "in the Ascendant", "detail": f"bhāva {bhava}"})
    if bhava in ADVERSE_HOUSES:
        adv.append({"condition": "in the 6th, the 8th, or the 12th house",
                    "detail": f"bhāva {bhava}"})

    if is_node:
        caveats.append(NODE_NOTE)
    else:
        d = dignity.dignity_of(graha, sign * 30 + 15.0)   # mid-sign: the verse
        state = d["state"]                                # is sign-level, not
        if state == "moolatrikona":                       # degree-level
            caveats.append(MOOLATRIKONA_NOTE)

        if d["exaltation"]["sign"] == sign:
            fav.append({"condition": "in his sign of exaltation",
                        "detail": f"exalted in this rāśi"})
        if d["debilitation"]["sign"] == sign:
            adv.append({"condition": "in his sign of debilitation",
                        "detail": f"debilitated in this rāśi"})
        if lord_of_sign == graha:
            fav.append({"condition": "in his own sign",
                        "detail": f"the rāśi is ruled by {graha}"})
        else:
            rel = dignity.NATURAL_RELATIONS[graha].get(lord_of_sign)
            if rel == "friend":
                fav.append({"condition": "in a friend's sign",
                            "detail": f"ruled by {lord_of_sign}, a natural friend"})
            elif rel == "enemy":
                adv.append({"condition": "in an inimical sign",
                            "detail": f"ruled by {lord_of_sign}, a natural enemy"})
            # "neutral" is named by NEITHER branch of the verse. It contributes
            # nothing — which is exactly how `not_stated` arises.

        if graha in dignity.MOOLATRIKONA_UNVERIFIED:
            caveats.append(
                "This graha's mūlatrikoṇa arc comes from an OCR-damaged śloka, "
                "and its natural relationships derive from it (ch.3 v.55)."
            )

    if fav and adv:
        state = CONTESTED
    elif fav:
        state = FAVOURABLE
    elif adv:
        state = ADVERSE
    else:
        state = NOT_STATED

    return {
        "state": state,
        "graha": graha,
        "sign": sign,
        "bhava": bhava,
        "favourable": fav,
        "adverse": adv,
        "caveats": caveats + [FRAME_NOTE],
        "citation": CITATION,
        "verse": (
            "The effects are favourable if, at the commencernent [commencement] "
            "of the Dasa, the Dasa lord be in the Ascendant, in his sign of "
            "exaltation, in his own sign or in a friend's sign. The results are "
            "unfavourable if the Dasa lord be in the 6th, the 8th, or the l2th "
            "[12th] house, in his sign of debilitation or in an inimical .sign."
        ),
        "label": {
            FAVOURABLE: "favourable",
            ADVERSE: "adverse",
            CONTESTED: "both stated — BPHS does not arbitrate",
            NOT_STATED: "no stated verdict",
        }[state],
        # The one honest thing a UI must not lose: when nothing fired, the text
        # is silent, and silence is not neutrality.
        "silent": state == NOT_STATED,
    }


def verdicts_for_chart(positions: dict[str, int], lagna: int) -> dict[str, dict]:
    """ch.47 vv.5-6 for every graha. `positions` maps graha key -> rāśi index."""
    return {g: verdict(g, s, lagna) for g, s in positions.items()}
