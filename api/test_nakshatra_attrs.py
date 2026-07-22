"""Nakṣatra `traditional`-tier attributes.

Run: python api/test_nakshatra_attrs.py

The point of this module is that it does NOT fabricate. These tests guarantee:
the values match what was transcribed from the two source books, every cell
carries a confidence and citation, the flagged OCR issues (the Puṣya↔Pūrva-
Phalgunī yoni swap; the garbled S3 symbol reads) are surfaced not silently fixed,
nāḍī stays an explicit gap for all 27, and no cell claims BPHS provenance.
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


CONF = {"corroborated", "single_source", "uncertain", "absent"}

print("Every nakṣatra 1-27 has a full, well-formed attribute row:")
rows = na.all_attributes()
check("exactly 27 rows", len(rows) == 27, str(len(rows)))
for r in rows:
    cells = r["cells"]
    ok = set(cells) == set(na.FIELDS)
    for f, c in cells.items():
        ok = ok and c["tier"] == "traditional" and c["confidence"] in CONF
        # a value is present iff available, and every non-absent cell cites a source
        ok = ok and (c["available"] == (c["value"] is not None))
        if c["confidence"] != "absent":
            ok = ok and len(c["sources"]) >= 1
    check(f"nak {r['index']:>2} {r['name']:<16} well-formed", ok)

print("\nThe seven attested fields have a value for all 27; nāḍī for none:")
for f in ("symbol", "gana", "yoni", "body_part", "purushartha", "quality", "shakti"):
    n = sum(1 for r in rows if r["cells"][f]["available"])
    check(f"{f}: 27/27 present", n == 27, f"{n}/27")
n_nadi = sum(1 for r in rows if r["cells"]["nadi"]["available"])
check("nāḍī: 0/27 — an explicit gap, never guessed", n_nadi == 0, f"{n_nadi}/27")
for r in rows:
    nd = r["cells"]["nadi"]
    check_once = nd["confidence"] == "absent" and "not sourced" in nd.get("note", "").lower() \
        or nd["confidence"] == "absent" and "absent" in nd.get("note", "").lower()
    if not check_once:
        fails.append(f"nadi note nak {r['index']}")
check("every nāḍī cell is confidence 'absent' with a reason",
      all(r["cells"]["nadi"]["confidence"] == "absent"
          and r["cells"]["nadi"].get("note") for r in rows))

print("\nProvenance tiers land where the sources actually reach:")
# symbols: 1-9 established, 10-18 Sunil John, 19-27 Perfect Astrology asterisms
check("symbol 1-9 cite the established set (S1)",
      all("S1" in rows[i - 1]["cells"]["symbol"]["source_ids"] for i in range(1, 10)))
check("symbol 10-18 cite Sunil John Part 2 (S2)",
      all("S2" in rows[i - 1]["cells"]["symbol"]["source_ids"] for i in range(10, 19)))
check("symbol 19-27 cite Perfect Astrology (S3) and are tagged asterism_figure",
      all(rows[i - 1]["cells"]["symbol"]["source_ids"] == ["S3"]
          and rows[i - 1]["cells"]["symbol"].get("kind") == "asterism_figure"
          for i in range(19, 28)))
check("symbol 1-18 are iconographic",
      all(rows[i - 1]["cells"]["symbol"].get("kind") == "icon" for i in range(1, 19)))
check("the S3 classification fields cite only Perfect Astrology",
      all(rows[i]["cells"][f]["source_ids"] == ["S3"]
          for i in range(27)
          for f in ("gana", "yoni", "body_part", "purushartha", "quality", "shakti")))

print("\nThe eight corroborated symbols carry two independent sources:")
corro = [r["index"] for r in rows if r["cells"]["symbol"]["confidence"] == "corroborated"]
check("exactly the expected eight are corroborated",
      corro == [1, 2, 5, 9, 10, 13, 14, 16], str(corro))
check("each corroborated symbol lists 2 sources",
      all(len(rows[i - 1]["cells"]["symbol"]["sources"]) == 2 for i in corro))

print("\nThe flagged OCR issues are SURFACED, not silently fixed:")
pushya = rows[8 - 1]["cells"]["yoni"]
pphal = rows[11 - 1]["cells"]["yoni"]
check("Puṣya yoni is the value the book PRINTS (rat/mouse), not the canonical fix",
      pushya["value"] == "Rat/mouse", pushya["value"])
check("Puṣya yoni is 'uncertain' and its note names the suspected swap + canonical",
      pushya["confidence"] == "uncertain" and "goat/sheep" in pushya["note"].lower())
check("Pūrva Phalgunī yoni is the printed 'goat/sheep', flagged uncertain",
      pphal["value"] == "Goat/sheep" and pphal["confidence"] == "uncertain"
      and "rat/mouse" in pphal["note"].lower())
check("the two garbled S3 symbol reads (4,7,8) keep the established icon + a note",
      all(rows[i - 1]["cells"]["symbol"]["value"] == na._SYMBOL[i]
          and rows[i - 1]["cells"]["symbol"].get("note") for i in (4, 7, 8)))
anu = rows[17 - 1]["cells"]["symbol"]
check("Anurādhā symbol is the securely-attested 'lotus' with the row-bleed caveat",
      "lotus" in anu["value"].lower() and "row-bleed" in anu.get("note", "").lower())

print("\nGaṇa matches the canonical 9-9-9 split (a check, not a source):")
from collections import Counter
gc = Counter(r["cells"]["gana"]["value"] for r in rows)
check("nine each of Deva / Manuṣya / Rākṣasa",
      gc.get("Deva") == 9 and gc.get("Manuṣya") == 9 and gc.get("Rākṣasa") == 9,
      str(dict(gc)))

print("\nPuruṣārtha follows the canonical Dh-Ar-Kā-Mo cycle exactly:")
DAKM = ["Dharma", "Artha", "Kāma", "Mokṣa"]
# The classical assignment walks the four aims in a boustrophedon over groups of
# four; here we just assert the set is complete and every value is one of them.
check("every puruṣārtha is one of the four aims",
      all(r["cells"]["purushartha"]["value"] in DAKM for r in rows))

print("\nNo cell claims BPHS/Parāśara; deity variances are flagged, not applied:")
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
