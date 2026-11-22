"""The study view: which cited relations fire in a chart, across D1-D60 and transits.

Two products, both READ-ONLY over what is already registered. This module adds
no rule, no reading and no weight of its own:

  gap_map()       every relation axis (graha x rashi x nakshatra x bhaav x varga x
                  degree x transit) with the registered sources that cover it, the
                  cells each covers out of the cells the axis has, and what is
                  silent. The counts are read from the corpora at run time, so the
                  map cannot drift from the code.

  ledger(...)     for one chart (and optionally one transit moment): every cited
                  relation that fires, one row each, with its source, tier, locus
                  and confidence, plus a SILENCE row for every factor the chart has
                  but no registered text reads (most of D2-D60).

The discipline (CLAUDE.md, docs/classical-sources-policy.md):
  * cite or refuse: a row has a locus or it is a silence row, never a gap filled
    from general knowledge;
  * tiers are never blended: each row carries exactly one tier and one source;
  * no composite: there is no score, net or verdict key anywhere in the output
    (test_study.py fails if one appears);
  * sensitive passages (a death, a lifespan, a bereavement, a partner's
    fidelity) carry `sensitive: true` and their text is withheld unless the
    caller asks for it. The pattern mirrors web/src/findings.js SENSITIVE.
"""

from __future__ import annotations

import re

import saravali_rules as sv
import brihat_jataka_rules as bj
import phaladipika_rules as phal
import phaladipika_nodes_rules as phal_nodes
import phaladipika_lagna_rules as phal_lagna
import chamatkara_rules as cc
import gochara_rules
import bhava_phala_rules as bpr
import bhava_effects
import dhana_bhava
import yoga_rules
import antardasa_rules
import nakshatra_techniques
import charak_annual_rules
import varga_rules as vr
import bj_varga_rules as bjv
import arudha_argala as aa
import karakamsa_results as kres
import karakas
import vargas

GRAHAS7 = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn")
GRAHAS9 = GRAHAS7 + ("rahu", "ketu")
VARGAS = ("D1", "D2", "D3", "D4", "D7", "D9", "D10", "D12", "D16", "D20",
          "D24", "D27", "D30", "D40", "D45", "D60")
SIGN_COMMON = ["Mesh", "Vrishabh", "Mithun", "Kark", "Simha", "Kanya",
               "Tula", "Vrishchik", "Dhanu", "Makar", "Kumbh", "Meen"]
_GNAME = {"sun": "Surya", "moon": "Chandra", "mars": "Mangal", "mercury": "Budh", "jupiter": "Guru",
          "venus": "Shukr", "saturn": "Shani", "rahu": "Rahu", "ketu": "Ketu"}


def gname_plain(k):
    return _GNAME.get(k, k)


RASI_LORD = ["mars", "venus", "mercury", "moon", "sun", "mercury",
             "venus", "mars", "jupiter", "saturn", "saturn", "jupiter"]

# Mirrors web/src/findings.js SENSITIVE (test_study.py checks the two agree).
SENSITIVE_EN = re.compile(
    r"\b(destr(oy|oyed|uction)\w* (at once )?(of |both )?(the )?(coborn|co-born|preborn|afterborn|later born|wife|children|mother|father)|(preborn|afterborn|coborn|co-born|wife|children) will be destroyed|no offspring|no children|quit the world|death|die[sd]?|dying|dead|kill\w*|short-lived|short life|longevity|life-?span|widow\w*|bereave\w*|bereft of (his |her |a |the )?(child\w*|sons?|daughters?|wife|husband|spouse|father|mother|parents?|progeny|issue)|childless|issueless|adulter\w*|unchaste|los(e|es|ing|s) (of )?(his |her |a |the |one's )?(child\w*|sons?|daughters?|wife|husband|spouse|father|mother|parents?|brothers?|sisters?)|other(s'|'s)? (wives|women|men)|another('s)? (wife|woman))\b",
    re.I)
SENSITIVE_HI = re.compile(
    r"मृत्यु|मरण|अल्पायु|आयु क्षीण|विधवा|विधुर|निःसंतान|संतानहीन|व्यभिचार|परस्त्री|परपुरुष|(पुत्र|संतान|पत्नी|पति|पिता|माता)[^।]{0,12}(नाश|हानि|वियोग)")


def is_sensitive(text) -> bool:
    s = str(text or "")
    return bool(SENSITIVE_EN.search(s) or SENSITIVE_HI.search(s))


# ---------------------------------------------------------------- gap map

def _cells(grid, keys=None) -> int:
    """Number of filled (outer, inner) cells in a {outer: {inner: entry}} grid."""
    keys = keys or grid.keys()
    return sum(len(grid.get(k) or {}) for k in keys)


def _src(mod_or_id, tier, cells, note="", confidence=None):
    sid = mod_or_id if isinstance(mod_or_id, str) else mod_or_id.SOURCE.get("id")
    return {"source": sid, "tier": tier, "cells": cells,
            **({"confidence": confidence} if confidence else {}),
            **({"note": note} if note else {})}


def _status(possible, sources):
    best = max((s["cells"] for s in sources), default=0)
    if best == 0:
        return "silent"
    if possible is None:          # not a grid (verses, yogas): listed, not "complete"
        return "listed"
    return "covered" if best >= possible else "partial"


def _row(axis, dims, possible, sources, note="", candidates=None):
    return {"axis": axis, "dims": dims, "possible": possible,
            "sources": sources, "status": _status(possible, sources),
            **({"note": note} if note else {}),
            "candidates": candidates or []}


