"""
Gochara-phala (transit effects) from Phaldeepika (Bhavartha Bodhini) Chapter 26,
"The Effect of Transit" — CLASSICAL tier, transits counted FROM THE MOON SIGN.

COVERAGE IS HONESTLY PARTIAL. The held scan is a preview PDF that omits roughly
three of every four pages of ch.26 (printed pp.576-628); what survives — and was
extracted from rendered pages and adversarially verified — is:

  * Śloka 3 (printed p.581): the SUN's favourable transit houses from the Moon
    sign, their vedha (obstruction) houses, and the Sun–Saturn vedha exception.
  * The "another opinion" commentary chart (printed p.597): per-graha outcomes
    when a favourable transit is vedha-obstructed.

Ślokas 4-28 (the Moon…Ketu per-house results and their favourable/vedha lists)
fell on omitted pages and are NOT here — by the cite-or-refuse rule they stay
absent until a fuller edition is supplied, and nothing is reconstructed from
memory of the classics. BPHS's own transit treatment is aṣṭakavarga (its ch.66-74),
already implemented separately.
"""

SOURCE = {
    "id": "phaladipika_gochara", "text": "Phaldeepika (Bhavartha Bodhini)",
    "author": "Mantreśvara",
    "date": "~13th c. CE", "translator": "Gopesh Kumar Ojha & Ashutosh Ojha",
    "edition": "Motilal Banarsidass, Delhi 2008",
    "tier": "classical",
}

COVERAGE_NOTE = (
    "Partial by source: only ch.26 śloka 3 (the Sun) and the vedha-outcome chart "
    "survive in the held scan; the other grahas' transit ślokas (4-28) await a "
    "fuller edition and are never invented."
)

# graha -> favourable transit houses FROM THE MOON SIGN, with each house's vedha
# (obstruction) house. A planet standing in the vedha house — counted from the
# Moon sign, Nārada's method, as the commentary adopts — voids the favourable
# transit. Exception (śloka 3): no vedha operates between the Sun and Saturn
# (father and son).
FAVOURABLE = {
    "sun": {
        "houses": {11: 5, 3: 9, 10: 4, 6: 12},   # favourable house -> its vedha house
        "vedha_exempt": ["saturn"],
        "citation": "Phaldeepika ch.26 śl.3 (printed p.581)",
        "confidence": "corroborated",
    },
}

# Per-graha outcome when a favourable transit is vedha-obstructed — from the
# commentary chart "Chart showing the transit effects of Vedh of Sun, Moon, Mars
# etc. — another opinion" (printed p.597). COMMENTARY tier (the chart is the
# edition's own supplement, labelled "another opinion"), never blended upward.
VEDHA_OUTCOME = {
    "sun":     {"gist": "loss of place and travels",
                "citation": "Phaldeepika ch.26, vedha chart (printed p.597)", "tier": "commentary"},
    "saturn":  {"gist": "all is lost; fears",
                "citation": "Phaldeepika ch.26, vedha chart (printed p.597)", "tier": "commentary"},
    "ketu":    {"gist": "losses and fear of disease",
                "citation": "Phaldeepika ch.26, vedha chart (printed p.597)", "tier": "commentary"},
}


def sun_transit_judgment(house_from_moon: int, occupants_of_house_from_moon) -> dict | None:
    """The cited ch.26 judgment for the Sun transiting ``house_from_moon`` from
    the natal Moon. ``occupants_of_house_from_moon`` maps house-from-Moon (1-12)
    -> list of transiting graha keys standing there (for the vedha check).
    Returns None when the text says nothing (cite-or-refuse), else a dict with
    status favourable / obstructed / not-favourable + citation."""
    fav = FAVOURABLE.get("sun")
    if not fav:
        return None
    if house_from_moon not in fav["houses"]:
        return {"status": "not-favourable",
                "note": "not among the Sun's favourable transit houses (11, 3, 10, 6 from the Moon)",
                "citation": fav["citation"], "tier": "classical"}
    vedha_house = fav["houses"][house_from_moon]
    blockers = [g for g in (occupants_of_house_from_moon.get(vedha_house) or [])
                if g not in fav["vedha_exempt"] and g != "sun"]
    if blockers:
        out = {"status": "obstructed", "vedhaHouse": vedha_house, "blockers": blockers,
               "citation": fav["citation"], "tier": "classical"}
        oc = VEDHA_OUTCOME.get("sun")
        if oc:
            out["outcome"] = oc["gist"]
            out["outcomeCitation"] = oc["citation"]
            out["outcomeTier"] = oc["tier"]
        return out
    return {"status": "favourable", "vedhaHouse": vedha_house,
            "citation": fav["citation"], "tier": "classical"}
