"""Cara (variable) and sthira (fixed) kārakas — BPHS Vol I, Chapter 32.
Kārakāṁśa — BPHS Vol I, Chapter 33 v.1.

Every rule here is transcribed from the ślokas as rendered by R. Santhanam, not
from the popular Jaimini literature — and on three points BPHS and the popular
literature genuinely disagree. Those divergences are preserved, cited, and
flagged; they are the doctrine, not defects.

------------------------------------------------------------------------------
WHICH GRAHAS ARE ELIGIBLE — ch.32 vv.1-2
------------------------------------------------------------------------------
  "I now detail below Atmakarka etc. obtainable from among the 7 planets viz
   the Sun to Saturn. Some say that Rahu will become a Karka when there is a
   state of similarity in terms of longitude between (two) planets. Yet some
   say that the 8 planets including Rahu will have to be considered
   irrespective of such a state."

Parāśara reports THREE positions and settles none of them, so all three are
exposed as `grahas=`:

  "seven"          the Sun to Saturn only.
  "seven_rahu_on_tie"  the seven, with Rāhu admitted only to make up the
                   shortfall when two of them tie (see TIES below).
  "eight"          the seven plus Rāhu, always.

KETU DOES NOT PARTICIPATE. He is named nowhere in the chapter: v.1 bounds the
set at "the 7 planets viz the Sun to Saturn" and the only extension offered is
"the 8 planets including Rahu". The Vol II ch.46 worked example independently
confirms it — Ketu is present in that chart yet absent from its eight-kāraka
table. This is not an omission on our part; the text has no eighth-plus body.

------------------------------------------------------------------------------
THE RANKING QUANTITY — ch.32 vv.3-8
------------------------------------------------------------------------------
  "ATMA KARAKA DEFINED: Among the planets from the Sun etc. whichever has
   traversed maximum number of degrees in a particular sign is called
   Atmakarka. If the degrees are identical, then the one with more minutes of
   arc and if the minutes are also identical then the one with higher seconds
   of arc will have to be considered. ... In the case of Rahu, deduct his
   longitude in that particular sign from 30."

So the sign is stripped and only the arc travelled WITHIN it is compared —
Santhanam glosses the Ātmakāraka as "highest in longitude devoid of Rasis".
Comparison runs to the arcsecond and stops there; that is the text's own
resolution, and it is why `karaka_value_arcsec` returns an integer.

RĀHU is reckoned as 30° − (his degrees within the sign), because he moves
backwards: Santhanam's note, "The degrees traversed by Rahu should be counted
from the end of the Rasi he is in."  This is verified twice over, since the
standard nativity's Rāhu at 97°37'06" — Karka (Cancer) 7°37'06" — in the ch.29
longitude table (pdf 293) appears in the ch.32 kāraka table (pdf 318) as
22°22'54", and 30° − 7°37'06" = 22°22'54" exactly.

------------------------------------------------------------------------------
THE KĀRAKA SEQUENCE — ch.32 vv.13-17
------------------------------------------------------------------------------
  "OTHER KARAKAS: The planet next to Atmakaraka in terms of longitude is
   called Amatyakaraka. Similarly follow one another in terms of longitude are
   Bhratru Karaka, Matru karaka, Pitru karaka, Putrakaraka, Gnati karaka and
   Streekaraka. These are chara karakas or inconstant significators. Some
   consider Matrukaraka and Putrakaraka as identical."

Eight roles, in that order. Both of the book's worked tables agree with it.

THE SEVEN-ROLE SCHEME IS NOT THE POPULAR ONE. The familiar Jaimini seven drops
PITṚ-kāraka. BPHS instead merges MĀTṚ and PUTRA ("Some consider Matrukaraka and
Putrakaraka as identical"), keeping Pitṛ. Santhanam's note confirms the reading:
"a school of thought which considers only seven significators, treating Matru
Karaka and Putra Karaka as identical. This section thus counts only 7 Karakas."
Selected with `roles=7`.

------------------------------------------------------------------------------
TIES — ch.32 vv.13-17, and Santhanam's note to the worked table
------------------------------------------------------------------------------
  "If two planets have the same longitude, both become the same karaka in which
   case there will be a deficit of one karaka. In that circumstance, consider
   constant significator in the context of benefic/malefic influence for the
   concerned relative."

  Note: "If two planets have the same longitude identical to the second of arc,
   both of them will be qualified for that particular karakatwa or
   significatorship. In that case, there will be shortage of planet for Dara
   Karakatwa. The constant indicator Venus should then be considered in the
   matter of marriage etc."

A tie is therefore NOT broken. Both grahas hold the same kāraka, the sequence
runs one short, and the roles left over at the TAIL fall back to the sthira
kāraka. Degrees→minutes→seconds is the comparison's resolution, not a
tie-breaker: at equal arcseconds the text stops comparing and shares the role.

THE FALLBACK IS ONLY PARTIAL, and this module says so rather than filling the
hole. ch.32 names a constant significator for five of the eight cara roles
(bhrātṛ, mātṛ, pitṛ, putra, strī) and for NONE of ātma, amātya or gnāti. When a
tie leaves one of those three unfilled, `sthira_fallback` returns None for it
and `sthira_fallback_unavailable` names it; see TIE_FALLBACK_INCOMPLETE.

A tie at the TOP rank is likewise not resolved: the scalar `atmakaraka` is None
when the ātma role is shared, `atmakarakas` carries both, and `karakamsa()`
returns both candidates with `ambiguous=True` rather than picking one.

------------------------------------------------------------------------------
KĀRAKĀṀŚA — ch.33 v.1 (Santhanam's note)
------------------------------------------------------------------------------
  "Karakamsa is the Navamsa occupied by the Atma Karaka planet. The Atmakaraka
   is the one who traversed the higher number of degrees etc. (devoid of Rasi),
   among the 8 planets, from Sun to Rahu."

The same gloss is given three more times, and none of them is in ch.33:

  ch.6, note to sloka 52 (pdf 88), on the word Swāṁśa — the OCR of the
  Devanagari gloss is unrecoverable and is left as scanned:
  "(Similarly ,.Swamsa" or Frivr [Devanagari, illegible] means the Navamsa
   occupied by Atma Karaka i.e. Kara-kamsa ascendant, vide ch. 33, infra.)"

  ch.29, note to sloka 29 (pdf 301): "Notes : Karakamsa is the Navamsa occupied
  by Atma-karaka. For more information about Karekamsa, see ch. -a9 [33] infra.
  Atmakaraka btc. are discussed in ch. 32."

  ch.39, note to slokas 3-5 (pdf 387): "(Karakamsa Lagna is the Navamsa
  occupied by the Atma Karaka planet.)"

Note that ch.33's note assumes the EIGHT-graha reading, which is why
`karakamsa()` defaults to it.

------------------------------------------------------------------------------
THE RANK OF PUTRA — ch.39, note to slokas 3-5
------------------------------------------------------------------------------
That Pitṛ sits at rank 5 and Putra at rank 6 (and not the popular Jaimini
arrangement) is stated OUTRIGHT elsewhere in the book, not merely inferred from
the vv.13-17 word order:

  "Here Putra Karaka is Chara Karaka. He is the 6th in status in the Atma
   Karaka scheme, as eiplained in slokas 13-17 of ch. 32 supra."  (pdf 387)

The Mrs Gandhi worked example in the same chapter (note to vv.6-7) confirms it
arithmetically — see FIXTURE 3 in the test.

------------------------------------------------------------------------------
STHIRA KĀRAKAS — ch.32 vv.18-21, AND SEPARATELY vv.22-24
------------------------------------------------------------------------------
BPHS gives two fixed-significator lists in the same chapter and they do not
agree with each other. Both are exposed.

  vv.18-21 (pdf 319-320), as scanned, repairs in square brackets:
   "l8-21 [18-21]. CONSTANT SIGNIFICATOR,S .' I narrate below the constant
    significators as related to the planets. The stronger &mong [among] the Sun
    4nd [and] Venus indicafes [indicates] the father while the stronger among
    the Moon a;nd [and] Mars gdicates the'mother [indicates the mother]. Mars
    denotes sister, brother-in-law, younger brother and mother. Mercury rules
    maternal relative while Jupiter indicates paternal grand-father. Husband and
    sons are respectivcly [respectively] denoted by Venus and Saturn. From Ketu
    note wife, father, mother, parents-in-law and maternal grand father. These
    are conslant [constant] significators."

  Every signification below is legible; only spelling is damaged. Santhanam's
  own tabulation of the same verses (pdf 320) corroborates each entry.

  vv.22-24 (pdf 320) — the scan is BADLY damaged here and is reproduced as
  scanned, every repair in square brackets:
   "The 9th from the Sun denotes father, the 4th fromthe [from the] Moon
    mother, the 3r. [3rd] from Mars brothers, the 6;il- i-;;;Mercury maternar
    [6th from Mercury maternal] uncle, the 5th from Jupiter sons,
    irr"-^iii,from venus [the 7th from Venus] wife and the gth [8th] from
    saturn deatrr [death]."

  NOTE what that means for `STHIRA_KARAKA_HOUSES`. Six of the seven ordinals
  survive at least their leading digit (9th, 4th, 3r., 6;il-, 5th, gth). VENUS'S
  DOES NOT — 'irr"-^iii,' preserves no legible numeral at all. The 7 is a
  RECONSTRUCTION, not a reading. It is retained rather than removed because the
  same translation uses the idiom elsewhere with the numeral intact — pdf 165,
  "is in thc 7th from Venus, m4rriage will be in the l8th year", and pdf 168,
  "7th from Venus while Mercury is in the 7th from the Moon" — so 7th-from-Venus
  = the wife is Santhanam's own settled usage, and it is the only ordinal left
  unused by the other six. See VENUS_HOUSE_RECONSTRUCTED.

THE DIVERGENCE IS REAL AND IT IS THE POINT. vv.18-21 make VENUS the husband,
SATURN the sons and KETU the wife — where the popular list (which Santhanam
himself derives, but from vv.22-24, not from vv.18-21) makes Venus the wife,
JUPITER the sons and Saturn death/longevity. Anyone reconciling this module
against a commercial ephemeris will find vv.18-21 "wrong"; it is not. It is
what Parāśara says, and `STHIRA_KARAKAS` reports it verbatim.
"""

