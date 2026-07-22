"""Nakṣatra attributes on the `traditional` tier — NOT BPHS, NOT invented.

WHAT THIS IS, AND THE TIER IT SITS ON
-------------------------------------
The app already computes, for all 27 nakṣatras and from BPHS:
    - the nakṣatra name and its deity   (BPHS ch.6, vedic.NAKSHATRAS)
    - the Viṁśottarī lord               (BPHS ch.46, derived)
    - the pāda→rāśi / navāṁśa spans     (arithmetic)

The classical SYMBOL of a nakṣatra (Aśvinī = a horse's head, Bharaṇī = the yoni,
…) and the muhūrta-tradition classifications (gaṇa, yoni/animal, kālapuruṣa
body-part, puruṣārtha, quality, śakti) are NOT in BPHS — the rāśi cards correctly
mark this whole layer "BPHS is silent (ch.3 v.7)". They belong to the older
Bṛhat-Saṁhitā / muhūrta tradition, so they ship here on a `traditional` footing,
beside the BPHS deity and never as Parāśara.

WHERE EACH CELL COMES FROM, AND HOW SURE WE ARE
-----------------------------------------------
Every value here was transcribed from a named source, never filled from memory.
Two scanned books were read (redundantly, then reconciled and cross-checked):

    S1  the established classical symbol set (nakṣatras 1-9, previously shipped)
    S2  Sunil John & V. Pandya, *Predicting Through Nakṣatras, Part 2*
        (Saptarishis) — chapter header tables, nakṣatras 10-18
    S3  Ram Babu Sao, *Perfect Astrology (Nakṣatra)* — §3.2-3.3 classification
        tables, all 27 (gaṇa, yoni/animal, body-part, puruṣārtha, quality, śakti,
        and asterism star-shapes for the symbols S1/S2 do not reach, 19-27)

Each cell carries a `confidence`:
    corroborated  — two independent sources agree
    single_source — one book states it (the honest ceiling for the S3 layer:
                    it is ONE OCR'd book; its two reads are the same book, not
                    independent witnesses)
    uncertain     — the stored value may itself be wrong (a specific competing
                    reading or a flagged OCR artefact); see the note
    absent        — no source states it; a first-class gap, never guessed

THE ONE FIELD BOTH BOOKS LACK: NĀḌĪ.
Neither book carries an Ādi/Madhya/Antya nāḍī table (the whole nakṣatra section
of *Perfect Astrology*, pp.47-85, was scanned to confirm this). So nāḍī is
`absent` for all 27 — not filled from memory, even though the cycle is trivial.
Closing it needs a muhūrta / Aṣṭakūṭa source (Muhūrta Cintāmaṇi, Kālaprakāśikā).

TWO DEITY VARIANCES ARE FLAGGED, NOT APPLIED (now reconciled against BPHS).
Sunil John's headers give Hasta = Savitṛ and Svātī = Vāyu, where the app's
BPHS-cited vedic.py gives Sūrya and Marut. A `traditional` source does not get to
overwrite a BPHS-tier value, so vedic.py is left untouched and the variance is
recorded in DEITY_TRADITION_VARIANTS. That reconciliation was carried out
(2026-07-21) against the BPHS text itself — Santhanam Vol I, ch.6
"24-26. BHAMSA (NAKSHATRAMSA)", pp.78-79 — and the primary Vedic authority,
the Taittirīya Brāhmaṇa III.1.1-5 nakṣatra-devatā hymn: Parāśara genuinely
prints Sūrya (Hasta) and Marut (Svātī), each the same deity-family as the TB's
Savitṛ / Vāyu (solar; wind), so the divergence is a real textual variant, not an
OCR slip. The BPHS reading stands in vedic.py; the two tiers are kept apart, as
always.
"""

from __future__ import annotations

TIER = "traditional"

# Full citations for the provenance ids used in every cell's `sources`.
SOURCES = {
    "S1": "Established classical symbol set (nakṣatras 1-9), cross-checked "
          "against the Bṛhat-Saṁhitā / muhūrta standard",
    "S2": "Sunil John & V. Pandya, Predicting Through Nakṣatras, Part 2 "
          "(Saptarishis Publications) — chapter header tables, nakṣatras 10-18",
    "S3": "Ram Babu Sao, Perfect Astrology (Nakṣatra) — §3.2-3.3 classification "
          "tables (Tables 7-10, §3.3 Gaṇa), all 27 nakṣatras",
}

