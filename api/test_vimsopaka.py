import sys
sys.path.insert(0, r"C:\proj\astrodev\api")
from vimsopaka import (
    vimsopaka, swaviswa, verdict, grade, grade_table, natural_relation_rungs,
    SHADVARGA, SAPTAVARGA, DASAVARGA, SHODASAVARGA, SCHEMES,
    VARGA_VISWA, RUNGS, TOTAL,
    SAPTAVARGA_READINGS, SAPTAVARGA_UNAVAILABLE, SAPTAVARGA_AMBIGUOUS,
    SAPTAVARGA_READING_EVIDENCE,
    GRADE_NAMES, GRADE_BAND, VERDICT_BANDS,
    VERDICT_BOUNDARIES_OPEN, GRADE_BOUNDARIES_OPEN, GROUP_CITATION,
)

fails = []
def check(label, cond, detail=""):
    if not cond: fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  '+detail) if detail else ''}")

def near(a, b, tol=1e-9):
    return abs(a - b) < tol


print("BPHS ch.7 vv.17-20 — group membership is DERIVED, each from the one before:")
check("Shadvarga = Rasi Hora Drekkana Navamsa Dvadasamsa Trimsamsa",
      SHADVARGA == ("D1","D2","D3","D9","D12","D30"), str(SHADVARGA))
check("vv.17-19 'Adding the Sapthamamsa to the Shad Vargas' -> Saptavarga = Shad + D7",
      SAPTAVARGA == SHADVARGA + ("D7",) and len(SAPTAVARGA) == 7)
check("v.20 'Add Dasamsa, Shodasamsa and Shastiamsa to the said Saptha Varga'",
      DASAVARGA == SAPTAVARGA + ("D10","D16","D60") and len(DASAVARGA) == 10)
check("vv.21-25 Shodasavarga = all 16 vargas, no repeats",
      len(SHODASAVARGA) == 16 and len(set(SHODASAVARGA)) == 16)
check("Shodasavarga contains every Dasavarga member", set(DASAVARGA) <= set(SHODASAVARGA))
check("'Turyamsa' row of the table is D4 (the quarter)", "D4" in SHODASAVARGA)
# The source labels that block '42-53. VARGA CLASSIFICATION' and Santhanam's
# 'Four kinds of summary of the Vargas' note follows the WHOLE block. There is
# no note to a v.52.
check("group membership is cited to ch.6 vv.42-53, not to a 'v.52'",
      GROUP_CITATION == "R. Santhanam's note to BPHS Vol I ch.6 vv.42-53",
      GROUP_CITATION)


print("\nEvery scheme's Swaviswa column totals 20 (the point of 'Vimsopaka'):")
for s in ("shadvarga", "dasavarga", "shodasavarga"):
    w = swaviswa(s)
    check(f"{s} sums to 20.0", near(sum(w.values()), TOTAL), f"got {sum(w.values())}")
    check(f"{s} covers exactly its own vargas", set(w) == set(SCHEMES[s]))
for name, w in SAPTAVARGA_READINGS.items():
    check(f"saptavarga[{name}] sums to 20.0", near(sum(w.values()), TOTAL), f"got {sum(w.values())}")


print("\nvv.17-19 Shadvarga weights, read straight off the sloka (6,2,4,5,2,1):")
w = swaviswa("shadvarga")
for k, want in zip(SHADVARGA, (6, 2, 4, 5, 2, 1)):
    check(f"shadvarga {k} = {want}", near(w[k], want), f"got {w[k]}")


print("\nv.20 Dasavarga: '3 for Rasi, 5 for Shashtiamsa and for the other 8 divisions 1.5 each':")
w = swaviswa("dasavarga")
check("Rasi = 3", near(w["D1"], 3.0), str(w["D1"]))
check("Shastiamsa = 5", near(w["D60"], 5.0), str(w["D60"]))
others = [k for k in DASAVARGA if k not in ("D1", "D60")]
check("the OTHER EIGHT are 1.5 each", len(others) == 8 and all(near(w[k], 1.5) for k in others),
      f"{len(others)} divisions")