from __future__ import annotations

ARCSEC_PER_SIGN = 30 * 3600

# ch.32 vv.1-2. Ketu is absent from the chapter and so is absent here.
SEVEN_GRAHAS = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn")
EIGHT_GRAHAS = SEVEN_GRAHAS + ("rahu",)

# Grahas whose arc is measured from the END of their sign (v.8). Only Rāhu is
# named. Ketu is never eligible, so he never reaches this rule.
REVERSE_RECKONED = frozenset({"rahu"})

# ch.32 vv.13-17, confirmed by all three worked examples AND stated outright in
# ch.39's note to slokas 3-5 (pdf 387): "Here Putra Karaka is Chara Karaka. He
# is the 6th in status in the Atma Karaka scheme, as eiplained in slokas 13-17
# of ch. 32 supra." Putra at rank 6 forces Pitṛ to rank 5, which is where the
# popular Jaimini seven differs — it drops Pitṛ and pulls Putra up to 5.
KARAKA_ORDER_8 = (
    "atma",     # Ātmakāraka   — the self
    "amatya",   # Amātyakāraka — the minister
    "bhratru",  # Bhrātṛkāraka — brothers
    "matru",    # Mātṛkāraka   — mother
    "pitru",    # Pitṛkāraka   — father
    "putra",    # Putrakāraka  — sons
    "gnati",    # Jñātikāraka  — kinsmen
    "stree",    # Strīkāraka / Dārakāraka — wife
)

