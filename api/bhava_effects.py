"""
BPHS Vol I chs 12, 14-18, 20-23 — the house-by-house "Effects of the Nth House"
chapters (bhāva-phala), the verses whose own conditions can be tested from the
rāśi chart. Ch.13 (2nd house) is in dhana_bhava.py.

Tier: sloka. The English is R. Santhanam's translation, read from the PAGE IMAGES
(Ranjan Publications; printed page numbers in each citation; PDF page = printed
page - 1) on 2026-11-15. The scan's OCR layer was not used. Printer's slips
repaired: 15.8 "huffaloes" → "buffaloes"; 20.6 "is an angle" → "is [in] an angle";
22.5 n/a. The Sanskrit on the same pages is not re-translated here.

Each verse is returned WHOLE with the clause(s) this chart meets — a verse's
favourable and unfavourable halves travel together.

WHAT IS NOT REGISTERED, and why (so an absence is not "fixed" later):
  * ch.19 (8th house) — it is the longevity chapter; the site never dates or
    grades a lifespan (CLAUDE.md rule 2).
  * Every verse that fixes an event to an age ("in his 32nd year", "at the age
    of 56 …") — chs 15.10-14, 16.18-23, 17.13-22, 20.5/10-28, 22.4/5/8. The site
    gives windows and directions, never dated events.
  * Verses on a spouse's character or fidelity, on illegitimate birth, on sexual
    conduct, on the number of wives (ch.18 vv.3-21 mostly, ch.16 vv.14-15).
  * Verses whose condition needs something this module cannot test honestly:
    a planet's "strength" (ch.20 vv.1-3, ch.21 v.2/12, …), a navāṁśa position,
    Māndi/Gulika, "deep exaltation", combustion (the text gives no orb).
  * ch.15 v.3 — the translation prints "5th lord" where the Sanskrit on the same
    page has the 4th lord (sukhasthānādhipa). Left out until checked against a
    second edition.
  * Number-of-children / number-of-siblings counts, limb tables, twin and
    coiled-birth verses (chs 12.8-15, 14.4/7-13, 16.24-32).

HOW A CONDITION IS READ (the same definitions throughout):
  * houses are whole-sign from the lagna; "angle" = 1/4/7/10, "trine" = 1/5/9;
  * "benefic" / "malefic" = the natural classing of ch.3 v.11 (dhana_bhava
    .natural_natures); the Moon by her phase;
  * "aspected by" = a FULL graha dṛṣṭi (ch.26) on the sign; the partial aspects
    are not counted; the nodes cast none;
  * "with" / "conjunct" / "joins" = in the same sign;
  * exaltation, fall, own sign, enemy's sign = dignity.dignity_of (ch.3);
  * where a verse joins a testable clause to an untestable one, only the
    testable clause is evaluated and the payload says so (`notes`).
"""
from __future__ import annotations

from dhana_bhava import natural_natures, RASI_LORD, KENDRA, TRIKONA, DUSTHANA
from dignity import dignity_of
from drishti import graha_drishti_chart

SOURCE = {"id": "bphs", "text": "Bṛhat Parāśara Horā Śāstra", "author": "Parāśara",
          "translator": "R. Santhanam", "tier": "sloka"}
MOVABLE = (0, 3, 6, 9)
MALEFIC_SIGNS = (0, 7, 4, 9, 10)   # signs owned by Mars, the Sun, Saturn
HI_ORD = ["", "पहले", "दूसरे", "तीसरे", "चौथे", "पाँचवें", "छठे", "सातवें", "आठवें", "नौवें", "दसवें", "ग्यारहवें", "बारहवें"]


def _ord(n):
    return f"{n}{'st' if n % 10 == 1 and n != 11 else 'nd' if n % 10 == 2 and n != 12 else 'rd' if n % 10 == 3 and n != 13 else 'th'}"


def _g(k):
    """A graha placeholder the page fills with the reader's name style."""
    return "{g:%s}" % k


def _gs(ks, hi=False):
    ks = list(ks)
    if not ks:
        return ""
    if len(ks) == 1:
        return _g(ks[0])
    return ", ".join(_g(k) for k in ks[:-1]) + (" और " if hi else " and ") + _g(ks[-1])


class Chart:
    def __init__(self, positions, lagna, moon_waxing=None):
        self.lagna = lagna
        self.rasi = {g: p["rasi"] for g, p in positions.items()}
        self.lon = {g: p.get("longitude") for g, p in positions.items()}
        self.house = {g: (r - lagna) % 12 + 1 for g, r in self.rasi.items()}
        self.nature = natural_natures(self.rasi, moon_waxing)
        rec = graha_drishti_chart(self.rasi)["received"]["signs"]
        self._asp = {int(s): {g for g, v in d.items() if v >= 1} for s, d in rec.items()}
        self._dig = {}

    def lord(self, h):
        return RASI_LORD[(self.lagna + h - 1) % 12]

    def sign_of_house(self, h):
        return (self.lagna + h - 1) % 12

    def occ(self, h):
        return [g for g, hh in self.house.items() if hh == h]

    def asp_house(self, h):
        return self._asp.get(self.sign_of_house(h), set())

    def asp_graha(self, g):
        return {x for x in self._asp.get(self.rasi[g], set()) if x != g}

    def with_(self, g):
        return [x for x in self.rasi if x != g and self.rasi[x] == self.rasi[g]]

    def ben(self, gs):
        return [g for g in gs if self.nature.get(g) == "benefic"]

    def mal(self, gs):
        return [g for g in gs if self.nature.get(g) == "malefic"]

    def dig(self, g):
        if g not in self._dig:
            try:
                d = dignity_of(g, self.lon[g]) if self.lon.get(g) is not None else None
            except Exception:  # noqa: BLE001
                d = None
            self._dig[g] = (d or {}).get("state")
        return self._dig[g]

    def exalted(self, g):
        return self.dig(g) == "exalted"

    def fallen(self, g):
        return self.dig(g) == "debilitated"

    def own(self, g):
        return self.dig(g) in ("own", "moolatrikona") or RASI_LORD[self.rasi[g]] == g

    def enemy(self, g):
        return self.dig(g) == "enemy"

    def kt(self, g):
        return self.house[g] in KENDRA or self.house[g] in TRIKONA


