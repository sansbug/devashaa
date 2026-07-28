"""Navāṁśa (D9) analysis — tier `modern`, source C. S. Patel, *Navamsa in Astrology*.

WHAT THIS IS, AND THE TIER IT SITS ON
-------------------------------------
The navāṁśa itself is BPHS ch.6 v.12 (see vargas.d9_navamsa). BPHS assigns the
division a name and a method and stops there — it states no vargottama, no
pushkara, no 64th-navāṁśa, no bhāva-sūchaka reading. The rāśi cards already say
as much. Those *readings* of the D9 are the older classical + Nāḍī tradition,
synthesised for a modern reader by C. S. Patel (*Navamsa in Astrology*, Sagar
Publications, 1997). So they ship here on a `modern` footing, attributed to Patel
and his cited chapter, and are never presented as Parāśara.

WHAT IS COMPUTED (and what is NOT)
----------------------------------
Everything here is a STRUCTURAL fact computed from the D1 longitudes the chart
already carries — "Jupiter is vargottama", "the 64th navāṁśa from the Moon is
Makara" — each certain. The *meaning* attached to that fact is Patel's `modern`
claim, kept as a short attributed gloss beside the structural value, never fused
into it. In particular the 64th-navāṁśa point is reported as the sensitive point
Patel names; his death-mode combinations (Ch.V) are NOT evaluated into a verdict —
this site does not predict death.

Signals (all attributed to a Patel chapter):
    vargottama     Ch.III  — same sign in D1 and D9; kind (uccha/nīca/sva/…)
    pushkara       Ch.IV   — the two auspicious navāṁśas of each sign
    khara (64th)   Ch.V    — the 64th navāṁśa (in the 8th rāśi) and its lord
    bhava_suchaka  Ch.VI   — each navāṁśa-sign named by its rāśi-chart house
"""

from __future__ import annotations

from vargas import (d9_navamsa, _split, FIERY, EARTHY, AIRY, WATERY)

TIER = "modern"
SOURCE = "C. S. Patel, Navamsa in Astrology (Sagar Publications, 1997)"
NOTE = ("Computed from the D9 navāṁśa (BPHS ch.6 v.12). The readings — vargottama, "
        "pushkara, the 64th navāṁśa, the bhāva-sūchaka nomenclature — are C. S. "
        "Patel's modern synthesis of classical and Nāḍī sources, NOT BPHS, and are "
        "kept on their own tier beside the śloka layer, never blended into it.")

# The seven planets + the two nodes + the lagna are all navāṁśa points.
_GRAHAS = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn",
           "rahu", "ketu")

# Rāśi lords (0 = Aries … 11 = Pisces) — for the 64th-navāṁśa lord.
SIGN_LORD = ["mars", "venus", "mercury", "moon", "sun", "mercury",
             "venus", "mars", "jupiter", "saturn", "saturn", "jupiter"]

# Exaltation / debilitation / own signs, for classifying a vargottama (Ch.III).
_EXALT = {"sun": 0, "moon": 1, "mars": 9, "mercury": 5, "jupiter": 3,
          "venus": 11, "saturn": 6}
_DEBIL = {"sun": 6, "moon": 7, "mars": 3, "mercury": 11, "jupiter": 9,
          "venus": 5, "saturn": 0}
_OWN = {"sun": {4}, "moon": {3}, "mars": {0, 7}, "mercury": {2, 5},
        "jupiter": {8, 11}, "venus": {1, 6}, "saturn": {9, 10}}

# Śubha- vs Pāpa-Vargottama lagna, by sign (Patel Ch.III, 1-indexed 2/3/4/6/7/9/12
# vs 1/5/8/10/11 → 0-indexed here).
_SUBHA_SIGNS = {1, 2, 3, 5, 6, 8, 11}
_PAPA_SIGNS = {0, 4, 7, 9, 10}

# Vargottama results per planet (Ch.III, p.28) — short attributed glosses.
_VARGOTTAMA_RESULT = {
    "sun": "firmness of mind, status, a desire for knowledge",
    "moon": "intellect, good memory, an impartial mind",
    "mars": "drive and the reasons behind rise and fall",
    "mercury": "sharp intellect and persuasiveness",
    "jupiter": "intelligence, a sound physique, a searching mind",
    "venus": "balanced judgement and physical development",
    "saturn": "longevity and self-restraint",
    "rahu": "amplified results of its placement",
    "ketu": "amplified results of its placement",
}

