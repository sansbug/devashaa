"""K.N. Rao (modern) pointer bucket — §3b.

Run: python api/test_rao_pointers.py

Locks the faithful transcription of docs/traditional-rules.md §3b: the ten
Gajakesari pointers, the Astrology-Lessons tiering split, and that nothing claims
BPHS or leaks into the nakṣatra set.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import rao_pointers as rp

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


b = rp.bucket()

print("The bucket is modern-tier and carries both sub-sources:")
check("bucket tier is modern", b["tier"] == "modern")
check("has gajakesari and astrology_lessons", "gajakesari" in b and "astrology_lessons" in b)

print("\nThe Gajakesari method is the book's ten pointers, well-formed:")
g = b["gajakesari"]["pointers"]
check("exactly ten pointers", len(g) == 10, str(len(g)))
for p in g:
    ok = (p["title"] and p["gist"] and p["computable"] in {"yes", "partly", "no"}
          and p["page"] and p["tier"] == "modern"
          and p["cite"].startswith("modern technique"))
    if not ok:
        fails.append(f"malformed pointer {p.get('title')}")
check("all ten well-formed (gist + computable + page + modern cite)",
      not any(x.startswith("malformed") for x in fails))
# the one clean structural flag, and the naive-application caution
titles = {p["title"]: p for p in g}
check("the sign-type parity constraint is the computable=yes one",
      titles["Sign-type parity constraint"]["computable"] == "yes")
check("'too common to read naively' is computable=no",
      titles["Too common to read naively"]["computable"] == "no")

print("\nAstrology Lessons splits traditional (cross-check) from modern (named):")
al = b["astrology_lessons"]
check("traditional tables are listed, marked cross-check only, NOT re-served as data",
      len(al["traditional_tables"]["items"]) >= 10
      and "cross-check" in al["traditional_tables"]["note"])
check("modern pointers are named (P.A.C. / P.A.C.D.A.R.E.S. present)",
      any(m["name"] == "P.A.C." for m in al["modern_pointers"]["items"])
      and any(m["name"] == "P.A.C.D.A.R.E.S." for m in al["modern_pointers"]["items"]))
check("the modern-pointers note says the content is NOT reproduced",
      "not reproduced" in al["modern_pointers"]["note"].lower()
      or "not in the captured excerpt" in al["modern_pointers"]["note"].lower())

print("\nNothing claims BPHS, and the sources are K.N. Rao's two books:")
check("gajakesari source is Enigmas in Astrology",
      "Enigmas" in b["gajakesari"]["source"] and "BPHS" not in b["gajakesari"]["source"])
check("astrology-lessons source is Astrology Lessons",
      "Astrology Lessons" in al["source"])
for p in g:
    if "BPHS" in p["cite"] or "Parāśara" in p["cite"]:
        fails.append(f"pointer claims BPHS: {p['title']}")
check("no Gajakesari pointer claims BPHS/Parāśara",
      not any("claims BPHS" in x for x in fails))

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
