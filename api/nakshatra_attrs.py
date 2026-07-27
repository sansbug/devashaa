"""Nakṣatra attributes on the `traditional` tier — NOT BPHS, NOT invented.

WHAT THIS IS, AND THE TIER IT SITS ON
-------------------------------------
The app already computes, for all 27 nakṣatras and from BPHS:
    - the nakṣatra name and its deity   (BPHS ch.6, vedic.NAKSHATRAS)
    - the Viṁśottarī lord               (BPHS ch.46, derived)
    - the pāda→rāśi / navāṁśa spans     (arithmetic)

The classical SYMBOL of a nakṣatra (Aśvinī = a horse's head, Bharaṇī = the yoni,
…) and the muhūrta-tradition classifications (gaṇa, guṇa, yoni/animal, kālapuruṣa
body-part, puruṣārtha, quality, śakti, dosha, nāḍī) are NOT in BPHS — the rāśi
cards correctly mark this whole layer "BPHS is silent (ch.3 v.7)". They belong to
the older Bṛhat-Saṁhitā / muhūrta tradition, so they ship here on a `traditional`
footing, beside the BPHS deity and never as Parāśara.

WHERE EACH CELL COMES FROM, AND HOW SURE WE ARE
-----------------------------------------------
Every value here was transcribed from a named source, never filled from memory:

    S1  the established classical symbol set (nakṣatras 1-9, previously shipped)
    S2  Sunil John & V. Pandya, *Predicting Through Nakṣatras, Part 2*
        (Saptarishis) — chapter header tables, nakṣatras 10-18
    S3  Ram Babu Sao, *Perfect Astrology (Nakṣatra)* — §3.2-3.3 classification
        tables, all 27 (gaṇa, yoni/animal, body-part, puruṣārtha, quality, śakti,
        and asterism star-shapes for the symbols S1/S2 do not reach, 19-27)
    S4  Komilla Sutton, *Vedic Astrology* (Jyotish 2000) — the per-nakṣatra
        data-boxes: symbol, animal(yoni), deity, motivation(puruṣārtha), guṇa
        triplicity, Ayurvedic dosha (added 2026-07-26)

Each cell carries a `confidence`:
    corroborated  — two independent sources agree
    single_source — one book states it
    uncertain     — the stored value may itself be wrong; see the note
    absent        — no source states it; a first-class gap, never guessed

WHAT S4 (KOMILLA SUTTON) CHANGED, 2026-07-26
--------------------------------------------
A fourth book (an independent modern compiler of the traditional attributes)
reconciled the earlier grid and closed its biggest gap. Only her FACTUAL
data-box fields were taken; her personality prose, "famous <nakṣatra>" lists and
self-devised compatibility grids are her own modern interpretation and are NOT
reproduced.

  • NĀḌĪ — WAS ABSENT FOR ALL 27, NOW FILLED. S4's "Ayurvedic dosha" column
    (Vāta/Pitta/Kapha) maps by the standard identity Ādi=Vāta / Madhya=Pitta /
    Antya=Kapha, and it reproduces the canonical Aṣṭakūṭa nāḍī assignment EXACTLY
    for all 27 (a perfect 9-9-9 in the canonical positions). That independent
    agreement — a centuries-old muhūrta standard + Komilla's printed dosha — is
    what finally closes the gap the two earlier books left open. `dosha` ships as
    its own field beside `nadi`.
  • YONI SWAP RESOLVED. S3 printed Puṣya = *rat* and Pūrva-Phalgunī = *goat*
    (a column-swap, flagged `uncertain`). S4 independently gives Puṣya = sheep,
    Pūrva-Phalgunī = rat — the canonical pairing. Both cells are now the canonical
    value, `corroborated`, with the resolution recorded.
  • CORROBORATION. S4's animal(yoni) matches S3 for every other nakṣatra, and her
    motivation(puruṣārtha) matches S3 for all 27 — so yoni and puruṣārtha move
    from `single_source` to `corroborated`. Her symbol corroborates the icon for
    1-18 and PROVIDES the iconographic symbol for 19-27 (which the grid had only
    as star-shapes).
  • GUṆA (dominant sattva/rajas/tamas) added from S4 — a clean 9-9-9 (1-9 Rajas,
    10-18 Tamas, 19-27 Sattva). Distinct from the muhūrta `quality`/activity field.
  • DEITY VARIANCES reinforced. S4 independently gives Hasta = Savitṛ and
    Svātī = Vāyu — a THIRD witness for the two variances already flagged against
    BPHS's Sūrya / Marut. vedic.py is still not touched; see DEITY_TRADITION_VARIANTS.

The gaṇa, kālapuruṣa body-part, quality(activity) and śakti fields are not in
Komilla's boxes, so they remain `single_source` (S3).
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
    "S4": "Komilla Sutton, Vedic Astrology (Jyotish 2000) — per-nakṣatra "
          "data-boxes: symbol, animal (yoni), deity, motivation (puruṣārtha), "
          "guṇa triplicity, Ayurvedic dosha. Facts only; her interpretive prose "
          "and compatibility grids are not reproduced.",
}

# Kept for backward compatibility with the original symbols-only endpoint.
CITATION = ("Symbols & muhūrta-tradition classifications on the `traditional` "
            "tier; see SOURCES for the per-field provenance. NOT BPHS.")

SOURCE_NOTE = (
    "Every value is transcribed from a named source (S1-S4), never guessed. "
    "Komilla Sutton (S4) added a second independent witness: yoni and puruṣārtha "
    "are now corroborated, and her Ayurvedic-dosha column — which reproduces the "
    "canonical Aṣṭakūṭa nāḍī 9-9-9 exactly — finally fills the nāḍī gap the two "
    "earlier books left open. Gaṇa, body-part, activity and śakti rest on the one "
    "S3 book still (single_source)."
)

FIELDS = ("symbol", "gana", "guna", "yoni", "body_part", "purushartha",
          "quality", "shakti", "dosha", "nadi")

# Human labels + a one-line gloss of what each field is, for the UI.
FIELD_META = {
    "symbol":      ("Symbol", "The classical emblem / asterism figure"),
    "gana":        ("Gaṇa", "Temperament class — Deva / Manuṣya / Rākṣasa"),
    "guna":        ("Guṇa", "Dominant strand — Sattva / Rajas / Tamas"),
    "yoni":        ("Yoni (animal)", "Sexual-compatibility animal (Aṣṭakūṭa)"),
    "body_part":   ("Kālapuruṣa aṅga", "Body part in the cosmic-person scheme"),
    "purushartha": ("Puruṣārtha", "Life-aim — Dharma / Artha / Kāma / Mokṣa"),
    "quality":     ("Activity (muhūrta)", "Muhūrta activity-class — Light/Fierce/Fixed/…"),
    "shakti":      ("Śakti", "The nakṣatra's animating power"),
    "dosha":       ("Dosha", "Āyurvedic humour — Vāta / Pitta / Kapha"),
    "nadi":        ("Nāḍī", "Ādi / Madhya / Antya (Aṣṭakūṭa compatibility)"),
}

# ── Values, 1-indexed (Aśvinī = 1) ───────────────────────────────────────────

# 1-18 keep the established iconographic symbols (S1/S2, corroborated by S3/S4);
# 19-27 are now the iconographic symbols Komilla Sutton (S4) supplies — the grid
# previously had only Perfect Astrology's asterism star-shapes for those, which
# are kept in _SYMBOL_ASTERISM_S3 for the note.
_SYMBOL = {
    1: "Horse's head",
    2: "Yoni (the vulva / womb)",
    3: "Knife or razor / a flame",
    4: "Cart or chariot",
    5: "Deer's or antelope's head",
    6: "A teardrop, a gem, or a human head",
    7: "A bow and quiver of arrows",
    8: "A cow's udder, a lotus, or an arrow",
    9: "A coiled serpent",
    10: "Royal throne / palanquin",
    11: "Front legs of a bed (also: fireplace, hammock, fig tree)",
    12: "Hind legs of a bed; the four legs of a couch",
    13: "Hand or palm; a closed fist",
    14: "A bright jewel or pearl",
    15: "A young shoot of a plant; coral",
    16: "A triumphal archway; a potter's wheel",
    17: "A lotus",
    18: "A circular amulet; an umbrella; an earring",
    19: "A tail of a lion, or an elephant goad",
    20: "An elephant's tusk (also: a fan / winnowing basket)",
    21: "The planks of a bed",
    22: "An ear (also: three footprints)",
    23: "A flute or a drum",
    24: "A hundred stars; an empty circle",
    25: "A sword (also: the front legs of a funeral cot)",
    26: "Twins (also: the back legs of a funeral cot)",
    27: "A fish (also: a drum)",
}
# Perfect Astrology's (S3) star-shape reads for 19-27 — kept for the note now that
# 19-27 carry Komilla's iconographic symbol instead.
_SYMBOL_ASTERISM_S3 = {
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
# Every symbol is now iconographic (19-27 gained an icon from S4).
_SYMBOL_KIND = {i: "icon" for i in range(1, 28)}
# 1-18: S3's asterism list independently corroborates the icon for these.
_SYMBOL_S3_CORROB = frozenset({1, 2, 5, 9, 10, 13, 14, 16})
# 1-18: Komilla (S4) corroborates the iconographic symbol (matches, or matches a
# listed alternate — e.g. her "Fireplace" = an alternate for Pūrva-Phalgunī).
_SYMBOL_S4_CORROB = frozenset(range(1, 19))

_GANA = {
    1: "Deva", 2: "Manuṣya", 3: "Rākṣasa", 4: "Manuṣya", 5: "Deva",
    6: "Manuṣya", 7: "Deva", 8: "Deva", 9: "Rākṣasa", 10: "Rākṣasa",
    11: "Manuṣya", 12: "Manuṣya", 13: "Deva", 14: "Rākṣasa", 15: "Deva",
    16: "Rākṣasa", 17: "Deva", 18: "Rākṣasa", 19: "Rākṣasa", 20: "Manuṣya",
    21: "Manuṣya", 22: "Deva", 23: "Rākṣasa", 24: "Rākṣasa", 25: "Manuṣya",
    26: "Manuṣya", 27: "Deva",
}

# Dominant guṇa (first of Komilla's three-level triplicity, S4). Classical
# three-cycles-of-nine: 1-9 Rajas, 10-18 Tamas, 19-27 Sattva.
_GUNA = {**{i: "Rajas" for i in range(1, 10)},
         **{i: "Tamas" for i in range(10, 19)},
         **{i: "Sattva" for i in range(19, 28)}}

# Yoni animals. The Puṣya(8)/Pūrva-Phalgunī(11) swap S3 printed is now RESOLVED to
# the canonical pairing, confirmed by Komilla (S4). Male/female gender that S4
# sometimes specifies is the same yoni and is not separately stored.
_YONI = {
    1: "Horse", 2: "Elephant", 3: "Goat/sheep", 4: "Serpent", 5: "Serpent",
    6: "Dog", 7: "Cat", 8: "Goat/sheep", 9: "Cat", 10: "Rat/mouse",
    11: "Rat/mouse", 12: "Cow", 13: "Buffalo", 14: "Tiger", 15: "Buffalo",
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

# Ayurvedic dosha (S4, Komilla). Maps to nāḍī by the standard identity below.
_DOSHA = {
    1: "Vāta", 2: "Pitta", 3: "Kapha", 4: "Kapha", 5: "Pitta", 6: "Vāta",
    7: "Vāta", 8: "Pitta", 9: "Kapha", 10: "Kapha", 11: "Pitta", 12: "Vāta",
    13: "Vāta", 14: "Pitta", 15: "Kapha", 16: "Kapha", 17: "Pitta", 18: "Vāta",
    19: "Vāta", 20: "Pitta", 21: "Kapha", 22: "Kapha", 23: "Pitta", 24: "Vāta",
    25: "Vāta", 26: "Pitta", 27: "Kapha",
}
# The standard dosha↔nāḍī identity used in the muhūrta / Aṣṭakūṭa tradition.
_DOSHA_TO_NADI = {"Vāta": "Ādi", "Pitta": "Madhya", "Kapha": "Antya"}
_NADI = {i: _DOSHA_TO_NADI[_DOSHA[i]] for i in range(1, 28)}

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

# Yoni cells whose printed value was the OCR column-swap — now RESOLVED by S4.
_YONI_RESOLVED = {
    8: "Perfect Astrology printed 'rat' here and 'goat' at Pūrva Phalgunī — a "
       "column-swap. Komilla Sutton (S4) independently gives Puṣya = sheep, the "
       "canonical pairing, so the corrected value is shown and corroborated.",
    11: "Perfect Astrology printed 'goat' here and 'rat' at Puṣya — a column-swap. "
        "Komilla Sutton (S4) independently gives Pūrva Phalgunī = rat, the "
        "canonical pairing, so the corrected value is shown and corroborated.",
}

_GANA_NOTE = ("The source merged the tail of each gaṇa group; both independent "
              "reads resolved identically and to the standard 9-9-9 split.")
_GANA_TAIL = frozenset({6, 17, 19, 22, 23, 24, 25, 26, 27})

# quality/śakti past nakṣatra 11 came from a stretch the single reader flagged.
_GOAL_THIN_NOTE = ("From a single OCR read whose reader flagged reduced "
                   "confidence for nakṣatras 12-27.")

_GUNA_NOTE = ("Dominant guṇa — the first of Komilla Sutton's (S4) three-level "
              "triplicity. Follows the classical three-cycles-of-nine: 1-9 Rajas, "
              "10-18 Tamas, 19-27 Sattva. Distinct from the muhūrta activity above.")

_DOSHA_NOTE = ("Ayurvedic humour, from Komilla Sutton's (S4) data-box. All 27 map "
               "cleanly to the canonical Aṣṭakūṭa nāḍī (Vāta=Ādi, Pitta=Madhya, "
               "Kapha=Antya) — see the nāḍī cell.")

_NADI_NOTE = ("Filled at last (was an explicit gap for all 27). Derived from "
              "Komilla Sutton's Ayurvedic-dosha column (S4) by the standard "
              "Ādi=Vāta / Madhya=Pitta / Antya=Kapha identity — and it reproduces "
              "the canonical Aṣṭakūṭa nāḍī assignment EXACTLY for all 27 (a perfect "
              "9-9-9 in the canonical positions). That independent agreement — a "
              "centuries-old muhūrta standard and Komilla's printed dosha — is the "
              "corroboration that closes the gap the earlier two books left open.")

_ICON_FROM_S4_NOTE = ("Iconographic symbol from Komilla Sutton (S4). Perfect "
                      "Astrology (S3) gave only the star-pattern here: ")

# Recorded, NOT applied: the traditional deity vs the app's BPHS-cited vedic.py.
# RECONCILED 2026-07-21 against the BPHS text (Santhanam Vol I, ch.6
# "24-26. BHAMSA (NAKSHATRAMSA)", pp.78-79) and the primary Vedic authority
# (Taittirīya Brāhmaṇa III.1.1-5): Parāśara genuinely prints Sūrya (Hasta) and
# Marut (Svātī) — same deity-family as the TB's Savitṛ / Vāyu (solar; wind), so
# each is a real textual variant, not an OCR slip. vedic.py keeps the BPHS
# reading; the traditional value stays here, unapplied. Komilla Sutton (S4)
# independently gives the same traditional deities, so each variance now rests on
# two witnesses (S2 + S4), which the note records.
DEITY_TRADITION_VARIANTS = {
    13: {"nakshatra": "Hasta", "traditional": "Savitṛ", "bphs_app": "Sūrya",
         "source": "S2", "also": "S4",
         "bphs_citation": "BPHS ch.6 vv.24-26 (Santhanam Vol I, pp.78-79)",
         "vedic_authority": "Taittirīya Brāhmaṇa III.1.1-5 gives Savitṛ",
         "resolution": "BPHS text confirmed to print Sūrya (same solar family as "
                       "Savitṛ); BPHS-tier value kept, traditional not applied.",
         "note": "Sunil John (S2) and Komilla Sutton (S4) — and the common Vedic "
                 "devatā list / Taittirīya Brāhmaṇa — give Savitṛ; BPHS ch.6 "
                 "prints the same-family solar deity Sūrya. Genuine Parāśara "
                 "variant, now on two traditional witnesses — not overwritten."},
    15: {"nakshatra": "Svātī", "traditional": "Vāyu", "bphs_app": "Marut",
         "source": "S2", "also": "S4",
         "bphs_citation": "BPHS ch.6 vv.24-26 (Santhanam Vol I, pp.78-79)",
         "vedic_authority": "Taittirīya Brāhmaṇa III.1.1-5 gives Vāyu",
         "resolution": "BPHS text confirmed to print Marut (same wind family as "
                       "Vāyu); BPHS-tier value kept, traditional not applied.",
         "note": "Sunil John (S2) and Komilla Sutton (S4) — and the common Vedic "
                 "devatā list / Taittirīya Brāhmaṇa — give Vāyu; BPHS ch.6 prints "
                 "the related storm/wind deity Marut. Genuine Parāśara variant, "
                 "now on two traditional witnesses — not overwritten."},
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
    # 19-27: the iconographic symbol now comes from Komilla (S4); Perfect
    # Astrology only had the star-shape, which is preserved in the note.
    if i >= 19:
        note = _ICON_FROM_S4_NOTE + f"'{_SYMBOL_ASTERISM_S3[i]}'."
        return _cell(_SYMBOL[i], "single_source", ["S4"], note, kind="icon")
    # 1-18: the established icon, corroborated by S3's asterism (some) and S4.
    primary = "S1" if i <= 9 else "S2"
    sources = [primary]
    if i in _SYMBOL_S3_CORROB:
        sources.append("S3")
    if i in _SYMBOL_S4_CORROB:
        sources.append("S4")
    confidence = "corroborated" if len(sources) >= 2 else "single_source"
    return _cell(_SYMBOL[i], confidence, sources, _SYMBOL_NOTE.get(i), kind="icon")


def _gana_cell(i: int) -> dict:
    note = _GANA_NOTE if i in _GANA_TAIL else None
    return _cell(_GANA[i], "single_source", ["S3"], note)


def _guna_cell(i: int) -> dict:
    return _cell(_GUNA[i], "single_source", ["S4"], _GUNA_NOTE)


def _yoni_cell(i: int) -> dict:
    # S3 + S4 agree everywhere; the 8/11 swap is resolved to the canonical value.
    note = _YONI_RESOLVED.get(i)
    return _cell(_YONI[i], "corroborated", ["S3", "S4"], note)


def _purushartha_cell(i: int) -> dict:
    # Komilla (S4) matches S3 for all 27 — corroborated.
    return _cell(_PURUSHARTHA[i], "corroborated", ["S3", "S4"])


def _goal_cell(table, i: int) -> dict:
    """quality / śakti: single-read (S3), reader flagged 12-27 as thinner."""
    note = _GOAL_THIN_NOTE if i >= 12 else None
    return _cell(table[i], "single_source", ["S3"], note)


def _dosha_cell(i: int) -> dict:
    return _cell(_DOSHA[i], "single_source", ["S4"], _DOSHA_NOTE)


def _nadi_cell(i: int) -> dict:
    # Corroborated: Komilla's dosha column (S4) + its exact match to the canonical
    # Aṣṭakūṭa assignment (an independent muhūrta standard). See _NADI_NOTE.
    return _cell(_NADI[i], "corroborated", ["S4"], _NADI_NOTE)


def attributes_of(index: int) -> dict:
    """Every `traditional`-tier attribute of one nakṣatra (1-27), with provenance.

    `index` is 1-based, Aśvinī = 1. Each cell carries its value, tier, confidence
    and source citations. The BPHS deity/lord live in vedic.py and are not
    duplicated here.
    """
    if not 1 <= index <= 27:
        raise ValueError(f"nakṣatra index out of range: {index}")
    name, name_iast = _NAMES[index - 1]
    cells = {
        "symbol":      _symbol_cell(index),
        "gana":        _gana_cell(index),
        "guna":        _guna_cell(index),
        "yoni":        _yoni_cell(index),
        "body_part":   _cell(_BODY_PART[index], "single_source", ["S3"]),
        "purushartha": _purushartha_cell(index),
        "quality":     _goal_cell(_QUALITY, index),
        "shakti":      _goal_cell(_SHAKTI, index),
        "dosha":       _dosha_cell(index),
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

    Sourced for all 27 and iconographic throughout: 1-18 from the established set
    (corroborated by S3/S4); 19-27 from Komilla Sutton (S4), which supplied the
    iconographic symbol the earlier books lacked (they had only star-shapes).
    """
    if not 1 <= index <= 27:
        raise ValueError(f"nakṣatra index out of range: {index}")
    c = _symbol_cell(index)
    return {"attribute": "symbol", "citation": CITATION, **c}


def all_symbols() -> list[dict]:
    """Symbol status for every nakṣatra 1-27."""
    return [{"index": i, **symbol_of(i)} for i in range(1, 28)]
