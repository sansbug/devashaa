"""
K.S. Charak, A Textbook of Varshaphala (1996) — MODERN tier, registered as
`charak_varshaphala` in docs/classical-sources-policy.md.

The stated results of the annual chart that a Mudda period is read against:

  * IN_HOUSE      — each of the nine grahas in each of the twelve houses of the
                    varṣa kuṇḍalī (ch. IX, pp. 93-106)
  * BY_STRENGTH   — each of the seven by its pañcavargīya band, the four labels
                    the book uses for the daśā lords (pp. 73-75); the lagna by
                    its own three (p. 73)
  * HINTS         — the eight "hints about interpretation" (pp. 106-107), which
                    the engine applies mechanically as flags, never as a verdict
  * the favourable / adverse houses the book names per graha (pp. 93-102, 107)

Every entry is a concise, cited, adaptation-classified GIST in this site's own
words (policy §4), not the author's prose. The gist is the *substance* only; the
panel prefixes the attribution ("Charak (1996), p. N, states for X in the Nth").
Classification per policy §5: 'wife'/'women' rendered partner-neutral; illness
clauses kept as the text's stated result with the not-medical-advice framing;
'ruler / government / royal' glossed as those in authority; the source's few
death clauses OMITTED (lifespan is never dated on this site); value-laden
clauses about the character of others omitted. Charak's own caveat (p. 93) is
carried: these results are very generalised and are modified by the lagna and
the sign.

Extracted from the edition pp. 73-75 and 93-107 on 2026-09-29. The §7.5
independent verification pass has NOT yet been run over this corpus; it ships
with `confidence: "corroborated"` in the §7.6 sense (read off the edition, page
by page) and the pass is recorded as pending in SOURCE.
"""

SOURCE = {
    "id": "charak_varshaphala", "text": "A Textbook of Varshaphala", "author": "K.S. Charak",
    "date": "1996", "translator": None, "tier": "modern",
    "verification": "extracted from the edition (pp. 73-75, 93-107) 2026-09-29; policy §7.5 independent pass pending",
}

# ── §5 adaptation vocabulary used by this corpus ─────────────────────────────

_FRAG = {
    "gender": "'wife' / 'women' rendered partner-neutral — the principle is kept, the gendered framing dropped (§5 gender)",
    "health": "illness clauses kept as the text's stated result, not a diagnosis and not medical advice (§5 health)",
    "archaic": "'ruler / government / royal' (and agrarian 'crops and cattle') glossed as those in authority / as a dated referent (§5 gloss)",
    "death": "a death clause in the source is OMITTED — lifespan is never dated on this site (§5; site rule)",
    "moral": "a value-laden clause about the character or standing of others is omitted (§5)",
}
_ACTION = {"gender": "neutralise", "health": "stated-not-fated", "archaic": "gloss", "death": "omit", "moral": "omit"}


def _ad(*classes: str, note: str = "") -> dict:
    cls = list(classes)
    if not cls:
        return {"classes": [], "action": "clean", "note": note or "No dated or value-laden content; ships plainly."}
    parts = [_FRAG[c] for c in cls] + ([note] if note else [])
    return {"classes": cls, "action": "; ".join(dict.fromkeys(_ACTION[c] for c in cls)), "note": ". ".join(parts) + "."}


def _e(page: int, gist: str, *classes: str, note: str = "") -> dict:
    return {"citation": f"Charak p.{page}", "page": page, "gist": gist,
            "adaptation": _ad(*classes, note=note), "confidence": "corroborated"}


# ── the houses the book singles out per graha ────────────────────────────────

FAVOURABLE_HOUSES = {"sun": (3, 6, 10, 11), "mars": (3, 6, 10, 11), "saturn": (3, 6, 11),
                     "rahu": (3, 6, 11), "ketu": (3, 6, 11)}   # pp. 93, 96, 102; p.107 §7 for the nodes
ADVERSE_HOUSES = {"mercury": (6, 8, 12), "jupiter": (6, 8, 12), "venus": (6, 8, 12)}   # pp. 98, 99, 101; p.107 §6

# ── ch. IX — planets in the twelve houses of the annual chart (pp. 93-106) ───

