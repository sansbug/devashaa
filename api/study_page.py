"""Write the study view as one local HTML page (owner's study, not a site page).

    cd api && PYTHONUTF8=1 ../.venv/Scripts/python.exe study_page.py OUT.html \
        --date 1975-06-25 --time 22:30 --lat 26.46523 --lon 80.34975 --tz Asia/Kolkata \
        [--transit 2026-11-19] [--show-sensitive]

Section 1 is the gap map; section 2 is the chart's ledger grouped by division,
then by axis; section 3 is what the texts are silent on for this chart.
Nothing leaves the machine.
"""

from __future__ import annotations

import argparse
import html
import re

import study
from app import app

RASI = ["Mesh", "Vrishabh", "Mithun", "Kark", "Simha", "Kanya",
        "Tula", "Vrishchik", "Dhanu", "Makar", "Kumbh", "Meen"]
TIER_CSS = {"sloka": "#7a4b00", "classical": "#174f86", "modern": "#5b5b5b",
            "traditional": "#2d6a3e", "synthesis": "#8a1c1c"}


def e(x):
    return html.escape("" if x is None else str(x))


def _factors(f):
    out = []
    if "graha" in f: out.append(f["graha"].capitalize())
    if f.get("rashi") is not None: out.append(RASI[f["rashi"]])
    if f.get("bhaav") is not None: out.append(f"Bhaav {f['bhaav']}")
    if f.get("nakshatra") is not None: out.append(f"Nakshatr {f['nakshatra']}")
    if f.get("degree") is not None: out.append(f"{f['degree']:.2f}°")
    return " · ".join(out)


def render(gaps, led, title):
    p = [f"<!doctype html><meta charset=utf-8><title>{e(title)}</title><style>"
         "body{font:14px/1.45 system-ui,sans-serif;margin:24px;max-width:1100px;color:#222;background:#fff}"
         "table{border-collapse:collapse;width:100%;margin:8px 0 20px}td,th{border:1px solid #ddd;padding:4px 6px;vertical-align:top;text-align:left}"
         "th{background:#f4f1ea}.t{color:#fff;border-radius:3px;padding:0 5px;font-size:12px}"
         ".silent{color:#8a1c1c}.covered{color:#2d6a3e}.partial,.listed{color:#7a4b00}.muted{color:#777}"
         "h2{margin-top:32px}</style>",
         f"<h1>{e(title)}</h1>",
         "<p class=muted>Every line is one source's cited reading. Lines are never added, netted or ranked. "
         "A blank cell means the registered texts are silent.</p>",
         "<h2>1. Gap map</h2><table><tr><th>Relation</th><th>Status</th><th>Cells</th><th>Registered sources (cells each)</th><th>Leads on hand (unverified)</th></tr>"]
    for r in gaps["axes"]:
        srcs = "<br>".join(f"<span class=t style='background:{TIER_CSS.get(s['tier'], '#444')}'>{e(s['tier'])}</span> "
                           f"{e(s['source'])}: {s['cells']}" + (f" <span class=muted>{e(s.get('note'))}</span>" if s.get("note") else "")
                           for s in r["sources"]) or "—"
        p.append(f"<tr><td>{e(r['axis'])}<div class=muted>{e(r.get('note'))}</div></td>"
                 f"<td class={r['status']}>{r['status']}</td><td>{e(r['possible'] or 'n/a')}</td>"
                 f"<td>{srcs}</td><td class=muted>{'<br>'.join(e(c) for c in r['candidates'])}</td></tr>")
    p.append("</table><p class=muted>" + e(gaps["note"]) + "</p>")

    p.append("<h2>2. What fires in this chart</h2>")
    c = led["counts"]
    p.append(f"<p>{c['rows']} cited lines · {c['silences']} silences · "
             f"{c['sensitive_withheld']} sensitive passages withheld.</p>")
    if led.get("uses"):
        p.append("<h3>What each division is read for</h3><table><tr><th>Division</th><th>Topic</th>"
                 "<th>The translation's words</th></tr>")
        for v, u in led["uses"].items():
            p.append(f"<tr><td>{v}</td><td>{e(u['topic'])}</td><td class=muted>{e(u['words'])}</td></tr>")
        p.append(f"</table><p class=muted>{e(next(iter(led['uses'].values()))['citation'])}</p>")
    order = study.VARGAS + ("D1-D60",)
    for v in order:
        rows = [r for r in led["rows"] if r["varga"] == v]
        if not rows:
            continue
        p.append(f"<h3>{v}</h3><table><tr><th>Relation</th><th>Factors</th><th>Source</th><th>Text</th></tr>")
        for r in sorted(rows, key=lambda r: (r["transit"], r["axis"])):
            txt = e(r["text"]) if r["text"] is not None else "<i class=muted>Sensitive passage, withheld. Ask to show it.</i>"
            extra = ""
            if r.get("polarity"): extra += f" <b>[{e(r['polarity'])}]</b>"
            if r.get("why"):
                why = re.sub(r"\{g:(\w+)\}", lambda m: m.group(1).capitalize(), r["why"])
                extra += f"<div class=muted>Why: {e(why)}</div>"
            if r.get("yoga"): extra = f"<b>{e(r['yoga'])}</b>: " + extra
            p.append(f"<tr><td>{e(r['axis'])}{' (transit)' if r['transit'] else ''}</td>"
                     f"<td>{e(_factors(r['factors']))}</td>"
                     f"<td><span class=t style='background:{TIER_CSS.get(r['tier'], '#444')}'>{e(r['tier'])}</span> "
                     f"{e(r['source'])}<div class=muted>{e(r['citation'])}"
                     f"{' · ' + e(r['confidence']) if r.get('confidence') else ''}</div></td>"
                     f"<td>{extra}{txt}</td></tr>")
        p.append("</table>")

    p.append("<h2>3. Where the texts are silent for this chart</h2><table><tr><th>Relation</th><th>Division</th><th>Chart has</th><th>Reason</th></tr>")
    for s in led["silences"]:
        f = s["factors"]
        if "placements" in f:
            has = ", ".join(f"{k.capitalize()} {RASI[x]}" for k, x in f["placements"].items() if x is not None)
            if f.get("own_sign"):
                has += f" <b>(own sign: {e(', '.join(f['own_sign']))})</b>"
        else:
            has = e(_factors(f) if f else "")
        p.append(f"<tr><td>{e(s['axis'])}</td><td>{e(s['varga'])}</td><td>{has}</td><td class=muted>{e(s['reason'])}</td></tr>")
    p.append("</table>")
    return "".join(p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--date", required=True); ap.add_argument("--time", required=True)
    ap.add_argument("--lat", type=float, required=True); ap.add_argument("--lon", type=float, required=True)
    ap.add_argument("--tz"); ap.add_argument("--transit"); ap.add_argument("--name", default="Study chart")
    ap.add_argument("--show-sensitive", action="store_true")
    a = ap.parse_args()
    body = {"date": a.date, "time": a.time, "latitude": a.lat, "longitude": a.lon,
            "show_sensitive": a.show_sensitive}
    if a.tz: body["timezone"] = a.tz
    if a.transit: body["transit_date"] = a.transit
    r = app.test_client().post("/api/study", json=body)
    if r.status_code != 200:
        raise SystemExit(r.get_data(as_text=True))
    gaps = app.test_client().get("/api/study/gaps").get_json()
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(render(gaps, r.get_json(), a.name))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
