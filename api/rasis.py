"""The twelve rāśis, as BPHS describes them — and as it does not.

Vol I ch.4 is the sign-description chapter. It is far terser than any modern
sign card, and the gaps are not OCR damage: Parāśara simply does not assign
some attributes. Those absences are recorded here as first-class values with
`Src.ABSENT`, because on this site an empty cell that says "BPHS is silent"
is content, and filling it from general astrological knowledge would be the
clearest possible violation of the project standard.

WHAT IS TRANSCRIBED HERE vs WHAT IS DERIVED
-------------------------------------------
Only ch.4's sign descriptions are typed out. Everything computable is derived
from a module that already has its own tests and its own citations:

    dignity.py       exaltation / debilitation / mūlatrikoṇa hosted by a sign
    drishti.py       rāśi dṛṣṭi (ch.8) — which signs this one aspects
    functional.py    ch.34's benefic/malefic table for this sign as lagna
    (arithmetic)     nakṣatra and pāda spans; bādhaka; modality; gender

Transcription is where errors enter. The mining pass proved it — its worst
single error was lifting Gemini's degree column into the Virgo row. So this
module types as little as possible.

THINGS EVERY OTHER RĀŚI CARD SHOWS AND THIS ONE CANNOT
------------------------------------------------------
BPHS assigns a rāśi no lucky number, no colour, no day, no gemstone, no
presiding deity, no season, no fertility, no personality of the native, and —
for seven of the twelve — no symbol at all. It never calls Meṣa a ram, Vṛṣa a
bull or Siṁha a lion. Colours, gems, tastes and deities all belong to the
GRAHAS (ch.3), and deities also to the nakṣatras and the varga divisions, but
never to a sign. See ABSENT_FROM_ALL_RASIS.

There is likewise no compatibility doctrine of any kind: no kūṭa, no
guṇa-milan, no gaṇa/yoni/nāḍī. BPHS judges marriage from the 7th bhāva, its
lord, Venus and the Upapada — never by pairing two signs.
"""

from __future__ import annotations

from enum import Enum

import ch78_notes
import dignity
import drishti
import functional

ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO = 0, 1, 2, 3, 4, 5
LIBRA, SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES = 6, 7, 8, 9, 10, 11


class Src(str, Enum):
    """Where a value comes from. This is the module's central promise."""
    SLOKA = "sloka"        # Parāśara's own text
    NOTE = "note"          # Santhanam's commentary — NOT doctrine
    TABLE = "table"        # the translator's tabulation
    DERIVED = "derived"    # from a stated general rule; this sign never named
    ABSENT = "absent"      # BPHS says nothing. Render as an explicit gap.
    OCR_LOST = "ocr_lost"  # present in the book, destroyed in this scan


def cited(value, src, ref, *, conflict=None, ocr=None, note=None):
    return {
        "value": value, "src": src.value, "ref": ref,
        "conflict": conflict,   # a second mūla passage that disagrees
        "ocr": ocr,             # what the scan actually shows, if damaged
        "note": note,
    }


NAMES = [
    ("Meṣa", "Mesha", "Aries"), ("Vṛṣabha", "Vrishabha", "Taurus"),
    ("Mithuna", "Mithuna", "Gemini"), ("Karka", "Karka", "Cancer"),
    ("Siṁha", "Simha", "Leo"), ("Kanyā", "Kanya", "Virgo"),
    ("Tulā", "Tula", "Libra"), ("Vṛścika", "Vrishchika", "Scorpio"),
    ("Dhanus", "Dhanus", "Sagittarius"), ("Makara", "Makara", "Capricorn"),
    ("Kumbha", "Kumbha", "Aquarius"), ("Mīna", "Meena", "Pisces"),
]

CH4 = "Vol I ch.4"

