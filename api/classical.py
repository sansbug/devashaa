"""
Classical-tier readings served as a cited concordance (docs/classical-sources-policy.md).

PILOT: Sārāvalī's Sun-in-sign (ch.22). Each placement carries a list of `sources`;
each source is a cited, adaptation-classified GIST — a rendering, never a reproduction
of the copyrighted translation — on the `classical` provenance tier, NEVER blended with
BPHS. The list shape is deliberate: adding Jātaka Pārijāta / Bṛhat Jātaka later appends
another entry to `sources`, turning each placement into a genuine multi-source concordance.
"""
import saravali_rules as sv

_NOTE = (
    "Readings from classical texts other than BPHS, on their own provenance tier and "
    "never blended with Parāśara. Each line is a cited, dated rendering — not a fated "
    "prediction — adapted per our historical-material policy: caste verdicts are dropped, "
    "gendered judgements about a spouse are refused, disease is kept only as the text's "
    "own dated view (not medical advice), and archaic referents (kings, etc.) are glossed."
)


def _sun_reading(sign: int) -> dict | None:
    entry = sv.SUN_IN_SIGN.get(sign)
    if not entry:
        return None
    return {
        "graha": "sun",
        "sign": sign,
        "sources": [{
            "source": sv.SOURCE,
            "citation": entry["citation"],
            "gist": entry["gist"],
            "adaptation": entry["adaptation"],
            "confidence": entry["confidence"],
        }],
    }


def build(positions: dict) -> dict:
    """`positions` maps graha key -> {"rasi": int, ...}. Returns the classical
    concordance for the placements we have extracted so far. PILOT: the Sun's rāśi."""
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
        "coverage": "Pilot — Sārāvalī, Sun in the rāśis (ch.22).",
    }
