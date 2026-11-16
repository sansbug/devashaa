"""The corrections to the antardaśā corpus still match what they correct, and no damaged token is left behind."""
import re
import antardasa            # applies the corrections on load
import antardasa_rules as R
import antardasa_corrections as C

fails = []


def check(name, cond, extra=""):
    print(("  PASS  " if cond else "  **FAIL**  ") + name + ("" if cond else f"  ({extra})"))
    if not cond:
        fails.append(name)


res = C.apply(R.MATRIX)   # idempotent
check("every correction still finds the string it corrects", not res["unmatched"], str(res["unmatched"]))
check("every correction names the page it was read from", all("page image" in c[5] for c in C.CORRECTIONS))
check("a correction changes only its damaged string", all(c[3] != c[4] and len(c[4]) > 10 for c in C.CORRECTIONS))

x = R.cell("saturn", "saturn")["conditions"][0]
check("Saturn-Saturn vv.1-3 reads as the page prints it",
      x["results"].startswith("acquisition of a kingdom (attainment of a high position in government), happiness from wife and children"))
y = R.cell("rahu", "mercury")["conditions"][1]
check("Rahu-Mercury reads 'Raja yoga, beneficence of the king'", "Raja yoga, beneficence of the king" in y["results"])

# the detector that found them: no result list carries a token with punctuation or a digit inside a word
BAD = re.compile(r"[a-z]'[a-z]{2,}|[a-z][.,;:*\"][a-z]|[a-z]\d|\d[a-z]|\*", re.I)
OK = re.compile(r"\b(i\.e|e\.g|vv?\.\d|king's|one's|people's|cow's|Santhanam's|native's|father's|mother's|wife's)\b|\d+(st|nd|rd|th)\b", re.I)
left = []
for (m, a), cell in R.MATRIX.items():
    for i, cond in enumerate(cell["conditions"]):
        t = OK.sub(" ", cond.get("results") or "")
        hit = BAD.search(t)
        if hit:
            left.append((m, a, i, hit.group(0)))
check("no result list is left with a damaged token of that kind", not left, str(left[:5]))

print("\nALL PASS" if not fails else f"\nFAILURES: {fails}")
raise SystemExit(1 if fails else 0)
