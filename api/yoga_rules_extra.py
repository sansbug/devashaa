"""Yogas registered by hand from page images, 2026-11-22: the ones the web comparison
(_reading/study/web-vs-devashaa-28.md) found popular sites using but devashaa lacking.

Each verse was read on the printed page. Nothing is blended across texts:
  * BPHS (Santhanam tr.) Vol I ch.36 vv.27-28 — Lakshmi Yoga. tier "sloka", effect quoted
    like the rest of yoga_rules.YOGAS.
  * BPHS (Santhanam) Vol I ch.41 v.28 (printed pp.409-410, page images, 2026-11-23): an
    angle lord related to a trine lord. Registered for its 9th-lord / 10th-lord case only,
    under the popular name Dharma-Karmadhipati (no registered text gives that name). The
    verse does not say what a 'relationship' is; the five kinds are Santhanam's Notes.
  * Phaladipika (Mantresvara; V. Subrahmanya Sastri tr., 2nd ed. 1950) — tier "classical".
    Adh.6 v.57 + vv.63/65/69: Harsha, Sarala, Vimala (what web sites call "Viparita Raja
    Yoga"). Adh.7 vv.26-29: nicabhanga raja yogas. Effects are site-authored GISTS of the
    translation (as phaladipika_rules.py does), not quotations; "king" rendered as
    "authority" and "sons" as "children" (section 5).
    NOT read: Adh.7 v.30 (its English is missing from the scan's text layer and the page
    images are JBIG2, which this toolchain cannot decode). The other nine yogas of
    Adh.6 v.57 (Ava ... Daridra, vv.58-62/64/66-68) are V57_ADVERSE below, read from the
    text layer only (2026-11-22, second pass).
  * Brhat Jataka (Varahamihira; B. Suryanarain Row tr., 1919) ch.15 stanzas 1-2 —
    Pravrajya (renunciation) yoga, tier "classical". Row's Notes are not used.
    Stanzas 3-4 (the Janma-rasi lord / Saturn routes) are not registered yet.
    ch.14 stanzas 1-2 (read on the page images, printed pp.179-180, 2026-11-23): the
    Sun with Mercury and the Moon with Mars in one sign. The stanzas give results but
    no yoga NAME. The names Budh-Aditya and Chandra-Mangal are B.V. Raman's (Three
    Hundred Important Combinations, 1947, nos. 24 and 6): a pointer only, kept in
    `name_source`. His extra conditions (Mercury more than 10 degrees from the Sun;
    the Moon and Mars in mutual aspect) are his own and are NOT applied.
"""

PD = "Phaladīpikā (V. Subrahmanya Sastri tr., 2nd ed. 1950)"
BJ = "Bṛhat Jātaka (B. Suryanarain Row tr., 1919)"

_V57 = ("Adh.6 v.57 states the condition for each house in one sentence: its lord in the 6th, "
        "8th or 12th, OR the house joined or aspected by malefics. devashaa reports which of the "
        "two clauses holds. Popular sites' 'Viparita Raja Yoga' is the first clause only. "
        "Malefics here are the seven-planet set (waning Moon, Sun, Mars, Saturn, afflicted "
        "Mercury); 'aspected' is a full graha drishti. Rahu and Ketu are not counted.")

_NB_NOTE = ("Sastri's note to Adh.7 v.26: some read 'the lord of the exaltation sign' as the "
            "planet that is EXALTED in the debilitation sign. devashaa evaluates both readings, "
            "labels which one holds, and chooses neither. Kendra = whole-sign 1st/4th/7th/10th.")

_TEXT_LAYER = ("Effect read from the 1950 scan's text layer (OCR); the page image is a JBIG2 layer "
               "this toolchain cannot decode, so it is not page-image checked. ")


def _v57_entry(house, name, verse, effect, adapt=""):
    return {"family": "dusthana", "source": "phaladipika",
            "citation": f"{PD}, Adh.6 v.57 (condition), v.{verse} (effect)",
            "effect": effect,
            "condition": f"{house} lord in the 6th, 8th or 12th; or the {house} joined or aspected by malefics.",
            "computability": "clean", "strength_note": _V57, "tier": "classical",
            "confidence": "text_layer", "adaptation": _TEXT_LAYER + adapt}


