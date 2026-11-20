"""BPHS Vol I chs 6-7: what each division is read for, the presiding deity of each
part of each division, and the ch.7 rules that give a result from a division.

Tier: sloka. The English is R. Santhanam's translation (Ranjan Publications), read
from the PAGE IMAGES of "BPHS - 1 RSanthanam-1.pdf" on 2026-11-19 (PDF page =
printed page - 1). The scan's OCR layer was not used. Printed pages per entry.

Two things here come from Santhanam's NOTES, not from the verses, and carry tier
"note" (never "sloka"):
  * which Shashtyamsa (D60) parts are benefic and which malefic: the verses (33-41)
    name the 60 parts and say benefic ones give good results and malefic ones the
    opposite, but the (B)/(M) marks are in the translator's table (pp.84-86);
  * "a benefic Shodasamsa" (ch.7 v.7) read as the Shodasamsa of a benefic planet
    (the note on p.93).

WHAT IS NOT REGISTERED, and why:
  * D2 (Hora) deities. The Sanskrit of ch.6 v.6 names them, but the translation
    does not. We do not translate Sanskrit ourselves (CLAUDE.md).
  * The D60 meanings ("aweful", "death personified" ...). They are the translator's
    glosses, and several are fated readings. Only the names and the marks are kept.
  * Vaiseshikamsha (ch.6 vv.42-53) needs the Arudha lagna and combustion, neither
    tested here. Step B of docs/study-plan.md.
  * ch.7 v.16 "the effects applicable to Rasi will apply to Trimsamsa". Following
    it would mean reading other texts' sign results into D30, a chain we do not
    build without a registered inference.
"""

from __future__ import annotations

SOURCE = {"id": "bphs", "text": "Bṛhat Parāśara Horā Śāstra", "author": "Parāśara",
          "translator": "R. Santhanam (Ranjan Publications)", "tier": "sloka"}
CONFIDENCE = "page_image_checked"   # read, then re-read at zoom on 2026-11-19

MOVABLE, FIXED = {0, 3, 6, 9}, {1, 4, 7, 10}


def _odd(sign: int) -> bool:
    return sign % 2 == 0


# ---- ch.7 vv.1-5: what each division is consulted for ----------------------------
# `words` = the translation's own words (p.91-92); `topic` = our neutral label.
USES = {
    "D1": ("the body", "physique"),
    "D2": ("wealth", "wealth"),
    "D3": ("siblings", "happiness through coborn"),
    "D4": ("fortune", "fortunes"),
    "D7": ("children and grandchildren", "sons and grandsons"),
    "D9": ("spouse", "spouse"),
    "D10": ("power and position", "power (and position)"),
    "D12": ("parents", "parents"),
    "D16": ("vehicles", "benefits and adversities through conveyances"),
    "D20": ("worship", "worship"),
    "D24": ("learning", "learning"),
    "D27": ("strength and weakness", "strength and weakness"),
    "D30": ("evil effects", "evil effects"),
    "D40": ("auspicious and inauspicious effects", "auspicious and inauspicious effects"),
    "D45": ("all indications", "all indications"),
    "D60": ("all indications", "all indications"),
}
USES_CITATION = "BPHS I ch.7 vv.1-5 (pp.91-92)"
USES_ADAPTATION = {"D7": {"classes": ["gender"], "action": "neutralise",
                          "note": "'Sons and grandsons' rendered as children and grandchildren."}}

# ---- ch.6: presiding deities of the parts ----------------------------------------
_D3 = ["Narada", "Agasthya", "Doorvasa"]
_D4 = ["Sanaka", "Sananda", "Kumara", "Sanatana"]
_D7 = ["Kshaara", "Ksheera", "Dadhi", "Ghritha", "Ikshu Rasa", "Madhya", "Suddha Jala"]
_D9 = {"movable": ["Deva", "Manushya", "Rakshasa"], "fixed": ["Manushya", "Rakshasa", "Deva"],
       "dual": ["Rakshasa", "Manushya", "Deva"]}
