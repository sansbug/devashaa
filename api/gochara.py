"""Gochara (transit) geometry — where the grahas are now, against a natal chart.

Given a natal chart and a moment, this relates the transiting grahas to the
birth chart. Each field carries the tier it deserves — this is NOT a flat
"facts only" payload, because two of its fields are reused from ``motion`` and
inherit that module's traditional tier:

  * house-from-Moon and house-from-lagna — whole-sign counts (facts). BPHS
    supplies no gochara frame, so house-from-Moon is offered as the customary
    primary reference and house-from-lagna alongside it, with NO claim of a BPHS
    primacy for either.
  * graha dṛṣṭi from each transiting graha to the natal points, graded by BPHS
    ch.26 (¼/½/¾/full + the special 3/10, 5/9, 4/8). ch.26 is a NATAL aspect
    doctrine; grading a *transiting* graha's aspect onto a natal point the same
    way is a project decision (consistency with the natal chart), not a
    separately-cited rule — flagged, not smuggled. Only graha dṛṣṭi is surfaced,
    not rāśi dṛṣṭi (a static sign-to-sign relation, not the moving graha's act).
  * conjunctions (a transiting graha in a natal graha's sign) and returns (a
    transiting graha back over its OWN natal longitude) — facts.
  * the transiting graha's gati and combustion, reused from ``motion``. The
    separation-from-Sun and speed are facts; the gati NAME and the combustion
    ORB ride the TRADITIONAL tier they carry there (out-of-BPHS — a retrograde
    Mercury/Venus orb is uncertain). That tier is on each sub-dict, not
    overridden here.

It does NOT say whether a transit is good or bad. BPHS's gochara RESULT rules —
the benefic transit-houses-from-the-Moon per graha and the vedha (mutual
obstruction) — are a separate chapter, and Aṣṭakavarga (the transit-scoring
bindus) is Vol II material this engine does not yet carry. docs/bphs-rules.md
records that "BPHS gives no transit machinery" in the daśā chapters; that
result-doctrine is a source-cited layer to build on top of this, not guessed here.
"""

from __future__ import annotations

from drishti import graha_drishti, house_distance, SPECIAL_DRISHTI_HOUSES
import motion as motion_mod

# Rāhu and Ketu transit and can be conjoined/aspected, but they cast no graha
# dṛṣṭi here — adopting the natal engine's DEFAULT (its graha_drishti_chart also
# excludes nodal dṛṣṭi by default, flagging it NODE_GRAHA_DRISHTI_UNVERIFIED only
# when explicitly enabled). Combustion does not apply to them either.
_NODES = ("rahu", "ketu")


def _house(from_rasi: int, to_rasi: int) -> int:
    """Whole-sign house of ``to_rasi`` counted from ``from_rasi`` (1 = same sign)."""
    return (to_rasi - from_rasi) % 12 + 1


def _signed_arc(a: float, b: float) -> float:
    """Shortest signed longitude arc from b to a, in [-180, 180).

    An exact opposition returns -180 (magnitude is what every consumer uses).
    """
    return (a - b + 180.0) % 360.0 - 180.0


