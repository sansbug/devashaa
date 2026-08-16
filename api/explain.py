"""Search-driven, chart-tailored "explain" (MVP).

A free-text query about a placement — "impact of jupiter in the 2nd house",
"saturn in taurus", or just "venus" — resolved into three composed layers, each
from an engine that already exists (no new astronomy):

  1. THE READING   — the cited classical concordance for that (graha, house|sign)
                     cell (classical.py). Multiple dated sources, never blended,
                     and honestly absent when no text covers the cell.
  2. IN YOUR CHART — this chart's own verdict: whether the placement actually
                     occurs here, the bhāva's iṣṭa/kaṣṭa net + its cited ledger,
                     and the graha's disposition/state (matrix.build).
  3. OVER YOUR LIFE— when the graha ran its mahādaśā across the life arc, and how
                     the house's own life-facets fared in those windows vs the
                     lifetime average — an indication of how it has played, not a
                     record of events (matrix.lifearc).

Everything here is routing + composition. The query parser is the only new logic.
"""
from __future__ import annotations

import re
import unicodedata

import classical
import matrix as _matrix
import vedic


# ── vocabulary (canonical keys are lowercase English; rāśi is 0-11) ──────────────
def _fold(s: str) -> str:
    """Lowercase + strip diacritics so 'Guru', 'Rāhu', 'Meṣa' all match plainly."""
    n = unicodedata.normalize("NFKD", str(s).lower())
    return "".join(c for c in n if not unicodedata.combining(c)).strip()


_GRAHA_ALIASES: dict[str, str] = {}
for _row in vedic.GRAHAS:                       # (key, common, iast, english, glyph, id)
    _k = _row[0]
    for _name in (_row[0], _row[1], _row[2], _row[3]):
        _GRAHA_ALIASES[_fold(_name)] = _k
# spelling variants a user is likely to type that aren't the shipped display names
_GRAHA_ALIASES.update({
    "surya": "sun", "ravi": "sun", "aditya": "sun",
    "chandra": "moon", "soma": "moon", "luna": "moon",
    "mangala": "mars", "mangal": "mars", "kuja": "mars", "angaraka": "mars",
    "budha": "mercury", "budh": "mercury",
    "guru": "jupiter", "brihaspati": "jupiter", "brhaspati": "jupiter",
    "shukra": "venus", "sukra": "venus",
    "shani": "saturn", "sani": "saturn", "manda": "saturn",
})
# two-word aliases for the nodes, matched on the whitespace-stripped query
_GRAHA_COMPOUND = {"northnode": "rahu", "dragonshead": "rahu", "dragonhead": "rahu",
                   "southnode": "ketu", "dragonstail": "ketu", "dragontail": "ketu"}

_RASI_ALIASES: dict[str, int] = {}
for _i in range(12):
    for _arr in (vedic.RASIS, vedic.RASIS_IAST, vedic.RASIS_EN):
        _RASI_ALIASES[_fold(_arr[_i])] = _i

_ORDINAL_WORDS = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
                  "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
                  "eleventh": 11, "twelfth": 12}

_SUGGESTIONS = ["Jupiter in the 2nd house", "Saturn in the 7th house",
                "Venus in Taurus", "Moon in the 4th house", "Rahu in the 10th house"]