# --------------------------------------------------------------------------
# ch.4 sign descriptions — the only transcribed block in this module.
# Keys left out of a sign's dict are ABSENT by default (see attribute()).
# --------------------------------------------------------------------------
_D = {
    ARIES: dict(
        complexion=("blood-red", Src.SLOKA), build=("prominent", Src.SLOKA),
        habitat=(None, Src.OCR_LOST), direction=("east", Src.SLOKA),
        rising=("pṛṣṭhodaya", Src.SLOKA), strong=("night", Src.SLOKA),
        feet=("quadruped", Src.SLOKA), element=("fiery", Src.SLOKA),
        dosha=("bilious", Src.SLOKA), guna=("rajas", Src.SLOKA),
        varna=("related to kings", Src.SLOKA),
    ),
    TAURUS: dict(
        complexion=("white", Src.SLOKA), build=("long", Src.SLOKA),
        habitat=(None, Src.OCR_LOST), direction=("south", Src.SLOKA),
        rising=(None, Src.OCR_LOST), strong=("night", Src.SLOKA),
        feet=("quadruped", Src.SLOKA), element=("earthy", Src.SLOKA),
        dosha=("windy", Src.SLOKA),
        varna=("vilāsis and businessmen", Src.SLOKA),
    ),
    GEMINI: dict(
        complexion=("green, the hue of grass", Src.SLOKA),
        build=("even body", Src.SLOKA), habitat=("villages", Src.SLOKA),
        direction=("west", Src.SLOKA), rising=("śīrṣodaya", Src.SLOKA),
        strong=("night", Src.SLOKA), feet=("biped", Src.SLOKA),
        element=("airy", Src.SLOKA), dosha=("windy", Src.SLOKA),
    ),
    CANCER: dict(
        complexion=("pale red", Src.SLOKA), build=("bulky", Src.SLOKA),
        habitat=("forests", Src.SLOKA), rising=("pṛṣṭhodaya", Src.SLOKA),
        strong=("night", Src.SLOKA), feet=("centipede (bahupada)", Src.SLOKA),
        element=("watery", Src.SLOKA), dosha=("phlegmatic", Src.SLOKA),
        guna=("sattva", Src.SLOKA), varna=("Brāhmaṇa", Src.SLOKA),
    ),
    LEO: dict(
        complexion=("white, and large of body", Src.SLOKA),
        build=("large", Src.SLOKA), habitat=("forests", Src.SLOKA),
        direction=("east", Src.SLOKA), rising=("śīrṣodaya", Src.SLOKA),
        strong=("day", Src.SLOKA), feet=("quadruped", Src.SLOKA),
        dosha=("bilious", Src.SLOKA), guna=("sattva", Src.SLOKA),
        varna=("a royal sign", Src.SLOKA),
    ),
    VIRGO: dict(
        complexion=("variegated", Src.SLOKA), build=("medium", Src.SLOKA),
        habitat=("hills", Src.SLOKA), direction=("south", Src.SLOKA),
        rising=("śīrṣodaya", Src.SLOKA), strong=("day", Src.SLOKA),
        feet=("biped", Src.SLOKA), dosha=("windy", Src.SLOKA),
        guna=("tamas", Src.SLOKA), varna=("the business community", Src.SLOKA),
    ),
    LIBRA: dict(
        complexion=("black", Src.SLOKA), build=("medium", Src.SLOKA),
        habitat=("land", Src.SLOKA), direction=("west", Src.SLOKA),
        rising=("śīrṣodaya", Src.SLOKA), strong=("day", Src.SLOKA),
        feet=("biped", Src.SLOKA), dosha=("mixed", Src.SLOKA),
        guna=("rajas", Src.SLOKA), varna=("Śūdra, the 4th varṇa", Src.SLOKA),
    ),
    SCORPIO: dict(
        complexion=("reddish-brown", Src.SLOKA),
        build=("slender, and hairy", Src.SLOKA),
        habitat=("resides in holes; water and land", Src.SLOKA),
        direction=("north", Src.SLOKA), strong=("day", Src.SLOKA),
        feet=("centipede", Src.SLOKA), dosha=("phlegmatic", Src.DERIVED),
        varna=("Brāhmaṇa", Src.SLOKA),
    ),
    SAGITTARIUS: dict(
        complexion=("tawny", Src.SLOKA), build=("even build", Src.SLOKA),
        habitat=("land", Src.SLOKA), direction=("east", Src.SLOKA),
        rising=("śīrṣodaya", Src.SLOKA), strong=("night", Src.SLOKA),
        feet=("biped in its first half, quadruped in its second", Src.SLOKA),
        element=("fiery", Src.SLOKA), dosha=("bilious", Src.SLOKA),
        guna=("sattva", Src.SLOKA), varna=("a royal sign", Src.SLOKA),
    ),
    CAPRICORN: dict(
        complexion=("variegated", Src.SLOKA), build=("large body", Src.SLOKA),
        habitat=("forests and lands", Src.SLOKA), direction=("south", Src.SLOKA),
        rising=("pṛṣṭhodaya", Src.SLOKA), strong=("night", Src.SLOKA),
        feet=("quadruped in its first half, footless and aquatic in its second",
              Src.SLOKA),
        element=("earthy", Src.SLOKA), dosha=("windy", Src.SLOKA),
        guna=("tamas", Src.SLOKA),
    ),
    AQUARIUS: dict(
        complexion=("deep brown", Src.SLOKA), build=("medium", Src.SLOKA),
        habitat=("deep water", Src.SLOKA), direction=("west", Src.SLOKA),
        rising=("śīrṣodaya", Src.SLOKA), strong=("day", Src.SLOKA),
        feet=("biped", Src.SLOKA), element=("airy", Src.SLOKA),
        dosha=("mixed", Src.SLOKA), guna=("tamas", Src.SLOKA),
        varna=("Śūdra, the 4th varṇa", Src.SLOKA),
    ),
    PISCES: dict(
        build=("medium", Src.SLOKA), habitat=("resorts to water", Src.SLOKA),
        direction=("north", Src.SLOKA), rising=("ubhayodaya", Src.SLOKA),
        strong=("night", Src.SLOKA), feet=("footless", Src.SLOKA),
        element=("watery", Src.SLOKA), dosha=("phlegmatic", Src.SLOKA),
        guna=("sattva", Src.SLOKA),
    ),
}