# The seven-role reading merges mātṛ and putra. Which of the two slots survives
# is NOT stated; the later duplicate is dropped so the ranks stay contiguous,
# and the merged role carries both significations. See the flag below.
KARAKA_ORDER_7 = (
    "atma", "amatya", "bhratru", "matru_putra", "pitru", "gnati", "stree",
)

KARAKA_SEVEN_MERGE_AMBIGUOUS = (
    "ch.32 v.17 says only that 'some consider Matrukaraka and Putrakaraka as "
    "identical'. It does not say which of the two RANKS the merged karaka "
    "occupies. We keep the earlier slot (4th) and drop the later (6th) so the "
    "seven ranks remain contiguous; the alternative reading, keeping the 6th, "
    "is not excluded by the text."
)

# ch.32 vv.3-8 (pdf 316), immediately after the degrees/minutes/seconds rule,
# reads: "In thatcase' these three are called Anthyakaraka, Madhyakarka and
# Upakheta'". There is no antecedent for "these three" in this translation.
#
# The term is NOT a hapax, and an earlier draft of this module wrongly said so.
# It recurs at ch.33 v.11 (pdf 327), with an explicit back-reference to this
# very passage — and Santhanam's parenthesis there glosses it as a wholly
# different kind of object:
#   "If the Upakheta (or upagraha, vidc sloka 5 ch. 32) is in its cxaltation
#    sign, or own/frienly sign, and is devoid o f malefic aspect, thc nativc
#    will go to heavens after death."
# An UPAGRAHA is a calculated sub-planet (Dhūma, Vyatīpāta, Gulika etc.), not a
# kāraka at all. So the referent is doubtful in KIND as well as in detail: the
# ch.32 clause may be a mistranslation, or a sentence displaced from the
# upagraha material. We still decline to implement it — but the reason is
# conflicting evidence about what it denotes, not absence of evidence.
ANTHYA_MADHYA_UPAKHETA_UNRECOVERABLE = (
    "ch.32 vv.3-8 (pdf 316) name 'Anthyakaraka, Madhyakarka and Upakheta' in a "
    "clause with no antecedent for 'these three'. The term recurs at ch.33 v.11 "
    "(pdf 327) referring back to 'sloka 5 ch. 32', where Santhanam glosses it "
    "'(or upagraha)' — i.e. as a sub-planet, not a karaka. The referent is "
    "therefore uncertain in kind as well as in detail, and no rule is derivable. "
    "None is implemented."
)

