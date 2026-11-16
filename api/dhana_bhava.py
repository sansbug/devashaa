"""
BPHS Vol I ch.13 — "Effects of Second House" (dhana-bhāva-phala), vv.1-7.

Tier: sloka. The English is R. Santhanam's translation, read from the page scans
(Ranjan Publications; printed pp.132-134 = PDF pp.131-133) on 2026-11-15 — the
OCR layer was not trusted. One printer's slip is repaired: v.5 prints "supject".
The Sanskrit is on the same pages and is not re-translated here (never
self-translate; see CLAUDE.md).

What this module does: for each verse, test the verse's OWN stated conditions
against the chart and report which clause matched, with the planets involved.
It returns the WHOLE verse text with every match — a verse's favourable and
unfavourable halves travel together.

Deliberate limits (each reported in the payload, never silently skipped):

  * vv.4-5 speak of a relation BETWEEN the 2nd lord and the 11th lord. For the
    two ascendants where one planet rules both houses (Kumbha: Jupiter; Siṁha:
    Mercury) an exchange or a conjunction of "the two lords" is not a meaningful
    test, so those verses are not applied.
  * v.5's alternative ("or is aspected by or conjunct by Jupiter and Venus") is
    ambiguous in the translation — the translator's own note reads it as
    "Jupiter (and) or Venus" — and is not evaluated.
  * v.7's "combust": the text gives no orb for combustion (see motion.py), so
    that branch is not evaluated; only "be with malefics" is.
  * Benefic / malefic here is the NATURAL classing of ch.3 v.11 (printed p.26):
    "the Sun, Saturn, Mars, decreasing Moon, Rahu and Ketu ... are malefics while
    the rest are benefics. Mercury, however, is a malefic if he joins a malefic."
    With the Moon's phase unknown the Moon is left out of both lists.
"""
from __future__ import annotations

RASI_LORD = ["mars", "venus", "mercury", "moon", "sun", "mercury",
             "venus", "mars", "jupiter", "saturn", "saturn", "jupiter"]
KENDRA = (1, 4, 7, 10)
TRIKONA = (1, 5, 9)
DUSTHANA = (6, 8, 12)

SOURCE = {"id": "bphs", "text": "Bṛhat Parāśara Horā Śāstra", "author": "Parāśara",
          "translator": "R. Santhanam", "tier": "sloka"}
NATURE_CITATION = "BPHS I ch.3 v.11 (p.26)"

VERSES = {
    "1-2": {
        "citation": "BPHS I ch.13 vv.1-2 (pp.132-133)",
        "text": ("O excellent of the Brahmanas, listen to me speaking on the effects of the 2nd house. "
                 "If the lord of the 2nd is in the 2nd or is in an angle or in a trine, he will promote "
                 "one's wealth (or monetary state). Should he be in the 6th/8th/12th, financial conditions "
                 "will decline. A benefic in the 2nd will give wealth while a malefic instead will destroy "
                 "the same."),
    },
    "3": {
        "citation": "BPHS I ch.13 v.3 (p.133)",
        "text": "One will be wealthy if Jupiter is in the 2nd as the lord of the 2nd or is with Mars.",
    },
    "4": {
        "citation": "BPHS I ch.13 v.4 (p.133)",
        "text": ("If the 2nd lord is in the 11th while the lord of the 11th is in the 2nd, wealth will be "
                 "acquired by the native. Alternatively these two lords may join in an angle or in a trine."),
    },
    "5": {
        "citation": "BPHS I ch.13 v.5 (p.134)",
        "text": ("If the lord of the 2nd is in an angle while the 11th lord is in a trine thereof or is "
                 "aspected by or conjunct by Jupiter and Venus, the subject will be wealthy."),
    },
    "6-7": {
        "citation": "BPHS I ch.13 vv.6-7 (p.134)",
        "text": ("One will be penniless if the lord of the 2nd is in an evil house while the 11th lord is "
                 "also so placed and the 2nd is occupied by a malefic. There will be penury right from "
                 "birth and the native will have to beg even for his food if the lords of the 2nd and the "
                 "11th are both combust or be with malefics."),
    },
}


def _house(rasi: int, lagna: int) -> int:
    return (rasi - lagna) % 12 + 1


def natural_natures(rasi: dict, moon_waxing=None) -> dict:
    """graha -> 'malefic' | 'benefic' by ch.3 v.11. The Moon is omitted when its phase is unknown."""
    mal = {g for g in ("sun", "saturn", "mars", "rahu", "ketu") if g in rasi}
    if moon_waxing is False and "moon" in rasi:
        mal.add("moon")
    # "Mercury, however, is a malefic if he joins a malefic."
    if "mercury" in rasi and any(rasi[m] == rasi["mercury"] for m in mal):
        mal.add("mercury")
    out = {}
    for g in rasi:
        if g in mal:
            out[g] = "malefic"
        elif g == "moon" and moon_waxing is None:
            continue
        else:
            out[g] = "benefic"
    return out


