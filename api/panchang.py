"""Pañcāṅga — the five limbs of the Vedic almanac (tithi · vāra · nakṣatra · yoga ·
karaṇa) for a given civil date at a given place, plus the day's auspicious and
inauspicious time-windows.

All astronomy reuses the SAME sidereal (Lahiri) engine as the birth chart:
``vedic`` for Sun/Moon longitudes and ``shadbala_context._sun_events`` for the
sunrise/sunset that bound the Hindu day. Longitudes are nirayaṇa; the tithi
elongation is ayanāṁśa-independent by construction.

Definitions are the standard almanac reckonings (Sūrya-Siddhānta lunar model);
the day-windows follow the muhūrta convention (see docs — Muhūrta Cintāmaṇi).
Nothing here is a fated verdict: a pañcāṅga states the qualities of the *day*,
which the chart-tailored scoring in :mod:`panchang_score` then reads against a
specific horoscope.
"""
from __future__ import annotations

import datetime as _dt
from zoneinfo import ZoneInfo

import swisseph as swe

import vedic
from vedic import CALC_FLAGS, NAKSHATRA_ARC, _configure_thread, _norm360, _nakshatra_of
from shadbala_context import _sun_events, ShadbalaUnavailable

# ── static tables ───────────────────────────────────────────────────────────
# 15 tithi names (repeated each pakṣa; the 15th is Pūrṇimā in śukla, Amāvāsyā in kṛṣṇa)
_TITHI = ["Pratipadā", "Dvitīyā", "Tṛtīyā", "Caturthī", "Pañcamī", "Ṣaṣṭhī",
          "Saptamī", "Aṣṭamī", "Navamī", "Daśamī", "Ekādaśī", "Dvādaśī",
          "Trayodaśī", "Caturdaśī", "Pūrṇimā"]
# Nanda(1/6/11) Bhadrā(2/7/12) Jayā(3/8/13) Riktā(4/9/14) Pūrṇā(5/10/15) groups.
_TITHI_GROUP = ["Nandā", "Bhadrā", "Jayā", "Riktā", "Pūrṇā"]

_YOGA = ["Viṣkambha", "Prīti", "Āyuṣmān", "Saubhāgya", "Śobhana", "Atigaṇḍa",
         "Sukarmā", "Dhṛti", "Śūla", "Gaṇḍa", "Vṛddhi", "Dhruva", "Vyāghāta",
         "Harṣaṇa", "Vajra", "Siddhi", "Vyatīpāta", "Varīyān", "Parigha",
         "Śiva", "Siddha", "Sādhya", "Śubha", "Śukla", "Brahmā", "Indra", "Vaidhṛti"]
# The malefic yogas (avoid for muhūrta).
_YOGA_BAD = {0, 5, 8, 9, 12, 14, 16, 18, 26}  # Viṣkambha Atigaṇḍa Śūla Gaṇḍa Vyāghāta Vajra Vyatīpāta Parigha Vaidhṛti

_KARANA_MOV = ["Bava", "Bālava", "Kaulava", "Taitila", "Gara", "Vaṇija", "Viṣṭi"]
_KARANA_FIX = {1: "Kiṁstughna", 58: "Śakuni", 59: "Catuṣpada", 60: "Nāga"}
_KARANA_BAD = {"Viṣṭi", "Śakuni", "Catuṣpada", "Nāga", "Kiṁstughna"}  # Viṣṭi = Bhadrā

# Nakṣatra lords — the Viṁśottarī cycle from Aśvinī (Ketu … Mercury), repeating.
_NAK_LORD = ["ketu", "venus", "sun", "moon", "mars", "rahu", "jupiter", "saturn", "mercury"]

# vāra: index = ISO weekday%7 with Sunday=0. name, iast, graha lord.
_VARA = [("Ravivāra", "sun"), ("Somavāra", "moon"), ("Maṅgalavāra", "mars"),
         ("Budhavāra", "mercury"), ("Guruvāra", "jupiter"), ("Śukravāra", "venus"),
         ("Śanivāra", "saturn")]