check("3 + 5 + 8x1.5 = 20 (the sloka's own arithmetic closes)",
      near(3.0 + 5.0 + 8 * 1.5, TOTAL))


print("\nvv.21-25 Shodasavarga: the seven named, then 'the rest of the nine divisions each a half':")
w = swaviswa("shodasavarga")
for k, want, label in (("D2",1.0,"Hora"), ("D30",1.0,"Trimsamsa"), ("D3",1.0,"decanate"),
                       ("D16",2.0,"Shodasamsa"), ("D9",3.0,"Navamsa"),
                       ("D1",3.5,"Rasi"), ("D60",4.0,"Shashtiamsa")):
    check(f"{label} ({k}) = {want}", near(w[k], want), f"got {w[k]}")
rest = [k for k in SHODASAVARGA if k not in ("D2","D30","D3","D16","D9","D1","D60")]
check("the REST are exactly nine divisions", len(rest) == 9, f"got {len(rest)}")
check("...each a half", all(near(w[k], 0.5) for k in rest))
check("15.5 + 9x0.5 = 20 (the damaged 'Rasi 3l' MUST be 3.5 for this to close)",
      near(1+1+1+2+3+3.5+4 + 9*0.5, TOTAL))

print("\n  ...and that reconstruction must reproduce Santhanam's printed table (book p.97 = pdf p.96):")
# The Shodasa Varga column of the table, in its printed row order.
printed = [("D1",3.5),("D2",1.0),("D3",1.0),("D9",3.0),("D12",0.5),("D30",1.0),
           ("D7",0.5),("D10",0.5),("D16",2.0),("D60",4.0),("D20",0.5),("D24",0.5),
           ("D27",0.5),("D4",0.5),("D40",0.5),("D45",0.5)]
check("all 16 printed cells match the sloka-derived column",
      all(near(w[k], v) for k, v in printed),
      "mismatches: %s" % [k for k, v in printed if not near(w[k], v)])
check("printed Dasa Varga column (3.0, eight 1.5s, 5.0) matches too",
      near(swaviswa("dasavarga")["D1"], 3.0) and near(swaviswa("dasavarga")["D60"], 5.0))


print("\nSaptavarga is REFUSED, not guessed (vv.17-19 OCR damage: '2t' and '412'):")
try:
    swaviswa("saptavarga")
    check("swaviswa('saptavarga') raises without a named reading", False, "it returned")
except ValueError as e:
    check("swaviswa('saptavarga') raises without a named reading", True)
    check("...and the message explains the damage", "OCR-damaged" in str(e))
try:
    vimsopaka("saptavarga", {k: "own" for k in SAPTAVARGA})
    check("vimsopaka('saptavarga', ...) raises too", False, "it returned")
except ValueError:
    check("vimsopaka('saptavarga', ...) raises too", True)
a = SAPTAVARGA_READINGS["sloka_order"]
b = SAPTAVARGA_READINGS["ascending_divisor"]
check("exactly two readings are offered, and neither is named 'table_consistent' "
      "(the table does NOT support reading B — see below)",
      set(SAPTAVARGA_READINGS) == {"sloka_order", "ascending_divisor"},
      str(sorted(SAPTAVARGA_READINGS)))
check("both readings agree on the undamaged head Rasi 5, Hora 2, Drekkana 3",
      all(near(a[k], b[k]) for k in ("D1","D2","D3")) and
      near(a["D1"],5.0) and near(a["D2"],2.0) and near(a["D3"],3.0))
check("both readings carry the SAME multiset {5,2,3,2.5,4.5,2,1}",
      sorted(a.values()) == sorted(b.values()) == [1.0,2.0,2.0,2.5,3.0,4.5,5.0])