# ch.4's dik for a sign vs ch.8's layout for DRAWING the rāśi-dṛṣṭi diagram.
# Both are mūla and they disagree for eight signs. We print ch.4 and disclose
# ch.8 rather than silently picking — see CONFLICTS.
_CH8_DIRECTION = {
    ARIES: "east", TAURUS: "east", GEMINI: "north-east", CANCER: "north",
    LEO: "north", VIRGO: "north-west", LIBRA: "west", SCORPIO: "west",
    SAGITTARIUS: "south-west", CAPRICORN: "south", AQUARIUS: "south",
    PISCES: "south-east",
}

# Only where the text genuinely fights itself. Never resolved silently.
CONFLICTS = {
    GEMINI: "ch.4 sl.9 calls Mithuna windy in temperament; ch.4 sl.5½ makes "
            "its trine mixed. Both are legible mūla and they are not "
            "reconciled.",
    SCORPIO: "Vṛścika is the ONLY sign given no rising type. That is not an "
             "OCR loss — the śloka omits it, which leaves a real hole in "
             "ch.27 vv.30-31's bhāva-bala rule, since that rule keys off "
             "śīrṣodaya vs pṛṣṭhodaya.",
    AQUARIUS: "One half-śloka says Kumbha 'resorts to deep water and is airy'. "
              "The water clause is usually dropped to tidy up an air sign. "
              "We keep both.",
    PISCES: "The śloka makes Mīna night-strong; Santhanam's Naṣṭa-jātaka note "
            "(p.58) lists Pisces among the diurnal signs. The śloka governs.",
}