def transit_geometry(
    natal_grahas: list[dict],
    natal_lagna_rasi: int,
    transit_grahas: list[dict],
    transit_utc: str | None = None,
) -> dict:
    """Geometry of ``transit_grahas`` against a natal chart.

    ``natal_grahas`` and ``transit_grahas`` are the graha dicts from a computed
    chart (``VedicChart.to_dict()["grahas"]``): each needs at least ``key``,
    ``longitude`` (sidereal), ``rasi``, ``speed`` and the degree/nakṣatra fields.
    """
    natal_by_key = {g["key"]: g for g in natal_grahas}
    moon = natal_by_key.get("moon")
    if moon is None:
        raise ValueError("natal chart has no Moon — cannot count house-from-Moon")
    moon_rasi = moon["rasi"]

    # Natal points a transit can sit on or aspect: the grahas plus the lagna.
    natal_points = [(g["key"], g["rasi"], g["longitude"]) for g in natal_grahas]

    # Motion (gati + combustion) of the TRANSITING grahas — combustion is judged
    # against the transiting Sun, retrograde against each graha's own speed. If
    # the caller passed no Sun, motion would score combustion against a phantom
    # Sun at 0° Aries, so combustion is withheld rather than reported as fact.
    has_sun = any(g["key"] == "sun" for g in transit_grahas)
    motion = motion_mod.motion_analysis(transit_grahas)
    motion_by_key = (
        {m["key"]: m for m in motion["grahas"]} if not motion.get("error") else {}
    )
    _no_sun_combustion = {"applies": False,
                          "reason": "no Sun in the supplied set — combustion not evaluated"}

    out = []
    for tg in transit_grahas:
        key = tg["key"]
        t_rasi = tg["rasi"]
        t_lon = tg["longitude"]
        m = motion_by_key.get(key, {})

        # Conjunctions: natal points sharing the transiting graha's sign. `arc`
        # is the exact longitude separation — near 0 marks a tight hit.
        conj = []
        for nk, nr, nl in natal_points:
            if nr == t_rasi:
                conj.append({"key": nk, "arc": round(_signed_arc(t_lon, nl), 3)})
        if natal_lagna_rasi == t_rasi:
            conj.append({"key": "lagna", "arc": None})

        # Whole-sign graha dṛṣṭi from the transiting graha to each natal point.
        # A point in the same sign is a conjunction, not an aspect, so it is
        # skipped. Nodes cast no graha dṛṣṭi.
        asp = []
        if key not in _NODES:
            targets = [(nk, nr) for nk, nr, _ in natal_points]
            targets.append(("lagna", natal_lagna_rasi))
            for nk, nr in targets:
                if nr == t_rasi:
                    continue
                strength = graha_drishti(t_rasi, nr, key)
                if strength > 0:
                    h = house_distance(t_rasi, nr)
                    asp.append({
                        "target": nk,
                        "house": h,
                        "strength": round(strength, 3),
                        "special": h in SPECIAL_DRISHTI_HOUSES.get(key, ()),
                    })

        # Return: the transiting graha over its OWN natal longitude (Jupiter
        # return ~12y, Saturn return ~29.5y, …). `distance` near 0 is the return.
        nat = natal_by_key.get(key)
        ret = None
        if nat is not None:
            ret = {
                "natal_longitude": nat["longitude"],
                "distance": round(_signed_arc(t_lon, nat["longitude"]), 3),
                "same_sign": nat["rasi"] == t_rasi,
            }

        out.append({
            "key": key,
            "longitude": t_lon,
            "rasi": t_rasi,
            "degree": tg.get("degree"),
            "minute": tg.get("minute"),
            "second": tg.get("second"),
            "nakshatra": tg.get("nakshatra"),
            "retrograde": tg.get("retrograde"),
            "speed": tg.get("speed"),
            "house_from_moon": _house(moon_rasi, t_rasi),
            "house_from_lagna": _house(natal_lagna_rasi, t_rasi),
            "motion": m.get("motion"),
            "combustion": m.get("combustion") if has_sun else _no_sun_combustion,
            "conjunct_natal": conj,
            "aspects_natal": asp,
            "return": ret,
        })

    return {
        "transit_utc": transit_utc,
        "reference": {"moon_rasi": moon_rasi, "lagna_rasi": natal_lagna_rasi},
        "grahas": out,
        "note": (
            "Positions, house-from-Moon/lagna, conjunctions and returns are "
            "facts; house-from-Moon is the customary primary frame, not a BPHS "
            "one. Graha dṛṣṭi is BPHS ch.26 grading extended to transit→natal (a "
            "project decision — ch.26 is natal-only). The gati name and "
            "combustion orb are traditional (see each sub-dict's tier). No "
            "good/bad transit verdict is asserted: BPHS's gochara result-rules "
            "and Aṣṭakavarga are a separate, source-cited layer not yet built."
        ),
    }
