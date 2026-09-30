"""
Tājika — pinned to K.S. Charak's worked Example Chart (the 41st year of Rajiv
Gandhi, praveśa 20 Aug 1984, day) which the book carries to the sub-unit for
every strength, and to Nīlakaṇṭhī's worked dṛṣṭi.

Every EXPECT_* value is a printed figure, cited to its table.

Run:  PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python test_tajika.py
"""
import tajika
import varshaphal


def _dms(s, d, m):          # sign (0-based), deg, min → longitude
    return s * 30 + d + m / 60.0


# Charak Chart X-1 / Table VI-5: sidereal longitudes; Mercury and Jupiter retrograde
GRAHAS = [
    {"key": "sun", "longitude": _dms(4, 3, 50), "retrograde": False},
    {"key": "moon", "longitude": _dms(1, 9, 40), "retrograde": False},
    {"key": "mars", "longitude": _dms(7, 7, 42), "retrograde": False},
    {"key": "mercury", "longitude": _dms(4, 18, 19), "retrograde": True},
    {"key": "jupiter", "longitude": _dms(8, 9, 38), "retrograde": True},
    {"key": "venus", "longitude": _dms(4, 21, 45), "retrograde": False},
    {"key": "saturn", "longitude": _dms(6, 17, 13), "retrograde": False},
    {"key": "rahu", "longitude": _dms(3, 8, 55), "retrograde": True},
]
ASC = _dms(7, 9, 26)                 # Scorpio 9°26′
CTX = tajika.Ctx(GRAHAS, ASC, is_day=True)
MUNTHA_SIGN = 8                      # Sagittarius (Leo janma lagna + 40)
JANMA_LAGNA = 4                      # Leo

# Table VI-2 — mutual relationships in the example chart
EXPECT_FRIENDS = {"sun": {"jupiter", "saturn"}, "moon": set(), "mars": set(), "mercury": {"jupiter", "saturn"},
                  "jupiter": {"sun", "mercury", "venus", "saturn"}, "venus": {"jupiter", "saturn"},
                  "saturn": {"sun", "mercury", "jupiter", "venus"}}
# Table VI-10 — the five sources (units) and the Viśva-bala
EXPECT_PV = {
    #          kshetra uchcha  hadda  drek   nav    total   VB
    "sun":     (30.0, 7.35, 11.25, 7.5, 1.25, 57.35, 14.337),
    "moon":    (7.5, 19.25, 3.75, 2.5, 2.5, 35.50, 8.875),
    "mars":    (30.0, 11.07, 3.75, 10.0, 1.25, 56.07, 14.016),
    "mercury": (7.5, 17.03, 15.0, 7.5, 5.0, 52.03, 13.008),
    "jupiter": (30.0, 2.82, 15.0, 7.5, 3.75, 59.07, 14.766),
    "venus":   (7.5, 3.92, 3.75, 2.5, 5.0, 22.67, 5.666),
    "saturn":  (22.5, 19.68, 11.25, 10.0, 3.75, 67.18, 16.796),
}
EXPECT_HADDA_LORD = {"sun": "jupiter", "moon": "mercury", "mars": "venus", "mercury": "mercury",
                     "jupiter": "jupiter", "venus": "mercury", "saturn": "jupiter"}          # Table VI-5
EXPECT_DREK_LORD = {"sun": "saturn", "moon": "mercury", "mars": "mars", "mercury": "jupiter",
                    "jupiter": "mercury", "venus": "mars", "saturn": "saturn"}              # Table VI-7
EXPECT_NAV_LORD = {"sun": "venus", "moon": "jupiter", "mars": "mercury", "mercury": "mercury",
                   "jupiter": "mercury", "venus": "venus", "saturn": "jupiter"}             # Table VI-9
EXPECT_HARSHA = {"sun": 15, "moon": 10, "mars": 10, "mercury": 0, "jupiter": 10, "venus": 0, "saturn": 10}  # Table VI-1


def _ok(name, cond, detail=""):
    print(f"  {'OK ' if cond else 'XX '}{name:56s} {detail}")
    assert cond, f"{name} {detail}"


