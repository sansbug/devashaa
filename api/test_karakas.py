import sys
sys.path.insert(0, r"C:\proj\astrodev\api")
from karakas import (chara_karakas, karakamsa, karaka_value_arcsec, dms,
                     sthira_karaka_houses,
                     KARAKA_ORDER_8, KARAKA_ORDER_7,
                     SEVEN_GRAHAS, EIGHT_GRAHAS,
                     STHIRA_KARAKAS, STHIRA_KARAKA_HOUSES,
                     ARCSEC_PER_SIGN,
                     _TIE_FALLBACK, TIE_FALLBACK_AMBIGUOUS,
                     TIE_FALLBACK_INCOMPLETE,
                     ANTHYA_MADHYA_UPAKHETA_UNRECOVERABLE,
                     VOL2_CH46_DEGREES_UNRECOVERABLE,
                     VENUS_HOUSE_RECONSTRUCTED)
from vargas import d9_navamsa
import karakas as _karakas
karakas_doc = _karakas.__doc__

S = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya",
     "Tula","Vrishchika","Dhanus","Makara","Kumbha","Meena"]
fails = []
def check(label, cond, detail=""):
    if not cond: fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  '+detail) if detail else ''}")

def arc(d, m, s): return d*3600 + m*60 + s

print("BPHS ch.32 vv.1-2 — the eligible set (Ketu is named NOWHERE in ch.32):")
check("seven grahas = Sun..Saturn",
      SEVEN_GRAHAS == ("sun","moon","mars","mercury","jupiter","venus","saturn"))
check("eight grahas = the seven + Rahu ONLY", EIGHT_GRAHAS == SEVEN_GRAHAS + ("rahu",))
check("ketu is not eligible in either scheme", "ketu" not in EIGHT_GRAHAS)

print("\nvv.3-8 — the ranked quantity is the arc WITHIN the sign, sign discarded:")
check("Jupiter at Karka 26d07'13\" scores 26d07'13\"",
      karaka_value_arcsec("jupiter", 3*30 + dms(26,7,13)) == arc(26,7,13))
check("same degrees in a different sign score identically",
      karaka_value_arcsec("jupiter", 3*30 + dms(26,7,13)) ==
      karaka_value_arcsec("jupiter", 9*30 + dms(26,7,13)))

print("\nv.8 — 'In the case of Rahu, deduct his longitude in that sign from 30':")
# Cross-verified against the book itself: ch.29's standard nativity (pdf 293)
# lists Rahu at 97d37'06" = KARKA 7d37'06" -- 277d37'06" = Makara is KETU's
# entry -- and the ch.32 karaka table (pdf 318) lists Rahu at 22d22'54".
check("ch.29 Rahu Karka 7d37'06\" -> ch.32 table's 22d22'54\"",
      karaka_value_arcsec("rahu", 3*30 + dms(7,37,6)) == arc(22,22,54),
      "got %d arcsec" % karaka_value_arcsec("rahu", 3*30 + dms(7,37,6)))
# Vol II ch.46 (pdf 68) spells out Rahu's arc as "16'-4',-26"." and says it is
# taken "after deducting from" ... "30". The RESULT is our arithmetic, not a
# quotation: the numerals after "30 would be" are jumbled in the scan.
check("Vol II ch.46: Rahu 16d04'26\", deducted from 30, gives 13d55'34\"",
      karaka_value_arcsec("rahu", 2*30 + dms(16,4,26)) == arc(13,55,34),
      "got %d arcsec" % karaka_value_arcsec("rahu", 2*30 + dms(16,4,26)))
check("the inversion applies to Rahu ONLY, never to a normal graha",
      karaka_value_arcsec("saturn", 9*30 + dms(7,37,6)) == arc(7,37,6))
check("Rahu at 0d00'00\" of a sign scores a full 30d",
      karaka_value_arcsec("rahu", 5*30.0) == ARCSEC_PER_SIGN)

