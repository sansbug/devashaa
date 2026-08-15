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


def test_double_transit_hits_only_full_aspects():
    # The strict double-transit 'hit' is occupation or a FULL aspect, never a
    # Parāśari ¼/½/¾ partial. Saturn's full aspects are its 3rd/7th/10th.
    assert matrix._hits(9, 9, "saturn")               # occupation
    assert matrix._hits(9, 11, "saturn")              # 3rd  (full)
    assert matrix._hits(9, 3, "saturn")               # 7th  (full)
    assert matrix._hits(9, 6, "saturn")               # 10th (full)
    assert not matrix._hits(9, 10, "saturn")          # 2nd  (¼ partial — not a hit)
    # Jupiter's full aspects are its 5th/7th/9th.
    assert matrix._hits(0, 4, "jupiter") and matrix._hits(0, 6, "jupiter") and matrix._hits(0, 8, "jupiter")
    assert not matrix._hits(0, 2, "jupiter")          # 3rd (partial for Jupiter)


def test_double_transit_coverage_grades():
    # lagna=0, house=1 -> bhāva sign 0; lord Mars natal @ sign 2; kāraka of 1st = Sun (absent here).
    gs = {"mars": 2}
    # Jup@8 fully aspects 0 (5th) & 2 (7th); Sat@10 fully aspects 0 (3rd) but NOT 2 -> 1 of 2 covered.
    assert abs(matrix._dt_coverage(8, 10, 1, 0, "mars", gs) - 0.5) < 1e-9
    # No coverage when neither target is doubly hit.
    assert matrix._dt_coverage(3, 5, 1, 0, "mars", gs) == 0.0
    # Full when both planets occupy/fully-aspect every target.
    full = matrix._dt_coverage(0, 6, 1, 0, "mars", {"mars": 6})
    assert full == 1.0


def test_changes_can_emit_doubletransit_trigger():
    # The user's own chart raises a strict full three-target double transit on a
    # relationship house (7th) — a textbook marriage-timing yoga.
    chart = vedic.compute_chart(dt.datetime(1975, 6, 25, 22, 32), 26.4499, 80.3319, "Asia/Kolkata")
    m = matrix.build(chart)
    ch = matrix.changes(chart, m)
    types = {e["triggerType"] for g in ("health", "wealthCareer", "relationships") for e in ch[g]}
    assert "doubletransit" in types
    # every sig carrying the trigger only ever grades it 2/3+ (the strict gate).
    dt_sigs = [s for s in matrix.CHANGE_SIGS if "doubletransit" in s["triggers"]]
    assert dt_sigs and all("doubletransit" in s["triggers"] for s in dt_sigs)