# Kept for backward compatibility with the original symbols-only endpoint.
CITATION = ("Symbols & muhūrta-tradition classifications on the `traditional` "
            "tier; see SOURCES for the per-field provenance. NOT BPHS.")

SOURCE_NOTE = (
    "Every value is transcribed from a named source (S1/S2/S3), never guessed. "
    "The S3 layer (gaṇa, yoni, body-part, puruṣārtha, quality, śakti) rests on a "
    "single OCR'd book, so those cells are `single_source` at best. Nāḍī is "
    "absent from both books and left an explicit gap."
)

FIELDS = ("symbol", "gana", "yoni", "body_part", "purushartha", "quality",
          "shakti", "nadi")

# Human labels + a one-line gloss of what each field is, for the UI.
FIELD_META = {
    "symbol":      ("Symbol", "The classical emblem / asterism figure"),
    "gana":        ("Gaṇa", "Temperament class — Deva / Manuṣya / Rākṣasa"),
    "yoni":        ("Yoni (animal)", "Sexual-compatibility animal (Aṣṭakūṭa)"),
    "body_part":   ("Kālapuruṣa aṅga", "Body part in the cosmic-person scheme"),
    "purushartha": ("Puruṣārtha", "Life-aim — Dharma / Artha / Kāma / Mokṣa"),
    "quality":     ("Guṇa / activity", "Muhūrta activity-type of the nakṣatra"),
    "shakti":      ("Śakti", "The nakṣatra's animating power"),
    "nadi":        ("Nāḍī", "Ādi / Madhya / Antya (compatibility)"),
}

# ── Values, 1-indexed (Aśvinī = 1) ───────────────────────────────────────────

# 1-9 keep the established icon strings; 10-18 from Sunil John Part 2; 19-27 are
# Perfect Astrology's asterism star-shapes (a different KIND of symbol — see
# _SYMBOL_KIND — because the classical icon for those is not in either book).
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
    10: "Royal throne / palanquin",
    11: "Front legs of a bed (also: fireplace, hammock, fig tree)",
    12: "Hind legs of a bed; the four legs of a couch",
    13: "Hand or closed fist",
    14: "A bright jewel or pearl",
    15: "A young shoot of a plant; coral",
    16: "A triumphal archway; a potter's wheel",
    17: "A lotus",
    18: "A circular amulet; an umbrella; an earring",
    19: "Five stars like a crouching lion",
    20: "Stars forming a square",
    21: "Stars forming a square",
    22: "Three stars like an arrow",
    23: "Three stars (likened to a head)",
    24: "About a hundred stars, like a flower",
    25: "Stars forming the legs of a cot",
    26: "Stars forming the legs of a cot",
    27: "Three stars like a fish",
}
# 1-18 are iconographic symbols; 19-27 are only star-pattern descriptions.
_SYMBOL_KIND = {i: ("icon" if i <= 18 else "asterism_figure") for i in range(1, 28)}
# Symbols where a second source independently corroborates (S1/S2 + S3 asterism).
_SYMBOL_CORROBORATED = frozenset({1, 2, 5, 9, 10, 13, 14, 16})

_GANA = {
    1: "Deva", 2: "Manuṣya", 3: "Rākṣasa", 4: "Manuṣya", 5: "Deva",
    6: "Manuṣya", 7: "Deva", 8: "Deva", 9: "Rākṣasa", 10: "Rākṣasa",
    11: "Manuṣya", 12: "Manuṣya", 13: "Deva", 14: "Rākṣasa", 15: "Deva",
    16: "Rākṣasa", 17: "Deva", 18: "Rākṣasa", 19: "Rākṣasa", 20: "Manuṣya",
    21: "Manuṣya", 22: "Deva", 23: "Rākṣasa", 24: "Rākṣasa", 25: "Manuṣya",
    26: "Manuṣya", 27: "Deva",
}

# Yoni animals as Perfect Astrology PRINTS them — including the flagged 8/11 swap.
_YONI = {
    1: "Horse", 2: "Elephant", 3: "Goat/sheep", 4: "Serpent", 5: "Serpent",
    6: "Dog", 7: "Cat", 8: "Rat/mouse", 9: "Cat", 10: "Rat/mouse",
    11: "Goat/sheep", 12: "Cow", 13: "Buffalo", 14: "Tiger", 15: "Buffalo",
    16: "Tiger", 17: "Hare/deer", 18: "Hare/deer", 19: "Dog", 20: "Monkey",
    21: "Mongoose", 22: "Monkey", 23: "Lion", 24: "Horse", 25: "Lion",
    26: "Cow", 27: "Elephant",
}

