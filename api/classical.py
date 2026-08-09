"""
Classical-tier readings served as a cited concordance (docs/classical-sources-policy.md).

Sun-in-sign concordance: for the Sun's rāśi, every registered classical source that
has an extracted reading contributes one cited, adaptation-classified GIST — a
rendering, never a reproduction — on the `classical` provenance tier, NEVER blended
with BPHS. Each placement's `sources` list IS the concordance; adding a text just
appends another entry.
"""
import saravali_rules as sv

# Registered Sun-in-sign sources, in display order. Each is a module exposing
# SOURCE + SUN_IN_SIGN. Import defensively so a not-yet-populated source never
# breaks the chart.
_SOURCES = [sv]
try:
    import brihat_jataka_rules as bj
    _SOURCES.append(bj)
except Exception:  # noqa: BLE001
    pass

_NOTE = (
    "Readings from classical texts other than BPHS, on their own provenance tier and "
    "never blended with Parāśara. Each line is a cited, dated rendering — not a fated "
    "prediction — adapted per our historical-material policy: caste verdicts are dropped, "
    "gendered judgements about a spouse are refused, disease is kept only as the text's "
    "own dated view (not medical advice), and archaic referents (kings, etc.) are glossed."
)


def _source_reading(module, sign: int) -> dict | None:
    entry = getattr(module, "SUN_IN_SIGN", {}).get(sign)
    if not entry:
        return None
    return {
        "source": module.SOURCE,
        "citation": entry["citation"],
        "gist": entry["gist"],
        "adaptation": entry["adaptation"],
        "confidence": entry["confidence"],
    }


def _sun_reading(sign: int) -> dict | None:
    sources = [r for m in _SOURCES if (r := _source_reading(m, sign))]
    if not sources:
        return None
    return {"graha": "sun", "sign": sign, "sources": sources}


def build(positions: dict) -> dict:
    """`positions` maps graha key -> {"rasi": int, ...}. Returns the classical
    concordance for the placements we have extracted. Pilot: the Sun's rāśi."""
    readings = []
    sun = positions.get("sun")
    if sun is not None:
        r = _sun_reading(sun["rasi"])
        if r:
            readings.append(r)
    return {
        "readings": readings,
        "note": _NOTE,
        "policy": "docs/classical-sources-policy.md",
        "coverage": "Sun in the rāśis — Sārāvalī (ch.22) + Bṛhat Jātaka (ch.18).",
    }
