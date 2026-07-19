"""Pañcadhā Sambandha — the five-fold compound relationship.

BPHS Vol I, Chapter 3, vv.56-58. Every table here is transcribed from the
ślokas, not from memory.

QUOTATION CONVENTION. Our scan of Santhanam is unevenly OCR'd. Every quotation
below reproduces the scan CHARACTER FOR CHARACTER, with the repaired reading
following each damaged token in [square brackets]. Nothing inside a quotation
mark has been silently normalised. Line references are to the extracted text
(vol1.txt) so any claim here can be checked against the scan directly.

Citations:

  v.55      NATURAL (naisargika) RELATIONSHIP — not repeated here. It is
            already derived in `dignity.NATURAL_RELATIONS` from the
            mūlatrikoṇa rule, and this module imports it rather than
            restating it.

  v.56      TEMPORARY (tātkālika / horoscopic) RELATIONSHIP   [vol1.txt:1435]
    "The planet posited in the l0th [10th], 4th, llth [11th],3rd, 2nd or the
     l2tlt [12th] frornanother [from another] becomes mutual friend. There is
     enmity otherwise. (This applies to a given horoscope)'- [.]"

    Santhanam's note restates it as the three reciprocal pairs
    [vol1.txt:1441]:
    "If two are mutually in 4th and lbth [10th], or in 3rd and llth [11th] or
     in 2nd and l2th [12th], they become temporarily cordial to each other.
     Should they be otherwise, theie [there] previils [prevails] mutual
     temporary enmity."

  vv.57-58  COMPOUND RELATIONSHIP                              [vol1.txt:1450]
    "Should two planets be naturally and temporarily fiiendly [friendly], they
     become ixtremely [extremely] friendly. Friendship on one count and
     neutrality on another count make them friendly. Enmity on one count
     cornbined [combined] with afifinity [affinity] on the other turns jnto
     [into] equality. Enmity and neutralship cause only enmity. Should there be
     enmity in both manners, extreme enmity is obtained. ihJ [The] astrologer
     shourd [should] consider thcse [these] and decrare [declare] horoscopic
     effect accordingly."

    Santhanam names the result [vol1.txt:1460]:
    "The 1inal [final] relationshrp [relationship], as a result of natural and
     l:.I_n_oluy [temporary — the token is destroyed in the scan; the reading is
     fixed by v.56, which is the only other count the śloka combines]
     dispositions is cailed [called] S-fold [5-fold] relationship"

    — and tabulates it as the "Speculum of Compound Relat ionships [Compound
    Relationships]" on book p.42 (===PDFPAGE 41===, whose running head reads
    "42 Brihat pitrasara [Parasara] Hora Sastra"). His closing line
    [vol1.txt:1488] —
    "It is understood that if there is friendship with enmity,then [enmity,
     then] also neutrality will prevail."
    — is what establishes that the table is symmetric in its two INPUTS (it
    does not matter which count is the natural one and which the temporary).

THERE IS NO TEMPORARY "NEUTRAL". v.56 is strictly binary: the six houses
listed, or enmity. So of the 3x3 grid only six cells are ever reachable, and
`COMPOUND` below is written over the reachable pairs only.

CO-LOCATION IS TEMPORARY ENMITY — see `CONJUNCTION_IS_ENMITY` below. This is a
reading of the śloka that no worked example in either volume tests, and it is
flagged as such in the payload.

THE RELATION IS DIRECTIONAL. The temporary half is symmetric (the six friend
houses map onto each other under h -> 14-h, and so do the six enemy houses —
`test_relationships.py` asserts this rather than assuming it). The natural
half is NOT: by v.55 Venus counts the Moon an enemy while the Moon counts
Venus a neutral. So `compound_relation(a, b)` is the relationship a holds
TOWARDS b, and is not in general equal to `compound_relation(b, a)`.

RĀŚI CHART ONLY — see `RASI_ONLY` below.
RĀHU AND KETU — see `NODES_UNAVAILABLE` below.
THE MOON'S UNVERIFIED MŪLATRIKOṆA — see `NATURAL_UNVERIFIED` below.
"""

