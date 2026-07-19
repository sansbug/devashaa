"""Bālādi and Jāgradādi avasthās — BPHS Vol I, Chapter 45.

Chapter 45 ("Avasthas Of Planets") opens by saying that many avasthā schemes
exist and that Parāśara will give the Bālādi summary "in the first instance"
(v.2). FIVE schemes follow in the chapter — Bālādi (vv.3-4), Jāgradādi
(vv.5-6), Dīptādi (vv.7-10), Lajjitādi (vv.11-29) and Sāyanādi (vv.30-155) —
which is also how the volume's own table of contents enumerates them ("Infant
state etc,, Awakening, dreaming and sleeping states, Deepta and other 8 ptates,
Lajjitadi avasthas, calculation of Sayana and other I I Avasthas"). THIS MODULE
IMPLEMENTS ONLY THE FIRST TWO — the two that are complete in the text and that
need nothing but a longitude and ch.3 dignity. The other THREE are surveyed at
the foot of this file and deliberately NOT implemented; see DEEPTADI_* and
LAJJITADI_* / SAYANADI_*.

QUOTATION CONVENTION IN THIS FILE. The scan of this chapter is unevenly OCR'd.
Where a quoted line is damaged, the raw scan reading is given verbatim under
"scan:" and any reconstruction is shown in [square brackets]. Nothing inside
quote marks is silently normalised.

  v.3  BĀLĀDI — THE FIVE STATES BY DEGREE
    "3. INFANT STATE ETC : Infant, youthful, adolescent, old and dead are the
     states of planets placed in the ascending ord[e]r at the rate of six
     degrees in odd signs. This arrangement is reverse in the case of even
     signs."
    scan: "ascending ordcr" — sole damage; the rest is clean.

    Santhanam's NOTE (not mūla) tabulates the odd-sign bands. The scan of the
    table is badly broken, so it is given raw first:
    scan: ". Infant state (Baalavastha) - 0 to.6o- Youthful state
           (Kumaravastha) _ 6 to 12"" / "Adolescent state (yuvavastlra) -12 to
           lg"" / "Advanced state (Vridhdhavastha) _lg to 24." / "In exrremis
           (Mritavastha) _24 to 30o" / "The above order is to be reversed for
           placement in an even sign."
    reading: Baalavastha 0-6°, Kumaravastha 6-12°, Yuvavastha 12-[18]°,
           Vridhdhavastha [18]-24°, Mritavastha 24-30°, reversed in even signs.
           ("lg" is OCR for "18" in both places; "yuvavastlra" for
           "yuvavastha"; "exrremis" for "extremis".) The numbers are fixed
           independently by v.3's own "six degrees" and by ch.11 below, so the
           broken digits are recovered rather than guessed.

  v.4  BĀLĀDI — THE GRADING OF RESULTS
    In our scan this śloka is shattered into five fragments printed out of
    order across the page break, so it is given raw rather than as a quote:
    scan: "4. RESULTS .. One fourth," / "are the grades of results due to" /
          "adolescent, old and dead states." / "half, full, negligible and
          nit" / "a planet in infant, youthful,"
    reading: "RESULTS : One fourth, half, full, negligible and ni[l] are the
          grades of results due to a planet in infant, youthful, adolescent,
          old and dead states."
    The fragments reassemble uniquely (each is a clause with exactly one
    possible neighbour), and every term is corroborated by ch.11 — see
    BALADI_GRADE below.

  v.5  JĀGRADĀDI — THE THREE STATES BY DIGNITY
    "5. AWAKENING, DREAMING AND SLEEPING srATES.' If a planet is in its own
     sign or in exaltatio[n] it is said to be in a state of awakening (or
     alertness). In the sign of a friend or of a neutral it is in dreaming
     state while in e[n]emy's sign or in deb[i]litation it is in a state of
     sleeping."
    scan: "srATES.'" for "STATES :", "exaltatioa", "afriend" (run together),
          "eiemy's", "debjlitation".

  v.6  JĀGRADĀDI — THE GRADING OF RESULTS
    "[6]. According to a planet being in Awakening, Dreaming. or Sleeping
     states, the results due to it will be full, medium or nil."
    scan: ". lt. According to a planet being in Awakening, Dreaming." — the
          verse NUMBER is OCR'd "lt.", not "6.". Its sequential position
          between v.5 and v.7 on the same page makes the numbering certain, so
          the citation "vv.5-6" stands; the mis-scan is recorded here so that
          anyone grepping the raw text for "6." and failing is not misled.

INDEPENDENT CORROBORATION. Chapter 45 is not the only place BPHS uses these
states. Ch.11 vv.14-16 ("Prosperity Or Annihilation Of A House") turns on them,
and Santhanam's notes there restate the bands in a form that is an exact
cross-check on the even-sign reversal — arrived at from the other direction,
naming the ODD arc and the EVEN arc for the same state. All three notes are
damaged in the scan, so each is given raw:

  note (c) Yuva or Kumāra —
    scan: "Soto say ifthe lord ofa house is in 6. to lgoofan odd eign, he will
           be in one of the two Avasthas required. Alternati-vely, it shbuld be
           between 12'and 24' of 0n even sign."
    reading: 6° to [18]° of an odd sign; alternatively between 12° and 24° of
           an even sign.
  note (e) Vṛddha —
    scan: "results" FpEnfiiIEEIitftFT8'-240 of an odd sign or betiveen 6o and
           12" of an even sign is said to be in such an Avastha."
    reading: "[between 1]8°-24° of an odd sign or between 6° and 12° of an even
           sign". The leading run "FpEnfiiIEEIitftFT" is DESTROYED, not merely
           mis-OCR'd — the word "between" there is a reconstruction from the
           parallel clause later in the same sentence, not a reading of the
           scan. Only the "8'-240" tail and the even-sign arc are legible.
  note (f) Mṛta —
    scan: "(f) If a planet is in Mgi!rygllA(in extremis) its bhava
           wil!-be.destroypd. This state ffis to a planet in the firffif an
           even sign or in the last 6" of an odd sign."
    reading: "This state [applies] to a planet in the fir[st 6° o]f an even
           sign or in the last 6° of an odd sign." ("ffis" and "firffif" are
           both destroyed runs; the last-6°-of-an-odd-sign clause is clean and
           by itself fixes the arc.)

All three fall out of "reverse in the case of even signs" and of nothing else,
which is why the reversal is treated here as verified rather than assumed. Ch.11
also glosses the Jāgradādi side:
  note (d) scan: "(d) Praluddhavastha is another name for Jagradavastha,
           meening a stote of awakenness. This applies to a planet in own eign
           or in cxaltation sign."
           reading: "P[r]abuddhavastha is another name for Jagradavastha …
           This applies to a planet in own [s]ign or in [e]xaltation sign."
  note (g) scan: "(g) Lastly, a planet in $uptavastha neutralises the "trect sf
           t@ This-Avastha-is due to a debititated planet or the one in an
           inimical camp."
           reading: "a planet in Suptavastha neutralises the [effect] of [the
           bhāva] … This Avastha is due to a debi[l]itated planet or the one in
           an inimical camp."

ODD AND EVEN SIGNS are ordinal, counted from Meṣa: Meṣa is the 1st and therefore
ODD. In this codebase signs are 0-indexed, so an odd sign is an EVEN index.

TWO GRADES ARE LEFT UNQUANTIFIED. v.4's "negligible" and v.6's "medium" are
words, not fractions. "One fourth", "half", "full" and "nil" are numbers and are
returned as 0.25 / 0.5 / 1.0 / 0.0. `fraction` is None for the other two rather
than being assigned an invented value — see BALADI_NEGLIGIBLE_UNQUANTIFIED and
JAGRADADI_MEDIUM_UNQUANTIFIED.

RANK IS NOT WHOLLY GIVEN BY THE TEXT EITHER. v.4 lists its five grades in STATE
order and never states a total order across them. Four of the five comparisons
are forced anyway; ONE — "negligible" (vṛddha) against "one fourth" (bāla) — is
an interpolation, and is flagged as such rather than presented as doctrine. See
BALADI_VRIDDHA_VS_BALA_INTERPOLATED, and the `rank_verified` key that every
baladi() result carries.

THE NODES. Ch.45 does treat Rāhu and Ketu as grahas — vv.30-37 assign them
Sāyanādi additaments ("Rahu 4 (and Ketu 4)"). Bālādi is a pure function of
degree within the sign, so it is returned for the nodes like any other graha;
the text states no exception for them. Jāgradādi is not, because it is a pure
function of dignity, and ch.3 v.50 gives the nodes no exaltation, debilitation
or rāśi lordship — dignity.py returns None for them and so does jagradadi().
An unrecognised graha key is a ValueError, NOT a silent None.
"""

