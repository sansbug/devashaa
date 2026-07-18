"""Ṣoḍaśavarga — the sixteen divisional charts of BPHS chapter 6.

Every rule is transcribed from the ślokas, not from the book's speculum tables
(which are OCR noise in our scan). See docs/bphs-rules.md for the citation of
each rule and the worked examples that pin it down.

Sign indices are 0 = Aries .. 11 = Pisces throughout.
"""

from __future__ import annotations

MOVABLE = {0, 3, 6, 9}      # Aries, Cancer, Libra, Capricorn
FIXED = {1, 4, 7, 10}       # Taurus, Leo, Scorpio, Aquarius
DUAL = {2, 5, 8, 11}        # Gemini, Virgo, Sagittarius, Pisces

FIERY = {0, 4, 8}
EARTHY = {1, 5, 9}
AIRY = {2, 6, 10}
WATERY = {3, 7, 11}

ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO = 0, 1, 2, 3, 4, 5
LIBRA, SCORPIO, SAGITTARIUS, CAPRICORN, AQUARIUS, PISCES = 6, 7, 8, 9, 10, 11


def _is_odd(sign: int) -> bool:
    """Aries/Gemini/Leo/... are 'odd' signs (1st, 3rd, 5th ... of the zodiac)."""
    return sign % 2 == 0  # 0-indexed Aries is the 1st sign, hence odd


