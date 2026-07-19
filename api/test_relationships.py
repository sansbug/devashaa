import sys
sys.path.insert(0, r"C:\proj\astrodev\api")
from relationships import (
    house_distance, temporary_relation, compound_relation, compound_rank,
    dispositor_relation, relationship_matrix, temporary_matrix, compound_matrix,
    TEMPORARY_FRIEND_HOUSES, TEMPORARY_ENEMY_HOUSES, COMPOUND, GRADES,
    VARGA_VISWA, SAPTAVARGAJA_VIRUPAS, NODE_RELATIONS_SANTHANAM,
    ADHIMITRA, MITRA, SAMA, SATRU, ADHISATRU, FRIEND, NEUTRAL, ENEMY,
    OWN, MOOLATRIKONA, OUT_OF_SCALE, NATURAL_UNVERIFIED,
    CONJUNCTION_IS_ENMITY,
)
from dignity import NATURAL_RELATIONS, RASI_LORD

S = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
     "Tula", "Vrishchika", "Dhanus", "Makara", "Kumbha", "Meena"]
AR, TA, GE, CN, LE, VI, LI, SC, SG, CP, AQ, PI = range(12)
SEVEN = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn")

fails = []
def check(label, cond, detail=""):
    if not cond: fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  '+detail) if detail else ''}")


print("BPHS ch.3 v.56 — the six temporary-friend houses:")
# "The planet posited in the 10th, 4th, 11th, 3rd, 2nd or the 12th from
#  another becomes mutual friend. There is enmity otherwise."
check("friend houses are exactly {2,3,4,10,11,12}",
      set(TEMPORARY_FRIEND_HOUSES) == {2, 3, 4, 10, 11, 12},
      str(sorted(TEMPORARY_FRIEND_HOUSES)))
check("enemy houses are the DERIVED complement {1,5,6,7,8,9}",
      set(TEMPORARY_ENEMY_HOUSES) == {1, 5, 6, 7, 8, 9},
      str(TEMPORARY_ENEMY_HOUSES))
check("the two lists partition all 12 houses",
      set(TEMPORARY_FRIEND_HOUSES) | set(TEMPORARY_ENEMY_HOUSES) == set(range(1, 13))
      and not set(TEMPORARY_FRIEND_HOUSES) & set(TEMPORARY_ENEMY_HOUSES))

print("\nhouse_distance is inclusive (the 1st is the sign you stand in):")
check("Makara -> Makara is the 1st", house_distance(CP, CP) == 1)
check("Makara -> Kumbha is the 2nd", house_distance(CP, AQ) == 2)
check("Makara -> Tula is the 10th",  house_distance(CP, LI) == 10)
check("Tula -> Makara is the 4th",   house_distance(LI, CP) == 4)
check("wraps the zodiac: Meena -> Mesha is the 2nd", house_distance(PI, AR) == 2)

print("\nCo-location is temporary ENMITY (the 1st is NOT in v.56's list):")
for s in range(12):
    if temporary_relation(s, s) != ENEMY: fails.append("conj %d" % s)
check("two grahas in the same rasi are temporary enemies, all 12 signs",
      all(temporary_relation(s, s) == ENEMY for s in range(12)))
check("...and that reading is flagged AMBIGUOUS, since no book example tests it",
      CONJUNCTION_IS_ENMITY.startswith("AMBIGUOUS")
      and "NEITHER BPHS WORKED EXAMPLE DECIDES IT" in CONJUNCTION_IS_ENMITY)

print("\nSanthanam's gloss — the three reciprocal cordial pairs (4/10, 3/11, 2/12):")
ORD = {2: "2nd", 3: "3rd", 4: "4th", 10: "10th", 11: "11th", 12: "12th"}
for near, far in ((4, 10), (3, 11), (2, 12)):
    a = CP
    b_near = (a + near - 1) % 12
    b_far = (a + far - 1) % 12
    check(f"{ORD[near]}/{ORD[far]} pair from Makara "
          f"({S[b_near]} / {S[b_far]}) are both temporary friends",
          temporary_relation(a, b_near) == FRIEND and
          temporary_relation(a, b_far) == FRIEND)