check("the two readings genuinely differ (so the choice matters)",
      any(not near(a[k], b[k]) for k in SAPTAVARGA_AMBIGUOUS),
      f"differ on {[k for k in SAPTAVARGA_AMBIGUOUS if not near(a[k], b[k])]}")
check("only the four ambiguous vargas differ",
      all(near(a[k], b[k]) for k in SAPTAVARGA if k not in SAPTAVARGA_AMBIGUOUS))
check("the module RECOMMENDS NEITHER reading (the text does not decide)",
      "recommends NEITHER" in SAPTAVARGA_UNAVAILABLE and
      "recommended" not in SAPTAVARGA_UNAVAILABLE,
      SAPTAVARGA_UNAVAILABLE)
check("every offered reading carries its own evidence string",
      set(SAPTAVARGA_READING_EVIDENCE) == set(SAPTAVARGA_READINGS))

print("\n  ARGUMENT FOR 'ascending_divisor' — column monotonicity. It is TWO of")
print("  three undamaged columns, not three: the Dasavarga column TIES at 1.5.")
strict = {s: swaviswa(s) for s in ("shadvarga", "dasavarga", "shodasavarga")}
check("shadvarga: Navamsa 5 STRICTLY exceeds Dvadasamsa 2",
      strict["shadvarga"]["D9"] > strict["shadvarga"]["D12"],
      f"{strict['shadvarga']['D9']} vs {strict['shadvarga']['D12']}")
check("shodasavarga: Navamsa 3.0 STRICTLY exceeds Dvadasamsa 0.5",
      strict["shodasavarga"]["D9"] > strict["shodasavarga"]["D12"],
      f"{strict['shodasavarga']['D9']} vs {strict['shodasavarga']['D12']}")
check("dasavarga: Navamsa EQUALS Dvadasamsa (1.5 vs 1.5) -> that column is "
      "SILENT on the point, it does not support the argument",
      near(strict["dasavarga"]["D9"], strict["dasavarga"]["D12"]),
      f"{strict['dasavarga']['D9']} vs {strict['dasavarga']['D12']}")
check("so the monotonicity argument rests on exactly 2 of 3 columns",
      sum(1 for s in strict if strict[s]["D9"] > strict[s]["D12"]) == 2)
check("reading 'ascending_divisor' preserves Navamsa > Dvadasamsa; "
      "'sloka_order' inverts it",
      b["D9"] > b["D12"] and a["D9"] < a["D12"],
      f"B {b['D9']}>{b['D12']}, A {a['D9']}<{a['D12']}")
check("under 'ascending_divisor' the Shad->Sapta shift funds Saptamsa exactly",
      near((6.0-b["D1"]) + (4.0-b["D3"]) + (5.0-b["D9"]), b["D7"]),
      "Rasi/Drekkana/Navamsa give up %.1f, Saptamsa takes %.1f"
      % ((6.0-b["D1"])+(4.0-b["D3"])+(5.0-b["D9"]), b["D7"]))

print("\n  ARGUMENT FOR 'sloka_order' — Santhanam's table fragment (vol1.txt")
print("  lines 3881-3888). The extractor keeps PRINTED ROW ORDER inside a")
print("  column run: the Shad Varga column comes out '6 2 4 5 2 I' = rows 1-6.")
print("  The Saptha Varga column comes out in two blocks, split at the total.")
SAPTHA_RUN = [3.0, 2.5, 4.5, 20.0, 5.0, 2.0, 2.0, 1.0]   # as extracted
check("the extracted run carries the seven weights plus the 20.0 total",
      sorted(x for x in SAPTHA_RUN if x != 20.0) == [1.0,2.0,2.0,2.5,3.0,4.5,5.0],
      str(SAPTHA_RUN))
