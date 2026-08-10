"""Chart-tailored day scoring — reads a day's pañcāṅga against a specific
horoscope to answer "how auspicious is this day *for this person*".

FIVE transparent, individually-cited components (never a black box — each is
returned with its own verdict and source, mirroring the site's show-your-work
ethos; the single 0–100 number exists only to tint the heatmap, and the exact
component weights ride along in the payload so nothing is hidden):

  • tārā-bala   — the day's nakṣatra counted from the birth (janma) nakṣatra,
                  in the 9-tārā cycle (BPHS/muhūrta).                    w=0.30
  • candra-bala — the day's Moon-sign counted from the birth Moon-sign.  w=0.20
  • moon-transit— the day's Moon-sign as a bhāva from the lagna (gochara).w=0.15
  • daśā-fit    — naisargika friendship (BPHS ch.3 v.55) between the running
                  mahā/antar-daśā lords and the day's vāra-lord.         w=0.15
  • day-quality — the day's own tithi / yoga / karaṇa auspiciousness.    w=0.20

On the daśā component: folding the operative period into day-selection is a
*practical* muhūrta synthesis, not a single cited śloka — so it is built ONLY
from cited primitives (Viṁśottarī lordship ch.46; naisargika maitrī ch.3 v.55;
the vāra-lord) and, like the whole score, it only tints — it is never a fated
verdict. When the birth daśā lords are not supplied the component is dropped and
the remaining four weights are renormalised (the actual weights used are always
returned, so the heatmap stays honest about what went into it).
"""
from __future__ import annotations

from panchang import _YOGA_BAD

# Naisargika (natural) friendship — BPHS Vol I ch.3 v.55, transcribed in
# dignity.py from the mūlatrikoṇa rule; the nodes' relations are Santhanam's
# translator's note (Vol I p.41), used only when a daśā lord IS a node.
from dignity import NATURAL_RELATIONS
from relationships import NODE_RELATIONS_SANTHANAM

# Display names for the nine Viṁśottarī lords (the daśā component surfaces them).
_GRAHA_EN = {"sun": "Sun", "moon": "Moon", "mars": "Mars", "mercury": "Mercury",
             "jupiter": "Jupiter", "venus": "Venus", "saturn": "Saturn",
             "rahu": "Rāhu", "ketu": "Ketu"}
_GRAHA_HI = {"sun": "सूर्य", "moon": "चन्द्र", "mars": "मङ्गल", "mercury": "बुध",
             "jupiter": "गुरु", "venus": "शुक्र", "saturn": "शनि",
             "rahu": "राहु", "ketu": "केतु"}

# ── tārā-bala: 9-fold cycle from the janma nakṣatra ──────────────────────────
_TARA = ["Janma", "Sampat", "Vipat", "Kṣema", "Pratyari", "Sādhaka", "Vadha",
         "Mitra", "Ati-mitra"]
_TARA_HI = ["जन्म", "सम्पत्", "विपत्", "क्षेम", "प्रत्यरि", "साधक", "वध", "मित्र", "अति-मित्र"]
_TARA_GOOD = {1, 3, 5, 7, 8}   # Sampat, Kṣema, Sādhaka, Mitra, Ati-mitra (0-based)
_TARA_BAD = {2, 4, 6}          # Vipat, Pratyari, Vadha
# Janma (0) is mixed/neutral.


def tarabala(birth_nak_index: int, day_nak_index: int) -> dict:
    """birth/day nakṣatra 1..27. Returns the tārā and its verdict."""
    n = (day_nak_index - birth_nak_index) % 27
    idx = n % 9
    verdict = "favourable" if idx in _TARA_GOOD else ("unfavourable" if idx in _TARA_BAD else "mixed")
    return {"tara": _TARA[idx], "tara_hi": _TARA_HI[idx], "index": idx + 1, "verdict": verdict,
            "source": "9-tārā cycle from the janma-nakṣatra (muhūrta / BPHS)",
            "source_hi": "जन्म-नक्षत्र से 9-तारा चक्र (मुहूर्त / बीपीएचएस)"}


# ── candra-bala: day Moon-sign counted from the birth Moon-sign ──────────────
_CHANDRA_GOOD = {1, 3, 6, 7, 10, 11}
_CHANDRA_BAD = {4, 8, 12}


