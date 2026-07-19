import sys
sys.path.insert(0, r"C:\proj\astrodev\api")
from drishti import (
    rasi_drishti, RASI_DRISHTI, rasi_drishti_chart, quality,
    graha_drishti, house_distance, graha_drishti_chart,
    GRAHA_DRISHTI_FRACTION, SPECIAL_DRISHTI_HOUSES, SPECIAL_DRISHTI_GAPS,
    SPECIAL_DRISHTI_GAPS_UNRESOLVED,
    drishti_angle, drishti_virupa, drishti_virupa_detail,
    general_drishti_virupa, RUPA,
    CANONICAL_GRAHAS, OCR_NUMERIC_REPAIRS, DRISHTI_DIRECTION_CORRECTED,
    SATURN_DEGREES_TO_ELAPSE_AMBIGUOUS, NODE_GRAHA_DRISHTI_UNVERIFIED,
    CH8_EXAMPLE_INCONSISTENT, RASI_DRISHTI_UNGRADED, _sign_of,
)

S = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
     "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
IX = {n: i for i, n in enumerate(S)}
fails = []
run = 0


def check(label, cond, detail=""):
    global run
    run += 1
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


def raises(exc, fn, *a, **kw):
    """True iff fn(*a) raises `exc`. Used to prove a bad input FAILS LOUDLY."""
    try:
        fn(*a, **kw)
    except exc:
        return True
    except Exception:
        return False
    return False


# ===========================================================================
print("BPHS Vol I ch.8 vv.1-3 - RASI DRISHTI, the book's OWN table")
print("(printed p.106 = ===PDFPAGE 105===). Reproduced from the printed table:")
# "Sign/occupant aspecting  ->  Sign/occupant aspected"
BOOK_CH8_TABLE = {
    "Aries":       ["Leo", "Scorpio", "Aquarius"],
    "Taurus":      ["Cancer", "Libra", "Capricorn"],
    "Gemini":      ["Virgo", "Sagittarius", "Pisces"],
    "Cancer":      ["Scorpio", "Aquarius", "Taurus"],
    "Leo":         ["Libra", "Capricorn", "Aries"],
    "Virgo":       ["Sagittarius", "Pisces", "Gemini"],
    "Libra":       ["Aquarius", "Taurus", "Leo"],
    "Scorpio":     ["Capricorn", "Aries", "Cancer"],
    "Sagittarius": ["Pisces", "Gemini", "Virgo"],
    "Capricorn":   ["Taurus", "Leo", "Scorpio"],
    "Aquarius":    ["Aries", "Cancer", "Libra"],
    "Pisces":      ["Gemini", "Virgo", "Sagittarius"],
}
for name, targets in BOOK_CH8_TABLE.items():
    got = sorted(RASI_DRISHTI[IX[name]])
    want = sorted(IX[t] for t in targets)
    check(f"{name} aspects {', '.join(targets)}", got == want,
          "got " + ", ".join(S[g] for g in got))

print("\nThe three clauses of vv.1-3, stated as invariants:")
check("every sign aspects exactly 3 signs",
      all(len(RASI_DRISHTI[s]) == 3 for s in range(12)))
check("no sign aspects itself",
      all(s not in RASI_DRISHTI[s] for s in range(12)))
check("movable aspects only FIXED signs",
      all(all(quality(t) == 1 for t in RASI_DRISHTI[s])
          for s in range(12) if quality(s) == 0))
check("fixed aspects only MOVABLE signs",
      all(all(quality(t) == 0 for t in RASI_DRISHTI[s])
          for s in range(12) if quality(s) == 1))
check("dual aspects only the other DUAL signs",
      all(all(quality(t) == 2 for t in RASI_DRISHTI[s])
          for s in range(12) if quality(s) == 2))
check("movable skips the ADJACENT fixed sign (Aries not Taurus)",
      not rasi_drishti(IX["Aries"], IX["Taurus"]))
check("fixed skips the ADJACENT movable sign (Taurus not Aries)",
      not rasi_drishti(IX["Taurus"], IX["Aries"]))

print("\nRasi drishti is SYMMETRIC (a consequence, not an assumption):")
asym = [(S[a], S[b]) for a in range(12) for b in range(12)
        if rasi_drishti(a, b) != rasi_drishti(b, a)]
check("sign A aspects B iff B aspects A", not asym, f"{len(asym)} asymmetric pairs")

