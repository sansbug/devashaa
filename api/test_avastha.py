import sys
sys.path.insert(0, r"C:\proj\astrodev\api")
from avastha import (baladi, jagradadi, avasthas, is_odd_sign, GRAHAS, NODES,
                     BALADI_ORDER, BALADI_BAND, BALADI_GRADE, BALADI_FRACTION,
                     BALADI_RANK, BALADI_RANK_INTERPOLATED_PAIR,
                     BALADI_RANK_UNVERIFIED, BALADI_VRIDDHA_VS_BALA_INTERPOLATED,
                     JAGRADADI_GRADE, JAGRADADI_FRACTION,
                     DEEPTADI_STATES, DEEPTADI_NINTH_STATE,
                     DEEPTADI_NINTH_STATE_SOURCE, DEEPTADI_DUKKHITA_CAUSE_UNSTATED,
                     DEEPTADI_VIKALA_SPELLING_AMBIGUOUS, DEEPTADI_VIKALA_SPELLINGS,
                     LAJJITADI_STATES, SAYANADI_STATES,
                     SAYANADI_MAIN_STATES_BUILDABLE, SAYANADI_SUBSTATE_NEEDS_NAME)
from dignity import EXALTATION, DEBILITATION, RASI_LORD, NATURAL_RELATIONS

S = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya",
     "Tula","Vrishchika","Dhanus","Makara","Kumbha","Meena"]
ODD  = 0    # Mesha  — the 1st sign, therefore ODD
EVEN = 1    # Vrishabha — the 2nd sign, therefore EVEN

fails = []

# Every check declares what it is anchored to, so the PASS count cannot be read
# as N independent doctrinal confirmations:
#   BOOK     — asserts a statement made in BPHS or in Santhanam's notes/errata,
#              reached independently of this codebase's tables.
#   INTERNAL — consistency of avastha.py against dignity.py's tables, or
#              against itself. Real regression value, ZERO doctrinal value:
#              if dignity.py's table were wrong these would still pass.
#   FLAG     — asserts that a known gap is declared rather than filled in.
counts = {"BOOK": [0, 0], "INTERNAL": [0, 0], "FLAG": [0, 0]}

def check(label, cond, detail="", anchor="BOOK"):
    counts[anchor][0] += 1
    if not cond:
        fails.append(label)
        counts[anchor][1] += 1
    print(f"  {'PASS' if cond else '**FAIL**'} [{anchor[:4]}] "
          f"{label}{('  '+detail) if detail else ''}")

def st(sign, deg):
    return baladi(sign*30 + deg)["state"]

print("Sign parity — v.3 counts signs ORDINALLY from Mesha (1st = odd):")
for s in (0,2,4,6,8,10):
    check(f"{S[s]} is an ODD sign", is_odd_sign(s))
for s in (1,3,5,7,9,11):
    check(f"{S[s]} is an EVEN sign", not is_odd_sign(s))

print("\nch.45 v.3 — five states, 6deg each, ascending order in ODD signs")
print("(Santhanam's note tabulates exactly these bands):")
book_odd = [("Baalavastha","bala",0,6), ("Kumaravastha","kumara",6,12),
            ("Yuvavastha","yuva",12,18), ("Vridhdhavastha","vriddha",18,24),
            ("Mritavastha","mrita",24,30)]
for name, key, lo, hi in book_odd:
    mid = (lo+hi)/2
    check(f"odd sign {lo}-{hi}deg -> {name}", st(ODD, mid)==key, f"got {st(ODD,mid)}")
    check(f"  band lower bound {lo}deg inclusive", st(ODD, lo)==key, f"got {st(ODD,lo)}")
    check(f"  band upper bound {hi}deg exclusive", st(ODD, hi-1e-9)==key, f"got {st(ODD,hi-1e-9)}")