block1 = SAPTHA_RUN[:SAPTHA_RUN.index(20.0)]          # [3.0, 2.5, 4.5]
block2 = SAPTHA_RUN[SAPTHA_RUN.index(20.0) + 1:]      # [5.0, 2.0, 2.0, 1.0]

def is_subsequence(block, rows):
    """True iff `block` appears in `rows` in printed row order."""
    it = iter(rows)
    return all(any(near(r, x) for r in it) for x in block)

rows_a = [a[k] for k in SAPTAVARGA]
rows_b = [b[k] for k in SAPTAVARGA]
check("under 'sloka_order' BOTH extracted blocks run in printed row order",
      is_subsequence(block1, rows_a) and is_subsequence(block2, rows_a),
      f"rows {rows_a}")
check("under 'ascending_divisor' the FIRST block does NOT — 3.0, 2.5, 4.5 "
      "would be rows 3, 7, 4, out of order",
      not is_subsequence(block1, rows_b), f"rows {rows_b}")
check("the second block is order-compatible with BOTH, so it cannot arbitrate",
      is_subsequence(block2, rows_a) and is_subsequence(block2, rows_b))
check("the control: the Shad Varga column '6 2 4 5 2 I' IS in printed row "
      "order, which is why the run-order argument has any force at all",
      is_subsequence([6.0,2.0,4.0,5.0,2.0,1.0],
                     [swaviswa("shadvarga")[k] for k in SHADVARGA]))

print("\n  ...and when a reading IS named, the payload keeps the provenance:")
rs = vimsopaka("saptavarga", {k: "own" for k in SAPTAVARGA},
               saptavarga_reading="sloka_order")
check("saptavarga payload records WHICH reading was used",
      rs["saptavarga_reading"] == "sloka_order", str(rs["saptavarga_reading"]))
check("...names the four vargas that are not settled",
      rs["saptavarga_ambiguous"] == list(SAPTAVARGA_AMBIGUOUS))
check("...carries the UNAVAILABLE note into the payload itself",
      rs["saptavarga_unavailable_note"] == SAPTAVARGA_UNAVAILABLE)
check("...and the evidence for the reading chosen",
      rs["saptavarga_reading_evidence"] == SAPTAVARGA_READING_EVIDENCE["sloka_order"])
check("a NON-saptavarga payload carries none of those keys",
      not ({"saptavarga_ambiguous", "saptavarga_unavailable_note",
            "saptavarga_reading_evidence"} &
           set(vimsopaka("shadvarga", {k: "own" for k in SHADVARGA}))))
check("both readings still total 20 through the full pipeline",
      all(near(vimsopaka("saptavarga", {k: "own" for k in SAPTAVARGA},
                         saptavarga_reading=n)["points"], 20.0)
          for n in SAPTAVARGA_READINGS))


print("\nvv.21-25 Varga Viswa ladder — 20/18/15/10/7/5:")
for rung, want in (("own",20),("adhimitra",18),("mitra",15),
                   ("sama",10),("satru",7),("adhisatru",5)):
    check(f"{rung} = {want}", near(VARGA_VISWA[rung], want), f"got {VARGA_VISWA[rung]}")
check("exactly six rungs, no more", len(VARGA_VISWA) == 6 and len(RUNGS) == 6)
check("ladder is strictly descending as listed",
      all(VARGA_VISWA[RUNGS[i]] > VARGA_VISWA[RUNGS[i+1]] for i in range(len(RUNGS)-1)))
check("'own in every varga' scores the full 20 in every scheme",
      all(near(vimsopaka(s, {k: "own" for k in SCHEMES[s]})["points"], 20.0)
          for s in ("shadvarga","dasavarga","shodasavarga")))
check("'sworn enemy everywhere' floors at 5 (= 20 x 5/20)",
      all(near(vimsopaka(s, {k: "adhisatru" for k in SCHEMES[s]})["points"], 5.0)
          for s in ("shadvarga","dasavarga","shodasavarga")))