def candrabala(birth_moon_sign: int, day_moon_sign: int) -> dict:
    """signs 0..11. The Moon in the 1/3/6/7/10/11 from the janma-rāśi is strong."""
    h = (day_moon_sign - birth_moon_sign) % 12 + 1
    verdict = "favourable" if h in _CHANDRA_GOOD else ("unfavourable" if h in _CHANDRA_BAD else "mixed")
    return {"house_from_moon": h, "verdict": verdict,
            "source": "candra-bala: the transiting Moon-sign counted from the janma-rāśi",
            "source_hi": "चन्द्र-बल: जन्म-राशि से गिनी गई गोचर चन्द्र-राशि"}


# ── moon transit as a bhāva from the lagna (gochara) ─────────────────────────
_TRANSIT_GOOD = {1, 4, 5, 7, 9, 10, 11}   # kendra / trikoṇa / upachaya-ish
_TRANSIT_BAD = {6, 8, 12}                 # dusthānas


def moon_transit(lagna_sign: int, day_moon_sign: int) -> dict:
    h = (day_moon_sign - lagna_sign) % 12 + 1
    verdict = "favourable" if h in _TRANSIT_GOOD else ("unfavourable" if h in _TRANSIT_BAD else "mixed")
    return {"bhava_from_lagna": h, "verdict": verdict,
            "source": "gochara: the transiting Moon as a bhāva from the lagna",
            "source_hi": "गोचर: लग्न से भाव के रूप में गोचर चन्द्र"}


# ── the day's own quality (tithi / yoga / karaṇa) ────────────────────────────
_RIKTA = {4, 9, 14}   # Riktā tithis (number in pakṣa) — weak for beginnings


def day_quality(pan: dict) -> dict:
    flags, flags_hi = [], []
    t = pan["tithi"]
    if t["number_in_paksha"] in _RIKTA:
        flags.append("Riktā tithi"); flags_hi.append("रिक्ता तिथि")
    if t["name"] == "Amāvāsyā":
        flags.append("Amāvāsyā"); flags_hi.append("अमावस्या")
    if not pan["yoga"]["auspicious"]:
        flags.append("malefic yoga (%s)" % pan["yoga"]["name"])
        flags_hi.append("अशुभ योग (%s)" % pan["yoga"].get("name_hi", pan["yoga"]["name"]))
    if not pan["karana"]["auspicious"] and pan["karana"]["name"] == "Viṣṭi":
        flags.append("Viṣṭi (Bhadrā) karaṇa"); flags_hi.append("विष्टि (भद्रा) करण")
    verdict = "clean" if not flags else ("weak" if len(flags) == 1 else "unfavourable")
    return {"flags": flags, "flags_hi": flags_hi, "verdict": verdict,
            "source": "day's own tithi / yoga / karaṇa (muhūrta)",
            "source_hi": "दिन की अपनी तिथि / योग / करण (मुहूर्त)"}


# ── daśā-fit: the running period lords vs the day's vāra-lord ────────────────
_REL_VALUE = {"friend": 1, "neutral": 0, "enemy": -1}


def _relation(dasha_lord: str, vara_lord: str) -> tuple[int, bool]:
    """Naisargika relation the running-period lord holds toward the weekday
    ruler → (+1 friend / 0 neutral / −1 enemy), and whether it rests on the
    (non-mūla) node note. A lord ruling its own weekday counts as friendly."""
    if dasha_lord == vara_lord:
        return 1, False
    if dasha_lord in NATURAL_RELATIONS:          # one of the seven grahas
        return _REL_VALUE[NATURAL_RELATIONS[dasha_lord].get(vara_lord, "neutral")], False
    node = NODE_RELATIONS_SANTHANAM.get(dasha_lord, {})   # rāhu / ketu
    return _REL_VALUE.get(node.get(vara_lord, "neutral"), 0), True