def parse_query(q: str) -> dict | None:
    """Free text → {"graha": key, "house": 1-12 | None, "sign": 0-11 | None}, or None
    if no graha is recognised. A graha with neither house nor sign is valid — the
    composer falls back to the graha's actual placement in the chart."""
    if not q or not str(q).strip():
        return None
    folded = _fold(q)
    tokens = re.findall(r"[a-z0-9]+", folded)
    tokenset = set(tokens)

    graha = None
    for tok in tokens:                          # first recognised graha token wins
        if tok in _GRAHA_ALIASES:
            graha = _GRAHA_ALIASES[tok]
            break
    if graha is None:                           # two-word node names ("north node")
        nospace = folded.replace(" ", "")
        for alias, key in _GRAHA_COMPOUND.items():
            if alias in nospace:
                graha = key
                break
    if graha is None:
        return None

    sign = None
    for tok in tokens:
        if tok in _RASI_ALIASES:
            sign = _RASI_ALIASES[tok]
            break
    if sign is not None:
        return {"graha": graha, "house": None, "sign": sign}

    house = None
    for tok in tokens:
        if tok in _ORDINAL_WORDS:
            house = _ORDINAL_WORDS[tok]
            break
        m = re.match(r"^(\d{1,2})(?:st|nd|rd|th)?$", tok)
        if m and 1 <= int(m.group(1)) <= 12:
            house = int(m.group(1))
            break
    return {"graha": graha, "house": house, "sign": None}


# ── house → life-facet routing (reuses THEMES + _FACETS; no new data) ────────────
_THEME_FACETS: dict[str, list[str]] = {}
for _fk, _blend in _matrix._FACETS.items():
    for _tk in _blend:
        _THEME_FACETS.setdefault(_tk, []).append(_fk)

_HOUSE_THEME: dict[int, str] = {}               # a house → its dominant life-theme
_house_best: dict[int, float] = {}
for _t in _matrix.THEMES:
    for _h, _w in _t.get("houses", {}).items():
        if _w > _house_best.get(_h, 0.0):
            _house_best[_h] = _w
            _HOUSE_THEME[_h] = _t["key"]


def _facets_for_house(house: int) -> list[str]:
    """The life-facets tied to a house, via its dominant theme (e.g. 2nd → wealth →
    [wealthEarned, wealthReceived])."""
    return _THEME_FACETS.get(_HOUSE_THEME.get(house), [])


# ── gist cleaning — strip concordance framing on either axis ─────────────────────
def _clean_gist(gist: str) -> str:
    t = str(gist)
    m = re.search(r"reads\b.*?\bas\s+", t, flags=re.I)   # "<Source> reads … as EFFECT"
    if m:
        t = t[m.end():]
    t = t.split(" — in the text")[0].split(", not any prediction")[0]
    t = t.replace("the text also reads", "")
    return " ".join(t.split()).strip(" ;,.")


_REFUSE = {
    "en": ("No source in our classical concordance carries a reading for this exact "
           "placement — so, by our cite-or-refuse rule, nothing is invented here. Your "
           "chart's own verdict below still applies."),
    "hi": ("हमारी शास्त्रीय समुच्चय-सूची में इस ठीक स्थिति के लिए कोई पाठ नहीं है — अतः हमारे "
           "‘उद्धरण-या-मौन’ नियम अनुसार यहाँ कुछ गढ़ा नहीं गया। नीचे आपकी कुंडली का अपना "
           "निर्णय फिर भी लागू है।"),
}


def _reading_block(sources: list[dict], lang: str) -> dict:
    if not sources:
        return {"available": False, "note": _REFUSE.get(lang, _REFUSE["en"])}
    ordered = sorted(sources, key=lambda s: _matrix._SOURCE_ORDER.get(
        (s.get("source") or {}).get("id"), 5))
    items = []
    for s in ordered:
        src = s.get("source") or {}
        items.append({
            "book": src.get("text") or src.get("id"),
            "id": src.get("id"),
            "citation": s.get("citation"),
            "text": _clean_gist(s.get("gist") or ""),
            "adaptation": (s.get("adaptation") or {}).get("classes") or [],
        })
    return {"available": True, "sources": items}


def _bhava_block(bh: dict | None) -> dict | None:
    if not bh:
        return None
    ledger = []
    for c in bh.get("components", []):
        ledger.append({
            "factor": c.get("factor"),
            "graha": c.get("graha") or c.get("grahas"),
            "value": c.get("value"),
            "weight": c.get("weight"),
            "detail": c.get("detail"),
            "citation": c.get("citation"),
            "tier": c.get("tier"),
        })
    return {"house": bh["house"], "sign": bh["sign"], "lord": bh["lord"],
            "net": bh["net"], "band": bh["band"], "ledger": ledger}