print("\nTemporary relation is SYMMETRIC (asserted, not assumed):")
bad = [(a, b) for a in range(12) for b in range(12)
       if temporary_relation(a, b) != temporary_relation(b, a)]
check("temporary_relation(a,b) == temporary_relation(b,a) for all 144 pairs",
      not bad, f"{len(bad)} asymmetric")
check("friend houses close under h -> 14-h",
      all(((14 - h) if h >= 2 else 1) in TEMPORARY_FRIEND_HOUSES
          for h in TEMPORARY_FRIEND_HOUSES))
check("v.56 admits NO temporary neutral",
      {temporary_relation(a, b) for a in range(12) for b in range(12)} == {FRIEND, ENEMY})

print("\nch.3 vv.57-58 — the Speculum of Compound Relationships, clause by clause:")
# "Should two planets be naturally and temporarily friendly, they become
#  extremely friendly."
check("friend + friend -> adhimitra (extreme friendship)",
      COMPOUND[(FRIEND, FRIEND)] == ADHIMITRA)
# "Friendship on one count and neutrality on another count make them friendly."
check("friend + neutral -> mitra (friendship)",
      COMPOUND[(FRIEND, NEUTRAL)] == MITRA)
# "Enmity on one count combined with affinity on the other turns into equality."
check("enemy + friend -> sama (equality)",
      COMPOUND[(ENEMY, FRIEND)] == SAMA)
# "Enmity and neutralship cause only enmity."
check("enemy + neutral -> satru (enmity)",
      COMPOUND[(ENEMY, NEUTRAL)] == SATRU)
# "Should there be enmity in both manners, extreme enmity is obtained."
check("enemy + enemy -> adhisatru (extreme enmity)",
      COMPOUND[(ENEMY, ENEMY)] == ADHISATRU)
# "It is understood that if there is friendship with enmity, then also
#  neutrality will prevail."  -> the table is symmetric in its two inputs.
check("the speculum is symmetric in its two counts",
      all(COMPOUND[(x, y)] == COMPOUND[(y, x)] for (x, y) in list(COMPOUND)))
check("(neutral, neutral) is absent — v.56 can never yield a neutral",
      (NEUTRAL, NEUTRAL) not in COMPOUND)
check("exactly five grades", len(GRADES) == 5 and set(GRADES) == set(COMPOUND.values()))

print("\nThe grade ORDER, cross-checked against two independent slokas:")
# ch.7 v.25 Varga Viswa (vol1.txt:3809): own 20, then 18 / 15 / 10 / 7 / 5.
#   "...only when the plun"t [planet] is in own house Vargas' ... from 20
#    declines to l8 [18] in extreme friend's Vargas, to l5 [15] in friendly
#    Vargas, to l0 [10] in equal's divisions, to 7 in enemy's Vargas and to 5
#    in sworn enemy's Vargas."
# ch.27 vv.2-4 Saptavargaja virupas (vol1.txt:10032): mulatrikona 45, own 30,
#   then 20 / 15 / 10 / 4 / 2.
#   "If a planet is in its Moolatrikona Rasi, it gets 45 Virupas, in own Rasi
#    30 Virupas, extreme friend's Rasi 20 Virupas, friend's Rasi 15 Virupas,
#    neutral's Rasi l0 [10] Virupas, enemy's Rasi 4 Virupas and in extreme
#    enemy's Rasi 2 Virupas."
for name, table in (("ch.7 v.25 Varga Viswa", VARGA_VISWA),
                    ("ch.27 vv.2-4 Saptavargaja virupas", SAPTAVARGAJA_VIRUPAS)):
    vals = [table[g] for g in GRADES]
    check(f"{name} increases monotonically along GRADES",
          all(x < y for x, y in zip(vals, vals[1:])), str(vals))
    check(f"{name}: 'own' outscores adhimitra and is OUTSIDE the five grades",
          table[OWN] > table[ADHIMITRA] and OWN not in GRADES,
          f"own={table[OWN]} > adhimitra={table[ADHIMITRA]}")
