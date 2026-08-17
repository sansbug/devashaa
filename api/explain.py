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
import gochara_rules
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
                 "love", "married", "marry", "wedding", "engaged", "engagement",
                 "divorce", "partnership"],
    "children": ["children", "child", "kids", "kid", "progeny", "son", "daughter",
                 "offspring", "fertility", "baby", "babies", "born"],
    "health": ["health", "illness", "disease", "sickness", "wellbeing", "wellness", "fitness"],
    "education": ["education", "learning", "study", "studies", "knowledge", "academics",
                  "school", "college", "intellect"],
    "home": ["home", "house", "property", "mother", "land", "vehicles", "comforts", "domestic"],
    "fortune": ["fortune", "luck", "dharma", "father", "religion", "spirituality", "faith"],
    "enemies": ["enemies", "enemy", "debt", "debts", "litigation", "rivals", "obstacles",
                "competition", "disputes"],
    "foreign": ["foreign", "abroad", "overseas", "moksha", "liberation", "expenses",
                "isolation"],
    "longevity": ["longevity", "lifespan", "age", "vitality", "die", "death", "dying", "dead"],
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
                "How is September 2026 looking?", "Chance of marriage next year",
                "When did my career rise?"]

# ── time vocabulary for period / when intents ────────────────────────────────────
_MONTH_WORDS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], 1)}
_MONTH_WORDS.update({"jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7,
                     "aug": 8, "sep": 9, "sept": 9, "oct": 10, "nov": 11, "dec": 12})


def _parse_window(tokens: list[str], folded: str):
    """A (y1, m1, y2, m2) month-window from the query, or None. 'may' needs an
    explicit year beside it (it is also a modal verb)."""
    today = _dt.date.today()
    year = next((int(t) for t in tokens if re.fullmatch(r"(19|20)\d\d", t)), None)
    mon = next((_MONTH_WORDS[t] for t in tokens
                if t in _MONTH_WORDS and (t != "may" or year is not None)), None)
    if "next year" in folded:
        y = today.year + 1
        return (y, 1, y, 12)
    if "this year" in folded:
        return (today.year, today.month, today.year, 12)
    if "next month" in folded:
        y, m = (today.year + 1, 1) if today.month == 12 else (today.year, today.month + 1)
        return (y, m, y, m)
    if "this month" in folded:
        return (today.year, today.month, today.year, today.month)
    if year and mon:
        return (year, mon, year, mon)
    if mon:                                     # bare month → its next occurrence
        y = today.year + (1 if mon < today.month else 0)
        return (y, mon, y, mon)
    if year:
        return (year, 1, year, 12)
    return None


