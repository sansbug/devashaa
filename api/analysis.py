"""D1 analysis — assembles the Tier 0 BPHS engines into one chart payload.

This module computes nothing itself. Every value comes from a cited engine:

    dignity.py        ch.3 vv.49-55   exaltation, mūlatrikoṇa, natural relations
    relationships.py  ch.3 vv.55-58   temporary + compound (pañchadhā) relations
    vimsopaka.py      ch.7 vv.17-27   Viṁśopaka bala, 0-20, with its own bands
    avastha.py        ch.45 vv.3-6    Bālādi and Jāgradādi states
    drishti.py        ch.26, ch.8     graha dṛṣṭi and rāśi dṛṣṭi
    functional.py     ch.34, ch.44    functional nature by lagna, and mārakas
    karakas.py        ch.32           chara kārakas and Karakāṁśa

WHY THERE IS NO SINGLE VERDICT HERE
-----------------------------------
BPHS contains at least seven partially overlapping judgements of a graha and it
never combines them. There is no śloka anywhere in either volume that says how
to weigh Viṁśopaka against Bālādi against functional nature. So a composite
"this graha is good / bad" score would be OUR arithmetic wearing Parāśara's
authority, which is the one thing this project refuses to do.

What this module returns instead is a SIGNAL STACK: each judgement kept on its
own scale, with its own citation, and — crucially — its own availability state.
A signal that cannot be computed is returned explicitly as unavailable with the
reason, never silently omitted and never quietly replaced by a proxy.

THE FLAGS ARE THE POINT
-----------------------
Every engine exposes constants marking values the text does not settle: an
OCR-damaged word, an ambiguous śloka, a name that is conventional rather than
quoted. Those propagate into `flags` on the affected signal. A non-empty `flags`
means the UI must not present that value as settled. Dropping them here would
undo the whole audit, so `_flag()` is deliberately the only way a signal is
built.
"""

from __future__ import annotations

import dignity
import relationships as rel
import vimsopaka as vim
import avastha as av
import drishti as dr
import functional as fn
import karakas as kar

# The seven grahas BPHS assigns dignity, lordship and relationships to. The
# nodes are handled separately and mostly return unavailable — that absence is
# a finding (ch.3 v.50 gives them no exaltation), not a gap to be filled.
SEVEN = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn")
NODES = ("rahu", "ketu")


def _signal(name, citation, value=None, scale=None, label=None,
            available=True, reason=None, flags=None, detail=None):
    """One row of the signal stack. `flags` non-empty => do not present as settled."""
    return {
        "name": name,
        "citation": citation,
        "value": value,
        "scale": scale,
        "label": label,
        "available": available,
        "reason": reason,           # why unavailable — shown to the user verbatim
        "flags": list(flags or []),
        "detail": detail,           # per-signal working, for the expanded view
    }


def _vimsopaka_signal(graha, varga_signs, rasi_positions):
    """Viṁśopaka bala — the headline number, ch.7 vv.17-27.

    Uses the COMPOUND relationship of the graha with each division's lord, which
    is what the book's own worked example does (Venus = 16.8, book p.99). The
    temporary half of that relationship is read from the RĀŚI chart even when
    scoring a varga — see relationships.RASI_ONLY.

    Shadvarga only. The other schemes are computable but Saptavarga's weights
    are unrecoverable from this scan, and shipping one scheme whose fixture
    reproduces the book exactly beats shipping four where one is a guess.
    """
    if graha not in SEVEN:
        return _signal(
            "vimsopaka", "BPHS Vol I ch.7 vv.17-27", scale="0-20",
            available=False,
            reason="Viṁśopaka rests on the graha's relationship with each "
                   "division's lord. BPHS gives Rāhu and Ketu no rāśi lordship "
                   "and no natural relationships (ch.3 v.50), so the ladder has "
                   "no rung for them. This is an absence in the text, not a "
                   "missing feature.",
        )

    rungs, flags = {}, []
    for key in vim.SCHEMES["shadvarga"]:
        sign = varga_signs.get(key)
        if sign is None:
            return _signal("vimsopaka", "BPHS Vol I ch.7 vv.17-27", scale="0-20",
                           available=False, reason=f"varga {key} not computed")
        rung = rel.dispositor_relation(graha, sign, rasi_positions)
        if rung is None:
            return _signal("vimsopaka", "BPHS Vol I ch.7 vv.17-27", scale="0-20",
                           available=False,
                           reason=f"no compound relationship available in {key}")
        rungs[key] = rung

    out = vim.vimsopaka("shadvarga", rungs)
    v = out["points"]
    # Two banding schemes come back. `verdict` is the ŚLOKA's own (vv.26-27) and
    # is what we label with — its words carry a citation. `grade` (Poorna,
    # Atipoorna…) is Santhanam's NOTE, so it stays in `detail` and is never the
    # headline label.
    band = out.get("verdict") or {}

    # The Moon's mūlatrikoṇa is OCR-damaged, and every natural relationship
    # involving her derives from it — so her ladder inherits that doubt.
    if graha in rel.NATURAL_UNVERIFIED or "moon" in (graha,):
        if graha in rel.NATURAL_UNVERIFIED:
            flags.append(rel.NATURAL_UNVERIFIED_NOTE)
    if v in (5.0, 10.0, 15.0):
        flags.append("Sits exactly on a band boundary; ch.7 vv.26-27's bands "
                     "are printed with overlapping endpoints and the text does "
                     "not say which side an exact value falls.")
    # Any conjunction in the chart engages the one reading the text leaves open.
    if _has_conjunction(rasi_positions):
        flags.append(rel.CONJUNCTION_IS_ENMITY)

    return _signal(
        "vimsopaka", "BPHS Vol I ch.7 vv.17-27",
        value=round(v, 4), scale="0-20", label=band.get("effect"),
        flags=flags, detail=out,
    )


