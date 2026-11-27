"""BPHS chs 12, 14-18, 20-23 (bhava_effects.py): each verse fires on its own condition, and carries its text whole."""
import re
import bhava_effects as B

fails = []


def check(name, cond, extra=""):
    print(("  PASS  " if cond else "  **FAIL**  ") + name + ("" if cond else f"  ({extra})"))
    if not cond:
        fails.append(name)


ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO, LIBRA, SCORPIO, SAG, CAP, AQU, PISCES = range(12)


def pos(**kw):
    """graha=(sign, degree) → positions with longitudes"""
    return {g: {"rasi": s, "longitude": s * 30 + d} for g, (s, d) in kw.items()}


def got(res):
    return {f"{m['chapter']}.{m['verse']}" for m in res["matches"]}


print("The registry:")
check("63 verses are registered (54 + the 9 dated ones of 2026-11-27)", len(B.VERSES) == 63, str(len(B.VERSES)))
check("every verse has its text, a locus with a printed page, and a house",
      all(v["text"] and re.search(r"BPHS I ch\.\d+ vv?\.[\d-]+ \(pp?\.[\d-]+\)", v["citation"]) and 1 <= v["house"] <= 12 for v in B.VERSES))
check("ch.19 (longevity) is not registered", not any(v["chapter"] == 19 for v in B.VERSES))
# owner 2026-11-26: a dated GOOD event may be shown; a dated death, lifespan, disease or danger may not (no fear)
DATED = {"15.10-14", "16.18", "16.19", "16.20", "20.10", "20.27-28", "22.4", "22.5", "22.8"}
AGE_RE = r"\b(\d+(st|nd|rd|th) year|age of \d+|at \d+ and \d+)\b"
check("the verses that name an age are exactly the registered dated ones",
      {f"{v['chapter']}.{v['verse']}" for v in B.VERSES if re.search(AGE_RE, v["text"])} == DATED,
      str({f"{v['chapter']}.{v['verse']}" for v in B.VERSES if re.search(AGE_RE, v["text"])} ^ DATED))
check("no dated verse speaks of a death, a lifespan, a disease or a danger",
      not any(re.search(r"\b(death|die|lose|loss|fatal|life|disease|danger|fear|fever|leprosy)\b", v["text"], re.I)
              for v in B.VERSES if f"{v['chapter']}.{v['verse']}" in DATED))
check("ch.17's dated verses (diseases, unfortunate years) stay out", not any(v["chapter"] == 17 and v["verse"] != "2" for v in B.VERSES))
check("every note is given in both languages", all(len(v["notes"]["en"]) == len(v["notes"]["hi"]) for v in B.VERSES))

print("\nThe owner's configuration (Aquarius ascendant):")
r = B.evaluate(pos(sun=(GEMINI, 10), moon=(CAP, 3), mars=(ARIES, 2), mercury=(TAURUS, 21), jupiter=(PISCES, 27),
                   venus=(CANCER, 25), saturn=(GEMINI, 26), rahu=(SCORPIO, 8), ketu=(TAURUS, 8)), AQU, moon_waxing=False)
check("no verse raised an error", not r["errors"], str(r["errors"]))
check("ch.21 v.3: Rāhu in an angle", "21.3" in got(r))
check("ch.12 vv.1-2 fires on both sides (lord in a trine; with a malefic)",
      {c["polarity"] for m in r["matches"] if m["chapter"] == 12 and m["verse"] == "1-2" for c in m["clauses"]} == {"favourable", "adverse"})
check("ch.22 v.3 does not fire (the 2nd lord is not in an angle)", "22.3" not in got(r))
check("ch.22 v.9 / ch.21 v.13 need two different lords", "22.9" not in got(r))
check("every match returns the registered verse whole",
      all(m["text"] == next(v["text"] for v in B.VERSES if v["chapter"] == m["chapter"] and v["verse"] == m["verse"]) for m in r["matches"]))
check("every clause says why, in both languages, and names its grahas",
      all(c["why"]["en"] and c["why"]["hi"] and c["grahas"] for m in r["matches"] for c in m["clauses"]))

print("\nSingle verses:")
# Aries ascendant. 7th = Libra (Venus). Venus in Pisces = exalted, 12th house.
base = dict(sun=(LEO, 5), moon=(TAURUS, 5), mars=(CAP, 10), mercury=(LEO, 20), jupiter=(SAG, 5), venus=(PISCES, 20),
            saturn=(AQU, 5), rahu=(GEMINI, 5), ketu=(SAG, 5))