def dasha_fit(maha_lord: str, antar_lord: str | None, vara_lord: str) -> dict:
    """How the running daśā sits with the day's weekday ruler. The mahādaśā lord
    carries 0.6 of the sub-weight, the antardaśā 0.4; the blend maps to a verdict
    that the outer score then weights at 0.15. Every input is a cited primitive
    (Viṁśottarī lordship, vāra-lord, naisargika maitrī); the synthesis tints."""
    m_val, m_node = _relation(maha_lord, vara_lord)
    if antar_lord:
        a_val, a_node = _relation(antar_lord, vara_lord)
        blend = 0.6 * m_val + 0.4 * a_val
    else:
        a_val, a_node = None, False
        blend = float(m_val)
    verdict = "favourable" if blend > 0.2 else ("unfavourable" if blend < -0.2 else "mixed")
    uses_node = m_node or a_node
    src = ("naisargika maitrī (BPHS ch.3 v.55) of the running mahā/antar-daśā "
           "lords toward the day's vāra-lord")
    src_hi = ("दिन के वार-स्वामी के प्रति चालू महा/अन्तर्दशा स्वामियों की "
              "नैसर्गिक मैत्री (बीपीएचएस अ.3 श्लो.55)")
    if uses_node:
        src += " — node relations per Santhanam's note (not mūla)"
        src_hi += " — राहु/केतु हेतु सन्थानम् की टिप्पणी (मूल नहीं)"
    return {
        "maha": maha_lord, "maha_name": _GRAHA_EN.get(maha_lord, maha_lord),
        "maha_name_hi": _GRAHA_HI.get(maha_lord, maha_lord),
        "antar": antar_lord,
        "antar_name": _GRAHA_EN.get(antar_lord, antar_lord) if antar_lord else None,
        "antar_name_hi": _GRAHA_HI.get(antar_lord, antar_lord) if antar_lord else None,
        "vara_lord": vara_lord, "vara_lord_name": _GRAHA_EN.get(vara_lord, vara_lord),
        "vara_lord_name_hi": _GRAHA_HI.get(vara_lord, vara_lord),
        "verdict": verdict, "source": src, "source_hi": src_hi,
        "node_basis": uses_node,
    }


_W = {"favourable": 1.0, "clean": 1.0, "mixed": 0.5, "weak": 0.4,
      "unfavourable": 0.0}

# The published component weights (sum 1.0). Returned in every score so the tint
# is never a black box; when daśā is unavailable the other four renormalise.
_WEIGHTS = {"tarabala": 0.30, "candrabala": 0.20, "moon_transit": 0.15,
            "dasha": 0.15, "day_quality": 0.20}


def score_day(pan: dict, birth: dict) -> dict:
    """`birth` = {moon_nak, moon_sign, lagna_sign, dasha_maha, dasha_antar}.
    Returns the per-component verdicts, the exact weights used, and a 0-100 tint
    score. The daśā component is included when `dasha_maha` is supplied, else the
    remaining four weights are renormalised to keep the score on 0-100."""
    tb = tarabala(birth["moon_nak"], pan["nakshatra"]["index"])
    cb = candrabala(birth["moon_sign"], pan["_moon_sign"])
    mt = moon_transit(birth["lagna_sign"], pan["_moon_sign"])
    dq = day_quality(pan)

    maha = birth.get("dasha_maha")
    df = dasha_fit(maha, birth.get("dasha_antar"), pan["vara"]["lord"]) if maha else None

    weights = dict(_WEIGHTS)
    if df is None:                       # drop daśā, renormalise the rest to 1.0
        weights.pop("dasha")
        s = sum(weights.values())
        weights = {k: round(v / s, 4) for k, v in weights.items()}

    parts = [(_W[tb["verdict"]], weights["tarabala"]),
             (_W[cb["verdict"]], weights["candrabala"]),
             (_W[mt["verdict"]], weights["moon_transit"]),
             (_W[dq["verdict"]], weights["day_quality"])]
    if df is not None:
        parts.append((_W[df["verdict"]], weights["dasha"]))
    score = round(100 * sum(v * w for v, w in parts))
    band = "auspicious" if score >= 66 else ("mixed" if score >= 40 else "inauspicious")

    out = {
        "score": score, "band": band, "weights": weights,
        "tarabala": tb, "candrabala": cb, "moon_transit": mt, "day_quality": dq,
    }
    if df is not None:
        out["dasha_fit"] = df
    return out