print("\nv.3 — 'This arrangement is reverse in the case of even signs':")
for name, key, lo, hi in book_odd:
    mid = (lo+hi)/2
    mirror = 30 - mid
    check(f"even sign {30-hi}-{30-lo}deg -> {name}", st(EVEN, mirror)==key,
          f"got {st(EVEN, mirror)}")
check("even sign order is exactly the odd order reversed",
      [st(EVEN, b*6+3) for b in range(5)] == list(reversed(BALADI_ORDER)),
      str([st(EVEN, b*6+3) for b in range(5)]))
check("reversal holds in every one of the 12 signs",
      all(st(s, d) == (st(0, d) if is_odd_sign(s) else st(1, d))
          for s in range(12) for d in (1,7,13,19,25)), anchor="INTERNAL")

print("\nCROSS-CHECK vs ch.11 vv.14-16 NOTES (Santhanam, reached independently):")
# note (c): "if the lord of a house is in 6 to 18 of an odd sign, he will be in
#            one of the two Avasthas required [Yuva or Kumara]. Alternatively,
#            it should be between 12 and 24 of an even sign."
check("note(c) ODD 6-18deg is Kumara-or-Yuva",
      all(st(ODD, d) in ("kumara","yuva") for d in (6,9,12,15,17.9)))
check("note(c) ODD outside 6-18 is NOT Kumara-or-Yuva",
      all(st(ODD, d) not in ("kumara","yuva") for d in (0,3,5.9,18,21,25,29)))
check("note(c) EVEN 12-24deg is Kumara-or-Yuva",
      all(st(EVEN, d) in ("kumara","yuva") for d in (12,15,18,21,23.9)))
check("note(c) EVEN outside 12-24 is NOT Kumara-or-Yuva",
      all(st(EVEN, d) not in ("kumara","yuva") for d in (0,5,11.9,24,27,29)))
# note (e): "[between 1]8-24 of an odd sign or between 6 and 12 of an even sign"
check("note(e) Vriddha = ODD 18-24deg",
      all(st(ODD, d)=="vriddha" for d in (18,20,23.9)))
check("note(e) Vriddha = EVEN 6-12deg",
      all(st(EVEN, d)=="vriddha" for d in (6,9,11.9)))
check("note(e) Vriddha occurs NOWHERE ELSE in an odd sign",
      not any(st(ODD,d)=="vriddha" for d in (0,5,10,15,17.9,24,29)))
check("note(e) Vriddha occurs NOWHERE ELSE in an even sign",
      not any(st(EVEN,d)=="vriddha" for d in (0,3,5.9,12,20,29)))
# note (f): "the fir[st 6 o]f an even sign or in the last 6 of an odd sign"
check("note(f) Mrita = first 6deg of an EVEN sign",
      all(st(EVEN, d)=="mrita" for d in (0,2,5.9)))
check("note(f) Mrita = last 6deg of an ODD sign",
      all(st(ODD, d)=="mrita" for d in (24,27,29.99)))
check("note(f) 6deg of an even sign is NO LONGER Mrita", st(EVEN,6)!="mrita")
check("note(f) 23.9deg of an odd sign is NOT YET Mrita", st(ODD,23.9)!="mrita")

print("\nch.45 v.4 — 'One fourth, half, full, negligible and ni[l] ... due to a")
print("planet in infant, youthful, adolescent, old and dead states':")
book_grade = [("bala","one_fourth",0.25), ("kumara","half",0.5),
              ("yuva","full",1.0), ("vriddha","negligible",None),
              ("mrita","nil",0.0)]
for key, grade, frac in book_grade:
    check(f"{key} graded '{grade}'", BALADI_GRADE[key]==grade, BALADI_GRADE[key])
    check(f"{key} fraction {frac}", BALADI_FRACTION[key]==frac, str(BALADI_FRACTION[key]))
check("'negligible' is NOT given an invented number (v.4 gives only a word)",
      BALADI_FRACTION["vriddha"] is None, anchor="FLAG")
