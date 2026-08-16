"""Search-driven, chart-tailored "explain" (full scope).

A free-text query resolved into a chart-tailored answer. Four intents:

  • PLACEMENT — "jupiter in the 2nd house", "saturn in taurus", "venus":
      cited classical reading (concordance) + this chart's bhāva verdict +
      the graha's mahādaśā windows across the life arc.
  • YOGA — "gajakesari yoga", "hamsa", "amala yoga":
      the yoga's cited BPHS effect + whether it is present in THIS chart (with
      its forming grahas / strength) + those grahas' daśā windows over life.
  • THEME — "career", "my wealth", "marriage", "health":
      the theme's standing verdict + cited ledger + significators + near-future
      typed events + the theme's life-facet across the life arc.
  • HOUSE — "10th house", "tell me about my 2nd bhāva":
      the bhāva verdict + every occupant's cited planet-in-house reading + the
      house's life-facet over life.

Everything is routing + composition over engines that already exist. The query
parser and the per-intent composers are the only new logic. Nothing is fated:
readings are cited/dated, verdicts open a weighted ledger, arcs are broad shapes.
"""
from __future__ import annotations

import datetime as _dt
import re
import unicodedata

import swisseph as swe

import classical
import drishti
import matrix as _matrix
import vedic
import yoga_rules
import yogas as _yogas
import shadbala_context

# graha key → Swiss-Ephemeris body id (Ketu has none — derived from Rāhu +180°)
_SWE_ID = {row[0]: row[5] for row in vedic.GRAHAS if row[5] is not None}
# sign index 0-11 → its rāśi lord (dispositor), graha key
_RASI_LORD_KEY = ["mars", "venus", "mercury", "moon", "sun", "mercury",
                  "venus", "mars", "jupiter", "saturn", "saturn", "jupiter"]


# ── folding + graha/rāśi vocab (canonical keys lowercase English; rāśi 0-11) ─────
def _fold(s: str) -> str:
    n = unicodedata.normalize("NFKD", str(s).lower())
    return "".join(c for c in n if not unicodedata.combining(c)).strip()


_GRAHA_ALIASES: dict[str, str] = {}
for _row in vedic.GRAHAS:                       # (key, common, iast, english, glyph, id)
    for _name in (_row[0], _row[1], _row[2], _row[3]):
        _GRAHA_ALIASES[_fold(_name)] = _row[0]
_GRAHA_ALIASES.update({
    "surya": "sun", "ravi": "sun", "aditya": "sun",
    "chandra": "moon", "soma": "moon", "luna": "moon",
    "mangala": "mars", "mangal": "mars", "kuja": "mars", "angaraka": "mars",
    "budha": "mercury", "budh": "mercury",
    "guru": "jupiter", "brihaspati": "jupiter", "brhaspati": "jupiter",
    "shukra": "venus", "sukra": "venus",
    "shani": "saturn", "sani": "saturn", "manda": "saturn",
})
_GRAHA_COMPOUND = {"northnode": "rahu", "dragonshead": "rahu", "dragonhead": "rahu",
                   "southnode": "ketu", "dragonstail": "ketu", "dragontail": "ketu"}

_RASI_ALIASES: dict[str, int] = {}
for _i in range(12):
    for _arr in (vedic.RASIS, vedic.RASIS_IAST, vedic.RASIS_EN):
        _RASI_ALIASES[_fold(_arr[_i])] = _i

_ORDINAL_WORDS = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5,
                  "sixth": 6, "seventh": 7, "eighth": 8, "ninth": 9, "tenth": 10,
                  "eleventh": 11, "twelfth": 12}

# ── yoga aliases from the catalog. Catalog KEYS carry spaces / unicode / long
#    descriptive raja phrases, so: always alias the whitespace-stripped whole name,
#    and for a "proper-named" yoga (single word, or a name with no digit/slash) also
#    alias its first distinctive word — so "gajakesari", "gajakesari yoga" and
#    "gajakesariyoga" all resolve. Descriptive raja phrases (which carry digits or
#    slashes) get ONLY the nospace alias, and theme words are stop-listed, so a query
#    like "wealth" never captures a raja yoga instead of the wealth theme. ─
_YOGA_STOP = {"yoga", "from", "the", "and", "with", "aspecting", "aspected", "lord",
              "lords", "kendra", "kendras", "trikona", "planets", "planet", "exalted",
              "exaltation", "benefic", "benefics", "malefic", "malefics", "navamsa",
              "house", "class", "strong", "moon", "sun", "luminary", "conjoined",
              "conjunction", "association", "mutual", "dusthana", "debilitation",
              "exchange", "minister", "ascendant",
              # theme words — never let a yoga capture these (theme intent owns them)
              "wealth", "career", "health", "marriage", "children", "education", "home",
              "fortune", "enemies", "foreign", "longevity", "money", "love", "work"}