# Books ON HAND (C:\books\astro) that may cover a silent axis. A candidate is a
# lead to read, NOT a citation: its locus is unverified until extracted from the
# page and registered in docs/classical-sources-policy.md section 2.
CAND = {
    "bphs_ch7_vaiseshika": "BPHS I ch.6 vv.42-53 (pp.87-90, read 2026-11-19): the Vaiseshikamsha "
                           "names by the count of good vargas. Needs the Arudha lagna and combustion "
                           "before it can be applied.",
    "bj_sastri": "Brihat Jataka, V. Subramanya Sastri tr. (on hand, no text layer): to fill the Moon "
                 "in Asvini-Punarvasu and drekkanas 13-19, 27, 30, 31 (gists only, modern tr.).",
    "bj_moon_navamsa": "Brihat Jataka (Row 1919, public domain) ch.19, from about printed p.204: the "
                       "Moon in the navamsas of each sign. Locus to verify.",
    "saravali_navamsa": "Saravali (Santhanam): the chapters on the Moon/planets in navamsas and on "
                        "trimshamsas. Locus to verify.",
    "phal_ch3": "Phaladipika (V. Subrahmanya Sastri 1950 / Ojha Hindi): ch.3 on the vargas and "
                "their grades. Locus to verify.",
    "jp_vargas": "Jataka Parijata (Subramanya Sastri): its varga chapter. Locus to verify.",
    "bphs_av_transit": "BPHS Vol II, the Ashtakavarga chapters: results of transits through signs "
                       "by bindus (kakshya). Locus to verify.",
    "bphs_ch29": "BPHS I ch.29 (Santhanam, from PDF p.292, located 2026-11-21): the Arudha padas of the "
                 "houses and planets, and results from the Arudha Lagna.",
    "bphs_ch30": "BPHS I ch.30 (from PDF p.302): Upapada, the Arudha of the 12th. Its spouse and child verses "
                 "fall under the site's sensitive rules (CLAUDE.md rule 2).",
    "bphs_ch31": "BPHS I ch.31 (PDF pp.310-316): Argala (planetary intervention), its obstruction and effects.",
    "bphs_ch33": "BPHS I ch.33 (from about PDF p.318): results from the Karakamsa. The engine computes the "
                 "Karakamsa itself (karakas.py, ch.33 v.1) but registers none of its results.",
    "hora_sara":"Hora Sara (Santhanam): nakshatra and degree results. Locus to verify.",
}


