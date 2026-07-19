"""Graha dignity — BPHS Vol I, Chapter 3.

Every table here is transcribed from the ślokas, not from memory. Citations:

  vv.49-50  EXALTATION AND DEBILITATION
    "For the seven planets from the Sun on, the signs of exaltation are
     respectively Aries, Taurus, Capricorn, Virgo, Cancer, Pisces and Libra.
     The deepest exaltation degrees are respectively 10, 3, 28, 15, 5, 27 and
     20 in those signs. And in the seventh sign from the said exaltation sign
     each planet has its own debilitation. The same degrees of deep exaltation
     apply to deep fall."

  vv.51-54  ADDITIONAL DIGNITIES (mūlatrikoṇa / own-sign arcs)

  v.55      NATURAL RELATIONSHIPS
    "Note the signs which are the 4th, 2nd, 12th, 5th, 9th and the 8th from the
     Mūlatrikoṇa of a planet. The planets ruling such signs are its friends,
     apart from the lord of its exaltation sign. Lords other than these are its
     enemies. If a planet becomes its friend as well as its enemy … then it is
     neutral."

RĀHU AND KETU CARRY NO DIGNITY HERE. On the nodes v.50's note says only "there
are different views" — BPHS assigns them no exaltation, debilitation,
mūlatrikoṇa or rāśi lordship, so they are returned as `None` rather than being
given a value this text does not support.
"""

from __future__ import annotations

ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO = 0, 1, 2, 3, 4, 5
LIBRA, SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES = 6, 7, 8, 9, 10, 11

# Rāśi lords, 0 = Meṣa .. 11 = Mīna.
RASI_LORD = [
    "mars", "venus", "mercury", "moon", "sun", "mercury",
    "venus", "mars", "jupiter", "saturn", "saturn", "jupiter",
]

# v.49-50. (sign, exact degree). Debilitation is derived, never hardcoded:
# it is the SAME degree of the 7th sign, which is +6 signs.
EXALTATION: dict[str, tuple[int, float]] = {
    "sun": (ARIES, 10.0),
    "moon": (TAURUS, 3.0),
    "mars": (CAPRICORN, 28.0),
    "mercury": (VIRGO, 15.0),
    "jupiter": (CANCER, 5.0),
    "venus": (PISCES, 27.0),
    "saturn": (LIBRA, 20.0),
}
DEBILITATION: dict[str, tuple[int, float]] = {
    g: ((sign + 6) % 12, deg) for g, (sign, deg) in EXALTATION.items()
}

# A graha is exalted throughout its exaltation sign — EXCEPT where vv.51-54
# explicitly partition that sign. Only Mercury is partitioned: Virgo is its
# exaltation sign AND its own sign, and the text splits it
# "the first 15 degrees are exaltation zone, the next 5 degrees Moolatrikona
#  and the last 10 degrees are own house."
# The upper bound is inclusive so 15°00' — the deep exaltation POINT itself —
# resolves as exalted rather than falling into the mūlatrikoṇa arc that starts
# at the same degree.
EXALTATION_ARC: dict[str, tuple[float, float]] = {
    "mercury": (0.0, 15.0),
}

# vv.51-54. Arc within a sign that is mūlatrikoṇa: (sign, start_deg, end_deg).
#   Sun      "In Leo the first 20 degrees are the Sun's Mūlatrikoṇa while the
#             rest is his own house."
#   Mars     "the first 12 degrees in Aries as Mūlatrikoṇa with the rest
#             becoming simply his own house."
#   Mercury  "in Virgo the first 15 degrees are exaltation zone, the next 5
#             degrees Mūlatrikoṇa and the last 10 degrees are own house."
#   Jupiter  "The first one third of Sagittarius is the Mūlatrikoṇa"  (0-10°)
#   Venus    "Venus divides Libra into two halves keeping the first as
#             Mūlatrikoṇa and the second as own house."
#   Saturn   "Saturn's arrangements are same in Aquarius as the Sun has in Leo."
#
#   Moon: the śloka is illegible in our scan at this point (OCR damage on the
#   line following the Sun's). The classical reading — Vṛṣabha 4°-30°, with
#   Karka as own sign — is used, and flagged rather than presented as verified.
MOOLATRIKONA: dict[str, tuple[int, float, float]] = {
    "sun": (LEO, 0.0, 20.0),
    "moon": (TAURUS, 4.0, 30.0),        # UNVERIFIED — see note above
    "mars": (ARIES, 0.0, 12.0),
    "mercury": (VIRGO, 15.0, 20.0),
    "jupiter": (SAGITTARIUS, 0.0, 10.0),
    "venus": (LIBRA, 0.0, 15.0),
    "saturn": (AQUARIUS, 0.0, 20.0),
}
MOOLATRIKONA_UNVERIFIED = {"moon"}

