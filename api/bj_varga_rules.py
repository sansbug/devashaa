"""Bṛhat Jātaka, B. Suryanarain Row tr. (1919, public domain): the Moon in each
nakshatra (ch.16) and the forms of the 36 drekkanas (ch.27).

Read from the PAGE IMAGES of "302779100-Brihat-Jataka-English-Translation-B-
Suryanarain-Row-1919-LR.pdf" on 2026-11-19 (ch.16 = PDF pp.183-184, printed
187-188; ch.27 = PDF pp.256-261, printed 260-266). The scan has no text layer.
Being public domain, Row's words are kept as printed (`text`). Where §5 of
docs/classical-sources-policy.md applies, `shown` is the adapted line and
`adaptation` says why. Row's own notes (the masculine/armed/serpent class of a
drekkana) are kept apart as `row_note`.

WHAT IS NOT REGISTERED, and why:
  * Moon in Aśvinī-Punarvasu (ch.16 st.1-4): printed p.186 is MISSING from this
    scan (PDF p.182 = printed 185, PDF p.183 = printed 187).
  * Drekkanas 13-19 (Simha 1 to Thula 1): printed p.262 is MISSING from this scan.
  * Drekkana 27 (Dhanus 3): the printing gives the heading "Stanza 27" and then
    no text before Stanza 28.
  * Drekkanas 30-31 (Makara 3, Kumbha 1): the printing runs the end of st.30 into
    st.31 with no break. Which words belong to which stanza is not certain.
  The second edition on hand (V. Subramanya Sastri) could fill these; it has no
  text layer and is a modern translation (gists only). Not done yet.

HOW CH.27 IS USED: the chapter DESCRIBES each drekkana. It states no natal result.
Row's note under st.36 applies the forms to journeys and to questions about lost
articles. The study view shows them as descriptions, never as a reading of a person.
"""

from __future__ import annotations

SOURCE = {"id": "brihat_jataka", "text": "Bṛhat Jātaka", "author": "Varāhamihira",
          "date": "~550 CE", "translator": "B. Suryanarain Row, 1919 (public domain)",
          "tier": "classical"}
CONFIDENCE = "page_image_checked"   # read, then re-read word by word at zoom on 2026-11-19
CHECK_NOTE = ("Second pass 2026-11-19: every entry re-read against the page image at 1.25-1.5x. "
              "Words match. Punctuation on this low-resolution scan is not always certain.")

_G = {"classes": ["gender"], "action": "neutralise"}

# nakshatra index (1-27) -> entry
MOON_IN_NAKSHATRA = {
    8: {"st": 5, "text": "Control over passions, popular, learned, rich and charitable"},
    9: {"st": 5, "text": "Dissimulator, clever in selfishness, sinful, ungrateful and a cheat"},
    10: {"st": 6, "text": "Many servants and great wealth, enjoying, respector of elders and gods and very enterprising",
         "shown": "Many attendants and great wealth, enjoying, respector of elders and gods and very enterprising",
         "adaptation": {"classes": ["slavery"], "action": "historicise",
                        "note": "'Servants' shown as attendants, as the household of its time."}},
    11: {"st": 6, "text": "sweet speech liberal handsome, fond of travelling and royal servant",
         "shown": "sweet speech liberal handsome, fond of travelling and in the service of a ruler",
         "adaptation": {"classes": ["archaic"], "action": "gloss",
                        "note": "'Royal servant' glossed: in the service of a ruler (government service today)."}},
    12: {"st": 7, "text": "Popular, self acquired property—enjoying and happy"},
    13: {"st": 7, "text": "enterprising — intelligent or (shameless), drunkard, cruel and thievish",
         "variant": "Row prints two readings: 'intelligent' or 'shameless'."},
    14: {"st": 8, "text": "Using various cloths and garlands, good looks and limbs"},
    15: {"st": 8, "text": "Polite, merchant, kind hearted, (not able to endure thirst), sweet tongued and generous",
         "variant": "Row's note: one reading is 'generous' (kripalu), the other 'thirsty' (thripalu)."},
    16: {"st": 9, "text": "Jealous, avaricious, handsome, clever speaker, and quarrelsome, or maker of money",
         "variant": "Row's note: 'clever speaker' or 'clever in earning money'."},
    17: {"st": 9, "text": "Master, or Chief, living in foreign countries, not able to bear hunger and fond of travelling"},
    18: {"st": 10, "text": "Few friends, contented, charitable, very irritable"},
    19: {"st": 10, "text": "Proud, rich, happy, good, steady and enjoying"},
    20: {"st": 11, "text": "good and pleasant wife—proud and a steady friend",
         "shown": "a good and pleasant spouse—proud and a steady friend",
         "adaptation": {**_G, "note": "'Wife' rendered as spouse."}},
    21: {"st": 11, "text": "Polite, knowing, virtuous, many friends, grateful and popular",
         "printed": "The page prints 'Konwing'; read as 'knowing'."},
    22: {"st": 12, "text": "Rich surroundings, learned, good and liberal or liberal to wife, wealthy and renowned",
         "shown": "Rich surroundings, learned, good and liberal or liberal to the spouse, wealthy and renowned",
         "adaptation": {**_G, "note": "'Wife' rendered as spouse."}},
    23: {"st": 12, "text": "Liberal, rich, courageous, fond of music and money"},
    24: {"st": 13, "text": "Plain and truthful, striken from sorrow through females, etc., killer of enemies, adventurous and irreconcilable",
         "shown": "Plain and truthful, stricken with sorrow through relationships, a killer of enemies, adventurous and irreconcilable",
         "adaptation": {**_G, "note": "'Sorrow through females' neutralised to relationships. Row's note gives a second "
                                        "reading, 'one whose wealth has been conquered by females'; it is not shown."}},
    25: {"st": 13, "text": "sorrowful, loss of money through females, skilful and miserly",
         "shown": "sorrowful, loss of money through relationships, skilful and miserly",
         "adaptation": {**_G, "note": "'Through females' neutralised to relationships."}},
    26: {"st": 14, "text": "Good speaker, happy, many children and grand children, successful over enemies and charitable"},
    27: {"st": 14, "text": "Well developed organs, popular, courageous, clean and wealthy."},
}
NAKSHATRA_PAGES = {5: 187, 6: 187, 7: 187, 8: 187, 9: 187, 10: 187, 11: 187, 12: 187, 13: 187, 14: 188}
NAKSHATRA_MISSING = (1, 2, 3, 4, 5, 6, 7)
NAKSHATRA_CAVEAT = ("Row's note (p.188): these results follow the strength of the Moon. A weak Moon "
                    "shows faint traces of them; a strong one shows them to a larger extent.")