check("'nil' IS a number, and it is zero", BALADI_FRACTION["mrita"]==0.0)
check("grade rides along with the state",
      baladi(ODD*30+15)["grade"]=="full" and baladi(ODD*30+15)["fraction"]==1.0,
      anchor="INTERNAL")

print("\nv.4 RANK — four comparisons are forced by the text, one is NOT:")
# Forced by arithmetic on the words v.4 actually uses.
check("one fourth < half < full  =>  bala < kumara < yuva",
      BALADI_RANK["bala"] < BALADI_RANK["kumara"] < BALADI_RANK["yuva"])
check("negligible > nil  =>  vriddha > mrita",
      BALADI_RANK["vriddha"] > BALADI_RANK["mrita"])
check("nil is the floor: mrita is rank 0", min(BALADI_RANK.values())==BALADI_RANK["mrita"])
check("full is the ceiling: yuva is rank 4", max(BALADI_RANK.values())==BALADI_RANK["yuva"])
# ch.11 vv.14-16 MULA names the bhava-destroying states and Baala is NOT among
# them: "or is in one of thc threc Avasthas, viz, Vriddhavastha, Mritavastha
# and Suptava-sth8." ch.11 note (c) names Yuva and Kumara as the GOOD ones.
check("ch.11 mula's two bad Baladi states outrank nothing above bala",
      BALADI_RANK["vriddha"] < BALADI_RANK["kumara"]
      and BALADI_RANK["mrita"] < BALADI_RANK["kumara"])
check("ch.11 note(c): the two GOOD states are the top two ranks",
      sorted(BALADI_RANK, key=BALADI_RANK.get)[-2:] == ["kumara","yuva"],
      str(sorted(BALADI_RANK, key=BALADI_RANK.get)))
# THE UNDECIDED ONE. This must be flagged, not silently asserted.
check("vriddha-vs-bala is declared an INTERPOLATION, not doctrine",
      BALADI_RANK_INTERPOLATED_PAIR == ("vriddha","bala"), anchor="FLAG")
check("the flag text names ch.11 as the basis and admits the other reading",
      "ch.11" in BALADI_VRIDDHA_VS_BALA_INTERPOLATED
      and "not refuted" in BALADI_VRIDDHA_VS_BALA_INTERPOLATED, anchor="FLAG")
check("baladi() marks vriddha rank_verified=False",
      baladi(ODD*30+20)["rank_verified"] is False, anchor="FLAG")
check("baladi() marks bala rank_verified=False",
      baladi(ODD*30+3)["rank_verified"] is False, anchor="FLAG")
check("baladi() marks the three FORCED states rank_verified=True",
      all(baladi(ODD*30+d)["rank_verified"] is True for d in (9,15,27)),
      anchor="FLAG")
check("exactly the two interpolated states are unverified",
      BALADI_RANK_UNVERIFIED == {"vriddha","bala"}, anchor="FLAG")

print("\nch.45 v.5 — own sign or exaltation -> Jagrat (awakening):")
print("  (the sweeps below are INTERNAL: they read dignity.py's own tables)")
for g,(s,d) in EXALTATION.items():
    r = jagradadi(g, s*30+d)
    check(f"{g} at its exact uccha -> jagrat", r["state"]=="jagrat", r["state"],
          anchor="INTERNAL")
for g in EXALTATION:
    own = [s for s in range(12) if RASI_LORD[s]==g]
    for s in own:
        r = jagradadi(g, s*30+25)
        check(f"{g} in own sign {S[s]} -> jagrat", r["state"]=="jagrat", r["state"],
              anchor="INTERNAL")
# ch.11 note (d): "P[r]abuddhavastha is another name for Jagradavastha ... This
#                  applies to a planet in own [s]ign or in [e]xaltation sign."
check("note(d) cross-check: Sun in Simha -> jagrat",
      jagradadi("sun", 4*30+15)["state"]=="jagrat")