from __future__ import annotations

from dignity import NATURAL_RELATIONS, RASI_LORD, dignity_of

# The nine grahas of ch.3. Derived from dignity.py's own seven so the two
# modules cannot drift apart; the nodes are named here because ch.45 vv.30-37
# treat them as grahas even though ch.3 v.50 gives them no dignity.
NODES = frozenset({"rahu", "ketu"})
GRAHAS = frozenset(NATURAL_RELATIONS) | NODES

# ---------------------------------------------------------------------------
# BĀLĀDI — v.3, v.4
# ---------------------------------------------------------------------------

# v.3, in the śloka's own ascending order for an ODD sign.
BALADI_ORDER = ("bala", "kumara", "yuva", "vriddha", "mrita")

# "at the rate of six degrees" — five states across a 30° sign.
BALADI_BAND = 6.0

# v.3's translated names, and Santhanam's note-labels where they differ.
BALADI_NAME = {
    "bala":    {"sanskrit": "Bālāvasthā",    "english": "infant"},
    "kumara":  {"sanskrit": "Kumārāvasthā",  "english": "youthful"},
    "yuva":    {"sanskrit": "Yuvāvasthā",    "english": "adolescent"},
    "vriddha": {"sanskrit": "Vṛddhāvasthā",  "english": "old"},
    "mrita":   {"sanskrit": "Mṛtāvasthā",    "english": "dead"},
}

