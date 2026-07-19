"""Dṛṣṭi — BPHS Vol I, Chapter 8 (rāśi dṛṣṭi) and Chapter 26 (graha dṛṣṭi).

TWO DOCTRINES. They are not variants of one rule and are never mixed here.

===========================================================================
QUOTATION POLICY — read this before trusting a quote in this file
===========================================================================
The source is Santhanam's translation as recovered by OCR, and the OCR of
these two chapters is bad: word-joins are lost, digits turn into letters, and
apostrophes stand in for full stops. THIS MODULE THEREFORE NEVER PUTS A
CLEANED-UP SENTENCE INSIDE QUOTE MARKS.

Wherever a śloka is cited below it is given twice:

    VERBATIM — reproduced character for character from the OCR text, however
               damaged. Line references are to the extracted plain text and
               are given as  printed-page / ===PDFPAGE marker  so the two
               page conventions can never drift apart.
    READING  — the plain-English reading this module implements. This is an
               EDITORIAL RECONSTRUCTION, not a quotation, and is never shown
               in quote marks.

Every numeric repair made in a READING is listed in OCR_NUMERIC_REPAIRS.

===========================================================================
(a) RĀŚI DṚṢṬI — signs aspect signs.  Ch.8 vv.1-3, restated for occupants
    in vv.4-5.  COUNTED FROM THE SIGN, NEVER THE DEGREE.
    printed p.105 = ===PDFPAGE 104=== ;  vv.4-5 printed p.107 = PDFPAGE 106
===========================================================================

  vv.1-3 VERBATIM:
      l-3. SIGN ASPECT,S .' O Maitreya, now detailed are ths
      aspects emanating from the signs Aries etc' Every movable
      siin aspects the 3 fixed signs leavirrg the' fixed sign adjacent to
      it] gvery fixod sigo lends aspect to the 3 movable signs barring
      the adjactnt movable sign. And a cotnmon sign aspects the
      other three common slgns. The planet in a sign lends the same
      sspect as tho sign (in which the planet is) does'

  vv.1-3 READING: O Maitreya, now detailed are the aspects emanating from
      the signs Aries etc. Every movable sign aspects the 3 fixed signs
      leaving the fixed sign adjacent to it. Every fixed sign lends aspect
      to the 3 movable signs barring the adjacent movable sign. And a common
      sign aspects the other three common signs. The planet in a sign lends
      the same aspect as the sign (in which the planet is) does.

  vv.4-5 VERBATIM:
      4-5. PLANETARY ASPECTS : A planet in a movable
      sign aspects the other 3 fixed' signs leaving the fixed sign
      nJxt toit. A planet in a fixed sign does not aspect the next
      movabte sign but the remaining 3 movable signs' The one in
      a common sign throws aspect over'the remaining 3 common
      signs. sinultaneously a planet in the aspected sign is also
      subjected to the aspect concerned.

  vv.4-5 READING: as vv.1-3 but for the occupant, and — the clause this
      module needs — simultaneously a planet in the aspected sign is also
      subjected to the aspect concerned.

  The degree is IRRELEVANT here, and Santhanam's note says so in as many
  words. VERBATIM: "Hence, in these aspccts, longitudes of the aspector and
  the aspected are ignorable." READING: ...in these aspects... So rāśi dṛṣṭi
  is exactly drawable on a whole-sign chart: it is a property of the boxes.

  BPHS GIVES RĀŚI DṚṢṬI NO STRENGTH GRADING — confirmed. Chapter 8 has no
  fraction, no virūpa, no "full/half" anywhere; a sign either aspects another
  or it does not. `rasi_drishti()` therefore returns bool, not a fraction.
  Grading rāśi dṛṣṭi would be importing a doctrine this text does not state.

  "Common" is Santhanam's rendering of dvisvabhāva (dual/mutable).

  THE CH.8 WORKED EXAMPLE (a)-(f), printed pp.107-108, is internally
  inconsistent; see CH8_EXAMPLE_INCONSISTENT and test_drishti.py, which
  reconstructs the strongest placement consistent with (a),(c),(d),(e),(f)
  and shows it must break (b).

===========================================================================
(b) GRAHA DṚṢṬI — grahas aspect places.  Ch.26.  Given at TWO RESOLUTIONS.
    printed p.255 = ===PDFPAGE 254===
===========================================================================

  vv.2-5 VERBATIM (the OCR has lost the word-breaks; reproduced as found):
      2'5. PLANETARY ASPECTS .' O Brahmin, I have ear-
      lier stated aspects based on signs. The other kind is between
      planets which I detail below. 3rd and l0th, 5rh and 9th, 4thand 8th
      and lastly zth-on thcse praces the aspects inci."s"gradually in slabs
      of quarters i.e l14, 112,3l4thand fult. Theeffects (due to such
      aspects) wiil also be proportionate. Ailplanets aspect the Tth fully.
      Saturn, Jupiter and Mars havespecial aspects respectively on 3rd and
      lOth, 5th and 9th, and4th and 8th. The ancient preceptors have
      exprained these which
      are ordinary (arising by mere sign .positions).- By subtle
      mathematical calculations, these aspects will bave to be clearly
      understood as under.

  vv.2-5 READING: O Brahmin, I have earlier stated aspects based on signs.
      The other kind is between planets which I detail below. 3rd and 10th,
      5th and 9th, 4th and 8th and lastly 7th — on these places the aspects
      increase gradually in slabs of quarters i.e. 1/4, 1/2, 3/4 and full.
      The effects (due to such aspects) will also be proportionate. All
      planets aspect the 7th fully. Saturn, Jupiter and Mars have special
      aspects respectively on 3rd and 10th, 5th and 9th, and 4th and 8th.
      The ancient preceptors have explained these which are ordinary
      (arising by mere sign positions). By subtle mathematical calculations,
      these aspects will have to be clearly understood as under.

  So the mapping is, from the śloka's own pairing of its two lists — the
  houses in the order 3/10, 5/9, 4/8, 7 against the fractions in the order
  1/4, 1/2, 3/4, full:

        3rd and 10th  ->  1/4
        5th and 9th   ->  1/2
        4th and 8th   ->  3/4
        7th           ->  full
        everything else (1,2,6,11,12) -> nothing

  NOTE THAT THIS IS NOT MONOTONIC IN HOUSE NUMBER. The 4th/8th outrank the
  5th/9th. It is easy to "tidy" this into 3,4,5 -> 1/4,1/2,3/4 and get the
  4th and 5th backwards; the degree-based engine below proves the śloka's
  order is the right one.

  vv.2-5 are COUNTED FROM THE SIGN — the śloka says so itself, calling them
  the aspects arising by mere sign positions. This is the layer that can be
  drawn on a whole-sign chart, and it is what `graha_drishti()` returns.

  vv.6-12 are COUNTED FROM THE DEGREE (by subtle mathematical calculations)
  and yield a value in virūpas, 0-60. That is `drishti_virupa()`. It is not
  drawable as a whole-sign arrow; it is what Drig Bala (ch.27 v.19, printed
  p.278) consumes.

  THE TWO LAYERS ARE THE SAME DOCTRINE AT TWO RESOLUTIONS, and this module
  proves it rather than asserting it: evaluate the degree engine at the cusp
  of each house (0°, 30°, 60° …) and it returns exactly 0, 0, 15, 45, 30, 0,
  60, 45, 30, 15, 0, 0 virūpas — i.e. 0, 0, 1/4, 3/4, 1/2, 0, full, 3/4, 1/2,
  1/4, 0, 0 of a rūpa. Every one of the twelve houses agrees with vv.2-5,
  including the non-monotonic 4th-over-5th. See test_drishti.py.

---------------------------------------------------------------------------
DIRECTION OF THE SUBTRACTION — a correction to the printed text
---------------------------------------------------------------------------
This module deliberately departs from the mūla as printed. The departure is
named in the importable constant DRISHTI_DIRECTION_CORRECTED so that a later
reader cannot "restore" the printed direction without meeting the argument.

v.6 VERBATIM: "Deduct the longi-\ntude of tbe aspected planet (or house)
from that of the\naspecting planet." Santhanam's note repeats it: "The
longitude of 'the aspected' .is to be\ndeducted from that of the aspector."
THAT IS BACKWARDS, and three independent things in the same chapter show it:

  1. vv.11 and 12 state the opposite and are unambiguous. VERBATIM (v.11):
     "Deduct the longitude of Mars from that of theplanet aspected (by
     Mars)."
  2. The note's own arithmetic clause only works the other way. VERBATIM:
     "If the longitude of the\naspected is lesser than that of the aspector,
     increase the longi-\ntude of 'the aspected' by 360 to facilitate
     deduction". One does not need to add 360 to a quantity one is
     subtracting FROM a smaller number — that clause is written for
     aspected − aspector.
  3. It is falsifiable, and false. Saturn's special aspect is the 3rd, i.e.
     the place 60° AHEAD of him. Under (aspected − aspector) the angle is 60°
     and Saturn's rule peaks there at 60 virūpas. Under (aspector − aspected)
     it is 300°, where Saturn's rule returns 0. Likewise every general-case
     house: the 3rd would score 0 instead of a quarter.

We therefore use  angle = (aspected − aspector) mod 360  throughout.

---------------------------------------------------------------------------
THE ŚLOKAS vv.6-12 VS SANTHANAM'S "SIMPLE FORMULA" NOTE — they disagree
---------------------------------------------------------------------------
After the ślokas Santhanam adds a shortcut of his own (printed p.257): for
Mars add 15 virūpas to the plain speculum value over 90°-120° and 210°-240°,
for Jupiter add 30 over 120°-150° and 240°-270°, for Saturn add 45 over
60°-90° and 270°-300°.

  ⚠ The 210°-240° band above is an OCR REPAIR of a printed digit; the page
    reads 210-249. See OCR_NUMERIC_REPAIRS. The module does not depend on it.

This is a NOTE, not mūla, and it is only correct at the exact peak. At 90°
his Saturn shortcut yields 45 + 45 = 90 virūpas — more than the one rūpa that
is by definition the maximum. The ślokas' own piecewise rules (vv.9-12,
encoded below) are used instead, and they are self-consistent: each one hands
back to the general rule at exactly the general rule's value at the segment
ends, except where flagged in SPECIAL_DRISHTI_GAPS.

---------------------------------------------------------------------------
WHAT THIS MODULE DOES NOT DO
---------------------------------------------------------------------------
Ch.27 v.19's Drig Bala itself — reduce a quarter of the Drishti Pinda for a
malefic aspect, add a quarter for a benefic, super-add the whole of Mercury's
and Jupiter's — is deliberately NOT implemented here. It is Ṣaḍbala doctrine
and needs a benefic/malefic classifier this module has no business owning.
`drishti_virupa()` is the input it will need.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Declared uncertainties and departures. House style follows dignity.py's
# MOOLATRIKONA_UNVERIFIED: a module-level constant that names the doubt, and a
# flag on every dict this module hands back, so the API layer can act on it.
# ---------------------------------------------------------------------------

# Every place a printed digit in the source was overruled. Nothing in the
# COMPUTED path depends on either of these; both are prose/fixture repairs.
OCR_NUMERIC_REPAIRS = (
    {
        "where": "Santhanam's 'simple formula' note (A), printed p.257 "
                 "= ===PDFPAGE 256===",
        "printed": "210-249 degrees",
        "read_as": "210-240 degrees",
        "why": "The band is Mars's 8th and every other band in the same note "
               "is exactly one sign wide (90-120, 120-150, 240-270, 60-90, "
               "270-300); 210-249 is 39° wide and would overlap Jupiter's "
               "240-270. 240 is also a segment boundary in v.11 itself.",
        "affects_computation": False,
    },
    {
        "where": "Speculum of Aspectual Values, entry 59:30, printed p.258 "
                 "= ===PDFPAGE 257===",
        "printed": "14.7J",
        "read_as": "14.75",
        "why": "OCR J for 5. The column runs …14.50, 14.7?, 15.00 in steps "
               "of 0.25.",
        "affects_computation": False,
    },
)

# The module contradicts the mūla as printed. Named so it cannot be silently
# "corrected back". See the header section on the direction of the subtraction.
DRISHTI_DIRECTION_CORRECTED = (
    "Ch.26 v.6 as printed, and Santhanam's note on it, say to deduct the "
    "longitude of the ASPECTED from that of the ASPECTOR. This module does "
    "the reverse: angle = (aspected − aspector) mod 360. The printed "
    "direction is refuted inside the same chapter — vv.11 and 12 state the "
    "reverse explicitly, the note's own 'add 360 to the aspected' clause "
    "only parses the reverse way, and the printed direction sends Saturn's "
    "special 3rd-house aspect to 0 virūpas instead of 60. Do not restore the "
    "printed direction without meeting all three."
)

# v.9-10's fourth clause is genuinely ambiguous in English. Flagged rather
# than resolved in a comment.
SATURN_DEGREES_TO_ELAPSE_AMBIGUOUS = (
    "Ch.26 v.10 VERBATIM: \"If the sum is above nine sinls, thedegrees to "
    "elapse be doubred to get aspectual vatue.\" 'Degrees to elapse' admits "
    "two readings over 270°-300°: degrees REMAINING, (300 − a) × 2, or "
    "degrees ELAPSED past 270°, (a − 270) × 2. They are exact mirror images. "
    "This module implements REMAINING. Warrant: the preceding segment "
    "(240°-270°) ends at 60 virūpas and the general rule stands at 0 at "
    "300°, so only REMAINING is continuous at both ends — ELAPSED would open "
    "a 60-virūpa cliff at 270° and another at 300°, and would put Saturn's "
    "maximum on his 11th house rather than the 10th the śloka names. The "
    "mūla does not decide the wording; continuity does."
)

# Ch.26 says all planets aspect the 7th fully without enumerating who the
# planets are. Ch.27's NOTE on Ṣaḍbala — the only consumer of these values —
# VERBATIM: "These strengths are computed for the seven planets fromthe Sun
# to Saturn. The nodes aro not considered." Against that, Santhanam remarks
# in a NOTE to ch.9 v.11, VERBATIM: "(This goes to prove that Rahu has
# aspects.)" Both are notes; the mūla settles neither way.
NODE_GRAHA_DRISHTI_UNVERIFIED = (
    "BPHS ch.26 never names Rāhu/Ketu among the aspecting grahas, and ch.27's "
    "note excludes the nodes from Ṣaḍbala outright. Their graha dṛṣṭi rests "
    "on Santhanam's note to ch.9 v.11, not on the mūla. Nodal graha dṛṣṭi is "
    "computed only when include_nodes=True, and it is flagged, not asserted. "
    "(Nodal RĀŚI dṛṣṭi is not in doubt: there the SIGN aspects, so a node "
    "participates like any other occupant — ch.8 v.5.)"
)

CH8_EXAMPLE_INCONSISTENT = (
    "The worked example (a)-(f) in Santhanam's notes to ch.8 vv.4-5 (printed "
    "pp.107-108) cannot be satisfied by any placement whatever. Rāśi dṛṣṭi is "
    "symmetric, so (c) 'Jupiter aspects the Moon, Ketu, Sun and Venus' forces "
    "the Sun and Venus to aspect Jupiter back, contradicting (b) 'Venus, the "
    "Sun and Mercury aspect none'. Clauses (a), (c), (d), (e), (f) ARE "
    "mutually satisfiable and test_drishti.py reconstructs a placement "
    "meeting all five exactly; that placement then breaks (b) for the Sun and "
    "Venus and for nobody else. The horoscope itself is a diagram, absent "
    "from the extracted text, so it cannot arbitrate."
)


# ---------------------------------------------------------------------------
# (a) RĀŚI DṚṢṬI — Ch.8 vv.1-5
# ---------------------------------------------------------------------------

MOVABLE, FIXED, DUAL = 0, 1, 2          # cara, sthira, dvisvabhāva
QUALITY_NAMES = ("movable", "fixed", "dual")


def quality(sign: int) -> int:
    """Movable/fixed/dual of a sign. Meṣa is movable and it alternates by 3s."""
    return sign % 3


def _rasi_drishti_targets(sign: int) -> tuple[int, ...]:
    """Derive one row of ch.8's table from the śloka, rather than typing it.

    The verse is three clauses and this is three clauses: a movable sign takes
    the fixed signs minus the adjacent one, a fixed sign takes the movable
    signs minus the adjacent one, a dual sign takes the other duals. "Adjacent"
    is the neighbour in the zodiac — the fixed sign immediately AFTER a movable
    one (Meṣa's Vṛṣabha), the movable sign immediately BEFORE a fixed one
    (Vṛṣabha's Meṣa). Both readings name the same pair of neighbouring signs,
    which is why the doctrine comes out symmetric.
    """
    q = quality(sign)
    if q == MOVABLE:
        return tuple(s for s in range(12)
                     if quality(s) == FIXED and s != (sign + 1) % 12)
    if q == FIXED:
        return tuple(s for s in range(12)
                     if quality(s) == MOVABLE and s != (sign - 1) % 12)
    return tuple(s for s in range(12) if quality(s) == DUAL and s != sign)


# The ch.8 table, derived. sign -> signs it aspects.
RASI_DRISHTI: dict[int, tuple[int, ...]] = {
    s: _rasi_drishti_targets(s) for s in range(12)
}

# Ch.8 attaches no fraction, virūpa or grade to a rāśi aspect. Kept as an
# explicit statement so nobody later "fills it in" from another tradition.
RASI_DRISHTI_UNGRADED = (
    "BPHS Vol I ch.8 vv.1-5 grade rāśi dṛṣṭi in no way whatever: a sign either "
    "aspects another or it does not. Any 1/4-1/2-3/4 grading of a RĀŚI aspect "
    "is an import from ch.26's GRAHA dṛṣṭi and is not this doctrine."
)


def rasi_drishti(from_sign: int, to_sign: int) -> bool:
    """Does `from_sign` aspect `to_sign` (ch.8 vv.1-3)? Degrees are ignorable."""
    return to_sign % 12 in RASI_DRISHTI[from_sign % 12]


# ---------------------------------------------------------------------------
# (b) GRAHA DṚṢṬI, sign resolution — Ch.26 vv.2-5
# ---------------------------------------------------------------------------

# The nine keys this module accepts, matching vedic.GRAHAS. A mis-cased or
# misspelt key used to fall through to the general rule and return a plausible
# WEAKER aspect — a confident wrong answer. It now raises.
CANONICAL_GRAHAS = ("sun", "moon", "mars", "mercury", "jupiter",
                    "venus", "saturn", "rahu", "ketu")

NODES = ("rahu", "ketu")


def _check_graha(graha) -> str:
    if graha not in CANONICAL_GRAHAS:
        raise ValueError(
            f"unknown graha key {graha!r}; expected one of "
            f"{', '.join(CANONICAL_GRAHAS)} (lower case). Silently treating an "
            "unrecognised key as a generic graha would return a plausible but "
            "wrong aspect strength."
        )
    return graha


# The śloka's two lists, paired in the śloka's own order. Houses it does not
# name get nothing, so a plain dict lookup with a 0.0 default IS the rule.
GRAHA_DRISHTI_FRACTION: dict[int, float] = {
    3: 0.25, 10: 0.25,
    5: 0.50, 9: 0.50,
    4: 0.75, 8: 0.75,
    7: 1.00,
}

# "Saturn, Jupiter and Mars have special aspects respectively on 3rd and 10th,
#  5th and 9th, and 4th and 8th." A special aspect is FULL — that is what
#  makes it special, since all three of those pairs are already partial
#  aspects for everyone under the general grading.
SPECIAL_DRISHTI_HOUSES: dict[str, tuple[int, int]] = {
    "saturn": (3, 10),
    "jupiter": (5, 9),
    "mars": (4, 8),
}


def house_distance(from_sign: int, to_sign: int) -> int:
    """Whole-sign house count, inclusive of both ends — the sign itself is 1."""
    return ((to_sign - from_sign) % 12) + 1


def graha_drishti(from_sign: int, to_sign: int, graha: str) -> float:
    """Strength of `graha`'s aspect from `from_sign` onto `to_sign`, 0.0-1.0.

    Ch.26 vv.2-5, the "ordinary" sign-counted layer. 0.0 means no aspect.
    Sa/Ju/Ma get 1.0 on their special pairs, which overrides the 1/4, 1/2 and
    3/4 those pairs carry generally.

    Raises ValueError on any key outside CANONICAL_GRAHAS.
    """
    _check_graha(graha)
    h = house_distance(from_sign, to_sign)
    if h in SPECIAL_DRISHTI_HOUSES.get(graha, ()):
        return 1.0
    return GRAHA_DRISHTI_FRACTION.get(h, 0.0)


# ---------------------------------------------------------------------------
# (b) GRAHA DṚṢṬI, degree resolution — Ch.26 vv.6-12, in virūpas
# ---------------------------------------------------------------------------

RUPA = 60.0          # "60 such\nunits make onq Rupa." — Santhanam's note, ch.26


def drishti_angle(aspector_longitude: float, aspected_longitude: float) -> float:
    """The dṛṣṭi-koṇa: (aspected − aspector) mod 360.

    See DRISHTI_DIRECTION_CORRECTED for why this is the direction, and why
    v.6 as printed has it backwards."""
    return (aspected_longitude - aspector_longitude) % 360.0


def general_drishti_virupa(angle: float) -> float:
    """vv.6-8 — the six-branch general rule, in virūpas (0-60).

    Santhanam restates the six branches as numbered Rules 1-6 (printed p.257);
    they are, in his order, in READING form:

      Rule 1   30°-60°    reduce 30 from the angle and divide by 2
      Rule 2   60°-90°    reduce 60 from the angle and add 15
      Rule 3   90°-120°   reduce the angle from 120, halve, increase by 30
      Rule 4   120°-150°  reduce the angle from 150
      Rule 5   150°-180°  reduce 150 from the angle and double
      Rule 6   180°-300°  deduct the angle from 300 and halve

    and VERBATIM: "Needless to mention there is no aspectual value if the angle
    is between 300 and 30 degrees." The branches are continuous at every seam.
    """
    a = angle % 360.0
    if 30.0 <= a < 60.0:
        return (a - 30.0) / 2.0
    if 60.0 <= a < 90.0:
        return (a - 60.0) + 15.0
    if 90.0 <= a < 120.0:
        return (120.0 - a) / 2.0 + 30.0
    if 120.0 <= a < 150.0:
        return 150.0 - a
    if 150.0 <= a < 180.0:
        return (a - 150.0) * 2.0
    if 180.0 <= a < 300.0:
        return (300.0 - a) / 2.0
    return 0.0


def _saturn_virupa(a: float) -> float | None:
    """vv.9-10. Four segments, a tent peaked at the 3rd (60°) and the 10th
    (270°). Each hands back to the general rule at its own value.

    VERBATIM (word-joins as found in the OCR):
      "if Saturn is the aspecting planet findout tbe difference between him
       and the aspected planet; if thesum is above I sign, multiply the
       degrees etc. (ignoring sign)by 2 to get Drishti value. If the sum is
       above nine sinls, thedegrees to elapse be doubred to get aspectual
       vatue. rf thi 'sum is above 2 signs, the degrees etc. (in excess of 2
       signs) behalved and deducted from 60. tfthe sum exceecrs g signsiaia
       to the degrees etc, a figure of 30 to get Drishti value. in othercases,
       the sums be processed as explained earlier."

    READING: above 1 sign -> double the degrees; above 2 signs -> halve the
    excess degrees and deduct from 60; exceeding 8 signs -> add 30 to the
    degrees; above 9 signs -> double the degrees to elapse; otherwise the
    general rule. ("g signs" is 8: the segment must join 240° to 270°.)

    ⚠ "degrees to elapse" is ambiguous — see SATURN_DEGREES_TO_ELAPSE_AMBIGUOUS
      for both readings and the continuity argument for the one used here.
    """
    if 30.0 <= a < 60.0:
        return (a - 30.0) * 2.0                 # 0 -> 60, peaking on the 3rd
    if 60.0 <= a < 90.0:
        return 60.0 - (a - 60.0) / 2.0          # 60 -> 45
    if 240.0 <= a < 270.0:
        return (a - 240.0) + 30.0               # 30 -> 60, peaking on the 10th
    if 270.0 <= a < 300.0:
        return (300.0 - a) * 2.0                # 60 -> 0  [degrees REMAINING]
    return None


def _mars_virupa(a: float) -> float | None:
    """v.11. Peaks at the 4th (90°) and the 8th (210°).

    VERBATIM: "Deduct the longitude of Mars from that of theplanet aspected
      (by Mars). If the sum is 3 Rasis & c or 7Rasis & c, the degrees etc.
      (after ignoring Rasis) be reduceO from 60. If it is abovg 2. Rasis, the
      degrees etc. be increased byhalf of it (i.e. add 50'/,1 and superadd 15.
      If the sum.is bsigns, one Rupa is the value."

    READING: 3 Rāśis &c or 7 Rāśis &c (i.e. 90°-120° and 210°-240°) -> reduce
    the degrees from 60; above 2 Rāśis (60°-90°) -> increase the degrees by
    half of themselves and superadd 15; a sum of 6 signs (180°) -> one rūpa,
    which the general rule already gives, Mars needing no exception there.
    """
    if 60.0 <= a < 90.0:
        return (a - 60.0) * 1.5 + 15.0          # 15 -> 60, peaking on the 4th
    if 90.0 <= a < 120.0:
        return 60.0 - (a - 90.0)                # 60 -> 30
    if 210.0 <= a < 240.0:
        return 60.0 - (a - 210.0)               # 60 -> 30, peaked on the 8th
    return None


def _jupiter_virupa(a: float) -> float | None:
    """v.12. Peaks at the 5th (120°) and the 9th (240°).

    VERBATIM: "Deduct the longitude of Jupiter from that of the planet
      aspected by him. If the resultant sum is 3 Rasis & c or 7 Rasis & c,
      halve the degrees etc. (ignoring Rasis) and increase it by 45. If the
      sum is 4 Rasis & c or g Rasis & c, the degrees etc. (ignoring Rasis) be
      subtracted from 60. This will be the aspectual value. The sum being in
      conformity with others than these be treated as stated earlier."

    READING: 3 or 7 Rāśis &c (90°-120°, 210°-240°) -> halve the degrees and
    add 45; 4 or 8 Rāśis &c (120°-150°, 240°-270°) -> subtract the degrees
    from 60; otherwise the general rule. ("g Rasis" is 8 Rāśis: the two
    segments must be the 4th/8th-Rāśi pair, 120°-150° and 240°-270°.)
    """
    if 90.0 <= a < 120.0:
        return (a - 90.0) / 2.0 + 45.0          # 45 -> 60, peaking on the 5th
    if 120.0 <= a < 150.0:
        return 60.0 - (a - 120.0)               # 60 -> 30
    if 210.0 <= a < 240.0:
        return (a - 210.0) / 2.0 + 45.0         # 45 -> 60, peaking on the 9th
    if 240.0 <= a < 270.0:
        return 60.0 - (a - 240.0)               # 60 -> 30
    return None


_SPECIAL_VIRUPA = {
    "saturn": _saturn_virupa,
    "mars": _mars_virupa,
    "jupiter": _jupiter_virupa,
}

# Where the ślokas' own piecewise rules do not join up. These are properties of
# the text, not of this transcription, and are left visible rather than smoothed
# away. Each entry is (graha, angle, value just below, value at/above).
SPECIAL_DRISHTI_GAPS = (
    # v.11 gives Mars a rule for 210-240 but none for 180-210, so the general
    # rule runs down to 45 virūpas at 210° and Mars's own rule restarts at 60.
    ("mars", 210.0, 45.0, 60.0),
    # v.12's 120-150 and 240-270 segments both end at 30 virūpas, where the
    # general rule stands at 0 and 15 respectively.
    ("jupiter", 150.0, 30.0, 0.0),
    ("jupiter", 270.0, 30.0, 15.0),
)

# Filling any of the three would be inventing text. If a later reviewer decides
# Mars's 180-210 gap should be filled by symmetry with his 60-90 rise, that is
# a doctrinal decision and this constant is where to make it.
SPECIAL_DRISHTI_GAPS_UNRESOLVED = (
    "Three angles where ch.26's own special ślokas do not join up: Mars at "
    "210° (45 -> 60 virūpas, because v.11 covers 210-240 but nothing covers "
    "180-210), Jupiter at 150° (30 -> 0) and Jupiter at 270° (30 -> 15). "
    "Saturn's vv.9-10 are continuous everywhere. The steps are the text's, "
    "not this transcription's, and are left visible rather than smoothed."
)


def drishti_virupa(aspector_longitude: float, aspected_longitude: float,
                   graha: str) -> float:
    """Ch.26 vv.6-12 aspectual value in virūpas, 0-60 (60 = one rūpa = full).

    Degree-based, so this is NOT the whole-sign layer — use `graha_drishti()`
    to draw a chart. This is the quantity Drig Bala (ch.27 v.19) consumes.
    `aspected_longitude` may be a bhāva cusp; VERBATIM: "For house in aspect,
    consider the cusp of the hpuse, akin to a planetary degree."

    Raises ValueError on any key outside CANONICAL_GRAHAS.
    """
    _check_graha(graha)
    a = drishti_angle(aspector_longitude, aspected_longitude)
    special = _SPECIAL_VIRUPA.get(graha)
    if special is not None:
        v = special(a)
        if v is not None:
            return v
    return general_drishti_virupa(a)


def drishti_virupa_detail(aspector_longitude: float, aspected_longitude: float,
                          graha: str) -> dict:
    """`drishti_virupa()` plus the flags an API layer needs to caveat it."""
    a = drishti_angle(aspector_longitude, aspected_longitude)
    v = drishti_virupa(aspector_longitude, aspected_longitude, graha)
    notes = [DRISHTI_DIRECTION_CORRECTED]
    if graha == "saturn" and 270.0 <= a < 300.0:
        notes.append(SATURN_DEGREES_TO_ELAPSE_AMBIGUOUS)
    if graha in NODES:
        notes.append(NODE_GRAHA_DRISHTI_UNVERIFIED)
    return {
        "graha": graha,
        "angle": a,
        "virupa": v,
        "rupa": v / RUPA,
        "citation": "BPHS Vol I ch.26 vv.6-12",
        "counted_from": "degree",
        "verified": graha not in NODES,
        "notes": notes,
    }


# ---------------------------------------------------------------------------
# Chart builders
# ---------------------------------------------------------------------------

SIGN_UNITS = ("auto", "sign", "longitude")


def _sign_of(position, units: str = "auto") -> int:
    """Resolve a position to a sign index 0-11.

    A bare scalar is DANGEROUSLY ambiguous — 100 is both a legal longitude
    (Cancer) and, mod 12, a legal sign index (Leo) — and the old code resolved
    it by Python TYPE, so an upstream int()/round() silently rotated the whole
    chart. It now resolves as follows:

      units="sign"       every scalar is a sign index; a non-integral value
                         raises.
      units="longitude"  every scalar is a longitude in degrees.
      units="auto"       an object with .rasi or .longitude is read from that
                         attribute. A scalar >= 12 (or < 0) can only be a
                         longitude and is taken as one. A scalar in [0, 12) is
                         a sign index if it is an int, and RAISES if it is a
                         float, because there is nothing to decide it on.
    """
    if units not in SIGN_UNITS:
        raise ValueError(f"units must be one of {SIGN_UNITS}, not {units!r}")

    rasi = getattr(position, "rasi", None)
    if rasi is not None:
        return int(rasi) % 12
    lon = getattr(position, "longitude", None)
    if lon is not None:
        return int(float(lon) % 360.0 // 30)

    if isinstance(position, bool) or not isinstance(position, (int, float)):
        raise TypeError(f"cannot read a sign from {position!r}")

    if units == "sign":
        if float(position) != int(position):
            raise ValueError(
                f"units='sign' but {position!r} is not a whole sign index")
        return int(position) % 12
    if units == "longitude":
        return int(float(position) % 360.0 // 30)

    # auto
    if isinstance(position, int):
        if 0 <= position < 12:
            return position
        raise ValueError(
            f"ambiguous position {position!r}: an int outside 0-11 could be a "
            "sign index taken mod 12 or a longitude in degrees. Pass "
            "units='sign' or units='longitude'."
        )
    if 0.0 <= position < 12.0:
        raise ValueError(
            f"ambiguous position {position!r}: a value in [0, 12) could be a "
            "sign index or a longitude in degrees. Pass units='sign' or "
            "units='longitude'."
        )
    return int(float(position) % 360.0 // 30)


def graha_drishti_chart(positions: dict, include_nodes: bool = False,
                        units: str = "auto") -> dict:
    """Ch.26 vv.2-5 over a whole chart, both directions.

    `positions` maps a CANONICAL_GRAHAS key to a vedic.Graha (or anything with
    .rasi / .longitude), a sign index, or a longitude. Bare scalars are
    disambiguated by `units` — see `_sign_of`. An unknown graha key raises.

    Returns:
      casts    : graha -> {"signs": {sign: fraction}, "grahas": {graha: fraction}}
      received : {"signs":  {sign:  {graha: fraction}},
                  "grahas": {graha: {graha: fraction}}}

    Only non-zero aspects appear. `casts[g]["signs"]` is what you draw; the
    graha-to-graha view is the same relation restricted to occupied signs, and
    is asymmetric — Saturn may aspect Mars fully while Mars aspects Saturn not
    at all.
    """
    for g in positions:
        _check_graha(g)
    signs = {g: _sign_of(p, units) for g, p in positions.items()}
    actors = [g for g in signs if include_nodes or g not in NODES]

    casts: dict[str, dict] = {}
    recv_signs: dict[int, dict] = {s: {} for s in range(12)}
    recv_grahas: dict[str, dict] = {g: {} for g in signs}

    for g in actors:
        src = signs[g]
        to_signs = {}
        for s in range(12):
            f = graha_drishti(src, s, g)
            if f > 0.0:
                to_signs[s] = f
                recv_signs[s][g] = f
        to_grahas = {}
        for other, s in signs.items():
            if other == g:
                continue
            f = to_signs.get(s, 0.0)
            if f > 0.0:
                to_grahas[other] = f
                recv_grahas[other][g] = f
        casts[g] = {"signs": to_signs, "grahas": to_grahas,
                    "from_sign": src,
                    "verified": g not in NODES}

    return {
        "doctrine": "graha_drishti",
        "citation": "BPHS Vol I ch.26 vv.2-5 (printed p.255 = PDFPAGE 254)",
        "counted_from": "sign",
        "casts": casts,
        "received": {"signs": recv_signs, "grahas": recv_grahas},
        "nodes_included": include_nodes,
        "all_verified": not include_nodes,
        "unverified": ([NODE_GRAHA_DRISHTI_UNVERIFIED] if include_nodes else []),
    }


def rasi_drishti_chart(positions: dict, units: str = "auto") -> dict:
    """Ch.8 vv.1-5 over a whole chart. Boolean throughout — the text grades
    nothing here (see RASI_DRISHTI_UNGRADED).

    Occupants ride their sign in both directions, per v.5: a graha lends the
    same aspect as the sign, and simultaneously a planet in the aspected sign
    is also subjected to the aspect concerned. Nodes take part like any
    occupant; that is not in doubt here (the SIGN aspects).

    Bare scalars are disambiguated by `units` — see `_sign_of`. An unknown
    graha key raises.
    """
    for g in positions:
        _check_graha(g)
    signs = {g: _sign_of(p, units) for g, p in positions.items()}

    casts: dict[str, dict] = {}
    recv_signs: dict[int, list] = {s: [] for s in range(12)}
    recv_grahas: dict[str, list] = {g: [] for g in signs}

    for g, src in signs.items():
        to_signs = list(RASI_DRISHTI[src])
        to_grahas = sorted(o for o, s in signs.items()
                           if o != g and s in RASI_DRISHTI[src])
        for s in to_signs:
            recv_signs[s].append(g)
        for o in to_grahas:
            recv_grahas[o].append(g)
        casts[g] = {"signs": to_signs, "grahas": to_grahas, "from_sign": src}

    return {
        "doctrine": "rasi_drishti",
        "citation": "BPHS Vol I ch.8 vv.1-5 (printed pp.105-107 "
                    "= PDFPAGE 104-106)",
        "counted_from": "sign",
        "graded": False,
        "ungraded_note": RASI_DRISHTI_UNGRADED,
        "sign_table": {s: list(t) for s, t in RASI_DRISHTI.items()},
        "casts": casts,
        "received": {"signs": recv_signs,
                     "grahas": {g: sorted(v) for g, v in recv_grahas.items()}},
        "all_verified": True,
        "unverified": [],
    }