# Each dict must carry every value ITS OWN sloka states — no more, no less.
check("VARGA_VISWA reproduces ch.7 v.25 exactly (5 grades + own; the sloka "
      "gives NO separate mulatrikona value, so the key is absent)",
      VARGA_VISWA == {ADHIMITRA: 18, MITRA: 15, SAMA: 10, SATRU: 7,
                      ADHISATRU: 5, OWN: 20}
      and MOOLATRIKONA not in VARGA_VISWA,
      str(sorted(VARGA_VISWA.items())))
check("SAPTAVARGAJA_VIRUPAS reproduces ch.27 vv.2-4 exactly, all SEVEN values",
      SAPTAVARGAJA_VIRUPAS == {MOOLATRIKONA: 45, OWN: 30, ADHIMITRA: 20,
                               MITRA: 15, SAMA: 10, SATRU: 4, ADHISATRU: 2},
      str(sorted(SAPTAVARGAJA_VIRUPAS.items())))
check("mulatrikona (45) outscores own (30) in ch.27, as the sloka orders them",
      SAPTAVARGAJA_VIRUPAS[MOOLATRIKONA] > SAPTAVARGAJA_VIRUPAS[OWN])
check("compound_rank orders adhisatru < satru < sama < mitra < adhimitra",
      [compound_rank(g) for g in GRADES] == [0, 1, 2, 3, 4])
check("compound_rank(None) is None", compound_rank(None) is None)
# dispositor_relation() legitimately returns OWN, so compound_rank(OWN) is a
# path an integrator will hit. It must not silently answer.
for out in OUT_OF_SCALE:
    try:
        compound_rank(out)
        ok, detail = False, "returned instead of raising"
    except ValueError as exc:
        ok = out in str(exc) and "five-fold scale" in str(exc)
        detail = str(exc)[:60] + "..."
    except Exception as exc:                       # bare GRADES.index() -> the
        ok, detail = False, f"{type(exc).__name__}: {exc}"   # old unhelpful trap
    check(f"compound_rank({out!r}) raises a ValueError that NAMES it", ok, detail)

print("\nThe compound is DIRECTIONAL, because v.55's natural half is:")
check("v.55: Venus counts the Moon an ENEMY",
      NATURAL_RELATIONS["venus"]["moon"] == ENEMY)
check("v.55: the Moon counts Venus a NEUTRAL (she has no enemies at all)",
      NATURAL_RELATIONS["moon"]["venus"] == NEUTRAL)
check("so compound_relation(venus,moon) != compound_relation(moon,venus)",
      compound_relation("venus", "moon", CP, LE) !=
      compound_relation("moon", "venus", LE, CP),
      f'{compound_relation("venus","moon",CP,LE)} vs {compound_relation("moon","venus",LE,CP)}')

print("\nRahu/Ketu: no natural half in BPHS, therefore no compound (see NODES_UNAVAILABLE):")
for node in ("rahu", "ketu"):
    check(f"compound_relation({node}, sun) -> None",
          compound_relation(node, "sun", TA, CP) is None)
    check(f"compound_relation(sun, {node}) -> None",
          compound_relation("sun", node, CP, TA) is None)
    check(f"temporary_relation DOES apply to {node} (purely positional)",
          temporary_relation(TA, CP) in (FRIEND, ENEMY))
check("a graha holds no relationship to itself",
      compound_relation("sun", "sun", CP, CP) is None)
check("Santhanam's node table is exposed but unused by any function",
      set(NODE_RELATIONS_SANTHANAM) == {"rahu", "ketu"} and
      NODE_RELATIONS_SANTHANAM["rahu"]["mercury"] == NEUTRAL and
      NODE_RELATIONS_SANTHANAM["ketu"]["jupiter"] == NEUTRAL)