check("note(d) cross-check: Sun in Mesha (exaltation) -> jagrat",
      jagradadi("sun", 0*30+10)["state"]=="jagrat")

print("\nv.5 — friend's or neutral's sign -> Swapna (dreaming):")
for g in EXALTATION:
    for s in range(12):
        lord = RASI_LORD[s]
        if lord == g or s == EXALTATION[g][0] or s == DEBILITATION[g][0]:
            continue
        rel = NATURAL_RELATIONS[g][lord]
        if rel in ("friend","neutral"):
            check(f"{g} in {S[s]} ({rel} of {lord}) -> swapna",
                  jagradadi(g, s*30+15)["state"]=="swapna",
                  jagradadi(g, s*30+15)["state"], anchor="INTERNAL")

print("\nv.5 — enemy's sign or debilitation -> Supta (sleeping):")
for g,(s,d) in DEBILITATION.items():
    r = jagradadi(g, s*30+d)
    check(f"{g} at its exact nica -> supta", r["state"]=="supta", r["state"],
          anchor="INTERNAL")
for g in EXALTATION:
    for s in range(12):
        lord = RASI_LORD[s]
        if lord == g or s == EXALTATION[g][0] or s == DEBILITATION[g][0]:
            continue
        if NATURAL_RELATIONS[g][lord] == "enemy":
            check(f"{g} in {S[s]} (enemy {lord}) -> supta",
                  jagradadi(g, s*30+15)["state"]=="supta",
                  jagradadi(g, s*30+15)["state"], anchor="INTERNAL")
# ch.11 note (g): "a planet in Suptavastha neutralises the [effect] of [the
#                  bhava] ... due to a debi[l]itated planet or the one in an
#                  inimical camp."
check("note(g) cross-check: Sun in Tula (debilitated) -> supta",
      jagradadi("sun", 6*30+10)["state"]=="supta")

print("\nv.5 covers all 12 signs for all 7 grahas with no gap:")
for g in EXALTATION:
    got = {jagradadi(g, s*30+15)["state"] for s in range(12)}
    check(f"{g}: every sign resolves to one of the three states",
          got <= {"jagrat","swapna","supta"} and got, str(sorted(got)),
          anchor="INTERNAL")

print("\nMoolatrikona arcs are not a v.5 category — they resolve via own sign:")
for g,(s,lo,hi) in [(g, __import__('dignity').MOOLATRIKONA[g]) for g in EXALTATION]:
    if RASI_LORD[s] == g:
        mid = (lo+hi)/2
        check(f"{g} in its MT arc ({S[s]} {mid}deg) -> jagrat, its own rasi",
              jagradadi(g, s*30+mid)["state"]=="jagrat",
              jagradadi(g, s*30+mid)["state"], anchor="INTERNAL")
check("Mercury Kanya 17deg (MT arc inside own sign) -> jagrat",
      jagradadi("mercury", 5*30+17)["state"]=="jagrat", anchor="INTERNAL")

print("\nch.45 v.6 — 'full, medium or nil' for Jagrat, Swapna, Supta:")
for key, grade, frac in (("jagrat","full",1.0), ("swapna","medium",None),
                         ("supta","nil",0.0)):
    check(f"{key} graded '{grade}'", JAGRADADI_GRADE[key]==grade, JAGRADADI_GRADE[key])
    check(f"{key} fraction {frac}", JAGRADADI_FRACTION[key]==frac,
          str(JAGRADADI_FRACTION[key]))
check("'medium' is NOT assumed to be 0.5 (v.6 gives only a word)",
      JAGRADADI_FRACTION["swapna"] is None, anchor="FLAG")
check("v.6 DOES order its three grades, so jagradadi rank_verified=True",
      jagradadi("sun", 4*30+15)["rank_verified"] is True, anchor="FLAG")

