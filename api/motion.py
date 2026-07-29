"""Planetary motion (gati) and combustion — computed facts + traditional labels.

WHAT IS COMPUTED, AND WHAT IS REFUSED
-------------------------------------
From the .se1 ephemeris the chart already carries each graha's signed sidereal
SPEED (°/day). That, and the angular separation from the Sun, are astronomical
FACTS. On top of them this module lays two `traditional`-tier readings and, as
always here, refuses the one the text cannot supply:

  • MOTION STATE (gati). direction (retrograde ⇔ speed < 0) and near-stationary
    (|speed| far below the graha's mean, on EITHER side of a station) are FACTS;
    the gati NAMES — a five-band reduction of the classical aṣṭa-gati, here
    vakra / vikala / manda / sama / atichāra — and the fast/slow bands are the
    classical scheme, so they ship `traditional`. The Sun and Moon never
    retrograde; Rāhu/Ketu (mean node) are ALWAYS retrograde by definition, not by
    cheṣṭā — flagged as such.

  • COMBUSTION (astaṅgata). the separation from the Sun is a FACT. The verdict
    "combust within N°" is `traditional` and, per docs/bphs-rules.md, explicitly
    OUT of BPHS: Parāśara gives no orb — his combustion is the ch.7 vv.28-29
    rule-of-three proportion across 0–180° from Sūrya. The fixed orbs come only
    from a Santhanam note (Vol I, scoped to āyurdāya) whose RETROGRADE column is
    OCR-damaged, so a retrograde Mercury/Venus verdict is `uncertain`.

  • CHEṢṬĀ BALA (the numeric motion-strength) is REFUSED. BPHS ch.27 vv.24-25
    needs each graha's Seeghrocha and never tabulates one (the word appears 3× in
    1,034 pages, always undefined); there is no worked Ṣaḍbala example to check
    against. The analysis panel already reports it unavailable — this module does
    not invent it, and says so.
"""

from __future__ import annotations

TIER_FACT = "computed"          # from the ephemeris — astronomical fact
TIER_TRAD = "traditional"       # the classical label / orb, NOT BPHS

# Mean geocentric daily motion (°/day). Superior planets complete 360°
# geocentrically over one sidereal period, so their mean = 360 / period; Mercury
# and Venus track the Sun geocentrically, so their mean is the Sun's own rate;
# the nodes are the mean lunar node (~18.6-year retrograde cycle).
MEAN_DAILY = {
    "sun": 0.9856, "moon": 13.1764, "mars": 0.5240,
    "mercury": 0.9856, "jupiter": 0.0831, "venus": 0.9856,
    "saturn": 0.0335, "rahu": 0.0529, "ketu": 0.0529,
}

# Grahas that can turn retrograde (so can be genuinely near-stationary).
_RETRO_CAPABLE = frozenset({"mars", "mercury", "jupiter", "venus", "saturn"})
_NODES = frozenset({"rahu", "ketu"})

# Below this fraction of its mean, a retro-capable graha is treated as
# near-stationary (approaching a station). Auto-scales per graha; a convention.
_STATIONARY_FRAC = 0.15
# The "average" (sama) band around the mean; outside it is slow / swift.
_SLOW_HI, _SWIFT_LO = 0.90, 1.10

_GATI = {
    "vakra":    {"iast": "vakra", "en": "retrograde"},
    "vikala":   {"iast": "vikala", "en": "near-stationary"},
    "manda":    {"iast": "manda", "en": "slow"},
    "sama":     {"iast": "sama", "en": "average"},
    "atichara": {"iast": "atichāra", "en": "swift"},
    "node":     {"iast": "vakra", "en": "retrograde — by definition (mean node)"},
}

# Traditional combustion orbs (°), DIRECT motion. Out-of-BPHS (Santhanam's
# āyurdāya note); widely followed. No orb for the Sun (the source) or the nodes.
_COMBUST_ORB = {
    "moon": 12.0, "mars": 17.0, "mercury": 14.0,
    "jupiter": 11.0, "venus": 10.0, "saturn": 15.0,
}
# Retrograde orbs for the two that combust while retrograde — from the
# OCR-DAMAGED column, so any verdict resting on these is `uncertain`.
_COMBUST_ORB_RETRO = {"mercury": 12.0, "venus": 8.0}

_BPHS_COMBUSTION_NOTE = (
    "BPHS gives no fixed orb — its combustion is the ch.7 vv.28-29 rule-of-three "
    "proportion across 0–180° from Sūrya. These fixed orbs come only from a "
    "Santhanam note in BPHS Vol I (which he scopes to āyurdāya); the orb-based "
    "verdict here is the later traditional convention, not Parāśara."
)
_RETRO_ORB_NOTE = (
    "Retrograde-motion orb: from an OCR-damaged column in the only source that "
    "gives fixed orbs, so this verdict is uncertain."
)

