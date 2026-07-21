"""Nakṣatra attributes on the `traditional` tier — NOT BPHS, NOT invented.

WHAT THIS IS, AND THE HARD LIMIT ON IT
--------------------------------------
The app already computes, for all 27 nakṣatras and from BPHS:
    - the nakṣatra name and its deity   (BPHS ch.6 vv.24-26, vedic.NAKSHATRAS)
    - the Viṁśottarī lord               (BPHS ch.46, derived)
    - the pāda→rāśi / navāṁśa spans     (arithmetic)

The classical SYMBOL of a nakṣatra (Aśvinī = a horse's head, Bharaṇī = the yoni,
…) is NOT in BPHS — the rāśi cards correctly mark this whole layer "BPHS is
silent (ch.3 v.7)". It belongs to the older Bṛhat-Saṁhitā / muhūrta tradition,
so it ships here on a `traditional` footing, beside the BPHS deity and never as
Parāśara.

THE SOURCE ONLY COVERS NINE OF TWENTY-SEVEN.
The book these symbols came from — *Predicting Through Nakṣatras, Part I*
(Saptarishis) — tabulates only Aśvinī → Āśleṣā. Rows 10-27 are simply not in it.
Every one of the nine present was cross-checked, cell by cell, against the
canonical classical standard: zero corrections needed. But the eighteen absent
rows are left ABSENT, not filled from memory. Inventing a symbol for Maghā
because "everyone knows it is a throne" is exactly the fabrication this project
refuses, and the reason the rāśi cards refuse this material in the first place.

So `symbol_of(i)` returns the sourced string for 1-9 and None for 10-27, and the
UI must render that None as an explicit "not yet sourced on this tier" gap — the
same first-class-absence pattern used everywhere else here.

The book states NO gaṇa, yoni or nāḍī for any nakṣatra, so this module carries
none. A complete gaṇa/yoni/nāḍī table needs a primary source (Bṛhat Saṁhitā
ch.98, or Parts II-III of the nakṣatra series) and is deliberately not faked.
"""

from __future__ import annotations

TIER = "traditional"
CITATION = "Predicting Through Nakṣatras, Part I (Saptarishis); classical symbols cross-checked against the Bṛhat-Saṁhitā / muhūrta standard"

# Which indices the source volume actually covers. Everything outside this range
# is a sourcing gap, not a nakṣatra without a symbol.
SOURCED = range(1, 10)   # 1..9 inclusive

SOURCE_NOTE = (
    "Symbols are sourced only for nakṣatras 1-9 (Aśvinī → Āśleṣā); the source "
    "book is Part I and does not cover Maghā → Revatī. The remaining eighteen "
    "are shown as not-yet-sourced rather than guessed."
)

# 1-indexed. Alternate symbols the tradition also records are kept, because more
# than one is genuinely canonical (Puṣya is variously a cow's udder, a lotus or
# an arrow). Verified against the canonical standard; zero corrections.
_SYMBOL = {
    1: "Horse's head",
    2: "Yoni (the vulva / womb)",
    3: "Knife or razor / a flame",
    4: "Cart or chariot",
    5: "Deer's or antelope's head",
    6: "A teardrop, or a human head",
    7: "A bow and quiver of arrows",
    8: "A cow's udder, a lotus, or an arrow",
    9: "A coiled serpent",
}


def symbol_of(index: int) -> dict:
    """The classical symbol for a nakṣatra (1-27), or an explicit gap.

    `index` is 1-based, Aśvinī = 1. Returns a dict carrying the tier and either
    the sourced symbol or `available: False` with the reason — never a guess.
    """
    if not 1 <= index <= 27:
        raise ValueError(f"nakṣatra index out of range: {index}")
    if index in _SYMBOL:
        return {
            "attribute": "symbol",
            "value": _SYMBOL[index],
            "tier": TIER,
            "citation": CITATION,
            "available": True,
        }
    return {
        "attribute": "symbol",
        "value": None,
        "tier": TIER,
        "available": False,
        "reason": "Not yet sourced. The Part I source volume covers only "
                  "Aśvinī → Āśleṣā; this symbol needs a primary source (Bṛhat "
                  "Saṁhitā ch.98, or a later part of the nakṣatra series) and "
                  "is deliberately not guessed.",
    }


def all_symbols() -> list[dict]:
    """Symbol status for every nakṣatra 1-27 — sourced ones and the gaps."""
    return [{"index": i, **symbol_of(i)} for i in range(1, 28)]