print("\nBPHS gives rasi drishti NO strength grading - it is a boolean:")
check("rasi_drishti returns bool, never a fraction",
      all(isinstance(rasi_drishti(a, b), bool) for a in range(12) for b in range(12)))
check("chart builder marks it ungraded", rasi_drishti_chart({"sun": 0})["graded"] is False)
check("chart builder carries RASI_DRISHTI_UNGRADED for the API layer",
      rasi_drishti_chart({"sun": 0})["ungraded_note"] == RASI_DRISHTI_UNGRADED)

print("\nCounted from the SIGN - 'longitudes of the aspector and the aspected")
print("are ignorable' (note to vv.1-3). Degree within the sign cannot matter:")
ch = rasi_drishti_chart({"sun": 0.5, "moon": 29.9}, units="longitude")
check("two grahas 29deg apart in ONE sign cast identical rasi aspects",
      ch["casts"]["sun"]["signs"] == ch["casts"]["moon"]["signs"])
check("both land on Leo/Scorpio/Aquarius",
      sorted(ch["casts"]["sun"]["signs"]) == [IX["Leo"], IX["Scorpio"], IX["Aquarius"]])
check("v.5: an occupant of an aspected sign is itself aspected",
      "moon" in rasi_drishti_chart({"sun": 0, "moon": 4})["casts"]["sun"]["grahas"])
check("nodes take part in rasi drishti (the SIGN aspects - ch.8 v.5)",
      rasi_drishti_chart({"rahu": 0})["casts"]["rahu"]["signs"] != [])

# ===========================================================================
print("\n\nBPHS Vol I ch.26 vv.2-5 - GRAHA DRISHTI, sign-counted")
print("(printed p.255 = ===PDFPAGE 254===).")
print("'3rd and 10th, 5th and 9th, 4th and 8th and lastly 7th ... 1/4, 1/2, 3/4 and full':")
BOOK_GRADES = {3: 0.25, 10: 0.25, 5: 0.50, 9: 0.50, 4: 0.75, 8: 0.75, 7: 1.00}
for h, f in sorted(BOOK_GRADES.items()):
    check(f"house {h} -> {f}", GRAHA_DRISHTI_FRACTION[h] == f,
          str(GRAHA_DRISHTI_FRACTION.get(h)))
for h in (1, 2, 6, 11, 12):
    check(f"house {h} -> no aspect (not named by the sloka)",
          graha_drishti(0, (0 + h - 1) % 12, "sun") == 0.0)

print("\nThe grading is NOT monotonic in house number - 4th/8th beat 5th/9th:")
check("4th (3/4) outranks 5th (1/2)",
      GRAHA_DRISHTI_FRACTION[4] > GRAHA_DRISHTI_FRACTION[5], "0.75 > 0.50")
check("8th (3/4) outranks 9th (1/2)",
      GRAHA_DRISHTI_FRACTION[8] > GRAHA_DRISHTI_FRACTION[9], "0.75 > 0.50")

print("\n'All planets aspect the 7th fully':")
for g in CANONICAL_GRAHAS:
    check(f"{g} aspects the 7th fully", graha_drishti(0, 6, g) == 1.0)

print("\n'Saturn, Jupiter and Mars have special aspects respectively on")
print("3rd and 10th, 5th and 9th, and 4th and 8th' (special = FULL):")
for g, houses in SPECIAL_DRISHTI_HOUSES.items():
    for h in houses:
        check(f"{g} aspects the {h}th fully (special)",
              graha_drishti(0, (h - 1) % 12, g) == 1.0)
        check(f"  ... where a general graha gets only {BOOK_GRADES[h]}",
              graha_drishti(0, (h - 1) % 12, "sun") == BOOK_GRADES[h])
print("  and nobody else gets those specials:")
check("Sun does NOT aspect the 3rd fully", graha_drishti(0, 2, "sun") == 0.25)
check("Mars does NOT aspect the 3rd fully", graha_drishti(0, 2, "mars") == 0.25)
check("Saturn does NOT aspect the 4th fully", graha_drishti(0, 3, "saturn") == 0.75)
check("Jupiter does NOT aspect the 4th fully", graha_drishti(0, 3, "jupiter") == 0.75)
check("Mars does NOT aspect the 5th fully", graha_drishti(0, 4, "mars") == 0.50)

print("\nHouse counting is whole-sign and wraps:")
check("Aries->Aries is house 1", house_distance(0, 0) == 1)
check("Aries->Libra is house 7", house_distance(0, 6) == 7)
check("Scorpio->Capricorn is house 3", house_distance(7, 9) == 3)
check("Pisces->Gemini is house 4 (wraps)", house_distance(11, 2) == 4)
check("Saturn in Scorpio aspects Capricorn fully (3rd)",
      graha_drishti(7, 9, "saturn") == 1.0)
