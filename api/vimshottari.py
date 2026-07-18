"""Viṁśottarī daśā — the 120-year nakṣatra daśā.

VALIDATED against BPHS Vol II, Chapter 46 (Santhanam):
  - year-counts        ch.46 v.15   (6,10,7,18,16,19,17,7,20; sum 120)
  - nakṣatra → lord    ch.46 vv.12-14 + Table of Daśās
  - balance at birth   ch.46 v.16   (balance = dasa_years × (1 − fraction))
See docs/bphs-rules.md for the citations and the worked-example reconciliation.

Method: Moon's-longitude (arc) fraction — the modern method Santhanam endorses
(p.18-19), not the older Pañcāṅga ghaṭi/pala time method.

OPEN: the days-per-year for projecting daśā-years to calendar dates. BPHS's own
worked example (ch.46, Moon at Sag 13° → balance 2m3d) implies the 360-day
sāvana year; YEAR_DAYS below currently defaults to 365.25 (JHora). See docs.

Levels: Mahādaśā → Antardaśā → Pratyantardaśā (extensible via `depth`).
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, field
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import swisseph as swe

# Viṁśottarī lord order with daśā lengths in years (sum = 120). Names are the
# common spelling, matching vedic.py's "common" system.
VIMSHOTTARI: list[tuple[str, str, int]] = [
    ("ketu",    "Ketu",    7),
    ("venus",   "Shukra",  20),
    ("sun",     "Surya",   6),
    ("moon",    "Chandra", 10),
    ("mars",    "Mangala", 7),
    ("rahu",    "Rahu",    18),
    ("jupiter", "Guru",    16),
    ("saturn",  "Shani",   19),
    ("mercury", "Budha",   17),
]
TOTAL_YEARS = 120

# Days per daśā-year, for projecting daśā-years onto the calendar. BPHS's own
# ch.46 worked example implies 360 (sāvana), so that is the default; 365.25
# (Julian) is what Jagannātha Hora and most modern software use. See docs.
YEAR_DAYS_SAVANA = 360.0
YEAR_DAYS_JULIAN = 365.25
DEFAULT_YEAR_DAYS = YEAR_DAYS_SAVANA

_ORDER = [k for k, _, _ in VIMSHOTTARI]
_YEARS = {k: y for k, _, y in VIMSHOTTARI}
_NAME = {k: n for k, n, _ in VIMSHOTTARI}

LEVEL_NAMES = ["Mahādaśā", "Antardaśā", "Pratyantardaśā", "Sūkṣmadaśā", "Prāṇadaśā"]


@dataclass
class DashaPeriod:
    level: int              # 0 = Mahā, 1 = Antar, 2 = Pratyantar …
    level_name: str
    lord: str               # graha key, e.g. "ketu"
    lord_name: str          # display name, e.g. "Ketu"
    start_jd: float
    end_jd: float
    start: str              # ISO date-time (UT)
    end: str
    years: float            # duration in Viṁśottarī years
    is_current: bool = False
    sub: list["DashaPeriod"] = field(default_factory=list)


def _rotated_from(lord_key: str) -> list[str]:
    """Viṁśottarī order beginning at `lord_key` and wrapping once."""
    i = _ORDER.index(lord_key)
    return _ORDER[i:] + _ORDER[:i]


def _jd_to_local(jd: float, tz: timezone | ZoneInfo) -> str:
    """JD(UT) → local wall-clock 'YYYY-MM-DD HH:MM' in `tz`.

    Building the UTC instant from midnight + a timedelta avoids revjul's float
    hour rounding to minute==60. astimezone applies the correct offset for that
    specific date, so DST-observing birth places get the right wall clock at each
    daśā boundary even decades out; fixed-offset zones (e.g. IST) are unaffected.
    """
    y, m, d, hf = swe.revjul(jd, swe.GREG_CAL)
    dt_utc = datetime(y, m, d, tzinfo=timezone.utc) + timedelta(hours=hf)
    return dt_utc.astimezone(tz).strftime("%Y-%m-%d %H:%M")


def _subdivide(start_jd: float, total_days: float, lord_key: str, level: int,
               depth: int, as_of_jd: float | None, tz, year_days: float) -> list[DashaPeriod]:
    """Split [start, start+total_days] into the 9 sub-periods for `lord_key`."""
    out: list[DashaPeriod] = []
    cursor = start_jd
    for sub_key in _rotated_from(lord_key):
        dur_days = total_days * _YEARS[sub_key] / TOTAL_YEARS
        end = cursor + dur_days
        node = DashaPeriod(
            level=level,
            level_name=LEVEL_NAMES[level] if level < len(LEVEL_NAMES) else f"L{level}",
            lord=sub_key,
            lord_name=_NAME[sub_key],
            start_jd=cursor,
            end_jd=end,
            start=_jd_to_local(cursor, tz),
            end=_jd_to_local(end, tz),
            years=dur_days / year_days,
            is_current=(as_of_jd is not None and cursor <= as_of_jd < end),
        )
        if depth > level + 1:
            node.sub = _subdivide(cursor, dur_days, sub_key, level + 1, depth,
                                  as_of_jd, tz, year_days)
        out.append(node)
        cursor = end
    return out


def build_vimshottari(
    birth_jd: float,
    moon_nakshatra_index: int,   # 1-27
    moon_nakshatra_fraction: float,  # 0-1 through the nakṣatra
    depth: int = 3,
    as_of_jd: float | None = None,
    span_years: float = 120.0,
    tz_name: str | None = None,  # birth-place IANA zone; dates shown in it
    year_days: float = DEFAULT_YEAR_DAYS,  # 360 sāvana (BPHS) or 365.25 Julian
) -> dict:
    """Full Viṁśottarī tree from birth.

    The starting mahādaśā is the Moon-nakṣatra lord, entered `fraction` of the way
    through. Its NOTIONAL start is therefore before birth; we anchor the whole
    sequence to that notional start so every boundary is exact, then report the
    balance remaining at birth separately.

    All internal math is in JD(UT); dates are formatted in `tz_name` (the birth
    place's local wall clock) if given, else UTC. `year_days` sets how daśā-years
    project onto the calendar (see module docstring). Neither affects the lord
    sequence, the year-counts, or is_current — only the calendar dates.
    """
    tz = ZoneInfo(tz_name) if tz_name else timezone.utc
    start_lord = _ORDER[(moon_nakshatra_index - 1) % 9]
    start_years = _YEARS[start_lord]

    elapsed_years = moon_nakshatra_fraction * start_years
    balance_years = start_years - elapsed_years

    # Notional start of the running mahādaśā (before birth).
    notional_start_jd = birth_jd - elapsed_years * year_days

    # Generate mahādaśās from the notional start over one full cycle (span_years,
    # default 120 = exactly the 9 lords once). The first one begins before birth
    # and contains it; balance_years reports the part left at birth.
    end_target_jd = notional_start_jd + span_years * year_days - 0.5  # -0.5d guards fp
    mahas: list[DashaPeriod] = []
    cursor = notional_start_jd
    seq = _rotated_from(start_lord)
    idx = 0
    while cursor < end_target_jd:
        lord = seq[idx % 9]
        dur_days = _YEARS[lord] * year_days
        end = cursor + dur_days
        node = DashaPeriod(
            level=0, level_name=LEVEL_NAMES[0],
            lord=lord, lord_name=_NAME[lord],
            start_jd=cursor, end_jd=end,
            start=_jd_to_local(cursor, tz), end=_jd_to_local(end, tz),
            years=float(_YEARS[lord]),
            is_current=(as_of_jd is not None and cursor <= as_of_jd < end),
        )
        if depth > 1:
            node.sub = _subdivide(cursor, dur_days, lord, 1, depth, as_of_jd, tz,
                                  year_days)
        mahas.append(node)
        cursor = end
        idx += 1

    return {
        "system": "Viṁśottarī",
        "year_days": year_days,
        "year_system": "sāvana (360)" if year_days == YEAR_DAYS_SAVANA
                       else ("Julian (365.25)" if year_days == YEAR_DAYS_JULIAN
                             else f"{year_days}-day"),
        "total_years": TOTAL_YEARS,
        "timezone": tz_name or "UTC",
        "levels": LEVEL_NAMES[:depth],
        "starting_lord": start_lord,
        "starting_lord_name": _NAME[start_lord],
        "balance_years": balance_years,
        "balance_at_birth": _fmt_ymd(balance_years, year_days),
        "mahadashas": [_strip_jd(m) for m in mahas],
    }


def _fmt_ymd(years: float, year_days: float) -> str:
    """Years as 'Ny Mm Dd' — the traditional balance format.

    Months are `year_days / 12`, so with the 360-day sāvana year a month is
    exactly 30 days (matching BPHS's ghaṭi/pala worked example).
    """
    month_days = year_days / 12.0
    total_days = years * year_days
    y = int(total_days // year_days)
    rem = total_days - y * year_days
    m = int(rem // month_days)
    d = int(round(rem - m * month_days))
    return f"{y}y {m}m {d}d"


def _strip_jd(node: DashaPeriod) -> dict:
    """Serialize, keeping the ISO strings but dropping raw JD from the payload."""
    d = asdict(node)
    d.pop("start_jd", None)
    d.pop("end_jd", None)
    d["sub"] = [_strip_jd(s) for s in node.sub]
    # asdict already recursed; rebuild sub cleanly to also strip nested jd
    return d
