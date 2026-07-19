"""Antardaśā conditions — which of BPHS ch.52-60's clauses fire on a chart.

THIS IS A CONDITION-FIRING ENGINE, NOT A VERDICT ENGINE.

The distinction is forced by the corpus, not by caution. Two censuses over
ch.52-60's 559 conditions decided it:

  FRAMES — 326 conditions reference a house. 111 count from the lagna, 107 from
  the daśā lord, 1 from the Moon, and 107 STATE NO FRAME AT ALL. Two thirds are
  computable, so refusing to compute would throw away most of the corpus; but
  the unframed third clusters on the OPENING kendra/trikoṇa branch of a cell —
  the branch a real chart most often lands on. Those are returned UNAVAILABLE
  and counted, never silently skipped, because an engine that omits them
  reports "nothing fires" on charts where BPHS does state something.

  POLARITY — roughly one branch in five carries a valence word, and the mined
  data does not record whether that word governs the branch or merely names an
  item in an outcome list. So polarity is passed through for display beside its
  quote and NEVER used to derive a state. No antardaśā band is coloured.

What this returns is: for each (mahā, antar) pair, the conditions that FIRE,
each with its quoted śloka — plus an explicit count of what could not be
evaluated and why. The reader gets the text, not our opinion of it.

WHAT IS DELIBERATELY NOT EVALUATED
----------------------------------
* Any house condition whose frame is `unstated`. No default. Adjacency supplies
  none either: ch.55's Mercury vv.36-38 sits immediately after a verse glossed
  "from the lord of the Dasa" and its Moon vv.68-70 immediately before one.
* Predicates that are not house tests — dignity is often computable but
  combustion orbs, "endowed with strength", "favourable in transit" and
  aspect/association clauses are variously undefined in BPHS or need machinery
  this project does not have. They report unavailable with the predicate shown.
* Conditions whose house numbers are OCR-destroyed. ch.56's "the 6th or the6rh"
  is *probably* 6/8/12 and ch.60's Saturn "8th, llth, 12th" *probably* 6/8/12,
  but pattern-matching a damaged numeral into a verdict about someone's life is
  exactly the failure this project exists to avoid.
"""

from __future__ import annotations

import re

import antardasa_rules as rules
from dasha_effects import bhava_from

FIRED = "fired"
NOT_FIRED = "not_fired"
UNAVAILABLE = "unavailable"

# Whole-sign house groups named in the ślokas by name rather than by number.
KENDRA = (1, 4, 7, 10)
TRIKONA = (1, 5, 9)
DUSTHANA = (6, 8, 12)
UPACHAYA = (3, 6, 10, 11)

_GROUPS = {"kendra": KENDRA, "trikona": TRIKONA, "trikone": TRIKONA,
           "kona": TRIKONA, "dusthana": DUSTHANA, "upachaya": UPACHAYA}

# A clean ordinal: 1-12, optionally with an English suffix. Anything else that
# carries a digit is treated as damage.
_CLEAN = re.compile(r"^(\d{1,2})(st|nd|rd|th)?$")
# The scan's characteristic numeral damage: 'l' standing in for '1', so "llth"
# is 11th and "l2th" is 12th. These are RECOVERABLE BY EYE AND MUST NOT BE
# RECOVERED BY CODE — see the module docstring. Their presence poisons the
# whole spec, because a partial parse is worse than none: "8th, llth, 12th"
# would otherwise silently become (8, 12) and quietly drop the 11th.
_DAMAGED = re.compile(r"\d[a-z]|[a-z]\d|\bl+\d|\bl{2,}", re.I)


def parse_houses(spec: str):
    """The mined `houses` string -> a tuple of house numbers, or None.

    None means UNEVALUABLE, never "matched nothing". A condition we cannot
    parse has not failed to fire; it has failed to be evaluated at all, and the
    caller must report it as unavailable rather than as a quiet negative.

    Refuses the entire spec if any token shows numeral damage. Salvaging the
    legible numbers from a damaged list is exactly the pattern-matching this
    project refuses: it produces a confident, partial, wrong answer about a
    real person's chart.
    """
    if not spec:
        return None
    text = str(spec).replace("/", ",")
    out, saw_number = set(), False
    for part in text.split(","):
        p = part.strip().lower()
        if not p:
            continue
        named = [g for name, g in _GROUPS.items() if name in p]
        if named:
            for g in named:
                out.update(g)
            continue
        m = _CLEAN.match(p)
        if m:
            v = int(m.group(1))
            if 1 <= v <= 12:
                out.add(v)
                saw_number = True
                continue
            return None            # an out-of-range house is not a house
        if _DAMAGED.search(p) or any(ch.isdigit() for ch in p):
            return None            # damaged, or a numeral we cannot read cleanly
    if not out:
        return None
    return tuple(sorted(out))


def _origin(frame, lagna, maha_lord_sign, moon_sign):
    if frame == "from_lagna":
        return lagna
    if frame == "from_dasa_lord":
        return maha_lord_sign
    if frame == "from_moon":
        return moon_sign
    return None


