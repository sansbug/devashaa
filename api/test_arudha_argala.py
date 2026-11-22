"""arudha_argala.py against Santhanam's own worked examples (BPHS I chs 29 and 31).

    cd api && PYTHONUTF8=1 ../.venv/Scripts/python.exe -c "import test_arudha_argala as T; [getattr(T,n)() for n in dir(T) if n.startswith('test_')]; print('ok')"
"""

import arudha_argala as aa

ARI, TAU, GEM, CAN, LEO, VIR, LIB, SCO, SAG, CAP, AQU, PIS = range(12)

# ch.29 "standard nativity" (p.293-294): Scorpio lagna 0°48'34"; longitudes from the table.
STD_LON = {"sun": 37 + 12 / 60, "moon": 27 + 35 / 60, "mars": 96 + 18 / 60, "mercury": 14 + 54 / 60,
           "jupiter": 116 + 7 / 60, "venus": 27 + 17 / 60, "saturn": 63 + 9 / 60,
           "rahu": 97 + 37 / 60, "ketu": 277 + 37 / 60}
STD = {g: {"longitude": x, "rasi": int(x // 30)} for g, x in STD_LON.items()}


PRINTED_CHART = {1: PIS, 2: AQU, 3: SCO, 4: LIB, 5: SCO, 6: CAN, 7: PIS, 8: AQU, 9: CAP, 10: AQU, 11: SCO, 12: CAN}


def test_printed_chart_differs_only_where_it_skips_the_7th_exception():
    """Houses 9 and 10 of the printed chart (p.295) are the plain count of vv.2-3: their
    count lands on the 7th from the house and the printed chart keeps it there."""
    rasi = {g: p["rasi"] for g, p in STD.items()}
    for h in (9, 10):
        s = (SCO + h - 1) % 12
        assert aa.pada_plain(s, rasi[aa.RASI_LORD[s]]) == PRINTED_CHART[h]
        assert PRINTED_CHART[h] == (s + 6) % 12


def test_verse_exceptions_change_only_houses_9_and_10():
    got = aa.bhava_padas(SCO, {g: p["rasi"] for g, p in STD.items()})
    diff = {h for h in got if got[h] != PRINTED_CHART[h]}
    assert diff == {9, 10}
    assert got[9] == LIB and got[10] == SCO      # the 4th from Cancer / from Leo (v.5)


def test_exceptions_from_the_notes():
    # Note 1 (p.296): Sagittarius house with Jupiter in it -> Virgo (verse and note agree).
    assert aa.pada(SAG, SAG) == VIR
    # Note 3 (p.297): Leo lagna, the Sun in Scorpio (4th) -> Scorpio itself (agree).
    assert aa.pada(LEO, SCO) == SCO
    # Note 2: Aquarius with Saturn in Leo. The note says Taurus; by the verse the count
    # lands on Aquarius itself, so its 10th, Scorpio. The verse is followed.
    assert aa.pada(AQU, LEO) == SCO


def test_graha_pada_example():
    # p.297: the Sun in Capricorn -> Leo is the 8th -> 8th from Leo = Pisces.
    assert aa.graha_pada("sun", CAP) == PIS
    assert aa.graha_pada("mars", ARI) is None


def test_argala_hypothetical_chart():
    """ch.31 p.313: Aries lagna; Mars 4th, Sun+Mercury 2nd, Jupiter 11th cause Argala;
    Saturn 10th, Venus 12th, Moon+Rahu 3rd obstruct them."""
    pos = {"mars": CAN, "sun": TAU, "mercury": TAU, "jupiter": AQU, "saturn": CAP,
           "venus": PIS, "moon": GEM, "rahu": GEM, "ketu": SAG}
    lon = {g: s * 30 + 10 for g, s in pos.items()}
    nat = {"sun": "malefic", "mars": "malefic", "saturn": "malefic", "rahu": "malefic", "ketu": "malefic",
           "jupiter": "benefic", "venus": "benefic", "moon": "benefic", "mercury": "malefic"}
    a = aa.argala(ARI, pos, lon, nat)
    by = {p["from"]: p for p in a["places"]}
    assert set(by) == {4, 2, 11}
    assert by[4]["obstructors"] == ["saturn"] and by[4]["status_vv2_9"] == "obstructed_unless_stronger"
    assert set(by[2]["argala"]) == {"sun", "mercury"} and by[2]["obstructors"] == ["venus"]
    assert by[2]["status_vv2_9"] == "prevails_by_number"          # two against one (v.4)
    assert set(by[11]["obstructors"]) == {"moon", "rahu"}
    assert by[11]["grade_v7"] == "limited" and by[2]["grade_v7"] == "medium"


def test_quarter_rule_v10():
    pos = {"mars": CAN, "saturn": CAP}
    nat = {"mars": "malefic", "saturn": "malefic"}
    q1, q4 = CAN * 30 + 3, CAP * 30 + 25
    a = aa.argala(ARI, pos, {"mars": q1, "saturn": q4}, nat)
    assert a["places"][0]["countered_v10"] is True
    a = aa.argala(ARI, pos, {"mars": q1, "saturn": CAP * 30 + 3}, nat)
    assert a["places"][0]["countered_v10"] is False


def test_v16_needs_a_conjunct_benefic_and_malefic_aspecting_the_12th():
    # Aries lagna; Mars in Aries rules it -> 9th? keep it simple: put the AL in Aries by
    # making the lagna Aries with Mars in Libra (7th) -> pada falls on Aries itself -> 10th = Capricorn.
    # So build directly: AL = Capricorn, 12th from it = Sagittarius; Jupiter + Saturn in Gemini aspect it.
    pos = {"mars": LIB, "jupiter": GEM, "saturn": GEM, "sun": TAU, "moon": TAU, "mercury": TAU,
           "venus": TAU, "rahu": LEO, "ketu": AQU}
    P = {g: {"rasi": s, "longitude": s * 30 + 12} for g, s in pos.items()}
    out = aa.evaluate(P, ARI)
    assert out["padas"][1]["sign"] == CAP
    m = [x for x in out["matches"] if x["key"] == "29.16-17"]
    assert m and "Guru" in m[0]["clauses"][0]["why"] and "Shani" in m[0]["clauses"][0]["why"]
    # The same pair placed IN the 12th instead (not aspecting it) does not fire.
    pos2 = {**pos, "jupiter": SAG, "saturn": SAG}
    out2 = aa.evaluate({g: {"rasi": s, "longitude": s * 30 + 12} for g, s in pos2.items()}, ARI)
    assert not [x for x in out2["matches"] if x["key"] == "29.16-17"]


def test_vipareeta_needs_three_malefics_in_the_3rd():
    pos = {"sun": GEM, "mars": GEM, "saturn": GEM}
    nat = {g: "malefic" for g in pos}
    assert aa.argala(ARI, pos, {g: GEM * 30 + 5 for g in pos}, nat)["vipareeta"] == ["sun", "mars", "saturn"]


def test_standard_nativity_verses_are_whole_and_cited():
    out = aa.evaluate(STD, SCO)
    assert out["padas"][1]["sign"] == PIS
    for m in out["matches"]:
        assert m["citation"].startswith("BPHS I ch.") and m["text"] and m["clauses"]
    # Santhanam's note to v.17 (p.299): Mars's 8th aspect falls on the 12th from the Arudha Lagna (Aquarius).
    keys = {m["key"] for m in out["matches"]}
    assert "29.8-11" in keys       # Jupiter (exalted, Cancer) aspects the 11th from AL (Capricorn), per his note on vv.13-15
