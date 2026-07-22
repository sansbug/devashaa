"""Jyotiṣa chart engine — sidereal (Lahiri), whole-sign bhāvas, nine grahas.

Doctrine follows BPHS (Parāśara / Santhanam). See docs/bphs-rules.md for the
śloka citation behind each rule.

Conventions fixed by the user 2026-07-16:
  - Ayanāṁśa   : Lahiri / Chitrapakṣa  (BPHS itself defines none)
  - Rāhu/Ketu  : MEAN node
  - Bhāvas     : whole sign (rāśi == bhāva)
"""

from __future__ import annotations

import os
import threading
from dataclasses import dataclass, asdict, field
from datetime import datetime
from zoneinfo import ZoneInfo

import swisseph as swe

from vargas import VARGAS, all_vargas

EPHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ephe")

_thread_state = threading.local()


def _configure_thread() -> None:
    """Apply the ephemeris path and sidereal mode to the CURRENT thread.

    swisseph holds both in THREAD-LOCAL storage. Configuring them once at import
    only ever reaches the importing thread — a Flask worker thread starts with
    neither, and swisseph does not complain: it quietly answers from the Moshier
    theory using the DEFAULT Fagan-Bradley ayanamsa. That yields a chart that is
    ~0.9° wrong and looks entirely plausible. So configure per thread, and let
    compute_chart() verify rather than assume.
    """
    if getattr(_thread_state, "configured", False):
        return
    swe.set_ephe_path(EPHE_DIR)
    swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)
    _thread_state.configured = True


_configure_thread()

# Sidereal, from the .se1 files, with speed for retrogression.
CALC_FLAGS = swe.FLG_SWIEPH | swe.FLG_SPEED | swe.FLG_SIDEREAL

# Names are carried in three systems and the client chooses. "common" is the
# ordinary English spelling people actually write (Chandra, Surya, Mesha);
# "iast" is the scholarly transliteration with diacritics (Candra, Sūrya, Meṣa);
# "en" is the plain English equivalent (Moon, Sun, Aries).
RASIS = [
    "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
    "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena",
]
RASIS_IAST = [
    "Meṣa", "Vṛṣabha", "Mithuna", "Karka", "Siṁha", "Kanyā",
    "Tulā", "Vṛścika", "Dhanu", "Makara", "Kumbha", "Mīna",
]
RASIS_EN = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces",
]
RASI_LORDS = [
    "Mangala", "Shukra", "Budha", "Chandra", "Surya", "Budha",
    "Shukra", "Mangala", "Guru", "Shani", "Shani", "Guru",
]
RASI_LORDS_IAST = [
    "Maṅgala", "Śukra", "Budha", "Candra", "Sūrya", "Budha",
    "Śukra", "Maṅgala", "Guru", "Śani", "Śani", "Guru",
]
RASI_LORDS_EN = [
    "Mars", "Venus", "Mercury", "Moon", "Sun", "Mercury",
    "Venus", "Mars", "Jupiter", "Saturn", "Saturn", "Jupiter",
]

# Navagraha in Parāśara's order (Sun .. Ketu). Ketu is derived, not a body id.
# (key, common, iast, english, glyph, swisseph id)
GRAHAS = [
    ("sun",     "Surya",   "Sūrya",   "Sun",     "☉", swe.SUN),
    ("moon",    "Chandra", "Candra",  "Moon",    "☽", swe.MOON),
    ("mars",    "Mangala", "Maṅgala", "Mars",    "♂", swe.MARS),
    ("mercury", "Budha",   "Budha",   "Mercury", "☿", swe.MERCURY),
    ("jupiter", "Guru",    "Guru",    "Jupiter", "♃", swe.JUPITER),
    ("venus",   "Shukra",  "Śukra",   "Venus",   "♀", swe.VENUS),
    ("saturn",  "Shani",   "Śani",    "Saturn",  "♄", swe.SATURN),
    ("rahu",    "Rahu",    "Rāhu",    "Rahu",    "☊", swe.MEAN_NODE),
    ("ketu",    "Ketu",    "Ketu",    "Ketu",    "☋", None),  # = Rahu + 180°
]