def _has_conjunction(rasi_positions):
    """True if any two of the seven share a rāśi — engages CONJUNCTION_IS_ENMITY."""
    seen = {}
    for g in SEVEN:
        s = rasi_positions.get(g)
        if s is None:
            continue
        if s in seen:
            return True
        seen[s] = g
    return False


def _avastha_signals(graha, longitude):
    """Bālādi (degree) and Jāgradādi (dignity) — ch.45 vv.3-6."""
    out = []
    b = av.baladi(longitude)
    bflags = []
    if set(av.BALADI_RANK_UNVERIFIED):
        # v.4 lists the five gradings in state order; whether "negligible"
        # ranks below "one fourth" is an ordering the śloka does not state.
        bflags.append(
            "Bālādi states are fully sourced, but the RANK ORDER of the "
            "'negligible' and 'one fourth' gradings is not stated by v.4 — "
            "compare states by name, not by rank."
        )
    out.append(_signal(
        "baladi", "BPHS Vol I ch.45 vv.3-4",
        value=b.get("state"), scale=b.get("grade"),
        label=b.get("english") or b.get("state"),
        flags=bflags, detail=b,
    ))

    j = av.jagradadi(graha, longitude)
    if j is None:
        out.append(_signal(
            "jagradadi", "BPHS Vol I ch.45 vv.5-6", available=False,
            reason="Jāgradādi is read from the graha's dignity, which BPHS does "
                   "not assign to Rāhu or Ketu (ch.3 v.50).",
        ))
    else:
        jf = []
        if j.get("state") == "swapna":
            jf.append(av.SWAPNA_NAME_UNATTESTED)
        out.append(_signal(
            "jagradadi", "BPHS Vol I ch.45 vv.5-6",
            value=j.get("state"), scale=j.get("grade"),
            label=j.get("english") or j.get("state"),
            flags=jf, detail=j,
        ))
    return out


def _functional_signal(row):
    """Functional benefic/malefic for THIS lagna — ch.34.

    `row` is one entry of fn.lagna_profile()['grahas'], which already carries
    the śloka verdict, its source tag (sloka vs Santhanam note), the verbatim
    quote, and the derived-from-general-law verdict alongside it.

    Where the śloka states no nature we return unavailable rather than falling
    back to the derived verdict. ch.34's own note keeps a MĀRAKA verdict
    strictly apart from a benefic/malefic nature, and several verses issue only
    the former — promoting the derivation there would manufacture a judgement
    the sage declined to give.
    """
    nature = row.get("nature")
    citation = f"BPHS Vol I {row.get('citation') or 'ch.34'}"
    if nature is None:
        return _signal(
            "functional", citation, available=False,
            reason=row.get("quote")
                   or "BPHS states no nature for this graha at this lagna.",
            flags=row.get("flags") or [], detail=row,
        )
    flags = list(row.get("flags") or [])
    # The module's central promise is the source tag. A verdict resting on the
    # translator rather than the sage must say so, in the payload, not just in
    # a docstring.
    if row.get("source") == "note":
        flags.append(
            "This classification comes from Santhanam's NOTES, not from a "
            "śloka. Parāśara is silent for this graha at this lagna."
        )
    return _signal(
        "functional", citation,
        value=nature, scale="benefic/malefic", label=nature,
        flags=flags, detail=row,
    )


