"""
Production wiring for the Ṣaḍbala engine: turn a computed chart into the birth
context every bala needs, then assemble the six-fold strength.

``shadbala.py`` holds the pure, unit-validated formulas. This module supplies
their real-world inputs from swisseph and the civil calendar — declinations
(Ayana), the Ascendant/Midheaven (Dig), apparent solar time (Nathonnatha),
sunrise/sunset (Thribhāga, Horā), the weekday (Vāra), the ahargana (Abda, Masa),
and the secular mean longitudes (Cheṣṭā). The chart's own sidereal longitudes
feed Sthāna, Dṛk and Pakṣa.

Two provenance caveats, surfaced to the reader in the API payload:
  • Cheṣṭā uses modern secular mean longitudes (Meeus), not Raman's 1900-era
    Book-of-Fate tables. The kendra is a *difference* of longitudes, so it is
    ayanāṁśa-independent; for the outer grahas it reproduces Raman to ≤0.7
    virūpa, and for Mercury it is deliberately more accurate than his table.
  • Ayana uses swisseph's true declination (real obliquity + latitude) rather
    than Raman's flat 24°/β=0 increment table.
"""
from __future__ import annotations

import math
from datetime import date, datetime

import swisseph as swe

import shadbala
import vedic

# Raman computes kranti (declination) from the SĀYANA longitude alone, ignoring
# ecliptic latitude (β=0), with a flat 24° obliquity (Art. 72). We reproduce that
# exactly from swisseph's tropical longitude — matching his Moon/Mercury values,
# where the true (latitude-bearing) declination would diverge by up to 5°.
_OBLIQUITY_DEG = 24.0
_SIN_OBL = math.sin(math.radians(_OBLIQUITY_DEG))


def _beta0_declination(jd_ut: float, ipl: int) -> float:
    """Signed declination (North + / South −) from the tropical longitude, β=0."""
    trop_long = swe.calc_ut(jd_ut, ipl, swe.FLG_SWIEPH)[0][0]   # tropical, of date
    return math.degrees(math.asin(_SIN_OBL * math.sin(math.radians(trop_long))))

_IPL = {
    "sun": swe.SUN, "moon": swe.MOON, "mars": swe.MARS, "mercury": swe.MERCURY,
    "jupiter": swe.JUPITER, "venus": swe.VENUS, "saturn": swe.SATURN,
}

# Meeus mean longitudes (of-date, tropical, degrees), linear term; T = Julian
# centuries from J2000. Heliocentric for each planet; Earth's + 180 = mean Sun.
_MEAN_LON = {
    "mercury": (252.250906, 149474.0722491),
    "venus": (181.979801, 58519.2130302),
    "earth": (100.466449, 36000.7698231),
    "mars": (355.433275, 19141.6964746),
    "jupiter": (34.351484, 3036.3027889),
    "saturn": (50.077471, 1223.5110141),
}

# Raman's condensed-ahargana epoch: Wednesday, 2 May 1827.
_AHARGANA_EPOCH = date(1827, 5, 2)
_EPOCH_WEEKDAY = 3           # Wednesday (0 = Sunday)
# Calibration so the epoch day itself is ahargana 1 (inclusive count), which
# makes Vāra reproduce the true birth weekday and Abda/Masa match Raman's Ex.24–25.
_AHARGANA_OFFSET = 1


def _ut_hours(jd_ut: float) -> float:
    """UT clock hours of a Julian Day (JD .5 = midnight)."""
    return ((jd_ut - 0.5) % 1.0) * 24.0


def _time_equ_days(jd_ut: float) -> float:
    e = swe.time_equ(jd_ut)
    return e[1] if isinstance(e, (tuple, list)) else e


def _mean_longitudes_sidereal(jd_ut: float, ayanamsa: float) -> dict[str, float]:
    T = (jd_ut - 2451545.0) / 36525.0
    return {k: (a + b * T - ayanamsa) % 360.0 for k, (a, b) in _MEAN_LON.items()}


class ShadbalaUnavailable(ValueError):
    """Ṣaḍbala cannot be computed for this birth — e.g. the Sun neither rises nor
    sets (a polar day/night), so Kāla bala's sunrise-based components (day/night,
    thribhāga, horā) are undefined. The chart itself is unaffected; the caller
    degrades this to an error row."""


