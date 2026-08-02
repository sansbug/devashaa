"""Yoga detection — which named BPHS yogas a chart forms.

Each yoga's RESULT text + citation lives in yoga_rules.py (mined from BPHS Vol I
chs 35-39 + Vol II ch.75, Notes excluded). Here is the CONDITION as code: a
predicate over the chart that says whether the yoga is present. A yoga whose BPHS
result is gated on Ṣaḍbala ("if the lord is strong") is detected on its GEOMETRY
and shipped with strength_note — the condition is met, the strength claim refused,
never faked (this engine has no Ṣaḍbala). A few under-specified/complex yogas are
catalogued in yoga_rules but deliberately have no detector yet.

Nothing here asserts an outcome as fate: a detected yoga carries its cited śloka
effect, for the reader to weigh.
"""

from __future__ import annotations

from types import SimpleNamespace

from dignity import RASI_LORD
from drishti import graha_drishti
import yoga_rules
try:
    from motion import _COMBUST_ORB
except Exception:  # pragma: no cover
    _COMBUST_ORB = {"moon": 12.0, "mars": 17.0, "mercury": 14.0, "jupiter": 11.0,
                    "venus": 10.0, "saturn": 15.0}

GRAHAS7 = ("sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn")
KENDRA = frozenset({1, 4, 7, 10})
TRIKONA = frozenset({1, 5, 9})


def _house(rasi: int, ref: int) -> int:
    """Whole-sign house (1-12) of `rasi` counted from reference sign `ref`."""
    return (rasi - ref) % 12 + 1


def _sep(a: float, b: float) -> float:
    d = abs((a - b) % 360.0)
    return min(d, 360.0 - d)


def _build(positions, lagna, lagna_d9):
    g7 = [g for g in GRAHAS7 if g in positions]
    rasi = {g: p["rasi"] for g, p in positions.items()}
    lon = {g: p["longitude"] for g, p in positions.items()}
    vargas = {g: (p.get("vargas") or {}) for g, p in positions.items()}
    d9 = {g: vargas[g].get("D9") for g in positions}

    # dignity state per graha (exalted/own/moolatrikona/friend/neutral/enemy/debilitated)
    import dignity
    state = {}
    for g in positions:
        dd = dignity.dignity_of(g, lon[g])
        state[g] = dd["state"] if dd else None

    house = {g: _house(rasi[g], lagna) for g in rasi}   # from the lagna, all grahas

    # Moon waxing (bright half) from Sun-Moon elongation.
    moon_waxing = None
    if "moon" in lon and "sun" in lon:
        moon_waxing = 0.0 < ((lon["moon"] - lon["sun"]) % 360.0) < 180.0

    # Natural benefics/malefics (ch.34): Jupiter, Venus always; Moon if waxing;
    # Mercury unless conjoined a hard malefic. Nodes are malefic (excluded here).
    benefics = {"jupiter", "venus"}
    if moon_waxing is None or moon_waxing:
        benefics.add("moon")
    if "mercury" in rasi:
        hard = {"sun", "mars", "saturn"}
        if not any(rasi.get(m) == rasi["mercury"] for m in hard):
            benefics.add("mercury")
    malefics = set(g7) - benefics

    lord_of = {h: RASI_LORD[(lagna + h - 1) % 12] for h in range(1, 13)}

    combust = {}
    for g in g7:
        if g == "sun":
            combust[g] = False
        else:
            combust[g] = _sep(lon[g], lon["sun"]) < _COMBUST_ORB.get(g, 12.0)

    return SimpleNamespace(
        g7=g7, rasi=rasi, lon=lon, d9=d9, state=state, house=house,
        moon_waxing=moon_waxing, benefics=benefics, malefics=malefics,
        lord_of=lord_of, lagna=lagna, lagna_d9=lagna_d9, combust=combust)


# --- little predicates on the context -------------------------------------
def _all_in(c, hs):                       # every graha in a house-set
    return all(c.house[g] in hs for g in c.g7)