from __future__ import annotations

from dignity import NATURAL_RELATIONS, RASI_LORD, MOOLATRIKONA_UNVERIFIED

# ---------------------------------------------------------------------------
# v.56 — the temporary relationship.
# ---------------------------------------------------------------------------

# The six houses named in v.56, in the order the śloka names them. Counting is
# inclusive from the reference sign, so the 1st is the sign the reference graha
# itself occupies.
TEMPORARY_FRIEND_HOUSES: tuple[int, ...] = (10, 4, 11, 3, 2, 12)

# "There is enmity otherwise." Derived as the complement, never typed out as a
# second list — the śloka defines it by exclusion and so do we.
TEMPORARY_ENEMY_HOUSES: tuple[int, ...] = tuple(
    h for h in range(1, 13) if h not in TEMPORARY_FRIEND_HOUSES
)   # == (1, 5, 6, 7, 8, 9)

FRIEND, NEUTRAL, ENEMY = "friend", "neutral", "enemy"

# The 1st house — two grahas sharing a rāśi — is absent from v.56's list, and
# "There is enmity otherwise" therefore makes them temporary ENEMIES. We follow
# the śloka. But this is an INFERENCE FROM SILENCE, not something the book
# demonstrates, and it is the single most consequential interpretive fork in
# this module: every conjunction in a real chart renders satru or adhisatru
# where much modern software renders friendship. It is flagged rather than
# presented as settled.
CONJUNCTION_IS_ENMITY = (
    "AMBIGUOUS — a reading, not a demonstrated result. v.56 lists the 10th, "
    "4th, 11th, 3rd, 2nd and 12th as temporary friends and says 'There is "
    "enmity otherwise'; the 1st is not in that list, so we read co-location "
    "(conjunction) as temporary ENMITY, and Santhanam's gloss is consistent, "
    "naming only the 2/12, 3/11 and 4/10 reciprocal pairs. The rival reading, "
    "common in modern handbooks, promotes conjunction to friendship. NEITHER "
    "BPHS WORKED EXAMPLE DECIDES IT: ch.7's Viṁśopaka example has no "
    "co-located dispositor pair, and in Vol II ch.73 the three Kumbha "
    "occupants are all disposited by Saturn in Vṛścika, so no pair in either "
    "example is conjunct its own dispositor. Consumers rendering a "
    "conjunction should surface this."
)


def house_distance(from_sign: int, to_sign: int) -> int:
    """Inclusive house count from one rāśi to another, 1..12.

    The 1st is the sign you start in — the counting convention every "Nth
    from" statement in BPHS uses.
    """
    return (int(to_sign) - int(from_sign)) % 12 + 1


def temporary_relation(a_sign: int, b_sign: int) -> str:
    """v.56 tātkālika relation between grahas occupying two rāśis.

    Pure geometry: it depends only on the two signs, never on which grahas
    they are. Returns `FRIEND` or `ENEMY` — v.56 admits no third value.

    This is well-defined for Rāhu and Ketu too, since it asks nothing of them
    but a position. It is the *natural* half that the nodes lack.

    The same-sign case returns ENEMY — see `CONJUNCTION_IS_ENMITY`.
    """
    return (FRIEND if house_distance(a_sign, b_sign) in TEMPORARY_FRIEND_HOUSES
            else ENEMY)


# ---------------------------------------------------------------------------
# vv.57-58 — the compound relationship, the five grades.
# ---------------------------------------------------------------------------

ADHIMITRA = "adhimitra"      # "extremely friendly"  — parama/adhi mitra
MITRA = "mitra"              # "friendly"
SAMA = "sama"                # "equality"           — neutral
SATRU = "satru"              # "enmity"
ADHISATRU = "adhisatru"      # "extreme enmity"

# Two states that sit OUTSIDE the five-fold scale. A graha does not hold a
# relationship with itself, so when it occupies its own rāśi the bala ślokas
# score it on a separate footing (and higher than adhimitra in both).
OWN = "own"
MOOLATRIKONA = "moolatrikona"