ABSENT_FROM_ALL_RASIS = (
    "lucky number", "lucky colour", "lucky day", "gemstone", "metal",
    "compatible signs", "presiding deity", "personality of the native",
    "fertile / barren", "season", "taste", "symbol or emblem",
)

SYMBOL_NOTE = (
    "BPHS gives an emblem to only five signs — Mithuna (a male and a female, "
    "holding a mace and a lute), Kanyā (a virgin holding grains and fire), "
    "Dhanus (adores an arch), Kumbha (a man holding a pot) and Mīna (a pair of "
    "fish). There is no ram, no bull, no lion, no scorpion and no goat "
    "anywhere in either volume. The familiar animal set is convention, not text."
)

KALAPURUSHA = [
    "head", "face", "arms", "heart", "stomach", "hip",
    "the space below the navel", "privities", "thighs", "knees", "ankles", "feet",
]
KALAPURUSHA_NOTE = (
    "ch.4 vv.1-2: 'Śrī Viṣṇu, the Invisible, is Time personified. His limbs "
    "are the 12 Rāśis commencing from Aries.' The limb above is the "
    "KĀLAPURUṢA mapping, counted from Meṣa. In a natal chart Santhanam's note "
    "(p.48) counts the limbs from the LAGNA instead, using a Scorpio "
    "ascendant as his worked example."
)

MODALITY = ("chara (movable)", "sthira (fixed)", "dvisvabhāva (dual)")
MODALITY_NOTE = (
    "Movable, fixed and dual repeat in that order from Meṣa (ch.4 vv.4½-5½). "
    "The śloka states the ORDERING rule; the naming of each individual sign is "
    "Santhanam's note."
)

# Vol II ch.69, and Vol II ch.46 vv.168-169.
RASIMANA = [7, 10, 8, 4, 10, 6, 7, 8, 9, 6, 11, 12]
STHIRA_DASHA_YEARS = [7, 8, 9, 7, 8, 9, 7, 8, 9, 7, 8, 9]

# ch.27 vv.26-29: which angle is deducted when computing a bhāva's bala.
BHAVA_BALA_DEDUCTION = {
    ARIES: "the 4th (Nadir)", TAURUS: "the 4th", GEMINI: "the 7th (Descendant)",
    CANCER: "the Ascendant itself", LEO: "the 4th", VIRGO: "the 7th",
    LIBRA: "the 7th", SCORPIO: "the Ascendant itself",
    SAGITTARIUS: "the 7th in its first half, the 4th in its second",
    CAPRICORN: "the 4th in its first half, the 10th (MC) in its second",
    AQUARIUS: "the 7th", PISCES: "the 10th (MC)",
}


def _movable(sign):
    return sign % 3 == 0


def badhaka_for(sign):
    """Which sign is the bādhaka-sthāna of `sign`, per Vol II ch.50 vv.20-21.

    DERIVED, not transcribed: the śloka gives the 11th from a movable rāśi.

    BPHS defines bādhaka for the FOUR MOVABLE SIGNS ONLY. The 9th-from-fixed
    and 7th-from-dual rules that every other Jyotiṣa site prints are not in
    either volume — the Vol II contents page promises all three and the verses
    deliver one. Returning None for fixed and dual signs is the finding.
    """
    if not _movable(sign):
        return None
    return (sign + 10) % 12


def is_badhaka_for(sign):
    """Which rāśi (if any) THIS sign obstructs — the inverse of badhaka_for().

    Worth showing because it is the only bādhaka fact a fixed or dual sign has:
    Siṁha has no bādhaka of its own, but it IS the bādhaka-sthāna of Tulā. Only
    the four movable signs have a bādhaka, so only four signs are one.
    """
    for m in range(0, 12, 3):        # the movable rāśis
        if badhaka_for(m) == sign:
            return m
    return None