# v.4, taken strictly in the śloka's order: the five grades are listed against
# the five states in the same sequence v.3 named them.
#   "One fourth, half, full, negligible and ni[l] are the grades of results due
#    to a planet in infant, youthful, adolescent, old and dead states."
BALADI_GRADE = {
    "bala": "one_fourth",
    "kumara": "half",
    "yuva": "full",
    "vriddha": "negligible",
    "mrita": "nil",
}

# The three that are arithmetic, plus nil. "negligible" is a word — see below.
BALADI_FRACTION: dict[str, float | None] = {
    "bala": 0.25,
    "kumara": 0.5,
    "yuva": 1.0,
    "vriddha": None,
    "mrita": 0.0,
}

BALADI_NEGLIGIBLE_UNQUANTIFIED = (
    "v.4 grades Vṛddhāvasthā 'negligible'. The śloka gives fractions for the "
    "other four grades but not for this one, so `fraction` is None. ch.11 "
    "note (e) says such a bhāva 'becomes ineffective from the view point of "
    "good results', which is a description, not a number. No value is "
    "supplied here."
)

# Ordered worst→best. FOUR of these five positions are forced by the text; one
# is not — see the flag immediately below and `rank_verified` in baladi().
BALADI_RANK = {"mrita": 0, "vriddha": 1, "bala": 2, "kumara": 3, "yuva": 4}

# The single comparison the text does not decide.
BALADI_RANK_INTERPOLATED_PAIR = ("vriddha", "bala")

