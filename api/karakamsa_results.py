"""BPHS Vol I ch.33: the effects of the Karakamsa.

Tier: sloka. The English is R. Santhanam's translation (Ranjan Publications), read from
the PAGE IMAGES of "BPHS - 1 RSanthanam-1.pdf" on 2026-11-21 (PDF page = printed - 1;
ch.33 = printed pp.326-340). The OCR layer was not used. Every verse is returned WHOLE
with the clause(s) this chart meets. Printer's slips repaired: "onh" -> "one", "benfic"
-> "benefic" (v.32), "aud" -> "and" (vv.36-40), "expensess" -> "expenses" and the line-
break hyphen "con-sort" (vv.63-74), "frienly" -> "friendly" (vv.9-11), "Karakasmsa" ->
"Karakamsa" (vv.50-56).

THE KARAKAMSA is the navamsa sign of the Atmakaraka (karakas.karakamsa; ch.33 v.1 and
Santhanam's notes). Where a shared Atma role gives two Karakamsas, nothing is evaluated.

THE FRAME IS NOT STATED. The chapter counts houses "from the Karakamsa" and speaks of
planets "in" it, but neither the verses nor Santhanam's notes say whether the other
planets are read in the navamsa chart or in the rasi chart. Every house-from-Karakamsa
rule is therefore evaluated in BOTH frames, each labelled, and neither is chosen
(the same stance as dasha_effects.frames_for_chart). vv.2-8 depend only on the sign.
"Aspected" = a full graha drishti (ch.26) in the same frame, as in arudha_argala.py.
Exalted / own sign / a malefic's sign are read from the sign in that frame.

NOT REGISTERED, and why:
  * v.12 and vv.30-31: "the divisions of" a planet; the text does not say which.
  * vv.23-24: Gulika is not computed by this engine.
  * vv.25-29: their clauses include "the son of a female slave or of a female
    remarried" (classical-sources §5: slavery and a gendered verdict); the verse is
    shown whole or not at all, so it is left out.
  * vv.47-48: the character of a wife, and widowhood (CLAUDE.md rule 2; as bhava_effects).
  * v.49: length of life (CLAUDE.md rule 2: lifespan is never graded).
  * vv.77-92: they restate vv.36-45 in other words; not registered twice.
  * vv.94-99: Kemadruma "in the Karakamsa, Arudha Lagna and the 2nd and 8th from these"
    (which places must hold malefics is not clear) and dasha timing.
  * Clauses that need strength ("strong Mars", "strong Mercury"), the "Full Moon",
    "six identical vargas" / "benefic Shadvargas", and the Upakheta are not evaluated.
"""

from __future__ import annotations

from drishti import graha_drishti_chart

SOURCE = {"id": "bphs", "text": "Bṛhat Parāśara Horā Śāstra", "author": "Parāśara",
          "translator": "R. Santhanam (Ranjan Publications)", "tier": "sloka"}
CONFIDENCE = "page_image_checked"   # read, then re-read against the page images on 2026-11-21
EXALT = {"sun": 0, "moon": 1, "mars": 9, "mercury": 5, "jupiter": 3, "venus": 11, "saturn": 6}
OWN = {"sun": {4}, "moon": {3}, "mars": {0, 7}, "mercury": {2, 5}, "jupiter": {8, 11},
       "venus": {1, 6}, "saturn": {9, 10}}
MALEFIC_SIGNS = {0, 7, 4, 9, 10}          # owned by Mars, the Sun, Saturn (as bhava_effects)
NAME = {"sun": "Surya", "moon": "Chandra", "mars": "Mangal", "mercury": "Budh", "jupiter": "Guru",
        "venus": "Shukr", "saturn": "Shani", "rahu": "Rahu", "ketu": "Ketu"}
SIGN = ["Mesh", "Vrishabh", "Mithun", "Kark", "Simha", "Kanya",
        "Tula", "Vrishchik", "Dhanu", "Makar", "Kumbh", "Meen"]
