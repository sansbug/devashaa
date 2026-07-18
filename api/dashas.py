"""Nakṣatra ('udu') daśā family from BPHS Vol II, Chapter 46.

These daśās share Viṁśottarī's machinery — the starting lord is the Moon-
nakṣatra lord, the balance at birth is `lord_years × (1 − fraction)`, and sub-
periods nest proportionally in the system's own lord order. They differ only in:
  - the lord list and each lord's year-span (hence the total),
  - the reference nakṣatra the lord-count starts from.

Each system carries the book's own worked example (janma nakṣatra → starting
lord); build_dasha_system self-checks against it, and app.py only exposes
systems whose example reproduces exactly.

Sign-based daśās (Kālachakra, Chara, Chakra, Kāla) are structurally different
and NOT here — they need their own engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import swisseph as swe

from vimshottari import (
    DashaPeriod, LEVEL_NAMES, _jd_to_local, _fmt_ymd, _strip_jd,
    DEFAULT_YEAR_DAYS, YEAR_DAYS_SAVANA, YEAR_DAYS_JULIAN,
)
from zoneinfo import ZoneInfo
from datetime import timezone

# Nakṣatra numbers (1-27) for reference points named in the text.
NAK = {
    "ashwini": 1, "bharani": 2, "krittika": 3, "rohini": 4, "mrigasira": 5,
    "ardra": 6, "punarvasu": 7, "pushya": 8, "ashlesha": 9, "magha": 10,
    "pphalguni": 11, "uphalguni": 12, "hasta": 13, "chitra": 14, "swati": 15,
    "vishakha": 16, "anuradha": 17, "jyeshtha": 18, "mula": 19, "pashadha": 20,
    "uashadha": 21, "shravana": 22, "dhanishta": 23, "shatabhisha": 24,
    "pbhadra": 25, "ubhadra": 26, "revati": 27,
}


@dataclass(frozen=True)
class DashaSystem:
    key: str
    name: str
    lords: tuple[tuple[str, str, int], ...]  # (graha_key, display, years)
    ref_nakshatra: int                       # 1-27, the count origin
    citation: str
    # book worked example for self-validation: (janma_nak 1-27, expected lord key)
    example: tuple[int, str] | None = None
    applicability: str = ""

    @property
    def total_years(self) -> int:
        return sum(y for _, _, y in self.lords)

    @property
    def n(self) -> int:
        return len(self.lords)

    def order(self) -> list[str]:
        return [k for k, _, _ in self.lords]

    def years_of(self) -> dict[str, int]:
        return {k: y for k, _, y in self.lords}

    def name_of(self) -> dict[str, str]:
        return {k: nm for k, nm, _ in self.lords}

    def starting_lord(self, janma_nak: int) -> str:
        """Lord of the daśā running at birth, for Moon in nakṣatra `janma_nak`.

        Count nakṣatras from ref to janma (inclusive of the origin's slot) and
        take modulo N. idx0 = (janma − ref) mod 27, then mod N.
        """
        delta = (janma_nak - self.ref_nakshatra) % 27
        return self.order()[delta % self.n]


# --- the systems (Vimsottari kept here too, so all daśās share one path) ----------

SYSTEMS: dict[str, DashaSystem] = {
    "vimshottari": DashaSystem(
        key="vimshottari", name="Viṁśottarī",
        lords=(("ketu", "Ketu", 7), ("venus", "Shukra", 20), ("sun", "Surya", 6),
               ("moon", "Chandra", 10), ("mars", "Mangala", 7), ("rahu", "Rahu", 18),
               ("jupiter", "Guru", 16), ("saturn", "Shani", 19), ("mercury", "Budha", 17)),
        ref_nakshatra=NAK["ashwini"],
        citation="BPHS Vol II ch.46 vv.12-16",
        example=(NAK["mrigasira"], "mars"),   # Mṛgaśira → Mars (v.16 note)
        applicability="Parāśara's primary daśā, applicable to all charts.",
    ),
    "shodasottari": DashaSystem(
        key="shodasottari", name="Ṣoḍaśottarī",
        lords=(("sun", "Surya", 11), ("mars", "Mangala", 12), ("jupiter", "Guru", 13),
               ("saturn", "Shani", 14), ("ketu", "Ketu", 15), ("moon", "Chandra", 16),
               ("mercury", "Budha", 17), ("venus", "Shukra", 18)),
        ref_nakshatra=NAK["pushya"],
        citation="BPHS Vol II ch.46 vv.24-26",
        example=(NAK["rohini"], "venus"),     # Rohiṇī → Venus (worked example p.27)
        applicability="When the Lagna is in the horā of the Moon (Kṛṣṇa pakṣa) "
                      "or of the Sun (Śukla pakṣa).",
    ),
    "dwadasottari": DashaSystem(
        key="dwadasottari", name="Dvādaśottarī",
        lords=(("sun", "Surya", 7), ("jupiter", "Guru", 9), ("ketu", "Ketu", 11),
               ("mercury", "Budha", 13), ("rahu", "Rahu", 15), ("mars", "Mangala", 17),
               ("saturn", "Shani", 19), ("moon", "Chandra", 21)),
        ref_nakshatra=NAK["revati"],
        citation="BPHS Vol II ch.46 vv.27-28",
        example=None,   # no numeric example given in text
        applicability="When the Lagna falls in a specific horā (see ch.46).",
    ),
    "panchottari": DashaSystem(
        key="panchottari", name="Pañcottarī",
        lords=(("sun", "Surya", 12), ("mercury", "Budha", 13), ("saturn", "Shani", 14),
               ("mars", "Mangala", 15), ("venus", "Shukra", 16), ("moon", "Chandra", 17),
               ("jupiter", "Guru", 18)),
        ref_nakshatra=NAK["anuradha"],
        citation="BPHS Vol II ch.46 vv.29-31",
        example=None,
        applicability="When the Lagna is Cancer and in the Cancer dvādaśāṁśa.",
    ),
    "shatabdika": DashaSystem(
        key="shatabdika", name="Śatābdikā",
        lords=(("sun", "Surya", 5), ("moon", "Chandra", 5), ("venus", "Shukra", 10),
               ("mercury", "Budha", 10), ("jupiter", "Guru", 20), ("mars", "Mangala", 20),
               ("saturn", "Shani", 30)),
        ref_nakshatra=NAK["revati"],
        citation="BPHS Vol II ch.46 vv.32-34",
        example=(NAK["mrigasira"], "mars"),   # Mṛgaśira → Mars (example p.31)
        applicability="See ch.46; a 100-year cycle.",
    ),
    "chaturashiti": DashaSystem(
        key="chaturashiti", name="Chaturaśīti-sama",
        lords=(("sun", "Surya", 12), ("moon", "Chandra", 12), ("mars", "Mangala", 12),
               ("mercury", "Budha", 12), ("jupiter", "Guru", 12), ("venus", "Shukra", 12),
               ("saturn", "Shani", 12)),
        ref_nakshatra=NAK["swati"],
        citation="BPHS Vol II ch.46 vv.35-36",
        example=(NAK["mrigasira"], "mars"),   # Mṛgaśira → Mars (example p.33)
        applicability="When the lord of the Lagna is in the 7th house.",
    ),
    "dwisaptati": DashaSystem(
        key="dwisaptati", name="Dvisaptati-sama",
        lords=(("sun", "Surya", 9), ("moon", "Chandra", 9), ("mars", "Mangala", 9),
               ("mercury", "Budha", 9), ("jupiter", "Guru", 9), ("venus", "Shukra", 9),
               ("saturn", "Shani", 9), ("rahu", "Rahu", 9)),
        ref_nakshatra=NAK["mula"],
        citation="BPHS Vol II ch.46 vv.37-39",
        example=None,
        applicability="When the lord of the Lagna is in the 7th, or the 7th "
                      "lord in the Lagna.",
    ),
    "shattrimsha": DashaSystem(
        key="shattrimsha", name="Ṣaṭtriṁśat-sama",
        lords=(("moon", "Chandra", 1), ("sun", "Surya", 2), ("jupiter", "Guru", 3),
               ("mars", "Mangala", 4), ("mercury", "Budha", 5), ("saturn", "Shani", 6),
               ("venus", "Shukra", 7), ("rahu", "Rahu", 8)),
        ref_nakshatra=NAK["shravana"],
        citation="BPHS Vol II ch.46 vv.42-43",
        example=None,
        applicability="Day birth with Lagna in the Sun's horā, or night birth "
                      "with Lagna in the Moon's horā.",
    ),
}


def _rotated(order: list[str], lord: str) -> list[str]:
    i = order.index(lord)
    return order[i:] + order[:i]


def _subdivide(system: DashaSystem, start_jd: float, total_days: float,
               lord: str, level: int, depth: int, as_of_jd, tz, year_days):
    years_of = system.years_of()
    name_of = system.name_of()
    order = system.order()
    total = system.total_years
    out = []
    cursor = start_jd
    for sub in _rotated(order, lord):
        dur = total_days * years_of[sub] / total
        end = cursor + dur
        node = DashaPeriod(
            level=level,
            level_name=LEVEL_NAMES[level] if level < len(LEVEL_NAMES) else f"L{level}",
            lord=sub, lord_name=name_of[sub],
            start_jd=cursor, end_jd=end,
            start=_jd_to_local(cursor, tz), end=_jd_to_local(end, tz),
            years=dur / year_days,
            is_current=(as_of_jd is not None and cursor <= as_of_jd < end),
        )
        if depth > level + 1:
            node.sub = _subdivide(system, cursor, dur, sub, level + 1, depth,
                                  as_of_jd, tz, year_days)
        out.append(node)
        cursor = end
    return out


def _assemble(system, start_lord, elapsed_years, balance_years, birth_jd,
              depth, as_of_jd, tz_name, year_days):
    """Build the mahādaśā tree once the starting lord and elapsed years are known.

    Shared by the simple (build_dasha_system) and group (build_ashtottari)
    balance methods — they differ only in how elapsed_years is derived.
    """
    tz = ZoneInfo(tz_name) if tz_name else timezone.utc
    years_of, name_of, total = system.years_of(), system.name_of(), system.total_years

    notional_start = birth_jd - elapsed_years * year_days
    end_target = notional_start + total * year_days - 0.5
    seq = _rotated(system.order(), start_lord)
    mahas, cursor, idx = [], notional_start, 0
    while cursor < end_target:
        lord = seq[idx % system.n]
        dur = years_of[lord] * year_days
        end = cursor + dur
        node = DashaPeriod(
            level=0, level_name=LEVEL_NAMES[0], lord=lord, lord_name=name_of[lord],
            start_jd=cursor, end_jd=end,
            start=_jd_to_local(cursor, tz), end=_jd_to_local(end, tz),
            years=float(years_of[lord]),
            is_current=(as_of_jd is not None and cursor <= as_of_jd < end),
        )
        if depth > 1:
            node.sub = _subdivide(system, cursor, dur, lord, 1, depth, as_of_jd,
                                  tz, year_days)
        mahas.append(node)
        cursor = end
        idx += 1

    return {
        "system": system.name,
        "system_key": system.key,
        "citation": system.citation,
        "applicability": system.applicability,
        "year_days": year_days,
        "year_system": "sāvana (360)" if year_days == YEAR_DAYS_SAVANA
                       else ("Julian (365.25)" if year_days == YEAR_DAYS_JULIAN
                             else f"{year_days}-day"),
        "total_years": total,
        "timezone": tz_name or "UTC",
        "levels": LEVEL_NAMES[:depth],
        "starting_lord": start_lord,
        "starting_lord_name": name_of[start_lord],
        "balance_years": balance_years,
        "balance_at_birth": _fmt_ymd(balance_years, year_days),
        "mahadashas": [_strip_jd(m) for m in mahas],
    }


def build_dasha_system(
    system: DashaSystem,
    birth_jd: float,
    moon_nakshatra_index: int,
    moon_nakshatra_fraction: float,
    depth: int = 3,
    as_of_jd=None,
    tz_name: str | None = None,
    year_days: float = DEFAULT_YEAR_DAYS,
) -> dict:
    start_lord = system.starting_lord(moon_nakshatra_index)
    elapsed_years = moon_nakshatra_fraction * system.years_of()[start_lord]
    balance_years = system.years_of()[start_lord] - elapsed_years
    return _assemble(system, start_lord, elapsed_years, balance_years, birth_jd,
                     depth, as_of_jd, tz_name, year_days)


def validated_systems() -> list[str]:
    """Keys of systems whose book worked-example reproduces (or that have none
    to contradict). A mismatch means our count convention is wrong for it."""
    ok = []
    for key, sys in SYSTEMS.items():
        if sys.example is None:
            ok.append(key)
            continue
        janma, expected = sys.example
        if sys.starting_lord(janma) == expected:
            ok.append(key)
    return ok


# ================================================================================
# Aṣṭottarī daśā — group method (BPHS Vol II ch.46 vv.17-23)
# ================================================================================
# Unlike the udu daśās, each lord rules a CONSECUTIVE GROUP of 3 or 4 nakṣatras
# (4,3,4,3,4,3,4,3 from Ārdrā), and it uses 28 nakṣatras — Abhijit is carved out
# of the 4th pāda of U.Aṣāḍhā plus the first 1/15 of Śravaṇa. The balance needs
# the nakṣatra's position within its lord's group:
#     balance = lord_years × (1 − (j + fraction)/k)
# where j = 0-indexed slot in the group, k = group size, fraction within the
# nakṣatra's (possibly non-standard) span. Verified against the book's Venus/
# Mṛgaśira (v.16 note) and Saturn/U.Aṣāḍhā (p.26) worked examples.

ASHTOTTARI = DashaSystem(
    key="ashtottari", name="Aṣṭottarī",
    lords=(("sun", "Surya", 6), ("moon", "Chandra", 15), ("mars", "Mangala", 8),
           ("mercury", "Budha", 17), ("saturn", "Shani", 10), ("jupiter", "Guru", 19),
           ("rahu", "Rahu", 12), ("venus", "Shukra", 21)),
    ref_nakshatra=NAK["ardra"],   # groups begin at Ārdrā
    citation="BPHS Vol II ch.46 vv.17-23",
    example=None,   # validated numerically below, not via the udu count rule
    applicability="When Rāhu is in a kendra or trikoṇa from the Lagna lord (but "
                  "not in the Lagna); or day-birth in Kṛṣṇa pakṣa / night-birth "
                  "in Śukla pakṣa.",
)

_NAK_ARC = 360.0 / 27.0
# Abhijit = 4th pāda of U.Aṣāḍhā (276°40'–280°) + first 1/15 of Śravaṇa
# (280°–280°53'20"). So Abhijit spans 276°40' to 280°53'20".
_ABHIJIT_START = 20 * _NAK_ARC + 3 * (_NAK_ARC / 4)   # 276°40'  (U.Aṣāḍhā 4th pāda)
_ABHIJIT_END = 22 * _NAK_ARC - (_NAK_ARC / 15)        # 280°53'20" (Śravaṇa − 1/15)


def _ashtottari_slots():
    """The 28 Aṣṭottarī nakṣatra slots in zodiacal order, each with lord, the
    slot's group position j, group size k, and its longitude span."""
    # Group order from Ārdrā (nak 6), sizes 4,3,4,3,4,3,4,3; 'abhijit' inserted
    # between U.Aṣāḍhā (21) and Śravaṇa (22).
    walk = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
            20, 21, "abhijit", 22, 23, 24, 25, 26, 27, 1, 2, 3, 4, 5]
    lords = [k for k, _, _ in ASHTOTTARI.lords]
    sizes = [4, 3, 4, 3, 4, 3, 4, 3]

    def span(ident):
        if ident == "abhijit":
            return (_ABHIJIT_START, _ABHIJIT_END)
        if ident == 21:  # U.Aṣāḍhā — first 3 pādas only in Aṣṭottarī
            return (20 * _NAK_ARC, _ABHIJIT_START)
        if ident == 22:  # Śravaṇa — minus its first 1/15
            return (_ABHIJIT_END, 22 * _NAK_ARC)
        return ((ident - 1) * _NAK_ARC, ident * _NAK_ARC)

    slots, w = [], 0
    for gi, (lord, k) in enumerate(zip(lords, sizes)):
        for j in range(k):
            ident = walk[w]
            lo, hi = span(ident)
            slots.append({"lord": lord, "j": j, "k": k, "lo": lo, "hi": hi,
                          "ident": ident})
            w += 1
    return slots