def _split(lon: float) -> tuple[int, float]:
    lon %= 360.0
    return int(lon // 30), lon % 30.0


def _mobility_start(sign: int, movable: int, fixed: int, dual: int) -> int:
    if sign in MOVABLE:
        return movable
    if sign in FIXED:
        return fixed
    return dual


# --- the sixteen -----------------------------------------------------------------

def d1_rasi(sign: int, deg: float) -> int:
    """v.5 — the sign itself."""
    return sign


def d2_hora(sign: int, deg: float) -> int:
    """vv.5-6 — odd sign: 1st half Sun's horā, 2nd half Moon's horā; even reversed.

    Sun's horā -> Leo, Moon's horā -> Cancer, so D2 only ever yields those two.
    """
    first_half = deg < 15.0
    sun_hora = first_half if _is_odd(sign) else not first_half
    return LEO if sun_hora else CANCER


def d3_drekkana(sign: int, deg: float) -> int:
    """vv.7-8 — the 1st, 5th and 9th signs from the sign."""
    return (sign + [0, 4, 8][int(deg // 10.0)]) % 12


def d4_chaturthamsa(sign: int, deg: float) -> int:
    """v.9 — the four angles (kendras) from the sign."""
    return (sign + [0, 3, 6, 9][int(deg // 7.5)]) % 12


def d7_saptamsa(sign: int, deg: float) -> int:
    """vv.10-11 — odd: from the same sign; even: from the 7th thereof."""
    part = int(deg // (30.0 / 7.0))
    start = sign if _is_odd(sign) else sign + 6
    return (start + part) % 12


def d9_navamsa(sign: int, deg: float) -> int:
    """v.12 — movable: from itself; fixed: from the 9th; dual: from the 5th."""
    part = int(deg // (30.0 / 9.0))
    start = _mobility_start(sign, sign, sign + 8, sign + 4)
    return (start + part) % 12


def d10_dasamsa(sign: int, deg: float) -> int:
    """vv.13-14 — odd: from the same sign; even: from the 9th."""
    part = int(deg // 3.0)
    start = sign if _is_odd(sign) else sign + 8
    return (start + part) % 12


def d12_dvadasamsa(sign: int, deg: float) -> int:
    """v.15 — always from the same sign."""
    return (sign + int(deg // 2.5)) % 12


def d16_shodasamsa(sign: int, deg: float) -> int:
    """v.16 — movable from Aries, fixed from Leo, dual from Sagittarius."""
    part = int(deg // 1.875)
    start = _mobility_start(sign, ARIES, LEO, SAGITTARIUS)
    return (start + part) % 12


def d20_vimsamsa(sign: int, deg: float) -> int:
    """vv.17-21 — movable from Aries, fixed from Sagittarius, dual from Leo.

    Note the fixed/dual starts are NOT the same as D16's — easy to conflate.
    """
    part = int(deg // 1.5)
    start = _mobility_start(sign, ARIES, SAGITTARIUS, LEO)
    return (start + part) % 12


def d24_siddhamsa(sign: int, deg: float) -> int:
    """vv.22-23 — odd from Leo, even from Cancer."""
    part = int(deg // 1.25)
    start = LEO if _is_odd(sign) else CANCER
    return (start + part) % 12


def d27_bhamsa(sign: int, deg: float) -> int:
    """vv.24-26 — fiery/earthy/airy/watery start from Aries/Cancer/Libra/Capricorn."""
    part = int(deg // (30.0 / 27.0))
    if sign in FIERY:
        start = ARIES
    elif sign in EARTHY:
        start = CANCER
    elif sign in AIRY:
        start = LIBRA
    else:
        start = CAPRICORN
    return (start + part) % 12


# vv.27-28 — irregular spans. (span_degrees, resulting_sign)
_TRIMSAMSA_ODD = [(5.0, ARIES), (5.0, AQUARIUS), (8.0, SAGITTARIUS),
                  (7.0, GEMINI), (5.0, LIBRA)]
_TRIMSAMSA_EVEN = [(5.0, TAURUS), (7.0, VIRGO), (8.0, PISCES),
                   (5.0, CAPRICORN), (5.0, SCORPIO)]


def d30_trimsamsa(sign: int, deg: float) -> int:
    """vv.27-28 — unequal spans ruled by the five non-luminaries.

    Because the Sun and Moon rule no triṁśāṁśa, nothing ever falls in Cancer or
    Leo here. That is the rule, not a bug.
    """
    table = _TRIMSAMSA_ODD if _is_odd(sign) else _TRIMSAMSA_EVEN
    cursor = 0.0
    for span, result in table:
        cursor += span
        if deg < cursor:
            return result
    return table[-1][1]  # exactly 30.0000 -> last division


def d40_khavedamsa(sign: int, deg: float) -> int:
    """vv.29-30 — odd from Aries, even from Libra."""
    part = int(deg // 0.75)
    start = ARIES if _is_odd(sign) else LIBRA
    return (start + part) % 12


def d45_akshavedamsa(sign: int, deg: float) -> int:
    """vv.31-32 — movable from Aries, fixed from Leo, dual from Sagittarius."""
    part = int(deg // (2.0 / 3.0))
    start = _mobility_start(sign, ARIES, LEO, SAGITTARIUS)
    return (start + part) % 12


def d60_shashtiamsa(sign: int, deg: float) -> int:
    """v.33 — degrees x 2, mod 12, counted forward from the sign itself.

    Parāśara: "ignore the sign position ... take the degrees ... Multiply that
    figure by 2 and divide the degrees by 12. Add 1 to the remainder which will
    indicate the sign". The "+1" is inclusive counting, so offset 0 == the sign
    itself. Pinned by his Venus/Capricorn 13°25' -> Pisces example.
    """
    return (sign + int(deg * 2.0) % 12) % 12


# --- registry --------------------------------------------------------------------

VARGAS = [
    ("D1",  "Rāśi",           "Rasi",           d1_rasi),
    ("D2",  "Horā",           "Hora",           d2_hora),
    ("D3",  "Drekkāṇa",       "Drekkana",       d3_drekkana),
    ("D4",  "Chaturthāṁśa",   "Chaturthamsa",   d4_chaturthamsa),
    ("D7",  "Saptāṁśa",       "Saptamsa",       d7_saptamsa),
    ("D9",  "Navāṁśa",        "Navamsa",        d9_navamsa),
    ("D10", "Daśāṁśa",        "Dasamsa",        d10_dasamsa),
    ("D12", "Dvādaśāṁśa",     "Dvadasamsa",     d12_dvadasamsa),
    ("D16", "Ṣoḍaśāṁśa",      "Shodasamsa",     d16_shodasamsa),
    ("D20", "Viṁśāṁśa",       "Vimsamsa",       d20_vimsamsa),
    ("D24", "Chaturviṁśāṁśa", "Siddhamsa",      d24_siddhamsa),
    ("D27", "Saptaviṁśāṁśa",  "Bhamsa",         d27_bhamsa),
    ("D30", "Triṁśāṁśa",      "Trimsamsa",      d30_trimsamsa),
    ("D40", "Khavedāṁśa",     "Khavedamsa",     d40_khavedamsa),
    ("D45", "Akṣavedāṁśa",    "Akshavedamsa",   d45_akshavedamsa),
    ("D60", "Ṣaṣṭiāṁśa",      "Shashtiamsa",    d60_shashtiamsa),
]

VARGA_BY_KEY = {key: fn for key, _, _, fn in VARGAS}


def varga_sign(key: str, sidereal_longitude: float) -> int:
    """Divisional sign for a *sidereal* longitude. `key` is e.g. 'D9'."""
    sign, deg = _split(sidereal_longitude)
    return VARGA_BY_KEY[key](sign, deg)


def all_vargas(sidereal_longitude: float) -> dict[str, int]:
    sign, deg = _split(sidereal_longitude)
    return {key: fn(sign, deg) for key, _, _, fn in VARGAS}