FRAME_LABEL = {"navamsa": "in the navamsa chart", "rasi": "in the rasi chart"}


def _n(keys):
    return ", ".join(NAME.get(k, k) for k in keys)


V = {
    "2-8": ("BPHS I ch.33 vv.2-8 (p.327)",
            "If Atmakaraka be in Aries Navamsa, there will be nuisance from rats and cats at all times. A malefic joining will further increase the nuisance. Should Atmakaraka be in Taurus Navamsa, happiness from quadrupeds will result. Should he be in Gemini Navamsa, the native will be afflicted by itch etc. If he be in Cancer Navamsa, there will be fear from water etc. If he be in Leo Navamsa, fear will be from tiger etc. If he be in Virgo Navamsa, itch, corpulence, fire etc. will cause trouble while in Libra Navamsa, the Atmakaraka will make one a trader and skilful in making robes etc. Scorpio Navamsa holding the said planet will bring troubles from snakes etc. and also affliction to mother's breasts. There will be falls from height and conveyances etc. if it is Sagittarius Navamsa that is occupied by Atmakaraka. Capricorn Navamsa in this respect denotes gains from water-dwelling beings and conch, pearl, coral etc. If it is Aquarius Navamsa holding the said planet, the native will construct tanks etc. And in Pisces Navamsa the Atmakaraka will grant final emancipation. A benefic's aspect will remove evils while that of a malefic will cause no good."),
    "9-11": ("BPHS I ch.33 vv.9-11 (p.328)",
             "O Brahmin, if there be only benefics in the Karakamsa and the Navamsa of Lagna and be aspected by benefics, the native will undoubtedly become a king. Should the angles/trines from the Karakamsa be occupied by benefics devoid of malefic association, the native will be endowed with wealth and learning. The combination of benefic and malefic will in this context yield mixed results. If the Upakheta (or upagraha, vide sloka 5 ch. 32) is in its exaltation sign, or own/friendly sign, and is devoid of malefic aspect, the native will go to heavens after death."),
    "13-18": ("BPHS I ch.33 vv.13-18 (p.329)",
              "O Brahmin, if the Sun is in the Karakamsa, the native will be engaged in royal assignments. If the Full Moon is there, he will enjoy pleasures and be a scholar; more so if Venus aspects. If strong Mars is in Karakamsa, he will use the weapon spear, will live through fire and be an alchemist Should strong Mercury be in Karakamsa, he will be skilful in arts and trading, be intelligent and educated. Jupiter in Karakamsa denotes one doing good acts, endowed with spiritualism and Vedic learning. One will be endowed with a longevity of 100 years, be sensuous and will look after state affairs if Venus is in Karakamsa. Saturn in Karakamsa will give such livelihood as due to the native's family. Rahu in Karakamsa denotes a thief, a bowman, a machinery maker, and a doctor treating poisonous afflictions. If Ketu be in Karakamsa, one will deal in elephants and be a thief"),
    "19-22": ("BPHS I ch.33 vv.19-22 (p.329)",
              "Should Rahu and the Sun be in Karakamsa there will be fear from snakes; if a benefic aspects the said combination there will be no fear but a malefic aspects will bring death (through serpents). If Rahu and the Sun occupy benefic Shadvargas, being in Karakamsa, one will be a doctor treating poisonous afflictions while the aspect from Mars on the said combination denotes that the native will burn either his own house or that of others. Mercury's aspect, instead of that of Mars, will not cause the said effects. If Rahu and the Sun be in Karakamsa and be in a malefic's sign in aspect to Jupiter, one will burn neighbouring house while the aspect of Venus will not cause such an event."),
    "32": ("BPHS I ch.33 v.32 (p.331)",
           "A malefic in the 3rd from Karakamsa will make one valorous while a benefic will make one timid."),
    "33-35": ("BPHS I ch.33 vv.33-35 (p.331)",
              "If the 4th from Karakamsa be occupied by Venus and the Moon, one will own palacial (or large) buildings. Similar is the effect of an exalted planet in the said 4th. A house made of stones is denoted by the occupation of Rahu and Saturn. Mars and Ketu indicate a house made of bricks while Jupiter denotes one made of wood. The Sun so related will give a house of grass. If the Moon be in the 4th from Karakamsa, one will have union with his wife in an uncompounded house."),
    "36-40": ("BPHS I ch.33 vv.36-40 (p.332)",
              "If Rahu and Mars are in the 5th from Karakamsa, one will suffer from a pulmonary consumption, more so if the Moon aspects them. The aspect of Mars on the said house will bring boils or ulcers. Ketu's aspect on the said house will cause dysentery and said diseases caused by (impure) water. If Rahu and Gulika be in the house there will be fear from mean people and poison. Should Mercury be in the said house, the native will be an ascetic of the highest order or one holding staff. The Sun and Mars in the said house respectively denote one using a knife and spear. Saturn denotes a bowman in this context. Rahu and Ketu in the said house respectively denote a machinist and a watch maker. Venus in the said house will make one a poet and an eloquent speaker."),
    "41-45": ("BPHS I ch.33 vv.41-45 (pp.332-333)",
              "If Jupiter and the Moon are in Karakamsa or the 5th thereof, the native will be an author. Venus in the said place will make one an ordinary writer while Mercury will give still lesser effects in this respect. Should Jupiter be alone in the said house, one will be a knower of everything, be a writer, and be versed in Vedas and Vedanta philosophy, but not an oratorian or a grammarian. Mars in this respect denotes a logician, Mercury a Mimamsaka (follower of Mimamsa philosophy, one of the six chief systems of Hindu philosophy), Saturn one dull-witted in the assembly, the Sun a musician, the Moon a follower of Sankhya Philosophy (of sage Kapila enumerating 25 true principles with emphasis on final bliss), and versed in rhetorics and singing, and Ketu or Rahu an astrologer. Should Jupiter be related to the said positions (caused by others than him), the effected stated will effectively come to pass. Some say that the 2nd from Karakamsa be also similarly considered."),
    "46": ("BPHS I ch.33 v.46 (p.333)",
           "If the 6th from Karakamsa is occupied by a malefic, the native will be an agriculturist while he will be indolent if a benefic is there. The 3rd from Karakamsa be also similarly considered."),
    "50-56": ("BPHS I ch.33 vv.50-56 (p.334)",
              "If the 9th from Karakamsa is aspected or occupied by a benefic, the native will be truthful, devoted to elders and attached to his own religion. If a malefic is so related as above, one will be attached to his religion in boyhood but will take to falsehood in old age. If Saturn and Rahu are so related as above, one will betray his elders and be averse to ancient learning. If Jupiter and the Sun are so related as above, one will betray his elders and will be disobedient to them. Should Mars and Venus be so related as above, and joining in six identical vargas, a female ill-related to the native will die. Mercury and the Moon so related will cause imprisonment of the native due to association with a female not of his own. If Jupiter is alone related to the 9th from Karakamsa by aspect or by conjunction, the native will be addicted to females and be devoted to sensual enjoyments."),
    "57-60": ("BPHS I ch.33 vv.57-60 (p.335)",
              "If the 10th from Karakamsa be aspected or conjoined by a benefic, the native will have firm riches, be sagacious, strong and intelligent. A malefic so related will cause harm to his profession and deprive him of paternal bliss. Mercury and Venus so related will confer many gains in business (or profession) and will make him do many great deeds. The luminaries so related to the 10th from Karakamsa and if be in aspect to or conjunction with Jupiter the native will acquire a kingdom."),
    "61-62": ("BPHS I ch.33 vv.61-62 (p.335)",
              "If the 11th from Karakamsa be aspected by or conjunct a benefic, the native will enjoy happiness from coborn apart from gaining in every undertaking of his. If a malefic is in the said 11th the native will gain by questionable means, be famous and valorous."),
    "63-74": ("BPHS I ch.33 vv.63-74 (pp.336-337)",
              "If the 12th from Karakamsa has a benefic, the expenses will be on good account while a malefic will cause bad expenses. If the said 12th be vacant then also good effects (in respect of expenses) will follow. If there be a benefic planet in exaltation or in own house in the 12th from Karakamsa or if Ketu is so placed and aspected by or conjunct a benefic one will attain heavens after death. One will attain final emancipation if Ketu is in the 12th (from Karakamsa) identical with Aries/Sagittarius and is aspected by a benefic. If Ketu in the 12th from Karakamsa and be with aspect/conjunction of a malefic one will not attain final emancipation. If the Sun and Ketu are in the said 12th the native will worship Lord Siva. The Moon and Ketu in the said 12th denotes a worshipper of Gauri (a consort of Lord Siva) Venus and Ketu in the said 12th denotes a worshipper of Lakshmi (a consort of Lord Vishnu) and a wealthy person. Mars and Ketu in the said 12th denotes a worshipper of Lord Subramanya (an offspring of Lord Siva). Rahu in the 12th from Karakamsa will make one worship Durga or some mean deity. Ketu alone in the said 12th denotes Subramanya's or Ganesa's worshipper. If Saturn is in the said 12th in a malefic's sign one will worship mean deities. Venus and Saturn in the said 12th in a malefic's sign will also make one worship mean deities. Similar inferences can be drawn from the 6th Navamsa counted from Amatya Karaka's Navamsa."),
    "75-76": ("BPHS I ch.33 vv.75-76 (p.337)",
              "O Brahmin, if there are two malefics in a trine from Karakamsa, the native will have knowledge of Mantras (sacred spells) and Tantras (mystical formularies for the worship of deities for attainment of super-human powers). If a malefic simultaneously aspects the said yoga, the native will use these learnings for malevolent purposes while a benefic's aspect will make him use the same for public good."),
    "93": ("BPHS I ch.33 v.93 (p.339)",
           "Should Ketu be in the 2nd/3rd from Karakamsa, the native will be defective in speech, more so if a malefic aspects Ketu as above."),
}
GLOSS = {"9-11": "'A king' = authority in its context (classical-sources §5 gloss).",
         "13-18": "'Royal assignments' = work for the state or an authority (§5 gloss).",
         "33-35": "'His wife' = the partner (§5).",
         "57-60": "'A kingdom' = authority in its context (§5 gloss)."}