# ---------------------------------------------------------------------------
# BOOK FIXTURE 1 — Vol I ch.32, pdf p.318. The standard nativity of ch.29,
# worked as EIGHT karakas with arcsecond longitudes.
# ---------------------------------------------------------------------------
print("\nBOOK FIXTURE 1 — Vol I ch.32 pdf p.318, the standard nativity (ch.29):")
# ch.29 longitudes, pdf 293. The scan's columns are interleaved but the DEGREE
# column reads, against the label order Sun/Moon/Mars/Mercury/Jupiter/Venus/
# Saturn/Bahu[Rahu]/Ketu:  37, 27, 96, 14, 116, 27, 63(9), 97, 277 -- i.e. these
# are absolute longitudes, so the signs fall out of them directly.
# Corroborated by the prose: "its lord Mars is 9 signs away from the ascendant
# and is iri Canccr" (Mars 96 = Karka), and Jupiter 116 = Karka 26d07'13" is
# both exalted and the 9th from the stated Scorpio lagna.
# NOTE Rahu 97 = KARKA and Ketu 277 = MAKARA -- they are 180 degrees apart and
# share the arc 7d37'06", which is what makes them easy to transpose. An earlier
# version of this fixture had them swapped, and had Saturn in Vrishabha instead
# of Mithuna.
nativity = {
    "sun":     1*30 + dms(7,12,18),    # 37d12'18"  Vrishabha
    "moon":    0*30 + dms(27,35,46),   # 27d35'46"  Mesha
    "mars":    3*30 + dms(6,18,46),    # 96d18'46"  Karka
    "mercury": 0*30 + dms(14,54,13),   # 14d54'13"  Mesha
    "jupiter": 3*30 + dms(26,7,13),    # 116d07'13" Karka (exalted, 9th)
    "venus":   0*30 + dms(27,17,50),   # 27d17'50"  Mesha
    "saturn":  2*30 + dms(3,9,41),     # 63d09'41"  Mithuna
    "rahu":    3*30 + dms(7,37,6),     # 97d37'06"  Karka -> reckoned 22d22'54"
    "ketu":    9*30 + dms(7,37,6),     # 277d37'06" Makara; NOT a karaka
}
# Guard the transposition directly, in absolute longitude, so the fixture cannot
# drift back: these are the ch.29 table's own numbers.
check("ch.29 table: Saturn 63d09'41\" (Mithuna), not 33d (Vrishabha)",
      abs(nativity["saturn"] - (63 + 9/60 + 41/3600)) < 1e-9)
check("ch.29 table: Rahu 97d37'06\" (Karka), Ketu 277d37'06\" (Makara)",
      abs(nativity["rahu"] - (97 + 37/60 + 6/3600)) < 1e-9 and
      abs(nativity["ketu"] - (277 + 37/60 + 6/3600)) < 1e-9)
check("Rahu and Ketu are exactly 180 degrees apart",
      abs((nativity["ketu"] - nativity["rahu"]) - 180.0) < 1e-9)
# The book's table, verbatim: karaka / planet / longitude.
FIXTURE1 = [
    ("atma",    "moon",    (27,35,46)),
    ("amatya",  "venus",   (27,17,50)),
    ("bhratru", "jupiter", (26, 7,13)),
    ("matru",   "rahu",    (22,22,54)),
    ("pitru",   "mercury", (14,54,13)),
    ("putra",   "sun",     ( 7,12,18)),
    ("gnati",   "mars",    ( 6,18,46)),
    ("stree",   "saturn",  ( 3, 9,41)),
]
r = chara_karakas(nativity, grahas="eight", roles=8)
for role, graha, (d, m, s) in FIXTURE1:
    check(f"{role:8s} = {graha:8s} @ {d:2d}d{m:02d}'{s:02d}\"",
          r["assignment"][role] == [graha],
          "got %s" % r["assignment"][role])
for (role, graha, (d, m, s)), row in zip(FIXTURE1, r["ranking"]):
    check(f"  ranking arcsec for {graha}", row["arcsec"] == arc(d, m, s),
          "got %dd%02d'%02d\"" % (row["degrees"], row["minutes"], row["seconds"]))
check("ranking is strictly descending, 8 planets",
      [x["arcsec"] for x in r["ranking"]] ==
      sorted([x["arcsec"] for x in r["ranking"]], reverse=True) and
      len(r["ranking"]) == 8)
check("Ketu excluded even though he is in the chart",
      "ketu" not in r["karaka_of"] and
      all(x["graha"] != "ketu" for x in r["ranking"]))
check("no ties -> nothing shared, nothing unfilled",
      r["shared"] == {} and r["unfilled"] == [])
check("Atmakaraka is the Moon", r["atmakaraka"] == "moon", r["atmakaraka"])

