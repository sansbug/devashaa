"""Regression: "own sign or exaltation" includes the mula-trikona part of the sign.

BPHS Vol II ch.75 vv.1-2 (p.924): Mars ... Saturn "being in their own sign or in their sign of
exaltation, be in kendra to the Ascendant". dignity.dignity_of labels the mula-trikona arc
"moolatrikona", and the detectors used to skip it (found by the web comparison, 2026-11-21:
Van Gogh's and Prince Harry's Jupiter in early Sagittarius, Ali's Mars in early Aries, Elvis's
Saturn in early Aquarius, Nehru's Venus in early Libra).

    cd api && PYTHONUTF8=1 ../.venv/Scripts/python.exe -c "import test_yoga_own_sign as T; [getattr(T,n)() for n in dir(T) if n.startswith('test_')]; print('ok')"
"""

import dignity
import yogas
import vargas

SAG, ARI, AQU, LIB, GEM = 8, 0, 10, 6, 2


def _pos(lons):
    return {g: {"longitude": x, "rasi": int(x // 30),
                "vargas": {"D9": vargas.d9_navamsa(int(x // 30), x % 30)}} for g, x in lons.items()}


BASE = {"sun": 40.0, "moon": 70.0, "mars": 100.0, "mercury": 130.0, "jupiter": 160.0,
        "venus": 190.0, "saturn": 220.0, "rahu": 250.0, "ketu": 70.0}


def _names(lons, lagna):
    return {y["name"] for y in yogas.detect_yogas(_pos(lons), lagna)["detected"]}


def test_jupiter_moolatrikona_in_kendra_is_hamsa():
    lons = {**BASE, "jupiter": SAG * 30 + 2.5}
    assert dignity.dignity_of("jupiter", lons["jupiter"])["state"] == "moolatrikona"
    assert "Hamsa" in _names(lons, SAG)               # Jupiter in the 1st, its own sign


def test_mars_moolatrikona_in_kendra_is_ruchaka():
    lons = {**BASE, "mars": ARI * 30 + 5}
    assert dignity.dignity_of("mars", lons["mars"])["state"] == "moolatrikona"
    assert "Ruchaka" in _names(lons, ARI)


def test_not_in_kendra_is_still_no_yoga():
    lons = {**BASE, "jupiter": SAG * 30 + 2.5}
    assert "Hamsa" not in _names(lons, GEM + 1)       # Sagittarius is the 6th from Cancer