def _ben_in(c, h):                        # a benefic occupies house h
    return any(g in c.benefics and c.house[g] == h for g in c.g7)


def _mal_in(c, h):
    return any(g in c.malefics and c.house[g] == h for g in c.g7)


def _occ(c, h):                           # any of the 7 occupies house h
    return any(c.house[g] == h for g in c.g7)


def _from_moon(c, g):
    return _house(c.rasi[g], c.rasi["moon"])


def _from_sun(c, g):
    return _house(c.rasi[g], c.rasi["sun"])


def _in_from_moon(c, h, exclude=("sun",)):
    return any(g != "moon" and g not in exclude and _from_moon(c, g) == h for g in c.g7)


def _in_from_sun(c, h, exclude=("moon",)):
    return any(g != "sun" and g not in exclude and _from_sun(c, g) == h for g in c.g7)


def _aspects_full(c, g, target_sign):     # g casts a FULL (7th/special) aspect on target sign
    try:
        return graha_drishti(c.rasi[g], target_sign, g) >= 1.0
    except Exception:
        return False


def _aspects_any(c, g, target_sign):
    try:
        return graha_drishti(c.rasi[g], target_sign, g) > 0
    except Exception:
        return False


def _n_aspecting(c, target_sign, exclude=()):   # how many grahas full-aspect a sign
    return sum(1 for g in c.g7 if g not in exclude and _aspects_full(c, g, target_sign))


def _conjunct(c, a, b):                   # two grahas in the same sign
    return a in c.rasi and b in c.rasi and c.rasi[a] == c.rasi[b]


def _parivartana(c, h1, h2):              # lords of h1,h2 exchange signs
    l1, l2 = c.lord_of[h1], c.lord_of[h2]
    return c.house.get(l1) == h2 and c.house.get(l2) == h1


def _count_state(c, states):              # how many grahas are in one of `states`
    return sum(1 for g in c.g7 if c.state.get(g) in states)


# --- Nābhasa (32; Ardhachandra excluded — no defining śloka) ----------------
def _modality(c, m):                      # 0 movable, 1 fixed, 2 dual
    return all(c.rasi[g] % 3 == m for g in c.g7)


def _dala(c, nature):                     # exactly 3 kendras tenanted, occupants all `nature`
    occ = {h for h in KENDRA if _occ(c, h)}
    if len(occ) != 3:
        return False
    grp = c.benefics if nature == "benefic" else c.malefics
    return all(g in grp for g in c.g7 if c.house[g] in KENDRA)


def _gada(c):
    for a, b in [(1, 4), (4, 7), (7, 10), (10, 1)]:
        if _all_in(c, {a, b}) and _occ(c, a) and _occ(c, b):
            return True
    return False


def _hala(c):
    return any(_all_in(c, t) for t in ({2, 6, 10}, {3, 7, 11}, {4, 8, 12}))


def _vajra(c, ben_houses, mal_houses):    # benefics/malefics split across the two kendra axes
    if not all(_occ(c, h) for h in (1, 4, 7, 10)):
        return False
    for g in c.g7:
        if g in c.benefics and c.house[g] not in ben_houses:
            return False
        if g in c.malefics and c.house[g] not in mal_houses:
            return False
    return True


def _distinct_signs(c):
    return len({c.rasi[g] for g in c.g7})


_NABHASA_NON_SANKHYA = {}   # filled after DETECTORS is defined (for the Saṅkhyā void rule)


def _sankhya(c, n):
    if _distinct_signs(c) != n:
        return False
    for fn in _NABHASA_NON_SANKHYA.values():
        try:
            if fn(c):
                return False   # void if any Āśraya/Dala/Ākṛti is formed
        except Exception:
            pass
    return True


# --- Pañca-Mahāpuruṣa -------------------------------------------------------
def _maha(c, planet):
    return c.state.get(planet) in ("own", "exalted") and c.house.get(planet) in KENDRA


