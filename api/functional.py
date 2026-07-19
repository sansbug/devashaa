"""Functional benefic / malefic by lagna, and maraka.

    BPHS Vol I, Chapter 34 — "Yoga Karakas" (nature due to lordships)
    BPHS Vol I, Chapter 44 — "Maraka (Killer) Planets"

Two things live here, because the text puts them together: ch.34 vv.19-44 hand
out a functional NATURE and a MARAKA verdict in the same breath, lagna by
lagna ("Saturn, Mercury and Venus are malefics ... Venus is a direct killer").

THE POINT OF THIS MODULE IS THE SOURCE TAG.
Parāśara's per-lagna verses are not complete. For twelve of the eighty-four
(12 lagnas x 7 non-nodal grahas) cells the ślokas simply say nothing, and the
value everyone quotes comes from R. Santhanam's NOTES. Santhanam says so
himself, three times in as many words:

    Aries / Moon    "The Moon's role is not discussed by the sage."
    Gemini / Saturn "There is no hint on saturn's role ..."  (sic, scan)
    Virgo / Saturn  "There is no hint in the text about Saturn's role."

So every cell of LAGNA_NATURE carries `source` = 'sloka' or 'note', and six
cells carry no verdict at all (`nature` is None) because NEITHER the śloka nor
the note states one — or because the only text touching the cell is a MARAKA
verdict, which this module never promotes to a nature (MARAKA_IS_NOT_A_NATURE).
Those are listed in NATURE_UNAVAILABLE. They are not guessed.
`classify_by_lordship()` will still derive a value for most of them from the
general law, but that is clearly marked a derivation, not the text.

---------------------------------------------------------------------------
THE GENERAL LAW — ch.34 vv.2-7
---------------------------------------------------------------------------
    "Benefics owning angles will not give benefic effects while malefics
     owning angles will not remain inauspicious. The lord of a trine will
     give auspicious results. The lord of the ascendant is specially
     auspicious as the ascendant is an angle as well as trine. The 5th and
     9th houses are specially for wealth while the 7th and 10th are specially
     for happiness. Any planet owning the 3rd, 6th, or the 11th will give
     evil effects. The effects due to the lords of the 12th, and 8th will
     depend on their association. In each group, the significance will be in
     the ascending order. The 8th lord is not auspicious as he owns the 12th
     from the 9th. If the lord of the 8th simultaneously owns the 3rd, 7th or
     11th, he will prove specifically harmful while his simultaneous
     ownership of a trine will bestow auspicious effects. The planet owning a
     predominant house will stall the effects due to another owning a less
     significant house and will give his own results. THE 8TH LORDSHIP OF THE
     SUN AND THE MOON IS NOT EVIL."

    v.13  "If one and the same planet gets the lordships of a trine as well
           as an angle or if a planet is in an angle or in a trine, it will
           prove specially a yogakaraka."
    v.14  "It has been said that a malefic owning an angle will become
           auspicious which is true only when it simultaneously lords over a
           trine and not by merely owning an angle."

    Notes to vv.2-7, point 2, is emphatic about what v.2's malefic clause does
    NOT say: "If a malefic owns an angle he will not be inauspicious. THIS
    DOES NOT MEAN THAT HE WILL BECOME AUSPICIOUS. (The sage has cautiously
    worded his verse.)"  — hence MALEFIC_KENDRA_IS_NEUTRAL below.

    Notes to vv.2-7, point 4: "In considering two lordships in any context,
    the Moolatrikona house has prime importance as against the other ordinary
    house."  — hence the mūlatrikoṇa tie-break, imported from dignity.py
    rather than retyped.

NATURAL BENEFICS AND MALEFICS — ch.34 vv.8-10
    "Jupiter and Venus are benefics while the Moon is mediocre in beneficence.
     Mercury is neutral (i.e. a benefic when associated with a benefic and a
     malefic when related to a malefic). Malefics are the Sun, Saturn and
     Mars. Full Moon, Mercury, Jupiter and Venus are stronger in the ascending
     order. Weak Moon, the Sun, Saturn and Mars are stronger (in malefic
     disposition) in the ascending order. In revealing maleficence due to
     angular rulership, the Moon, Mercury, Jupiter and Venus are significant
     in the ascending order."

RĀHU AND KETU — ch.34 vv.16-17
    v.16 "Rahu and Ketu give predominantly the effects as due to their
          conjunction with a house lord or as due to the house they occupy."
    v.17 "If a node is in an angle in aspect to or association with a trinal
          lord or be in a trine in similar relation with an angular lord it
          will become Yogakaraka."
    Note to v.16: "Inasmuch as they do not have a sign of their own, they
    have also not been specifically classified as malefic or benefic for the
    various ascendants ..."
    So the nodes get NO per-lagna nature here — 24 cells deliberately absent —
    but v.17 IS a positive rule and is exposed as node_yogakaraka().

---------------------------------------------------------------------------
OCR AND THE QUOTATION CONVENTION
---------------------------------------------------------------------------
The scan is uneven. Every quote below reproduces the English translation as
PRINTED IN THE SCAN, character for character, and EVERY repair is shown in
[square brackets] — including inserted spaces, shown as [ ]. So

    scan   "Auspicious effects will be givin by Mars, Jupiter and the Sun."
    here   "Auspicious effects will be giv[e]n by Mars, Jupiter and the Sun."

    scan   "Mars, Jupiter andthe Moon are malefics"
    here   "Mars, Jupiter and[ ]the Moon are malefics"

Nothing is silently normalised inside quote marks. Text after an em dash
inside a quote string is THIS MODULE'S editorial note, not the book.
Nothing was repaired where the reading itself was in doubt; see
CH44_VERSE_NUMBERING_AMBIGUOUS and AQU_MERCURY_OCR_AMBIGUOUS.
"""

from __future__ import annotations

from dignity import RASI_LORD, MOOLATRIKONA

# ---------------------------------------------------------------------------
# House groups — ch.34 vv.2-7
# ---------------------------------------------------------------------------

KENDRAS = (1, 4, 7, 10)          # angles
TRIKONAS = (1, 5, 9)             # trines
# The lagna is both, which is exactly why v.2-7 singles it out.
KENDRAS_EX_LAGNA = (4, 7, 10)
TRIKONAS_EX_LAGNA = (5, 9)

# "Any planet owning the 3rd, 6th, or the 11th will give evil effects."
# The note adds the order: "the 11th lord is the most evil in his group".
EVIL_HOUSES = (3, 6, 11)
EVIL_ASCENDING = (3, 6, 11)

# "The effects due to the lords of the 12th, and 8th will depend on their
# association."  Note point 7 puts the 2nd in the same group and orders them:
# "(b) 12th, 2nd and 8th ... the 8th lord is so [most evil] in his group."
CONDITIONAL_HOUSES = (2, 8, 12)
CONDITIONAL_ASCENDING = (12, 2, 8)

# Note point 8: "the 10th and 9th lords are the highest benefic planets while
# the 11th and 8th lords are the most adverse."
BEST_KENDRA, BEST_TRIKONA = 10, 9
WORST_EVIL, WORST_CONDITIONAL = 11, 8

# ---------------------------------------------------------------------------
# Natural nature — ch.34 vv.8-10
# ---------------------------------------------------------------------------

NATURAL_BENEFICS = ("jupiter", "venus", "moon")     # Moon "mediocre"
NATURAL_MALEFICS = ("sun", "saturn", "mars")
NATURAL_NEUTRAL = ("mercury",)

# "Weak Moon, the Sun, Saturn and Mars are stronger (in malefic disposition)
# in the ascending order."
MALEFIC_ASCENDING = ("moon_weak", "sun", "saturn", "mars")
# "Full Moon, Mercury, Jupiter and Venus are stronger in the ascending order."
BENEFIC_ASCENDING = ("moon_full", "mercury", "jupiter", "venus")
# "In revealing maleficence due to angular rulership, the Moon, Mercury,
# Jupiter and Venus are significant in the ascending order."
KENDRADHIPATYA_ASCENDING = ("moon", "mercury", "jupiter", "venus")

NODES = ("rahu", "ketu")
GRAHAS = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn",
          "rahu", "ketu")
SEVEN = GRAHAS[:7]

NODES_UNCLASSIFIED = (
    "ch.34 v.16 + note: the nodes own no rāśi, so BPHS 'has also not "
    "specifically classified [them] as malefic or benefic for the various "
    "ascendants'. They act per their dispositor, conjunction and occupied "
    "house. v.17 is the one positive rule — see node_yogakaraka()."
)

