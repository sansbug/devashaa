"""Flask API — BPHS/Jyotiṣa chart service.

Sidereal (Lahiri), whole-sign bhāvas, nine grahas. See docs/bphs-rules.md.
"""

from __future__ import annotations

import os
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS

import swisseph as swe

from vedic import (
    compute_chart, ephemeris_status,
    RASIS, RASIS_IAST, RASIS_EN, RASI_LORDS, RASI_LORDS_IAST, RASI_LORDS_EN,
)
from vargas import VARGAS
from vimshottari import DEFAULT_YEAR_DAYS, YEAR_DAYS_SAVANA, YEAR_DAYS_JULIAN
from dashas import (
    SYSTEMS, build_dasha_system, validated_systems, ASHTOTTARI, build_ashtottari,
)
from dignity import dignity_of, sign_landmarks, nakshatra_gandanta
from analysis import analyse
from rasis import all_rasis, rasi
from geocode import search, timezone_at, database_status

app = Flask(__name__)
# In production set ALLOWED_ORIGINS to your site, e.g.
# "https://devashaa.com,https://www.devashaa.com". Defaults to * for local dev.
_origins = os.environ.get("ALLOWED_ORIGINS", "*")
CORS(app, origins="*" if _origins == "*" else [o.strip() for o in _origins.split(",")])

# The loaded .se1 files (sepl_18 / semo_18) cover 1800-2399.
EPHE_YEAR_MIN, EPHE_YEAR_MAX = 1800, 2399

# Daśā systems we expose: the udu systems whose BPHS example reproduces, plus
# Aṣṭottarī (group method, validated numerically against its own examples).
VALID_DASHAS = validated_systems() + ["ashtottari"]


def _now_jd():
    now = datetime.utcnow()
    return swe.julday(now.year, now.month, now.day,
                      now.hour + now.minute / 60.0, swe.GREG_CAL)


def _dasha_variants(system_key, birth_jd, nak_index, nak_fraction, moon_longitude,
                    tz_name, as_of_jd):
    """A daśā system's tree in both year-length variants for client-side toggle.

    Aṣṭottarī uses the group method (needs the Moon's longitude for Abhijit);
    the udu systems use nakṣatra index + fraction.
    """
    def one(year_days):
        if system_key == "ashtottari":
            return build_ashtottari(moon_longitude, birth_jd, depth=3,
                                    as_of_jd=as_of_jd, tz_name=tz_name,
                                    year_days=year_days)
        return build_dasha_system(
            SYSTEMS[system_key], birth_jd, nak_index, nak_fraction, depth=3,
            as_of_jd=as_of_jd, tz_name=tz_name, year_days=year_days)

    return {
        "default_year_days": DEFAULT_YEAR_DAYS,
        "variants": {"360": one(YEAR_DAYS_SAVANA), "365.25": one(YEAR_DAYS_JULIAN)},
    }


def _system_meta(key):
    s = ASHTOTTARI if key == "ashtottari" else SYSTEMS[key]
    return {"key": key, "name": s.name, "total_years": s.total_years,
            "applicability": s.applicability, "citation": s.citation}


@app.get("/api/health")
def health():
    """Confirms the ephemeris files are actually being read — not merely that the
    process is up. If sepl_18/semo_18 were missing, swisseph would silently fall
    back to its lower-precision Moshier theory and still return plausible-looking
    numbers, which is worse than an outright failure.
    """
    ephe_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ephe")
    files = sorted(os.listdir(ephe_dir)) if os.path.isdir(ephe_dir) else []

    # Must go through vedic.ephemeris_status(), NOT swisseph directly: swisseph's
    # config is thread-local and this request is on a worker thread, so the check
    # has to configure the same thread it then probes.
    try:
        ok, detail = ephemeris_status()
    except Exception as e:  # noqa: BLE001
        ok, detail = False, str(e)

    # The offline place DB is equally load-bearing — without it no chart can be
    # cast at all, so a missing file should show up here rather than as a 500.
    places_ok, places_detail = database_status()

    return jsonify({
        "status": "ok" if (ok and places_ok) else "degraded",
        "ephemeris": "Swiss Ephemeris .se1 (JPL DE431)" if ok else "FALLBACK/UNAVAILABLE",
        "ephe_files": files,
        "probe": detail,
        "places": places_detail if places_ok else f"UNAVAILABLE — {places_detail}",
        "swisseph_version": swe.version,
        "ayanamsa": "Lahiri (Chitrapakṣa)",
        "zodiac": "Sidereal",
        "bhava_system": "Whole sign",
    }), (200 if (ok and places_ok) else 503)