# stanza (1-36) -> entry; stanza = 3*sign + part (part 1-3)
DREKKANA = {
    1: {"text": "represents a man with a white cloth round his waist, dark complexion, pretending to protect, fearful red eyes and a lifted axe", "row_note": "masculine and armed", "page": 260},
    2: {"text": "is sketched by Yavanas as representing a woman with red cloth, fond of ornaments and food, pot belly, horse face, thirsty and single-footed", "row_note": "quadruped, feminine", "page": 260},
    3: {"text": "represents a man, cruel, skilled in arts, yellowish, fond of work, unprincipled, with a lifted up stick, angry and covered with purple clothes", "row_note": "masculine and armed", "page": 260},
    4: {"text": "represents a woman with torn ringlets, pot belly, burnt cloth, thirsty, fond of food and ornaments", "row_note": "feminine, fiery", "page": 260},
    5: {"text": "represents a man possessing knowledge of lands, grains, houses, cows, arts ploughing and carts, hungry sheep faced, dirty clothes and shoulders like the hump of an ox", "row_note": "masculine, quadruped", "page": 260},
    6: {"text": "is represented by a man with a body like that of an elephant, white teeth, legs like that of sarabha, yellowish color, and clever in capturing sheep and deer", "row_note": "masculine, quadruped", "page": 260},
    7: {"text": "represents a female, fond of needle work, handsome, fond of ornamentation, issueless, lifted hands, and in menses", "row_note": "feminine", "page": 261},
    8: {"text": "represents a man, living in garden, in armour, with a bow, warlike, armed with weapons, face like that of Garuda, and fond of play, children, ornamentation and wealth", "row_note": "masculine, bird, armed", "page": 261},
    9: {"text": "represents a man, adorned, decked with gems, armoured with quiver and bow, skilled in dancing, drumming and arts, and poet", "row_note": "masculine and armed", "page": 261},
    10: {"text": "represents a man, holding fruits roots and leaves, elephant bodied, residing on sandal trees in the forest, legs like that of Sarabha, and horse necked", "row_note": "quadruped, masculine", "page": 261},
    11: {"text": "represents a female worshipped on the head by lotus flowers, with serpents, full blown youthfulness, living in forests on the branch of palasa and crying", "row_note": "feminine", "page": 261},
    12: {"text": "represents a man covered with serpents, flat faced, and crossing the ocean in a boat in search of wife's jewels", "row_note": "masculine, serpent", "page": 261,
         "shown": "represents a man covered with serpents, flat faced, and crossing the ocean in a boat in search of his spouse's jewels",
         "adaptation": {**_G, "note": "'Wife' rendered as spouse."}},
    20: {"printed": "The page prints 'valture's'; read as 'vulture's'.",
         "text": "represents a man with a vulture's face, hungry and thirsty, holding a pot which is ready to fall and thinking of his wife and children", "row_note": "masculine, bird", "page": 263,
         "shown": "represents a man with a vulture's face, hungry and thirsty, holding a pot which is ready to fall and thinking of his spouse and children",
         "adaptation": {**_G, "note": "'Wife' rendered as spouse."}},
    21: {"text": "say the Yavanas, represents a man, decked with gems, wearing golden quiver and armour and frightening the animals in the wilderness, resembling a monkey and holding in the hand fruits and flesh", "row_note": "masculine, quadruped", "page": 263},
    22: {"text": "represents a woman naked and without ornaments, coming from the middle of a great ocean to the shore, dislocated from her original place, the feet bound by serpents and handsome", "row_note": "feminine, serpent", "page": 263},
    23: {"text": "represents a woman fond of home and happiness for her husband's sake and covered by serpents with a body resembling a tortoise and a pot", "row_note": "feminine, serpent", "page": 263,
         "shown": "represents a woman fond of home and happiness for her partner's sake and covered by serpents with a body resembling a tortoise and a pot",
         "adaptation": {**_G, "note": "'Husband' rendered as partner."}},
    24: {"text": "represents a lion with a broad flat face resembling a tortoise, frightening dogs, deer, boars, and jackals, protecting localities covered with sandalwood trees", "row_note": "masculine, quadruped", "page": 263},
    25: {"text": "represents a man with a human face and a horse's body with a bow in hand residing in a hermitage, protecting sacrificial articles and Maharshis", "row_note": "masculine, quadruped, armed", "page": 263},
    26: {"text": "represents a woman, handsome, with the color of Champaca or gold, picking up the gems from the ocean and sitting in the Bhadrasana fashion", "row_note": "feminine", "page": 264},
    28: {"text": "represents a man covered with much hair, teeth like those of a crocodile, body like that of a pig, keeping yokes, nets and bandages, and with a cruel face", "row_note": "masculine, nigala (chains)", "page": 264},
    29: {"text": "represents a woman, skilled in arts, broad eyes like lotus petals, greenish dark, searching all kinds of articles and wearing iron ear ornaments", "row_note": "feminine", "page": 264},
    32: {"text": "represents a woman, covered with a dirty cloth in a forest, bearing pots on her head and dragging metals in a burnt cart loaded with cotton trees in it", "row_note": "fiery, feminine", "page": 265},
    33: {"text": "indicates a man, dark, with ears covered with long hair, wearing a crown and wandering with pots filled with iron, skin, leaves gum and fruits", "row_note": "masculine", "page": 265},
    34: {"text": "represents a man decked with ornaments, holding in hand sacrificial vessels, pearls, gems, and conch shells and crossing the ocean in a boat in search of jewels for his wife", "row_note": "masculine", "page": 265,
         "shown": "represents a man decked with ornaments, holding in hand sacrificial vessels, pearls, gems, and conch shells and crossing the ocean in a boat in search of jewels for his spouse",
         "adaptation": {**_G, "note": "'Wife' rendered as spouse."}},
    35: {"text": "indicates a woman with a color more beautiful than that of Champaka, surrounded by her attendants, and sailing in a boat decked with long flags in search of the coast of the ocean", "row_note": "feminine", "page": 265},
    36: {"text": "represents a man crying in a pit in a forest, naked and covered over his body by serpents and with a mind distracted by thieves and fire", "row_note": "masculine, serpent", "page": 265},
}
DREKKANA_MISSING = {13: "printed p.262 missing from the scan", 14: "printed p.262 missing from the scan",
                    15: "printed p.262 missing from the scan", 16: "printed p.262 missing from the scan",
                    17: "printed p.262 missing from the scan", 18: "printed p.262 missing from the scan",
                    19: "printed p.262 missing from the scan",
                    27: "the printing has the heading but no text",
                    30: "the printing runs st.30 into st.31 with no break",
                    31: "the printing runs st.30 into st.31 with no break"}