# ch.34 notes to vv.2-7, point 2. The verse says a malefic owning an angle
# "will not remain inauspicious"; the note refuses to read that as "becomes
# auspicious". Kept as a named constant because a lot of modern writing gets
# this backwards.
MALEFIC_KENDRA_IS_NEUTRAL = (
    "ch.34 note to vv.2-7 (2): 'If a malefic owns an angle he will not be "
    "inauspicious. This does not mean that he will become auspicious.' Only "
    "simultaneous trine lordship (v.14) makes him auspicious."
)

# ch.34 notes to vv.23-24 (Taurus). A NOTE, not a śloka — it is the reason the
# derivation gives Taurus/Sun and Scorpio/Sun a benefic reading rather than the
# bare-v.14 'neutral'.
LUMINARY_KENDRA_EXCEPTION = (
    "ch.34 note to vv.23-24 (NOTE, not śloka): 'The rule that a malefic "
    "owning an angle should own a trine also, so that he becomes a "
    "Yogakaraka (vide sloka 14 supra) is naturally not applicab[l]e to the "
    "luminaries as they own only one sign each.' Applied to the Sun only — "
    "the Moon is a natural benefic and falls under kendrādhipatya instead. "
    "See LUMINARY_EXCEPTION_NARROWED_TO_SUN: the note's wording is PLURAL."
)

# ---- Flags: places where this module makes a choice the text does not make --

LUMINARY_EXCEPTION_NARROWED_TO_SUN = (
    "NARROWING FLAG. The ch.34 note to vv.23-24 says the v.14 rule 'is "
    "naturally not applicab[l]e to the LUMINARIES as they own only one sign "
    "each' — plural, i.e. the Sun AND the Moon. This module applies it to "
    "the Sun only, on the ground that v.14 is a rule about MALEFICS owning "
    "angles and the Moon is a natural benefic (vv.8-10), so v.14 never "
    "reached her and there is nothing for the exception to disapply; she "
    "falls under kendrādhipatya doṣa (note to vv.2-7, point 1) instead. "
    "That reasoning is THIS MODULE'S, not the book's. The cells materially "
    "changed by the narrowing are Meṣa/Candra, Tulā/Candra and "
    "Makara/Candra — the three lagnas where the Moon owns a kendra and "
    "nothing else. Under the note's plural wording those three would derive "
    "'benefic' instead of the phase-dependent value below."
)

MOON_KENDRA_PHASE_DEPENDENT = (
    "PHASE FLAG. The two ch.34 notes to vv.2-7 scope the Moon's "
    "kendrādhipatya verdict to her PHASE and they do not agree with each "
    "other unless the phase is supplied:\n"
    "  point 1: 'Natural benefics are increasing Moon, Mercury, Jupiter and "
    "Venus. T[h]eir angular lordsbip blemish will be in the ascending "
    "order. That is the Moon is the least malefic a[n]d Venus is the most "
    "malefic by such ownership.'   -> INCREASING (waxing) Moon owning an "
    "angle is MALEFIC, least of the four.\n"
    "  point 2: 'weak Moon by virtue of angular lordship remains just "
    "neutral.'   -> WEAK (waning) Moon owning an angle is NEUTRAL.\n"
    "vv.8-10 make the same distinction ('Full Moon ...' vs 'Weak Moon ...'), "
    "so it is the text's distinction, not an imported one. "
    "classify_by_lordship() therefore REFUSES to return a nature for a "
    "kendra-only Moon unless moon_waxing is given: with moon_waxing=None it "
    "returns nature=None and this flag. Affects Meṣa/Candra (4th), "
    "Tulā/Candra (10th) and Makara/Candra (7th)."
)

# ch.34 vv.19-22 + its note. Mars for Meṣa is the module's sharpest
# demotion: the verse's own benefic list has exactly two names in it.
ARI_MARS_NOT_INDEPENDENTLY_BENEFIC = (
    "ch.34 vv.19-22 say of Mars only that '[h]e will be help[f]ul to "
    "(other) auspicious planets' — a CONDITIONAL clause. The verse's "
    "explicit benefic list is 'Auspicious are Jupiter and the Sun.' and the "
    "note closes the door twice: 'He cannot be independently auspicious but "
    "can he[l]p another favo[u]rable planet like the Sun or Jupiter or even "
    "the Moon through w[hom] he will reveal his good qua[l]ities' and 'As "
    "r[e]gards other unsullied benefic planets for this ascendant we have "
    "only two. These are Jupiter and the Sun.' So the book states there are "
    "exactly TWO benefics for Meṣa lagna and Mars is not one of them. Coded "
    "'conditional', NOT 'benefic'."
)

# The maraka -> nature leap this module refuses to make.
MARAKA_IS_NOT_A_NATURE = (
    "POLICY. A verse that says a graha 'is a killer' / 'will inflict death' "
    "has issued a MARAKA verdict, which ch.34's own note to vv.45-46 keeps "
    "strictly apart from nature: 'A killer is a killer irrespective of his "
    "havi[n]g become a Rajayogakaraka or so. Killer and Yogakaraka should "
    "not be mixed together in respect of o[n]e and the same planet.' A "
    "maraka verdict is therefore NEVER promoted to a benefic/malefic "
    "nature here. It is recorded in LAGNA_MARAKA and the nature cell is "
    "left None. Cells that fall to this policy: Mithuna/Candra, "
    "Vṛṣabha/Maṅgala, Siṁha/Candra, Kumbha/Sūrya, Dhanus/Śani."
)

DHANUS_SATURN_AMBIGUOUS = (
    "AMBIGUOUS — the text does not decide, so no nature is shipped.\n"
    "  Reading A (malefic): the note to vv.37-38 says 'S[a]turn is "
    "straightaway a killer, ruling the 2nd and the 3rd.' The 3rd is an evil "
    "house under vv.2-7 ('Any planet owning the 3rd, 6th, or the llth "
    "will[ ]give evil effects'), which would make him a malefic.\n"
    "  Reading B (not malefic): that sentence is a MARAKA verdict (see "
    "MARAKA_IS_NOT_A_NATURE), and the śloka itself opens exclusively — "
    "'Only Venus is is[ ]inauspicious.' — which on a strict reading bars "
    "any second malefic for this lagna. This module reads 'only' strictly "
    "in the opposite direction for Mithuna/Budha, so it must read it "
    "strictly here too.\n"
    "Neither the śloka nor the note states a nature for Śani in so many "
    "words. nature=None. The maraka verdict IS shipped, in LAGNA_MARAKA."
)

MITHUNA_MERCURY_AMBIGUOUS = (
    "AMBIGUOUS — the text does not decide, so no nature is shipped. The "
    "Mithuna śloka never names its own lagna lord. Its one positive clause "
    "is exclusive — 'while Venus is the only auspicious planet' — which on "
    "a strict reading bars Budha, yet vv.2-7 say 'The lord of the ascendant "
    "is specially auspicious as the ascendant is an angle as well as "
    "trine.' The notes to vv.25-26 discuss Guru, Śani, Maṅgala, Sūrya and "
    "Śukra for this lagna and pass over Budha in silence. General law and "
    "per-lagna verse point opposite ways and nothing in the chapter "
    "reconciles them. nature=None."
)

AQU_MERCURY_OCR_AMBIGUOUS = (
    "The Kumbha śloka's word for Budha is damaged in the scan: 'Mercury "
    "gives meddting eftlcts.' The repair is either 'medd[l]ing' or "
    "'m[i]dd[l]ing' — different words. The note settles the VERDICT if not "
    "the word: 'Mercury ruling the 5th and the 8th will give mixed "
    "results.' Coded 'mixed'; the quote is left with the damage marked."
)


# ---------------------------------------------------------------------------
# Lordship geometry.  Whole-sign bhāvas: house = sign - lagna + 1.
# ---------------------------------------------------------------------------

def house_of(sign: int, lagna: int) -> int:
    """Whole-sign bhāva number (1-12) of a rāśi for a given lagna rāśi."""
    return ((sign - lagna) % 12) + 1


def houses_owned(graha: str, lagna: int) -> tuple[int, ...]:
    """Bhāvas this graha lords for this lagna. Empty for the nodes."""
    return tuple(sorted(house_of(s, lagna)
                        for s in range(12) if RASI_LORD[s] == graha))


def moolatrikona_house(graha: str, lagna: int) -> int | None:
    """Which bhāva holds the graha's mūlatrikoṇa — the tie-break of note (4).

    Taken from dignity.MOOLATRIKONA rather than retyped; note that the Moon's
    mūlatrikoṇa rāśi is flagged unverified there, but only its SIGN matters
    here and the sign (Vṛṣabha) is not the part in doubt.
    """
    if graha not in MOOLATRIKONA:
        return None
    return house_of(MOOLATRIKONA[graha][0], lagna)


