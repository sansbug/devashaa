"""Jaimini Chara Daśā length engine — validated against the book's own numbers.

Run: python api/test_charadasha.py

The two headline tests reconstruct the graha positions of the book's worked
Illustrations One and Two from their published "counted" columns — which are a
mathematical consequence of the method, not the copyrighted chart — and feed
those positions to the engine. The engine must then reproduce the book's exact
per-sign year table AND make the dual-lord tie-break choices the book states,
without being told them. Two illustrations exercise different tie-break branches
(Illus One: both-associated higher-degree, and associated-beats-solitary; Illus
Two: associated-beats-solitary again, and lord-in-sign-so-count-to-the-other).

A note on the reconstruction: for a single-lord sign, `counted` fixes the lord's
sign exactly (lord_sign = sign +/- (counted-1) by the sign's group). Where a
lord rules two signs, both reconstruct to the SAME sign — an internal-consistency
check that independently validates the counting-direction groups.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import charadasha as cd

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


ARI, TAU, GEM, CAN, LEO, VIR = 0, 1, 2, 3, 4, 5
LIB, SCO, SAG, CAP, AQU, PIS = 6, 7, 8, 9, 10, 11

print("The two fixed counting groups are exactly the book's (ch.6):")
check("DIRECT group = Aries,Taurus,Gemini,Libra,Scorpio,Sagittarius",
      cd.DIRECT_GROUP == frozenset({ARI, TAU, GEM, LIB, SCO, SAG}))
check("INDIRECT group = Cancer,Leo,Virgo,Capricorn,Aquarius,Pisces",
      cd.INDIRECT_GROUP == frozenset({CAN, LEO, VIR, CAP, AQU, PIS}))
check("the two groups partition all twelve signs",
      cd.DIRECT_GROUP | cd.INDIRECT_GROUP == frozenset(range(12))
      and not (cd.DIRECT_GROUP & cd.INDIRECT_GROUP))
check("the dual-lord signs are Scorpio (Mars,Ketu) and Aquarius (Saturn,Rahu)",
      cd.DUAL_LORDS == {SCO: ("mars", "ketu"), AQU: ("saturn", "rahu")})

print("\nILLUSTRATION ONE — Aries lagna (book total 86 years):")
# Reconstructed from the book's counted column; Ketu deg > Mars deg so the
# engine picks Ketu for Scorpio on higher-degree, as the book does.
# Sun sits in Aries: Leo is an INDIRECT sign so its lord is counted BACKWARD, and
# the book's "Leo counted 5" places the Sun 4 signs back from Leo, i.e. Aries.
pos1 = {"sun": ARI, "moon": LIB, "mars": TAU, "mercury": PIS, "jupiter": ARI,
        "venus": TAU, "saturn": ARI, "rahu": VIR, "ketu": PIS}
deg1 = {"sun": 15, "moon": 15, "mars": 10, "mercury": 15, "jupiter": 15,
        "venus": 15, "saturn": 15, "rahu": 20, "ketu": 20}
EXPECT_ONE = {ARI: 1, TAU: 12, GEM: 9, CAN: 9, LEO: 4, VIR: 6,
              LIB: 7, SCO: 4, SAG: 4, CAP: 9, AQU: 10, PIS: 11}
L1 = cd.sign_lengths(pos1, deg1)
got1 = {x["sign"]: x["years"] for x in L1}
for s in range(12):
    check(f"  sign {s}: {EXPECT_ONE[s]}y", got1[s] == EXPECT_ONE[s],
          f"got {got1[s]}")
check("total is the book's 86 years", sum(got1.values()) == 86, str(sum(got1.values())))
# the engine chose the same operative lords the book names for the dual signs
sco1 = next(x for x in L1 if x["sign"] == SCO)
aqu1 = next(x for x in L1 if x["sign"] == AQU)
check("Scorpio: engine independently chose Ketu (both elsewhere, higher degree)",
      sco1["lord"] == "ketu", sco1["lord"])
check("Aquarius: engine independently chose Saturn (it has company, Rāhu alone)",
      aqu1["lord"] == "saturn", aqu1["lord"])

print("\nILLUSTRATION TWO — Virgo lagna (book total 56 years):")
# Different tie-break branches: Scorpio -> Ketu because Mars is solitary;
# Aquarius -> Saturn because Rahu sits in Aquarius (count to the other lord).
# Sun in Cancer for the same reason: Leo counts backward, and the book's
# "Leo counted 2" places the Sun one sign back from Leo, i.e. Cancer.
pos2 = {"sun": CAN, "moon": PIS, "mars": GEM, "mercury": LEO, "jupiter": PIS,
        "venus": LEO, "saturn": VIR, "rahu": AQU, "ketu": LEO}
EXPECT_TWO = {ARI: 2, TAU: 3, GEM: 2, CAN: 4, LEO: 1, VIR: 1,
              LIB: 10, SCO: 9, SAG: 3, CAP: 4, AQU: 5, PIS: 12}
L2 = cd.sign_lengths(pos2)
got2 = {x["sign"]: x["years"] for x in L2}
for s in range(12):
    check(f"  sign {s}: {EXPECT_TWO[s]}y", got2[s] == EXPECT_TWO[s], f"got {got2[s]}")
check("total is the book's 56 years", sum(got2.values()) == 56, str(sum(got2.values())))
sco2 = next(x for x in L2 if x["sign"] == SCO)
aqu2 = next(x for x in L2 if x["sign"] == AQU)
check("Scorpio: engine chose Ketu (Mars solitary, Ketu has company)", sco2["lord"] == "ketu")
check("Aquarius: engine chose Saturn (Rāhu sits in Aquarius, count to the other)",
      aqu2["lord"] == "saturn")
check("Pisces is own-sign for Jupiter → the flat 12 years", got2[PIS] == 12
      and next(x for x in L2 if x["sign"] == PIS)["own_sign"])

print("\nThe own-sign exception and the 1..12 bounds (ch.6):")
own = cd.sign_lengths({"sun": LEO, "moon": TAU, "mars": ARI, "mercury": VIR,
                       "jupiter": SAG, "venus": TAU, "saturn": CAP,
                       "rahu": GEM, "ketu": SAG})
check("Sun in Leo → Leo daśā is the flat 12, no deduction",
      next(x for x in own if x["sign"] == LEO)["years"] == 12)
check("every sign's length is a whole number in 1..12",
      all(x["years"] == int(x["years"]) and 1 <= x["years"] <= 12
          for r in (L1, L2, own) for x in r))

print("\nDual-lord tie-break, each of Rao's cases exercised directly:")
base = {"sun": GEM, "moon": GEM, "jupiter": GEM}   # some filler occupants
# (c) both lords in the sign → own-sign, 12 years
c = cd.sign_lengths({**base, "mars": SCO, "ketu": SCO, "mercury": ARI,
                     "venus": ARI, "saturn": ARI, "rahu": ARI})
check("(c) both Mars and Ketu in Scorpio → 12 years",
      next(x for x in c if x["sign"] == SCO)["years"] == 12)
# (a) Mars in Scorpio, Ketu elsewhere → count to Ketu
a = cd.sign_lengths({**base, "mars": SCO, "ketu": SAG, "mercury": ARI,
                     "venus": ARI, "saturn": ARI, "rahu": ARI})
ax = next(x for x in a if x["sign"] == SCO)
check("(a) Mars in Scorpio → operative lord is Ketu", ax["lord"] == "ketu")
# (d)(iv) both solitary, same degree+minute, seconds decides
d = cd.sign_lengths(
    {"mars": ARI, "ketu": LEO, "sun": GEM, "moon": CAP, "mercury": PIS,
     "jupiter": VIR, "venus": LIB, "saturn": AQU, "rahu": AQU},
    {"mars": 10.5000, "ketu": 10.5003, "sun": 5, "moon": 5, "mercury": 5,
     "jupiter": 5, "venus": 5, "saturn": 5, "rahu": 5})
check("(d) both solitary → the higher longitude-within-sign wins (Ketu by seconds)",
      next(x for x in d if x["sign"] == SCO)["lord"] == "ketu")

print("\nThe SEQUENCE DIRECTION is never guessed — it must be supplied:")
r = cd.chara_dasha(pos1, deg1, lagna=ARI)     # no direction
check("with no direction, no sequence is produced", r["sequence"] is None)
check("...and it says why: the selection rule is not in the source",
      "Chapter 3" in r["sequence_note"] or "ch.3" in r["sequence_note"])
r2 = cd.chara_dasha(pos1, deg1, lagna=ARI, direction="direct")
check("given 'direct' from an Aries lagna, the sequence starts at Aries",
      r2["sequence"][0]["sign"] == ARI)
check("...and runs zodiacally forward (next is Taurus)",
      r2["sequence"][1]["sign"] == TAU)
check("...carrying each sign's own length and cumulative offset",
      r2["sequence"][0]["years"] == 1 and r2["sequence"][1]["start_offset"] == 1)
rev = cd.chara_dasha(pos1, deg1, lagna=ARI, direction="reverse")
check("given 'reverse', the sequence runs backward (Aries then Pisces)",
      rev["sequence"][1]["sign"] == PIS)
check("the caveat travels with any supplied direction",
      "not inferred" in r2["direction_caveat"])
try:
    cd.chara_dasha(pos1, deg1, lagna=ARI, direction="sideways")
    check("a bad direction is rejected", False)
except ValueError:
    check("a bad direction is rejected", True)

print("\nProvenance is Jaimini, never labelled BPHS:")
check("the citation names the Jaimini source and marks it NOT BPHS",
      "jaimini" in cd.CITATION.lower() and "NOT BPHS" in cd.CITATION)
check("the payload tier is 'jaimini'",
      cd.chara_dasha(pos1, deg1)["tier"] == "jaimini")

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