def _life_block(chart, m_out: dict, graha: str, house: int) -> dict:
    la = _matrix.lifearc(chart, m_out)
    pts = la.get("points", [])
    windows = [{"from": seg["from"], "to": seg["to"]}
               for seg in la.get("ribbon", []) if seg.get("lord") == graha]

    def _in_win(yr):
        return any(w["from"] <= yr <= w["to"] for w in windows)

    def _avg(vals):
        vals = [v for v in vals if v is not None]
        return round(sum(vals) / len(vals), 3) if vals else None

    facet_keys = list(_matrix._FACETS)
    relevant = _facets_for_house(house)
    deltas = {}
    for fk in facet_keys:
        life = _avg([p["facets"].get(fk) for p in pts])
        dur = _avg([p["facets"].get(fk) for p in pts if _in_win(p["year"])]) if windows else None
        deltas[fk] = {
            "during": dur, "lifetime": life,
            "delta": round(dur - life, 3) if (dur is not None and life is not None) else None,
            "relevant": fk in relevant,
        }

    primary = relevant[0] if relevant else None
    series = ([{"year": p["year"], "value": p["facets"].get(primary), "inWindow": _in_win(p["year"])}
               for p in pts] if primary else [])

    tone = "none"
    if windows and primary and deltas[primary]["delta"] is not None:
        d = deltas[primary]["delta"]
        tone = "lifted" if d >= 0.05 else "pressured" if d <= -0.05 else "steady"

    return {"birthYear": la.get("birthYear"), "nowYear": la.get("nowYear"),
            "windows": windows, "relevantFacets": relevant, "primaryFacet": primary,
            "facetDeltas": deltas, "series": series, "tone": tone}


def explain(chart, m_out: dict, query: str, lang: str = "en") -> dict:
    """Compose the three layers for one query against one chart's matrix."""
    parsed = parse_query(query)
    if not parsed:
        return {"query": query, "parsed": None, "suggestions": _SUGGESTIONS}

    g = parsed["graha"]
    nodes = m_out.get("nodes", {})
    node = nodes.get(g, {})
    actual_house = node.get("bhava")
    actual_sign = node.get("rasi")
    lagna = chart.lagna_rasi

    out = {
        "query": query,
        "graha": g,
        "placement": {"house": actual_house, "sign": actual_sign,
                      "state": node.get("state"), "retro": node.get("retro"),
                      "strength": node.get("strength")},
        "disposition": m_out.get("grahaDisposition", {}).get(g),
    }

    if parsed.get("sign") is not None:
        sign = parsed["sign"]
        house = (sign - lagna) % 12 + 1            # whole-sign bhāva of that rāśi here
        out.update({
            "axis": "sign", "sign": sign, "signHouse": house,
            "inChart": actual_sign == sign,
            "parsed": {"graha": g, "sign": sign, "axis": "sign"},
            "reading": _reading_block(classical.readings_for(g, sign=sign, lang=lang), lang),
        })
    else:
        house = parsed.get("house") or actual_house    # fall back to actual placement
        out.update({
            "axis": "house", "house": house,
            "inChart": actual_house == house,
            "askedActual": parsed.get("house") is None,
            "parsed": {"graha": g, "house": house, "axis": "house"},
            "reading": _reading_block(classical.readings_for(g, house=house, lang=lang), lang),
            "occupants": [k for k, nd in nodes.items() if nd.get("bhava") == house],
        })

    bh = next((b for b in m_out.get("bhavas", []) if b["house"] == house), None)
    out["bhava"] = _bhava_block(bh)
    out["life"] = _life_block(chart, m_out, g, house)
    return out