# --- misc helpers for ch.36 / raja -----------------------------------------
def _benefics_in_kendra(c):
    return any(g in c.benefics and c.house[g] in KENDRA for g in c.g7)


def _trimurti(c, ref_lord_house, offsets):
    ref = c.rasi.get(c.lord_of[ref_lord_house])
    if ref is None:
        return False
    return all(any(g in c.benefics and _house(c.rasi[g], ref) == off for g in c.g7) for off in offsets)


def _gajakesari(c):
    j = "jupiter"
    in_kendra = c.house.get(j) in KENDRA or _house(c.rasi[j], c.rasi["moon"]) in KENDRA
    if not in_kendra:
        return False
    helped = any(b != j and b in c.benefics and (_conjunct(c, b, j) or _aspects_any(c, b, c.rasi[j])) for b in c.g7)
    ok = c.state.get(j) not in ("debilitated", "enemy") and not c.combust.get(j, False)
    return helped and ok


def _amala(c):
    for ref in (c.lagna, c.rasi["moon"]):
        occ = [g for g in c.g7 if _house(c.rasi[g], ref) == 10]
        if occ and all(g in c.benefics for g in occ):
            return True
    return False


def _kalpadruma(c):
    p1 = c.lord_of[1]
    if c.rasi.get(p1) is None:
        return False
    p2 = RASI_LORD[c.rasi[p1]]
    p3 = RASI_LORD[c.rasi[p2]]
    if c.d9.get(p3) is None:
        return None       # need D9 — skip rather than assert
    p4 = RASI_LORD[c.d9[p3]]
    good = TRIKONA | KENDRA
    return all(c.house.get(p) in good or c.state.get(p) == "exalted" for p in (p1, p2, p3, p4))


def _kendra_trikona_conj(c):              # (L4|L10) conjunct (L5|L9)
    for a in (c.lord_of[4], c.lord_of[10]):
        for b in (c.lord_of[5], c.lord_of[9]):
            if a != b and _conjunct(c, a, b):
                return True
    return False


