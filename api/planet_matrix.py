"""The planet and house matrix: one table of who sits where, who aspects what, and who is whose friend.

NOTHING HERE IS A NEW RULE. Every column is read from a module that already carries its verse:

  natural nature     BPHS I ch.3 v.11   dhana_bhava.natural_natures
                     "the Sun, Saturn, Mars, decreasing Moon, Rahu and Ketu ... are malefics while the
                     rest are benefics. Mercury, however, is a malefic if he joins a malefic."
  nature for the     BPHS I ch.34       functional.lagna_profile (the text's own verdict per ascendant;
  ascendant                             the nodes are not classed, ch.34 v.16)
  friendship         BPHS I ch.3        relationships.relationship_matrix
                     vv.55-58           natural, temporary, and the five-fold compound of the two
  Nakshatr lord      BPHS I ch.46       vimshottari.VIMSHOTTARI (the Dasha order: the lord of the
                     vv.12-14           Nakshatr a planet sits in). The planet's five-fold relation
                                        towards that lord is the SAME ch.3 relation as above. The texts
                                        registered here state no result for it: it is shown as a fact of
                                        the chart, and the page says so. A node has no friendship
                                        (relationships.NODES_UNAVAILABLE), so the relation is None when
                                        the planet or the lord is Rahu or Ketu.
  aspects            BPHS I ch.26       drishti.graha_drishti_chart
                     vv.2-5             every planet aspects the 7th fully; Mars the 4th and 8th,
                                        Jupiter the 5th and 9th, Saturn the 3rd and 10th fully as well.
                                        The 3rd/10th, 5th/9th and 4th/8th carry a quarter, a half and
                                        three quarters for the others. The 2nd, 6th, 11th and 12th
                                        receive no aspect.

TWO THINGS THIS MODULE REFUSES, because the text does not state them:

  * An aspect is not good or bad by the house it falls on. Ch.26 grades the STRENGTH of an aspect by
    the distance and says "the effects ... will also be proportionate"; whether the effect helps or
    harms is read from the planet that casts it. So a house's influences are sorted by the caster's
    natural nature (ch.3 v.11), and the nature for the ascendant (ch.34) is given beside it, unblended.
    (The scheme "3, 5, 9, 11 friendly; 1, 4, 7, 10 hostile" is Tajika doctrine for the annual chart,
    tajika.py, and is not applied to a birth chart.)
  * Rahu and Ketu cast no aspect here. Ch.26 does not name them among the aspecting planets
    (drishti.NODE_GRAHA_DRISHTI_UNVERIFIED), so none is shown and the payload says so.

Keys only: the sentences a reader sees are written on the page (web/src/planetmatrix.js).
"""
from __future__ import annotations

import dhana_bhava
import drishti as dr
from dignity import RASI_LORD
from vimshottari import VIMSHOTTARI

SEVEN = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn")
NODES = ("rahu", "ketu")
ORDER = SEVEN + NODES

CITATIONS = {
    "natural": "BPHS I ch.3 v.11",
    "functional": "BPHS I ch.34",
    "friendship": "BPHS I ch.3 vv.55-58",
    "aspects": "BPHS I ch.26 vv.2-5",
    "nakshatra_lord": "BPHS I ch.46 vv.12-14",
}

NAKSHATRA_ARC = 360.0 / 27.0
_DASHA_ORDER = [k for k, _, _ in VIMSHOTTARI]      # Ketu, Venus, Sun, Moon, Mars, Rahu, Jupiter, Saturn, Mercury


