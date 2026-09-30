"""
Varṣaphala — pin the calculation layer to what can be checked.

The Tājika text is not on hand, so there is no worked example to reproduce.
What CAN be checked: the varṣa-praveśa against the ephemeris (it is only the
Sun returning to a longitude), the Muntha against its own definition, and the
nine Mudda boundaries against an independent implementation (AstroSage, report
of 1 Jan 2026, for the 2026-27 year of the reference chart). The rule that
produced those nine dates — count the completed years on from the janma
nakṣatra, then Viṁśottarī order in years/120 of the solar year, first period
not prorated — is stated in varshaphal.py and pinned here; a text may say
otherwise, and if it does, this test is where that change lands.

Run:  PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python test_varshaphal.py
"""
import datetime as dt

import swisseph as swe

import varshaphal
import vedic  # noqa: F401
from vedic import compute_chart

BIRTH = dict(local_dt=dt.datetime(1975, 6, 25, 22, 30), latitude=26.46523,
             longitude=80.34975, tz_name="Asia/Kolkata", name="")
# AstroSage, Varshaphal 2026 (Kanpur): praveśa 26/6/2026 00:17:30 IST, lagna
# Pisces, Muntha 3rd bhāva, then nine Mudda periods:
AS_BOUNDARIES = ["2026-06-26", "2026-08-16", "2026-09-07", "2026-11-06", "2026-11-25",
                 "2026-12-25", "2027-01-15", "2027-03-11", "2027-04-29", "2027-06-26"]
AS_ORDER = ["mercury", "ketu", "venus", "sun", "moon", "mars", "rahu", "jupiter", "saturn"]


def _build(year=2026):
    natal = compute_chart(**BIRTH)
    now = swe.julday(2026, 9, 29, 12.0, swe.GREG_CAL)
    return varshaphal.build(natal, year, BIRTH["latitude"], BIRTH["longitude"],
                            BIRTH["tz_name"], now, BIRTH["local_dt"])


def _ok(name, cond, detail=""):
    print(f"  {'OK ' if cond else 'XX '}{name:52s} {detail}")
    assert cond, f"{name} {detail}"


def test_pravesha_is_the_suns_return():
    """The praveśa instant is when the Sun is back at its natal sidereal place."""
    v = _build()
    natal_sun = next(g["longitude"] for g in compute_chart(**BIRTH).to_dict()["grahas"] if g["key"] == "sun")
    sun_then = swe.calc_ut(v["pravesha"]["jd_ut"], swe.SUN, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0][0]
    diff = ((sun_then - natal_sun + 180.0) % 360.0 - 180.0) * 3600.0
    _ok("Sun at praveśa == natal Sun (arcsec)", abs(diff) < 0.05, f"{diff:+.4f}″")
    _ok("praveśa local 2026-06-26 00:18 (AstroSage 00:17:30)", v["pravesha"]["local"].startswith("2026-06-26 00:18"), v["pravesha"]["local"])
    _ok("year length ≈ 365.26 d", abs(v["mudda"]["variants"]["prorated"]["year_days"] - 365.2564) < 0.01, str(v["mudda"]["variants"]["prorated"]["year_days"]))


def test_muntha_definition_and_astrosage_bhava():
    v = _build()
    natal = compute_chart(**BIRTH)
    _ok("age at praveśa = 51", v["age"] == 51, str(v["age"]))
    _ok("muntha sign = janma lagna + 51 (Taurus)", v["muntha"]["sign"] == (natal.lagna_rasi + 51) % 12 == 1, str(v["muntha"]["sign"]))
    _ok("muntha bhāva from varṣa lagna = 3 (AstroSage 3)", v["muntha"]["house_from_varsha_lagna"] == 3)
    _ok("varṣa lagna Pisces (AstroSage)", v["varsha_lagna"]["sign"] == 11)


def test_mudda_boundaries_match_astrosage():
    v = _build()
    ps = v["mudda"]["variants"]["unprorated"]["periods"]
    _ok("nine periods (unprorated)", len(ps) == 9)
    _ok("start lord Mercury, from nakṣatra 18 (Jyeṣṭhā)", ps[0]["lord"] == "mercury" and v["mudda"]["variants"]["unprorated"]["start_nakshatra"] == 18)
    _ok("Viṁśottarī order from Mercury", [p["lord"] for p in ps] == AS_ORDER, str([p["lord"] for p in ps]))
    for i, p in enumerate(ps):
        got = dt.date.fromisoformat(p["start"][:10]); want = dt.date.fromisoformat(AS_BOUNDARIES[i])
        _ok(f"{p['lord']:8s} starts {AS_BOUNDARIES[i]}", abs((got - want).days) <= 1, f"got {got}")
    end = dt.date.fromisoformat(ps[-1]["end"][:10])
    _ok("year ends at next praveśa 2027-06-26", abs((end - dt.date.fromisoformat(AS_BOUNDARIES[-1])).days) <= 1, str(end))
    _ok("periods sum to the year (days)", abs(sum(p["days"] for p in ps) - v["mudda"]["variants"]["unprorated"]["year_days"]) < 0.05)
    pro = v["mudda"]["variants"]["prorated"]["periods"]
    _ok("prorated: Mercury opens with the balance (48% of 51.7 d ≈ 24.8) and closes the year", pro[0]["kind"] == "balance" and abs(pro[0]["days"] - 24.8) < 0.5 and pro[-1]["lord"] == "mercury" and pro[-1]["kind"] == "remainder", f"{pro[0]}, {pro[-1]['lord']}")


def test_refusals_are_explicit():
    v = _build()
    what = " ".join(r["what"] for r in v["refused"])
    for must in ("phala", "Patyāyinī", "dvādaśavargīya"):
        _ok(f"refused lists {must}", must in what)
    _ok("year-lord IS chosen now (night praveśa)", v["varshesha"]["lord"] in ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn") and v["is_day"] is False)
    _ok("all five office-bearers named", all(v["panchadhikari"][k] for k in ("muntha_lord", "janma_lagna_lord", "varsha_lagna_lord", "trirasi_lord", "dinaratri_lord")))
    _ok("fifty sahams, sixteen-yoga table for 11 houses", len(v["sahams"]) == 50 and len(v["yogas"]["houses"]) == 11)


def test_default_year_is_the_running_varsha():
    natal = compute_chart(**BIRTH)
    before = swe.julday(2026, 6, 20, 12.0, swe.GREG_CAL)   # before the 2026 praveśa → 2025 varṣa
    after = swe.julday(2026, 7, 1, 12.0, swe.GREG_CAL)
    v0 = varshaphal.build(natal, None, BIRTH["latitude"], BIRTH["longitude"], BIRTH["tz_name"], before, BIRTH["local_dt"])
    v1 = varshaphal.build(natal, None, BIRTH["latitude"], BIRTH["longitude"], BIRTH["tz_name"], after, BIRTH["local_dt"])
    _ok("20 Jun 2026 → varṣa 2025", v0["year"] == 2025, str(v0["year"]))
    _ok("1 Jul 2026 → varṣa 2026", v1["year"] == 2026, str(v1["year"]))


def main():
    names = [n for n in globals() if n.startswith("test_")]
    failed = 0
    for n in names:
        print(f"\n{n}")
        try:
            globals()[n]()
        except AssertionError as e:
            failed += 1
            print(f"  FAILED: {e}")
    print("\n" + ("ALL PASS ✓" if not failed else f"{failed} FAILED ✗"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
