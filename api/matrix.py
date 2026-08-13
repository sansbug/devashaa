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

import swisseph as swe

import ashtakavarga
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
    base = {t["key"]: t["net"] for t in m_out["themes"]}
    names = {t["key"]: t["name"] for t in m_out["themes"]}
    chara = (m_out.get("karakas") or {}).get("chara") or {}
    av = m_out.get("ashtakavarga") or {}
    bav, sav = av.get("bhinna"), av.get("sarva")

    sig, houses = {}, {}
    for t in THEMES:
        s = set(t.get("sthira", {}))
        for role in t.get("chara", {}):
            if chara.get(role):
                s.add(chara[role])
        ph = max(t["houses"], key=t["houses"].get)
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
        jup_p = ashtakavarga.transit_potency("jupiter", jup_s, bav, sav) if bav else 1.0
        sat_p = ashtakavarga.transit_potency("saturn", sat_s, bav, sav) if bav else -1.0
        tv = {}
        for tk in sig:
            act = sum(_LEVEL_W[i] * disp.get(L, 0.0) for i, L in enumerate(lords) if L in sig[tk])
            goch = 0.0
            if jup_h in houses[tk]:
                goch += 0.14 * jup_p
            if sat_h in houses[tk]:
                goch += 0.14 * sat_p
            v = (0.5 * base[tk] + 0.5 * act + goch) if (act or goch) else base[tk]
            tv[tk] = round(max(-1.0, min(1.0, v)), 3)
        steps.append({"date": d.isoformat(),
                      "maha": lords[0] if lords else None,
                      "antar": lords[1] if len(lords) > 1 else None,
                      "pratyantar": lords[2] if len(lords) > 2 else None,
                      "overall": round(sum(tv.values()) / len(tv), 3), "themes": tv})

    # flagged windows — contiguous runs where a theme is notably good/bad (|v|≥.33)
    windows = []
    for tk in sig:
        run = None
        for s in steps:
            v = s["themes"][tk]
            good = v >= 0
            # a *window* is timing-driven: notable AND moved from the standing base
            if abs(v) >= 0.28 and abs(v - base[tk]) >= 0.07:
                if run and run["good"] == good:
                    run["to"] = s["date"]
                    if abs(v) > abs(run["peak"]):
                        run.update(peak=v, maha=s["maha"], antar=s["antar"])
                else:
                    if run:
                        windows.append(run)
                    run = {"key": tk, "name": names[tk], "good": good, "from": s["date"],
                           "to": s["date"], "peak": v, "maha": s["maha"], "antar": s["antar"]}
            elif run:
                windows.append(run)
                run = None
        if run:
            windows.append(run)
    windows.sort(key=lambda w: abs(w["peak"]), reverse=True)

    return {"start": start.isoformat(), "months": months, "steps": steps,
            "themeOrder": [t["key"] for t in THEMES], "windows": windows[:12],
            "note": "Near-future indication: the running daśā activates a theme's significators, "
                    "swung by their disposition; Jupiter/Saturn transits nudge. Not a fated event."}
