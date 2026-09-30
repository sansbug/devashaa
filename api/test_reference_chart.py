"""
Reference chart — an external cross-check of the whole engine on one nativity.

Every other test here validates a formula against the text that states it.
This one validates the ASSEMBLED engine against things outside the codebase:

  1. JPL Horizons (NASA's ephemeris) for the raw positions. Pinned, not fetched:
     the test must run offline and must not move when JPL refines a theory by
     a milliarcsecond. The retrieval is documented so it can be repeated.
  2. An independent commercial implementation (AstroSage, report printed
     1 Jan 2026) for everything that SHOULD agree — Viṁśottarī dates,
     sarvāṣṭakavarga, chara-daśā lengths, the solar return, five of the six
     ṣaḍbala components.
  3. The places where that implementation and this one differ, pinned as
     DOCUMENTED CHOICES so a future edit cannot flip them silently:
       - horā bala: Raman (Art. 68-70) counts equal 24ths from sunrise; the
         other engine divides day and night into 12 unequal parts each. At this
         birth that moves 60 virūpa from Jupiter to Saturn.
       - dṛk bala: signed per Art. 120; the other engine nets aspects with a
         different convention and gets the opposite sign for Saturn.
       - ayanāṁśa as PRINTED: this engine prints the true Lahiri value (mean +
         nutation); the other prints the mean. Positions agree either way.
     And one external ERROR, pinned so nobody "fixes" the engine toward it:
       - AstroSage's Saturn is 4′27″ from JPL; every other body it prints is
         within 20″. Our Saturn is within 1″ of JPL.
  4. One difference that is NEITHER engine's fault, recorded so it is never
     "fixed": the Sun's sthāna bala (244.4 here vs 199.4 there). The Sun
     sits 0.08″ before 10°00′ Gemini — two seconds of birth time — and that
     degree is both a drekkāṇa boundary and a navāṁśa boundary. Our Sun is
     in the 1st drekkāṇa and the Sagittarius navāṁśa; theirs (18″ later) is
     in the 2nd and Capricorn. Three sthāna rules (drekkāṇa, ojāyugma,
     saptavargaja) flip on that, 44 virūpa in all. The number is not wrong on
     either side; the birth time is not known to two seconds. An engine that
     wants to be honest about this should FLAG a body that close to a cusp.

The nativity: 25 June 1975, 22:30 IST, Kanpur (26.46523 N, 80.34975 E).

Run:  PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python test_reference_chart.py
"""
import datetime as dt

import swisseph as swe

import ashtakavarga
import charadasha
import shadbala_context
import vedic  # noqa: F401  (configures the ephemeris path and sidereal mode)
import vimshottari
from vedic import compute_chart

BIRTH = dict(local_dt=dt.datetime(1975, 6, 25, 22, 30), latitude=26.46523,
             longitude=80.34975, tz_name="Asia/Kolkata", name="")
BIRTH_UT_JD = swe.julday(1975, 6, 25, 17.0, swe.GREG_CAL)   # 22:30 IST = 17:00 UT

# ── 1. JPL Horizons ────────────────────────────────────────────────────────────
# Apparent geocentric ecliptic longitude of date, 1975-06-25 17:00:00 UT.
# Retrieved 2026-09-29 from https://ssd.jpl.nasa.gov/api/horizons.api with
#   EPHEM_TYPE=OBSERVER  CENTER=500@399  QUANTITIES=31  ANG_FORMAT=DEG
#   COMMAND = 10 / 301 / 499 / 199 / 599 / 299 / 699
# Sidereal = tropical − true Lahiri ayanāṁśa (the value the chart prints).
JPL_TROPICAL = {
    "sun": 93.51883, "moon": 297.11818, "mars": 26.09447, "mercury": 75.38117,
    "jupiter": 20.87458, "venus": 138.70201, "saturn": 109.94192,
}
JPL_TOL_ARCSEC = 30.0

