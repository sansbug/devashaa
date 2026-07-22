"""Nakṣatra interaction techniques on the `modern` tier — NOT BPHS, NOT doctrine.

WHAT THIS IS, AND THE WALL AROUND IT
------------------------------------
These are one modern author-group's interpretive techniques — "a planet in
Aśvinī adds a travel theme", "anything in Kṛttikā tends to split in two" — for
how a graha in a nakṣatra reads. They are NOT classical facts (those are the
`traditional` attribute table, api/nakshatra_attrs.py) and they are NOT Parāśara.
They ship on a `modern` footing and must never be blended into either.

Captured as POINTERS ONLY, per the project's provenance rules: a one-line neutral
gist, the author's page, and a `computable` flag — with NO worked examples, no
example-native names/dates/charts, and no reproduction of the book's prose. The
UI must present them as attributed "modern technique" cards and NEVER as chart
verdicts.

`computable` describes only whether the app COULD detect the STRUCTURAL trigger
(a graha or house-lord in the nakṣatra), never whether the interpretation is
endorsed:
    yes    — a clean structural flag (graha/lord in the nakṣatra)
    partly — needs an affliction / house-connection judgment we can approximate
    no     — interpretive, or leans on non-Parāśara material (see `non_parashara`)

THREE TECHNIQUES ARE NON-PARĀŚARA AND QUARANTINED. Rohiṇī T2 (outer planets),
Mṛgaśira T7 (Vāstu) and Puṣya T2 (a remedial mantra) lean on material outside
BOTH BPHS and the traditional canon. They carry `non_parashara` with the reason
and must be shown, if at all, only as clearly fenced notes — never auto-rendered
as computed results.

SOURCED FOR NINE OF TWENTY-SEVEN. The source book is Part I; it numbers 46
techniques across Aśvinī → Āśleṣā only. Rows 10-27 have no techniques here and
say so — they are a sourcing gap, not nakṣatras without techniques. Completing
them needs Parts II/III of the series.

SOURCE-NAME NOTE. The intake brief called this "Sunil John's book", but Part I
carries no mention of Sunil John — it is the Saptarishis / Vidhan Pandya
compilation, and is cited as such. (Sunil John is credited on Part 2, which the
`traditional` symbol table draws on for nakṣatras 10-18 — a different book.)
"""

from __future__ import annotations

TIER = "modern"

SOURCE = ("Predicting Through Nakṣatras, Part I (Saptarishis Publications; "
          "compiled & edited by Vidhan Pandya)")

SOURCE_NOTE = (
    "One modern author-group's interpretive techniques — not BPHS, not the "
    "traditional canon, and never a chart verdict. Captured as attributed "
    "pointers only (gist + page + a structural-trigger flag), no worked examples "
    "reproduced. Sourced for nakṣatras 1-9 only (the book is Part I)."
)

SOURCED = range(1, 10)            # 1..9; Part I stops at Āśleṣā

COMPUTABLE_MEANING = {
    "yes": "The structural trigger (a graha or house-lord in the nakṣatra) is "
           "cleanly detectable.",
    "partly": "The trigger needs an affliction / house-connection judgment the "
              "app can only approximate.",
    "no": "Interpretive, or leans on non-Parāśara material — not a structural "
          "flag the app computes.",
}

# The author-group's one-line THEME for each nakṣatra (modern framing).
_THEME = {
    1: "travel / transport",
    2: "restraint, sudden reversal",
    3: "cutting / splitting",
    4: "growth, attachment",
    5: "searching, direction",
    6: "storms, animals, sacrifice",
    7: "return, renewal",
    8: "nourishment, priesthood",
    9: "the serpent's coil",
}

# Non-Parāśara quarantine reasons, keyed (nakṣatra, technique-number).
_NP = {
    (4, 2): "outer planets (Pluto/Neptune) — outside both BPHS and the traditional canon",
    (5, 7): "Vāstu — outside both BPHS and the traditional canon",
    (8, 2): "a remedial mantra (Nārāyaṇa Kavaca) — outside both BPHS and the traditional canon",
}

