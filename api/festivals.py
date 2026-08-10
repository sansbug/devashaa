"""Hindu festivals / special observances for a given day.

A festival is a (month, pakṣa, tithi) coordinate — or, for the recurring vratas,
just (pakṣa, tithi), and for the two saṅkrānti days a solar ingress. This module
matches a day's pañcāṅga against the verified table in :mod:`festivals_data`
(37 rows, every one adversarially checked — see the ``panchang-festivals-verify``
workflow — with the amānta/pūrṇimānta kṛṣṇa-pakṣa month-shift resolved per cell).

MATCHING CONVENTION — the tithi PREVAILING AT SUNRISE, the same reckoning the
five limbs use and the ordinary sunrise-tithi rule most almanacs print. A few
festivals are observed by a tithi at a specific muhūrta rather than at sunrise —
Diwali's Lakṣmī-pūjā wants amāvāsyā during pradoṣa (dusk), Janmāṣṭamī wants
kṛṣṇa-aṣṭamī at midnight — so on rare boundary years those can land one civil day
off a dṛk-pañcāṅga. That limitation is stated in the payload (``convention``),
never hidden; the intent here is to let a reader SEE roughly when Diwali / Ekādaśī
/ Amāvāsyā fall, not to adjudicate a contested muhūrta.

Adhika (intercalary) months: festivals are observed in the nija month, so a
month flagged ``adhika`` matches no month-specific festival (the recurring vratas
still match — they occur every lunar month).
"""
from __future__ import annotations

from festivals_data import FESTIVALS
from panchang import tithi_pk_num_at, kala_instant

CONVENTION = (
    "Most festivals are matched on the tithi prevailing at sunrise; those fixed "
    "to another kāla are matched there — Diwali/Dhanteras at pradoṣa (dusk), "
    "Mahā-śivarātri at niśīta (midnight), Vijayadaśamī at aparāhṇa (afternoon), "
    "Holi at pradoṣa — and assigned to the first civil day the tithi covers that "
    "kāla, the standard almanac rule. Rare muhūrta ties can still differ a day "
    "from a dṛk-pañcāṅga. Amānta month reckoning."
)

_IMPORTANCE_RANK = {"major": 0, "notable": 1, "observance": 2}

# The five limbs carry IAST pakṣa; the table uses ASCII keys.
_PAKSHA = {"śukla": "shukla", "kṛṣṇa": "krishna"}

# Festivals observed by a tithi at a specific kāla rather than at sunrise. The
# day is the FIRST one whose tithi covers that kāla (see festivals_for_day) — so
# an amāvāsyā spanning two dusks lands Diwali on the earlier day, as almanacs do.
_KALA = {
    "diwali": "pradosha", "dhanteras": "pradosha", "holi": "pradosha",
    # Evening / moonrise vratas — dusk is the closest kāla we compute to the
    # chandrodaya (moonrise) the fast actually turns on.
    "karva-chauth": "pradosha", "sankashti-chaturthi": "pradosha",
    "maha-shivaratri": "nishita", "masik-shivaratri": "nishita",
    "vijayadashami": "aparahna", "vasant-panchami": "purvahna",
    # Naraka Chaturdaśī turns on the pre-dawn (aruṇodaya) chaturdaśī, which the
    # sunrise tithi tracks better than dusk — so it is left on the sunrise rule.
}


def _public(f: dict, **extra) -> dict:
    """The client-facing shape — no internal match coordinates, just what a
    reader needs, plus how the day was matched."""
    out = {
        "key": f["key"], "name": f["name"], "name_hi": f["name_hi"],
        "importance": f["importance"], "basis": f["basis"],
        "significance": f["significance"], "significance_hi": f["significance_hi"],
    }
    if f.get("masa_purnimanta"):
        out["masa_purnimanta"] = f["masa_purnimanta"]
    out.update(extra)
    return out


def festivals_for_day(pan: dict, masa: dict | None, sankranti_sign: int | None) -> list[dict]:
    """Every festival/observance falling on this day.

    `pan` — a :func:`panchang.panchanga` dict. `masa` — an
    :func:`panchang_masa.amanta_masa` dict (or None to skip month-specific
    festivals). `sankranti_sign` — the sidereal rāśi the Sun enters today, or
    None. Returns public dicts sorted major→observance.
    """
    tithi = pan["tithi"]
    sr_paksha = _PAKSHA.get(tithi["paksha"])
    sr_num = tithi["number_in_paksha"]         # 1..15 at sunrise
    masa_idx = masa["index"] if masa else None
    adhika = bool(masa and masa.get("adhika"))

    hits: list[dict] = []
    for f in FESTIVALS:
        if f["basis"] == "solar":
            if sankranti_sign is not None and f["solar_sign"] == sankranti_sign:
                hits.append(_public(f))
            continue

        # Which tithi decides this festival — sunrise, or a named kāla?
        kala = _KALA.get(f["key"])
        if kala:
            jd = kala_instant(pan, kala)
            pk, num = tithi_pk_num_at(jd)
            if pk != f["paksha"] or num != f["tithi"]:
                continue
            # First-day rule: skip if the SAME tithi already covered this kāla a
            # day earlier (a tithi spanning two dusks → the earlier day wins).
            pk0, num0 = tithi_pk_num_at(jd - 1.0)
            if pk0 == f["paksha"] and num0 == f["tithi"]:
                continue
            matched_via = kala
        else:
            if f["paksha"] != sr_paksha or f["tithi"] != sr_num:
                continue
            matched_via = "sunrise"

        if f["recurring"]:
            hits.append(_public(f, kala=matched_via))
        elif not adhika and masa_idx is not None and f["masa"] == masa_idx:
            hits.append(_public(f, kala=matched_via))

    hits.sort(key=lambda x: _IMPORTANCE_RANK.get(x["importance"], 9))
    return hits
