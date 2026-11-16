"""BPHS ch.13 vv.1-7 (dhana_bhava.py): each clause fires on its own stated condition, and only then."""
import dhana_bhava as D

fails = []


def check(name, cond, extra=""):
    print(("  PASS  " if cond else "  **FAIL**  ") + name + ("" if cond else f"  ({extra})"))
    if not cond:
        fails.append(name)


def pos(**kw):
    return {g: {"rasi": r} for g, r in kw.items()}


def codes(res):
    return {c["code"] for m in res["matches"] for c in m["clauses"]}


ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO, LIBRA, SCORPIO, SAG, CAP, AQU, PISCES = range(12)

print("The owner's configuration — Aquarius ascendant, Jupiter in Pisces (2nd), Mars in Aries:")
r = D.evaluate(pos(sun=GEMINI, moon=CAP, mars=ARIES, mercury=TAURUS, jupiter=PISCES, venus=CANCER,
                   saturn=GEMINI, rahu=SCORPIO, ketu=TAURUS), AQU, moon_waxing=False)
check("the 2nd lord is Jupiter, and so is the 11th lord", r["lord2"] == "jupiter" and r["lord11"] == "jupiter")
check("vv.1-2: the 2nd lord in the 2nd", "lord2_well_placed" in codes(r))
check("vv.1-2: a benefic (Jupiter) in the 2nd", "benefic_in_2nd" in codes(r))
check("v.3: Jupiter in the 2nd as the lord of the 2nd", "jupiter_lord2_in_2nd" in codes(r))
check("v.3's other branch does not fire (Jupiter is not with Mars)", "jupiter_with_mars" not in codes(r))
check("vv.4-5 are not applied when one planet rules both houses",
      any(n["reason"] == "one_planet_rules_both" for n in r["not_applied"]) and not ({"lords_2_11_exchange", "lords_2_11_join_kendra_kona", "lord2_kendra_lord11_trine_from_it"} & codes(r)))
check("no poverty clause fires", not ({"lords_in_evil_houses_malefic_in_2nd", "lords_2_11_with_malefics"} & codes(r)))
check("every match carries the whole verse and its locus",
      all(m["text"] == D.VERSES[m["verse"]]["text"] and "ch.13" in m["citation"] for m in r["matches"]))

print("\nvv.1-2, the adverse halves:")
# Aries ascendant: 2nd = Taurus (Venus). Venus in Virgo = 6th. Saturn in Taurus = malefic in the 2nd.
r = D.evaluate(pos(sun=ARIES, moon=LEO, mars=ARIES, mercury=PISCES, jupiter=LEO, venus=VIRGO, saturn=TAURUS,
                   rahu=GEMINI, ketu=SAG), ARIES, moon_waxing=True)
check("the 2nd lord in the 6th", "lord2_in_6_8_12" in codes(r))
check("a malefic in the 2nd", "malefic_in_2nd" in codes(r))
check("the favourable half does not fire", "lord2_well_placed" not in codes(r))

print("\nThe natural classing (ch.3 v.11):")
n = D.natural_natures({"sun": 0, "moon": 1, "mercury": 0, "jupiter": 5, "venus": 6}, moon_waxing=True)
check("Mercury with the Sun is a malefic", n["mercury"] == "malefic")
check("a waxing Moon is a benefic, a waning one a malefic",
      n["moon"] == "benefic" and D.natural_natures({"moon": 1}, moon_waxing=False)["moon"] == "malefic")
check("the Moon is left out when its phase is unknown", "moon" not in D.natural_natures({"moon": 1, "sun": 3}))
check("Mercury alone is a benefic", D.natural_natures({"mercury": 2, "sun": 0})["mercury"] == "benefic")

print("\nv.3, v.4, v.5 and vv.6-7:")
r = D.evaluate(pos(sun=LEO, moon=CANCER, mars=LIBRA, mercury=LEO, jupiter=LIBRA, venus=VIRGO, saturn=CAP,
                   rahu=GEMINI, ketu=SAG), ARIES, moon_waxing=True)
check("Jupiter with Mars, whatever the house", "jupiter_with_mars" in codes(r))
# Aries: 2nd lord Venus, 11th lord Saturn. Exchange: Venus in Aquarius (11th), Saturn in Taurus (2nd).
r = D.evaluate(pos(sun=LEO, moon=CANCER, mars=LIBRA, mercury=LEO, jupiter=SAG, venus=AQU, saturn=TAURUS,
                   rahu=GEMINI, ketu=SAG), ARIES, moon_waxing=True)
check("v.4: the 2nd and 11th lords exchange houses", "lords_2_11_exchange" in codes(r))
# join in a trine: both in Leo (5th)
r = D.evaluate(pos(sun=ARIES, moon=CANCER, mars=LIBRA, mercury=ARIES, jupiter=SAG, venus=LEO, saturn=LEO,
                   rahu=GEMINI, ketu=SAG), ARIES, moon_waxing=True)
check("v.4: the two lords join in a trine", "lords_2_11_join_kendra_kona" in codes(r))
# v.5: Venus in Cancer (4th, an angle); Saturn in Scorpio (5th from Cancer)
r = D.evaluate(pos(sun=ARIES, moon=LEO, mars=LIBRA, mercury=ARIES, jupiter=SAG, venus=CANCER, saturn=SCORPIO,
                   rahu=GEMINI, ketu=SAG), ARIES, moon_waxing=True)
check("v.5: the 2nd lord in an angle, the 11th lord in a trine from it", "lord2_kendra_lord11_trine_from_it" in codes(r))
# vv.6-7: Venus in Virgo (6th), Saturn in Scorpio (8th), Mars in Taurus (2nd)
r = D.evaluate(pos(sun=ARIES, moon=LEO, mars=TAURUS, mercury=ARIES, jupiter=SAG, venus=VIRGO, saturn=SCORPIO,
                   rahu=GEMINI, ketu=SAG), ARIES, moon_waxing=True)
check("v.6: both lords in evil houses and a malefic in the 2nd", "lords_in_evil_houses_malefic_in_2nd" in codes(r))
check("v.7's combustion branch is reported as not evaluated",
      any(n["reason"] == "combustion_has_no_orb_in_the_text" for n in r["not_applied"]))

print("\nALL PASS" if not fails else f"\nFAILURES: {fails}")
raise SystemExit(1 if fails else 0)
