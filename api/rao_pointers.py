"""Adjacent modern pointers — K.N. Rao — on the `modern` tier, NOT BPHS.

§3b of docs/traditional-rules.md. These are NOT nakṣatra-based, so they are kept
in their own "K.N. Rao (modern)" bucket and NEVER merged with the Saptarishis
nakṣatra technique set (api/nakshatra_techniques.py) or with anything BPHS. Same
pointer-only discipline: a neutral gist + page + a `computable` structural-trigger
flag, no worked examples, no prose reproduced, and never a chart verdict.

`computable` describes only whether the app COULD detect the structural condition,
never whether the reading is endorsed:
    yes    — a clean structural flag
    partly — needs an affliction / strength judgment we can only approximate
    no     — interpretive, or method guidance rather than a chart condition

TWO SOURCES, TWO SHAPES
-----------------------
1. *Enigmas in Astrology* — a ten-pointer method for ASSESSING the Gajakesari
   (Moon-Jupiter) yoga. Captured in full as pointers.
2. *Astrology Lessons, Part A* — the excerpt mostly reproduces classical FACT
   tables that are `traditional` and already in the app's BPHS core, so they are
   NOT re-served here (cross-check only). Its genuinely-modern items (the P.A.C.
   mnemonic and its P.A.C.D.A.R.E.S. extension, a spiritual-house framework, an
   Ariṣṭa/health checklist, modern-profession significations) are NAMED only —
   their content is not in the captured excerpt, so it is not reproduced.
"""

from __future__ import annotations

TIER = "modern"

GAJAKESARI_SOURCE = "K.N. Rao, Enigmas in Astrology (Gajakesari-yoga assessment)"
LESSONS_SOURCE = "K.N. Rao, Astrology Lessons, Part A"

BUCKET_NOTE = (
    "One modern author's method notes — not BPHS, not the traditional canon, and "
    "never a chart verdict. Not nakṣatra-based; kept in their own bucket. Captured "
    "as attributed pointers only."
)

# (title, gist, computable, page)
_GAJAKESARI = [
    ("Three/four-fold assessment",
     "Judge the yoga from the lagna, from the Moon, and via the 10th house / 10th "
     "lord counted from each, weighing aspects and associations.", "partly", "23"),
    ("Too common to read naively",
     "The Moon forms it about a third of each month and by rising lagna, so a large "
     "share of people carry it — never apply its promise blindly.", "no", "14, 23"),
    ("Sign-type parity constraint",
     "Moon and Jupiter in mutual kendras always share the same modality (movable / "
     "fixed / dual); both cannot be exalted or both debilitated.", "yes", "13-14"),
    ("Jupiter primary, Moon secondary",
     "Jupiter's sign, ownership and condition carry more weight than the Moon's.",
     "no", "14"),
    ("Seven schemes of modification",
     "Degraders — a retrograde / combust / malefic-hit Jupiter, or the Moon in "
     "gaṇḍānta / kemadruma / heavy affliction — plus examining the full daśā and "
     "antardaśā of both.", "no", "16"),
    ("Grading good / better / best",
     "By whether Jupiter or the Moon is merely unafflicted, in mūlatrikoṇa, or "
     "exalted and benefic-joined.", "partly", "36"),
    ("Strength check",
     "Graha bala, an aṣṭakavarga method, and vargottama status.", "partly", "36"),
    ("Timing by daśā",
     "Full results come in the Moon or Jupiter mahādaśās; certain following "
     "yogakāraka daśās can exceed them.", "no", "36-37"),
    ("Per-lagna significance",
     "The identical yoga means different things by ascendant, through the specific "
     "houses the Moon and Jupiter own.", "partly", "21-22"),
    ("Damage-control in dusthāna axes",
     "On a 6/8/12 axis, read it as protective rather than glorifying — the 3rd "
     "house an exception, favouring artistic work.", "partly", "45"),
]

# Fact tables in Astrology Lessons that are `traditional` and already in the app's
# BPHS core — listed for transparency, NOT re-served here (cross-check only).
_LESSONS_TRADITIONAL = [
    "weekday rulers", "nakṣatra Viṁśottarī lords / years", "rāśi lordships",
    "exaltation / debilitation / mūlatrikoṇa / own-house", "graha aspects",
    "kendra / trikoṇa house categories", "rāśi attributes", "natural kārakas",
    "house significations", "māraka lords",
]

# The genuinely-modern items — NAMED only; their content is not in the excerpt.
_LESSONS_MODERN = [
    ("P.A.C.", "Position–Aspect–Conjunction — his rule of the three ways a graha acts on a house."),
    ("P.A.C.D.A.R.E.S.", "P.A.C. extended with a D.A.R.E.S. step (content not in the captured excerpt)."),
    ("Spiritual-house framework", "His scheme of the houses that signify spiritual life."),
    ("Ariṣṭa / health checklist", "His checklist of combinations for ill-health / early-life risk."),
    ("Modern-profession significations", "His mapping of contemporary careers onto grahas/houses."),
]


def _pointer(title: str, gist: str, computable: str, page: str) -> dict:
    return {
        "title": title,
        "gist": gist,
        "computable": computable,
        "page": page,
        "tier": TIER,
        "cite": f"modern technique — {GAJAKESARI_SOURCE}, p.{page}",
    }


def gajakesari() -> dict:
    """The ten-pointer Gajakesari-yoga assessment method."""
    return {
        "topic": "Gajakesari yoga — assessment method",
        "source": GAJAKESARI_SOURCE,
        "tier": TIER,
        "pointers": [_pointer(t, g, c, p) for (t, g, c, p) in _GAJAKESARI],
    }


def astrology_lessons() -> dict:
    """The Astrology Lessons Part A tiering note — traditional tables (cross-check
    only) and the named modern pointers (content not reproduced)."""
    return {
        "topic": "Astrology Lessons, Part A",
        "source": LESSONS_SOURCE,
        "tier": TIER,
        "traditional_tables": {
            "note": "Fact tables that are `traditional` and almost all already in "
                    "the app's BPHS core — kept as a cross-check only, not re-served "
                    "here.",
            "items": list(_LESSONS_TRADITIONAL),
        },
        "modern_pointers": {
            "note": "Genuinely-modern items — named only; their content is not in "
                    "the captured excerpt, so it is not reproduced.",
            "items": [{"name": n, "gist": g} for (n, g) in _LESSONS_MODERN],
        },
    }


def bucket() -> dict:
    """The whole K.N. Rao (modern) bucket."""
    return {
        "tier": TIER,
        "note": BUCKET_NOTE,
        "gajakesari": gajakesari(),
        "astrology_lessons": astrology_lessons(),
    }
