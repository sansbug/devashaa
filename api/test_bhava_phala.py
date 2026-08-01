"""Bhāva-phala engine.

Run: python api/test_bhava_phala.py

Validates the house/lord derivation, that the correct cited ch.24 verse fires
for each (lord, placed) pair (incl. v110 "10th lord in 2nd = wealthy" — the very
rule the Morarji Desai worked example illustrates), dual-lordship (ch.24 vv.145-
148) flagging, occupant listing WITHOUT an asserted effect (the sourced planet-
in-house refusal), and aspects-in — on a controlled synthetic chart, then runs
the whole thing end-to-end on a real chart.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bhava_phala as bp
import bhava_phala_rules as R

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


# Verse index within ch.24: (lord_house, placed_house) -> (lord-1)*12 + placed.
def verse_of(lord, placed):
    return (lord - 1) * 12 + placed


print("Rule table: (lord, placed) -> verse mapping is the ch.24 sequence:")
check("(1,1) is v1", R.LORD_IN_HOUSE[(1, 1)]["verse"] == 1)
check("(10,2) is v110", R.LORD_IN_HOUSE[(10, 2)]["verse"] == 110)
check("(12,12) is v144", R.LORD_IN_HOUSE[(12, 12)]["verse"] == 144)
check("every (lord,placed) verse = (lord-1)*12+placed",
      all(R.LORD_IN_HOUSE[(l, p)]["verse"] == verse_of(l, p) for l in range(1, 13) for p in range(1, 13)))

# --- controlled synthetic chart, Aries lagna (lagna sign 0) -----------------
# Aries lagna → house h has sign (h-1); lords: 1&8→Mars, 2&7→Venus, 3&6→Mercury,
# 4→Moon, 5→Sun, 9&12→Jupiter, 10&11→Saturn.
lagna = 0
positions = {
    "sun": {"rasi": 0},      # house 1  (Sun lords house 5)
    "moon": {"rasi": 3},     # house 4  (Moon lords house 4)
    "mars": {"rasi": 1},     # house 2  (Mars lords houses 1, 8)
    "mercury": {"rasi": 2},  # house 3  (Mercury lords 3, 6)
    "jupiter": {"rasi": 8},  # house 9  (Jupiter lords 9, 12)
    "venus": {"rasi": 6},    # house 7  (Venus lords 2, 7)
    "saturn": {"rasi": 1},   # house 2  (Saturn lords 10, 11)  → 10th lord in 2nd
    "rahu": {"rasi": 5},     # house 6  (node — occupant only)
    "ketu": {"rasi": 11},    # house 12
}
out = bp.bhava_phala(positions, lagna)
bh = {b["house"]: b for b in out["bhavas"]}

print("\nTwelve houses, each with its lord and a cited lord-in-house rule:")
check("12 bhāvas", len(out["bhavas"]) == 12)
check("every house has a cited lord_rule", all(bh[h]["lord_rule"] and bh[h]["lord_rule"]["verse"] for h in range(1, 13)))
check("house 1 lord is Mars (Aries)", bh[1]["lord"] == "mars")
check("house 10 lord is Saturn (Capricorn)", bh[10]["lord"] == "saturn")

print("\nThe 10th lord (Saturn) sits in the 2nd → ch.24 v110 fires:")
check("10th lord's house is 2", bh[10]["lord_in_house"] == 2)
check("fired verse is 110", bh[10]["lord_rule"]["verse"] == 110)
check("effect says 'wealthy'", "wealthy" in bh[10]["lord_rule"]["effect"].lower())
check("citation is ch.24 v.110", bh[10]["lord_rule"]["citation"] == "BPHS I ch.24 v.110")

print("\nDual lordship (Saturn rules 10 & 11) flags the ch.24 vv.145-148 combination:")
check("house 10 combination_applies", bh[10]["combination_applies"] is True)
check("house 10 lord_also_rules includes 11", 11 in bh[10]["lord_also_rules"])
check("Sun rules only the 5th → house 5 no combination", bh[5]["combination_applies"] is False)

print("\nOccupants are listed but carry NO asserted effect (sourced refusal):")
check("house 2 occupants = Mars + Saturn", bh[2]["occupants"] == ["mars", "saturn"])
check("house 6 lists Rahu as occupant", "rahu" in bh[6]["occupants"])
check("no per-occupant effect field on any bhāva",
      all("occupant_effect" not in b for b in out["bhavas"]))
check("planet-in-house refusal note present", "no systematic" in out["planet_in_house"])
check("no-composite note present", "No per-house verdict" in out["no_composite"])

print("\nSignifications, kāraka, and aspects-in ride along, cited:")
check("house 2 significations mention wealth", "wealth" in bh[2]["significations"]["text"].lower())
check("house 10 kāraka is Mercury", bh[10]["karaka"] == "mercury")
check("kāraka carries a ch.32 citation", bh[10]["karaka_citation"].startswith("BPHS I ch.32"))
check("aspects_in is a list (fact from ch.26 dṛṣṭi)", isinstance(bh[7]["aspects_in"], list))

# --- real chart, end to end -------------------------------------------------
print("\nReal chart end-to-end (1985-07-13 14:30 Varanasi; lagna Tula):")
try:
    from datetime import datetime
    from vedic import compute_chart
    c = compute_chart(local_dt=datetime(1985, 7, 13, 14, 30),
                      latitude=25.3176, longitude=82.9739, tz_name="Asia/Kolkata")
    pos = {g.key: {"rasi": g.rasi} for g in c.grahas}
    real = bp.bhava_phala(pos, c.lagna_rasi)
    rb = {b["house"]: b for b in real["bhavas"]}
    check("12 bhāvas", len(real["bhavas"]) == 12)
    check("lagna (house 1) sign == lagna_rasi", rb[1]["sign"] == c.lagna_rasi)
    check("every house names a 7-planet lord",
          all(rb[h]["lord"] in ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn") for h in range(1, 13)))
    check("every house fires a cited lord_rule (verse 1..144)",
          all(1 <= rb[h]["lord_rule"]["verse"] <= 144 for h in range(1, 13)))
    check("occupants are a partition of the 9 grahas",
          sorted(g for b in real["bhavas"] for g in b["occupants"]) == sorted(pos))
    check("nodes never appear as a house lord",
          all(rb[h]["lord"] not in ("rahu", "ketu") for h in range(1, 13)))
except Exception as e:  # noqa: BLE001
    check("real chart end-to-end ran", False, f"raised {e!r}")

print(f"\n{'ALL PASS' if not fails else str(len(fails)) + ' FAILED: ' + ', '.join(fails)}")
sys.exit(1 if fails else 0)