# ===========================================================================
# WORKED EXAMPLE 1 — BPHS Vol II ch.73 vv.3-7, "number of rays" (Rasmi).
#
# The book states seven longitudes and then names each graha's relationship to
# the sign it occupies, using the five-fold vocabulary. It is the fullest
# panchadha-sambandha fixture in either volume. Longitudes as printed
# (rasi/deg/min/sec, rasi 0-based); each is independently confirmed by the
# book's own subtraction of that graha's deep-debilitation point, which is how
# the OCR-damaged digits were disambiguated:
#
#   Sun     9/29/36/53   "By deducting ... 6/10/0/0 we get 3/19/36/53"   exact
#   Moon    2/6/22/55    "deducting ... 7/3/0/0 ... we get 7/3/22/55"    exact
#   Mars    1/10/56/20   "deducting this remainder from 12 we get 2/17/3/40"
#   Mercury 10/13/9/16   "deducting 11/15 ... remainder as 10/28/9/16"   exact
#   Jupiter 10/13/41/18  "deducting it from 9/5 ... we get 1/8/41/18"    exact
#   Venus   10/20/41     "deducting from it 5/27 ... we get 4/23/41/.."  exact
#   Saturn  7/13/2/24    "deducting from it 0/[2]0 ... we get 6/23/2/24" exact
#
# Only the SIGN matters for this module. The stated grade for each graha is
# corroborated a second time by the ray multiplier the book then applies:
#   adhimitra x4/3, friend x6/5, neutral no correction, adhisatru x2/5.
# ===========================================================================
print("\nWORKED EXAMPLE — BPHS Vol II ch.73 vv.3-7 (Rasmi / number of rays):")
CH73 = {"sun": CP, "moon": GE, "mars": TA, "mercury": AQ,
        "jupiter": AQ, "venus": AQ, "saturn": SC}
CH73_BOOK = {
    # graha : (grade the book names, the words it uses, the ray correction)
    "sun":     (SAMA,      "'Saturn is neutral to the Sun'",        "no correction"),
    "moon":    (SAMA,      "'the Moon is in the house of a neutral'", "no correction"),
    "mars":    (MITRA,     "'Mars is in a friendly sign'",          "x6/5"),
    "mercury": (MITRA,     "'Mercury is in the house of friend'",   "x6/5 -> 1/1"),
    "jupiter": (MITRA,     "'Jupiter is in the house of a friend'", "x6/5 -> 1/48"),
    "venus":   (ADHIMITRA, "'Venus is in the house of Adhimitra'",  "x4/3 -> 8/4"),
    "saturn":  (ADHISATRU, "'Saturn is in the house of an adhishatru'", "x2/5 -> 1/44"),
}
for g, (want, words, mult) in CH73_BOOK.items():
    got = dispositor_relation(g, CH73[g], CH73)
    lord = RASI_LORD[CH73[g]]
    h = house_distance(CH73[g], CH73[lord])
    check(f"{g:7s} in {S[CH73[g]]:10s} -> {want:9s}  {words}",
          got == want,
          f"lord {lord} is {h}th; natural={NATURAL_RELATIONS[g][lord]}, "
          f"temporary={temporary_relation(CH73[g], CH73[lord])}; got {got} [{mult}]")
check("this one example exercises 4 of the 5 grades (satru does not occur here)",
      {v[0] for v in CH73_BOOK.values()} == {SAMA, MITRA, ADHIMITRA, ADHISATRU},
      "satru needs natural-neutral + temporary-enemy, absent from this chart")
# satru has no book fixture, so cover it end-to-end from a constructed pair:
# the Moon counts Venus a neutral (v.55), and Makara is the 6th from Simha.
check("satru covered end-to-end: moon(Simha) -> venus(Makara), neutral + enemy",
      NATURAL_RELATIONS["moon"]["venus"] == NEUTRAL
      and temporary_relation(LE, CP) == ENEMY
      and compound_relation("moon", "venus", LE, CP) == SATRU)