def gap_map() -> dict:
    rows = []

    # D1 -- graha in rashi
    rows.append(_row(
        "graha x rashi (D1)", ["graha", "rashi"], 9 * 12,
        [_src(sv, "classical", _cells(sv.IN_SIGN)),
         _src(bj, "classical", _cells(bj.IN_SIGN))],
        note="Seven grahas x 12 from both. No registered text reads Rahu/Ketu in a sign."))

    # D1 -- graha in bhaav
    rows.append(_row(
        "graha x bhaav (D1)", ["graha", "bhaav"], 9 * 12,
        [_src(sv, "classical", _cells(sv.IN_HOUSE)),
         _src(bj, "classical", _cells(bj.IN_HOUSE),
              note="BJ defers Mars/Venus/Saturn elsewhere to the Sun/Jupiter."),
         _src(phal, "classical", _cells(phal.IN_HOUSE)),
         _src(phal_nodes.SOURCE.get("id", "phaladipika") + ":nodes", "classical",
              _cells(phal_nodes.IN_HOUSE), confidence="ocr_text"),
         _src(cc, "classical", _cells(cc.IN_HOUSE))]))

    # D1 -- house lord in house
    rows.append(_row(
        "bhaav lord x bhaav (D1)", ["bhaav", "bhaav"], 144,
        [_src("bphs", "sloka", len(bpr.LORD_IN_HOUSE), note="BPHS ch.24.")]))

    rows.append(_row(
        "bhaav-specific conditions (D1)", ["bhaav", "graha", "lord", "aspect"],
        None,
        [_src("bphs", "sloka", len(bhava_effects.VERSES),
              note="BPHS chs 12, 14-18, 20-23, matched on each verse's own condition."),
         _src("bphs", "sloka", len(dhana_bhava.VERSES), note="BPHS ch.13 vv.1-7 (2nd house).")],
        note="Not a grid: counted in verses. bhava_effects.py's docstring lists what is not evaluated."))

    rows.append(_row(
        "lagna rashi", ["rashi"], 12,
        [_src(phal_lagna, "classical", len(phal_lagna.BY_SIGN), confidence="ocr_text"),
         _src("bphs", "sloka", 12, note="BPHS ch.34: functional natures by ascendant (no phala).")]))

    rows.append(_row(
        "yoga", ["graha", "bhaav", "rashi", "lord"], None,
        [_src("bphs", "sloka", sum(1 for m in yoga_rules.YOGAS.values() if m.get("tier") == "sloka"),
              note="Catalogue; each yoga carries its own citation and tier."),
         _src("phaladipika", "classical",
              sum(1 for m in yoga_rules.YOGAS.values() if m.get("source") == "phaladipika"),
              note="Adh.6 v.57 Harsha/Sarala/Vimala; Adh.7 vv.26-29 nicabhanga (v.30 not read)."),
         _src("brihat_jataka", "classical",
              sum(1 for m in yoga_rules.YOGAS.values() if m.get("source") == "brihat_jataka"),
              note="ch.15 st.1-2 Pravrajya (st.3-4 not registered).")]))

    # Nakshatra axes
    rows.append(_row(
        "graha x nakshatra", ["graha", "nakshatra"], 9 * 27,
        [_src(bjv, "classical", len(bjv.MOON_IN_NAKSHATRA), confidence=bjv.CONFIDENCE,
              note="Moon only, Bṛhat Jātaka ch.16. Aśvinī-Punarvasu missing from the scan.")],
        note="Only the Moon is read, and only for 20 of its 27 nakshatras.",
        candidates=["hora_sara"]))
    rows.append(_row(
        "nakshatra (as a place)", ["nakshatra"], 27,
        [_src("bphs", "sloka", 27, note="Lord (Vol II ch.46 vv.12-14) and deity (ch.6 vv.24-26). Facts, no phala."),
         _src("traditional", "traditional", 27, note="nakshatra_attrs.py: gana, yoni, quality ... (muhurta tradition)."),
         _src("nakshatra_techniques", "modern", len(nakshatra_techniques._TECHNIQUES),
              note="Saptarishis Part I/II: techniques for nakshatras 1-18 only.")]))
    rows.append(_row(
        "nakshatra lord x graha", ["graha", "nakshatra lord"], None, [],
        note="The registered texts use the nakshatra lord for the dasha only. The planet "
             "matrix shows the relation as a fact; no text states a result for it."))

    # Degree
    rows.append(_row(
        "graha x degree (D1)", ["graha", "degree"], None,
        [_src("bphs", "sloka", 5, note="Baladi avastha, ch.45 vv.3-4 (five 6-degree stages)."),
         _src("bphs", "sloka", 3, note="Jagradadi avastha, ch.45 vv.5-6."),
         _src("bphs", "sloka", 7, note="Exaltation / deep debilitation degree, ch.3 vv.49-55; uccha bala ch.27 v.1."),
         _src("bphs", "sloka", 1, note="Nakshatra gandanta of the Moon, Vol II ch.92 v.3."),
         _src("patel", "modern", 2, note="Pushkara navamsa / bhaga; 64th navamsa (navamsa.py)."),
         _src("bphs", "sloka", 4, note="Full / medium / nil by the third of a hora, decanate, "
                                       "turyamsa or navamsa, ch.7 vv.13-16."),
         _src("bphs", "sloka", 60, note="Each half-degree's D60 deity, ch.6 vv.33-41.")],
        note="Degree enters as stage, distance from exaltation, the third of a part, and the part "
             "it falls in. No registered text gives a result for an exact degree.",
        candidates=["hora_sara"]))
    rows.append(_row(
        "what each division is read for", ["varga"], 16,
        [_src("bphs", "sloka", len(vr.USES), note="ch.7 vv.1-5.")]))
    rows.append(_row(
        "graha x hora (D2)", ["graha", "varga"], 7,
        [_src("bphs", "sloka", 7, note="Which grahas give effects in which hora, ch.7 v.13.")]))
    rows.append(_row(
        "bhaav lord x D60 / D16 part", ["bhaav", "lord", "varga"], 12,
        [_src("bphs+note", "note", 12, note="ch.7 vv.6-8. Which parts are benefic is the "
                                            "translator's note, so the row is tier 'note'.")]))
    rows.append(_row(
        "drekkana form (description)", ["rashi", "degree"], 36,
        [_src(bjv, "classical", len(bjv.DREKKANA), confidence=bjv.CONFIDENCE,
              note="Bṛhat Jātaka ch.27. A description, not a result for a person.")],
        note="10 stanzas not readable in the 1919 edition on hand."))

    # Vargas D2-D60
    for v in VARGAS[1:]:
        srcs = [_src("bphs", "sloka", 1, note="Division rule, ch.6 (calculation only).")]
        if v == "D9":
            srcs.append(_src("patel", "modern", 9 + 12,
                             note="C.S. Patel: vargottama results (9) and bhava-suchaka (12)."))
        srcs_reading = [s for s in srcs if s["tier"] != "sloka"]
        if v in vr.DEITY_CITATION:
            n = 5 if v == "D30" else vr.PARTS[v]
            rows.append(_row(
                f"graha x part deity ({v})", ["graha", "varga", "degree"], n,
                [_src("bphs", "sloka", n, note=vr.DEITY_CITATION[v])]
                + ([_src("bphs-note", "note", 60, note="Benefic / malefic marks: " + vr.D60_MARK_CITATION)]
                   if v == "D60" else []),
                note="The part's presiding deity. The text states no result for a deity "
                     "except in D60 (benefic or malefic)." if v != "D60" else
                     "Planets in benefic parts give auspicious results, malefic parts the opposite."))
        elif v == "D2":
            rows.append(_row("graha x part deity (D2)", ["graha", "varga"], 2, [],
                             note="The Sanskrit names the hora deities; the translation does not."))
        rows.append(_row(
            f"graha x rashi ({v})", ["graha", "rashi", "varga"], 9 * 12,
            srcs_reading,
            note=("Calculated (BPHS ch.6) and counted in Vimshopaka strength (ch.7 vv.17-27). "
                  "No registered text reads a graha in a sign of this division.")
            if v != "D9" else
            "Patel (modern tier) reads vargottama, pushkara and the D1 house of each D9 sign. "
            "No classical-tier graha-in-D9-sign reading is registered.",
            candidates=["bphs_ch7_vaiseshika"] + (["bj_moon_navamsa"] if v == "D9" else []) + (["bj_sastri"] if v == "D3" else [])
            + (["saravali_navamsa", "phal_ch3", "jp_vargas"] if v in ("D9", "D30") else [])))
    rows.append(_row(
        "strength across vargas", ["graha", "varga"], 9,
        [_src("bphs", "sloka", 7, note="Vimshopaka bala, ch.7 vv.17-27 (Rahu/Ketu excluded).")]))

    # Jaimini-style points that BPHS itself teaches (chs 29-33). Found missing when the
    # Science of Light syllabus was mapped against this table (docs/sol-topic-map.md).
    rows.append(_row("Arudha pada x bhaav / graha", ["bhaav", "rashi"], None,
                     [_src("bphs", "sloka", 12, note="The 12 bhava padas, ch.29 vv.1-5 (the verse's exceptions applied)."),
                      _src("bphs", "sloka", sum(1 for k in aa.V if k.startswith("29.") or k == "30.39"),
                           note="Result verses from the Arudha Lagna, ch.29 vv.8-36 and ch.30 v.39.")],
                     note="Graha padas of Mars to Saturn, v.24, v.29 and the strength clauses are not evaluated "
                          "(arudha_argala.py lists why). Upapada (ch.30) is left out.",
                     candidates=["bphs_ch30"]))
    rows.append(_row("Argala on a bhaav", ["bhaav", "graha"], None,
                     [_src("bphs", "sloka", 2, note="Formation and obstruction, ch.31 vv.2-9 and the quarter rule v.10, "
                                                   "both shown, never merged."),
                      _src("bphs", "sloka", 2, note="Effects, ch.31 vv.11-18.")],
                     note="Strength is not evaluated: where obstructors are as many as the Argala planets, "
                          "the result is left undecided."))
    rows.append(_row("Karakamsa results", ["graha", "varga"], None,
                     [_src("bphs", "sloka", len(kres.V), note="BPHS I ch.33: the sign verse and 14 verse groups on "
                                                              "houses from the Karakamsa, each in BOTH frames "
                                                              "(navamsa and rasi chart), neither chosen.")],
                     note="Left out: vv.12, 23-31, 47-49, 77-99 and the strength / Full Moon / shadvarga "
                          "clauses (karakamsa_results.py lists why)."))

    # Transits
    rows.append(_row(
        "transit graha x bhaav from Moon", ["transit", "graha", "bhaav"], 9 * 12,
        [_src(gochara_rules, "classical", _cells(gochara_rules.PHALA),
              note="Phaladipika ch.26 with the favourable houses and vedha.")]))
    rows.append(_row(
        "transit graha x bhaav from lagna", ["transit", "graha", "bhaav"], 9 * 12, [],
        note="Geometry only (gochara.py)."))
    rows.append(_row(
        "transit graha x natal graha / degree", ["transit", "graha", "degree"], None, [],
        note="Conjunction and aspect geometry only. A 'return' is a Western frame, not BPHS."))
    rows.append(_row(
        "transit x ashtakavarga bindus", ["transit", "rashi"], 7 * 12,
        [_src("bphs", "sloka", 0, note="Bindu TABLES are registered (ashtakavarga.py). "
                                       "transit_potency is our synthesis, not a text's result.")],
        candidates=["bphs_av_transit"]))
    rows.append(_row(
        "transit x nakshatra (tara)", ["transit", "nakshatra"], 27, []))

    # Time lords
    rows.append(_row(
        "dasha lord (natal placement)", ["graha", "bhaav", "rashi"], 9,
        [_src("bphs", "sloka", 9, note="Vol II ch.47 vv.5-6.")]))
    rows.append(_row(
        "antar-dasha (lord x sub-lord)", ["graha", "graha"], 81,
        [_src("bphs", "sloka", len(antardasa_rules.MATRIX), note="Vol II chs 52-60, with branch conditions.")]))
    rows.append(_row(
        "annual chart graha x bhaav", ["graha", "bhaav", "year"], 9 * 12,
        [_src("charak_varshaphala", "modern", _cells(charak_annual_rules.IN_HOUSE))]))

    summary = {s: sum(1 for r in rows if r["status"] == s) for s in ("covered", "partial", "listed", "silent")}
    return {"axes": rows, "summary": summary, "candidates": CAND,
            "note": ("Cells are counted per source and never added across sources: two sources "
                     "covering the same cell is a concordance, not double coverage.")}


