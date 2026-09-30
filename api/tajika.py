"""Tājika — the annual-chart toolkit. Tier `tajika`, never blended with BPHS.

SOURCES (registered in docs/classical-sources-policy.md):
  tajika_nilakanthi  Nīlakaṇṭha Daivajña, Tājika-Nīlakaṇṭhī (1587). D.P. Saxena
                     tr., Ranjan Publications. Cited "TN p.N (śl. M)" — the book's
                     page, with the śloka number where the page prints one.
  charak_varshaphala K.S. Charak, A Textbook of Varshaphala. Modern tier. Its
                     Example Chart (the 41st year of Rajiv Gandhi, 20 Aug 1984)
                     is worked to the sub-unit for every strength below and is
                     the fixture in test_tajika.py.
  raman_varshaphal   B.V. Raman, Varshaphal or the Hindu Progressed Horoscope.
                     Modern tier; corroborates the unit table and the tri-rāśi
                     lords.

WHAT IS HERE
  relations      the Tājika friendship: 3/5/9/11 friend, 1/4/7/10 enemy,
                 2/6/8/12 neutral, from mutual placement — TN p.40 (śl. 41-42)
  pañcavargīya   kṣetra · uccha · hadda · drekkāṇa · navāṁśa, in units;
                 Viśva-bala = total/4 — TN p.40-41, Charak ch.VI
  harṣa bala     four 5-unit joys — TN p.87, Charak ch.VI
  varṣeśa        the year-lord from the five office-bearers — TN p.50-52,
                 Charak ch.VII
  dṛṣṭi          the twelve-house aspect values with degree interpolation —
                 TN p.56-58 (śl. 77-82)
  yogas          the sixteen, from itthaśāla outward — TN ch.2, Charak ch.X
  sahams         the fifty, with the +30 rule, lords, strength, timing —
                 TN ch.3, Charak ch.XI

WHAT IS NOT: any phala text. Every function returns geometry, a rule and a
citation; the sentence a reader might want is refused upstream.
"""
from __future__ import annotations

import swisseph as swe

import vargas
from dignity import RASI_LORD, EXALTATION, DEBILITATION
from motion import _COMBUST_ORB, _COMBUST_ORB_RETRO

TIER = "tajika"
SEVEN = ["sun", "moon", "mars", "mercury", "jupiter", "venus", "saturn"]
# fastest → slowest (Charak p.117): the fast one must be BEHIND to form itthaśāla
SPEED_ORDER = ["moon", "mercury", "venus", "sun", "mars", "jupiter", "saturn"]
MALE = {"sun", "mars", "jupiter"}
FEMALE = {"moon", "mercury", "venus", "saturn"}          # TN p.84: no eunuchs in Tājika
NATURAL_MALEFIC = {"sun", "mars", "saturn"}
KENDRA = {1, 4, 7, 10}
PANAPHARA = {2, 5, 8, 11}
APOKLIMA = {3, 6, 9, 12}
TRIK = {6, 8, 12}

# Deeptāṁśa — the orb of each graha (Charak Table X-1; TN śl. 79 "sun 15 …")
DEEPTAMSA = {"sun": 15.0, "moon": 12.0, "mars": 8.0, "mercury": 7.0,
             "jupiter": 9.0, "venus": 7.0, "saturn": 9.0}

# Tājika dṛṣṭi, by the HOUSE of the aspected graha counted from the aspecting
# one. TN p.57 table ("Balance signs 1..12 / Numbers 0 40 15 45 0 60 0 45 15 10
# 0 60") and śl. 77-78: 5th/9th pādona (¾), 3rd tryaṁśona (⅔), 11th ṣaḍbhāga
# (⅙), 4th/10th pāda (¼), 7th and same sign full — open enmity.
DRISHTI = {1: 60.0, 2: 0.0, 3: 40.0, 4: 15.0, 5: 45.0, 6: 0.0,
           7: 60.0, 8: 0.0, 9: 45.0, 10: 15.0, 11: 10.0, 12: 0.0}
DRISHTI_KIND = {1: "open enemy", 7: "open enemy", 4: "secret enemy", 10: "secret enemy",
                5: "open friend", 9: "open friend", 3: "secret friend", 11: "secret friend"}
ASPECT_HOUSES = {h for h, v in DRISHTI.items() if v > 0}

