"""antardasa_plain.py: a branch applies only when its own conditions are met, and the death clause never travels."""
import antardasa
import antardasa_plain as A

fails = []


def check(name, cond, extra=""):
    print(("  PASS  " if cond else "  **FAIL**  ") + name + ("" if cond else f"  ({extra})"))
    if not cond:
        fails.append(name)


ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO, LIBRA, SCORPIO, SAG, CAP, AQU, PISCES = range(12)


def pos(**kw):
    return {g: {"rasi": s, "longitude": s * 30 + d} for g, (s, d) in kw.items()}


# the owner's configuration (Aquarius ascendant)
P = pos(sun=(GEMINI, 10), moon=(CAP, 3), mars=(ARIES, 2), mercury=(TAURUS, 21), jupiter=(PISCES, 27),
        venus=(CANCER, 25), saturn=(GEMINI, 26), rahu=(SCORPIO, 8), ketu=(TAURUS, 8))

print("Jupiter-Mars, Mars in his own sign:")
r = A.plain_cell("jupiter", "mars", P, AQU)
check("the cell is cited to its chapter and verses", r["citation"].startswith("BPHS Vol II ch.56 vv."))
check("the own-sign branch applies, by dignity", any(m["how"] == "dignity" and "own sign" in m["predicate"] for b in r["applies"] for m in b["met"]))
check("an applying branch carries the text's actual list, not a back-reference",
      all(b["results"] and not b["results"].lower().startswith(("as above", "same")) for b in r["applies"]))
check("the death (māraka) clause is left out and counted", r["counts"]["clauses_left_out"] >= 1 and
      not any("maraka" in m["predicate"].lower() for b in r["applies"] for m in b["met"]))
check("the counts add up", r["counts"]["apply"] + r["counts"]["undetermined"] + r["counts"]["not_met"] == r["counts"]["branches"])
check("no verdict is given", "no_verdict" in r and "verdict" not in {k for b in r["applies"] for k in b})

print("\nThe same cell with Mars debilitated in Cancer:")
r2 = A.plain_cell("jupiter", "mars", {**P, "mars": {"rasi": CANCER, "longitude": CANCER * 30 + 20}}, AQU)
check("the own-sign branch no longer applies", not any("own sign" in m["predicate"] for b in r2["applies"] for m in b["met"]))

print("\nA branch with a required conjunct that cannot be evaluated is not shown as applying:")
bad = []
for maha in antardasa.rules.CHAPTER_OF:
    for antar in antardasa.rules.CHAPTER_OF:
        c = A.plain_cell(maha, antar, P, AQU)
        if c is None:
            continue
        cell = antardasa.evaluate_cell(maha, antar, positions={g: p["rasi"] for g, p in P.items()}, lagna=AQU)
        req_unavailable = {x["predicate"] for x in cell["conditions"]
                           if "REQUIRED" in (x.get("results") or "") and x["state"] == antardasa.UNAVAILABLE
                           and A._dignity_test(x["predicate"], antar, P[antar]) is None}
        for b in c["applies"]:
            if any(m["predicate"] in req_unavailable for m in b["met"]):
                bad.append((maha, antar))
check("across all 81 cells", not bad, str(bad[:3]))

print("\nThe nodes get no dignity test:")
check("Rāhu 'in his own sign' is not evaluated", A._dignity_test("in his own sign", "rahu", P["rahu"]) is None)
check("a compound predicate is not treated as a plain dignity test",
      A._dignity_test("in his sign of debilitation AND associated with or aspected by malefics", "mars", P["mars"]) is None)

print("\nALL PASS" if not fails else f"\nFAILURES: {fails}")
raise SystemExit(1 if fails else 0)
