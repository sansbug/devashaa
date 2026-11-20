"""Hit-rate harness for the study view: does a rule fire on the right events
more often than it does by chance?  NO DATA IS BUNDLED: the subject file is
assembled only after the owner approves the plan in docs/study-plan.md.

Input (JSON, kept OUTSIDE the public repo):
  {"subjects": [{"id", "birth": {date, time, latitude, longitude, timezone},
                 "rating": "AA"|"A",            # Rodden rating; nothing below A
                 "birth_source": "<url or record>",
                 "events": [{"date": "YYYY-MM-DD", "category": "<code>",
                             "polarity": "favourable"|"adverse",
                             "source": "<url>"}]}]}
  Event categories are coded from the public record BEFORE any chart is cast.
  Death, lifespan and a partner's fidelity are never categories (CLAUDE.md rule 2).

A rule here is a TIMING rule that has a state on a given date:
  gochara:<graha>   Phaladipika ch.26: the graha's transit from the natal Moon is
                    favourable / obstructed / not favourable on that date.
  dasha:maha        BPHS Vol II ch.47 vv.5-6: the running maha-dasha lord's verdict.
  dasha:antar       the same verdict for the running antar-dasha lord.
A rule "hits" an event when its state agrees with the event's polarity
(favourable <-> favourable; adverse <-> obstructed / not favourable / adverse).

Two controls, both reported, never merged:
  within   the same subject, N random dates inside the same span of life;
  swapped  the same event dates, read against OTHER subjects' charts.
Reported per rule: hits/n, the control rate, the difference, a Wilson 95% interval
and a two-sided permutation p, then a Benjamini-Hochberg adjustment over all rules.
No pooled score across rules.
"""

from __future__ import annotations

import datetime as dt
import json
import math
import random
import sys

import vedic
import gochara_rules
from app import app

GRAHAS9 = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "rahu", "ketu")
FORBIDDEN_CATEGORIES = {"death", "lifespan", "bereavement", "fidelity", "longevity"}


def _chart(birth):
    r = app.test_client().post("/api/chart", json=birth)
    if r.status_code != 200:
        raise ValueError(r.get_data(as_text=True)[:200])
    return r.get_json()


def _running(dasha, date: str, level: int):
    days = str(dasha.get("default_year_days", 365.25)).split(".")[0]
    v = (dasha.get("variants") or {}).get("365" if days == "365" else days) \
        or next(iter((dasha.get("variants") or {}).values()), {})
    nodes = v.get("mahadashas") or []
    lord = None
    for _ in range(level + 1):
        hit = next((n for n in nodes if n["start"][:10] <= date < n["end"][:10]), None)
        if not hit:
            return None
        lord, nodes = hit["lord"], hit.get("sub") or []
    return lord


def states_on(chart, birth, date: str) -> dict:
    """Each timing rule's state on `date` for one natal chart."""
    out = {}
    moon = next(g for g in chart["grahas"] if g["key"] == "moon")
    t = vedic.compute_chart(local_dt=dt.datetime.fromisoformat(date + "T12:00"),
                            latitude=float(birth["latitude"]), longitude=float(birth["longitude"]),
                            tz_name=chart.get("timezone") or "UTC")
    hfm = {g.key: (g.rasi - moon["rasi"]) % 12 + 1 for g in t.grahas}
    occ = {}
    for k, h in hfm.items():
        occ.setdefault(h, []).append(k)
    for k in GRAHAS9:
        j = gochara_rules.transit_judgment(k, hfm[k], occ)
        if j and j.get("status"):
            out[f"gochara:{k}"] = j["status"]
    verdicts = (chart.get("dasha") or {}).get("verdicts") or {}
    for name, lvl in (("dasha:maha", 0), ("dasha:antar", 1)):
        lord = _running(chart.get("dasha") or {}, date, lvl)
        vd = verdicts.get(lord) if lord else None
        if vd and not vd.get("silent") and vd.get("state") in ("favourable", "adverse"):
            out[name] = vd["state"]
    return out


