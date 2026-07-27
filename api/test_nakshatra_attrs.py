"""Nakṣatra `traditional`-tier attributes.

Run: python api/test_nakshatra_attrs.py

The point of this module is that it does NOT fabricate. These tests guarantee:
the values match what was transcribed from the source books, every cell carries a
confidence and citation, the resolved OCR swap and the deity variances are
surfaced not silently invented, and no cell claims BPHS provenance.

Updated 2026-07-26 for the Komilla Sutton (S4) reconciliation: nāḍī is now filled
(from S4's dosha column, matching the canonical Aṣṭakūṭa 9-9-9), dosha and guṇa
are new fields, yoni + puruṣārtha are corroborated, and the Puṣya↔Pūrva-Phalgunī
yoni swap is resolved to the canonical pairing.
"""
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import nakshatra_attrs as na
import vedic

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


CONF = {"corroborated", "single_source", "uncertain", "absent"}

print("Every nakṣatra 1-27 has a full, well-formed attribute row:")
rows = na.all_attributes()
check("exactly 27 rows", len(rows) == 27, str(len(rows)))
check("FIELDS now include dosha and guna",
      "dosha" in na.FIELDS and "guna" in na.FIELDS and "nadi" in na.FIELDS)
for r in rows:
    cells = r["cells"]
    ok = set(cells) == set(na.FIELDS)
    for f, c in cells.items():
        ok = ok and c["tier"] == "traditional" and c["confidence"] in CONF
        ok = ok and (c["available"] == (c["value"] is not None))
        if c["confidence"] != "absent":
            ok = ok and len(c["sources"]) >= 1
    check(f"nak {r['index']:>2} {r['name']:<16} well-formed", ok)

print("\nAll ten fields now have a value for every one of the 27 (nāḍī closed):")
for f in ("symbol", "gana", "guna", "yoni", "body_part", "purushartha",
          "quality", "shakti", "dosha", "nadi"):
    n = sum(1 for r in rows if r["cells"][f]["available"])
    check(f"{f}: 27/27 present", n == 27, f"{n}/27")

print("\nNāḍī is FILLED from S4's dosha and matches the canonical Aṣṭakūṭa 9-9-9:")
CANON_NADI = {
    "Ādi": {1, 6, 7, 12, 13, 18, 19, 24, 25},
    "Madhya": {2, 5, 8, 11, 14, 17, 20, 23, 26},
    "Antya": {3, 4, 9, 10, 15, 16, 21, 22, 27},
}
for name, idxs in CANON_NADI.items():
    got = {r["index"] for r in rows if r["cells"]["nadi"]["value"] == name}
    check(f"nāḍī {name}: exactly the canonical nine", got == idxs, str(sorted(got)))
check("every nāḍī cell is corroborated and cites Komilla (S4)",
      all(r["cells"]["nadi"]["confidence"] == "corroborated"
          and "S4" in r["cells"]["nadi"]["source_ids"] for r in rows))
# dosha ↔ nāḍī identity is internally consistent for all 27
D2N = {"Vāta": "Ādi", "Pitta": "Madhya", "Kapha": "Antya"}
check("dosha maps to nāḍī by Vāta=Ādi / Pitta=Madhya / Kapha=Antya, all 27",
      all(D2N[r["cells"]["dosha"]["value"]] == r["cells"]["nadi"]["value"] for r in rows))

print("\nDosha and guṇa are the new S4 fields with clean 9-9-9 structure:")
dc = Counter(r["cells"]["dosha"]["value"] for r in rows)
check("dosha: nine each of Vāta / Pitta / Kapha",
      dc.get("Vāta") == 9 and dc.get("Pitta") == 9 and dc.get("Kapha") == 9, str(dict(dc)))
check("dosha cells are single_source S4",
      all(r["cells"]["dosha"]["source_ids"] == ["S4"] for r in rows))
check("guṇa follows the three-cycles-of-nine: 1-9 Rajas, 10-18 Tamas, 19-27 Sattva",
      all(rows[i - 1]["cells"]["guna"]["value"] == "Rajas" for i in range(1, 10))
      and all(rows[i - 1]["cells"]["guna"]["value"] == "Tamas" for i in range(10, 19))
      and all(rows[i - 1]["cells"]["guna"]["value"] == "Sattva" for i in range(19, 28)))
check("guṇa cells are single_source S4",
      all(r["cells"]["guna"]["source_ids"] == ["S4"] for r in rows))

print("\nYoni and puruṣārtha are now corroborated (S3 + S4):")
check("every yoni cell is corroborated and cites both S3 and S4",
      all(r["cells"]["yoni"]["confidence"] == "corroborated"
          and set(r["cells"]["yoni"]["source_ids"]) == {"S3", "S4"} for r in rows))