IN_HOUSE = {
    "sun": {
        1: _e(93, "Alone, or with or aspected by malefics: physical ailment, fever, headache, heavy expenditure, illness to the partner, laziness, travel, proneness to anger and trouble from enemies; benefic influence reduces the suffering.", "gender", "health"),
        2: _e(93, "Alone or under malefics: heavy expenditure, strife in the family, financial trouble, disease of the throat or eye, varied disappointments; under benefic influence, acquisition of wealth.", "health"),
        3: _e(93, "Enthusiasm and valour rise; name and fame, dominance over opponents, favours from superiors, good health. Siblings suffer when this Sun is under malefic influence.", "health"),
        4: _e(94, "Suffering to the mother; to crops and cattle (a dated agrarian referent); fear of injury from animals and vehicles; strife with higher-ups, suffering on journeys, proneness to ill health.", "archaic", "health"),
        5: _e(94, "Strife with children and partner, loss of money, heavy expenditure, illness to children, fear from superiors, mental anguish, abdominal discomfort. Benefic influence, by association or aspect, reduces the suffering and may bring the birth of a child.", "gender", "health"),
        6: _e(94, "Destruction of enemies, harmony with friends and near ones, success in litigation, gains in business; adversity to maternal uncles and eye trouble.", "health"),
        7: _e(94, "Physical ailment, eye trouble, loss of wealth, ill health to the partner, fear from foes and thieves while travelling. Benefic influence brings professional elevation and general comforts.", "gender", "health"),
        8: _e(94, "Opposition from near ones, strife at home, physical illness with much suffering, abdominal, eye and perineal disease, loss of dignity, illness to partner and children, loss of wealth, fear from fire, a sudden calamity.", "gender", "health"),
        9: _e(94, "Well aspected or associated: virtuous deeds, a beneficial journey, comforts from partner, children and friends, favours from superiors. Under malefic influence: fall in earnings, disappointments, suffering in travel, strife with siblings.", "gender"),
        10: _e(94, "Favour from those in authority (the text: royal favours), professional elevation, gain in wealth, general progress, comfort of animals and vehicles, dominance over opponents, wise decisions, success in ventures, fulfilment of desires.", "archaic"),
        11: _e(94, "Income from business and other undertakings, rise in status, inflow of wealth, harmony with friends and near ones, acquisition of vehicles, inclination toward virtuous deeds. Under malefic influence it indicates ill health to children.", "health"),
        12: _e(95, "Eye disease, headache, abdominal discomfort, disappointments, illness to the partner, heavy expenditure on treatment of illness, suffering through a false allegation. Under benefic influence the spending goes to virtuous or religious pursuits.", "gender", "health"),
    },
    "moon": {
        1: _e(95, "In Aries, Taurus or Cancer: increased income, good health, support from those around (the text: favours from women), generally good results. In any other sign, and especially if afflicted: loss of wealth, opposition from superiors, disappointments, eye disease, disease of the mouth, cough and asthmatic illness.", "gender", "health"),
        2: _e(95, "Acquisition of wealth, gains in business, association with good people, favours from superiors, general harmony in the family. If afflicted, eye disease.", "health"),
        3: _e(95, "Good for siblings; inclination toward virtuous and religious deeds, fulfilment of a secret desire, support from those around (the text: favours from women). An afflicted Moon is adverse for siblings and inclines the native toward unscrupulous deeds.", "gender"),
        4: _e(95, "Comforts from partner, friends and relatives, gain in professional status, benefit from agriculture and cattle (a dated referent), acquisition of a vehicle, gains from dealing in white-coloured objects. Afflicted by Rāhu or Ketu: abdominal pain and a change of residence.", "gender", "archaic", "health"),
        5: _e(95, "Comfort from children and partner, the birth of a child (the text specifies a daughter), gain of name and fame, acquisition of wealth, improved thinking, inclination toward learning. Afflicted, it is adverse for progeny and distorts thinking.", "gender", note="'birth of a daughter' rendered 'birth of a child' — the sex of a child is not something this site reads"),
        6: _e(96, "Fear from foes, loss of favour from superiors, false allegations with loss of mental peace, chest infections, cough, eye disease, fear from water, an undesired journey, loss of money.", "health"),
        7: _e(96, "Support from those around (the text: favours from women), earnings from business and travel, elevation in profession, gain from dealings in white-coloured objects. Afflicted, it brings illness to the native and the partner.", "gender", "health"),
        8: _e(96, "Loss of earnings and wealth, inclination toward unscrupulous deeds, grave illness and suffering, fear of drowning, dominance by opponents, mental anguish, abdominal pain, eye disease, coughs and colds. Benefic influence on the Moon gives some relief.", "health"),
        9: _e(96, "Virtuous deeds, harmonious relations with friends and relatives, comfort from partner and children, fulfilment of desires, wealth through business and travel, elevation in profession. Affliction to this Moon obstructs the fulfilment of undertakings.", "gender"),
        10: _e(96, "Favours from superiors, professional elevation, dominance over opponents, good health, domestic harmony, fulfilment of desires, access to comforts and wealth."),
        11: _e(96, "Gains from dealing in clothes and white-coloured objects, rise in professional status, domestic harmony, dominance over enemies and opponents."),
        12: _e(96, "Eye disease, coughs and colds, more opponents, quarrels, mental anguish, heavy expenditure in the pursuit of good and religious deeds, general laziness; the expenditure generally exceeds the income.", "health"),
    },
    "mars": {
        1: _e(96, "Fear from fire, weapons and thieves, loss of money, blood disorders, fever, headache, abdominal pain, mental anguish, easy excitability, illness to the partner, proneness to accident and injury (the text adds: a surgical operation).", "gender", "health"),
        2: _e(97, "Eye disease, loss of wealth, fear from fire, enemies and those in authority (the text: the ruler), disappointments, illness to the partner, losses in business, strife with family members.", "gender", "health", "archaic"),
        3: _e(97, "Enhancement of status, acquisition of land, vehicles and wealth, dominance over opponents, favours from those in authority, fulfilment of desires, success through personal effort, success in litigation. When afflicted it harms siblings.", "archaic"),
        4: _e(97, "Separation from friends and relatives, illness to the mother, injury from weapon or fire, loss of cattle or vehicles, losses from land, lack of mental peace, a troublesome journey; the text adds that the native's house may be damaged by fire.", "health", "archaic"),
        5: _e(97, "Adverse for children and partner; abdominal and chest disease, loss of status, disappointments, loss of mental poise, injury from fire or weapon.", "gender", "health"),
        6: _e(97, "Annihilation of opponents, success in litigation, elevation of status, favours from those in authority (the text: the government), acquisition of wealth and vehicles, support from those around (the text: favours from women), varied comforts.", "gender", "archaic"),
        7: _e(97, "Illness to the partner, domestic strife, physical illness to the native, mental anguish, suffering in travel, association with unscrupulous people. The text carries K.N. Rao's note that a marriage arranged for that year may break down.", "gender", "health", note="K.N. Rao's note is stated for 'a marriageable lady'; rendered partner-neutral"),
        8: _e(97, "Serious illness, blood disorders, injury from weapons or accidents, a surgical operation, loss of wealth, domestic strife, secret worries. (Footnote: Ketu in the eighth acts in a similar way.)", "health"),
        9: _e(97, "Loss of wealth, heavy expenditure, disappointments, frequent travel, strife with siblings, proneness to selfishness. The text carries K.N. Rao's note that this is also a combination for a transfer or a foreign journey."),
        10: _e(98, "Favours from those in authority (the text: governmental), promotion in profession, gain in wealth and health, dominance over opponents, success in undertakings. The native may become a centre of controversy.", "archaic"),
        11: _e(98, "Good income, professional elevation, enhanced dignity, gains in business, acquisition of comforts, vehicles and new clothes, satisfaction from children, partner and friends.", "gender"),
        12: _e(98, "Loss of wealth and health, illness to children, fear from those in authority (the text: the ruler), eye disease, disappointments, injury from fire or accidents. Benefic influence on Mars mitigates the evil to a large extent.", "health", "archaic"),
    },
    "mercury": {
        1: _e(98, "Good health, earnings through the application of intelligence, commencement of a new business, enhancement of status, mental happiness, comforts to partner and children, dominance over enemies. Afflicted: domestic strife, illness, lack of comforts.", "gender", "health"),
        2: _e(98, "Domestic harmony, increase in income and wealth, gain of name and fame, dominance over opponents. Affliction here brings domestic strife and loss of money."),
        3: _e(98, "Dominance over opponents through personal courage, peace of mind, comforts from partner and children, gain in wealth and fame, income through business, inclination toward frequent travel.", "gender"),
        4: _e(98, "Favours from superiors, domestic harmony, acquisition of vehicles, land or cattle, comfort to the mother, harmony with near and dear ones. If afflicted: illness to the mother and a change of residence.", "health", "archaic"),
        5: _e(98, "Earnings through the application of intelligence, comforts to and from children, favours from superiors, fulfilment of desires, acquisition of name and fame, higher studies, success in examinations, general comforts."),
        6: _e(99, "Increase in enemies, wasteful expenditure, quarrels, mental anguish, generally ill health.", "gender", "health", note="a clause naming trouble from women is omitted — it carries no structural principle to neutralise"),
        7: _e(99, "Comfort from the partner, gain of status, a comfortable journey, benefit from business transactions, generally favourable results.", "gender"),
        8: _e(99, "Eye disease, fever, chest infections, loss of wealth, heavy expenditure, trouble from opponents. Under benefic influence, the text says, it gives excessively benefic results.", "health"),
        9: _e(99, "Fulfilment of desires, inclination toward religious deeds, good fortune, elevation of professional status, gain in wealth, the birth of a child, success in undertakings, a profitable journey."),
        10: _e(99, "Professional elevation, gain of wealth and vehicles, enhanced dignity, profit from business, inclination toward virtuous deeds. If afflicted, strife with superiors."),
        11: _e(99, "Gain of health, wealth and valour, fulfilment of desires, enhancement of status and dignity, acquisition of wealth through business and travel."),
        12: _e(99, "Physical ailment, mental anguish, eye disease, heavy expenditure, increase in opponents, disfavour from those in authority (the text: governmental). Under benefic influence the spending goes to religious and virtuous pursuits.", "health", "archaic"),
    },
    "jupiter": {
        1: _e(99, "Generally favourable in respect of partner, children, vehicles and wealth; elevation of status (the text adds: promotion in job), gains from business, profitable association with friends, fulfilment of desires. When afflicted: ill health and worry about the profession.", "gender", "health"),
        2: _e(100, "Good income, favours from those in authority (the text: governmental), elevation of status, comforts from partner and children, pilgrimage, acquisition of vehicles, earnings from business and travel.", "gender", "archaic"),
        3: _e(100, "Harmonious association with friends and relatives, gains from business, inclination toward virtuous deeds, gainful travel, favourable for the siblings (footnote: affection for them may grow out of their dire needs). A sudden tragedy or loss of money may also occur."),
        4: _e(100, "Domestic harmony, good income, access to comforts and vehicles, favours from those in authority, monetary gains from lands and business; good for the mother. If afflicted: illness to the mother and a change of residence.", "health", "archaic"),
        5: _e(100, "Acquisition of knowledge and learning, gain in wealth and health, increased fame and dignity, dominance over opponents, favourable for progeny, the birth of a child."),
        6: _e(100, "Frequent quarrels, increase in enemies, disappointments, mental anguish, eye disease, abdominal discomfort, general frailty, disinclination toward religious pursuits.", "health"),
        7: _e(100, "A profitable journey, comfort from the partner, sudden happiness, acquisition of vehicles, professional elevation, gain of wealth, name and fame, development of new and fruitful associations.", "gender"),
        8: _e(100, "Loss of health and wealth, injury or accident, fever, eye disease, losses in business and travel, separation from near and dear ones, general disappointments. On the positive side, the text says, monetary gains to the partner.", "gender", "health"),
        9: _e(100, "Pilgrimage, virtuous deeds, gain of wealth and wisdom, acquisition of land and vehicles, association with near and dear ones, a profitable journey, auspicious events."),
        10: _e(101, "Professional elevation, favours from those in authority (the text: governmental), dominance over opponents, increased income, physical comforts, auspicious events.", "archaic"),
        11: _e(101, "Freedom from disease, comforts from partner, children and friends, acquisition of vehicles and wealth, professional elevation, bestowal of honours and awards, inclination toward virtuous deeds, dominance over opponents, fulfilment of desires.", "gender"),
        12: _e(101, "Heavy expenditure, strife with friends, disfavour from those in authority (the text: the ruler), fear from foes, a fruitless journey, physical illness. Also expenditure on good deeds, like the marriage of a child.", "health", "archaic"),
    },
    "venus": {
        1: _e(101, "Companionship and social warmth (the text: association with women), increase in income, fulfilment of desires, indulgence in luxuries, elevation of professional status, domestic harmony.", "gender"),
        2: _e(101, "Fulfilment of desires, benefit from friends, ample wealth, success in ventures, companionship (the text: association with women), acquisition of vehicles.", "gender"),
        3: _e(101, "Profitable association with friends and siblings, inclination to undertake a journey, good health, gain of money, success in undertakings, companionship (the text: association with women), domestic harmony.", "gender"),
        4: _e(101, "Acquisition of vehicles and wealth, gain from lands and business, favours from those in authority (the text: the government; and, for a government servant, a posting with an official car), comfort to the mother, general material comforts. It may also cause wasteful expenditure, dissociation from near ones, and instability of temper.", "archaic"),
        5: _e(101, "Gain of wealth without effort, much comfort to partner and children, fulfilment of desires, acquisition of knowledge, gain of name and fame, dominance over enemies. It also indicates travel.", "gender"),
        6: _e(102, "Fear from foes, quarrels, instability of temper, loss of wealth, secret worries, physical illness. Also, the text states, separation from the partner or a divorce.", "gender", "health"),
        7: _e(102, "Overindulgence in sensual pursuits, marriage, gain of wealth, profit from business, success in undertakings, earnings from travel, fulfilment of desires, acquisition of vehicles."),
        8: _e(102, "Illness and physical suffering, affliction to partner and children, heavy expenditure, losses in business and travel, eye disease, fear from water.", "gender", "health"),
        9: _e(102, "Elevation of professional status, gain of wealth, good health, benefit from a journey, comforts from partner and children, success in undertakings, inclination toward good deeds; good for work connected with television.", "gender"),
        10: _e(102, "Professional elevation (the text adds: promotion in job), domestic happiness, gain of wealth and dignity, dominance over opponents, acquisition of land, house, vehicles and other material comforts, a gainful journey; good for art, culture and television."),
        11: _e(102, "Earnings from business, a gainful journey, association with friends, enhancement of status and dignity, favours from those in authority, comfort from partner and children; gains from handicrafts, handloom, clothes and musical performances.", "gender", "archaic"),
        12: _e(102, "Heavy expenditure, mental anguish, fear from foes, disfavour from those in authority (the text: the ruler), eye disease, travel. Under benefic influence the spending goes to religious and profitable undertakings and to happy events like a marriage.", "health", "archaic"),
    },
    "saturn": {
        1: _e(102, "Laziness, ill health, fear from enemies, a sudden calamity, disfavour from those in authority, illness to the partner, disappointments. (A clause ranking the native's company as 'the wicked and the low' is omitted.) When the ascendant is Saturn's own sign (Capricorn, Aquarius) or its exaltation sign (Libra), beneficial results may accrue.", "gender", "health", "moral", "archaic"),
        2: _e(103, "Domestic strife, disease of the eye, abdomen or mouth, a false allegation, physical injury, loss of wealth, poor earnings, opposition from near and dear ones, unwelcome travel.", "health"),
        3: _e(103, "Dominance over opponents, excessive enthusiasm, success in undertakings, gain in wealth, favours from those in authority (the text: governmental), strife with siblings.", "archaic"),
        4: _e(103, "Illness to the mother, abdominal pain, fear from opponents and thieves, tensions in respect of land and vehicle, mental anguish, travel.", "health"),
        5: _e(103, "Illness to partner, children and friends, interruption in education, distorted thinking, mental depression, loss of wealth, abdominal ailments.", "gender", "health"),
        6: _e(103, "Good health, increased wealth, annihilation of enemies, success in litigation, relief from ailments, professional rise, gain in wealth, fulfilment of desires.", "health"),
        7: _e(103, "Illness to the partner, change of place of residence, a foreign journey, suffering in travel, fear from enemies, a false allegation, abdominal pain, loss of money.", "gender", "health", note="a clause about association with 'other women' is refused as a value-laden gendered judgement"),
        8: _e(103, "Serious illness, loss of wealth, ill health to partner and children, false allegations, separation from near and dear ones (the text adds: an unpleasant transfer), fall in professional status, obstruction to education, mental anguish.", "death", "gender", "health", note="the text conditions its death clause on the natal daśā; omitted as a whole"),
        9: _e(103, "Misfortune, loss in business, fall from virtue, disappointments, harm to an elder sibling (the text: elder brother) and to enemies.", "gender"),
        10: _e(103, "Success only through excessive effort, losses in business, fall in professional status, a quarrelsome nature, travel, change of residence, domestic strife. When strong or exalted: elevation of status and profits through dealings in metals and dark-coloured objects (like iron and steel)."),
        11: _e(104, "Professional elevation, dominance over opponents, good health, high earnings, change of residence; illness to children or to an elder sibling (the text: elder brother).", "gender", "health"),
        12: _e(104, "Loss of earnings, fear from those in authority, disease of the eye, chest or feet, domestic strife, an unexpected calamity, likelihood of travel.", "health", "archaic"),
    },
    "rahu": {
        1: _e(104, "Mental anguish, loss of dignity, fear from opponents, ill health to the partner, heavy expenditure, distorted thinking, headache, eye disease.", "gender", "health"),
        2: _e(104, "Loss of wealth, ill health, eye disease, disease of the mouth, fear from those in authority (the text: the ruler), losses in business and travel.", "health", "archaic"),
        3: _e(104, "Favours from those in authority (the text: governmental), good health, monetary gains, dominance over enemies and opponents, professional elevation, success in undertakings. May prove adverse to siblings.", "archaic"),
        4: _e(104, "Ill health to the mother, fall from status, suffering in travel, strife with friends and relatives, heavy expenditure, ill health, some sudden calamity.", "health"),
        5: _e(104, "Intellectual deterioration, mental anguish, unfounded fears, loss of money, interruption in studies, abdominal pain. Under benefic influence it may bring the birth of a child (the text: a son), gain in wealth, dominance over opponents.", "gender", "health", note="'birth of a son' rendered 'birth of a child'"),
        6: _e(104, "Good health, loss of enemies, gain in wealth, access to vehicles and comforts, rise in professional status."),
        7: _e(104, "Adverse for the partner: domestic strife, ill health, suffering in travel, fear of fire, water or poison, some secret illness; likelihood of separation from the partner, or a divorce.", "gender", "health"),
        8: _e(104, "Varied ailments, disease of the private parts, abdominal pain, increase in enemies, loss of health and wealth, ill health to partner and children, unfounded fears and phobias, losses in business and travel.", "gender", "health"),
        9: _e(105, "Misfortunes, strife with near and dear ones, disappointments, fall from status, harm from animals and vehicles, travel (including foreign travel), differences with the father."),
        10: _e(105, "Loss of earnings and physical illness. If well associated or well aspected: rise in professional status, increased name and fame, gainful business and travel.", "health"),
        11: _e(105, "Good earnings, good health, gainful business and travel, comfort from partner and children, elevation in professional status.", "gender"),
        12: _e(105, "Loss of wealth, physical ailment, eye disease, fear from those in authority (the text: the ruler), change of place of residence, fear from fire and thieves, losses in business and travel.", "health", "archaic"),
    },
    "ketu": {
        1: _e(105, "Ill health, loss through thefts, loss of dignity, strife with friends and dear ones, fear from fire or injury, numerous worries.", "health"),
        2: _e(105, "Loss of wealth, wasteful expenditure, disease of the eye or mouth, disappointments, fruitless travel.", "health"),
        3: _e(105, "Destruction of opponents, gainful business and travel, favours from those in authority (the text: governmental), ill health to a sibling.", "health", "archaic"),
        4: _e(105, "Ill health to the mother, a vehicular accident, heavy expenditure, disfavour from those in authority (the text: the ruler), loss of mental poise.", "health", "archaic"),
        5: _e(105, "Loss of wealth, interruption in studies, lack of discrimination, illness to children, some sudden calamity, association with unscrupulous people.", "health"),
        6: _e(105, "Loss of enemies, increased wealth, comforts from partner, children and vehicles, professional elevation, fulfilment of desires.", "gender"),
        7: _e(106, "Illness to the partner, lower abdominal ailments, frequent travel, loss in business, unfounded worries.", "gender", "health"),
        8: _e(106, "Varied ailments, heart disease, fear of injury, fire or theft, loss of money, change of residence, fear from those in authority (the text: the ruler). (p.97 footnote: Ketu in the eighth acts like Mars there.)", "health", "archaic"),
        9: _e(106, "Opposition from friends, misfortunes, inclination toward wicked deeds, failure in undertakings, disease of the upper limbs.", "health"),
        10: _e(106, "Fear from those in authority (the text: the ruler), a change of job, loss of wealth, illness to the mother, change of residence, failure in undertakings.", "health", "archaic"),
        11: _e(106, "Good health, increased wealth, domestic comforts, professional elevation, gains in business and travel. (A clause about indulgence in black magic or cheating is omitted.)", "moral"),
        12: _e(106, "Loss of money, fear from foes, losses in business and travel, eye disease, decline in professional status, much mental suffering.", "health"),
    },
}