_D10 = ["Indra", "Agni", "Yama", "Rakshasa", "Varuna", "Vayu", "Kubera", "Isana", "Brahma", "Anantha"]
_D12 = ["Ganesa", "Aswini Kumara", "Yama", "Sarpa"]
_D16 = ["Brahma", "Vishnu", "Siva", "Sun"]
_D20_ODD = ["Kaali", "Gauri", "Jaya", "Lakshmi", "Vijaya", "Vimala", "Sati", "Tara", "Jvala-Mukhi",
            "Sveta", "Lalita", "Bagala-mukhi", "Pratyangira", "Sachi", "Raudri", "Bhavani",
            "Varada", "Jaya", "Tripura", "Sumukhi"]
_D20_EVEN = ["Daya", "Megha", "Chinnasi", "Pisachini", "Dhoomavathi", "Matangi", "Bala", "Bhadra",
             "Aruna", "Anala", "Pingala", "Chuchchuka", "Ghora", "Vaarahi", "Vaishnavi", "Sita",
             "Bhuvanesvari", "Bhairavi", "Mangala", "Aparajita"]
_D24 = ["Skanda", "Parsudhara", "Anala", "Viswakarma", "Bhaga", "Mitra", "Maya", "Antaka",
        "Vrisha-dhwaja", "Govinda", "Madana", "Bhima"]
_D27 = ["Dastra (Aswini Kumara)", "Yama", "Agni", "Brahma", "Chandra", "Isa", "Aditi", "Jiva", "Ahi",
        "Pitara", "Bhaga", "Aryama", "Surya", "Tvashta", "Marut", "Sakragni", "Mitra", "Vasava",
        "Rakshasa", "Varuna", "Visvadeva", "Govinda", "Vasu", "Varuna", "Ajapa", "Ahirbudhanya",
        "Pusha"]
_D30_ODD = [(5.0, "Agni"), (5.0, "Vayu"), (8.0, "Indra"), (7.0, "Kubera"), (5.0, "Varuna")]
_D30_EVEN = list(reversed(_D30_ODD))
_D40 = ["Vishnu", "Chandra", "Marichi", "Tvashta", "Dhata", "Siva", "Ravi", "Yama", "Yaksha",
        "Gandharva", "Kala", "Varuna"]
_D45 = {"movable": ["Brahma", "Siva", "Vishnu"], "fixed": ["Siva", "Vishnu", "Brahma"],
        "dual": ["Vishnu", "Brahma", "Siva"]}
# D60: the verse's names (vv.33-41, p.83) with the translator's (B)/(M) (pp.84-86).
D60 = [("Ghora", "M"), ("Rakshasa", "M"), ("Deva", "B"), ("Kubera", "B"), ("Yaksha", "B"),
       ("Kinnara", "B"), ("Bhrashta", "M"), ("Kulaghna", "M"), ("Garala", "M"), ("Vahni", "M"),
       ("Maya", "M"), ("Purishaka", "M"), ("Apampathi", "B"), ("Marutwan", "B"), ("Kala", "M"),
       ("Sarpa", "M"), ("Amrita", "B"), ("Indu", "B"), ("Mridu", "B"), ("Komala", "B"),
       ("Heramba", "B"), ("Brahma", "B"), ("Vishnu", "B"), ("Maheswara", "B"), ("Deva", "B"),
       ("Ardra", "B"), ("Kalinasa", "B"), ("Kshiteesa", "B"), ("Kamalakara", "B"), ("Gulika", "M"),
       ("Mrithyu", "M"), ("Kaala", "M"), ("Davagni", "M"), ("Ghora", "M"), ("Yama", "M"),
       ("Kantaka", "M"), ("Sudha", "B"), ("Amrita", "B"), ("Poornachandra", "B"), ("Vishadagdha", "M"),
       ("Kulanasa", "M"), ("Vamsakshaya", "M"), ("Utpata", "M"), ("Kaala", "M"), ("Saumya", "B"),
       ("Komala", "B"), ("Seetala", "B"), ("Karala Damshtra", "M"), ("Chandramukhi", "B"),
       ("Praveena", "B"), ("Kalapavaka", "M"), ("Dandayudha", "M"), ("Nirmala", "B"), ("Saumya", "B"),
       ("Kroora", "M"), ("Atiseetala", "B"), ("Amrita", "B"), ("Payodhi", "B"), ("Bhramana", "M"),
       ("Chandrarekha (Indurekha)", "B")]