check("every puruṣārtha cell is corroborated and cites both S3 and S4",
      all(r["cells"]["purushartha"]["confidence"] == "corroborated"
          and set(r["cells"]["purushartha"]["source_ids"]) == {"S3", "S4"} for r in rows))

print("\nThe Puṣya↔Pūrva-Phalgunī yoni swap is RESOLVED to the canonical pairing:")
pushya = rows[8 - 1]["cells"]["yoni"]
pphal = rows[11 - 1]["cells"]["yoni"]
check("Puṣya yoni is now the canonical goat/sheep (was the printed 'rat')",
      pushya["value"] == "Goat/sheep", pushya["value"])
check("Puṣya yoni note records the resolution via Komilla",
      "column-swap" in pushya.get("note", "").lower() and "komilla" in pushya.get("note", "").lower())
check("Pūrva Phalgunī yoni is now the canonical rat/mouse (was the printed 'goat')",
      pphal["value"] == "Rat/mouse", pphal["value"])

print("\nGaṇa / body-part / activity / śakti still rest on the single S3 book:")
check("gaṇa, body-part, quality, śakti cite only Perfect Astrology (S3)",
      all(rows[i]["cells"][f]["source_ids"] == ["S3"]
          for i in range(27)
          for f in ("gana", "body_part", "quality", "shakti")))
gc = Counter(r["cells"]["gana"]["value"] for r in rows)
check("gaṇa still the canonical 9-9-9 Deva/Manuṣya/Rākṣasa",
      gc.get("Deva") == 9 and gc.get("Manuṣya") == 9 and gc.get("Rākṣasa") == 9, str(dict(gc)))

print("\nSymbols: 1-18 iconographic & corroborated; 19-27 now iconic from S4:")
check("all 27 symbols are iconographic (19-27 gained an icon from S4)",
      all(r["cells"]["symbol"].get("kind") == "icon" for r in rows))
check("symbols 1-18 are corroborated (established icon + S4, some + S3)",
      all(rows[i - 1]["cells"]["symbol"]["confidence"] == "corroborated"
          and "S4" in rows[i - 1]["cells"]["symbol"]["source_ids"] for i in range(1, 19)))
check("symbols 19-27 cite Komilla (S4) and note the S3 star-shape",
      all(rows[i - 1]["cells"]["symbol"]["source_ids"] == ["S4"]
          and "star-pattern" in rows[i - 1]["cells"]["symbol"].get("note", "")
          for i in range(19, 28)))
check("symbol 1-9 still cite the established set (S1); 10-18 cite Sunil John (S2)",
      all("S1" in rows[i - 1]["cells"]["symbol"]["source_ids"] for i in range(1, 10))
      and all("S2" in rows[i - 1]["cells"]["symbol"]["source_ids"] for i in range(10, 19)))

print("\nNo cell claims BPHS/Parāśara; deity variances flagged, not applied:")
for r in rows:
    for f, c in r["cells"].items():
        for s in c["sources"]:
            if "BPHS" in s or "Parāśara" in s:
                fails.append(f"nak {r['index']} {f} claims BPHS")
check("no source string claims BPHS or Parāśara", not any("claims BPHS" in x for x in fails))
check("Hasta & Svātī deity variances are recorded (Savitṛ/Sūrya, Vāyu/Marut)",
      na.DEITY_TRADITION_VARIANTS[13]["traditional"] == "Savitṛ"
      and na.DEITY_TRADITION_VARIANTS[13]["bphs_app"] == "Sūrya"
      and na.DEITY_TRADITION_VARIANTS[15]["traditional"] == "Vāyu"
      and na.DEITY_TRADITION_VARIANTS[15]["bphs_app"] == "Marut")
check("both variances now name a second witness (S4 / Komilla)",
      na.DEITY_TRADITION_VARIANTS[13].get("also") == "S4"
      and na.DEITY_TRADITION_VARIANTS[15].get("also") == "S4")
check("those variances match the BPHS-tier values still standing in vedic.py",
      "Surya" in vedic.NAKSHATRAS[13 - 1][2] and "Marut" in vedic.NAKSHATRAS[15 - 1][2])

print("\nBackward-compatible symbols surface still works for every index:")
for i in range(1, 28):
    s = na.symbol_of(i)
    check(f"symbol_of({i}) available with a value", s["available"] and s["value"])
check("all_symbols() returns 27", len(na.all_symbols()) == 27)

print("\nOut-of-range indices raise rather than returning a plausible answer:")
for bad in (0, 28, -1, 100):
    for fn in (na.symbol_of, na.attributes_of):
        try:
            fn(bad)
            check(f"{fn.__name__}({bad}) rejected", False)
        except ValueError:
            check(f"{fn.__name__}({bad}) rejected", True)

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
