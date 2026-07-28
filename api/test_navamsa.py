"""Navāṁśa (D9) analysis — tier `modern` (C. S. Patel).

Run: python api/test_navamsa.py

Validated against the BOOK's own worked charts: Patel's standard horoscope
(navāṁśa signs, and that it has no vargottama), his Indira-Gandhi 64th-navāṁśa
examples, and his Ch.VI bhāva-sūchaka examples. Structural facts only — the
readings are attributed to Patel, never fused into the computed value.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import navamsa as nv

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


# Signs 0=Aries … 11=Pisces
ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO = 0, 1, 2, 3, 4, 5
LIBRA, SCORPIO, SAG, CAP, AQU, PISCES = 6, 7, 8, 9, 10, 11


def dms(sign, d, m=0):
    return sign * 30 + d + m / 60.0


print("The navāṁśa sign matches BPHS ch.6 v.12 on Patel's standard horoscope:")
# Author's chart (Patel Ch.I) — absolute sidereal longitudes and the navāṁśa
# signs the book states for each.
STD = {
    "sun":     (256 + 10 / 60, LEO),        # Dhanus 16°10' → Siṁha navāṁśa
    "moon":    (192 + 13 / 60, CAP),        # Tulā 12°13' → Makara
    "mars":    (127 + 9 / 60, GEMINI),      # Siṁha 7°09' → Mithuna
    "mercury": (265 + 13 / 60, SCORPIO),    # Dhanus 25°13' → Vṛścika
    "jupiter": (329 + 29 / 60, GEMINI),     # Kumbha 29°29' → Mithuna
    "venus":   (283 + 14 / 60, ARIES),      # Makara 13°14' → Meṣa
    "saturn":  (80 + 42 / 60, ARIES),       # Mithuna 20°42' → Meṣa
    "rahu":    (287 + 6 / 60, GEMINI),      # Makara 17°06' → Mithuna
    "ketu":    (107 + 6 / 60, SAG),         # Kaṭaka 17°06' → Dhanus
}
STD_LAGNA = (98 + 53 / 60, VIRGO)           # Karka 8°53' → Kanyā navāṁśa
for g, (lon, expect) in STD.items():
    got = nv.navamsa_sign(lon)
    check(f"{g:<8} navāṁśa sign", got == expect, f"got {got}, want {expect}")
check("lagna navāṁśa sign (Kanyā)", nv.navamsa_sign(STD_LAGNA[0]) == STD_LAGNA[1])

print("\nPatel's standard horoscope has NO vargottama planet (a real negative):")
pos = {g: {"longitude": lon, "rasi": int(lon // 30)} for g, (lon, _) in STD.items()}
res = nv.navamsa_analysis(pos, STD_LAGNA[0], int(STD_LAGNA[0] // 30))
check("vargottama list is empty for the author's chart",
      res["vargottama"]["items"] == [], str(res["vargottama"]["items"]))

print("\nThe 64th navāṁśa matches Patel's Indira-Gandhi worked chart exactly:")
# asc Karka 27°03', Moon Vṛṣabha 23°58', Mercury Vṛścika 13°15', Ketu Mithuna 10°33'
IG = {
    "asc":     (dms(CANCER, 27, 3),  GEMINI, AQU),    # → Mithuna navāṁśa in Kumbha (8th)
    "moon":    (dms(TAURUS, 23, 58), SCORPIO, SAG),   # → Vṛścika navāṁśa in Dhanus (8th)
    "mercury": (dms(SCORPIO, 13, 15), CAP, GEMINI),   # → Makara navāṁśa in Mithuna (8th)
    "ketu":    (dms(GEMINI, 10, 33), ARIES, CAP),     # → Meṣa navāṁśa in Makara (8th)
}
for who, (lon, exp_nav, exp_8th) in IG.items():
    k = nv.khara_64th(lon)
    check(f"64th navāṁśa from {who}: navāṁśa sign",
          k["navamsa_sign"] == exp_nav, f"got {k['navamsa_sign']}, want {exp_nav}")
    check(f"64th navāṁśa from {who}: falls in the 8th rāśi",
          k["rasi_8th"] == exp_8th, f"got {k['rasi_8th']}, want {exp_8th}")
# The 64th navāṁśa is always exactly the 8th rāśi from the point, for any longitude.
check("64th navāṁśa rāśi is always the 8th from the point (structural)",
      all(nv.khara_64th(L)["rasi_8th"] == (int(L // 30) + 7) % 12
          for L in (1.0, 47.3, 118.9, 200.0, 271.4, 359.9)))

print("\nVargottama is exactly D1==D9, and the kinds classify correctly:")
check("Sun at Meṣa 1° is uccha-vargottama (exalted)",
      nv.is_vargottama(dms(ARIES, 1)) and nv.vargottama_kind("sun", ARIES) == "uccha")
check("Saturn at Meṣa 1° is nīca-vargottama (debilitated)",
      nv.vargottama_kind("saturn", ARIES) == "neecha")
check("Mars at Meṣa 1° is svakṣetra-vargottama (own sign)",
      nv.vargottama_kind("mars", ARIES) == "swakshetra")
check("lagna vargottama in Vṛṣabha (a benefic sign) is śubha",
      nv.is_vargottama(dms(TAURUS, 14)) and nv.vargottama_kind("lagna", TAURUS) == "subha")
check("lagna vargottama in Meṣa (a malefic sign) is pāpa",
      nv.vargottama_kind("lagna", ARIES) == "papa")
# a fixed sign is vargottama only in its 5th navāṁśa, a dual only in its 9th
check("Vṛṣabha (fixed) is vargottama in the 5th navāṁśa, not the 1st",
      nv.is_vargottama(dms(TAURUS, 14)) and not nv.is_vargottama(dms(TAURUS, 1)))
check("Mithuna (dual) is vargottama in the 9th navāṁśa, not the 1st",
      nv.is_vargottama(dms(GEMINI, 28)) and not nv.is_vargottama(dms(GEMINI, 1)))

print("\nPushkara navāṁśa follows Patel's element-group rule (2 of 9 per sign):")
check("Meṣa 21° (7th navāṁśa) is pushkara; Meṣa 5° is not",
      nv.is_pushkara_navamsa(dms(ARIES, 21)) and not nv.is_pushkara_navamsa(dms(ARIES, 5)))
check("Kaṭaka 1° (1st navāṁśa, watery) is pushkara",
      nv.is_pushkara_navamsa(dms(CANCER, 1)))
check("every sign has exactly two pushkara navāṁśas",
      all(sum(1 for n in range(9)
              if nv.is_pushkara_navamsa(dms(s, n * (10 / 3) + 0.5))) == 2
          for s in range(12)))

print("\nBhāva-sūchaka names the navāṁśa-sign by its rāśi-chart house (Ch.VI):")
# Patel's Ch.VI example: lagna Kanyā; a point whose navāṁśa is Dhanus → 4th
# house → Sukhāṁśa; navāṁśa Kumbha → 6th → Ṣaṣṭhāṁśa.
def house_of(nsign, lagna):
    return ((nsign - lagna) % 12) + 1
check("navāṁśa Dhanus with Kanyā lagna → 4th house (Sukhāṁśa)",
      house_of(SAG, VIRGO) == 4 and nv._BHAVA_SUCHAKA[4][0] == "Sukhāṁśa")
check("navāṁśa Kumbha with Kanyā lagna → 6th house (Ṣaṣṭhāṁśa)",
      house_of(AQU, VIRGO) == 6 and nv._BHAVA_SUCHAKA[6][0] == "Ṣaṣṭhāṁśa")
check("bhāva-sūchaka tally sums to the ten points (9 grahas + lagna)",
      sum(res["bhava_suchaka"]["tally"].values()) == 10,
      str(res["bhava_suchaka"]["tally"]))

print("\nProvenance: everything is tier `modern` and attributed to Patel, not BPHS:")
check("top-level tier is modern and names C. S. Patel",
      res["tier"] == "modern" and "Patel" in res["source"])
for grp in ("vargottama", "pushkara", "khara", "bhava_suchaka"):
    check(f"{grp} cites a Patel chapter",
          "Patel" in res[grp]["citation"])
check("nothing claims BPHS/Parāśara for the readings",
      "BPHS" not in res["source"] and "Parāśara" not in res["source"])
check("the note keeps the D9 itself (BPHS ch.6) distinct from Patel's readings",
      "ch.6" in res["note"] and "NOT BPHS" in res["note"])

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