# 46 techniques, transcribed as neutral one-line gists from docs/traditional-rules.md
# §3 (which was itself distilled from the book with no prose reproduced). Each:
# (gist, computable, page).
_TECHNIQUES = {
    1: [  # Aśvinī
        ("A planet or house-lord in Aśvinī adds a travel / transport theme to what that planet or lord signifies.", "yes", 1),
        ("A planet aspecting Aśvinī reads as a lesson urging self-improvement along that planet's significations.", "partly", 11),
        ("Aśvinī afflicted (occupant or lord) leans toward a vehicle accident, if other factors concur.", "partly", 16),
        ("Key planets in Aśvinī can point to a vehicle accident involving three or more people.", "yes", 28),
        ("Aśvinī afflicted can mean chronically failing to reach places on time (missing a train, flight or bus).", "partly", 35),
        ("Aśvinī's condition can make the native instrumental in uniting or separating other people.", "partly", 40),
    ],
    2: [  # Bharaṇī
        ("A planet in Bharaṇī (by lordship or kāraka) marks that relative or matter for disproportionate punishment or an assured reversal.", "yes", 43),
        ("A house-lord in Bharaṇī suggests the relative signified is secretive, sometimes concealing an addiction.", "yes", 63),
        ("A planet in Bharaṇī can give the relative ankle or lower-foot ailments, especially when afflicted.", "partly", 78),
        ("Mercury, Rāhu, Moon, Venus or Mars in Bharaṇī tied to the 7th/8th/12th can mean intense but short-lived affairs and unwise partner choices.", "partly", 86),
        ("Any planet in Bharaṇī tends to deliver its results suddenly.", "yes", 91),
        ("A key planet in Bharaṇī can bring a woman (not necessarily a lover) who profoundly, unconventionally changes the native's life.", "yes", 94),
        ("Any planet in Bharaṇī can give a major loss or reversal in that planet's kārakatva or lordship.", "yes", 97),
    ],
    3: [  # Kṛttikā
        ("Anything in Kṛttikā tends to split into two — a division of family, property or opinion.", "yes", 105),
        ("A key planet (7L/8L/Venus/5L) in Kṛttikā can mean a love affair where the partner rejects the native, or a lover whose mind wanders.", "partly", 110),
        ("A focal planet (Sun, Moon or lagna-lord) in Kṛttikā can mark a significant event around age 27.", "yes", 113),
        ("The 9L or Sun (from ascendant or Moon), also 5L or Jupiter, in Kṛttikā points to karmic payback between son and father.", "partly", 119),
    ],
    4: [  # Rohiṇī
        ("A key planet in Rohiṇī, afflicted, can mean the native is blamed at least once for an act he did not commit.", "partly", 121),
        ("Pluto or Neptune in Rohiṇī is read as a death-like situation or water problem at ages 38-50 or 65-75.", "no", 126),
        ("Key planets in Rohiṇī can incline the native to compare a spouse with previous partners.", "partly", 135),
        ("Key planets in Rohiṇī can incline toward relationships within the extended family.", "partly", 136),
        ("Key planets in Rohiṇī can give a plagiarism or forgery theme — as perpetrator, victim, or a copyright / false-signature dispute.", "partly", 147),
    ],
    5: [  # Mṛgaśira
        ("Key planets in Mṛgaśira can mean the native's children find fortune late in life.", "partly", 157),
        ("Key planets in Mṛgaśira can bring friction with one's children, especially during their upbringing.", "partly", 159),
        ("Key planets in Mṛgaśira can mean involvement in sports that require chasing or running.", "partly", 164),
        ("A planet in Mṛgaśira connected to the 6th house can mean that relative habitually eats left-over or junk food.", "partly", 170),
        ("A relative signified by a Mṛgaśira planet has a strong sense of direction if unafflicted; if afflicted, tends to get lost or run late.", "partly", 177),
        ("The 5L in Mṛgaśira can mean a division of property brings a grievance (a child unhappy with their share).", "partly", 182),
        ("A Mṛgaśira planet afflicted (or Mars afflicted) is read in Vāstu as afflicting the north-east (Īśānya) corner of the house.", "no", 182),
    ],
    6: [  # Ārdrā
        ("A planet in Ārdrā can mean the relative it signifies has a strong link — love, hate or a story — with animals.", "partly", 185),
        ("Key planets in Ārdrā can give a self-sacrifice theme.", "partly", 196),
        ("A 'storm' theme — key planets in Ārdrā tied to upheaval, whistle-blowing or exposure, often via the 10th house/lord or a 6th-house aspect.", "partly", 200),
    ],
    7: [  # Punarvasu
        ("Key planets in Punarvasu (especially Rāhu) can give a fascination with technology, tech-field work, or constant gadget upgrading.", "yes", 203),
        ("Key planets in Punarvasu can mean fortune and stability arrive only after much searching or repetition.", "partly", 217),
        ("Key planets in Punarvasu can give a fixation on healthy food or fitness, later lapsing into junk food.", "partly", 220),
        ("When such a native cares for someone, they tend to become the mother or father figure for that person.", "partly", 222),
    ],
    8: [  # Puṣya
        ("Key planets in Puṣya can mean indulging in, or being targeted by, sorcery or left-hand tantra (more so with the nodes / 8L / Venus / 5L involved).", "partly", 223),
        ("A remedial pointer: recitation of the Nārāyaṇa Kavaca is offered as the best remedy for focal planets in Puṣya.", "no", 230),
        ("Focal planets or the lagna-nakṣatra in Puṣya can incline toward playing politics or manipulating others for gain, or being the victim of it.", "partly", 231),
        ("A foster-parenting theme — fostering or being fostered.", "partly", 239),
    ],
    9: [  # Āśleṣā
        ("Any planet in Āśleṣā tends to deliver its result between ages 18 and 20.", "yes", 241),
        ("An ethic (gaṇḍānta): as a nāga star at the end of Cancer, the chief lesson is never to gossip or speak ill of anyone.", "no", 255),
        ("Key or focal planets in Āśleṣā can give psychic experiences or encounters with spirits.", "partly", 261),
        ("If Āśleṣā is afflicted, the native may damage the reputation or career of a few people.", "partly", 268),
        ("A 'plastic surgery of Āśleṣā' — wherever it sits, a major transformation in that area, for better or worse.", "yes", 274),
        ("Sexual planets (Venus, Mars) in Āśleṣā, if afflicted, can mean sexual imbalance.", "partly", 283),
    ],
}