DETECTORS = {
    # Nābhasa — Āśraya
    "Rajju": lambda c: _modality(c, 0),
    "Musala": lambda c: _modality(c, 1),
    "Nala": lambda c: _modality(c, 2),
    # Nābhasa — Dala
    "Maala": lambda c: _dala(c, "benefic"),
    "Sarpa": lambda c: _dala(c, "malefic"),
    # Nābhasa — Ākṛti
    "Gada": _gada,
    "Sakata": lambda c: _all_in(c, {1, 7}),
    "Vihaga": lambda c: _all_in(c, {4, 10}),
    "Sringataka": lambda c: _all_in(c, {1, 5, 9}),
    "Hala": _hala,
    "Vajra": lambda c: _vajra(c, {1, 7}, {4, 10}),
    "Yava": lambda c: _vajra(c, {4, 10}, {1, 7}),
    "Kamala": lambda c: _all_in(c, {1, 4, 7, 10}),
    "Vapi": lambda c: _all_in(c, {3, 6, 9, 12}) or _all_in(c, {2, 5, 8, 11}),
    "Yupa": lambda c: _all_in(c, {1, 2, 3, 4}),
    "Sara": lambda c: _all_in(c, {4, 5, 6, 7}),
    "Sakthi": lambda c: _all_in(c, {7, 8, 9, 10}),
    "Danda": lambda c: _all_in(c, {10, 11, 12, 1}),
    "Nauka": lambda c: _all_in(c, {1, 2, 3, 4, 5, 6, 7}),
    "Koota": lambda c: _all_in(c, {4, 5, 6, 7, 8, 9, 10}),
    "Chatra": lambda c: _all_in(c, {7, 8, 9, 10, 11, 12, 1}),
    "Chapa": lambda c: _all_in(c, {10, 11, 12, 1, 2, 3, 4}),
    "Chakra": lambda c: _all_in(c, {1, 3, 5, 7, 9, 11}),
    "Samudra": lambda c: _all_in(c, {2, 4, 6, 8, 10, 12}),
    # Nābhasa — Saṅkhyā (void if any earlier Nābhasa forms)
    "Veena": lambda c: _sankhya(c, 7),
    "Daama": lambda c: _sankhya(c, 6),
    "Paasa": lambda c: _sankhya(c, 5),
    "Kedara": lambda c: _sankhya(c, 4),
    "Soola": lambda c: _sankhya(c, 3),
    "Yuga": lambda c: _sankhya(c, 2),
    "Gola": lambda c: _sankhya(c, 1),

    # Pañca-Mahāpuruṣa
    "Ruchaka": lambda c: _maha(c, "mars"),
    "Bhadra": lambda c: _maha(c, "mercury"),
    "Hamsa": lambda c: _maha(c, "jupiter"),
    "Malavya": lambda c: _maha(c, "venus"),
    "Sasa": lambda c: _maha(c, "saturn"),

    # Lunar
    "Sunapha Yoga": lambda c: _in_from_moon(c, 2) and not _in_from_moon(c, 12),
    "Anapha Yoga": lambda c: _in_from_moon(c, 12) and not _in_from_moon(c, 2),
    "Duradhara (Duradhura) Yoga": lambda c: _in_from_moon(c, 2) and _in_from_moon(c, 12),
    "Kemadruma Yoga": lambda c: not _in_from_moon(c, 2) and not _in_from_moon(c, 12)
        and not any(g not in ("sun", "moon") and c.rasi[g] == c.rasi["moon"] for g in c.g7)
        and not any(g != "sun" and c.house[g] in KENDRA for g in c.g7 if g != "moon"),
    "Adhi Yoga from the Moon": lambda c: all(
        any(g in c.benefics and _from_moon(c, g) == h for g in c.g7) for h in (6, 7, 8)),
    "Dhana Yoga from the Moon (benefics in Upachaya)": lambda c: (
        (lambda n: {"benefics_in_upachaya": n} if n >= 1 else False)(
            sum(1 for g in c.g7 if g in c.benefics and _from_moon(c, g) in {3, 6, 10, 11}))),

    # Solar
    "Vesi Yoga": lambda c: _in_from_sun(c, 2) and not _in_from_sun(c, 12),
    "Vasi (Vosi) Yoga": lambda c: _in_from_sun(c, 12) and not _in_from_sun(c, 2),
    "Ubhayachari Yoga": lambda c: _in_from_sun(c, 2) and _in_from_sun(c, 12),

    # ch.36 "Many Other"
    "Subha Yoga": lambda c: _ben_in(c, 1) or (_ben_in(c, 12) and _ben_in(c, 2)),
    "Asubha Yoga": lambda c: _mal_in(c, 1) or (_mal_in(c, 12) and _mal_in(c, 2)),
    "Gajakesari Yoga": _gajakesari,
    "Amala Yoga": _amala,
    "Parvata Yoga": lambda c: _benefics_in_kendra(c) and not _mal_in(c, 7) and not _mal_in(c, 8),
    "Kahala Yoga": lambda c: (_house(c.rasi[c.lord_of[4]], c.rasi["jupiter"]) in KENDRA)
        or (c.state.get(c.lord_of[4]) in ("own", "exalted") and _conjunct(c, c.lord_of[4], c.lord_of[10])),
    "Chamara Yoga": lambda c: (c.state.get(c.lord_of[1]) == "exalted" and c.house.get(c.lord_of[1]) in KENDRA
        and _aspects_any(c, "jupiter", c.rasi[c.lord_of[1]]))
        or any(sum(1 for g in c.g7 if g in c.benefics and c.house[g] == h) >= 2 for h in (1, 9, 10, 7)),
    "Sankha Yoga": lambda c: (_house(c.rasi[c.lord_of[5]], c.rasi[c.lord_of[6]]) in KENDRA)
        or (_conjunct(c, c.lord_of[1], c.lord_of[10]) and c.rasi[c.lord_of[1]] % 3 == 0),
    "Bheri Yoga": lambda c: all(_occ(c, h) for h in (12, 1, 2, 7))
        or (c.house.get("venus") in KENDRA and c.house.get("jupiter") in KENDRA and c.house.get(c.lord_of[1]) in KENDRA),
    "Srinatha Yoga": lambda c: c.house.get(c.lord_of[7]) == 10 and c.state.get(c.lord_of[10]) == "exalted"
        and _conjunct(c, c.lord_of[10], c.lord_of[9]),
    "Matsya Yoga": lambda c: _ben_in(c, 9) and _ben_in(c, 1) and _mal_in(c, 4) and _mal_in(c, 8)
        and any(g in c.benefics and c.house[g] == 5 for g in c.g7)
        and any(g in c.malefics and c.house[g] == 5 for g in c.g7),
    "Koorma Yoga": lambda c: all(any(g in c.benefics and c.house[g] == h
        and c.state.get(g) in ("own", "exalted", "friend") for g in c.g7) for h in (5, 6, 7))
        and all(any(g in c.malefics and c.house[g] == h and c.state.get(g) in ("own", "exalted")
        for g in c.g7) for h in (3, 11, 1)),
    "Khadga Yoga": lambda c: _parivartana(c, 2, 9) and c.house.get(c.lord_of[1]) in (KENDRA | TRIKONA),
    "Kusuma Yoga": lambda c: c.lagna % 3 == 1 and c.house.get("venus") in KENDRA
        and c.house.get("moon") in TRIKONA
        and any(g in c.benefics and c.rasi[g] == c.rasi["moon"] for g in c.g7 if g != "moon")
        and c.house.get("saturn") == 10,
    "Kalanidhi Yoga": lambda c: c.house.get("jupiter") in (2, 5)
        and (_conjunct(c, "mercury", "jupiter") or _aspects_any(c, "mercury", c.rasi["jupiter"]))
        and (_conjunct(c, "venus", "jupiter") or _aspects_any(c, "venus", c.rasi["jupiter"])),
    "Kalpadruma Yoga (a.k.a. Parijata Yoga)": _kalpadruma,
    "Hari Yoga (Trimurthi)": lambda c: _trimurti(c, 2, (2, 12, 8)),
    "Hara Yoga (Trimurthi)": lambda c: _trimurti(c, 7, (4, 9, 8)),
    "Brahma Yoga (Trimurthi)": lambda c: _trimurti(c, 1, (4, 10, 11)),
    "Lagnadhi Yoga (Adhi Yoga from lagna)": lambda c: _ben_in(c, 7) and _ben_in(c, 8)
        and not any(g in c.benefics and c.house[g] in (7, 8)
                    and any(m in c.malefics and (c.rasi[m] == c.rasi[g] or _aspects_any(c, m, c.rasi[g])) for m in c.g7)
                    for g in c.g7),

    # Rāja (Pārāśarī cluster)
    "Mahā Rāja Yoga (lagna-lord ↔ 5th-lord exchange)": lambda c: _parivartana(c, 1, 5),
    "Benefics in 1st/2nd/4th, malefic in 3rd": lambda c: _ben_in(c, 1) and _ben_in(c, 2) and _ben_in(c, 4) and _mal_in(c, 3),
    "Luminary/benefic exalted in 2nd (wealth)": lambda c: any(
        g in ("moon", "jupiter", "venus", "mercury") and c.house.get(g) == 2 and c.state.get(g) == "exalted" for g in c.g7),
    "Dusthana debilitation + exalted lagna-lord aspecting lagna": lambda c: all(
        any(c.house[g] == h and c.state.get(g) == "debilitated" for g in c.g7) for h in (6, 8, 3))
        and c.state.get(c.lord_of[1]) in ("exalted", "own") and _aspects_full(c, c.lord_of[1], c.lagna),
    "Weak 6/8/12 lords + exalted-or-own lagna-lord aspecting lagna": lambda c: all(
        c.state.get(c.lord_of[h]) in ("debilitated", "enemy") or c.combust.get(c.lord_of[h], False) for h in (6, 8, 12))
        and c.state.get(c.lord_of[1]) in ("own", "exalted") and _aspects_full(c, c.lord_of[1], c.lagna),
    "10th-lord (own/exalted) aspecting lagna; benefics in kendras": lambda c: (
        c.state.get(c.lord_of[10]) in ("own", "exalted") and _aspects_full(c, c.lord_of[10], c.lagna))
        or all(g in c.benefics and c.house[g] in KENDRA for g in c.g7 if g in c.benefics),
    "5th-lord – 9th-lord association (minister yoga)": lambda c: _conjunct(c, c.lord_of[5], c.lord_of[9])
        or (_aspects_full(c, c.lord_of[5], c.rasi[c.lord_of[9]]) and _aspects_full(c, c.lord_of[9], c.rasi[c.lord_of[5]])),
    "4th–10th exchange aspecting 5th & 9th lords": lambda c: _parivartana(c, 4, 10)
        and (_aspects_any(c, c.lord_of[4], c.rasi[c.lord_of[5]]) or _aspects_any(c, c.lord_of[10], c.rasi[c.lord_of[5]]))
        and (_aspects_any(c, c.lord_of[4], c.rasi[c.lord_of[9]]) or _aspects_any(c, c.lord_of[10], c.rasi[c.lord_of[9]])),
    "5th/10th/4th/lagna lords conjoined in the 9th": lambda c: all(c.house.get(c.lord_of[h]) == 9 for h in (5, 10, 4, 1)),
    "Kendra-lord + trikona-lord conjunction (4th/10th with 5th/9th)": _kendra_trikona_conj,
    "5th-lord in kendra with 9th-lord or lagna-lord": lambda c: c.house.get(c.lord_of[5]) in (1, 4, 10)
        and (_conjunct(c, c.lord_of[5], c.lord_of[9]) or _conjunct(c, c.lord_of[5], c.lord_of[1])),
    "Jupiter in own 9th with Venus or 5th-lord": lambda c: c.house.get("jupiter") == 9
        and c.state.get("jupiter") in ("own", "exalted")
        and (_conjunct(c, "jupiter", "venus") or _conjunct(c, "jupiter", c.lord_of[5])),
    "Moon–Venus mutual 3rd/11th or mutual aspect": lambda c: _from_moon(c, "venus") in (3, 11)
        or (_aspects_full(c, "moon", c.rasi["venus"]) and _aspects_full(c, "venus", c.rasi["moon"])),
    "Strong Vargottama Moon aspected by 4+ planets": lambda c: c.d9.get("moon") == c.rasi["moon"]
        and _n_aspecting(c, c.rasi["moon"], exclude=("moon",)) >= 4,
    "Ascendant in Uttamāmśa aspected by 4+ (non-Moon)": lambda c: None if c.lagna_d9 is None
        else (c.lagna_d9 in _EXALT_SIGN and _n_aspecting(c, c.lagna, exclude=("moon",)) >= 4),
    "1–3 planets in exaltation": lambda c: _count_state(c, ("exalted",)) in (1, 2, 3),
    "4 or 5 planets in exaltation or Moolatrikona": lambda c: _count_state(c, ("exalted", "moolatrikona")) in (4, 5),
    "6 planets exalted (emperor)": lambda c: _count_state(c, ("exalted",)) >= 6,
    "Jup/Ven/Mer exalted + a benefic in a kendra": lambda c: any(
        c.state.get(g) == "exalted" for g in ("jupiter", "venus", "mercury")) and _benefics_in_kendra(c),
    "All benefics in kendras, malefics in 3/6/11": lambda c: all(c.house[g] in KENDRA for g in c.g7 if g in c.benefics)
        and all(c.house[g] in {3, 6, 11} for g in c.g7 if g in c.malefics),
}

