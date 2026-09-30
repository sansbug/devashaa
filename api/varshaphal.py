"""Varṣaphala — the Tājika annual chart. Tier `tajika`.

The root text (Tājika-Nīlakaṇṭhī, Saxena tr.) and two modern treatments
(Charak; Raman) are on hand and registered; the calculation rules below cite
them. Nothing interpretive ships: the readings beside a Mudda period come from
this site's own projection engine and are labelled `synthesis`.

  * varṣa-praveśa — the Sun's return to its natal sidereal longitude
  * the varṣa kuṇḍalī, cast for that instant at the place given
  * Muntha — janma lagna + one sign per completed year (TN p.52-53)
  * the five office-bearers and the year-lord (TN p.50-52, Charak ch.VII)
  * pañcavargīya and harṣa balas (TN p.40-41, 87; Charak ch.VI)
  * Tājika dṛṣṭi, the sixteen yogas, the fifty sahams (tajika.py)
  * Mudda daśā — Charak ch.V: (completed years + janma nakṣatra − 2) mod 9
    picks the first lord; Viṁśottarī order; each lord years/120 of the solar
    year; the FIRST period is prorated by the un-traversed part of the janma
    nakṣatra and the remainder closes the year. Two variants ship: `prorated`
    (Charak) and `unprorated` (what some software does; it matches an
    independent implementation's boundaries to the day).
"""
from __future__ import annotations

import datetime as _dt
from zoneinfo import ZoneInfo

import swisseph as swe

import tajika
import vedic  # noqa: F401  (ephemeris + sidereal mode)
from vedic import compute_chart
from dignity import RASI_LORD
from vimshottari import _ORDER, _YEARS, _NAME, TOTAL_YEARS

TIER = "tajika"
CITATION = "Tājika-Nīlakaṇṭhī (Saxena tr., Ranjan); K.S. Charak, A Textbook of Varshaphala; B.V. Raman, Varshaphal"


def _nak_lord(nak_1based: int) -> str:
    return _ORDER[(nak_1based - 1) % 9]


def _sun_sidereal(jd: float) -> float:
    return swe.calc_ut(jd, swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]


def varsha_pravesha_jd(natal_sun: float, year: int, birth_month: int, birth_day: int) -> float:
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


def _day_or_night(jd: float, latitude: float, longitude: float) -> tuple[bool, dict]:
    """Day = between sunrise and the following sunset at the place (Charak p.51)."""
    geo = (longitude, latitude, 0.0)
    flag_r = swe.CALC_RISE | swe.BIT_DISC_CENTER
    flag_s = swe.CALC_SET | swe.BIT_DISC_CENTER
    rise = swe.rise_trans(jd - 1.2, swe.SUN, flag_r, geo)[1][0]
    for _ in range(4):
        nxt = swe.rise_trans(rise + 0.5, swe.SUN, flag_r, geo)[1][0]
        if nxt > jd:
            break
        rise = nxt
    sett = swe.rise_trans(rise, swe.SUN, flag_s, geo)[1][0]
    return (rise <= jd < sett), {"sunrise_jd": rise, "sunset_jd": sett}


def mudda_dasha(janma_nak_1based: int, age: int, start_jd: float, end_jd: float, tz_name: str,
                now_jd: float | None, frac_traversed: float, prorate: bool) -> dict:
    start_nak = ((janma_nak_1based + age - 1) % 27) + 1
    lord0 = _nak_lord(start_nak)
    seq = _ORDER[_ORDER.index(lord0):] + _ORDER[:_ORDER.index(lord0)]
    span = end_jd - start_jd
    full = {l: span * _YEARS[l] / TOTAL_YEARS for l in seq}
    if prorate:
        bal = 1.0 - frac_traversed
        segs = [(seq[0], full[seq[0]] * bal, "balance")] + [(l, full[l], "full") for l in seq[1:]] \
               + [(seq[0], full[seq[0]] * frac_traversed, "remainder")]
    else:
        segs = [(l, full[l], "full") for l in seq]
    periods, cursor = [], start_jd
    for lord, days, kind in segs:
        if days <= 1e-9:
            continue
        s, e = cursor, cursor + days
        periods.append({"lord": lord, "lord_name": _NAME[lord], "kind": kind,
                        "start": _fmt(_jd_to_local(s, tz_name)), "end": _fmt(_jd_to_local(e, tz_name)),
                        "start_jd": s, "end_jd": e, "days": round(days, 2),
                        "is_current": bool(now_jd is not None and s <= now_jd < e)})
        cursor = e
    return {"start_nakshatra": start_nak, "start_lord": lord0, "prorated": prorate,
            "balance_fraction": round(1.0 - frac_traversed, 4), "year_days": round(span, 4), "periods": periods}