def evaluate_condition(cond, *, antar_sign, lagna, maha_lord_sign, moon_sign):
    """One condition against one chart. fired / not_fired / unavailable.

    The subject of these clauses is the ANTARDAŚĀ lord — "if he be in a kendra"
    inside ch.56's Śani section means Śani, the antar lord, not Guru.
    """
    frame = cond.get("frame")
    base = {
        "predicate": cond.get("predicate"),
        "frame": frame,
        "frame_quote": cond.get("frame_quote"),
        "polarity": cond.get("polarity"),
        "polarity_word": cond.get("polarity_word"),
        "polarity_scope_unresolved": cond.get("polarity") != "none",
        "results": cond.get("results"),
        "source": cond.get("source"),
        "quote": cond.get("quote"),
        "pdf_page": cond.get("pdf_page"),
        "ocr_flag": cond.get("ocr_flag") or None,
    }

    if frame == "not_a_house":
        return {**base, "state": UNAVAILABLE,
                "reason": "Not a house condition. It tests dignity, "
                          "association, combustion, strength or transit — "
                          "predicates BPHS either leaves undefined here or "
                          "that need machinery this engine does not have."}

    if frame == "unstated":
        return {**base, "state": UNAVAILABLE,
                "reason": "The śloka names a house but no reference frame — "
                          "neither 'from the Ascendant' nor 'from the lord of "
                          "the Dasa'. BPHS does not resolve it and neither do "
                          "we; a frame assumed here would be a confident wrong "
                          "answer. Roughly one house condition in three is like "
                          "this, and they cluster on the opening favourable "
                          "branch of a cell."}

    houses = parse_houses(cond.get("houses"))
    if houses is None:
        return {**base, "state": UNAVAILABLE,
                "reason": "The house numbers are not legibly recoverable from "
                          "this scan." if cond.get("ocr_flag") else
                          "No house numbers could be read from this clause."}

    origin = _origin(frame, lagna, maha_lord_sign, moon_sign)
    if origin is None:
        return {**base, "state": UNAVAILABLE, "reason": f"unknown frame {frame!r}"}

    h = bhava_from(origin, antar_sign)
    return {**base,
            "state": FIRED if h in houses else NOT_FIRED,
            "houses": list(houses),
            "actual_bhava": h,
            "reading": f"the antardaśā lord stands in the {h}"
                       f"{'st' if h == 1 else 'nd' if h == 2 else 'rd' if h == 3 else 'th'}"
                       f" {frame.replace('from_', 'from the ').replace('_', ' ')}"}


def evaluate_cell(maha_lord, antar_lord, *, positions, lagna):
    """Every condition of one (mahā, antar) cell against one chart."""
    c = rules.cell(maha_lord, antar_lord)
    if c is None:
        return None

    antar_sign = positions.get(antar_lord)
    maha_sign = positions.get(maha_lord)
    moon_sign = positions.get("moon")
    if antar_sign is None or maha_sign is None:
        return None

    evaluated = [
        evaluate_condition(x, antar_sign=antar_sign, lagna=lagna,
                           maha_lord_sign=maha_sign, moon_sign=moon_sign)
        for x in c["conditions"]
    ]
    fired = [e for e in evaluated if e["state"] == FIRED]
    unavailable = [e for e in evaluated if e["state"] == UNAVAILABLE]

    return {
        "maha_lord": maha_lord,
        "antar_lord": antar_lord,
        "chapter": f"BPHS Vol II ch.{rules.CHAPTER_OF[maha_lord]}",
        "verses": c["verses"],
        "conditions": evaluated,
        "fired": fired,
        "counts": {
            "total": len(evaluated),
            "fired": len(fired),
            "not_fired": sum(1 for e in evaluated if e["state"] == NOT_FIRED),
            "unavailable": len(unavailable),
        },
        # Absent is not empty. ch.52's Jupiter cell is the only one in its
        # chapter with no death clause at all, and that is a fact about the
        # text rather than a hole in the data.
        "maraka": c["maraka"],
        "remedy": c["remedy"],
        # Carried so a UI can say "3 of 8 conditions here could not be
        # evaluated" instead of implying the text is silent.
        "polarity_scope_unresolved": rules.POLARITY_SCOPE_UNRESOLVED,
        "no_verdict": (
            "BPHS labels only about one antardaśā branch in five, and does not "
            "state how a mahādaśā verdict and an antardaśā condition combine. "
            "This cell reports which clauses fire, not whether the period is "
            "good."
        ),
    }


def evaluate_chart(positions: dict[str, int], lagna: int) -> dict:
    """All 81 cells against one chart, plus a corpus-level summary."""
    cells, totals = {}, {"fired": 0, "not_fired": 0, "unavailable": 0, "total": 0}
    for maha in rules.CHAPTER_OF:
        for antar in rules.CHAPTER_OF:
            got = evaluate_cell(maha, antar, positions=positions, lagna=lagna)
            if got is None:
                continue
            cells[f"{maha}|{antar}"] = got
            for k in totals:
                totals[k] += got["counts"][k]
    return {
        "cells": cells,
        "totals": totals,
        "citation": rules.CITATION,
        "note": (
            "Condition firing, not a verdict. Of the corpus's house conditions "
            "about one in three states no reference frame, and roughly one "
            "branch in five carries any valence word at all — so this reports "
            "which clauses of ch.52-60 apply to this chart and quotes them, "
            "and colours nothing."
        ),
    }