# The Vol II ch.46 chart (pdf 68) is one of the book's worked kāraka examples.
# Its rāśi column ("RDM") survives the scan intact — Sun 9, Moon 2, Mars 1,
# Mercury 10, Jupiter 10, Venus 10, Saturn 7, Rāhu 2, Ascendant 10 — and that
# column is 0-INDEXED (0 = Mesha), which the prose settles independently:
# Mercury R=10 is called Aquarius, and Sun R=9 = Capricorn is then the 12th
# from an Aquarius lagna, as stated.
#
# The corroborating prose does NOT adjoin the table; it sits several pages
# later, in the Sthira/Kāraka Daśā worked examples, and is cited here to where
# it actually occurs:
#   pdf 69: "of the 8th Mercury occupies the odd sign Aquarius"
#   pdf 72: "Th. Atmakaraka is the Sun in Capricorn."
#   pdf 73: "The Atmakaraka is the Sun. He is in the l2th to the Ascendant."
# They refer to this same chart — pdf 71 introduces them with "Example : See
# the birth chart given earlier."
#
# The degree/minute/second columns, by contrast, are shredded into loose
# numerals with prose interleaved. Only Rāhu's is legible, and only because the
# sentence spells it out. What is CONTIGUOUS in the scan is:
#     Rahu's degr"ees etc.
#     16'-4',-26".
#   ... "after deducting from" ... "30 would be" ...
# The numerals after "30 would be" are jumbled ('l3 / 20 / 4l / 4') and do NOT
# read 13°55'34" contiguously. That value is our ARITHMETIC from the legible
# 16°04'26" (30° − 16°04'26" = 13°55'34"), not a quotation, and the test asserts
# it as a derivation.
VOL2_CH46_DEGREES_UNRECOVERABLE = (
    "BPHS Vol II ch.46 (pdf 68): the worked chart's degree/minute/second "
    "columns are destroyed in this scan. The rāśi column, the resulting kāraka "
    "assignment (pdf 69) and Rāhu's 16°04'26\" are recoverable; the other seven "
    "grahas' individual arcs are not, and are not reconstructed."
)

# ch.32 vv.18-21, verbatim. NOT the popular list — see the module docstring.
STHIRA_KARAKAS: dict[str, tuple[str, ...]] = {
    "sun": ("father (stronger of Sun and Venus)",),
    "venus": ("father (stronger of Sun and Venus)", "husband"),
    "moon": ("mother (stronger of Moon and Mars)",),
    "mars": ("mother (stronger of Moon and Mars)", "sister", "brother-in-law",
             "younger brother", "mother"),
    "mercury": ("maternal relatives",),
    "jupiter": ("paternal grandfather",),
    "saturn": ("sons",),
    "ketu": ("wife", "father", "mother", "parents-in-law",
             "maternal grandfather"),
}

# vv.18-21 make two significations depend on a strength comparison the śloka
# does not itself define ("the stronger among..."). Callers supply the winner.
STHIRA_KARAKA_CONTESTS: dict[str, tuple[str, str]] = {
    "father": ("sun", "venus"),
    "mother": ("moon", "mars"),
}