# ── phrases: (english, hindi) for "why this clause applies" ────────────────────
def w_lord_in(h, g, at):
    return (f"your {_ord(h)} lord, {_g(g)}, is in your {_ord(at)} house",
            f"आपके {HI_ORD[h]} भाव के स्वामी {_g(g)} {HI_ORD[at]} भाव में हैं")


def w_in(gs, at):
    return (f"{_gs(gs)} {'is' if len(gs) == 1 else 'are'} in your {_ord(at)} house",
            f"{_gs(gs, True)} आपके {HI_ORD[at]} भाव में {'हैं'}")


def w_with(g, others):
    return (f"{_g(g)} is with {_gs(others)}", f"{_g(g)} के साथ {_gs(others, True)} हैं")


def w_asp_house(h, by):
    return (f"your {_ord(h)} house is aspected by {_gs(by)}", f"आपके {HI_ORD[h]} भाव पर {_gs(by, True)} की पूर्ण दृष्टि है")


def w_asp_graha(g, by):
    return (f"{_g(g)} is aspected by {_gs(by)}", f"{_g(g)} पर {_gs(by, True)} की पूर्ण दृष्टि है")


def w_state(g, en, hi):
    return (f"{_g(g)} is {en}", f"{_g(g)} {hi} हैं")


def _join(parts):
    # one condition a sentence (the site's style: no semicolons)
    en = ". ".join(p[0][0].upper() + p[0][1:] for p in parts)
    hi = "। ".join(p[1] for p in parts)
    return {"en": en + ".", "hi": hi + "।"}


def C(polarity, grahas, *parts):
    return {"polarity": polarity, "grahas": sorted(set(grahas)), "why": _join(parts)}


FAV, ADV = "favourable", "adverse"

# notes (english, hindi) reused across verses
N_STRENGTH = ("The part of this verse that depends on a planet's strength is not evaluated.",
              "इस श्लोक का वह भाग जो ग्रह के बल पर निर्भर है, नहीं जाँचा गया।")
N_COMBUST = ("“Combustion” is not evaluated: the text gives no orb for it.",
             "“अस्त” नहीं जाँचा गया: ग्रंथ उसकी कोई अंश-सीमा नहीं देता।")
N_NAVAMSA = ("The navāṁśa / divisional conditions of this verse are not evaluated here.",
             "इस श्लोक की नवांश / वर्ग संबंधी शर्तें यहाँ नहीं जाँची गईं।")
N_FULL = ("Only full aspects are counted.", "केवल पूर्ण दृष्टि गिनी गई है।")


# ── the verses ─────────────────────────────────────────────────────────────────
def v12_1_2(c):
    l = c.lord(1); out = []
    m = c.mal(c.with_(l))
    if m:
        out.append(C(ADV, [l, *m], w_with(l, m)))
    if c.house[l] in DUSTHANA:
        out.append(C(ADV, [l], w_lord_in(1, l, c.house[l])))
    if c.kt(l):
        out.append(C(FAV, [l], w_lord_in(1, l, c.house[l])))
    if c.fallen(l):
        out.append(C(ADV, [l], w_state(l, "in debilitation", "नीच राशि में")))
    elif c.enemy(l):
        out.append(C(ADV, [l], w_state(l, "in an enemy's sign", "शत्रु की राशि में")))
    b = [g for g in c.ben(c.rasi) if c.kt(g)]
    if b:
        out.append(C(FAV, b, (f"a benefic is in an angle or a trine: {_gs(b)}", f"केंद्र/त्रिकोण में शुभ ग्रह: {_gs(b, True)}")))
    return out


def v12_3(c):
    out = []
    for label_en, label_hi, sign, occ in (("your ascendant", "आपका लग्न", c.lagna, c.occ(1)),
                                          ("your Moon", "आपका चंद्र", c.rasi.get("moon"), c.with_("moon") if "moon" in c.rasi else [])):
        if sign is None:
            continue
        asp = c._asp.get(sign, set())
        m = c.mal(set(occ) | asp)
        if m and not c.ben(asp):
            out.append(C(ADV, m, (f"{label_en} is aspected by or joined with a malefic ({_gs(m)}) and has no benefic's aspect",
                                  f"{label_hi} पाप ग्रह ({_gs(m, True)}) से युक्त/दृष्ट है और उस पर किसी शुभ ग्रह की दृष्टि नहीं")))
    return out


def v12_4(c):
    out = []
    o = c.occ(1)
    if c.ben(o):
        out.append(C(FAV, c.ben(o), w_in(c.ben(o), 1)))
    if c.mal(o):
        out.append(C(ADV, c.mal(o), w_in(c.mal(o), 1)))
    a = c.ben(c.asp_house(1))
    if a:
        out.append(C(FAV, a, w_asp_house(1, a)))
    return out


def v12_5_7(c):
    out = []
    l = c.lord(1)
    who = [g for g in dict.fromkeys([l, "mercury", "jupiter", "venus"]) if g in c.rasi and c.kt(g)]
    if who:
        out.append(C(FAV, who, (f"{_gs(who)} {'is' if len(who) == 1 else 'are'} in an angle or a trine (the ascendant lord here is {_g(l)})",
                                f"{_gs(who, True)} केंद्र/त्रिकोण में हैं (यहाँ लग्नेश {_g(l)} हैं)")))
    a = c.ben(c.asp_graha(l))
    if c.rasi[l] in MOVABLE and a:
        out.append(C(FAV, [l, *a], (f"the ascendant lord {_g(l)} is in a movable sign", f"लग्नेश {_g(l)} चर राशि में हैं"), w_asp_graha(l, a)))
    bjv = [g for g in ("mercury", "jupiter", "venus") if g in c.rasi]
    k = [g for g in bjv if c.house[g] in KENDRA]
    if k:
        out.append(C(FAV, k, (f"{_gs(k)} {'is' if len(k) == 1 else 'are'} in an angle from the ascendant", f"{_gs(k, True)} लग्न से केंद्र में हैं")))
    return out


