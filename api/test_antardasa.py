"""The 81-cell antardaśā matrix and its condition-firing engine.

Run: python api/test_antardasa.py

These tests are mostly about what the engine REFUSES to do. The corpus's
frames are stated only two times in three, and its valence words only about one
branch in five, so the failure modes worth pinning are: assuming a frame,
inferring polarity, inheriting a missing clause from a sibling cell, and
silently dropping what could not be evaluated.
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import antardasa as ad
import antardasa_rules as rules

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


LORDS = list(rules.CHAPTER_OF)
ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO = 0, 1, 2, 3, 4, 5
LIBRA, SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES = 6, 7, 8, 9, 10, 11

print("The matrix is complete and nothing was synthesised to fill it:")
check("81 cells — 9 mahādaśās x 9 antardaśās", len(rules.MATRIX) == 81, str(len(rules.MATRIX)))
check("every (mahā, antar) pair of the nine lords is present",
      all((m, a) in rules.MATRIX for m in LORDS for a in LORDS))
check("559 conditions carried over from the mine",
      sum(len(v["conditions"]) for v in rules.MATRIX.values()) == 559)
check("every condition carries a quote", all(
    c.get("quote") for v in rules.MATRIX.values() for c in v["conditions"]))
check("every condition carries a source tag of sloka or note", all(
    c.get("source") in ("sloka", "note")
    for v in rules.MATRIX.values() for c in v["conditions"]))
check("every cell names its verses", all(v["verses"] for v in rules.MATRIX.values()))

print("\nABSENCES are preserved, not inherited from a sibling cell:")
no_maraka = [k for k, v in rules.MATRIX.items() if v["maraka"] is None]
check("some cells genuinely have no death clause", len(no_maraka) > 0, str(len(no_maraka)))
check("...including ch.52's Jupiter cell, the only one in its chapter",
      ("sun", "jupiter") in no_maraka, str([k for k in no_maraka if k[0] == "sun"]))
check("some cells have no remedy either",
      any(v["remedy"] is None for v in rules.MATRIX.values()))

print("\nThe FRAME census — one house condition in three has no anchor:")
fr = Counter(c["frame"] for v in rules.MATRIX.values() for c in v["conditions"])
house = fr["from_lagna"] + fr["from_dasa_lord"] + fr["from_moon"] + fr["unstated"]
check("frames are only ever the five known values",
      set(fr) <= {"from_lagna", "from_dasa_lord", "from_moon", "unstated", "not_a_house"},
      str(set(fr)))
check("about a third of house conditions are UNSTATED",
      0.28 < fr["unstated"] / house < 0.38,
      f'{fr["unstated"]}/{house} = {fr["unstated"]/house:.0%}')
check("from_moon is vanishingly rare (1 in the whole corpus)",
      fr["from_moon"] == 1, str(fr["from_moon"]))
check("from_dasa_lord is a major frame, not a curiosity",
      fr["from_dasa_lord"] > 100, str(fr["from_dasa_lord"]))

print("\nHouse-group parsing:")
check("'kendra' expands to 1,4,7,10", ad.parse_houses("kendra") == (1, 4, 7, 10))
check("'trikona' expands to 1,5,9", ad.parse_houses("trikona") == (1, 5, 9))
check("a mixed list unions correctly",
      ad.parse_houses("kendra,5,9,11,3,2") == (1, 2, 3, 4, 5, 7, 9, 10, 11),
      str(ad.parse_houses("kendra,5,9,11,3,2")))
# Refusing the WHOLE spec, rather than salvaging its legible parts, is the
# point. A partial parse is worse than none: it yields a confident, incomplete
# answer about a real person's chart.
check("an out-of-range house poisons the spec rather than being dropped",
      ad.parse_houses("6,99,0") is None, str(ad.parse_houses("6,99,0")))
check("an unreadable spec returns None, not an empty match",
      ad.parse_houses("") is None and ad.parse_houses("the6rh") is None,
      str(ad.parse_houses("the6rh")))
# The scan's characteristic damage: 'l' for '1'. These are recoverable by eye
# and must NOT be recovered by code.
check("OCR-damaged numerals refuse the whole list, not just their own token",
      ad.parse_houses("8th, llth, 12th") is None,
      str(ad.parse_houses("8th, llth, 12th")))
check("...so the 11th is never silently dropped to leave (8, 12)",
      ad.parse_houses("8th, llth, 12th") != (8, 12))
check("a clean ordinal list still parses", ad.parse_houses("6th, 8th, 12th") == (6, 8, 12))

print("\nTHE CARDINAL REFUSAL — an unstated frame is never resolved:")
uns = {"predicate": "in a kendra", "houses": "kendra", "frame": "unstated",
       "frame_quote": "", "polarity": "none", "quote": "x", "source": "sloka"}
r = ad.evaluate_condition(uns, antar_sign=ARIES, lagna=ARIES,
                          maha_lord_sign=ARIES, moon_sign=ARIES)
check("an unstated frame is UNAVAILABLE even when every origin would fire",
      r["state"] == ad.UNAVAILABLE, r["state"])
check("...and says why, naming the missing 'from' clause",
      "no reference frame" in r["reason"])
# The same predicate WITH a frame must compute — otherwise the refusal above is
# just a broken evaluator rather than a principled one.
framed = {**uns, "frame": "from_dasa_lord", "frame_quote": "from the lord of the Dasa"}
r2 = ad.evaluate_condition(framed, antar_sign=ARIES, lagna=LEO,
                           maha_lord_sign=ARIES, moon_sign=LEO)
check("the SAME predicate with a stated frame fires", r2["state"] == ad.FIRED, r2["state"])
check("...and reports the actual bhāva it computed", r2["actual_bhava"] == 1)

print("\nThe frame is load-bearing: the same clause differs by origin.")
# Antar lord in Meṣa; lagna Meṣa; mahā lord in Karka. "in a kendra" from the
# lagna fires (1st); from the daśā lord it does not (10th is a kendra, but the
# antar lord is in the 10th from Karka... so it does). Use the 5th instead.
c5 = {"predicate": "in the 5th", "houses": "5", "frame": "from_lagna",
      "frame_quote": "from the Ascendant", "polarity": "none",
      "quote": "x", "source": "sloka"}
a = ad.evaluate_condition(c5, antar_sign=LEO, lagna=ARIES,
                          maha_lord_sign=CANCER, moon_sign=ARIES)
b = ad.evaluate_condition({**c5, "frame": "from_dasa_lord"}, antar_sign=LEO,
                          lagna=ARIES, maha_lord_sign=CANCER, moon_sign=ARIES)
check("5th from the lagna fires for this placement", a["state"] == ad.FIRED, a["state"])
check("...and the identical clause from the daśā lord does NOT",
      b["state"] == ad.NOT_FIRED, f'{b["state"]} (bhāva {b["actual_bhava"]})')

print("\nPolarity is carried but NEVER becomes a state:")
pol = {"predicate": "in the 6th", "houses": "6", "frame": "from_lagna",
       "frame_quote": "from the Ascendant", "polarity": "adverse",
       "polarity_word": "evil", "quote": "x", "source": "sloka"}
r = ad.evaluate_condition(pol, antar_sign=VIRGO, lagna=ARIES,
                          maha_lord_sign=ARIES, moon_sign=ARIES)
check("a fired condition's state is 'fired', never its polarity",
      r["state"] == ad.FIRED, r["state"])
check("the polarity word is passed through for display", r["polarity_word"] == "evil")
check("...flagged as scope-unresolved (branch-level vs item-level)",
      r["polarity_scope_unresolved"] is True)
check("no state name anywhere is a valence word",
      {ad.FIRED, ad.NOT_FIRED, ad.UNAVAILABLE}
      .isdisjoint({"favourable", "adverse", "good", "bad", "evil"}))

print("\nWhole-chart evaluation:")
pos = {"sun": LEO, "moon": TAURUS, "mars": SCORPIO, "mercury": VIRGO,
       "jupiter": CANCER, "venus": LIBRA, "saturn": AQUARIUS,
       "rahu": GEMINI, "ketu": SAGITTARIUS}
out = ad.evaluate_chart(pos, ARIES)
check("all 81 cells evaluate", len(out["cells"]) == 81, str(len(out["cells"])))
check("every condition lands in exactly one of the three states",
      out["totals"]["fired"] + out["totals"]["not_fired"]
      + out["totals"]["unavailable"] == out["totals"]["total"],
      str(out["totals"]))
check("nothing is silently dropped — unavailable is COUNTED",
      out["totals"]["unavailable"] > 0, str(out["totals"]["unavailable"]))
check("something actually fires (the engine is not vacuous)",
      out["totals"]["fired"] > 0, str(out["totals"]["fired"]))
check("the payload says plainly that it colours nothing",
      "colours nothing" in out["note"])
one = out["cells"]["jupiter|saturn"]
check("a cell carries its chapter", one["chapter"] == "BPHS Vol II ch.56", one["chapter"])
check("...and its fired conditions carry their quotes",
      all(f.get("quote") for f in one["fired"]))
check("...and no cell exposes a verdict field at all",
      not any(k in one for k in ("state", "verdict", "score", "polarity")),
      str([k for k in one if k in ("state", "verdict", "score", "polarity")]))

print("\nUnavailable dominates, and that is the honest result:")
print(f'   {out["totals"]}')
check("unavailable exceeds fired — the corpus is mostly unevaluable per chart",
      out["totals"]["unavailable"] > out["totals"]["fired"],
      f'{out["totals"]["unavailable"]} vs {out["totals"]["fired"]}')

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