def _close(name, got, want, tol):
    _ok(name, abs(got - want) <= tol, f"got {got:.4f} want {want:.4f} ±{tol}")


def test_relations_table_vi2():
    for p, want in EXPECT_FRIENDS.items():
        got = {q for q in tajika.SEVEN if q != p and tajika.tajika_relation(p, q, CTX.sign) == "friend"}
        _ok(f"friends of {p}", got == want, f"got {sorted(got)}")


def test_varga_lords_tables_vi5_vi7_vi9():
    for p in tajika.SEVEN:
        s, d = CTX.sign[p], CTX.deg[p]
        _ok(f"hadda lord {p}", tajika.hadda_lord(s, d) == EXPECT_HADDA_LORD[p], tajika.hadda_lord(s, d))
        _ok(f"drekkāṇa lord {p}", tajika.drekkana_lord(s, d) == EXPECT_DREK_LORD[p], tajika.drekkana_lord(s, d))
        _ok(f"navāṁśa lord {p}", tajika.navamsa_lord(s, d) == EXPECT_NAV_LORD[p], tajika.navamsa_lord(s, d))


def test_hadda_table_sums_to_thirty():
    for s, row in enumerate(tajika.HADDA):
        _ok(f"hadda sign {s} ends at 30", row[-1][0] == 30 and all(a[0] < b[0] for a, b in zip(row, row[1:])))


def test_pancha_vargiya_table_vi10():
    pv = tajika.pancha_vargiya(CTX)
    for p, (ks, uc, ha, dr, na, tot, vb) in EXPECT_PV.items():
        _close(f"{p} kṣetra", pv[p]["kshetra"]["units"], ks, 0.01)
        _close(f"{p} uccha", pv[p]["uchcha"]["units"], uc, 0.02)
        _close(f"{p} hadda", pv[p]["hadda"]["units"], ha, 0.01)
        _close(f"{p} drekkāṇa", pv[p]["drekkana"]["units"], dr, 0.01)
        _close(f"{p} navāṁśa", pv[p]["navamsa"]["units"], na, 0.01)
        _close(f"{p} total", pv[p]["total"], tot, 0.03)
        _close(f"{p} viśva-bala", pv[p]["vishwa_bala"], vb, 0.01)
    _ok("Saturn parākramī (>15)", pv["saturn"]["category"] == "parakrami")
    _ok("Venus madhya (5-10)", pv["venus"]["category"] == "madhya")


def test_harsha_bala_table_vi1():
    h = tajika.harsha_bala(CTX)
    for p, want in EXPECT_HARSHA.items():
        _close(f"harṣa {p}", h[p]["total"], want, 0.01)


def test_office_bearers_and_year_lord_ch_vii():
    pv = tajika.pancha_vargiya(CTX)
    b = tajika.office_bearers(CTX, MUNTHA_SIGN, JANMA_LAGNA)
    _ok("muntha lord Jupiter", b["muntha_lord"] == "jupiter")
    _ok("janma-lagna lord Sun", b["janma_lagna_lord"] == "sun")
    _ok("varṣa-lagna lord Mars", b["varsha_lagna_lord"] == "mars")
    _ok("tri-rāśi lord Mars (Scorpio, day)", b["trirasi_lord"] == "mars")
    _ok("dina-rātri lord Sun (day → Sun's sign Leo)", b["dinaratri_lord"] == "sun")
    v = tajika.varshesha(CTX, pv, b)
    _ok("Jupiter excluded — strongest but in the 2nd (no aspect)", any("jupiter is strongest" in s for s in v["steps"]))
    _ok("year-lord = Sun (14.337 > Mars 14.016, both aspect)", v["lord"] == "sun", v["lord"])


def test_drishti_worked_example_tn_p58():
    # Sun 9s25°28′ → Moon 10s0°49′: same sign, 5°21′ ahead → 60 falling to 0: ≈49.3 (book prints 49.18)
    v, h = tajika.drishti_value(_dms(9, 25, 28), _dms(10, 0, 49))
    _close("Sun→Moon aspect (TN p.58)", v, 49.3, 0.5)
    _ok("house counted = 1 (same sign)", h == 1)
    _ok("table row 0 40 15 45 0 60 0 45 15 10 0 60", [tajika.DRISHTI[h] for h in range(2, 13)] + [tajika.DRISHTI[1]]
        == [0, 40, 15, 45, 0, 60, 0, 45, 15, 10, 0, 60])