def v14_1(c):
    b = c.ben(set(c.occ(3)) | c.asp_house(3))
    return [C(FAV, b, (f"your 3rd house is joined or aspected by a benefic: {_gs(b)}", f"आपके तीसरे भाव में शुभ ग्रह है या उस पर शुभ दृष्टि है: {_gs(b, True)}"))] if b else []


def v14_2(c):
    l = c.lord(3); pair = sorted({l, "mars"})
    if all(c.house[g] == 3 for g in pair):
        return [C(FAV, pair, w_in(pair, 3))]
    if all(g in c.asp_house(3) for g in pair):
        return [C(FAV, pair, w_asp_house(3, pair))]
    return []


def v14_3(c):
    l = c.lord(3)
    if l == "mars" or c.rasi[l] != c.rasi["mars"]:
        return []
    m = [g for g in c.mal(c.with_(l)) if g != "mars"]
    if m:
        return [C(ADV, [l, "mars", *m], w_with(l, ["mars", *m]))]
    if c.rasi[l] in MALEFIC_SIGNS:
        return [C(ADV, [l, "mars"], (f"{_g(l)} and {_g('mars')} are together in a sign owned by a malefic", f"{_g(l)} और {_g('mars')} एक साथ पाप ग्रह की राशि में हैं"))]
    return []


def v14_5_6(c):
    l = c.lord(3); out = []
    if c.house[l] == 8 and c.house["mars"] == 8:
        out.append(C(ADV, [l, "mars"], w_in(sorted({l, "mars"}), 8)))
    good = [g for g in dict.fromkeys(["mars", l]) if c.kt(g)]
    if good:
        out.append(C(FAV, good, (f"{_gs(good)} {'is' if len(good) == 1 else 'are'} in an angle or a trine", f"{_gs(good, True)} केंद्र/त्रिकोण में हैं")))
    return out


def v14_14(c):
    g = [x for x in ("sun", "saturn", "mars") if c.house.get(x) == 3]
    return [C(ADV, g, w_in(g, 3))] if g else []


def v15_2(c):
    l4, l1 = c.lord(4), c.lord(1)
    who = [g for g in dict.fromkeys([l4, l1]) if c.house[g] == 4]
    a = c.ben(c.asp_house(4))
    return [C(FAV, [*who, *a], w_in(who, 4), w_asp_house(4, a))] if who and a else []


def v15_4(c):
    l4, l10 = c.lord(4), c.lord(10)
    if l4 != l10 and c.rasi[l4] == c.rasi[l10] and c.kt(l4):
        return [C(FAV, [l4, l10], (f"your 10th lord {_g(l10)} joins your 4th lord {_g(l4)} in your {_ord(c.house[l4])} house, an angle or a trine",
                                   f"आपके दसवें भाव के स्वामी {_g(l10)} और चौथे के स्वामी {_g(l4)} {HI_ORD[c.house[l4]]} भाव (केंद्र/त्रिकोण) में साथ हैं"))]
    return []


def v15_5(c):
    l4 = c.lord(4)
    a = [g for g in c.ben(c.asp_graha(l4))]
    if c.house.get("mercury") == 1 and c.nature.get(l4) == "benefic" and a:
        return [C(FAV, ["mercury", l4, *a], w_in(["mercury"], 1), (f"your 4th lord {_g(l4)} is a benefic", f"चौथे भाव के स्वामी {_g(l4)} शुभ ग्रह हैं"), w_asp_graha(l4, a))]
    return []


def v15_7(c):
    l4 = c.lord(4)
    if c.house[l4] in KENDRA and c.house["venus"] in KENDRA and c.exalted("mercury"):
        return [C(FAV, [l4, "venus", "mercury"], w_lord_in(4, l4, c.house[l4]), (f"{_g('venus')} is in an angle", f"{_g('venus')} केंद्र में हैं"), w_state("mercury", "exalted", "उच्च के"))]
    return []


def v15_8(c):
    if c.house["sun"] == 4 and c.house["moon"] == 9 and c.house["saturn"] == 9 and c.house["mars"] == 11:
        return [C(FAV, ["sun", "moon", "saturn", "mars"], w_in(["sun"], 4), w_in(["moon", "saturn"], 9), w_in(["mars"], 11))]
    return []


def v15_9(c):
    l4 = c.lord(4)
    if c.sign_of_house(4) in MOVABLE and l4 != "mars" and c.rasi[l4] == c.rasi["mars"] and c.house[l4] in (6, 8):
        return [C(ADV, [l4, "mars"], (f"your 4th house is a movable sign", "आपका चौथा भाव चर राशि है"), w_in(sorted({l4, "mars"}), c.house[l4]))]
    return []


def v16_1_3(c):
    l1, l5 = c.lord(1), c.lord(5); out = []
    ok = lambda g: c.own(g) or c.kt(g)
    if ok(l1) and ok(l5):
        out.append(C(FAV, [l1, l5], (f"the lords of your ascendant ({_g(l1)}) and your 5th ({_g(l5)}) are each in own sign, an angle or a trine",
                                     f"लग्नेश ({_g(l1)}) और पंचमेश ({_g(l5)}) दोनों स्वराशि या केंद्र/त्रिकोण में हैं")))
    if c.house[l5] in DUSTHANA:
        out.append(C(ADV, [l5], w_lord_in(5, l5, c.house[l5])))
    return out


