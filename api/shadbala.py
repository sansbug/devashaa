"""
Ṣaḍbala — the six-fold strength of a graha (B. V. Raman, *Graha and Bhava
Balas*, the standard modern codification of Parāśara's Ṣaḍbala).

Milestone 1 (this module, validated): **Naisargika bala** (natural strength —
fixed per-graha constants, Art. 52) and **Sthāna bala** (positional strength —
the five sub-components of Art. 18–40). Every constant and formula is
transcribed from Raman with the article number cited inline, and the whole
module is validated to the virūpa against Raman's own worked "Standard
Horoscope" (16 Oct 1918) in test_shadbala.py. The remaining four balas (Dig,
Kāla, Cheṣṭā, Dṛk) land in later milestones; nothing computes a Ṣaḍbala *total*
or a strong/weak verdict until all six reconcile, because a partial total would
be a fabricated number.

Units: every value is in **virūpa** (= shashtiāṁśa). 60 virūpa = 1 rūpa.

Provenance: `traditional`. This is Raman's numeric method, not a single BPHS
śloka — Parāśara gives the scheme, Raman gives the arithmetic. The values are
ayanāṁśa-independent (they take longitudes as input); production feeds the
chart's Lahiri longitudes, exactly as every other module does.
"""
from __future__ import annotations

from dataclasses import dataclass

import vargas
from dignity import RASI_LORD, MOOLATRIKONA

# The seven grahas that receive a Ṣaḍbala. Rāhu/Ketu have no strength table in
# Raman's scheme — the nodes are shadow points, not luminous bodies.
GRAHAS = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn")


# ── Naisargika (natural) bala — Art. 52, fixed constants ─────────────────────
# The permanent brightness ranking, Sun brightest. Raman lists these to two
# decimals; they are 60·(rank/7) with Sun=60. (The printed Saturn cell reads
# 8.37 in one table — an OCR slip; 8.57 is the constant that reconciles the
# column, confirmed in the recon.)
NAISARGIKA = {
    "sun": 60.00, "moon": 51.43, "venus": 42.85, "jupiter": 34.28,
    "mercury": 25.70, "mars": 17.14, "saturn": 8.57,
}


# ── Sthāna bala machinery ────────────────────────────────────────────────────

# (1) Ochcha bala — deep-debilitation longitudes (Art. 20, Example 3). Ochcha
# bala = (angular distance from this point, reduced to [0,180]) / 3, so it runs
# 0 at debilitation to 60 at exaltation (the point 180° opposite).
DEBILITATION_LON = {
    "sun": 190.0, "moon": 213.0, "mars": 118.0, "mercury": 345.0,
    "jupiter": 275.0, "venus": 177.0, "saturn": 20.0,
}

# (2) Saptavargaja bala — the relation of a graha to the lord of the sign it
# occupies in each of seven vargas, valued in virūpa (Art. 30).
_SAPTA_VARGAS = (
    ("D1", vargas.d1_rasi), ("D2", vargas.d2_hora), ("D3", vargas.d3_drekkana),
    ("D7", vargas.d7_saptamsa), ("D9", vargas.d9_navamsa),
    ("D12", vargas.d12_dvadasamsa), ("D30", vargas.d30_trimsamsa),
)
_MT_SIGN = {g: MOOLATRIKONA[g][0] for g in GRAHAS}  # Sun=Leo, Moon=Taurus, …
_SWAVARGA = 30.0      # own sign (any varga)
_MOOLATRIKONA = 45.0  # own Mūlatrikoṇa RĀŚI only — never in D2–D30 (Art. 30 rule)