def nakshatra_of(longitude: float) -> int:
    """Index 0-26 of the Nakshatr a sidereal longitude falls in (Ashwini = 0)."""
    return int((float(longitude) % 360.0) // NAKSHATRA_ARC) % 27


def nakshatra_lord(index: int) -> str:
    """ch.46 vv.12-14: the nine lords repeat three times over the 27, from Ashwini (Ketu)."""
    return _DASHA_ORDER[int(index) % 9]


def full_aspect_distances(graha: str) -> list[int]:
    """The house counts (from the planet's own sign as the 1st) that receive its full aspect."""
    if graha in NODES:
        return []
    return sorted({7, *dr.SPECIAL_DRISHTI_HOUSES.get(graha, ())})


def _house(sign: int, lagna: int) -> int:
    return (sign - lagna) % 12 + 1


def build(rasi_positions: dict, lagna: int, moon_waxing, profile: dict, relationships: dict,
          graha_drishti: dict, longitudes: dict | None = None) -> dict:
    """`rasi_positions`: graha -> sign 0-11. The other three are the payloads the analysis already built.
    `longitudes` (graha -> sidereal longitude) adds each planet's Nakshatr, its lord, and the planet's
    relation towards that lord; without it those three are None."""
    rasi = {g: int(s) for g, s in rasi_positions.items()}
    present = [g for g in ORDER if g in rasi]
    natural = dhana_bhava.natural_natures(rasi, moon_waxing)
    frows = {r["graha"]: r for r in (profile or {}).get("grahas", [])}
    nat_rel = (relationships or {}).get("natural", {})
    cmp_rel = (relationships or {}).get("compound", {})
    tmp_rel = (relationships or {}).get("temporary", {})
    disp = (relationships or {}).get("dispositor", {})
    recv = ((graha_drishti or {}).get("received") or {}).get("signs", {})

    def why(g):
        if g == "moon":
            return None if moon_waxing is None else ("waxing" if moon_waxing else "waning")
        if g == "mercury":
            return "with_malefic" if natural.get(g) == "malefic" else "not_with_malefic"
        return None

    def nak(g):
        if not longitudes or g not in longitudes:
            return {"nakshatra": None, "nakshatra_lord": None, "to_nakshatra_lord": None}
        i = nakshatra_of(longitudes[g])
        lord = nakshatra_lord(i)
        to = "own" if lord == g else (cmp_rel.get(g) or {}).get(lord)
        return {"nakshatra": i, "nakshatra_lord": lord, "to_nakshatra_lord": to}

    planets = []
    for g in present:
        h = _house(rasi[g], lagna)
        dist = full_aspect_distances(g)
        row = {
            "graha": g, "sign": rasi[g], "house": h,
            "natural": natural.get(g), "natural_why": why(g),
            "functional": (frows.get(g) or {}).get("nature"),
            "functional_citation": (frows.get(g) or {}).get("citation"),
            "owns": list((frows.get(g) or {}).get("houses_owned") or []),
            "aspect_rule": dist,
            "aspect_houses": [(h + d - 2) % 12 + 1 for d in dist],
            "is_node": g in NODES,
            **nak(g),
        }
        if g in SEVEN:
            others = [o for o in SEVEN if o != g]
            row["friends"] = [o for o in others if (nat_rel.get(g) or {}).get(o) == "friend"]
            row["neutrals"] = [o for o in others if (nat_rel.get(g) or {}).get(o) == "neutral"]
            row["enemies"] = [o for o in others if (nat_rel.get(g) or {}).get(o) == "enemy"]
            row["in_chart"] = {o: {"temporary": (tmp_rel.get(g) or {}).get(o),
                                   "compound": (cmp_rel.get(g) or {}).get(o)}
                               for o in others if o in rasi}
        planets.append(row)

    houses = []
    for n in range(1, 13):
        sign = (lagna + n - 1) % 12
        lord = RASI_LORD[sign]
        occ = [g for g in present if rasi[g] == sign]
        got = recv.get(sign) or recv.get(str(sign)) or {}
        full = [g for g in SEVEN if got.get(g, 0) >= 1.0 - 1e-9]
        partial = [{"graha": g, "fraction": got[g]} for g in SEVEN if 0 < got.get(g, 0) < 1.0 - 1e-9]
        side = {"benefic": {"occupants": [], "aspects": []}, "malefic": {"occupants": [], "aspects": []}}
        unclassed = []
        for g in occ:
            (side[natural[g]]["occupants"] if natural.get(g) in side else unclassed).append(g)
        for g in full:
            (side[natural[g]]["aspects"] if natural.get(g) in side else unclassed).append(g)
        houses.append({
            "house": n, "sign": sign, "lord": lord,
            "lord_house": _house(rasi[lord], lagna) if lord in rasi else None,
            "occupants": [{"graha": g, "to_lord": disp.get(g), **nak(g)} for g in occ],
            "full_aspects": full, "partial_aspects": partial,
            "benefic": side["benefic"], "malefic": side["malefic"], "unclassed": unclassed,
        })

    return {
        "lagna": lagna,
        "moon_waxing": moon_waxing,
        "planets": planets,
        "houses": houses,
        "citations": CITATIONS,
        "nodes_cast_no_aspect": True,
        "conjunction_affected": list((relationships or {}).get("conjunction_affected") or []),
    }