def v16_8(c):
    l5 = c.lord(5); parts = []
    if c.house[l5] in DUSTHANA or c.house[l5] == 5:
        parts.append(w_lord_in(5, l5, c.house[l5]))
    if c.fallen(l5):
        parts.append(w_state(l5, "in fall", "नीच के"))
    elif c.enemy(l5):
        parts.append(w_state(l5, "in an enemy's sign", "शत्रु की राशि में"))
    return [C(ADV, [l5], *parts)] if parts else []


def v16_16(c):
    l5 = c.lord(5); parts = []
    if c.exalted(l5):
        parts.append(w_state(l5, "exalted", "उच्च के"))
    if c.house[l5] in (2, 5, 9):
        parts.append(w_lord_in(5, l5, c.house[l5]))
    if l5 != "jupiter" and (c.rasi[l5] == c.rasi["jupiter"] or "jupiter" in c.asp_graha(l5)):
        parts.append((f"{_g(l5)} is joined or aspected by {_g('jupiter')}", f"{_g(l5)} {_g('jupiter')} से युक्त या दृष्ट हैं"))
    return [C(FAV, [l5, "jupiter"] if len(parts) and "jupiter" in parts[-1][0] else [l5], *parts)] if parts else []


def v17_2(c):
    l6 = c.lord(6)
    return [C(ADV, [l6], w_lord_in(6, l6, c.house[l6]))] if c.house[l6] in (6, 1, 8) else []


def v18_1(c):
    l7 = c.lord(7)
    if c.exalted(l7):
        return [C(FAV, [l7], (f"your 7th lord {_g(l7)} is exalted", f"आपके सातवें भाव के स्वामी {_g(l7)} उच्च के हैं"))]
    if c.own(l7):
        return [C(FAV, [l7], (f"your 7th lord {_g(l7)} is in his own sign", f"आपके सातवें भाव के स्वामी {_g(l7)} स्वराशि में हैं"))]
    return []


def v18_2(c):
    l7 = c.lord(7)
    if c.house[l7] in DUSTHANA and not (c.exalted(l7) or c.own(l7)):
        return [C(ADV, [l7], w_lord_in(7, l7, c.house[l7]), (f"that sign is neither his own nor his exaltation", "वह राशि न उनकी अपनी है, न उच्च की"))]
    return []


def v20_4(c):
    l9 = c.lord(9)
    if c.fallen(l9) and c.house["mars"] in (10, 12):
        return [C(ADV, [l9, "mars"], w_state(l9, "debilitated", "नीच के"), w_in(["mars"], c.house["mars"]))]
    return []


def v20_6(c):
    l9 = c.lord(9)
    if l9 != "jupiter" and c.house[l9] in KENDRA and "jupiter" in c.asp_graha(l9):
        return [C(FAV, [l9, "jupiter"], w_lord_in(9, l9, c.house[l9]), w_asp_graha(l9, ["jupiter"]))]
    return []


def v20_7(c):
    l9, l10 = c.lord(9), c.lord(10)
    a = c.ben(c.asp_graha(l10))
    if c.house[l9] == 10 and a:
        return [C(FAV, [l9, l10, *a], w_lord_in(9, l9, 10), (f"your 10th lord {_g(l10)} is aspected by a benefic ({_gs(a)})", f"दसवें भाव के स्वामी {_g(l10)} पर शुभ ग्रह ({_gs(a, True)}) की दृष्टि है"))]
    return []


def v20_29(c):
    l1, l9 = c.lord(1), c.lord(9)
    if l1 != l9 and c.house[l1] == 9 and c.house[l9] == 1 and c.house["jupiter"] == 7:
        return [C(FAV, [l1, l9, "jupiter"], w_lord_in(1, l1, 9), w_lord_in(9, l9, 1), w_in(["jupiter"], 7))]
    return []


def v20_30(c):
    l9 = c.lord(9)
    if c.house.get("rahu") == 5:
        d = RASI_LORD[c.rasi["rahu"]]
        if c.house[d] == 8 and c.fallen(l9):
            return [C(ADV, ["rahu", d, l9], w_in(["rahu"], 5), (f"his dispositor {_g(d)} is in your 8th house", f"उस राशि के स्वामी {_g(d)} आठवें भाव में हैं"), w_state(l9, "in fall", "नीच के"))]
    return []


def v20_31(c):
    l1 = c.lord(1)
    if c.house["saturn"] == 9 and c.house["moon"] == 9 and c.fallen(l1):
        return [C(ADV, ["saturn", "moon", l1], w_in(["saturn", "moon"], 9), w_state(l1, "in fall", "नीच के"))]
    return []


def v21_3(c):
    if "rahu" in c.house and (c.house["rahu"] in KENDRA or c.house["rahu"] in TRIKONA):
        return [C(FAV, ["rahu"], (f"{_g('rahu')} is in your {_ord(c.house['rahu'])} house, an angle or a trine", f"{_g('rahu')} आपके {HI_ORD[c.house['rahu']]} भाव (केंद्र/त्रिकोण) में हैं"))]
    return []


def v21_4(c):
    l10 = c.lord(10); w = c.with_(l10)
    if c.ben(w):
        return [C(FAV, [l10, *c.ben(w)], w_with(l10, c.ben(w)))]
    if c.mal(w):
        return [C(ADV, [l10, *c.mal(w)], w_with(l10, c.mal(w)), ("no benefic is with him", "उनके साथ कोई शुभ ग्रह नहीं"))]
    return []


def v21_5(c):
    a, b = c.mal(c.occ(10)), c.mal(c.occ(11))
    return [C(ADV, [*a, *b], w_in(a, 10), w_in(b, 11))] if a and b else []


def v21_6(c):
    l10 = c.lord(10)
    if c.house[l10] == 8 and c.house.get("rahu") == 8:
        return [C(ADV, [l10, "rahu"], w_lord_in(10, l10, 8), w_with(l10, ["rahu"]))]
    return []


def v21_7(c):
    l10, l7 = c.lord(10), c.lord(7)
    if c.house["saturn"] == 7 and c.house["mars"] == 7 and c.house[l10] == 7 and c.mal(c.with_(l7)):
        return [C(ADV, ["saturn", "mars", l10, l7], w_in(sorted({"saturn", "mars", l10}), 7), w_with(l7, c.mal(c.with_(l7))))]
    return []


