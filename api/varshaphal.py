"""Varṣaphala — the Tājika annual chart. CALCULATION layer only.

Tier `tajika`. The root text, Nīlakaṇṭha's *Tājika-Nīlakaṇṭhī*, is NOT on hand,
so this module ships only what can be justified without it:

  * varṣa-praveśa — pure astronomy: the instant the Sun returns to its natal
    sidereal longitude in a given year. Checked against an independent
    implementation to 31 seconds (see test_reference_chart.py).
  * the varṣa kuṇḍalī — the ordinary chart cast for that instant.
  * Muntha — an identity: the janma lagna advanced one sign per completed
    year; its bhāva counted from the varṣa lagna. Checked (bhāva 3).
  * Mudda daśā — Viṁśottarī proportions laid over the solar year, starting
    from the lord of the nakṣatra reached by counting the completed years on
    from the janma nakṣatra. VALIDATED AGAINST AN INDEPENDENT IMPLEMENTATION
    (all nine boundaries of the 2026 year within a day), not yet against the
    text — `mudda.validation` says exactly that.

Everything interpretive is REFUSED and listed, with the reason, until the text
is registered in docs/classical-sources-policy.md:
  * varṣeśa (the year-lord) — needs the pañcavargīya bala and the hadda
    (term) table as the text states them;
  * the tri-rāśi and dina-rātri office-bearers — a stated table;
  * sahams — their day/night formulas;
  * the sixteen Tājika yogas (itthaśāla, īśarāpha, …) — stated orbs.

Nothing here predicts. The readings the site attaches to a Mudda period come
from its own projection engine (synthesis tier) and are labelled as such.
"""
from __future__ import annotations

import datetime as _dt
from zoneinfo import ZoneInfo

import swisseph as swe

import vedic
from vedic import compute_chart
from dignity import RASI_LORD
from vimshottari import _ORDER, _YEARS, _NAME, TOTAL_YEARS

TIER = "tajika"
CITATION = "Tājika-Nīlakaṇṭhī (source not on hand — calculation layer only)"

# Viṁśottarī nakṣatra lords, Aśvinī first: nakṣatra n (1-27) → lord index in the
# nine-fold cycle Ketu, Venus, Sun, Moon, Mars, Rāhu, Jupiter, Saturn, Mercury.
def _nak_lord(nak_1based: int) -> str:
    return _ORDER[(nak_1based - 1) % 9]


def _sun_sidereal(jd: float) -> float:
    return swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]


def varsha_pravesha_jd(natal_sun: float, year: int, birth_month: int, birth_day: int) -> float:
    """JD(UT) at which the Sun returns to `natal_sun` (sidereal) near the
    birthday in `year`. Newton on the Sun's mean daily motion; converges in a
    handful of steps to < 0.01 s."""
    day = min(birth_day, 28) if birth_month == 2 else birth_day
    jd = swe.julday(year, birth_month, day, 12.0, swe.GREG_CAL)
    for _ in range(40):
        diff = (_sun_sidereal(jd) - natal_sun + 180.0) % 360.0 - 180.0
        jd -= diff / 0.9856
        if abs(diff) < 1e-8:
            break
    return jd


def _jd_to_local(jd: float, tz_name: str) -> _dt.datetime:
    y, m, d, h = swe.revjul(jd, swe.GREG_CAL)
    ut = _dt.datetime(y, m, d, tzinfo=_dt.timezone.utc) + _dt.timedelta(hours=h)
    return ut.astimezone(ZoneInfo(tz_name))


def _fmt(dtv: _dt.datetime) -> str:
    return dtv.strftime("%Y-%m-%d %H:%M:%S")


def mudda_dasha(janma_nak_1based: int, age: int, start_jd: float, end_jd: float,
                tz_name: str, now_jd: float | None = None) -> dict:
    """Nine Viṁśottarī-proportioned periods over [start_jd, end_jd].

    Start lord = lord of nakṣatra ((janma + age − 1) mod 27) + 1, i.e. count the
    completed years on from the janma nakṣatra. Periods run in Viṁśottarī order
    from that lord, each years/120 of the solar year. The first period is NOT
    prorated (the independent implementation does not prorate; a text may)."""
    start_nak = ((janma_nak_1based + age - 1) % 27) + 1
    lord0 = _nak_lord(start_nak)
    seq = _ORDER[_ORDER.index(lord0):] + _ORDER[:_ORDER.index(lord0)]
    span = end_jd - start_jd
    periods, cursor = [], start_jd
    for lord in seq:
        days = span * _YEARS[lord] / TOTAL_YEARS
        s, e = cursor, cursor + days
        periods.append({
            "lord": lord, "lord_name": _NAME[lord],
            "start": _fmt(_jd_to_local(s, tz_name)), "end": _fmt(_jd_to_local(e, tz_name)),
            "start_jd": s, "end_jd": e, "days": round(days, 2),
            "is_current": bool(now_jd is not None and s <= now_jd < e),
        })
        cursor = e
    return {
        "rule": ("start lord = lord of nakṣatra ((janma nakṣatra + completed years − 1) mod 27) + 1; "
                 "then Viṁśottarī order, each lord's years/120 of the solar year; first period not prorated"),
        "start_nakshatra": start_nak, "start_lord": lord0,
        "year_days": round(span, 4),
        "periods": periods,
        "validation": ("validated against an independent implementation (AstroSage, report of 1 Jan 2026): "
                       "all nine boundaries of the 2026-27 year within one day — NOT yet against the text"),
    }