# Deliberately NO detector (catalogued in yoga_rules, not asserted): the Moon's
# house-class-from-Sun 3-way reading, the day/night Navamsa-aspect lunar yoga, and
# Mridanga (śloka under-specifies which planets) — honest "listed, not detected".

# Any exaltation sign → the graha exalted there (for the lagna-Uttamāṁśa yoga).
_EXALT_SIGN = {0: "sun", 1: "moon", 3: "jupiter", 5: "mercury", 6: "saturn", 9: "mars", 11: "venus"}


def _lagna_d9_exalt(c):
    return c.lagna_d9 in _EXALT_SIGN


# The Saṅkhyā void-rule needs every non-Saṅkhyā Nābhasa detector.
_SANKHYA_NAMES = {"Veena", "Daama", "Paasa", "Kedara", "Soola", "Yuga", "Gola"}
_NABHASA_NAMES = {"Rajju", "Musala", "Nala", "Maala", "Sarpa", "Gada", "Sakata", "Vihaga",
                  "Sringataka", "Hala", "Vajra", "Yava", "Kamala", "Vapi", "Yupa", "Sara",
                  "Sakthi", "Danda", "Nauka", "Koota", "Chatra", "Chapa", "Chakra", "Samudra"}
for _nm in _NABHASA_NAMES:
    _NABHASA_NON_SANKHYA[_nm] = DETECTORS[_nm]