D60_DISPUTED = {26: "The note marks Kalinasa (B) and adds that some count it malefic."}
D60_CITATION = "BPHS I ch.6 vv.33-41 (p.83)"
D60_MARK_CITATION = "Santhanam's note to BPHS I ch.6 vv.33-41 (pp.84-86)"

DEITY_CITATION = {
    "D3": "BPHS I ch.6 vv.7-8 (p.69)", "D4": "BPHS I ch.6 v.9 (p.70)",
    "D7": "BPHS I ch.6 vv.10-11 (p.71)", "D9": "BPHS I ch.6 v.12 (p.72)",
    "D10": "BPHS I ch.6 vv.13-14 (p.73)", "D12": "BPHS I ch.6 v.15 (p.73)",
    "D16": "BPHS I ch.6 v.16 (p.74)", "D20": "BPHS I ch.6 vv.17-21 (p.76)",
    "D24": "BPHS I ch.6 vv.22-23 (p.77)", "D27": "BPHS I ch.6 vv.24-26 (pp.78-79)",
    "D30": "BPHS I ch.6 vv.27-28 (p.80)", "D40": "BPHS I ch.6 vv.29-30 (pp.80-81)",
    "D45": "BPHS I ch.6 vv.31-32 (p.81)", "D60": D60_CITATION,
}
DEITY_NOTES = {
    "D24": "The translation's list ends with Bhima; its next sentence prints 'Bhishma'. The list is followed.",
    "D9": "The order for fixed and dual signs is the translator's parenthesis inside the verse's rendering.",
}
PARTS = {"D3": 3, "D4": 4, "D7": 7, "D9": 9, "D10": 10, "D12": 12, "D16": 16, "D20": 20,
         "D24": 24, "D27": 27, "D40": 40, "D45": 45, "D60": 60}


def _mobility(sign):
    return "movable" if sign in MOVABLE else "fixed" if sign in FIXED else "dual"


def part_of(varga: str, deg: float) -> int:
    """0-based part of the sign (equal parts; D30 by its own spans)."""
    if varga == "D30":
        raise ValueError("D30 has unequal parts: use deity()")
    n = PARTS[varga]
    return min(int(deg / (30.0 / n)), n - 1)


