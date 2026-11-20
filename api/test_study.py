"""study.py: the gap map and the per-chart ledger keep the site's rules.

Run by import (there is no pytest in the venv):
    cd api && PYTHONUTF8=1 ../.venv/Scripts/python.exe -c "import test_study as T; [getattr(T,n)() for n in dir(T) if n.startswith('test_')]; print('ok')"
"""

import json
import os
import re

import study
from app import app

BIRTH = {"date": "1975-06-25", "time": "22:30", "latitude": 26.46523,
         "longitude": 80.34975, "timezone": "Asia/Kolkata"}
FORBIDDEN = re.compile(r'"(score|net|total_score|composite|verdict_overall|weighted)"')


def _post(extra=None):
    r = app.test_client().post("/api/study", json={**BIRTH, **(extra or {})})
    assert r.status_code == 200, r.get_data(as_text=True)[:300]
    return r.get_json()


def test_gap_map_counts_come_from_the_corpora():
    g = study.gap_map()
    axes = {r["axis"]: r for r in g["axes"]}
    assert axes["graha x nakshatra"]["status"] == "partial"           # the Moon only (BJ ch.16)
    assert [s["cells"] for s in axes["graha x nakshatra"]["sources"]] == [20]
    assert axes["graha x rashi (D60)"]["status"] == "silent"
    # D9 has only a modern-tier reading: never reported as classical coverage
    assert {s["tier"] for s in axes["graha x rashi (D9)"]["sources"]} == {"modern"}
    import saravali_rules as sv
    sv_cells = next(s["cells"] for s in axes["graha x rashi (D1)"]["sources"] if s["source"] == "saravali")
    assert sv_cells == sum(len(v) for v in sv.IN_SIGN.values())
    # a candidate is a lead, never a source
    for r in g["axes"]:
        assert all(c.split(" ")[0] in study.CAND for c in r["candidates"]), r["axis"]


def test_every_row_has_one_source_one_tier_and_a_locus():
    L = _post({"transit_date": "2026-11-19"})
    assert L["rows"]
    for r in L["rows"]:
        assert r["source"] and r["tier"] and r["citation"], r
        assert isinstance(r["tier"], str)
    assert any(r["transit"] for r in L["rows"])


def test_no_composite_anywhere():
    for obj in (study.gap_map(), _post({"transit_date": "2026-11-19"})):
        assert not FORBIDDEN.search(json.dumps(obj)), FORBIDDEN.search(json.dumps(obj))


def test_every_division_is_answered_or_refused():
    L = _post()
    answered = {s["varga"] for s in L["silences"]} | {r["varga"] for r in L["rows"]}
    for v in study.VARGAS:
        assert v in answered, v


def test_sensitive_text_is_withheld_unless_asked():
    hidden = _post()
    shown = _post({"show_sensitive": True})
    for r in hidden["rows"]:
        if r["sensitive"]:
            assert r["text"] is None
    assert sum(1 for r in shown["rows"] if r["sensitive"] and r["text"]) == \
        sum(1 for r in hidden["rows"] if r["sensitive"])


def test_sensitive_pattern_matches_the_web_one():
    js = open(os.path.join(os.path.dirname(__file__), "..", "web", "src", "findings.js"),
              encoding="utf-8").read()
    en = re.search(r"^\s*en: /(.*)/i,\s*$", js, re.M).group(1)
    hi = re.search(r"^\s*hi: /(.*)/,\s*$", js, re.M).group(1)
    assert en == study.SENSITIVE_EN.pattern, "findings.js SENSITIVE.en changed: update study.py"
    assert hi == study.SENSITIVE_HI.pattern, "findings.js SENSITIVE.hi changed: update study.py"