print("\nBOOK FIXTURE 1 — Santhanam's worked table, Vol I book p.99 (pdf p.98):")
print("  native born 11-2-1984, 22:35 IST, New Delhi; ascendant lord Venus at 9s 4d 32' 30\"")
# Division      occupation   Lord   Relationship  SV  VV   VS
venus_book = [
    ("D1",  "Capricorn", "Sat.",  "adhimitra", 6, 18, 5.4),
    ("D2",  "Cancer",    "Moon",  "adhisatru", 2,  5, 0.5),
    ("D3",  "Capricorn", "Sat.",  "adhimitra", 4, 18, 3.6),
    ("D9",  "Aquarius",  "Sat.",  "adhimitra", 5, 18, 4.5),
    ("D12", "Aquarius",  "Sat.",  "adhimitra", 2, 18, 1.8),
    ("D30", "Taurus",    "Ven.",  "own",       1, 20, 1.0),
]
r = vimsopaka("shadvarga", {k: rel for k, _, _, rel, _, _, _ in venus_book})
for (k, occ, lord, rel, sv, vv, vs), row in zip(venus_book, r["rows"]):
    ok = (row["varga"] == k and near(row["swaviswa"], sv)
          and near(row["varga_viswa"], vv) and near(row["points"], vs, 1e-6))
    check(f"{k} {occ} ({lord}) {rel}: SV={sv} VV={vv} -> VS={vs}", ok,
          f"got SV={row['swaviswa']} VV={row['varga_viswa']} VS={row['points']}")
check("VENUS TOTAL = 16.8", near(r["points"], 16.8, 1e-6), f"got {r['points']}")
check("book: 'Venus gets 16.8 points and hence he should confer wholly "
      "favourable effects' -> >15 band",
      r["verdict"]["effect"] == "yields wholly favourable effects", r["verdict"]["effect"])
check("book: 'when Shad Varga scheme is considered'", r["scheme"] == "shadvarga")
check("16.8 grades as Poorna (Santhanam's note)", r["grade"]["name"] == "Poorna", r["grade"]["name"])
check("16.8 is 84% of 20", near(r["grade"]["percent"], 84.0, 1e-9), str(r["grade"]["percent"]))


print("\nBOOK FIXTURE 2 — Vol I book p.389 (pdf p.388): 'Their Vimsopaka strengths are")
print("  respectively 16.45 and 16.80 points' (Jupiter and Mars, ch.29 nativity).")
print("  The book prints NO working and NO scheme for these, and the ch.29 chart's")
print("  longitude column is OCR-shredded, so they CANNOT be recomputed. What is")
print("  testable is that each total is ATTAINABLE under the weights we derived:")

def attainable(weights):
    """All totals reachable by assigning some rung to every varga, in cents."""
    sums = {0}
    for w in weights.values():
        cents = {round(w * vv / TOTAL * 100) for vv in VARGA_VISWA.values()}
        sums = {s + c for s in sums for c in cents}
    return sums

for target in (16.45, 16.80):
    hits = [s for s in ("shadvarga","dasavarga","shodasavarga")
            if round(target * 100) in attainable(swaviswa(s))]
    check(f"{target} is attainable under at least one derived scheme",
          bool(hits), f"schemes: {hits}")
check("16.80 is attainable in Shadvarga (as fixture 1 in fact attains it)",
      round(1680) in attainable(swaviswa("shadvarga")))
check("16.45 IS reachable in Shadvarga too — the Satru rung is 7/20 = 0.35, so "
      "even all-integer weights reach 0.05 granularity",
      round(1645) in attainable(swaviswa("shadvarga")))
check("16.45 IS reachable in Shodasavarga (0.5 x 18/20 = 0.45 supplies the 0.05)",
      round(1645) in attainable(swaviswa("shodasavarga")))
