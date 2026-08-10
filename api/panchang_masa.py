"""Amānta lunar month (māsa) for a civil date — the missing coordinate that
lets the pañcāṅga name festivals (Diwali, Holi, Janmāṣṭamī …).

The five limbs give tithi/pakṣa but not the *month*, and a festival is a
(month, pakṣa, tithi) triple. This module supplies the month.

CONVENTION — amānta (new-moon to new-moon), the scheme most Vedic software and
southern/western India use. An amānta month runs from one new moon to the next;
the śukla pakṣa (pratipadā→pūrṇimā) comes first, then the kṛṣṇa pakṣa ending at
amāvāsyā. It is NAMED by the solar saṅkrānti — the rāśi the Sun ENTERS — that
falls within its span:

    Sun enters rāśi s (0=Meṣa)  →  the month is index s in the Caitra…Phālguna
    order (0=Caitra … 11=Phālguna).

That identity is not assumed; it is what real festival dates give, and it is
asserted by ``test`` below (Holi=Phālguna with Meena-saṅkrānti, Diwali=Āśvina
with Tulā-saṅkrānti, Janmāṣṭamī=Śrāvaṇa with Siṁha-saṅkrānti, Gudi-Padwa=Caitra
with Meṣa-saṅkrānti). If NO saṅkrānti falls in the span the month is *adhika*
(intercalary); festivals are then observed in the following nija month, so the
detector simply does not tag festivals inside an adhika month rather than risk
mis-tagging.

All astronomy reuses the sidereal (Lahiri) engine — ``vedic.CALC_FLAGS`` — so a
māsa here is on the same footing as every other number the site shows.

PŪRṆIMĀNTA NOTE. North-Indian almanacs name the *same* kṛṣṇa-pakṣa day one month
later (their month ends at pūrṇimā). So amānta Śrāvaṇa-kṛṣṇa-aṣṭamī is
purṇimānta Bhādrapada-kṛṣṇa-aṣṭamī — the same Janmāṣṭamī. The festival table
carries the popular pūrṇimānta name alongside for display; matching is amānta.
"""
from __future__ import annotations

import datetime as _dt
from zoneinfo import ZoneInfo

import swisseph as swe

from vedic import CALC_FLAGS, _norm360, _configure_thread

# 0=Caitra … 11=Phālguna. Index i is the month named by the Sun entering rāśi i.
AMANTA_MONTHS = ["Caitra", "Vaiśākha", "Jyeṣṭha", "Āṣāḍha", "Śrāvaṇa",
                 "Bhādrapada", "Āśvina", "Kārtika", "Mārgaśīrṣa", "Pauṣa",
                 "Māgha", "Phālguna"]
AMANTA_MONTHS_HI = ["चैत्र", "वैशाख", "ज्येष्ठ", "आषाढ", "श्रावण", "भाद्रपद",
                    "आश्विन", "कार्तिक", "मार्गशीर्ष", "पौष", "माघ", "फाल्गुन"]

# Mean synodic elongation rate (deg/day): 360 / 29.53059.
_ELONG_RATE = 12.19074


def _lon(jd: float, ipl: int) -> float:
    vals, rf = swe.calc_ut(jd, ipl, CALC_FLAGS)
    if rf < 0:
        raise RuntimeError(f"swisseph failed (ipl {ipl}): flag {rf}")
    return _norm360(vals[0])


def _elong(jd: float) -> float:
    """Moon − Sun, 0..360. Zero at new moon, 180 at full moon."""
    return _norm360(_lon(jd, swe.MOON) - _lon(jd, swe.SUN))


def _signed_elong(jd: float) -> float:
    """Elongation folded to (−180, 180]: 0 at new moon with positive slope,
    which makes the new moon a simple sign-changing root."""
    e = _elong(jd)
    return e - 360.0 if e > 180.0 else e


def _refine_new_moon(jd_guess: float) -> float:
    """Newton on the signed elongation to the new-moon instant near jd_guess.
    The slope is very nearly constant (_ELONG_RATE), so this converges in a few
    steps for any guess within a day or two of the conjunction."""
    jd = jd_guess
    for _ in range(60):
        s = _signed_elong(jd)
        if abs(s) < 1e-6:
            break
        jd -= s / _ELONG_RATE
    return jd


def _new_moons_around(jd0: float) -> tuple[float, float]:
    """The new moon at/just-before jd0 and the next one — i.e. the amānta month
    span containing jd0. On an amāvāsyā the elongation is still < 360, so jd0
    lands in the ENDING month (the amāvāsyā is that month's last tithi)."""
    e0 = _elong(jd0)                     # 0..360 — degrees since the last new moon
    prev = _refine_new_moon(jd0 - e0 / _ELONG_RATE)
    nxt = _refine_new_moon(jd0 + (360.0 - e0) / _ELONG_RATE)
    # Guard the bracket against a guess that overshot.
    if prev > jd0:
        prev = _refine_new_moon(prev - 29.53)
    if nxt <= jd0:
        nxt = _refine_new_moon(nxt + 29.53)
    return prev, nxt