# The states whose rank position depends on that interpolation.
BALADI_RANK_UNVERIFIED = frozenset(BALADI_RANK_INTERPOLATED_PAIR)

BALADI_VRIDDHA_VS_BALA_INTERPOLATED = (
    "INTERPOLATION, NOT DOCTRINE. ch.45 v.4 lists its grades in STATE order "
    "('One fourth, half, full, negligible and nil' against 'infant, youthful, "
    "adolescent, old and dead') and nowhere states a total order across the "
    "grades. Four comparisons are forced: one fourth < half < full by "
    "arithmetic, and 'negligible' > 'nil' because negligible is small and nil "
    "is zero. The FIFTH — 'negligible' (Vṛddha) against 'one fourth' (Bāla) — "
    "is NOT stated anywhere in ch.45. BALADI_RANK places Vṛddha BELOW Bāla on "
    "the strength of ch.11 vv.14-16, whose mūla names the bhāva-destroying "
    "states as 'threc Avasthas, viz, Vriddhavastha, Mritavastha and "
    "Suptava-sth8' [Vṛddhāvasthā, Mṛtāvasthā and Suptāvasthā] and does NOT "
    "name Bālāvasthā, while ch.11 note (c) names Yuva and Kumāra as the good "
    "ones — leaving Bāla in neither list and Vṛddha squarely in the bad one. "
    "That is an argument from a list Bāla is absent from, not a statement of "
    "rank, so `rank_verified` is False for both Vṛddha and Bāla. A reading "
    "that puts 'one fourth' below 'negligible' is not refuted by the text."
)


def is_odd_sign(sign: int) -> bool:
    """True for Meṣa, Mithuna, Siṁha, Tulā, Dhanus, Kumbha.

    v.3's rule hangs entirely on this parity. Signs are ORDINAL in the śloka
    (Meṣa = 1st = odd) but 0-indexed here, so odd sign ⇔ even index.
    """
    return sign % 2 == 0