# Weakest to strongest. Two independent ślokas enumerate the grades in this
# order, which is why we can be confident the set is exactly five and that
# `sama` sits in the middle:
#
#   ch.7 v.25 (Varga Viśva, out of 20) — [vol1.txt:3809]
#     "The Vimsopaka strength remains as 20 (in the above computat'ions
#      [computations]) only when the plun"t [planet] is in own house Vargas'
#      Otherwis.e [Otherwise] iU.-iotuf'r,rength [the total strength] from 20
#      declines to l8 [18] in €xtreme [extreme] friend's V;;"t [Vargas], to l5
#      [15] [in] frien<lly [friendly] Vargas, to l0 [10] in equal's divisions'
#      to 7 in eiemy's [enemy's] Vargas and to 5 in sworn enemy's Vargas'
#      (These figures are called Varga Viswa.)"
#
#   ch.27 vv.2-4 (Saptavargaja Bala, in virūpas) — [vol1.txt:10032]
#     "If a planet is in its Moolatrikona Rasi, it gets 45 Virupas, in own
#      Rasi 30 Virupas, cxtreme. [extreme] friend's Rasi 20 Virupas, friend's
#      Rasi 15 Virupas, neutral's Rasi l0 [10] Virupas, enemy's Rasi 4
#      Virr:pas [Virupas] and in extreme enemy's Rasi 2 Virupas."
GRADES: tuple[str, ...] = (ADHISATRU, SATRU, SAMA, MITRA, ADHIMITRA)

# Those two ślokas' own numbers, kept here because they are the textual
# EVIDENCE for the grade set above, not because this module computes bala.
# A bala module should cite the ślokas itself rather than import these.
#
# Each dict now carries EVERY value its śloka states, so that its name is not a
# promise it fails to keep — including the out-of-scale OWN (and MOOLATRIKONA,
# which only ch.27 gives). Callers iterating a scale must therefore iterate
# `GRADES`, not `dict.values()`; `OUT_OF_SCALE` names the extra keys.
OUT_OF_SCALE: tuple[str, ...] = (OWN, MOOLATRIKONA)

VARGA_VISWA = {                      # ch.7 v.25, out of 20
    ADHIMITRA: 18, MITRA: 15, SAMA: 10, SATRU: 7, ADHISATRU: 5,
    OWN: 20,
    # ch.7 v.25 states no separate mūlatrikoṇa value — it says only "own house
    # Vargas". MOOLATRIKONA is therefore deliberately ABSENT here rather than
    # borrowed from ch.27; the śloka does not give it.
}
SAPTAVARGAJA_VIRUPAS = {             # ch.27 vv.2-4
    ADHIMITRA: 20, MITRA: 15, SAMA: 10, SATRU: 4, ADHISATRU: 2,
    OWN: 30, MOOLATRIKONA: 45,
}

# vv.57-58, one entry per clause of the śloka. Keyed (one count, other count);
# the pair is unordered per Santhanam's "if there is friendship with enmity,
# then also neutrality will prevail", so the reversed key is filled in below
# rather than typed twice.
_COMPOUND_SLOKA = {
    (FRIEND, FRIEND): ADHIMITRA,     # "naturally and temporarily friendly ->
                                     #  extremely friendly"
    (FRIEND, NEUTRAL): MITRA,        # "friendship on one count and neutrality
                                     #  on another -> friendly"
    (FRIEND, ENEMY): SAMA,           # "enmity on one count combined with
                                     #  affinity on the other -> equality"
    (ENEMY, NEUTRAL): SATRU,         # "enmity and neutralship cause only
                                     #  enmity"
    (ENEMY, ENEMY): ADHISATRU,       # "enmity in both manners -> extreme
                                     #  enmity"
}
COMPOUND: dict[tuple[str, str], str] = dict(_COMPOUND_SLOKA)
COMPOUND.update({(b, a): v for (a, b), v in _COMPOUND_SLOKA.items()})