# Hadda (Arabic ḥadd, "bound") — the Egyptian terms, per sign as (upper bound
# °, lord). Charak Table VI-4 (verified row by row; every sign sums to 30) and
# Raman p.20; identical to Ptolemy's "terms according to the Egyptians".
HADDA = [
    [(6, "jupiter"), (12, "venus"), (20, "mercury"), (25, "mars"), (30, "saturn")],   # Meṣa
    [(8, "venus"), (14, "mercury"), (22, "jupiter"), (27, "saturn"), (30, "mars")],   # Vṛṣabha
    [(6, "mercury"), (12, "jupiter"), (17, "venus"), (24, "mars"), (30, "saturn")],   # Mithuna
    [(7, "mars"), (13, "venus"), (19, "mercury"), (26, "jupiter"), (30, "saturn")],   # Karka
    [(6, "jupiter"), (11, "venus"), (18, "saturn"), (24, "mercury"), (30, "mars")],   # Siṁha
    [(7, "mercury"), (17, "venus"), (21, "jupiter"), (28, "mars"), (30, "saturn")],   # Kanyā
    [(6, "saturn"), (14, "mercury"), (21, "jupiter"), (28, "venus"), (30, "mars")],   # Tulā
    [(7, "mars"), (11, "venus"), (19, "mercury"), (24, "jupiter"), (30, "saturn")],   # Vṛścika
    [(12, "jupiter"), (17, "venus"), (21, "mercury"), (26, "saturn"), (30, "mars")],  # Dhanu
    [(7, "mercury"), (14, "jupiter"), (22, "venus"), (26, "saturn"), (30, "mars")],   # Makara
    [(7, "mercury"), (13, "venus"), (20, "jupiter"), (25, "mars"), (30, "saturn")],   # Kumbha
    [(12, "venus"), (16, "jupiter"), (19, "mercury"), (28, "mars"), (30, "saturn")],  # Mīna
]
# Tājika drekkāṇa lords run in the Chaldean order through the 36 decans from
# Meṣa-1 = Mars (Charak Table VI-6). NOT the Parāśarī drekkāṇa.
_CHALDEAN = ["mars", "sun", "venus", "mercury", "moon", "saturn", "jupiter"]

# Tri-rāśi lords by varṣa lagna, (day, night) — TN p.50, Charak Table VII-1,
# Raman p.25 all agree.
TRIRASI = {0: ("sun", "jupiter"), 1: ("venus", "moon"), 2: ("saturn", "mercury"),
           3: ("venus", "mars"), 4: ("jupiter", "sun"), 5: ("moon", "venus"),
           6: ("mercury", "saturn"), 7: ("mars", "venus"), 8: ("saturn", "saturn"),
           9: ("mars", "mars"), 10: ("jupiter", "jupiter"), 11: ("moon", "moon")}

# Harṣa-sthāna: the house from the varṣa lagna where each graha is "happy" —
# TN p.87, Charak p.51.
HARSHA_STHANA = {"sun": 9, "moon": 3, "mars": 6, "mercury": 1, "jupiter": 11, "venus": 5, "saturn": 12}
# Pañcavargīya units by relation (own, friend, neutral, enemy) — TN p.40, Charak Table VI-3
PV_UNITS = {"kshetra": (30.0, 22.5, 15.0, 7.5), "hadda": (15.0, 11.25, 7.5, 3.75),
            "drekkana": (10.0, 7.5, 5.0, 2.5), "navamsa": (5.0, 3.75, 2.5, 1.25)}
_REL_IDX = {"own": 0, "friend": 1, "neutral": 2, "enemy": 3}


# ── geometry helpers ─────────────────────────────────────────────────────────

def house_from(sign_from: int, sign_to: int) -> int:
    return (sign_to - sign_from) % 12 + 1


