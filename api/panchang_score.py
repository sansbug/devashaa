"""Chart-tailored day scoring — reads a day's pañcāṅga against a specific
horoscope to answer "how auspicious is this day *for this person*".

Four transparent, individually-cited components (never a black box — each is
returned with its own verdict and source, mirroring the site's show-your-work
ethos; the single 0–100 number exists only to tint the heatmap):

  • tārā-bala   — the day's nakṣatra counted from the birth (janma) nakṣatra,
                  in the 9-tārā cycle (BPHS/muhūrta).
  • candra-bala — the day's Moon-sign counted from the birth Moon-sign.
  • moon-transit— the day's Moon-sign as a bhāva from the lagna (gochara).
  • day-quality — the day's own tithi / yoga / karaṇa auspiciousness.

The running daśā lord is surfaced as context (not scored — attributing a day's
fortune to the daśā would over-reach what the classical rules state).
"""
from __future__ import annotations

from panchang import _YOGA_BAD

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
            "source": "9-tārā cycle from the janma-nakṣatra (muhūrta / BPHS)"}


# ── candra-bala: day Moon-sign counted from the birth Moon-sign ──────────────
_CHANDRA_GOOD = {1, 3, 6, 7, 10, 11}
_CHANDRA_BAD = {4, 8, 12}


def candrabala(birth_moon_sign: int, day_moon_sign: int) -> dict:
    """signs 0..11. The Moon in the 1/3/6/7/10/11 from the janma-rāśi is strong."""
    h = (day_moon_sign - birth_moon_sign) % 12 + 1
    verdict = "favourable" if h in _CHANDRA_GOOD else ("unfavourable" if h in _CHANDRA_BAD else "mixed")
    return {"house_from_moon": h, "verdict": verdict,
            "source": "candra-bala: the transiting Moon-sign counted from the janma-rāśi"}


# ── moon transit as a bhāva from the lagna (gochara) ─────────────────────────
_TRANSIT_GOOD = {1, 4, 5, 7, 9, 10, 11}   # kendra / trikoṇa / upachaya-ish
_TRANSIT_BAD = {6, 8, 12}                 # dusthānas


def moon_transit(lagna_sign: int, day_moon_sign: int) -> dict:
    h = (day_moon_sign - lagna_sign) % 12 + 1
    verdict = "favourable" if h in _TRANSIT_GOOD else ("unfavourable" if h in _TRANSIT_BAD else "mixed")
    return {"bhava_from_lagna": h, "verdict": verdict,
            "source": "gochara: the transiting Moon as a bhāva from the lagna"}


# ── the day's own quality (tithi / yoga / karaṇa) ────────────────────────────
_RIKTA = {4, 9, 14}   # Riktā tithis (number in pakṣa) — weak for beginnings


def day_quality(pan: dict) -> dict:
    flags = []
    t = pan["tithi"]
    if t["number_in_paksha"] in _RIKTA:
        flags.append("Riktā tithi")
    if t["name"] == "Amāvāsyā":
        flags.append("Amāvāsyā")
    if not pan["yoga"]["auspicious"]:
        flags.append("malefic yoga (%s)" % pan["yoga"]["name"])
    if not pan["karana"]["auspicious"] and pan["karana"]["name"] == "Viṣṭi":
        flags.append("Viṣṭi (Bhadrā) karaṇa")
    verdict = "clean" if not flags else ("weak" if len(flags) == 1 else "unfavourable")
    return {"flags": flags, "verdict": verdict,
            "source": "day's own tithi / yoga / karaṇa (muhūrta)"}


_W = {"favourable": 1.0, "clean": 1.0, "mixed": 0.5, "weak": 0.4,
      "unfavourable": 0.0}


def score_day(pan: dict, birth: dict) -> dict:
    """`birth` = {moon_nak, moon_sign, lagna_sign, dasha_lord}. Returns the
    per-component verdicts + a 0-100 tint score (weighted, transparent)."""
    tb = tarabala(birth["moon_nak"], pan["nakshatra"]["index"])
    cb = candrabala(birth["moon_sign"], pan["_moon_sign"])
    mt = moon_transit(birth["lagna_sign"], pan["_moon_sign"])
    dq = day_quality(pan)
    # weighted: tārā 0.35, candra 0.25, transit 0.15, day-quality 0.25
    parts = [(_W[tb["verdict"]], 0.35), (_W[cb["verdict"]], 0.25),
             (_W[mt["verdict"]], 0.15), (_W[dq["verdict"]], 0.25)]
    score = round(100 * sum(v * w for v, w in parts))
    band = "auspicious" if score >= 66 else ("mixed" if score >= 40 else "inauspicious")
    return {
        "score": score, "band": band,
        "tarabala": tb, "candrabala": cb, "moon_transit": mt, "day_quality": dq,
        "dasha_context": birth.get("dasha_lord"),
    }
