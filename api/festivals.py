"""Hindu festivals / special observances for a given day — dṛg-gaṇita vyāpti.

A festival is a (māsa, pakṣa, tithi) that must PREVAIL during a particular period
of the day; the recurring vratas drop the māsa; the two saṅkrāntis are solar. We
match against the verified table in :mod:`festivals_data` (37 rows, every one
adversarially checked — see the ``panchang-festivals-verify`` workflow — with the
amānta/pūrṇimānta kṛṣṇa-pakṣa month-shift resolved per cell).

MATCHING = vyāpti (prevalence), not point-sampling. For each festival we take its
required kāla WINDOW (a real time interval — sunrise, pradoṣa, niśīta, aparāhṇa,
madhyāhna, pūrvāhṇa, or moonrise) and test whether the exact tithi OVERLAPS it,
then apply the observance's tie-break (``first`` day it covers the window, or
``last``). Because the tithi is computed to the second and a tithi (≥19 h) always
dwarfs a kāla window (≤ ~2.5 h), testing the window's two edges is an exact
overlap test. This is the rule a dṛk (dṛg-gaṇita) almanac uses — e.g. Diwali =
the day amāvāsyā covers pradoṣa, Mahā-śivarātri = kṛṣṇa-caturdaśī over niśīta,
Vijayadaśamī = śukla-daśamī over aparāhṇa, Saṅkaṣṭī = kṛṣṇa-caturthī at moonrise.

IRREDUCIBLE AMBIGUITY, stated not hidden: a few observances legitimately fall on
two different days by tradition (smārta vs vaiṣṇava Ekādaśī / Janmāṣṭamī); we take
the mainstream (smārta / pūrva-viddhā) reading, which is the one a general almanac
prints first. Holika Dahan's bhadrā (Viṣṭi-karaṇa) exclusion is not modelled.

Adhika (intercalary) months: month-specific festivals shift to the nija month, so
an ``adhika`` month matches none of them (the recurring vratas still match).
"""
from __future__ import annotations

from festivals_data import FESTIVALS
from panchang import tithi_pk_num_at, kala_window

CONVENTION = (
    "Festival days are found by vyāpti: the exact tithi (computed to the second) "
    "must overlap the observance's kāla window — sunrise for most; pradoṣa "
    "(Diwali, Dhanteras), niśīta (Śivarātri, Janmāṣṭamī), aparāhṇa (Vijayadaśamī), "
    "madhyāhna (Rāma-navamī, Gaṇeśa-caturthī), pūrvāhṇa (Vasant-pañcamī), or "
    "moonrise (Saṅkaṣṭī, Karva Chauth) — with the standard first/last tie-break. "
    "Amānta month reckoning. Observances that split by tradition (smārta vs "
    "vaiṣṇava) are given on the mainstream day. Holika-Dahan's bhadrā (Viṣṭi-"
    "karaṇa) deferral is not modelled, so in a bhadrā-complicated year Holika-"
    "Dahan and the Holi that follows it can fall one day early."
)

_IMPORTANCE_RANK = {"major": 0, "notable": 1, "observance": 2}

# The five limbs carry IAST pakṣa; the table uses ASCII keys.
_PAKSHA = {"śukla": "shukla", "kṛṣṇa": "krishna"}