# v.55: friends are the lords of the 2nd, 4th, 5th, 8th, 9th and 12th from a
# graha's mūlatrikoṇa; the rest are enemies; the exaltation lord is always a
# friend; friend-and-enemy at once resolves to neutral.
_FRIEND_HOUSES = (2, 4, 5, 8, 9, 12)


def _relationships(graha: str) -> dict[str, str]:
    mt_sign = MOOLATRIKONA[graha][0]
    friends, enemies = set(), set()
    for h in range(1, 13):
        lord = RASI_LORD[(mt_sign + h - 1) % 12]
        if lord == graha:
            continue
        (friends if h in _FRIEND_HOUSES else enemies).add(lord)
    friends.add(RASI_LORD[EXALTATION[graha][0]])   # "apart from the lord of its
    friends.discard(graha)                          #  exaltation sign"
    out = {}
    for other in set(RASI_LORD):
        if other == graha:
            continue
        f, e = other in friends, other in enemies
        out[other] = "neutral" if (f and e) else ("friend" if f else "enemy")
    return out


NATURAL_RELATIONS: dict[str, dict[str, str]] = {
    g: _relationships(g) for g in EXALTATION
}


def dignity_of(graha: str, longitude: float) -> dict | None:
    """Dignity of a graha at a sidereal longitude, or None for the nodes.

    `uccha_distance` is the signed arc to the exact deep-exaltation point of
    THIS graha (negative = short of it), and `nica_distance` likewise. They are
    what make the degree meaningful rather than decorative: BPHS locates peak
    strength at a point, not across a whole sign.
    """
    if graha not in EXALTATION:
        return None   # Rāhu / Ketu — BPHS gives them none

    lon = longitude % 360.0
    sign = int(lon // 30)
    deg = lon % 30.0

    ex_sign, ex_deg = EXALTATION[graha]
    de_sign, de_deg = DEBILITATION[graha]
    mt_sign, mt_lo, mt_hi = MOOLATRIKONA[graha]

    # Precedence: strongest claim first. Exaltation is the whole sign unless
    # vv.51-54 partition it (Mercury/Virgo), in which case only the stated arc
    # counts. Mūlatrikoṇa then beats plain own-sign, being an arc inside it.
    ex_lo, ex_hi = EXALTATION_ARC.get(graha, (0.0, 30.0))
    if sign == ex_sign and ex_lo <= deg <= ex_hi:
        state = "exalted"
    elif sign == de_sign:
        state = "debilitated"
    elif sign == mt_sign and mt_lo <= deg < mt_hi:
        state = "moolatrikona"
    elif RASI_LORD[sign] == graha:
        state = "own"
    else:
        state = NATURAL_RELATIONS[graha].get(RASI_LORD[sign], "neutral")

    def arc_to(target_sign, target_deg):
        """Shortest signed arc from the graha to a point, in degrees."""
        d = (lon - (target_sign * 30 + target_deg) + 180) % 360 - 180
        return round(d, 4)

    return {
        "state": state,                       # exalted|debilitated|moolatrikona|own|friend|neutral|enemy
        "lord_of_sign": RASI_LORD[sign],
        "exaltation": {"sign": ex_sign, "degree": ex_deg},
        "debilitation": {"sign": de_sign, "degree": de_deg},
        "moolatrikona": {"sign": mt_sign, "from": mt_lo, "to": mt_hi},
        "moolatrikona_verified": graha not in MOOLATRIKONA_UNVERIFIED,
        # Signed arcs: 0 means sitting exactly on the point.
        "uccha_distance": arc_to(ex_sign, ex_deg),
        "nica_distance": arc_to(de_sign, de_deg),
        # 1.0 at the exact exaltation point, 0.0 at the exact debilitation
        # point, linear in the 180° between. This is the classical
        # uccha-bala proportion, and is what a degree bar should encode.
        "uccha_bala": round(1.0 - abs(arc_to(ex_sign, ex_deg)) / 180.0, 4),
    }


def sign_landmarks(sign: int) -> dict:
    """Doctrinal landmarks inside one sign, for drawing a degree scale.

    Everything a 0-30° ruler for this sign needs: which grahas peak or fall
    here and at what degree, the mūlatrikoṇa arc if any, and the gaṇḍānta zone.
    """
    uccha = [{"graha": g, "degree": d} for g, (s, d) in EXALTATION.items() if s == sign]
    nica = [{"graha": g, "degree": d} for g, (s, d) in DEBILITATION.items() if s == sign]
    mt = [{"graha": g, "from": lo, "to": hi}
          for g, (s, lo, hi) in MOOLATRIKONA.items() if s == sign]

    return {
        "sign": sign,
        "lord": RASI_LORD[sign],
        "exaltation_points": uccha,
        "debilitation_points": nica,
        "moolatrikona_arcs": mt,
    }


# ---------------------------------------------------------------------------
# Gaṇḍānta — BPHS Vol II, Chapter 92 ("Remedies from Birth in Gandanta"), vv.1-5
#
# NOT ch.3 material and NOT a dignity: it is ariṣṭa/muhūrta doctrine. Parāśara
# names three kinds (v.1) — Tithi, Nakṣatra and Lagna — and measures every one
# of them in GHAṬIKĀS OF TIME, never in degrees of arc:
#
#   v.3  "the last two ghatikas of Revti and first two [ghatikas] of Aswini,
#         the last two ghatikas of Ashlesha and [fir]st two ghatikas of Makha
#         and the last two g[h]atikas of [Jy]estha and first two ghatikas of
#         Moola (total 4 ghatikas) are known as Nakshatra Gandanta."
#
#   v.4  "The last half ghatika of Pisces and first half ghatika of Aries, the
#         last half gha[tik]a of Cancer and first half ghatika of Leo, the last
#         half ghatika of Scorpio and first half ghatika of Sagittarius, are
#         known as Lagna Gandanta."
#
# Those two verses agree on the SAME three junctions, because the nakṣatras
# named end exactly on the sign boundaries: Āśleṣā at 120°, Jyeṣṭhā at 240°,
# Revatī at 360°. Three junctions only — not every sign boundary.
#
# THE WIDELY-QUOTED "LAST 3°20′" IS NOT PARĀŚARA. It is Santhanam's own note to
# Vol I ch.9 v.13 ("The last Navamsas of Cancer, of Scorpio and of Pisces are
# called as Gandanta"), which he expressly attributes to "a host of authors".
# Two ghaṭikās is 48 minutes; the Moon covers ~0°26′ in that time, so the
# navāṁśa reading is roughly EIGHT TIMES too wide. We follow the śloka and
# derive the arc from the body's own motion.
#
# Scope: the three kinds are the three components of the birth MOMENT — the
# tithi, the birth nakṣatra (i.e. Candra) and the lagna. Parāśara never places
# an arbitrary graha "in gaṇḍānta", so neither do we.
# ---------------------------------------------------------------------------

GHATIKA_DAYS = 1.0 / 60.0          # a ghaṭikā is 1/60 of a day (24 min)
NAKSHATRA_GANDANTA_GHATIKAS = 2.0  # v.3, each side of the junction
GANDANTA_JUNCTIONS = (120.0, 240.0, 360.0)   # Karka|Siṁha, Vṛścika|Dhanus, Mīna|Meṣa


def nakshatra_gandanta(moon_longitude: float, moon_speed: float) -> dict | None:
    """Candra's nakṣatra-gaṇḍānta (ch.92 v.3), as an arc derived from her speed.

    `moon_speed` is degrees per day. Two ghaṭikās either side of the junction
    is 2/60 of a day, so the half-width is simply the distance she travels in
    that time — which is why this is narrow (~0°26′) and why it moves with her
    actual, varying rate rather than being a fixed navāṁśa.

    Returns None when the Moon is not in a gaṇḍānta, which is the usual case.
    """
    half = abs(moon_speed) * NAKSHATRA_GANDANTA_GHATIKAS * GHATIKA_DAYS
    lon = moon_longitude % 360.0
    for j in GANDANTA_JUNCTIONS:
        # Signed arc to the junction, wrapping at 0/360.
        d = (lon - j + 180.0) % 360.0 - 180.0
        if abs(d) <= half:
            return {
                "junction": j % 360.0,
                "half_width": round(half, 4),
                "distance": round(d, 4),      # negative = before the junction
                "from": round((j - half) % 360.0, 4),
                "to": round((j + half) % 360.0, 4),
                "citation": "BPHS Vol II ch.92 v.3",
            }
    return None
