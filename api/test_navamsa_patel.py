"""Navāṁśa Part-II technique index (C. S. Patel) — tier `modern`, pointer-only.

Run: python api/test_navamsa_patel.py

The point of these tests is the copyright + provenance discipline: every entry
NAMES a technique and cites a source, none reproduces Patel's result tables, and
nothing claims BPHS or emits a verdict.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import navamsa_patel as np

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


data = np.part2_techniques()
techs = data["techniques"]

print("The index is well-formed and modern-tier:")
check("tier is modern and names C. S. Patel",
      data["tier"] == "modern" and "Patel" in data["source"])
check("ten Part-II techniques, count matches", data["count"] == len(techs) == 10, str(data["count"]))
FIELDS = {"n", "chapter", "technique", "gist", "source", "page", "computable", "detects"}
for t in techs:
    check(f"#{t['n']:>2} {t['technique']:<34} well-formed",
          set(t) == FIELDS and isinstance(t["page"], int))

print("\nEvery pointer cites a source and a valid trigger flag:")
check("computable flag is one of yes/partly/no",
      all(t["computable"] in ("yes", "partly", "no") for t in techs))
check("every pointer names a classical / magazine source",
      all(t["source"] and len(t["source"]) > 4 for t in techs))
check("chapters span Ch.XVI–XX",
      {t["chapter"] for t in techs} == {"XVI", "XVII", "XVIII", "XIX", "XX"})
check("page numbers land in Part II (154–204)",
      all(154 <= t["page"] <= 204 for t in techs))

print("\nCopyright discipline: pointers name the METHOD, never reproduce results:")
# A gist is a one-line description of the technique. Guard against a result table
# leaking in as a long semicolon-separated list of attributes.
check("no gist exceeds 26 words (a one-line method, not a result table)",
      all(len(t["gist"].split()) <= 26 for t in techs),
      str(max(len(t["gist"].split()) for t in techs)))
check("no gist is a reproduced result list (≤1 semicolon)",
      all(t["gist"].count(";") <= 1 for t in techs))
check("the scope note states results are NOT reproduced",
      "not reproduced" in data["note"].lower() or "none of his result" in data["note"].lower())

print("\nNothing claims BPHS, and no death verdict is emitted:")
check("no source or gist claims BPHS / Parāśara",
      not any("BPHS" in (t["source"] + t["gist"]) or "Parāśara" in (t["source"] + t["gist"])
              for t in techs))
check("the death-mode material is named as NOT evaluated",
      "does not predict death" in data["note"].lower())
# The ariṣṭa-years pointer (the one nearest a death claim) is flagged partly and
# explicitly says the death sub-rule is not evaluated.
arishta = next(t for t in techs if "Ariṣṭa" in t["technique"])
check("the ariṣṭa-years pointer is `partly` and defers its death sub-rule",
      arishta["computable"] == "partly" and "not evaluated" in arishta["detects"])

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