# ── 2. AstroSage cross-values (report of 1 Jan 2026) ──────────────────────────
AS_LAGNA_LON = 300.0 + 7 + 19 / 60 + 25 / 3600          # Aquarius 07°19′25″
AS_SATURN_LON = 60.0 + 26 + 29 / 60 + 50 / 3600         # Gemini 26°29′50″ (their error)
AS_SARVA = [31, 25, 22, 27, 22, 25, 28, 30, 29, 32, 34, 32]
AS_CHARA_YEARS = [12, 2, 11, 6, 2, 4, 9, 6, 3, 7, 8, 12]  # Ari..Pis
AS_BALANCE = "2y 10m 17d"
AS_JUPITER_MAHA = ("2013-05-13", "2029-05-13")
AS_MARS_ANTAR = ("2026-01-13", "2026-12-19")
AS_SOLAR_RETURN_UT = dt.datetime(2026, 6, 25, 18, 47, 30)  # 26/6/2026 00:17:30 IST
AS_VARSHA_LAGNA_SIGN = 11                                  # Pisces
AS_MUNTHA_BHAVA = 3
# ṣaḍbala components AstroSage prints (virūpa); only the ones that should agree
AS_STHANA = {"moon": 128.95, "mars": 300.97, "mercury": 189.16, "jupiter": 229.95,
             "venus": 168.73, "saturn": 189.04}          # sun 199.37: unreconciled, see §4
AS_DIK = {"sun": 7.79, "moon": 15.65, "mars": 14.69, "mercury": 25.15,
          "jupiter": 43.32, "venus": 37.16, "saturn": 46.39}
AS_NAISARGIKA = {"sun": 60.0, "moon": 51.42, "mars": 17.16, "mercury": 25.74,
                 "jupiter": 34.26, "venus": 42.84, "saturn": 8.58}
AS_CHESHTA_AGREEING = {"mars": 30.35, "saturn": 5.57}
AS_SATURN_DRIK = 13.34                                     # ours is negative: documented fork
AS_HORA_GOES_TO = "saturn"                                 # ours: jupiter (equal 24ths)

_CHART = None


def _chart():
    global _CHART
    if _CHART is None:
        _CHART = compute_chart(**BIRTH)
    return _CHART


def _dms(x):
    x %= 30
    d = int(x); m = (x - d) * 60
    return "%02d°%02d′%02d″" % (d, int(m), round((m - int(m)) * 60))


def _close(name, got, want, tol):
    ok = abs(got - want) <= tol
    print(f"  {'OK ' if ok else 'XX '}{name:46s} got {got:.4f}  want {want:.4f}  (±{tol})")
    assert ok, f"{name}: got {got}, want {want} ± {tol}"


def _eq(name, got, want):
    ok = got == want
    print(f"  {'OK ' if ok else 'XX '}{name:46s} got {got!s}  want {want!s}")
    assert ok, f"{name}: got {got!r}, want {want!r}"


# ── tests ──────────────────────────────────────────────────────────────────────

def test_positions_match_jpl_horizons():
    """Every graha within 30″ of JPL, after subtracting the true ayanāṁśa."""
    c = _chart()
    ay = c.to_dict()["ayanamsa_value"]
    lon = {g.key: g.longitude for g in c.grahas}
    for key, trop in JPL_TROPICAL.items():
        want = (trop - ay) % 360.0
        diff = ((lon[key] - want + 180.0) % 360.0) - 180.0
        _close(f"JPL {key} (arcsec)", diff * 3600.0, 0.0, JPL_TOL_ARCSEC)


def test_ayanamsa_is_true_lahiri():
    """The printed ayanāṁśa is Lahiri INCLUDING nutation — the value that
    reconciles with the positions to 0″ — and differs from the mean by exactly
    the nutation in longitude (~15″ at this birth)."""
    c = _chart()
    printed = c.to_dict()["ayanamsa_value"]
    true_ay = swe.get_ayanamsa_ex_ut(c.jd_ut, swe.FLG_SWIEPH)[1]
    mean_ay = swe.get_ayanamsa_ut(c.jd_ut)
    dpsi = swe.calc_ut(c.jd_ut, swe.ECL_NUT, 0)[0][2]
    _close("printed == true ayanāṁśa (arcsec)", (printed - true_ay) * 3600, 0.0, 0.5)
    _close("true − mean == nutation Δψ (arcsec)", (true_ay - mean_ay - dpsi) * 3600, 0.0, 0.5)