# ---------------------------------------------------------------------------
# FIXTURE 2 — Vol II ch.46. NOT A BOOK CHART: the arcs below are CONSTRUCTED
# BY US from the book's stated RANK ORDER, because the chart's degree columns
# are destroyed in the scan (see VOL2_CH46_DEGREES_UNRECOVERABLE).
#
# Only TWO things here are evidence, and only those two are asserted below:
#   (a) Rahu's 16d04'26" -> 13d55'34", which is real data (pdf 68); and
#   (b) the role sequence, which the prose spells out in words (pdf 69).
# The seven round numbers (26d, 20d, 13d, 9d, 5d, 3d, 1d) are invented spacers
# chosen to realise that sequence. Asserting that they sort into the sequence
# they were built from would test nothing but sorted(); so we do not.
# ---------------------------------------------------------------------------
print("\nFIXTURE 2 — Vol II ch.46, role sequence + Rahu (arcs CONSTRUCTED):")
# "the Sun here has traversed the maximum number of degrees, will be Atmakarka
#  and Venus who comes next ... After that comes Rahu, Karaka for brother,
#  Jupiter Karaka for mother, Saturn Karaka for father, Mercury Karaka for son,
#  Moon Karaka for gnati and Mars Karaka for wife."
# This IS book evidence: the role sequence is written out in prose, and it is an
# independent witness to Vol I vv.13-17 -- in particular to Pitru at rank 5 and
# Putra at rank 6, the point the popular Jaimini seven disagrees on.
FIXTURE2_ROLES = ["atma","amatya","bhratru","matru","pitru","putra","gnati","stree"]
check("Vol II role sequence == KARAKA_ORDER_8 from Vol I vv.13-17",
      list(KARAKA_ORDER_8) == FIXTURE2_ROLES, str(KARAKA_ORDER_8))
check("Vol II independently puts Pitru 5th and Putra 6th",
      FIXTURE2_ROLES[4] == "pitru" and FIXTURE2_ROLES[5] == "putra")
# The constructed chart below exists ONLY to exercise Rahu's placement in the
# ranking; its other seven arcs are ours, so nothing about them is asserted.
vol2 = {"sun": 9*30 + dms(26,0,0), "venus": 10*30 + dms(20,0,0),
        "rahu": 2*30 + dms(16,4,26),
        "jupiter": 10*30 + dms(13,0,0), "saturn": 7*30 + dms(9,0,0),
        "mercury": 10*30 + dms(5,0,0), "moon": 2*30 + dms(3,0,0),
        "mars": 1*30 + dms(1,0,0), "ketu": 8*30 + dms(16,4,26)}
r2 = chara_karakas(vol2, grahas="eight", roles=8)
check("Vol II: Rahu's ranked arc is the inverted 13d55'34\", not 16d04'26\"",
      r2["ranking"][2]["graha"] == "rahu" and
      r2["ranking"][2]["arcsec"] == arc(13,55,34),
      str(r2["ranking"][2]))
check("Vol II: Ketu is in the chart but absent from the 8-karaka table",
      "ketu" not in r2["karaka_of"])

# ---------------------------------------------------------------------------
# BOOK FIXTURE 3 — Mrs Indira Gandhi. Real book chart AND a real book verdict,
# printed in different chapters, which is what makes it the strongest fixture
# in either volume.
#
#   CHART   Vol I ch.24, note to sloka 50 (pdf 201): "born on lgth November
#           l9l7 (Monday) at 2317 hrs IST at Allahabad, 81854 25N28", with arcs
#           Jup(R) 15-0, Ketu 15-34, Asc 2E'05 [28-05], 2r-48 [21-48],
#           Mars t6-23 [16-23], Moon 5-3 5 [5-35], en 20-57 [Ven 20-57],
#           Rahu I 0-34 [10-34], Merc l3-ll [13-11], Sun4-04 [4-04].
#   VERDICT Vol I ch.39, note to slokas 6-7 (pdf 388-389): "The Atma Karaka is
#           Saturn (21" 50') while Putra Karaka is Mercury (13'll')."
#
# TWO CAVEATS, both stated rather than smoothed over:
#  1. The label on the 21-48 box is lost in the OCR. It is identified as Saturn
#     because ch.39 names Saturn the Atmakaraka and 21-48 is the largest arc.
#  2. ch.39 prints Saturn as 21d50' where the ch.24 chart prints 21-48. We use
#     the CHART value; the 2-arcminute discrepancy is the book's own and does
#     not affect the ranking (the next arc down is Venus at 20-57).
#
# Only the arcs are used, because vv.3-8 discard the sign -- and the scan's box
# layout does not reliably give signs anyway. That is asserted, not assumed.
# ---------------------------------------------------------------------------
print("\nBOOK FIXTURE 3 — Mrs Gandhi (chart ch.24 pdf 201, verdict ch.39 pdf 388):")
gandhi = {
    "saturn":  dms(21,48), "venus":   dms(20,57), "rahu":    dms(10,34),
    "mars":    dms(16,23), "jupiter": dms(15, 0), "mercury": dms(13,11),
    "moon":    dms( 5,35), "sun":     dms( 4, 4), "ketu":    dms(15,34),
}
rg = chara_karakas(gandhi, grahas="eight", roles=8)
check("ch.39: 'The Atma Karaka is Saturn' (chart 21-48; ch.39 prints 21d50')",
      rg["assignment"]["atma"] == ["saturn"], str(rg["assignment"]["atma"]))