# Naisargika (permanent) friendship, Art. 24. Neutral = everyone not listed.
_NAIS_FRIEND = {
    "sun": {"moon", "mars", "jupiter"},
    "moon": {"sun", "mercury"},
    "mars": {"sun", "moon", "jupiter"},
    "mercury": {"sun", "venus"},
    "jupiter": {"sun", "moon", "mars"},
    "venus": {"mercury", "saturn"},
    "saturn": {"mercury", "venus"},
}
_NAIS_ENEMY = {
    "sun": {"venus", "saturn"},
    "moon": set(),
    "mars": {"mercury"},
    "mercury": {"moon"},
    "jupiter": {"mercury", "venus"},
    "venus": {"sun", "moon"},
    "saturn": {"sun", "moon", "mars"},
}
# Combined (Naisargika + Tātkālika) shade → virūpa, Art. 26–27.
#   key = (tātkālika friend/enemy, naisargika friend/neutral/enemy)
_COMBINE = {
    ("friend", "friend"): 22.5,   # Adhi Mitra
    ("friend", "neutral"): 15.0,  # Mitra
    ("friend", "enemy"): 7.5,     # Sama
    ("enemy", "friend"): 7.5,     # Sama
    ("enemy", "neutral"): 3.75,   # Satru
    ("enemy", "enemy"): 1.875,    # Adhi Satru
}

# (5) Drekkāṇa bala — planet gender picks the rewarded decanate (Art. 36–39).
_GENDER_DECANATE = {  # decanate index (0,1,2) that scores 15 virūpa
    "sun": 0, "jupiter": 0, "mars": 0,       # masculine → 1st drekkāṇa
    "saturn": 1, "mercury": 1,               # hermaphrodite → 2nd (middle)
    "moon": 2, "venus": 2,                   # feminine → 3rd (last)
}


@dataclass
class _Pos:
    sign: int   # 0..11 (Aries..Pisces)
    deg: float  # degrees within the sign, 0..30