def build(natal, year: int | None, latitude: float, longitude: float, tz_name: str,
          now_jd: float, birth_local: _dt.datetime) -> dict:
    """The annual chart for `year` (default: the varṣa running now)."""
    natal_sun = next(g.longitude for g in natal.grahas if g.key == "sun")
    by, bm, bd = birth_local.year, birth_local.month, birth_local.day
    if year is None:
        y_now, _m, _d, _h = swe.revjul(now_jd, swe.GREG_CAL)
        year = y_now
        if varsha_pravesha_jd(natal_sun, year, bm, bd) > now_jd:
            year -= 1
    year = max(by, int(year))
    jd0 = varsha_pravesha_jd(natal_sun, year, bm, bd)
    jd1 = varsha_pravesha_jd(natal_sun, year + 1, bm, bd)
    age = year - by                         # completed years at this praveśa

    local0 = _jd_to_local(jd0, tz_name)
    chart = compute_chart(local_dt=local0.replace(tzinfo=None), latitude=latitude,
                          longitude=longitude, tz_name=tz_name, name="")
    cd = chart.to_dict()

    v_lagna = chart.lagna_rasi
    muntha_sign = (natal.lagna_rasi + age) % 12
    muntha = {
        "sign": muntha_sign, "lord": RASI_LORD[muntha_sign],
        "house_from_varsha_lagna": (muntha_sign - v_lagna) % 12 + 1,
        "house_from_janma_lagna": (muntha_sign - natal.lagna_rasi) % 12 + 1,
        "rule": "janma lagna advanced one sign per completed year",
    }
    janma_moon = next(g for g in natal.grahas if g.key == "moon")
    mudda = mudda_dasha(janma_moon.nakshatra.index, age, jd0, jd1, tz_name, now_jd)

    return {
        "tier": TIER, "citation": CITATION,
        "year": year, "age": age,
        "pravesha": {
            "jd_ut": jd0, "local": _fmt(local0), "timezone": tz_name,
            "utc": _fmt(_jd_to_local(jd0, "UTC")),
            "next_local": _fmt(_jd_to_local(jd1, tz_name)),
            "place": {"latitude": latitude, "longitude": longitude},
            "note": "the Sun's return to its natal sidereal longitude, cast for the place given",
        },
        "chart": {k: cd[k] for k in ("grahas", "lagna_rasi", "lagna_longitude", "lagna_nakshatra",
                                     "ayanamsa", "ayanamsa_value") if k in cd},
        "varsha_lagna": {"sign": v_lagna, "lord": RASI_LORD[v_lagna]},
        "muntha": muntha,
        "panchadhikari": {
            "muntha_lord": RASI_LORD[muntha_sign],
            "varsha_lagna_lord": RASI_LORD[v_lagna],
            "janma_lagna_lord": RASI_LORD[natal.lagna_rasi],
            "trirasi_lord": None, "dinaratri_lord": None,
            "note": "two of the five office-bearers need the text's table; the year-lord is not chosen",
        },
        "mudda": mudda,
        "refused": [
            {"what": "varṣeśa (year-lord)", "why": "needs the pañcavargīya bala and the hadda table as the text states them"},
            {"what": "tri-rāśi and dina-rātri lords", "why": "a stated table, not on hand"},
            {"what": "sahams", "why": "day/night formulas, not on hand"},
            {"what": "Tājika yogas (itthaśāla, īśarāpha, …)", "why": "stated orbs, not on hand"},
            {"what": "any phala (prediction) text", "why": "cite-or-refuse: no registered Tājika source"},
        ],
        "note": ("Calculation only. The varṣa chart, Muntha and Mudda periods are geometry; the readings "
                 "shown beside each period come from this site's own projection engine (synthesis tier), "
                 "not from a Tājika text."),
    }