check("graha drishti is ASYMMETRIC (Saturn 3rd vs its own 11th)",
      graha_drishti(0, 2, "saturn") == 1.0 and graha_drishti(2, 0, "saturn") == 0.0)

# ===========================================================================
print("\n\nA MISTYPED GRAHA KEY MUST RAISE, NOT DEGRADE.")
print("These all used to fall through to the general rule and return a")
print("plausible WEAKER aspect - a confident wrong answer about a real chart:")
check("graha_drishti('Saturn') raises (wrong case)",
      raises(ValueError, graha_drishti, 0, 2, "Saturn"),
      "used to return 0.25 instead of 1.0")
check("graha_drishti('sturn') raises (typo)",
      raises(ValueError, graha_drishti, 0, 2, "sturn"))
check("graha_drishti('lagna') raises (not a graha)",
      raises(ValueError, graha_drishti, 0, 2, "lagna"))
check("drishti_virupa('Saturn') raises",
      raises(ValueError, drishti_virupa, 0.0, 60.0, "Saturn"),
      "used to return 15.0 instead of 60.0")
check("graha_drishti_chart with a bad key raises",
      raises(ValueError, graha_drishti_chart, {"Saturn": 0}))
check("rasi_drishti_chart with a bad key raises",
      raises(ValueError, rasi_drishti_chart, {"ascendant": 0}))
check("all nine canonical keys are accepted by both entry points",
      all(isinstance(graha_drishti(0, 6, g), float)
          and isinstance(drishti_virupa(0.0, 180.0, g), float)
          for g in CANONICAL_GRAHAS))
check("CANONICAL_GRAHAS is exactly the navagraha, lower case",
      CANONICAL_GRAHAS == ("sun", "moon", "mars", "mercury", "jupiter",
                           "venus", "saturn", "rahu", "ketu"))

print("\nA BARE SCALAR MUST NOT MEAN TWO THINGS. _sign_of used to resolve")
print("sign-index vs longitude by Python TYPE: 100 -> Leo but 100.0 -> Cancer,")
print("so an upstream int() silently rotated the whole chart:")
check("_sign_of(100) now RAISES instead of silently meaning sign 4",
      raises(ValueError, _sign_of, 100))
check("_sign_of(100.0) == 3 - a float >= 12 can ONLY be a longitude",
      _sign_of(100.0) == 3)
check("_sign_of(5.0) RAISES - a float in [0,12) is undecidable",
      raises(ValueError, _sign_of, 5.0))
check("_sign_of(5) == 5 - a small int is a sign index", _sign_of(5) == 5)
check("units='sign' forces the sign reading: 100 -> 4",
      _sign_of(100, "sign") == 4)
check("units='longitude' forces the longitude reading: 100 -> 3",
      _sign_of(100, "longitude") == 3)
check("units='longitude' on the SAME value gives a DIFFERENT sign than 'sign'",
      _sign_of(100, "sign") != _sign_of(100, "longitude"),
      "which is exactly why the overload was unsafe")
check("units='sign' rejects a fractional index",
      raises(ValueError, _sign_of, 5.5, "sign"))
check("an unknown units value raises", raises(ValueError, _sign_of, 5, "degrees"))
check("charts honour units= end to end",
      graha_drishti_chart({"sun": 100}, units="sign")["casts"]["sun"]["from_sign"] == 4
      and graha_drishti_chart({"sun": 100}, units="longitude")
          ["casts"]["sun"]["from_sign"] == 3)


class _FakeGraha:
    def __init__(self, rasi):
        self.rasi = rasi


class _FakeLon:
    def __init__(self, longitude):
        self.longitude = longitude


check("an object with .rasi is read as a sign index (units irrelevant)",
      _sign_of(_FakeGraha(7)) == 7 and _sign_of(_FakeGraha(7), "longitude") == 7)
check("an object with .longitude is read as a longitude",
      _sign_of(_FakeLon(100.0)) == 3)
check("a string position raises TypeError", raises(TypeError, _sign_of, "Aries"))
check("True is not a sign index", raises(TypeError, _sign_of, True))

