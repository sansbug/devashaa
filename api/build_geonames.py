"""Build the offline place database from GeoNames dumps.

Run this to (re)generate `data/geonames.sqlite3`, which `geocode.py` queries.
The generated DB is committed, so deployment never depends on geonames.org.

Download these into a folder first (https://download.geonames.org/export/dump/):
    cities1000.zip  (unzip -> cities1000.txt)   population >= 1,000  <- best coverage
      or cities5000.zip / cities15000.zip       smaller, fewer villages
    admin1CodesASCII.txt                        state/province names
    countryInfo.txt                             country names

    python build_geonames.py <folder-with-those-files> [-o data/geonames.sqlite3]

The densest cities*.txt present is used unless --cities names one explicitly.

Data: GeoNames (https://www.geonames.org), licensed CC BY 4.0. Attribution is
required wherever the data is surfaced — see the site footer.
"""

from __future__ import annotations

import argparse
import difflib
import io
import os
import sqlite3
import unicodedata

# cities file column indices (19 tab-separated columns)
C_NAME, C_ASCII, C_ALT = 1, 2, 3
C_LAT, C_LON = 4, 5
C_FCODE = 7
C_COUNTRY, C_ADMIN1 = 8, 10
C_POP, C_TZ = 14, 17

MAX_ALT_PER_CITY = 12

# An alias this similar to the primary name is just a transliteration of it
# ("Cennai", "Chennaj", "Csennai" for Chennai) and is dead weight — the primary
# name is already indexed. Dropping them frees the budget for the aliases that
# actually matter: the historical names people write on birth records
# ("Madras", "Bombay", "Calcutta", "Benares"), which are by nature dissimilar.
ALIAS_SIMILARITY_DROP = 0.72

# Populated places only — drop farms, sections of cities, abandoned places, etc.
KEEP_FCODES = {
    "PPL", "PPLA", "PPLA2", "PPLA3", "PPLA4", "PPLA5",
    "PPLC", "PPLG", "PPLS", "PPLX", "PPLL",
}


def _is_latin(s: str) -> bool:
    """True if every letter is Latin — filters out Devanagari/Arabic/CJK aliases
    that a user typing on a Latin keyboard will never match."""
    for ch in s:
        if ch.isalpha() and not unicodedata.name(ch, "").startswith("LATIN"):
            return False
    return True


def _fold(s: str) -> str:
    """Lowercase, strip diacritics, keep only alphanumerics — for comparison."""
    d = unicodedata.normalize("NFKD", s.lower())
    return "".join(ch for ch in d if ch.isalnum() and not unicodedata.combining(ch))


def _pick_aliases(alternates: list[str], primary_folds: set[str],
                  seen: set[str]) -> list[str]:
    """Choose the most useful aliases: drop mere transliterations of the primary
    name, then prefer the most dissimilar (i.e. genuinely different) names."""
    ref = next(iter(primary_folds))
    scored = []
    for alt in alternates:
        a = alt.strip()
        t = a.lower()
        f = _fold(a)
        if not (2 <= len(a) <= 60) or not f or t in seen or f in primary_folds:
            continue
        if not _is_latin(a):
            continue
        sim = difflib.SequenceMatcher(None, f, ref).ratio()
        if sim >= ALIAS_SIMILARITY_DROP:
            continue
        scored.append((sim, t))
    # Most dissimilar first, so distinct historical names win the budget.
    scored.sort()
    out, folds = [], set()
    for _, t in scored:
        f = _fold(t)
        if f in folds:
            continue
        folds.add(f)
        out.append(t)
        if len(out) >= MAX_ALT_PER_CITY:
            break
    return out