check("attainability therefore does NOT identify which scheme p.388 used — "
      "it only shows the derived weights are not arithmetically excluded",
      len([s for s in ("shadvarga","dasavarga","shodasavarga")
           if round(1645) in attainable(swaviswa(s))]) > 1)


print("\nvv.26-27 verdict bands — the sloka's own wording:")
check("below 5 -> 'not capable of giving auspicious results'",
      verdict(4.99)["effect"] == "not capable of giving auspicious results")
check("above 5 but below 10 -> 'yields some good effects'",
      verdict(7.5)["effect"] == "yields some good effects")
check("upto 15 -> 'indicative of mediocre effect'",
      verdict(14.99)["effect"] == "indicative of mediocre effect")
check("above 15 -> 'yields wholly favourable effects'",
      verdict(15.01)["effect"] == "yields wholly favourable effects")
check("a perfect 20 stays in the top band (not off the end)",
      verdict(20.0)["effect"] == "yields wholly favourable effects")
check("0.0 lands in the bottom band", verdict(0.0)["effect"].startswith("not capable"))
check("bands are contiguous and cover 0-20 with no gap",
      [b[0] for b in VERDICT_BANDS] == [0.0,5.0,10.0,15.0] and
      [b[1] for b in VERDICT_BANDS] == [5.0,10.0,15.0,20.0])
check("verdict is labelled as sloka (mula text)", verdict(12.0)["source"] == "sloka")
check("exactly 5.0 / 10.0 / 15.0 are FLAGGED as unaddressed by the sloka",
      all("boundary_open" in verdict(p) for p in (5.0, 10.0, 15.0)))
check("...and the flag is the module's own VERDICT_BOUNDARIES_OPEN text",
      verdict(10.0)["boundary_open"] == VERDICT_BOUNDARIES_OPEN)
check("a score NOT on a boundary carries no such flag",
      all("boundary_open" not in verdict(p) for p in (4.99, 7.5, 16.8, 20.0)))
# A negative total is impossible from vimsopaka() (every weight and every rung
# is positive), so it means the CALLER's arithmetic is wrong. It must not fall
# through onto the most favourable band.
try:
    v = verdict(-1.0)
    check("verdict(-1.0) REFUSES rather than returning the top band", False,
          f"it returned {v['effect']!r}")
except ValueError:
    check("verdict(-1.0) REFUSES rather than returning the top band", True)
try:
    verdict(float("nan"))
    check("verdict(nan) refuses too", False, "it returned")
except ValueError:
    check("verdict(nan) refuses too", True)
try:
    grade(-1.0)
    check("grade(-1.0) refuses on the same rule", False, "it returned")
except ValueError:
    check("grade(-1.0) refuses on the same rule", True)


print("\nvv.30-32 grades — EIGHT NAMES ARE THE SAGE'S, THE BANDS ARE SANTHANAM'S:")
check("grade is labelled 'note', never presented as mula",
      grade(12.0)["source"] == "note", grade(12.0)["source"])
check("all eight names present",
      set(GRADE_NAMES) == {"Poorna","Atipoorna","Madhya","Atimadhya",
                           "Heena","Atiheena","Swalpa","Atiswalpa"})
check("band width derived as 20/8 = 2.5, not typed", near(GRADE_BAND, 2.5), str(GRADE_BAND))
# Santhanam's table, book p.101 = pdf p.100 (the marker ===PDFPAGE 100=== is
# followed by the running head 'Clapter 7 lol') — reproduced strongest first.
santhanam = [("Atipoorna",17.5,20.0,87.5,100.0), ("Poorna",15.0,17.5,75.0,87.5),
             ("Atimadhya",12.5,15.0,62.5,75.0),  ("Madhya",10.0,12.5,50.0,62.5),
             ("Swalpa",7.5,10.0,37.5,50.0),      ("Atiswalpa",5.0,7.5,25.0,37.5),
             ("Heena",2.5,5.0,12.5,25.0),        ("Atiheena",0.0,2.5,0.0,12.5)]
