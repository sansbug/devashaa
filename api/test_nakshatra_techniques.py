"""Nakṣatra interaction techniques — `modern` tier, pointer-only.

Run: python api/test_nakshatra_techniques.py

Locks the transcription of docs/traditional-rules.md §3 (Part I, nakṣ 1-9) plus
the Part 2 extraction (nakṣ 10-18): the book counts, the non-Parāśara / remedial
quarantines, the two distinct source attributions, the explicit 19-27 gap, and
that nothing claims BPHS.
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


# Book counts per nakṣatra: Part I §3 (1-9) + Part 2 ToC (10-18); 46 + 51 = 97.
EXPECT = {1: 6, 2: 7, 3: 4, 4: 5, 5: 7, 6: 3, 7: 4, 8: 4, 9: 6,
          10: 7, 11: 13, 12: 4, 13: 3, 14: 6, 15: 7, 16: 3, 17: 3, 18: 5}

print("Parts I-II give 97 techniques, sourced for 1-18:")
check("total is 46 (Part I) + 51 (Part 2) = 97", nt.total_count() == 97, str(nt.total_count()))
for i in range(1, 19):
    t = nt.techniques_of(i)
    check(f"nak {i:>2} has {EXPECT[i]} techniques, tier modern, with a theme",
          t["available"] and len(t["techniques"]) == EXPECT[i]
          and t["tier"] == "modern" and t.get("theme"),
          f"got {len(t['techniques'])}")

print("\nEach nakṣatra cites its OWN book — Part I for 1-9, Part 2 for 10-18:")
check("1-9 cite Part I (Pandya, no Sunil John)",
      all("Part I" in nt.techniques_of(i)["source"] for i in range(1, 10)))
check("10-18 cite Part 2 (Sunil John)",
      all("Part 2" in nt.techniques_of(i)["source"]
          and "Sunil John" in nt.techniques_of(i)["source"] for i in range(10, 19)))
check("a 10-18 technique's cite names Part 2, not Part I",
      "Part 2" in nt.techniques_of(13)["techniques"][0]["cite"]
      and "Part I" not in nt.techniques_of(13)["techniques"][0]["cite"])

print("\nNakṣatras 19-27 are an explicit gap, never invented:")
for i in range(19, 28):
    t = nt.techniques_of(i)
    check(f"nak {i} unavailable with a reason and no techniques",
          t["available"] is False and t["techniques"] == []
          and "Part 3" in t["reason"])

print("\nEvery technique is a well-formed pointer (gist + computable + page + cite):")
allrows = nt.all_techniques()
for t in allrows:
    for tech in t["techniques"]:
        ok = (tech["gist"] and tech["computable"] in {"yes", "partly", "no"}
              and isinstance(tech["page"], int) and tech["cite"].startswith("modern technique"))
        if not ok:
            fails.append(f"malformed nak {t['index']} T{tech['n']}")
check("all 97 are well-formed", not any(x.startswith("malformed") for x in fails))

print("\nThe eight non-Parāśara / remedial techniques are flagged, and all computable=no:")
NP = {(4, 2): "outer planets", (5, 7): "vāstu", (8, 2): "mantra",
      (11, 5): "homa", (11, 11): "vāstu", (15, 4): "breath",
      (15, 6): "herbal", (18, 5): "holy-dip"}
flagged = {(t["index"], tech["n"]) for t in allrows for tech in t["techniques"]
           if "non_parashara" in tech}
check("exactly the expected eight carry a non_parashara flag", flagged == set(NP), str(sorted(flagged)))
for (i, n), frag in NP.items():
    tech = next(x for x in nt.techniques_of(i)["techniques"] if x["n"] == n)
    check(f"nak {i} T{n} names its reason ({frag}) and is computable=no",
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

print("\nOut-of-range indices raise rather than returning a plausible answer:")
for bad in (0, 28, -1, 100):
    try:
        nt.techniques_of(bad)
        check(f"index {bad} rejected", False)
    except ValueError:
        check(f"index {bad} rejected", True)

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
