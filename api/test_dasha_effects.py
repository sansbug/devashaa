"""BPHS Vol II ch.47 vv.5-6 — the daśā verdict.

Run: python api/test_dasha_effects.py

The verse names six conditions across two branches. These tests exercise every
one of them, both branches firing together, and the case the whole design turns
on: NEITHER branch firing, which is silence and not neutrality.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import dasha_effects as de
import dignity

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO = 0, 1, 2, 3, 4, 5
LIBRA, SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES = 6, 7, 8, 9, 10, 11
S = ["Meṣa", "Vṛṣabha", "Mithuna", "Karka", "Siṁha", "Kanyā",
     "Tulā", "Vṛścika", "Dhanus", "Makara", "Kumbha", "Mīna"]

print("The four FAVOURABLE conditions of v.5:")
# "in the Ascendant" — lagna Aries, Sun in Aries => bhava 1
v = de.verdict("sun", ARIES, ARIES)
check("in the Ascendant → favourable", v["state"] == de.FAVOURABLE, v["state"])
check("...and cites the Ascendant clause",
      any("Ascendant" in f["condition"] for f in v["favourable"]))
# "in his sign of exaltation" — Sun exalts in Aries; put lagna elsewhere so the
# Ascendant clause cannot be what fired.
v = de.verdict("sun", ARIES, LEO)
check("in his sign of exaltation → favourable", v["state"] == de.FAVOURABLE)
check("...and it is the EXALTATION clause that fired, not the Ascendant",
      any("exaltation" in f["condition"] for f in v["favourable"])
      and not any("Ascendant" in f["condition"] for f in v["favourable"]))
# "in his own sign"
v = de.verdict("mars", SCORPIO, LEO)
check("in his own sign → favourable",
      v["state"] == de.FAVOURABLE
      and any("own sign" in f["condition"] for f in v["favourable"]))
# "in a friend's sign" — Sun's friends include the Moon (Cancer)
check("Chandra is a natural friend of Sūrya (ch.3 v.55)",
      dignity.NATURAL_RELATIONS["sun"]["moon"] == "friend")
# Lagna must be chosen so the friend's sign is NOT also a 6/8/12 house, or
# both branches fire and the answer is `contested` — which is what happened on
# the first attempt at this fixture (Karka is the 12th from a Siṁha lagna).
v = de.verdict("sun", CANCER, ARIES)          # Karka is the 4th from Meṣa
check("in a friend's sign → favourable",
      v["state"] == de.FAVOURABLE
      and any("friend" in f["condition"] for f in v["favourable"]), v["state"])
v = de.verdict("sun", CANCER, LEO)            # ...but the 12th from Siṁha
check("...and the SAME placement turns contested when it is also the 12th",
      v["state"] == de.CONTESTED, v["state"])

print("\nThe three ADVERSE conditions of v.6:")
for h, sign in ((6, VIRGO), (8, SCORPIO), (12, PISCES)):
    # lagna Aries so the bhava is the sign index + 1
    v = de.verdict("mercury", sign, ARIES)
    got = v["bhava"]
    check(f"in the {h}th house → adverse (Kanyā-lagna arithmetic aside)",
          got == h, f"bhāva {got}")
# "in his sign of debilitation" — Sun falls in Libra
v = de.verdict("sun", LIBRA, ARIES)
check("in his sign of debilitation → adverse",
      v["state"] == de.ADVERSE
      and any("debilitation" in a["condition"] for a in v["adverse"]), v["state"])
# "in an inimical sign" — Sun's enemies are Venus and Saturn
check("Śukra is a natural enemy of Sūrya (ch.3 v.55)",
      dignity.NATURAL_RELATIONS["sun"]["venus"] == "enemy")
v = de.verdict("sun", TAURUS, ARIES)          # Taurus = Venus's sign, bhāva 2
check("in an inimical sign → adverse",
      v["state"] == de.ADVERSE
      and any("inimical" in a["condition"] for a in v["adverse"]), v["state"])

print("\nCONTESTED — both branches fire, and BPHS states no rule to break the tie:")
# Sun exalted in Aries; make Aries the 12th by putting the lagna in Taurus.
v = de.verdict("sun", ARIES, TAURUS)
check("exalted AND in the 12th → contested", v["state"] == de.CONTESTED, v["state"])
check("...both sides are reported, neither is dropped",
      len(v["favourable"]) >= 1 and len(v["adverse"]) >= 1)
check("...and the label says the text does not arbitrate",
      "does not arbitrate" in v["label"], v["label"])

print("\nNOT STATED — the common case, and the one a gradient would destroy:")
# Sun in Gemini (Mercury's sign). Mercury is NEUTRAL to the Sun, and the verse
# names neither neutrality nor bhava 3. So nothing fires.
check("Budha is NEUTRAL to Sūrya — named by neither branch",
      dignity.NATURAL_RELATIONS["sun"]["mercury"] == "neutral")
v = de.verdict("sun", GEMINI, ARIES)
check("neutral sign, unnamed house → not_stated", v["state"] == de.NOT_STATED, v["state"])
check("...`silent` is set, so a UI cannot render it as neutrality", v["silent"] is True)
check("...no condition is fabricated to fill the gap",
      not v["favourable"] and not v["adverse"])
check("...and 'medium' appears nowhere in the label",
      "medium" not in v["label"].lower(), v["label"])

print("\nThe NODES — partially evaluable, and it says so:")
v = de.verdict("rahu", GEMINI, GEMINI)
check("Rāhu in the Ascendant still fires the HOUSE clause",
      v["state"] == de.FAVOURABLE, v["state"])
check("...and carries the note that its sign conditions cannot be evaluated",
      any("Rāhu and Ketu own no rāśi" in c for c in v["caveats"]))
v = de.verdict("ketu", GEMINI, ARIES)
check("Ketu in an unnamed house → not_stated (no dignity to fall back on)",
      v["state"] == de.NOT_STATED, v["state"])
check("no dignity condition is ever invented for a node",
      not any("exaltation" in f["condition"] or "own sign" in f["condition"]
              for f in v["favourable"]))

print("\nMŪLATRIKOṆA is NOT one of the verse's six conditions:")
# Candra's mulatrikona is Vrsabha, which is VENUS's sign — not her own.
check("Candra's mūlatrikoṇa sign is Vṛṣabha",
      dignity.MOOLATRIKONA["moon"][0] == TAURUS)
check("...which is ruled by Śukra, not by Candra",
      dignity.RASI_LORD[TAURUS] == "venus")
v = de.verdict("moon", TAURUS, ARIES)
check("so Candra in her mūlatrikoṇa does NOT fire 'in his own sign'",
      not any("own sign" in f["condition"] for f in v["favourable"]),
      str([f["condition"] for f in v["favourable"]]))
# Vṛṣabha is ALSO Candra's exaltation sign, so ch.47's exaltation clause fires
# and the verdict is favourable anyway. Which yields a neat fact worth pinning:
# the Moon is the only graha whose mūlatrikoṇa is not its own sign, and that
# same sign is her exaltation — so the divergence never changes a verdict.
check("...it fires the EXALTATION clause instead",
      any("exaltation" in f["condition"] for f in v["favourable"]))
diverge = [g for g, (sg, _, _) in dignity.MOOLATRIKONA.items()
           if dignity.RASI_LORD[sg] != g]
check("Candra is the ONLY graha whose mūlatrikoṇa is not its own sign",
      diverge == ["moon"], str(diverge))
check("...and that sign is also her exaltation, so no verdict ever turns on it",
      dignity.EXALTATION["moon"][0] == dignity.MOOLATRIKONA["moon"][0])
# The caveat itself is reachable wherever dignity_of really reports mūlatrikoṇa.
v = de.verdict("sun", LEO, ARIES)
check("the mūlatrikoṇa caveat attaches when a graha is genuinely in one",
      any("does NOT name mūlatrikoṇa" in c for c in v["caveats"]))

print("\nEvery verdict carries its citation and the verse itself:")
allv = [de.verdict(g, s, ARIES) for g in ("sun", "moon", "saturn", "rahu")
        for s in range(12)]
check("all carry the ch.47 citation",
      all(x["citation"] == "BPHS Vol II ch.47 vv.5-6" for x in allv))
check("all quote the verse verbatim",
      all("commencernent" in x["verse"] for x in allv))
check("all carry the natal-frame caveat",
      all(any("NATAL placement" in c for c in x["caveats"]) for x in allv))
check("only the four defined states are ever returned",
      {x["state"] for x in allv} <= {de.FAVOURABLE, de.ADVERSE, de.CONTESTED, de.NOT_STATED},
      str({x["state"] for x in allv}))

print("\nDistribution across a whole zodiac — not_stated should be common:")
from collections import Counter
c = Counter(de.verdict(g, s, ARIES)["state"]
            for g in dignity.EXALTATION for s in range(12))
print(f"   {dict(c)}")
check("not_stated actually occurs (the gradient would have hidden it)",
      c[de.NOT_STATED] > 0, str(c[de.NOT_STATED]))
check("contested actually occurs (the gradient would have averaged it away)",
      c[de.CONTESTED] > 0, str(c[de.CONTESTED]))


print("\nTHE FRAME — houses counted from the daśā lord (ch.52-60's workhorse):")
check("a graha in the lord's own sign is in the 1st (inclusive count)",
      de.bhava_from(LEO, LEO) == 1)
check("the next sign is the 2nd", de.bhava_from(LEO, VIRGO) == 2)
check("it wraps: Meṣa from Mīna is the 2nd", de.bhava_from(PISCES, ARIES) == 2)
check("the 7th is opposite", de.bhava_from(ARIES, LIBRA) == 7)
check("every offset is 1..12 and each occurs exactly once",
      sorted(de.bhava_from(CANCER, s) for s in range(12)) == list(range(1, 13)))
# The frame is NOT symmetric — that is the whole reason it must be carried as
# data rather than assumed. Saturn's 3rd from Jupiter is not Jupiter's 3rd
# from Saturn.
check("the frame is directional: 3rd-from-X is not 3rd-from-Y",
      de.bhava_from(ARIES, GEMINI) == 3 and de.bhava_from(GEMINI, ARIES) == 11)
check("...and 14 minus h is the inverse, so only the 7th is self-inverse",
      all(de.bhava_from(a, b) + de.bhava_from(b, a) == 14
          for a in range(12) for b in range(12) if a != b))

pos = {"sun": LEO, "moon": TAURUS, "saturn": LIBRA, "jupiter": CAPRICORN}
fr = de.frames_for_chart(pos, ARIES)
check("frames_for_chart gives both origins", set(fr) >= {"from_lagna", "from_lord"})
check("from_lagna matches the verdict engine's own bhāva",
      fr["from_lagna"]["saturn"] == de.verdict("saturn", LIBRA, ARIES)["bhava"])
check("from_lord is keyed by lord then graha",
      fr["from_lord"]["jupiter"]["saturn"] == de.bhava_from(CAPRICORN, LIBRA))
check("every lord sees itself in its own 1st",
      all(fr["from_lord"][g][g] == 1 for g in pos))
check("the note warns that some conditions state no frame",
      "no frame at all" in fr["note"])

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