_BODY_PART = {
    1: "Top of the foot", 2: "Sole of the foot", 3: "Head", 4: "Forehead",
    5: "Eyebrows", 6: "Eyes", 7: "Nose", 8: "Face", 9: "Ears",
    10: "Lips / chin", 11: "Right hand", 12: "Left hand", 13: "Fingers",
    14: "Neck", 15: "Chest", 16: "Breasts", 17: "Stomach", 18: "Right torso",
    19: "Left torso", 20: "Back", 21: "Waist", 22: "Genitals", 23: "Anus",
    24: "Right thigh", 25: "Left thigh", 26: "Lower legs", 27: "Ankles",
}

_PURUSHARTHA = {
    1: "Dharma", 2: "Artha", 3: "Kāma", 4: "Mokṣa", 5: "Mokṣa", 6: "Kāma",
    7: "Artha", 8: "Dharma", 9: "Dharma", 10: "Artha", 11: "Kāma", 12: "Mokṣa",
    13: "Mokṣa", 14: "Kāma", 15: "Artha", 16: "Dharma", 17: "Dharma",
    18: "Artha", 19: "Kāma", 20: "Mokṣa", 21: "Mokṣa", 22: "Artha",
    23: "Dharma", 24: "Dharma", 25: "Artha", 26: "Kāma", 27: "Mokṣa",
}

_QUALITY = {
    1: "Light", 2: "Fierce", 3: "Mixed", 4: "Fixed", 5: "Soft", 6: "Sharp",
    7: "Mutable", 8: "Light", 9: "Sharp", 10: "Fierce", 11: "Fierce",
    12: "Fixed", 13: "Light", 14: "Soft", 15: "Mutable", 16: "Mixed",
    17: "Soft", 18: "Sharp", 19: "Sharp", 20: "Fierce", 21: "Fixed",
    22: "Mutable", 23: "Mutable", 24: "Mutable", 25: "Fierce", 26: "Fixed",
    27: "Soft",
}

_SHAKTI = {
    1: "Healing", 2: "Removing", 3: "Burning", 4: "Growing", 5: "Enjoying",
    6: "Achieving", 7: "Revitalising", 8: "Creating energy",
    9: "Destroying energy", 10: "Spiritual rebirth", 11: "Procreating",
    12: "Prospering", 13: "Gaining", 14: "Creating power", 15: "Transforming",
    16: "Harvesting", 17: "Abundance", 18: "Heroism", 19: "Clearing",
    20: "Invigorating", 21: "Victory", 22: "Connecting", 23: "Joining",
    24: "Healing", 25: "Upraising", 26: "Stabilising", 27: "Nourishing",
}

# ── Per-cell notes / confidence exceptions ───────────────────────────────────

_SYMBOL_NOTE = {
    4: "Perfect Astrology's asterism read here ('resembling an ear') is garbled; "
       "the established icon is kept.",
    7: "Perfect Astrology's asterism read here ('potter's wheel') is a mis-carry "
       "it also prints at Viśākhā; the established icon is kept.",
    8: "Perfect Astrology's asterism read here was broken in the scan; the "
       "established icon is kept.",
    17: "Sunil John's header also prints a truncated 'Triumphal Archwa[y]' that "
        "also appears at Viśākhā (a likely row-bleed); only 'lotus' is securely "
        "attested here.",
}
_ASTERISM_NOTE = ("Star-pattern description from Perfect Astrology; the classical "
                  "iconographic symbol for this nakṣatra is not sourced in the "
                  "provided books.")

# Yoni cells whose stored value may itself be wrong (the OCR column-swap).
_YONI_UNCERTAIN = {
    8: "Perfect Astrology prints 'rat' here, but both independent reads suspect "
       "an OCR column-swap with Pūrva Phalgunī; the widely-attested yoni for "
       "Puṣya is goat/sheep.",
    11: "Perfect Astrology prints 'goat' here, but both independent reads suspect "
        "an OCR column-swap with Puṣya; the widely-attested yoni for Pūrva "
        "Phalgunī is rat/mouse.",
}