print("\nThe nodes — ch.3 v.50 gives them no dignity, so no Jagradadi:")
for g in ("rahu","ketu"):
    check(f"{g} jagradadi -> None", jagradadi(g, 123.4) is None)
    check(f"{g} baladi still computes (v.3 is degree-only)",
          baladi(123.4)["state"] in BALADI_ORDER)
    a = avasthas(g, 123.4)
    check(f"{g} avasthas(): baladi present, jagradadi None",
          a["baladi"] is not None and a["jagradadi"] is None)

print("\nNone means RAHU/KETU and nothing else — a bad key must RAISE:")
check("GRAHAS is exactly the nine of ch.3", GRAHAS == set(EXALTATION) | {"rahu","ketu"},
      str(sorted(GRAHAS)), anchor="INTERNAL")
check("NODES is exactly rahu+ketu", NODES == {"rahu","ketu"}, anchor="INTERNAL")
for bad in ("Moon", "moon ", "", "lagna", "uranus", "Rahu"):
    try:
        jagradadi(bad, 100.0)
        ok, why = False, "returned instead of raising"
    except ValueError:
        ok, why = True, ""
    except Exception as e:                       # noqa: BLE001
        ok, why = False, f"raised {type(e).__name__}, wanted ValueError"
    check(f"jagradadi({bad!r}) raises ValueError", ok, why, anchor="INTERNAL")
try:
    avasthas("Moon", 100.0)
    ok = False
except ValueError:
    ok = True
check("avasthas() propagates the same guard", ok, anchor="INTERNAL")

print("\nWorked walk-through (v.3 + v.5 together on one position):")
# Sun at Karka 20deg. Karka is the 4th sign -> EVEN, so v.3 reverses:
# 18-24deg of an even sign is the 2nd band from the far end -> Kumara.
# Karka's lord is the Moon, a friend of the Sun by ch.3 v.55 -> Swapna.
a = avasthas("sun", 3*30+20)
check("Sun Karka 20deg: Karka is an EVEN sign", a["baladi"]["sign_parity"]=="even")
check("Sun Karka 20deg -> Kumara (reversed band)", a["baladi"]["state"]=="kumara",
      a["baladi"]["state"])
check("Sun Karka 20deg -> grade 'half'", a["baladi"]["grade"]=="half")
check("Sun Karka 20deg -> Swapna (Moon is a friend)",
      a["jagradadi"]["state"]=="swapna", a["jagradadi"]["state"], anchor="INTERNAL")
check("Sun Karka 20deg -> grade 'medium'", a["jagradadi"]["grade"]=="medium")
check("the two gradings are NOT combined into one score",
      "fraction" not in a and "score" not in a, anchor="INTERNAL")

print("\nBookkeeping — bands tile the sign exactly, no gaps or overlaps:")
check("five bands of 6deg span exactly 30deg", len(BALADI_ORDER)*BALADI_BAND==30.0,
      anchor="INTERNAL")
check("every 0.1deg step in every sign yields a valid state",
      all(baladi(s*30 + d/10.0)["state"] in BALADI_ORDER
          for s in range(12) for d in range(300)), anchor="INTERNAL")
check("longitude wraps at 360", baladi(370.0)["state"]==baladi(10.0)["state"],
      anchor="INTERNAL")
check("negative longitude wraps", baladi(-350.0)["state"]==baladi(10.0)["state"],
      anchor="INTERNAL")

print("\nDEEPTADI — v.7 says NINE; the ninth is in the ERRATA, not lost:")
# Vol I errata p.483 pairs "450 l0 Vikala" (For) with "Dukkhita, Vikala" (Read).
# Vol I table of contents: "Deepta and other 8 ptates" = nine in all.
check("v.7's declared count of NINE is met", len(DEEPTADI_STATES)==9,
      f"{len(DEEPTADI_STATES)} states")
check("the ninth state is Dukkhita", DEEPTADI_NINTH_STATE=="dukkhita",
      DEEPTADI_NINTH_STATE)