def split(lon: float) -> tuple[int, float]:
    lon %= 360.0
    s = int(lon // 30)
    return s, lon - s * 30.0


def hadda_lord(sign: int, deg: float) -> str:
    for ub, lord in HADDA[sign]:
        if deg < ub:
            return lord
    return HADDA[sign][-1][1]


def drekkana_lord(sign: int, deg: float) -> str:
    return _CHALDEAN[(sign * 3 + min(2, int(deg // 10))) % 7]


def navamsa_lord(sign: int, deg: float) -> str:
    return RASI_LORD[vargas.d9_navamsa(sign, deg)]


def tajika_relation(p: str, q: str, signs: dict[str, int]) -> str:
    """Friend 3/5/9/11, enemy 1/4/7/10, neutral 2/6/8/12 — by MUTUAL placement
    in this chart, not by nature (TN p.40 śl. 41-42; Charak p.53). Symmetric."""
    if p == q:
        return "own"
    h = house_from(signs[p], signs[q])
    if h in (3, 5, 9, 11):
        return "friend"
    if h in (1, 4, 7, 10):
        return "enemy"
    return "neutral"


def drishti_value(from_lon: float, to_lon: float) -> tuple[float, int]:
    """Strength of the aspect FROM one point ON another, 0-60, interpolated by
    the degrees beyond the whole signs (TN p.57-58, worked Sun→Moon 49.2)."""
    d = (to_lon - from_lon) % 360.0
    b = int(d // 30)
    x = d - b * 30.0
    h = b + 1
    v0, v1 = DRISHTI[h], DRISHTI[h % 12 + 1]
    return v0 + (v1 - v0) * x / 30.0, h


# ── the chart as this module sees it ─────────────────────────────────────────

class Ctx:
    """Positions of the seven (plus nodes where present), the lagna, day/night."""

    def __init__(self, grahas: list[dict], lagna_lon: float, is_day: bool):
        self.lon = {g["key"]: float(g["longitude"]) % 360.0 for g in grahas}
        self.retro = {g["key"]: bool(g.get("retrograde")) for g in grahas}
        self.sign = {k: split(v)[0] for k, v in self.lon.items()}
        self.deg = {k: split(v)[1] for k, v in self.lon.items()}
        self.lagna_lon = lagna_lon % 360.0
        self.lagna = int(self.lagna_lon // 30)
        self.is_day = is_day
        self.house = {k: house_from(self.lagna, s) for k, s in self.sign.items()}
        self.lagna_lord = RASI_LORD[self.lagna]
        sun, moon = self.lon["sun"], self.lon["moon"]
        self.moon_waxing = ((moon - sun) % 360.0) < 180.0

    def aspects(self, p: str, q: str) -> bool:
        return DRISHTI[house_from(self.sign[p], self.sign[q])] > 0

    def orb(self, p: str, q: str) -> float:
        return (DEEPTAMSA[p] + DEEPTAMSA[q]) / 2.0

    def combust(self, p: str) -> bool:
        if p == "sun" or p not in self.lon:
            return False
        sep = abs(((self.lon[p] - self.lon["sun"] + 180.0) % 360.0) - 180.0)
        orb = _COMBUST_ORB_RETRO.get(p) if (self.retro.get(p) and p in _COMBUST_ORB_RETRO) else _COMBUST_ORB.get(p)
        return orb is not None and sep <= orb

    def benefic(self, p: str) -> bool:
        """Jupiter, Venus, the waxing Moon, and Mercury when not with a malefic
        (TN p.46, Charak p.46)."""
        if p in ("jupiter", "venus"):
            return True
        if p == "moon":
            return self.moon_waxing
        if p == "mercury":
            return not any(self.sign[m] == self.sign["mercury"] for m in NATURAL_MALEFIC)
        return False

    def state(self, p: str) -> dict:
        s, d = self.sign[p], self.deg[p]
        own_sign = RASI_LORD[s] == p
        exalted = EXALTATION[p][0] == s
        debil = DEBILITATION[p][0] == s
        hl, dl, nl = hadda_lord(s, d), drekkana_lord(s, d), navamsa_lord(s, d)
        enemy_sign = (not own_sign) and tajika_relation(p, RASI_LORD[s], self.sign) == "enemy"
        conj = [q for q in SEVEN if q != p and self.sign[q] == s]
        aspected_by = [q for q in SEVEN if q != p and DRISHTI[house_from(self.sign[q], s)] > 0]
        malefic_aff = any(q in NATURAL_MALEFIC for q in conj) or any(q in NATURAL_MALEFIC for q in aspected_by)
        benefic_asp = any(self.benefic(q) for q in aspected_by) or any(self.benefic(q) for q in conj)
        strong = exalted or own_sign or hl == p or dl == p or nl == p
        weak_flags = [f for f, on in (("retrograde", self.retro.get(p, False)), ("combust", self.combust(p)),
                                      ("debilitated", debil), ("in 6/8/12", self.house[p] in TRIK),
                                      ("enemy sign", enemy_sign), ("malefic-afflicted", malefic_aff)) if on]
        dignity = [f for f, on in (("exalted", exalted), ("own sign", own_sign), ("own hadda", hl == p),
                                   ("own drekkāṇa", dl == p), ("own navāṁśa", nl == p)) if on]
        shunya = (not strong) and (not debil) and (not enemy_sign) and not conj and not aspected_by
        grade = ("uttama" if (exalted or own_sign) else
                 "madhyama" if (hl == p or dl == p or nl == p) else
                 "adhama" if (debil or enemy_sign) else "sama")
        return {"sign": s, "deg": round(d, 4), "house": self.house[p], "own_sign": own_sign, "exalted": exalted,
                "debilitated": debil, "hadda_lord": hl, "drekkana_lord": dl, "navamsa_lord": nl,
                "enemy_sign": enemy_sign, "retrograde": self.retro.get(p, False), "combust": self.combust(p),
                "conjunct": conj, "aspected_by": aspected_by, "malefic_afflicted": malefic_aff,
                "benefic_aspect": benefic_asp, "strong": strong, "weak": bool(weak_flags),
                "weak_flags": weak_flags, "dignity": dignity, "shunya_marga": shunya, "grade": grade}


# ── strengths ────────────────────────────────────────────────────────────────

def pancha_vargiya(ctx: Ctx) -> dict:
    """Five sources in units (TN p.40-41; Charak Table VI-3, VI-10). Viśva-bala
    = total/4; >15 parākramī, 10-15 pūrṇa, 5-10 madhya, <5 alpa (Charak p.62)."""
    out = {}
    for p in SEVEN:
        s, d, lon = ctx.sign[p], ctx.deg[p], ctx.lon[p]
        row, total = {}, 0.0
        for comp, lord in (("kshetra", RASI_LORD[s]), ("hadda", hadda_lord(s, d)),
                           ("drekkana", drekkana_lord(s, d)), ("navamsa", navamsa_lord(s, d))):
            rel = tajika_relation(p, lord, ctx.sign)
            u = PV_UNITS[comp][_REL_IDX[rel]]
            row[comp] = {"units": u, "lord": lord, "relation": rel}
            total += u
        ds, dd = DEBILITATION[p]
        deb_lon = ds * 30.0 + dd
        dist = abs(((lon - deb_lon + 180.0) % 360.0) - 180.0)
        u = dist / 9.0
        row["uchcha"] = {"units": round(u, 4), "debilitation_point": deb_lon, "distance": round(dist, 4)}
        total += u
        vb = total / 4.0
        cat = "parakrami" if vb > 15 else "purna" if vb >= 10 else "madhya" if vb >= 5 else "alpa"
        out[p] = {**row, "total": round(total, 4), "vishwa_bala": round(vb, 4), "category": cat}
    return out


def harsha_bala(ctx: Ctx) -> dict:
    """Four joys of 5 units each (TN p.87; Charak p.51-52): the harṣa-sthāna,
    exaltation or own sign, a house of one's own sex, and the day/night of the
    praveśa. Max 20; 15 pūrṇa, 10 madhya, 5 alpa, 0 nirbala."""
    out = {}
    for p in SEVEN:
        h = ctx.house[p]
        sthana = 5.0 if h == HARSHA_STHANA[p] else 0.0
        uccha = 5.0 if (EXALTATION[p][0] == ctx.sign[p] or RASI_LORD[ctx.sign[p]] == p) else 0.0
        if p in FEMALE:
            sex = 5.0 if h in (1, 2, 3, 7, 8, 9) else 0.0
            dn = 5.0 if not ctx.is_day else 0.0
        else:
            sex = 5.0 if h in (4, 5, 6, 10, 11, 12) else 0.0
            dn = 5.0 if ctx.is_day else 0.0
        tot = sthana + uccha + sex + dn
        cat = "purna" if tot >= 15 else "madhya" if tot >= 10 else "alpa" if tot >= 5 else "nirbala"
        out[p] = {"sthana": sthana, "uchcha_swakshetra": uccha, "stri_purusha": sex, "dina_ratri": dn,
                  "total": tot, "category": cat}
    return out


def office_bearers(ctx: Ctx, muntha_sign: int, janma_lagna: int) -> dict:
    trirasi = TRIRASI[ctx.lagna][0 if ctx.is_day else 1]
    dinaratri = RASI_LORD[ctx.sign["sun"]] if ctx.is_day else RASI_LORD[ctx.sign["moon"]]
    return {"muntha_lord": RASI_LORD[muntha_sign], "janma_lagna_lord": RASI_LORD[janma_lagna],
            "varsha_lagna_lord": ctx.lagna_lord, "trirasi_lord": trirasi, "dinaratri_lord": dinaratri,
            "rule": ("tri-rāśi lord by the varṣa lagna and day/night (TN p.50); dina-rātri lord = lord of "
                     "the Sun's sign by day, of the Moon's sign by night (TN p.50, Charak p.77)")}


def varshesha(ctx: Ctx, pv: dict, bearers: dict) -> dict:
    """The year-lord (TN p.50-52; Charak p.78-80). Strongest office-bearer by
    Viśva-bala that ASPECTS the varṣa lagna; ties by portfolios; none aspecting
    → the Muntha lord; the Moon never rules the year (Charak p.80)."""
    roles = [("muntha", bearers["muntha_lord"]), ("janma_lagna", bearers["janma_lagna_lord"]),
             ("varsha_lagna", bearers["varsha_lagna_lord"]), ("trirasi", bearers["trirasi_lord"]),
             ("dinaratri", bearers["dinaratri_lord"])]
    port: dict[str, list[str]] = {}
    for r, p in roles:
        port.setdefault(p, []).append(r)
    contenders, steps = [], []
    for p, rs in port.items():
        val, h = drishti_value(ctx.lon[p], ctx.lagna_lon)
        asp = DRISHTI[house_from(ctx.sign[p], ctx.lagna)] > 0
        contenders.append({"planet": p, "roles": rs, "portfolios": len(rs), "vishwa_bala": pv[p]["vishwa_bala"],
                           "aspects_lagna": asp, "aspect_house": house_from(ctx.sign[p], ctx.lagna),
                           "aspect_value": round(val, 2), "aspect_kind": DRISHTI_KIND.get(house_from(ctx.sign[p], ctx.lagna))})
    contenders.sort(key=lambda c: (-c["vishwa_bala"], -c["portfolios"]))
    strongest = contenders[0]["planet"]
    pool = [c for c in contenders if c["aspects_lagna"]]
    moon_note = None
    if any(c["planet"] == "moon" for c in pool):
        moon_note = "the Moon is not made year-lord even when strongest and aspecting (Charak p.80)"
        pool = [c for c in pool if c["planet"] != "moon"]
    if not pool:
        winner, why = bearers["muntha_lord"], "no office-bearer aspects the varṣa lagna → the Muntha lord (Charak p.79 4a)"
    else:
        best = pool[0]
        if best["vishwa_bala"] < 5:
            winner, why = bearers["muntha_lord"], "the strongest aspecting office-bearer is below 5 units → the Muntha lord (Charak p.79 4b)"
        else:
            tied = [c for c in pool if abs(c["vishwa_bala"] - best["vishwa_bala"]) < 1e-9]
            if len(tied) > 1:
                tied.sort(key=lambda c: -c["portfolios"])
                if tied[0]["portfolios"] == tied[1]["portfolios"]:
                    winner, why = bearers["muntha_lord"], "equal strength, aspect and portfolios → the Muntha lord (Charak p.79 4c)"
                else:
                    winner, why = tied[0]["planet"], "equal strength; the one holding more portfolios (Charak p.78 §3)"
            else:
                winner, why = best["planet"], "strongest office-bearer that aspects the varṣa lagna (Charak p.78 §1-2; TN p.51)"
    for c in contenders:
        if c["planet"] == strongest and not c["aspects_lagna"]:
            steps.append(f"{strongest} is strongest ({c['vishwa_bala']:.3f}) but does not aspect the lagna "
                         f"(lagna is its {c['aspect_house']}th) — excluded")
    steps.append(why)
    return {"lord": winner, "contenders": contenders, "steps": steps, "moon_note": moon_note,
            "rule": "TN p.50-52; Charak ch.VII"}


# ── aspects ──────────────────────────────────────────────────────────────────

def drishti_matrix(ctx: Ctx) -> dict:
    out = {}
    for p in SEVEN:
        row = {}
        for q in SEVEN:
            if p == q:
                continue
            v, h = drishti_value(ctx.lon[p], ctx.lon[q])
            row[q] = {"value": round(v, 2), "house": h, "kind": DRISHTI_KIND.get(h), "mutual": ctx.aspects(p, q)}
        out[p] = row
    return {"matrix": out, "deeptamsa": DEEPTAMSA, "table": DRISHTI, "rule": "TN p.56-58 śl. 77-82"}


# ── itthaśāla family ─────────────────────────────────────────────────────────

def _fast_slow(p: str, q: str) -> tuple[str, str]:
    return (p, q) if SPEED_ORDER.index(p) < SPEED_ORDER.index(q) else (q, p)


def itthasala(ctx: Ctx, p: str, q: str) -> dict | None:
    """Vartamāna / pūrṇa / bhaviṣyat (Charak p.118-125, Table X-3; TN p.61).
    The fast graha must be BEHIND the slow one in degrees within their signs,
    in mutual aspect, within the mean of their deeptāṁśas."""
    fast, slow = _fast_slow(p, q)
    df, ds = ctx.deg[fast], ctx.deg[slow]
    orb = ctx.orb(fast, slow)
    if ctx.aspects(fast, slow):
        if abs(ds - df) <= 1.0:
            return {"type": "purna", "fast": fast, "slow": slow, "gap": round(ds - df, 3), "orb": orb}
        if df < ds and ds - df <= orb:
            return {"type": "vartamana", "fast": fast, "slow": slow, "gap": round(ds - df, 3), "orb": orb}
        if df < ds and ds - df <= DEEPTAMSA[fast] + DEEPTAMSA[slow]:
            return {"type": "bhavishyat", "variant": "beyond the mean orb, within the sum (Charak p.125 note)",
                    "fast": fast, "slow": slow, "gap": round(ds - df, 3), "orb": orb}
    if df >= 29.0:      # rāśyanta: the fast graha works from the next sign (Charak p.119)
        nsign = (ctx.sign[fast] + 1) % 12
        if DRISHTI[house_from(nsign, ctx.sign[slow])] > 0 and ds <= orb:
            return {"type": "bhavishyat", "variant": "rāśyanta — the fast graha at 29°+ operates from the next sign",
                    "fast": fast, "slow": slow, "gap": round(ds, 3), "orb": orb}
    return None


def isarapha(ctx: Ctx, p: str, q: str) -> dict | None:
    """The fast graha AHEAD of the slow by more than a degree, in mutual aspect —
    separation (Charak p.121, Table X-3; TN p.61)."""
    fast, slow = _fast_slow(p, q)
    df, ds = ctx.deg[fast], ctx.deg[slow]
    if ctx.aspects(fast, slow) and df - ds > 1.0:
        return {"fast": fast, "slow": slow, "separation": round(df - ds, 3)}
    return None


def yogas(ctx: Ctx, pv: dict) -> dict:
    """The sixteen, evaluated between the lagneśa and the lord of every house
    (Charak p.110: in the annual chart any house may be taken as the 'question').
    Definitions per Charak Table X-3 with TN's chapter-2 ślokas."""
    st = {p: ctx.state(p) for p in SEVEN}
    houses = {p: ctx.house[p] for p in SEVEN}
    ikka = all(houses[p] in KENDRA | PANAPHARA for p in SEVEN)
    indu = all(houses[p] in APOKLIMA for p in SEVEN)
    n_apo = sum(1 for p in SEVEN if houses[p] in APOKLIMA)
    pairs = []
    for i, p in enumerate(SEVEN):
        for q in SEVEN[i + 1:]:
            it = itthasala(ctx, p, q)
            isr = isarapha(ctx, p, q)
            if it or isr:
                pairs.append({"a": p, "b": q, "itthasala": it, "isarapha": isr})
    L = ctx.lagna_lord
    per_house = {}
    for k in range(2, 13):
        K = RASI_LORD[(ctx.lagna + k - 1) % 12]
        row = {"karyesha": K, "same_lord": K == L}
        if K == L:
            per_house[k] = row
            continue
        it = itthasala(ctx, L, K)
        row["itthasala"] = it
        row["isarapha"] = isarapha(ctx, L, K)
        fast, slow = _fast_slow(L, K)
        mutual = ctx.aspects(L, K)
        # nakta / yamayā: no mutual aspect; an intermediary aspecting both from within orb
        if not mutual:
            for name, faster in (("nakta", True), ("yamaya", False)):
                found = []
                for X in SEVEN:
                    if X in (L, K):
                        continue
                    xi = SPEED_ORDER.index(X)
                    cond = (xi < min(SPEED_ORDER.index(L), SPEED_ORDER.index(K))) if faster \
                        else (xi > max(SPEED_ORDER.index(L), SPEED_ORDER.index(K)))
                    if not cond or not (ctx.aspects(X, L) and ctx.aspects(X, K)):
                        continue
                    lo, hi = sorted((ctx.deg[L], ctx.deg[K]))
                    if lo < ctx.deg[X] < hi and abs(ctx.deg[X] - ctx.deg[L]) <= ctx.orb(X, L) \
                            and abs(ctx.deg[X] - ctx.deg[K]) <= ctx.orb(X, K):
                        found.append(X)
                if found:
                    row[name] = {"via": found}
        if it:
            # manau: Mars/Saturn casting an inimical aspect (1/4/7/10) on the faster
            for m in ("mars", "saturn"):
                if m not in (L, K) and house_from(ctx.sign[m], ctx.sign[fast]) in (1, 4, 7, 10):
                    row.setdefault("manau", []).append(m)
            # kambūla: the Moon in itthaśāla with either lord
            mi = None
            for lord in (L, K):
                if lord != "moon":
                    mi = mi or itthasala(ctx, "moon", lord)
            if "moon" not in (L, K):
                lords_grade = min((st[L]["grade"], st[K]["grade"]), key=["uttama", "madhyama", "sama", "adhama"].index)
                if mi:
                    row["kambula"] = {"with": mi["slow"] if mi["fast"] == "moon" else mi["fast"], "type": mi["type"],
                                      "moon": st["moon"]["grade"], "lords": lords_grade,
                                      "label": f"{lords_grade}-{st['moon']['grade']}"}
                else:
                    mdeg = ctx.deg["moon"]
                    nodig = not st["moon"]["dignity"]
                    if mdeg >= 29.0 and nodig:
                        nsign = (ctx.sign["moon"] + 1) % 12
                        hits = [lord for lord in (L, K)
                                if DRISHTI[house_from(nsign, ctx.sign[lord])] > 0 and ctx.deg[lord] <= ctx.orb("moon", lord)]
                        if hits:
                            row["gairi_kambula"] = {"with": hits}
                    if nodig and st["moon"]["shunya_marga"] and ctx.sign["moon"] not in (ctx.sign[L], ctx.sign[K]):
                        row["khallasara"] = True
            # rudda / duphālikuttha / manau are qualities of the itthaśāla
            wk = {p: st[p]["weak_flags"] for p in (L, K) if st[p]["weak"]}
            if wk:
                row["rudda"] = {"weak": wk, "fast_weak": fast in wk}
            if st[slow]["strong"] and not (st[fast]["exalted"] or st[fast]["own_sign"]):
                row["duphalikuttha"] = {"slow_strong": st[slow]["dignity"], "fast": fast}
        # dutthottha-dāvīra: both weak, one in itthaśāla with a strong third
        if st[L]["weak"] and st[K]["weak"]:
            helpers = [X for X in SEVEN if X not in (L, K) and (st[X]["exalted"] or st[X]["own_sign"])
                       and (itthasala(ctx, L, X) or itthasala(ctx, K, X))]
            if helpers:
                row["dutthottha"] = {"via": helpers}
        # tambīra: no mutual aspect; kāryeśa at rāśyanta; on entering the next sign, itthaśāla with L and a strong graha
        if not mutual and ctx.deg[K] >= 29.0:
            nsign = (ctx.sign[K] + 1) % 12
            if DRISHTI[house_from(nsign, ctx.sign[L])] > 0 and ctx.deg[L] <= ctx.orb(K, L):
                strong3 = [X for X in SEVEN if X not in (L, K) and (st[X]["strong"] or st[X]["own_sign"])
                           and DRISHTI[house_from(nsign, ctx.sign[X])] > 0 and ctx.deg[X] <= ctx.orb(K, X)]
                if strong3:
                    row["tambira"] = {"with": strong3}
        # kuttha / durpha
        if st[L]["strong"] and st[K]["strong"] and houses[L] in KENDRA | PANAPHARA and houses[K] in KENDRA | PANAPHARA \
                and (st[L]["benefic_aspect"] or st[K]["benefic_aspect"]) and not (st[L]["malefic_afflicted"] or st[K]["malefic_afflicted"]):
            row["kuttha"] = True
        if st[L]["weak"] and st[K]["weak"] and houses[L] in TRIK and houses[K] in TRIK \
                and (st[L]["combust"] or st[L]["retrograde"]) and (st[K]["combust"] or st[K]["retrograde"]):
            row["durpha"] = True
        per_house[k] = row
    return {"ikkavala": {"present": ikka, "rule": "all seven in kendras or paṇapharas (TN śl. 3; Charak p.112)"},
            "induvara": {"present": indu, "partial": n_apo >= 5, "in_apoklimas": n_apo,
                         "rule": "all seven in apoklimas 3/6/9/12 (TN śl. 3; Charak p.114)"},
            "lagnesha": L, "pairs": pairs, "houses": per_house, "states": st,
            "rule": "Charak Table X-3; TN ch.2 śl. 1-61"}


# ── sahams ───────────────────────────────────────────────────────────────────

# (key, gloss, day-formula, night-formula) with terms as names; None night = same
# as day. Formula = a − b + c, +30 if c does not lie in the arc from b forward to
# a (TN p.93; Charak p.157). TN p.93-101 for the fifty; Charak ch.XI for the gloss.
SAHAMS = [
    ("punya", "fortune / auspiciousness", ("moon", "sun", "asc"), ("sun", "moon", "asc")),
    ("vidya", "learning (guru)", ("sun", "moon", "asc"), ("moon", "sun", "asc")),
    ("jnana", "knowledge (= vidya)", ("sun", "moon", "asc"), ("moon", "sun", "asc")),
    ("yasha", "fame", ("jupiter", "saham:punya", "asc"), ("saham:punya", "jupiter", "asc")),
    ("mitra", "friends", ("saham:vidya", "saham:punya", "venus"), ("saham:punya", "saham:vidya", "venus")),
    ("mahatmya", "greatness", ("saham:punya", "mars", "asc"), ("mars", "saham:punya", "asc")),
    ("asha", "hope", ("saturn", "venus", "asc"), ("venus", "saturn", "asc")),
    ("samarthya", "capability", ("mars", "lord_asc", "asc"), ("lord_asc", "mars", "asc")),
    ("bhratri", "siblings", ("jupiter", "saturn", "asc"), None),
    ("gaurava", "dignity / honour", ("jupiter", "moon", "sun"), ("jupiter", "sun", "moon")),
    ("rajya", "kingdom / authority", ("saturn", "sun", "asc"), ("sun", "saturn", "asc")),
    ("pitri", "father (= rajya)", ("saturn", "sun", "asc"), ("sun", "saturn", "asc")),
    ("matri", "mother", ("moon", "venus", "asc"), ("venus", "moon", "asc")),
    ("putra", "progeny", ("jupiter", "moon", "asc"), None),
    ("jiva", "life", ("saturn", "jupiter", "asc"), ("jupiter", "saturn", "asc")),
    ("ambu", "water (= matri)", ("moon", "venus", "asc"), ("venus", "moon", "asc")),
    ("karma", "profession / action", ("mars", "mercury", "asc"), ("mercury", "mars", "asc")),
    ("roga", "disease / physical inability", ("asc", "moon", "asc"), None),
    ("kamadeva", "desire", ("moon", "lord_asc", "asc"), ("lord_asc", "moon", "asc")),
    ("kali", "strife", ("jupiter", "mars", "asc"), ("mars", "jupiter", "asc")),
    ("kshama", "forgiveness (= kali)", ("jupiter", "mars", "asc"), ("mars", "jupiter", "asc")),
    ("shastra", "scripture / science", ("jupiter", "saturn", "asc"), ("saturn", "jupiter", "asc")),
    ("bandhu", "relatives", ("mercury", "moon", "asc"), None),
    ("bandhaka", "imprisonment", ("moon", "mercury", "asc"), ("mercury", "moon", "asc")),
    ("mrityu", "death", ("cusp8", "moon", "saturn"), None),
    ("pardesha", "foreign land", ("cusp9", "lord_cusp9", "asc"), None),
    ("dhana", "wealth", ("cusp2", "lord_cusp2", "asc"), None),
    ("anyadara", "another's spouse", ("venus", "sun", "asc"), None),
    ("anyakarma", "other work", ("moon", "saturn", "asc"), ("saturn", "moon", "asc")),
    ("vanik", "trade (= bandhaka)", ("moon", "mercury", "asc"), ("mercury", "moon", "asc")),
    ("karyasiddhi", "success in a venture", ("saturn", "sun", "lord_sun"), ("saturn", "moon", "lord_moon")),
    ("vivaha", "marriage", ("venus", "saturn", "asc"), None),
    ("prasava", "childbirth", ("jupiter", "mercury", "asc"), ("mercury", "jupiter", "asc")),
    ("santapa", "sorrow", ("saturn", "moon", "cusp6"), None),
    ("shraddha", "devotion", ("venus", "mars", "asc"), None),
    ("preeti", "love", ("saham:vidya", "saham:punya", "asc"), None),
    ("bala", "strength (= yasha)", ("jupiter", "saham:punya", "asc"), ("saham:punya", "jupiter", "asc")),
    ("tanu", "body (= yasha)", ("jupiter", "saham:punya", "asc"), ("saham:punya", "jupiter", "asc")),
    ("jadya", "chronic disease", ("mars", "saturn", "mercury"), ("saturn", "mars", "mercury")),
    ("vyapara", "business", ("mars", "mercury", "asc"), None),
    ("paniyapatana", "falling into water", ("saturn", "moon", "asc"), ("moon", "saturn", "asc")),
    ("shatru", "enemies", ("mars", "saturn", "asc"), ("saturn", "mars", "asc")),
    ("shaurya", "valour", ("saham:punya", "mars", "asc"), ("mars", "saham:punya", "asc")),
    ("upaya", "remedy / means", ("saturn", "jupiter", "asc"), ("jupiter", "saturn", "asc")),
    ("daridrata", "poverty", ("saham:punya", "mercury", "mercury"), ("mercury", "saham:punya", "mercury")),
    ("guruta", "eminence", ("exalt_sun", "sun", "asc"), ("exalt_moon", "moon", "asc")),
    ("jalapatha", "sea voyage", ("deg105", "saturn", "asc"), ("saturn", "deg105", "asc")),
    ("bandhana", "bondage", ("saham:punya", "saturn", "asc"), ("saturn", "saham:punya", "asc")),
    ("kanya", "daughter", ("venus", "moon", "asc"), None),
    ("ashwa", "horses / conveyance", ("saham:punya", "sun", "cusp11"), ("sun", "saham:punya", "cusp11")),
]
INVERTED_SAHAMS = {"roga", "shatru", "kali", "mrityu"}   # better when weak (TN p.107)


def _between_forward(c: float, b: float, a: float) -> bool:
    return (c - b) % 360.0 <= (a - b) % 360.0


def sahams(ctx: Ctx, pv: dict, harsha: dict, year_lord: str | None, praveshe_jd: float,
           rasimana: dict[int, float] | None) -> list[dict]:
    """The fifty of TN p.93-101 in the year's chart. Cusps are equal houses from
    the lagna DEGREE (a convention: the text does not fix a house system)."""
    cusp = {n: (ctx.lagna_lon + 30.0 * (n - 1)) % 360.0 for n in range(1, 13)}
    terms = {**{p: ctx.lon[p] for p in SEVEN}, "asc": ctx.lagna_lon, "deg105": 105.0,
             "exalt_sun": EXALTATION["sun"][0] * 30.0 + EXALTATION["sun"][1],
             "exalt_moon": EXALTATION["moon"][0] * 30.0 + EXALTATION["moon"][1],
             "lord_asc": ctx.lon[ctx.lagna_lord],
             "lord_sun": ctx.lon[RASI_LORD[ctx.sign["sun"]]], "lord_moon": ctx.lon[RASI_LORD[ctx.sign["moon"]]]}
    for n in (2, 6, 8, 9, 11):
        terms[f"cusp{n}"] = cusp[n]
        terms[f"lord_cusp{n}"] = ctx.lon[RASI_LORD[int(cusp[n] // 30)]]
    computed: dict[str, float] = {}
    out = []
    for key, gloss, day_f, night_f in SAHAMS:
        f = day_f if (ctx.is_day or night_f is None) else night_f
        a_k, b_k, c_k = f
        # the two special cases the text states
        if key == "samarthya" and ctx.lagna_lord == "mars":
            a_k, b_k, c_k = "jupiter", "mars", "asc"
        if key == "kamadeva" and ctx.lagna_lord == "moon":
            a_k, b_k, c_k = "sun", "moon", "asc"
        def val(k):
            return computed[k[6:]] if k.startswith("saham:") else terms[k]
        a, b, c = val(a_k), val(b_k), val(c_k)
        v = (a - b + c) % 360.0
        added = not _between_forward(c, b, a)
        if added:
            v = (v + 30.0) % 360.0
        computed[key] = v
        s, d = split(v)
        lord = RASI_LORD[s]
        lst = ctx.state(lord)
        lord_asp, _h = drishti_value(ctx.lon[lord], v)
        conj = [p for p in SEVEN if ctx.sign[p] == s]
        strong = [f_ for f_, on in (
            ("lord exalted / own sign / own hadda or navāṁśa", lst["exalted"] or lst["own_sign"] or lst["hadda_lord"] == lord or lst["navamsa_lord"] == lord),
            ("with a benefic", any(ctx.benefic(p) for p in conj)),
            ("with the year-lord", year_lord in conj),
            ("lord aspects or joins the saham", lord_asp > 0 or lord in conj),
        ) if on]
        weak = [f_ for f_, on in (
            ("lord below 5 units (pañcavargīya)", pv[lord]["vishwa_bala"] < 5),
            ("lord without harṣa bala", harsha[lord]["total"] == 0),
            ("lord neither aspects nor joins the saham", not (lord_asp > 0 or lord in conj)),
            ("with a malefic", any(p in NATURAL_MALEFIC for p in conj)),
            ("in the 6th, 8th or 12th", house_from(ctx.lagna, s) in TRIK),
        ) if on]
        verdict = "strong" if strong and not weak else "weak" if weak and not strong else "mixed"
        timing = None
        if rasimana and s in rasimana:
            days = ((v - ctx.lon[lord]) % 360.0) * rasimana[s] / 300.0
            timing = {"days": round(days, 1), "jd": praveshe_jd + days,
                      "rule": "(saham − its lord) × rāśimāna of the saham's sign ÷ 300, in days (TN p.104-105)"}
        out.append({"key": key, "gloss": gloss, "formula": f"{a_k} − {b_k} + {c_k}" + (" + 30" if added else ""),
                    "longitude": round(v, 4), "sign": s, "deg": round(d, 4), "house": house_from(ctx.lagna, s),
                    "lord": lord, "lord_vishwa_bala": pv[lord]["vishwa_bala"], "lord_aspect_on_saham": round(lord_asp, 1),
                    "conjunct": conj, "strength": {"verdict": verdict, "strong": strong, "weak": weak,
                                                  "inverted": key in INVERTED_SAHAMS},
                    "timing": timing})
    return out


def rasimana_palas(jd: float, latitude: float, longitude: float) -> dict[int, float]:
    """Rising time of each sign at the place, in palas (1 pala = 24 s), by
    sampling the sidereal ascendant every minute across 27 hours. Only a sign
    whose INGRESS was observed is recorded — the sign rising at the start of
    the window is picked up when it comes round again. Sums to ~3600."""
    out: dict[int, float] = {}
    prev, t_in = None, None
    for k in range(0, 27 * 60 + 1):
        t = jd + k / 1440.0
        asc = swe.houses_ex(t, latitude, longitude, b"W", swe.FLG_SIDEREAL)[1][0]
        s = int(asc // 30) % 12
        if s != prev:
            if prev is not None and t_in is not None and prev not in out:
                out[prev] = round((t - t_in) * 1440.0 * 2.5, 1)
            prev, t_in = s, (t if prev is not None else None)
    return out
