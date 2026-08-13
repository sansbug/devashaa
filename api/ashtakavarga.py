"""Aṣṭakavarga — the transit-scoring bindu system (Parāśari / prastāra).

Builds on ``gochara.py``, which deliberately stops at transit GEOMETRY and leaves
the result-doctrine to "a separate, source-cited layer not yet built". This is that
layer's quantitative core: each graha's *bhinnāṣṭakavarga* (benefic bindus per sign,
0..8) and the *sarvāṣṭakavarga* (their sum per sign, 0..56), from the classical
benefic-house tables (BPHS Aṣṭakavarga adhyāya). The bindu count of the sign a graha
transits is the classical measure of that transit's potency — a graha through a
bindu-rich sign supports, through a bindu-poor sign afflicts — which is what lets the
matrix timeline grade a transit instead of guessing "Jupiter good, Saturn bad".

The tables are FIXED classical data, not a model. Two independent checksums guard
them: each graha's total across the twelve signs is invariant

    Sun 48 · Moon 49 · Mars 39 · Mercury 54 · Jupiter 56 · Venus 52 · Saturn 39

and their sum is the sarva total 337. ``verify_tables()`` asserts both; the test
module runs it. Rāhu/Ketu carry no aṣṭakavarga in the standard Parāśari system, so
only the seven grahas participate (as both contributors and reference points), the
Lagna joining them as the eighth reference point.
"""

from __future__ import annotations

# The seven contributing grahas (nodes carry no aṣṭakavarga in Parāśara).
PLANETS = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn")
# The eight reference points a bindu is counted from: the seven grahas + the Lagna.
REFS = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn", "lagna")

# Invariant per-graha totals (checksum); their sum is the sarvāṣṭakavarga total.
CANONICAL_TOTALS = {"sun": 48, "moon": 49, "mars": 39, "mercury": 54,
                    "jupiter": 56, "venus": 52, "saturn": 39}
SARVA_TOTAL = 337

# BENEFIC_HOUSES[graha][ref] = houses (1..12, counted from the ref point's own sign
# as house 1) in which `graha` contributes one benefic bindu. Standard Parāśari
# bhinnāṣṭakavarga tables (BPHS Aṣṭakavarga adhyāya).
BENEFIC_HOUSES: dict[str, dict[str, list[int]]] = {
    "sun": {
        "sun":     [1, 2, 4, 7, 8, 9, 10, 11],
        "moon":    [3, 6, 10, 11],
        "mars":    [1, 2, 4, 7, 8, 9, 10, 11],
        "mercury": [3, 5, 6, 9, 10, 11, 12],
        "jupiter": [5, 6, 9, 11],
        "venus":   [6, 7, 12],
        "saturn":  [1, 2, 4, 7, 8, 9, 10, 11],
        "lagna":   [3, 4, 6, 10, 11, 12],
    },
    "moon": {
        "sun":     [3, 6, 7, 8, 10, 11],
        "moon":    [1, 3, 6, 7, 10, 11],
        "mars":    [2, 3, 5, 6, 9, 10, 11],
        "mercury": [1, 3, 4, 5, 7, 8, 10, 11],
        "jupiter": [1, 4, 7, 8, 10, 11, 12],
        "venus":   [3, 4, 5, 7, 9, 10, 11],
        "saturn":  [3, 5, 6, 11],
        "lagna":   [3, 6, 10, 11],
    },
    "mars": {
        "sun":     [3, 5, 6, 10, 11],
        "moon":    [3, 6, 11],
        "mars":    [1, 2, 4, 7, 8, 10, 11],
        "mercury": [3, 5, 6, 11],
        "jupiter": [6, 10, 11, 12],
        "venus":   [6, 8, 11, 12],
        "saturn":  [1, 4, 7, 8, 9, 10, 11],
        "lagna":   [1, 3, 6, 10, 11],
    },
    "mercury": {
        "sun":     [5, 6, 9, 11, 12],
        "moon":    [2, 4, 6, 8, 10, 11],
        "mars":    [1, 2, 4, 7, 8, 9, 10, 11],
        "mercury": [1, 3, 5, 6, 9, 10, 11, 12],
        "jupiter": [6, 8, 11, 12],
        "venus":   [1, 2, 3, 4, 5, 8, 9, 11],
        "saturn":  [1, 2, 4, 7, 8, 9, 10, 11],
        "lagna":   [1, 2, 4, 6, 8, 10, 11],
    },
    "jupiter": {
        "sun":     [1, 2, 3, 4, 7, 8, 9, 10, 11],
        "moon":    [2, 5, 7, 9, 11],
        "mars":    [1, 2, 4, 7, 8, 10, 11],
        "mercury": [1, 2, 4, 5, 6, 9, 10, 11],
        "jupiter": [1, 2, 3, 4, 7, 8, 10, 11],
        "venus":   [2, 5, 6, 9, 10, 11],
        "saturn":  [3, 5, 6, 12],
        "lagna":   [1, 2, 4, 5, 6, 7, 9, 10, 11],
    },
    "venus": {
        "sun":     [8, 11, 12],
        "moon":    [1, 2, 3, 4, 5, 8, 9, 11, 12],
        "mars":    [3, 5, 6, 9, 11, 12],
        "mercury": [3, 5, 6, 9, 11],
        "jupiter": [5, 8, 9, 10, 11],
        "venus":   [1, 2, 3, 4, 5, 8, 9, 10, 11],
        "saturn":  [3, 4, 5, 8, 9, 10, 11],
        "lagna":   [1, 2, 3, 4, 5, 8, 9, 11],
    },
    "saturn": {
        "sun":     [1, 2, 4, 7, 8, 10, 11],
        "moon":    [3, 6, 11],
        "mars":    [3, 5, 6, 10, 11, 12],
        "mercury": [6, 8, 9, 10, 11, 12],
        "jupiter": [5, 6, 11, 12],
        "venus":   [6, 11, 12],
        "saturn":  [3, 5, 6, 11],
        "lagna":   [1, 3, 4, 6, 10, 11],
    },
}