def lordship_profile(graha: str, lagna: int) -> dict:
    """Everything vv.2-7 needs to know about one graha's lordships."""
    owned = houses_owned(graha, lagna)
    return {
        "graha": graha,
        "lagna": lagna,
        "houses_owned": owned,
        "moolatrikona_house": moolatrikona_house(graha, lagna),
        "is_lagna_lord": 1 in owned,
        "kendras_owned": tuple(h for h in owned if h in KENDRAS_EX_LAGNA),
        "trikonas_owned": tuple(h for h in owned if h in TRIKONAS_EX_LAGNA),
        "evil_owned": tuple(h for h in owned if h in EVIL_HOUSES),
        "conditional_owned": tuple(h for h in owned if h in CONDITIONAL_HOUSES),
        "natural": ("benefic" if graha in NATURAL_BENEFICS else
                    "malefic" if graha in NATURAL_MALEFICS else
                    "neutral" if graha in NATURAL_NEUTRAL else None),
    }


# ---------------------------------------------------------------------------
# The general law, applied.  This is a DERIVATION from vv.2-7/13/14, not a
# transcription — hence it is kept in its own function and compared against
# the per-lagna verses rather than substituted for them.
# ---------------------------------------------------------------------------

def classify_by_lordship(graha: str, lagna: int,
                         moon_waxing: bool | None = None) -> dict:
    """Functional nature derived from the general law alone.

    Returns {'nature', 'rule', 'reasons', 'profile'}. `nature` is one of
    yogakaraka | benefic | mixed | neutral | conditional | malefic | None.

    `moon_waxing` is REQUIRED to classify a kendra-only Moon: the notes to
    vv.2-7 give her two different verdicts depending on phase (point 1,
    increasing Moon -> least malefic; point 2, weak Moon -> just neutral).
    Left None, that one cell returns nature=None and the
    MOON_KENDRA_PHASE_DEPENDENT flag rather than silently picking one.
    """
    p = lordship_profile(graha, lagna)
    owned, mt = p["houses_owned"], p["moolatrikona_house"]
    reasons: list[str] = []

    if not owned:
        return {"nature": None, "rule": "ch.34 v.16",
                "reasons": [NODES_UNCLASSIFIED], "profile": p}

    if p["kendras_owned"] and p["trikonas_owned"]:
        reasons.append("v.13: owns angle %s and trine %s"
                       % (p["kendras_owned"], p["trikonas_owned"]))
        return {"nature": "yogakaraka", "rule": "ch.34 v.13",
                "reasons": reasons, "profile": p}

    if p["is_lagna_lord"] and p["evil_owned"]:
        reasons.append("vv.2-7: lagna lord ('specially auspicious') but also "
                       "owns evil house %s" % (p["evil_owned"],))
        return {"nature": "mixed", "rule": "ch.34 vv.2-7",
                "reasons": reasons, "profile": p}

    if p["evil_owned"] and p["trikonas_owned"]:
        # "his simultaneous ownership of a trine will bestow auspicious
        # effects" vs. "any planet owning the 3rd, 6th, or the 11th will give
        # evil effects" — note (4) breaks the tie with the mūlatrikoṇa.
        if mt in p["evil_owned"]:
            nature = "malefic"
        elif mt in p["trikonas_owned"]:
            nature = "benefic"
        else:
            nature = "mixed"
        reasons.append("vv.2-7 + note(4): evil %s vs trine %s, mūlatrikoṇa in "
                       "the %dth decides" % (p["evil_owned"],
                                             p["trikonas_owned"], mt or 0))
        return {"nature": nature, "rule": "ch.34 vv.2-7 + note(4)",
                "reasons": reasons, "profile": p}

    if p["evil_owned"]:
        reasons.append("vv.2-7: owns %s — 'will give evil effects'"
                       % (p["evil_owned"],))
        return {"nature": "malefic", "rule": "ch.34 vv.2-7",
                "reasons": reasons, "profile": p}

    if p["is_lagna_lord"] and 8 in owned and graha not in ("sun", "moon"):
        reasons.append("vv.2-7: lagna lord, but also 8th lord — 'the 8th lord "
                       "is not auspicious as he owns the 12th from the 9th'")
        return {"nature": "neutral", "rule": "ch.34 vv.2-7",
                "reasons": reasons, "profile": p}

    if p["is_lagna_lord"]:
        reasons.append("vv.2-7: 'the lord of the ascendant is specially "
                       "auspicious as the ascendant is an angle as well as "
                       "trine'")
        return {"nature": "benefic", "rule": "ch.34 vv.2-7",
                "reasons": reasons, "profile": p}

    if p["trikonas_owned"]:
        reasons.append("vv.2-7: 'the lord of a trine will give auspicious "
                       "results' (%s)" % (p["trikonas_owned"],))
        return {"nature": "benefic", "rule": "ch.34 vv.2-7",
                "reasons": reasons, "profile": p}

    if p["kendras_owned"]:
        if graha == "sun":
            reasons.append(LUMINARY_KENDRA_EXCEPTION)
            return {"nature": "benefic", "rule": "ch.34 note to vv.23-24",
                    "reasons": reasons, "profile": p}
        if graha in KENDRADHIPATYA_ASCENDING:
            # "Benefics owning angles will not give benefic effects."
            # For the Moon the two notes to vv.2-7 disagree unless the phase
            # is known — point 1 (increasing Moon) makes her the LEAST
            # MALEFIC of the four, point 2 (weak Moon) makes her NEUTRAL.
            if graha == "moon":
                if moon_waxing is None:
                    reasons.append(MOON_KENDRA_PHASE_DEPENDENT)
                    reasons.append(LUMINARY_EXCEPTION_NARROWED_TO_SUN)
                    return {"nature": None,
                            "rule": "ch.34 notes to vv.2-7 (1) vs (2)"
                                    " — phase not supplied",
                            "reasons": reasons, "profile": p}
                if moon_waxing:
                    nature = "malefic"
                    reasons.append(
                        "vv.2-7 note (1): kendrādhipatya doṣa — 'increasing "
                        "Moon' owning angle %s; 'the Moon is the least "
                        "malefic' of the four (severity rank 1 of 4)"
                        % (p["kendras_owned"],))
                else:
                    nature = "neutral"
                    reasons.append(
                        "vv.2-7 note (2): 'weak Moon by virtue of angular "
                        "lordship remains just neutral' (angle %s)"
                        % (p["kendras_owned"],))
                reasons.append(LUMINARY_EXCEPTION_NARROWED_TO_SUN)
                return {"nature": nature, "rule": "ch.34 note to vv.2-7",
                        "reasons": reasons, "profile": p}
            reasons.append("vv.2-7: kendrādhipatya doṣa — natural benefic "
                           "owning angle %s (severity rank %d of 4)"
                           % (p["kendras_owned"],
                              KENDRADHIPATYA_ASCENDING.index(graha) + 1))
            return {"nature": "malefic", "rule": "ch.34 vv.2-7",
                    "reasons": reasons, "profile": p}
        reasons.append(MALEFIC_KENDRA_IS_NEUTRAL)
        return {"nature": "neutral", "rule": "ch.34 v.14",
                "reasons": reasons, "profile": p}

    if 8 in owned and graha in ("sun", "moon"):
        reasons.append("vv.2-7: 'the 8th lordship of the Sun and the Moon is "
                       "not evil'")
        return {"nature": "neutral", "rule": "ch.34 vv.2-7",
                "reasons": reasons, "profile": p}

    reasons.append("vv.2-7: 'the effects due to the lords of the 12th, and "
                   "8th will depend on their association' (%s)"
                   % (p["conditional_owned"],))
    return {"nature": "conditional", "rule": "ch.34 vv.2-7",
            "reasons": reasons, "profile": p}


def node_yogakaraka(node_house: int, related_lord_houses) -> bool:
    """ch.34 v.17 — the one positive rule the text gives a node.

    "If a node is in an angle in aspect to or association with a trinal lord
     or be in a trine in similar relation with an angular lord it will become
     Yogakaraka."

    `related_lord_houses` is the set of houses lorded by the graha(s) the node
    is conjoined with or aspected by.
    """
    rel = set(related_lord_houses)
    if node_house in KENDRAS and rel & set(TRIKONAS_EX_LAGNA):
        return True
    if node_house in TRIKONAS and rel & set(KENDRAS_EX_LAGNA):
        return True
    return False