for name, lo, hi, plo, phi in santhanam:
    g = grade(lo)
    ok = (g["name"] == name and near(g["from"], lo) and near(g["to"], hi)
          and near(g["percent_from"], plo) and near(g["percent_to"], phi))
    check(f"{name}: {lo}-{hi} pts = {plo}-{phi}%", ok,
          f"got {g['name']} {g['from']}-{g['to']} {g['percent_from']}-{g['percent_to']}%")
check("grade_table() returns all eight bands ascending",
      [g["name"] for g in grade_table()] == list(GRADE_NAMES))
check("percent is just points/20 (derived, not tabulated)",
      near(grade(13.3)["percent"], 66.5))

print("\n  Santhanam's printed bands OVERLAP at every 2.5 mark ('17.5 to 20.0'")
print("  AND '15.0 to 17.5'). grade() resolves upward — that is a CHOICE, and")
print("  it must be flagged, exactly as VERDICT_BOUNDARIES_OPEN flags vv.26-27:")
for p in (2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5):
    g = grade(p)
    check(f"grade({p}) resolves UPWARD and says so", "boundary_open" in g,
          f"{g['name']} {g['from']}-{g['to']}")
check("resolving upward means grade(17.5) is Atipoorna, not Poorna",
      grade(17.5)["name"] == "Atipoorna" and grade(15.0)["name"] == "Poorna",
      f"{grade(17.5)['name']} / {grade(15.0)['name']}")
check("the flag is the module's own GRADE_BOUNDARIES_OPEN text",
      grade(17.5)["boundary_open"] == GRADE_BOUNDARIES_OPEN)
check("0.0 and 20.0 are the OUTER edges — no band competes for them",
      "boundary_open" not in grade(0.0) and "boundary_open" not in grade(20.0))
check("a score inside a band carries no flag",
      all("boundary_open" not in grade(p) for p in (16.8, 14.45, 13.3, 1.0)))
check("GRADE_BOUNDARIES_OPEN cites the corrected page (pdf p.100, not p.99)",
      "pdf p.100" in GRADE_BOUNDARIES_OPEN and "pdf p.99" not in GRADE_BOUNDARIES_OPEN)


print("\nFALLBACK — natural relations only (dignity.py, ch.3 v.55), no temporal half:")
# Venus's six Shadvarga signs, exactly as the book's p.98 table lists them.
venus_signs = {"D1": 9, "D2": 3, "D3": 9, "D9": 10, "D12": 10, "D30": 1}
fb = natural_relation_rungs("venus", venus_signs)
check("D30 Taurus is Venus's own sign -> 'own' (the one rung it gets right)",
      fb["D30"] == "own", fb["D30"])
check("no 'adhimitra' or 'adhisatru' can EVER come out of it",
      not ({"adhimitra","adhisatru"} & set(fb.values())), str(sorted(set(fb.values()))))
check("book's five Adhimitra vargas degrade to Mitra",
      [fb[k] for k in ("D1","D3","D9","D12")] == ["mitra"]*4, str(fb))
check("book's Adhisatru Hora degrades to Satru", fb["D2"] == "satru", fb["D2"])
fbr = vimsopaka("shadvarga", fb)
check("fallback total for Venus = 14.45, NOT the book's 16.80",
      near(fbr["points"], 14.45, 1e-6), f"got {fbr['points']}")
check("and that crosses the sloka's 15-point line: 'mediocre', not 'wholly favourable'",
      fbr["verdict"]["effect"] == "indicative of mediocre effect", fbr["verdict"]["effect"])
check("so the fallback UNDER-reports here by 2.35 points",
      near(16.8 - fbr["points"], 2.35, 1e-6), f"gap {16.8 - fbr['points']:.2f}")
try:
    natural_relation_rungs("rahu", venus_signs)
    check("fallback refuses the nodes (BPHS gives them no rasi lordship)", False, "it returned")