def _technique(index: int, n: int, gist: str, computable: str, page: int) -> dict:
    out = {
        "n": n,
        "gist": gist,
        "computable": computable,
        "page": page,
        "tier": TIER,
        "cite": f"modern technique — {SOURCE}, p.{page}",
    }
    reason = _NP.get((index, n))
    if reason:
        out["non_parashara"] = reason
    return out


def techniques_of(index: int) -> dict:
    """The `modern`-tier interaction techniques for one nakṣatra (1-27).

    For 1-9 returns the sourced technique list with the author's theme; for 10-27
    an explicit gap (the book is Part I) — never invented.
    """
    if not 1 <= index <= 27:
        raise ValueError(f"nakṣatra index out of range: {index}")
    if index not in _TECHNIQUES:
        return {
            "index": index,
            "available": False,
            "tier": TIER,
            "reason": "No techniques sourced. The source book is Part I "
                      "(Aśvinī → Āśleṣā); nakṣatras 10-27 need Parts II/III and "
                      "are not guessed.",
            "techniques": [],
        }
    techs = [_technique(index, n, g, c, p)
             for n, (g, c, p) in enumerate(_TECHNIQUES[index], start=1)]
    return {
        "index": index,
        "available": True,
        "tier": TIER,
        "theme": _THEME[index],
        "source": SOURCE,
        "techniques": techs,
    }


def all_techniques() -> list[dict]:
    """Technique status for every nakṣatra 1-27 — the sourced nine and the gaps."""
    return [techniques_of(i) for i in range(1, 28)]


def total_count() -> int:
    """How many techniques are sourced in all (the book's 46)."""
    return sum(len(v) for v in _TECHNIQUES.values())