# ---------------------------------------------------------------------------
# ch.34 vv.19-44 — the twelve lagnas, verse by verse.
#
# Each cell: (nature, source, citation, quote).
#   nature : benefic | malefic | neutral | mixed | yogakaraka | conditional
#            | None  — None means NEITHER śloka NOR note states one.
#   source : 'sloka' — the per-lagna verse itself says it
#            'note'  — only Santhanam's commentary says it
# `maraka` cells are separate and separately sourced.
# ---------------------------------------------------------------------------

_B, _M, _N, _X, _Y = "benefic", "malefic", "neutral", "mixed", "yogakaraka"
_C = "conditional"

LAGNA_NATURE: dict[int, dict[str, dict]] = {

    # ---- 0  Meṣa / Aries — vv.19-22 --------------------------------------
    0: {
        "sun":     (_B, "sloka", "ch.34 vv.19-22", "Auspicious are Jupiter and the Sun."),
        "moon":    (_X, "note",  "ch.34 note to vv.19-22",
                    "The Moon's role is not discussed by the sage. The Moon will give "
                    "mixed results according to association etc. as she is an angular ruler."),
        # NOT benefic — see ARI_MARS_NOT_INDEPENDENTLY_BENEFIC. The verse
        # names exactly two benefics for this lagna and Mars is not one.
        "mars":    (_C, "sloka", "ch.34 vv.19-22",
                    "Even though Mars is the lord of the 8th, [h]e will be help[f]ul "
                    "to (other) auspicious planets. — a CONDITIONAL clause; the "
                    "verse's own benefic list is 'Auspicious are Jupiter and the "
                    "Sun.' and the note adds 'He cannot be independently auspicious "
                    "but can he[l]p another favo[u]rable planet'."),
        "mercury": (_M, "sloka", "ch.34 vv.19-22", "Saturn, Mercury and Venus are malefics."),
        "jupiter": (_B, "sloka", "ch.34 vv.19-22", "Auspicious are Jupiter and the Sun."),
        "venus":   (_M, "sloka", "ch.34 vv.19-22", "Saturn, Mercury and Venus are malefics."),
        "saturn":  (_M, "sloka", "ch.34 vv.19-22", "Saturn, Mercury and Venus are malefics."),
    },

    # ---- 1  Vṛṣabha / Taurus — vv.23-24 ----------------------------------
    1: {
        "sun":     (_B, "sloka", "ch.34 vv.23-24", "Saturn and the Sun are auspicious."),
        "moon":    (_M, "sloka", "ch.34 vv.23-24", "Jupiter, Venus and the Moon are malefics."),
        # MARAKA ONLY. The śloka's malefic list is 'Jupiter, Venus and the
        # Moon' and omits Mars; the only text touching him is a killer
        # verdict. See MARAKA_IS_NOT_A_NATURE. The maraka cell is kept, in
        # LAGNA_MARAKA where it belongs.
        "mars":    (None, None,  "ch.34 vv.23-24 + note",
                    "Mars is classified as a killer apart from Jupiter, Venus and the "
                    "L[o]on. Mars is a killer for he owns the 7th and l2th. — a MARAKA "
                    "verdict only. The śloka's malefic list, 'Jupiter, Venus and the "
                    "Moon are malefics.', does not name Mars, and neither śloka nor "
                    "note states a nature for him."),
        # 'mixed' is the NOTE's word, not the śloka's ('somewhat auspicious').
        "mercury": (_X, "note",  "ch.34 note to vv.23-24",
                    "he is only of mixed nature for Taurus ascendant and he is not an "
                    "excellent benefic by virtue of o[w]ning a Maraka house in "
                    "addition to a trine. — the śloka itself says only 'Mercury is "
                    "somewhat auspicious,'; the word 'mixed' is Santhanam's."),
        "jupiter": (_M, "sloka", "ch.34 vv.23-24", "Jupiter, Venus and the Moon are malefics."),
        "venus":   (_M, "sloka", "ch.34 vv.23-24", "Jupiter, Venus and the Moon are malefics."),
        "saturn":  (_Y, "sloka", "ch.34 vv.23-24",
                    "Saturn and the Sun are auspicious. Saturn will cause Rajayoga."),
    },

    # ---- 2  Mithuna / Gemini — vv.25-26 ----------------------------------
    2: {
        "sun":     (_M, "sloka", "ch.34 vv.25-26", "Mars, Jupiter and the Sun are malefics."),
        "moon":    (None, None,  "ch.34 vv.25-26",
                    "The Moon is the prime killer, but it is[ ]dependant on her "
                    "association. — a MARAKA verdict only; no benefic/malefic "
                    "classification is given for her, in verse or in note."),
        "mars":    (_M, "sloka", "ch.34 vv.25-26", "Mars, Jupiter and the Sun are malefics."),
        "mercury": (None, None,  "ch.34 vv.25-26",
                    "The lagna lord is not named. The verse says 'Venus is the ONLY "
                    "auspicious planet', which read strictly excludes Mercury and "
                    "contradicts vv.2-7 ('the lord of the ascendant is specially "
                    "auspicious'). The notes do not resolve it. Left unstated."),
        "jupiter": (_M, "sloka", "ch.34 vv.25-26", "Mars, Jupiter and the Sun are malefics."),
        "venus":   (_B, "sloka", "ch.34 vv.25-26", "Venus is the only auspicious planet."),
        "saturn":  (_B, "note",  "ch.34 note to vv.2-7 (4) and to vv.25-26",
                    "There is no hint on saturn's role ... — and note (4): 'saturn, "
                    "though owning the 8th, will be favourab[l]e for a Gemini nativity "
                    "as he is the lord of the 9th as w[e]ll.'"),
    },

    # ---- 3  Karka / Cancer — vv.27-28 ------------------------------------
    3: {
        # The verse's 'give effects according to association' clause is a
        # NATURE clause and it governs BOTH named grahas, exactly as the
        # Kanyā verse's 'The Sun[']s role will depend on [his] association'
        # does. The note confirms it of both: 'they are not independently
        # capable of doing bad or good but act as per their relationship
        # with others.' Coded 'conditional' for parity with Kanyā/Sūrya.
        "sun":     (_C, "sloka", "ch.34 vv.27-28",
                    "Saturn and the Sun are killers and give effects according "
                    "to association."),
        "moon":    (_B, "sloka", "ch.34 vv.27-28", "Mars, Jupiter and the Moon are auspicious."),
        "mars":    (_Y, "sloka", "ch.34 vv.27-28",
                    "Mars is capable of conferring a full-fledged yoga and giving "
                    "auspicious effects."),
        "mercury": (_M, "sloka", "ch.34 vv.27-28", "Venus and Mercury are malefics."),
        "jupiter": (_B, "sloka", "ch.34 vv.27-28", "Mars, Jupiter and the Moon are auspicious."),
        "venus":   (_M, "sloka", "ch.34 vv.27-28", "Venus and Mercury are malefics."),
        # Was 'malefic' from 'hence he is classified as a killer' — a maraka
        # verdict, and the very next sentence of the same note withdraws
        # independent agency from him. Same clause, same verdict as the Sun.
        "saturn":  (_C, "sloka", "ch.34 vv.27-28",
                    "Saturn and the Sun are killers and give effects according "
                    "to association. — the note: 'Both the houses of Saturn are "
                    "inauspicious and hence he is classified as a killer. However, "
                    "they are not independently capable of doing bad or good but act "
                    "as per their relationship with others.'"),
    },

    # ---- 4  Siṁha / Leo — vv.29-30 ---------------------------------------
    4: {
        "sun":     (_B, "sloka", "ch.34 vv.29-30",
                    "Auspicious effects will be giv[e]n by Mars, Jupiter and the Sun."),
        "moon":    (None, None,  "ch.34 vv.29-30",
                    "Saturn and the Moon are killers who will give effects according "
                    "to [a]ssociation. — a MARAKA verdict only. The note adds only "
                    "Santhanam's OWN EXPERIENCE ('as per our experience'), which is "
                    "not taken as a classification."),
        "mars":    (_B, "sloka", "ch.34 vv.29-30",
                    "Auspicious effects will be given by Mars, Jupiter and the Sun."),
        "mercury": (_M, "sloka", "ch.34 vv.29-30", "Mercury, Venus and Saturn are malefics."),
        "jupiter": (_B, "sloka", "ch.34 vv.29-30",
                    "Auspicious effects will be given by Mars, Jupiter and the Sun."),
        "venus":   (_M, "sloka", "ch.34 vv.29-30", "Mercury, Venus and Saturn are malefics."),
        "saturn":  (_M, "sloka", "ch.34 vv.29-30", "Mercury, Venus and Saturn are malefics."),
    },

    # ---- 5  Kanyā / Virgo — vv.31-32 -------------------------------------
    5: {
        "sun":     ("conditional", "sloka", "ch.34 vv.31-32",
                    "The Sun[']s role will depend on [his] association."),
        "moon":    (_M, "sloka", "ch.34 vv.31-32",
                    "Mars, Jupiter and the Moon are malefics."),
        "mars":    (_M, "sloka", "ch.34 vv.31-32",
                    "Mars, Jupiter and the Moon are malefics."),
        "mercury": (_B, "sloka", "ch.34 vv.31-32",
                    "Mercury and Venus are auspicio[u]s."),
        "jupiter": (_M, "sloka", "ch.34 vv.31-32",
                    "Mars, Jupiter and the Moon are malefics."),
        "venus":   (_B, "sloka", "ch.34 vv.31-32",
                    "Mercury and Venus are auspicio[u]s. The conjunction of Venus and "
                    "Mercury will produce yoga. Venus is a killer as well."),
        "saturn":  (_X, "note",  "ch.34 note to vv.31-32",
                    "There is no hint in the text about Saturn's role. By virtue of "
                    "the 5th lordship and good relationship with the ascendant lord "
                    "Mercury, he will prove auspicious. But the stain due to 6th "
                    "[l]ordship will cause a change in his disposition and he cannot be "
                    "counted as an invariable dependent."),
    },

    # ---- 6  Tulā / Libra — vv.33-34 --------------------------------------
    6: {
        "sun":     (_M, "sloka", "ch.34 vv.33-34", "Jupiter, the Sun and Mars are malefics."),
        "moon":    (_B, "sloka", "ch.34 vv.33-34", "The Moon and Mercury will cause Rajayoga."),
        "mars":    (_M, "sloka", "ch.34 vv.33-34",
                    "Jupiter, the Sun and Mars are malefics. Mars is a killer."),
        "mercury": (_B, "sloka", "ch.34 vv.33-34",
                    "Auspicious are Saturn and Mercury. The Moon and Mercury will "
                    "cause Rajayoga."),
        "jupiter": (_M, "sloka", "ch.34 vv.33-34", "Jupiter, the Sun and Mars are malefics."),
        "venus":   (_N, "sloka", "ch.34 vv.33-34", "Venus is neutral."),
        "saturn":  (_B, "sloka", "ch.34 vv.33-34", "Auspicious are Saturn and Mercury."),
    },

    # ---- 7  Vṛścika / Scorpio — vv.35-36 ---------------------------------
    7: {
        "sun":     (_Y, "sloka", "ch.34 vv.35-36", "The Sun as well as the Moon are Yogakarakas."),
        "moon":    (_Y, "sloka", "ch.34 vv.35-36",
                    "Jupiter and the Moon are auspicious. The Sun as well as the Moon "
                    "are Yogakarakas."),
        "mars":    (_N, "sloka", "ch.34 vv.35-36", "Mars is neutral."),
        "mercury": (_M, "sloka", "ch.34 vv.35-36", "Venus, Mercury and Saturn are malefics."),
        "jupiter": (_B, "sloka", "ch.34 vv.35-36", "Jupiter and the Moon are auspicious."),
        "venus":   (_M, "sloka", "ch.34 vv.35-36", "Venus, Mercury and Saturn are malefics."),
        "saturn":  (_M, "sloka", "ch.34 vv.35-36", "Venus, Mercury and Saturn are malefics."),
    },

    # ---- 8  Dhanus / Sagittarius — vv.37-38 ------------------------------
    8: {
        "sun":     (_B, "sloka", "ch.34 vv.37-38",
                    "Mars and the Sun are auspicious. The Sun and[ ]Mercury are capable "
                    "of conferrin[g] [a] yo[ga]."),
        "moon":    (_X, "note",  "ch.34 note to vv.37-38",
                    "The Moon ruling the 8th cannot be a powerful yogakaraka unless "
                    "well-re[la]te[d] to Mercury, the Sun or Mars."),
        "mars":    (_B, "sloka", "ch.34 vv.37-38", "Mars and the Sun are auspicious."),
        "mercury": (_B, "sloka", "ch.34 vv.37-38",
                    "The Sun and[ ]Mercury are capable of conferrin[g] [a] yo[ga]."),
        "jupiter": (_N, "sloka", "ch.34 vv.37-38", "Jupiter is neutral."),
        "venus":   (_M, "sloka", "ch.34 vv.37-38",
                    "Only Venus is[ ]inauspicious. ... [V]enus acquires ki[ll]ing powers."),
        # MARAKA ONLY, and contradicted by the verse's own exclusivity
        # ('Only Venus is inauspicious'). See DHANUS_SATURN_AMBIGUOUS.
        "saturn":  (None, None,  "ch.34 vv.37-38 + note",
                    "S[a]turn is straightaway a killer, ruling the 2nd and the 3rd. — "
                    "a MARAKA verdict only, and the śloka opens 'Only Venus is"
                    "[ ]inauspicious.', which read strictly bars a second malefic for "
                    "this lagna. The text does not decide; nature=None."),
    },

    # ---- 9  Makara / Capricorn — vv.39-40 --------------------------------
    9: {
        "sun":     (_N, "sloka", "ch.34 vv.39-40", "The Sun is neutral."),
        "moon":    (_M, "sloka", "ch.34 vv.39-40", "Mars, Jupiter and the Moon are malefics."),
        "mars":    (_M, "sloka", "ch.34 vv.39-40",
                    "Mars, Jupiter and[ ]the Moon are malefics. ... Mars and other "
                    "malefics[ ]will inflict death."),
        "mercury": (_B, "sloka", "ch.34 vv.39-40", "Venus and Mercury are auspicious."),
        "jupiter": (_M, "sloka", "ch.34 vv.39-40", "Mars, Jupiter and the Moon are malefics."),
        "venus":   (_Y, "sloka", "ch.34 vv.39-40",
                    "Only Venus is capable of causing a superior yoga."),
        "saturn":  (_N, "note",  "ch.34 note to vv.39-40",
                    "Saturn and the Sun are neither very favourable nor very[ ]adverse."),
    },

    # ---- 10  Kumbha / Aquarius — vv.41-42 --------------------------------
    10: {
        "sun":     (None, None,  "ch.34 vv.41-42",
                    "Jupiter, the Sun and Mars are killers. — a MARAKA verdict only; "
                    "the note explains only that 'the Sun is termed as a killer as he "
                    "rules the 7th, a maraka house'. No nature is stated."),
        "moon":    (_M, "sloka", "ch.34 vv.41-42", "Jupiter, the Moon and Mars are malefics."),
        "mars":    (_M, "sloka", "ch.34 vv.41-42", "Jupiter, the Moon and Mars are malefics."),
        # Quoted with the damage intact: the scan reads "meddting eftlcts" and
        # does NOT decide between "meddling" and "middling", which point opposite
        # ways (interfering vs middling/mediocre). Repairing it inside the quote
        # would hide the choice. See AQU_MERCURY_OCR_AMBIGUOUS.
        "mercury": (_X, "sloka", "ch.34 vv.41-42", "Mercury gives meddting eftlcts. — damaged; see AQU_MERCURY_OCR_AMBIGUOUS."),
        "jupiter": (_M, "sloka", "ch.34 vv.41-42", "Jupiter, the Moon and Mars are malefics."),
        "venus":   (_Y, "sloka", "ch.34 vv.41-42",
                    "Venus and Satu[r]n are auspicious. Ve[nu]s is the only Rajayoga "
                    "causing planet."),
        "saturn":  (_B, "sloka", "ch.34 vv.41-42", "Venus and Satu[r]n are auspicious."),
    },

    # ---- 11  Mīna / Pisces — vv.43-44 ------------------------------------
    11: {
        "sun":     (_M, "sloka", "ch.34 vv.43-44",
                    "Saturn, Venus, the Sun[ ]and Mercury are malefics."),
        "moon":    (_B, "sloka", "ch.34 vv.43-44", "Mars and the Moon are auspicious."),
        "mars":    (_B, "sloka", "ch.34 vv.43-44",
                    "Mars and the Moon are auspicious. Mars and Jupiter will cause [a] "
                    "yoga. Though Mars is [a] ki[lle]r, he will not kill the native "
                    "(independent[l]y)."),
        "mercury": (_M, "sloka", "ch.34 vv.43-44",
                    "Saturn, Venus, the Sun and Mercury are malefics."),
        "jupiter": (_B, "sloka", "ch.34 vv.43-44", "Mars and Jupiter will cause [a] yoga."),
        "venus":   (_M, "sloka", "ch.34 vv.43-44",
                    "Saturn, Venus, the Sun and Mercury are malefics."),
        "saturn":  (_M, "sloka", "ch.34 vv.43-44",
                    "Saturn, Venus, the Sun and Mercury are malefics."),
    },
}

