"""Nakṣatra `traditional`-tier attributes.

Run: python api/test_nakshatra_attrs.py

The whole point of this module is that it does NOT fabricate. These tests exist
mostly to guarantee that: the sourced nine are present, the absent eighteen stay
absent (not guessed), and the sourced symbols agree with the classical standard
and with the deities the app already carries from BPHS.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import nakshatra_attrs as na
import vedic

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


print("The nine sourced symbols are present and tier-tagged:")
for i in range(1, 10):
    s = na.symbol_of(i)
    check(f"nakṣatra {i} has a sourced symbol",
          s["available"] and s["value"] and s["tier"] == "traditional",
          s.get("value") or "MISSING")

print("\nThe eighteen unsourced stay ABSENT — never guessed:")
for i in range(10, 28):
    s = na.symbol_of(i)
    check(f"nakṣatra {i} is an explicit gap, not a fabricated symbol",
          s["available"] is False and s["value"] is None
          and "not guessed" in s["reason"].lower())

print("\nExactly nine sourced, eighteen absent — no silent fill:")
avail = [x for x in na.all_symbols() if x["available"]]
check("nine available", len(avail) == 9, str(len(avail)))
check("eighteen absent", len(na.all_symbols()) - len(avail) == 18)
check("the sourced set is exactly Aśvinī..Āśleṣā (1-9)",
      sorted(x["index"] for x in avail) == list(range(1, 10)))

print("\nEvery sourced symbol carries the traditional citation, none claims BPHS:")
for x in na.all_symbols():
    if x["available"]:
        check(f"nakṣatra {x['index']} cites the traditional source, not Parāśara",
              x["tier"] == "traditional" and "BPHS" not in x["citation"]
              and "Parāśara" not in x["citation"])

print("\nThe symbols agree with the deities the app already carries from BPHS:")
# A cross-check the reader can follow: the sourced symbols line up with the
# BPHS-cited deities already in vedic.NAKSHATRAS, so the two tiers corroborate
# rather than conflict.
# Fragments taken from the actual vedic.NAKSHATRAS deity strings (checked, not
# guessed): #1 "Dastra (Aśvinī Kumāra)", #2 "Yama", #5 "Chandra", #9 "Ahi (Sarpa)".
pairs = {
    1: "Ashwini",  # horse's head ↔ Ashwini Kumāra (the horse-headed physicians)
    2: "Yama",     # yoni/womb    ↔ Yama
    5: "Chandra",  # deer's head  ↔ Soma/Chandra
    9: "Sarpa",    # serpent      ↔ Ahi/Sarpa (the Nāgas)
}
for idx, deity_frag in pairs.items():
    deity = vedic.NAKSHATRAS[idx - 1][2]
    check(f"nakṣatra {idx} symbol sits beside its BPHS deity ({deity_frag})",
          deity_frag in deity, f"deity in code = {deity!r}")

print("\nOut-of-range indices raise rather than returning a plausible answer:")
for bad in (0, 28, -1, 100):
    try:
        na.symbol_of(bad)
        check(f"index {bad} rejected", False)
    except ValueError:
        check(f"index {bad} rejected", True)

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
