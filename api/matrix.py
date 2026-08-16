"""Chart-analysis matrix — per-chart domain verdicts (v1: bhāva + kāraka).

This assembles the natal factor web (Layer 2 of the design) into a single signed
iṣṭa/kaṣṭa verdict per **bhāva** (the classical primitive) and per **life-theme**
(a weighted composite of bhāvas + kārakas + a signature yoga). It integrates the
existing engines — ``bhava_phala`` (per-house lord/occupants/aspects/kāraka),
``functional`` (benefic/malefic per lagna), ``dignity``, ``drishti`` (virūpa
aspect strength), ``shadbala`` (magnitude), ``karakas`` (sthira + Jaimini chara),
``yogas`` — and rolls them up. No new astronomy; the weights are the only new
judgement, and they are transparent, returned in every verdict, and tunable.

DISCIPLINE (matches the pañcāṅga score + the site's cite-or-refuse ethos):
  * every contribution keeps its own value, weight, detail and CITATION;
  * the band is a tint over a visible weighted ledger — never a black box;
  * tiers stay separate — bhāva significations & lord-effects are BPHS ``sloka``;
    kāraka roles ``sloka``/``jaimini``; the theme WEIGHTS are a ``synthesis``
    tier (a curated heuristic), never merged into the śloka tier;
  * a verdict is an *indication*, not a fated outcome.

Varga (each theme's divisional chart) is the next phase — its weight is reserved
in the catalog as ``_varga`` slots that, until wired, drop out and the remaining
contributors renormalise (so the number stays honest about what went into it).
"""
from __future__ import annotations

import datetime as _dt
import random as _random
import re as _re

import swisseph as swe

import antardasa
import ashtakavarga
import charadasha
import classical
import functional
import bhava_phala as bhp
import karakas as kar
import yogas as yg
import shadbala_context
import drishti
from dignity import dignity_of
from vedic import CALC_FLAGS, _norm360
from vimshottari import running_lords

# ── the bhāva aggregator (signed contributors, sum 1.0) ─────────────────────────
# A house's net iṣṭa/kaṣṭa is a weighted sum of four contributors, each mapped to
# a signed strength in [-1, +1] (benefic well-placed → +, malefic/afflicted → −).
BHAVA_WEIGHTS = {
    "lord": 0.40,       # the house lord's condition (functional nature × dignity/placement)
    "occupants": 0.25,  # tenants' nature × dignity
    "aspects": 0.20,    # dṛṣṭi received, benefic(+)/malefic(−) by virūpa strength
    "karaka": 0.15,     # the house's sthira (naisargika) kāraka's disposition
}

# ── verdict bands over [-1, +1] ────────────────────────────────────────────────
_BANDS = [
    (0.40, "thriving"), (0.15, "supported"), (-0.15, "mixed"),
    (-0.40, "stressed"),
]


def band_of(net: float) -> str:
    """Classify a signed net ∈ [-1,+1] into one of five bands."""
    for lo, name in _BANDS:
        if net >= lo:
            return name
    return "afflicted"


# ── the theme catalog (starting weights — signed-off v1; each row sums to 1.0) ──
# houses: {house 1..12: weight}; sthira: {graha: weight}; chara: {Jaimini role:
# weight}; yoga: {yoga-key: weight}. A "_varga" yoga-key is the reserved slot for
# the theme's divisional chart (next phase); until then it renormalises away.
THEMES = [
    {"key": "self", "name": "Self · vitality · mind",
     "houses": {1: 0.55}, "sthira": {"sun": 0.15, "moon": 0.15}, "chara": {},
     "yoga": {"arishta": 0.15}, "varga": None},          # D1 = the natal chart itself
    {"key": "wealth", "name": "Wealth · finances",
     "houses": {2: 0.28, 11: 0.20, 5: 0.06, 9: 0.06},
     "sthira": {"jupiter": 0.08, "venus": 0.06}, "chara": {}, "yoga": {"dhana": 0.16},
     "varga": {"chart": "D2", "weight": 0.10}},
    {"key": "career", "name": "Career · status",
     "houses": {10: 0.28, 6: 0.07, 7: 0.05, 11: 0.06, 2: 0.04},
     "sthira": {"sun": 0.04, "saturn": 0.05, "mercury": 0.03},
     "chara": {"AmK": 0.11}, "yoga": {"raja": 0.12}, "varga": {"chart": "D10", "weight": 0.15}},
    {"key": "marriage", "name": "Marriage · partner",
     "houses": {7: 0.40, 2: 0.06, 8: 0.04, 12: 0.04},
     "sthira": {"venus": 0.12, "jupiter": 0.06},
     "chara": {"DK": 0.12}, "yoga": {}, "varga": {"chart": "D9", "weight": 0.16}},
    {"key": "children", "name": "Children · progeny",
     "houses": {5: 0.40, 9: 0.08}, "sthira": {"jupiter": 0.14},
     "chara": {"PK": 0.12}, "yoga": {"santana": 0.10}, "varga": {"chart": "D7", "weight": 0.16}},
    {"key": "health", "name": "Health · body",
     "houses": {1: 0.28, 6: 0.22, 8: 0.08, 12: 0.06},
     "sthira": {"sun": 0.05, "moon": 0.05}, "chara": {}, "yoga": {"balarishta": 0.14},
     "varga": {"chart": "D30", "weight": 0.12}},
    {"key": "education", "name": "Education · learning",
     "houses": {4: 0.24, 5: 0.24, 2: 0.08},
     "sthira": {"mercury": 0.10, "jupiter": 0.08}, "chara": {}, "yoga": {"budhaditya": 0.12},
     "varga": {"chart": "D24", "weight": 0.14}},
    {"key": "home", "name": "Home · property",
     "houses": {4: 0.56}, "sthira": {"mars": 0.12, "moon": 0.10, "venus": 0.06},
     "chara": {}, "yoga": {}, "varga": {"chart": "D4", "weight": 0.16}},
    {"key": "fortune", "name": "Fortune · dharma · father",
     "houses": {9: 0.56}, "sthira": {"sun": 0.10, "jupiter": 0.10},
     "chara": {}, "yoga": {}, "varga": {"chart": "D9", "weight": 0.24}},
    {"key": "enemies", "name": "Enemies · disease · debt",
     "houses": {6: 0.72}, "sthira": {"mars": 0.14, "saturn": 0.14},
     "chara": {}, "yoga": {}, "varga": None},            # 6th has no ṣoḍaśa varga
    {"key": "foreign", "name": "Foreign · loss · mokṣa",
     "houses": {12: 0.44, 9: 0.10, 8: 0.06},
     "sthira": {"saturn": 0.08, "ketu": 0.08, "jupiter": 0.06},
     "chara": {}, "yoga": {}, "varga": {"chart": "D20", "weight": 0.18}},
    {"key": "longevity", "name": "Longevity",
     "houses": {8: 0.30, 1: 0.24, 3: 0.10}, "sthira": {"saturn": 0.16},
     "chara": {}, "yoga": {"ayur": 0.20}, "varga": None, "maraka_modifier": True},
]

# Which detected-yoga categories satisfy each theme's signature-yoga slot. The
# yoga engine's category/name is matched against these; a "_varga" key never
# matches (its weight renormalises away until the divisional charts are wired).
_YOGA_SLOT_MATCH = {
    "raja": ("raja",), "dhana": ("dhana",), "arishta": ("arishta",),
    "balarishta": ("arishta", "balarishta"), "santana": ("santana", "progeny"),
    "budhaditya": ("budhaditya", "nipuna"), "ayur": ("ayur", "longevity"),
}


def compose(components: list[dict]) -> dict:
    """Weighted, renormalised iṣṭa/kaṣṭa from signed components.

    Each component is ``{value ∈ [-1,1], weight, ...}``. Components whose value
    is None (an inapplicable chara-kāraka, or a reserved/unmatched yoga slot) are
    dropped and the remaining weights renormalise to 1.0 — so the reserved varga
    slots simply hand their weight back to the live contributors, and the net
    stays a clean [-1,1] with the *effective* weights returned for transparency.
    """
    live = [c for c in components if c.get("value") is not None]
    wsum = sum(c["weight"] for c in live) or 1.0
    net = 0.0
    for c in live:
        c["effWeight"] = round(c["weight"] / wsum, 4)
        net += c["effWeight"] * c["value"]
    net = max(-1.0, min(1.0, net))
    return {"net": round(net, 4), "band": band_of(net),
            "components": components, "usedWeightSum": round(wsum, 4)}


# ════════════════════════════════════════════════════════════════════════════════
#  Integration — signed dispositions from the existing engines
# ════════════════════════════════════════════════════════════════════════════════
_NATURAL_BENEFIC = {"jupiter", "venus", "mercury"}
_NATURAL_MALEFIC = {"sun", "mars", "saturn", "rahu", "ketu"}
_KENDRA = {1, 4, 7, 10}
_TRIKONA = {1, 5, 9}
_DUSTHANA = {6, 8, 12}
_CHARA_ROLE = {"AmK": "amatya", "DK": "stree", "PK": "putra"}   # Jaimini role keys
# dignity state → additive magnitude nudge (uccha-bala already carried separately)
_DIGNITY_NUDGE = {"exalted": 0.20, "moolatrikona": 0.12, "own": 0.10,
                  "friend": 0.03, "neutral": 0.0, "enemy": -0.10, "debilitated": -0.30}


def _polarity(graha: str, nature: str | None, moon_waxing: bool) -> int:
    """+1 benefic / −1 malefic / 0 neutral — functional verdict first, natural fallback."""
    if nature in ("benefic", "yogakaraka"):
        return 1
    if nature == "malefic":
        return -1
    if nature in ("neutral", "mixed"):
        return 0
    if graha in _NATURAL_BENEFIC:                 # no text/derived verdict → natural
        return 1
    if graha == "moon":
        return 1 if moon_waxing else -1
    return -1