# The per-lagna MARAKA verdicts of ch.34, kept apart from nature because the
# text keeps them apart: "A killer is a killer irrespective of his having
# become a Rajayogakaraka or so. Killer and Yogakaraka should not be mixed
# together in respect of one and the same planet." (note to vv.45-46)
#   'primary'     — kills of its own
#   'conditional' — kills only in association with another maraka/adverse graha
LAGNA_MARAKA: dict[int, dict[str, tuple[str, str, str]]] = {
    0: {"venus":  ("primary", "sloka", "Venus is a direct (or independent) killer."),
        "saturn": ("conditional", "sloka",
                   "[S]aturn etc. will also inflict death if associated with an "
                   "ad[V]erse[ ]planet (i.e. Venus)."),
        "mercury": ("conditional", "note",
                    "Saturn and Mercury will also inflict death if related to Venus.")},
    1: {"jupiter": ("primary", "sloka", "Jupiter etc. and Mars will inflict death."),
        "venus":   ("primary", "note",
                    "The words 'Jeevadayo' indicate the Jupiter group, i.e. Jupiter, "
                    "the Moon and Venus."),
        "mars":    ("primary", "sloka", "Jupiter etc. and Mars will inflict death."),
        "moon":    ("conditional", "note",
                    "Though the Moon is said to be a killer, she cannot independently "
                    "do so ... Her connections with Jupiter, or Mars can empower her "
                    "to inflict death on the Taurus native.")},
    2: {"moon": ("conditional", "sloka",
                 "The Moon is the prime killer, but it is[ ]dependant on her association.")},
    3: {"saturn": ("conditional", "sloka",
                   "Saturn and the Sun are killers and give effects according to association."),
        "sun":    ("conditional", "sloka",
                   "Saturn and the Sun are killers and give effects according to association.")},
    4: {"saturn": ("conditional", "sloka",
                   "Saturn and the Moon are killers who will give effects according to [a]ssociation."),
        "moon":   ("conditional", "sloka",
                   "Saturn and the Moon are killers who will give effects according to association.")},
    5: {"venus": ("primary", "sloka", "Venus is a killer as well."),
        "mars":  ("conditional", "note", "(Mars ruling the 8th can also act as a killer.)")},
    6: {"mars":    ("primary", "sloka", "Mars is a killer."),
        "jupiter": ("conditional", "sloka",
                    "Jupiter and other malefics will also acquire a[ ]disposition to "
                    "inflict death."),
        "sun":     ("conditional", "sloka",
                    "Jupiter and other malefics will also acquire a disposition to "
                    "inflict death.")},
    7: {"venus":   ("primary", "sloka",
                    "Venus and other malefics acquire the quality of causing d[e]ath."),
        "mercury": ("conditional", "sloka",
                    "Venus and other malefics acquire the quality of causing death."),
        "saturn":  ("conditional", "sloka",
                    "Venus and other malefics acquire the quality of causing death.")},
    8: {"saturn": ("primary", "sloka", "Saturn is a killer."),
        "venus":  ("conditional", "sloka", "Venus acquires killing powers.")},
    9: {"mars":   ("primary", "sloka", "Mars and other malefics will inflict death."),
        "saturn": ("conditional", "note",
                   "Saturn will reveal killing powers if he joins Jupiter, Mars or the Moon."
                   " — the śloka itself says only 'Saturn will not be a killer of his own'.")},
    10: {"jupiter": ("primary", "sloka", "Jupiter, [the] Su[n] [a]nd Mars are killers."),
         "sun":     ("primary", "sloka", "Jupiter, the Sun and Mars are killers."),
         "mars":    ("primary", "sloka",
                     "Jupiter, [the] Su[n] [a]nd Mars are killers. — note: 'Out of t[h]e 3 "
                     "killers, Mars is the last in order.'")},
    11: {"saturn":  ("primary", "sloka", "[S]aturn and Mercury are killers."),
         "mercury": ("primary", "sloka", "Saturn and Mercury are killers."),
         "mars":    ("conditional", "sloka",
                     "Though Mars is [a] ki[lle]r, he will not kill the native "
                     "(independent[l]y). ... To be a killer, Mars must be "
                     "instigated by another killer. viz. [S]aturn or Mercury."),
         "venus":   ("conditional", "note",
                     "Though there is no specific mention of Venus becoming a killer, "
                     "such role can be seen in him as he owns the 8th house.")},
}

