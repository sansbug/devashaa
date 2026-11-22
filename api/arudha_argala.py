"""BPHS Vol I chs 29-31: Arudha padas (bhava padas), their results, and Argala.

Tier: sloka. The English is R. Santhanam's translation (Ranjan Publications), read from
the PAGE IMAGES of "BPHS - 1 RSanthanam-1.pdf" on 2026-11-21 (PDF page = printed - 1;
ch.29 = printed pp.292-303, ch.30 v.39 = p.310, ch.31 = pp.311-316). The OCR layer was
not used. Every verse is returned WHOLE with the clause this chart meets.

CALCULATION (ch.29 vv.1-5): count from a house to its lord, then the same number of
signs from the lord. If that lands on the house itself, take the 10th from it; if it
lands on the 7th from the house, take the 4th from the house (vv.4-5). For Scorpio and
Aquarius the lord used is Mars and Saturn, as in Santhanam's own worked examples.
Test fixture: his "standard nativity" (21 May 1944) and its Arudha chart (pp.294-295).

ARGALA (ch.31 vv.2-10): planets in the 4th, 2nd, 11th and 5th from a sign cause Argala;
those in the 10th, 12th, 3rd and 9th obstruct them respectively. Two rules for
obstruction stand in the text side by side, and BOTH are reported, never merged:
  * vv.2-9: the stronger side prevails, or the side with more planets. Strength is not
    evaluated here, so when the obstructors are at least as many, the result is
    "obstructed unless the Argala planet is stronger" (not decided);
  * v.10: an Argala planet in the 1st quarter of its sign is countered by an obstructor
    in the 4th quarter of its sign; 2nd quarter by 3rd quarter. Santhanam's note reads
    these as the ONLY two cases that obstruct (tier: his note).
Three or more malefics in the 3rd = Vipareeta Argala (v.4). One planet = limited,
two = medium, more = excellent (v.7). Natural benefic/malefic = ch.3 v.11.
Argala is computed here FROM SIGNS only (houses, the Arudha Lagna); the verse's reverse
counting for the nodes applies to Argala reckoned from a node, which is not done.

"Aspected" = a FULL graha drishti (ch.26), as in bhava_effects.py and as Santhanam's own
note on v.17 uses it ("aspected by Mars (8th aspect)").

WHAT IS NOT EVALUATED, and why:
  * ch.29 vv.6-7 graha padas for Mars to Saturn ("consider the stronger" of two signs);
    the Sun's and Moon's are computed as facts only (no verse gives their results).
  * v.24: its clause on the body is a sexual, gendered verdict (classical-sources §5).
  * v.29 (the same yogas from the Karakamsa): the text does not say whether to count in
    the rasi or the navamsa chart.
  * vv.33, 35, 37 and the "strong planets" alternative of vv.31-32: they need strength,
    or are stated only as "similarly".
  * ch.30 (Upapada) except v.39: mostly spouse and children verses (CLAUDE.md rule 2).
"""

from __future__ import annotations

import dignity
from drishti import graha_drishti_chart

SOURCE = {"id": "bphs", "text": "Bṛhat Parāśara Horā Śāstra", "author": "Parāśara",
          "translator": "R. Santhanam (Ranjan Publications)", "tier": "sloka"}
CONFIDENCE = "page_image_checked"   # read, then re-read against the page images on 2026-11-21
RASI_LORD = ["mars", "venus", "mercury", "moon", "sun", "mercury",
             "venus", "mars", "jupiter", "saturn", "saturn", "jupiter"]
OWN = {"sun": 4, "moon": 3}
PADA_NAME = {1: "Lagna Pada (Arudha Lagna)", 2: "Dhana Pada", 3: "Vikrama Pada", 4: "Matru Pada",
             5: "Mantra Pada", 6: "Roga Pada", 7: "Dara Pada", 8: "Marana Pada",
             9: "Pitru Pada", 10: "Karma Pada", 11: "Labha Pada", 12: "Vyaya Pada"}
