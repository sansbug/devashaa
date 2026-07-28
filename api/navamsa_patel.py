"""Navāṁśa (D9) — Part II technique INDEX from C. S. Patel — tier `modern`.

WHAT THIS IS (and, deliberately, what it is NOT)
------------------------------------------------
Part II of C. S. Patel's *Navamsa in Astrology* (Ch.XVI-XX) is a body of
INTERPRETIVE result material: the physique/character a rising navāṁśa gives, the
108-navāṁśa readings of the Naṣṭa-Jātaka, the results of a planet in each
navāṁśa, and so on. Those are result TABLES — the substance of the book.

This module reproduces NONE of them. It is a POINTER INDEX, exactly like
`nakshatra_techniques.py` and `rao_pointers.py`: it NAMES each technique in one
line, cites the classical text Patel draws it from and his page, and flags
whether the app could detect the STRUCTURAL trigger from the D9 it already
computes. The reading itself stays Patel's, unquoted. It is `modern`-tier — never
BPHS, never a verdict on any chart. Patel's death-mode combinations (Ch.V/XVIII)
are named as existing but are NOT evaluated: this site does not predict death.

`computable`:
    yes    — the trigger (a D9 sign, a navāṁśa index, a dispositor) is cleanly
             detectable from what the chart already carries.
    partly — the trigger is partly detectable but leans on something the app does
             not compute (D9-internal aspects, an ariṣṭa/timing or death judgment).
    no     — not a structural flag the app computes (e.g. a navāṁśa Aṣṭakavarga).
"""

from __future__ import annotations

TIER = "modern"
SOURCE = "C. S. Patel, Navamsa in Astrology (Sagar Publications, 1997), Part II"
SCOPE_NOTE = (
    "A pointer index of Patel's Part II (Ch.XVI-XX) techniques — each named with "
    "its classical source and page, none of his result tables reproduced. Modern "
    "tier, attributed, never BPHS and never a verdict. The trigger flag says only "
    "whether the app could detect the structural condition; the reading stays "
    "Patel's. His death-mode combinations are named, not evaluated — this site "
    "does not predict death."
)

# Each pointer: the technique named, the classical text Patel cites, his book
# page, whether the app can detect the trigger, and what it would detect. The
# `gist` states the METHOD, never a result the book tabulates.
_TECHNIQUES = [
    {
        "n": 1, "chapter": "XVI", "technique": "Rising-navāṁśa lord",
        "gist": "The planet ruling the rising (D9-lagna) navāṁśa sign shapes the "
                "native's physique and temperament.",
        "source": "Horā-Ratnam Part I (R. Santhanam, pp.406-408)",
        "page": 154, "computable": "yes",
        "detects": "the D9-lagna sign and its dispositor",
    },
    {
        "n": 2, "chapter": "XVI", "technique": "1st–9th navāṁśa of the lagna",
        "gist": "Which of the nine navāṁśas (1–9) the lagna occupies within its "
                "sign marks a character type.",
        "source": "Māna-Sāgarī p.58, vv.1–9",
        "page": 156, "computable": "yes",
        "detects": "the lagna's navāṁśa index 1–9",
    },
    {
        "n": 3, "chapter": "XVII", "technique": "The 108 rising navāṁśas",
        "gist": "Birth in each of the 108 navāṁśas (12 signs × 9) gives a detailed "
                "appearance-and-character reading.",
        "source": "Naṣṭa-Jātaka (Astrological Magazine, Dec 1968)",
        "page": 160, "computable": "yes",
        "detects": "which of the 108 navāṁśas the lagna occupies",
    },
    {
        "n": 4, "chapter": "XVIII", "technique": "Udit navāṁśa — the rising sign",
        "gist": "The rising-navāṁśa SIGN (Meṣa … Mīna) gives a one-line life-"
                "tendency and physique.",
        "source": "Horā-Sāra ch.XXX (Pandit V. S. Sastri)",
        "page": 171, "computable": "yes",
        "detects": "the D9-lagna sign",
    },
    {
        "n": 5, "chapter": "XVIII", "technique": "Ariṣṭa years by rising navāṁśa",
        "gist": "Each rising-navāṁśa sign flags particular ages as ariṣṭa (risk / "
                "disease) years, plus years common to all.",
        "source": "Horā-Sāra ch.XXX",
        "page": 172, "computable": "partly",
        "detects": "the D9-lagna sign (the flagged ages follow); the linked "
                   "death sub-rule is named but not evaluated",
    },
    {
        "n": 6, "chapter": "XIX", "technique": "The Moon's navāṁśa, aspected",
        "gist": "The Moon's navāṁśa, by which planet aspects it, gives results — "
                "scaled by whether the Moon is vargottama (100 / 50 / 25%).",
        "source": "Astrological Magazine, Jan 1969",
        "page": 178, "computable": "partly",
        "detects": "the Moon's D9 sign and vargottama status; D9-internal aspects "
                   "are not computed",
    },
    {
        "n": 7, "chapter": "XIX", "technique": "A planet in another's navāṁśa",
        "gist": "A planet in the navāṁśa OWNED by each of the planets (its own or "
                "another's) gives a character result.",
        "source": "Yavana-Jātaka (Sphujidhwaja) ch.33",
        "page": 181, "computable": "yes",
        "detects": "the dispositor of each graha's D9 sign",
    },
    {
        "n": 8, "chapter": "XX", "technique": "A planet in its own navāṁśa",
        "gist": "A planet occupying its OWN navāṁśa sign gives a distinct result "
                "(the D9 counterpart of svakṣetra).",
        "source": "Horā-Ratnam Part I (R. Santhanam)",
        "page": 184, "computable": "yes",
        "detects": "a graha whose D9 sign it rules",
    },
    {
        "n": 9, "chapter": "XX", "technique": "Each planet in the 1st–9th navāṁśa",
        "gist": "For each planet, which of the nine navāṁśas (1–9) it occupies "
                "gives a result and a life-span note.",
        "source": "Aṅkana Śāstra",
        "page": 187, "computable": "yes",
        "detects": "each graha's navāṁśa index 1–9",
    },
    {
        "n": 10, "chapter": "XX", "technique": "Navāṁśa Aṣṭakavarga & Rāśi↔Navāṁśa",
        "gist": "An Aṣṭakavarga cast on the navāṁśa chart, and a comparative "
                "reading of the rāśi and navāṁśa charts together.",
        "source": "Patel Ch.XX (miscellaneous)",
        "page": 200, "computable": "no",
        "detects": "not built — the navāṁśa Aṣṭakavarga is a separate computation",
    },
]


def part2_techniques() -> dict:
    """The `modern`-tier pointer index of Patel's Part II navāṁśa techniques."""
    return {
        "tier": TIER,
        "source": SOURCE,
        "note": SCOPE_NOTE,
        "count": len(_TECHNIQUES),
        "techniques": [dict(t) for t in _TECHNIQUES],
    }