NAKSHATRAS = [
    "Aśvinī", "Bharaṇī", "Kṛttikā", "Rohiṇī", "Mṛgaśira", "Ārdrā",
    "Punarvasu", "Puṣya", "Āśleṣā", "Maghā", "P.Phalgunī", "U.Phalgunī",
    "Hasta", "Citrā", "Svātī", "Viśākhā", "Anurādhā", "Jyeṣṭhā",
    "Mūla", "P.Āṣāḍhā", "U.Āṣāḍhā", "Śravaṇa", "Dhaniṣṭhā", "Śatabhiṣā",
    "P.Bhādrapada", "U.Bhādrapada", "Revatī",
]
NAK_ARC = 360.0 / 27.0
PADA_ARC = NAK_ARC / 4.0


def nakshatra_spans(sign):
    """The nakṣatra/pāda segments falling inside one rāśi.

    Computed, never transcribed — this is pure arithmetic on a 27-fold and a
    12-fold division of the same circle, and transcribing it is exactly where
    the mining pass made its worst error (it lifted Mithuna's degrees into the
    Kanyā row).

    Each rāśi holds 2¼ nakṣatras, i.e. nine pādas, always.
    """
    out, start, end = [], sign * 30.0, (sign + 1) * 30.0
    first_pada = int(round(start / PADA_ARC))
    for p in range(first_pada, first_pada + 9):
        nak, pada = divmod(p, 4)
        lo, hi = p * PADA_ARC, (p + 1) * PADA_ARC
        if out and out[-1]["nakshatra_index"] == nak:
            out[-1]["padas"].append(pada + 1)
            out[-1]["to"] = hi - start
        else:
            out.append({
                "nakshatra_index": nak, "nakshatra": NAKSHATRAS[nak],
                "padas": [pada + 1], "from": lo - start, "to": hi - start,
            })
    return out


def dignities_hosted(sign):
    """Which grahas peak, fall or hold mūlatrikoṇa in this sign — from
    dignity.py, so the ch.3 numbers live in exactly one place."""
    lm = dignity.sign_landmarks(sign)
    return {
        "exaltation": lm["exaltation_points"],
        "debilitation": lm["debilitation_points"],
        "moolatrikona": lm["moolatrikona_arcs"],
        "lord": lm["lord"],
        # ch.3 vv.49-50 name only the exaltations; every debilitation is the
        # 7th sign from one, so a sign's fall points are derived, not stated.
        "debilitation_is_derived": True,
        "empty": not (lm["exaltation_points"] or lm["debilitation_points"]),
    }


def attribute(sign, key):
    """One ch.4 attribute, always cited — ABSENT when the text is silent."""
    entry = _D.get(sign, {}).get(key)
    if entry is None:
        return cited(None, Src.ABSENT, f"{CH4} — not stated for this rāśi")
    value, src = entry
    if src is Src.OCR_LOST:
        return cited(None, Src.OCR_LOST, f"{CH4}",
                     ocr="The line is destroyed in this scan; the book has it.")
    out = cited(value, src, f"{CH4}")
    if key == "direction":
        out["conflict"] = (
            f"ch.8 vv.6-9 places this rāśi in the {_CH8_DIRECTION[sign]} when "
            f"laying out the rāśi-dṛṣṭi diagram. Both passages are mūla. We "
            f"print ch.4's dik; ch.8's is a drawing convention."
        )
    return out


ATTRS = ("complexion", "build", "habitat", "direction", "rising", "strong",
         "feet", "element", "dosha", "guna", "varna")