_YOGA_ALIASES: dict[str, str] = {}
for _yname in yoga_rules.YOGAS:
    _folded = _fold(_yname)
    _YOGA_ALIASES.setdefault(_folded.replace(" ", ""), _yname)
    _words = re.findall(r"[a-z0-9]+", _folded)
    _descriptive = bool(re.search(r"[0-9/]", _folded))          # raja phrases → nospace only
    if len(_words) == 1:
        _YOGA_ALIASES.setdefault(_words[0], _yname)
    elif not _descriptive:
        for _w in _words:
            if len(_w) >= 4 and _w not in _YOGA_STOP:
                _YOGA_ALIASES.setdefault(_w, _yname)
                break
_YOGA_ALIASES.update({"gajakesri": "Gajakesari Yoga", "gajkesari": "Gajakesari Yoga",
                      "shasha": "Sasa", "sasha": "Sasa"})

# ── theme aliases (route free text to a life-theme key) ──────────────────────────
_THEME_ALIASES: dict[str, str] = {}
_THEME_WORDS = {
    "self": ["self", "personality", "body", "mind", "vitality", "character"],
    "wealth": ["wealth", "money", "finances", "financial", "rich", "riches", "income",
               "prosperity", "savings", "earnings"],
    "career": ["career", "job", "work", "profession", "occupation", "status", "business",
               "employment", "promotion", "livelihood"],
    "marriage": ["marriage", "spouse", "partner", "wife", "husband", "relationship",
                 "love", "married", "partnership"],
    "children": ["children", "child", "kids", "kid", "progeny", "son", "daughter",
                 "offspring", "fertility"],
    "health": ["health", "illness", "disease", "sickness", "wellbeing", "wellness", "fitness"],
    "education": ["education", "learning", "study", "studies", "knowledge", "academics",
                  "school", "college", "intellect"],
    "home": ["home", "property", "mother", "land", "vehicles", "comforts", "domestic"],
    "fortune": ["fortune", "luck", "dharma", "father", "religion", "spirituality", "faith"],
    "enemies": ["enemies", "enemy", "debt", "debts", "litigation", "rivals", "obstacles",
                "competition", "disputes"],
    "foreign": ["foreign", "abroad", "overseas", "moksha", "liberation", "expenses",
                "isolation"],
    "longevity": ["longevity", "lifespan", "age", "vitality"],
}
for _tk, _words in _THEME_WORDS.items():
    for _w in _words:
        _THEME_ALIASES.setdefault(_fold(_w), _tk)     # first theme claiming a word wins

# grahas that form a graha-specific yoga (for its life-arc activation windows) —
# keys are the exact catalog names (with spaces)
_YOGA_GRAHAS = {"Ruchaka": ["mars"], "Bhadra": ["mercury"], "Hamsa": ["jupiter"],
                "Malavya": ["venus"], "Sasa": ["saturn"],
                "Gajakesari Yoga": ["moon", "jupiter"],
                "Amala Yoga": ["jupiter", "mercury", "venus"]}

_SUGGESTIONS = ["Jupiter in the 2nd house", "Gajakesari yoga", "My career",
                "Saturn in the 7th house", "10th house", "Venus in Taurus"]