# SAV midpoint = 337 / 12 signs ≈ 28.08 — the neutral bindu level a sign carries.
_SAV_MID = SARVA_TOTAL / 12.0
_BAV_MID = 4.0   # bhinna midpoint (0..8)


def verify_tables() -> bool:
    """Assert the two classical checksums. Raises AssertionError on any mismatch."""
    for p in PLANETS:
        # every cell is a valid, de-duplicated set of houses in 1..12
        for r in REFS:
            hs = BENEFIC_HOUSES[p][r]
            assert all(1 <= h <= 12 for h in hs), f"{p}/{r}: house out of range"
            assert len(hs) == len(set(hs)), f"{p}/{r}: duplicate house"
        total = sum(len(BENEFIC_HOUSES[p][r]) for r in REFS)
        assert total == CANONICAL_TOTALS[p], f"{p} total {total} != {CANONICAL_TOTALS[p]}"
    assert sum(CANONICAL_TOTALS.values()) == SARVA_TOTAL
    return True


def bhinna(graha_signs: dict[str, int], lagna_sign: int) -> dict[str, list[int]]:
    """Bhinnāṣṭakavarga: for each graha, its bindus in each of the 12 signs.

    ``graha_signs`` maps the seven planet keys to their natal sign index (0..11);
    ``lagna_sign`` is the lagna's sign index. Returns ``{graha: [b0..b11]}`` where
    each entry is 0..8. A graha earns a bindu in sign S from reference R when S is
    one of ``BENEFIC_HOUSES[graha][R]`` counted from R's own sign.
    """
    ref_sign = {r: graha_signs[r] for r in PLANETS}
    ref_sign["lagna"] = lagna_sign
    out: dict[str, list[int]] = {}
    for p in PLANETS:
        bins = [0] * 12
        for r in REFS:
            sr = ref_sign[r]
            for h in BENEFIC_HOUSES[p][r]:
                bins[(sr + h - 1) % 12] += 1
        out[p] = bins
    return out


def sarva(bav: dict[str, list[int]]) -> list[int]:
    """Sarvāṣṭakavarga: the per-sign sum of the seven bhinna charts (each 0..56)."""
    return [sum(bav[p][s] for p in PLANETS) for s in range(12)]


def from_chart(chart) -> dict:
    """Compute the aṣṭakavarga of a natal chart.

    Returns ``{"bhinna": {graha: [12]}, "sarva": [12], "planetTotals": {graha: int},
    "sarvaTotal": 337}`` — the bindu maps that grade every subsequent transit.
    """
    signs = {g.key: g.rasi for g in chart.grahas if g.key in PLANETS}
    if len(signs) != len(PLANETS):
        missing = [p for p in PLANETS if p not in signs]
        raise ValueError(f"chart missing grahas for aṣṭakavarga: {missing}")
    bav = bhinna(signs, chart.lagna_rasi)
    sav = sarva(bav)
    return {
        "bhinna": bav,
        "sarva": sav,
        "planetTotals": {p: sum(bav[p]) for p in PLANETS},
        "sarvaTotal": sum(sav),
    }


def transit_potency(planet: str, sign: int, bav: dict[str, list[int]], sav: list[int]) -> float:
    """Signed potency ∈ [−1, +1] of ``planet`` transiting ``sign`` (0..11).

    The classical aṣṭakavarga transit reading: a graha's transit is favourable
    through a bindu-rich sign and unfavourable through a bindu-poor one — governed
    by the graha's OWN bhinna bindus there and the sign's sarva total, independent
    of the graha's natural benefic/malefic nature. Both are centred on their neutral
    level and averaged, so ~4 own-bindus / ~28 sarva reads as 0.
    """
    zb = (bav[planet][sign] - _BAV_MID) / _BAV_MID          # own bindus, centred
    zs = (sav[sign] - _SAV_MID) / (_SAV_MID / 2.0)           # sign sarva, centred
    v = 0.5 * zb + 0.5 * zs
    return max(-1.0, min(1.0, v))
