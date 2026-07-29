"""Planetary motion (gati) + combustion.

Run: python api/test_motion.py

Validates the ephemeris facts on a REAL chart (speeds in astronomical range,
direction matches sign, nodes always retrograde, Sun/Moon never retrograde),
the synthetic classification edge cases (stationary / slow / swift / combust),
and the provenance discipline (facts vs traditional labels; Cheṣṭā bala refused;
combustion orbs marked out-of-BPHS with the retrograde column uncertain).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import motion as mo

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


print("Mean daily motions match 360 / period (superior) or the Sun's rate:")
import math
EXPECT = {"sun": 360 / 365.2422, "moon": 360 / 27.32158, "mars": 360 / 686.980,
          "mercury": 360 / 365.2422, "jupiter": 360 / 4332.589, "venus": 360 / 365.2422,
          "saturn": 360 / 10759.22, "rahu": 360 / 6798.383, "ketu": 360 / 6798.383}
for k, v in EXPECT.items():
    check(f"mean[{k}] ≈ {v:.4f}", abs(mo.MEAN_DAILY[k] - v) < 0.01, str(mo.MEAN_DAILY[k]))

print("\nOn a real chart the motion facts hold (1985-07-13 Varanasi):")
from vedic import compute_chart
from datetime import datetime
r = compute_chart(local_dt=datetime(1985, 7, 13, 14, 30), latitude=25.3176,
                  longitude=82.9739, tz_name="Asia/Kolkata", name="t")
grahas = [{"key": g.key, "longitude": g.longitude, "speed": g.speed} for g in r.grahas]
res = mo.motion_analysis(grahas)
rows = {row["key"]: row for row in res["grahas"]}
RANGE = {"sun": (0.95, 1.03), "moon": (11.7, 15.4), "mars": (-0.45, 0.85),
         "mercury": (-1.6, 2.3), "jupiter": (-0.15, 0.25), "venus": (-0.7, 1.3),
         "saturn": (-0.09, 0.14), "rahu": (-0.09, 0.0), "ketu": (-0.09, 0.0)}
for k, (lo, hi) in RANGE.items():
    sp = rows[k]["motion"]["speed"]
    check(f"{k:<8} speed {sp:+.4f} in astronomical range", lo <= sp <= hi)
check("direction matches the sign of speed for every graha",
      all((row["motion"]["retrograde"]) == (row["motion"]["speed"] < 0) for row in res["grahas"]))
check("the Sun is never retrograde", not rows["sun"]["motion"]["retrograde"])
check("the Moon is never retrograde and never stationary",
      not rows["moon"]["motion"]["retrograde"] and not rows["moon"]["motion"]["stationary"])
check("both nodes are retrograde 'by definition' (mean node)",
      all(rows[n]["motion"]["retrograde"] and "definition" in rows[n]["motion"]["gati"]["en"]
          for n in ("rahu", "ketu")))
check("ratio = |speed| / mean for every graha",
      all(abs(row["motion"]["ratio"] - abs(row["motion"]["speed"]) / row["motion"]["mean"]) < 0.01
          for row in res["grahas"]))
check("combustion separation is in 0–180° where it applies",
      all(0 <= row["combustion"]["separation"] <= 180
          for row in res["grahas"] if row["combustion"]["applies"]))

print("\nThe classification bands land where they should (synthetic):")
def state(key, speed):
    return mo._motion_state(key, speed)
check("Mars at 0.05°/day is near-stationary (vikala), not slow",
      state("mars", 0.05)["stationary"] and state("mars", 0.05)["gati"]["iast"] == "vikala")
check("Mercury at 0.50°/day is slow (manda)",
      state("mercury", 0.50)["gati"]["iast"] == "manda" and state("mercury", 0.50)["pace"] == "slow")
check("the Moon at 15.0°/day is swift (atichāra)",
      state("moon", 15.0)["gati"]["iast"] == "atichāra" and state("moon", 15.0)["pace"] == "swift")
check("the Sun at 0.986°/day is average (sama)",
      state("sun", 0.986)["gati"]["iast"] == "sama")
check("a fully-retrograde speed (well above its station) is vakra",
      state("saturn", -0.03)["gati"]["iast"] == "vakra" and state("saturn", -0.03)["retrograde"])
check("a graha near a RETROGRADE station is stationary (vikala) — the fact holds on both sides",
      state("mars", -0.01)["stationary"] and state("mars", -0.01)["gati"]["iast"] == "vikala"
      and state("mars", -0.01)["retrograde"])
check("the near-stationary fact straddles the 0.15 band (Mercury 0.14→vikala, 0.16→manda)",
      state("mercury", 0.14)["stationary"] and not state("mercury", 0.16)["stationary"]
      and state("mercury", 0.16)["gati"]["iast"] == "manda")
check("every gati label carries its own traditional tier",
      all(row["motion"]["gati"]["tier"] == "traditional" for row in res["grahas"]))

print("\nCombustion: fact + traditional verdict, Sun/nodes excluded, retro uncertain:")
def comb(key, lon, sun_lon, retro):
    return mo._combustion(key, lon, sun_lon, retro)
check("the Sun has no combustion (it is the source)",
      comb("sun", 100, 100, False)["applies"] is False)
check("Rāhu/Ketu have no combustion (shadow points)",
      comb("rahu", 100, 100, False)["applies"] is False)
check("a planet within its orb of the Sun is combust",
      comb("mercury", 105, 100, False)["combust"] is True
      and comb("mercury", 105, 100, False)["separation"] == 5.0)
check("a planet beyond its orb is not combust",
      comb("jupiter", 130, 100, False)["combust"] is False)
mercRetro = comb("mercury", 108, 100, True)
check("a RETROGRADE Mercury combustion uses the OCR-damaged retro orb (12°) & is uncertain",
      mercRetro["orb"] == 12.0 and mercRetro["confidence"] == "uncertain"
      and "OCR-damaged" in mercRetro["note"])
venRetro = comb("venus", 106, 100, True)
check("a RETROGRADE Venus combustion uses the retro orb (8°) & is uncertain",
      venRetro["orb"] == 8.0 and venRetro["combust"] is True and venRetro["confidence"] == "uncertain")
check("every combustion verdict is traditional and carries the 'no fixed orb' BPHS note",
      all("no fixed orb" in row["combustion"].get("note", "")
          and row["combustion"].get("tier") == "traditional"
          for row in res["grahas"] if row["combustion"]["applies"]))

print("\nProvenance: Cheṣṭā bala refused; nothing claims BPHS orbs:")
cb = res["cheshta_bala"]
check("Cheṣṭā bala is unavailable and names the Seeghrocha as the reason",
      cb["available"] is False and "Seeghrocha" in cb["reason"])
check("the combustion note says BPHS gives no fixed orb (rule-of-three instead)",
      all("ch.7 vv.28-29" in row["combustion"].get("note", "")
          for row in res["grahas"] if row["combustion"]["applies"]))
check("no combustion note claims the orbs ARE BPHS/Parāśara doctrine",
      not any("Parāśara's orb" in row["combustion"].get("note", "")
              for row in res["grahas"] if row["combustion"]["applies"]))
check("the tier legend names facts vs traditional",
      "fact" in res["tiers"] and "traditional" in res["tiers"])

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