def parse_query(q: str) -> dict | None:
    """Free text → a typed intent, or None. Priority: a graha (with/without a house
    or sign) → placement; else a yoga name → yoga; else a bare house number → house;
    else a theme word → theme."""
    if not q or not str(q).strip():
        return None
    folded = _fold(q)
    tokens = re.findall(r"[a-z0-9]+", folded)
    nospace = folded.replace(" ", "")

    # 1 — graha (→ placement)
    graha = next((_GRAHA_ALIASES[t] for t in tokens if t in _GRAHA_ALIASES), None)
    if graha is None:
        graha = next((k for a, k in _GRAHA_COMPOUND.items() if a in nospace), None)
    if graha is not None:
        sign = next((_RASI_ALIASES[t] for t in tokens if t in _RASI_ALIASES), None)
        if sign is not None:
            return {"kind": "placement", "graha": graha, "house": None, "sign": sign}
        return {"kind": "placement", "graha": graha, "house": _house_token(tokens), "sign": None}

    # 2 — yoga
    yoga = next((_YOGA_ALIASES[t] for t in tokens if t in _YOGA_ALIASES), None)
    if yoga is None:                                   # multi-word like "gaja kesari"
        yoga = next((v for a, v in _YOGA_ALIASES.items() if len(a) > 5 and a in nospace), None)
    if yoga is not None:
        return {"kind": "yoga", "yoga": yoga}

    # 3 — a bare house (needs a house/bhava cue so "in 2020" isn't a house)
    if any(t in ("house", "bhava", "bhāva", "houses") for t in tokens):
        h = _house_token(tokens)
        if h:
            return {"kind": "house", "house": h}

    # 4 — a life-theme word
    theme = next((_THEME_ALIASES[t] for t in tokens if t in _THEME_ALIASES), None)
    if theme is not None:
        return {"kind": "theme", "theme": theme}

    return None


def _house_token(tokens: list[str]) -> int | None:
    for t in tokens:
        if t in _ORDINAL_WORDS:
            return _ORDINAL_WORDS[t]
        m = re.match(r"^(\d{1,2})(?:st|nd|rd|th)?$", t)
        if m and 1 <= int(m.group(1)) <= 12:
            return int(m.group(1))
    return None


# ── house → life-facet routing (reuses THEMES + _FACETS) ─────────────────────────
_THEME_FACETS: dict[str, list[str]] = {}
for _fk, _blend in _matrix._FACETS.items():
    for _tk in _blend:
        _THEME_FACETS.setdefault(_tk, []).append(_fk)

_HOUSE_THEME: dict[int, str] = {}
_house_best: dict[int, float] = {}
for _t in _matrix.THEMES:
    for _h, _w in _t.get("houses", {}).items():
        if _w > _house_best.get(_h, 0.0):
            _house_best[_h] = _w
            _HOUSE_THEME[_h] = _t["key"]


def _facets_for_house(house: int) -> list[str]:
    return _THEME_FACETS.get(_HOUSE_THEME.get(house), [])


# ── gist cleaning + reading block (cite-or-refuse) ───────────────────────────────
def _clean_gist(gist: str) -> str:
    t = str(gist)
    m = re.search(r"reads\b.*?\bas\s+", t, flags=re.I)
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


def _one_source(reading: dict) -> dict:
    src = reading.get("source") or {}
    return {"book": src.get("text") or src.get("id"), "id": src.get("id"),
            "citation": reading.get("citation"), "text": _clean_gist(reading.get("gist") or ""),
            "adaptation": (reading.get("adaptation") or {}).get("classes") or []}


def _reading_block(sources: list[dict], lang: str) -> dict:
    if not sources:
        return {"available": False, "note": _REFUSE.get(lang, _REFUSE["en"])}
    ordered = sorted(sources, key=lambda s: _matrix._SOURCE_ORDER.get(
        (s.get("source") or {}).get("id"), 5))
    return {"available": True, "sources": [_one_source(s) for s in ordered]}


def _bhava_block(bh: dict | None) -> dict | None:
    if not bh:
        return None
    ledger = [{"factor": c.get("factor"), "graha": c.get("graha") or c.get("grahas"),
               "value": c.get("value"), "weight": c.get("weight"), "detail": c.get("detail"),
               "citation": c.get("citation"), "tier": c.get("tier")}
              for c in bh.get("components", [])]
    return {"house": bh["house"], "sign": bh["sign"], "lord": bh["lord"],
            "net": bh["net"], "band": bh["band"], "ledger": ledger}