# ===========================================================================
print("\n\nBPHS Vol I ch.26 vv.6-8 - the DEGREE engine, against the book's own")
print("printed 'Speculum of Aspectual Values' (printed pp.258-263 =")
print("===PDFPAGE 257-262===). One check per entry, straight off the page:")
BOOK_SPECULUM = [                      # (deg, min, virupa)
    (30, 0, 0.00), (30, 30, 0.25), (31, 0, 0.50), (32, 0, 1.00), (35, 0, 2.50),
    (40, 0, 5.00), (45, 0, 7.50), (50, 0, 10.00), (55, 0, 12.50), (59, 30, 14.75),
    (60, 0, 15.00), (60, 30, 15.50), (61, 0, 16.00), (64, 0, 19.00), (65, 0, 20.00),
    (70, 0, 25.00), (75, 0, 30.00), (77, 0, 32.00), (80, 0, 35.00), (85, 0, 40.00),
    (89, 0, 44.00), (90, 0, 45.00), (90, 30, 44.75), (91, 0, 44.50), (95, 0, 42.50),
    (100, 0, 40.00), (105, 30, 37.25), (110, 0, 35.00), (115, 0, 32.50),
    (119, 0, 30.50), (120, 0, 30.00), (120, 30, 29.50), (121, 0, 29.00),
    (125, 0, 25.00), (130, 0, 20.00), (135, 0, 15.00), (140, 0, 10.00),
    (145, 0, 5.00), (149, 30, 0.50), (150, 0, 0.00), (150, 30, 1.00),
    (151, 0, 2.00), (155, 0, 10.00), (160, 0, 20.00), (165, 0, 30.00),
    (170, 0, 40.00), (175, 0, 50.00), (179, 30, 59.00), (180, 0, 60.00),
    (180, 30, 59.75), (181, 0, 59.50), (185, 0, 57.50), (190, 0, 55.00),
    (200, 0, 50.00), (205, 0, 47.50), (209, 30, 45.25), (210, 0, 45.00),
    (215, 0, 42.50), (220, 0, 40.00), (230, 0, 35.00), (239, 30, 30.25),
    (240, 0, 30.00), (250, 0, 25.00), (255, 0, 22.50), (260, 0, 20.00),
    (261, 0, 19.50),
]
# The one entry whose printed digit was repaired: the page prints "59:30 14.7J".
SPECULUM_OCR_REPAIRED = {(59, 30)}
matched = 0
for d, m, v in BOOK_SPECULUM:
    got = general_drishti_virupa(d + m / 60.0)
    ok = abs(got - v) < 1e-9
    matched += ok
    tag = "  [OCR '14.7J' read as 14.75]" if (d, m) in SPECULUM_OCR_REPAIRED else ""
    check(f"speculum {d:>3}:{m:02d} -> {v:5.2f} virupa{tag}", ok, f"got {got:.4f}")
check(f"...and that is {len(BOOK_SPECULUM)}/{len(BOOK_SPECULUM)} printed entries reproduced",
      matched == len(BOOK_SPECULUM), f"{matched} matched")

print("\n'Needless to mention there is no aspectual value if the angle is")
print("between 300 and 30 degrees' - swept at 0.25deg, reported by count:")
dead_lo = [a / 4.0 for a in range(0, 120) if general_drishti_virupa(a / 4.0) != 0.0]
dead_hi = [a / 4.0 for a in range(1200, 1441) if general_drishti_virupa(a / 4.0) != 0.0]
check(f"120/120 samples in 0-30deg are zero", not dead_lo, f"nonzero at {dead_lo[:3]}")
check(f"241/241 samples in 300-360deg are zero", not dead_hi, f"nonzero at {dead_hi[:3]}")
for seam in (60.0, 90.0, 120.0, 150.0, 180.0, 300.0):
    lo = general_drishti_virupa(seam - 1e-7)
    hi = general_drishti_virupa(seam)
    check(f"general rule is continuous at the {seam:5.1f}deg seam",
          abs(lo - hi) < 1e-5, f"{lo:.4f} vs {hi:.4f}")
check("maximum is exactly one Rupa, at 180deg",
      max(general_drishti_virupa(a / 10.0) for a in range(3600)) == RUPA
      and general_drishti_virupa(180.0) == RUPA)

# ===========================================================================
print("\n\nTHE KEYSTONE: vv.6-12 evaluated at each house CUSP must reproduce")
print("vv.2-5 exactly. Two independent passages of the same chapter, one in")
print("houses and one in degrees - they are the same doctrine or the OCR lied:")
for h in range(1, 13):
    cusp = (h - 1) * 30.0
    virupa = general_drishti_virupa(cusp)
    want = GRAHA_DRISHTI_FRACTION.get(h, 0.0)
    check(f"house {h:>2} (cusp {cusp:5.0f}deg) -> {virupa:5.2f} virupa = {virupa/RUPA:.2f} rupa"
          f"  vs sloka {want:.2f}",
          abs(virupa / RUPA - want) < 1e-12)