# ---------------------------------------------------------------- ledger

def _r(axis, *, source, tier, citation, text=None, confidence=None, varga="D1",
       graha=None, rashi=None, nakshatra=None, bhaav=None, degree=None,
       transit=False, polarity=None, adaptation=None, show_sensitive=False, extra=None):
    sens = is_sensitive(text)
    row = {"axis": axis, "varga": varga, "transit": transit,
           "factors": {k: v for k, v in (("graha", graha), ("rashi", rashi),
                                         ("nakshatra", nakshatra), ("bhaav", bhaav),
                                         ("degree", degree)) if v is not None},
           "source": source, "tier": tier, "citation": citation,
           "confidence": confidence, "sensitive": sens,
           "text": text if (show_sensitive or not sens) else None}
    if polarity:
        row["polarity"] = polarity
    if adaptation:
        row["adaptation"] = adaptation
    if extra:
        row.update(extra)
    return row


def _silence(axis, varga, reason, factors):
    return {"axis": axis, "varga": varga, "silent": True, "reason": reason, "factors": factors}


def ledger(payload: dict, transit_grahas=None, show_sensitive=False) -> dict:
    """Every cited relation that fires for the chart in `payload` (/api/chart output).

    `transit_grahas`: optional list of {"key", "rasi", "longitude"} for one moment.
    """
    rows, silences = [], []
    S = dict(show_sensitive=show_sensitive)
    grahas = {g["key"]: g for g in payload.get("grahas", [])}
    lagna = payload.get("lagna_rasi")
    a = payload.get("analysis") or {}

    def fac(k):
        g = grahas.get(k) or {}
        n = g.get("nakshatra") or {}
        return dict(graha=k, rashi=g.get("rasi"), nakshatra=n.get("index"),
                    bhaav=g.get("bhava"), degree=round(g.get("longitude", 0) % 30, 4) if g else None)

    # graha x rashi / bhaav concordances
    cl = a.get("classical") or {}
    for rd in cl.get("readings") or []:
        for s in rd.get("sources") or []:
            src = s.get("source") or {}
            rows.append(_r("graha x rashi", source=src.get("id"), tier=src.get("tier", "classical"),
                           citation=s.get("citation"), text=s.get("gist"),
                           confidence=s.get("confidence"), adaptation=s.get("adaptation"),
                           **fac(rd["graha"]), **S))
    seen_sign = {rd["graha"] for rd in cl.get("readings") or []}
    for k in GRAHAS9:
        if k in grahas and k not in seen_sign:
            silences.append(_silence("graha x rashi", "D1",
                                     "No registered text reads this graha in a sign.",
                                     {"graha": k, "rashi": grahas[k]["rasi"]}))
    for rd in cl.get("house_readings") or []:
        for s in rd.get("sources") or []:
            src = s.get("source") or {}
            rows.append(_r("graha x bhaav", source=src.get("id"), tier=src.get("tier", "classical"),
                           citation=s.get("citation"), text=s.get("gist"),
                           confidence=s.get("confidence"), adaptation=s.get("adaptation"),
                           **fac(rd["graha"]), **S))

    # lord in house (BPHS ch.24)
    for b in (a.get("bhava_phala") or {}).get("bhavas") or []:
        lr = b.get("lord_rule") or {}
        if lr.get("citation"):
            rows.append(_r("bhaav lord x bhaav", source="bphs", tier="sloka",
                           citation=lr["citation"], text=lr.get("effect"),
                           graha=b.get("lord"), bhaav=b.get("lord_in_house"),
                           extra={"lord_of": b.get("house")}, **S))

    # bhaav-condition verses
    for m in (a.get("bhava_effects") or {}).get("matches") or []:
        for c in m.get("clauses") or []:
            rows.append(_r("bhaav condition", source="bphs", tier="sloka",
                           citation=m.get("citation"), text=m.get("text"),
                           bhaav=m.get("house"), polarity=c.get("polarity"),
                           extra={"grahas": c.get("grahas"), "why": (c.get("why") or {}).get("en")}, **S))
    for m in (a.get("dhana_bhava") or {}).get("matches") or []:
        for c in m.get("clauses") or []:
            rows.append(_r("bhaav condition", source="bphs", tier="sloka",
                           citation=m.get("citation"), text=m.get("text"), bhaav=2,
                           polarity=c.get("polarity"),
                           extra={"grahas": c.get("grahas"), "code": c.get("code")}, **S))

    # lagna / Moon sign descriptions
    ch = a.get("character") or {}
    csrc = (ch.get("source") or {}).get("id", "phaladipika")
    if (ch.get("lagna") or {}).get("citation"):
        rows.append(_r("lagna rashi", source=csrc, tier="classical", citation=ch["lagna"]["citation"],
                       text=ch["lagna"].get("gist"), confidence=ch["lagna"].get("confidence"),
                       rashi=ch["lagna"].get("sign"), **S))
    if (ch.get("moon") or {}).get("citation"):
        rows.append(_r("Moon rashi", source=csrc, tier="classical", citation=ch["moon"]["citation"],
                       text=ch["moon"].get("gist"), confidence=ch["moon"].get("confidence"),
                       graha="moon", rashi=ch["moon"].get("sign"),
                       extra={"basis": (ch["moon"].get("basis") or {}).get("citation")}, **S))

    # yogas
    for y in (a.get("yogas") or {}).get("detected") or []:
        rows.append(_r("yoga", source=y.get("source") or ("bphs" if y.get("tier") == "sloka" else y.get("tier")),
                       tier=y.get("tier"), citation=y.get("citation"), text=y.get("effect"),
                       extra={"yoga": y.get("name"), "computability": y.get("computability")}, **S))

    # per-graha signals with a degree basis (avastha, dignity, uccha) and vimshopaka
    for k, sigs in (a.get("grahas") or {}).items():
        for s in sigs:
            if not s.get("available", True) or not s.get("citation"):
                continue
            axis = {"baladi": "graha x degree", "jagradadi": "graha x degree",
                    "uccha_bala": "graha x degree", "dignity": "graha x rashi",
                    "vimsopaka": "strength across vargas",
                    "functional": "graha x lagna"}.get(s["name"])
            if not axis:
                continue
            rows.append(_r(axis, source="bphs", tier="sloka", citation=s["citation"],
                           text=s.get("label"), varga="D1-D60" if axis.startswith("strength") else "D1",
                           extra={"signal": s["name"], "value": s.get("value")}, **fac(k), **S))

    # gandanta (Moon)
    gd = payload.get("gandanta")
    if gd:
        rows.append(_r("graha x degree", source="bphs", tier="sloka",
                       citation=gd.get("citation", "BPHS Vol II ch.92 v.3"),
                       text=gd.get("note") or "Moon in nakshatra gandanta.", **fac("moon"), **S))

    # nakshatra as a place: facts with a locus, no phala
    for k, g in grahas.items():
        n = g.get("nakshatra") or {}
        if n:
            rows.append(_r("nakshatra (fact)", source="bphs", tier="sloka",
                           citation="BPHS ch.6 vv.24-26 (deity); Vol II ch.46 vv.12-14 (lord)",
                           text=f"{n.get('name')} pada {n.get('pada')}, deity {n.get('deity')}",
                           extra={"fact": True}, **fac(k), **S))
            if k != "moon":
                silences.append(_silence("graha x nakshatra", "D1",
                                         "No registered text gives a result for this planet in a nakshatra.",
                                         {"graha": k, "nakshatra": n.get("index")}))

    # D9 (modern tier, Patel)
    nv = payload.get("navamsa") or {}
    for it in (nv.get("vargottama") or {}).get("items") or []:
        rows.append(_r("graha x rashi", varga="D9", source="patel", tier="modern",
                       citation=nv["vargottama"].get("citation"), text=it.get("result"),
                       graha=it.get("key"), rashi=it.get("sign"), **S))
    for it in (nv.get("bhava_suchaka") or {}).get("items") or []:
        rows.append(_r("D9 sign x D1 bhaav", varga="D9", source="patel", tier="modern",
                       citation=nv["bhava_suchaka"].get("citation"),
                       text=f"{it.get('label')}: {it.get('meaning')}",
                       graha=it.get("key"), bhaav=it.get("house"), **S))

    # D2-D60: placements, and an explicit silence for each
    for v in VARGAS[1:]:
        place = {k: (g.get("vargas") or {}).get(v) for k, g in grahas.items()}
        lag_v = (payload.get("lagna_vargas") or {}).get(v)
        reason = ("No registered text reads a graha in a SIGN of this division. The part's deity "
                  "(BPHS ch.6) is listed where the translation names one.")
        if v == "D9":
            reason = ("Only the modern tier (Patel) reads the D9 here. No classical-tier "
                      "graha-in-D9-sign reading is registered.")
        silences.append(_silence(f"graha x rashi ({v})", v, reason,
                                 {"lagna": lag_v, "placements": place,
                                  "own_sign": sorted(k for k, s in place.items()
                                                     if s is not None and RASI_LORD[s] == k)}))

    # BPHS ch.6-7: part deities across D3-D60, hora, thirds, lord rules
    points = {k: (g["rasi"], g["longitude"] % 30) for k, g in grahas.items()}
    if payload.get("lagna_longitude") is not None:
        points["lagna"] = (lagna, payload["lagna_longitude"] % 30)
    for k, (sign, deg) in points.items():
        f = {"graha": k, "rashi": sign, "degree": round(deg, 4)}
        for v in vr.DEITY_CITATION:
            d = vr.deity(v, sign, deg)
            txt = f"Part {d['part']} of {v}: {d['name']}"
            rows.append(_r("graha x part deity", varga=v, source="bphs", tier="sloka",
                           citation=d["citation"], text=txt, confidence=vr.CONFIDENCE,
                           extra={"deity": d["name"], "fact": v != "D60",
                                  **({"note": d["note"]} if d.get("note") else {})}, **f, **S))
            if v == "D60":
                rows.append(_r("graha x part deity", varga="D60", source="bphs-note", tier="note",
                               citation=d["nature_source"],
                               text=f"{d['name']} (D60 part {d['number']}) is marked {d['nature']}. "
                                    "The verse: planets in benefic parts give auspicious results, "
                                    "in malefic parts the opposite.",
                               polarity="favourable" if d["nature"] == "benefic" else "adverse",
                               confidence=vr.CONFIDENCE,
                               extra={"verse": vr.D60_CITATION,
                                      **({"disputed": d["disputed"]} if d.get("disputed") else {})},
                               **f, **S))
        if k == "lagna":
            continue
        he = vr.hora_effect(k, sign, deg)
        if he:
            rows.append(_r("graha x hora", varga="D2", source="bphs", tier="sloka", citation=he["citation"],
                           text=(f"In the {he['hora'].capitalize()}'s hora. "
                                 + ("The verse names this graha as giving effects there."
                                    if he["gives_effects"] else
                                    "The verse names this graha as giving effects in the other hora.")),
                           confidence=vr.CONFIDENCE, extra={"hora_powerful": he["hora_powerful"]}, **f, **S))
        for v in vr.THIRDS_VARGAS:
            t = vr.thirds(v, deg)
            third = ["first", "middle", "last"][["full", "medium", "nil"].index(t["grade"])]
            rows.append(_r("graha x degree (thirds)", varga=v, source="bphs", tier="sloka",
                           citation=t["citation"],
                           text=f"In the {third} third of its {v} part: effects {t['grade']}.",
                           confidence=vr.CONFIDENCE, extra={"grade": t["grade"]}, **f, **S))

    natures = ((a.get("dhana_bhava") or {}).get("natures")) or {}
    if lagna is not None:
        for h in range(1, 13):
            lord = RASI_LORD[(lagna + h - 1) % 12]
            if lord not in points:
                continue
            sign, deg = points[lord]
            d60 = vr.deity("D60", sign, deg)
            if d60["nature"] == "malefic":
                rows.append(_r("bhaav lord x D60 / D16 part", varga="D60", source="bphs-note", tier="note",
                               citation=vr.LORD_RULE_CITATION, text=vr.LORD_RULE_TEXT, polarity="adverse",
                               graha=lord, bhaav=h,
                               extra={"why": f"The lord of house {h} is in {d60['name']}, a part the note marks malefic.",
                                      "basis": vr.D60_MARK_CITATION}, **S))
            d16_sign = (grahas.get(lord) or {}).get("vargas", {}).get("D16")
            d16_lord = RASI_LORD[d16_sign] if d16_sign is not None else None
            if d16_lord and natures.get(d16_lord) == "benefic":
                rows.append(_r("bhaav lord x D60 / D16 part", varga="D16", source="bphs-note", tier="note",
                               citation=vr.LORD_RULE_CITATION, text=vr.LORD_RULE_TEXT, polarity="favourable",
                               graha=lord, bhaav=h,
                               extra={"why": f"The lord of house {h} is in a D16 sign ruled by {d16_lord}, a natural benefic here.",
                                      "basis": vr.D16_NOTE_CITATION + "; natures BPHS I ch.3 v.11"}, **S))

    # BPHS chs 29-31: Arudha padas, their verses, and Argala
    try:
        aad = aa.evaluate({k: {"rasi": g["rasi"], "longitude": g["longitude"]} for k, g in grahas.items()},
                          lagna, natures=natures or None)
    except Exception:  # noqa: BLE001 — a failure here must not cost the rest of the study
        aad = None
    if aad:
        for h, p in aad["padas"].items():
            txt = (f"{p['name']} (pada of house {h}) is in {SIGN_COMMON[p['sign']]}, "
                   f"house {p['house_from_lagna']} from the Lagn.")
            if p["exception_applied"]:
                txt += (f" The verse's exception (vv.4-5) moved it from {SIGN_COMMON[p['plain_count']]}.")
            rows.append(_r("Arudha pada (fact)", source="bphs", tier="sloka", citation=aad["padas_citation"],
                           text=txt, confidence=aa.CONFIDENCE, rashi=p["sign"], bhaav=h,
                           extra={"fact": True, "pada_of": h}, **S))
        for h, a in aad["argala"]["houses"].items():
            for p in a["places"]:
                status = {"unobstructed": "unobstructed", "prevails_by_number": "prevails by number (v.4)",
                          "obstructed_unless_stronger": "obstructed unless the Argala planet is stronger (not evaluated)"}[p["status_vv2_9"]]
                txt = (f"From the {p['from']}: {', '.join(gname_plain(g) for g in p['argala'])} ({p['kind']}, {p['grade_v7']}). "
                       + (f"Obstructors in the {p['obstructed_from']}: {', '.join(gname_plain(g) for g in p['obstructors'])}. " if p["obstructors"] else "")
                       + f"By vv.2-9: {status}."
                       + (f" By v.10 (quarters): countered." if p["countered_v10"] else (" By v.10 (quarters): not countered." if p["obstructors"] else "")))
                rows.append(_r("Argala on a bhaav", source="bphs", tier="sloka", citation=a["citation"], text=txt,
                               confidence=aa.CONFIDENCE, bhaav=h, extra={"fact": True, "argala": p}, **S))
            if a["vipareeta"]:
                rows.append(_r("Argala on a bhaav", source="bphs", tier="sloka", citation="BPHS I ch.31 v.4 (p.312)",
                               text=f"Vipareeta Argala: three or more malefics in the 3rd ({', '.join(a['vipareeta'])}).",
                               polarity="favourable", confidence=aa.CONFIDENCE, bhaav=h, **S))
        for m in aad["matches"]:
            for c in m["clauses"]:
                rows.append(_r("Arudha / Argala verse", source="bphs", tier="sloka", citation=m["citation"],
                               text=m["text"], polarity=c.get("polarity"), confidence=aa.CONFIDENCE,
                               bhaav=m.get("house"),
                               extra={"why": c.get("why"), **({"gloss": m["gloss"]} if m.get("gloss") else {}),
                                      **({"note": m["note"]} if m.get("note") else {}),
                                      **({"via": m["via"]} if m.get("via") else {})}, **S))

    # BPHS ch.33: the effects of the Karakamsa, in both frames
    try:
        kk_info = karakas.karakamsa({k: g["longitude"] for k, g in grahas.items()},
                                    navamsa_of=vargas.d9_navamsa)
        kout = kres.evaluate(kk_info, {k: g["rasi"] for k, g in grahas.items()},
                             {k: (g.get("vargas") or {}).get("D9") for k, g in grahas.items()},
                             natures, (payload.get("lagna_vargas") or {}).get("D9"))
    except Exception:  # noqa: BLE001
        kout = None
    if kout and kout.get("available"):
        for m in kout["matches"]:
            for c in m["clauses"]:
                rows.append(_r("Karakamsa verse", varga="D9", source="bphs", tier="sloka", citation=m["citation"],
                               text=m["text"], polarity=c.get("polarity"), confidence=kres.CONFIDENCE,
                               graha=kout["atmakaraka"], rashi=kout["karakamsa"],
                               extra={"why": c.get("why"), "frame": m["frame"],
                                      **({"gloss": m["gloss"]} if m.get("gloss") else {}),
                                      **({"note": m["note"]} if m.get("note") else {})}, **S))
    elif kout:
        silences.append(_silence("Karakamsa results", "D9", kout["reason"], {}))

    # Brihat Jataka: the Moon in its nakshatra (ch.16), drekkana forms (ch.27)
    mn = (grahas.get("moon") or {}).get("nakshatra") or {}
    if mn.get("index"):
        e = bjv.moon_in_nakshatra(mn["index"])
        if e:
            rows.append(_r("graha x nakshatra", source="brihat_jataka", tier="classical",
                           citation=e["citation"], text=e["shown"], confidence=e["confidence"],
                           adaptation=e.get("adaptation"),
                           extra={"caveat": e["caveat"], **({"variant": e["variant"]} if e.get("variant") else {})},
                           **fac("moon"), **S))
        else:
            silences.append(_silence("graha x nakshatra", "D1",
                                     "Brihat Jataka ch.16 reads this nakshatra on a page missing from the edition on hand.",
                                     {"graha": "moon", "nakshatra": mn["index"]}))
    for k, (sign, deg) in points.items():
        e = bjv.drekkana_form(sign, deg)
        if e.get("missing"):
            silences.append(_silence("drekkana form (description)", "D3",
                                     f"{e['label'][0].upper() + e['label'][1:]}: {e['missing']}.", {"graha": k, "rashi": sign}))
            continue
        rows.append(_r("drekkana form (description)", varga="D3", source="brihat_jataka", tier="classical",
                       citation=e["citation"], text=e["shown"], confidence=e["confidence"],
                       adaptation=e.get("adaptation"), graha=k, rashi=sign, degree=round(deg, 4),
                       extra={"use": e["use"], "row_note": e["row_note"], "fact": True}, **S))

    # dasha lord verdicts (ch.47)
    for k, vd in ((payload.get("dasha") or {}).get("verdicts") or {}).items():
        if vd.get("silent"):
            continue
        rows.append(_r("dasha lord", source="bphs", tier="sloka", citation=vd.get("citation"),
                       text=vd.get("verse"), polarity=vd.get("state"), **fac(k), **S))

    # transits from the Moon (Phaladipika ch.26)
    if transit_grahas and "moon" in grahas:
        moon_r = grahas["moon"]["rasi"]
        hfm = {t["key"]: (t["rasi"] - moon_r) % 12 + 1 for t in transit_grahas}
        occ = {}
        for k, h in hfm.items():
            occ.setdefault(h, []).append(k)
        for t in transit_grahas:
            j = gochara_rules.transit_judgment(t["key"], hfm[t["key"]], occ)
            if not j:
                continue
            ph = j.get("phala") or {}
            rows.append(_r("transit graha x bhaav from Moon", transit=True,
                           source=gochara_rules.SOURCE["id"], tier="classical",
                           citation=ph.get("citation") or j.get("citation"),
                           text=ph.get("en"), confidence=ph.get("confidence"),
                           graha=t["key"], rashi=t["rasi"], bhaav=hfm[t["key"]],
                           polarity={"favourable": "favourable", "obstructed": "obstructed",
                                     "not-favourable": "not favourable"}.get(j.get("status")),
                           extra={"vedha": {"house": j.get("vedhaHouse"), "blockers": j.get("blockers")}
                                  if j.get("vedhaHouse") else None,
                                  "status_citation": j.get("citation")}, **S))
        silences.append(_silence("transit graha x bhaav from lagna", "D1",
                                 "Geometry only: no registered text reads transits from the lagna.",
                                 {"houses_from_lagna": {t["key"]: (t["rasi"] - lagna) % 12 + 1
                                                        for t in transit_grahas}}))
        silences.append(_silence("transit x nakshatra", "D1",
                                 "No registered text reads a transit by nakshatra (tara).", {}))

    by_axis, by_tier = {}, {}
    for r in rows:
        by_axis[r["axis"]] = by_axis.get(r["axis"], 0) + 1
        by_tier[r["tier"]] = by_tier.get(r["tier"], 0) + 1
    # Start here: for each house, the lines that are ABOUT that house. Counts by side are
    # shown side by side and never combined into a verdict.
    houses = []
    for h in range(1, 13):
        sign = (lagna + h - 1) % 12 if lagna is not None else None
        lord = RASI_LORD[sign] if sign is not None else None
        idx = []
        for i, r in enumerate(rows):
            f = r.get("factors") or {}
            if r["transit"]:
                continue
            if r["axis"] == "bhaav lord x bhaav" and r.get("lord_of") == h:
                idx.append(i)
            elif r["axis"] in ("bhaav condition", "bhaav lord x D60 / D16 part", "Argala on a bhaav",
                               "Arudha / Argala verse") and f.get("bhaav") == h:
                idx.append(i)
            elif r["axis"] == "graha x bhaav" and f.get("bhaav") == h:
                idx.append(i)
        side = {"favourable": 0, "adverse": 0, "stated": 0}
        for i in idx:
            p = rows[i].get("polarity")
            side[p if p in ("favourable", "adverse") else "stated"] += 1
        houses.append({
            "house": h, "sign": sign, "lord": lord,
            "lord_in": (grahas.get(lord) or {}).get("bhava"),
            "occupants": [k for k, g in grahas.items() if g.get("bhava") == h],
            "rows": idx, "lines": side,
            "sources": sorted({rows[i]["source"] for i in idx if rows[i].get("source")}),
            "sensitive_withheld": sum(1 for i in idx if rows[i]["sensitive"] and rows[i]["text"] is None),
        })

    uses = {v: {"topic": t, "words": w, "citation": vr.USES_CITATION,
                **({"adaptation": vr.USES_ADAPTATION[v]} if v in vr.USES_ADAPTATION else {})}
            for v, (t, w) in vr.USES.items()}
    return {"rows": rows, "silences": silences, "uses": uses, "houses": houses,
            "counts": {"rows": len(rows), "silences": len(silences),
                       "by_axis": by_axis, "by_tier": by_tier,
                       "sensitive_withheld": sum(1 for r in rows if r["sensitive"] and r["text"] is None)},
            "note": ("Each row is one source's cited line for one relation. Rows are never "
                     "added, netted or ranked; agreement and disagreement stay visible.")}