# 27 nakṣatras. Deities per BPHS ch.6 vv.24-26 (the Bhāṁśa / Nakṣatrāṁśa /
# Saptaviṁśāṁśa lords are the presiding deities of the nakṣatras, listed there
# in order). Transcribed word-for-word from Santhanam's Vol I text (ch.6,
# "24-26. BHAMSA (NAKSHATRAMSA OR SAPTAVIMSAMSA)", pp.78-79): Dastra, Yama,
# Agni, Brahma, Chandra, Isa, Aditi, Jiva, Ahi, Pitara, Bhaga, Aryama, Sūrya,
# Tvashta, Marut, Sakragni, Mitra, Vasava, Rakshasa, Varuna, Visvadeva, Govinda,
# Vasu, Varuna, Ajapa, Ahirbudhanya, Pusha. All 27 rows below reproduce it exactly.
#
# TWO ENTRIES DIVERGE FROM THE COMMON VEDIC LIST — kept as BPHS doctrine, NOT
# "corrected" to it (checked 2026-07-21 against the Santhanam PDF itself). Hasta
# (13) and Svātī (15): the primary Vedic authority — the Taittirīya Brāhmaṇa
# III.1.1-5 nakṣatra-devatā hymn, and with it the ordinary devatā list and Sunil
# John's Predicting Through Nakṣatras — give Savitṛ and Vāyu. Parāśara's text
# here prints Sūrya (Hasta) and Marut (Svātī). Each is the same deity-FAMILY as
# the TB reading (Sūrya/Savitṛ are both solar; Marut/Vāyu are both wind-gods),
# so these are genuine textual variants of Parāśara's, not transcription slips.
# This is a BPHS-tier value; the traditional-tier alternative is recorded,
# unapplied, in nakshatra_attrs.DEITY_TRADITION_VARIANTS.
# (common, iast, deity_common, deity_iast)
NAKSHATRAS = [
    ("Ashwini",            "Aśvinī",            "Dastra (Ashwini Kumara)", "Dastra (Aśvinī Kumāra)"),
    ("Bharani",            "Bharaṇī",           "Yama",                    "Yama"),
    ("Krittika",           "Kṛttikā",           "Agni",                    "Agni"),
    ("Rohini",             "Rohiṇī",            "Brahma",                  "Brahmā"),
    ("Mrigashira",         "Mṛgaśira",          "Chandra",                 "Candra"),
    ("Ardra",              "Ārdrā",             "Isha (Rudra)",            "Īśa (Rudra)"),
    ("Punarvasu",          "Punarvasu",         "Aditi",                   "Aditi"),
    ("Pushya",             "Puṣya",             "Jiva (Brihaspati)",       "Jīva (Bṛhaspati)"),
    ("Ashlesha",           "Āśleṣā",            "Ahi (Sarpa)",             "Ahi (Sarpa)"),
    ("Magha",              "Maghā",             "Pitara",                  "Pitara"),
    ("Purva Phalguni",     "Pūrva Phalgunī",    "Bhaga",                   "Bhaga"),
    ("Uttara Phalguni",    "Uttara Phalgunī",   "Aryama",                  "Aryamā"),
    ("Hasta",              "Hasta",             "Surya",                   "Sūrya"),      # BPHS ch.6 v.25; TB III.1 & common list have Savitṛ — see DEITY_TRADITION_VARIANTS
    ("Chitra",             "Citrā",             "Tvashta",                 "Tvaṣṭā"),
    ("Swati",              "Svātī",             "Marut",                   "Marut"),      # BPHS ch.6 v.25; TB III.1 & common list have Vāyu — see DEITY_TRADITION_VARIANTS
    ("Vishakha",           "Viśākhā",           "Shakragni",               "Śakrāgni"),
    ("Anuradha",           "Anurādhā",          "Mitra",                   "Mitra"),
    ("Jyeshtha",           "Jyeṣṭhā",           "Vasava (Indra)",          "Vāsava (Indra)"),
    ("Mula",               "Mūla",              "Rakshasa (Nirriti)",      "Rākṣasa (Nirṛti)"),
    ("Purva Ashadha",      "Pūrva Āṣāḍhā",      "Varuna",                  "Varuṇa"),
    ("Uttara Ashadha",     "Uttara Āṣāḍhā",     "Vishvadeva",              "Viśvadeva"),
    ("Shravana",           "Śravaṇa",           "Govinda (Vishnu)",        "Govinda (Viṣṇu)"),
    ("Dhanishta",          "Dhaniṣṭhā",         "Vasu",                    "Vasu"),
    ("Shatabhisha",        "Śatabhiṣā",         "Varuna",                  "Varuṇa"),
    ("Purva Bhadrapada",   "Pūrva Bhādrapadā",  "Ajapa",                   "Ajapa"),
    ("Uttara Bhadrapada",  "Uttara Bhādrapadā", "Ahirbudhanya",            "Ahirbudhanya"),
    ("Revati",             "Revatī",            "Pusha",                   "Pūṣā"),
]