def evaluate(positions: dict, lagna: int, moon_waxing=None) -> dict:
    """`positions`: graha key -> {"rasi": int, ...}; `lagna`: lagna sign 0-11.

    Returns {"source", "matches": [...], "not_applied": [...]}. A match is
    {verse, citation, text, clauses: [{code, polarity, grahas, houses}]}.
    """
    rasi = {g: p["rasi"] for g, p in positions.items()}
    house = {g: _house(r, lagna) for g, r in rasi.items()}
    l2 = RASI_LORD[(lagna + 1) % 12]
    l11 = RASI_LORD[(lagna + 10) % 12]
    nature = natural_natures(rasi, moon_waxing)
    in_2nd = [g for g, h in house.items() if h == 2]
    same_lord = l2 == l11
    matches, not_applied = [], []

    def add(verse, clauses):
        if clauses:
            matches.append({"verse": verse, **VERSES[verse], "clauses": clauses})

    # ── vv.1-2 ────────────────────────────────────────────────────────────────
    c = []
    h2 = house.get(l2)
    if h2 is not None:
        if h2 == 2 or h2 in KENDRA or h2 in TRIKONA:
            c.append({"code": "lord2_well_placed", "polarity": "favourable", "grahas": [l2], "houses": [h2]})
        elif h2 in DUSTHANA:
            c.append({"code": "lord2_in_6_8_12", "polarity": "adverse", "grahas": [l2], "houses": [h2]})
    ben = [g for g in in_2nd if nature.get(g) == "benefic"]
    mal = [g for g in in_2nd if nature.get(g) == "malefic"]
    if ben:
        c.append({"code": "benefic_in_2nd", "polarity": "favourable", "grahas": ben, "houses": [2]})
    if mal:
        c.append({"code": "malefic_in_2nd", "polarity": "adverse", "grahas": mal, "houses": [2]})
    add("1-2", c)

    # ── v.3 ───────────────────────────────────────────────────────────────────
    c = []
    if "jupiter" in rasi:
        if l2 == "jupiter" and house["jupiter"] == 2:
            c.append({"code": "jupiter_lord2_in_2nd", "polarity": "favourable", "grahas": ["jupiter"], "houses": [2]})
        if "mars" in rasi and rasi["mars"] == rasi["jupiter"]:
            c.append({"code": "jupiter_with_mars", "polarity": "favourable", "grahas": ["jupiter", "mars"],
                      "houses": [house["jupiter"]]})
    add("3", c)

    # ── vv.4-5: a relation between two different lords ────────────────────────
    if same_lord:
        not_applied.append({"verses": "4-5", "reason": "one_planet_rules_both",
                            "grahas": [l2]})
    elif l2 in house and l11 in house:
        c = []
        if house[l2] == 11 and house[l11] == 2:
            c.append({"code": "lords_2_11_exchange", "polarity": "favourable", "grahas": [l2, l11], "houses": [11, 2]})
        elif house[l2] == house[l11] and (house[l2] in KENDRA or house[l2] in TRIKONA):
            c.append({"code": "lords_2_11_join_kendra_kona", "polarity": "favourable", "grahas": [l2, l11],
                      "houses": [house[l2]]})
        add("4", c)
        c = []
        if house[l2] in KENDRA and (house[l11] - house[l2]) % 12 + 1 in (5, 9):
            c.append({"code": "lord2_kendra_lord11_trine_from_it", "polarity": "favourable", "grahas": [l2, l11],
                      "houses": [house[l2], house[l11]]})
        add("5", c)
    not_applied.append({"verses": "5", "reason": "alternative_ambiguous"})

    # ── vv.6-7 ────────────────────────────────────────────────────────────────
    c = []
    if l2 in house and l11 in house:
        if house[l2] in DUSTHANA and house[l11] in DUSTHANA and mal:
            c.append({"code": "lords_in_evil_houses_malefic_in_2nd", "polarity": "adverse",
                      "grahas": sorted({l2, l11, *mal}), "houses": sorted({house[l2], house[l11], 2})})

        def with_malefic(g):
            return [m for m, n in nature.items() if n == "malefic" and m != g and rasi[m] == rasi[g]]

        w2, w11 = with_malefic(l2), with_malefic(l11)
        if w2 and w11:
            c.append({"code": "lords_2_11_with_malefics", "polarity": "adverse",
                      "grahas": sorted({l2, l11, *w2, *w11}), "houses": sorted({house[l2], house[l11]})})
    add("6-7", c)
    not_applied.append({"verses": "7", "reason": "combustion_has_no_orb_in_the_text"})

    return {"source": SOURCE, "lord2": l2, "lord11": l11, "natures": nature,
            "nature_citation": NATURE_CITATION, "matches": matches, "not_applied": not_applied}
