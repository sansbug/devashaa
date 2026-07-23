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

# TWO books, TWO attributions — they must never be conflated. Part I (nakṣatras
# 1-9) is the Saptarishis/Pandya compilation with no Sunil John credit; Part 2
# (nakṣatras 10-18) IS credited to Sunil John. Each row cites its own book.
SOURCE = ("Predicting Through Nakṣatras, Part I (Saptarishis Publications; "
          "compiled & edited by Vidhan Pandya)")
SOURCE_PART2 = ("Predicting Through Nakṣatras, Part 2 (Saptarishis Publications; "
                "Sunil John & Vidhan Pandya)")


def _source_for(index: int) -> str:
    return SOURCE if index <= 9 else SOURCE_PART2


SOURCE_NOTE = (
    "One modern author-group's interpretive techniques — not BPHS, not the "
    "traditional canon, and never a chart verdict. Captured as attributed "
    "pointers only (gist + page + a structural-trigger flag), no worked examples "
    "or native chart data reproduced. Sourced for nakṣatras 1-18: Part I covers "
    "1-9, Part 2 covers 10-18 (Maghā → Jyeṣṭhā). 19-27 await Part 3."
)

SOURCED = range(1, 19)            # 1..18; Parts I-II reach Jyeṣṭhā

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
    # Part 2 (10-18) — neutral summaries of each nakṣatra's technique cluster.
    10: "power, downfall, lineage",
    11: "relationships, contracts, home, eyes",
    12: "sexuality, occult pull, addiction, wealth-marriage",
    13: "manipulation, 24th-year events, the father",
    14: "health, intricate craft, order",
    15: "illusion, breath, remedies",
    16: "grudges, dual careers, ambition",
    17: "26th-year events, humbled pride, desertion",
    18: "loss, scandal, injury, ritual timing",
}