check("ch.39: 'while Putra Karaka is Mercury' (13-11, matching '13'll'')",
      rg["assignment"]["putra"] == ["mercury"], str(rg["assignment"]["putra"]))
check("Mercury's arc reproduces the note's 13d11' to the arcminute",
      rg["ranking"][5]["degrees"] == 13 and rg["ranking"][5]["minutes"] == 11,
      str(rg["ranking"][5]))
# DOUBLE PROOF. Putra is rank 6, so Mercury lands there only if BOTH of these
# hold. Break either one and the book's own verdict fails.
check("proof (a): Rahu's inverted arc puts him 3rd, displacing Mercury to 6th",
      rg["ranking"][2]["graha"] == "rahu" and
      rg["ranking"][2]["arcsec"] == arc(19,26,0), str(rg["ranking"][2]))
check("proof (b): Pitru occupies rank 5, so Putra is rank 6 (= Mercury)",
      rg["assignment"]["pitru"] == ["jupiter"] and
      KARAKA_ORDER_8.index("putra") == 5, str(rg["assignment"]["pitru"]))
# Counterfactual 1: without the Rahu inversion, Putra Karaka becomes Rahu.
cf_no_inversion = sorted(gandhi, key=lambda g: -round((gandhi[g] % 30)*3600))
cf_no_inversion = [g for g in cf_no_inversion if g != "ketu"]
check("counterfactual: drop the Rahu inversion and Putra becomes Rahu, "
      "contradicting the book",
      cf_no_inversion[5] == "rahu", str(cf_no_inversion))
# Counterfactual 2: on the popular Jaimini order (Pitru dropped), Putra sits at
# rank 5, which in this chart is JUPITER, not Mercury -- so this chart also
# refutes that ordering for BPHS.
POPULAR_JAIMINI_7 = ["atma","amatya","bhratru","matru","putra","gnati","dara"]
check("counterfactual: the popular seven put Putra at rank 5 (= Jupiter), "
      "which the book's 'Putra Karaka is Mercury' rules out",
      POPULAR_JAIMINI_7.index("putra") == 4 and
      rg["ranking"][4]["graha"] == "jupiter", str(rg["ranking"][4]))
# The ranking must not depend on the sign, which is why arcs alone suffice.
shifted = {g: (i * 30) + v for i, (g, v) in enumerate(gandhi.items())}
check("assignment is sign-independent (vv.3-8 discard the Rasi)",
      chara_karakas(shifted, grahas="eight", roles=8)["assignment"] ==
      rg["assignment"])

print("\nvv.13-17 — the SEVEN-role reading merges Matru with Putra (NOT the")
print("popular Jaimini seven, which instead drops Pitru):")
check("7-role order keeps pitru", "pitru" in KARAKA_ORDER_7)
check("7-role order has a merged matru_putra", "matru_putra" in KARAKA_ORDER_7)
check("7-role order drops the standalone matru and putra",
      "matru" not in KARAKA_ORDER_7 and "putra" not in KARAKA_ORDER_7)
check("7 roles, not 8", len(KARAKA_ORDER_7) == 7 and len(KARAKA_ORDER_8) == 8)
r7 = chara_karakas(nativity, grahas="eight", roles=7)
check("standard nativity, 7 roles: matru_putra = Rahu (4th rank, unchanged)",
      r7["assignment"]["matru_putra"] == ["rahu"], str(r7["assignment"]))
check("standard nativity, 7 roles: pitru shifts up to Mercury",
      r7["assignment"]["pitru"] == ["mercury"])
check("standard nativity, 7 roles: gnati = Sun, stree = Mars",
      r7["assignment"]["gnati"] == ["sun"] and r7["assignment"]["stree"] == ["mars"])
check("with 8 planets and 7 roles the 8th planet (Saturn) gets none",
      "saturn" not in r7["karaka_of"])

print("\nvv.1-2 — the seven-graha school drops Rahu entirely:")
r_seven = chara_karakas(nativity, grahas="seven", roles=8)
check("Rahu absent from the ranking",
      all(x["graha"] != "rahu" for x in r_seven["ranking"]))