# The cells shipped with NO nature: either both śloka and note are silent,
# or the only text touching the cell is a maraka verdict, which this module
# refuses to promote (MARAKA_IS_NOT_A_NATURE) — or the two readings conflict
# and the text does not decide (DHANUS_SATURN_AMBIGUOUS).
NATURE_UNAVAILABLE = tuple(sorted(
    (lagna, graha)
    for lagna, row in LAGNA_NATURE.items()
    for graha, cell in row.items()
    if cell[0] is None
))

# Per-cell flags, surfaced by functional_nature() so the API layer can act on
# them rather than having to know this module's internals. House pattern:
# dignity.MOOLATRIKONA_UNVERIFIED.
NATURE_CELL_FLAGS: dict[tuple[int, str], tuple[str, ...]] = {
    (0, "mars"):   (ARI_MARS_NOT_INDEPENDENTLY_BENEFIC,),
    (1, "mars"):   (MARAKA_IS_NOT_A_NATURE,),
    (2, "moon"):   (MARAKA_IS_NOT_A_NATURE,),
    (2, "mercury"): (MITHUNA_MERCURY_AMBIGUOUS,),
    (4, "moon"):   (MARAKA_IS_NOT_A_NATURE,),
    (8, "saturn"): (DHANUS_SATURN_AMBIGUOUS, MARAKA_IS_NOT_A_NATURE),
    (10, "sun"):   (MARAKA_IS_NOT_A_NATURE,),
    (10, "mercury"): (AQU_MERCURY_OCR_AMBIGUOUS,),
}

# The cells whose nature comes only from Santhanam.
NATURE_FROM_NOTE_ONLY = tuple(sorted(
    (lagna, graha)
    for lagna, row in LAGNA_NATURE.items()
    for graha, cell in row.items()
    if cell[1] == "note"
))


def functional_nature(graha: str, lagna: int) -> dict:
    """The text's own verdict for this graha at this lagna, with its source.

    Never falls back to the derivation. If the text is silent, `nature` is
    None and `source` is None — call classify_by_lordship() explicitly if a
    derived value is wanted, and label it as derived.
    """
    if graha in NODES:
        return {"graha": graha, "lagna": lagna, "nature": None, "source": None,
                "citation": "ch.34 vv.16-17", "quote": NODES_UNCLASSIFIED,
                "maraka": None, "maraka_source": None, "is_node": True}

    nature, source, citation, quote = LAGNA_NATURE[lagna][graha]
    mk = LAGNA_MARAKA[lagna].get(graha)
    return {
        "graha": graha, "lagna": lagna,
        "nature": nature, "source": source,
        "citation": citation, "quote": quote,
        "maraka": mk[0] if mk else None,
        "maraka_source": mk[1] if mk else None,
        "maraka_quote": mk[2] if mk else None,
        "is_node": False,
        "flags": list(NATURE_CELL_FLAGS.get((lagna, graha), ())),
    }


def lagna_profile(lagna: int, moon_waxing: bool | None = None) -> dict:
    """All nine grahas for one lagna: text verdict, derivation, and agreement.

    `moon_waxing` is passed straight to classify_by_lordship(); left None,
    a kendra-only Moon derives nature=None rather than a guessed one.
    """
    rows = []
    for g in GRAHAS:
        text = functional_nature(g, lagna)
        derived = classify_by_lordship(g, lagna, moon_waxing)
        rows.append({
            **text,
            "houses_owned": derived["profile"]["houses_owned"],
            "moolatrikona_house": derived["profile"]["moolatrikona_house"],
            "derived_nature": derived["nature"],
            "derived_rule": derived["rule"],
            "derived_reasons": derived["reasons"],
            "agreement": _agreement(text["nature"], derived["nature"]),
        })
    return {"lagna": lagna, "grahas": rows,
            "yogakarakas": [r["graha"] for r in rows
                            if r["derived_nature"] == "yogakaraka"],
            "maraka_houses": maraka_houses(lagna)}


# ---------------------------------------------------------------------------
# Text vs. general law.  Reported, not resolved.
# ---------------------------------------------------------------------------

# Ordering used only to grade how far apart two verdicts are.
_RANK = {"yogakaraka": 2, "benefic": 1, "mixed": 0, "neutral": 0,
         "conditional": 0, "malefic": -1}