def _rise_or_set(tjd: float, flag: int, geopos: tuple[float, float, float]) -> float:
    ret, tret = swe.rise_trans(tjd, swe.SUN, flag, geopos)
    if ret < 0 or not tret or not tret[0]:   # retflag −2 / JD 0.0 = no such event
        raise ShadbalaUnavailable(
            "the Sun does not rise and set on the birth date at this latitude "
            "(circumpolar); Kāla bala's day/night, thribhāga and horā are undefined")
    return tret[0]


def _sun_events(jd_ut: float, geopos: tuple[float, float, float]) -> tuple[float, float, float]:
    """(sunrise, sunset, next_sunrise) in JD(UT), with sunrise ≤ birth < next.
    Raises ShadbalaUnavailable rather than looping or trusting a null event."""
    rise = swe.CALC_RISE | swe.BIT_DISC_CENTER
    sett = swe.CALC_SET | swe.BIT_DISC_CENTER
    s = _rise_or_set(jd_ut - 1.2, rise, geopos)
    nxt = s
    for _ in range(4):                       # bounded — at most a couple of days
        nxt = _rise_or_set(s + 0.5, rise, geopos)
        if nxt > jd_ut:
            break
        s = nxt
    else:
        raise ShadbalaUnavailable("could not bracket the birth between two sunrises")
    return s, _rise_or_set(s, sett, geopos), nxt


def build_context(jd_ut: float, latitude: float, longitude_east: float,
                  local_dt: datetime, positions_sidereal: dict[str, float],
                  ayanamsa_value: float) -> dict:
    """All the non-longitude inputs the six balas need, computed from swisseph
    and the civil calendar. Returns a dict ready to hand to :func:`assemble`."""
    vedic._configure_thread()

    # Kranti (β=0, 24° obliquity) per Raman, from each graha's tropical longitude.
    declinations = {g: _beta0_declination(jd_ut, ipl) for g, ipl in _IPL.items()}

    # True Ascendant and Midheaven (the physical angles; whole-sign house choice
    # does not move them).
    _, ascmc = swe.houses_ex(jd_ut, latitude, longitude_east, b"W", swe.FLG_SIDEREAL)
    asc_long, mc_long = ascmc[0], ascmc[1]

    # Apparent solar time from local apparent midnight.
    lmt = _ut_hours(jd_ut) + longitude_east / 15.0
    hours_from_apparent_midnight = (lmt + _time_equ_days(jd_ut) * 24.0) % 24.0

    # Sun events → day/night, thribhāga third, horā number. _sun_events()
    # guarantees sunrise ≤ birth < next_sunrise, so the horā is simply the fixed
    # clock-hour count from that sunrise (1-based), day or night alike.
    geopos = (longitude_east, latitude, 0.0)
    sunrise, sunset, next_sunrise = _sun_events(jd_ut, geopos)
    is_day = sunrise <= jd_ut < sunset
    if is_day:
        frac = (jd_ut - sunrise) / (sunset - sunrise)
    else:                                       # between sunset and next sunrise
        frac = (jd_ut - sunset) / (next_sunrise - sunset)
    third_index = min(2, max(0, int(frac * 3)))
    hora_number = int((jd_ut - sunrise) * 24.0) + 1

    # Vāra weekday & ahargana. The Hindu day begins at the anchor sunrise, so we
    # take that sunrise's CIVIL (local) date. The zone offset is read from the
    # birth itself (JD of the civil wall-clock minus jd_ut), so we never mix the
    # civil clock with local mean solar time — a pre-sunrise birth rolls back to
    # the previous day exactly as is_day / hora_number already do.
    jd_local_naive = swe.julday(
        local_dt.year, local_dt.month, local_dt.day,
        local_dt.hour + local_dt.minute / 60.0 + local_dt.second / 3600.0, swe.GREG_CAL)
    offset_days = jd_local_naive - jd_ut
    y, m, d, _h = swe.revjul(sunrise + offset_days, swe.GREG_CAL)
    hindu_date = date(int(y), int(m), int(d))
    weekday = (hindu_date.weekday() + 1) % 7          # Python Mon=0 → our Sun=0
    ahargana = (hindu_date - _AHARGANA_EPOCH).days + _AHARGANA_OFFSET

    # Cheṣṭā mean elements (secular, sidereal).
    mean_sid = _mean_longitudes_sidereal(jd_ut, ayanamsa_value)
    mean_sun = (mean_sid["earth"] + 180.0) % 360.0
    cheshta_true = {g: positions_sidereal[g] for g in shadbala.CHESHTA_GRAHAS}
    cheshta_mean, cheshta_sig = {}, {}
    for g in shadbala.CHESHTA_GRAHAS:
        if g in ("mars", "jupiter", "saturn"):
            cheshta_mean[g], cheshta_sig[g] = mean_sid[g], mean_sun
        else:                                   # mercury, venus
            cheshta_mean[g], cheshta_sig[g] = mean_sun, mean_sid[g]

    return {
        "positions": positions_sidereal,
        "asc_long": asc_long, "mc_long": mc_long,
        "declinations": declinations,
        "hours_from_apparent_midnight": hours_from_apparent_midnight,
        "is_day": is_day, "thribhaga_third": third_index,
        "weekday": weekday, "ahargana": ahargana, "hora_number": hora_number,
        "cheshta_true": cheshta_true, "cheshta_mean": cheshta_mean,
        "cheshta_sig": cheshta_sig,
        "epoch_weekday": _EPOCH_WEEKDAY,
    }


