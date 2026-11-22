"""Hand-registered yogas (yoga_rules_extra.py, 2026-11-22), each checked on a constructed chart.

    cd api && PYTHONUTF8=1 ../.venv/Scripts/python.exe -c "import test_yoga_extra as T; [getattr(T,n)() for n in dir(T) if n.startswith('test_')]; print('ok')"
"""

import yoga_rules
import yogas
import vargas

ARI, TAU, GEM, CAN, LEO, VIR, LIB, SCO, SAG, CAP, AQU, PIS = range(12)


def _pos(lons):
    return {g: {"longitude": x, "rasi": int(x // 30),
                "vargas": {"D9": vargas.d9_navamsa(int(x // 30), x % 30)}} for g, x in lons.items()}


def _det(lons, lagna, shadbala=None):
    return {y["name"]: y for y in yogas.detect_yogas(_pos(lons), lagna, shadbala=shadbala)["detected"]}


def _at(sign, deg=15.0):
    return sign * 30 + deg


def test_catalogue_entries_carry_source_and_citation():
    for name in ("Lakshmi Yoga", "Harsha Yoga", "Sarala Yoga", "Vimala Yoga", "Pravrajya Yoga",
                 "Nicabhanga: a lord in a kendra", "Nicabhanga: the two lords in mutual kendras",
                 "Nicabhanga: aspected by its sign's lord"):
        m = yoga_rules.YOGAS[name]
        assert m["citation"] and m["source"] and m["tier"] in ("sloka", "classical"), name
        assert name in yogas.DETECTORS, name
    assert yoga_rules.YOGAS["Lakshmi Yoga"]["tier"] == "sloka"          # BPHS
    assert yoga_rules.YOGAS["Harsha Yoga"]["tier"] == "classical"       # Phaladipika, never "sloka"


# Lagna Aries: 9th = Sagittarius, lord Jupiter. Jupiter in Sagittarius is in the 9th (a trikona,
# not a kendra): no Lakshmi. Jupiter exalted in Cancer = the 4th (kendra): Lakshmi.
BASE = {"sun": _at(TAU), "moon": _at(GEM), "mars": _at(LEO), "mercury": _at(TAU, 20),
        "jupiter": _at(SAG), "venus": _at(GEM, 20), "saturn": _at(AQU)}


def test_lakshmi_needs_ninth_lord_in_kendra_with_dignity():
    assert "Lakshmi Yoga" not in _det(BASE, ARI)
    assert "Lakshmi Yoga" in _det({**BASE, "jupiter": _at(CAN, 5)}, ARI)
    assert "Lakshmi Yoga" not in _det({**BASE, "jupiter": _at(LIB)}, ARI)   # kendra, no dignity


def test_lakshmi_strength_gate_is_the_ascendant_lord():
    lons = {**BASE, "jupiter": _at(CAN, 5)}
    weak = {g: {"strong": g != "mars", "total_rupa": 6.0, "min_required_rupa": 5.0} for g in lons}
    y = _det(lons, ARI, shadbala=weak)["Lakshmi Yoga"]
    assert y["strength"]["grahas"][0]["graha"] == "mars" and y["strength"]["fructifies"] is False


def test_v57_clauses_are_reported_separately():
    # Lagna Aries: 6th Virgo (lord Mercury). Mercury in Taurus = 2nd; no malefic in/aspecting Virgo
    lons = {**BASE, "mercury": _at(TAU, 20)}
    d = _det(lons, ARI)
    if "Harsha Yoga" in d:                      # only via a malefic clause, never the lord clause
        assert d["Harsha Yoga"]["detail"]["clause_lord_in_6_8_12"] is False
    # Mercury into Scorpio (the 8th): lord clause holds
    h = _det({**lons, "mercury": _at(SCO), "sun": _at(SCO, 25)}, ARI)["Harsha Yoga"]["detail"]
    assert h["clause_lord_in_6_8_12"] is True and h["lord"] == "mercury" and h["lord_in_house"] == 8


def test_nicabhanga_kendra_both_readings_labelled():
    # Sun debilitated in Libra (lord Venus; Sun's exaltation sign Aries, lord Mars; Saturn is
    # exalted in Libra = the note's reading). Lagna Aries: Mars in the 1st is a kendra.
    lons = {**BASE, "sun": _at(LIB), "mars": _at(ARI), "venus": _at(GEM), "saturn": _at(CAP)}
    hits = _det(lons, ARI)["Nicabhanga: a lord in a kendra"]["detail"]["hits"]
    assert {"planet": "sun", "by": "mars", "role": "lord of the exaltation sign",
            "from": "lagna", "reading": "text"} in hits
    assert {h["by"] for h in hits if h["reading"] == "note"} == {"saturn"}   # Capricorn = 10th


def test_nicabhanga_never_counts_the_moon_against_itself():
    # Mars debilitated in Cancer; its sign's lord is the Moon. Moon in Taurus = 2nd from Aries.
    lons = {**BASE, "mars": _at(CAN), "moon": _at(TAU), "saturn": _at(LEO)}
    d = _det(lons, ARI).get("Nicabhanga: a lord in a kendra")
    assert not d or all(h["by"] != "moon" for h in d["detail"]["hits"])


def test_nicabhanga_aspect_by_sign_lord():
    # Jupiter debilitated in Capricorn (the 10th from Aries); Saturn in Cancer aspects it (7th).
    lons = {**BASE, "jupiter": _at(CAP), "saturn": _at(CAN)}
    h = _det(lons, ARI)["Nicabhanga: aspected by its sign's lord"]["detail"]["hits"]
    assert h == [{"planet": "jupiter", "by": "saturn", "outside_6_8_12": True}]


def test_pravrajya_four_in_one_sign_and_strongest_names_the_order():
    lons = {**BASE, "mars": _at(PIS, 2), "jupiter": _at(PIS, 10), "venus": _at(PIS, 27),
            "saturn": _at(PIS, 18)}
    y = _det(lons, ARI)
    assert y["Pravrajya Yoga"]["detail"]["planets"] == ["mars", "jupiter", "venus", "saturn"]
    sb = {g: {"strong": True, "total_rupa": r, "min_required_rupa": 5.0}
          for g, r in {"sun": 5, "moon": 5, "mars": 6, "mercury": 6, "jupiter": 9, "venus": 7,
                       "saturn": 6.5}.items()}
    s = _det(lons, ARI, shadbala=sb)["Pravrajya Yoga"]["strength"]
    assert s["fructifies"] and s["strongest"] == "jupiter" and s["order"] == "Bhikshu"
    sb["saturn"]["strong"] = False                       # only three strong: does not fructify
    assert _det(lons, ARI, shadbala=sb)["Pravrajya Yoga"]["strength"]["fructifies"] is False
    assert "Pravrajya Yoga" not in _det(BASE, ARI)
