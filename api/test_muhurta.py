"""
Muhūrta — pin the day-divisions to what the printed almanacs carry.

The choghaḍiyā rows are the standard weekday tables; the rest are identities
of the construction (a clear window never overlaps an avoided span; pradoṣa
opens at sunset; abhijit is void on Wednesday; the five-fold day tiles
sunrise to sunset).

Run:  PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python test_muhurta.py
"""
import datetime as dt

import muhurta
import vedic  # noqa: F401

DELHI = (28.6139, 77.209, "Asia/Kolkata")
# The standard tables, as printed: day and night series for each weekday.
DAY = {
    "sun": ["Udvega", "Cara", "Lābha", "Amṛta", "Kāla", "Śubha", "Roga", "Udvega"],
    "mon": ["Amṛta", "Kāla", "Śubha", "Roga", "Udvega", "Cara", "Lābha", "Amṛta"],
    "tue": ["Roga", "Udvega", "Cara", "Lābha", "Amṛta", "Kāla", "Śubha", "Roga"],
    "wed": ["Lābha", "Amṛta", "Kāla", "Śubha", "Roga", "Udvega", "Cara", "Lābha"],
    "thu": ["Śubha", "Roga", "Udvega", "Cara", "Lābha", "Amṛta", "Kāla", "Śubha"],
    "fri": ["Cara", "Lābha", "Amṛta", "Kāla", "Śubha", "Roga", "Udvega", "Cara"],
    "sat": ["Kāla", "Śubha", "Roga", "Udvega", "Cara", "Lābha", "Amṛta", "Kāla"],
}
NIGHT = {
    "sun": ["Śubha", "Amṛta", "Cara", "Roga", "Kāla", "Lābha", "Udvega", "Śubha"],
    "mon": ["Cara", "Roga", "Kāla", "Lābha", "Udvega", "Śubha", "Amṛta", "Cara"],
    "tue": ["Kāla", "Lābha", "Udvega", "Śubha", "Amṛta", "Cara", "Roga", "Kāla"],
    "wed": ["Udvega", "Śubha", "Amṛta", "Cara", "Roga", "Kāla", "Lābha", "Udvega"],
    "thu": ["Amṛta", "Cara", "Roga", "Kāla", "Lābha", "Udvega", "Śubha", "Amṛta"],
    "fri": ["Roga", "Kāla", "Lābha", "Udvega", "Śubha", "Amṛta", "Cara", "Roga"],
    "sat": ["Lābha", "Udvega", "Śubha", "Amṛta", "Cara", "Roga", "Kāla", "Lābha"],
}
# 2026-10-25 is a Sunday.
WEEK = [("sun", dt.date(2026, 10, 25)), ("mon", dt.date(2026, 10, 26)), ("tue", dt.date(2026, 10, 27)),
        ("wed", dt.date(2026, 10, 28)), ("thu", dt.date(2026, 10, 29)), ("fri", dt.date(2026, 10, 30)), ("sat", dt.date(2026, 10, 31))]


def _ok(name, cond, detail=""):
    print(f"  {'OK ' if cond else 'XX '}{name:58s} {detail}")
    assert cond, f"{name} {detail}"


def _mins(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def test_choghadiya_weekday_tables():
    for key, d in WEEK:
        m = muhurta.day_muhurta(d, *DELHI)
        _ok(f"{key} is weekday {d.strftime('%A')}", m["panchang"]["vara"]["index"] == ["sun", "mon", "tue", "wed", "thu", "fri", "sat"].index(key))
        _ok(f"{key} day series", [c["name"] for c in m["choghadiya"]["day"]] == DAY[key], str([c["name"] for c in m["choghadiya"]["day"]]))
        _ok(f"{key} night series", [c["name"] for c in m["choghadiya"]["night"]] == NIGHT[key], str([c["name"] for c in m["choghadiya"]["night"]]))


def test_clear_windows_avoid_the_three_kalas():
    for _key, d in WEEK:
        m = muhurta.day_muhurta(d, *DELHI)
        for c in m["clear"]:
            for a in m["avoid"]:
                overlap = _mins(c["start"]) < _mins(a["end"]) and _mins(c["end"]) > _mins(a["start"])
                _ok(f"{d} clear {c['start']}-{c['end']} vs {a['key']}", not overlap)
            _ok(f"{d} clear window is a good or fair choghaḍiyā", c["quality"] >= 0 and c["minutes"] >= 20)


def test_structure_identities():
    m = muhurta.day_muhurta(dt.date(2026, 10, 26), *DELHI, ritual="lakshmi")
    k = m["kala"]
    _ok("five-fold day tiles sunrise → sunset", k["pratah"]["start"] == m["sunrise"] and k["sayahna"]["end"] == m["sunset"]
        and k["pratah"]["end"] == k["sangava"]["start"] and k["madhyahna"]["end"] == k["aparahna"]["start"])
    _ok("pradoṣa opens at sunset", k["pradosha"]["start"] == m["sunset"])
    _ok("pradoṣa is three night-muhūrtas (≈ 2h20–2h50 in late October at Delhi)", 135 <= k["pradosha"]["minutes"] <= 175, str(k["pradosha"]["minutes"]))
    _ok("abhijit straddles local midday", _mins(k["abhijit"]["start"]) < (_mins(m["sunrise"]) + _mins(m["sunset"])) / 2 < _mins(k["abhijit"]["end"]))
    _ok("Lakṣmī pūjā → pradoṣa, with its reason", m["preferred"]["kala"] == "pradosha" and "pradoṣa" in m["preferred"]["why"])
    wed = muhurta.day_muhurta(dt.date(2026, 10, 28), *DELHI)
    _ok("abhijit is void on Wednesday", "abhijit" not in wed["kala"])
    sh = muhurta.day_muhurta(dt.date(2026, 10, 10), *DELHI, ritual="shraddha")     # Amāvāsyā
    _ok("śrāddha → aparāhṇa", sh["preferred"]["kala"] == "aparahna")
    _ok("Amāvāsyā is cautioned for beginnings, not applied to śrāddha", any(c["key"] == "amavasya" for c in sh["cautions"]) and sh["cautions_apply"] is False)
    gp = muhurta.day_muhurta(dt.date(2026, 10, 10), *DELHI, ritual="griha-pravesh")
    _ok("…and applied to a gṛha praveśa", gp["cautions_apply"] is True)


def test_rahu_kala_weekday_slots():
    """Rāhu kāla's eighth of the day by weekday: Sun 8, Mon 2, Tue 7, Wed 5, Thu 6, Fri 4, Sat 3."""
    want = {"sun": 8, "mon": 2, "tue": 7, "wed": 5, "thu": 6, "fri": 4, "sat": 3}
    for key, d in WEEK:
        m = muhurta.day_muhurta(d, *DELHI)
        rahu = next(a for a in m["avoid"] if a["key"] == "rahu_kala")
        day = _mins(m["sunset"]) - _mins(m["sunrise"])
        slot = round((_mins(rahu["start"]) - _mins(m["sunrise"])) / (day / 8.0)) + 1
        _ok(f"{key} rāhu kāla in eighth {want[key]}", slot == want[key], f"got {slot} ({rahu['start']}–{rahu['end']})")


def main():
    failed = 0
    for n in [k for k in globals() if k.startswith("test_")]:
        print(f"\n{n}")
        try:
            globals()[n]()
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  FAILED: {e}")
    print("\n" + ("ALL PASS ✓" if not failed else f"{failed} FAILED ✗"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
