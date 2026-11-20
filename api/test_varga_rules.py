"""varga_rules.py (BPHS I chs 6-7) and bj_varga_rules.py (Bṛhat Jātaka chs 16, 27):
each value is pinned to what the page image shows.

    cd api && PYTHONUTF8=1 ../.venv/Scripts/python.exe -c "import test_varga_rules as T; [getattr(T,n)() for n in dir(T) if n.startswith('test_')]; print('ok')"
"""

import varga_rules as vr
import bj_varga_rules as bj

ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO = range(6)
LIBRA, SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES = range(6, 12)


def test_list_lengths_match_the_pages():
    assert len(vr._D20_ODD) == len(vr._D20_EVEN) == 20
    assert len(vr._D24) == 12 and len(vr._D27) == 27 and len(vr._D40) == 12
    assert len(vr.D60) == 60
    assert sum(1 for _, m in vr.D60 if m == "B") == 33   # counted on pp.84-86
    assert set(vr.USES) == {"D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20",
                            "D24", "D27", "D30", "D40", "D45", "D60"}


def test_d60_order_and_reversal():
    assert vr.deity("D60", ARIES, 0.2)["name"] == "Ghora"                 # odd, 0-0°30'
    assert vr.deity("D60", ARIES, 29.9)["name"] == "Chandrarekha (Indurekha)"         # odd, 29°30'-30°
    assert vr.deity("D60", TAURUS, 0.2)["name"] == "Chandrarekha (Indurekha)"         # even 0°-0°30' = No.60
    assert vr.deity("D60", TAURUS, 29.9)["name"] == "Ghora"
    d = vr.deity("D60", ARIES, 1.2)                                       # 1°-1°30' Deva (B)
    assert (d["name"], d["nature"], d["number"]) == ("Deva", "benefic", 3)
    assert vr.deity("D60", ARIES, 13.2).get("disputed")                   # Kalinasa


def test_reversals_for_even_signs():
    assert vr.deity("D10", TAURUS, 1)["name"] == "Anantha"
    assert vr.deity("D7", TAURUS, 1)["name"] == "Suddha Jala"
    assert vr.deity("D16", ARIES, 1)["name"] == "Brahma"
    assert vr.deity("D16", TAURUS, 1)["name"] == "Sun"
    assert vr.deity("D24", ARIES, 1)["name"] == "Skanda"
    assert vr.deity("D24", TAURUS, 1)["name"] == "Bhima"
    assert vr.deity("D24", ARIES, 29.9)["name"] == "Bhima"                # 12 names, twice
    assert vr.deity("D27", TAURUS, 0.5)["name"] == "Pusha"
    assert vr.deity("D20", TAURUS, 0.5)["name"] == "Daya"                 # its own list
    assert vr.deity("D30", ARIES, 1)["name"] == "Agni"
    assert vr.deity("D30", ARIES, 12)["name"] == "Indra"                  # 10-18 odd
    assert vr.deity("D30", TAURUS, 1)["name"] == "Varuna"
    assert vr.deity("D30", TAURUS, 6)["name"] == "Kubera"                 # even 5-12
    assert vr.deity("D3", TAURUS, 25)["name"] == "Doorvasa"               # no reversal stated
    assert vr.deity("D12", ARIES, 29)["name"] == "Sarpa"


def test_mobility_orders():
    assert vr.deity("D9", ARIES, 1)["name"] == "Deva"
    assert vr.deity("D9", TAURUS, 1)["name"] == "Manushya"
    assert vr.deity("D9", GEMINI, 1)["name"] == "Rakshasa"
    assert vr.deity("D45", LEO, 0.1)["name"] == "Siva"
    assert vr.deity("D45", PISCES, 0.1)["name"] == "Vishnu"
    assert vr.deity("D40", LIBRA, 29.9)["name"] == "Tvashta"              # 4th round stops at Tvashta


def test_hora_and_thirds():
    assert vr.hora_of(ARIES, 5) == "sun" and vr.hora_of(TAURUS, 5) == "moon"
    assert vr.hora_effect("jupiter", ARIES, 5)["gives_effects"] is True
    assert vr.hora_effect("saturn", ARIES, 5)["gives_effects"] is False
    assert vr.hora_effect("mercury", TAURUS, 20)["gives_effects"] is True
    assert vr.hora_effect("rahu", ARIES, 5) is None
    assert vr.thirds("D2", 4)["grade"] == "full"
    assert vr.thirds("D2", 7)["grade"] == "medium"
    assert vr.thirds("D2", 14)["grade"] == "nil"
    assert vr.thirds("D9", 3.3)["grade"] == "nil"


def test_bj_coverage_and_gaps_are_disjoint():
    assert set(bj.MOON_IN_NAKSHATRA) == set(range(8, 28))
    assert not set(bj.MOON_IN_NAKSHATRA) & set(bj.NAKSHATRA_MISSING)
    assert set(bj.DREKKANA) | set(bj.DREKKANA_MISSING) == set(range(1, 37))
    assert not set(bj.DREKKANA) & set(bj.DREKKANA_MISSING)


def test_bj_lookup():
    assert bj.drekkana_form(ARIES, 5)["stanza"] == 1
    assert bj.drekkana_form(PISCES, 25)["stanza"] == 36
    assert bj.drekkana_form(LEO, 5).get("missing")
    assert bj.moon_in_nakshatra(1) is None
    assert bj.moon_in_nakshatra(8)["citation"] == "Bṛhat Jātaka 16.5 (Row, p.187)"
    assert bj.moon_in_nakshatra(27)["citation"].endswith("p.188)")


def test_every_adapted_line_says_why():
    for table in (bj.MOON_IN_NAKSHATRA, bj.DREKKANA):
        for k, e in table.items():
            if "shown" in e:
                assert e["shown"] != e["text"] and e["adaptation"]["note"], k
            if "adaptation" in e:
                assert "shown" in e, k