def v21_8_10(c):
    l9, l10, l11 = c.lord(9), c.lord(10), c.lord(11); out = []
    if l10 != "jupiter" and c.exalted(l10) and c.rasi[l10] == c.rasi["jupiter"] and c.house[l9] == 10:
        out.append(C(FAV, [l10, "jupiter", l9], w_state(l10, "exalted", "उच्च के"), w_with(l10, ["jupiter"]), w_lord_in(9, l9, 10)))
    if l10 != l11:
        if c.house[l11] == 10 and c.house[l10] == 1:
            out.append(C(FAV, [l10, l11], w_lord_in(11, l11, 10), w_lord_in(10, l10, 1)))
        elif c.rasi[l10] == c.rasi[l11] and c.house[l10] in KENDRA:
            out.append(C(FAV, [l10, l11], (f"your 10th and 11th lords ({_g(l10)}, {_g(l11)}) are together in an angle", f"दसवें और ग्यारहवें भाव के स्वामी ({_g(l10)}, {_g(l11)}) केंद्र में साथ हैं")))
    return out


def v21_11(c):
    g = ["rahu", "sun", "saturn", "mars"]
    return [C(ADV, g, w_in(g, 11))] if all(c.house.get(x) == 11 for x in g) else []


def v21_13(c):
    l10, l11 = c.lord(10), c.lord(11)
    if l10 != l11 and c.house[l10] == 11 and c.house[l11] == 1 and c.house["venus"] == 10:
        return [C(FAV, [l10, l11, "venus"], w_lord_in(10, l10, 11), w_lord_in(11, l11, 1), w_in(["venus"], 10))]
    return []


def v21_14(c):
    l10 = c.lord(10)
    if l10 != "jupiter" and c.exalted(l10) and c.kt(l10) and (c.rasi[l10] == c.rasi["jupiter"] or "jupiter" in c.asp_graha(l10)):
        return [C(FAV, [l10, "jupiter"], w_state(l10, "exalted", "उच्च के"), w_lord_in(10, l10, c.house[l10]), (f"he is with or aspected by {_g('jupiter')}", f"वे {_g('jupiter')} से युक्त या दृष्ट हैं"))]
    return []


def v21_15(c):
    l10, l1 = c.lord(10), c.lord(1)
    if l10 != l1 and c.house[l10] == 1 and c.house[l1] == 1 and c.kt("moon"):
        return [C(FAV, [l10, l1, "moon"], w_in(sorted({l10, l1}), 1), (f"{_g('moon')} is in an angle or a trine", f"{_g('moon')} केंद्र/त्रिकोण में हैं"))]
    return []


def v21_17(c):
    l10, l8 = c.lord(10), c.lord(8)
    if l10 != l8 and c.house[l10] == 8 and c.house[l8] == 10 and c.mal(c.with_(l8)):
        return [C(ADV, [l10, l8, *c.mal(c.with_(l8))], w_lord_in(10, l10, 8), w_lord_in(8, l8, 10), w_with(l8, c.mal(c.with_(l8))))]
    return []


def v21_18(c):
    l10 = c.lord(10); a, b = c.mal(c.occ(10)), c.mal(c.occ(7))
    if c.fallen(l10) and a and b:
        return [C(ADV, [l10, *a, *b], w_state(l10, "in fall", "नीच के"), w_in(a, 10), w_in(b, 7))]
    return []


def v21_19_21(c):
    l10, l1 = c.lord(10), c.lord(1); out = []
    if c.house["moon"] == 10 and c.house[l10] in (10, 2, 6) and c.house[l1] in KENDRA:
        out.append(C(FAV, ["moon", l10, l1], w_in(["moon"], 10), (f"your 10th lord {_g(l10)} is in a trine from the 10th", f"दसवें भाव के स्वामी {_g(l10)} दसवें से त्रिकोण में हैं"), w_lord_in(1, l1, c.house[l1])))
    if c.house[l10] == 9 and c.house[l1] == 10 and c.house["moon"] == 5:
        out.append(C(FAV, [l10, l1, "moon"], w_lord_in(10, l10, 9), w_lord_in(1, l1, 10), w_in(["moon"], 5)))
    return out


def v22_2(c):
    l = c.lord(11); out = []
    if c.house[l] == 11 or c.kt(l):
        out.append(C(FAV, [l], w_lord_in(11, l, c.house[l])))
    if c.exalted(l):
        out.append(C(FAV, [l], w_state(l, "exalted", "उच्च के")))
    return out


def v22_3(c):
    l11, l2 = c.lord(11), c.lord(2)
    if l11 != l2 and c.house[l11] == 2 and c.house[l2] in KENDRA and (l2 == "jupiter" or c.rasi[l2] == c.rasi["jupiter"]):
        return [C(FAV, [l11, l2, "jupiter"], w_lord_in(11, l11, 2), w_lord_in(2, l2, c.house[l2]), w_with(l2, ["jupiter"]))]
    return []


def v22_6(c):
    if c.house["jupiter"] == 11 and c.house["moon"] == 2 and c.house["venus"] == 9:
        return [C(FAV, ["jupiter", "moon", "venus"], w_in(["jupiter"], 11), w_in(["moon"], 2), w_in(["venus"], 9))]
    return []


def v22_7(c):
    g = ["jupiter", "mercury", "moon"]
    return [C(FAV, g, w_in(g, 9))] if all(c.house[x] == 9 for x in g) else []


def v22_9(c):
    l11, l2 = c.lord(11), c.lord(2)
    if l11 != l2 and c.house[l11] == 2 and c.house[l2] == 11:
        return [C(FAV, [l11, l2], w_lord_in(11, l11, 2), w_lord_in(2, l2, 11))]
    return []