def test_lagna_and_nakshatra():
    c = _chart()
    d = c.to_dict()
    _eq("lagna rāśi (10 = Kumbha)", c.lagna_rasi, 10)
    _close("lagna vs AstroSage (arcmin)", (d["lagna_longitude"] - AS_LAGNA_LON) * 60, 0.0, 3.0)
    moon = next(g for g in c.grahas if g.key == "moon")
    _eq("Moon nakṣatra (21 = Uttarāṣāḍhā)", moon.nakshatra.index, 21)
    _eq("Moon pada", moon.nakshatra.pada, 3)


def test_astrosage_saturn_is_the_external_outlier():
    """Pinned so nobody 'corrects' Saturn toward the other engine's value."""
    c = _chart()
    ay = c.to_dict()["ayanamsa_value"]
    ours = next(g.longitude for g in c.grahas if g.key == "saturn")
    jpl = (JPL_TROPICAL["saturn"] - ay) % 360.0
    _close("our Saturn vs JPL (arcsec)", (ours - jpl) * 3600, 0.0, JPL_TOL_ARCSEC)
    gap = abs(AS_SATURN_LON - jpl) * 60
    print(f"      AstroSage Saturn {_dms(AS_SATURN_LON)} is {gap:.1f}′ from JPL — their ephemeris, not ours")
    assert gap > 3.0, "AstroSage's Saturn is no longer an outlier — re-examine the fixture"


def test_vimshottari_matches_astrosage_within_a_day():
    """Their dates fall on the 13th where ours fall on the 12th: the one-day
    offset is exactly what the 365.25-day year gives, which is why 365.25 is
    the default and 360 sāvana is the labelled alternative."""
    c = _chart()
    moon = next(g for g in c.grahas if g.key == "moon")
    tree = vimshottari.build_vimshottari(c.jd_ut, moon.nakshatra.index, moon.nakshatra.fraction,
                                         depth=2, tz_name=c.timezone, year_days=365.25)
    _eq("balance at birth", tree["balance_at_birth"], AS_BALANCE)
    jup = next(m for m in tree["mahadashas"] if m["lord"] == "jupiter")
    mars = next(a for a in jup["sub"] if a["lord"] == "mars")

    def days_apart(a, b):
        return abs((dt.date.fromisoformat(a[:10]) - dt.date.fromisoformat(b)).days)
    _close("Jupiter mahā start vs AstroSage (days)", days_apart(jup["start"], AS_JUPITER_MAHA[0]), 0, 1)
    _close("Jupiter mahā end vs AstroSage (days)", days_apart(jup["end"], AS_JUPITER_MAHA[1]), 0, 1)
    _close("Mars antar start vs AstroSage (days)", days_apart(mars["start"], AS_MARS_ANTAR[0]), 0, 2)
    _close("Mars antar end vs AstroSage (days)", days_apart(mars["end"], AS_MARS_ANTAR[1]), 0, 1)


def test_sarvashtakavarga_matches_astrosage():
    sav = ashtakavarga.from_chart(_chart())["sarva"]
    _eq("sarvāṣṭakavarga, 12 signs", list(sav), AS_SARVA)


def test_chara_dasha_lengths_match_astrosage():
    """Same twelve lengths. The other engine also picks a direction; this one
    refuses to, because the rule is not in the available source."""
    c = _chart()
    pos = {g.key: g.rasi for g in c.grahas}
    deg = {g.key: g.longitude % 30 for g in c.grahas}
    out = charadasha.chara_dasha(pos, deg, lagna=c.lagna_rasi)
    years = [None] * 12
    for row in out["lengths"]:
        years[row["sign"]] = row["years"]
    _eq("chara daśā years, Ari..Pis", years, AS_CHARA_YEARS)
    _eq("sequence direction is NOT guessed", out.get("sequence"), None)