NAKSHATRA_ARC = 360.0 / 27.0        # 13°20'
PADA_ARC = NAKSHATRA_ARC / 4.0      # 3°20' — same span as a navāṁśa


def ephemeris_status() -> tuple[bool, str]:
    """Is swisseph actually reading the .se1 files?

    With no ephemeris path set, swisseph does not error — it silently answers
    from its built-in Moshier theory and returns plausible numbers roughly
    0.1" off. For a chart that is a wrong nakṣatra at a boundary, invisibly.
    The return flag is the only honest signal, so check it rather than trusting
    that set_ephe_path() took.
    """
    _configure_thread()
    vals, retflag = swe.calc_ut(2451545.0, swe.MOON, swe.FLG_SWIEPH)
    ok = bool(retflag & swe.FLG_SWIEPH)
    ayan = swe.get_ayanamsa_ex_ut(2451545.0, swe.FLG_SWIEPH)[1]
    # Lahiri at J2000 is 23°51'; Fagan-Bradley (swisseph's default, i.e. what an
    # unconfigured thread would silently use) is ~24°44'. Catch the wrong one.
    lahiri_ok = abs(ayan - 23.8532) < 0.01
    ok = ok and lahiri_ok
    return ok, (f"moon@J2000={vals[0]:.6f} retflag={retflag} "
                f"ayanamsa@J2000={ayan:.4f} lahiri_ok={lahiri_ok} "
                f"thread={threading.current_thread().name} ephe_dir={EPHE_DIR}")


def _norm360(x: float) -> float:
    return x % 360.0


def _dms(lon: float) -> tuple[int, int, int]:
    within = _norm360(lon) % 30.0
    d = int(within)
    mf = (within - d) * 60.0
    m = int(mf)
    s = int(round((mf - m) * 60.0))
    if s == 60:
        s, m = 0, m + 1
    if m == 60:
        m, d = 0, d + 1
    return d, m, s


@dataclass
class Nakshatra:
    index: int          # 1-27
    name: str           # common English spelling
    name_iast: str
    deity: str
    deity_iast: str
    pada: int           # 1-4
    degrees_in: float   # arc traversed within the nakṣatra
    fraction: float     # 0-1 through the nakṣatra (Viṁśottarī needs this)


@dataclass
class Graha:
    key: str
    name: str           # common English spelling, e.g. "Chandra"
    name_iast: str      # scholarly transliteration, e.g. "Candra"
    name_en: str        # plain English, e.g. "Moon"
    glyph: str
    longitude: float    # SIDEREAL ecliptic longitude
    latitude: float
    speed: float
    rasi: int           # 0-11
    rasi_name: str
    rasi_name_iast: str
    rasi_name_en: str
    rasi_lord: str
    rasi_lord_iast: str
    rasi_lord_en: str
    degree: int
    minute: int
    second: int
    retrograde: bool
    bhava: int          # whole-sign house, 1-12
    nakshatra: Nakshatra
    vargas: dict[str, int]