@app.get("/api/rasis")
def rasis_all():
    """The twelve rāśi reference cards.

    No date ranges, deliberately. BPHS has no sun-sign doctrine — there is not
    one statement of the form "one born with the Sun in X" in either volume,
    and ch.34, the closest thing to "what your sign means", is keyed to the
    LAGNA throughout. Printing tropical ranges would also contradict this
    site's own sidereal engine. Users reach their signs by casting a chart.
    """
    return jsonify({"rasis": all_rasis()})


@app.get("/api/rasis/<int:sign>")
def rasis_one(sign):
    if not 0 <= sign <= 11:
        return jsonify({"error": "sign must be 0-11 (Meṣa..Mīna)"}), 400
    return jsonify(rasi(sign))


@app.get("/api/reference")
def reference():
    """Static tables the UI needs to render a chart."""
    return jsonify({
        "rasis": [
            {
                "index": i,
                "name": RASIS[i], "name_iast": RASIS_IAST[i], "name_en": RASIS_EN[i],
                "lord": RASI_LORDS[i], "lord_iast": RASI_LORDS_IAST[i],
                "lord_en": RASI_LORDS_EN[i],
            }
            for i in range(12)
        ],
        "vargas": [{"key": k, "name_iast": sa, "name": en} for k, sa, en, _ in VARGAS],
        "naming_systems": [
            {"key": "common", "label": "Sanskrit", "example": "Chandra · Mesha"},
            {"key": "iast", "label": "Sanskrit (IAST)", "example": "Candra · Meṣa"},
            {"key": "english", "label": "English", "example": "Moon · Aries"},
        ],
    })


@app.get("/api/places")
def places():
    q = request.args.get("q", "")
    if not q.strip():
        return jsonify({"places": []})
    try:
        found = search(q)
    except Exception as e:  # noqa: BLE001
        return jsonify({"error": f"Place lookup failed: {e}"}), 502
    return jsonify({"places": [p.to_dict() for p in found]})