def _strength01(graha: str, sha: dict, dig: dict | None) -> float:
    """Magnitude in [0.05, 1] — ṣaḍbala ratio (≈1 = threshold) nudged by dignity."""
    e = sha.get(graha)
    s = min(1.0, e["ratio"] / 1.5) if (e and e.get("ratio") is not None) else 0.5
    if dig:
        s += _DIGNITY_NUDGE.get(dig.get("state"), 0.0)
    return max(0.05, min(1.0, s))


def _disposition(graha: str, nature: str | None, moon_waxing: bool,
                 sha: dict, dig: dict | None) -> float:
    """A graha's signed disposition ∈ [−1,+1] = polarity × strength."""
    return round(_polarity(graha, nature, moon_waxing) * _strength01(graha, sha, dig), 3)


def _state_label(dig: dict | None) -> str:
    return dig.get("state") if dig else "node"


def _varga_disp(graha: str, varga_sign: int, varga_lagna: int | None, polarity: int) -> float:
    """A graha's signed disposition IN a divisional chart — sign-based dignity plus
    placement from the varga-lagna. Value ∈ [−1,+1] = polarity × varga-strength. The
    varga gives only the SIGN, so dignity is by sign (own/exalt/friend/enemy/debil),
    not the degree-precise uccha-bala."""
    dig = dignity_of(graha, varga_sign * 30 + 15.0)          # None for nodes
    s = 0.40 + (_DIGNITY_NUDGE.get(dig.get("state"), 0.0) if dig else 0.0)
    if varga_lagna is not None:
        vb = (varga_sign - varga_lagna) % 12 + 1
        s += 0.12 if vb in (_KENDRA | _TRIKONA) else (-0.15 if vb in _DUSTHANA else 0.0)
    return round(polarity * max(0.05, min(1.0, s)), 3)


def _bhava_verdict(bh: dict, disp: dict, bhava_of: dict, dig_of: dict) -> dict:
    """One house → net iṣṭa/kaṣṭa from the four cited contributors."""
    house, lord, karaka = bh["house"], bh["lord"], bh.get("karaka")
    comps = []

    # lord (.40) — its disposition, modulated by where the lord itself sits
    place = bhava_of.get(lord)
    mod = 0.15 if place in (_KENDRA | _TRIKONA) else (-0.15 if place in _DUSTHANA else 0.0)
    lord_val = max(-1.0, min(1.0, disp.get(lord, 0.0) + mod))
    comps.append({"factor": "lord", "graha": lord, "value": round(lord_val, 3),
                  "weight": BHAVA_WEIGHTS["lord"],
                  "detail": f"{lord} ({_state_label(dig_of.get(lord))}), rules from house {place}",
                  "citation": (bh.get("lord_rule") or {}).get("citation") or "BPHS I ch.24",
                  "tier": "sloka"})

    # occupants (.25) — mean disposition; empty house drops out (renormalises)
    occ = bh.get("occupants") or []
    comps.append({"factor": "occupants", "grahas": occ,
                  "value": round(sum(disp[o] for o in occ) / len(occ), 3) if occ else None,
                  "weight": BHAVA_WEIGHTS["occupants"],
                  "detail": ", ".join(occ) if occ else "empty",
                  "citation": "BPHS I ch.24 (occupation)", "tier": "sloka"})

    # aspects-in (.20) — strength-weighted mean disposition of aspecting grahas
    asp = bh.get("aspects_in") or []
    if asp:
        den = sum(a["strength"] for a in asp) or 1.0
        num = sum(a["strength"] * disp.get(a["graha"], 0.0) for a in asp)
        aval = round(max(-1.0, min(1.0, num / den)), 3)
    else:
        aval = None
    comps.append({"factor": "aspects", "value": aval, "weight": BHAVA_WEIGHTS["aspects"],
                  "detail": ", ".join(f"{a['graha']}·{a['strength']}" for a in asp) if asp else "none",
                  "citation": "BPHS I ch.26 (dṛṣṭi)", "tier": "sloka"})

    # sthira-kāraka (.15)
    comps.append({"factor": "karaka", "graha": karaka,
                  "value": round(disp.get(karaka, 0.0), 3) if karaka else None,
                  "weight": BHAVA_WEIGHTS["karaka"], "detail": f"sthira kāraka {karaka}",
                  "citation": bh.get("karaka_citation") or "BPHS I ch.32", "tier": "sloka"})

    res = compose(comps)
    return {"house": house, "sign": bh["sign"], "lord": lord,
            "net": res["net"], "band": res["band"], "components": res["components"]}


def _theme_verdict(theme: dict, bhava_net: dict, disp: dict, chara_assign: dict,
                   yoga_names: list[str], yoga_families: set,
                   graha_vargas: dict, lagna_vargas: dict, pol: dict) -> dict:
    """One life-theme → net, blending its bhāvas + kārakas + signature yoga + the
    relevant divisional chart (varga)."""
    comps = []
    for h, w in theme.get("houses", {}).items():
        bn = bhava_net.get(h)
        comps.append({"factor": "bhava", "house": h,
                      "value": bn["net"] if bn else None, "weight": w,
                      "detail": f"house {h}" + (f" · {bn['band']}" if bn else ""),
                      "citation": "→ bhāva verdict", "tier": "synthesis"})
    for g, w in theme.get("sthira", {}).items():
        comps.append({"factor": "sthira_karaka", "graha": g, "value": disp.get(g),
                      "weight": w, "detail": f"sthira kāraka {g}",
                      "citation": "BPHS I ch.32", "tier": "sloka"})
    for role, w in theme.get("chara", {}).items():
        rk = _CHARA_ROLE.get(role)
        cand = chara_assign.get(rk) if rk else None
        g = cand[0] if cand else None
        comps.append({"factor": "chara_karaka", "role": role, "graha": g,
                      "value": disp.get(g) if g else None, "weight": w,
                      "detail": f"{role} = {g or '—'}",
                      "citation": "BPHS II (Jaimini chara kārakas)", "tier": "jaimini"})
    for slot, w in theme.get("yoga", {}).items():
        val, detail, tier = None, f"{slot}: absent", "sloka"
        if slot == "_varga":
            detail, tier = "varga slot (next phase)", "synthesis"
        else:
            subs = _YOGA_SLOT_MATCH.get(slot, (slot,))
            hit = any(any(s in nm for s in subs) for nm in yoga_names) or \
                  (slot == "raja" and "raja" in yoga_families)
            neg = slot in ("arishta", "balarishta")
            if hit:
                val, detail = (-0.6 if neg else 0.6), f"{slot}: present"
        comps.append({"factor": "yoga", "slot": slot, "value": val, "weight": w,
                      "detail": detail, "citation": "BPHS yoga chapters" if tier == "sloka" else "reserved (varga)",
                      "tier": tier})

    vg = theme.get("varga")
    if vg:
        Dxx, w = vg["chart"], vg["weight"]
        sigs = list(theme.get("sthira", {}))          # significators = kārakas + primary-house lord
        ph = max(theme["houses"], key=theme["houses"].get)
        plord = (bhava_net.get(ph) or {}).get("lord")
        if plord and plord not in sigs:
            sigs.append(plord)
        vlagna = (lagna_vargas or {}).get(Dxx)
        vals = [_varga_disp(s, (graha_vargas.get(s) or {})[Dxx], vlagna, pol.get(s, 0))
                for s in sigs if (graha_vargas.get(s) or {}).get(Dxx) is not None]
        comps.append({"factor": "varga", "chart": Dxx,
                      "value": round(sum(vals) / len(vals), 3) if vals else None, "weight": w,
                      "detail": f"{Dxx} · " + ", ".join(sigs),
                      "citation": "BPHS ṣoḍaśavarga (ch.6–7)", "tier": "sloka"})

    res = compose(comps)
    return {"key": theme["key"], "name": theme["name"], "net": res["net"],
            "band": res["band"], "components": res["components"],
            "weightsNote": "starting weights · synthesis tier"}