# ── Devanāgarī parallels (served alongside IAST for Hindi mode) ──────────────
_TITHI_HI = ["प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पञ्चमी", "षष्ठी", "सप्तमी",
             "अष्टमी", "नवमी", "दशमी", "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा"]
_YOGA_HI = ["विष्कम्भ", "प्रीति", "आयुष्मान्", "सौभाग्य", "शोभन", "अतिगण्ड", "सुकर्मा",
            "धृति", "शूल", "गण्ड", "वृद्धि", "ध्रुव", "व्याघात", "हर्षण", "वज्र", "सिद्धि",
            "व्यतीपात", "वरीयान्", "परिघ", "शिव", "सिद्ध", "साध्य", "शुभ", "शुक्ल",
            "ब्रह्मा", "इन्द्र", "वैधृति"]
_VARA_HI = ["रविवार", "सोमवार", "मङ्गलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार"]
_NAK_HI = ["अश्विनी", "भरणी", "कृत्तिका", "रोहिणी", "मृगशिरा", "आर्द्रा", "पुनर्वसु", "पुष्य",
           "आश्लेषा", "मघा", "पूर्वाफाल्गुनी", "उत्तराफाल्गुनी", "हस्त", "चित्रा", "स्वाति",
           "विशाखा", "अनुराधा", "ज्येष्ठा", "मूल", "पूर्वाषाढा", "उत्तराषाढा", "श्रवण",
           "धनिष्ठा", "शतभिषा", "पूर्वाभाद्रपदा", "उत्तराभाद्रपदा", "रेवती"]
_KARANA_HI = {"Bava": "बव", "Bālava": "बालव", "Kaulava": "कौलव", "Taitila": "तैतिल",
              "Gara": "गर", "Vaṇija": "वणिज", "Viṣṭi": "विष्टि", "Kiṁstughna": "किंस्तुघ्न",
              "Śakuni": "शकुनि", "Catuṣpada": "चतुष्पद", "Nāga": "नाग"}

# Which 1/8th of the daytime each inauspicious window falls in, by weekday (Sun=0).
_RAHU = [8, 2, 7, 5, 6, 4, 3]        # rāhu-kāla part (1-8)
_YAMA = [5, 4, 3, 2, 1, 7, 6]        # yama-gaṇḍa
_GULIKA = [7, 6, 5, 4, 3, 2, 1]      # gulika / māndi


def _lon(jd: float, ipl: int) -> float:
    vals, rf = swe.calc_ut(jd, ipl, CALC_FLAGS)
    if rf < 0:
        raise RuntimeError(f"swisseph failed (ipl {ipl}): flag {rf}")
    return _norm360(vals[0])


def _jd_local_noon(date: _dt.date, tz: ZoneInfo) -> tuple[float, float]:
    """JD(UT) of ~local noon on `date`, and the local UTC offset (hours)."""
    aware = _dt.datetime(date.year, date.month, date.day, 12, 0, tzinfo=tz)
    off = aware.utcoffset().total_seconds() / 3600.0
    u = aware.astimezone(ZoneInfo("UTC"))
    return swe.julday(u.year, u.month, u.day, u.hour + u.minute / 60.0, swe.GREG_CAL), off