# ── pp. 73-75 — the daśā lords by pañcavargīya strength ──────────────────────
# Charak p.62: Viśva-bala > 15 parākramī · 10-15 pūrṇa · 5-10 madhya · < 5 alpa;
# the interpretation section labels the same four "very strong / strong / of
# medium strength / weak".

BAND_LABEL = {"parakrami": "very strong", "purna": "strong", "madhya": "of medium strength", "alpa": "weak"}

BY_STRENGTH = {
    "sun": {
        "parakrami": _e(73, "Vehicles, high status, authority."),
        "purna": _e(73, "The same, to a slightly lesser extent; generally favourable."),
        "madhya": _e(73, "Struggles, opposition at the place of work, biliary ailments.", "health"),
        "alpa": _e(73, "Fear from those in authority and from enemies, loss of wealth, ill health, loss of discrimination. The text adds: in houses 3, 6, 10 and 11 the Sun gives favourable results even when weak.", "health"),
    },
    "moon": {
        "parakrami": _e(73, "Increased wealth, companionship (the text: association with women), acquisition of precious stones.", "gender"),
        "purna": _e(73, "Generally good results along the same lines."),
        "madhya": _e(74, "Loss of wealth, opposition from near and dear ones, phlegmatic ailments.", "health"),
        "alpa": _e(74, "Defamation, loss of wealth and virtue, chest diseases.", "health"),
    },
    "mars": {
        "parakrami": _e(74, "A position of authority (the text names the army or police), victory in contest (the text: in war), fulfilment of desires.", "archaic"),
        "purna": _e(74, "Wealth, status, favours from those in authority (the text: the ruler).", "archaic"),
        "madhya": _e(74, "Fear from enemies, inflammatory diseases, biliary ailments.", "health"),
        "alpa": _e(74, "Quarrels, strife at home and at the place of work, fear from foes, blood disorders, fever. The text adds: favourable results accrue when Mars is in houses 3, 6 and 11.", "health"),
    },
    "mercury": {
        "parakrami": _e(74, "Gain of knowledge and learning, attainment of status, increase of fame, a high public appointment (the text: as an ambassador or a minister).", "archaic"),
        "purna": _e(74, "Gain of wealth through friends, a teacher or writings; comforts from near and dear ones."),
        "madhya": _e(74, "Loss of fame, ill temper, injury from a fall, fear of ill health.", "health"),
        "alpa": _e(74, "Distorted reasoning, loss of wealth, fear of imprisonment, foreign travel."),
    },
    "jupiter": {
        "parakrami": _e(74, "Favours from those in authority (the text: the ruler), from a teacher, friends and elders; attainment of fame, wealth and virtue; the birth of a child.", "archaic"),
        "purna": _e(74, "Virtuous deeds, favours from superiors, increased enthusiasm, success in undertakings."),
        "madhya": _e(74, "Illness, poverty, ear ailment, loss of wealth and virtue.", "health"),
        "alpa": _e(74, "Varied troubles and ailments, domestic strife, loss of wealth.", "health"),
    },
    "venus": {
        "parakrami": _e(75, "Gain of wealth, comforts, vehicles and a partner (the text: a wife), good health, general contentment.", "gender"),
        "purna": _e(75, "Gains from business, good food and drink, good clothes, favours from friends and from those around (the text: from women).", "gender"),
        "madhya": _e(75, "Altered thinking, loss of wealth, ill health, opposition from a partner (the text: from the fair sex).", "gender", "health"),
        "alpa": _e(75, "Opposition from near and dear ones, ill health to the partner, distorted reasoning, foreign travel.", "gender", "health"),
    },
    "saturn": {
        "parakrami": _e(75, "A new house, new clothes, acquisition of new land, increased wealth from association with those in authority (the text: the ruler).", "archaic"),
        "purna": _e(75, "Association with elders (the text: older women), acquisition of cattle and vehicles.", "gender", "archaic"),
        "madhya": _e(75, "Fear from foes and thieves, penury, ill health.", "health"),
        "alpa": _e(75, "Varied calamities and disappointments, domestic strife. The text adds: Saturn, like the Sun and Mars, is particularly favourable in houses 3, 6 and 11.", "death"),
    },
}