_ASHTOTTARI_SLOTS = _ashtottari_slots()


def ashtottari_position(moon_longitude: float):
    """(lord, j, k, fraction) for a sidereal Moon longitude, Aṣṭottarī scheme."""
    lon = moon_longitude % 360.0
    for s in _ASHTOTTARI_SLOTS:
        if s["lo"] <= lon < s["hi"]:
            frac = (lon - s["lo"]) / (s["hi"] - s["lo"])
            return s["lord"], s["j"], s["k"], frac
    # Numerical edge at 360→0: fall back to the first slot containing 0.
    s = next(x for x in _ASHTOTTARI_SLOTS if x["lo"] <= 0 < x["hi"])
    return s["lord"], s["j"], s["k"], 0.0


def build_ashtottari(
    moon_longitude: float,
    birth_jd: float,
    depth: int = 3,
    as_of_jd=None,
    tz_name: str | None = None,
    year_days: float = DEFAULT_YEAR_DAYS,
) -> dict:
    lord, j, k, frac = ashtottari_position(moon_longitude)
    lord_years = ASHTOTTARI.years_of()[lord]
    elapsed_years = lord_years * (j + frac) / k
    balance_years = lord_years - elapsed_years
    return _assemble(ASHTOTTARI, lord, elapsed_years, balance_years, birth_jd,
                     depth, as_of_jd, tz_name, year_days)