def rasi(sign):
    """Everything BPHS says about one rāśi, and what it does not say."""
    name, common, english = NAMES[sign]
    attrs = {k: attribute(sign, k) for k in ATTRS}

    absent = [k for k, v in attrs.items() if v["src"] == Src.ABSENT.value]
    lost = [k for k, v in attrs.items() if v["src"] == Src.OCR_LOST.value]

    bad = badhaka_for(sign)
    return {
        "sign": sign, "name": name, "name_common": common, "name_en": english,
        "lord": dignity.RASI_LORD[sign],
        "modality": cited(MODALITY[sign % 3], Src.SLOKA, f"{CH4} vv.4½-5½",
                          note=MODALITY_NOTE),
        "gender": cited("male" if sign % 2 == 0 else "female", Src.DERIVED,
                        f"{CH4} — odd signs male, even female"),
        "kalapurusha_limb": cited(KALAPURUSHA[sign], Src.SLOKA,
                                  f"{CH4} vv.1-2, 4-4½", note=KALAPURUSHA_NOTE),
        "attributes": attrs,
        "absent": absent,          # the text is silent — render as a gap
        "ocr_lost": lost,          # the book has it; this scan does not
        "conflict": CONFLICTS.get(sign),
        "dignities": dignities_hosted(sign),
        "nakshatras": {
            "spans": nakshatra_spans(sign),
            "src": Src.TABLE.value,
            "ref": "Vol II ch.46, translator's table",
            "note": "Computed arithmetically here. BPHS mūla never assigns "
                    "nakṣatras to rāśis — the mapping is Santhanam's apparatus, "
                    "which he introduces as such.",
        },
        "rasi_drishti": {
            "aspects": [s for s in range(12) if drishti.rasi_drishti(sign, s)],
            "src": Src.SLOKA.value, "ref": "Vol I ch.8 vv.1-5",
            "note": "Sign aspect — NOT compatibility. BPHS contains no "
                    "marriage matching by sign: no kūṭa, no guṇa-milan, no "
                    "gaṇa, yoni or nāḍī.",
        },
        "as_lagna": functional.lagna_profile(sign),
        "technical": {
            "bhava_bala_deduction": cited(
                BHAVA_BALA_DEDUCTION[sign], Src.SLOKA, "Vol I ch.27 vv.26-29"),
            "badhaka_of": cited(
                bad, Src.DERIVED if bad is not None else Src.ABSENT,
                "Vol II ch.50 vv.20-21",
                note=("The 11th from a movable rāśi." if bad is not None else
                      "BPHS defines bādhaka only for the four movable rāśis. "
                      "The fixed (9th) and dual (7th) rules other sites print "
                      "are in neither volume.")),
            "is_badhaka_for": cited(
                is_badhaka_for(sign),
                Src.DERIVED if is_badhaka_for(sign) is not None else Src.ABSENT,
                "Vol II ch.50 vv.20-21",
                note="This rāśi is the bādhaka-sthāna of that one — the 11th "
                     "from it. Only four rāśis are, since only movable signs "
                     "have a bādhaka at all."),
            "rasimana": cited(RASIMANA[sign], Src.SLOKA, "Vol II ch.69 vv.1-4"),
            "sthira_dasha_years": cited(
                STHIRA_DASHA_YEARS[sign], Src.SLOKA, "Vol II ch.46 vv.168-169"),
        },
        # Santhanam's ascendant sketch. Deliberately the LAST key, tagged NOTE,
        # and carrying its own disclaimer — it is the one block on the card that
        # is not Parāśara, and the UI keeps it collapsed and visually apart. See
        # ch78_notes.py for why it is excerpted rather than reproduced whole.
        "translator_sketch": {
            **(ch78_notes.sketch(sign) or {}),
            "src": Src.NOTE.value,
            "ref": ch78_notes.CITATION,
            "disclaimer": ch78_notes.DISCLAIMER,
        },
        "not_in_bphs": {
            "attributes": list(ABSENT_FROM_ALL_RASIS),
            "symbol_note": SYMBOL_NOTE,
            "note": "BPHS assigns none of these to any rāśi. Colours, gems, "
                    "tastes and deities belong to the GRAHAS (ch.3); deities "
                    "also to the nakṣatras and the vargas — never to a sign.",
        },
    }


def all_rasis():
    return [rasi(s) for s in range(12)]