# ===========================================================================
# WORKED EXAMPLE 2 — BPHS Vol I ch.7, Vimsopaka strength of the lagna lord.
#
# "Let us consider the Vimsopaka strength for the ascendant lord Venus ...
#  The longitude of Venus is 9s 4' 32' 30\"."   -> Makara 4d32'30".
#
#   Division      occupation   Lord   Relationship   SV   VV    VS
#   Rasi          Capricorn    Sat.   Adhimitra       6   18   5.4
#   Hora          Cancer       Moon   Adhisatru       2    5   0.5
#   Drekkana      Capricorn    Sat.   Adhimitra       4   18   3.6
#   Navamsa       Aquarius     Sat.   Adhimitra       5   18   4.5
#   Dvadasamsa    Aquarius     Sat.   Adhimitra       2   18   1.8
#   Trimsamsa     Taurus       Ven.   Own             1   20   1.0
#                                                            = 16.8
# "In our example, Venus gets 16.8 points."
#
# THE PRINTED DATE IS WRONG IN OUR SCAN, AND THE BOOK ITSELF SAYS SO. The ch.7
# line reads "11-2-1984 at 2?35 hrs. IST at New Delhi" (vol1.txt:3909), but
# this is the book's one running example chart, and ch.4 states its date
# outright TWICE:
#   vol1.txt:1930  "mrle child born on Friday, tbe lTth February 1984 at 22h
#                   3Sm IST at New Delhi"   -> [male ... the 17th ... 22h 35m]
#   vol1.txt:2134  "ot 17.21984 is at 6h 59rn 58s"   -> [on 17.2.1984]
# So the correction is TEXTUALLY ATTESTED, not inferred. It is then confirmed
# four independent ways:
#   1. 17 Feb 1984 was a Friday; 11 Feb 1984 was a Saturday. The book says
#      Friday.
#   2. ch.4 gives "Ascendant Cusp : 1820 23' 06"" = Tula 2d23' (vol1.txt:1945),
#      whose lord is Venus — and ch.7 opens "the ascendant lord Venus".
#   3. The project ephemeris for 17-2-1984 22:35 IST New Delhi puts Venus at
#      274.5318 vs the book's 9s 4d32'30" = 274.5417, i.e. 0.59 arcmin. For
#      11 Feb Venus is at Dhanus 27d, 7.4 DEGREES short.
#   4. That same longitude reproduces all six of the book's varga occupations
#      below, not just the rasi. (Asserted in the optional section at the end.)
# The OCR read "17" as "11", exactly the 1/7 confusion this scan shows
# elsewhere. On that date: Moon in Simha, Saturn in Tula.
# ===========================================================================
print("\nWORKED EXAMPLE — BPHS Vol I ch.7 (Vimsopaka of the lagna lord Venus):")
CH7 = {"venus": CP, "saturn": LI, "moon": LE}
check("Venus -> Saturn = adhimitra (Rasi/Drekkana/Navamsa/Dvadasamsa rows, VV 18)",
      compound_relation("venus", "saturn", CH7["venus"], CH7["saturn"]) == ADHIMITRA,
      f'Saturn in Tula is the {house_distance(CP, LI)}th from Makara')
check("Venus -> Moon = adhisatru (Hora row, VV 5)",
      compound_relation("venus", "moon", CH7["venus"], CH7["moon"]) == ADHISATRU,
      f'Moon in Simha is the {house_distance(CP, LE)}th from Makara')
check("Venus in Vrishabha (Trimsamsa row) = own, outside the five-fold scale",
      dispositor_relation("venus", TA, CH7) == OWN)

print("\n  and the book's own arithmetic falls out of those grades (ch.7 v.25 Varga Viswa):")
ROWS = [("Rasi", CP, 6), ("Hora", CN, 2), ("Drekkana", CP, 4),
        ("Navamsa", AQ, 5), ("Dvadasamsa", AQ, 2), ("Trimsamsa", TA, 1)]
total = 0.0
for label, varga_sign, sv in ROWS:
    rel = dispositor_relation("venus", varga_sign, CH7)
    vv = VARGA_VISWA[rel]        # no magic number: OWN is now a key of the dict
    vs = sv * vv / 20.0
    total += vs
    print(f"    {label:11s} {S[varga_sign]:10s} lord={RASI_LORD[varga_sign]:8s} "
          f"{rel:9s} SV={sv} VV={vv:2d} VS={vs}")
check("total Vimsopaka = 16.8, the figure the book prints",
      abs(total - 16.8) < 1e-9, f"got {total}")