# ── life-arc activation (generic over one or more grahas; facet or overall) ───────
def _life_block(chart, m_out: dict, grahas: list[str], facet: str | None) -> dict:
    la = _matrix.lifearc(chart, m_out)
    pts = la.get("points", [])
    gset = set(grahas)
    windows = [{"from": seg["from"], "to": seg["to"], "lord": seg["lord"]}
               for seg in la.get("ribbon", []) if seg.get("lord") in gset]

    def _in_win(yr):
        return any(w["from"] <= yr <= w["to"] for w in windows)

    def _avg(vals):
        vals = [v for v in vals if v is not None]
        return round(sum(vals) / len(vals), 3) if vals else None

    relevant: list[str] = []
    deltas = {}
    if facet:
        relevant = [facet] if not isinstance(facet, list) else facet
        for fk in _matrix._FACETS:
            life = _avg([p["facets"].get(fk) for p in pts])
            dur = _avg([p["facets"].get(fk) for p in pts if _in_win(p["year"])]) if windows else None
            deltas[fk] = {"during": dur, "lifetime": life,
                          "delta": round(dur - life, 3) if (dur is not None and life is not None) else None,
                          "relevant": fk in relevant}
        val_of = lambda p: p["facets"].get(relevant[0]) if relevant else p.get("overall")
        primary = relevant[0] if relevant else None
    else:
        primary = None
        val_of = lambda p: p.get("overall")

    series = [{"year": p["year"], "value": val_of(p), "inWindow": _in_win(p["year"])} for p in pts]
    tone = "none"
    if windows and primary and deltas.get(primary, {}).get("delta") is not None:
        d = deltas[primary]["delta"]
        tone = "lifted" if d >= 0.05 else "pressured" if d <= -0.05 else "steady"

    return {"birthYear": la.get("birthYear"), "nowYear": la.get("nowYear"),
            "windows": windows, "relevantFacets": (relevant if facet else []),
            "primaryFacet": primary, "facetDeltas": deltas, "series": series, "tone": tone,
            "overall": facet is None}


# ── "everything related to this graha" — dṛṣṭi, gochara, and its role in the chart ─
def _graha_transit(g, lagna, moon_sign, av):
    """Where the graha transits TODAY: sign, house from lagna & Moon, and an
    aṣṭakavarga tone (its bindus in the transited sign). None if it can't be read."""
    try:
        now = _dt.datetime.utcnow()
        jd = swe.julday(now.year, now.month, now.day, 12.0, swe.GREG_CAL)
        if g == "ketu":
            tsign = (_matrix._transit_sign(jd, swe.MEAN_NODE) + 6) % 12
        else:
            ipl = _SWE_ID.get(g)
            if ipl is None:
                return None
            tsign = _matrix._transit_sign(jd, ipl)
    except Exception:  # noqa: BLE001
        return None
    bav = (av.get("bhinna") or {}).get(g)
    bindu = bav[tsign] if (bav and 0 <= tsign < len(bav)) else None
    tone = "neutral"
    if bindu is not None:
        tone = "supportive" if bindu >= 5 else "straining" if bindu <= 3 else "neutral"
    return {"sign": tsign, "houseFromLagna": (tsign - lagna) % 12 + 1,
            "houseFromMoon": ((tsign - moon_sign) % 12 + 1) if moon_sign is not None else None,
            "bindu": bindu, "tone": tone}