# Venus's ordinal is DESTROYED in the pdf-320 scan ('irr"-^iii,from venus wife'
# preserves no digit). The 7 below is reconstructed from Santhanam's own usage
# of the idiom elsewhere (pdf 165, pdf 168) and from its being the only ordinal
# the other six leave free. Every other entry's leading digit is legible. This
# is surfaced per-call by `sthira_karaka_houses` so the API layer can mark it.
VENUS_HOUSE_RECONSTRUCTED = (
    "ch.32 vv.22-24 (pdf 320): the ordinal for Venus is illegible in this scan "
    "— it reads 'irr\"-^iii,from venus wife', with no surviving numeral. The 7th "
    "is RECONSTRUCTED, not read: Santhanam uses '7th from Venus' for marriage "
    "elsewhere with the numeral intact (pdf 165, pdf 168), and 7 is the only "
    "ordinal not taken by the other six significators. Treat as high-confidence "
    "but not directly attested. The other six ordinals ARE legible in the scan."
)

# ch.32 vv.22-24 — the OTHER list: a bhāva counted from a graha, not the graha.
STHIRA_KARAKA_HOUSES: dict[str, tuple[int, str]] = {
    "sun": (9, "father"),
    "moon": (4, "mother"),
    "mars": (3, "brothers"),
    "mercury": (6, "maternal uncle"),
    "jupiter": (5, "sons"),
    "venus": (7, "wife"),
    "saturn": (8, "death"),
}

# Which sthira kāraka answers for a cara role that went unfilled by a tie
# (vv.13-17: "consider constant significator ... for the concerned relative").
#
# THE ONLY ADMISSIBLE SOURCE is vv.22-24 as Santhanam tabulates them, because
# that is the list he himself applies when he sends Dārakāraka's shortfall to
# Venus. Verbatim, pdf 320 — the scan is damaged and is quoted AS SCANNED, with
# each repair in square brackets rather than silently normalised:
# "From these three verses, the constant Karakasbmerge [Karakas emerge] as under
# as normalry [normally] discussea [discussed] in standard riterature
# [literature] onastrology [on astrology] :" followed by the list, which IS
# undamaged and is quoted exactly:
# The S'rn - father / The Moon - mother / Mars - brothers (and sisters) /
# Mercury - maternal relatives / Jupiter - Sons (and daughters) / Venus - wife
# (or husband) / Saturn - death (or longeviiy)".
#
# That list covers exactly FIVE of the eight cara roles. It names a significator
# for father, mother, brothers, sons and wife — and for nothing else.
#
# An earlier version of this table also carried atma->sun, amatya->mercury and
# gnati->mars. Those three were INVENTED. ch.32 supplies no sthira kāraka for
# the self, for the minister, or for kinsmen — not in vv.18-21, not in vv.22-24,
# not in Santhanam's notes to either. (Mercury's entry is "maternal relatives",
# which is not amātya; Mars's is "brothers", which is already bhrātṛ's.) They are
# removed rather than shipped, and the gap is reported explicitly instead.
_TIE_FALLBACK = {
    "bhratru": "mars",    # "Mars - brothers (and sisters)"
    "matru": "moon",      # "The Moon - mother"
    "pitru": "sun",       # "The S'rn - father"
    "putra": "jupiter",   # "Jupiter - Sons (and daughters)"
    "stree": "venus",     # "Venus - wife (or husband)", and the note to vv.13-17
}

# The merged seven-role slot carries BOTH significations, and the text nowhere
# says which sthira kāraka answers for the merger. Both readings are exposed;
# neither is chosen.
TIE_FALLBACK_AMBIGUOUS: dict[str, tuple[str, ...]] = {
    "matru_putra": ("moon", "jupiter"),
}

TIE_FALLBACK_INCOMPLETE = (
    "ch.32 gives a sthira (constant) significator for only five of the eight "
    "cara roles: bhratru/matru/pitru/putra/stree, via vv.22-24 as tabulated by "
    "Santhanam at pdf 320. There is NO sthira karaka anywhere in the chapter "
    "for atma (the self), amatya (the minister) or gnati (kinsmen), so when a "
    "tie leaves one of those three unfilled the text supplies no fallback and "
    "this module returns None rather than a graha. The merged seven-role slot "
    "matru_putra has two candidates (Moon for matr, Jupiter for putra) and the "
    "text does not decide between them; see TIE_FALLBACK_AMBIGUOUS."
)


