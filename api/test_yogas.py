"""Yoga detection.

Run: python api/test_yogas.py

Validates the detection predicates on controlled synthetic charts (Mahāpuruṣa,
Nābhasa modality/house-set, the Saṅkhyā void-rule, Sunapha, Amala, Gajakesari,
exaltation counts), that every detector name matches the catalogue, and that
strength-gated yogas ship the "unverified" flag — then runs the two dated worked
charts the recon flagged (Tilak → Kalpadruma, a 1959 chart → Amala) as soft checks
(exact reproduction depends on the historical timezone, so they warn, not fail).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import yogas
import yoga_rules

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


# exaltation longitudes, for making a graha "exalted" in a synthetic chart
EX = {"sun": 10, "moon": 33, "mars": 298, "mercury": 165, "jupiter": 95, "venus": 357, "saturn": 200}


def g(rasi, deg=15.0, d9=None):
    return {"rasi": rasi, "longitude": rasi * 30 + deg, "vargas": ({"D9": d9} if d9 is not None else {})}


def names(res):
    return {y["name"] for y in res["detected"]}


print("Every detector name is in the catalogue, and 3 are deliberately catalogue-only:")
check("all detectors valid", all(n in yoga_rules.YOGAS for n in yogas.DETECTORS))
check("85 detectors, 88 catalogued", len(yogas.DETECTORS) == 85 and len(yoga_rules.YOGAS) == 88)

print("\nPañca-Mahāpuruṣa — Saturn exalted (Libra) in a kendra → Śaśa:")
# lagna Libra(6): Saturn exalted in Libra sits in house 1.
pos = {"sun": g(2), "moon": g(1), "mars": g(2, 5), "mercury": g(3),
       "jupiter": g(8), "venus": g(4), "saturn": {"rasi": 6, "longitude": 200, "vargas": {}}}
res = yogas.detect_yogas(pos, 6)
check("Śaśa detected", "Sasa" in names(res))

print("\nNābhasa — all seven in movable signs → Rajju; and the Saṅkhyā void-rule:")
# all 7 in Aries(0) + Libra(6), both movable → Rajju; 2 distinct signs would be Yuga, but voided.
mov = {"sun": g(0), "moon": g(0, 20), "mars": g(0, 25), "mercury": g(6), "jupiter": g(6, 10), "venus": g(6, 20), "saturn": g(0, 5)}
res = yogas.detect_yogas(mov, 0)
check("Rajju detected (all movable)", "Rajju" in names(res))
check("Yuga (2 signs) is VOID under Rajju", "Yuga" not in names(res))

print("\nNābhasa — all seven confined to houses 1 and 7 → Sakata:")
sk = {"sun": g(0), "moon": g(0, 10), "mars": g(6), "mercury": g(6, 5), "jupiter": g(0, 20), "venus": g(6, 15), "saturn": g(0, 25)}
res = yogas.detect_yogas(sk, 0)   # lagna Aries: Aries=H1, Libra=H7
check("Sakata detected", "Sakata" in names(res))

print("\nLunar — a planet in the 2nd from the Moon (none in the 12th) → Sunapha:")
# Moon Aries(0); Mars in Taurus(1)=2nd from Moon; nothing in Pisces(11)=12th from Moon.
sun_ = {"moon": g(0), "mars": g(1), "sun": g(4), "mercury": g(5), "jupiter": g(6), "venus": g(7), "saturn": g(8)}
res = yogas.detect_yogas(sun_, 3)
check("Sunapha detected", "Sunapha Yoga" in names(res))
check("Anapha NOT detected", "Anapha Yoga" not in names(res))

print("\nch.36 — only a benefic in the 10th → Amala:")
# lagna Aries(0): 10th = Capricorn(9). Put only Jupiter there.
am = {"jupiter": g(9), "sun": g(0), "moon": g(1), "mars": g(2), "mercury": g(3), "venus": g(4), "saturn": g(5)}
res = yogas.detect_yogas(am, 0)
check("Amala detected", "Amala Yoga" in names(res))

print("\nch.36 — Jupiter in a kendra from the Moon, benefic aspect, not afflicted → Gajakesari:")
# Moon Aries(0); Jupiter exalted in Cancer(3)=4th from Moon (kendra); Venus in Capricorn(9)=7th aspect onto Cancer.
gk = {"moon": g(0), "jupiter": {"rasi": 3, "longitude": 95, "vargas": {}}, "venus": g(9),
      "sun": g(6), "mars": g(2), "mercury": g(7), "saturn": g(10)}
res = yogas.detect_yogas(gk, 0)
check("Gajakesari detected", "Gajakesari Yoga" in names(res))

print("\nRāja — exactly two planets exalted → '1–3 planets in exaltation':")
ex2 = {"saturn": {"rasi": 6, "longitude": 200, "vargas": {}}, "moon": {"rasi": 1, "longitude": 33, "vargas": {}},
       "sun": g(4), "mars": g(2), "mercury": g(0), "jupiter": g(11), "venus": g(7)}
res = yogas.detect_yogas(ex2, 6)
check("'1–3 planets in exaltation' detected", "1–3 planets in exaltation" in names(res))
check("'6 planets exalted' NOT detected", "6 planets exalted (emperor)" not in names(res))

print("\nStrength-gated yogas carry the 'strength unverified' flag when detected:")
sg = [y for y in res["detected"] if y["computability"] == "strength_gated"]
check("every strength_gated detected yoga has a strength_note",
      all(y.get("strength_note") for y in sg) if sg else True)

# --- soft worked-chart fixtures (timezone-sensitive) ------------------------
print("\nWorked charts (soft — exact reproduction depends on historical tz):")
try:
    from datetime import datetime
    from vedic import compute_chart

    def detect(dt, lat, lon, tz):
        c = compute_chart(local_dt=dt, latitude=lat, longitude=lon, tz_name=tz)
        pos = {x.key: {"rasi": x.rasi, "longitude": x.longitude, "vargas": x.vargas} for x in c.grahas}
        return names(yogas.detect_yogas(pos, c.lagna_rasi, c.lagna_vargas.get("D9")))

    tilak = detect(datetime(1856, 7, 23, 6, 12), 18.53, 73.95, "Asia/Kolkata")
    print(f"  Tilak (1856): Kalpadruma {'DETECTED' if 'Kalpadruma Yoga (a.k.a. Parijata Yoga)' in tilak else 'not detected (check tz/LMT)'}  · {len(tilak)} yogas total")
    amf = detect(datetime(1959, 5, 16, 11, 29), 26.48, 80.35, "Asia/Kolkata")
    print(f"  1959 female: Amala {'DETECTED' if 'Amala Yoga' in amf else 'not detected (check tz)'}  · {len(amf)} yogas total")
    check("both worked charts ran without error", True)
except Exception as e:  # noqa: BLE001
    check("worked charts ran", False, f"raised {e!r}")

print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAILED: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