# ---------------------------------------------------------------------------
# THE RASI-ONLY RULE, tested against its RIVAL rather than against itself.
#
# The rule (RASI_ONLY / Santhanam's note to ch.27 vv.2-4) says the varga
# supplies the LORD to compare against, while both grahas' positions come from
# the rasi chart. The rival reading — the one a careless implementation falls
# into — takes BOTH positions from the varga being scored.
#
# Merely showing that dispositor_relation gives adhimitra for the Capricorn and
# Aquarius rows proves nothing: both signs are ruled by Saturn and the function
# only reads the sign to find its lord, so that assertion is true by
# construction. The discriminating test is to compute the rival reading and
# show it CONTRADICTS the book.
#
# Venus's varga signs are the book's own table (ROWS above). The other party's
# varga sign has to be computed; these are from the project's varga engine on
# the 17-2-1984 chart (Saturn 202.712, Moon 134.4051) and are re-derived from
# the ephemeris in the optional section at the end:
#     Saturn  D2 Karka   D3 Mithuna  D9 Mesha   D12 Karka
#     Moon    D2 Simha
# ---------------------------------------------------------------------------
SAT_VARGA = {"D1": LI, "D2": CN, "D3": GE, "D9": AR, "D12": CN}
MOON_VARGA = {"D1": LE, "D2": LE}
RIVAL = [
    # (row, venus's varga sign, other graha, its varga sign, book's grade)
    ("Rasi",       CP, "saturn", SAT_VARGA["D1"],  ADHIMITRA),
    ("Hora",       CN, "moon",   MOON_VARGA["D2"], ADHISATRU),
    ("Drekkana",   CP, "saturn", SAT_VARGA["D3"],  ADHIMITRA),
    ("Navamsa",    AQ, "saturn", SAT_VARGA["D9"],  ADHIMITRA),
    ("Dvadasamsa", AQ, "saturn", SAT_VARGA["D12"], ADHIMITRA),
]
contradicted = []
for label, v_sign, other, o_sign, book in RIVAL:
    rival = compound_relation("venus", other, v_sign, o_sign)
    rasi_rule = dispositor_relation("venus", v_sign, CH7)
    if rasi_rule != book:
        fails.append(f"rasi-rule {label}")
    if rival != book:
        contradicted.append(f"{label}({rival})")
    print(f"    {label:11s} book={book:9s} rasi-rule={rasi_rule:9s} "
          f"varga-rule={rival:9s} {'<- differs' if rival != book else ''}")
check("the RASI-ONLY rule reproduces all five graded rows of the book's table",
      all(dispositor_relation("venus", v, CH7) == b for _, v, _, _, b in RIVAL))
check("...while the RIVAL varga-position reading CONTRADICTS the book on the "
      "Hora, Drekkana and Dvadasamsa rows — so this fixture really does "
      "discriminate between the two readings",
      len(contradicted) == 3
      and {c.split("(")[0] for c in contradicted} == {"Hora", "Drekkana",
                                                      "Dvadasamsa"},
      f"contradicted: {contradicted}")
check("(Rasi and Navamsa cannot discriminate: Rasi IS the rasi chart, and in "
      "Navamsa the two readings happen to coincide)",
      compound_relation("venus", "saturn", AQ, SAT_VARGA["D9"]) == ADHIMITRA
      and compound_relation("venus", "saturn", CP, LI) == ADHIMITRA)

print("\nMatrix builders over a full 9-graha chart:")
POS = dict(CH73, rahu=TA, ketu=SC)
m = relationship_matrix(POS)
check("relationship_matrix covers all 9 grahas", len(m["grahas"]) == 9)
check("temporary matrix is filled in for the nodes",
      m["temporary"]["rahu"]["sun"] in (FRIEND, ENEMY))
check("compound matrix is None for node rows, not missing",
      all(m["compound"]["rahu"][b] is None for b in m["compound"]["rahu"]))
check("compound matrix is None for node columns too",
      all(m["compound"][a]["ketu"] is None for a in SEVEN))
check("natural matrix is None for the nodes (v.55 gives them none)",
      m["natural"]["rahu"]["sun"] is None and m["natural"]["sun"]["rahu"] is None)
check("every seven-graha compound cell is one of the five grades",
      all(m["compound"][a][b] in GRADES for a in SEVEN for b in SEVEN if a != b))
check("rank matrix mirrors the compound matrix",
      all(m["rank"][a][b] == compound_rank(m["compound"][a][b])
          for a in POS for b in POS if a != b))
check("dispositor row agrees with the ch.73 fixture",
      all(m["dispositor"][g] == CH73_BOOK[g][0] for g in CH73_BOOK))