@app.post("/api/chart")
def chart():
    body = request.get_json(silent=True) or {}

    missing = [f for f in ("date", "time", "latitude", "longitude")
               if body.get(f) in (None, "")]
    if missing:
        return jsonify({"error": f"Missing required field(s): {', '.join(missing)}"}), 400

    try:
        lat = float(body["latitude"])
        lon = float(body["longitude"])
    except (TypeError, ValueError):
        return jsonify({"error": "latitude and longitude must be numbers"}), 400

    if not -90 <= lat <= 90:
        return jsonify({"error": f"latitude {lat} out of range (-90..90)"}), 400
    if not -180 <= lon <= 180:
        return jsonify({"error": f"longitude {lon} out of range (-180..180)"}), 400

    try:
        local_dt = datetime.strptime(f"{body['date']} {body['time']}", "%Y-%m-%d %H:%M")
    except ValueError:
        return jsonify({"error": "date must be YYYY-MM-DD and time HH:MM (24h)"}), 400

    if not EPHE_YEAR_MIN <= local_dt.year <= EPHE_YEAR_MAX:
        return jsonify({
            "error": f"Year {local_dt.year} is outside the loaded ephemeris range "
                     f"({EPHE_YEAR_MIN}-{EPHE_YEAR_MAX}). Add the adjoining .se1 "
                     "files to widen it."
        }), 400

    tz_name = body.get("timezone") or timezone_at(lat, lon)

    try:
        result = compute_chart(
            local_dt=local_dt,
            latitude=lat,
            longitude=lon,
            tz_name=tz_name,
            name=(body.get("name") or "").strip(),
        )
    except Exception as e:  # noqa: BLE001
        return jsonify({"error": f"Chart calculation failed: {e}"}), 500

    payload = result.to_dict()

    # Dignity (BPHS ch.3 vv.49-55) rides along with each graha, and the twelve
    # signs' doctrinal landmarks ride along once. Keeping the landmarks on the
    # payload — rather than letting the client hardcode exaltation degrees — is
    # what stops BPHS numbers leaking into JavaScript, where they would have no
    # citation and no test.
    for g in payload["grahas"]:
        g["dignity"] = dignity_of(g["key"], g["longitude"])   # None for the nodes
    payload["landmarks"] = [sign_landmarks(s) for s in range(12)]

    # Gaṇḍānta (Vol II ch.92 v.3) is about the birth MOMENT, not about dignity,
    # and its width comes from Candra's own rate — so it is computed here, per
    # chart, rather than baked into a per-sign table. Usually None.
    _moon = next((g for g in result.grahas if g.key == "moon"), None)
    payload["gandanta"] = (
        nakshatra_gandanta(_moon.longitude, _moon.speed) if _moon else None
    )
    # Lagna-gaṇḍānta (v.4, half a ghaṭikā of ASCENDANT motion) is not computed:
    # it needs the ascendant's rate of change, which varies with latitude and
    # rising sign and is not on this payload. See docs/bphs-rules.md.

    # D1 analysis — the Tier 0 engines assembled as a per-graha SIGNAL STACK.
    # Deliberately NOT a single score: BPHS states these judgements separately
    # and never combines them (see analysis.py). A failure here must not cost
    # the user their chart, so it degrades to an error row rather than a 500.
    try:
        analysis_positions = {
            g.key: {"longitude": g.longitude, "rasi": g.rasi, "vargas": g.vargas}
            for g in result.grahas
        }
        payload["analysis"] = analyse(analysis_positions, result.lagna_rasi)
    except Exception as e:  # noqa: BLE001
        payload["analysis"] = {"error": f"Analysis failed: {e}"}

    # Daśā is driven by the Moon's nakṣatra; attach the default (Viṁśottarī) here.
    # Other validated systems are fetched on demand via /api/dasha. Both year-
    # length variants are precomputed so the UI toggles 360/365.25 with no fetch.
    try:
        moon = next(g for g in result.grahas if g.key == "moon")
        payload["dasha"] = _dasha_variants(
            "vimshottari", result.jd_ut, moon.nakshatra.index,
            moon.nakshatra.fraction, moon.longitude, result.timezone, _now_jd(),
        )
        payload["dasha"]["available_systems"] = [_system_meta(k) for k in VALID_DASHAS]
    except Exception as e:  # noqa: BLE001
        payload["dasha"] = {"error": f"Daśā calculation failed: {e}"}

    return jsonify(payload)


@app.post("/api/dasha")
def dasha():
    """A single daśā system's tree, from Moon-nakṣatra data the client already has.

    Avoids recomputing the whole chart when the user switches daśā system.
    """
    body = request.get_json(silent=True) or {}
    system_key = body.get("system", "vimshottari")
    if system_key not in VALID_DASHAS:
        return jsonify({"error": f"Unknown or unvalidated daśā system '{system_key}'"}), 400
    try:
        birth_jd = float(body["jd_ut"])
        nak_index = int(body["moon_nakshatra_index"])
        nak_fraction = float(body["moon_nakshatra_fraction"])
        moon_longitude = float(body["moon_longitude"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "need jd_ut, moon_nakshatra_index, "
                                 "moon_nakshatra_fraction, moon_longitude"}), 400
    tz_name = body.get("timezone") or "UTC"
    try:
        out = _dasha_variants(system_key, birth_jd, nak_index, nak_fraction,
                              moon_longitude, tz_name, _now_jd())
    except Exception as e:  # noqa: BLE001
        return jsonify({"error": f"Daśā calculation failed: {e}"}), 500
    return jsonify(out)


if __name__ == "__main__":
    # Local dev only — production runs under gunicorn (see Dockerfile).
    # use_reloader=False is deliberate. On this machine the venv is based on the
    # anaconda3 install, and Werkzeug's reloader respawns the app under the BASE
    # interpreter rather than the venv's — which loses pyswisseph's configured
    # ephemeris path and silently drops every chart onto the Moshier fallback.
    # The /api/health probe catches it, but the reloader is not worth the trap.
    port = int(os.environ.get("PORT", 5174))
    app.run(host="127.0.0.1", port=port, debug=True, use_reloader=False)