ARGALA_PAIRS = ((4, 10), (2, 12), (11, 3), (5, 9))


def _from(sign: int, n: int) -> int:
    """The n-th sign counted from `sign` (1 = itself)."""
    return (sign + n - 1) % 12


def _count(a: int, b: int) -> int:
    """b is the n-th from a."""
    return (b - a) % 12 + 1


def pada_plain(sign: int, lord_sign: int) -> int:
    """ch.29 vv.2-3 alone: the count, with no exception applied."""
    return _from(lord_sign, _count(sign, lord_sign))


def pada(sign: int, lord_sign: int) -> int:
    """ch.29 vv.2-5. `sign`: the house's sign; `lord_sign`: where its lord stands.

    The verse's exceptions are applied as the verse states them. Santhanam's printed
    Arudha chart (p.295) agrees for 10 of 12 houses (including both exceptions in houses
    6 and 12) but skips the 7th exception in houses 9 and 10: it shows the plain count
    (Capricorn, Aquarius) where the verse gives Libra and Scorpio. His note 2
    (p.296: Aquarius with Saturn in Leo -> Taurus) gives a third answer; by the verse the
    count lands on the house itself, so the 10th from it (Scorpio) is the pada. The verse
    is followed; pada_plain() is reported beside it so the difference stays visible."""
    p = pada_plain(sign, lord_sign)
    if p == sign:
        return _from(sign, 10)
    if p == _from(sign, 7):
        return _from(sign, 4)
    return p


def bhava_padas(lagna: int, rasi: dict) -> dict:
    out = {}
    for h in range(1, 13):
        s = _from(lagna, h)
        lord = RASI_LORD[s]
        out[h] = pada(s, rasi[lord])
    return out


def graha_pada(graha: str, sign: int) -> int | None:
    """ch.29 vv.6-7, Sun and Moon only (one own sign each); the exceptions do not apply."""
    own = OWN.get(graha)
    if own is None:
        return None
    return _from(own, _count(sign, own))


NAME = {"sun": "Surya", "moon": "Chandra", "mars": "Mangal", "mercury": "Budh", "jupiter": "Guru",
        "venus": "Shukr", "saturn": "Shani", "rahu": "Rahu", "ketu": "Ketu"}


def _names(keys) -> str:
    return ", ".join(NAME.get(k, k) for k in keys)