def v22_10(c):
    l11, l3 = c.lord(11), c.lord(3)
    if l11 != l3 and c.house[l11] == 3 and c.house[l3] == 11:
        return [C(FAV, [l11, l3], w_lord_in(11, l11, 3), w_lord_in(3, l3, 11))]
    return []


def v22_11(c):
    l = c.lord(11); out = []
    if c.fallen(l):
        out.append(C(ADV, [l], w_state(l, "in fall", "नीच के")))
    m = c.mal(c.with_(l))
    if c.house[l] in DUSTHANA and m:
        out.append(C(ADV, [l, *m], w_lord_in(11, l, c.house[l]), w_with(l, m)))
    return out


def v23_1_4(c):
    l = c.lord(12); out = []; parts = []; who = [l]
    b = c.ben(c.with_(l))
    if b:
        parts.append(w_with(l, b)); who += b
    if c.exalted(l):
        parts.append(w_state(l, "exalted", "उच्च के"))
    elif c.own(l):
        parts.append(w_state(l, "in own house", "स्वराशि में"))
    bo = c.ben(c.occ(12))
    if bo:
        parts.append(w_in(bo, 12)); who += bo
    if parts:
        out.append(C(FAV, who, *parts))
    if l == "moon" and (c.exalted("moon") or c.own("moon") or c.house["moon"] in (11, 9, 5)):
        out.append(C(FAV, ["moon"], (f"{_g('moon')} is your 12th lord", f"{_g('moon')} आपके बारहवें भाव के स्वामी हैं"), w_lord_in(12, "moon", c.house["moon"])))
    return out


def v23_5_6(c):
    l = c.lord(12)
    if c.house[l] in (6, 8):
        return [C(ADV, [l], w_lord_in(12, l, c.house[l]))]
    if c.kt(l):
        return [C(FAV, [l], w_lord_in(12, l, c.house[l]))]
    return []


def v23_10(c):
    l = c.lord(12); bo = c.ben(c.occ(12))
    if not bo:
        return []
    if c.exalted(l):
        return [C(FAV, [*bo, l], w_in(bo, 12), w_state(l, "exalted", "उच्च के"))]
    b = c.ben(set(c.with_(l)) | c.asp_graha(l))
    if b:
        return [C(FAV, [*bo, l, *b], w_in(bo, 12), (f"your 12th lord {_g(l)} is joined or aspected by a benefic ({_gs(b)})", f"बारहवें भाव के स्वामी {_g(l)} शुभ ग्रह ({_gs(b, True)}) से युक्त या दृष्ट हैं"))]
    return []


def _v23_11_12(c, pick, pol):
    l = c.lord(12)
    w, o = pick(c.with_(l)), pick(c.occ(12))
    a1, a2 = pick(c.asp_graha(l)), pick(c.asp_house(12))
    if w and o and a1 and a2:
        return [C(pol, [l, *w, *o, *a1, *a2], w_with(l, w), w_in(o, 12), w_asp_graha(l, a1), w_asp_house(12, a2))]
    return []


def v23_11(c):
    return _v23_11_12(c, c.mal, ADV)


def v23_12(c):
    return _v23_11_12(c, c.ben, FAV)


def v23_13(c):
    m = [g for g in ("saturn", "mars") if c.house[g] == 12]
    if m and not c.ben(c.asp_house(12)):
        return [C(ADV, m, w_in(m, 12), ("no benefic aspects your 12th house", "आपके बारहवें भाव पर किसी शुभ ग्रह की दृष्टि नहीं"))]
    return []


def v23_14(c):
    l1, l12 = c.lord(1), c.lord(12)
    if l1 != l12 and c.house[l1] == 12 and c.house[l12] == 1 and c.house["venus"] == 1:
        return [C(FAV, [l1, l12, "venus"], w_lord_in(1, l1, 12), w_lord_in(12, l12, 1), w_in(["venus"], 1))]
    return []


def _V(ch, verse, pages, house, fn, text, *notes):
    return {"chapter": ch, "verse": verse, "house": house, "fn": fn, "text": text,
            "citation": f"BPHS I ch.{ch} v{'v' if '-' in verse else ''}.{verse} ({'pp' if '-' in pages else 'p'}.{pages})",
            "notes": {"en": [n[0] for n in notes], "hi": [n[1] for n in notes]}}