check("Matru shifts from Rahu to Mercury when Rahu is dropped",
      r_seven["assignment"]["matru"] == ["mercury"],
      str(r_seven["assignment"]["matru"]))
check("7 planets cannot fill 8 roles -> Dara/Stree karaka unfilled",
      r_seven["unfilled"] == ["stree"], str(r_seven["unfilled"]))
check("the unfilled role falls back to the sthira karaka Venus",
      r_seven["sthira_fallback"]["stree"] == "venus")
r_seven7 = chara_karakas(nativity, grahas="seven", roles=7)
check("7 planets fill 7 roles exactly", r_seven7["unfilled"] == [])

print("\nvv.13-17 — a TIE is not broken: both planets take the SAME karaka and")
print("the sequence runs one short ('there will be a deficit of one karaka'):")
tied = dict(nativity)
tied["saturn"] = 1*30 + dms(6,18,46)     # exactly Mars's arc, to the second
rt = chara_karakas(tied, grahas="eight", roles=8)
check("Mars and Saturn tie to the arcsecond -> both are Gnati karaka",
      sorted(rt["assignment"]["gnati"]) == ["mars","saturn"],
      str(rt["assignment"]["gnati"]))
check("the tie is reported as shared", "gnati" in rt["shared"])
check("Dara/Stree karakatwa falls short, exactly as the book's note says",
      rt["unfilled"] == ["stree"], str(rt["unfilled"]))
check("'The constant indicator Venus should then be considered' (note, p.318)",
      rt["sthira_fallback"]["stree"] == "venus")
check("a 1-arcsecond difference is NOT a tie (v.8 compares to the second)",
      chara_karakas({**nativity, "saturn": 1*30 + dms(6,18,45)},
                    grahas="eight")["shared"] == {})

print("\nA tie at rank 1 leaves NO single Atmakaraka — the module must not pick:")
tie_top = dict(nativity)
tie_top["venus"] = 0*30 + dms(27,35,46)     # exactly the Moon's arc
rtop = chara_karakas(tie_top, grahas="eight", roles=8)
check("Moon and Venus share the atma role",
      sorted(rtop["atmakarakas"]) == ["moon","venus"], str(rtop["atmakarakas"]))
check("the scalar atmakaraka is None, NOT the first in SEVEN_GRAHAS order",
      rtop["atmakaraka"] is None, str(rtop["atmakaraka"]))
kmt = karakamsa(tie_top, navamsa_of=d9_navamsa)
check("karakamsa reports the tie as ambiguous", kmt["ambiguous"] is True)
check("karakamsa refuses to name one Atmakaraka", kmt["atmakaraka"] is None)
check("karakamsa refuses to compute one sign", kmt["karakamsa"] is None)
check("but it returns BOTH candidates with their own karakamsas",
      sorted(c["graha"] for c in kmt["candidates"]) == ["moon","venus"] and
      all(c["karakamsa"] is not None for c in kmt["candidates"]),
      str(kmt["candidates"]))
check("an untied chart still yields a single scalar karakamsa",
      karakamsa(nativity, navamsa_of=d9_navamsa)["ambiguous"] is False)

print("\nch.32 names NO sthira karaka for atma / amatya / gnati — a tie that")
print("leaves those unfilled has no textual fallback, and none is invented:")
check("_TIE_FALLBACK covers exactly the five roles vv.22-24 license",
      sorted(_TIE_FALLBACK) == ["bhratru","matru","pitru","putra","stree"],
      str(sorted(_TIE_FALLBACK)))
for absent in ("atma", "amatya", "gnati"):
    check(f"no sthira fallback is asserted for {absent!r}",
          absent not in _TIE_FALLBACK)
# Collapse the seven into a single tied group so the whole tail goes unfilled.
allsame = {g: 4*30 + dms(11,11,11) for g in SEVEN_GRAHAS}
allsame["rahu"] = 4*30 + dms(18,48,49)   # inverts to the same 11d11'11"
ra = chara_karakas(allsame, grahas="seven", roles=8)
check("all seven tie -> one group -> seven roles unfilled",
      ra["unfilled"] == ["amatya","bhratru","matru","pitru","putra","gnati","stree"],
      str(ra["unfilled"]))
check("amatya and gnati report None, not a guessed graha",
      ra["sthira_fallback"]["amatya"] is None and
      ra["sthira_fallback"]["gnati"] is None, str(ra["sthira_fallback"]))
check("and they are named in sthira_fallback_unavailable",
      ra["sthira_fallback_unavailable"] == ["amatya","gnati"],
      str(ra["sthira_fallback_unavailable"]))
