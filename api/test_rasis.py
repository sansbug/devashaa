"""The twelve rāśis — structure, derivations, and the absences.

Run: python api/test_rasis.py

Two of these checks exist because an earlier mining pass got those exact rows
wrong by transcribing them. They are now derived, so the error cannot recur —
these tests pin that down.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import rasis
from rasis import Src

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


N = [n[0] for n in rasis.NAMES]

print("Nakṣatra spans are DERIVED, not transcribed:")
for s in range(12):
    sp = rasis.nakshatra_spans(s)
    check(f"{N[s]} holds exactly 9 pādas",
          sum(len(x["padas"]) for x in sp) == 9,
          str(sum(len(x["padas"]) for x in sp)))
check("every rāśi spans 0°→30° with no gap",
      all(abs(rasis.nakshatra_spans(s)[0]["from"]) < 1e-9
          and abs(rasis.nakshatra_spans(s)[-1]["to"] - 30) < 1e-9
          for s in range(12)))
check("every rāśi holds 2 or 3 nakṣatra segments (2¼ nakṣatras)",
      all(2 <= len(rasis.nakshatra_spans(s)) <= 3 for s in range(12)))

# THE REGRESSION. The mining pass lifted Mithuna's degree column into Kanyā.
kanya = rasis.nakshatra_spans(5)
check("KANYĀ = U.Phalgunī 2-4 (0°-10°) — the row a transcription pass corrupted",
      kanya[0]["nakshatra"] == "U.Phalgunī" and kanya[0]["padas"] == [2, 3, 4]
      and abs(kanya[0]["to"] - 10.0) < 1e-9,
      f'{kanya[0]["nakshatra"]} {kanya[0]["padas"]} →{kanya[0]["to"]:.2f}')
check("KANYĀ ends with Citrā 1-2 at 23°20'",
      kanya[-1]["nakshatra"] == "Citrā" and kanya[-1]["padas"] == [1, 2])
check("Kanyā's first segment is NOT Mṛgaśira (the corrupted reading)",
      kanya[0]["nakshatra"] != "Mṛgaśira")

print("\nRāśi dṛṣṭi is DERIVED from drishti.py (ch.8 vv.1-5):")
# THE OTHER REGRESSION: the miner gave Kumbha Capricorn's row.
kumbha = rasis.rasi(10)["rasi_drishti"]["aspects"]
check("KUMBHA aspects Meṣa, Karka, Tulā — not Capricorn's row",
      sorted(kumbha) == [0, 3, 6], str([N[i] for i in kumbha]))
check("every rāśi aspects exactly 3 signs",
      all(len(rasis.rasi(s)["rasi_drishti"]["aspects"]) == 3 for s in range(12)))
check("no rāśi aspects itself",
      all(s not in rasis.rasi(s)["rasi_drishti"]["aspects"] for s in range(12)))
# The consistency law of ch.8: movable aspects FIXED, fixed aspects MOVABLE,
# and dual aspects DUAL — the third case is same-modality, which is why the
# rule cannot be stated as "never its own kind". In each case the three
# aspected signs share one modality and the excluded one is the adjacent sign.
TARGET = {0: 1, 1: 0, 2: 2}   # movable→fixed, fixed→movable, dual→dual
ok = True
for s in range(12):
    asp = rasis.rasi(s)["rasi_drishti"]["aspects"]
    if {(a % 3) for a in asp} != {TARGET[s % 3]}:
        ok = False
check("movable→fixed, fixed→movable, dual→dual (ch.8's law holds for all 12)", ok)
check("a dual sign aspects only dual signs — the same-modality case",
      {a % 3 for a in rasis.rasi(2)["rasi_drishti"]["aspects"]} == {2},
      str([N[i] for i in rasis.rasi(2)["rasi_drishti"]["aspects"]]))

print("\nBādhaka — movable signs ONLY (Vol II ch.50 vv.20-21):")
for s in range(12):
    b = rasis.badhaka_for(s)
    if s % 3 == 0:
        check(f"{N[s]} (movable) → {N[b]}, the 11th", b == (s + 10) % 12)
    else:
        check(f"{N[s]} (non-movable) → None; BPHS gives no rule", b is None)

print("\nABSENCES are first-class, not gaps to be filled:")
leo = rasis.rasi(4)
check("Siṁha has NO element in BPHS",
      leo["attributes"]["element"]["src"] == Src.ABSENT.value,
      leo["attributes"]["element"]["src"])
check("...and 'element' is listed in Siṁha's `absent`",
      "element" in leo["absent"])
for s, name in ((4, "Siṁha"), (5, "Kanyā"), (6, "Tulā"), (7, "Vṛścika")):
    check(f"{name} element absent (only 7 of 12 signs get one)",
          rasis.rasi(s)["attributes"]["element"]["src"] == Src.ABSENT.value)
check("Vṛścika has NO rising type — the only sign so omitted",
      rasis.rasi(7)["attributes"]["rising"]["src"] == Src.ABSENT.value)
check("Mīna has NO complexion",
      rasis.rasi(11)["attributes"]["complexion"]["src"] == Src.ABSENT.value)
check("Meṣa's habitat is OCR-LOST, not absent (the book has it)",
      rasis.rasi(0)["attributes"]["habitat"]["src"] == Src.OCR_LOST.value)
check("an OCR-lost value carries no invented text",
      rasis.rasi(0)["attributes"]["habitat"]["value"] is None)

print("\nEvery attribute of every sign carries a source tag:")
bad = [(N[s], k) for s in range(12)
       for k, v in rasis.rasi(s)["attributes"].items()
       if v.get("src") not in {e.value for e in Src} or not v.get("ref")]
check("no attribute is untagged or uncited anywhere in the 12 signs",
      not bad, str(bad[:4]))

print("\nDirection: ch.4 vs ch.8 disclosed, never silently resolved:")
check("all 12 signs carry the ch.8 conflict note on `direction`",
      all(rasis.rasi(s)["attributes"]["direction"]["conflict"]
          for s in range(12) if rasis.rasi(s)["attributes"]["direction"]["value"]))

print("\nDignities come from dignity.py, so ch.3's numbers live in one place:")
check("Tulā hosts Saturn's exaltation at 20°",
      rasis.rasi(6)["dignities"]["exaltation"] == [{"graha": "saturn", "degree": 20.0}])
check("Tulā hosts Sūrya's debilitation at 10°",
      rasis.rasi(6)["dignities"]["debilitation"] == [{"graha": "sun", "degree": 10.0}])
empty = [N[s] for s in range(12) if rasis.rasi(s)["dignities"]["empty"]]
check("exactly 4 signs host no exaltation or fall (Mithuna/Siṁha/Dhanus/Kumbha)",
      sorted(empty) == sorted(["Mithuna", "Siṁha", "Dhanus", "Kumbha"]), str(empty))

print("\nThe 'not in BPHS' list is present on every card:")
check("all 12 carry the absent-attribute list",
      all(len(rasis.rasi(s)["not_in_bphs"]["attributes"]) >= 10 for s in range(12)))
check("'compatible signs' is named as absent",
      "compatible signs" in rasis.ABSENT_FROM_ALL_RASIS)
check("'lucky number' is named as absent",
      "lucky number" in rasis.ABSENT_FROM_ALL_RASIS)
check("rāśi dṛṣṭi is labelled NOT compatibility",
      "NOT compatibility" in rasis.rasi(0)["rasi_drishti"]["note"])

print("\nch.34 as-lagna table comes from functional.py:")
check("every sign has a 9-graha as-lagna profile",
      all(len(rasis.rasi(s)["as_lagna"]["grahas"]) == 9 for s in range(12)))

print("\nSerialisable (it crosses the API boundary):")
import json
try:
    json.dumps(rasis.all_rasis())
    check("all_rasis() is JSON-serialisable", True)
except Exception as e:  # noqa: BLE001
    check("all_rasis() is JSON-serialisable", False, str(e))

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