# Non-Parāśara quarantine reasons, keyed (nakṣatra, technique-number). The flag
# marks a technique whose core is a non-canonical system (outer planets, Vāstu,
# KP, Western, numerology) OR a prescribed remedy / ritual rather than a
# chart-reading rule (mantra, homa, prāṇāyāma, herbal, ritual timing). Every
# flagged technique is also `computable: no`.
_NP = {
    (4, 2): "outer planets (Pluto/Neptune) — outside both BPHS and the traditional canon",
    (5, 7): "Vāstu — outside both BPHS and the traditional canon",
    (8, 2): "a remedial mantra (Nārāyaṇa Kavaca) — a prescribed remedy, not a chart-reading rule",
    (11, 5): "a prescribed household fire-ritual (homa) remedy — not a chart-reading rule",
    (11, 11): "an Astro-Vāstu directional method plus a decluttering remedy — outside the chart-reading canon",
    (15, 4): "a prescribed breath-control (prāṇāyāma) remedy — outside the classical jyotiṣa remedy set",
    (15, 6): "a prescribed herbal / Āyurvedic remedy — outside the classical jyotiṣa remedy set",
    (18, 5): "uses a ritual holy-dip as an event-timing device — outside classical daśā / transit timing",
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
    # ── Part 2 (Sunil John & V. Pandya), nakṣatras 10-18 — 51 techniques. Same
    #    pointer-only discipline: original one-line gists, no prose or worked
    #    examples reproduced. Distilled from the workflow extract→verify pass.
    10: [  # Maghā
        ("After roughly age 21 the Maghā span is said to grow active and influential in the chart, whether or not any planet occupies it.", "no", 11),
        ("Planets in Maghā give a hunger for power prone to a downfall when it or its lord is afflicted; a 6th- or 8th-lord aspect, or Ketu with the Sun, endangers one's standing.", "partly", 19),
        ("A planet in Maghā, or Maghā rising — especially a malefic — can bring a major fall from power or public disgrace, the planet's house-role hinting at the cause.", "yes", 27),
        ("When Maghā or its lord Ketu is afflicted, the native is prone to at least one severe investment or market loss, at times a dramatic collapse of wealth.", "partly", 35),
        ("Affliction of Maghā, particularly by Jupiter or Rāhu, inclines the native to a false spirituality they mistake for genuine depth.", "partly", 43),
        ("When Maghā is afflicted, or tied to an afflicted lunar node, the native is said to carry an ancestral or family curse in the lineage.", "partly", 44),
        ("Where the chart supports it, an unusual story or circumstance is said to surround the Maghā native's birth.", "no", 49),
    ],
    11: [  # Pūrva Phalgunī
        ("A key graha here (or being of this star) tends to bring a major relationship, or a strong activation of the star's themes, around age 24 give or take a year or two.", "yes", 58),
        ("A key graha here, or a document-signifying planet, inclines the native to at least one lifetime episode of trouble, entrapment or loss involving paperwork and contracts, worse under affliction.", "partly", 67),
        ("Mars occupying or aspecting this star can trigger property disputes, particularly when Mars is a functional malefic for the chart.", "yes", 78),
        ("Venus in the second quarter of this star can make an illicit relationship turn out badly, at times with serious consequences.", "yes", 84),
        ("Natives with key grahas here are drawn to fire and fire-offerings; a regular household fire-ritual is offered as their chief remedy.", "no", 87),
        ("With this star unafflicted, a native with key grahas here obtains and deeply wants a fine, well-placed home; Mars-affliction in the birth or property divisional chart instead gives a poorly-built one.", "partly", 90),
        ("For natives with key grahas here, the state of the bed and the state of the marriage are said to track each other.", "no", 97),
        ("Key grahas here incline the native to eye trouble and, figuratively, to being deceived or trusting blindly, more so under affliction.", "partly", 99),
        ("A subtle trait: natives with key grahas here keep expecting their fortune to swing between good and bad, the intensity tracking the star's strength.", "no", 118),
        ("Key grahas here incline the native to ostentation and lavish spending on celebrations, framed as a trait to outgrow.", "no", 124),
        ("Key grahas here accompany an accumulation of clutter to prune; the technique adds an Astro-Vāstu step mapping chart directions to household defects, with decluttering as remedy.", "no", 132),
        ("Key grahas here can give a carefree disposition that brings several notable setbacks or major life changes, presented as an area for growth.", "no", 139),
        ("Mars-based affliction or aspect on this star, including via the dispositor of Mars or Rāhu, is said to leave an injury-scar from a sharp object near the eye or eyebrow.", "partly", 142),
    ],
    12: [  # Uttara Phalgunī
        ("Malefic grahas tenanting or even aspecting this star can strain marriage or friendship and, at times, bring afflictions of the sexual organs or scandal.", "yes", 156),
        ("Natives tied to this star may be drawn toward occult or dark-tantra practice, pushed by an over-ambitious streak in their spiritual striving.", "partly", 169),
        ("Such natives may lean on alcohol or drugs to ease suffering; a benefic influence instead redirects them toward healing-oriented disciplines.", "partly", 179),
        ("A wealth-giving planet associating with or aspecting the star can make one materialistic in love or marry for money; heavy separative affliction risks a money-driven separation.", "partly", 180),
    ],
    13: [  # Hasta
        ("A significant planet in this star inclines the native to contriving or manipulative behaviour, sharpened when a malefic afflicts it, the sphere involved following that planet's significations.", "partly", 185),
        ("When any planet tenants this star and activates it, notable life events tend to fall around the native's twenty-fourth year.", "yes", 200),
        ("Affliction of this star — or the 9th lord (from lagna or Moon), or the Sun, placed here while afflicted — brings serious trouble to the father across the child's first four years.", "partly", 211),
    ],
    14: [  # Citrā
        ("Key planets in this star can incline the native to stomach ailments or complaints of the head.", "yes", 221),
        ("Natives of this star, or key planets here (which also stand for the relatives they signify), should take care during pregnancy, when complications may arise.", "yes", 240),
        ("Placement here inclines toward intricate design and craft — engineering, architecture, artistry — the particular field hinted by which house-lord tenants the star.", "yes", 243),
        ("An afflicted position here brings disorder to life, the remedy being to cultivate orderliness; unafflicted, the native is naturally methodical.", "partly", 251),
        ("When this star is afflicted it tends to produce separation, a split, or a lasting unfulfilled gap in the affected area; a Mars–Ketu pairing here is linked to electricity.", "partly", 260),
        ("High creativity is native here; using it for show or gain spoils the star, while detachment and selfless use uplift the whole chart.", "no", 265),
    ],
    15: [  # Svātī
        ("A graha in the 12th house that also sits in this star, or one influencing the 12th and tied to it, gives a quirky, asymmetric way of leaving one's footwear.", "partly", 267),
        ("When a prominent planet falls in this star, the native carries an unresolved bond or karmic debt tied to the mother or to inheritance.", "yes", 271),
        ("This Rāhu-ruled star gives one lasting area of self-delusion, its intensity scaled to Rāhu's strength, that the native keeps returning to despite setbacks.", "no", 282),
        ("Prescribes a breath-control practice as a corrective for natives with key planets in this star.", "no", 294),
        ("Affliction of this star, or an afflicted link to the 3rd house or its lord, is read as a marker of respiratory or breathing trouble.", "partly", 298),
        ("Recommends a specific herbal treatment for illness in natives with key planets here, conditional on an unafflicted Moon.", "no", 310),
        ("If this star is afflicted or linked to the 9th house or lord (from Moon or lagna), the native may change religion or turn religiously rigid.", "partly", 313),
    ],
    16: [  # Viśākhā
        ("Natives tend to hold a lifelong grudge or enmity, framed as carried over from a past life; the stated lesson is to release it for spiritual growth.", "yes", 317),
        ("Natives tend toward two parallel occupations — a second career, or a serious avocation that becomes one, an early specialization later branching in two.", "yes", 324),
        ("When the star or its lord is afflicted, natives put success first and pursue it at any cost, ending in at least one scandal of dishonest self-promotion.", "partly", 329),
    ],
    17: [  # Anurādhā
        ("When any planet tenants and activates this star, a notable life event of a distinct character tends to fall in the native's twenty-sixth year.", "yes", 333),
        ("When this star is afflicted, or holds any planet (a malefic most of all), a major event humbles the native by puncturing an inflated pride.", "partly", 348),
        ("The Moon, or another key planet linked to deception, in this star points to a mother-figure who abandons or betrays the native at a pivotal moment.", "yes", 351),
    ],
    18: [  # Jyeṣṭhā
        ("When an emphasized planet here is afflicted — more so where wealth houses are involved — the native tends to suffer monetary loss or to part with money.", "partly", 355),
        ("A malefic in this star, especially tied to sexual houses or planets and with the rest of the chart concurring, can involve the native in scandal, often of a sexual kind.", "partly", 365),
        ("When this star is afflicted, the relative signified by the house it occupies may have an ornament or amulet break or go missing.", "partly", 372),
        ("An afflicted Jyeṣṭhā, a malefic in it, or an afflicted 3rd lord (from lagna or Moon) here can injure or mark the middle finger; an afflicted 12th lord or afflicted Jupiter here is a further indicator.", "partly", 382),
        ("For a native with an important planet here, a holy dip in the Ganges is said to be followed within about a year by a significant event tied to that planet's house.", "no", 388),
    ],
}


