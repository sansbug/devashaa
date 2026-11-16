import sys
sys.path.insert(0, r"C:\proj\astrodev\api")
import planet_matrix as pm
import relationships as rel
import drishti as dr
import functional as fn

fails = []
def check(label, cond, detail=""):
    if not cond: fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  '+str(detail)) if detail else ''}")


print("BPHS ch.26 vv.2-5: the houses that receive a planet's full aspect")
check("Sun, Moon, Mercury, Venus aspect the 7th only",
      all(pm.full_aspect_distances(g) == [7] for g in ("sun", "moon", "mercury", "venus")))
check("Mars: 4th, 7th, 8th", pm.full_aspect_distances("mars") == [4, 7, 8])
check("Jupiter: 5th, 7th, 9th", pm.full_aspect_distances("jupiter") == [5, 7, 9])
check("Saturn: 3rd, 7th, 10th", pm.full_aspect_distances("saturn") == [3, 7, 10])
check("the nodes cast none (ch.26 does not name them)",
      pm.full_aspect_distances("rahu") == [] and pm.full_aspect_distances("ketu") == [])

# Meena lagna (11). Sun, Saturn in Dhanus (10th); Moon in Kumbha (12th); Mars in Vrischika (9th);
# Mercury, Venus, Rahu in Makara (11th); Jupiter in Mithuna (4th); Ketu in Karka (5th).
POS = {"sun": 8, "moon": 10, "mars": 7, "mercury": 9, "jupiter": 2, "venus": 9, "saturn": 8, "rahu": 9, "ketu": 3}
LAGNA = 11


def make(waxing=True, pos=POS, lagna=LAGNA):
    return pm.build(pos, lagna, waxing, fn.lagna_profile(lagna, moon_waxing=waxing),
                    rel.relationship_matrix(pos), dr.graha_drishti_chart(pos))


m = make()
P = {r["graha"]: r for r in m["planets"]}
H = {r["house"]: r for r in m["houses"]}

print("\nWho sits where")
check("nine planets, twelve houses", len(m["planets"]) == 9 and len(m["houses"]) == 12)
check("the 1st house is the ascendant's sign", H[1]["sign"] == LAGNA and H[1]["lord"] == "jupiter")
check("the 10th holds the Sun and Saturn", [o["graha"] for o in H[10]["occupants"]] == ["sun", "saturn"])
check("the 11th holds Mercury, Venus and Rahu", [o["graha"] for o in H[11]["occupants"]] == ["mercury", "venus", "rahu"])
check("every planet is in exactly one house",
      sorted(o["graha"] for h in m["houses"] for o in h["occupants"]) == sorted(POS))
check("a house lord's own house is given", H[1]["lord_house"] == 4)

print("\nAspects fall where the verse says")
check("Mars in the 9th aspects the 12th, 3rd and 4th fully", P["mars"]["aspect_houses"] == [12, 3, 4], P["mars"]["aspect_houses"])
check("Jupiter in the 4th aspects the 8th, 10th and 12th fully", P["jupiter"]["aspect_houses"] == [8, 10, 12])
check("Saturn in the 10th aspects the 12th, 4th and 7th fully", P["saturn"]["aspect_houses"] == [12, 4, 7])
for g in pm.SEVEN:
    for h in P[g]["aspect_houses"]:
        check(f"{g} is listed in house {h}'s full aspects", g in H[h]["full_aspects"])
check("no house lists a planet the rule does not send there",
      all(n in P[g]["aspect_houses"] for n, h in H.items() for g in h["full_aspects"]))
check("no node appears in any aspect column",
      not any(g in pm.NODES for h in m["houses"] for g in h["full_aspects"] + [p["graha"] for p in h["partial_aspects"]]))
check("partial aspects carry a quarter, a half or three quarters",
      all(p["fraction"] in (0.25, 0.5, 0.75) for h in m["houses"] for p in h["partial_aspects"]))