def baladi(longitude: float) -> dict:
    """Bālādi avasthā of a graha at a sidereal longitude — ch.45 vv.3-4.

    Needs nothing but the longitude: v.3 is a statement about position within
    the sign and about that sign's parity, and about nothing else. No dignity,
    no graha identity, so this is valid for Rāhu and Ketu too.
    """
    lon = longitude % 360.0
    sign = int(lon // 30)
    deg = lon % 30.0

    # Which 6° band, counted from 0° of the sign. The clamp guards only against
    # float dust at exactly 30°; bands are half-open [lo, hi).
    band = min(int(deg // BALADI_BAND), 4)

    odd = is_odd_sign(sign)
    # "This arrangement is reverse in the case of even signs" — the SAME five
    # states, read from the far end of the sign. Derived, not a second table.
    index = band if odd else 4 - band
    state = BALADI_ORDER[index]

    return {
        "state": state,
        "sanskrit": BALADI_NAME[state]["sanskrit"],
        "english": BALADI_NAME[state]["english"],
        "sign": sign,
        "sign_parity": "odd" if odd else "even",
        "degree_in_sign": round(deg, 6),
        # The arc of THIS sign that carries this state.
        "band": {"from": band * BALADI_BAND, "to": (band + 1) * BALADI_BAND},
        "grade": BALADI_GRADE[state],                 # v.4
        "fraction": BALADI_FRACTION[state],           # None where v.4 gives a word
        "rank": BALADI_RANK[state],                   # 0 = mṛta … 4 = yuva
        # False for vṛddha and bāla: their relative order is interpolated from
        # ch.11, not stated in ch.45. See BALADI_VRIDDHA_VS_BALA_INTERPOLATED.
        "rank_verified": state not in BALADI_RANK_UNVERIFIED,
        "citation": "BPHS Vol I ch.45 vv.3-4",
    }


# ---------------------------------------------------------------------------
# JĀGRADĀDI — v.5, v.6
# ---------------------------------------------------------------------------

JAGRADADI_ORDER = ("supta", "swapna", "jagrat")   # worst → best

# The three ENGLISH names are the translation's own (v.5: awakening / dreaming /
# sleeping). The Sanskrit is a different matter and the difference is flagged:
# "Jagradavastha" and "Suptavastha" both appear in the text (ch.11 note (d)), but
# the middle state's Sanskrit name appears NOWHERE in either volume — grepped
# across both, zero hits for Swapna/Svapna. "Svapnāvasthā" is the conventional
# reconstruction from the scheme's own name (jāgrad-ādi) and is marked as such
# rather than presented as attested.
JAGRADADI_NAME = {
    "jagrat": {"sanskrit": "Jāgradavasthā", "english": "awakening", "attested": True},
    "swapna": {"sanskrit": "Svapnāvasthā",  "english": "dreaming",  "attested": False},
    "supta":  {"sanskrit": "Suptāvasthā",   "english": "sleeping",  "attested": True},
}
SWAPNA_NAME_UNATTESTED = (
    "The Sanskrit name of the middle Jāgradādi state is not in this text. "
    "v.5 names the STATE by its condition ('in the sign of a friend'), and "
    "ch.11 note (d) supplies 'Jagradavastha' and 'Suptavastha' but not the "
    "third. 'Svapnāvasthā' is conventional, not quoted — the state itself and "
    "its 'medium' grading (v.6) are both fully attested."
)

# v.6: "the results due to it will be full, medium or nil", against v.5's own
# order of awakening / dreaming / sleeping.
JAGRADADI_GRADE = {"jagrat": "full", "swapna": "medium", "supta": "nil"}
JAGRADADI_FRACTION: dict[str, float | None] = {
    "jagrat": 1.0,
    "swapna": None,
    "supta": 0.0,
}
# Unlike Bālādi, this order IS given by the text: v.6 grades the three "full,
# medium or nil", and full > medium > nil is forced.
JAGRADADI_RANK = {"supta": 0, "swapna": 1, "jagrat": 2}

JAGRADADI_MEDIUM_UNQUANTIFIED = (
    "v.6 grades Svapnāvasthā 'medium'. The śloka gives no fraction for it — "
    "only 'full' and 'nil' are numbers — so `fraction` is None. It is not "
    "assumed to be 0.5."
)

JAGRADADI_RELATION_BASIS = (
    "v.5 says 'the sign of a friend or of a neutral' and \"e[n]emy's sign\" "
    "without saying WHICH friendship. It does not qualify the word as "
    "temporary (tātkālika) or compound, so the naisargika relations BPHS "
    "itself defines in ch.3 v.55 are used, via dignity.py. A compound-relation "
    "reading is possible but the text does not state one."
)

# v.5's three buckets, keyed by the dignity states dignity.py reports.
#   "own sign or in exaltation"           → jāgrat
#   "sign of a friend or of a neutral"    → svapna
#   "enemy's sign or in debilitation"     → supta
_JAGRADADI_FROM_DIGNITY = {
    "exalted": "jagrat",
    "own": "jagrat",
    "friend": "swapna",
    "neutral": "swapna",
    "enemy": "supta",
    "debilitated": "supta",
}


def jagradadi(graha: str, longitude: float) -> dict | None:
    """Jāgradādi avasthā of a graha at a sidereal longitude — ch.45 vv.5-6.

    Returns None for Rāhu and Ketu, AND ONLY for them. v.5 keys entirely off
    own / exalted / friend / neutral / enemy / debilitated, and ch.3 v.50 gives
    the nodes none of those, so there is nothing to compute rather than
    something to guess.

    Raises ValueError for any other key. dignity_of() answers None for anything
    it does not recognise, so a typo ("Moon", "moon ") would otherwise be
    reported as "this is a node" — a wrong statement about a real chart rather
    than an error.
    """
    if graha not in GRAHAS:
        raise ValueError(
            f"unknown graha {graha!r}; expected one of {sorted(GRAHAS)}"
        )
    if graha in NODES:
        return None                      # Rāhu / Ketu — see module docstring

    dig = dignity_of(graha, longitude)
    if dig is None:                      # unreachable given the guard above
        return None

    lon = longitude % 360.0
    sign = int(lon // 30)
    dstate = dig["state"]

    if dstate == "moolatrikona":
        # dignity.py reports mūlatrikoṇa as a distinct arc; v.5 has no such
        # category. Resolve it by what the sign actually IS to this graha —
        # for six of the seven the mūlatrikoṇa arc lies inside their own rāśi,
        # which v.5 does cover. Tested rather than assumed. The Moon is the one
        # exception (her mūlatrikoṇa is Vṛṣabha, Śukra's sign) and that arc is
        # unreachable anyway, Vṛṣabha being her exaltation sign — but if it ever
        # were reached, v.5 would judge it by the relation to the sign's lord.
        if RASI_LORD[sign] == graha:
            state = "jagrat"
        else:
            state = _JAGRADADI_FROM_DIGNITY[
                NATURAL_RELATIONS[graha].get(RASI_LORD[sign], "neutral")
            ]
    else:
        state = _JAGRADADI_FROM_DIGNITY[dstate]

    return {
        "state": state,
        "sanskrit": JAGRADADI_NAME[state]["sanskrit"],
        "english": JAGRADADI_NAME[state]["english"],
        "dignity_state": dstate,          # what ch.3 said, before v.5 bucketed it
        "lord_of_sign": dig["lord_of_sign"],
        "grade": JAGRADADI_GRADE[state],  # v.6
        "fraction": JAGRADADI_FRACTION[state],
        "rank": JAGRADADI_RANK[state],    # 0 = supta, 1 = svapna, 2 = jāgrat
        "rank_verified": True,            # v.6's "full, medium or nil" is ordered
        "citation": "BPHS Vol I ch.45 vv.5-6",
    }


def avasthas(graha: str, longitude: float) -> dict:
    """Both implemented ch.45 schemes for one graha.

    `jagradadi` is None for the nodes. Nothing is combined into a single score:
    v.4 and v.6 are two separate gradings and Parāśara never multiplies them.
    """
    return {
        "graha": graha,
        "baladi": baladi(longitude),
        "jagradadi": jagradadi(graha, longitude),
    }


# ---------------------------------------------------------------------------
# SURVEY OF THE REST OF CHAPTER 45 — NOT IMPLEMENTED
#
# Recorded so the gaps are visible rather than silently absent. Each of these is
# either incomplete in the text or needs inputs (aspects, conjunctions, the
# native's NAME, the ghaṭīs of birth) that a longitude alone cannot supply.
# ---------------------------------------------------------------------------

# vv.7-10. DĪPTĀDI.
#
# v.7 scan: "7. OTHER KINDS OF STATES .' Thcre are nine kinds / of other
# states, viz. Deepta, Swastha, Pramudita, Santa, Deena, / Vikala, Khala. and
# KoPa." — the printed śloka SAYS nine and then names EIGHT.
#
# THE NINTH IS RECOVERED, from the volume's own ERRATA (Vol I p.483). The
# errata's two columns pair "450 l0 Vikala" (page 450, line 10, For) against
# "Dukkhita, Vikala" (Read); the alignment is exact — the ten entries of the
# second For block (358/376/382/400/431/432/450/454/456/462) map one-to-one
# onto the last ten entries of the Read column. Printed p.450 carries exactly
# one occurrence of "Vikala", the one in v.7's list above, so the correction
# has a single possible target and it INSERTS Duḥkhita before Vikala. Two
# corroborations: (a) the volume's table of contents reads "Deepta and other 8
# ptates" — nine in all, matching v.7's declared count; (b) v.7's Sanskrit line
# scans "dl.t: €rr[: qgfec' nr* ala]sq g:ftre: t", whose final word "g:ftre:"
# is a visarga-terminated form consistent with duḥkhitaḥ, i.e. the mūla has the
# word and the English translation dropped it. (b) is a reading of a mangled
# transliteration font and is treated as secondary; the errata is the warrant.
#
# THE SCHEME IS STILL NOT IMPLEMENTED. Recovering the ninth NAME does not
# recover its CAUSE: vv.8-10 assign causes to eight states and Duḥkhita is not
# among them. See DEEPTADI_DUKKHITA_CAUSE_UNSTATED and
# DEEPTADI_RESULTS_NOT_STATED.
DEEPTADI_STATES: dict[str, str | None] = {
    "deepta":    "exaltation sign",
    "swastha":   "own sign",
    "pramudita": "thick friend's sign",
    "santa":     "friendly sign",
    "deena":     "neutral's sign",
    "dukkhita":  None,                      # cause not stated — see flag below
    "vikala":    "in the company of a malefic",
    "khala":     "enemy's sign",
    "kopa":      "eclipsed by (combust with) the Sun",
}

DEEPTADI_NINTH_STATE = "dukkhita"

DEEPTADI_NINTH_STATE_SOURCE = (
    "ch.45 v.7 declares 'nine kinds' of Dīptādi states and the printed list "
    "names eight. The ninth is Duḥkhita, restored from BPHS Vol I's own errata "
    "(p.483): For 'Vikala' at p.450 line 10, Read 'Dukkhita, Vikala'. p.450 "
    "contains exactly one 'Vikala', in v.7's list, so the target is "
    "unambiguous. Corroborated by the table of contents ('Deepta and other 8 "
    "ptates' = nine) and by v.7's Sanskrit, which carries a duḥkhitaḥ-shaped "
    "word the English dropped."
)

DEEPTADI_DUKKHITA_CAUSE_UNSTATED = (
    "UNAVAILABLE. The ninth state's NAME is recovered (see "
    "DEEPTADI_NINTH_STATE_SOURCE) but its CAUSE is not. vv.8-10 assign causes "
    "to eight states — exaltation, own, thick friend's, friendly, neutral's, "
    "company of a malefic, enemy's, combustion — and Duḥkhita is not one of "
    "them. The errata corrects v.7 only; it does not touch vv.8-10. No cause "
    "is supplied, and none is guessed: DEEPTADI_STATES['dukkhita'] is None."
)

DEEPTADI_VIKALA_SPELLING_AMBIGUOUS = (
    "AMBIGUOUS. The same state is spelled two ways in our scan. v.7 (p.450) "
    "reads 'Vikala, Khala. and KoPa'; vv.8-10 (p.450) reads 'in the company of "
    "a malefic' Vikata'. This is the classic OCR l/t confusion and the text "
    "does not decide it — the errata's For column reads 'Vikala', targeting "
    "v.7's list on p.450 line 10, and says nothing about vv.8-10's 'Vikata'. "
    "DEEPTADI_STATES keys it 'vikala', following v.7 (the naming śloka, and "
    "the one the errata addresses). 'Vikata' is an equally supportable "
    "reading. Both are recorded in DEEPTADI_VIKALA_SPELLINGS."
)

DEEPTADI_VIKALA_SPELLINGS = {
    "chosen": "vikala",
    "v7_naming_sloka": "Vikala",
    "vv8_10_cause_slokas": "Vikata",
}

DEEPTADI_RESULTS_NOT_STATED = (
    "vv.8-10 close with only 'Depending on such a state of tlie planet, ttre "
    "house occupied by it will obtain corresponding cfiecr[effects].' No "
    "per-state results are given, so there is nothing to grade — unlike v.4 "
    "and v.6. Also 'thick friend' (pramudita) vs 'friendly' (santa) needs a "
    "five-fold compound relation that ch.3 v.55 does not define."
)

# vv.11-18, with effects at vv.24-29. LAJJITĀDI — six states. Complete in the
# text, but every one of them depends on conjunction, aspect and bhāva
# placement, not on longitude alone, so it belongs to a module that has the
# whole chart. Left out of this one deliberately.
LAJJITADI_STATES = {
    "lajjita":   "in the 5th house with a node, or with the Sun, Saturn or Mars",
    "garvita":   "in exaltation or in Mūlatrikoṇa",
    "kshudita":  "in an enemy's sign, or conjunct/aspected by an enemy, or conjunct Saturn",
    "trushita":  "in a watery sign, aspected by a malefic and not by a benefic",
    "mudita":    "in a friendly sign, or conjunct/aspected by a benefic, or conjunct Jupiter",
    "kshobhita": "conjunct the Sun and conjunct/aspected by a malefic, or aspected by an enemy",
}
LAJJITADI_NOT_IMPLEMENTED = (
    "ch.45 vv.11-18 (effects vv.24-29). Complete in the text but requires "
    "aspects, conjunctions and bhāva positions. Out of scope for a "
    "longitude-only module."
)

# vv.30-37, with effects from v.40 on. SĀYANĀDI — twelve main states plus three
# sub-states (Dṛṣṭi / Ceṣṭā / Viceṣṭā, graded at vv.38-39). Santhanam notes
# Parāśara's own authority for it is the Adbhuta Sāgara.
#
# The two halves have DIFFERENT inputs and are flagged separately, because they
# are not equally out of reach:
#
#   MAIN twelve — v.30-37 and Santhanam's formula (s × p × n) + (a + g + r),
#   mod 12. Every term is chart data or birth data this codebase already
#   holds: s = the graha's nakṣatra number from Aśvinī, p = the graha's own
#   number (Sun 1, Moon 2 …), n = its navāṁśa number 1-9, a = the janma
#   nakṣatra, g = the ghaṭī of birth, r = the lagna's sign counted from Meṣa.
#
#   SUB-state — vv.30-37's second half additionally needs "the figure denoted
#   by the Anka valuc for the first syllablc of the native's personal name",
#   which is not chart data at all and which this codebase never collects.
SAYANADI_STATES = (
    "sayana", "upavesana", "netrapani", "prakasana", "gamana", "aagamana",
    "sabha", "aagama", "bhojana", "nrityalipsa", "kautuka", "nidra",
)
SAYANADI_MAIN_STATES_BUILDABLE = (
    "ch.45 vv.30-37. The TWELVE main states are BUILDABLE — computable from "
    "data this codebase already has: the graha's nakṣatra number from Aśvinī, its own "
    "graha number, its navāṁśa number, the janma nakṣatra, the ghaṭīs of "
    "birth and the lagna's sign counted from Meṣa — (s × p × n) + (a + g + r), "
    "mod 12. Not built here only because this module is longitude-only and "
    "has no birth time or lagna. This is a scope decision, NOT a gap in the "
    "text."
)
SAYANADI_SUBSTATE_NEEDS_NAME = (
    "ch.45 vv.30-37 (second half), graded at vv.38-39 as Dṛṣṭi / Ceṣṭā / "
    "Viceṣṭā. Unlike the twelve main states, the sub-state is NOT a function "
    "of the chart: it needs 'the figure denoted by the Anka valuc for the "
    "first syllablc of the native's personal name'. This codebase does not "
    "collect a personal name, so the sub-state is unbuildable for it."
)
SAYANADI_NOT_IMPLEMENTED = (
    "ch.45 vv.30-37, not implemented — but for two different reasons. The "
    "twelve MAIN states need only chart plus birth data and are buildable: "
    "see SAYANADI_MAIN_STATES_BUILDABLE. Only the SUB-state needs the "
    "native's personal name: see SAYANADI_SUBSTATE_NEEDS_NAME. Santhanam "
    "notes Parāśara's own authority here is the Adbhuta Sāgara."
)
