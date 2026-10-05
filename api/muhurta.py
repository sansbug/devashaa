"""Muhūrta for a ceremony — the time-windows of one day at one place.

A booking needs more than a date: it needs to know WHEN in the day. This
module answers that from the same sunrise the pañcāṅga is computed at, with
the divisions of the day the almanacs use. Tier: `traditional` — almanac
practice, shared across the printed pañcāṅgas, not a single text's rule:

  * the EIGHT-fold day → rāhu kāla, yama-gaṇḍa, gulika kāla (to be avoided);
    weekday tables in panchang.py
  * the FIFTEEN-muhūrta day and night → abhijit (the 8th of the day, void on
    Wednesday), brahma muhūrta (the 14th of the night), niśītha (the 8th of
    the night), and pradoṣa (the first three muhūrtas after sunset)
  * the FIVE-fold day → prātaḥ, saṅgava, madhyāhna, aparāhṇa, sāyāhna
  * CHOGHAḌIYĀ — day and night each in eight parts, named from the weekday's
    lord in the order of the horā lords (Sun, Venus, Mercury, Moon, Saturn,
    Jupiter, Mars); the night series starts from the fifth lord on and steps
    by five. Amṛta, Śubha and Lābha are held good, Cara fair, Udvega, Kāla
    and Roga are avoided.

What it returns for a day: the five limbs at sunrise, the windows to avoid,
the clear windows (good choghaḍiyā with the three avoided spans cut out),
the kāla a given ceremony is traditionally kept in, and the cautions the
almanac itself would print (riktā tithi, Viṣṭi/Bhadrā karaṇa, a harsh yoga).

It is a calendar computation, not a judgement on a person: no birth chart
enters it. The pandit confirms the hour.
"""
from __future__ import annotations

import datetime as _dt
from zoneinfo import ZoneInfo

import swisseph as swe

import panchang

TIER = "traditional"

# Choghaḍiyā by lord, in horā order. Quality: +1 good, 0 fair, -1 avoid.
_HORA_ORDER = ["sun", "venus", "mercury", "moon", "saturn", "jupiter", "mars"]
_CHOG = {
    "sun": ("Udvega", "उद्वेग", -1), "venus": ("Cara", "चर", 0), "mercury": ("Lābha", "लाभ", 1),
    "moon": ("Amṛta", "अमृत", 1), "saturn": ("Kāla", "काल", -1), "jupiter": ("Śubha", "शुभ", 1),
    "mars": ("Roga", "रोग", -1),
}
_WEEKDAY_LORD = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"]   # 0 = Sunday

# The kāla a ceremony is traditionally kept in. (key of a window below, reason en, reason hi)
PREFERRED = {
    "lakshmi": ("pradosha", "Lakṣmī pūjā is kept in pradoṣa kāla — the first part of the night, just after sunset.",
                "लक्ष्मी पूजा प्रदोष काल में की जाती है — सूर्यास्त के ठीक बाद, रात्रि के पहले भाग में।"),
    "rudrabhishek": ("pradosha", "Śiva is worshipped in pradoṣa kāla; a clear morning window is also kept.",
                     "शिव पूजन प्रदोष काल में होता है; प्रातः का शुभ समय भी लिया जाता है।"),
    "mahamrityunjaya": ("pratah", "The japa and havan are usually begun in the morning.",
                        "जप और हवन प्रायः प्रातः आरंभ किए जाते हैं।"),
    "shraddha": ("aparahna", "Śrāddha is offered in the aparāhṇa, the fourth fifth of the day; its best part is the kutapa muhūrta at midday.",
                 "श्राद्ध अपराह्न में किया जाता है — दिन का चौथा पंचमांश; उसका श्रेष्ठ भाग मध्याह्न का कुतप मुहूर्त है।"),
    "ganesh": ("madhyahna", "Gaṇeśa is worshipped at madhyāhna, the middle fifth of the day.",
               "गणेश पूजन मध्याह्न में होता है — दिन का मध्य पंचमांश।"),
    "satyanarayan": ("sayahna", "The kathā is most often kept towards evening; any clear window of the day also serves.",
                     "कथा प्रायः सायंकाल की ओर रखी जाती है; दिन का कोई भी शुभ समय भी चलता है।"),
    "saraswati": ("pratah", "Sarasvatī is worshipped in the forenoon.", "सरस्वती पूजन पूर्वाह्न में होता है।"),
    "durga": ("pratah", "The pāṭha is begun in the morning.", "पाठ प्रातः आरंभ किया जाता है।"),
    "sundarkand": ("sayahna", "Often kept in the evening.", "प्रायः सायंकाल रखा जाता है।"),
}
# Ceremonies that BEGIN something: the almanac's day-cautions apply to them.
BEGINNINGS = {"griha-pravesh", "namakaran", "annaprashan", "mundan", "vahan", "janmadin", "gayatri-havan", "saraswati", "ganesh"}