# ── Ṣaḍbala resolution of the strength-gated yogas ──────────────────────────
# BPHS/Raman gate these yogas' results on a graha's Ṣaḍbala strength. With the
# validated Ṣaḍbala engine (shadbala.py) the gate is no longer refused: the yoga
# is resolved to "fructifies" (the required graha is strong) or "does not
# fructify" (it is present in geometry but the strength clause fails). Adhi is
# special — it always forms geometrically, and the office tier follows the
# participating benefics' strength order (balakramat).
def _gate_grahas(name, c):
    """The graha(s) whose Ṣaḍbala the yoga's result hinges on, per the clause that
    fired. An empty list means the satisfied clause carries no strength gate (it
    is fully computable from D1), so the yoga fructifies unconditionally."""
    if name == "Kahala Yoga":
        # Only the primary clause (4th lord / Jupiter mutual kendra) gates on the
        # ascendant lord. The alternative clause (4th lord own/exalted & conjunct
        # the 10th lord) is fully computable from D1 — no Ṣaḍbala gate.
        clause2 = (c.state.get(c.lord_of[4]) in ("own", "exalted")
                   and _conjunct(c, c.lord_of[4], c.lord_of[10]))
        return [] if clause2 else [c.lord_of[1]]       # ascendant lord (primary clause)
    if name == "Bheri Yoga":
        return [c.lord_of[9]]                          # the 9th lord
    if name == "Strong Vargottama Moon aspected by 4+ planets":
        return ["moon"]
    if name == "Sankha Yoga":
        gates = []
        if _house(c.rasi[c.lord_of[5]], c.rasi[c.lord_of[6]]) in KENDRA:
            gates.append(c.lord_of[1])                 # clause 1 → ascendant lord
        if _conjunct(c, c.lord_of[1], c.lord_of[10]) and c.rasi[c.lord_of[1]] % 3 == 0:
            gates.append(c.lord_of[9])                 # clause 2 → 9th lord
        return gates or [c.lord_of[1]]
    return []