print("\n...and each special graha reaches exactly ONE RUPA on its own houses:")
for g, houses in SPECIAL_DRISHTI_HOUSES.items():
    for h in houses:
        cusp = (h - 1) * 30.0
        v = drishti_virupa(0.0, cusp, g)
        check(f"{g:<8} at the {h:>2}th cusp ({cusp:3.0f}deg) -> {v:.2f} virupa (full)",
              abs(v - RUPA) < 1e-9)
print("  ...and the 7th, for a graha with no special aspect:")
check("Sun at the 7th cusp (180deg) -> 60.00 virupa",
      abs(drishti_virupa(0.0, 180.0, "sun") - RUPA) < 1e-9)
check("Sun's specials do not exist: 3rd cusp -> 15 virupa (a quarter)",
      abs(drishti_virupa(0.0, 60.0, "sun") - 15.0) < 1e-9)

print("\nDirection of the subtraction. v.6 as printed says 'deduct the aspected")
print("from the aspector'; vv.11-12 say the reverse. Only the reverse works,")
print("and the departure is named in DRISHTI_DIRECTION_CORRECTED:")
check("DRISHTI_DIRECTION_CORRECTED names the printed reading it overrules",
      "aspected − aspector" in DRISHTI_DIRECTION_CORRECTED
      and "v.6" in DRISHTI_DIRECTION_CORRECTED)
check("drishti_angle is (aspected - aspector) mod 360",
      drishti_angle(10.0, 70.0) == 60.0 and drishti_angle(70.0, 10.0) == 300.0)
check("Saturn -> a point 60deg AHEAD (his 3rd) = full",
      abs(drishti_virupa(10.0, 70.0, "saturn") - RUPA) < 1e-9)
check("the reversed reading would give Saturn's 3rd ZERO",
      drishti_virupa(70.0, 10.0, "saturn") == 0.0)
check("Jupiter -> a point 120deg AHEAD (his 5th) = full",
      abs(drishti_virupa(10.0, 130.0, "jupiter") - RUPA) < 1e-9)
check("Mars -> a point 90deg AHEAD (his 4th) = full",
      abs(drishti_virupa(10.0, 100.0, "mars") - RUPA) < 1e-9)
check("every cast carries the correction note for the API layer",
      DRISHTI_DIRECTION_CORRECTED in drishti_virupa_detail(0.0, 60.0, "saturn")["notes"])

print("\nSaturn v.10's 'degrees to elapse' is AMBIGUOUS. We read it as degrees")
print("REMAINING, (300-a)*2. The rival reading, (a-270)*2, is refuted by")
print("continuity - and the flag is carried in the payload, not buried:")
check("SATURN_DEGREES_TO_ELAPSE_AMBIGUOUS names BOTH readings",
      "(300 − a)" in SATURN_DEGREES_TO_ELAPSE_AMBIGUOUS
      and "(a − 270)" in SATURN_DEGREES_TO_ELAPSE_AMBIGUOUS)
check("the flag is attached to exactly the 270-300deg Saturn window",
      SATURN_DEGREES_TO_ELAPSE_AMBIGUOUS
      in drishti_virupa_detail(0.0, 285.0, "saturn")["notes"]
      and SATURN_DEGREES_TO_ELAPSE_AMBIGUOUS
      not in drishti_virupa_detail(0.0, 255.0, "saturn")["notes"]
      and SATURN_DEGREES_TO_ELAPSE_AMBIGUOUS
      not in drishti_virupa_detail(0.0, 285.0, "sun")["notes"])
# The refutation itself, computed rather than asserted.
_elapsed = lambda a: (a - 270.0) * 2.0
check("REMAINING joins the 240-270 segment at 270deg (60 -> 60)",
      abs(drishti_virupa(0.0, 270.0 - 1e-7, "saturn") - 60.0) < 1e-4
      and abs(drishti_virupa(0.0, 270.0, "saturn") - 60.0) < 1e-4)
check("ELAPSED would open a 60-virupa cliff at 270deg",
      abs(60.0 - _elapsed(270.0)) == 60.0, "60 -> 0")