PLANET_IN_KK = {"sun": "the Sun", "jupiter": "Jupiter", "venus": "Venus", "saturn": "Saturn",
                "rahu": "Rahu", "ketu": "Ketu"}          # vv.13-18 clauses evaluated (no strength)


def _from(sign, n):
    return (sign + n - 1) % 12


def evaluate_frame(frame: str, kk: int, sign_of: dict, natures: dict, lagna_navamsa: int | None) -> list:
    occ = {}
    for g, s in sign_of.items():
        occ.setdefault(s, []).append(g)
    rec = graha_drishti_chart(sign_of)["received"]["signs"]
    asp = {int(s): {g for g, v in d.items() if v >= 1} for s, d in rec.items()}
    ben = lambda gs: [g for g in gs if natures.get(g) == "benefic"]       # noqa: E731
    mal = lambda gs: [g for g in gs if natures.get(g) == "malefic"]       # noqa: E731
    at = lambda n: occ.get(_from(kk, n), [])                              # noqa: E731
    seen = lambda n: sorted(asp.get(_from(kk, n), set()))                 # noqa: E731
    rel = lambda n: sorted(set(at(n)) | set(seen(n)))                     # noqa: E731
    fl = FRAME_LABEL[frame]
    out = []

    def hit(key, clauses):
        cit, text = V[key]
        out.append({"key": key, "citation": cit, "text": text, "frame": frame,
                    "clauses": [{**c, "why": c["why"] + f" ({fl})"} for c in clauses],
                    **({"gloss": GLOSS[key]} if key in GLOSS else {})})

    # vv.9-11
    cl = []
    if frame == "navamsa" and lagna_navamsa is not None:
        a, b = occ.get(kk, []), occ.get(lagna_navamsa, [])
        if a and b and not mal(a + b) and ben(sorted(asp.get(kk, set()))) and ben(sorted(asp.get(lagna_navamsa, set()))):
            cl.append({"polarity": "favourable", "why": "Only benefics in the Karakamsa and in the navamsa of the Lagn, both aspected by benefics."})
    kt = [_from(kk, n) for n in (1, 4, 7, 10, 5, 9)]
    in_kt = [g for s in kt for g in occ.get(s, [])]
    if in_kt and not mal(in_kt):
        cl.append({"polarity": "favourable", "why": f"The angles and trines from the Karakamsa hold only benefics: {_n(in_kt)}."})
    elif ben(in_kt) and mal(in_kt):
        cl.append({"polarity": None, "why": f"The angles and trines from the Karakamsa hold benefics and malefics: {_n(in_kt)} (mixed)."})
    if cl:
        hit("9-11", cl)

    # vv.13-18 planets in the Karakamsa
    inkk = at(1)
    cl = [{"polarity": None, "why": f"{NAME[g]} is in the Karakamsa."} for g in inkk if g in PLANET_IN_KK]
    if cl:
        hit("13-18", cl)
    # vv.19-22
    if {"rahu", "sun"} <= set(inkk):
        a = sorted(asp.get(kk, set()) - {"rahu", "sun"})
        hit("19-22", [{"polarity": "adverse", "why": "Rahu and Surya are together in the Karakamsa"
                       + (f"; aspected by {_n(a)}." if a else "; no planet aspects them.")}])
    # v.32 (3rd)
    m3, b3 = mal(at(3)), ben(at(3))
    if m3 or b3:
        hit("32", ([{"polarity": None, "why": f"Malefic in the 3rd from the Karakamsa: {_n(m3)}."}] if m3 else [])
            + ([{"polarity": None, "why": f"Benefic in the 3rd from the Karakamsa: {_n(b3)}."}] if b3 else []))
    # vv.33-35 (4th)
    a4 = at(4)
    cl = []
    if {"venus", "moon"} <= set(a4):
        cl.append({"polarity": "favourable", "why": "Shukr and Chandra are in the 4th from the Karakamsa."})
    ex4 = [g for g in a4 if EXALT.get(g) == _from(kk, 4)]
    if ex4:
        cl.append({"polarity": "favourable", "why": f"Exalted in the 4th from the Karakamsa: {_n(ex4)}."})
    for pair, what in ((("rahu", "saturn"), "a house of stone"), (("mars", "ketu"), "a house of bricks")):
        if set(pair) <= set(a4):
            cl.append({"polarity": None, "why": f"{_n(pair)} in the 4th from the Karakamsa: {what}."})
    for g, what in (("jupiter", "a house of wood"), ("sun", "a house of grass"), ("moon", "union with the partner in an uncompounded house")):
        if g in a4:
            cl.append({"polarity": None, "why": f"{NAME[g]} in the 4th from the Karakamsa: {what}."})
    if cl:
        hit("33-35", cl)
    # vv.36-40 (5th)
    a5, s5 = at(5), seen(5)
    cl = []
    if {"rahu", "mars"} <= set(a5):
        cl.append({"polarity": "adverse", "why": "Rahu and Mangal are in the 5th from the Karakamsa"
                   + (", and Chandra aspects them." if "moon" in s5 else ".")})
    for g in ("mars", "ketu"):
        if g in s5:
            cl.append({"polarity": "adverse", "why": f"{NAME[g]} aspects the 5th from the Karakamsa."})
    for g in ("mercury", "sun", "mars", "saturn", "rahu", "ketu", "venus"):
        if g in a5:
            cl.append({"polarity": None, "why": f"{NAME[g]} is in the 5th from the Karakamsa."})
    if cl:
        hit("36-40", cl)
    # vv.41-45 (Karakamsa or 5th)
    k5 = sorted(set(inkk) | set(a5))
    cl = []
    if {"jupiter", "moon"} <= set(k5):
        cl.append({"polarity": "favourable", "why": "Guru and Chandra in the Karakamsa or the 5th from it."})
    for place, gs in (("the Karakamsa", inkk), ("the 5th from it", a5)):
        if gs == ["jupiter"]:
            cl.append({"polarity": None, "why": f"Guru alone in {place}."})
    for g in ("venus", "mercury", "mars", "saturn", "sun", "moon", "ketu", "rahu"):
        if g in k5 and not ({"jupiter", "moon"} <= set(k5) and g == "moon"):
            cl.append({"polarity": None, "why": f"{NAME[g]} in the Karakamsa or the 5th from it."})
    if cl:
        hit("41-45", cl)
    # v.46 (6th; and the 3rd similarly)
    cl = []
    for n in (6, 3):
        m, b = mal(at(n)), ben(at(n))
        if m:
            cl.append({"polarity": None, "why": f"Malefic in the {n}th from the Karakamsa: {_n(m)}." .replace("3th", "3rd")})
        if b:
            cl.append({"polarity": None, "why": f"Benefic in the {n}th from the Karakamsa: {_n(b)}." .replace("3th", "3rd")})
    if cl:
        hit("46", cl)
    # vv.50-56 (9th): the benefic / malefic / Saturn+Rahu / Jupiter+Sun clauses
    r9 = rel(9)
    cl = []
    if ben(r9):
        cl.append({"polarity": "favourable", "why": f"Benefics in or aspecting the 9th from the Karakamsa: {_n(ben(r9))}."})
    if mal(r9):
        cl.append({"polarity": "adverse", "why": f"Malefics in or aspecting the 9th from the Karakamsa: {_n(mal(r9))}."})
    for pair in (("saturn", "rahu"), ("jupiter", "sun")):
        if set(pair) <= set(r9):
            cl.append({"polarity": "adverse", "why": f"{_n(pair)} both relate to the 9th from the Karakamsa."})
    if cl:
        hit("50-56", cl)
    # vv.57-60 (10th)
    r10 = rel(10)
    cl = []
    if ben(r10):
        cl.append({"polarity": "favourable", "why": f"Benefics in or aspecting the 10th from the Karakamsa: {_n(ben(r10))}."})
    if mal(r10):
        cl.append({"polarity": "adverse", "why": f"Malefics in or aspecting the 10th from the Karakamsa: {_n(mal(r10))}."})
    if {"mercury", "venus"} <= set(r10):
        cl.append({"polarity": "favourable", "why": "Budh and Shukr both relate to the 10th from the Karakamsa."})
    lum = [g for g in ("sun", "moon") if g in r10]
    with_jup = [g for g in lum if "jupiter" in sign_of and (sign_of[g] == sign_of["jupiter"]
                                                          or "jupiter" in asp.get(sign_of[g], set()))]
    if with_jup:
        cl.append({"polarity": "favourable", "why": f"{_n(with_jup)} relate to the 10th from the Karakamsa and have Guru's aspect or company."})
    if cl:
        hit("57-60", cl)
    # vv.61-62 (11th)
    cl = []
    if ben(rel(11)):
        cl.append({"polarity": "favourable", "why": f"Benefics in or aspecting the 11th from the Karakamsa: {_n(ben(rel(11)))}."})
    if mal(at(11)):
        cl.append({"polarity": None, "why": f"Malefics in the 11th from the Karakamsa: {_n(mal(at(11)))}."})
    if cl:
        hit("61-62", cl)
    # vv.63-74 (12th)
    a12, s12, sg12 = at(12), seen(12), _from(kk, 12)
    cl = []
    if not a12:
        cl.append({"polarity": "favourable", "why": "The 12th from the Karakamsa is empty."})
    if ben(a12):
        cl.append({"polarity": "favourable", "why": f"Benefics in the 12th from the Karakamsa: {_n(ben(a12))}."})
    if mal(a12):
        cl.append({"polarity": "adverse", "why": f"Malefics in the 12th from the Karakamsa: {_n(mal(a12))}."})
    if "ketu" in a12:
        rk = set(s12) | (set(a12) - {"ketu"})
        if sg12 in (0, 8) and ben(sorted(s12)):
            cl.append({"polarity": "favourable", "why": f"Ketu in the 12th from the Karakamsa, in {SIGN[sg12]}, aspected by a benefic."})
        if mal(sorted(rk)):
            cl.append({"polarity": "adverse", "why": "Ketu in the 12th from the Karakamsa with a malefic's aspect or company."})
        for g, deity in (("sun", "Siva"), ("moon", "Gauri"), ("venus", "Lakshmi"), ("mars", "Subramanya")):
            if g in a12:
                cl.append({"polarity": None, "why": f"{NAME[g]} and Ketu in the 12th from the Karakamsa ({deity})."})
        if a12 == ["ketu"]:
            cl.append({"polarity": None, "why": "Ketu alone in the 12th from the Karakamsa."})
    if "rahu" in a12:
        cl.append({"polarity": None, "why": "Rahu in the 12th from the Karakamsa."})
    if "saturn" in a12 and sg12 in MALEFIC_SIGNS:
        cl.append({"polarity": None, "why": f"Shani in the 12th from the Karakamsa, in a malefic's sign ({SIGN[sg12]})"
                   + (" with Shukr." if "venus" in a12 else ".")})
    if cl:
        hit("63-74", cl)
    # vv.75-76 two malefics in a trine
    for n in (1, 5, 9):
        m = mal(at(n))
        if len(m) >= 2:
            s = sorted(asp.get(_from(kk, n), set()) - set(m))
            hit("75-76", [{"polarity": None, "why": f"Two malefics ({_n(m)}) in the {['', '1st', '', '', '', '5th', '', '', '', '9th'][n]} from the Karakamsa"
                           + (f"; aspected by {_n(s)}." if s else ".")}])
    # v.93
    for n in (2, 3):
        if "ketu" in at(n):
            hit("93", [{"polarity": "adverse", "why": f"Ketu in the {'2nd' if n == 2 else '3rd'} from the Karakamsa"
                        + (" with a malefic's aspect." if mal(sorted(asp.get(sign_of['ketu'], set()))) else ".")}])
    return out