_GATE_ROLE = {
    "Kahala Yoga": "ascendant lord",
    "Bheri Yoga": "9th lord",
    "Sankha Yoga": "ascendant / 9th lord",
    "Strong Vargottama Moon aspected by 4+ planets": "the Moon",
}


def _strength_detail(g, sb):
    v = sb.get(g) or {}
    return {"graha": g, "rupa": round(v.get("total_rupa", 0.0), 2),
            "min": v.get("min_required_rupa"), "strong": bool(v.get("strong"))}


def _resolve_strength(name, c, sb):
    """Resolve a strength-gated yoga against the Ṣaḍbala verdict table ``sb``
    ({graha: {strong, total_rupa, min_required_rupa}})."""
    if name == "Adhi Yoga from the Moon":
        parts = [g for g in c.g7 if g in c.benefics and _from_moon(c, g) in (6, 7, 8)]
        ranked = sorted((_strength_detail(g, sb) for g in parts),
                        key=lambda e: -e["rupa"])
        return {
            "resolved": True, "role": "participating benefics (balakramat)",
            "grahas": ranked, "met": any(e["strong"] for e in ranked),
            # geometry forms the yoga; strength orders the office, it never voids it
            "fructifies": True,
            "basis": "the office follows the participants' strength order"
                     + (f"; strongest is {ranked[0]['graha']}" if ranked else ""),
        }
    gates = dict.fromkeys(_gate_grahas(name, c))
    if not gates:
        # Formed via a clause that carries no strength requirement — fully
        # computable from D1, so it fructifies with no Ṣaḍbala gate.
        return {
            "resolved": True, "role": "no strength gate (computable from D1)",
            "grahas": [], "met": True, "fructifies": True,
            "basis": "formed via a clause requiring no Ṣaḍbala — fully computable from D1",
        }
    details = [_strength_detail(g, sb) for g in gates]
    met = any(e["strong"] for e in details)            # either satisfied clause suffices
    return {
        "resolved": True, "role": _GATE_ROLE.get(name, "the required graha"),
        "grahas": details, "met": met, "fructifies": met,
        "basis": ("the " + _GATE_ROLE.get(name, "required graha")
                  + (" is strong (Ṣaḍbala ≥ minimum)" if met
                     else " is not strong, so the yoga does not fructify")),
    }