def parse_query(q: str) -> dict | None:
    """Free text → a typed intent, or None. Priority: a graha (with/without a house
    or sign) → placement; else a yoga name → yoga; else a bare house number → house;
    else a theme word → theme."""
    if not q or not str(q).strip():
        return None
    folded = _fold(q)
    tokens = re.findall(r"[a-z0-9]+", folded)
    nospace = folded.replace(" ", "")
    window = _parse_window(tokens, folded)

    # 0 — mortality guard FIRST: any death-dating question gets the care refusal,
    # whoever it is about — before 'mother'→home or any other token can outrank it.
    if any(t in ("die", "death", "dying", "dead") for t in tokens):
        return {"kind": "when", "theme": "longevity", "direction": "future",
                "window": None, "mortality": True}

    # 1 — graha (→ daśā timing, or placement)
    graha = next((_GRAHA_ALIASES[t] for t in tokens if t in _GRAHA_ALIASES), None)
    if graha is None:
        graha = next((k for a, k in _GRAHA_COMPOUND.items() if a in nospace), None)
    if graha is not None:
        if any(t in ("dasha", "dasa", "mahadasha", "antardasha", "period", "periods") for t in tokens):
            return {"kind": "dasha", "graha": graha}
        sign = next((_RASI_ALIASES[t] for t in tokens if t in _RASI_ALIASES), None)
        if sign is not None:
            return {"kind": "placement", "graha": graha, "house": None, "sign": sign}
        house = _house_token(tokens)
        return {"kind": "placement", "graha": graha, "house": house, "sign": None,
                "window": window if house is None else None}

    # 2 — yoga
    yoga = next((_YOGA_ALIASES[t] for t in tokens if t in _YOGA_ALIASES), None)
    if yoga is None:                                   # multi-word like "gaja kesari"
        yoga = next((v for a, v in _YOGA_ALIASES.items() if len(a) > 5 and a in nospace), None)
    if yoga is not None:
        return {"kind": "yoga", "yoga": yoga}

    # 3 — timing questions: "when did/will …", "chance of …", a theme + a window
    theme = next((_THEME_ALIASES[t] for t in tokens if t in _THEME_ALIASES), None)
    past = bool(re.search(r"\bwhen\s+(did|was|were|had)\b", folded))
    future = bool(re.search(r"\bwhen\s+(will|would|shall|can|could|do|does|am|is|might|may)\b", folded)
                  or re.search(r"\b(chance|chances|likelihood|odds)\b", folded)
                  or re.search(r"\b(will|shall|can)\s+i\b", folded))
    if theme is not None and (past or future):
        return {"kind": "when", "theme": theme,
                "direction": "past" if past and not future else "future",
                "window": window}

    # 4 — a bare house (needs a house/bhava cue so "in 2020" isn't a house)
    if any(t in ("house", "bhava", "bhāva", "houses") for t in tokens):
        h = _house_token(tokens)
        if h:
            return {"kind": "house", "house": h, "window": window}

    # 5 — a theme scoped to a window: past windows look back, future ones ahead
    if theme is not None and window is not None:
        today = _dt.date.today()
        w_past = (window[2], window[3]) < (today.year, today.month)
        return {"kind": "when", "theme": theme,
                "direction": "past" if w_past else "future", "window": window}

    # 6 — a bare window ("how is september 2026 looking?") → the period overview
    if window is not None:
        return {"kind": "period", "window": window}

    # 7 — a life-theme word
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
def _transit_occupants_from_moon(jd, moon_sign):
    """House-from-Moon (1-12) -> transiting graha keys standing there, for the
    ch.26 vedha (obstruction) check."""
    occ: dict[int, list[str]] = {}
    for g, ipl in _SWE_ID.items():
        try:
            s = _matrix._transit_sign(jd, ipl)
        except Exception:  # noqa: BLE001
            continue
        occ.setdefault((s - moon_sign) % 12 + 1, []).append(g)
        if g == "rahu":
            occ.setdefault(((s + 6) % 12 - moon_sign) % 12 + 1, []).append("ketu")
    return occ


def _graha_transit(g, lagna, moon_sign, av, jd=None):
    """Where the graha transits at ``jd`` (default: today): sign, house from lagna &
    Moon, an aṣṭakavarga tone (its bindus in the transited sign) — and, where the
    extracted Phaladīpikā ch.26 text covers the graha, the cited gochara judgment
    (favourable / vedha-obstructed / not among its favourable houses)."""
    try:
        if jd is None:
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
    hfm = ((tsign - moon_sign) % 12 + 1) if moon_sign is not None else None
    out = {"sign": tsign, "houseFromLagna": (tsign - lagna) % 12 + 1,
           "houseFromMoon": hfm, "bindu": bindu, "tone": tone}
    if hfm is not None and (g in gochara_rules.FAVOURABLE or g in gochara_rules.PHALA):
        try:
            out["gochara"] = gochara_rules.transit_judgment(
                g, hfm, _transit_occupants_from_moon(jd, moon_sign))
        except Exception:  # noqa: BLE001
            pass
    return out


def _graha_facets(chart, m_out, g, jd=None):
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
            "transit": _graha_transit(g, lagna, moon_sign, m_out.get("ashtakavarga") or {}, jd=jd),
            "role": role}