check("REMAINING hands back to the general rule at 300deg (0 -> 0)",
      abs(drishti_virupa(0.0, 300.0 - 1e-7, "saturn")) < 1e-4
      and general_drishti_virupa(300.0) == 0.0)
check("ELAPSED would open a second cliff at 300deg",
      abs(_elapsed(300.0 - 1e-7) - general_drishti_virupa(300.0)) > 59.0,
      "60 -> 0")
check("ELAPSED would peak Saturn on his 11th (300deg), not the 10th the sloka names",
      max(range(2700, 3000), key=lambda i: _elapsed(i / 10.0)) / 10.0 > 299.0)

print("\nThe special slokas hand back to the general rule at their seams:")
for g, seams in (("saturn", (30.0, 60.0, 90.0, 240.0, 270.0, 300.0)),
                 ("mars", (60.0, 90.0, 120.0, 240.0)),
                 ("jupiter", (90.0, 120.0, 210.0, 240.0))):
    for s in seams:
        lo = drishti_virupa(0.0, s - 1e-7, g)
        hi = drishti_virupa(0.0, s, g)
        check(f"{g:<8} continuous at {s:5.1f}deg", abs(lo - hi) < 1e-5,
              f"{lo:.4f} vs {hi:.4f}")

print("\n...except at three angles, where the TEXT itself does not join up.")
print("Flagged in SPECIAL_DRISHTI_GAPS, not silently smoothed:")
check("SPECIAL_DRISHTI_GAPS_UNRESOLVED says filling them would invent text",
      "inventing" in SPECIAL_DRISHTI_GAPS_UNRESOLVED
      or "smoothed" in SPECIAL_DRISHTI_GAPS_UNRESOLVED)
for g, angle, below, at in SPECIAL_DRISHTI_GAPS:
    lo = drishti_virupa(0.0, angle - 1e-7, g)
    hi = drishti_virupa(0.0, angle, g)
    check(f"{g:<8} at {angle:5.1f}deg jumps {below:.0f} -> {at:.0f} virupa",
          abs(lo - below) < 1e-4 and abs(hi - at) < 1e-4,
          f"got {lo:.2f} -> {hi:.2f}")
found = sorted((g, a) for g in ("saturn", "mars", "jupiter")
               for a in [i / 10.0 for i in range(3600)]
               if abs(drishti_virupa(0.0, a, g)
                      - drishti_virupa(0.0, a - 0.1, g)) > 1.6)
want = sorted((g, a) for g, a, _, _ in SPECIAL_DRISHTI_GAPS)
check(f"no OTHER discontinuity hides in 3 x 3600 sampled angles",
      found == want, f"found {found}")

print("\nNo aspect value anywhere exceeds one Rupa (Santhanam's 'simple formula'")
print("note would give Saturn 90 virupas at 90deg - that is why we follow the sloka):")
over = [(g, a / 10.0) for g in CANONICAL_GRAHAS
        for a in range(3600) if drishti_virupa(0.0, a / 10.0, g) > RUPA + 1e-9]
check(f"all 9 grahas x 3600 angles stay within 0..60 virupas", not over,
      f"{len(over)} overshoots")
check("Santhanam's shortcut really would overshoot at 90deg (45+45=90 > 60)",
      general_drishti_virupa(90.0) + 45.0 > RUPA,
      f"{general_drishti_virupa(90.0)} + 45 = {general_drishti_virupa(90.0) + 45.0}")

print("\nThe one repaired digit in that note is declared, not silently fixed:")
mars_repair = [r for r in OCR_NUMERIC_REPAIRS if "210-249" in r["printed"]]
check("OCR_NUMERIC_REPAIRS records the printed '210-249' -> read '210-240'",
      len(mars_repair) == 1 and mars_repair[0]["read_as"] == "210-240 degrees")
check("...and states the repair does not touch the computed path",
      all(r["affects_computation"] is False for r in OCR_NUMERIC_REPAIRS))
check("...and every repair cites both page conventions",
      all("printed p." in r["where"] and "PDFPAGE" in r["where"]
          for r in OCR_NUMERIC_REPAIRS))

# ===========================================================================
print("\n\nChart builders:")
# Saturn in Aries, Mars in Cancer, Jupiter in Leo, Sun in Libra, Rahu in Gemini.
pos = {"saturn": IX["Aries"], "mars": IX["Cancer"], "jupiter": IX["Leo"],
       "sun": IX["Libra"], "rahu": IX["Gemini"], "ketu": IX["Sagittarius"]}