def deity(varga: str, sign: int, deg: float) -> dict | None:
    """The presiding deity of the part of `sign` holding `deg` (0-30), or None."""
    if varga == "D30":
        spans = _D30_ODD if _odd(sign) else _D30_EVEN
        cur = 0.0
        for k, (span, name) in enumerate(spans):
            cur += span
            if deg < cur or k == len(spans) - 1:
                return {"varga": varga, "part": k + 1, "name": name,
                        "citation": DEITY_CITATION[varga]}
    if varga not in PARTS:
        return None
    k = part_of(varga, deg)
    n = PARTS[varga]
    odd = _odd(sign)
    out = {"varga": varga, "part": k + 1, "citation": DEITY_CITATION[varga]}
    if varga == "D3":
        out["name"] = _D3[k]
    elif varga == "D4":
        out["name"] = _D4[k]
    elif varga == "D7":
        out["name"] = _D7[k] if odd else _D7[n - 1 - k]
    elif varga == "D9":
        out["name"] = _D9[_mobility(sign)][k % 3]
    elif varga == "D10":
        out["name"] = _D10[k] if odd else _D10[n - 1 - k]
    elif varga == "D12":
        out["name"] = _D12[k % 4]
    elif varga == "D16":
        seq = _D16 * 4
        out["name"] = seq[k] if odd else seq[n - 1 - k]
    elif varga == "D20":
        out["name"] = (_D20_ODD if odd else _D20_EVEN)[k]
    elif varga == "D24":
        out["name"] = _D24[k % 12] if odd else _D24[11 - k % 12]
    elif varga == "D27":
        out["name"] = _D27[k] if odd else _D27[n - 1 - k]
    elif varga == "D40":
        out["name"] = _D40[k % 12]
    elif varga == "D45":
        out["name"] = _D45[_mobility(sign)][k % 3]
    elif varga == "D60":
        i = k if odd else n - 1 - k
        name, mark = D60[i]
        out.update(name=name, number=i + 1,
                   nature={"B": "benefic", "M": "malefic"}[mark],
                   nature_source=D60_MARK_CITATION)
        if i in D60_DISPUTED:
            out["disputed"] = D60_DISPUTED[i]
    if varga in DEITY_NOTES:
        out["note"] = DEITY_NOTES[varga]
    return out


# ---- ch.7 vv.13-16: hora effects, and the thirds of a part -----------------------
HORA_CITATION = "BPHS I ch.7 vv.13-16 (p.94)"
HORA_TEXT = ("Jupiter, the Sun and Mars give (pronounced) effects in the hora of the Sun. The Moon, "
             "Venus and Saturn do so when in Moon's hora. Mercury is effective in both the Horas. "
             "In the case of an even Rasi the hora of the Moon will be powerful in effects while "
             "the Sun's hora in an odd sign will be so. Full, medium and nil will be the effects "
             "respectively in the beginning, middle and the end of a hora. Similar applications be "
             "made for a decanate, Turyamsa, Navamsa etc.")
_SUN_HORA_GRAHAS = {"jupiter", "sun", "mars"}
_MOON_HORA_GRAHAS = {"moon", "venus", "saturn"}
THIRDS_VARGAS = ("D2", "D3", "D4", "D9")   # the four the verse names; "etc." is not extended


def hora_of(sign: int, deg: float) -> str:
    first = deg < 15.0
    return "sun" if (first if _odd(sign) else not first) else "moon"


def hora_effect(graha: str, sign: int, deg: float) -> dict | None:
    if graha not in _SUN_HORA_GRAHAS | _MOON_HORA_GRAHAS | {"mercury"}:
        return None
    h = hora_of(sign, deg)
    gives = (graha == "mercury" or (h == "sun" and graha in _SUN_HORA_GRAHAS)
             or (h == "moon" and graha in _MOON_HORA_GRAHAS))
    return {"hora": h, "gives_effects": gives,
            "hora_powerful": (h == "sun") == _odd(sign),
            "citation": HORA_CITATION}


def thirds(varga: str, deg: float) -> dict:
    """Full / medium / nil by the third of the part the degree falls in (v.15)."""
    n = {"D2": 2, "D3": 3, "D4": 4, "D9": 9}[varga]
    size = 30.0 / n
    pos = (deg % size) / size
    grade = "full" if pos < 1 / 3 else "medium" if pos < 2 / 3 else "nil"
    return {"varga": varga, "grade": grade, "citation": HORA_CITATION}


# ---- ch.7 vv.6-8: a house lord in a malefic D60 / a benefic D16 ------------------
LORD_RULE_CITATION = "BPHS I ch.7 vv.6-8 (p.92)"
LORD_RULE_TEXT = ("The bhava whose lord is in a malefic Shashtiamsa will diminish, so say Garga and "
                  "others. The bhava whose lord is in a benefic Shodasamsa (or Kalamsa) flourish.")
D16_NOTE_CITATION = "Santhanam's note to BPHS I ch.7 vv.6-8 (p.93)"