def _agrees(state, polarity):
    return (state == "favourable") == (polarity == "favourable")


def wilson(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(c - h, 4), round(c + h, 4))


def perm_p(obs_hits, obs_n, ctrl_flags, iters=5000, rng=None):
    """Two-sided: how often a draw of obs_n control outcomes lands as far from the
    control rate as the observed hit count."""
    rng = rng or random.Random(7)
    if obs_n == 0 or not ctrl_flags:
        return None
    base = sum(ctrl_flags) / len(ctrl_flags)
    obs = abs(obs_hits / obs_n - base)
    ge = sum(1 for _ in range(iters)
             if abs(sum(rng.choice(ctrl_flags) for _ in range(obs_n)) / obs_n - base) >= obs - 1e-12)
    return (ge + 1) / (iters + 1)


def bh(pvals: dict) -> dict:
    items = sorted(((p, k) for k, p in pvals.items() if p is not None))
    m, out, prev = len(items), {}, 1.0
    for i, (p, k) in reversed(list(enumerate(items, 1))):
        prev = min(prev, p * m / i)
        out[k] = round(prev, 4)
    return out


def run(subjects, within_n=20, seed=7):
    rng = random.Random(seed)
    charts = {s["id"]: _chart(s["birth"]) for s in subjects}
    obs, within, swapped = {}, {}, {}
    for s in subjects:
        assert s.get("rating") in ("AA", "A"), f"{s['id']}: rating below A is not used"
        for ev in s["events"]:
            assert ev["category"] not in FORBIDDEN_CATEGORIES, ev["category"]
            for rule, st in states_on(charts[s["id"]], s["birth"], ev["date"]).items():
                obs.setdefault(rule, []).append(_agrees(st, ev["polarity"]))
            # within-subject control: random dates in the same span of life
            b = dt.date.fromisoformat(s["birth"]["date"])
            last = max(dt.date.fromisoformat(e["date"]) for e in s["events"])
            for _ in range(within_n):
                d = b + dt.timedelta(days=rng.randint(365 * 5, max(365 * 5 + 1, (last - b).days)))
                for rule, st in states_on(charts[s["id"]], s["birth"], d.isoformat()).items():
                    within.setdefault(rule, []).append(_agrees(st, ev["polarity"]))
            # swapped control: the same date on other subjects' charts
            for o in subjects:
                if o["id"] == s["id"] or o["birth"]["date"] >= ev["date"]:
                    continue
                for rule, st in states_on(charts[o["id"]], o["birth"], ev["date"]).items():
                    swapped.setdefault(rule, []).append(_agrees(st, ev["polarity"]))
    report, pw, ps = [], {}, {}
    for rule, flags in sorted(obs.items()):
        k, n = sum(flags), len(flags)
        row = {"rule": rule, "hits": k, "n": n, "rate": round(k / n, 4), "ci95": wilson(k, n)}
        for name, ctrl, pd in (("within", within, pw), ("swapped", swapped, ps)):
            c = ctrl.get(rule) or []
            row[name] = {"rate": round(sum(c) / len(c), 4) if c else None, "n": len(c),
                         "diff": round(k / n - sum(c) / len(c), 4) if c else None}
            pd[rule] = perm_p(k, n, [int(x) for x in c], rng=rng)
            row[name]["p"] = None if pd[rule] is None else round(pd[rule], 4)
        report.append(row)
    qw, qs = bh(pw), bh(ps)
    for row in report:
        row["within"]["q_bh"] = qw.get(row["rule"])
        row["swapped"]["q_bh"] = qs.get(row["rule"])
    return {"rules": report, "subjects": len(subjects),
            "events": sum(len(s["events"]) for s in subjects),
            "note": ("Each rule is reported alone, beside both controls. A small n is shown as it "
                     "is; nothing is pooled across rules and nothing is re-run to find a better seed.")}


if __name__ == "__main__":
    data = json.load(open(sys.argv[1], encoding="utf-8"))
    json.dump(run(data["subjects"]), sys.stdout, indent=1)