except ValueError:
    check("fallback refuses the nodes (BPHS gives them no rasi lordship)", True)


print("\nCITATION HYGIENE — the translation numbers these as BLOCKS ('17-19',")
print("'21-25'); it has no verse-by-verse split, so no string may claim one:")
import vimsopaka as _m
for name in ("SAPTAVARGA_UNAVAILABLE", "EXALTATION_RUNG_UNSPECIFIED",
             "VERDICT_BOUNDARIES_OPEN", "GRADE_BANDS_ARE_SANTHANAMS_NOTE",
             "GRADE_BOUNDARIES_OPEN", "NATURAL_FALLBACK_IS_WEAKER"):
    s = getattr(_m, name)
    bad = [v for v in ("v.17", "v.18", "v.19", "v.21", "v.22", "v.23", "v.24",
                       "v.25", "v.26", "v.27", "v.30", "v.31", "v.32")
           if v in s and ("v" + v) not in s and ("-" + v[2:]) not in s]
    check(f"{name} uses block verse form only", not bad, f"found {bad}")
check("SAPTAVARGA_UNAVAILABLE cites vv.17-19 (where the damaged list lives)",
      "vv.17-19" in SAPTAVARGA_UNAVAILABLE)
check("EXALTATION_RUNG_UNSPECIFIED cites vv.21-25 (where the six rungs live)",
      "vv.21-25" in _m.EXALTATION_RUNG_UNSPECIFIED)

print("\nQUOTATION RULE — quotes are VERBATIM, every repair in [brackets]:")
with open(_m.__file__, encoding="utf-8") as fh:
    doc = fh.read()          # docstring AND the comment blocks that quote too
for frag, where in (
    ("classrfied as unser:Poorna", "vv.30-32"),
    ("respectively are 6,2, 4,5,2 and l.", "vv.17-19"),
    ("strength for which is : 5, 2, 3,2t,412, 2 and 1.", "vv.17-19"),
    ("for the other 8 divisions' I I each'", "v.20"),
    ("Navamsa 3, Rasi 3l'", "vv.21-25"),
    ("V\"ig\" Vi.\"\" ooi diuid\" by 20", "vv.26-27"),
    ("you fintl 3.5 which is the Swaviswa.", "note to vv.26-27"),
):
    check(f"{where}: the DAMAGED text is quoted verbatim, not cleaned up",
          frag in doc, "" if frag in doc else f"MISSING {frag!r}")
for repair, where in (
    ("class[i]fied as un[d]er", "vv.30-32"),
    ("[S]walpa and Atiswa[l]pa", "vv.30-32"),
    ("2[.5], 4[.5]", "vv.17-19"),
    ("[1½] each", "v.20"),
    ("Rasi 3[.5]", "vv.21-25"),
    ("you fin[d] 3.5", "note to vv.26-27"),
):
    check(f"{where}: the repair is shown in [brackets]", repair in doc,
          "" if repair in doc else f"MISSING {repair!r}")


print("\nInput validation — a bad rung or a missing varga must not score silently:")
try:
    vimsopaka("shadvarga", {k: "own" for k in SHADVARGA[:-1]})
    check("missing varga raises", False, "it returned")
except ValueError:
    check("missing varga raises", True)
try:
    vimsopaka("shadvarga", {**{k: "own" for k in SHADVARGA}, "D1": "exalted"})
    check("unknown rung ('exalted' is NOT one of vv.21-25's six) raises", False, "it returned")
except ValueError:
    check("unknown rung ('exalted' is NOT one of vv.21-25's six) raises", True)
try:
    swaviswa("navavarga")
    check("unknown scheme raises", False, "it returned")
except ValueError:
    check("unknown scheme raises", True)


print("\n" + ("ALL PASS" if not fails else f"FAILURES ({len(fails)}): {fails}"))
sys.exit(1 if fails else 0)