def _local(jd_ut: float, tz: ZoneInfo) -> _dt.datetime:
    y, m, d, h = swe.revjul(jd_ut, swe.GREG_CAL)
    return (_dt.datetime(y, m, d, tzinfo=_dt.timezone.utc) + _dt.timedelta(hours=h)).astimezone(tz)


def _span(a: float, b: float, tz: ZoneInfo, day: _dt.date) -> dict:
    la, lb = _local(a, tz), _local(b, tz)
    return {"start": la.strftime("%H:%M"), "end": lb.strftime("%H:%M"),
            "minutes": int(round((b - a) * 1440)), "next_day": la.date() > day or lb.date() > day}


def _cut(a: float, b: float, holes: list[tuple[float, float]]) -> list[tuple[float, float]]:
    """[a, b) with every hole removed."""
    out = [(a, b)]
    for h0, h1 in holes:
        nxt = []
        for s, e in out:
            if h1 <= s or h0 >= e:
                nxt.append((s, e))
            else:
                if h0 > s:
                    nxt.append((s, h0))
                if h1 < e:
                    nxt.append((h1, e))
        out = nxt
    return out


def choghadiya(jd_rise: float, jd_set: float, jd_next: float, weekday: int) -> dict:
    """Day and night series as (lord, start_jd, end_jd)."""
    first = _HORA_ORDER.index(_WEEKDAY_LORD[weekday])
    dpart, npart = (jd_set - jd_rise) / 8.0, (jd_next - jd_set) / 8.0
    day = [(_HORA_ORDER[(first + i) % 7], jd_rise + i * dpart, jd_rise + (i + 1) * dpart) for i in range(8)]
    nfirst = (first + 5) % 7          # the night opens with the fifth lord on
    night = [(_HORA_ORDER[(nfirst + 5 * i) % 7], jd_set + i * npart, jd_set + (i + 1) * npart) for i in range(8)]
    return {"day": day, "night": night}