VERSES = [
    _V(12, "1-2", "126-127", 1, v12_1_2, "Should the ascendant lord be conjunct a malefic or be in the 8th, 6th or 12th, physical felicity will diminish. If he is in an angle/trine there will be at all times comforts of the body. If the ascendant lord is in debilitation, combustion or enemy's sign, there will be diseases. With a benefic in an angle or trine, all diseases will disappear.", N_COMBUST),
    _V(12, "3", "127", 1, v12_3, "There will not be bodily health if the ascendant or the Moon be aspected by or conjunct a malefic, being devoid of a benefic's aspect.", N_FULL),
    _V(12, "4", "127", 1, v12_4, "A benefic in the ascendant will give a pleasing appearance, while a malefic will make one bereft of good appearance. Felicity of the body will be enjoyed if the ascendant is aspected by or conjunct a benefic.", N_FULL),
    _V(12, "5-7", "127-128", 1, v12_5_7, "If the ascendant lord, Mercury, Jupiter or Venus be in an angle or in a trine, the native will be longlived, wealthy, intelligent and liked by the king. Fame, wealth, abundant pleasures and comforts of the body will be acquired if the ascendant lord is in a movable sign and be aspected by a benefic planet. One will be endowed with royal marks (of fortune) if Mercury, Jupiter or Venus be in the ascendant along with the Moon, or be in angle from the ascendant."),
    _V(14, "1", "137", 3, v14_1, "O Brahmin, I now tell you about the 3rd house. Should the 3rd house be conjunct or aspected by a benefic, the native will be endowed with co-born and be courageous.", N_FULL),
    _V(14, "2", "138", 3, v14_2, "If the 3rd lord along with Mars aspects the 3rd house the native will enjoy good results due to the 3rd house. Alternatively these two planets may be in the 3rd itself.", N_FULL),
    _V(14, "3", "138", 3, v14_3, "Destruction at once of coborn will come to pass if the said 2 planets are together with a malefic or in a sign owned by a malefic."),
    _V(14, "5-6", "139", 3, v14_5_6, "Should the 3rd lord and Mars be together in the 8th, destruction of coborn will result. Happiness in this respect will come to pass if Mars or the 3rd lord is in an angle or in a trine or in exaltation/friendly divisions.", N_NAVAMSA),
    _V(14, "14", "141", 3, v14_14, "The Sun in the 3rd will destroy the preborn. The afterborn will be destroyed if Saturn is found in the 3rd. In the same situation Mars will destroy both the preborn and later born."),
    _V(15, "2", "142", 4, v15_2, "One will have residential comforts in full degree if the 4th is occupied by its lord or by the ascendant lord and be aspected by a benefic.", N_FULL),
    _V(15, "4", "142", 4, v15_4, "If the 10th lord joins the 4th lord in an angle or in a trine, the native will acquire beautiful mansions."),
    _V(15, "5", "142", 4, v15_5, "Should Mercury be in the ascendant while the 4th lord being a benefic is aspected by another benefic, the native will be honoured by his relatives.", N_FULL),
    _V(15, "7", "143", 4, v15_7, "The native's mother will be happy if the 4th lord is in an angle while Venus is also in an angle as Mercury is exalted."),
    _V(15, "8", "143", 4, v15_8, "The Sun in the 4th, Moon and Saturn in the 9th and Mars in the 11th—this yoga will confer cows and buffaloes on the native."),
    _V(15, "9", "143", 4, v15_9, "Should the 4th house be a movable one while its lord and Mars are together in the 6th or the 8th house, the native will be dumb."),
    _V(16, "1-3", "145", 5, v16_1_3, "O Brahmin, now I tell you the effects related to the 5th house. If the lords of the ascendant and the 5th are in their own signs or in an angle or in a trine, one will enjoy thorough happiness through his children. Should the 5th lord be in the 6th, 8th or 12th, there will be no offspring. Should the lord of the 5th be combust or be with malefics and be weak, there will be no children; even if per chance issues are obtained they will only quit the world soon.", N_COMBUST, N_STRENGTH),
    _V(16, "8", "146", 5, v16_8, "If the 5th lord is in the 6th, 8th or the 12th or be in an inimical sign or be in fall or in the 5th itself, the native will beget issues with difficulty."),
    _V(16, "16", "149", 5, v16_16, "If the 5th lord is exalted or be in the 2nd, 5th or 9th from the ascendant or be conjunct or aspected by Jupiter, obtainment of children will be there.", N_FULL),
    _V(17, "2", "152", 6, v17_2, "Should the 6th lord be in the 6th itself or in the ascendant/8th, there will be ulcers or bruises on the body. The sign becoming the 6th house will lead to the knowledge of the concerned limb."),
    _V(18, "1", "160", 7, v18_1, "O excellent of the Brahmins, listen to me detailing the effects of the 7th house. If the 7th lord is in his own sign or in exaltation, one will derive full happiness through his wife (and marriage)."),
    _V(18, "2", "160", 7, v18_2, "Should the 7th lord be in the 6th, 8th or the 12th, the wife will be sickly. This, however, does not apply to own house or exaltation placement as above."),
    _V(20, "4", "173", 9, v20_4, "If the 9th lord is debilitated while the 2nd/4th from the 9th is occupied by Mars, the native's father is poor."),
    _V(20, "6", "174", 9, v20_6, "If the 9th lord is [in] an angle in aspect to Jupiter, the native's father will be a king endowed with conveyances or be equal to a king.", N_FULL),
    _V(20, "7", "174", 9, v20_7, "Should the lord of the 9th be in the 10th while the 10th lord being aspected by a benefic the native's father will be very rich and famous.", N_FULL),
    _V(20, "29", "177", 9, v20_29, "Should the ascendant lord be in the 9th as the 9th lord is in the ascendant, and Jupiter is in the 7th, there will be gains of wealth and conveyances."),
    _V(20, "30", "177", 9, v20_30, "If Rahu is in the 9th from the 9th (i.e. 5th from the ascendant), as his dispositor is in the 8th from the ascendant and the 9th lord is in fall, the native will be devoid of fortunes."),
    _V(20, "31", "178", 9, v20_31, "Should Saturn be in the 9th along with the Moon as the ascendant lord is in fall, the native will acquire food by begging."),
    _V(21, "3", "179", 10, v21_3, "If the 10th lord is devoid of strength, the native will face obstructions in his work. If Rahu is in an angle or in a trine, he will perform religious sacrifices like Jyotishtoma.", N_STRENGTH),
    _V(21, "4", "179", 10, v21_4, "If the 10th lord is with a benefic or be in an auspicious house, one will always gain through royal patronage and in business. In a contrary situation, only opposite results will come to pass.",
       ("“An auspicious house” is not defined in the verse and is not evaluated; only who is with the 10th lord is.", "“शुभ स्थान” श्लोक में परिभाषित नहीं है और नहीं जाँचा गया; केवल यह देखा गया कि दशमेश के साथ कौन है।")),
    _V(21, "5", "180", 10, v21_5, "Should the 10th and 11th be both occupied by malefics the native will indulge only in bad deeds and will defile his own men."),
    _V(21, "6", "180", 10, v21_6, "If the lord of the 10th is relegated to the 8th along with Rahu, the native will hate others, be a great fool and will do bad deeds."),
    _V(21, "7", "180", 10, v21_7, "If Saturn, Mars and the 10th lord are in the 7th as the 7th lord is with a malefic, the native will be fond of carnal pleasures and of filling his belly."),
    _V(21, "8-10", "180-181", 10, v21_8_10, "Should the 10th lord be in exaltation and be in the company of Jupiter as the 9th lord is in the 10th the native will be endowed with honour, wealth, and valour. One will lead a happy life if the 11th lord is in the 10th and the 10th lord is in the ascendant or if the lords of the 10th and 11th are conjunct in an angle. Should the 10th lord in strength be in Pisces along with Jupiter, the native will doubtless obtain robes, ornaments and happiness.", N_STRENGTH),
    _V(21, "11", "181", 10, v21_11, "Should Rahu, Sun, Saturn and Mars be in the 11th, the native will incur cessation of his duties."),
    _V(21, "13", "182", 10, v21_13, "Should the 10th lord be in the 11th while the 11th lord is in the ascendant and Venus is in the 10th, the native will be endowed with precious stones."),
    _V(21, "14", "182", 10, v21_14, "If the lord of the 10th is exalted in an angle or a trine and be in the company of or in aspect to Jupiter, one will be endowed with (worthy) deeds.", N_FULL),
    _V(21, "15", "182", 10, v21_15, "Should the 10th lord be in the ascendant along with the ascendant lord as the Moon is in an angle or in a trine, the native will be interested in good deeds."),
    _V(21, "17", "182", 10, v21_17, "One will indulge in bad acts if the 10th lord is in the 8th while the 8th lord is in the 10th with a malefic."),
    _V(21, "18", "182", 10, v21_18, "Obstructions to the native's acts will crop up if the 10th lord is in fall, as both the 10th house from the ascendant and the 10th from the 10th (i.e. 7th from the ascendant) have malefic occupations."),
    _V(21, "19-21", "183", 10, v21_19_21, "One will be endowed with fame if the Moon is in the 10th while the 10th lord is in a trine from the 10th and the ascendant lord is in ascendant's angle. Similar effects will come to pass if the 11th lord is in the 10th while the 10th lord is strong and be in aspect to Jupiter. Fame will come to the native if the 10th lord is in the 9th as the ascendant lord is in the 10th and the Moon is in the 5th from the ascendant.", N_STRENGTH),
    _V(22, "2", "184", 11, v22_2, "Should the 11th lord be in the 11th itself or be in an angle or in a trine from the ascendant, there will be many gains. Similarly if the 11th lord is exalted, though in combustion, there will be many gains."),
    _V(22, "3", "184", 11, v22_3, "If the 11th lord is in the 2nd while the 2nd lord is in angle (from the ascendant) along with Jupiter, the gains will be great."),
    _V(22, "6", "185", 11, v22_6, "The native will own 6000 Nishkas if the 11th is occupied by Jupiter while the 2nd and 9th are respectively taken over by the Moon and Venus by position."),
    _V(22, "7", "185", 11, v22_7, "Should Jupiter, Mercury and the Moon be in the 11th from the 11th (i.e. 9th from the ascendant) the native will be endowed with wealth, grains, fortunes, diamonds, ornaments etc."),
    _V(22, "9", "185", 11, v22_9, "If the 11th lord is in the 2nd as the 2nd lord is in the 11th, one will amass abundant fortunes after marriage."),
    _V(22, "10", "185", 11, v22_10, "If the 11th lord is in the 3rd as the 3rd lord is in the 11th, one will gain wealth through co-born and be endowed with excellent ornaments."),
    _V(22, "11", "185", 11, v22_11, "There will be no gains in spite of numerous efforts if the 11th lord is in fall, in combustion or be in the 6th/8th/12th with a malefic.", N_COMBUST),
    _V(23, "1-4", "186", 12, v23_1_4, "O Brahmin, now I tell you about the effects of the 12th house. There will be expenses on good accounts if the 12th lord is with a benefic, or be in own house or be exalted or if a benefic occupies the 12th. One will own beautiful houses and beds and be endowed with superior scented articles and pleasures if the Moon happens to be the 12th lord and be exalted or be in own sign/Navamsa or in the 11th/9th/5th in Rasi/Navamsa. The said native will live with rich clothes, and ornaments, be learned and lordly.", N_NAVAMSA),
    _V(23, "5-6", "186", 12, v23_5_6, "And if the 12th lord is in the 6th/8th or be in enemy's Navamsa, debilitation Navamsa or in 8th in Navamsa, one will be devoid of happiness from wife, be troubled by expenses and deprived of general happiness. If he be in an angle/trine, the native will beget a spouse.", N_NAVAMSA),
    _V(23, "10", "188", 12, v23_10, "If there is a benefic in the 12th while its lord is exalted or is conjunct or aspected by a benefic, one will attain final emancipation.", N_FULL),
    _V(23, "11", "188", 12, v23_11, "One will wander from country to country if the 12th lord and 12th house are with malefics and be in aspect to malefics.", N_FULL),
    _V(23, "12", "188", 12, v23_12, "One will move in his own country if the 12th lord and 12th house are with benefics and be in aspect to benefics.", N_FULL),
    _V(23, "13", "188", 12, v23_13, "Earnings will be through sinful measures if the 12th is occupied by Saturn or Mars etc. and be not aspected by a benefic.", N_FULL),
    _V(23, "14", "188", 12, v23_14, "If the ascendant lord is in the 12th while the 12th lord is in the ascendant with Venus, expenses will be on religious grounds."),
]


def evaluate(positions: dict, lagna: int, moon_waxing=None) -> dict:
    """Every registered verse whose own condition this chart meets, whole, with the clause(s) that fired."""
    c = Chart(positions, lagna, moon_waxing)
    matches, errors = [], []
    for v in VERSES:
        try:
            clauses = v["fn"](c)
        except Exception as e:  # noqa: BLE001 — one verse must not cost the rest
            errors.append(f"ch.{v['chapter']} v.{v['verse']}: {e}")
            continue
        if clauses:
            matches.append({"chapter": v["chapter"], "verse": v["verse"], "house": v["house"],
                            "citation": v["citation"], "text": v["text"], "clauses": clauses, "notes": v["notes"]})
    return {"source": SOURCE, "registered": len(VERSES), "matches": matches, "errors": errors}