def detect_yogas(positions: dict, lagna: int, lagna_d9: int | None = None,
                 shadbala: dict | None = None) -> dict:
    """`positions` maps graha key -> {rasi, longitude, vargas}; `lagna` is the
    lagna sign. When ``shadbala`` (the per-graha Ṣaḍbala verdict table) is given,
    strength-gated yogas are resolved to fructifies / does-not-fructify instead
    of carrying the 'strength unverified' flag."""
    c = _build(positions, lagna, lagna_d9)
    detected = []
    for name, meta in yoga_rules.YOGAS.items():
        fn = DETECTORS.get(name)
        if fn is None:
            continue                                   # catalogued, detection not implemented
        try:
            hit = fn(c)
        except Exception:                              # a bad predicate must not sink the rest
            hit = None
        if hit:
            entry = {"name": name, **meta}
            if isinstance(hit, dict):
                entry["detail"] = hit
            if meta.get("computability") == "strength_gated" and shadbala:
                try:
                    entry["strength"] = _resolve_strength(name, c, shadbala)
                except Exception:                      # never let resolution sink the yoga
                    pass
            detected.append(entry)
    return {
        "detected": detected,
        "count": len(detected),
        "checked": sum(1 for n in yoga_rules.YOGAS if n in DETECTORS),
        "catalogued": len(yoga_rules.YOGAS),
        "strength_resolved": bool(shadbala),
        "note": (
            "A yoga is listed only when its geometric condition is met. Strength-gated "
            "yogas are resolved against the Ṣaḍbala engine — 'fructifies' when the gating "
            "graha is strong, 'does not fructify' when the geometry is present but that "
            "strength is lacking. Effects are the cited śloka, not a fated prediction; "
            "no per-yoga score."
        ) if shadbala else (
            "A yoga is listed only when its geometric condition is met. Strength-gated "
            "yogas show 'strength unverified' — the condition holds, but BPHS gates the "
            "result on a Ṣaḍbala this engine does not compute. Effects are the cited "
            "śloka, not a fated prediction; no per-yoga score."
        ),
    }


# Fail loudly at import if a detector name doesn't match the catalogue.
_unknown = [n for n in DETECTORS if n not in yoga_rules.YOGAS]
if _unknown:   # pragma: no cover
    raise RuntimeError(f"yogas.py detectors not in yoga_rules: {_unknown}")