DREKKANA_USE = ("Bṛhat Jātaka ch.27 describes each drekkana; it states no result for a person. Row's "
                "note (p.266) applies the forms to journeys and to questions about lost articles.")
SIGNS = ["Mesha", "Vrishabha", "Mithuna", "Kataka", "Simha", "Kanya",
         "Thula", "Vrischika", "Dhanus", "Makara", "Kumbha", "Meena"]
PART = ["first", "second", "third"]


def moon_in_nakshatra(index: int) -> dict | None:
    e = MOON_IN_NAKSHATRA.get(index)
    if not e:
        return None
    return {**e, "citation": f"Bṛhat Jātaka 16.{e['st']} (Row, p.{NAKSHATRA_PAGES[e['st']]})",
            "shown": e.get("shown", e["text"]), "caveat": NAKSHATRA_CAVEAT, "confidence": CONFIDENCE}


def drekkana_form(sign: int, deg: float) -> dict | None:
    part = min(int(deg // 10), 2)
    st = 3 * sign + part + 1
    e = DREKKANA.get(st)
    label = f"the {PART[part]} drekkana of {SIGNS[sign]}"
    if not e:
        return {"stanza": st, "label": label, "missing": DREKKANA_MISSING.get(st)}
    shown = e.get("shown", e["text"])
    return {**e, "stanza": st, "label": label, "shown": f"The {PART[part]} drekkana of {SIGNS[sign]} {shown}",
            "citation": f"Bṛhat Jātaka 27.{st} (Row, p.{e['page']})", "use": DREKKANA_USE,
            "confidence": CONFIDENCE}