# Per-festival vyāpti: (kāla window, tie-break). Default is sunrise / first.
# Windows are real intervals (see panchang.kala_window); the tie-break picks the
# civil day when the tithi covers the window on more than one consecutive day.
_DEFAULT = ("sunrise", "first")
_VYAPTI = {
    "rama-navami":         ("madhyahna", "first"),   # Rāma born at midday
    "ganesh-chaturthi":    ("madhyahna", "first"),   # Gaṇeśa born at midday
    "krishna-janmashtami": ("nishita", "first"),     # Kṛṣṇa born at midnight (smārta)
    "maha-shivaratri":     ("nishita", "first"),
    "masik-shivaratri":    ("nishita", "first"),
    "diwali":              ("pradosha", "first"),    # Lakṣmī-pūjā at dusk
    "dhanteras":           ("pradosha", "first"),
    "holika-dahan":        ("pradosha", "first"),    # bhadrā rule not modelled
    "holi":                ("pradosha", "first"),    # Dhulandi: pratipadā the eve after Holika Dahan
    "vijayadashami":       ("aparahna", "first"),
    "akshaya-tritiya":     ("madhyahna", "first"),  # tṛtīyā at midday
    "vasant-panchami":     ("purvahna", "first"),
    "sharad-purnima":      ("nishita", "first"),     # Kojāgarī — midnight moon vigil
    # Evening (pradoṣa/moonrise) vratas: the tithi's presence at dusk fixes the
    # day even when it lapses just before moonrise.
    "karva-chauth":        ("pradosha", "first"),
    "sankashti-chaturthi": ("pradosha", "first"),
    "chhath":              ("sunset", "first"),      # sandhyā (evening) arghya
    # naraka-chaturdashi keeps the sunrise rule (aruṇodaya ≈ sunrise).
}


def _idx_at(jd: float) -> int:
    """Absolute tithi index 0..29 at instant `jd` (0=śukla-pratipadā … 29=amāvāsyā)."""
    pk, num = tithi_pk_num_at(jd)
    return (0 if pk == "shukla" else 15) + (num - 1)


def _covers(pan: dict, window: str, tidx: int, shift: float = 0.0) -> bool:
    """Does tithi index `tidx` cover `window` on this day (optionally shifted
    `shift` days for the adjacent-day tie-break)? For a point window this is
    presence at the instant; for the pradoṣa interval, presence at either edge (a
    tithi ≥19 h dwarfs the ≤2½ h window, so the two edges are an exact test)."""
    a, b = kala_window(pan, window)
    return _idx_at(a + shift) == tidx or _idx_at(b + shift) == tidx


def _public(f: dict, **extra) -> dict:
    """The client-facing shape — what a reader needs, plus how it was matched."""
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

    `pan` — a :func:`panchang.panchanga` dict (carrying the private sunrise/…/
    moonrise JDs). `masa` — an :func:`panchang_masa.amanta_masa` dict (or None to
    skip month-specific festivals). `sankranti_sign` — the sidereal rāśi the Sun
    enters today, or None. Returns public dicts sorted major→observance.
    """
    masa_idx = masa["index"] if masa else None
    adhika = bool(masa and masa.get("adhika"))

    hits: list[dict] = []
    for f in FESTIVALS:
        if f["basis"] == "solar":
            if sankranti_sign is not None and f["solar_sign"] == sankranti_sign:
                hits.append(_public(f))
            continue

        tidx = (0 if f["paksha"] == "shukla" else 15) + (f["tithi"] - 1)   # 0..29
        window, tie = _VYAPTI.get(f["key"], _DEFAULT)

        matched = _covers(pan, window, tidx)
        ksaya = False
        if not matched and window == "sunrise":
            # Kṣaya (skipped) tithi: it begins after this sunrise and ends before
            # the next, so it touches no sunrise. If the target is that lost tithi
            # it is observed today (the day it runs). a→a+2 across the ahorātra.
            a, b = _idx_at(pan["_jd_rise"]), _idx_at(pan["_jd_next"])
            if (b - a) % 30 == 2 and (a + 1) % 30 == tidx:
                matched = ksaya = True
        if not matched:
            continue
        # Tie-break when the tithi covers the window on two consecutive days
        # (a genuine vṛddhi tithi); a kṣaya day is unique, so it is exempt.
        if not ksaya:
            if tie == "first" and _covers(pan, window, tidx, -1.0):
                continue
            if tie == "last" and _covers(pan, window, tidx, 1.0):
                continue

        if f["recurring"]:
            hits.append(_public(f, kala=window))
        elif not adhika and masa_idx is not None and f["masa"] == masa_idx:
            hits.append(_public(f, kala=window))

    hits.sort(key=lambda x: _IMPORTANCE_RANK.get(x["importance"], 9))
    return hits