# The two Pushkara navāṁśas of each sign, by element group, as navāṁśa index 1-9
# within the sign (Patel Ch.IV, from Vidyā-mādhavīyam).
_PUSHKARA_NAV = {
    "fiery": {7, 9},    # Meṣa, Siṁha, Dhanus  → 7th (Tulā) & 9th (Dhanus)
    "earthy": {3, 5},   # Vṛṣabha, Kanyā, Makara → 3rd (Mīna) & 5th (Vṛṣabha)
    "airy": {6, 8},     # Mithuna, Tulā, Kumbha → 6th (Mīna) & 8th (Vṛṣabha)
    "watery": {1, 3},   # Kaṭaka, Vṛścika, Mīna → 1st (Kaṭaka) & 3rd (Kanyā)
}
# Pushkara-bhāga: the single auspicious degree in each sign (cycle 21/14/24/7).
_PUSHKARA_BHAGA = [21, 14, 24, 7, 21, 14, 24, 7, 21, 14, 24, 7]

# Bhāva-sūchaka nomenclature by house of the navāṁśa-sign in the rāśi chart (Ch.VI).
_BHAVA_SUCHAKA = {
    1:  ("Lagnāṁśa", "self, body", True),
    2:  ("Vittāṁśa", "wealth, family", None),
    3:  ("Vikramāṁśa", "valour, effort", None),
    4:  ("Sukhāṁśa", "happiness, home", True),
    5:  ("Putrāṁśa", "progeny, intellect", True),
    6:  ("Ṣaṣṭhāṁśa", "enemies, disease, debt", False),
    7:  ("Bhāryāṁśa", "spouse, partnership", None),
    8:  ("Nidhanāṁśa", "obstacles, longevity", False),
    9:  ("Bhāgyāṁśa", "fortune, dharma", True),
    10: ("Karmāṁśa", "career, action", True),
    11: ("Lābhāṁśa", "gains", True),
    12: ("Vyayāṁśa", "loss, expense", False),
}
_PROSPEROUS = {1, 4, 5, 9, 10, 11}
_DIFFICULT = {6, 8, 12}

# ── primitives ───────────────────────────────────────────────────────────────

def navamsa_sign(lon: float) -> int:
    """The D9 sign (0-11) of a sidereal longitude — BPHS ch.6 v.12."""
    sign, deg = _split(lon)
    return d9_navamsa(sign, deg)