def day_muhurta(date: _dt.date, latitude: float, longitude: float, tz_name: str, ritual: str | None = None) -> dict:
    tz = ZoneInfo(tz_name)
    pan = panchang.panchanga(date, latitude, longitude, tz_name)
    rise, sett, nxt = pan["_jd_rise"], pan["_jd_set"], pan["_jd_next"]
    wd = pan["vara"]["index"]
    day, night = sett - rise, nxt - sett
    e8, m15, n15, f5 = day / 8.0, day / 15.0, night / 15.0, day / 5.0
    sp = lambda a, b: _span(a, b, tz, date)   # noqa: E731

    def eighth(n):
        return rise + (n - 1) * e8, rise + n * e8
    avoid_jd = {
        "rahu_kala": eighth(panchang._RAHU[wd]),
        "yama_ganda": eighth(panchang._YAMA[wd]),
        "gulika_kala": eighth(panchang._GULIKA[wd]),
    }
    avoid = [{"key": k, "name": n, "name_hi": h, **sp(*avoid_jd[k])} for k, n, h in (
        ("rahu_kala", "Rāhu kāla", "राहु काल"), ("yama_ganda", "Yama-gaṇḍa", "यमगण्ड"), ("gulika_kala", "Gulika kāla", "गुलिक काल"))]

    abhijit_jd = None if wd == 3 else (rise + 7 * m15, rise + 8 * m15)
    kala_jd = {
        "pratah": (rise, rise + f5), "sangava": (rise + f5, rise + 2 * f5), "madhyahna": (rise + 2 * f5, rise + 3 * f5),
        "aparahna": (rise + 3 * f5, rise + 4 * f5), "sayahna": (rise + 4 * f5, sett),
        "pradosha": (sett, sett + 3 * n15), "nishitha": (sett + 7 * n15, sett + 8 * n15),
        "brahma": (nxt - 2 * n15, nxt - n15),
    }
    if abhijit_jd:
        kala_jd["abhijit"] = abhijit_jd
    KALA_NAME = {
        "pratah": ("Prātaḥ kāla", "प्रातः काल"), "sangava": ("Saṅgava kāla", "संगव काल"),
        "madhyahna": ("Madhyāhna", "मध्याह्न"), "aparahna": ("Aparāhṇa", "अपराह्न"), "sayahna": ("Sāyāhna", "सायाह्न"),
        "pradosha": ("Pradoṣa kāla", "प्रदोष काल"), "nishitha": ("Niśītha", "निशीथ"),
        "brahma": ("Brahma muhūrta (next dawn)", "ब्रह्म मुहूर्त (अगली भोर)"), "abhijit": ("Abhijit muhūrta", "अभिजित् मुहूर्त"),
    }
    kala = {k: {"name": KALA_NAME[k][0], "name_hi": KALA_NAME[k][1], **sp(*v)} for k, v in kala_jd.items()}

    ch = choghadiya(rise, sett, nxt, wd)

    def chog_rows(rows):
        return [{"lord": lord, "name": _CHOG[lord][0], "name_hi": _CHOG[lord][1], "quality": _CHOG[lord][2], **sp(a, b)}
                for lord, a, b in rows]

    # Clear windows: every good or fair daytime choghaḍiyā, with the three avoided spans cut out.
    holes = list(avoid_jd.values())
    clear = []
    for lord, a, b in ch["day"]:
        q = _CHOG[lord][2]
        if q < 0:
            continue
        for s, e in _cut(a, b, holes):
            if (e - s) * 1440 < 20:
                continue
            clear.append({"choghadiya": _CHOG[lord][0], "choghadiya_hi": _CHOG[lord][1], "quality": q,
                          "abhijit": bool(abhijit_jd and s < abhijit_jd[1] and e > abhijit_jd[0]),
                          "_s": s, **sp(s, e)})
    # The evening: pradoṣa, minus any harsh night choghaḍiyā.
    bad_night = [(a, b) for lord, a, b in ch["night"] if _CHOG[lord][2] < 0]
    evening = [{"kala": "pradosha", "_s": s, **sp(s, e)} for s, e in _cut(*kala_jd["pradosha"], bad_night) if (e - s) * 1440 >= 20]

    pref = None
    if ritual and ritual in PREFERRED:
        key, why, why_hi = PREFERRED[ritual]
        a, b = kala_jd[key]
        inside = [c for c in clear if c["_s"] < b and c["_s"] + c["minutes"] / 1440.0 > a] if key != "pradosha" else evening
        pref = {"kala": key, "name": KALA_NAME[key][0], "name_hi": KALA_NAME[key][1], "why": why, "why_hi": why_hi,
                **sp(a, b), "clear_within": [{k: v for k, v in c.items() if not k.startswith("_")} for c in inside]}

    cautions = []
    grp = pan["tithi"]["group"]
    if grp == "Riktā":
        cautions.append({"key": "rikta", "text": f"{pan['tithi']['name']} is a riktā tithi — the almanac avoids it for beginning something new.",
                         "text_hi": f"{pan['tithi']['name_hi']} रिक्ता तिथि है — पंचांग नए आरंभ के लिए इसे टालता है।"})
    if pan["tithi"]["index"] == 30:
        cautions.append({"key": "amavasya", "text": "Amāvāsyā — kept for the ancestors; the almanac avoids it for beginnings.",
                         "text_hi": "अमावस्या — पितरों के लिए; पंचांग इसे नए आरंभ के लिए टालता है।"})
    if not pan["karana"]["auspicious"]:
        cautions.append({"key": "karana", "text": f"{pan['karana']['name']} karaṇa at sunrise — avoided for auspicious beginnings{' (Bhadrā)' if pan['karana']['name'] == 'Viṣṭi' else ''}.",
                         "text_hi": f"सूर्योदय पर {pan['karana']['name_hi']} करण — शुभारंभ के लिए टाला जाता है{' (भद्रा)' if pan['karana']['name'] == 'Viṣṭi' else ''}।"})
    if not pan["yoga"]["auspicious"]:
        cautions.append({"key": "yoga", "text": f"{pan['yoga']['name']} yoga at sunrise — the almanac marks it harsh.",
                         "text_hi": f"सूर्योदय पर {pan['yoga']['name_hi']} योग — पंचांग इसे कठोर मानता है।"})

    strip = lambda rows: [{k: v for k, v in r.items() if not k.startswith("_")} for r in rows]   # noqa: E731
    return {
        "tier": TIER, "date": date.isoformat(), "timezone": tz_name,
        "sunrise": _local(rise, tz).strftime("%H:%M"), "sunset": _local(sett, tz).strftime("%H:%M"),
        "next_sunrise": _local(nxt, tz).strftime("%H:%M"),
        "panchang": {k: pan[k] for k in ("tithi", "vara", "nakshatra", "yoga", "karana")},
        "avoid": avoid, "kala": kala,
        "choghadiya": {"day": chog_rows(ch["day"]), "night": chog_rows(ch["night"])},
        "clear": strip(clear), "evening": strip(evening),
        "preferred": pref,
        "cautions": cautions, "cautions_apply": bool(ritual in BEGINNINGS) if ritual else None,
        "note": ("Computed for this place from its sunrise and sunset. Clear windows are the good and fair "
                 "choghaḍiyās of the day with rāhu kāla, yama-gaṇḍa and gulika kāla cut out. Almanac practice "
                 "(traditional tier), not a judgement on any person; your pandit confirms the hour."),
    }