_GANA_NOTE = ("The source merged the tail of each gaṇa group; both independent "
              "reads resolved identically and to the standard 9-9-9 split.")
_GANA_TAIL = frozenset({6, 17, 19, 22, 23, 24, 25, 26, 27})

# quality/śakti past nakṣatra 11 came from a stretch the single reader flagged.
_GOAL_THIN_NOTE = ("From a single OCR read whose reader flagged reduced "
                   "confidence for nakṣatras 12-27.")

_NADI_REASON = ("Nāḍī (Ādi/Madhya/Antya) is absent from both source books — the "
                "whole nakṣatra section of Perfect Astrology (pp.47-85) was "
                "scanned to confirm it. Left an explicit gap; closing it needs a "
                "muhūrta / Aṣṭakūṭa source (e.g. Muhūrta Cintāmaṇi).")

# Recorded, NOT applied: Sunil John's deity vs the app's BPHS-cited vedic.py.
# RECONCILED 2026-07-21 against the BPHS text (Santhanam Vol I, ch.6
# "24-26. BHAMSA (NAKSHATRAMSA)", pp.78-79) and the primary Vedic authority
# (Taittirīya Brāhmaṇa III.1.1-5): Parāśara genuinely prints Sūrya (Hasta) and
# Marut (Svātī) — same deity-family as the TB's Savitṛ / Vāyu (solar; wind), so
# each is a real textual variant, not an OCR slip. vedic.py keeps the BPHS
# reading; the traditional value stays here, unapplied. See the header comment on
# vedic.NAKSHATRAS.
DEITY_TRADITION_VARIANTS = {
    13: {"nakshatra": "Hasta", "traditional": "Savitṛ", "bphs_app": "Sūrya",
         "source": "S2",
         "bphs_citation": "BPHS ch.6 vv.24-26 (Santhanam Vol I, pp.78-79)",
         "vedic_authority": "Taittirīya Brāhmaṇa III.1.1-5 gives Savitṛ",
         "resolution": "BPHS text confirmed to print Sūrya (same solar family as "
                       "Savitṛ); BPHS-tier value kept, traditional not applied.",
         "note": "Sunil John (and the common Vedic devatā list / Taittirīya "
                 "Brāhmaṇa) give Savitṛ; BPHS ch.6 prints the same-family solar "
                 "deity Sūrya. Genuine Parāśara variant — not overwritten."},
    15: {"nakshatra": "Svātī", "traditional": "Vāyu", "bphs_app": "Marut",
         "source": "S2",
         "bphs_citation": "BPHS ch.6 vv.24-26 (Santhanam Vol I, pp.78-79)",
         "vedic_authority": "Taittirīya Brāhmaṇa III.1.1-5 gives Vāyu",
         "resolution": "BPHS text confirmed to print Marut (same wind family as "
                       "Vāyu); BPHS-tier value kept, traditional not applied.",
         "note": "Sunil John (and the common Vedic devatā list / Taittirīya "
                 "Brāhmaṇa) give Vāyu; BPHS ch.6 prints the related storm/wind "
                 "deity Marut. Genuine Parāśara variant — not overwritten."},
}

# Nakṣatra names, kept local so this module is self-contained and testable.
_NAMES = [
    ("Ashwini", "Aśvinī"), ("Bharani", "Bharaṇī"), ("Krittika", "Kṛttikā"),
    ("Rohini", "Rohiṇī"), ("Mrigashira", "Mṛgaśira"), ("Ardra", "Ārdrā"),
    ("Punarvasu", "Punarvasu"), ("Pushya", "Puṣya"), ("Ashlesha", "Āśleṣā"),
    ("Magha", "Maghā"), ("Purva Phalguni", "Pūrva Phalgunī"),
    ("Uttara Phalguni", "Uttara Phalgunī"), ("Hasta", "Hasta"),
    ("Chitra", "Citrā"), ("Swati", "Svātī"), ("Vishakha", "Viśākhā"),
    ("Anuradha", "Anurādhā"), ("Jyeshtha", "Jyeṣṭhā"), ("Mula", "Mūla"),
    ("Purva Ashadha", "Pūrva Āṣāḍhā"), ("Uttara Ashadha", "Uttara Āṣāḍhā"),
    ("Shravana", "Śravaṇa"), ("Dhanishta", "Dhaniṣṭhā"),
    ("Shatabhisha", "Śatabhiṣā"), ("Purva Bhadrapada", "Pūrva Bhādrapadā"),
    ("Uttara Bhadrapada", "Uttara Bhādrapadā"), ("Revati", "Revatī"),
]