@dataclass
class VedicChart:
    name: str
    jd_ut: float
    utc: str
    local_time: str
    timezone: str
    utc_offset_hours: float
    latitude: float
    longitude: float
    ayanamsa: str
    ayanamsa_value: float
    zodiac: str
    bhava_system: str
    lagna_longitude: float
    lagna_rasi: int
    lagna_nakshatra: Nakshatra
    # Each divisional chart has its OWN lagna — the varga of the lagna's
    # longitude — not the D1 lagna carried over. {'D9': sign_index, ...}
    lagna_vargas: dict[str, int]
    grahas: list[Graha]
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _nakshatra_of(lon: float) -> Nakshatra:
    lon = _norm360(lon)
    idx = int(lon // NAKSHATRA_ARC)
    within = lon - idx * NAKSHATRA_ARC
    name, name_iast, deity, deity_iast = NAKSHATRAS[idx]
    return Nakshatra(
        index=idx + 1,
        name=name,
        name_iast=name_iast,
        deity=deity,
        deity_iast=deity_iast,
        pada=int(within // PADA_ARC) + 1,
        degrees_in=within,
        fraction=within / NAKSHATRA_ARC,
    )


def to_julian_day(local_dt: datetime, tz_name: str) -> tuple[float, datetime, float]:
    """Local wall-clock birth time -> JD(UT).

    The tz database supplies the historical offset actually in force at that
    place on that date — which is what makes pre-1970 and DST-boundary births
    come out right.
    """
    tz = ZoneInfo(tz_name)
    aware = local_dt.replace(tzinfo=tz)
    utc_dt = aware.astimezone(ZoneInfo("UTC"))
    offset = aware.utcoffset().total_seconds() / 3600.0
    hour = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0
    return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, hour, swe.GREG_CAL), utc_dt, offset


def compute_chart(
    local_dt: datetime,
    latitude: float,
    longitude: float,
    tz_name: str,
    name: str = "",
) -> VedicChart:
    """Full sidereal rāśi chart with nakṣatras, bhāvas and all 16 vargas."""
    _configure_thread()
    ok, detail = ephemeris_status()
    if not ok:
        raise RuntimeError(
            "swisseph is not correctly configured on this thread — either the "
            ".se1 files are not being read (Moshier fallback) or the ayanamsa is "
            f"not Lahiri. Refusing to serve an approximated chart. ({detail})"
        )

    warnings: list[str] = []
    jd_ut, utc_dt, offset = to_julian_day(local_dt, tz_name)

    # get_ayanamsa_ut() returns the MEAN ayanamsa (no nutation) and does NOT
    # reconcile with the sidereal positions above — it is ~14" adrift, because
    # swisseph computes sidereal longitudes against the true equinox of date.
    # get_ayanamsa_ex_ut() includes nutation, matches the positions to 0.0000",
    # and agrees with the published Indian Astronomical Ephemeris value
    # (23°51'11" at J2000). Use it; never the plain one.
    ayanamsa_value = swe.get_ayanamsa_ex_ut(jd_ut, swe.FLG_SWIEPH)[1]

    # Whole-sign houses, sidereal: the 1st bhāva begins at 0° of the lagna's rāśi.
    cusps, ascmc = swe.houses_ex(jd_ut, latitude, longitude, b"W", swe.FLG_SIDEREAL)
    lagna_lon = ascmc[0]
    lagna_rasi = int(_norm360(lagna_lon) // 30)

    grahas: list[Graha] = []
    rahu_lon: float | None = None

    for key, name_common, name_iast, name_en, glyph, ipl in GRAHAS:
        if key == "ketu":
            # Ketu is always exactly opposite Rāhu; it has no body of its own.
            lon = _norm360(rahu_lon + 180.0)
            lat, speed = 0.0, ketu_speed
        else:
            vals, retflag = swe.calc_ut(jd_ut, ipl, CALC_FLAGS)
            if retflag < 0:
                raise RuntimeError(f"swisseph failed for {name_en}: flag {retflag}")
            if not retflag & swe.FLG_SWIEPH:
                warnings.append(
                    f"{name_en} did not come from the .se1 files (flag {retflag}); "
                    "position may be a lower-precision fallback."
                )
            lon, lat, speed = vals[0], vals[1], vals[3]
            if key == "rahu":
                rahu_lon, ketu_speed = lon, speed

        rasi = int(_norm360(lon) // 30)
        d, m, s = _dms(lon)
        grahas.append(Graha(
            key=key, name=name_common, name_iast=name_iast, name_en=name_en,
            glyph=glyph,
            longitude=lon, latitude=lat, speed=speed,
            rasi=rasi,
            rasi_name=RASIS[rasi], rasi_name_iast=RASIS_IAST[rasi],
            rasi_name_en=RASIS_EN[rasi],
            rasi_lord=RASI_LORDS[rasi], rasi_lord_iast=RASI_LORDS_IAST[rasi],
            rasi_lord_en=RASI_LORDS_EN[rasi],
            degree=d, minute=m, second=s,
            retrograde=speed < 0,
            bhava=(rasi - lagna_rasi) % 12 + 1,   # whole sign
            nakshatra=_nakshatra_of(lon),
            vargas=all_vargas(lon),
        ))

    return VedicChart(
        name=name,
        jd_ut=jd_ut,
        utc=utc_dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
        local_time=local_dt.strftime("%Y-%m-%d %H:%M:%S"),
        timezone=tz_name,
        utc_offset_hours=offset,
        latitude=latitude,
        longitude=longitude,
        ayanamsa="Lahiri (Chitrapakṣa)",
        ayanamsa_value=ayanamsa_value,
        zodiac="Sidereal",
        bhava_system="Whole sign (rāśi = bhāva)",
        lagna_longitude=lagna_lon,
        lagna_rasi=lagna_rasi,
        lagna_nakshatra=_nakshatra_of(lagna_lon),
        lagna_vargas=all_vargas(lagna_lon),
        grahas=grahas,
        warnings=warnings,
    )


def varga_chart(chart: VedicChart, key: str) -> dict[str, int]:
    """The divisional chart `key` (e.g. 'D9') as {graha_key: sign index}."""
    return {g.key: g.vargas[key] for g in chart.grahas}