# (NEUTRAL, NEUTRAL) is absent on purpose and is unreachable: v.56 never
# yields a neutral, so at least one of the two counts is always friend or
# enemy. Leaving the cell out means a bug surfaces as a KeyError instead of
# being silently absorbed.


def compound_relation(a: str, b: str, a_sign: int, b_sign: int) -> str | None:
    """vv.57-58 pañcadhā sambandha that `a` holds towards `b`.

    `a_sign`/`b_sign` are the RĀŚI positions (0 = Meṣa .. 11 = Mīna) — see
    `RASI_ONLY`. Returns one of `GRADES`, or None when either graha is a node
    (see `NODES_UNAVAILABLE`).

    Directional: the natural half of the compound is asymmetric, so
    compound_relation("venus","moon",...) and compound_relation("moon","venus",...)
    legitimately differ.
    """
    if a not in NATURAL_RELATIONS or b not in NATURAL_RELATIONS:
        return None                  # Rāhu / Ketu — BPHS gives them none
    if a == b:
        return None                  # a graha holds no relationship to itself
    natural = NATURAL_RELATIONS[a][b]
    temporary = temporary_relation(a_sign, b_sign)
    return COMPOUND[(natural, temporary)]


def compound_rank(grade: str | None) -> int | None:
    """Ordinal 0..4 over `GRADES`, weakest first. None passes through.

    `OWN` and `MOOLATRIKONA` are rejected with an explicit error rather than
    ranked. They are not points on this scale: both bala ślokas score them on a
    separate and higher footing, so silently mapping them to None (which this
    module uses for "BPHS supplies no value") or to 4 would misrepresent them.
    """
    if grade is None:
        return None
    if grade in OUT_OF_SCALE:
        raise ValueError(
            f"{grade!r} is outside the five-fold scale of BPHS ch.3 vv.57-58 "
            f"and has no rank. dispositor_relation() returns it when a graha "
            f"occupies its own rāśi; score it from VARGA_VISWA / "
            f"SAPTAVARGAJA_VIRUPAS instead, which give it its own value."
        )
    return GRADES.index(grade)


# ---------------------------------------------------------------------------
# Applying it — dispositor and matrix.
# ---------------------------------------------------------------------------

# ch.27 vv.2-4, Santhanam's note [vol1.txt:10042-10044]:
#   "T.be [The] compound relationships of two given planets, vide p. i2 [42]
#    npra [supra] (including Hora lordship etc.) be seen in thc [the] Rasi
#    chart only and not in the concerned divisional chart."
#
# "p. 42 supra" is the Speculum of Compound Relationships: ===PDFPAGE 41=== of
# vol1.txt carries the running head "42 Brihat pitrasara Hora Sastra" and the
# speculum table is on it.
#
# NOTE, not mūla text — but it resolves a real ambiguity, and ch.7's own
# worked example obeys it: there Venus is scored across six vargas, and in
# every one of them the temporary half is read off Saturn's RĀŚI position
# (Libra), never off Saturn's position in the varga being scored. The test
# demonstrates this by computing the rival reading and showing it contradicts
# the book on three of the six rows.
#
# So the varga chooses WHICH lord you compare against; the rāśi chart supplies
# the positions the comparison is made from. `dispositor_relation` takes the
# occupied sign and the rāśi positions as separate arguments precisely so this
# cannot be got wrong.
RASI_ONLY = (
    "Pañcadhā sambandha is judged on the rāśi chart only. When scoring a "
    "divisional occupation, the varga supplies the sign-lord to compare "
    "against, but both grahas' positions are taken from the rāśi chart. "
    "Santhanam's note to ch.27 vv.2-4; followed by BPHS's own ch.7 "
    "Viṁśopaka worked example."
)

