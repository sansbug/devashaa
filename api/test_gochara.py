"""Gochara (transit) geometry.

Run: python api/test_gochara.py

Validates the whole-sign counts (house-from-Moon / house-from-lagna, including
wrap-around), conjunction detection, transit graha dṛṣṭi to natal points (7th and
the special 3/10, 4/8, 5/9 aspects), the node refusal (nodes transit and are
conjoined but cast no aspect), and returns (a transit over its own natal point),
on a controlled synthetic chart — then runs the whole thing on a REAL chart end
to end and checks the output is astronomically sane.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gochara
from gochara import _house, _signed_arc

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


def g(key, rasi, deg, speed=1.0, retro=False):
    return {"key": key, "longitude": rasi * 30 + deg, "rasi": rasi,
            "degree": int(deg), "minute": 0, "second": 0,
            "nakshatra": None, "retrograde": retro, "speed": speed}


print("Whole-sign house counts (1 = same sign), incl. wrap-around:")
check("same sign is house 1", _house(0, 0) == 1)
check("next sign is house 2", _house(0, 1) == 2)
check("wrap 11 -> 0 is house 2", _house(11, 0) == 2, f"got {_house(11, 0)}")
check("wrap 0 -> 11 is house 12", _house(0, 11) == 12, f"got {_house(0, 11)}")
check("7th opposite", _house(3, 9) == 7)

print("\nSigned shortest arc:")
check("arc 5.5 - 5.0 = 0.5", abs(_signed_arc(5.5, 5.0) - 0.5) < 1e-9)
check("arc wraps to negative side", abs(_signed_arc(1.0, 359.0) - 2.0) < 1e-9,
      f"got {_signed_arc(1.0, 359.0)}")

# ---- controlled synthetic scenario -----------------------------------------
# Natal: Moon in Aries(0), lagna Cancer(3). Points placed to sit on each of
# Saturn's aspect houses from Aries.
natal = [
    g("moon", 0, 5.0),        # transit Saturn will conjoin this
    g("sun", 2, 5.0),         # Gemini — 3rd from Aries (Saturn's special full aspect)
    g("venus", 4, 5.0),       # Leo — 5th from Aries (general ½ aspect for everyone)
    g("mars", 6, 6.0),        # Libra — 7th from Aries (the universal full aspect)
    g("jupiter", 9, 5.0),     # Capricorn — 10th from Aries (Saturn special) + return target
    g("rahu", 10, 5.0),       # Aquarius — 11th from Aries (NO graha dṛṣṭi reaches it)
    g("saturn", 8, 20.0),     # Sagittarius — unrelated natal Saturn
]
natal_lagna = 3

transit = [
    g("saturn", 0, 5.5, speed=0.03),   # Aries — conjunct natal Moon
    g("jupiter", 9, 5.8, speed=0.2),   # Capricorn 5°48' — over natal Jupiter (return)
    g("sun", 5, 5.0),                  # Virgo — needed so combustion has a Sun
    g("mercury", 3, 10.0),             # Cancer = the lagna sign — conjoins the lagna
    g("rahu", 0, 8.0, speed=-0.05, retro=True),  # Aries — node, transits but casts nothing
]

res = gochara.transit_geometry(natal, natal_lagna, transit, transit_utc="TEST")
by_key = {r["key"]: r for r in res["grahas"]}

print("\nReference anchors are the natal Moon and lagna:")
check("moon_rasi = 0", res["reference"]["moon_rasi"] == 0)
check("lagna_rasi = 3", res["reference"]["lagna_rasi"] == 3)

sat = by_key["saturn"]
print("\nTransit Saturn in Aries against the natal chart:")
check("house-from-Moon = 1", sat["house_from_moon"] == 1)
check("house-from-lagna = 10", sat["house_from_lagna"] == 10, f"got {sat['house_from_lagna']}")
check("conjoins natal Moon", any(c["key"] == "moon" for c in sat["conjunct_natal"]))
conj_moon = next(c for c in sat["conjunct_natal"] if c["key"] == "moon")
check("conjunction arc ~ 0.5", abs(conj_moon["arc"] - 0.5) < 1e-6, f"got {conj_moon['arc']}")

asp = {a["target"]: a for a in sat["aspects_natal"]}
check("aspects natal Sun (3rd, special, full)",
      "sun" in asp and asp["sun"]["house"] == 3 and asp["sun"]["special"] and asp["sun"]["strength"] == 1.0)
check("aspects natal Venus (5th, general ½, not special)",
      "venus" in asp and asp["venus"]["house"] == 5 and not asp["venus"]["special"] and abs(asp["venus"]["strength"] - 0.5) < 1e-9)
check("aspects natal Mars (7th, full, not special)",
      "mars" in asp and asp["mars"]["house"] == 7 and abs(asp["mars"]["strength"] - 1.0) < 1e-9 and not asp["mars"]["special"])
check("aspects natal Jupiter (10th, special, full)",
      "jupiter" in asp and asp["jupiter"]["house"] == 10 and asp["jupiter"]["special"] and asp["jupiter"]["strength"] == 1.0)
check("aspects natal Saturn (9th, general ½)",
      "saturn" in asp and asp["saturn"]["house"] == 9 and abs(asp["saturn"]["strength"] - 0.5) < 1e-9)
check("aspects the lagna (4th, general ¾)",
      "lagna" in asp and asp["lagna"]["house"] == 4 and abs(asp["lagna"]["strength"] - 0.75) < 1e-9)
check("does NOT aspect natal Rahu (11th — no graha dṛṣṭi there)", "rahu" not in asp)
check("aspect target set is EXACTLY the reachable points",
      set(asp) == {"sun", "venus", "mars", "saturn", "jupiter", "lagna"}, f"got {sorted(asp)}")
check("all aspect strengths > 0", all(a["strength"] > 0 for a in sat["aspects_natal"]))

merc = by_key["mercury"]
print("\nA transit graha in the lagna sign conjoins the lagna (arc None):")
check("transit Mercury conjoins the lagna",
      any(c["key"] == "lagna" and c["arc"] is None for c in merc["conjunct_natal"]))

print("\nTransit Jupiter over its own natal Jupiter is a near-return:")
jup = by_key["jupiter"]
check("return same_sign True", jup["return"]["same_sign"])
check("return distance ~ 0.8", abs(jup["return"]["distance"] - 0.8) < 1e-6, f"got {jup['return']['distance']}")

print("\nNodes transit and are conjoined but cast no graha dṛṣṭi:")
rahu = by_key["rahu"]
check("transit Rahu present", rahu is not None)
check("Rahu house-from-Moon = 1", rahu["house_from_moon"] == 1)
check("Rahu conjoins natal Moon", any(c["key"] == "moon" for c in rahu["conjunct_natal"]))
check("Rahu casts NO aspects", rahu["aspects_natal"] == [])
check("Rahu combustion does not apply", not rahu["combustion"]["applies"])

# ---- real chart, end to end ------------------------------------------------
print("\nReal chart end-to-end (natal 1985-07-13 14:30 Varanasi; transit 2026-07-30):")
try:
    from datetime import datetime
    from vedic import compute_chart
    n = compute_chart(local_dt=datetime(1985, 7, 13, 14, 30),
                      latitude=25.3176, longitude=82.9739, tz_name="Asia/Kolkata")
    t = compute_chart(local_dt=datetime(2026, 7, 30, 12, 0),
                      latitude=25.3176, longitude=82.9739, tz_name="UTC")
    real = gochara.transit_geometry(n.to_dict()["grahas"], n.lagna_rasi,
                                    t.to_dict()["grahas"], transit_utc=t.utc)
    check("nine transiting grahas", len(real["grahas"]) == 9, f"got {len(real['grahas'])}")
    check("every house-from-Moon in 1..12",
          all(1 <= r["house_from_moon"] <= 12 for r in real["grahas"]))
    check("every house-from-lagna in 1..12",
          all(1 <= r["house_from_lagna"] <= 12 for r in real["grahas"]))
    check("reference Moon matches natal Moon sign",
          real["reference"]["moon_rasi"] == next(x["rasi"] for x in n.to_dict()["grahas"] if x["key"] == "moon"))
    check("each graha's own return distance in [-180,180]",
          all(-180 <= r["return"]["distance"] <= 180 for r in real["grahas"] if r["return"]))
    check("nodes cast no aspects on a real chart",
          all(real_r["aspects_natal"] == [] for real_r in real["grahas"] if real_r["key"] in ("rahu", "ketu")))
    # A concrete, independently-known fact: Saturn is in sidereal Pisces (rasi 11)
    # throughout 2026, so its house-from-Moon must equal Pisces counted from the
    # natal Moon — not just "somewhere in 1..12".
    sat_t = next(r for r in real["grahas"] if r["key"] == "saturn")
    check("real transit Saturn is in sidereal Pisces (rasi 11) in 2026",
          sat_t["rasi"] == 11, f"got {sat_t['rasi']}")
    check("its house-from-Moon equals Pisces counted from the natal Moon",
          sat_t["house_from_moon"] == _house(real["reference"]["moon_rasi"], 11))
except Exception as e:  # noqa: BLE001
    check("real chart end-to-end ran", False, f"raised {e!r}")

# ---- the /api/gochara route --------------------------------------------------
print("\n/api/gochara route (Flask test client): validation, range, 'now' default:")
try:
    from app import app as flask_app
    c = flask_app.test_client()
    base = {"date": "1985-07-13", "time": "14:30", "latitude": 25.3176,
            "longitude": 82.9739, "timezone": "Asia/Kolkata"}
    check("missing fields -> 400", c.post("/api/gochara", json={}).status_code == 400)
    check("bad date -> 400",
          c.post("/api/gochara", json={**base, "date": "nope"}).status_code == 400)
    check("transit year outside ephemeris range -> 400",
          c.post("/api/gochara", json={**base, "transit_date": "1500-01-01"}).status_code == 400)
    now_resp = c.post("/api/gochara", json=base)   # no transit_date -> now
    check("'now' default -> 200", now_resp.status_code == 200)
    check("'now' response carries nine grahas",
          now_resp.status_code == 200 and len(now_resp.get_json().get("grahas", [])) == 9)
except Exception as e:  # noqa: BLE001
    check("route test ran", False, f"raised {e!r}")

print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAILED: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