gd = graha_drishti_chart(pos)
check("graha chart is labelled sign-counted", gd["counted_from"] == "sign")
check("graha chart cites both page conventions",
      "p.255" in gd["citation"] and "PDFPAGE 254" in gd["citation"])
check("nodes excluded from graha drishti by default",
      "rahu" not in gd["casts"] and "ketu" not in gd["casts"])
check("...and the payload then claims all_verified", gd["all_verified"] is True
      and gd["unverified"] == [])
check("Saturn(Aries) casts on Gemini/Capricorn fully (3rd & 10th)",
      gd["casts"]["saturn"]["signs"][IX["Gemini"]] == 1.0
      and gd["casts"]["saturn"]["signs"][IX["Capricorn"]] == 1.0)
check("Saturn(Aries) reaches Rahu in Gemini at full strength",
      gd["casts"]["saturn"]["grahas"]["rahu"] == 1.0)
check("Saturn(Aries) aspects Libra fully (7th)",
      gd["casts"]["saturn"]["signs"][IX["Libra"]] == 1.0)
check("Jupiter(Leo) casts on Sagittarius/Aries fully (5th & 9th)",
      gd["casts"]["jupiter"]["signs"][IX["Sagittarius"]] == 1.0
      and gd["casts"]["jupiter"]["signs"][IX["Aries"]] == 1.0)
check("Mars(Cancer) casts on Libra/Aquarius fully (4th & 8th)",
      gd["casts"]["mars"]["signs"][IX["Libra"]] == 1.0
      and gd["casts"]["mars"]["signs"][IX["Aquarius"]] == 1.0)
check("Sun(Libra) casts only 3,4,5,7,8,9,10 - seven signs",
      len(gd["casts"]["sun"]["signs"]) == 7)
check("received view is the inverse of the cast view",
      all(gd["received"]["signs"][s][g] == f
          for g, c in gd["casts"].items() for s, f in c["signs"].items()))
check("Saturn appears among what Rahu RECEIVES",
      gd["received"]["grahas"]["rahu"]["saturn"] == 1.0)
gdn = graha_drishti_chart(pos, include_nodes=True)
check("include_nodes=True computes them but flags them unverified",
      "rahu" in gdn["casts"] and gdn["casts"]["rahu"]["verified"] is False
      and gdn["casts"]["saturn"]["verified"] is True)
check("...and the payload drops all_verified and carries the reason",
      gdn["all_verified"] is False
      and gdn["unverified"] == [NODE_GRAHA_DRISHTI_UNVERIFIED])

rd = rasi_drishti_chart(pos)
check("rasi chart: Aries(Saturn) aspects Leo/Scorpio/Aquarius",
      sorted(rd["casts"]["saturn"]["signs"])
      == sorted([IX["Leo"], IX["Scorpio"], IX["Aquarius"]]))
check("rasi chart: Saturn(Aries) therefore aspects Jupiter(Leo)",
      "jupiter" in rd["casts"]["saturn"]["grahas"])
check("rasi chart: and Jupiter(Leo) aspects Saturn(Aries) back (symmetric)",
      "saturn" in rd["casts"]["jupiter"]["grahas"])
check("rasi chart: nodes are included as ordinary occupants",
      "rahu" in rd["casts"] and "ketu" in rd["casts"])
check("rasi chart: nodal rasi drishti is NOT flagged (the SIGN aspects)",
      rd["all_verified"] is True)
check("rasi chart: Gemini(Rahu) aspects Sagittarius(Ketu), both dual",
      "ketu" in rd["casts"]["rahu"]["grahas"])
check("the two doctrines genuinely differ on this chart",
      set(rd["casts"]["saturn"]["signs"]) != set(gd["casts"]["saturn"]["signs"]))