# ── intent composers ─────────────────────────────────────────────────────────────
def _explain_placement(chart, m_out, intent, lang, geo=None):
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
    # "jupiter in 2027" — a graha with a window means its transit THEN, not just now
    tjd = None
    if intent.get("window"):
        wy1, wm1, wy2, wm2 = intent["window"]
        wmonths = _month_iter(wy1, wm1, wy2, wm2)
        my, mm = wmonths[len(wmonths) // 2]
        tjd = swe.julday(my, mm, 15, 12.0, swe.GREG_CAL)
        out["transitAsOf"] = f"{my:04d}-{mm:02d}"
    out["grahaFacets"] = _graha_facets(chart, m_out, g, jd=tjd)
    facets = _facets_for_house(house)
    out["life"] = _life_block(chart, m_out, [g], facets[0] if facets else None)
    return out


def _explain_yoga(chart, m_out, intent, lang, geo=None):
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


def _explain_theme(chart, m_out, intent, lang, geo=None):
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


def _explain_house(chart, m_out, intent, lang, geo=None):
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
    # "2nd house in 2027" — score the house's dominant life-theme over that window
    if intent.get("window"):
        tk = _HOUSE_THEME.get(house)
        if tk:
            ctx = _matrix._projection_context(chart, m_out)
            names = {t["key"]: t["name"] for t in m_out.get("themes", [])}
            wy1, wm1, wy2, wm2 = intent["window"]
            rows = []
            for (y, m) in _month_iter(wy1, wm1, wy2, wm2):
                jd = max(chart.jd_ut, swe.julday(y, m, 15, 12.0, swe.GREG_CAL))
                tv = _matrix._project_at(jd, ctx)["themes"].get(tk)
                rows.append((tv["v"], tv["cf"]))
            if rows:
                fv = sum(v for v, _ in rows) / len(rows)
                out["focus"] = {"from": f"{wy1:04d}-{wm1:02d}", "to": f"{wy2:04d}-{wm2:02d}",
                                "theme": tk, "themeName": names.get(tk, tk),
                                "v": round(fv, 3),
                                "cf": round(sum(c for _, c in rows) / len(rows), 2),
                                "tone": "supportive" if fv >= 0.08 else "challenging" if fv <= -0.08 else "neutral"}
    out["life"] = _life_block(chart, m_out, [lord] if lord else [], facets[0] if facets else None)
    return out


# ── period + when intents: "how is Sep 2026?", "when did/will …?" ────────────────
def _month_iter(y1, m1, y2, m2, cap=12):
    out = []
    y, m = y1, m1
    while (y, m) <= (y2, m2) and len(out) < cap:
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def _panchang_summary(chart, geo, months):
    """Chart-tailored auspicious-day counts for a short window (≤2 months) — the
    same tārā/candra/transit/daśā-fit/day-quality score the Pañcāṅga tab uses."""
    if not geo or len(months) > 2:
        return None
    try:
        import calendar as _cal
        import panchang as _pan
        import panchang_score as _ps
        import vimshottari as _vim
        moon = next(g for g in chart.grahas if g.key == "moon")
        birth = {"moon_nak": moon.nakshatra.index, "moon_sign": moon.rasi,
                 "lagna_sign": chart.lagna_rasi}
        lat, lon, tz = geo["latitude"], geo["longitude"], geo["timezone"]
        counts = {"auspicious": 0, "mixed": 0, "inauspicious": 0}
        best = []
        for (y, m) in months:
            for dd in range(1, _cal.monthrange(y, m)[1] + 1):
                try:
                    d = _dt.date(y, m, dd)
                    pan = _pan.panchanga(d, lat, lon, tz)
                    lords = _vim.running_lords(chart.jd_ut, birth["moon_nak"],
                                               moon.nakshatra.fraction,
                                               swe.julday(y, m, dd, 12.0, swe.GREG_CAL), depth=2)
                    birth["dasha_maha"] = lords[0] if lords else None
                    birth["dasha_antar"] = lords[1] if len(lords) > 1 else None
                    sc = _ps.score_day(pan, birth)
                    counts[sc["band"]] = counts.get(sc["band"], 0) + 1
                    best.append({"date": d.isoformat(), "score": sc["score"]})
                except Exception:  # noqa: BLE001
                    continue
        if not best:
            return None
        best.sort(key=lambda x: -x["score"])
        return {**counts, "days": sum(counts.values()), "best": best[:3]}
    except Exception:  # noqa: BLE001
        return None


def _explain_period(chart, m_out, intent, lang, geo=None):
    y1, mm1, y2, mm2 = intent["window"]
    months = _month_iter(y1, mm1, y2, mm2)
    # honesty guard: no confident readings for a window before the birth itself
    bj = swe.revjul(chart.jd_ut, swe.GREG_CAL)
    birth_ym = (int(bj[0]), int(bj[1]))
    if (months[-1][0], months[-1][1]) < birth_ym:
        return {"kind": "period", "parsed": {"kind": "period"}, "preBirth": True,
                "birth": f"{birth_ym[0]:04d}-{birth_ym[1]:02d}",
                "window": {"from": f"{y1:04d}-{mm1:02d}", "to": f"{y2:04d}-{mm2:02d}",
                           "months": len(months)}}
    months = [m for m in months if m >= birth_ym] or [birth_ym]
    ctx = _matrix._projection_context(chart, m_out)
    names = {t["key"]: t["name"] for t in m_out.get("themes", [])}
    per_theme: dict[str, list] = {}
    dashas = []
    for (y, m) in months:
        jd = swe.julday(y, m, 15, 12.0, swe.GREG_CAL)
        pj = _matrix._project_at(jd, ctx)
        if not dashas or (dashas[-1]["maha"], dashas[-1]["antar"]) != (pj["maha"], pj["antar"]):
            dashas.append({"month": f"{y:04d}-{m:02d}", "maha": pj["maha"], "antar": pj["antar"]})
        for tk, tv in pj["themes"].items():
            per_theme.setdefault(tk, []).append((tv["v"], tv["cf"]))
    agg = {tk: {"key": tk, "name": names.get(tk, tk),
                "v": round(sum(v for v, _ in rows) / len(rows), 3),
                "cf": round(sum(c for _, c in rows) / len(rows), 2)}
           for tk, rows in per_theme.items()}
    ranked = sorted(agg.values(), key=lambda a: -a["v"])
    overall = round(sum(a["v"] for a in agg.values()) / max(1, len(agg)), 3)

    lo, hi = f"{y1:04d}-{mm1:02d}", f"{months[-1][0]:04d}-{months[-1][1]:02d}"

    def _overlaps(a_from, a_to):
        return a_from[:7] <= hi and a_to[:7] >= lo

    events = [e for e in m_out.get("timeline", {}).get("events", [])
              if _overlaps(e.get("from", ""), e.get("to", ""))]
    changes = []
    for grp in ("health", "wealthCareer", "relationships"):
        for e in (m_out.get("changes") or {}).get(grp, []):
            if e.get("care"):
                continue
            if _overlaps(e.get("from", e.get("date", "")), e.get("to", e.get("date", ""))):
                changes.append({"group": grp, "label": e.get("label"), "date": e.get("date"),
                                "cf": e.get("cf"), "triggerType": e.get("triggerType")})
    mid = months[len(months) // 2]
    mid_jd = swe.julday(mid[0], mid[1], 15, 12.0, swe.GREG_CAL)
    nodes = m_out.get("nodes", {})
    moon_sign = nodes.get("moon", {}).get("rasi")
    av = m_out.get("ashtakavarga") or {}
    transits = [{"graha": g, **(_graha_transit(g, chart.lagna_rasi, moon_sign, av, jd=mid_jd) or {})}
                for g in ("jupiter", "saturn", "sun")]

    return {"kind": "period", "parsed": {"kind": "period", "from": lo, "to": hi},
            "window": {"from": lo, "to": hi, "months": len(months)},
            "overall": overall, "dasha": dashas,
            "themes": {"best": [a for a in ranked[:3] if a["v"] > 0.05],
                       "strain": [a for a in ranked[::-1][:3] if a["v"] < -0.05]},
            "events": events[:5], "changes": changes[:6], "transits": transits,
            "panchang": _panchang_summary(chart, geo, months)}


# Sensible age floors for event-timing questions. The math can show a life-event
# axis "activated" in childhood (a daśā favours the 5th house at age 2), but nobody
# has children at 2 or marries at 6 — so timing windows below the floor are not
# shown, and the floor is stated openly in the answer rather than applied silently.
_THEME_AGE_FLOOR = {"marriage": 18, "children": 20, "career": 16, "wealth": 16,
                    "home": 16, "foreign": 5, "enemies": 14, "education": 3}

# ── specific event texts for timing windows ──────────────────────────────────────
_XREF = re.compile(r"^\s*(?:same|as above|see above)", re.I)
_VREF = re.compile(r"vv?\.?\s*([0-9]+(?:\.[0-9]+)?(?:\s*-\s*[0-9]+(?:\.[0-9]+)?)?)")


def _resolve_results(cell, cond):
    """The mined corpus keeps the text's own back-references ('same list as
    vv.60-61.5', 'as above') instead of duplicating result lists. Follow the text's
    OWN pointer — to the condition whose śloka carries those verse numbers, or to
    the previous branch for a bare 'as above' — never inventing; unresolvable
    references yield nothing."""
    text = (cond.get("results") or "").strip()
    if not text or not _XREF.match(text):
        return text
    conds = cell.get("conditions") or []
    m = _VREF.search(text)
    if m:
        ref = m.group(1).replace(" ", "").split("-")[0]
        for other in conds:
            if other is cond:
                continue
            q = (other.get("quote") or "").lstrip()
            if q.startswith(ref):
                alt = (other.get("results") or "").strip()
                if alt and not _XREF.match(alt):
                    return alt
        return ""
    try:
        i = conds.index(cond)
    except ValueError:
        return ""
    for j in range(i - 1, -1, -1):
        alt = (conds[j].get("results") or "").strip()
        if alt and not _XREF.match(alt):
            return alt
    return ""


def _bhps_for_window(chart, tk, maha, antar, good=True):
    """The SPECIFIC classical prediction for a (mahā, antar) window, theme-matched.
    BPHS ch.52-60's antardaśā conditions are chart-gated (they fire on the antar
    lord's house in THIS chart) and their results are concrete event lists — 'birth
    of a son', 'gain of position through the ruler', 'marriage functions in the
    family'. We quote only a FIRED condition whose text matches the asked theme and
    doesn't contradict the window's direction; if none fires, no quote (cite-or-
    refuse) — never a paraphrase."""
    if not maha or not antar:
        return None
    try:
        import antardasa
        cell = antardasa.evaluate_cell(maha, antar,
                                       positions={g.key: g.rasi for g in chart.grahas},
                                       lagna=chart.lagna_rasi)
    except Exception:  # noqa: BLE001
        return None
    if not cell:
        return None
    kws = _matrix._THEME_KW.get(tk, [])
    best, best_score, general = None, 0, None
    for cond in cell.get("fired", []):
        text = _resolve_results(cell, cond)
        if not text:
            continue
        low = text.lower()
        val = _matrix._valence(low)
        if (good and val < 0) or ((not good) and val > 0):
            continue                       # never attach a contradicting quote
        score = _matrix._kw_score(low, kws)
        if score > best_score:
            best, best_score = (cond, text), score
        elif general is None:
            general = (cond, text)
    pick = best or general
    if not pick:
        return None
    cond, text = pick
    if len(text) > 240:
        text = text[:240].rsplit(",", 1)[0] + "…"
    return {"text": text, "cite": f"{cell.get('chapter', 'BPHS')} vv.{cell.get('verses')}",
            "reading": cond.get("reading"), "general": best is None}


def _yoga_indications(chart, m_out, tk):
    """Detected yogas whose cited BPHS effect speaks to the asked theme, each tied
    (classical principle) to the daśā windows of its forming grahas — a standing
    promise and WHEN it is most likely to fructify. Quote + citation only."""
    kws = _matrix._THEME_KW.get(tk, [])
    hits = []
    for y in m_out.get("yogas", []):
        meta = yoga_rules.YOGAS.get(y["name"]) or {}
        eff = (meta.get("effect") or "").lower()
        if not eff or _matrix._kw_score(eff, kws) <= 0:
            continue
        hits.append((y["name"], meta))
        if len(hits) >= 2:
            break
    if not hits:
        return []
    ribbon = None
    out = []
    for name, meta in hits:
        grahas = _YOGA_GRAHAS.get(name, [])
        windows = []
        if grahas:
            if ribbon is None:
                try:
                    ribbon = _matrix.lifearc(chart, m_out).get("ribbon", [])
                except Exception:  # noqa: BLE001
                    ribbon = []
            windows = [{"from": s["from"], "to": s["to"], "lord": s["lord"]}
                       for s in ribbon if s.get("lord") in grahas]
        eff = meta.get("effect") or ""
        if len(eff) > 240:
            eff = eff[:240].rsplit(",", 1)[0] + "…"
        out.append({"yoga": name, "effect": eff, "citation": meta.get("citation"),
                    "grahas": grahas, "windows": windows})
    return out


_WHEN_REFUSE = {
    "en": ("Questions of lifespan are not dated here — by design. The tradition treats "
           "them as a call to care and presence, not a forecast; so does this site."),
    "hi": ("आयु-संबंधी प्रश्नों की तिथि यहाँ नहीं दी जाती — यह हमारा सिद्धांत है। परंपरा इन्हें "
           "देखभाल और उपस्थिति का आह्वान मानती है, भविष्यवाणी नहीं; यह स्थल भी।"),
}


def _explain_when(chart, m_out, intent, lang, geo=None):
    tk, direction = intent["theme"], intent["direction"]
    names = {t["key"]: t["name"] for t in m_out.get("themes", [])}
    base = {"kind": "when", "theme": tk, "themeName": names.get(tk, tk),
            "direction": direction, "parsed": {"kind": "when", "theme": tk, "direction": direction},
            "care": False}
    if tk == "longevity":
        # No dating of lifespan, past or future, one's own or anyone else's.
        return {**base, "care": True, "refusal": _WHEN_REFUSE.get(lang, _WHEN_REFUSE["en"]),
                "windows": [], "changes": [], "focus": None, "empty": True}

    ctx = _matrix._projection_context(chart, m_out)
    floor = _THEME_AGE_FLOOR.get(tk, 0)
    by = int(swe.revjul(chart.jd_ut, swe.GREG_CAL)[0])
    if direction == "past":
        # Yearly walk from the age floor → now. Windows are RELATIVE — years the
        # theme ran clearly above its own average over the SENSIBLE span — so a
        # strained axis still shows when it was most activated, and the delta says
        # by how much. The mean deliberately excludes the sub-floor years too.
        now_y = _dt.date.today().year
        series = []
        for yr in range(by + floor, now_y + 1):
            jd = max(chart.jd_ut, swe.julday(yr, 6, 15, 12.0, swe.GREG_CAL))
            pj = _matrix._project_at(jd, ctx)
            tv = pj["themes"].get(tk)
            series.append((yr, tv["v"], tv["cf"], pj["maha"], pj["antar"]))
        if not series:
            return {**base, "windows": [], "changes": [], "focus": None,
                    "ageFloor": floor, "relative": True, "empty": True}
        mu = sum(v for _, v, _, _, _ in series) / max(1, len(series))
        sd = (sum((v - mu) ** 2 for _, v, _, _, _ in series) / max(1, len(series))) ** 0.5
        thr = mu + max(0.07, 0.5 * sd)
        wins, cur = [], None
        for (yr, v, cf, maha, antar) in series:
            if v >= thr:
                if cur is None:
                    cur = {"from": yr, "to": yr, "peak": yr, "v": v, "cf": cf,
                           "maha": maha, "antar": antar}
                else:
                    cur["to"] = yr
                    if v > cur["v"]:
                        cur.update({"peak": yr, "v": v, "cf": cf, "maha": maha, "antar": antar})
            elif cur:
                wins.append(cur); cur = None
        if cur:
            wins.append(cur)
        wins.sort(key=lambda w: -((w["v"] - mu) * max(w["cf"], 0.1)))
        for w in wins[:4]:
            w["delta"] = round(w["v"] - mu, 3)
            w["age"] = w["peak"] - by
            w["v"], w["cf"] = round(w["v"], 3), round(w["cf"], 2)
            w["bhps"] = _bhps_for_window(chart, tk, w["maha"], w["antar"], good=True)
        focus = None
        if intent.get("window"):
            wy1, wm1, wy2, wm2 = intent["window"]
            wmonths = [(y, m) for (y, m) in _month_iter(wy1, wm1, wy2, wm2)
                       if y - by >= floor]
            rows = []
            for (y, m) in wmonths:
                jd = max(chart.jd_ut, swe.julday(y, m, 15, 12.0, swe.GREG_CAL))
                tv = _matrix._project_at(jd, ctx)["themes"].get(tk)
                rows.append((tv["v"], tv["cf"]))
            if rows:
                fv = sum(v for v, _ in rows) / len(rows)
                fc = sum(c for _, c in rows) / len(rows)
                d = fv - mu
                focus = {"from": f"{wmonths[0][0]:04d}-{wmonths[0][1]:02d}",
                         "to": f"{wmonths[-1][0]:04d}-{wmonths[-1][1]:02d}",
                         "v": round(fv, 3), "cf": round(fc, 2), "delta": round(d, 3),
                         "tone": "supportive" if d >= 0.07 else "challenging" if d <= -0.07 else "neutral",
                         "changesInWindow": []}
        return {**base, "windows": wins[:4], "changes": [], "focus": focus,
                "indications": _yoga_indications(chart, m_out, tk),
                "ageFloor": floor, "lifeMean": round(mu, 3), "relative": True,
                "empty": not wins}

    # future: the 36-month timeline for this theme + its typed change events.
    # Windows are relative here too — months clearly above the horizon's own mean —
    # and the same age floor applies (a young chart asking about marriage gets
    # windows only from a sensible age on).
    steps = [s for s in m_out.get("timeline", {}).get("steps", [])
             if int(s["date"][:4]) - by >= floor]
    vs = [s["themes"].get(tk, 0.0) for s in steps] or [0.0]
    mu = sum(vs) / len(vs)
    sd = (sum((v - mu) ** 2 for v in vs) / len(vs)) ** 0.5
    thr = mu + max(0.07, 0.5 * sd)
    wins, cur = [], None
    for i, s in enumerate(steps):
        v, cf = s["themes"].get(tk, 0.0), s["conv"].get(tk, 0.0)
        mm = s["date"][:7]
        if v >= thr:
            clk = s["clocks"].get(tk, {})
            drv = max(((n, x) for n, x in clk.items() if x is not None),
                      key=lambda p: abs(p[1]), default=(None, 0))[0]
            if cur is None:
                cur = {"from": mm, "to": mm, "peak": mm, "v": v, "cf": cf,
                       "maha": s.get("maha"), "antar": s.get("antar"), "driver": drv}
            else:
                cur["to"] = mm
                if v > cur["v"]:
                    cur.update({"peak": mm, "v": v, "cf": cf, "maha": s.get("maha"),
                                "antar": s.get("antar"), "driver": drv})
        elif cur:
            wins.append(cur); cur = None
    if cur:
        wins.append(cur)
    wins.sort(key=lambda w: -((w["v"] - mu) * max(w["cf"], 0.1)))
    for w in wins[:4]:
        w["delta"] = round(w["v"] - mu, 3)
        w["age"] = int(w["peak"][:4]) - by
        w["v"], w["cf"] = round(w["v"], 3), round(w["cf"], 2)
        w["bhps"] = _bhps_for_window(chart, tk, w.get("maha"), w.get("antar"), good=True)

    sig_keys = {s["key"] for s in _matrix.CHANGE_SIGS
                if s.get("theme") == tk and not s.get("care")}
    changes = []
    for grp in ("health", "wealthCareer", "relationships"):
        for e in (m_out.get("changes") or {}).get(grp, []):
            if e.get("key") in sig_keys and e.get("date") \
                    and int(e["date"][:4]) - by >= floor:
                changes.append({"label": e.get("label"), "date": e.get("date"),
                                "cf": e.get("cf"), "triggerType": e.get("triggerType"),
                                "direction": e.get("direction"),
                                "maha": e.get("maha"), "antar": e.get("antar"),
                                "bhps": _bhps_for_window(chart, tk, e.get("maha"), e.get("antar"),
                                                         good=e.get("direction") != "down")})
    changes.sort(key=lambda e: e.get("date") or "")

    focus = None
    if intent.get("window"):
        y1, mm1, y2, mm2 = intent["window"]
        lo, hi = f"{y1:04d}-{mm1:02d}", f"{y2:04d}-{mm2:02d}"
        rows = [(s["themes"].get(tk, 0.0), s["conv"].get(tk, 0.0))
                for s in steps if lo <= s["date"][:7] <= hi]
        if rows:
            fv = sum(v for v, _ in rows) / len(rows)
            fc = sum(c for _, c in rows) / len(rows)
            focus = {"from": lo, "to": hi, "v": round(fv, 3), "cf": round(fc, 2),
                     "tone": "supportive" if fv >= 0.08 else "challenging" if fv <= -0.08 else "neutral",
                     "changesInWindow": [c for c in changes if c["date"] and lo <= c["date"][:7] <= hi]}
    return {**base, "windows": wins[:4], "changes": changes[:5], "focus": focus,
            "indications": _yoga_indications(chart, m_out, tk),
            "ageFloor": floor, "lifeMean": round(mu, 3), "relative": True,
            "empty": not wins and not changes}


def _explain_dasha(chart, m_out, intent, lang, geo=None):
    """"When does my Saturn period end?" — the graha's actual Viṁśottarī mahādaśā
    spans across the 120-year cycle, current one marked, with the running antar."""
    import vimshottari as _vim
    g = intent["graha"]
    moon = next(x for x in chart.grahas if x.key == "moon")
    now = _dt.datetime.utcnow()
    now_jd = swe.julday(now.year, now.month, now.day, 12.0, swe.GREG_CAL)
    tree = _vim.build_vimshottari(chart.jd_ut, moon.nakshatra.index, moon.nakshatra.fraction,
                                  depth=2, as_of_jd=now_jd,
                                  tz_name=(geo or {}).get("timezone"))
    periods, current = [], None
    for mh in tree.get("mahadashas", []):
        row = {"lord": mh["lord"], "from": str(mh["start"])[:10], "to": str(mh["end"])[:10],
               "years": mh.get("years"), "current": bool(mh.get("is_current"))}
        if mh.get("is_current"):
            antar = next((s for s in (mh.get("sub") or []) if s.get("is_current")), None)
            current = {"maha": mh["lord"], "mahaEnd": row["to"],
                       "antar": antar and antar.get("lord"),
                       "antarEnd": antar and str(antar.get("end"))[:10]}
        if mh["lord"] == g:
            periods.append(row)
    return {"kind": "dasha", "graha": g, "parsed": {"kind": "dasha", "graha": g},
            "periods": periods, "current": current,
            "balanceAtBirth": tree.get("balance_at_birth"),
            "yearSystem": tree.get("year_system")}


_DISPATCH = {"placement": _explain_placement, "yoga": _explain_yoga,
             "theme": _explain_theme, "house": _explain_house,
             "period": _explain_period, "when": _explain_when,
             "dasha": _explain_dasha}


def explain(chart, m_out: dict, query: str, lang: str = "en", geo: dict | None = None) -> dict:
    """Route one query to its intent composer against one chart's matrix."""
    intent = parse_query(query)
    if not intent:
        return {"query": query, "parsed": None, "suggestions": _SUGGESTIONS}
    fn = _DISPATCH.get(intent["kind"])
    if not fn:
        return {"query": query, "parsed": None, "suggestions": _SUGGESTIONS}
    out = fn(chart, m_out, intent, lang, geo)
    out["query"] = query
    return out