def evaluate(kk_info: dict, d1: dict, d9: dict, natures: dict, lagna_navamsa: int | None) -> dict:
    """kk_info: karakas.karakamsa(...). d1 / d9: graha -> sign in each chart."""
    kk = kk_info.get("karakamsa")
    if kk is None:
        return {"available": False, "reason": "The Atmakaraka role is shared, so there is no single Karakamsa.",
                "candidates": kk_info.get("candidates")}
    sign_verse = {"key": "2-8", "citation": V["2-8"][0], "text": V["2-8"][1], "frame": "sign",
                  "clauses": [{"polarity": None,
                               "why": f"The Atmakaraka, {NAME.get(kk_info['atmakaraka'], kk_info['atmakaraka'])}, is in {SIGN[kk]} navamsa."}],
                  "note": "The verse's closing aspect clause is not evaluated (the frame is not stated)."}
    return {"available": True, "karakamsa": kk, "atmakaraka": kk_info["atmakaraka"],
            "source": SOURCE, "confidence": CONFIDENCE,
            "matches": [sign_verse]
                       + evaluate_frame("navamsa", kk, d9, natures, lagna_navamsa)
                       + evaluate_frame("rasi", kk, d1, natures, lagna_navamsa),
            "frame_note": ("The chapter does not say whether planets are read in the navamsa or the "
                           "rasi chart; both are shown, labelled, and neither is chosen.")}
