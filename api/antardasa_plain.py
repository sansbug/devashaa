"""
A sub-period's results in plain form, for the simple view — which BRANCHES of the
text's antardaśā section (BPHS Vol II chs 52-60) this chart meets, with the
results the text lists for each.

It stands on antardasa.evaluate_cell (the condition-firing engine) and adds three
things that engine deliberately leaves out of its raw output:

  1. BRANCHES. The corpus stores one condition per row and marks the rows that
     share a result list "as above (same branch)". A branch here is a row with
     its own result list plus the rows that point back to it. A row marked as a
     REQUIRED conjunct ("joined by 'and'") must be met as well; the others are
     alternatives. A branch APPLIES only when an alternative is met and every
     required conjunct is met. If a required conjunct cannot be evaluated the
     branch is UNDETERMINED and is not shown as applying.
  2. SIGN DIGNITY. The engine marks every non-house condition unavailable. The
     four plain dignity conditions — "in his sign of exaltation", "in his own
     sign", "in his moolatrikona", "in his sign of debilitation" — are testable
     from the chart (dignity.dignity_of, ch.3), so they are tested here. Nothing
     else is: navāṁśa, aspect, association, strength and combustion conditions
     stay unevaluated, and so does every condition for Rāhu and Ketu's dignity
     (the text gives the nodes none).
  3. The text's back-references are followed (explain._resolve_results), so a
     branch carries its actual result list rather than "as above".

Left out on purpose: the māraka (death) clause of a cell and its remedy — the
site neither dates a death nor prescribes a remedy. The count of clauses left
out is reported.

There is still NO VERDICT: the text labels few branches and does not say how a
sub-period's results combine with the main period's. A branch's own valence word,
where the text has one, travels beside it as the text's word, not as a judgement.
"""
from __future__ import annotations

import re

import antardasa
from dignity import dignity_of
from explain import _resolve_results

RASI_LORD = ["mars", "venus", "mercury", "moon", "sun", "mercury",
             "venus", "mars", "jupiter", "saturn", "saturn", "jupiter"]
_XREF = re.compile(r"^\s*(as above|same)", re.I)

# plain dignity predicates → a test on (state, sign-lord-is-self)
_DIGNITY = [
    (re.compile(r"^in his (sign of exaltation|exaltation sign|exalted sign)$"), lambda st, own: st == "exalted"),
    (re.compile(r"^in his own sign$"), lambda st, own: own),
    (re.compile(r"^in his moolatrikona( sign)?$"), lambda st, own: st == "moolatrikona"),
    (re.compile(r"^in his (sign of debilitation|debilitation sign)$"), lambda st, own: st == "debilitated"),
]


def _dignity_test(predicate: str, graha: str, pos: dict):
    """True / False for a plain dignity predicate, None when it is not one (or not testable)."""
    if graha in ("rahu", "ketu"):
        return None
    p = (predicate or "").strip().lower().rstrip(".;,")
    for rx, test in _DIGNITY:
        if rx.match(p):
            lon = pos.get("longitude")
            if lon is None:
                return None
            try:
                st = (dignity_of(graha, lon) or {}).get("state")
            except Exception:  # noqa: BLE001
                return None
            return bool(test(st, RASI_LORD[pos["rasi"]] == graha))
    return None


def plain_cell(maha: str, antar: str, positions: dict, lagna: int) -> dict | None:
    """`positions`: graha -> {"rasi": int, "longitude": float}."""
    rasi = {g: p["rasi"] for g, p in positions.items()}
    cell = antardasa.evaluate_cell(maha, antar, positions=rasi, lagna=lagna)
    if cell is None:
        return None

    # 1. each row: met / not met / not evaluated — and why
    rows, withheld = [], 0
    for cond in cell["conditions"]:
        pred = cond.get("predicate") or ""
        if "maraka" in pred.lower():
            withheld += 1
            continue
        state, how = cond["state"], "house"
        if state == antardasa.UNAVAILABLE and cond.get("frame") == "not_a_house":
            t = _dignity_test(pred, antar, positions.get(antar) or {})
            if t is not None:
                state, how = (antardasa.FIRED if t else antardasa.NOT_FIRED), "dignity"
        raw = (cond.get("results") or "").strip()
        rows.append({
            "predicate": pred, "state": state, "how": how,
            "own_results": bool(raw) and not _XREF.match(raw),
            "required": "REQUIRED" in raw,
            "results": _resolve_results(cell, cond),
            "polarity": cond.get("polarity") or "none",
            "polarity_word": cond.get("polarity_word") or "",
        })

    # 2. group into branches: a row with its own result list opens one
    branches, cur = [], None
    for r in rows:
        if r["own_results"] or cur is None:
            cur = {"results": r["results"], "polarity": r["polarity"], "polarity_word": r["polarity_word"], "rows": []}
            branches.append(cur)
        cur["rows"].append(r)

    applies, undetermined, not_met = [], 0, 0
    for b in branches:
        alts = [r for r in b["rows"] if not r["required"]]
        reqs = [r for r in b["rows"] if r["required"]]
        alt_met = [r for r in alts if r["state"] == antardasa.FIRED]
        req_states = [r["state"] for r in reqs]
        if alt_met and all(s == antardasa.FIRED for s in req_states) and b["results"]:
            applies.append({
                "results": b["results"], "polarity": b["polarity"], "polarity_word": b["polarity_word"],
                "met": [{"predicate": r["predicate"], "how": r["how"]} for r in alt_met + reqs],
            })
        elif (alt_met and any(s == antardasa.UNAVAILABLE for s in req_states)) or \
                (not alt_met and any(r["state"] == antardasa.UNAVAILABLE for r in alts)):
            undetermined += 1
        else:
            not_met += 1

    return {
        "maha_lord": maha, "antar_lord": antar,
        "citation": f"{cell['chapter']} vv.{cell['verses']}",
        "applies": applies,
        "counts": {"branches": len(branches), "apply": len(applies), "undetermined": undetermined,
                   "not_met": not_met, "clauses_left_out": withheld},
        "no_verdict": cell["no_verdict"],
    }