def _graha_facets(chart, m_out, g):
    """Everything the chart says about one graha beyond a single placement: its
    dṛṣṭi (what it aspects / is aspected by), its gochara (transit today), and its
    structural role — lordships, natural kāraka, chara-kāraka role, dispositor,
    conjunctions and the yogas it forms."""
    nodes = m_out.get("nodes", {})
    node = nodes.get(g, {})
    sign, bhava = node.get("rasi"), node.get("bhava")
    lagna = chart.lagna_rasi
    moon_sign = nodes.get("moon", {}).get("rasi")
    edges = (m_out.get("edges") or {}).get("aspects", [])

    casts_grahas = sorted({e["to"] for e in edges if e["from"] == g and e.get("strength", 0) >= 0.5})
    recv_grahas = sorted({e["from"] for e in edges if e["to"] == g and e.get("strength", 0) >= 0.5})
    casts_houses = []
    if sign is not None:
        for h in range(1, 13):
            hs = (lagna + h - 1) % 12
            if hs != sign and drishti.graha_drishti(sign, hs, g) >= 1.0 - 1e-9:
                casts_houses.append(h)

    kar = m_out.get("karakas", {}) or {}
    chara = kar.get("chara", {}) or {}
    chara_roles = (["Ātmakāraka"] if kar.get("atmakaraka") == g else []) + \
                  [r for r, gg in chara.items() if gg == g]
    role = {
        "rules": [b["house"] for b in m_out.get("bhavas", []) if b["lord"] == g],
        "karakaHouses": [h for h, kk in _matrix._BHAVA_KARAKA.items() if kk == g],
        "charaRoles": chara_roles,
        "dispositor": _RASI_LORD_KEY[sign] if sign is not None else None,
        "conjunct": [k for k, nd in nodes.items() if nd.get("bhava") == bhava and k != g],
        "yogas": [y["name"] for y in m_out.get("yogas", []) if g in _YOGA_GRAHAS.get(y["name"], [])],
        "state": node.get("state"), "retro": node.get("retro"), "strength": node.get("strength"),
    }
    return {"aspects": {"castsHouses": casts_houses, "castsGrahas": casts_grahas, "receivedFrom": recv_grahas},
            "transit": _graha_transit(g, lagna, moon_sign, m_out.get("ashtakavarga") or {}),
            "role": role}


# ── intent composers ─────────────────────────────────────────────────────────────
def _explain_placement(chart, m_out, intent, lang):
    g = intent["graha"]
    nodes = m_out.get("nodes", {})
    node = nodes.get(g, {})
    lagna = chart.lagna_rasi
    out = {"kind": "placement", "graha": g,
           "placement": {"house": node.get("bhava"), "sign": node.get("rasi"),
                         "state": node.get("state"), "retro": node.get("retro"),
                         "strength": node.get("strength")},
           "disposition": m_out.get("grahaDisposition", {}).get(g)}
    if intent.get("sign") is not None:
        sign = intent["sign"]
        house = (sign - lagna) % 12 + 1
        out.update({"axis": "sign", "sign": sign, "signHouse": house,
                    "inChart": node.get("rasi") == sign,
                    "parsed": {"graha": g, "sign": sign, "axis": "sign"},
                    "reading": _reading_block(classical.readings_for(g, sign=sign, lang=lang), lang)})
    else:
        house = intent.get("house") or node.get("bhava")
        out.update({"axis": "house", "house": house, "inChart": node.get("bhava") == house,
                    "askedActual": intent.get("house") is None,
                    "parsed": {"graha": g, "house": house, "axis": "house"},
                    "reading": _reading_block(classical.readings_for(g, house=house, lang=lang), lang),
                    "occupants": [k for k, nd in nodes.items() if nd.get("bhava") == house]})
    out["bhava"] = _bhava_block(next((b for b in m_out.get("bhavas", []) if b["house"] == house), None))
    out["grahaFacets"] = _graha_facets(chart, m_out, g)
    facets = _facets_for_house(house)
    out["life"] = _life_block(chart, m_out, [g], facets[0] if facets else None)
    return out


def _explain_yoga(chart, m_out, intent, lang):
    name = intent["yoga"]
    meta = yoga_rules.YOGAS.get(name)
    if not meta:
        return {"kind": "yoga", "parsed": None, "suggestions": _SUGGESTIONS}
    present_names = {y["name"] for y in m_out.get("yogas", [])}
    present = name in present_names
    strength = detail = None
    if present:
        try:
            positions = {g.key: {"rasi": g.rasi, "longitude": g.longitude, "vargas": g.vargas}
                         for g in chart.grahas}
            sha = shadbala_context.shadbala_for_chart(chart).get("grahas", {})
            det = _yogas.detect_yogas(positions, chart.lagna_rasi,
                                      lagna_d9=chart.lagna_vargas.get("D9"),
                                      shadbala={"grahas": sha}, lang=lang)
            entry = next((e for e in det.get("detected", []) if e["name"] == name), None)
            if entry:
                strength, detail = entry.get("strength"), entry.get("detail")
        except Exception:  # noqa: BLE001
            pass
    grahas = _YOGA_GRAHAS.get(name, [])
    out = {"kind": "yoga", "name": name,
           "parsed": {"yoga": name, "kind": "yoga"},
           "yoga": {"name": name, "family": meta.get("family"), "effect": meta.get("effect"),
                    "citation": meta.get("citation"), "tier": meta.get("tier", "sloka"),
                    "computability": meta.get("computability"), "present": present,
                    "strength": strength, "grahas": grahas}}
    out["life"] = _life_block(chart, m_out, grahas, None) if grahas else None
    return out