# The other nine yogas of Adh.6 v.57 (the verse names twelve, one per house). Mostly adverse;
# effects that speak of a lifespan or a loss trip the SENSITIVE pattern and are held on the site.
V57_ADVERSE = {
    "Ava Yoga": _v57_entry("1st", "Ava", 58,
        "Phaladipika gives an insignificant standing, deep poverty and a short-lived life, humiliation, "
        "bad company and conduct, a bodily defect and an unsteady position: the text's dated view, "
        "not a prediction."),
    "Nisswa Yoga": _v57_entry("2nd", "Nisswa", 59,
        "Phaladipika gives speech without kindness, a childless marriage, bad associates, poor teeth "
        "and eyes, little intelligence or learning, no children and no power, and wealth taken by "
        "opponents: the text's dated view, not a prediction.",
        "'A barren wife' rendered as 'a childless marriage' (gender)."),
    "Mriti Yoga": _v57_entry("3rd", "Mriti", 60,
        "Phaladipika gives defeat by opponents, no siblings, little strength or wealth, fatigue from "
        "improper acts and an excitable temperament.",
        "One OCR word ('bhame', likely 'shame' or 'fame') is left out rather than guessed. "
        "'Brothers' rendered as 'siblings'."),
    "Kuhu Yoga": _v57_entry("4th", "Kuhu", 61,
        "Phaladipika gives one bereft of mother, vehicles, friends, comforts, ornaments and relations, "
        "and without a settled home, having lost the one first had.",
        "The verse's last clause (attachment to 'a low female') is omitted (section 5: caste/gender)."),
    "Pamara Yoga": _v57_entry("5th", "Pamara", 62,
        "Phaladipika gives a meagre living and poor judgement, untruthfulness and deceit, losing children "
        "or having none, bad company, irreligion and greed for food."),
    "Dushkriti Yoga": _v57_entry("7th", "Dushkriti", 64,
        "Phaladipika gives losing a spouse and being drawn into adultery, wandering unnoticed, venereal "
        "disease (the text's dated view, not a medical claim), trouble from the state, and contempt from "
        "relations with the distress that follows.",
        "'Lose his wife' rendered as 'losing a spouse'; 'others' wives' as 'adultery' (gender)."),
    "Nirbhagya Yoga": _v57_entry("9th", "Nirbhagya", 66,
        "Phaladipika gives the loss of inherited property (land, house), disregard for the good and for "
        "elders, irreligion, worn clothes, want and great hardship."),
    "Duryoga": _v57_entry("10th", "Duryoga", 67,
        "Phaladipika gives effort that bears no fruit, little regard from the public, betrayal of others, "
        "selfishness, and a life mostly away from home and abroad."),
    "Daridra Yoga": _v57_entry("11th", "Daridra", 68,
        "Phaladipika gives debts, harshness, poverty, ear trouble, poor ties with siblings, entanglement "
        "in wrongful acts, coarse speech and service to others: the text's dated view, not a prediction.",
        "'Brotherhood' rendered as 'ties with siblings'."),
}