def build(chart) -> dict:
    """Assemble the per-chart domain matrix (v1: bhāva + kāraka) from a VedicChart."""
    grahas = chart.grahas
    lagna = chart.lagna_rasi
    lon_of = {g.key: g.longitude for g in grahas}
    bhava_of = {g.key: g.bhava for g in grahas}
    sun_lon, moon_lon = lon_of["sun"], lon_of["moon"]
    moon_waxing = ((moon_lon - sun_lon) % 360) < 180

    # strengths + dignities + functional natures
    sha = shadbala_context.shadbala_for_chart(chart).get("grahas", {})
    dig_of = {g.key: dignity_of(g.key, g.longitude) for g in grahas}
    prof = functional.lagna_profile(lagna, moon_waxing=moon_waxing)
    nature = {}
    for row in prof.get("grahas", []):
        gk = row.get("graha")
        if gk:
            nature[gk] = row.get("nature") or row.get("derived_nature")
    for gk in (prof.get("yogakarakas") or []):
        nature[gk] = "yogakaraka"

    disp = {g.key: _disposition(g.key, nature.get(g.key), moon_waxing, sha, dig_of.get(g.key))
            for g in grahas}
    pol = {g.key: _polarity(g.key, nature.get(g.key), moon_waxing) for g in grahas}

    # bhāva verdicts
    bh_out = bhp.bhava_phala({g.key: {"rasi": g.rasi} for g in grahas}, lagna)
    bhavas = [_bhava_verdict(bh, disp, bhava_of, dig_of) for bh in bh_out.get("bhavas", [])]
    bhava_net = {b["house"]: b for b in bhavas}

    # kārakas + yogas
    chara = kar.chara_karakas({g.key: g.longitude for g in grahas})
    chara_assign = chara.get("assignment", {})
    detected = yg.detect_yogas({g.key: {"rasi": g.rasi, "longitude": g.longitude, "vargas": g.vargas}
                                for g in grahas}, lagna,
                               lagna_d9=chart.lagna_vargas.get("D9"), shadbala={"grahas": sha}).get("detected", [])
    yoga_names = [e["name"].lower() for e in detected]
    yoga_families = {e.get("family") for e in detected}

    graha_vargas = {g.key: g.vargas for g in grahas}
    themes = [_theme_verdict(t, bhava_net, disp, chara_assign, yoga_names, yoga_families,
                             graha_vargas, chart.lagna_vargas, pol) for t in THEMES]

    # aspect web (graha dṛṣṭi) — directed graha→graha edges for the network graph
    dchart = drishti.graha_drishti_chart({g.key: g.rasi for g in grahas}, include_nodes=True)
    edges = []
    for src, dd in (dchart.get("casts") or {}).items():
        for tgt, frac in (dd.get("grahas") or {}).items():
            if frac and src != tgt:
                edges.append({"from": src, "to": tgt, "strength": round(frac, 2)})
    nodes = {g.key: {"longitude": round(g.longitude, 2), "rasi": g.rasi, "bhava": g.bhava,
                     "disp": disp[g.key], "polarity": pol[g.key], "retro": bool(g.retrograde),
                     "strength": round(sha[g.key]["ratio"], 2) if sha.get(g.key, {}).get("ratio") is not None else None,
                     "state": _state_label(dig_of.get(g.key))}
             for g in grahas}

    out = {
        "bhavas": bhavas,
        "themes": themes,
        "nodes": nodes,
        "edges": {"aspects": edges},
        "grahaDisposition": {g: {"disp": disp[g], "polarity": _polarity(g, nature.get(g), moon_waxing),
                                 "nature": nature.get(g), "state": _state_label(dig_of.get(g)),
                                 "shadbalaRatio": round(sha.get(g, {}).get("ratio"), 3) if sha.get(g, {}).get("ratio") is not None else None}
                             for g in disp},
        "karakas": {"chara": {r: (chara_assign.get(rk) or [None])[0] for r, rk in _CHARA_ROLE.items()},
                    "atmakaraka": chara.get("atmakaraka")},
        "yogas": [{"name": e["name"], "family": e.get("family")} for e in detected],
        "provenance": {"weights": "synthesis (starting values, tunable)",
                       "tiers": ["sloka", "jaimini", "synthesis"],
                       "note": "Indications from classical measures, weighted transparently — not a fated verdict."},
    }
    try:
        out["ashtakavarga"] = ashtakavarga.from_chart(chart)
    except Exception:
        out["ashtakavarga"] = None
    out["timeline"] = timeline(chart, out, _dt.date.today(), 36)
    try:
        out["changes"] = changes(chart, out)
    except Exception:
        out["changes"] = None
    try:
        _enrich_bhps(chart, out)
    except Exception:
        pass
    return out


# ════════════════════════════════════════════════════════════════════════════════
#  Timeline (Layer 3) — the near future: daśā activation + gochara over the domains
# ════════════════════════════════════════════════════════════════════════════════
_LEVEL_W = (0.5, 0.32, 0.18)   # mahā, antar, pratyantar activation weights


def _add_months(d: _dt.date, m: int) -> _dt.date:
    y = d.year + (d.month - 1 + m) // 12
    mo = (d.month - 1 + m) % 12 + 1
    return _dt.date(y, mo, min(d.day, 28))