check("the five licensed roles still resolve",
      ra["sthira_fallback"]["bhratru"] == "mars" and
      ra["sthira_fallback"]["matru"] == "moon" and
      ra["sthira_fallback"]["pitru"] == "sun" and
      ra["sthira_fallback"]["putra"] == "jupiter" and
      ra["sthira_fallback"]["stree"] == "venus", str(ra["sthira_fallback"]))
# Not merely that the graha APPEARS in vv.22-24 (which any of the seven would
# satisfy) but that vv.22-24 give it the signification the cara role needs.
ROLE_SIGNIFICATION = {"bhratru": "brothers", "matru": "mother", "pitru": "father",
                      "putra": "sons", "stree": "wife"}
for role, graha in sorted(_TIE_FALLBACK.items()):
    check(f"vv.22-24 give {graha} the signification {role} needs "
          f"({ROLE_SIGNIFICATION[role]})",
          STHIRA_KARAKA_HOUSES[graha][1] == ROLE_SIGNIFICATION[role],
          "%s -> %s" % (graha, STHIRA_KARAKA_HOUSES[graha][1]))
# The merged seven-role slot: both readings exposed, neither chosen.
ra7 = chara_karakas(allsame, grahas="seven", roles=7)
check("the merged matru_putra slot has NO single fallback",
      ra7["sthira_fallback"]["matru_putra"] is None,
      str(ra7["sthira_fallback"]))
check("both of its candidates are reported instead",
      ra7["sthira_fallback_ambiguous"]["matru_putra"] == ("moon","jupiter"),
      str(ra7["sthira_fallback_ambiguous"]))
check("an ambiguous role is not also reported as flatly unavailable",
      "matru_putra" not in ra7["sthira_fallback_unavailable"])

print("\nvv.1-2 middle school — Rahu admitted ONLY to repair a tie's shortfall:")
r_lazy = chara_karakas(nativity, grahas="seven_rahu_on_tie", roles=7)
check("no tie among the seven -> Rahu stays out",
      all(x["graha"] != "rahu" for x in r_lazy["ranking"]))
r_lazy2 = chara_karakas(tied, grahas="seven_rahu_on_tie", roles=7)
check("a tie appears -> Rahu is brought in",
      any(x["graha"] == "rahu" for x in r_lazy2["ranking"]))
# v.1-2 admits ONE extra body for the tie, so it restores exactly one slot:
# seven planets with one tie give 6 groups, and Rahu makes the 7th.
check("and the shortfall is repaired: 7 roles all filled",
      r_lazy2["unfilled"] == [], str(r_lazy2["unfilled"]))
check("but one extra body cannot fill 8 roles after a tie -> stree still short",
      chara_karakas(tied, grahas="seven_rahu_on_tie", roles=8)["unfilled"] == ["stree"])
# The requested school must survive: a caller has to be able to tell the middle
# position from an outright 'eight'.
check("the requested school is preserved, not rewritten to 'eight'",
      r_lazy2["scheme"]["grahas"] == "seven_rahu_on_tie",
      str(r_lazy2["scheme"]))
check("and Rahu's admission under the tie rule is flagged",
      r_lazy2["scheme"]["rahu_admitted_on_tie"] is True, str(r_lazy2["scheme"]))
check("no tie -> the flag is False, though the school is still reported",
      r_lazy["scheme"]["grahas"] == "seven_rahu_on_tie" and
      r_lazy["scheme"]["rahu_admitted_on_tie"] is False, str(r_lazy["scheme"]))
check("an outright 'eight' is distinguishable from the middle school",
      chara_karakas(tied, grahas="eight", roles=7)["scheme"] ==
      {"grahas": "eight", "roles": 7, "rahu_admitted_on_tie": False})

print("\nDeclared gaps are exposed as flags, and say what the text does/doesn't:")
check("TIE_FALLBACK_INCOMPLETE names all three missing roles",
      all(k in TIE_FALLBACK_INCOMPLETE for k in ("atma", "amatya", "gnati")))
check("TIE_FALLBACK_AMBIGUOUS names both readings of the merged slot",
      TIE_FALLBACK_AMBIGUOUS["matru_putra"] == ("moon", "jupiter"))
check("the Upakheta flag records the ch.33 recurrence, not 'no further use'",
      "ch.33" in ANTHYA_MADHYA_UPAKHETA_UNRECOVERABLE and
      "upagraha" in ANTHYA_MADHYA_UPAKHETA_UNRECOVERABLE)
check("the Vol II flag concedes only the seven unreadable arcs",
      "16°04'26\"" in VOL2_CH46_DEGREES_UNRECOVERABLE)