NODES_STRENGTH_NOTE = _e(75, "There is no such calculation for Rāhu or Ketu, though their daśās are considered. The author suggests Saturn's strength may stand for Rāhu's and Mars' for Ketu's, and says this requires elaborate testing before practical application — so this site does not apply it.")

LAGNA_BY_STRENGTH = {
    "strong": _e(73, "Good health, monetary gains, respect from near and dear ones."),
    "medium": _e(73, "Foreign travel (displacement), loss of fame, undesirable expenditure."),
    "weak": _e(73, "Bad health, loss of money.", "death", "health"),
}
LAGNA_STRENGTH_RULE = "The strength of the lagna depends upon the strength of its lord, and on the association of the lagna with its lord and with natural benefics (Charak p.73, note). This site reads the lagna through its lord's pañcavargīya band: parākramī/pūrṇa → strong, madhya → medium, alpa → weak."

# ── pp. 106-107 — hints about interpretation, applied as flags ───────────────

HINTS = {
    1: _e(106, "All good results of a planet are adversely modified when it is under malefic association or aspect."),
    2: _e(106, "Adverse results are favourably modified when the planet obtains benefic association or aspect."),
    3: _e(106, "All planets give some benefit in the eleventh, the house of gains; a yoga with the eleventh house or its lord ensures fructification."),
    4: _e(106, "Planets in the twelfth, the house of loss, generally indicate loss of money; benefic and malefic influences on them only indicate spending in desirable or undesirable pursuits."),
    5: _e(107, "All planets in the eighth give adverse results, especially for health; the more malefic of them indicate more serious affliction; benefic influences mitigate to some extent.", "health"),
    6: _e(107, "The natural benefics produce adverse results in houses 6, 8 and 12."),
    7: _e(107, "The natural malefics — Sun, Mars, Saturn, Rāhu and Ketu — produce benefic results in houses 3, 6 and 11 (grit in the third, destroying opponents in the sixth, wealth through effort in the eleventh); the Sun additionally in the tenth, where it promises a position of authority."),
    8: _e(107, "The results are modified as the planet is exalted or debilitated, retrograde or direct, combust or not, and by its part in any of the Tājika yogas."),
}
CAVEAT = _e(93, "These results are very generalised, since they get vastly modified by the nature of the lagna as also by the sign in which the planet is located; they give clues, not conclusions.")
FRUCTIFICATION = _e(144, "The yogas manifest in the daśā-antardaśā of the planets taking part in them; the Mudda daśā is the main one. A pūrṇa itthaśāla gives its results in the earlier part of the year, a bhaviṣyat itthaśāla in the later part.")