def load_countries(path: str) -> dict[str, str]:
    out = {}
    with io.open(path, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            c = line.split("\t")
            if len(c) > 4:
                out[c[0]] = c[4]
    return out


def load_admin1(path: str) -> dict[str, str]:
    out = {}
    with io.open(path, encoding="utf-8") as f:
        for line in f:
            c = line.rstrip("\n").split("\t")
            if len(c) >= 2:
                out[c[0]] = c[1]
    return out


def find_cities_file(src_dir: str) -> str:
    """Pick the densest cities dump available (lower threshold = more villages)."""
    for name in ("cities1000.txt", "cities5000.txt", "cities15000.txt"):
        p = os.path.join(src_dir, name)
        if os.path.exists(p):
            return p
    raise SystemExit(f"No cities*.txt found in {src_dir}")


def build(src_dir: str, out_path: str, cities_file: str | None = None) -> None:
    countries = load_countries(os.path.join(src_dir, "countryInfo.txt"))
    admin1 = load_admin1(os.path.join(src_dir, "admin1CodesASCII.txt"))
    cities_path = cities_file or find_cities_file(src_dir)
    print(f"{len(countries)} countries, {len(admin1)} admin1 regions")
    print(f"source: {os.path.basename(cities_path)}")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    if os.path.exists(out_path):
        os.remove(out_path)
    db = sqlite3.connect(out_path)
    db.executescript("""
        PRAGMA journal_mode = OFF;
        CREATE TABLE cities (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            admin1 TEXT,
            country TEXT,
            lat REAL NOT NULL,
            lon REAL NOT NULL,
            tz TEXT NOT NULL,
            pop INTEGER NOT NULL
        );
        -- One row per searchable term (primary, ascii, and Latin aliases).
        -- `pop` is denormalised from cities purely for the (term, pop) index:
        -- it lets a prefix query order by population without joining and
        -- grouping the whole match set. On a one-letter prefix (~48k matching
        -- terms) that is the difference between ~480 ms and ~11 ms.
        CREATE TABLE names (
            city_id INTEGER NOT NULL,
            term TEXT NOT NULL,
            is_alt INTEGER NOT NULL,
            pop INTEGER NOT NULL
        );
    """)

    cities, names = [], []
    kept = skipped = 0
    with io.open(cities_path, encoding="utf-8") as f:
        for line in f:
            c = line.rstrip("\n").split("\t")
            if len(c) < 19 or c[C_FCODE] not in KEEP_FCODES:
                skipped += 1
                continue
            cid = int(c[0])
            name = c[C_NAME].strip()
            ascii_name = c[C_ASCII].strip()
            if not name or not c[C_TZ].strip():
                skipped += 1
                continue

            cities.append((
                cid, name,
                admin1.get(f"{c[C_COUNTRY]}.{c[C_ADMIN1]}", ""),
                countries.get(c[C_COUNTRY], c[C_COUNTRY]),
                float(c[C_LAT]), float(c[C_LON]), c[C_TZ].strip(),
                int(c[C_POP] or 0),
            ))

            pop = int(c[C_POP] or 0)
            seen, primary_folds = set(), set()
            for term in (name, ascii_name):
                t = term.lower().strip()
                if t and t not in seen:
                    seen.add(t)
                    primary_folds.add(_fold(t))
                    names.append((cid, t, 0, pop))
            for t in _pick_aliases(c[C_ALT].split(","), primary_folds, seen):
                seen.add(t)
                names.append((cid, t, 1, pop))
            kept += 1

    db.executemany("INSERT INTO cities VALUES (?,?,?,?,?,?,?,?)", cities)
    db.executemany("INSERT INTO names VALUES (?,?,?,?)", names)
    db.executescript("""
        CREATE INDEX idx_names_term_pop ON names(term, pop DESC);
        CREATE INDEX idx_cities_pop ON cities(pop DESC);
    """)
    db.commit()
    db.execute("VACUUM")
    db.close()

    size_mb = os.path.getsize(out_path) / 1024 / 1024
    print(f"kept {kept} cities ({skipped} skipped), {len(names)} search terms")
    print(f"wrote {out_path}  ({size_mb:.1f} MB)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src_dir", help="folder holding the GeoNames dump files")
    ap.add_argument("-o", "--out", default=os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "data", "geonames.sqlite3"))
    ap.add_argument("--cities", default=None,
                    help="explicit cities*.txt (default: densest one present)")
    a = ap.parse_args()
    build(a.src_dir, a.out, a.cities)