def _cell(value, confidence, sources, note=None, kind=None):
    """One attribute cell, carrying its own provenance so nothing is asserted."""
    out = {
        "value": value,
        "available": value is not None,
        "tier": TIER,
        "confidence": confidence,          # corroborated|single_source|uncertain|absent
        "sources": [SOURCES[s] for s in sources],
        "source_ids": list(sources),
    }
    if note:
        out["note"] = note
    if kind:
        out["kind"] = kind
    return out


def _symbol_cell(i: int) -> dict:
    if 1 <= i <= 9:
        primary = "S1"
    elif 10 <= i <= 18:
        primary = "S2"
    else:
        primary = "S3"
    sources = [primary]
    if i in _SYMBOL_CORROBORATED and primary != "S3":
        sources = [primary, "S3"]            # the S3 asterism list corroborates
        confidence = "corroborated"
    else:
        confidence = "single_source"
    note = _SYMBOL_NOTE.get(i)
    if _SYMBOL_KIND[i] == "asterism_figure":
        note = _ASTERISM_NOTE
    return _cell(_SYMBOL[i], confidence, sources, note, kind=_SYMBOL_KIND[i])


def _gana_cell(i: int) -> dict:
    note = _GANA_NOTE if i in _GANA_TAIL else None
    return _cell(_GANA[i], "single_source", ["S3"], note)


def _yoni_cell(i: int) -> dict:
    if i in _YONI_UNCERTAIN:
        return _cell(_YONI[i], "uncertain", ["S3"], _YONI_UNCERTAIN[i])
    return _cell(_YONI[i], "single_source", ["S3"])


def _goal_cell(table, i: int) -> dict:
    """quality / śakti: single-read, reader flagged 12-27 as thinner."""
    note = _GOAL_THIN_NOTE if i >= 12 else None
    return _cell(table[i], "single_source", ["S3"], note)


def _nadi_cell(i: int) -> dict:
    return _cell(None, "absent", [], _NADI_REASON)


def attributes_of(index: int) -> dict:
    """Every `traditional`-tier attribute of one nakṣatra (1-27), with provenance.

    `index` is 1-based, Aśvinī = 1. Each cell carries its value, tier, confidence
    and source citations; absent cells (nāḍī) say so explicitly rather than being
    filled. The BPHS deity/lord live in vedic.py and are not duplicated here.
    """
    if not 1 <= index <= 27:
        raise ValueError(f"nakṣatra index out of range: {index}")
    name, name_iast = _NAMES[index - 1]
    cells = {
        "symbol":      _symbol_cell(index),
        "gana":        _gana_cell(index),
        "yoni":        _yoni_cell(index),
        "body_part":   _cell(_BODY_PART[index], "single_source", ["S3"]),
        "purushartha": _cell(_PURUSHARTHA[index], "single_source", ["S3"]),
        "quality":     _goal_cell(_QUALITY, index),
        "shakti":      _goal_cell(_SHAKTI, index),
        "nadi":        _nadi_cell(index),
    }
    out = {"index": index, "name": name, "name_iast": name_iast, "cells": cells}
    if index in DEITY_TRADITION_VARIANTS:
        out["deity_variant"] = DEITY_TRADITION_VARIANTS[index]
    return out


def all_attributes() -> list[dict]:
    """The full 27-row `traditional`-tier attribute table, with provenance."""
    return [attributes_of(i) for i in range(1, 28)]


# ── Backward-compatible symbols-only surface (unchanged callers keep working) ─

def symbol_of(index: int) -> dict:
    """The classical symbol for a nakṣatra (1-27), with tier and provenance.

    Now sourced for all 27 (was 1-9 only): 1-18 are iconographic symbols; 19-27
    are asterism star-shapes from Perfect Astrology, tagged `kind` accordingly
    and noted as such — the classical icon for 19-27 remains unsourced.
    """
    if not 1 <= index <= 27:
        raise ValueError(f"nakṣatra index out of range: {index}")
    c = _symbol_cell(index)
    return {"attribute": "symbol", "citation": CITATION, **c}


def all_symbols() -> list[dict]:
    """Symbol status for every nakṣatra 1-27."""
    return [{"index": i, **symbol_of(i)} for i in range(1, 28)]