def test_solar_return_2026_and_varsha_lagna():
    """Varṣa-praveśa: the Sun back at its natal sidereal longitude."""
    c = _chart()
    natal_sun = next(g.longitude for g in c.grahas if g.key == "sun")
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    jd = swe.julday(2026, 6, 25, 12.0, swe.GREG_CAL)
    for _ in range(30):
        diff = (swe.calc_ut(jd, swe.SUN, flags)[0][0] - natal_sun + 180.0) % 360.0 - 180.0
        jd -= diff / 0.9856
        if abs(diff) < 1e-7:
            break
    y, m, d, h = swe.revjul(jd, swe.GREG_CAL)
    when = dt.datetime(y, m, d) + dt.timedelta(hours=h)
    _close("solar return vs AstroSage (seconds)", abs((when - AS_SOLAR_RETURN_UT).total_seconds()), 0, 60)
    _cusps, ascmc = swe.houses_ex(jd, BIRTH["latitude"], BIRTH["longitude"], b"W", swe.FLG_SIDEREAL)
    varsha_lagna = int(ascmc[0] // 30)
    _eq("varṣa lagna (11 = Mīna)", varsha_lagna, AS_VARSHA_LAGNA_SIGN)
    age = 51
    muntha = (c.lagna_rasi + age) % 12
    _eq("muntha bhāva from varṣa lagna", (muntha - varsha_lagna) % 12 + 1, AS_MUNTHA_BHAVA)


def test_shadbala_components_that_should_agree():
    sb = shadbala_context.shadbala_for_chart(_chart())
    g = sb["grahas"]
    for k, want in AS_STHANA.items():
        _close(f"sthāna {k}", g[k]["sthana"], want, 0.1)
    for k, want in AS_DIK.items():
        _close(f"dik {k}", g[k]["dik"], want, 0.1)
    for k, want in AS_NAISARGIKA.items():
        _close(f"naisargika {k}", g[k]["naisargika"], want, 0.05)
    for k, want in AS_CHESHTA_AGREEING.items():
        _close(f"cheṣṭā {k}", g[k]["cheshta"], want, 0.2)
    # §4 — the Sun's sthāna differs because the Sun is on a varga cusp (see
    # test_sun_sits_on_a_varga_cusp). Pin OUR value so drift is visible.
    _close("sthāna sun (ours; AstroSage 199.37 — cusp, see §4)", g["sun"]["sthana"], 244.38, 0.1)


def test_sun_sits_on_a_varga_cusp():
    """The Sun is within an arcsecond of 10°00′ Gemini, a drekkāṇa AND a
    navāṁśa boundary; 2 s of birth time moves it across. This is why the
    Sun's sthāna bala differs from AstroSage's by 44 virūpa and why neither
    value should be 'corrected' toward the other."""
    c = _chart()
    sun = next(g for g in c.grahas if g.key == "sun")
    within = sun.longitude % 30.0
    arcsec = (within - 10.0) * 3600.0
    seconds = abs(within - 10.0) / sun.speed * 86400.0
    print(f"      Sun at Gemini {within:.6f}°: {arcsec:+.3f}″ from the 10° cusp = {seconds:.1f} s of birth time")
    assert abs(arcsec) < 1.0, "the Sun has moved off the cusp — re-derive §4 of this fixture"
    v = sun.vargas
    _eq("Sun drekkāṇa index (0 = first)", int(within // 10.0), 0)
    _eq("Sun navāṁśa index (2 = Sagittarius for Gemini)", int(within // (30.0 / 9.0)), 2)
    _eq("Sun D9 sign (8 = Dhanu)", v["D9"], 8)


def test_shadbala_documented_forks():
    """The two places this engine and AstroSage legitimately differ. A change
    here must be a decision, with the rule that justifies it."""
    sb = shadbala_context.shadbala_for_chart(_chart())
    hora = sb["kala_components"]["hora"]
    _close("horā bala → Jupiter (equal 24ths from sunrise, Raman Art. 68-70)", hora["jupiter"], 60.0, 0.01)
    _close(f"horā bala → {AS_HORA_GOES_TO} is 0 here (seasonal horā would give 60)", hora[AS_HORA_GOES_TO], 0.0, 0.01)
    drik = sb["grahas"]["saturn"]["drik"]
    print(f"      Saturn dṛk here {drik:+.2f}; AstroSage {AS_SATURN_DRIK:+.2f} — signed per Art. 120 on this side")
    assert drik < 0, "Saturn dṛk changed sign — the aspect netting convention moved"


def main():
    import sys
    names = [n for n in globals() if n.startswith("test_")]
    failed = 0
    for n in names:
        print(f"\n{n}")
        try:
            globals()[n]()
        except AssertionError as e:
            failed += 1
            print(f"  FAILED: {e}")
    print("\n" + ("ALL PASS ✓" if not failed else f"{failed} FAILED ✗"))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
