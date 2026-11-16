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


# longitudes inside those signs: Sun 16°52' Dhanus (Purva Ashadha), Moon 0°30' Kumbha (Dhanishta), Mars 5° Vrischika
# (Anuradha), Mercury 28° Makara (Dhanishta), Jupiter 10° Mithuna (Ardra), Venus 12° Makara (Shravana),
# Saturn 22° Dhanus (Purva Ashadha), Rahu 25° Makara (Dhanishta), Ketu 25° Karka (Ashlesha)
LON = {"sun": 256.86, "moon": 300.5, "mars": 215.0, "mercury": 298.0, "jupiter": 70.0, "venus": 282.0,
       "saturn": 262.0, "rahu": 295.0, "ketu": 115.0}


def make(waxing=True, pos=POS, lagna=LAGNA, lon=LON):
    return pm.build(pos, lagna, waxing, fn.lagna_profile(lagna, moon_waxing=waxing),
                    rel.relationship_matrix(pos), dr.graha_drishti_chart(pos), longitudes=lon)


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

print("\nNakshatr, its lord, and the planet's relation to that lord: ch.46 vv.12-14 + ch.3 vv.55-58")
check("Ashwini, Magha and Mula belong to Ketu", all(pm.nakshatra_lord(i) == "ketu" for i in (0, 9, 18)))
check("the nine lords in Dasha order", [pm.nakshatra_lord(i) for i in range(9)] ==
      ["ketu", "venus", "sun", "moon", "mars", "rahu", "jupiter", "saturn", "mercury"])
check("each lord holds three of the 27", all([pm.nakshatra_lord(i) for i in range(27)].count(g) == 3 for g in pm.ORDER))
check("0 deg is Ashwini, 13 deg 20 min starts Bharani, 359.9 is Revati",
      pm.nakshatra_of(0) == 0 and pm.nakshatra_of(13.34) == 1 and pm.nakshatra_of(359.9) == 26 and pm.nakshatra_of(360) == 0)
check("Sun in Purva Ashadha (Venus), an enemy by nature and a temporary friend: neutral",
      (P["sun"]["nakshatra"], P["sun"]["nakshatra_lord"], P["sun"]["to_nakshatra_lord"]) == (19, "venus", "sama"), P["sun"])
check("Mars in Anuradha, lord Saturn", (P["mars"]["nakshatra"], P["mars"]["nakshatra_lord"]) == (16, "saturn"))
check("the relation is the chart's five-fold one, planet towards lord",
      all(P[g]["to_nakshatra_lord"] == P[g]["in_chart"][P[g]["nakshatra_lord"]]["compound"]
          for g in pm.SEVEN if P[g]["nakshatra_lord"] in pm.SEVEN and P[g]["nakshatra_lord"] != g))
check("a lord that is a node gives no relation (Jupiter in Ardra, lord Rahu)",
      P["jupiter"]["nakshatra_lord"] == "rahu" and P["jupiter"]["to_nakshatra_lord"] is None)
check("a node as the planet gives no relation (Ketu in Ashlesha, lord Mercury)",
      P["ketu"]["nakshatra_lord"] == "mercury" and P["ketu"]["to_nakshatra_lord"] is None)
own = {r["graha"]: r for r in make(lon=dict(LON, moon=45.0))["planets"]}     # Rohini, the Moon's own
check("a planet in its own Nakshatr is marked own", own["moon"]["nakshatra_lord"] == "moon" and own["moon"]["to_nakshatra_lord"] == "own")
check("the house rows carry the same three for every occupant",
      all(o["nakshatra"] == P[o["graha"]]["nakshatra"] and o["nakshatra_lord"] == P[o["graha"]]["nakshatra_lord"]
          and o["to_nakshatra_lord"] == P[o["graha"]]["to_nakshatra_lord"] for h in m["houses"] for o in h["occupants"]))
bare = pm.build(POS, LAGNA, True, fn.lagna_profile(LAGNA, moon_waxing=True), rel.relationship_matrix(POS), dr.graha_drishti_chart(POS))
check("without longitudes the three are None, nothing is guessed", all(r["nakshatra"] is None for r in bare["planets"]))

print()
print("ALL PASS ✓" if not fails else f"FAILED: {fails}")
sys.exit(1 if fails else 0)
