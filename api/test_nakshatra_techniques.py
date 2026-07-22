"""Nakṣatra interaction techniques — `modern` tier, pointer-only.

Run: python api/test_nakshatra_techniques.py

Locks the faithful transcription of docs/traditional-rules.md §3: the book's 46
techniques across nakṣatras 1-9, the three non-Parāśara quarantines, the explicit
10-27 gap, and that nothing claims BPHS.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import nakshatra_techniques as nt

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


# The book's own counts, per nakṣatra (§3 headings).
EXPECT = {1: 6, 2: 7, 3: 4, 4: 5, 5: 7, 6: 3, 7: 4, 8: 4, 9: 6}

print("The book's 46 techniques are present, sourced for 1-9 only:")
check("total is the book's 46", nt.total_count() == 46, str(nt.total_count()))
for i in range(1, 10):
    t = nt.techniques_of(i)
    check(f"nak {i} has {EXPECT[i]} techniques, tier modern, with a theme",
          t["available"] and len(t["techniques"]) == EXPECT[i]
          and t["tier"] == "modern" and t.get("theme"),
          f"got {len(t['techniques'])}")

print("\nNakṣatras 10-27 are an explicit gap, never invented:")
for i in range(10, 28):
    t = nt.techniques_of(i)
    check(f"nak {i} unavailable with a reason and no techniques",
          t["available"] is False and t["techniques"] == []
          and "Part I" in t["reason"])

print("\nEvery technique is a well-formed pointer (gist + computable + page + cite):")
allrows = nt.all_techniques()
for t in allrows:
    for tech in t["techniques"]:
        ok = (tech["gist"] and tech["computable"] in {"yes", "partly", "no"}
              and isinstance(tech["page"], int) and tech["cite"].startswith("modern technique"))
        if not ok:
            fails.append(f"malformed nak {t['index']} T{tech['n']}")
check("all 46 are well-formed", not any(x.startswith("malformed") for x in fails))

print("\nThe three non-Parāśara techniques are flagged and quarantined:")
NP = {(4, 2): "outer planets", (5, 7): "Vāstu", (8, 2): "mantra"}
flagged = {(t["index"], tech["n"]) for t in allrows for tech in t["techniques"]
           if "non_parashara" in tech}
check("exactly three carry a non_parashara flag", flagged == set(NP), str(sorted(flagged)))
for (i, n), frag in NP.items():
    tech = next(x for x in nt.techniques_of(i)["techniques"] if x["n"] == n)
    check(f"nak {i} T{n} names its non-Parāśara reason ({frag}) and is computable=no",
          frag.lower() in tech["non_parashara"].lower() and tech["computable"] == "no")

print("\nNo technique claims BPHS / Parāśara / the traditional tier:")
for t in allrows:
    if t.get("source") and ("BPHS" in t["source"] or "Parāśara" in t["source"]):
        fails.append(f"nak {t['index']} source claims BPHS")
    for tech in t["techniques"]:
        if "BPHS" in tech["cite"] or tech.get("tier") != "modern":
            fails.append(f"nak {t['index']} T{tech['n']} mis-tiered")
check("nothing claims BPHS and every tier is 'modern'",
      not any("claims BPHS" in x or "mis-tiered" in x for x in fails))
check("the source is the Saptarishis/Pandya Part I, not 'Sunil John'",
      "Pandya" in nt.SOURCE and "Sunil John" not in nt.SOURCE)

print("\nOut-of-range indices raise rather than returning a plausible answer:")
for bad in (0, 28, -1, 100):
    try:
        nt.techniques_of(bad)
        check(f"index {bad} rejected", False)
    except ValueError:
        check(f"index {bad} rejected", True)

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