def graha_signals(graha, chart_positions, lagna, functional_row=None):
    """The full signal stack for one graha. Each row independently cited."""
    lon = chart_positions[graha]["longitude"]
    varga_signs = chart_positions[graha]["vargas"]
    rasi_positions = {g: p["rasi"] for g, p in chart_positions.items()}

    sigs = [_vimsopaka_signal(graha, varga_signs, rasi_positions)]
    sigs += _avastha_signals(graha, lon)
    if functional_row is not None:
        sigs.append(_functional_signal(functional_row))

    d = dignity.dignity_of(graha, lon)
    if d is None:
        sigs.append(_signal(
            "dignity", "BPHS Vol I ch.3 vv.49-55", available=False,
            reason="BPHS assigns Rāhu and Ketu no exaltation, debilitation or "
                   "mūlatrikoṇa. v.50's note says only that 'there are "
                   "different views'. The absence is the finding.",
        ))
        sigs.append(_signal(
            "uccha_bala", "BPHS Vol I ch.27 v.1", available=False,
            reason="No exaltation point exists for the nodes, so there is no "
                   "distance to one.",
        ))
    else:
        df = []
        if not d.get("moolatrikona_verified", True):
            df.append("This graha's mūlatrikoṇa arc comes from an OCR-damaged "
                      "śloka; the classical reading is used and flagged.")
        sigs.append(_signal(
            "dignity", "BPHS Vol I ch.3 vv.49-55",
            value=d["state"], scale="exalted…debilitated",
            label=d["state"], flags=df, detail=d,
        ))
        sigs.append(_signal(
            "uccha_bala", "BPHS Vol I ch.27 v.1",
            value=d["uccha_bala"], scale="0-1",
            label=f"{abs(d['uccha_distance']):.2f}° "
                  f"{'past' if d['uccha_distance'] >= 0 else 'short of'} exact",
            detail={"uccha_distance": d["uccha_distance"]},
        ))

    # Ṣaḍbala and Iṣṭa/Kaṣṭa are deliberately present-and-unavailable. Hiding
    # them would misrepresent the site's coverage; showing the reason turns a
    # gap into information, and tells the user exactly what a book would buy.
    sigs.append(_signal(
        "shadbala", "BPHS Vol I ch.27 vv.32-33", scale="virūpas",
        available=False,
        reason="Cheṣṭā bala requires each graha's Seeghrocha (śīghrocca). "
               "BPHS ch.27 vv.24-25 instructs its use but never tabulates a "
               "single value — the word appears three times in 1,034 pages, "
               "always undefined. There is also no worked Ṣaḍbala example in "
               "either volume to validate against.",
    ))
    # Unavailable for BOTH reasons, and they are different reasons — the UI
    # should say which. For five grahas the text cannot supply the input; for
    # Sūrya and Chandra it can, and we simply have not built it yet. Reporting
    # the second as "available" with a null value would be a false promise.
    sigs.append(_signal(
        "ishta_kashta", "BPHS Vol I ch.28 vv.2-6", scale="0-60",
        available=False,
        reason=("Computable for Sūrya and Chandra — vv.3-4 give their Cheṣṭā "
                "Kendra directly — but not yet implemented."
                if graha in ("sun", "moon") else
                "Cheṣṭā Raśmi needs the graha's Seeghrocha, which BPHS never "
                "tabulates. Only Sūrya and Chandra avoid it (vv.3-4)."),
    ))
    return sigs


def analyse(chart_positions, lagna, moon_waxing=None):
    """Whole-chart analysis payload.

    `chart_positions` maps graha key -> {"longitude", "rasi", "vargas"}.
    """
    rasi_positions = {g: p["rasi"] for g, p in chart_positions.items()}

    # One profile for the whole chart: it carries the ch.34 śloka verdict, its
    # source tag and quote for all nine grahas at this lagna.
    profile = fn.lagna_profile(lagna, moon_waxing=moon_waxing)
    frows = {r["graha"]: r for r in profile.get("grahas", [])}

    out = {
        "grahas": {
            g: graha_signals(g, chart_positions, lagna, frows.get(g))
            for g in chart_positions
        },
        "lagna_profile": profile,
        "relationships": rel.relationship_matrix(rasi_positions),
        "drishti": {
            "graha": dr.graha_drishti_chart(rasi_positions),
            "rasi": dr.rasi_drishti_chart(rasi_positions),
        },
        "maraka": fn.maraka_analysis(
            lagna, rasi_positions,
            **({"moon_waxing": moon_waxing} if moon_waxing is not None else {}),
        ),
        "notes": {
            "no_composite": (
                "BPHS supplies these judgements separately and never states how "
                "to combine them. Each row is kept on its own scale with its own "
                "citation. Any single 'score' would be our arithmetic, not "
                "Parāśara's."
            ),
            "whole_sign": (
                "Bhāvas are whole-sign throughout: a graha at 29° is wholly in "
                "its own house. BPHS gives no cusp formula in either volume."
            ),
        },
    }

    try:
        out["karakas"] = kar.chara_karakas(
            {g: p["longitude"] for g, p in chart_positions.items()}
        )
    except Exception as e:  # noqa: BLE001
        out["karakas"] = {"available": False, "reason": str(e)}

    return out