# ── the engine hook ──────────────────────────────────────────────────────────

_NATURAL_MALEFIC = {"sun", "mars", "saturn", "rahu", "ketu"}
_ORD = {1: "1st", 2: "2nd", 3: "3rd"}


def ordinal(n: int) -> str:
    return _ORD.get(n, f"{n}th")


def lagna_reading(lord_category: str | None) -> dict | None:
    if not lord_category:
        return None
    band = "strong" if lord_category in ("parakrami", "purna") else "medium" if lord_category == "madhya" else "weak"
    return {"band": band, "lord_category": lord_category, "rule": LAGNA_STRENGTH_RULE, **LAGNA_BY_STRENGTH[band]}


def period_reading(lord: str, ctx, pv: dict, yog: dict) -> dict:
    """What the text states for this Mudda lord, from its place and strength in
    the varṣa chart. Geometry from tajika.Ctx; strength from pancha_vargiya;
    the yogas it takes part in from tajika.yogas. Flags, never a verdict."""
    house = ctx.house.get(lord)
    sign = ctx.sign.get(lord)
    seven = lord in pv
    st = ctx.state(lord) if seven else None
    if st is None:
        conj = [q for q in ctx.sign if q != lord and q in pv and ctx.sign[q] == sign]
        asp = [q for q in pv if q != lord and ctx.aspects(q, lord)]
        st = {"sign": sign, "house": house, "conjunct": conj, "aspected_by": asp,
              "malefic_afflicted": any(q in _NATURAL_MALEFIC for q in conj + asp),
              "benefic_aspect": any(ctx.benefic(q) for q in conj + asp),
              "retrograde": bool(ctx.retro.get(lord)), "combust": False, "exalted": False, "debilitated": False}
    cat = pv[lord]["category"] if seven else None
    mods = []
    near = list(dict.fromkeys(list(st.get("conjunct", [])) + list(st.get("aspected_by", []))))
    mal = [q for q in near if q in _NATURAL_MALEFIC]
    ben = [q for q in near if q in pv and ctx.benefic(q)]
    if mal:
        mods.append({"hint": 1, "flag": "malefic association or aspect", "bodies": mal, **HINTS[1]})
    if ben:
        mods.append({"hint": 2, "flag": "benefic association or aspect", "bodies": ben, **HINTS[2]})
    if house == 11:
        mods.append({"hint": 3, "flag": "in the eleventh", **HINTS[3]})
    if house == 12:
        mods.append({"hint": 4, "flag": "in the twelfth", **HINTS[4]})
    if house == 8:
        mods.append({"hint": 5, "flag": "in the eighth", **HINTS[5]})
    if seven and ctx.benefic(lord) and house in (6, 8, 12):
        mods.append({"hint": 6, "flag": "a natural benefic in 6, 8 or 12", **HINTS[6]})
    if lord in _NATURAL_MALEFIC and (house in (3, 6, 11) or (lord == "sun" and house == 10)):
        mods.append({"hint": 7, "flag": "a natural malefic in 3, 6 or 11 (the Sun: 10)", **HINTS[7]})
    dign = [f for f, on in (("exalted", st.get("exalted")), ("debilitated", st.get("debilitated")),
                            ("retrograde", st.get("retrograde")), ("combust", st.get("combust"))) if on]
    if dign:
        mods.append({"hint": 8, "flag": ", ".join(dign), **HINTS[8]})
    part = []
    for pr in yog.get("pairs", []):
        if lord in (pr["a"], pr["b"]):
            other = pr["b"] if pr["a"] == lord else pr["a"]
            if pr.get("itthasala"):
                part.append({"yoga": "itthasala", "type": pr["itthasala"].get("type"), "with": other})
            if pr.get("isarapha"):
                part.append({"yoga": "isarapha", "type": None, "with": other})
    fav = FAVOURABLE_HOUSES.get(lord)
    adv = ADVERSE_HOUSES.get(lord)
    return {
        "lord": lord, "house": house, "house_ordinal": ordinal(house), "sign": sign,
        "state": st, "category": cat, "band": BAND_LABEL.get(cat),
        "vishwa_bala": pv[lord]["vishwa_bala"] if seven else None,
        "house_flag": ("favourable" if fav and house in fav else "adverse" if adv and house in adv else None),
        "in_house": IN_HOUSE[lord][house],
        "by_strength": BY_STRENGTH[lord][cat] if seven else None,
        "strength_note": None if seven else NODES_STRENGTH_NOTE,
        "modifiers": mods, "yogas": part,
        "fructification": FRUCTIFICATION if part else None,
    }