def dms(degrees: int, minutes: int = 0, seconds: float = 0.0) -> float:
    """Assemble a degree value from arc degrees/minutes/seconds."""
    return degrees + minutes / 60.0 + seconds / 3600.0


def karaka_value_arcsec(graha: str, longitude: float) -> int:
    """The ranked quantity of vv.3-8, in integer arcseconds of a sign.

    The sign is discarded — only the arc traversed inside it counts. Rāhu is
    measured from the far end of his sign instead (v.8), so a Rāhu early in a
    sign scores high. Resolution is the arcsecond because that is where the
    śloka's own comparison stops.
    """
    within = round((longitude % 30.0) * 3600.0)
    if graha in REVERSE_RECKONED:
        return ARCSEC_PER_SIGN - within
    return within


def _eligible(longitudes: dict[str, float], grahas: str) -> list[str]:
    if grahas == "eight":
        pool = EIGHT_GRAHAS
    elif grahas in ("seven", "seven_rahu_on_tie"):
        pool = SEVEN_GRAHAS
    else:
        raise ValueError(
            "grahas must be 'seven', 'seven_rahu_on_tie' or 'eight'; "
            f"got {grahas!r}"
        )
    missing = [g for g in pool if g not in longitudes]
    if missing:
        raise ValueError(f"longitudes missing for: {', '.join(missing)}")
    return list(pool)


def chara_karakas(longitudes: dict[str, float], *,
                  grahas: str = "eight", roles: int = 8) -> dict:
    """Cara kārakas — ch.32 vv.3-8 and 13-17.

    `longitudes` maps graha key -> sidereal longitude in degrees; only the
    eligible keys are read, so a full chart may be passed in.

    `grahas` picks between the three schools of vv.1-2 ('seven',
    'seven_rahu_on_tie', 'eight'); `roles` picks between the eight-role
    sequence of vv.13-17 and the seven-role reading that merges mātṛ with
    putra. Neither is defaulted silently on doctrinal grounds — 'eight'/8 is
    chosen because both of the book's own worked tables use it.

    Returns the assignment plus the ranking that produced it, the shared roles
    a tie created, and the roles left unfilled with their sthira fallback.
    """
    if roles not in (7, 8):
        raise ValueError(f"roles must be 7 or 8; got {roles!r}")

    pool = _eligible(longitudes, grahas)
    values = {g: karaka_value_arcsec(g, longitudes[g]) for g in pool}

    # v.8's descending order. Ties are NOT broken (see module docstring), so the
    # secondary key only fixes a stable print order inside a tied group.
    ranked = sorted(pool, key=lambda g: (-values[g], pool.index(g)))

    # Group grahas that agree to the arcsecond — each group takes ONE role.
    groups: list[list[str]] = []
    for g in ranked:
        if groups and values[groups[-1][0]] == values[g]:
            groups[-1].append(g)
        else:
            groups.append([g])

    # vv.1-2, middle position: Rāhu is admitted only to repair a tie's shortfall.
    # The requested school is PRESERVED in the result — a caller must be able to
    # tell whether Rāhu came in under this rule or was asked for outright.
    if grahas == "seven_rahu_on_tie" and len(groups) < len(pool):
        if "rahu" not in longitudes:
            raise ValueError("longitudes missing for: rahu")
        widened = chara_karakas(longitudes, grahas="eight", roles=roles)
        widened["scheme"] = {"grahas": grahas, "roles": roles,
                             "rahu_admitted_on_tie": True}
        return widened

    order = KARAKA_ORDER_8 if roles == 8 else KARAKA_ORDER_7

    assignment: dict[str, list[str]] = {}
    karaka_of: dict[str, str] = {}
    for role, group in zip(order, groups):
        assignment[role] = list(group)
        for g in group:
            karaka_of[g] = role

    unfilled = list(order[len(groups):])

    # A tie at the TOP rank is not broken either. `atmakaraka` is the scalar
    # convenience key, so it must be None when the role is shared rather than
    # silently returning whichever graha sorts first; `atmakarakas` always
    # carries the full truth.
    atmakarakas = assignment.get(order[0], [])

    return {
        "scheme": {"grahas": grahas, "roles": roles,
                   "rahu_admitted_on_tie": False},
        "order": list(order),
        # role -> [graha, ...]; more than one only when they tie exactly.
        "assignment": assignment,
        # graha -> role, for the grahas that got one.
        "karaka_of": karaka_of,
        # None when the atma role is SHARED — see the note above.
        "atmakaraka": atmakarakas[0] if len(atmakarakas) == 1 else None,
        "atmakarakas": atmakarakas,
        "ranking": [
            {"graha": g, "arcsec": values[g],
             "degrees": values[g] // 3600,
             "minutes": (values[g] % 3600) // 60,
             "seconds": values[g] % 60,
             "reverse_reckoned": g in REVERSE_RECKONED}
            for g in ranked
        ],
        "shared": {r: gs for r, gs in assignment.items() if len(gs) > 1},
        "unfilled": unfilled,
        # role -> sthira graha, or None where ch.32 names no constant
        # significator for that role at all. NEVER guess a graha here.
        "sthira_fallback": {r: _TIE_FALLBACK.get(r) for r in unfilled},
        "sthira_fallback_unavailable": [
            r for r in unfilled
            if r not in _TIE_FALLBACK and r not in TIE_FALLBACK_AMBIGUOUS
        ],
        "sthira_fallback_ambiguous": {
            r: TIE_FALLBACK_AMBIGUOUS[r]
            for r in unfilled if r in TIE_FALLBACK_AMBIGUOUS
        },
        "citation": "BPHS Vol I ch.32 vv.1-2, 3-8, 13-17",
    }