CHESHTA_BALA = {
    "available": False,
    "citation": "BPHS Vol I ch.27 vv.24-25",
    "reason": "Cheṣṭā bala — the numeric strength of a graha's motion — needs each "
              "graha's Seeghrocha (śīghrocca). BPHS instructs its use but never "
              "tabulates a value (three occurrences in 1,034 pages, always "
              "undefined), and there is no worked Ṣaḍbala example to validate "
              "against. Sūrya and Chandra are the exception (ch.28 vv.3-4). The "
              "motion STATE below is descriptive; it is not this bala.",
}


def _sep_from_sun(lon: float, sun_lon: float) -> float:
    """Angular separation from the Sun, 0–180° (a fact)."""
    return abs((lon - sun_lon + 180.0) % 360.0 - 180.0)


def _gati(name: str) -> dict:
    """A gati label carrying its own tier (traditional), so a row read in
    isolation still shows the classical name is NOT a computed fact."""
    return {**_GATI[name], "tier": TIER_TRAD}


def _motion_state(key: str, speed: float) -> dict:
    mean = MEAN_DAILY[key]           # every value is nonzero; no guard needed
    ratio = abs(speed) / mean
    retro = speed < 0
    if key in _NODES:
        return {"direction": "retrograde", "retrograde": True, "stationary": False,
                "pace": None, "gati": _gati("node"),
                "speed": round(speed, 5), "mean": mean, "ratio": round(ratio, 3)}
    # Near-stationary is a FACT: |speed| far below the graha's mean, on EITHER
    # side of a station. Computed BEFORE the retro/direct split so a graha
    # approaching or leaving a retrograde station is caught too.
    stationary = key in _RETRO_CAPABLE and ratio < _STATIONARY_FRAC
    if stationary:
        gati, pace = "vikala", None          # vikala takes the name near a station
    elif retro:
        gati, pace = "vakra", None
    elif ratio > _SWIFT_LO:
        gati, pace = "atichara", "swift"
    elif ratio >= _SLOW_HI:
        gati, pace = "sama", "average"
    else:
        gati, pace = "manda", "slow"
    return {
        "direction": "retrograde" if retro else "direct",
        "retrograde": retro, "stationary": stationary, "pace": pace,
        "gati": _gati(gati),
        "speed": round(speed, 5), "mean": mean, "ratio": round(ratio, 3),
    }


def _combustion(key: str, lon: float, sun_lon: float, retro: bool) -> dict:
    if key == "sun":
        return {"applies": False, "reason": "the Sun is the source of combustion"}
    if key in _NODES:
        return {"applies": False,
                "reason": "Rāhu/Ketu are shadow points — combustion does not apply"}
    sep = round(_sep_from_sun(lon, sun_lon), 2)
    orb = _COMBUST_ORB[key]
    note = _BPHS_COMBUSTION_NOTE
    confidence = TIER_TRAD
    if retro and key in _COMBUST_ORB_RETRO:
        orb = _COMBUST_ORB_RETRO[key]
        confidence = "uncertain"
        note = _RETRO_ORB_NOTE + " " + _BPHS_COMBUSTION_NOTE
    return {
        "applies": True, "separation": sep, "orb": orb,
        "combust": sep <= orb, "tier": TIER_TRAD, "confidence": confidence,
        "note": note,
    }


def motion_analysis(grahas: list[dict]) -> dict:
    """Per-graha motion (gati) + combustion.

    `grahas` is a list of dicts each carrying at least "key", "longitude" and
    "speed" (the chart already computes these). Returns a facts-first payload
    with the traditional labels attached and Cheṣṭā bala reported unavailable.
    """
    sun = next((g for g in grahas if g["key"] == "sun"), None)
    sun_lon = sun["longitude"] if sun else 0.0
    rows = []
    for g in grahas:
        rows.append({
            "key": g["key"],
            "motion": _motion_state(g["key"], g["speed"]),
            "combustion": _combustion(g["key"], g["longitude"], sun_lon, g["speed"] < 0),
        })
    return {
        "tiers": {
            "fact": "speed, direction, stationary, separation from the Sun — "
                    "astronomical facts from the ephemeris",
            "traditional": "the gati names (vakra/manda/…) and the combustion "
                           "orbs — the classical scheme, NOT BPHS",
        },
        "cheshta_bala": CHESHTA_BALA,
        "grahas": rows,
    }