def _hhmm(jd_ut: float, off: float) -> str:
    """A JD(UT) instant → local 'HH:MM' clock string."""
    y, mo, d, h = swe.revjul(jd_ut + off / 24.0, swe.GREG_CAL)
    total = int(round(h * 60))
    return "%02d:%02d" % ((total // 60) % 24, total % 60)


def _local_dt(jd_ut: float, off: float) -> str:
    """A JD(UT) instant → local 'YYYY-MM-DD HH:MM' (fixed day-offset; sub-day DST
    shifts are immaterial here). Built via timedelta so 23:59.6 rolls the date."""
    y, mo, d, hf = swe.revjul(jd_ut, swe.GREG_CAL)
    loc = _dt.datetime(y, mo, d) + _dt.timedelta(hours=hf + off)
    return loc.strftime("%Y-%m-%d %H:%M")


def _span_at_sunrise(jd_sunrise: float, ipl_a: int, ipl_b: int, arc: float,
                     count: int) -> tuple[int, float]:
    """Return (index 0..count-1, fraction elapsed) of a limb defined by the
    (lonA − lonB) elongation (or lonA alone if ipl_b is None) at sunrise."""
    a = _lon(jd_sunrise, ipl_a)
    val = a if ipl_b is None else _norm360(a - _lon(jd_sunrise, ipl_b))
    idx = int(val // arc)
    return min(idx, count - 1), (val - idx * arc) / arc


def _karana_name(tithi_idx: int, tithi_frac: float) -> tuple[str, bool]:
    """Karaṇa = half-tithi. 60 half-tithis over the lunar month → 11 karaṇas."""
    half = tithi_idx * 2 + (0 if tithi_frac < 0.5 else 1)  # 0..59
    n = half + 1                                            # 1..60
    if n in _KARANA_FIX:
        name = _KARANA_FIX[n]
    else:
        name = _KARANA_MOV[(n - 2) % 7]
    return name, name in _KARANA_BAD


def _windows(jd_rise: float, jd_set: float, jd_next_rise: float, weekday: int,
             off: float) -> dict:
    """The muhūrta day-windows. Daytime is split into 8 equal parts for
    rāhu/yama/gulika; the 15-muhūrta scheme gives abhijit and brahma."""
    day = jd_set - jd_rise
    night = jd_next_rise - jd_set
    part = day / 8.0

    def eighth(n):  # 1-based part of the day
        s = jd_rise + (n - 1) * part
        return {"start": _hhmm(s, off), "end": _hhmm(s + part, off)}

    # Abhijit = the 8th of 15 daytime muhūrtas (midday). Void on Wednesday.
    m = day / 15.0
    abhijit = None if weekday == 3 else {
        "start": _hhmm(jd_rise + 7 * m, off), "end": _hhmm(jd_rise + 8 * m, off)}
    # Brahma muhūrta = the 14th of 15 night-muhūrtas (2nd-last before sunrise).
    nm = night / 15.0
    brahma = {"start": _hhmm(jd_next_rise - 2 * nm, off),
              "end": _hhmm(jd_next_rise - 1 * nm, off)}
    return {
        "rahu_kala": eighth(_RAHU[weekday]),
        "yama_ganda": eighth(_YAMA[weekday]),
        "gulika_kala": eighth(_GULIKA[weekday]),
        "abhijit": abhijit,
        "brahma_muhurta": brahma,
        "day_span": {"sunrise": _hhmm(jd_rise, off), "sunset": _hhmm(jd_set, off)},
    }


def panchanga(date: _dt.date, latitude: float, longitude: float, tz_name: str) -> dict:
    """The pañcāṅga for `date` at (latitude, longitude, tz_name). Computed at the
    day's sunrise, the start of the Hindu day. Raises ShadbalaUnavailable at
    latitudes where the Sun does not rise/set on the date."""
    _configure_thread()
    ok, detail = vedic.ephemeris_status()
    if not ok:
        raise RuntimeError(f"swisseph not configured for a sidereal pañcāṅga: {detail}")

    tz = ZoneInfo(tz_name)
    jd_noon, off = _jd_local_noon(date, tz)
    geopos = (longitude, latitude, 0.0)
    jd_rise, jd_set, jd_next = _sun_events(jd_noon, geopos)

    # Moonrise after sunset — the reference instant for the moonrise vratas
    # (Saṅkaṣṭī Caturthī, Karva Chauth). None where the Moon does not rise.
    try:
        m_ret, m_t = swe.rise_trans(jd_set, swe.MOON, swe.CALC_RISE | swe.BIT_DISC_CENTER, geopos)
        jd_moonrise = m_t[0] if (m_ret >= 0 and m_t and m_t[0]) else None
    except Exception:  # noqa: BLE001
        jd_moonrise = None

    # Five limbs at sunrise.
    ti_idx, ti_frac = _span_at_sunrise(jd_rise, swe.MOON, swe.SUN, 12.0, 30)
    paksha = "śukla" if ti_idx < 15 else "kṛṣṇa"
    ti_in_paksha = ti_idx % 15                       # 0..14
    ti_name = _TITHI[ti_in_paksha]
    ti_name_hi = _TITHI_HI[ti_in_paksha]
    if ti_in_paksha == 14:
        ti_name = "Pūrṇimā" if paksha == "śukla" else "Amāvāsyā"
        ti_name_hi = "पूर्णिमा" if paksha == "śukla" else "अमावस्या"
    yo_idx, yo_frac = _span_at_sunrise(jd_rise, swe.SUN, swe.MOON, NAKSHATRA_ARC, 27)
    # yoga uses the SUM; _span_at_sunrise subtracts, so recompute the sum here.
    moon_lon = _lon(jd_rise, swe.MOON)
    yo_val = _norm360(_lon(jd_rise, swe.SUN) + moon_lon)
    yo_idx = min(int(yo_val // NAKSHATRA_ARC), 26)
    nak = _nakshatra_of(moon_lon)
    kar_name, kar_bad = _karana_name(ti_idx, ti_frac)
    # Exact interval of the sunrise tithi, for display (dṛk-almanac parity).
    ti_start, ti_end, _ = tithi_start_end(jd_rise)

    # vāra from the sunrise's local civil date.
    rise_local = swe.revjul(jd_rise + off / 24.0, swe.GREG_CAL)
    wd = _dt.date(int(rise_local[0]), int(rise_local[1]), int(rise_local[2])).isoweekday() % 7
    vara_name, vara_lord = _VARA[wd]

    return {
        "date": date.isoformat(),
        "_moon_sign": int(moon_lon // 30),   # 0-11, for chart-tailored scoring
        # Sunrise/sunset/next-sunrise + moonrise JD(UT), private for the festival
        "_jd_rise": jd_rise, "_jd_set": jd_set, "_jd_next": jd_next,  # kāla matcher
        "_jd_moonrise": jd_moonrise,
        "tithi": {"index": ti_idx + 1, "name": ti_name, "name_hi": ti_name_hi, "paksha": paksha,
                  "number_in_paksha": ti_in_paksha + 1,
                  "group": _TITHI_GROUP[ti_in_paksha % 5], "elapsed": round(ti_frac, 3),
                  "start": _local_dt(ti_start, off), "end": _local_dt(ti_end, off)},
        "vara": {"index": wd, "name": vara_name, "name_hi": _VARA_HI[wd], "lord": vara_lord},
        "nakshatra": {"index": nak.index, "name": nak.name_iast, "name_hi": _NAK_HI[nak.index - 1],
                      "pada": nak.pada, "lord": _NAK_LORD[(nak.index - 1) % 9],
                      "elapsed": round(nak.fraction, 3)},
        "yoga": {"index": yo_idx + 1, "name": _YOGA[yo_idx], "name_hi": _YOGA_HI[yo_idx],
                 "auspicious": yo_idx not in _YOGA_BAD},
        "karana": {"name": kar_name, "name_hi": _KARANA_HI.get(kar_name, kar_name),
                   "auspicious": not kar_bad},
        "windows": _windows(jd_rise, jd_set, jd_next, wd, off),
        "note": ("Pañcāṅga computed at sunrise (sidereal/Lahiri). The five limbs and "
                 "the day-windows describe the day itself; they are not a verdict on "
                 "any person."),
    }


# ── exact tithi times + kāla windows (festival vyāpti matching) ──────────────
# A festival is a (māsa, pakṣa, tithi) that must PREVAIL during a particular
# period of the day — sunrise for most, pradoṣa / niśīta / aparāhṇa / madhyāhna /
# pūrvāhṇa / moonrise for others. We compute the tithi to the second (its exact
# elongation-crossing interval) and test whether it OVERLAPS the required window,
# then apply the observance's tie-break — the dṛg-gaṇita rule a dṛk almanac uses,
# rather than sampling the tithi at one instant.

def _elong_rate(jd: float) -> tuple[float, float]:
    """(elongation 0..360, its rate in deg/day) — Moon minus Sun, using speeds."""
    m, rf = swe.calc_ut(jd, swe.MOON, CALC_FLAGS)
    s, rf2 = swe.calc_ut(jd, swe.SUN, CALC_FLAGS)
    if rf < 0 or rf2 < 0:
        raise RuntimeError("swisseph failed computing elongation rate")
    return _norm360(m[0] - s[0]), (m[3] - s[3])


def _cross_time(jd_guess: float, target_deg: float) -> float:
    """Instant near jd_guess where the elongation equals target_deg (mod 360),
    by Newton with the true (variable) rate — converges to well under a second."""
    jd = jd_guess
    for _ in range(60):
        e, rate = _elong_rate(jd)
        d = ((e - target_deg + 180.0) % 360.0) - 180.0   # signed, 0 at target
        if abs(d) < 1e-8 or rate == 0:
            break
        jd -= d / rate
    return jd


def tithi_start_end(jd: float) -> tuple[float, float, int]:
    """(start_jd, end_jd, index 0..29) of the tithi live at `jd` — the exact
    elongation crossings of the two bounding 12° multiples."""
    e, rate = _elong_rate(jd)
    k = int(e // 12.0)
    start = _cross_time(jd - (e - 12.0 * k) / rate, (12.0 * k) % 360.0)
    end = _cross_time(jd + (12.0 * (k + 1) - e) / rate, (12.0 * (k + 1)) % 360.0)
    return start, end, k


def tithi_pk_num_at(jd: float) -> tuple[str, int]:
    """(pakṣa, number-in-pakṣa 1..15) of the tithi live at instant `jd`."""
    idx = int(_norm360(_lon(jd, swe.MOON) - _lon(jd, swe.SUN)) // 12.0)  # 0..29
    return ("shukla" if idx < 15 else "krishna"), (idx % 15) + 1


def kala_window(pan: dict, kala: str) -> tuple[float, float]:
    """(start_jd, end_jd) of a named kāla for the day in `pan` (which carries the
    private ``_jd_rise/_jd_set/_jd_next`` and, for moonrise, ``_jd_moonrise``).

    Two kinds. A festival "vyāpinī at" a wide day-part is judged at that part's
    MOMENT — solar noon (madhyāhna), mid-afternoon (aparāhṇa), mid-forenoon
    (pūrvāhṇa) — returned as a zero-width point; testing an instant, not a
    2½-hour span, stops a tithi that only clips the span's edge from claiming the
    wrong day. The short windows are real intervals: pradoṣa (the first 3 night
    muhūrtas after sunset) and niśīta (the 8th night muhūrta, straddling solar
    midnight) — the festival counts if the tithi covers any of them. Sunrise /
    sunset / moonrise are points. Daytime is split into five parts; night into
    fifteen muhūrtas."""
    r, s, n = pan["_jd_rise"], pan["_jd_set"], pan["_jd_next"]
    day, night = s - r, n - s
    if kala == "pradosha":  return (s, s + 3.0 * night / 15.0)   # interval: dusk
    if kala == "nishita":   return (s + 7.0 * night / 15.0, s + 8.0 * night / 15.0)  # 8th night muhūrta
    if kala == "madhyahna": return (r + day / 2.0,) * 2          # solar noon
    if kala == "aparahna":  return (r + 0.70 * day,) * 2         # mid-afternoon
    if kala == "purvahna":  return (r + 0.30 * day,) * 2         # mid-forenoon
    if kala == "sunset":    return (s, s)
    if kala == "moonrise":
        m = pan.get("_jd_moonrise")
        return (m, m) if m else (s, s + 3.0 * night / 15.0)      # no moonrise → dusk
    return (r, r)            # "sunrise"