def karakamsa(longitudes: dict[str, float], *,
              grahas: str = "eight", navamsa_of=None) -> dict:
    """Kārakāṁśa — ch.33 v.1: the navāṁśa sign held by the Ātmakāraka.

    `navamsa_of` is a callable (sign, degree_in_sign) -> sign 0-11; pass
    `vargas.d9_navamsa`. It is injected rather than imported so this module
    stays pure computation with no dependency of its own.

    NOTE the reckoning asymmetry, which is doctrine and not an oversight: the
    Ātmakāraka is SELECTED by Rāhu's inverted arc (v.8), but his kārakāṁśa is
    the navāṁśa of where he ACTUALLY stands. v.8's subtraction is a rule for
    ranking kārakas, and ch.33 asks only "the Navamsa occupied by" him.

    IF THE ĀTMA ROLE IS SHARED there is no single kārakāṁśa. ch.32 says both
    grahas hold the kārakatva; it gives no rule for preferring one. This
    function therefore reports BOTH in `candidates`, sets the scalar `karakamsa`
    and `atmakaraka` to None, and flags `ambiguous`. It does not pick.
    """
    if navamsa_of is None:
        raise ValueError("pass navamsa_of=vargas.d9_navamsa")

    ck = chara_karakas(longitudes, grahas=grahas)
    aks = ck["atmakarakas"]

    candidates = []
    for g in aks:
        lon = longitudes[g] % 360.0
        sign, deg = int(lon // 30), lon % 30.0
        candidates.append({
            "graha": g,
            "atmakaraka_longitude": lon,
            "rasi": sign,
            "karakamsa": navamsa_of(sign, deg),
        })

    single = candidates[0] if len(candidates) == 1 else None

    return {
        "atmakaraka": single["graha"] if single else None,
        "atmakaraka_longitude": single["atmakaraka_longitude"] if single else None,
        "rasi": single["rasi"] if single else None,
        "karakamsa": single["karakamsa"] if single else None,
        # Always populated. When len > 1 the ātma role is shared and the scalar
        # keys above are None — the caller must handle both kārakāṁśas.
        "candidates": candidates,
        "ambiguous": len(candidates) > 1,
        "citation": "BPHS Vol I ch.33 v.1 (note); definition at ch.32 vv.3-8",
    }


def sthira_karaka_houses(bhava_of: dict[str, int]) -> dict[str, dict]:
    """ch.32 vv.22-24: the significations sit in a house counted FROM a graha.

    `bhava_of` maps graha key -> the whole-sign bhāva (1-12) it occupies.
    Returns, per graha, the bhāva the śloka points at and what it signifies.
    """
    out = {}
    for graha, (offset, meaning) in STHIRA_KARAKA_HOUSES.items():
        if graha not in bhava_of:
            continue
        start = bhava_of[graha]
        out[graha] = {
            "from_bhava": start,
            "count": offset,
            "bhava": (start + offset - 2) % 12 + 1,
            "signifies": meaning,
            # True only for Venus, whose ordinal is illegible in the scan and
            # is reconstructed. See VENUS_HOUSE_RECONSTRUCTED.
            "count_reconstructed": graha == "venus",
        }
    return out
