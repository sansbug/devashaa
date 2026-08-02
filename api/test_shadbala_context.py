"""
Validate the production context builder against Raman's Standard Horoscope.

These inputs are physical (birth time + place + date), so they are computed from
swisseph and the civil calendar and must reproduce Raman's fixture regardless of
which ayanāṁśa the chart uses. Longitudes themselves are validated separately in
test_shadbala.py; here we confirm the *context* — apparent time, day/night,
thribhāga third, weekday, ahargana, horā number and declinations.

Run:  PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python test_shadbala_context.py
"""
from datetime import date, datetime

import swisseph as swe

import shadbala
import shadbala_context as ctxmod
import vedic

vedic._configure_thread()

# Standard Horoscope: 16 Oct 1918, 08:55:56 UT (= 2h06m16s pm LMT at 77°35′E),
# 13°N. Raman's kranti values (Ex.32) for the declination cross-check.
JD_UT = swe.julday(1918, 10, 16, 8 + 55 / 60.0 + 56 / 3600.0, swe.GREG_CAL)
LAT, LON_E = 13.0, 77.5833
LOCAL_DT = datetime(1918, 10, 16, 14, 6, 16)
AYAN = swe.get_ayanamsa_ex_ut(JD_UT, swe.FLG_SWIEPH)[1]
# Raman's Nirayana longitudes (only feed Pakṣa/Dṛk/Cheṣṭā — not asserted here).
POS = {"sun": 180.8986, "moon": 311.2886, "mars": 229.5094, "mercury": 181.5261,
       "jupiter": 84.0136, "venus": 171.1656, "saturn": 124.3781}
# Raman's kranti (Ex.32), signed physically (South −, North +). Mercury is South
# here; Raman uses its magnitude additively, so ayana_bala() takes abs().
RAMAN_KRANTI = {"sun": -8.75, "moon": -10.75, "mars": -22.45, "mercury": -9.00,
                "jupiter": 23.50, "venus": -4.96, "saturn": 13.00}


def main():
    ok = True

    def check(label, got, want, tol):
        nonlocal ok
        good = abs(got - want) <= tol
        ok &= good
        print(f"  {'OK ' if good else 'XX '}{label:32s} got {got:10.3f}  want {want:10.3f}"
              + ("" if good else f"   Δ={got-want:+.3f}"))

    def check_eq(label, got, want):
        nonlocal ok
        good = got == want
        ok &= good
        print(f"  {'OK ' if good else 'XX '}{label:32s} got {got!s:>10}  want {want!s:>10}")

    print("EPOCH sanity")
    check_eq("2-May-1827 is Wednesday", date(1827, 5, 2).weekday(), 2)  # py Wed=2

    ctx = ctxmod.build_context(JD_UT, LAT, LON_E, LOCAL_DT, POS, AYAN)

    print("\nBIRTH CONTEXT — vs Raman Standard Horoscope")
    check("apparent time from midnight (h)", ctx["hours_from_apparent_midnight"], 14.339, 0.03)
    check_eq("is_day", ctx["is_day"], True)
    check_eq("thribhaga third (0-based)", ctx["thribhaga_third"], 2)
    check_eq("weekday (0=Sun) → Wednesday", ctx["weekday"], 3)
    check_eq("ahargana", ctx["ahargana"], 33405)
    check_eq("hora number", ctx["hora_number"], 9)

    print("\nDECLINATIONS — swisseph true vs Raman's 24° kranti table (deg)")
    for g, want in RAMAN_KRANTI.items():
        check(f"{g} declination", ctx["declinations"][g], want, 0.5)

    # End-to-end: the context inputs + Raman's own longitudes must rebuild the
    # validated Ṣaḍbala verdict (all strong except Mars). Cheṣṭā here uses the
    # production mean elements, so the total drifts slightly from Raman's, but the
    # verdict is unchanged.
    print("\nEND-TO-END verdict with production context (Raman longitudes)")
    full = ctxmod.assemble_from_context(ctx, lagna_rasi=9)["grahas"]
    expect_strong = {"sun": True, "moon": True, "mars": False, "mercury": True,
                     "jupiter": True, "venus": True, "saturn": True}
    for g, want in expect_strong.items():
        got = full[g]["strong"]
        good = got == want
        ok &= good
        print(f"  {'OK ' if good else 'XX '}{g:10s} strong={got!s:5s} "
              f"ratio={full[g]['ratio']:.2f}  want={want}")

    # ── regression (audit): pre-sunrise birth rolls the Hindu day back using the
    # civil zone offset, not LMT. New York 2024-06-05 05:00 EDT is before the
    # 05:26 sunrise → Vāra must be Tuesday (Mars), not Wednesday (Mercury). ──────
    print("\nREGRESSION — pre-sunrise Vāra rollback (New York EDT)")
    ny = vedic.compute_chart(datetime(2024, 6, 5, 5, 0, 0), 40.7128, -73.9970, "America/New_York")
    ny_pos = {g.key: g.longitude for g in ny.grahas if g.key in ctxmod._IPL}
    ny_ctx = ctxmod.build_context(ny.jd_ut, ny.latitude, ny.longitude,
                                  datetime.strptime(ny.local_time, "%Y-%m-%d %H:%M:%S"),
                                  ny_pos, ny.ayanamsa_value)
    check_eq("NY pre-sunrise weekday → Tuesday(2)", ny_ctx["weekday"], 2)
    check_eq("NY Vāra bala awarded to Mars", max(shadbala.vara_bala(ny_ctx["weekday"]),
             key=shadbala.vara_bala(ny_ctx["weekday"]).get), "mars")

    # ── regression (audit): a circumpolar birth must fail cleanly, never hang. ──
    print("\nREGRESSION — circumpolar birth raises, does not loop")
    try:
        tromso = vedic.compute_chart(datetime(2024, 6, 21, 0, 30, 0), 69.65, 18.96, "Europe/Oslo")
        ctxmod.shadbala_for_chart(tromso)
        print("  XX no exception raised for polar midnight-sun birth"); ok = False
    except ctxmod.ShadbalaUnavailable:
        print("  OK raised ShadbalaUnavailable (Kāla bala undefined at polar day)")
    except Exception as e:  # noqa: BLE001
        print(f"  XX wrong exception type: {type(e).__name__}: {e}"); ok = False

    print("\n" + ("ALL PASS ✓" if ok else "FAILURES ✗"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