def _transit_sign(jd: float, ipl: int) -> int:
    """Sidereal sign (0..11) of graha ``ipl`` at ``jd`` — for aṣṭakavarga gating."""
    return int(_norm360(swe.calc_ut(jd, ipl, CALC_FLAGS)[0][0]) // 30)


# ── the ensemble: independent timing clocks fused into a central estimate + band ──
# Weights are synthesis (starting values, tunable), like the bhāva/theme weights.
# Daśā .60 (the primary frameworks) / transit .40. Within the .40 transit budget the
# double-transit (trig) sits at parity with gochara (goch) — BUT trig's activation is
# convex in coverage (see c_trig), so a bare 1/3 double transit is muted and only a
# near-full triple-target transit reaches full strength. The .20 is thus compensatory,
# not an inflation of the clock's *net* influence: it converts trig's distribution from
# frequent-and-weak to rare-and-decisive, matching how śāstra treats the yoga.
_CLOCK_W = {"vims": 0.40, "goch": 0.20, "chara": 0.20, "trig": 0.20}
_CHARA_LVL = (0.6, 0.4)   # mahā / antar weight inside the chara clock
_SPREAD_FULL = 0.5        # spread at which conviction hits 0


def _chara_direction(chart) -> str | None:
    """Chara-daśā SEQUENCE direction. K.N. Rao's rule (following Neelakantha; the
    Jagannatha Hora default): the sequence runs DIRECT if the 9th sign from the lagna
    is *odd-footed* (savya), else REVERSE. 'Odd-footed' is the savya/apasavya quadrant
    grouping — ``charadasha.DIRECT_GROUP`` {Ar,Ta,Ge,Li,Sc,Sg} — NOT the ordinal sign
    number (the common error). Same author the length engine already cites; the rule
    reproduces the canonical 12-lagna direct/reverse list. Tier: jaimini, not BPHS."""
    ninth = (chart.lagna_rasi + 8) % 12
    return "direct" if ninth in charadasha.DIRECT_GROUP else "reverse"


def _chara_sequence(chart, direction):
    if direction not in ("direct", "reverse"):
        return None
    positions = {g.key: g.rasi for g in chart.grahas}
    degrees = {g.key: (g.longitude % 30.0) for g in chart.grahas}
    res = charadasha.chara_dasha(positions, degrees, lagna=chart.lagna_rasi, direction=direction)
    seq = res.get("sequence")
    if not seq:
        return None
    return {"seq": seq, "step": 1 if direction == "direct" else -1,
            "total": res["total_years"] or 0.0}


def _chara_running(cs, age_years):
    """(mahā_rasi, antar_rasi) of the chara daśā at ``age_years``, or (None, None)."""
    if not cs or cs["total"] <= 0:
        return None, None
    a = age_years % cs["total"]
    for e in cs["seq"]:
        if e["start_offset"] <= a < e["end_offset"]:
            L = e["years"]
            ai = max(0, min(11, int((a - e["start_offset"]) / (L / 12.0)))) if L > 0 else 0
            return e["sign"], (e["sign"] + cs["step"] * ai) % 12
    return None, None


def _fuse(clocks: dict):
    """Fuse clock activations (name→value, or None to abstain) into
    (central, spread, conviction). Inactive clocks vote 0 (an unconfirmed lone
    signal thus reads as disagreement → low conviction); abstainers are excluded."""
    items = [(n, v) for n, v in clocks.items() if v is not None]
    wsum = sum(_CLOCK_W[n] for n, _ in items)
    if wsum <= 0:
        return 0.0, 0.0, 0.5
    central = sum(_CLOCK_W[n] * v for n, v in items) / wsum
    spread = (sum(_CLOCK_W[n] * (v - central) ** 2 for n, v in items) / wsum) ** 0.5
    conviction = max(0.0, min(1.0, 1.0 - spread / _SPREAD_FULL))
    return central, spread, conviction


def _hits(transit_sign: int, target_sign: int, graha: str) -> bool:
    """A transiting graha 'hits' a sign — for the double-transit fructification rule —
    only by OCCUPYING it or casting a FULL aspect on it (Jupiter's 5/7/9, Saturn's
    3/7/10, and every graha's 7th — all drishti 1.0). The Parāśari ¼/½/¾ partial
    aspects are a strength device, not a transit influence, and are excluded here so
    the double-transit stays the strict, precise yoga it is classically meant to be."""
    return (transit_sign == target_sign
            or drishti.graha_drishti(transit_sign, target_sign, graha) >= 1.0 - 1e-9)


# Parāśari bhāva-kārakas (sthira) — the natural significator of each house.
_BHAVA_KARAKA = {1: "sun", 2: "jupiter", 3: "mars", 4: "moon", 5: "jupiter", 6: "mars",
                 7: "venus", 8: "saturn", 9: "jupiter", 10: "mercury", 11: "jupiter", 12: "saturn"}


def _dt_coverage(jup_s, sat_s, house, lagna, lord_key, graha_sign):
    """Full double-transit — the fraction of {the bhāva, its lord, its kāraka} that
    BOTH Jupiter and Saturn transit or aspect. 1.0 is the strict classical rule for a
    promised result to fructify; 2/3 partial; the bare house alone is 1/3."""
    targets = [(lagna + house - 1) % 12]                    # the bhāva sign
    if lord_key and lord_key in graha_sign:
        targets.append(graha_sign[lord_key])                # the bhāva lord's natal sign
    kar = _BHAVA_KARAKA.get(house)
    if kar and kar in graha_sign:
        targets.append(graha_sign[kar])                     # the bhāva kāraka's natal sign
    covered = sum(1 for t in targets
                  if _hits(jup_s, t, "jupiter") and _hits(sat_s, t, "saturn"))
    return covered / len(targets)


def timeline(chart, m_out: dict, start: _dt.date, months: int = 24) -> dict:
    """A dated near-future potential per theme + overall. At each month the running
    Viṁśottarī lords (mahā→antar→pratyantar) ACTIVATE the themes whose significators
    they are (kārakas + primary-house lord) — swinging the standing verdict by the
    lord's own disposition — and transiting Jupiter/Saturn over a theme's houses add
    a gochara nudge that is *aṣṭakavarga-gated*: the nudge is signed by the bindus the
    transiting graha holds in the sign it occupies (a bindu-rich transit supports, a
    bindu-poor one afflicts), not by a flat good/bad. An indication, not a fated event."""
    birth_jd = chart.jd_ut
    moon = next(g for g in chart.grahas if g.key == "moon")
    ni, nf = moon.nakshatra.index, moon.nakshatra.fraction
    lagna = chart.lagna_rasi
    disp = {k: v["disp"] for k, v in m_out["grahaDisposition"].items()}
    lord_of = {b["house"]: b["lord"] for b in m_out["bhavas"]}
    graha_sign = {g.key: g.rasi for g in chart.grahas}
    base = {t["key"]: t["net"] for t in m_out["themes"]}
    names = {t["key"]: t["name"] for t in m_out["themes"]}
    chara = (m_out.get("karakas") or {}).get("chara") or {}
    av = m_out.get("ashtakavarga") or {}
    bav, sav = av.get("bhinna"), av.get("sarva")
    bnet = {b["house"]: b["net"] for b in m_out["bhavas"]}   # Layer-2 bhāva verdicts
    chara_seq = _chara_sequence(chart, _chara_direction(chart))   # None ⇒ chara abstains

    sig, houses, primary = {}, {}, {}
    for t in THEMES:
        s = set(t.get("sthira", {}))
        for role in t.get("chara", {}):
            if chara.get(role):
                s.add(chara[role])
        ph = max(t["houses"], key=t["houses"].get)
        primary[t["key"]] = ph
        if lord_of.get(ph):
            s.add(lord_of[ph])
        sig[t["key"]] = s
        houses[t["key"]] = set(t["houses"])

    steps = []
    for m in range(months + 1):
        d = _add_months(start, m)
        jd = swe.julday(d.year, d.month, d.day, 12.0, swe.GREG_CAL)
        lords = running_lords(birth_jd, ni, nf, jd, depth=3)
        # transiting Jupiter/Saturn: sign (for AV gating) and house-from-lagna.
        jup_s = _transit_sign(jd, swe.JUPITER)
        sat_s = _transit_sign(jd, swe.SATURN)
        jup_h, sat_h = (jup_s - lagna) % 12 + 1, (sat_s - lagna) % 12 + 1
        jup_p = ashtakavarga.transit_potency("jupiter", jup_s, bav, sav) if bav else 0.6
        sat_p = ashtakavarga.transit_potency("saturn", sat_s, bav, sav) if bav else -0.6
        # chara (Jaimini) daśā rāśis running now (or None,None if the clock abstains)
        c_maha, c_antar = _chara_running(chara_seq, (jd - birth_jd) / 365.25)
        tv, tband, tconv, tclk = {}, {}, {}, {}
        for tk in sig:
            th = houses[tk]
            # clock 1 — Viṁśottarī: running lords that are the theme's significators.
            c_vims = max(-1.0, min(1.0, sum(_LEVEL_W[i] * disp.get(L, 0.0)
                                            for i, L in enumerate(lords) if L in sig[tk])))
            # clock 2 — aṣṭakavarga-gated gochara of Jupiter/Saturn over the theme's houses.
            gp = [jup_p] * (jup_h in th) + [sat_p] * (sat_h in th)
            c_goch = sum(gp) / len(gp) if gp else 0.0
            # clock 3 — chara daśā: its rāśi lands on a theme house → that bhāva's verdict.
            c_chara = None
            if c_maha is not None:
                c_chara = 0.0
                mh = (c_maha - lagna) % 12 + 1
                if mh in th:
                    c_chara += _CHARA_LVL[0] * bnet.get(mh, 0.0)
                ah = (c_antar - lagna) % 12 + 1
                if ah in th:
                    c_chara += _CHARA_LVL[1] * bnet.get(ah, 0.0)
            # clock 4 — double transit: Jup AND Sat over the bhāva, its lord and its
            # kāraka. Coverage is SQUARED (convex): a bare 1/3 house-only hit is muted
            # to ~0.11 and only a near-full triple-target transit speaks — the rare,
            # decisive confirmator of classical doctrine, not a frequent weak nudge.
            ph = primary[tk]
            cov = _dt_coverage(jup_s, sat_s, ph, lagna, lord_of.get(ph), graha_sign)
            c_trig = bnet.get(ph, 0.0) * cov * cov

            clocks = {"vims": c_vims, "goch": c_goch, "chara": c_chara, "trig": c_trig}
            central, spread, cf = _fuse(clocks)
            v = max(-1.0, min(1.0, 0.5 * base[tk] + 0.5 * central))
            tv[tk] = round(v, 3)
            tband[tk] = [round(max(-1.0, v - 0.5 * spread), 3), round(min(1.0, v + 0.5 * spread), 3)]
            tconv[tk] = round(cf, 2)
            tclk[tk] = {"vims": round(c_vims, 2), "goch": round(c_goch, 2),
                        "chara": (round(c_chara, 2) if c_chara is not None else None),
                        "trig": round(c_trig, 2)}
        ov = sum(tv.values()) / len(tv)
        steps.append({"date": d.isoformat(),
                      "maha": lords[0] if lords else None,
                      "antar": lords[1] if len(lords) > 1 else None,
                      "pratyantar": lords[2] if len(lords) > 2 else None,
                      "charaMaha": c_maha, "charaAntar": c_antar,
                      "overall": round(ov, 3),
                      "overallBand": [round(sum(b[0] for b in tband.values()) / len(tband), 3),
                                      round(sum(b[1] for b in tband.values()) / len(tband), 3)],
                      "overallCf": round(sum(tconv.values()) / len(tconv), 2),
                      "themes": tv, "bands": tband, "conv": tconv, "clocks": tclk})

    # flagged windows — contiguous runs where a theme is timing-driven notable, with
    # the conviction and the dominant clock at the peak recorded.
    def _driver(clk):
        best, name = -1.0, None
        for n, val in clk.items():
            if val is None:
                continue
            m = _CLOCK_W[n] * abs(val)
            if m > best:
                best, name = m, n
        return name

    windows = []
    for tk in sig:
        run = None
        for s in steps:
            v = s["themes"][tk]
            good = v >= 0
            # a *window* is timing-driven: notable AND moved from the standing base
            if abs(v) >= 0.28 and abs(v - base[tk]) >= 0.07:
                peak_fields = {"peak": v, "maha": s["maha"], "antar": s["antar"],
                               "cf": s["conv"][tk], "driver": _driver(s["clocks"][tk])}
                if run and run["good"] == good:
                    run["to"] = s["date"]
                    if abs(v) > abs(run["peak"]):
                        run.update(peak_fields)
                else:
                    if run:
                        windows.append(run)
                    ph = primary[tk]
                    run = {"key": tk, "name": names[tk], "good": good,
                           "from": s["date"], "to": s["date"],
                           "house": ph, "lord": lord_of.get(ph), **peak_fields}
            elif run:
                windows.append(run)
                run = None
        if run:
            windows.append(run)
    # type each window into an event: intensity = |peak| · conviction, ranked.
    for w in windows:
        w["intensity"] = round(abs(w["peak"]) * (w.get("cf") or 0.0), 3)
    windows.sort(key=lambda w: w["intensity"], reverse=True)
    # surface variety across life areas: at most 2 events per theme, up to 10 total.
    events, per = [], {}
    for w in windows:
        if per.get(w["key"], 0) >= 2:
            continue
        per[w["key"]] = per.get(w["key"], 0) + 1
        events.append(w)
        if len(events) >= 10:
            break

    return {"start": start.isoformat(), "months": months, "steps": steps,
            "themeOrder": [t["key"] for t in THEMES], "events": events,
            "clockWeights": _CLOCK_W, "charaDirection": _chara_direction(chart),
            "note": "Near-future indication from an ensemble of independent clocks — Viṁśottarī "
                    "daśā, aṣṭakavarga-gated Jupiter/Saturn gochara, Jaimini chara daśā (K.N. Rao "
                    "sequence-direction rule), and the Saturn–Jupiter double-transit trigger — fused "
                    "into a central value with a confidence band whose width is the clocks' "
                    "disagreement. An indication, not a fated event; chara is jaimini-tier, not BPHS."}


# ════════════════════════════════════════════════════════════════════════════════
#  Monte-Carlo (Layer 4) — birth-time uncertainty envelope + event survival
# ════════════════════════════════════════════════════════════════════════════════
def montecarlo(chart_fn, base_dt: _dt.datetime, minutes: float = 4.0, samples: int = 160) -> dict:
    """Birth-time uncertainty of the projection. The dominant real-world error is an
    imprecise birth time — a few minutes moves the lagna ~1° and shifts the daśā
    balance, most sharply near a cusp. Perturb the birth time by a Gaussian ±``minutes``
    and recompute the whole projection ``samples`` times; the scatter is a distinct,
    second uncertainty (separate from the clocks' disagreement band). Each base event
    gets a *survival* = the fraction of perturbed runs in which it still fires. Fixed
    seed ⇒ a given request reproduces. ``chart_fn(dt)`` builds a chart for a datetime."""
    samples = max(20, min(300, int(samples)))
    minutes = max(0.5, min(60.0, float(minutes)))
    rng = _random.Random(0x0DE7A5)
    sigma = minutes / 2.0

    base_tl = build(chart_fn(base_dt))["timeline"]
    base_lagna = chart_fn(base_dt).lagna_rasi
    base_dir, base_events = base_tl["charaDirection"], base_tl["events"]
    n = len(base_tl["steps"])
    curves = [[] for _ in range(n)]
    hits = [0] * len(base_events)
    lagna_same = dir_same = 0

    for _ in range(samples):
        off = max(-minutes * 1.8, min(minutes * 1.8, rng.gauss(0.0, sigma)))
        pc = chart_fn(base_dt + _dt.timedelta(minutes=off))
        ptl = build(pc)["timeline"]
        for i, s in enumerate(ptl["steps"]):
            curves[i].append(s["overall"])
        lagna_same += (pc.lagna_rasi == base_lagna)
        dir_same += (ptl["charaDirection"] == base_dir)
        pev = ptl["events"]
        for j, be in enumerate(base_events):
            if any(pe["key"] == be["key"] and pe["good"] == be["good"]
                   and pe["from"] <= be["to"] and be["from"] <= pe["to"] for pe in pev):
                hits[j] += 1

    def pctile(arr, p):
        a = sorted(arr)
        return a[min(len(a) - 1, max(0, int(round(p * (len(a) - 1)))))]

    envelope = [{"date": base_tl["steps"][i]["date"],
                 "p10": round(pctile(curves[i], 0.10), 3),
                 "p50": round(pctile(curves[i], 0.50), 3),
                 "p90": round(pctile(curves[i], 0.90), 3)} for i in range(n)]
    events = [dict(be, survival=round(hits[j] / samples, 2)) for j, be in enumerate(base_events)]
    return {"samples": samples, "minutes": minutes, "envelope": envelope, "events": events,
            "lagnaStability": round(lagna_same / samples, 2),
            "charaDirStability": round(dir_same / samples, 2),
            "note": f"Birth-time uncertainty: the projection recomputed over a Gaussian ±{minutes:g} "
                    "min of birth time. The envelope is the p10–p90 spread of the overall curve; each "
                    "event's survival is how often it still fires. Low lagna stability ⇒ the reading "
                    "is sensitive to the exact birth time (rectification would help)."}


# ════════════════════════════════════════════════════════════════════════════════
#  Shared single-date evaluator — the ensemble at ONE moment (used by backtest; the
#  timeline loop mirrors this exact math, guarded by a parity test).
# ════════════════════════════════════════════════════════════════════════════════
def _projection_context(chart, m_out: dict) -> dict:
    """Precompute everything the per-date ensemble needs, once per chart."""
    moon = next(g for g in chart.grahas if g.key == "moon")
    lord_of = {b["house"]: b["lord"] for b in m_out["bhavas"]}
    bnet = {b["house"]: b["net"] for b in m_out["bhavas"]}
    disp = {k: v["disp"] for k, v in m_out["grahaDisposition"].items()}
    base = {t["key"]: t["net"] for t in m_out["themes"]}
    chara = (m_out.get("karakas") or {}).get("chara") or {}
    av = m_out.get("ashtakavarga") or {}
    sig, houses, primary = {}, {}, {}
    for t in THEMES:
        s = set(t.get("sthira", {}))
        for role in t.get("chara", {}):
            if chara.get(role):
                s.add(chara[role])
        ph = max(t["houses"], key=t["houses"].get)
        primary[t["key"]] = ph
        if lord_of.get(ph):
            s.add(lord_of[ph])
        sig[t["key"]] = s
        houses[t["key"]] = set(t["houses"])
    return {"birth_jd": chart.jd_ut, "ni": moon.nakshatra.index, "nf": moon.nakshatra.fraction,
            "lagna": chart.lagna_rasi, "disp": disp, "bnet": bnet, "base": base,
            "sig": sig, "houses": houses, "primary": primary, "lord_of": lord_of,
            "graha_sign": {g.key: g.rasi for g in chart.grahas},
            "bav": av.get("bhinna"), "sav": av.get("sarva"),
            "chara_seq": _chara_sequence(chart, _chara_direction(chart))}


def _project_at(jd: float, ctx: dict) -> dict:
    """The 4-clock ensemble at a single moment. Returns step meta + per-theme
    {v, central, spread, cf, clocks}. This is the same computation the timeline loop
    runs per month (test_matrix_ensemble asserts the two agree)."""
    lagna, bav, sav = ctx["lagna"], ctx["bav"], ctx["sav"]
    lords = running_lords(ctx["birth_jd"], ctx["ni"], ctx["nf"], jd, depth=3)
    jup_s, sat_s = _transit_sign(jd, swe.JUPITER), _transit_sign(jd, swe.SATURN)
    jup_h, sat_h = (jup_s - lagna) % 12 + 1, (sat_s - lagna) % 12 + 1
    jup_p = ashtakavarga.transit_potency("jupiter", jup_s, bav, sav) if bav else 0.6
    sat_p = ashtakavarga.transit_potency("saturn", sat_s, bav, sav) if bav else -0.6
    c_maha, c_antar = _chara_running(ctx["chara_seq"], (jd - ctx["birth_jd"]) / 365.25)
    themes = {}
    for tk in ctx["sig"]:
        th = ctx["houses"][tk]
        c_vims = max(-1.0, min(1.0, sum(_LEVEL_W[i] * ctx["disp"].get(L, 0.0)
                                        for i, L in enumerate(lords) if L in ctx["sig"][tk])))
        gp = [jup_p] * (jup_h in th) + [sat_p] * (sat_h in th)
        c_goch = sum(gp) / len(gp) if gp else 0.0
        c_chara = None
        if c_maha is not None:
            c_chara = 0.0
            mh = (c_maha - lagna) % 12 + 1
            if mh in th:
                c_chara += _CHARA_LVL[0] * ctx["bnet"].get(mh, 0.0)
            ah = (c_antar - lagna) % 12 + 1
            if ah in th:
                c_chara += _CHARA_LVL[1] * ctx["bnet"].get(ah, 0.0)
        ph = ctx["primary"][tk]
        cov = _dt_coverage(jup_s, sat_s, ph, lagna, ctx["lord_of"].get(ph), ctx["graha_sign"])
        c_trig = ctx["bnet"].get(ph, 0.0) * cov * cov      # convex — see the timeline clock 4
        clocks = {"vims": c_vims, "goch": c_goch, "chara": c_chara, "trig": c_trig}
        central, spread, cf = _fuse(clocks)
        v = max(-1.0, min(1.0, 0.5 * ctx["base"][tk] + 0.5 * central))
        themes[tk] = {"v": round(v, 3), "central": round(central, 3),
                      "spread": round(spread, 3), "cf": round(cf, 2), "clocks": clocks}
    return {"maha": lords[0] if lords else None, "antar": lords[1] if len(lords) > 1 else None,
            "charaMaha": c_maha, "charaAntar": c_antar, "themes": themes}


# ════════════════════════════════════════════════════════════════════════════════
#  Backtest (Layer 5) — calibrate against the user's own known life events
# ════════════════════════════════════════════════════════════════════════════════
def backtest(chart, m_out: dict, events: list) -> dict:
    """For each event the user logged — a life-area (theme key), a month, and whether
    it went well (+1) or badly (−1) — compute the projection value the engine would
    have shown for that theme at that date, and whether its sign matched. Yields a
    personal hit-rate: a track record, not a claim of proof."""
    ctx = _projection_context(chart, m_out)
    results, hits, dsum, tsum, thits, scored = [], 0, 0.0, 0.0, 0, 0
    for ev in events:
        key = ev.get("key")
        if key not in ctx["sig"]:
            continue
        pol = 1 if (ev.get("polarity", 1) or 0) >= 0 else -1
        m = str(ev.get("date", ""))
        try:
            y, mo = int(m[:4]), int(m[5:7])
            jd = swe.julday(y, mo, 15, 12.0, swe.GREG_CAL)
        except (ValueError, IndexError):
            continue
        pj = _project_at(jd, ctx)["themes"].get(key)
        if not pj:
            continue
        v, central = pj["v"], pj["central"]
        hit = (v * pol) > 0
        hits += int(hit)
        thits += int((central * pol) > 0)
        dsum += pol * v
        tsum += pol * central
        scored += 1
        results.append({"date": m, "key": key, "polarity": pol, "v": v,
                        "central": central, "hit": bool(hit)})
    summary = {"n": scored,
               "hitRate": round(hits / scored, 2) if scored else None,
               "timingHitRate": round(thits / scored, 2) if scored else None,
               "meanDirectional": round(dsum / scored, 3) if scored else None,
               "meanTimingDirectional": round(tsum / scored, 3) if scored else None}
    return {"events": results, "summary": summary,
            "note": "Backtest: for each event you logged, the projection value the engine would have "
                    "shown for that life-area at that date, and whether its sign matched what happened. "
                    "A personal, honest track record — indication, not proof; a small sample is only a hint."}


# ════════════════════════════════════════════════════════════════════════════════
#  Change engine (Layer 6) — transitions, not levels: daśā junction + transit
#  ingress + sharp swing, typed into changes across the three motives.
# ════════════════════════════════════════════════════════════════════════════════
_TRIGGER_PLANETS = {"mars": swe.MARS, "jupiter": swe.JUPITER, "saturn": swe.SATURN, "rahu": swe.MEAN_NODE}
_SWING_THRESH = 0.22
_CHANGES_NOTE = ("Projected *changes* — where a life-area is about to turn, from daśā junctions, "
                 "slow-transit ingresses and sharp swings landing on its significators. A window and "
                 "a direction, never a fated event or a date. The ♥ care-signals are indications to be "
                 "present and communicate — never verdicts about another person or a mortality forecast.")

# Each signature: houses + kārakas (its significators), the transit planets whose ingress
# triggers it, which detectors apply, and how direction reads. mode: pos/neg (fixed
# direction, gated by the driver's disposition) · shift (a move) · bi (up/down by driver)
# · care (reframed, opt-in). theme = the timeline theme used for swing + conviction.
CHANGE_SIGS = [
    # ── Health (theme "health") ──
    {"key": "health.vitality", "motive": "health", "theme": "health", "houses": [1], "karakas": ["sun"],
     "planets": ["jupiter"], "triggers": ["junction", "ingress"], "mode": "pos", "tier": "sloka",
     "labels": {"up": "Vitality & recovery"}, "note": "energy returns — a good time to build habits"},
    {"key": "health.chronic", "motive": "health", "theme": "health", "houses": [6, 8], "karakas": ["saturn"],
     "planets": ["saturn"], "triggers": ["junction", "ingress", "doubletransit"], "mode": "neg", "tier": "sloka",
     "labels": {"down": "Chronic load / fatigue"}, "note": "lifestyle caution: rest and pacing"},
    {"key": "health.acute", "motive": "health", "theme": "health", "houses": [6, 8], "karakas": ["mars"],
     "planets": ["mars"], "triggers": ["ingress"], "mode": "neg", "tier": "sloka",
     "labels": {"down": "Acute / accident-prone"}, "note": "physical caution: injury, inflammation, surgery"},
    {"key": "health.murky", "motive": "health", "theme": "health", "houses": [1, 6], "karakas": ["rahu", "ketu"],
     "planets": ["rahu", "ketu"], "triggers": ["ingress"], "mode": "neg", "tier": "synthesis",
     "labels": {"down": "Unexplained / murky"}, "note": "worth a check-up — hidden strain"},
    # ── Wealth (theme "wealth") ──
    {"key": "wealth.rise", "motive": "wealth", "theme": "wealth", "houses": [11, 2], "karakas": ["jupiter"],
     "planets": ["jupiter"], "triggers": ["junction", "ingress", "swing", "doubletransit"], "mode": "pos", "tier": "sloka",
     "labels": {"up": "Income rise"}, "note": "earnings trending up"},
    {"key": "wealth.windfall", "motive": "wealth", "theme": "wealth", "houses": [8, 11], "karakas": ["rahu", "jupiter"],
     "planets": ["rahu", "jupiter"], "triggers": ["ingress"], "mode": "pos", "tier": "synthesis",
     "labels": {"up": "Sudden gain / windfall"}, "note": "an unexpected jump — don't overextend on it"},
    {"key": "wealth.drain", "motive": "wealth", "theme": "wealth", "houses": [12, 8, 6], "karakas": ["saturn"],
     "planets": ["saturn", "mars"], "triggers": ["junction", "ingress", "swing", "doubletransit"], "mode": "neg", "tier": "sloka",
     "labels": {"down": "Expense / loss / debt"}, "note": "hold reserves — an outflow period"},
    # ── Career (theme "career") ──
    {"key": "career.promotion", "motive": "career", "theme": "career", "houses": [10], "karakas": ["sun"],
     "planets": ["jupiter"], "triggers": ["junction", "ingress", "doubletransit"], "mode": "pos", "tier": "sloka",
     "labels": {"up": "Promotion / recognition"}, "note": "status on the rise"},
    {"key": "career.jobloss", "motive": "career", "theme": "career", "houses": [10, 6], "karakas": ["saturn"],
     "planets": ["saturn"], "triggers": ["junction", "ingress", "swing", "doubletransit"], "mode": "neg", "tier": "sloka",
     "labels": {"down": "Job-loss risk"}, "note": "secure your position; keep a fallback"},
    {"key": "career.jobchange", "motive": "career", "theme": "career", "houses": [10, 6], "karakas": ["saturn", "mercury"],
     "planets": [], "triggers": ["junction", "doubletransit"], "mode": "shift", "tier": "synthesis",
     "labels": {"shift": "Job change (a move)"}, "note": "a lateral move is likely — not a loss"},
    {"key": "career.transition", "motive": "career", "theme": "career", "houses": [10], "karakas": ["rahu"],
     "planets": ["rahu"], "triggers": ["ingress", "junction"], "mode": "shift", "tier": "synthesis",
     "labels": {"shift": "Career transition (new field)"}, "note": "reinvention — a new direction opens"},
    # ── Relationships ──
    {"key": "rel.newbond", "motive": "rel", "theme": "marriage", "houses": [7, 5], "karakas": ["venus"],
     "planets": ["jupiter"], "triggers": ["junction", "ingress", "doubletransit"], "mode": "pos", "tier": "sloka",
     "labels": {"up": "New bond / commitment"}, "note": "a beginning — openness helps"},
    {"key": "rel.strain", "motive": "rel", "theme": "marriage", "houses": [7], "karakas": ["saturn"],
     "planets": ["saturn", "rahu"], "triggers": ["junction", "ingress", "swing", "doubletransit"], "mode": "neg", "tier": "sloka",
     "labels": {"down": "Strain / separation risk"}, "note": "a rough patch — tend it with patience"},
    {"key": "rel.trust", "motive": "rel", "theme": "marriage", "houses": [7, 12], "karakas": ["venus", "rahu"],
     "planets": ["rahu"], "triggers": ["ingress"], "mode": "care", "tier": "synthesis", "care": True,
     "labels": {"care": "Trust & openness"}, "note": "a period to nurture trust and communicate openly"},
    {"key": "rel.social", "motive": "rel", "theme": "enemies", "houses": [6, 11], "karakas": ["saturn", "mercury"],
     "planets": ["saturn", "jupiter"], "triggers": ["junction", "ingress"], "mode": "bi", "tier": "sloka",
     "labels": {"up": "Allies & support", "down": "Rivalry / friction — guard against betrayal"},
     "note": "the people around you are shifting"},
    {"key": "rel.family", "motive": "rel", "theme": "home", "houses": [2, 4, 9], "karakas": ["moon", "jupiter"],
     "planets": ["jupiter", "saturn"], "triggers": ["junction", "ingress"], "mode": "bi", "tier": "sloka",
     "labels": {"up": "Family warmth", "down": "Family friction / distance"}, "note": "the family climate is shifting"},
    {"key": "rel.gain", "motive": "rel", "theme": "children", "houses": [11, 5], "karakas": ["jupiter"],
     "planets": ["jupiter"], "triggers": ["junction", "ingress", "doubletransit"], "mode": "pos", "tier": "synthesis",
     "labels": {"up": "A new person / gain"}, "note": "a new bond or arrival"},
    {"key": "rel.tender", "motive": "rel", "theme": "longevity", "houses": [8], "karakas": ["saturn"],
     "planets": ["saturn", "ketu"], "triggers": ["ingress"], "mode": "care", "tier": "synthesis", "care": True,
     "labels": {"care": "A tender period for a loved one"}, "note": "cherish and attend — a time to be present"},
]

_MOTIVE_GROUP = {"health": "health", "wealth": "wealthCareer", "career": "wealthCareer", "rel": "relationships"}


def _months_between(a: str, b: str) -> int:
    ay, am = int(a[:4]), int(a[5:7])
    by, bm = int(b[:4]), int(b[5:7])
    return abs((by - ay) * 12 + (bm - am))


def _dedupe_changes(raw: list) -> list:
    """Merge same-signature fires within 3 months into one window; rank by conviction."""
    out = []
    for e in sorted(raw, key=lambda x: x["date"]):
        if out and out[-1]["key"] == e["key"] and _months_between(out[-1]["to"], e["date"]) <= 3:
            g = out[-1]
            g["to"] = e["date"]
            if e["cf"] > g["cf"]:
                g.update(cf=e["cf"], direction=e["direction"], label=e["label"],
                         trigger=e["trigger"], maha=e["maha"], antar=e["antar"])
        else:
            out.append(dict(e, **{"from": e["date"], "to": e["date"]}))
    return sorted(out, key=lambda x: x["cf"], reverse=True)


def changes(chart, m_out: dict) -> dict:
    """Detect typed change-windows over the projection horizon, grouped by motive."""
    steps = (m_out.get("timeline") or {}).get("steps") or []
    out = {"health": [], "wealthCareer": [], "relationships": []}
    if len(steps) < 2:
        return {**out, "note": _CHANGES_NOTE}
    lagna = chart.lagna_rasi
    lord_of = {b["house"]: b["lord"] for b in m_out["bhavas"]}
    graha_sign = {g.key: g.rasi for g in chart.grahas}
    disp = {k: v["disp"] for k, v in m_out["grahaDisposition"].items()}

    tsigns = []
    for s in steps:
        y, mo, d = (int(x) for x in s["date"].split("-"))
        jd = swe.julday(y, mo, d, 12.0, swe.GREG_CAL)
        row = {pk: _transit_sign(jd, ipl) for pk, ipl in _TRIGGER_PLANETS.items()}
        row["ketu"] = (row["rahu"] + 6) % 12
        tsigns.append(row)

    for sig in CHANGE_SIGS:
        sigset = set(sig.get("karakas", []))
        for h in sig["houses"]:
            if lord_of.get(h):
                sigset.add(lord_of[h])
        theme = sig.get("theme")
        raw = []
        for i in range(1, len(steps)):
            trigs, driver = [], None
            if "junction" in sig["triggers"]:
                for lvl, key in (("mahā", "maha"), ("antar", "antar")):
                    a, b = steps[i][key], steps[i - 1][key]
                    if a != b and (a in sigset or b in sigset):
                        trigs.append(f"{lvl}-daśā change")
                        driver = a if a in sigset else b
                        break
            if "ingress" in sig["triggers"]:
                for pk in sig.get("planets", []):
                    if tsigns[i][pk] != tsigns[i - 1][pk] and ((tsigns[i][pk] - lagna) % 12 + 1) in sig["houses"]:
                        trigs.append(f"{pk} transit")
                        driver = driver or pk
            if "swing" in sig["triggers"] and theme:
                k = min(3, i)
                if abs(steps[i]["themes"].get(theme, 0.0) - steps[i - k]["themes"].get(theme, 0.0)) >= _SWING_THRESH:
                    trigs.append("sharp swing")
            if "doubletransit" in sig["triggers"]:
                # Jup AND Sat both over the bhāva, its lord and its kāraka (Saravali's
                # fructification rule) — fired on the RISING edge, when the yoga forms.
                for h in sig["houses"]:
                    lk = lord_of.get(h)
                    now = _dt_coverage(tsigns[i]["jupiter"], tsigns[i]["saturn"], h, lagna, lk, graha_sign)
                    if now >= 2 / 3 - 1e-9:
                        prev = _dt_coverage(tsigns[i - 1]["jupiter"], tsigns[i - 1]["saturn"], h, lagna, lk, graha_sign)
                        if prev < 2 / 3 - 1e-9:
                            trigs.append("Jupiter–Saturn double transit")
                            driver = driver or lk or (sig.get("karakas") or [None])[0]
                            break
            if not trigs:
                continue
            dd = disp.get(driver, 0.0) if driver else 0.0
            if abs(dd) < 1e-9 and theme:
                dd = steps[i]["themes"].get(theme, 0.0)
            mode = sig["mode"]
            if mode == "pos":
                if dd <= 0.02:
                    continue
                direction = "up"
            elif mode == "neg":
                if dd >= -0.02:
                    continue
                direction = "down"
            elif mode == "shift":
                direction = "shift"
            elif mode == "care":
                direction = "care"
            else:  # bi
                direction = "up" if dd > 0.02 else "down" if dd < -0.02 else None
                if direction is None:
                    continue
            label = sig["labels"].get(direction) or sig["key"]
            tt = ("junction" if "daśā" in trigs[0] else "swing" if "swing" in trigs[0]
                  else "doubletransit" if "double transit" in trigs[0] else "ingress")
            cf = 0.4 + 0.12 * (len(trigs) - 1) + 0.22 * min(1.0, abs(dd))
            if theme:
                cf = 0.5 * cf + 0.5 * steps[i]["conv"].get(theme, 0.6)
            raw.append({"date": steps[i]["date"], "key": sig["key"], "direction": direction, "label": label,
                        "note": sig.get("note"), "cf": round(max(0.35, min(0.92, cf)), 2),
                        "trigger": trigs[0], "triggerType": tt,
                        "maha": steps[i]["maha"], "antar": steps[i]["antar"],
                        "care": sig.get("care", False), "tier": sig.get("tier", "synthesis")})
        for e in _dedupe_changes(raw)[:2]:
            out[_MOTIVE_GROUP[sig["motive"]]].append(e)
    for g in ("health", "wealthCareer", "relationships"):
        out[g].sort(key=lambda e: e["date"])
    return {**out, "note": _CHANGES_NOTE}


# ════════════════════════════════════════════════════════════════════════════════
#  Life arc (Layer 7) — the whole trajectory from birth across the three motives,
#  with the yogas that marked turning points.
# ════════════════════════════════════════════════════════════════════════════════
# Each life-facet is a transparent blend of the standing themes evaluated over life.
_FACETS = {
    "wealthEarned":   {"career": 0.5, "wealth": 0.5},                 # self-earned
    "wealthReceived": {"fortune": 0.5, "home": 0.3, "wealth": 0.2},   # inherited / given / fortune
    "healthPhysical": {"health": 0.5, "self": 0.3, "longevity": 0.2},
    "healthMental":   {"self": 0.5, "home": 0.3, "education": 0.2},   # mind + peace of home + intellect
    "relFamily":      {"home": 0.4, "fortune": 0.3, "children": 0.3},
    "relOthers":      {"marriage": 0.5, "enemies": 0.3, "foreign": 0.2},
}
_ASPECTS = {"wealth": ["wealthEarned", "wealthReceived"],
            "health": ["healthPhysical", "healthMental"],
            "relationships": ["relFamily", "relOthers"]}
_MAHAPURUSHA_PLANET = {"ruchaka": "mars", "bhadra": "mercury", "hamsa": "jupiter",
                       "malavya": "venus", "sasa": "saturn", "shasha": "saturn"}


def _life_turning_points(points: list, m_out: dict, ribbon: list) -> list:
    """Notable local peaks/troughs of the life curve + mahāpuruṣa-yoga activations."""
    if not points:
        return []
    ov = [p["overall"] for p in points]
    W = 3
    turns = []
    for i, p in enumerate(points):
        win = ov[max(0, i - W): min(len(ov), i + W + 1)]
        v = ov[i]
        # a *relative* rise/fall — prominence over the local window, not an absolute
        # level (a life can turn up while still below its overall mean).
        peak = v == max(win) and (v - min(win)) >= 0.07
        trough = v == min(win) and (max(win) - v) >= 0.07
        if peak or trough:
            fk = (max if peak else min)(p["facets"], key=lambda k: p["facets"][k])
            turns.append({"year": p["year"], "age": p["age"], "kind": "curve",
                          "direction": "rise" if peak else "hard", "maha": p["maha"],
                          "facet": fk, "value": v})
    # thin adjacent same-direction extrema (keep the sharper one)
    thinned = []
    for t in turns:
        if thinned and thinned[-1]["direction"] == t["direction"] and t["age"] - thinned[-1]["age"] <= 4:
            if abs(t["value"]) > abs(thinned[-1]["value"]):
                thinned[-1] = t
        else:
            thinned.append(t)
    # mahāpuruṣa yogas → their planet's mahādaśā is the activation window
    for y in (m_out.get("yogas") or []):
        pl = _MAHAPURUSHA_PLANET.get(str(y.get("name", "")).lower().split()[0])
        if not pl:
            continue
        seg = next((r for r in ribbon if r["lord"] == pl), None)
        if seg:
            thinned.append({"year": seg["from"], "toYear": seg["to"], "kind": "yoga",
                            "direction": "yoga", "maha": pl, "yoga": y.get("name"),
                            "family": y.get("family")})
    thinned.sort(key=lambda t: t["year"])
    return thinned[:14]


def lifearc(chart, m_out: dict, extra_years: int = 3) -> dict:
    """The person's arc from birth: yearly values for six life-facets (wealth earned/
    received · health physical/mental · relationships family/others), the mahādaśā
    ribbon across life, and the turning points. Reuses the shared date-evaluator."""
    ctx = _projection_context(chart, m_out)
    moon = next(g for g in chart.grahas if g.key == "moon")
    ni, nf = moon.nakshatra.index, moon.nakshatra.fraction
    by, bm, bd = swe.revjul(chart.jd_ut, swe.GREG_CAL)[:3]
    end_year = _dt.date.today().year + max(0, extra_years)

    points = []
    for yr in range(int(by), end_year + 1):
        jd = swe.julday(yr, 6, 15, 12.0, swe.GREG_CAL)
        if jd < chart.jd_ut:
            jd = chart.jd_ut
        pj = _project_at(jd, ctx)["themes"]
        facets = {fk: round(sum(pj[t]["v"] * w for t, w in blend.items()), 3)
                  for fk, blend in _FACETS.items()}
        lords = running_lords(chart.jd_ut, ni, nf, jd, depth=1)
        points.append({"year": yr, "age": yr - int(by), "maha": lords[0] if lords else None,
                       "overall": round(sum(facets.values()) / len(facets), 3), "facets": facets})

    ribbon = []
    for p in points:
        if ribbon and ribbon[-1]["lord"] == p["maha"]:
            ribbon[-1]["to"] = p["year"]
        else:
            ribbon.append({"lord": p["maha"], "from": p["year"], "to": p["year"]})

    return {"birthYear": int(by), "nowYear": _dt.date.today().year, "points": points,
            "ribbon": ribbon, "aspects": _ASPECTS, "facets": list(_FACETS),
            "turningPoints": _life_turning_points(points, m_out, ribbon),
            "note": "Life arc: each facet is a transparent blend of the standing themes evaluated "
                    "year by year as the daśā and transits move over the chart. A broad shape of "
                    "the life, an indication — not a record of events; the past is read the same "
                    "way the future is projected."}


# ════════════════════════════════════════════════════════════════════════════════
#  BPHS specifics — attach each period's fired antardaśā results (ch.52-60) to the
#  events & changes, theme-matched, so a label like "Promotion" carries the actual
#  cited classical prediction ("gain of position, favour of the king, conveyances…").
# ════════════════════════════════════════════════════════════════════════════════
_THEME_KW = {
    "self": ["happiness", "health", "body", "comfort", "honour", "strength", "fame", "mind"],
    "wealth": ["wealth", "riches", "money", "gold", "prosperity", "affluence", "treasure",
               "cattle", "income", "gain of", "financial", "fortune"],
    "career": ["position", "king", "government", "authority", "office", "status", "dignity",
               "master", "command", "business", "kingdom", "ruler", "rank", "fame", "honour",
               "promotion", "profession", "livelihood", "occupation", "work", "service", "trade"],
    "marriage": ["wife", "spouse", "marriage", "conjugal", "husband", "woman"],
    "children": ["children", "child", "progeny", "son", "daughter", "birth", "issue"],
    "health": ["disease", "illness", "fever", "sickness", "affliction", "danger", "injury",
               "ailment", "pain", "death"],
    "education": ["learning", "knowledge", "education", "wisdom", "scholar", "study", "intellect",
                  "skill", "science", "mantra"],
    "home": ["house", "home", "land", "property", "mother", "residence", "domestic",
             "conveyance", "vehicle", "comfort"],
    "fortune": ["fortune", "dharma", "religion", "father", "preceptor", "virtue", "charity",
                "pilgrimage", "righteous", "worship", "god"],
    "enemies": ["enemy", "enemies", "quarrel", "dispute", "litigation", "debt", "opponent",
                "loss", "theft", "imprisonment", "obstacle", "rival"],
    "foreign": ["foreign", "travel", "journey", "abroad", "distant", "pilgrimage", "wandering"],
    "longevity": ["death", "danger", "longevity", "end", "fatal", "life"],
}


def _fired_results(maha, antar, positions, lagna, cache):
    """The fired antardaśā conditions for (mahā, antar) — each a specific BPHS result
    string + its citation. Cached per pair (many events share a period)."""
    key = (maha, antar)
    if key not in cache:
        fired = []
        try:
            cell = antardasa.evaluate_cell(maha, antar, positions=positions, lagna=lagna)
            for c in cell.get("conditions", []):
                if c.get("state") == "fired" and c.get("results"):
                    fired.append({"text": " ".join(str(c["results"]).split()),
                                  "cite": cell.get("chapter") or "BPHS ch.52-60",
                                  "tier": c.get("source") or "sloka"})
        except Exception:
            pass
        cache[key] = fired
    return cache[key]


_BHPS_POS = ("gain", "happiness", "opulence", "acquisition", "glory", "prosperity", "success",
             "birth", "reverence", "fortune", "pleasure", "comfort", "honour", "auspicious",
             "wealth", "increase", "enjoyment", "favour", "good", "profit", "elevation")
_BHPS_NEG = ("loss", "danger", "quarrel", "disease", "debt", "theft", "destruction", "fear",
             "death", "enmity", "obstacle", "suffering", "grief", "illness", "misery", "poverty",
             "separation", "trouble", "evil", "difficulty", "anxiety", "downfall", "sorrow", "distress")


def _kw_score(text_low, kws):
    """Keyword hits by WHOLE WORD (so 'king' doesn't match 'seeking'); multi-word
    keywords match as a phrase."""
    words = _re.findall(r"[a-z]+", text_low)
    wset = set(words)
    n = 0
    for k in kws:
        if " " in k:
            n += text_low.count(k)
        elif k in wset:
            n += words.count(k)
    return n


def _valence(t):
    p = _kw_score(t, _BHPS_POS)
    n = _kw_score(t, _BHPS_NEG)
    return (p > n) - (p < n)   # +1 favourable · 0 mixed · −1 unfavourable


def _facet_clauses(text, theme):
    """Keep only the comma/semicolon-separated clauses that mention the theme, so a
    career line drops 'happiness from wife and children' and keeps 'favour of the
    king'. Falls back to the whole text if filtering leaves too little."""
    kws = _THEME_KW.get(theme, [])
    if not kws:
        return text
    parts = [p.strip() for p in text.replace(";", ",").split(",") if p.strip()]
    keep = [p for p in parts if _kw_score(p.lower(), kws)]
    joined = ", ".join(keep)
    return joined if len(joined) >= 20 else text


def _trim(txt):
    if len(txt) > 220:
        cut = txt.rfind(", ", 120, 220)
        txt = (txt[:cut] if cut > 0 else txt[:220]).rstrip(", ") + "…"
    return txt


def _pick_bhps(fired, theme, want_pos):
    """The fired antardaśā result that both mentions the theme AND agrees with the
    event's direction (``want_pos`` True/False, or None = either), narrowed to the
    theme-relevant clauses. None if no fired result is both relevant and consistent."""
    if not fired:
        return None
    kws = _THEME_KW.get(theme, [])
    cands = []
    for f in fired:
        t = f["text"].lower()
        ts = _kw_score(t, kws)
        if ts == 0:
            continue                                  # not about this theme
        val = _valence(t)
        if want_pos is not None and val != 0 and (val > 0) != want_pos:
            continue                                  # contradicts the event's direction
        cands.append((ts, f))
    if not cands:
        return None
    best = max(cands, key=lambda x: x[0])[1]
    return {"text": _trim(_facet_clauses(best["text"], theme)),
            "cite": best["cite"], "tier": best["tier"], "kind": "period"}


def _gist_core(gist):
    """Strip the concordance framing ('X reads a native with graha in the Nth bhava
    as …', the 'not any prediction' hedge) to the effect itself."""
    t = str(gist)
    i = t.find(" bhava as ")
    if i >= 0:
        t = t[i + len(" bhava as "):]
    t = t.split(" — in the text")[0].split(", not any prediction")[0]
    t = t.replace("the text also reads", "").strip(" ;,.")
    return " ".join(t.split())


# Moralistic / degrading terms — NOT general negativity (a difficult placement should
# still read as difficult), just the gratuitously judgmental framing to avoid.
_PEJORATIVE = ("degradation", "downfall", "wicked", "wickedness", "evil", "sinful", "sinner",
               "vile", "vices", "immoral", "cruel", "despicable", "shameless", "wretched",
               "disgrace", "disgraceful", "dishonour", "dishonourable", "adulterous", "adultery",
               "prostitute", "thief", "thieving", "wrongdoing", "intoxicants", "intoxicant",
               "debauched", "licentious", "lewd", "contemptible", "villain", "ruined", "doomed",
               "cursed", "torture", "torment", "tortures", "deceitful", "treacherous", "foolish",
               "idiot", "stupid", "ugly", "deformed", "despised", "hated", "criminal", "vulgar",
               "miserable", "wandering", "quarrelsome", "vain", "sinning", "odious", "indolent",
               "insulted", "immoral", "gluttonous", "greedy", "cheat", "cheating", "hateful")
# Tie-break: the gentler-toned texts first, Chamatkāra (the harshest) last.
_SOURCE_ORDER = {"saravali": 0, "phaladipika": 1, "brihat_jataka": 2, "chamatkara": 3}
# At/above this many moralistic words, a lone occupant reading yields to the lord effect.
_HARSH_MAX = 2


def _harshness(gist):
    return _kw_score(str(gist).lower(), _PEJORATIVE)


def _occupant_effects(chart, lagna):
    """Classical planet-in-house reading for each occupied house — a planet sitting IN
    a house speaks to it more directly than the house-lord's placement. Where a cell
    has several sources, take the LEAST pejorative-toned one (same reading, gentler
    framing), not the rosiest — a hard placement should still read as hard."""
    out = {}
    try:
        readings = classical.build({g.key: {"rasi": g.rasi} for g in chart.grahas}, lagna).get("house_readings", [])
        for r in readings:
            srcs = [s for s in (r.get("sources") or []) if _gist_core(s.get("gist"))]
            if not srcs or r["house"] in out:
                continue
            s = min(srcs, key=lambda x: (_harshness(x.get("gist")),
                                         _SOURCE_ORDER.get((x.get("source") or {}).get("id"), 5)))
            out[r["house"]] = {"text": _gist_core(s.get("gist")), "cite": s.get("citation") or "classical",
                               "tier": "classical", "kind": "occupant", "graha": r["graha"],
                               "harsh": _harshness(s.get("gist"))}
    except Exception:
        pass
    return out


def _house_effects(chart, lagna):
    """Dense per-house BPHS effect (the lord's placement result) — always available,
    the 'what this life-area holds' fallback when no antardaśā condition fires."""
    out = {}
    try:
        bp = bhp.bhava_phala({g.key: {"rasi": g.rasi} for g in chart.grahas}, lagna)
        for b in bp.get("bhavas", []):
            lr = b.get("lord_rule") or {}
            eff = lr.get("effect")
            if eff:
                sig = ((b.get("significations") or {}).get("text") or "")
                # keep just the governed-domains list (before "are to be understood…")
                sig = " ".join(sig.split(":", 1)[-1].split(" are to be ")[0].split())
                out[b["house"]] = {"text": " ".join(str(eff).split()),
                                   "sig": sig, "cite": lr.get("citation") or "BPHS",
                                   "tier": "sloka", "kind": "house"}
    except Exception:
        pass
    return out


def _enrich_bhps(chart, out):
    positions = {g.key: g.rasi for g in chart.grahas}
    lagna = chart.lagna_rasi
    cache = {}
    tl = out.get("timeline") or {}
    sig_theme = {s["key"]: s.get("theme") for s in CHANGE_SIGS}
    sig_house = {s["key"]: s["houses"][0] for s in CHANGE_SIGS}
    house_fx = _house_effects(chart, lagna)

    occ_fx = _occupant_effects(chart, lagna)

    def place_bhps(house, theme):
        # a planet occupying the house reads it more directly than the lord's placement —
        # but if the only occupant source is heavily moralistic, yield to the gentler
        # lord effect rather than surface a harsh lone reading.
        occ, lord = occ_fx.get(house), house_fx.get(house)
        src = lord if (occ and occ.get("harsh", 0) >= _HARSH_MAX and lord) else (occ or lord)
        if not src:
            return None
        eff = _facet_clauses(src["text"], theme)
        # if the effect isn't facet-worded, lead with the house's own domain terms.
        sig = (house_fx.get(house) or {}).get("sig", "")
        dom = _facet_clauses(sig, theme)
        if eff == src["text"] and dom and dom != sig and len(dom) < 90:
            eff = f"{dom} — {eff}"
        return {**src, "text": _trim(eff)}

    # (a) inline BPHS on each event/change: the direction-consistent antardaśā result if
    # one fires, else the primary house's occupant / lord effect — narrowed to the facet.
    for e in tl.get("events", []):
        b = _pick_bhps(_fired_results(e.get("maha"), e.get("antar"), positions, lagna, cache),
                       e.get("key"), bool(e.get("good"))) or place_bhps(e.get("house"), e.get("key"))
        if b:
            e["bhps"] = b
    for grp in ("health", "wealthCareer", "relationships"):
        for e in (out.get("changes") or {}).get(grp, []):
            theme = sig_theme.get(e.get("key"), "self")
            d = e.get("direction")
            want = True if d == "up" else False if d == "down" else None
            b = _pick_bhps(_fired_results(e.get("maha"), e.get("antar"), positions, lagna, cache),
                           theme, want) or place_bhps(sig_house.get(e.get("key")), theme)
            if b:
                e["bhps"] = b

    # (b) the full antardaśā reading, period by period over the horizon — the specific
    # cited classical text, always available whether or not it maps to a timing event.
    periods = []
    for s in tl.get("steps", []):
        k = (s["maha"], s["antar"])
        if periods and periods[-1]["_k"] == k:
            periods[-1]["to"] = s["date"]
        else:
            periods.append({"_k": k, "maha": s["maha"], "antar": s["antar"],
                            "from": s["date"], "to": s["date"]})
    for p in periods:
        seen, results = set(), []
        for f in _fired_results(p["maha"], p["antar"], positions, lagna, cache):
            t = f["text"]
            if not t or "as above" in t.lower() or t[:40] in seen:
                continue
            seen.add(t[:40])
            results.append({"text": (t[:280] + "…") if len(t) > 280 else t, "cite": f["cite"]})
        p["results"] = results[:3]
        del p["_k"]
    tl["periods"] = periods
