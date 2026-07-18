"""Birth place -> coordinates + IANA timezone.

Deliberately thin and swappable: everything downstream needs is (lat, lon, tz).
Nominatim is the default because it needs no API key and no committed data dump,
but it is rate-limited to ~1 req/sec by OSM's usage policy, so results are cached.

If you'd rather run fully offline, drop in a GeoNames `cities15000` dump and
reimplement `search()` — nothing else has to change.
"""

from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from functools import lru_cache

from timezonefinder import TimezoneFinder

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
# OSM's policy requires a real identifying UA on every request. Set NOMINATIM_UA
# in the environment for deployment (a contact URL/email for your site).
# NOTE: the public Nominatim endpoint is NOT for production traffic (1 req/sec,
# no heavy use). Swap in an offline city DB or a paid geocoder before real load.
USER_AGENT = os.environ.get(
    "NOMINATIM_UA", "astrodev-dev (Vedic chart calculator; local development)"
)

_tf = TimezoneFinder()
_last_request_at = 0.0


@dataclass
class Place:
    name: str
    latitude: float
    longitude: float
    timezone: str

    def to_dict(self) -> dict:
        return asdict(self)


def timezone_at(latitude: float, longitude: float) -> str:
    """IANA zone for a coordinate. Falls back to a UTC-offset zone at sea."""
    tz = _tf.timezone_at(lat=latitude, lng=longitude)
    if tz is None:
        tz = _tf.certain_timezone_at(lat=latitude, lng=longitude)
    if tz is None:
        # Open ocean: approximate from longitude so the chart still computes.
        offset = round(longitude / 15.0)
        tz = f"Etc/GMT{-offset:+d}"
    return tz


def _throttle() -> None:
    global _last_request_at
    elapsed = time.time() - _last_request_at
    if elapsed < 1.1:
        time.sleep(1.1 - elapsed)
    _last_request_at = time.time()


@lru_cache(maxsize=512)
def search(query: str, limit: int = 8) -> tuple[Place, ...]:
    """Look up a place name. Returns candidates ordered by OSM's relevance."""
    if not query or not query.strip():
        return ()

    _throttle()
    params = urllib.parse.urlencode({
        "q": query.strip(),
        "format": "jsonv2",
        "limit": limit,
        "addressdetails": 1,
    })
    req = urllib.request.Request(
        f"{NOMINATIM_URL}?{params}",
        headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = json.loads(resp.read().decode("utf-8"))

    places = []
    for row in raw:
        lat, lon = float(row["lat"]), float(row["lon"])
        places.append(Place(
            name=row.get("display_name", query),
            latitude=lat,
            longitude=lon,
            timezone=timezone_at(lat, lon),
        ))
    return tuple(places)