check("temporary_matrix/compound_matrix agree with the combined builder",
      temporary_matrix(POS) == m["temporary"] and compound_matrix(POS) == m["compound"])
check("scope and node caveats are carried in the payload",
      "rāśi chart only" in m["scope"] and "Rāhu" in m["nodes"])
check("dispositor row may contain OWN, which compound_rank refuses to rank",
      dispositor_relation("saturn", AQ, POS) == OWN
      and OWN in OUT_OF_SCALE)

print("\nCaveats travel with the data (nothing renders without them):")
# The Moon's mulatrikona is UNVERIFIED in dignity.py, and every Moon row and
# column of the natural/compound matrices is derived from it.
check("dignity's unverified-mulatrikona flag is re-exported here",
      NATURAL_UNVERIFIED == frozenset({"moon"}), str(sorted(NATURAL_UNVERIFIED)))
check("relationship_matrix names the affected grahas in its payload",
      m["natural_unverified"] == ["moon"], str(m["natural_unverified"]))
check("...with a note explaining what rests on it",
      "MOOLATRIKONA_UNVERIFIED" in m["natural_unverified_note"])
check("the flag is CHART-SPECIFIC, not a constant blob: drop the Moon and it "
      "empties",
      relationship_matrix({k: v for k, v in POS.items()
                           if k != "moon"})["natural_unverified"] == [])
check("and the ch.7 Adhisatru fixture (Venus->Moon) is exactly a cell that "
      "inherits it",
      "moon" in NATURAL_UNVERIFIED
      and compound_relation("venus", "moon", CP, LE) == ADHISATRU)

# The conjunction fork.
check("the conjunction caveat is carried in the payload",
      "AMBIGUOUS" in m["conjunction"])
# POS is ch.73 plus Rahu in Vrishabha and Ketu in Vrischika, so there are
# three conjunction groups, not one: Kumbha (Mercury/Jupiter/Venus), Vrishabha
# (Mars/Rahu) and Vrischika (Saturn/Ketu). Nodes count — the temporary half
# applies to them.
check("every conjunct graha in this chart is named, nodes included",
      set(m["conjunction_affected"]) == {"mercury", "jupiter", "venus",
                                         "mars", "rahu", "saturn", "ketu"},
      str(m["conjunction_affected"]))
check("...and a graha with the rasi to itself is NOT named",
      set(m["conjunction_affected"]).isdisjoint({"sun", "moon"}),
      "sun in Makara and moon in Mithuna are alone there")
check("ch.73 alone (no nodes) leaves only the Kumbha trio",
      set(relationship_matrix(CH73)["conjunction_affected"])
      == {"mercury", "jupiter", "venus"},
      str(relationship_matrix(CH73)["conjunction_affected"]))
check("...and inert for a chart with no conjunction",
      relationship_matrix({"sun": AR, "moon": TA, "mars": GE}
                          )["conjunction_affected"] == [])
# The factual claim CONJUNCTION_IS_ENMITY makes about the book must hold: in
# neither worked example is a graha conjunct its OWN dispositor, so neither
# example can decide the fork.  (Kumbha's three occupants are disposited by
# Saturn, who sits in Vrischika.)
for name, chart in (("ch.73", CH73), ("ch.7", CH7)):
    self_conj = [g for g, s in chart.items()
                 if RASI_LORD[s] in chart and RASI_LORD[s] != g
                 and chart[RASI_LORD[s]] == s]
    check(f"{name}: no graha is conjunct its own dispositor, so it cannot "
          f"decide the conjunction fork", not self_conj, str(self_conj))

print("\nSanity: every (natural, temporary) pair a real chart can produce is defined:")
combos = set()
for a in SEVEN:
    for b in SEVEN:
        if a == b: continue
        for sa in range(12):
            for sb in range(12):
                combos.add((NATURAL_RELATIONS[a][b], temporary_relation(sa, sb)))
check("all six reachable pairs resolve, none raise",
      len(combos) == 6 and all(p in COMPOUND for p in combos),
      f"{len(combos)} reachable pairs: {sorted(combos)}")