EXTRA = {
    "Lakshmi Yoga": {
        "family": "other", "source": "bphs",
        "citation": "BPHS (Santhanam) Vol I, Ch.36, v.27-28 (printed p.377)",
        "effect": "The native with this yoga will be charming, virtuous, kingly in status, "
                  "endowed with many sons and abundant wealth, be famous and be of high moral merits.",
        "condition": "9th lord in a kendra, in its own, mula-trikona or exaltation sign; "
                     "the ascendant lord endowed with strength.",
        "computability": "strength_gated",
        "strength_note": "Gated on 'the ascendant lord endowed with strength' — resolved against "
                         "the Shadbala engine (lagna lord at or above its minimum).",
        "tier": "sloka"},

    "Harsha Yoga": {
        "family": "dusthana", "source": "phaladipika",
        "citation": f"{PD}, Adh.6 v.57 (condition), v.63 (effect)",
        "effect": "Phaladipika gives happiness and enjoyment, good fortune and a strong "
                  "constitution; the person overcomes opponents, shrinks from wrongdoing, is a "
                  "friend of prominent people, and has wealth, standing, friends, fame and children.",
        "condition": "6th lord in the 6th, 8th or 12th; or the 6th joined or aspected by malefics.",
        "computability": "clean", "strength_note": _V57, "tier": "classical"},
    "Sarala Yoga": {
        "family": "dusthana", "source": "phaladipika",
        "citation": f"{PD}, Adh.6 v.57 (condition), v.65 (effect)",
        "effect": "Phaladipika gives a long life, resolve and fearlessness, prosperity, learning, "
                  "children and riches; the person succeeds in what they undertake, overcomes "
                  "opponents, and is upright and widely known.",
        "condition": "8th lord in the 6th, 8th or 12th; or the 8th joined or aspected by malefics.",
        "computability": "clean", "strength_note": _V57, "tier": "classical"},
    "Vimala Yoga": {
        "family": "dusthana", "source": "phaladipika",
        "citation": f"{PD}, Adh.6 v.57 (condition), v.69 (effect)",
        "effect": "Phaladipika gives one who spends little and saves much, is good to everyone, "
                  "happy and independent, has a respectable occupation or conduct, and is known "
                  "for good qualities.",
        "condition": "12th lord in the 6th, 8th or 12th; or the 12th joined or aspected by malefics.",
        "computability": "clean", "strength_note": _V57, "tier": "classical"},

    "Nicabhanga: a lord in a kendra": {
        "family": "nicabhanga", "source": "phaladipika",
        "citation": f"{PD}, Adh.7 v.26 and v.29",
        "effect": "Phaladipika (v.26): the person rises to authority and governs justly. "
                  "(v.29, same condition): high standing with full riches, virtue, the respect "
                  "of peers, power, fame and affluence.",
        "condition": "A planet in its debilitation sign, and the lord of that sign or the lord of "
                     "the planet's exaltation sign in a kendra from the Lagn or the Moon.",
        "computability": "clean", "strength_note": _NB_NOTE, "tier": "classical"},
    "Nicabhanga: the two lords in mutual kendras": {
        "family": "nicabhanga", "source": "phaladipika",
        "citation": f"{PD}, Adh.7 v.27",
        "effect": "Phaladipika: the person reaches the highest standing, respected by others "
                  "who themselves hold authority.",
        "condition": "A planet in its debilitation sign, and the lord of that sign and the lord "
                     "of the planet's exaltation sign in kendras from each other.",
        "computability": "clean", "strength_note": _NB_NOTE, "tier": "classical"},
    "Nicabhanga: aspected by its sign's lord": {
        "family": "nicabhanga", "source": "phaladipika",
        "citation": f"{PD}, Adh.7 v.28",
        "effect": "Phaladipika: the person holds authority and is famous; the text adds there is "
                  "no doubt of it when the debilitated planet is outside the 6th, 8th and 12th.",
        "condition": "A planet in its debilitation sign, aspected by the lord of that sign.",
        "computability": "clean",
        "strength_note": "v.28's stronger form (outside the 6th/8th/12th) is reported in the detail.",
        "tier": "classical"},

    "Pravrajya Yoga": {
        "family": "pravrajya", "source": "brihat_jataka",
        "citation": f"{BJ}, ch.15 stanza 1 (printed pp.182-183), stanza 2 (pp.183-184)",
        "effect": "Brihat Jataka: four or more powerful planets in one sign incline the person to "
                  "renounce worldly life; the most powerful of them names the order followed "
                  "(Mars Sakya, Mercury Ajivika, Jupiter Bhikshu, Moon Vriddha, Venus Charaka, "
                  "Saturn Nirgrantha, Sun Vanyasana). If those planets are combust, the person "
                  "honours renunciates instead of renouncing (stanza 2).",
        "condition": "Four or more of the seven planets in one sign, powerful.",
        "computability": "strength_gated",
        "strength_note": "'Powerful' is resolved against the Shadbala engine: the yoga fructifies "
                         "when four or more of the planets in that sign are strong. Planetary war "
                         "('defeat', stanza 1) is not evaluated. Rahu and Ketu are not counted.",
        "tier": "classical"},
}