def assemble_from_context(ctx: dict, lagna_rasi: int) -> dict:
    """Run every bala over a context from :func:`build_context` and return the
    full Ṣaḍbala table with the strong/weak verdict."""
    pos = ctx["positions"]
    sthana = shadbala.sthana_bala(pos, lagna_rasi)
    dik = shadbala.dig_bala(pos, ctx["asc_long"], ctx["mc_long"])
    kala = shadbala.kala_bala(
        pos, hours_from_apparent_midnight=ctx["hours_from_apparent_midnight"],
        is_day=ctx["is_day"], thribhaga_third=ctx["thribhaga_third"],
        weekday=ctx["weekday"], ahargana=ctx["ahargana"],
        hora_number=ctx["hora_number"], declinations=ctx["declinations"],
        epoch_weekday=ctx["epoch_weekday"],
        sthana_total={g: sthana[g]["total"] for g in sthana}, dik=dik,
    )
    cheshta = shadbala.cheshta_bala(ctx["cheshta_true"], ctx["cheshta_mean"], ctx["cheshta_sig"])
    naisargika = shadbala.naisargika_bala()
    drik = shadbala.drik_bala(pos)
    table = shadbala.assemble(sthana, dik, kala["totals"], cheshta, naisargika, drik)
    return {
        "grahas": table,
        "kala_components": kala["components"],
        "sthana_components": {g: {k: v for k, v in sthana[g].items() if k != "total"} for g in sthana},
    }


def shadbala_for_chart(chart: "vedic.VedicChart") -> dict:
    """Full Ṣaḍbala for a computed :class:`vedic.VedicChart`."""
    positions = {g.key: g.longitude for g in chart.grahas if g.key in _IPL}
    local_dt = datetime.strptime(chart.local_time, "%Y-%m-%d %H:%M:%S")
    ctx = build_context(chart.jd_ut, chart.latitude, chart.longitude,
                        local_dt, positions, chart.ayanamsa_value)
    result = assemble_from_context(ctx, chart.lagna_rasi)
    result["method"] = {
        "source": "B. V. Raman, Graha and Bhava Balas (Parāśara's Ṣaḍbala)",
        "unit": "virūpa (60 virūpa = 1 rūpa)",
        "cheshta_note": "modern secular mean longitudes (Meeus), not Raman's "
                        "Book-of-Fate tables; kendra is ayanāṁśa-independent",
        "ayana_note": "kranti from tropical longitude, β=0, 24° obliquity (Raman's method)",
        "validated": "reproduces Raman's Standard Horoscope to the virūpa per component",
    }
    return result