# v.55 derives natural relationship from a graha's mūlatrikoṇa and rāśi
# lordship. Rāhu and Ketu have neither, so the natural half — and therefore
# the compound — simply does not exist for them in Parāśara's text.
#
# The only thing the book offers is a Santhanam NOTE (Vol I p.41), and he
# flags its status himself [vol1.txt:1425]: "AsforRahuandKetu,thefollowingmay
# beofadditional intc rest.'' [As for Rahu and Ketu, the following may be of
# additional interest.]" It is unsourced, it supplies natural relations only,
# and no śloka in either volume ever computes a node's compound relationship.
# We therefore return None for the nodes and expose his note separately,
# clearly labelled, for a caller that knowingly wants it.
NODES_UNAVAILABLE = (
    "BPHS gives Rāhu and Ketu no mūlatrikoṇa and no rāśi lordship, so v.55 "
    "yields them no natural relationship and vv.57-58 no compound one. "
    "compound_relation() returns None for them. temporary_relation() DOES "
    "apply to them, being purely positional. See NODE_RELATIONS_SANTHANAM "
    "for the translator's note, which is not mūla text."
)

# Vol I p.41, Santhanam's note [vol1.txt:1426]:
#   "Rahu : The Sun, Moon and Mars are his enemies' [.] Jupiter, Venus and
#    Saturn are his friends' [.] Mercury is his ncutral [neutral].
#    Ketu : The luminaries are his enemics' [enemies.] Mars' [Mars,] Venus and
#    Saturn are his friends, while Mercury and Jupiter are his neutralS
#    [neutrals]."
# NOT used by any function in this module.
NODE_RELATIONS_SANTHANAM: dict[str, dict[str, str]] = {
    "rahu": {"sun": ENEMY, "moon": ENEMY, "mars": ENEMY,
             "jupiter": FRIEND, "venus": FRIEND, "saturn": FRIEND,
             "mercury": NEUTRAL},
    "ketu": {"sun": ENEMY, "moon": ENEMY,
             "mars": FRIEND, "venus": FRIEND, "saturn": FRIEND,
             "mercury": NEUTRAL, "jupiter": NEUTRAL},
}
NODE_RELATIONS_IS_NOTE = True

# Vol I p.41, on the Moon, corroborating v.55's derivation [vol1.txt:1419]:
#   "The Moon does not consider anyone as her enemy as per the folloiving
#    [following] statement of Parasara (Benares edition by Chaukamba
#    <devanāgarī, not legible in the extracted text> meanning [sic] meaning
#    further that the Sun and Mercury are Moon's friends while others are her
#    neutrals' [.] Saravali also has an identical view."
# dignity.NATURAL_RELATIONS reproduces exactly this from the mūlatrikoṇa rule.
MOON_HAS_NO_NATURAL_ENEMIES = True

# ...which matters, because the Moon's mūlatrikoṇa arc is itself flagged
# UNVERIFIED in dignity.py (the śloka is illegible in our scan). Only the SIGN
# is load-bearing here — dignity._relationships reads MOOLATRIKONA[graha][0]
# and never the degrees — and the Benares note above independently corroborates
# the sign. But by this module's own principle that caveats travel with the
# data, the flag is re-exported and carried in relationship_matrix()'s payload:
# every Moon row and column of the natural and compound matrices rests on it.
NATURAL_UNVERIFIED: frozenset[str] = frozenset(MOOLATRIKONA_UNVERIFIED)
NATURAL_UNVERIFIED_NOTE = (
    "The natural (v.55) half for these grahas is derived from a mūlatrikoṇa "
    "that dignity.py flags UNVERIFIED (dignity.MOOLATRIKONA_UNVERIFIED): the "
    "śloka is illegible in our scan and the classical reading is used. Only "
    "the mūlatrikoṇa SIGN affects v.55, not the degrees, and for the Moon "
    "Santhanam's Benares-edition note independently corroborates the sign — "
    "but every natural and compound cell in these grahas' rows and columns "
    "inherits the flag."
)