# ===========================================================================
print("\n\nTHE CH.8 WORKED EXAMPLE (Santhanam's notes to vv.4-5, printed")
print("pp.107-108 = ===PDFPAGE 106-107===). Its horoscope is a DIAGRAM and is")
print("absent from the extracted text, but five of the six clauses are jointly")
print("satisfiable and pin a placement down. Reconstructed, then run through")
print("rasi_drishti_chart() - the chart builder, not a restatement of the rule:")
print("  (a) 'Mars aspects Saturn, Moon and the nodes.'")
print("  (b) 'Venus, the Sun and Mercury aspect none.'")
print("  (c) 'Jupiter aspects the Moon, Ketu, Sun and Venus.'")
print("  (d) 'Saturn and Rahu aspect Mars.'")
print("  (e) 'Moon aspects Mars and Jupiter.'")
print("  (f) 'Ketu aspects Mars and Jupiter.'")
print()
print("Derivation: the nodes are 6 signs apart and (d)/(a) do not have them")
print("aspecting each other, so they are not dual -> movable or fixed. Mars")
print("aspects both nodes plus Moon and Saturn, so Mars is in the opposite")
print("class and those four are in the same class as each other. (c) has")
print("Jupiter missing Saturn AND Rahu, but a sign skips only ONE sign, so")
print("Saturn and Rahu share a sign; likewise (a) has Mars missing Sun and")
print("Venus, so Sun and Venus share the sign Mars skips. Mercury aspects")
print("nobody, and is within a sign of the Sun, so Mercury sits alone in the")
print("dual sign next to them. One such placement:")
CH8_RECONSTRUCTION = {
    "saturn": IX["Aries"],     "rahu":   IX["Aries"],
    "jupiter": IX["Taurus"],
    "mercury": IX["Gemini"],
    "sun":    IX["Cancer"],    "venus":  IX["Cancer"],
    "mars":   IX["Leo"],
    "ketu":   IX["Libra"],
    "moon":   IX["Capricorn"],
}
for g, s in sorted(CH8_RECONSTRUCTION.items()):
    print(f"    {g:<8} {S[s]}")
check("the reconstruction places all nine grahas",
      sorted(CH8_RECONSTRUCTION) == sorted(CANONICAL_GRAHAS))
check("Rahu and Ketu are 6 signs apart, as they must be",
      (CH8_RECONSTRUCTION["ketu"] - CH8_RECONSTRUCTION["rahu"]) % 12 == 6)
check("Mercury is within one sign of the Sun, as it must be",
      min((CH8_RECONSTRUCTION["mercury"] - CH8_RECONSTRUCTION["sun"]) % 12,
          (CH8_RECONSTRUCTION["sun"] - CH8_RECONSTRUCTION["mercury"]) % 12) <= 1)

ex = rasi_drishti_chart(CH8_RECONSTRUCTION)
casts = {g: set(c["grahas"]) for g, c in ex["casts"].items()}

print("\n  Five of the six clauses come out EXACTLY right - as complete lists,")
print("  not merely as subsets:")
CH8_CLAUSES = [
    ("a", "mars", {"saturn", "moon", "rahu", "ketu"}),
    ("c", "jupiter", {"moon", "ketu", "sun", "venus"}),
    ("d/saturn", "saturn", {"mars"}),
    ("d/rahu", "rahu", {"mars"}),
    ("e", "moon", {"mars", "jupiter"}),
    ("f", "ketu", {"mars", "jupiter"}),
]
for tag, g, want_set in CH8_CLAUSES:
    check(f"({tag}) {g} aspects exactly {', '.join(sorted(want_set))}",
          casts[g] == want_set, f"got {sorted(casts[g])}")

print("\n  ...and clause (b) breaks, in precisely the place symmetry forces it")
print("  to and nowhere else:")
check("(b) holds for Mercury - he really does aspect nobody",
      casts["mercury"] == set())
check("(b) FAILS for the Sun: (c) put Jupiter on him, so he aspects Jupiter back",
      casts["sun"] == {"jupiter"}, f"got {sorted(casts['sun'])}")
check("(b) FAILS for Venus, for the same reason",
      casts["venus"] == {"jupiter"}, f"got {sorted(casts['venus'])}")
check("no reading of the horoscope can rescue (b): rasi drishti is symmetric,",
      all(rasi_drishti(b, a) for a in range(12) for b in RASI_DRISHTI[a]),
      "so 'Jupiter aspects X' always implies 'X aspects Jupiter'")
check("CH8_EXAMPLE_INCONSISTENT records the contradiction for the API layer",
      "(b)" in CH8_EXAMPLE_INCONSISTENT and "(c)" in CH8_EXAMPLE_INCONSISTENT)

print("\n  The reconstruction is A witness, not THE horoscope - the book's")
print("  diagram is not in the text. It is used only to show the five clauses")
print("  are jointly realisable and that (b) is the one that must give way:")
check("the fixture is not claimed to be the book's own chart",
      "diagram" in CH8_EXAMPLE_INCONSISTENT
      and "cannot arbitrate" in CH8_EXAMPLE_INCONSISTENT)

print(f"\n{run} checks run, {run - len(fails)} passed, {len(fails)} failed.")
print("ALL PASS" if not fails else f"FAILURES ({len(fails)}): {fails}")
sys.exit(1 if fails else 0)