check("Dukkhita is in the list", "dukkhita" in DEEPTADI_STATES)
check("errata order: ... Deena, DUKKHITA, Vikala, Khala, Kopa",
      list(DEEPTADI_STATES)[4:] == ["deena","dukkhita","vikala","khala","kopa"],
      str(list(DEEPTADI_STATES)))
check("the printed v.7 eight are all still present and correctly caused",
      [DEEPTADI_STATES[k] for k in ("deepta","swastha","pramudita","santa",
                                    "deena","vikala","khala","kopa")]
      == ["exaltation sign","own sign","thick friend's sign","friendly sign",
          "neutral's sign","in the company of a malefic","enemy's sign",
          "eclipsed by (combust with) the Sun"])
check("the recovery cites the errata, not a guess",
      "errata" in DEEPTADI_NINTH_STATE_SOURCE and "450" in DEEPTADI_NINTH_STATE_SOURCE,
      anchor="FLAG")
check("Dukkhita's CAUSE is None — vv.8-10 give causes for eight only",
      DEEPTADI_STATES["dukkhita"] is None, anchor="FLAG")
check("exactly one state has an unstated cause",
      sum(v is None for v in DEEPTADI_STATES.values())==1, anchor="FLAG")
check("the missing cause is flagged UNAVAILABLE, not filled in",
      "UNAVAILABLE" in DEEPTADI_DUKKHITA_CAUSE_UNSTATED, anchor="FLAG")
check("Vikala/Vikata spelling conflict is flagged AMBIGUOUS",
      "AMBIGUOUS" in DEEPTADI_VIKALA_SPELLING_AMBIGUOUS, anchor="FLAG")
check("both spellings are recorded, with the chosen one named",
      DEEPTADI_VIKALA_SPELLINGS == {"chosen": "vikala",
                                    "v7_naming_sloka": "Vikala",
                                    "vv8_10_cause_slokas": "Vikata"},
      anchor="FLAG")
check("the chosen spelling is the key actually used",
      DEEPTADI_VIKALA_SPELLINGS["chosen"] in DEEPTADI_STATES, anchor="INTERNAL")

print("\nSURVEY of the rest of ch.45 (flagged, deliberately NOT implemented):")
check("Lajjitadi: six states recorded (vv.11-18)", len(LAJJITADI_STATES)==6)
check("Sayanadi: twelve states recorded (vv.30-37)", len(SAYANADI_STATES)==12)
check("Sayanadi MAIN twelve are declared BUILDABLE from chart+birth data",
      "buildable" in SAYANADI_MAIN_STATES_BUILDABLE.lower()
      and "ghaṭīs" in SAYANADI_MAIN_STATES_BUILDABLE, anchor="FLAG")
check("only the SUB-state is declared to need the personal NAME",
      "personal name" in SAYANADI_SUBSTATE_NEEDS_NAME
      and "personal name" not in SAYANADI_MAIN_STATES_BUILDABLE, anchor="FLAG")
print(f"  Deeptadi: {list(DEEPTADI_STATES)}")
print(f"  Lajjitadi: {sorted(LAJJITADI_STATES)}")

print("\nCOVERAGE BY ANCHOR (a PASS count is not a count of doctrinal proofs):")
for k in ("BOOK","INTERNAL","FLAG"):
    ran, bad = counts[k]
    print(f"  {k:9s} {ran:4d} checks, {bad} failed")
print("  BOOK     = asserts something BPHS/Santhanam/the errata actually says.")
print("  INTERNAL = avastha.py vs dignity.py's tables, or vs itself. Regression")
print("             value only — these would pass even if the tables were wrong.")
print("  FLAG     = asserts a known gap is DECLARED rather than filled in.")
print("  BPHS gives no worked example for Baladi or Jagradadi, so no numeric")
print("  fixture from the book exists for either; the book anchors are the band")
print("  tables and the ch.11 arcs, cross-checked from the opposite direction.")

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