print("\nch.33 v.1 — Karakamsa = the navamsa sign occupied by the Atmakaraka:")
# BOOK-ANCHORED. Vol I ch.39, note to slokas 3-5 (pdf 387-388) makes THREE
# checkable statements about this very chart, and all three are asserted here
# against the book rather than against our own d9 output:
#   "In the chart given in ch. 29 (sloka l-3), we have Atma Karaka Moon in
#    Jupiter's Navamsa."
#   "Putra Karaka (Chara scheme) for the gid [said] horoscope in the Sun."
#   "In the Navamsa chart, the Sun is placed in the 4th from Atma Karaka."
JUPITER_SIGNS = (8, 11)          # Dhanus, Meena
km = karakamsa(nativity, navamsa_of=d9_navamsa)
check("ch.39: 'we have Atma Karaka Moon ...'", km["atmakaraka"] == "moon")
check("ch.39: '... Moon in Jupiter's Navamsa' (Dhanus or Meena)",
      km["karakamsa"] in JUPITER_SIGNS, S[km["karakamsa"]])
check("ch.39: 'Putra Karaka (Chara scheme) ... in the Sun'",
      r["assignment"]["putra"] == ["sun"], str(r["assignment"]["putra"]))
# 4th from the Karakamsa, counted inclusively in signs.
sun_navamsa = d9_navamsa(int(nativity["sun"] // 30), nativity["sun"] % 30)
check("ch.39: 'the Sun is placed in the 4th from Atma Karaka' in the Navamsa",
      (sun_navamsa - km["karakamsa"]) % 12 + 1 == 4,
      "Sun navamsa %s, Karakamsa %s, distance %d" %
      (S[sun_navamsa], S[km["karakamsa"]], (sun_navamsa - km["karakamsa"]) % 12 + 1))
# Having confirmed the book's own description, pin the concrete signs.
check("Karakamsa is Dhanus (Mesha movable, 9th navamsa = Mesha+8)",
      km["karakamsa"] == 8, S[km["karakamsa"]])
check("and Dhanus is indeed one of Jupiter's signs", 8 in JUPITER_SIGNS)
check("the Sun's navamsa is Meena, the 4th from Dhanus",
      sun_navamsa == 11, S[sun_navamsa])
check("Moon sits in Mesha (rasi 0)", km["rasi"] == 0, S[km["rasi"]])
# The reckoning asymmetry: Rahu is SELECTED by 30-x but placed where he stands.
rahu_ak = {**nativity, "rahu": 9*30 + dms(0,0,30)}   # scores 29d59'30", top
kmr = karakamsa(rahu_ak, navamsa_of=d9_navamsa)
check("Rahu can become Atmakaraka via the inversion", kmr["atmakaraka"] == "rahu")
check("but his Karakamsa is the navamsa of where he ACTUALLY stands",
      kmr["karakamsa"] == d9_navamsa(9, dms(0,0,30)), S[kmr["karakamsa"]])

print("\nch.32 vv.18-21 — BPHS's OWN sthira karakas (they are NOT the popular list):")
check("Venus = husband (popular list says wife)",
      "husband" in STHIRA_KARAKAS["venus"], str(STHIRA_KARAKAS["venus"]))
check("Saturn = sons (popular list says death/longevity)",
      STHIRA_KARAKAS["saturn"] == ("sons",), str(STHIRA_KARAKAS["saturn"]))
check("Jupiter = paternal grandfather (popular list says sons)",
      STHIRA_KARAKAS["jupiter"] == ("paternal grandfather",))
check("Ketu = wife, father, mother, parents-in-law, maternal grandfather",
      STHIRA_KARAKAS["ketu"] == ("wife","father","mother","parents-in-law",
                                 "maternal grandfather"))
check("father is contested between Sun and Venus",
      "father (stronger of Sun and Venus)" in STHIRA_KARAKAS["sun"] and
      "father (stronger of Sun and Venus)" in STHIRA_KARAKAS["venus"])
check("mother is contested between Moon and Mars",
      "mother (stronger of Moon and Mars)" in STHIRA_KARAKAS["moon"] and
      "mother (stronger of Moon and Mars)" in STHIRA_KARAKAS["mars"])
check("Mercury = maternal relatives", STHIRA_KARAKAS["mercury"] == ("maternal relatives",))
check("Ketu IS a sthira karaka even though he is never a chara karaka",
      "ketu" in STHIRA_KARAKAS and "ketu" not in EIGHT_GRAHAS)

print("\nch.32 vv.22-24 — the separate house-based list (the popular list's source):")
book_houses = {"sun":(9,"father"), "moon":(4,"mother"), "mars":(3,"brothers"),
               "mercury":(6,"maternal uncle"), "jupiter":(5,"sons"),
               "venus":(7,"wife"), "saturn":(8,"death")}
for g,(off,mean) in book_houses.items():
    check(f"{off}th from {g} -> {mean}", STHIRA_KARAKA_HOUSES[g] == (off,mean),
          str(STHIRA_KARAKA_HOUSES[g]))
check("vv.22-24 contradict vv.18-21 on Venus (wife vs husband)",
      STHIRA_KARAKA_HOUSES["venus"][1] == "wife" and
      "husband" in STHIRA_KARAKAS["venus"])
check("vv.22-24 contradict vv.18-21 on sons (Jupiter vs Saturn)",
      STHIRA_KARAKA_HOUSES["jupiter"][1] == "sons" and
      STHIRA_KARAKAS["saturn"] == ("sons",))
# ch.29 standard nativity has Scorpio lagna, so whole-sign bhavas:
bh = {g: (int((nativity[g] % 360)//30) - 7) % 12 + 1 for g in book_houses}
sh = sthira_karaka_houses(bh)
check("Sun in Vrishabha = 7th from Vrishchika lagna", bh["sun"] == 7)
check("9th from the Sun (7th bhava) = 3rd bhava",
      sh["sun"]["bhava"] == 3, str(sh["sun"]))
check("Jupiter in Karka = 9th bhava; 5th from it = 1st bhava",
      bh["jupiter"] == 9 and sh["jupiter"]["bhava"] == 1, str(sh["jupiter"]))
# Load-bearing on the ch.29 table's Saturn 63d09'41" = MITHUNA. If the fixture
# ever drifts back to Vrishabha, bh["saturn"] becomes 7 and this fails.
check("Saturn in Mithuna = 8th bhava from Vrishchika lagna",
      bh["saturn"] == 8, str(bh["saturn"]))
check("8th from Saturn (8th bhava) = 3rd bhava, signifying death",
      sh["saturn"]["bhava"] == 3 and sh["saturn"]["signifies"] == "death",
      str(sh["saturn"]))
# Same for the Rahu/Ketu orientation, via the karaka table's own Rahu.
check("Rahu in Karka = 9th bhava (Ketu in Makara = 3rd)",
      (int(nativity["rahu"] // 30) - 7) % 12 + 1 == 9 and
      (int(nativity["ketu"] // 30) - 7) % 12 + 1 == 3)
check("counting is inclusive and wraps at 12",
      sthira_karaka_houses({"saturn": 12})["saturn"]["bhava"] == 7)
# Venus's ordinal is the ONE numeral vv.22-24 does not preserve in this scan.
# It must be flagged wherever it can reach a reader, not silently emitted.
print("\nThe one reconstructed numeral in vv.22-24 is flagged, not hidden:")
sh_all = sthira_karaka_houses({g: 1 for g in STHIRA_KARAKA_HOUSES})
check("Venus's count is marked reconstructed",
      sh_all["venus"]["count_reconstructed"] is True)
check("and it is the ONLY one so marked (the other six digits are legible)",
      [g for g in sh_all if sh_all[g]["count_reconstructed"]] == ["venus"],
      str([g for g in sh_all if sh_all[g]["count_reconstructed"]]))
check("the flag constant says the numeral is illegible and 7 reconstructed",
      "illegible" in VENUS_HOUSE_RECONSTRUCTED and
      "RECONSTRUCTED" in VENUS_HOUSE_RECONSTRUCTED)
check("the docstring quotes the damaged vv.22-24 scan, not a cleaned-up version",
      'irr"-^iii,from venus' in karakas_doc and "3r. [3rd]" in karakas_doc)
check("and the damaged vv.18-21 scan likewise, repairs bracketed",
      "conslant [constant]" in karakas_doc and "&mong [among]" in karakas_doc)

print("\nInput hygiene:")
for bad in ("six", "nine", ""):
    try:
        chara_karakas(nativity, grahas=bad); ok = False
    except ValueError:
        ok = True
    check(f"grahas={bad!r} rejected", ok)
try:
    chara_karakas(nativity, roles=6); ok = False
except ValueError:
    ok = True
check("roles=6 rejected", ok)
try:
    chara_karakas({k: v for k, v in nativity.items() if k != "venus"}); ok = False
except ValueError as e:
    ok = "venus" in str(e)
check("a missing eligible graha is reported, not silently skipped", ok)
try:
    karakamsa(nativity); ok = False
except ValueError:
    ok = True
check("karakamsa refuses to guess a navamsa function", ok)

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