def _jd_noon_ut(date: _dt.date, tz: ZoneInfo) -> float:
    aware = _dt.datetime(date.year, date.month, date.day, 12, 0, tzinfo=tz)
    u = aware.astimezone(ZoneInfo("UTC"))
    return swe.julday(u.year, u.month, u.day, u.hour + u.minute / 60.0, swe.GREG_CAL)


def amanta_masa(date: _dt.date, tz_name: str) -> dict:
    """The amānta lunar month for `date` (place only matters via the timezone,
    which fixes which civil day the lunation is read at). Returns the month
    index/name, the saṅkrānti sign that named it, and an `adhika` flag.

    Independent of latitude/longitude — the month is a global lunar-solar fact;
    only the civil-day boundary (tz) matters, and even that shifts the answer
    only within a few hours of a new moon.
    """
    _configure_thread()
    tz = ZoneInfo(tz_name)
    jd0 = _jd_noon_ut(date, tz)
    prev_nm, next_nm = _new_moons_around(jd0)

    # The saṅkrānti in the span: the Sun's sign at the start vs just before the
    # end. Normally exactly one boundary is crossed; the entered sign names it.
    s_start = int(_lon(prev_nm + 1e-3, swe.SUN) // 30)
    s_end = int(_lon(next_nm - 1e-3, swe.SUN) // 30)
    adhika = (s_start == s_end)          # no ingress in the span → intercalary
    entered = s_end                      # the sign the Sun moved INTO
    idx = entered % 12
    return {
        "index": idx,                    # 0=Caitra … 11=Phālguna
        "name": AMANTA_MONTHS[idx],
        "name_hi": AMANTA_MONTHS_HI[idx],
        "sankranti_sign": entered,
        "adhika": adhika,
    }


def sankranti_on(date: _dt.date, tz_name: str) -> int | None:
    """The sidereal rāśi (0=Meṣa … 11=Mīna) the Sun ENTERS during this civil day,
    or None if no ingress happens. Drives the solar festivals (Makara Saṅkrānti,
    Meṣa Saṅkrānti). Read across the local-midnight-to-midnight civil day."""
    _configure_thread()
    tz = ZoneInfo(tz_name)
    start = _dt.datetime(date.year, date.month, date.day, 0, 0, tzinfo=tz)
    end = start + _dt.timedelta(days=1)
    su = start.astimezone(ZoneInfo("UTC"))
    eu = end.astimezone(ZoneInfo("UTC"))
    jd_s = swe.julday(su.year, su.month, su.day, su.hour + su.minute / 60.0, swe.GREG_CAL)
    jd_e = swe.julday(eu.year, eu.month, eu.day, eu.hour + eu.minute / 60.0, swe.GREG_CAL)
    s0 = int(_lon(jd_s, swe.SUN) // 30)
    s1 = int(_lon(jd_e, swe.SUN) // 30)
    return s1 if s1 != s0 else None


if __name__ == "__main__":
    # Self-validation against real festival dates (amānta coords):
    #   Holi 2025-03-14        → Phālguna (11), Meena/Mīna saṅkrānti (11)
    #   Diwali 2024-11-01      → Āśvina   (6),  Tulā saṅkrānti (6)
    #   Janmāṣṭamī 2024-08-26  → Śrāvaṇa  (4),  Siṁha saṅkrānti (4)
    #   Gudi Padwa 2025-03-30  → Caitra   (0),  (Meṣa saṅkrānti falls just after)
    #   Ganesh Chaturthi 2024-09-07 → Bhādrapada (5)
    cases = [
        (_dt.date(2025, 3, 14), 11, "Phālguna"),
        (_dt.date(2024, 11, 1), 6, "Āśvina"),
        (_dt.date(2024, 8, 26), 4, "Śrāvaṇa"),
        (_dt.date(2025, 3, 30), 0, "Caitra"),
        (_dt.date(2024, 9, 7), 5, "Bhādrapada"),
    ]
    ok = True
    for d, want_idx, want_name in cases:
        m = amanta_masa(d, "Asia/Kolkata")
        flag = "OK " if m["index"] == want_idx else "XX "
        if m["index"] != want_idx:
            ok = False
        print(f"{flag}{d}  got {m['name']}({m['index']}) sankranti={m['sankranti_sign']} "
              f"adhika={m['adhika']}  want {want_name}({want_idx})")
    print("ALL PASS" if ok else "FAILURES ABOVE")