def dispositor_relation(graha: str, occupied_sign: int,
                        rasi_positions: dict[str, int]) -> str | None:
    """Compound relation a graha holds towards the lord of a sign it occupies.

    This is the form both of BPHS's worked examples use, and the form a bala
    or viṁśopaka computation needs. `occupied_sign` may be a VARGA sign;
    `rasi_positions` must always be rāśi positions (`RASI_ONLY`).

    Returns `OWN` when the graha rules the sign itself — a state outside the
    five-fold scale, scored separately by ch.7 v.25 and ch.27 vv.2-4, and
    rejected by `compound_rank` — or None if either graha is a node or the
    lord's position is unknown.
    """
    lord = RASI_LORD[int(occupied_sign) % 12]
    if lord == graha:
        return OWN
    if graha not in rasi_positions or lord not in rasi_positions:
        return None
    return compound_relation(graha, lord,
                             rasi_positions[graha], rasi_positions[lord])


def temporary_matrix(rasi_positions: dict[str, int]) -> dict[str, dict[str, str]]:
    """Full v.56 matrix over every graha given, nodes included."""
    keys = list(rasi_positions)
    return {
        a: {b: temporary_relation(rasi_positions[a], rasi_positions[b])
            for b in keys if b != a}
        for a in keys
    }


def compound_matrix(rasi_positions: dict[str, int]) -> dict[str, dict[str, str | None]]:
    """Full vv.57-58 matrix. Node rows and columns are None, not omitted.

    Kept as an explicit None rather than a missing key so that a caller
    rendering a 9x9 grid shows the nodes as "not applicable" instead of
    quietly dropping them.
    """
    keys = list(rasi_positions)
    return {
        a: {b: compound_relation(a, b, rasi_positions[a], rasi_positions[b])
            for b in keys if b != a}
        for a in keys
    }


def relationship_matrix(rasi_positions: dict[str, int]) -> dict:
    """Everything vv.55-58 say about one chart's grahas, in one structure.

    `rasi_positions` maps graha key -> rāśi index 0-11. Pass all nine; the
    node entries come back with natural/compound None and temporary filled in.

    Three caveats travel with the data and the API layer should surface them:
    `scope` (RASI_ONLY), `nodes` (NODES_UNAVAILABLE), `conjunction`
    (CONJUNCTION_IS_ENMITY), plus `natural_unverified`, which names the grahas
    whose natural half rests on an unverified mūlatrikoṇa.
    """
    keys = list(rasi_positions)
    natural = {
        a: {b: (NATURAL_RELATIONS[a][b]
                if a in NATURAL_RELATIONS and b in NATURAL_RELATIONS else None)
            for b in keys if b != a}
        for a in keys
    }
    compound = compound_matrix(rasi_positions)
    conjunct = sorted(
        {a for a in keys for b in keys
         if a != b and rasi_positions[a] == rasi_positions[b]}
    )
    return {
        "grahas": keys,
        "natural": natural,                       # v.55  (from dignity.py)
        "temporary": temporary_matrix(rasi_positions),   # v.56
        "compound": compound,                     # vv.57-58
        # compound_matrix never yields OWN (compound_relation() returns None
        # for a == b), so every cell here is a grade or None and compound_rank
        # is safe. The "dispositor" row below CAN be OWN, and is not ranked.
        "rank": {a: {b: compound_rank(v) for b, v in row.items()}
                 for a, row in compound.items()},
        "dispositor": {
            a: dispositor_relation(a, rasi_positions[a], rasi_positions)
            for a in keys
        },
        "citation": "BPHS Vol I ch.3 vv.55-58",
        "scope": RASI_ONLY,
        "nodes": NODES_UNAVAILABLE,
        # Grahas whose natural half rests on an UNVERIFIED mūlatrikoṇa, and
        # which are therefore present in this chart's matrices unflagged unless
        # the consumer acts on this key.
        "natural_unverified": sorted(NATURAL_UNVERIFIED & set(keys)),
        "natural_unverified_note": NATURAL_UNVERIFIED_NOTE,
        # The interpretive fork. `conjunction_affected` lists the grahas in
        # THIS chart that share a rāśi with another graha and whose temporary
        # relation therefore depends on the reading; empty means the caveat is
        # inert for this chart.
        "conjunction": CONJUNCTION_IS_ENMITY,
        "conjunction_affected": conjunct,
    }