_RAMAN = "B.V. Raman, Three Hundred Important Combinations (1947)"

# Brhat Jataka ch.14 (Dwigrahayogadhyaya): results of two planets in one sign. The text
# names no yoga; the popular names are Raman's (name_source). Effects are the stanza's
# result in our words.
CONJ = {
    "Budh-Aditya Yoga": {
        "family": "conjunction", "source": "brihat_jataka",
        "citation": f"{BJ}, ch.14 stanza 1 (printed p.179)",
        "effect": "Brihat Jataka: with the Sun and Mercury in one sign the person is skilful, "
                  "intelligent, renowned and happy.",
        "condition": "The Sun and Mercury in the same sign.",
        "computability": "clean", "tier": "classical", "confidence": "page_image",
        "name_source": f"{_RAMAN}, no. 24. The stanza itself gives no name.",
        "strength_note": "The stanza asks only that the two share a sign. Raman (modern) adds "
                         "that Mercury should be more than 10 degrees from the Sun; that is his "
                         "condition, not the text's, and is not applied. The distance is "
                         "reported in the detail."},
    "Chandra-Mangal Yoga": {
        "family": "conjunction", "source": "brihat_jataka",
        "citation": f"{BJ}, ch.14 stanza 2 (printed p.180)",
        "effect": "Brihat Jataka gives dealing in counterfeits and in saleable goods, and harm "
                  "done to the mother: the text's dated view, not a prediction.",
        "condition": "The Moon and Mars in the same sign.",
        "computability": "clean", "tier": "classical", "confidence": "page_image",
        "adaptation": "The stanza's list of what is sold (women, wives or, in Row's Notes, "
                      "wines, and pots) is not reproduced (section 5: gender).",
        "name_source": f"{_RAMAN}, no. 6. The stanza itself gives no name.",
        "strength_note": "The stanza asks only that the two share a sign. Raman (modern) would "
                         "also count the Moon and Mars in mutual aspect; that is his reading, "
                         "not the text's, and is not applied."},
}

DHARMA_KARMA = {
    "Dharma-Karmadhipati Yoga": {
        "family": "raja", "source": "bphs",
        "citation": "BPHS (Santhanam) Vol I, Ch.41, v.28 (printed pp.409-410)",
        "effect": "The angles are known as Vishnusthaana (i.e. houses of Lord Vishnu) while the "
                  "trines are called Lakshmi sthaanas (i.e. houses of Lakshmi). If the lord of an "
                  "angle establishes relationship with a trinal lord, a Rajayoga will obtain.",
        "condition": "The 10th lord (an angle) related to the 9th lord (a trine): exchange, "
                     "mutual aspect, conjunction, or mutual angular or trinal placement.",
        "computability": "clean", "tier": "sloka", "confidence": "page_image",
        "name_source": "Popular name. No registered text gives it. BPHS ch.41 v.28 states the "
                       "rule for any angle lord and any trine lord; this entry is its "
                       "9th-lord and 10th-lord case.",
        "strength_note": "The verse says only 'relationship'. The five kinds are Santhanam's "
                         "Notes to v.28, which call exchange, mutual aspect and conjunction more "
                         "powerful and the other two lesser; devashaa reports which kinds hold "
                         "and does not weigh them. When one planet rules both the 9th and the "
                         "10th there is no pair to relate, and no yoga is reported. vv.29-34 "
                         "(the pair's divisional dignities) are not evaluated."},
}

EXTRA.update(V57_ADVERSE)
EXTRA.update(DHARMA_KARMA)
EXTRA.update(CONJ)