def build(natal, year: int | None, latitude: float, longitude: float, tz_name: str,
          now_jd: float, birth_local: _dt.datetime) -> dict:
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
    age = year - by

    local0 = _jd_to_local(jd0, tz_name)
    chart = compute_chart(local_dt=local0.replace(tzinfo=None), latitude=latitude,
                          longitude=longitude, tz_name=tz_name, name="")
    cd = chart.to_dict()
    is_day, sun_ev = _day_or_night(jd0, latitude, longitude)

    v_lagna = chart.lagna_rasi
    muntha_sign = (natal.lagna_rasi + age) % 12
    ctx = tajika.Ctx(cd["grahas"], cd["lagna_longitude"], is_day)
    pv = tajika.pancha_vargiya(ctx)
    harsha = tajika.harsha_bala(ctx)
    bearers = tajika.office_bearers(ctx, muntha_sign, natal.lagna_rasi)
    vlord = tajika.varshesha(ctx, pv, bearers)
    drishti = tajika.drishti_matrix(ctx)
    yog = tajika.yogas(ctx, pv)
    try:
        rasimana = tajika.rasimana_palas(jd0, latitude, longitude)
    except Exception:  # noqa: BLE001
        rasimana = None
    sah = tajika.sahams(ctx, pv, harsha, vlord["lord"], jd0, rasimana)
    for s in sah:
        if s.get("timing"):
            s["timing"]["date"] = _fmt(_jd_to_local(s["timing"]["jd"], tz_name))[:10]

    janma_moon = next(g for g in natal.grahas if g.key == "moon")
    mud_pro = mudda_dasha(janma_moon.nakshatra.index, age, jd0, jd1, tz_name, now_jd,
                          janma_moon.nakshatra.fraction, prorate=True)
    mud_un = mudda_dasha(janma_moon.nakshatra.index, age, jd0, jd1, tz_name, now_jd,
                         janma_moon.nakshatra.fraction, prorate=False)

    return {
        "tier": TIER, "citation": CITATION,
        "year": year, "age": age, "is_day": is_day,
        "pravesha": {
            "jd_ut": jd0, "local": _fmt(local0), "timezone": tz_name,
            "utc": _fmt(_jd_to_local(jd0, "UTC")),
            "next_local": _fmt(_jd_to_local(jd1, tz_name)),
            "sunrise_local": _fmt(_jd_to_local(sun_ev["sunrise_jd"], tz_name)),
            "sunset_local": _fmt(_jd_to_local(sun_ev["sunset_jd"], tz_name)),
            "place": {"latitude": latitude, "longitude": longitude},
            "note": "the Sun's return to its natal sidereal longitude, cast for the place given",
        },
        "chart": {k: cd[k] for k in ("grahas", "lagna_rasi", "lagna_longitude", "lagna_nakshatra",
                                     "ayanamsa", "ayanamsa_value") if k in cd},
        "varsha_lagna": {"sign": v_lagna, "lord": RASI_LORD[v_lagna]},
        "muntha": {"sign": muntha_sign, "lord": RASI_LORD[muntha_sign],
                   "house_from_varsha_lagna": (muntha_sign - v_lagna) % 12 + 1,
                   "house_from_janma_lagna": (muntha_sign - natal.lagna_rasi) % 12 + 1,
                   "rule": "janma lagna advanced one sign per completed year (TN p.52-53 śl. 166-168)"},
        "panchadhikari": bearers,
        "varshesha": vlord,
        "pancha_vargiya": {"grahas": pv, "units": tajika.PV_UNITS, "rule": "TN p.40-41 (śl. 41-44); Charak ch.VI"},
        "harsha": {"grahas": harsha, "sthana": tajika.HARSHA_STHANA, "rule": "TN p.87 (śl. 62-63); Charak ch.VI"},
        "drishti": drishti,
        "yogas": yog,
        "sahams": sah,
        "rasimana_palas": rasimana,
        "mudda": {
            "rule": ("first lord from (completed years + janma nakṣatra − 2) mod 9 → Sun, Moon, Mars, Rāhu, "
                     "Jupiter, Saturn, Mercury, Ketu, Venus (0 → Venus); Viṁśottarī order; each lord years/120 "
                     "of the solar year; the first period prorated by the un-traversed janma nakṣatra, the "
                     "remainder closing the year (Charak ch.V p.40-42)"),
            "default": "prorated",
            "variants": {"prorated": mud_pro, "unprorated": mud_un},
            "validation": ("prorated: reproduces Charak's Example Chart (Rāhu balance 38.61 d, test_tajika.py); "
                           "unprorated: all nine boundaries of this chart's 2026-27 year match an independent "
                           "implementation to the day (test_varshaphal.py)"),
            "note": "Rāhu and Ketu periods are shown; the texts give them no separate strength (Charak p.43, 75).",
        },
        "refused": [
            {"what": "any phala (prediction) sentence", "why": "cite-or-refuse: the texts' verdicts are not shipped as the native's fate"},
            {"what": "Patyāyinī and Yoginī daśās", "why": "stated (Charak ch.V) but not yet built"},
            {"what": "dvādaśavargīya bala", "why": "stated (TN p.42-45) but not yet built; pañcavargīya is the one the year-lord uses"},
        ],
        "note": ("Calculation only. Every figure carries its rule and its page. The readings beside each Mudda "
                 "period come from this site's own projection engine (synthesis tier), not from a Tājika text."),
    }