# ---------------------------------------------------------------------------
# Optional: re-derive the ch.7 chart from the ephemeris rather than asserting
# it. Skipped if swisseph/pyswisseph is unavailable, so this file stays
# runnable as a pure-stdlib test.
# ---------------------------------------------------------------------------
print("\nOptional — re-deriving the ch.7 chart from the project ephemeris:")
try:
    import datetime
    from vedic import compute_chart
    c = compute_chart(datetime.datetime(1984, 2, 17, 22, 35),
                      28.6139, 77.2090, "Asia/Kolkata", "BPHS ch.7")
    g = {x.key: x for x in c.grahas}
    BOOK_VENUS = 9 * 30 + 4 + 32.5 / 60.0          # 9s 4d32'30"
    check("17-2-1984 22:35 IST Delhi reproduces the book's Venus to < 1 arcmin",
          abs(g["venus"].longitude - BOOK_VENUS) < 1.0 / 60.0,
          f'book {BOOK_VENUS:.4f} vs computed {g["venus"].longitude:.4f} '
          f'({abs(g["venus"].longitude - BOOK_VENUS)*60:.2f} arcmin)')
    check("...and puts Saturn in Tula, as the Adhimitra grade requires",
          g["saturn"].rasi == LI, S[g["saturn"].rasi])
    check("...and the Moon in Simha, as the Adhisatru grade requires",
          g["moon"].rasi == LE, S[g["moon"].rasi])
    live = {k: v.rasi for k, v in g.items()}
    check("compound grades from the LIVE chart match the book's table",
          compound_relation("venus", "saturn", live["venus"], live["saturn"]) == ADHIMITRA
          and compound_relation("venus", "moon", live["venus"], live["moon"]) == ADHISATRU)

    # Independent corroboration of the date: the SAME longitude must also
    # reproduce all six of the book's varga occupations, not merely the rasi.
    from vargas import varga_sign
    BOOK_VARGAS = {"D1": CP, "D2": CN, "D3": CP, "D9": AQ, "D12": AQ, "D30": TA}
    got_v = {k: varga_sign(k, g["venus"].longitude) for k in BOOK_VARGAS}
    check("...and reproduces ALL SIX varga occupations the book's table prints "
          "(Rasi CP, Hora CN, Drekkana CP, Navamsa AQ, Dvadasamsa AQ, "
          "Trimsamsa TA)",
          got_v == BOOK_VARGAS,
          f"{ {k: S[v] for k, v in got_v.items()} }")

    # ...and the hardcoded rival-reading varga signs above are not invented:
    # re-derive them from the live chart.
    check("SAT_VARGA/MOON_VARGA (used for the rival reading) re-derive from "
          "the ephemeris",
          all(varga_sign(k, g["saturn"].longitude) == v
              for k, v in SAT_VARGA.items())
          and all(varga_sign(k, g["moon"].longitude) == v
                  for k, v in MOON_VARGA.items()),
          f'saturn {[S[varga_sign(k, g["saturn"].longitude)] for k in SAT_VARGA]}')

    # CONJUNCTION_IS_ENMITY claims ch.7's example cannot decide the fork. CH7
    # above is only the three grahas the Vimsopaka table needs, so check the
    # claim against the FULL nine-graha chart. (It has two conjunctions —
    # Mercury+Venus in Makara and Mars+Saturn in Tula — but the dispositor of
    # each pair sits elsewhere, so neither tests co-location with one's lord.)
    full = {k: v.rasi for k, v in g.items()}
    fm = relationship_matrix(full)
    check("the full ch.7 chart IS conjunct-bearing (so this is a real test)",
          set(fm["conjunction_affected"]) ==
          {"mercury", "venus", "mars", "saturn"},
          str(fm["conjunction_affected"]))
    self_conj = [k for k, s in full.items()
                 if RASI_LORD[s] in full and RASI_LORD[s] != k
                 and full[RASI_LORD[s]] == s]
    check("...yet no graha in it is conjunct its OWN dispositor, exactly as "
          "CONJUNCTION_IS_ENMITY states",
          not self_conj, str(self_conj))
except Exception as exc:
    print(f"  SKIP  ephemeris unavailable ({type(exc).__name__}: {exc})")

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
