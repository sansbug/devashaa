"""Birth place -> coordinates + IANA timezone, fully offline.

Backed by a local SQLite database built from the GeoNames `cities5000` dump
(see build_geonames.py). No network call, no rate limit, no API key — which the
public Nominatim endpoint could not offer for production traffic.

GeoNames records carry their own IANA timezone, so a picked place needs no
timezone lookup at all; `timezone_at()` remains for raw coordinates.

Data: GeoNames (https://www.geonames.org), CC BY 4.0. Attribution is required
wherever results are shown — see the site footer.
"""

from __future__ import annotations

import math
import os
import sqlite3
import threading
from dataclasses import dataclass, asdict
from functools import lru_cache

from timezonefinder import TimezoneFinder

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "data", "geonames.sqlite3")

# How many name-rows (already population-ordered) to consider before ranking.
# Only bites on broad prefixes, where the biggest places are the right answer
# anyway; a specific name matches far fewer rows than this and is unaffected.
CANDIDATES = 400

_tf = TimezoneFinder()
_local = threading.local()


@dataclass
class Place:
    name: str
    latitude: float
    longitude: float
    timezone: str

    def to_dict(self) -> dict:
        return asdict(self)


def _conn() -> sqlite3.Connection:
    """One read-only connection per thread — sqlite3 connections are not
    shareable across threads, and gunicorn serves on a thread pool."""
    c = getattr(_local, "conn", None)
    if c is None:
        if not os.path.exists(DB_PATH):
            raise RuntimeError(
                f"Place database missing at {DB_PATH}. Build it with "
                "`python build_geonames.py <geonames-dump-dir>`."
            )
        c = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        _local.conn = c
    return c


def database_status() -> tuple[bool, str]:
    try:
        n = _conn().execute("SELECT COUNT(*) FROM cities").fetchone()[0]
        return True, f"{n} cities offline (GeoNames)"
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def timezone_at(latitude: float, longitude: float) -> str:
    """IANA zone for a raw coordinate. Falls back to a UTC-offset zone at sea."""
    tz = _tf.timezone_at(lat=latitude, lng=longitude)
    if tz is None:
        tz = _tf.certain_timezone_at(lat=latitude, lng=longitude)
    if tz is None:
        offset = round(longitude / 15.0)
        tz = f"Etc/GMT{-offset:+d}"
    return tz


def _display(name: str, admin1: str, country: str) -> str:
    return ", ".join(p for p in (name, admin1, country) if p)


@lru_cache(maxsize=1024)
def search(query: str, limit: int = 8) -> tuple[Place, ...]:
    """Prefix search over city names and their Latin aliases.

    Ranking blends match quality with log-population. Population has to carry
    real weight or a tiny exact match buries the intended city: "Calcutta" is
    the *primary* name of a hamlet in South Africa but only an *alias* of
    Kolkata, and "Madras" is a town in Oregon as well as an alias of Chennai.
    A birth-place box must return the metropolis. log10(pop) spans ~3 between a
    village and a megacity, which comfortably outweighs the match bonuses.

    Accepts "City, Region" too: text after the first comma filters on the
    region/country, so "Springfield, Illinois" narrows correctly.
    """
    q = (query or "").strip()
    if not q:
        return ()

    parts = [p.strip() for p in q.split(",") if p.strip()]
    term = parts[0].lower()
    qualifiers = [p.lower() for p in parts[1:]]
    if not term:
        return ()

    conn = _conn()

    # Range scan, not LIKE: terms are stored lowercased, so [term, term+￿) hits
    # the index directly (SQLite's LIKE is case-insensitive and forces a full
    # scan). Deliberately NO join/GROUP BY here — `pop` is denormalised into
    # names so the (term, pop) index alone answers this. Joining and grouping
    # the whole match set costs ~480 ms on a one-letter prefix vs ~11 ms here.
    rows = conn.execute(
        """
        SELECT city_id, term, is_alt FROM names
        WHERE term >= ? AND term < ?
        ORDER BY pop DESC
        LIMIT ?
        """,
        (term, term + "￿", CANDIDATES),
    ).fetchall()
    if not rows:
        return ()

    # Collapse the per-term rows to per-city, keeping the best match evidence.
    best: dict[int, list[int]] = {}
    for city_id, t, is_alt in rows:
        b = best.get(city_id)
        if b is None:
            b = best[city_id] = [1, 0, 0]  # best_is_alt, exact_primary, exact_alias
        if is_alt < b[0]:
            b[0] = is_alt
        if t == term:
            b[2 if is_alt else 1] = 1

    ids = list(best)
    cities = conn.execute(
        f"SELECT id, name, admin1, country, lat, lon, tz, pop FROM cities "
        f"WHERE id IN ({','.join('?' * len(ids))})", ids
    ).fetchall()

    if qualifiers:
        narrowed = [c for c in cities
                    if all(qf in f"{c[2]} {c[3]}".lower() for qf in qualifiers)]
        if narrowed:
            cities = narrowed

    def score(c):
        best_is_alt, exact_primary, exact_alias = best[c[0]]
        return (2.0 * exact_primary
                + 1.2 * exact_alias
                + 0.8 * (1 - best_is_alt)
                + math.log10(c[7] + 1))

    cities.sort(key=score, reverse=True)
    return tuple(
        Place(name=_display(c[1], c[2], c[3]), latitude=c[4], longitude=c[5],
              timezone=c[6])
        for c in cities[:limit]
    )