def navamsa_index(lon: float) -> int:
    """Which of the nine navāṁśas (1-9) within the sign the longitude falls in."""
    _, deg = _split(lon)
    return int(deg // (30.0 / 9.0)) + 1


def _element(sign: int) -> str:
    if sign in FIERY:
        return "fiery"
    if sign in EARTHY:
        return "earthy"
    if sign in AIRY:
        return "airy"
    return "watery"


def is_vargottama(lon: float) -> bool:
    """Same sign in D1 and D9 (Patel Ch.III)."""
    sign, _ = _split(lon)
    return sign == navamsa_sign(lon)


def vargottama_kind(graha: str, sign: int) -> str:
    """Classify a vargottama: uccha / nīca / svakṣetra / ordinary (planets);
    śubha / pāpa (the lagna)."""
    if graha == "lagna":
        return "subha" if sign in _SUBHA_SIGNS else "papa"
    if _EXALT.get(graha) == sign:
        return "uccha"
    if _DEBIL.get(graha) == sign:
        return "neecha"
    if sign in _OWN.get(graha, set()):
        return "swakshetra"
    return "ordinary"


def is_pushkara_navamsa(lon: float) -> bool:
    """In one of the sign's two auspicious navāṁśas (Patel Ch.IV)."""
    sign, _ = _split(lon)
    return navamsa_index(lon) in _PUSHKARA_NAV[_element(sign)]


def khara_64th(lon: float) -> dict:
    """The 64th navāṁśa (Khara) from a point — Patel Ch.V.

    63 navāṁśas = exactly 210°, so the 64th navāṁśa is the navāṁśa of
    (lon + 210°): it always falls in the 8th rāśi from the point, at the same
    degree-in-sign. Verified against Patel's Indira-Gandhi worked chart
    (asc Karka 27°03' → Mithuna navāṁśa in Kumbha, the 8th sign).
    """
    target = (lon + 210.0) % 360.0
    rasi_8th = int(target // 30)
    nsign = navamsa_sign(target)
    return {"rasi_8th": rasi_8th, "navamsa_sign": nsign, "lord": SIGN_LORD[nsign]}


# ── assembly ─────────────────────────────────────────────────────────────────

def navamsa_analysis(graha_positions: dict, lagna_longitude: float,
                     lagna_sign: int) -> dict:
    """The whole-chart navāṁśa (D9) analysis.

    `graha_positions` maps graha key -> {"longitude": float, "rasi": int}.
    Returns four attributed signal groups; each item names the point, its
    computed structural value, and (where the source gives one) a short gloss.
    """
    # All navāṁśa points: the lagna first, then the nine grahas.
    points = [("lagna", lagna_longitude, lagna_sign)]
    for g in _GRAHAS:
        p = graha_positions.get(g)
        if p is not None:
            points.append((g, p["longitude"], p["rasi"]))

    # 1. Vargottama --------------------------------------------------------------
    vargottama = []
    for key, lon, sign in points:
        if is_vargottama(lon):
            kind = vargottama_kind(key, sign)
            vargottama.append({
                "key": key, "sign": sign, "navamsa_sign": sign, "kind": kind,
                "result": (_VARGOTTAMA_RESULT.get(key) if key != "lagna" else None),
            })

    # 2. Pushkara navāṁśa --------------------------------------------------------
    pushkara = []
    for key, lon, sign in points:
        if is_pushkara_navamsa(lon):
            pushkara.append({
                "key": key, "sign": sign, "navamsa_sign": navamsa_sign(lon),
                "navamsa_index": navamsa_index(lon),
                "bhaga_degree": _PUSHKARA_BHAGA[sign],
            })

    # 3. The 64th navāṁśa (Khara) — for the three luminary-karaka points ---------
    #    lagna → self, Moon → mother, Sun → father (Patel applies it via kārakas).
    khara_targets = [("lagna", lagna_longitude, "the native / body"),
                     ("moon", None, "the mother"),
                     ("sun", None, "the father")]
    khara = []
    for key, lon, karaka in khara_targets:
        if lon is None:
            p = graha_positions.get(key)
            if p is None:
                continue
            lon = p["longitude"]
        k = khara_64th(lon)
        lord = k["lord"]
        lord_pos = graha_positions.get(lord)
        lord_house = (((lord_pos["rasi"] - lagna_sign) % 12) + 1
                      if lord_pos else None)
        khara.append({
            "key": key, "karaka": karaka,
            "navamsa_sign": k["navamsa_sign"], "rasi_8th": k["rasi_8th"],
            "lord": lord, "lord_house": lord_house,
            "lord_in_dusthana": lord_house in (6, 8, 12) if lord_house else None,
        })

    # 4. Bhāva-sūchaka navāṁśa ---------------------------------------------------
    bhava_items = []
    tally = {"prosperous": 0, "difficult": 0, "neutral": 0}
    for key, lon, sign in points:
        nsign = navamsa_sign(lon)
        house = ((nsign - lagna_sign) % 12) + 1
        label, meaning, favourable = _BHAVA_SUCHAKA[house]
        bhava_items.append({
            "key": key, "navamsa_sign": nsign, "house": house,
            "label": label, "meaning": meaning, "favourable": favourable,
        })
        if house in _PROSPEROUS:
            tally["prosperous"] += 1
        elif house in _DIFFICULT:
            tally["difficult"] += 1
        else:
            tally["neutral"] += 1

    return {
        "tier": TIER,
        "source": SOURCE,
        "note": NOTE,
        "vargottama": {
            "citation": "Patel Ch.III (Vargottama Navāṁśa)",
            "gloss": "A planet — or the lagna — occupying the same sign in the D1 "
                     "and the D9. Patel reads it as strong, its results amplified; "
                     "uccha-/nīca-vargottama fall in the planet's exaltation / "
                     "debilitation sign.",
            "items": vargottama,
        },
        "pushkara": {
            "citation": "Patel Ch.IV (Pushkara Navāṁśa)",
            "gloss": "One of a sign's two auspicious navāṁśas (2 of 9). Patel reads "
                     "a graha here as supported — tending to higher status.",
            "items": pushkara,
        },
        "khara": {
            "citation": "Patel Ch.V (The 64th Navāṁśa)",
            "gloss": "The 64th navāṁśa (Khara) — always in the 8th rāśi from the "
                     "point. A classical sensitive point: Patel keys malefic "
                     "transits and its dusthāna-placed lord to hardship for the "
                     "related significations. Reported as a point, not a verdict.",
            "items": khara,
        },
        "bhava_suchaka": {
            "citation": "Patel Ch.VI (Rāśi-tulya Navāṁśa)",
            "gloss": "Each navāṁśa-sign named by the house it holds in the rāśi "
                     "chart. More points in the prosperous houses (Lagna / Sukha / "
                     "Putra / Bhāgya / Karma / Lābha) → ease; more in the difficult "
                     "(Ṣaṣṭha / Nidhana / Vyaya) → struggle (Dhruva-Nāḍī via Patel).",
            "items": bhava_items,
            "tally": tally,
        },
    }