check("the 2nd, 6th, 11th and 12th from a planet get nothing from it",
      all(g not in H[(P[g]["house"] + d - 2) % 12 + 1]["full_aspects"]
          and g not in [p["graha"] for p in H[(P[g]["house"] + d - 2) % 12 + 1]["partial_aspects"]]
          for g in pm.SEVEN for d in (2, 6, 11, 12)))

print("\nNature: ch.3 v.11")
check("Sun, Mars, Saturn, Rahu, Ketu malefic", all(P[g]["natural"] == "malefic" for g in ("sun", "mars", "saturn", "rahu", "ketu")))
check("Jupiter benefic", P["jupiter"]["natural"] == "benefic")
check("waxing Moon benefic, and the reason is given", P["moon"]["natural"] == "benefic" and P["moon"]["natural_why"] == "waxing")
check("Mercury with Rahu is malefic", P["mercury"]["natural"] == "malefic" and P["mercury"]["natural_why"] == "with_malefic")
check("Venus with Rahu stays benefic (only Mercury turns)", P["venus"]["natural"] == "benefic")
w = {r["graha"]: r for r in make(waxing=False)["planets"]}
check("waning Moon malefic", w["moon"]["natural"] == "malefic" and w["moon"]["natural_why"] == "waning")
alone = dict(POS, mercury=0)
a = {r["graha"]: r for r in make(pos=alone)["planets"]}
check("Mercury away from malefics is benefic", a["mercury"]["natural"] == "benefic" and a["mercury"]["natural_why"] == "not_with_malefic")
u = {r["graha"]: r for r in make(waxing=None)["planets"]}
check("Moon's phase unknown: not classed", u["moon"]["natural"] is None)

print("\nNature for the ascendant: ch.34, kept apart")
check("the nodes are not classed for an ascendant", P["rahu"]["functional"] is None and P["ketu"]["functional"] is None)
check("Mars is a natural malefic and a benefic for Meena", P["mars"]["natural"] == "malefic" and P["mars"]["functional"] == "benefic")

print("\nInfluences on a house are sorted by the caster's nature, never by the distance")
for n, h in H.items():
    for kind in ("benefic", "malefic"):
        for g in h[kind]["occupants"] + h[kind]["aspects"]:
            check(f"house {n}: {g} is under {kind} because that is its nature", P[g]["natural"] == kind)
    listed = sorted(h["benefic"]["occupants"] + h["malefic"]["occupants"] + [g for g in h["unclassed"] if g in [o["graha"] for o in h["occupants"]]])
    check(f"house {n}: every occupant is placed once", listed == sorted(o["graha"] for o in h["occupants"]))
check("the 12th: Jupiter's aspect is benefic, Mars's and Saturn's malefic, all at the same count rule",
      H[12]["benefic"]["aspects"] == ["jupiter"] and H[12]["malefic"]["aspects"] == ["mars", "saturn"], H[12])

print("\nFriendship: ch.3 vv.55-58")
check("Sun's natural friends are Moon, Mars, Jupiter", P["sun"]["friends"] == ["moon", "mars", "jupiter"])
check("Sun's natural enemies are Venus, Saturn", P["sun"]["enemies"] == ["venus", "saturn"])
check("friends, neutrals and enemies cover the other six",
      all(len(P[g]["friends"]) + len(P[g]["neutrals"]) + len(P[g]["enemies"]) == 6 for g in pm.SEVEN))
check("the chart relation is the five-fold one",
      P["sun"]["in_chart"]["mars"] == {"temporary": "friend", "compound": "adhimitra"})
check("a node has no friendship row", "friends" not in P["rahu"])
check("an occupant's relation to the house lord is given", H[10]["occupants"][0]["to_lord"] == "sama", H[10]["occupants"])
check("planets that share a sign are named for the conjunction caveat",
      set(m["conjunction_affected"]) == {"sun", "saturn", "mercury", "venus", "rahu"})

print()
print("ALL PASS ✓" if not fails else f"FAILED: {fails}")
sys.exit(1 if fails else 0)
