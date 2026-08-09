"""
Classical-tier readings served as a cited concordance (docs/classical-sources-policy.md).

Planet-in-sign concordance: for each graha the chart places, every registered classical
source that has an extracted reading for that (graha, rāśi) contributes one cited,
adaptation-classified GIST — a rendering, never a reproduction — on the `classical`
provenance tier, NEVER blended with BPHS or with each other. Each placement's `sources`
list IS the concordance.

A source module exposes SOURCE plus either IN_SIGN = {graha_key: {sign: entry}} (the
general form) or the legacy SUN_IN_SIGN = {sign: entry} (Sun only). Hindi gists live in a
sibling `*_hi` module (GIST_HI = {graha: {sign: hi}}); `lang='hi'` swaps them in per
string, falling back to English wherever a translation is missing.
"""
import saravali_rules as sv

_SOURCES = [sv]
_HI = {}        # source id -> {graha: {sign: hi_gist}}
_ADAPT_HI = {}  # source id -> {graha: {sign: {action, note}}} (badge popover metadata)
try:
    import saravali_rules_hi
    _HI["saravali"] = saravali_rules_hi.GIST_HI
    _ADAPT_HI["saravali"] = getattr(saravali_rules_hi, "ADAPT_HI", {})
except Exception:  # noqa: BLE001
    pass
try:
    import brihat_jataka_rules as bj
    _SOURCES.append(bj)
except Exception:  # noqa: BLE001
    pass
try:
    import brihat_jataka_rules_hi
    _HI["brihat_jataka"] = brihat_jataka_rules_hi.GIST_HI
    _ADAPT_HI["brihat_jataka"] = getattr(brihat_jataka_rules_hi, "ADAPT_HI", {})
except Exception:  # noqa: BLE001
    pass

# Classical order; the nodes (Rāhu/Ketu) carry no graha-in-sign phala in these texts.
GRAHA_ORDER = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"]

_NOTE = {
    "en": (
        "Readings from classical texts other than BPHS, on their own provenance tier and "
        "never blended with Parāśara. Each line is a cited, dated rendering — not a fated "
        "prediction — adapted per our historical-material policy: caste verdicts are dropped, "
        "gendered judgements are neutralised or refused, disease/poverty are kept only as the "
        "text's own dated view (not advice), and archaic referents (kings, etc.) are glossed."
    ),
    "hi": (
        "बीपीएचएस से इतर शास्त्रीय ग्रंथों के पाठ — अपने पृथक् उद्गम-स्तर पर, पराशर के साथ कभी "
        "नहीं मिलाए गए। प्रत्येक पंक्ति एक उद्धृत, तिथि-सहित प्रस्तुति है, कोई नियति-कथन नहीं; हमारी "
        "ऐतिहासिक-सामग्री नीति के अनुसार अनुकूलित: जाति-निर्णय हटाए गए, लैंगिक निर्णय तटस्थ किए गए "
        "या अस्वीकृत, रोग/दरिद्रता केवल ग्रंथ के तत्कालीन मत के रूप में रखे गए (सलाह नहीं), और "
        "पुरातन संदर्भ (राजा आदि) की व्याख्या दी गई।"
    ),
}
_COVERAGE = {
    "en": "Grahas in the rāśis — Sārāvalī (Sun/Moon/Mars/Mercury) + Bṛhat Jātaka (all seven).",
    "hi": "राशियों में ग्रह — सारावली (सूर्य/चन्द्र/मङ्गल/बुध) + बृहत् जातक (सातों)।",
}


def _in_sign_map(module) -> dict:
    """A module's {graha: {sign: entry}} table, tolerating the legacy Sun-only form."""
    m = getattr(module, "IN_SIGN", None)
    if m is not None:
        return m
    return {"sun": getattr(module, "SUN_IN_SIGN", {})}


# Adaptation content-classes collapse to the six §5 tags the UI badge knows
# (docs/classical-sources-policy.md §5). Anything else is not a dated-content class
# and is dropped, so the badge only ever shows a recognised label.
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


def _source_reading(module, graha: str, sign: int, lang: str) -> dict | None:
    entry = _in_sign_map(module).get(graha, {}).get(sign)
    if not entry:
        return None
    gist = entry["gist"]
    adapt = dict(entry["adaptation"])
    if lang == "hi":
        sid = module.SOURCE["id"]
        hi = _HI.get(sid, {}).get(graha, {}).get(sign)
        if hi:
            gist = hi
        ah = _ADAPT_HI.get(sid, {}).get(graha, {}).get(sign)
        if ah:
            if ah.get("action"):
                adapt["action"] = ah["action"]
            if ah.get("note"):
                adapt["note"] = ah["note"]
    adapt["classes"] = _norm_classes(adapt.get("classes"))
    return {
        "source": module.SOURCE,
        "citation": entry["citation"],
        "gist": gist,
        "adaptation": adapt,
        "confidence": entry["confidence"],
    }


def build(positions: dict, lang: str = "en") -> dict:
    """`positions` maps graha key -> {"rasi": int, ...}. Returns the classical
    concordance: one reading per graha we have extracted, each with a `sources` list.
    ``lang='hi'`` serves the Hindi gist/note where available (English fallback)."""
    readings = []
    for g in GRAHA_ORDER:
        p = positions.get(g)
        if p is None:
            continue
        sign = p["rasi"]
        sources = [r for m in _SOURCES if (r := _source_reading(m, g, sign, lang))]
        if sources:
            readings.append({"graha": g, "sign": sign, "sources": sources})
    return {
        "readings": readings,
        "note": _NOTE.get(lang, _NOTE["en"]),
        "policy": "docs/classical-sources-policy.md",
        "coverage": _COVERAGE.get(lang, _COVERAGE["en"]),
    }