def _agreement(text_nature, derived_nature) -> str:
    if text_nature is None:
        return "no_text_verdict"
    if derived_nature is None:
        return "no_derived_verdict"
    if text_nature == derived_nature:
        return "exact"
    if abs(_RANK[text_nature] - _RANK[derived_nature]) <= 1:
        return "partial"
    return "conflict"


def disagreements(level: str = "conflict",
                  moon_waxing: bool | None = None) -> list[dict]:
    """Cells where the per-lagna verse and the general law do not agree.

    level 'conflict' returns only sign-flips (benefic vs malefic); 'partial'
    also returns the softer mismatches.
    """
    want = {"conflict"} if level == "conflict" else {"conflict", "partial"}
    out = []
    for lagna in range(12):
        for g in SEVEN:
            text = functional_nature(g, lagna)
            derived = classify_by_lordship(g, lagna, moon_waxing)
            verdict = _agreement(text["nature"], derived["nature"])
            if verdict in want:
                out.append({
                    "lagna": lagna, "graha": g,
                    "text_nature": text["nature"], "text_source": text["source"],
                    "citation": text["citation"],
                    "derived_nature": derived["nature"],
                    "derived_rule": derived["rule"],
                    "level": verdict,
                })
    return out


# Two cells where the per-lagna verse flatly reverses the general law's sign.
# Santhanam flags both himself; neither is silently preferred here.
KNOWN_CONFLICTS = {
    (3, "jupiter"): (
        "Cancer lagna. vv.27-28 call Jupiter auspicious. By vv.2-7 + note(4) "
        "he owns the 6th (evil, AND his mūlatrikoṇa) and the 9th, so the "
        "mūlatrikoṇa tie-break makes him malefic. Santhanam: 'Though 6th is "
        "his Moolatrikona, the sage has given preference to the 9th "
        "lordship' — i.e. the sage overrode his own tie-break here."
    ),
    (8, "mercury"): (
        "Sagittarius lagna. vv.37-38 make Mercury a yoga-giver. By vv.2-7 he "
        "owns the 7th and 10th, two kendras and no trine, which is textbook "
        "kendrādhipatya doṣa — the identical shape that makes Jupiter a "
        "malefic for Gemini (7th+10th) and for Virgo (4th+7th). Santhanam: "
        "'This supreme role of Mercury is possibly because of his ownership "
        "of the 10th house (moolatrikona and hence predominant against 7th "
        "house ownership) whereas Jupiter does not own Moolatrikona "
        "identical with the 10th house.'"
    ),
}

# Same lordship shape, opposite verdict — inside the ślokas themselves.
INTERNAL_ASYMMETRIES = {
    "lagna_lord_owning_the_6th": (
        "Taurus/Venus (owns 1st + 6th, mūlatrikoṇa in the 6th) is called a "
        "malefic in vv.23-24, but Scorpio/Mars (owns 1st + 6th, mūlatrikoṇa "
        "in the 6th) is called neutral in vv.35-36. Santhanam raises it: "
        "'for Scorpio ascendant there is no blemish (to Mars) of the 6th "
        "lordship and also for Taurus ascendant (in the case of Venus) ... "
        "Sage Parasara apparently took into serious consideration the 6th "
        "lordship (Moolatrikona) of Venus and classified him as an "
        "adversary.' Both are reported as 'mixed' by the derivation."
    ),
    "lagna_lord_owning_the_8th": (
        "Aries/Mars (owns 1st + 8th) gets a CONDITIONAL clause in vv.19-22 "
        "('[h]e will be help[f]ul to (other) auspicious planets'), while "
        "Libra/Venus (owns 1st + 8th) is flatly 'neutral' in vv.33-34 — and "
        "Santhanam explains only the latter ('Although Venus is the ruler of "
        "the as[c]endant, he owns 8th as well, and hence the sage term him "
        "as neutral'). Both mūlatrikoṇas sit in the lagna. The two verdicts "
        "are close but not identical and the text never reconciles them."
    ),
    "sun_owning_a_lone_kendra": (
        "vv.35-36 make the Sun — 10th lord only — a YOGAKARAKA for Scorpio, "
        "which v.14 forbids ('true only when it simultaneously lords over a "
        "trine'). The reconciliation is a NOTE, not a śloka: the luminaries "
        "own one sign each and so are exempt from v.14. See "
        "LUMINARY_KENDRA_EXCEPTION."
    ),
}


# ---------------------------------------------------------------------------
# MARAKA — BPHS Vol I ch.44
# ---------------------------------------------------------------------------
#
#   v.2   "O Brahmin, the 3rd and 8th are the two houses of longevity. The
#          houses related to death are the 12th from each of these, i.e. the
#          2nd and 7th are Maraka houses."
#
#   vv.3-5 "Out of the two (i.e. 2nd and 7th) the 2nd is a powerful Maraka
#          house (as against the 7th). The lords of the 2nd and the 7th,
#          malefics in the 2nd and the 7th, and malefics accompanying the 2nd
#          and the 7th lords are all known as Marakas. The major and sub
#          periods of these planets will bring death on the native depending
#          on whether he has a long life, medium life or short life."
#
#   vv.6-7 "The Dasa of a benefic planet related to the 12th lord may also
#          inflict death. End may descend on the native in the 8th lord's
#          Dasa. The Dasa of a planet which is an exclusive malefic (i.e.
#          first-rate malefic) may also cause death."
#
#   v.8   "The dasa of a malefic will not cause death in the Antardasa (sub
#          period) of a benefic planet, although the former is related to the
#          latter, but in the sub period of a malefic though not related."
#
#   v.9   "Should Saturn be ill-disposed and be related to a maraka planet, he
#          will be the first to kill in preference to other planets."
#
#   vv.22-24 "If Rahu or Ketu be in the ascendant, 7th, 8th or 12th thereof or
#          be in the 7th from a Maraka lord or be with such a planet, they
#          acquire powers of killing in their major or sub periods. For one
#          born in Capricorn or in Scorpio, Rahu will be a Maraka."
# ---------------------------------------------------------------------------

MARAKA_HOUSES = (2, 7)
MARAKA_STRONGEST = 2               # v.3
LONGEVITY_HOUSES = (3, 8)          # v.2

CH44_VERSE_NUMBERING_AMBIGUOUS = (
    "The scan labels the first English block of ch.44 '2-5.' and the next "
    "block '3.', while the intervening Sanskrit carries the markers for vv.3, "
    "4 and 5. The block boundaries are unambiguous but the numbers are not: "
    "the 'the 3rd and 8th are houses of longevity' passage is v.2, and the "
    "'lords of the 2nd and the 7th ... are all known as Marakas' passage "
    "covers vv.3-5. Cited here as 'ch.44 v.2' and 'ch.44 vv.3-5'. This "
    "corrects the working note that had it as 'vv.2-9'."
)

# ch.44 note to vv.6-7 — Santhanam's ranking, NOT a śloka. He extends maraka
# power to the 3rd, 8th and 12th (occupants as well as lords) and then grades:
#   "the Maraka planets in the ascending [order] are: occupants of or lords of
#    12th, 3rd, 8th, 7th and 2nd. The lords/occupants of 6th and 11th are
#    second grade killers. The last group consists of occupants/lords of 5th,
#    9th, 10th, 4th and 1st. They are the least marakas."
MARAKA_GRADES_NOTE = {
    "primary": (12, 3, 8, 7, 2),
    "second_grade": (6, 11),
    "least": (5, 9, 10, 4, 1),
}
MARAKA_GRADES_SOURCE = "note"

RAHU_PRIMARY_MARAKA_LAGNAS = (9, 7)      # Makara, Vṛścika — ch.44 vv.22-24
NODE_MARAKA_HOUSES = (1, 7, 8, 12)       # ch.44 vv.22-24 (śloka)
NODE_MARAKA_HOUSES_NOTE = (2,)           # note: "The 2nd house is naturally
                                         # added as another node will be in the
                                         # 2nd when one is in the specified 8th"
NODE_NON_MARAKA_HOUSES = (3, 5, 9, 11)   # note: "They will not be Marakas if
                                         # they are in the 3rd, 9th, 5th and 11th"