r = B.evaluate(pos(**base), ARIES, moon_waxing=True)
check("ch.18 v.1: the 7th lord exalted", "18.1" in got(r))
check("ch.18 v.2 excepts own sign and exaltation, as the verse says", "18.2" not in got(r))
check("ch.22 v.2: the 11th lord in the 11th", "22.2" in got(r))
r = B.evaluate(pos(**{**base, "venus": (VIRGO, 20)}), ARIES, moon_waxing=True)
check("ch.18 v.2: the 7th lord in the 6th, neither own nor exalted", "18.2" in got(r))
check("ch.18 v.1 does not fire then", "18.1" not in got(r))
# ch.22 v.9: Aries — 11th lord Saturn in Taurus (2nd), 2nd lord Venus in Aquarius (11th)
r = B.evaluate(pos(**{**base, "saturn": (TAURUS, 5), "venus": (AQU, 5)}), ARIES, moon_waxing=True)
check("ch.22 v.9: the 2nd and 11th lords exchange", "22.9" in got(r))
# ch.21 v.6: Aries — 10th lord Saturn with Rāhu in Scorpio (8th)
r = B.evaluate(pos(**{**base, "saturn": (SCORPIO, 5), "rahu": (SCORPIO, 9), "ketu": (TAURUS, 9)}), ARIES, moon_waxing=True)
check("ch.21 v.6: the 10th lord in the 8th with Rāhu", "21.6" in got(r))
# ch.15 v.8: Sun 4th, Moon+Saturn 9th, Mars 11th (Aries: Cancer, Sagittarius, Aquarius)
r = B.evaluate(pos(**{**base, "sun": (CANCER, 5), "moon": (SAG, 9), "saturn": (SAG, 12), "mars": (AQU, 3)}), ARIES, moon_waxing=True)
check("ch.15 v.8: the four-planet yoga", "15.8" in got(r))
check("…and it does not fire on the base chart", "15.8" not in got(B.evaluate(pos(**base), ARIES, moon_waxing=True)))

print("\nDated verses (each fires on its own condition, carries its age, and not on the base chart):")
base_got = got(B.evaluate(pos(**base), ARIES, moon_waxing=True))


def dated(key, lagna, age, **moves):
    r = B.evaluate(pos(**{**base, **moves}), lagna, moon_waxing=True)
    m = next((m for m in r["matches"] if f"{m['chapter']}.{m['verse']}" == key), None)
    ok = m and m["dated"] and any(c.get("age") == age for c in m["clauses"]) and not r["errors"]
    check(f"ch.{key} fires with age {age['kind']} {age['n']}", bool(ok), str(m and m["clauses"]) + str(r["errors"]))


for key in DATED:
    check(f"ch.{key} does not fire on the base chart", key not in base_got)
# Aries ascendant unless named. Lords: 1 Mars, 2 Venus, 4 Moon, 5 Sun, 9 Jupiter, 11 Saturn.
dated("22.8", ARIES, B.Y(33), saturn=(ARIES, 10), mars=(AQU, 10))
dated("22.4", ARIES, B.Y(36), saturn=(GEMINI, 10), jupiter=(AQU, 10))
dated("22.5", ARIES, B.Y(40), saturn=(CANCER, 10), jupiter=(CANCER, 12))
dated("20.10", ARIES, B.AFTER(32), jupiter=(TAURUS, 10), venus=(SAG, 10))
dated("20.27-28", GEMINI, B.AFTER(20), jupiter=(AQU, 10), saturn=(GEMINI, 10))   # Gemini: 9th lord Saturn
dated("16.18", ARIES, B.Y(32, 33), jupiter=(LEO, 10), sun=(PISCES, 2), venus=(PISCES, 20))
dated("16.19", ARIES, B.AGE(30, 36), sun=(CANCER, 3), jupiter=(CANCER, 12))
dated("16.20", ARIES, B.AGE(40), jupiter=(SAG, 10), venus=(LEO, 10), mars=(LEO, 20))
dated("15.10-14", ARIES, B.Y(12), moon=(AQU, 10), saturn=(CANCER, 10))                    # 4th–11th exchange
dated("15.10-14", ARIES, B.Y(32), sun=(CANCER, 5), moon=(TAURUS, 3), venus=(TAURUS, 20))   # Sun 4th, 4th lord exalted with Venus
dated("15.10-14", TAURUS, B.Y(12), venus=(ARIES, 10), sun=(PISCES, 10))                    # benefic lagna lord, 4th lord in 11th, Venus 12th
check("a verse that is not dated says so", all(not m["dated"] for m in B.evaluate(pos(**base), ARIES, moon_waxing=True)["matches"]))

print("\nALL PASS" if not fails else f"\nFAILURES: {fails}")
raise SystemExit(1 if fails else 0)