def _split(lon: float) -> _Pos:
    lon = lon % 360.0
    return _Pos(int(lon // 30), lon % 30.0)


def _naisargika_relation(planet: str, other: str) -> str:
    if other in _NAIS_FRIEND[planet]:
        return "friend"
    if other in _NAIS_ENEMY[planet]:
        return "enemy"
    return "neutral"


def _tatkalika_relation(planet_sign: int, other_sign: int) -> str:
    """Temporary friendship (Art. 25): the lord is a friend when it sits in the
    2/3/4/10/11/12 house *from* the planet (counted by sign in the rāśi)."""
    house = (other_sign - planet_sign) % 12 + 1
    return "friend" if house in (2, 3, 4, 10, 11, 12) else "enemy"


def _ochcha_bala(planet: str, pos: _Pos) -> float:
    """(1) Exaltation strength, 0–60 virūpa (Art. 20)."""
    lon = pos.sign * 30 + pos.deg
    diff = abs(lon - DEBILITATION_LON[planet])
    if diff > 180.0:
        diff = 360.0 - diff  # reduce to angular distance from the debilitation point
    return diff / 3.0


def _saptavargaja_bala(planet: str, pos: _Pos, d1_signs: dict[str, int]) -> float:
    """(2) Dignity summed across the seven vargas (Art. 30). Own sign = 30
    (45 only for the Mūlatrikoṇa rāśi, and only in D1); otherwise the combined
    Naisargika+Tātkālika shade toward the varga-lord."""
    total = 0.0
    for vkey, fn in _SAPTA_VARGAS:
        vsign = fn(pos.sign, pos.deg)
        vlord = RASI_LORD[vsign]
        if vlord == planet:
            if vkey == "D1" and vsign == _MT_SIGN[planet]:
                total += _MOOLATRIKONA
            else:
                total += _SWAVARGA
        else:
            tat = _tatkalika_relation(pos.sign, d1_signs[vlord])
            nais = _naisargika_relation(planet, vlord)
            total += _COMBINE[(tat, nais)]
    return total


def _ojayugma_bala(planet: str, pos: _Pos) -> float:
    """(3) Odd/even strength of rāśi and navāṁśa, 15 each (Art. 31). Moon and
    Venus favour even signs; the other five favour odd."""
    wants_even = planet in ("moon", "venus")
    nava = vargas.d9_navamsa(pos.sign, pos.deg)
    bala = 0.0
    for sign in (pos.sign, nava):
        is_even = (sign % 2 == 1)  # 0-indexed Aries is the 1st (odd) sign
        if is_even == wants_even:
            bala += 15.0
    return bala


def _kendra_bala(pos: _Pos, lagna_rasi: int) -> float:
    """(4) Angular/succedent/cadent strength, by sign from the lagna (Art. 32)."""
    house = (pos.sign - lagna_rasi) % 12 + 1
    if house in (1, 4, 7, 10):
        return 60.0   # kendra
    if house in (2, 5, 8, 11):
        return 30.0   # panapara
    return 15.0       # apoklima


def _drekkana_bala(planet: str, pos: _Pos) -> float:
    """(5) Decanate strength by planetary gender, 15 or 0 (Art. 36)."""
    decanate = int(pos.deg // 10.0)  # 0,1,2
    return 15.0 if decanate == _GENDER_DECANATE[planet] else 0.0


def sthana_bala(positions: dict[str, float], lagna_rasi: int) -> dict[str, dict]:
    """Positional strength for every graha present.

    ``positions`` maps a graha name to its sidereal longitude in degrees;
    ``lagna_rasi`` is the ascendant sign (0..11). Returns, per graha, the five
    sub-components and their total, all in virūpa.
    """
    d1_signs = {g: _split(lon).sign for g, lon in positions.items() if g in GRAHAS}
    out: dict[str, dict] = {}
    for g in GRAHAS:
        if g not in positions:
            continue
        pos = _split(positions[g])
        parts = {
            "ochcha": _ochcha_bala(g, pos),
            "saptavargaja": _saptavargaja_bala(g, pos, d1_signs),
            "ojayugma": _ojayugma_bala(g, pos),
            "kendra": _kendra_bala(pos, lagna_rasi),
            "drekkana": _drekkana_bala(g, pos),
        }
        parts["total"] = sum(parts.values())
        out[g] = parts
    return out


def naisargika_bala() -> dict[str, float]:
    """Natural strength — the same fixed constants for every chart (Art. 52)."""
    return dict(NAISARGIKA)


# ── Cheṣṭā (motional) bala — Ch. VI, Art. 79–107 ─────────────────────────────
# Strength from the arc of retrogression. Only the five tārā-grahas get it; the
# Sun and Moon have no Cheṣṭā row in the Ṣaḍbala (their motional strength is
# carried by Ayana and Pakṣa bala respectively). The śīghra-kendra is measured
# from the śīghrocha (apogee): mean Sun for the three superior grahas, a
# mean-elements value for Mercury/Venus. Because those mean elements are exactly
# the "Seeghrocha the śāstra never tabulates," this function takes them as
# inputs — the ephemeris supplies them upstream; the bala formula lives here.
CHESHTA_GRAHAS = ("mars", "mercury", "jupiter", "venus", "saturn")


def cheshta_bala(true_longs: dict[str, float], mean_longs: dict[str, float],
                 sighrochas: dict[str, float]) -> dict[str, float]:
    """Motional strength (Art. 105–107). Cheṣṭā-kendra = śīghrocha −
    (mean + true)/2, folded to ≤180°, ÷3 → 0–60 virūpa."""
    out = {}
    for g in CHESHTA_GRAHAS:
        if g not in true_longs:
            continue
        kendra = (sighrochas[g] - (mean_longs[g] + true_longs[g]) / 2.0) % 360.0
        if kendra > 180.0:
            kendra = 360.0 - kendra
        out[g] = kendra / 3.0
    return out


# ── Dig (directional) bala — Ch. IV, Art. 41–45 ──────────────────────────────
# Each graha has one powerful cardinal point and, 180° opposite, a powerless
# one; strength scales linearly with distance from the powerless point (0 there,
# 60 at the powerful point). Raman measures from the bhāva-madhya (mid-point) of
# the relevant kendra, i.e. the actual Ascendant/MC and their opposites.
_DIG_POWERLESS = {   # the cardinal cusp a graha is subtracted from (Art. 44)
    "sun": "nadir", "mars": "nadir",         # powerful in the 10th (south)
    "jupiter": "desc", "mercury": "desc",    # powerful in the 1st (east)
    "venus": "mc", "moon": "mc",             # powerful in the 4th (north)
    "saturn": "asc",                          # powerful in the 7th (west)
}


def dig_bala(positions: dict[str, float], asc_long: float, mc_long: float) -> dict[str, float]:
    """Directional strength (Art. 45). ``asc_long``/``mc_long`` are the
    Ascendant and Midheaven longitudes (bhāva-madhya of the 1st/10th); the 7th
    and 4th are their opposites."""
    cusp = {
        "asc": asc_long % 360, "desc": (asc_long + 180) % 360,
        "mc": mc_long % 360, "nadir": (mc_long + 180) % 360,
    }
    out = {}
    for g in GRAHAS:
        if g not in positions:
            continue
        arc = abs((positions[g] % 360) - cusp[_DIG_POWERLESS[g]])
        if arc > 180.0:
            arc = 360.0 - arc
        out[g] = arc / 3.0
    return out


# ── Kāla (temporal) bala, part 2: Pakṣa bala — Ch. V, Art. 52–55 ─────────────
# Waxing Moon strengthens benefics; the elongation (Moon − Sun), folded to
# ≤180°, over 3 is the benefic value; malefics take the complement. The Moon's
# own value is always doubled. (This is one of Kāla bala's nine components; the
# rest — Nathonnatha, Thribhāga, the four lordship balas, Ayana, Yuddha — land
# in a later milestone as they need birth-clock/ahargana/declination context.)
def paksha_bala(positions: dict[str, float], mercury_benefic: bool | None = None) -> dict[str, float]:
    """Pakṣa (lunar-fortnight) bala. ``mercury_benefic`` overrides Mercury's
    side; when None, Mercury is treated as malefic iff combust (within Raman's
    working rule that a combust/afflicted Budha is a pāpa)."""
    sun, moon = positions["sun"], positions["moon"]
    elong = (moon - sun) % 360.0
    folded = elong if elong <= 180.0 else 360.0 - elong
    subha = folded / 3.0            # benefic value = the Moon's illumination measure
    papa = 60.0 - subha            # malefic value

    if mercury_benefic is None:
        merc = positions.get("mercury")
        # combust iff within the Sun's combustion orb of Mercury (Art. 120 note)
        mercury_benefic = merc is None or abs((merc - sun + 180) % 360 - 180) > 14.0

    is_benefic = {
        "jupiter": True, "venus": True,
        "sun": False, "mars": False, "saturn": False,
        "mercury": bool(mercury_benefic),
    }
    out = {}
    for g in GRAHAS:
        if g not in positions:
            continue
        # The Moon ALWAYS takes the illumination (śubha) value, doubled — 0 at
        # new moon, 120 at full — never the pāpa complement. Taking the complement
        # in Kṛṣṇa pakṣa would make its strength discontinuous across the full
        # moon (≈119 → ≈0.7 as it crosses), which the method never intends.
        if g == "moon":
            out[g] = subha * 2.0
        else:
            out[g] = subha if is_benefic[g] else papa
    return out


# ── Dṛk (aspectual) bala — Ch. VIII, Art. 109–120 ───────────────────────────
# The Sripātī graded aspect. Every graha casts a dṛṣṭi whose strength depends on
# the aspect angle (dṛṣṭi-kendra = aspected − aspecting): nil below 30° or above
# 300°, rising to full 60 at the 7th (180°). Mars/Jupiter/Saturn add a fixed
# viśeṣa (special-aspect) bonus on their extra houses. A benefic's aspect is
# additive, a malefic's subtractive; the net over each graha, ÷4, is its Dṛk bala.
_VISESHA = {   # aspecting planet → (bonus virūpa, [special-aspect angle ranges])
    "mars": (15.0, ((90, 120), (210, 240))),        # 4th & 8th houses
    "jupiter": (30.0, ((120, 150), (240, 270))),    # 5th & 9th houses
    "saturn": (45.0, ((60, 90), (270, 300))),       # 3rd & 10th houses
}
_MERCURY_COMBUST_ORB = 14.0  # Budha is a pāpa when this close to the Sun (Art. 120)


def _drishti_value(dk: float) -> float:
    """Ordinary Sripātī dṛṣṭi value in virūpa for an aspect angle ``dk`` (Art. 114)."""
    if dk < 30.0 or dk > 300.0:
        return 0.0
    if dk <= 60.0:
        return (dk - 30.0) / 2.0
    if dk <= 90.0:
        return (dk - 60.0) + 15.0
    if dk <= 120.0:
        return (120.0 - dk) / 2.0 + 30.0
    if dk <= 150.0:
        return 150.0 - dk
    if dk <= 180.0:
        return (dk - 150.0) * 2.0
    return (300.0 - dk) / 2.0  # 180°–300°


def drik_bala(positions: dict[str, float], moon_waxing: bool | None = None,
              mercury_benefic: bool | None = None) -> dict[str, float]:
    """Aspectual strength (Art. 120), signed. ``moon_waxing`` and
    ``mercury_benefic`` fix the benefic/malefic side of those two; when None
    they are derived from the Sun–Moon elongation and Mercury's combustion."""
    sun, moon = positions["sun"], positions["moon"]
    if moon_waxing is None:
        moon_waxing = ((moon - sun) % 360.0) < 180.0
    if mercury_benefic is None:
        merc = positions.get("mercury")
        mercury_benefic = merc is None or \
            abs((merc - sun + 180.0) % 360.0 - 180.0) > _MERCURY_COMBUST_ORB
    sign = {
        "sun": -1.0, "mars": -1.0, "saturn": -1.0,      # natural pāpas
        "jupiter": 1.0, "venus": 1.0,                    # natural śubhas
        "moon": 1.0 if moon_waxing else -1.0,            # waxing śubha / waning pāpa
        "mercury": 1.0 if mercury_benefic else -1.0,
    }
    present = [g for g in GRAHAS if g in positions]
    out = {}
    for aspected in present:
        pinda = 0.0
        for aspecting in present:
            if aspecting == aspected:
                continue
            dk = (positions[aspected] - positions[aspecting]) % 360.0
            val = _drishti_value(dk)
            if aspecting in _VISESHA:
                bonus, ranges = _VISESHA[aspecting]
                if any(lo <= dk <= hi for lo, hi in ranges):
                    val += bonus
            pinda += sign[aspecting] * val
        out[aspected] = pinda / 4.0
    return out


# ── Kāla (temporal) bala — the remaining eight components (Ch. V, Art. 46–78) ─
# Weekday index 0=Sunday … 6=Saturday, and its ruling graha.
WEEKDAY_LORD = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn")
# The horā cycle (Chaldean order, slowest → fastest). The first horā after
# sunrise is ruled by the weekday-lord; successive horās step through this ring.
_CHALDEAN = ("saturn", "jupiter", "mars", "sun", "venus", "mercury", "moon")
# Thribhāga: the lord of each third of the day / of the night.
_DAY_THIRD_LORDS = ("mercury", "sun", "saturn")
_NIGHT_THIRD_LORDS = ("moon", "venus", "mars")
# Yuddha: apparent disc diameters (bimba-parimāṇa, arc-seconds).
_BIMBA = {"mars": 9.4, "mercury": 6.6, "jupiter": 190.4, "venus": 16.6, "saturn": 158.0}


def _zeros() -> dict[str, float]:
    return {g: 0.0 for g in GRAHAS}


def nathonnatha_bala(hours_from_apparent_midnight: float) -> dict[str, float]:
    """(1) Day/night strength (Art. 47–51). Birth time from local apparent
    midnight → degrees at 15°/hr, folded to ≤180°; day-strong grahas take
    deg/3, night-strong grahas the complement, Mercury always 60."""
    deg = (hours_from_apparent_midnight * 15.0) % 360.0
    if deg > 180.0:
        deg = 360.0 - deg
    diva = deg / 3.0            # full at apparent noon (deg=180)
    ratri = 60.0 - diva         # full at apparent midnight (deg=0)
    out = {}
    for g in GRAHAS:
        if g == "mercury":
            out[g] = 60.0
        elif g in ("sun", "jupiter", "venus"):
            out[g] = diva
        else:                    # moon, mars, saturn
            out[g] = ratri
    return out


def thribhaga_bala(is_day: bool, third_index: int) -> dict[str, float]:
    """(3) Strength of the day/night third of birth (Art. 56–57). The lord of
    that third scores 60; Jupiter always scores 60."""
    lords = _DAY_THIRD_LORDS if is_day else _NIGHT_THIRD_LORDS
    out = _zeros()
    out[lords[third_index]] = 60.0
    out["jupiter"] = 60.0
    return out


def _lordship_bala(weekday_of_start: int, award: float) -> dict[str, float]:
    out = _zeros()
    out[WEEKDAY_LORD[weekday_of_start]] = award
    return out


def abda_bala(ahargana: int, epoch_weekday: int = 3) -> dict[str, float]:
    """(4a) Year-lord (Art. 60, 65). Complete 360-day years since the epoch fix
    the weekday the running year began; that lord scores 15. ``epoch_weekday``
    defaults to Wednesday (Raman's condensed-ahargana epoch)."""
    q = ahargana // 360
    r = ((q * 3) + 1) % 7
    return _lordship_bala((epoch_weekday + (r - 1)) % 7, 15.0)


def masa_bala(ahargana: int, epoch_weekday: int = 3) -> dict[str, float]:
    """(4b) Month-lord (Art. 61, 66). Complete 30-day months → month-start
    weekday; that lord scores 30."""
    q = ahargana // 30
    r = ((q * 2) + 1) % 7
    return _lordship_bala((epoch_weekday + (r - 1)) % 7, 30.0)


def vara_bala(weekday: int) -> dict[str, float]:
    """(4c) Weekday-lord (Art. 62, 67) — the birth weekday's ruler scores 45."""
    return _lordship_bala(weekday, 45.0)


def hora_bala(weekday: int, hora_number: int) -> dict[str, float]:
    """(4d) Hour-lord (Art. 68–70). ``hora_number`` is 1-based from sunrise; its
    lord scores 60."""
    start = _CHALDEAN.index(WEEKDAY_LORD[weekday])
    lord = _CHALDEAN[(start + (hora_number - 1)) % 7]
    out = _zeros()
    out[lord] = 60.0
    return out


def ayana_bala(declinations: dict[str, float]) -> dict[str, float]:
    """(5) Declination strength (Art. 71–75). ``declinations`` maps a graha to
    its signed declination (North +, South −). Ayana = (24° + kranti-term)/48 ×
    60, doubled for the Sun; the term's sign follows Raman's per-graha rule."""
    out = {}
    for g in GRAHAS:
        if g not in declinations:
            continue
        d = declinations[g]
        if g in ("sun", "mars", "jupiter", "venus"):
            term = d           # North additive, South subtractive
        elif g in ("saturn", "moon"):
            term = -d          # South additive, North subtractive
        else:                   # mercury — always additive
            term = abs(d)
        val = (24.0 + term) / 48.0 * 60.0
        if g == "sun":
            val *= 2.0
        out[g] = val
    return out


def yuddha_adjustment(positions: dict[str, float],
                      pre_yuddha: dict[str, float]) -> dict[str, float]:
    """(9) Planetary war (Art. 76–77). Two tārā-grahas within 1° are at war; the
    one of lesser longitude wins. The victor gains, and the vanquished loses,
    (difference of their pre-Yuddha aggregates) ÷ (difference of disc diameters).
    ``pre_yuddha`` is each combatant's Sthāna + Dik + Kāla-through-Horā total.
    Returns a signed adjustment per graha (0 for everyone when there is no war)."""
    adj = _zeros()
    warriors = [g for g in ("mars", "mercury", "jupiter", "venus", "saturn") if g in positions]
    for i in range(len(warriors)):
        for j in range(i + 1, len(warriors)):
            a, b = warriors[i], warriors[j]
            sep = abs((positions[a] - positions[b] + 180.0) % 360.0 - 180.0)
            if sep >= 1.0:
                continue
            winner, loser = (a, b) if positions[a] < positions[b] else (b, a)
            disc_diff = abs(_BIMBA[a] - _BIMBA[b])
            if disc_diff == 0:
                continue
            delta = abs(pre_yuddha[a] - pre_yuddha[b]) / disc_diff
            adj[winner] += delta
            adj[loser] -= delta
    return adj


def kala_bala(positions: dict[str, float], *, hours_from_apparent_midnight: float,
              is_day: bool, thribhaga_third: int, weekday: int, ahargana: int,
              hora_number: int, declinations: dict[str, float],
              epoch_weekday: int = 3,
              sthana_total: dict[str, float] | None = None,
              dik: dict[str, float] | None = None,
              mercury_benefic: bool | None = None) -> dict:
    """Assemble all nine Kāla components. Yuddha is applied last, as it needs the
    Sthāna + Dik + Kāla-through-Horā aggregates of the combatants (passed via
    ``sthana_total`` and ``dik``); when those are absent Yuddha is left at zero."""
    comps = {
        "nathonnatha": nathonnatha_bala(hours_from_apparent_midnight),
        "paksha": paksha_bala(positions, mercury_benefic=mercury_benefic),
        "thribhaga": thribhaga_bala(is_day, thribhaga_third),
        "abda": abda_bala(ahargana, epoch_weekday),
        "masa": masa_bala(ahargana, epoch_weekday),
        "vara": vara_bala(weekday),
        "hora": hora_bala(weekday, hora_number),
        "ayana": ayana_bala(declinations),
        "yuddha": _zeros(),
    }
    # Sub-total through Horā (everything except Ayana and Yuddha) drives Yuddha.
    through_hora = {g: sum(comps[k][g] for k in
                           ("nathonnatha", "paksha", "thribhaga", "abda", "masa", "vara", "hora"))
                    for g in GRAHAS if g in positions}
    if sthana_total is not None and dik is not None:
        pre = {g: sthana_total[g] + dik[g] + through_hora[g] for g in through_hora}
        comps["yuddha"] = yuddha_adjustment(positions, pre)

    totals = {g: sum(comps[k][g] for k in comps)
              for g in GRAHAS if g in positions}
    return {"components": comps, "totals": totals}


# ── Full Ṣaḍbala assembly + verdict — Art. 121, Ex. 56–57 ────────────────────
# Minimum required strength per graha (rūpas), Ex. 57 / thresholds table. A graha
# is "strong" when its Ṣaḍbala Piṇḍa ≥ its minimum.
MIN_REQUIRED_RUPA = {
    "sun": 5.0, "moon": 6.0, "mars": 5.0, "mercury": 7.0,
    "jupiter": 6.5, "venus": 5.5, "saturn": 5.0,
}


def assemble(sthana: dict[str, dict], dik: dict[str, float],
             kala_totals: dict[str, float], cheshta: dict[str, float],
             naisargika: dict[str, float], drik: dict[str, float]) -> dict:
    """Combine the six balas into the Ṣaḍbala Piṇḍa (Art. 121): Sthāna + Dik +
    Kāla + Cheṣṭā + Naisargika, with the signed Dṛk bala added. Returns per-graha
    totals in virūpa and rūpa, plus the strong/weak verdict against the minimum."""
    out = {}
    for g in GRAHAS:
        if g not in sthana:
            continue
        virupa = (sthana[g]["total"] + dik[g] + kala_totals[g]
                  + cheshta.get(g, 0.0) + naisargika[g] + drik[g])
        rupa = virupa / 60.0
        minimum = MIN_REQUIRED_RUPA[g]
        out[g] = {
            "sthana": sthana[g]["total"],
            "dik": dik[g],
            "kala": kala_totals[g],
            "cheshta": cheshta.get(g),   # None for Sun/Moon (no Cheṣṭā row)
            "naisargika": naisargika[g],
            "drik": drik[g],
            "total_virupa": virupa,
            "total_rupa": rupa,
            "min_required_rupa": minimum,
            "ratio": rupa / minimum,
            "strong": rupa >= minimum,
        }
    return out