NODE_EXCLUSION_PRECEDENCE = (
    "PRECEDENCE FLAG. ch.44's note to vv.22-24 puts two sentences in this "
    "order: 'They will not be Marakas if they are in the 3rd, 9th, 5th and "
    "llth houses. lf a node joins a Maraka planet (or is in the house of a "
    "Maraka planet) it will act[ ]as[ ]a Maraka.' The text does not say "
    "which wins when a node sits in one of the four excluded houses AND "
    "meets a qualification — nor when it is Rāhu in an excluded house for "
    "Makara/Vṛścika, whom the śloka names a primary maraka outright. This "
    "module gives the EXCLUSION precedence, because it is the more specific "
    "and the more conservative rule. The choice is this module's, not the "
    "book's, so nothing is dropped: a node that qualified but was excluded "
    "is returned under 'nodes_suppressed' with its reasons and a "
    "'suppressed_by' field, and can be re-promoted by a caller who reads "
    "the precedence the other way."
)

# ch.44 vv.22-24, final clause. NOT IMPLEMENTED — needs aspect data, which
# this module does not take. Declared rather than silently omitted.
CH44_RAHU_DUSTHANA_GAP = (
    "GAP. ch.44 vv.22-24 close with a rule this module does NOT implement: "
    "'Should Rahu be in the 6th, 8[t]h or [1]2th, h[e] will give[ ]"
    "d[i]ff[i]culties in his dasa periods. He will not, howevcr, do so if "
    "aspected by or conjunct a bene[f]ic.' The exemption turns on aspect "
    "and conjunction, which maraka_analysis() has no input for, so the "
    "rule is declared here rather than half-applied. Note it is a "
    "DIFFICULTY rule, not strictly a maraka rule — the 8th and 12th "
    "already qualify as maraka houses under NODE_MARAKA_HOUSES; the 6th "
    "does not, and is not treated as one here."
)


def maraka_houses(lagna: int) -> dict:
    """The two death-dealing bhāvas and their rāśis/lords for this lagna."""
    out = {}
    for h in MARAKA_HOUSES:
        sign = (lagna + h - 1) % 12
        out[h] = {"sign": sign, "lord": RASI_LORD[sign],
                  "strength": "strongest" if h == MARAKA_STRONGEST else "secondary"}
    return out


def maraka_lords(lagna: int) -> dict[str, list[int]]:
    """graha -> the maraka house(s) it lords, for this lagna (ch.44 vv.3-5)."""
    out: dict[str, list[int]] = {}
    for h, info in maraka_houses(lagna).items():
        out.setdefault(info["lord"], []).append(h)
    return {g: sorted(hs) for g, hs in out.items()}


def natural_nature(graha: str, moon_waxing: bool = True,
                   mercury_with_malefic: bool | None = None) -> str:
    """ch.34 vv.8-10, applied to one graha in one chart.

    The Moon's and Mercury's classes are conditional in the verse itself, so
    they are conditional here: "the Moon is mediocre in beneficence" (weak
    Moon is listed among the malefics), "Mercury is neutral (i.e. a benefic
    when associated with a benefic and a malefic when related to a malefic)".
    `mercury_with_malefic=None` leaves Mercury 'neutral'.
    """
    if graha in NODES:
        return "unclassified"          # ch.34 v.16
    if graha == "moon":
        return "benefic" if moon_waxing else "malefic"
    if graha == "mercury":
        if mercury_with_malefic is None:
            return "neutral"
        return "malefic" if mercury_with_malefic else "benefic"
    return "benefic" if graha in NATURAL_BENEFICS else "malefic"


def maraka_analysis(lagna: int, positions: dict[str, int],
                    moon_waxing: bool = True,
                    saturn_ill_disposed: bool = False) -> dict:
    """Apply ch.44 vv.3-9 and vv.22-24 to a chart.

    `positions` maps graha key -> rāśi index 0-11 (whole-sign bhāvas, so the
    sign is all that is needed). Grahas absent from the dict are simply not
    placed; lordship-based marakas are still reported.

    Returns the three śloka categories separately, plus the node rule, plus
    v.9's Saturn precedence — none of them merged, because BPHS grades them.
    """
    houses = {g: house_of(s, lagna) for g, s in positions.items()}
    natural = {g: natural_nature(g, moon_waxing) for g in positions}
    lords = maraka_lords(lagna)

    by_lordship = [
        {"graha": g, "houses": hs, "reason": "lord of maraka house %s" % (hs,),
         "citation": "ch.44 vv.3-5",
         "strength": "strongest" if MARAKA_STRONGEST in hs else "secondary"}
        for g, hs in sorted(lords.items())
    ]

    malefics_in = [
        {"graha": g, "house": houses[g],
         "reason": "malefic occupying the %dth" % houses[g],
         "citation": "ch.44 vv.3-5"}
        for g in sorted(positions)
        if houses[g] in MARAKA_HOUSES and natural.get(g) == "malefic"
    ]

    lord_signs = {positions[g] for g in lords if g in positions}
    with_lords = [
        {"graha": g, "house": houses[g],
         "reason": "malefic conjoined a maraka lord",
         "citation": "ch.44 vv.3-5"}
        for g in sorted(positions)
        if g not in lords and natural.get(g) == "malefic"
        and positions[g] in lord_signs
    ]

    # vv.22-24 — the nodes, which ch.34 refused to classify but ch.44 does.
    nodes = []
    nodes_suppressed = []
    for n in NODES:
        if n not in houses:
            continue
        h = houses[n]
        hits = []
        if h in NODE_MARAKA_HOUSES:
            hits.append(("sloka", "in the %dth" % h))
        elif h in NODE_MARAKA_HOUSES_NOTE:
            hits.append(("note", "in the 2nd (added by the note)"))
        for g in lords:
            if g in positions:
                if positions[n] == positions[g]:
                    hits.append(("sloka", "conjoined the maraka lord %s" % g))
                elif house_of(positions[n], positions[g]) == 7:
                    hits.append(("sloka", "7th from the maraka lord %s" % g))
        if n == "rahu" and lagna in RAHU_PRIMARY_MARAKA_LAGNAS:
            hits.append(("sloka", "Rahu is a primary maraka for this lagna"))
        if not hits:
            continue
        entry = {"graha": n, "house": h,
                 "reasons": [r for _, r in hits],
                 "sources": sorted({s for s, _ in hits}),
                 "citation": "ch.44 vv.22-24"}
        if h in NODE_NON_MARAKA_HOUSES:
            # Qualified, then excluded. Reported, not dropped — the text
            # does not settle which sentence wins. See the flag.
            entry["suppressed_by"] = (
                "note to vv.22-24: 'They will not be Marakas if they are in "
                "the 3rd, 9th, 5th and llth houses.' (house %d)" % h)
            entry["precedence_flag"] = NODE_EXCLUSION_PRECEDENCE
            nodes_suppressed.append(entry)
        else:
            nodes.append(entry)

    named = {d["graha"] for d in by_lordship + malefics_in + with_lords}
    saturn = None
    if saturn_ill_disposed and ("saturn" in named
                                or (positions.get("saturn") in lord_signs)):
        saturn = {
            "graha": "saturn", "citation": "ch.44 v.9",
            "quote": "Should Saturn be ill-disposed and be related to a maraka "
                     "planet, he will be the first to kill in preference to "
                     "other planets.",
            "precedence": "first",
        }

    eighth = RASI_LORD[(lagna + 7) % 12]
    twelfth = RASI_LORD[(lagna + 11) % 12]

    return {
        "lagna": lagna,
        "maraka_houses": maraka_houses(lagna),
        "by_lordship": by_lordship,
        "malefics_in_maraka_houses": malefics_in,
        "malefics_with_maraka_lords": with_lords,
        "nodes": nodes,
        "nodes_suppressed": nodes_suppressed,
        "node_exclusion_precedence": NODE_EXCLUSION_PRECEDENCE,
        "unimplemented": [CH44_RAHU_DUSTHANA_GAP],
        "saturn_precedence": saturn,
        "secondary": {
            "eighth_lord": eighth,
            "twelfth_lord": twelfth,
            "citation": "ch.44 vv.6-7",
            "quote": "The Dasa of a benefic planet related to the 12th lord may "
                     "also inflict death. End may descend on the native in the "
                     "8th lord's Dasa. The Dasa of a planet which is an "
                     "exclusive malefic may also cause death.",
        },
        "antardasa_rule": {
            "citation": "ch.44 v.8",
            "quote": "The dasa of a malefic will not cause death in the "
                     "Antardasa of a benefic planet, although the former is "
                     "related to the latter, but in the sub period of a malefic "
                     "though not related.",
        },
        "chapter34_marakas": {
            g: {"grade": v[0], "source": v[1], "quote": v[2]}
            for g, v in sorted(LAGNA_MARAKA[lagna].items())
        },
    }


def maraka_grade(house: int) -> str:
    """Santhanam's three-tier maraka ranking (NOTE to ch.44 vv.6-7)."""
    for grade, hs in MARAKA_GRADES_NOTE.items():
        if house in hs:
            return grade
    return "least"