def _explain_theme(chart, m_out, intent, lang):
    tk = intent["theme"]
    tv = next((t for t in m_out.get("themes", []) if t["key"] == tk), None)
    theme_def = next((t for t in _matrix.THEMES if t["key"] == tk), {})
    ledger = [{"factor": c.get("factor"), "house": c.get("house"), "graha": c.get("graha"),
               "role": c.get("role"), "chart": c.get("chart"), "value": c.get("value"),
               "weight": c.get("weight"), "detail": c.get("detail"),
               "citation": c.get("citation"), "tier": c.get("tier")}
              for c in (tv or {}).get("components", [])] if tv else []
    events = [{"from": e["from"], "to": e["to"], "good": e.get("good"), "peak": e.get("peak"),
               "house": e.get("house"), "lord": e.get("lord"), "cf": e.get("cf"),
               "driver": e.get("driver"), "maha": e.get("maha"), "antar": e.get("antar")}
              for e in m_out.get("timeline", {}).get("events", []) if e.get("key") == tk][:4]
    facets = _THEME_FACETS.get(tk, [])
    # a theme's activating grahas: its sthira kārakas + the lord of its primary house
    lord_of = {b["house"]: b["lord"] for b in m_out.get("bhavas", [])}
    prim_house = max(theme_def.get("houses", {1: 1}).items(), key=lambda x: x[1])[0]
    grahas = list(theme_def.get("sthira", {})) + ([lord_of.get(prim_house)] if lord_of.get(prim_house) else [])
    out = {"kind": "theme", "theme": tk, "parsed": {"theme": tk, "kind": "theme"},
           "verdict": ({"key": tv["key"], "name": tv["name"], "net": tv["net"],
                        "band": tv["band"], "ledger": ledger} if tv else None),
           "houses": sorted(theme_def.get("houses", {}), key=lambda h: -theme_def["houses"][h]),
           "karakas": list(theme_def.get("sthira", {})),
           "events": events}
    out["life"] = _life_block(chart, m_out, [g for g in grahas if g], facets[0] if facets else None)
    return out


def _explain_house(chart, m_out, intent, lang):
    house = intent["house"]
    nodes = m_out.get("nodes", {})
    occupants = [k for k, nd in nodes.items() if nd.get("bhava") == house]
    occ_readings = []
    for g in occupants:
        srcs = classical.readings_for(g, house=house, lang=lang)
        if srcs:
            occ_readings.append({"graha": g, "sources": [_one_source(s) for s in
                                 sorted(srcs, key=lambda s: _matrix._SOURCE_ORDER.get((s.get("source") or {}).get("id"), 5))]})
    bh = next((b for b in m_out.get("bhavas", []) if b["house"] == house), None)
    facets = _facets_for_house(house)
    lord = bh["lord"] if bh else None
    out = {"kind": "house", "house": house, "parsed": {"house": house, "kind": "house"},
           "bhava": _bhava_block(bh), "occupants": occupants, "occupantReadings": occ_readings,
           "reading": {"available": bool(occ_readings)}}
    out["life"] = _life_block(chart, m_out, [lord] if lord else [], facets[0] if facets else None)
    return out


_DISPATCH = {"placement": _explain_placement, "yoga": _explain_yoga,
             "theme": _explain_theme, "house": _explain_house}


def explain(chart, m_out: dict, query: str, lang: str = "en") -> dict:
    """Route one query to its intent composer against one chart's matrix."""
    intent = parse_query(query)
    if not intent:
        return {"query": query, "parsed": None, "suggestions": _SUGGESTIONS}
    fn = _DISPATCH.get(intent["kind"])
    if not fn:
        return {"query": query, "parsed": None, "suggestions": _SUGGESTIONS}
    out = fn(chart, m_out, intent, lang)
    out["query"] = query
    return out
