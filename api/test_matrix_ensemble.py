"""Tests for the projection ensemble (phase 2): the chara-daśā direction rule,
the fusion math, and the per-step band/conviction invariants."""

import datetime as dt

import matrix
import vedic


class _Chart:
    def __init__(self, lagna):
        self.lagna_rasi = lagna


def test_chara_direction_matches_canonical_lagna_list():
    # K.N. Rao / Neelakantha: direct when the 9th sign from lagna is odd-footed (savya).
    # Canonical: DIRECT for Ar, Le, Vi, Li, Aq, Pi; REVERSE for the rest.
    direct = {0, 4, 5, 6, 10, 11}
    for lagna in range(12):
        want = "direct" if lagna in direct else "reverse"
        assert matrix._chara_direction(_Chart(lagna)) == want, (lagna, want)


def test_fuse_agreement_gives_high_conviction():
    central, spread, cf = matrix._fuse({"vims": 0.5, "goch": 0.5, "chara": 0.5, "trig": 0.5})
    assert abs(central - 0.5) < 1e-9 and spread < 1e-9 and cf > 0.99


def test_fuse_disagreement_lowers_conviction():
    _, spread, cf = matrix._fuse({"vims": 0.8, "goch": -0.8, "chara": 0.0, "trig": 0.0})
    assert spread > 0.4 and cf < 0.2


def test_fuse_abstain_excludes_clock():
    # chara=None must be dropped, not counted as 0.
    c1, _, _ = matrix._fuse({"vims": 0.6, "goch": 0.6, "chara": None, "trig": 0.6})
    c2, _, _ = matrix._fuse({"vims": 0.6, "goch": 0.6, "trig": 0.6})
    assert abs(c1 - c2) < 1e-9 and abs(c1 - 0.6) < 1e-9


def test_ensemble_band_contains_value_and_conviction_bounded():
    chart = vedic.compute_chart(dt.datetime(1990, 5, 15, 8, 30), 28.6139, 77.2090, "Asia/Kolkata")
    tl = matrix.build(chart)["timeline"]
    assert tl["charaDirection"] in ("direct", "reverse")
    for s in tl["steps"]:
        for tk, v in s["themes"].items():
            lo, hi = s["bands"][tk]
            assert lo - 1e-9 <= v <= hi + 1e-9, (tk, v, lo, hi)
            assert 0.0 <= s["conv"][tk] <= 1.0
            assert -1.0 <= v <= 1.0


def test_project_at_matches_timeline_exactly():
    # _project_at (used by backtest) must reproduce the timeline loop bit-for-bit,
    # so the two never silently diverge.
    import swisseph as swe
    chart = vedic.compute_chart(dt.datetime(1990, 5, 15, 8, 30), 28.6139, 77.2090, "Asia/Kolkata")
    m = matrix.build(chart)
    ctx = matrix._projection_context(chart, m)
    for s in m["timeline"]["steps"]:
        y, mo, d = (int(x) for x in s["date"].split("-"))
        jd = swe.julday(y, mo, d, 12.0, swe.GREG_CAL)
        pj = matrix._project_at(jd, ctx)["themes"]
        for tk, v in s["themes"].items():
            assert abs(pj[tk]["v"] - v) < 1e-9, (tk, s["date"], pj[tk]["v"], v)


def test_backtest_scores_and_hitrate_bounded():
    chart = vedic.compute_chart(dt.datetime(1990, 5, 15, 8, 30), 28.6139, 77.2090, "Asia/Kolkata")
    m = matrix.build(chart)
    events = [{"date": "2015-06", "key": "marriage", "polarity": 1},
              {"date": "2019-03", "key": "career", "polarity": -1}]
    bt = matrix.backtest(chart, m, events)
    assert bt["summary"]["n"] == 2
    assert 0.0 <= bt["summary"]["hitRate"] <= 1.0
    for e in bt["events"]:
        assert e["hit"] == ((e["v"] * e["polarity"]) > 0)
    # unknown theme keys and malformed dates are skipped, not fatal.
    bt2 = matrix.backtest(chart, m, [{"date": "bad", "key": "career", "polarity": 1},
                                     {"date": "2015-06", "key": "nope", "polarity": 1}])
    assert bt2["summary"]["n"] == 0


def test_changes_shape_and_care_tagging():
    chart = vedic.compute_chart(dt.datetime(1990, 5, 15, 8, 30), 28.6139, 77.2090, "Asia/Kolkata")
    m = matrix.build(chart)
    ch = matrix.changes(chart, m)
    assert set(ch) >= {"health", "wealthCareer", "relationships", "note"}
    dirs, care_keys = set(), set()
    for g in ("health", "wealthCareer", "relationships"):
        for e in ch[g]:
            assert e["from"] <= e["to"]
            assert 0.35 <= e["cf"] <= 0.92
            assert e["direction"] in ("up", "down", "shift", "care")
            dirs.add(e["direction"])
            if e["care"]:
                care_keys.add(e["key"])
    # every care-signal must be one of the two designated (opt-in) keys, marked care.
    assert care_keys <= {"rel.trust", "rel.tender"}
    for g in ("health", "wealthCareer", "relationships"):
        for e in ch[g]:
            if e["direction"] == "care":
                assert e["care"] is True


def test_lifearc_shape_and_turning_points():
    chart = vedic.compute_chart(dt.datetime(1990, 5, 15, 8, 30), 28.6139, 77.2090, "Asia/Kolkata")
    m = matrix.build(chart)
    la = matrix.lifearc(chart, m)
    assert la["birthYear"] == 1990 and len(la["points"]) >= 30
    facets = set(matrix._FACETS)
    for p in la["points"]:
        assert set(p["facets"]) == facets
        assert all(-1.0 <= v <= 1.0 for v in p["facets"].values())
        assert p["age"] == p["year"] - la["birthYear"]
    # ribbon covers the whole span contiguously
    assert la["ribbon"][0]["from"] == la["birthYear"]
    for t in la["turningPoints"]:
        assert t["direction"] in ("rise", "hard", "yoga")
        assert t["kind"] in ("curve", "yoga")


def test_changes_transit_planets_include_fast_movers():
    # Mars + nodes must be in the trigger set (phase-A faster transits).
    assert "mars" in matrix._TRIGGER_PLANETS
    assert "rahu" in matrix._TRIGGER_PLANETS
    # no signature triggers ingress on a fast graha (Sun/Moon/Mercury/Venus).
    fast = {"sun", "moon", "mercury", "venus"}
    for sig in matrix.CHANGE_SIGS:
        assert not (fast & set(sig.get("planets", []))), sig["key"]
