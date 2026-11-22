"""karakamsa_results.py (BPHS I ch.33).

    cd api && PYTHONUTF8=1 ../.venv/Scripts/python.exe -c "import test_karakamsa_results as T; [getattr(T,n)() for n in dir(T) if n.startswith('test_')]; print('ok')"
"""

import karakamsa_results as kr

ARI, TAU, GEM, CAN, LEO, VIR, LIB, SCO, SAG, CAP, AQU, PIS = range(12)
NAT = {"sun": "malefic", "mars": "malefic", "saturn": "malefic", "rahu": "malefic", "ketu": "malefic",
       "jupiter": "benefic", "venus": "benefic", "moon": "benefic", "mercury": "benefic"}


def _kk(sign, ak="venus"):
    return {"karakamsa": sign, "atmakaraka": ak, "candidates": [{"graha": ak, "karakamsa": sign}]}


def test_shared_atma_role_evaluates_nothing():
    out = kr.evaluate({"karakamsa": None, "atmakaraka": None, "candidates": [{}, {}]}, {}, {}, NAT, None)
    assert out["available"] is False


def test_sign_verse_names_the_navamsa():
    pos = {g: ARI for g in NAT}
    out = kr.evaluate(_kk(PIS), pos, pos, NAT, ARI)
    first = out["matches"][0]
    assert first["key"] == "2-8" and "Meen navamsa" in first["clauses"][0]["why"]


def test_both_frames_are_reported_and_labelled():
    d1 = {g: ARI for g in NAT}
    d9 = {**{g: TAU for g in NAT}, "saturn": GEM}        # Saturn in the 3rd from a Mesh Karakamsa, D9 only
    out = kr.evaluate(_kk(ARI), d1, d9, NAT, ARI)
    v32 = [m for m in out["matches"] if m["key"] == "32"]
    assert [m["frame"] for m in v32] == ["navamsa"]
    assert "(in the navamsa chart)" in v32[0]["clauses"][0]["why"]


def test_ketu_in_12th_in_sagittarius_aspected_by_benefic():
    # Karakamsa Capricorn -> 12th is Sagittarius; Jupiter in Gemini aspects it (7th).
    d = {"ketu": SAG, "jupiter": GEM, "sun": LEO, "moon": LEO, "mars": LEO, "mercury": LEO,
         "venus": LEO, "saturn": LEO, "rahu": GEM}
    out = kr.evaluate(_kk(CAP), d, d, NAT, ARI)
    whys = [c["why"] for m in out["matches"] if m["key"] == "63-74" for c in m["clauses"]]
    assert any("in Dhanu, aspected by a benefic" in w for w in whys)


def test_every_match_is_whole_and_cited():
    d = {"sun": ARI, "moon": TAU, "mars": GEM, "mercury": CAN, "jupiter": LEO, "venus": VIR,
         "saturn": LIB, "rahu": SCO, "ketu": TAU}
    out = kr.evaluate(_kk(ARI), d, d, NAT, ARI)
    for m in out["matches"]:
        assert m["citation"].startswith("BPHS I ch.33") and m["text"] == kr.V[m["key"]][1]
        assert m["clauses"]


def test_excluded_verses_are_not_registered():
    for k in ("12", "23-24", "25-29", "30-31", "47-48", "49", "94-99"):
        assert k not in kr.V