def _technique(index: int, n: int, gist: str, computable: str, page: int) -> dict:
    out = {
        "n": n,
        "gist": gist,
        "computable": computable,
        "page": page,
        "tier": TIER,
        "cite": f"modern technique — {_source_for(index)}, p.{page}",
    }
    reason = _NP.get((index, n))
    if reason:
        out["non_parashara"] = reason
    return out


def techniques_of(index: int) -> dict:
    """The `modern`-tier interaction techniques for one nakṣatra (1-27).

    For 1-18 returns the sourced technique list with the author's theme, each row
    citing its own book (Part I for 1-9, Part 2 for 10-18); for 19-27 an explicit
    gap (Part 3 not yet in hand) — never invented.
    """
    if not 1 <= index <= 27:
        raise ValueError(f"nakṣatra index out of range: {index}")
    if index not in _TECHNIQUES:
        return {
            "index": index,
            "available": False,
            "tier": TIER,
            "reason": "No techniques sourced. Parts I-II cover nakṣatras 1-18 "
                      "(Aśvinī → Jyeṣṭhā); nakṣatras 19-27 need Part 3 and are "
                      "not guessed.",
            "techniques": [],
        }
    techs = [_technique(index, n, g, c, p)
             for n, (g, c, p) in enumerate(_TECHNIQUES[index], start=1)]
    return {
        "index": index,
        "available": True,
        "tier": TIER,
        "theme": _THEME[index],
        "source": _source_for(index),
        "techniques": techs,
    }


def all_techniques() -> list[dict]:
    """Technique status for every nakṣatra 1-27 — the sourced nine and the gaps."""
    return [techniques_of(i) for i in range(1, 28)]


def total_count() -> int:
    """How many techniques are sourced in all (the book's 46)."""
    return sum(len(v) for v in _TECHNIQUES.values())
