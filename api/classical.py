"""
Classical-tier readings served as a cited concordance (docs/classical-sources-policy.md).

Planet-in-sign concordance: for each graha the chart places, every registered classical
source that has an extracted reading for that (graha, rāśi) contributes one cited,
adaptation-classified GIST — a rendering, never a reproduction — on the `classical`
provenance tier, NEVER blended with BPHS or with each other. Each placement's `sources`
list IS the concordance.

A source module exposes SOURCE plus either IN_SIGN = {graha_key: {sign: entry}} (the
general form) or the legacy SUN_IN_SIGN = {sign: entry} (Sun only).
"""
import saravali_rules as sv

_SOURCES = [sv]
try:
    import brihat_jataka_rules as bj
    _SOURCES.append(bj)
except Exception:  # noqa: BLE001
    pass

# Classical order; the nodes (Rāhu/Ketu) carry no graha-in-sign phala in these texts.
GRAHA_ORDER = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"]

_NOTE = (
    "Readings from classical texts other than BPHS, on their own provenance tier and "
    "never blended with Parāśara. Each line is a cited, dated rendering — not a fated "
    "prediction — adapted per our historical-material policy: caste verdicts are dropped, "
    "gendered judgements are neutralised or refused, disease/poverty are kept only as the "
    "text's own dated view (not advice), and archaic referents (kings, etc.) are glossed."
)


def _in_sign_map(module) -> dict:
    """A module's {graha: {sign: entry}} table, tolerating the legacy Sun-only form."""
    m = getattr(module, "IN_SIGN", None)
    if m is not None:
        return m
    return {"sun": getattr(module, "SUN_IN_SIGN", {})}


# Adaptation content-classes collapse to the six §5 tags the UI badge knows
# (docs/classical-sources-policy.md §5). Anything else (e.g. "else", "offspring",
# "clean") is not a dated-content class and is dropped, so the badge only ever
# shows a recognised label.
_CLASS_CANON = {
    "caste": "caste",
    "gender": "gender", "gender/marriage": "gender", "gender-marriage": "gender",
    "gender & marriage": "gender",
    "slavery": "slavery", "slavery/servitude": "slavery", "slavery-servitude": "slavery",
    "slavery/servitude/rank": "slavery", "slavery/rank": "slavery", "servitude": "slavery",
    "servitude/rank": "slavery",
    "occupation": "occupation", "occupation-status": "occupation",
    "occupation/commerce": "occupation",
    "health": "health", "disease": "health", "death/disease": "health",
    "poverty": "health", "death/disease/poverty": "health", "death-disease-poverty": "health",
    "archaic": "archaic", "archaic-referent": "archaic",
}


def _norm_classes(classes) -> list:
    out = []
    for c in classes or []:
        v = _CLASS_CANON.get(str(c).strip().lower())
        if v and v not in out:
            out.append(v)
    return out


def _source_reading(module, graha: str, sign: int) -> dict | None:
    entry = _in_sign_map(module).get(graha, {}).get(sign)
    if not entry:
        return None
    adapt = dict(entry["adaptation"])
    adapt["classes"] = _norm_classes(adapt.get("classes"))
    return {
        "source": module.SOURCE,
        "citation": entry["citation"],
        "gist": entry["gist"],
        "adaptation": adapt,
        "confidence": entry["confidence"],
    }


def build(positions: dict) -> dict:
    """`positions` maps graha key -> {"rasi": int, ...}. Returns the classical
    concordance: one reading per graha we have extracted, each with a `sources` list."""
    readings = []
    for g in GRAHA_ORDER:
        p = positions.get(g)
        if p is None:
            continue
        sign = p["rasi"]
        sources = [r for m in _SOURCES if (r := _source_reading(m, g, sign))]
        if sources:
            readings.append({"graha": g, "sign": sign, "sources": sources})
    return {
        "readings": readings,
        "note": _NOTE,
        "policy": "docs/classical-sources-policy.md",
        "coverage": "Grahas in the rāśis — Sārāvalī (Sun) + Bṛhat Jātaka (all seven).",
    }
