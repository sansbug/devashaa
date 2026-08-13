"""Tests for the aṣṭakavarga engine.

Two layers of guard:
  * the classical checksums (per-graha totals + sarva 337) via ``verify_tables``;
  * an end-to-end golden fixture — the bhinna/sarva that the independent,
    BPHS-derived ``jyotishganit`` library computes for one real chart
    (DOB 1975-06-25, lagna Aquarius). ``bhinna()`` must reproduce it bit-for-bit,
    which pins both the tables AND the counting rule ``(ref_sign + h - 1) % 12``.
"""

import ashtakavarga as av


def test_tables_pass_checksums():
    assert av.verify_tables() is True


def test_per_planet_totals_are_canonical():
    for p in av.PLANETS:
        total = sum(len(av.BENEFIC_HOUSES[p][r]) for r in av.REFS)
        assert total == av.CANONICAL_TOTALS[p], (p, total)
    assert sum(av.CANONICAL_TOTALS.values()) == av.SARVA_TOTAL == 337


# --- golden fixture: jyotishganit output for one chart --------------------------
# sign indices (Aries=0 … Pisces=11) of the seven grahas + lagna for the fixture.
_FIX_SIGNS = {"sun": 2, "moon": 9, "mars": 0, "mercury": 1,
              "jupiter": 11, "venus": 3, "saturn": 2}
_FIX_LAGNA = 10  # Aquarius
_FIX_SAV = [31, 25, 22, 27, 22, 25, 28, 30, 29, 32, 34, 32]
_FIX_BAV = {
    "sun":     [5, 2, 4, 6, 1, 3, 3, 4, 5, 7, 4, 4],
    "moon":    [4, 3, 3, 3, 4, 4, 4, 6, 5, 5, 3, 5],
    "mars":    [4, 2, 3, 3, 2, 2, 3, 4, 4, 3, 5, 4],
    "mercury": [5, 5, 2, 5, 3, 4, 6, 5, 3, 4, 8, 4],
    "jupiter": [4, 7, 4, 4, 5, 4, 5, 5, 4, 4, 5, 5],
    "venus":   [5, 4, 2, 3, 4, 6, 5, 3, 4, 5, 5, 6],
    "saturn":  [4, 2, 4, 3, 3, 2, 2, 3, 4, 4, 4, 4],
}


def test_bhinna_matches_golden_fixture():
    bav = av.bhinna(_FIX_SIGNS, _FIX_LAGNA)
    for p in av.PLANETS:
        assert bav[p] == _FIX_BAV[p], (p, bav[p], _FIX_BAV[p])


def test_sarva_matches_golden_fixture():
    bav = av.bhinna(_FIX_SIGNS, _FIX_LAGNA)
    assert av.sarva(bav) == _FIX_SAV


def test_totals_invariant_across_arbitrary_positions():
    # per-graha totals are a property of the tables, not the chart — always canonical.
    for lagna in (0, 5, 11):
        signs = {p: (i * 3 + lagna) % 12 for i, p in enumerate(av.PLANETS)}
        bav = av.bhinna(signs, lagna)
        for p in av.PLANETS:
            assert sum(bav[p]) == av.CANONICAL_TOTALS[p], (p, lagna)
        assert sum(av.sarva(bav)) == 337


def test_transit_potency_bounds_and_sign():
    bav = av.bhinna(_FIX_SIGNS, _FIX_LAGNA)
    sav = av.sarva(bav)
    for planet in av.PLANETS:
        for sign in range(12):
            v = av.transit_potency(planet, sign, bav, sav)
            assert -1.0 <= v <= 1.0
    # Mercury in Aquarius (sign 10) holds 8 own-bindus and the highest sarva (34) → strongly +.
    assert av.transit_potency("mercury", 10, bav, sav) > 0.4