def test_itthasala_sun_mars_charak_p118():
    it = tajika.itthasala(CTX, "sun", "mars")
    _ok("Sun (3°50′) behind Mars (7°42′), mutual 4/10 aspect, gap 3.87 ≤ 11.5", it is not None and it["type"] == "vartamana", str(it))
    _close("mean deeptāṁśa Sun/Mars = 11.5", it["orb"], 11.5, 0.01)
    _ok("no itthaśāla Sun–Moon (Moon fast, ahead)", tajika.itthasala(CTX, "sun", "moon") is None)


def test_sahams_charak_p157():
    pv = tajika.pancha_vargiya(CTX)
    h = tajika.harsha_bala(CTX)
    sah = {s["key"]: s for s in tajika.sahams(CTX, pv, h, "sun", 0.0, None)}
    _close("Punya = Moon − Sun + Asc = 4s15°16′ (no +30)", sah["punya"]["longitude"], _dms(4, 15, 16), 0.02)
    _ok("Punya formula unchanged", not sah["punya"]["formula"].endswith("+ 30"))
    _close("Raja = Saturn − Sun + Asc + 30 = 10s22°49′", sah["rajya"]["longitude"], _dms(10, 22, 49), 0.02)
    _ok("Raja carried the +30", sah["rajya"]["formula"].endswith("+ 30"))
    _ok("fifty sahams", len(sah) == 50)


def test_mudda_charak_example_ch_v():
    # completed years 40, janma nakṣatra 11 (Pūrva Phalgunī), Moon 4s17°8′ → 3°48′ of 13°20′ traversed
    frac = (3 + 48 / 60.0) / (13 + 20 / 60.0)
    import swisseph as swe
    start = swe.julday(1984, 8, 20, 0.0, swe.GREG_CAL)
    end = start + 360.0               # Charak works the year as 360 days (Table V-1)
    m = varshaphal.mudda_dasha(11, 40, start, end, "UTC", None, frac, prorate=True)
    _ok("first lord Rāhu ((40+11−2) mod 9 = 4)", m["start_lord"] == "rahu", m["start_lord"])
    _close("Rāhu balance 38.61 d", m["periods"][0]["days"], 38.61, 0.05)
    # Table V-2: Rāhu upto 29-9-84, Jupiter upto 17-11-84, Saturn upto 14-1-85
    _ok("Rāhu ends 1984-09-28/29 (Table V-2: 29-9-84)", m["periods"][0]["end"][:10] in ("1984-09-27", "1984-09-28", "1984-09-29"), m["periods"][0]["end"])
    _ok("Jupiter ends 1984-11-15/17 (Table V-2: 17-11-84)", m["periods"][1]["end"][:7] == "1984-11" and 14 <= int(m["periods"][1]["end"][8:10]) <= 17, m["periods"][1]["end"])
    _ok("then Jupiter 48, Saturn 57, Mercury 51, Ketu 21, Venus 60, Sun 18, Moon 30, Mars 21",
        [round(p["days"]) for p in m["periods"][1:9]] == [48, 57, 51, 21, 60, 18, 30, 21],
        str([round(p["days"]) for p in m["periods"][1:9]]))
    _close("Rāhu remainder 15.39 d closes the year", m["periods"][-1]["days"], 15.39, 0.05)
    _close("periods sum to the year", sum(p["days"] for p in m["periods"]), 360.0, 0.05)


def main():
    names = [n for n in globals() if n.startswith("test_")]
    failed = 0
    for n in names:
        print(f"\n{n}")
        try:
            globals()[n]()
        except Exception as e:  # noqa: BLE001 — one crashing test must not hide the rest
            failed += 1
            print(f"  FAILED: {type(e).__name__}: {e}")
    print("\n" + ("ALL PASS ✓" if not failed else f"{failed} FAILED ✗"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