def _ord(n: int) -> str:
    return f"{n}" + ("th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))


def _quarter(deg: float) -> int:
    return min(int(deg // 7.5), 3) + 1


def argala(ref: int, rasi: dict, lon: dict, natures: dict) -> dict:
    """Argala on the sign `ref`. rasi/lon: graha -> sign / longitude."""
    occ = {}
    for g, s in rasi.items():
        occ.setdefault(s, []).append(g)
    places = []
    for a, o in ARGALA_PAIRS:
        ag, ob = occ.get(_from(ref, a), []), occ.get(_from(ref, o), [])
        if not ag:
            continue
        if not ob:
            status = "unobstructed"
        elif len(ag) > len(ob):
            status = "prevails_by_number"
        else:
            status = "obstructed_unless_stronger"
        q_pairs = [(x, y) for x in ag for y in ob
                   if (_quarter(lon[x] % 30), _quarter(lon[y] % 30)) in ((1, 4), (2, 3))]
        sides = {natures.get(g) for g in ag}
        places.append({
            "from": a, "obstructed_from": o, "argala": ag, "obstructors": ob,
            "status_vv2_9": status,
            "countered_v10": bool(q_pairs), "v10_pairs": q_pairs,
            "grade_v7": "limited" if len(ag) == 1 else "medium" if len(ag) == 2 else "excellent",
            "kind": "benefic" if sides == {"benefic"} else "malefic" if sides == {"malefic"} else "mixed",
        })
    mal3 = [g for g in occ.get(_from(ref, 3), []) if natures.get(g) == "malefic"]
    return {"sign": ref, "places": places,
            "vipareeta": mal3 if len(mal3) >= 3 else None,
            "citation": "BPHS I ch.31 vv.2-10 (pp.311-314)"}


def _fires(p) -> bool:
    """Unobstructed by vv.2-9 (no obstructor, or more Argala planets than obstructors)."""
    return p["status_vv2_9"] in ("unobstructed", "prevails_by_number")


# --- the verses, word for word (Santhanam), with their printed pages ---------------
V = {
    "29.8-11": ("BPHS I ch.29 vv.8-11 (p.298)",
                "If the 11th from Lagna Pada is occupied or aspected by a planet, the native will be happy and rich; wealth will come through virtuous means if a benefic is related as above. A malefic will confer wealth through questionable means. If there be both a benefic and a malefic, it will be through both means. If the planet in question (i.e. the one so related to 11th from Lagna Pada) be in exaltation or in own sign etc., there will be plenty of gains and plenty of happiness."),
    "29.12": ("BPHS I ch.29 v.12 (p.298)",
              "O excellent of the Brahmins, if the 12th from Lagna Pada is unaspected as the 11th from Lagna Pada is being aspected by a planet, then the gains will be uninterrupted."),
    "29.13-15": ("BPHS I ch.29 vv.13-15 (pp.298-299)",
                 "O Brahmin, the quantum of gains will correspond to the number of planets in or aspecting the 11th from Lagna Pada. If there is Argala for the said 11th there will be more gains while a benefic Argala will bring still more gains. If the said benefic causing Argala be in his exaltation, the gains will be still higher. If the said 11th is aspected by a benefic from the ascendant, the 9th etc. gains will increase in the ascending order. In all these cases, the 12th from Pada be simultaneously free from malefic association."),
    "29.16-17": ("BPHS I ch.29 vv.16-17 (p.299)",
                 "If the 12th from Lagna Pada is aspected by conjunct both benefics and malefics, there will be abundant earnings but plenty of expenses. The benefic will cause through fair means, malefic through unfair means and mixed planets through both fair and unfair means."),
    "29.18": ("BPHS I ch.29 v.18 (p.300)",
              "If the 12th from Lagna Pada is conjunct the Sun, Venus and Rahu, there will be loss of wealth through the king. The Moon aspecting (the said trio in the said house) will specifically cause more such losses."),
    "29.19": ("BPHS I ch.29 v.19 (p.300)",
              "If Mercury is in the 12th from the Lagna Pada and be with or aspected by benefic similarly there will be expenses through paternal relatives. A malefic so related to the said Mercury will cause loss of wealth through disputes."),
    "29.20": ("BPHS I ch.29 v.20 (p.300)",
              "O Brahmin, if Jupiter is in the 12th from Lagna Pada, aspected by others, the expenses will be through taxes and on one's own."),
    "29.21": ("BPHS I ch.29 v.21 (p.300)",
              "O Brahmin, if Saturn is in the 12th from the Lagna Pada along with Mars and is aspected by others, the expenses will be through one's co-born."),
    "29.22": ("BPHS I ch.29 v.22 (p.300)",
              "Whatever sources of expenses are indicated above with reference to the 12th from Lagna Pada, gains through similar sources will occur if the 11th house so features with reference to Lagna Pada."),
    "29.23": ("BPHS I ch.29 v.23 (p.301)",
              "If Rahu or Ketu is placed in the 7th from Lagna Pada, the native will be troubled by stomachial disorders, or by fire."),
    "29.25": ("BPHS I ch.29 v.25 (p.301)",
              "Should one, two or all the three of Jupiter, Venus and the Moon be in the 7th from Lagna Pada, the native will be very wealthy."),
    "29.26": ("BPHS I ch.29 v.26 (p.301)",
              "Whether a benefic or a malefic if be exalted in the 7th from Lagna Pada, the native will be affluent, and be famous."),
    "29.27": ("BPHS I ch.29 v.27 (p.301)",
              "O Brahmin, these yogas as narrated by me with reference to the 7th from the Lagna Pada be also considered from the 2nd of Lagna Pada."),
    "29.28": ("BPHS I ch.29 v.28 (p.301)",
              "Anyone of Mercury, Jupiter and Venus be exalted in the 2nd from Lagna Pada and be with strength, will make the subject rich."),
    "29.30": ("BPHS I ch.29 v.30 (p.302)",
              "If Mercury is in the 2nd from Arudha Lagna, the native will lord over the whole country. Venus in the 2nd from Lagna Pada will make one a poet or a speaker."),
    "29.31-32": ("BPHS I ch.29 vv.31-32 (p.302)",
                 "If the Dara Pada (i.e. the Pada of the 7th house) falls in an angle or in a trine counted from the Lagna Pada or if the Lagna Pada and Dara Pada both have strong planets, the native will be rich and be famous in his country. If the Dara Pada falls in the 6th/8th/12th from the Lagna Pada, then the native will be poor."),
    "29.34": ("BPHS I ch.29 v.34 (pp.302-303)",
              "If the Lagna Pada and Dara Pada are mutually angular or trinal, there will be amity between the couple; if these be in mutually 6th/8th/12th, doubtlessly mutual enmity will crop up."),
    "29.36": ("BPHS I ch.29 v.36 (p.303)",
              "If the Lagna Pada and Dara Pada are mutually angular or 3rd and 11th or trinal, the native will be a king ruling the earth."),
    "30.39": ("BPHS I ch.30 v.39 (p.310)",
              "If Mercury is in Lagna Pada, the native will lord over whole country while Jupiter will make him a knower of all things. Venus in this context denotes a poet/speaker."),
    "31.11-17": ("BPHS I ch.31 vv.11-17 (p.315)",
                 "Should there be Argala for the Arudha Pada, for the natal ascendant, and for the 7th from both, the native will be famous and fortunate. A malefic or a benefic causing unobstructed Argala aspecting the ascendant will make one famous. Similarly aspect on the 2nd house denotes acquisition of wealth and grains, 3rd house—happiness from co-born; the 4th house—residences, quadrupeds and relatives; the 5th house—sons, grand sons and intelligence, the 6th house—fear from enemies; the 7th house—abundant wealth and marital happiness, the 8th house—difficulties, the 9th house—fortunes; the 10th house—royal honour; the 11th house—gains, and the 12th house—expenses. The Argala by benefics will give various kinds of happiness, while benefic effects will be meddling with malefic Argalas. Argala by both benefics and malefics will yield mixed results."),
    "31.18": ("BPHS I ch.31 v.18 (p.316)",
              "Should there be (unobstructed) Argala for the ascendant, the 5th and 9th the native will doubtlessly become a king and fortunate."),
}
GLOSS = {"29.18": "'The king' = the state or an authority (classical-sources §5: archaic referent glossed).",
         "29.30": "'Lord over the whole country' = authority in its context (§5 gloss).",
         "29.36": "'A king ruling the earth' = authority in its context (§5 gloss).",
         "30.39": "'Lord over whole country' = authority in its context (§5 gloss).",
         "31.11-17": "'Royal honour' = honour from authority; 'sons' = children (§5).",
         "31.18": "'A king' = authority in its context (§5 gloss).",
         "29.34": "'The couple' = the native and partner (§5 neutral reading)."}


def evaluate(positions: dict, lagna: int, moon_waxing=None, natures: dict | None = None) -> dict:
    """positions: graha -> {"rasi", "longitude"}. Returns padas, Argala and matched verses."""
    rasi = {g: p["rasi"] for g, p in positions.items()}
    lon = {g: p["longitude"] for g, p in positions.items()}
    if natures is None:
        from dhana_bhava import natural_natures
        if moon_waxing is None and "sun" in lon and "moon" in lon:
            moon_waxing = (lon["moon"] - lon["sun"]) % 360 < 180
        natures = natural_natures(rasi, moon_waxing)
    padas = bhava_padas(lagna, rasi)
    al, a7 = padas[1], padas[7]
    occ = {}
    for g, s in rasi.items():
        occ.setdefault(s, []).append(g)
    rec = graha_drishti_chart(rasi)["received"]["signs"]
    asp = {int(s): {g for g, v in d.items() if v >= 1} for s, d in rec.items()}
    state = {g: (dignity.dignity_of(g, lon[g]) or {}).get("state") for g in rasi}

    def in_(n, ref=al):
        return occ.get(_from(ref, n), [])

    def asp_(n, ref=al):
        return sorted(asp.get(_from(ref, n), set()))

    matches = []

    def hit(key, clauses, **extra):
        cit, text = V[key]
        matches.append({"key": key, "citation": cit, "text": text, "clauses": clauses,
                        **({"gloss": GLOSS[key]} if key in GLOSS else {}), **extra})

    # vv.8-11: the 11th from AL occupied or aspected
    rel11 = sorted(set(in_(11)) | set(asp_(11)))
    if rel11:
        cl = [{"polarity": "favourable", "why": f"Planets in or aspecting the 11th from the Arudha Lagna: {_names(rel11)}."}]
        strong = [g for g in rel11 if state.get(g) in ("exalted", "own", "moolatrikona")]
        if strong:
            cl.append({"polarity": "favourable", "why": f"Of these, in exaltation or own sign: {_names(strong)}."})
        kinds = {natures.get(g) for g in rel11}
        cl.append({"polarity": None, "why": "Means: " + ("virtuous (benefics only)." if kinds == {"benefic"}
                   else "questionable (malefics only)." if kinds == {"malefic"} else "both.")})
        hit("29.8-11", cl, grahas=rel11)
        # v.12
        if not asp_(12) and asp_(11):
            hit("29.12", [{"polarity": "favourable", "why": "The 11th from the Arudha Lagna is aspected and the 12th is not."}])
        # vv.13-15: the count, and Argala on that 11th
        arg11 = argala(_from(al, 11), rasi, lon, natures)
        hit("29.13-15", [{"polarity": None, "why": f"{len(rel11)} planet(s) in or aspecting the 11th from the Arudha Lagna."}]
            + ([{"polarity": "favourable", "why": "There is Argala on that 11th (see the Argala table)."}] if arg11["places"] else []),
            note="Whether the 12th from the Arudha Lagna is free of malefics is shown with v.16-21 below.")
    # vv.16-17: the 12th "aspected by conjunct both benefics and malefics": a benefic and a
    # malefic standing together, both casting a full aspect on the 12th from the AL.
    in12 = in_(12)
    a12 = set(asp_(12))
    pairs = sorted({(b, m) for b in a12 for m in a12
                    if natures.get(b) == "benefic" and natures.get(m) == "malefic" and rasi[b] == rasi[m]})
    if pairs:
        who = sorted({g for p in pairs for g in p})
        hit("29.16-17", [{"polarity": "adverse",
                          "why": f"Benefics and malefics standing together aspect the 12th from the Arudha Lagna: {_names(who)}."}])
    if {"sun", "venus", "rahu"} <= set(in12):
        hit("29.18", [{"polarity": "adverse", "why": "Surya, Shukr and Rahu are in the 12th from the Arudha Lagna."
                                                    + (" Chandra aspects them." if "moon" in asp_(12) else "")}])
    if "mercury" in in12:
        rel = (set(in12) | set(asp_(12))) - {"mercury"}
        b = [g for g in rel if natures.get(g) == "benefic"]
        m = [g for g in rel if natures.get(g) == "malefic"]
        if b or m:
            hit("29.19", ([{"polarity": "adverse", "why": f"Budh in the 12th from the Arudha Lagna, with or aspected by benefics: {_names(b)}."}] if b else [])
                + ([{"polarity": "adverse", "why": f"Budh there related to malefics: {_names(m)}."}] if m else []))
    if "jupiter" in in12 and set(asp_(12)) - {"jupiter"}:
        hit("29.20", [{"polarity": "adverse", "why": "Guru is in the 12th from the Arudha Lagna and others aspect it."}])
    if {"saturn", "mars"} <= set(in12) and set(asp_(12)) - {"saturn", "mars"}:
        hit("29.21", [{"polarity": "adverse", "why": "Shani and Mangal are in the 12th from the Arudha Lagna and others aspect it."}])
    # v.22 mirrors vv.18-21 for the 11th from the Arudha Lagna
    in11 = in_(11)
    mirror = []
    if {"sun", "venus", "rahu"} <= set(in11):
        mirror.append("Surya, Shukr and Rahu (as v.18)")
    if "mercury" in in11 and (set(in11) | set(asp_(11))) - {"mercury"}:
        mirror.append("Budh with or aspected by others (as v.19)")
    if "jupiter" in in11 and set(asp_(11)) - {"jupiter"}:
        mirror.append("Guru aspected by others (as v.20)")
    if {"saturn", "mars"} <= set(in11) and set(asp_(11)) - {"saturn", "mars"}:
        mirror.append("Shani with Mangal, aspected by others (as v.21)")
    if mirror:
        hit("29.22", [{"polarity": "favourable", "why": "In the 11th from the Arudha Lagna: " + "; ".join(mirror) + "."}])

    # vv.23-28 (7th from AL, and by v.27 the 2nd as well)
    for n, key_extra in ((7, None), (2, "29.27")):
        here = in_(n)
        tag = (f"the {'7th' if n == 7 else '2nd'} from the Arudha Lagna"
               + ("" if n == 7 else " (v.27: the 2nd is read like the 7th)"))
        via = {"via": V["29.27"][0]} if key_extra else {}
        nodes = [g for g in here if g in ("rahu", "ketu")]
        if nodes:
            hit("29.23", [{"polarity": "adverse", "why": f"{_names(nodes)} in {tag}."}], **via)
        jvm = [g for g in here if g in ("jupiter", "venus", "moon")]
        if jvm:
            hit("29.25", [{"polarity": "favourable", "why": f"{_names(jvm)} in {tag}."}], **via)
        ex = [g for g in here if state.get(g) == "exalted"]
        if ex:
            hit("29.26", [{"polarity": "favourable", "why": f"Exalted in {tag}: {_names(ex)}."}], **via)
    ex2 = [g for g in in_(2) if g in ("mercury", "jupiter", "venus") and state.get(g) == "exalted"]
    if ex2:
        hit("29.28", [{"polarity": "favourable", "why": f"Exalted in the 2nd from the Arudha Lagna: {_names(ex2)}."}],
            note="'And be with strength' is not evaluated beyond the exaltation itself.")
    mv = [g for g in in_(2) if g in ("mercury", "venus")]
    if mv:
        hit("29.30", [{"polarity": "favourable", "why": f"In the 2nd from the Arudha Lagna: {_names(mv)}."}])

    # vv.31-36: the Dara Pada (A7) from the Arudha Lagna
    d = _count(al, a7)
    back = _count(a7, al)
    if d in (1, 4, 7, 10, 5, 9):
        hit("29.31-32", [{"polarity": "favourable", "why": f"The Dara Pada is the {_ord(d)} from the Arudha Lagna (an angle or a trine)."}],
            note="The alternative, 'both have strong planets', is not evaluated.")
    elif d in (6, 8, 12):
        hit("29.31-32", [{"polarity": "adverse", "why": f"The Dara Pada is the {_ord(d)} from the Arudha Lagna."}])
    if d in (1, 4, 7, 10, 5, 9):
        hit("29.34", [{"polarity": "favourable", "why": f"The Arudha Lagna and the Dara Pada are {_ord(d)} and {_ord(back)} from each other."}])
    elif d in (6, 8, 12) or back in (6, 8, 12):
        hit("29.34", [{"polarity": "adverse", "why": f"The Arudha Lagna and the Dara Pada are {_ord(d)} and {_ord(back)} from each other."}])
    if d in (1, 4, 7, 10, 3, 11, 5, 9):
        hit("29.36", [{"polarity": "favourable", "why": f"The Arudha Lagna and the Dara Pada are {_ord(d)} and {_ord(back)} from each other."}])

    # ch.30 v.39: Mercury / Jupiter / Venus IN the Arudha Lagna
    mjv = [g for g in in_(1) if g in ("mercury", "jupiter", "venus")]
    if mjv:
        hit("30.39", [{"polarity": "favourable", "why": f"In the Arudha Lagna: {_names(mjv)}."}])

    # ch.31: Argala on every house, on the AL and the 7th from it
    on_house = {h: argala(_from(lagna, h), rasi, lon, natures) for h in range(1, 13)}
    on_al = argala(al, rasi, lon, natures)
    on_al7 = argala(_from(al, 7), rasi, lon, natures)
    free = {h for h, a in on_house.items() if any(_fires(p) for p in a["places"])}
    # vv.11-17 per house: "a malefic or a benefic causing unobstructed Argala ASPECTING"
    # the house. The planet must also cast a full graha drishti on that house's sign.
    for h in sorted(free):
        hs = _from(lagna, h)
        aspecting = sorted({g for p in on_house[h]["places"] if _fires(p) for g in p["argala"]
                            if g in asp.get(hs, set())})
        if not aspecting:
            continue
        hit("31.11-17", [{"polarity": "adverse" if h in (6, 8, 12) else "favourable",
                          "why": f"Unobstructed Argala on your house {h}, and {_names(aspecting)} also aspect"
                                 f"{'s' if len(aspecting) == 1 else ''} it."}],
            house=h)
    al_free = any(_fires(p) for p in on_al["places"])
    al7_free = any(_fires(p) for p in on_al7["places"])
    if al_free and 1 in free and 7 in free and al7_free:
        hit("31.11-17", [{"polarity": "favourable", "why": "Unobstructed Argala on the Arudha Lagna, the Lagn and the 7th from both."}],
            house=None)
    if {1, 5, 9} <= free:
        hit("31.18", [{"polarity": "favourable", "why": "Unobstructed Argala on the Lagn, the 5th and the 9th."}])

    return {
        "source": SOURCE, "confidence": CONFIDENCE,
        "padas": {h: {"sign": s, "name": PADA_NAME[h], "house_from_lagna": _count(lagna, s),
                      "plain_count": pada_plain(_from(lagna, h), rasi[RASI_LORD[_from(lagna, h)]]),
                      "exception_applied": s != pada_plain(_from(lagna, h), rasi[RASI_LORD[_from(lagna, h)]])}
                  for h, s in padas.items()},
        "padas_note": ("Santhanam's printed Arudha chart (p.295) skips the verse's 7th exception in two houses; "
                       "where they differ, 'plain_count' is that figure. The verse (vv.4-5) is followed."),
        "padas_citation": "BPHS I ch.29 vv.1-5 (pp.292-297)",
        "graha_padas": {g: graha_pada(g, rasi[g]) for g in ("sun", "moon") if g in rasi},
        "graha_padas_citation": "BPHS I ch.29 vv.6-7 (p.297); Mars to Saturn not evaluated (needs the stronger of two signs)",
        "argala": {"houses": on_house, "arudha_lagna": on_al, "seventh_from_al": on_al7,
                   "v10_note": "Santhanam's note to ch.31 v.10 (p.314): obstruction happens only in these two quarter cases.",
                   "aspect_convention": "full graha drishti (ch.26)"},
        "matches": matches,
    }
