import sys
sys.path.insert(0, r"C:\proj\astrodev\api")
from dignity import (dignity_of, sign_landmarks, nakshatra_gandanta,
                     EXALTATION, DEBILITATION,
                     NATURAL_RELATIONS, RASI_LORD)

S = ["Mesha","Vrishabha","Mithuna","Karka","Simha","Kanya",
     "Tula","Vrishchika","Dhanus","Makara","Kumbha","Meena"]
fails = []
def check(label, cond, detail=""):
    if not cond: fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  '+detail) if detail else ''}")

print("BPHS ch.3 vv.49-50 — exaltation signs and deep degrees:")
book = {"sun":("Mesha",10),"moon":("Vrishabha",3),"mars":("Makara",28),
        "mercury":("Kanya",15),"jupiter":("Karka",5),"venus":("Meena",27),
        "saturn":("Tula",20)}
for g,(sn,dg) in book.items():
    s,d = EXALTATION[g]
    check(f"{g} exalted {sn} {dg}deg", S[s]==sn and d==dg, f"got {S[s]} {d}")

print("\nDebilitation = SAME degree, 7th sign from exaltation (derived, not typed):")
for g in EXALTATION:
    es,ed = EXALTATION[g]; ds,dd = DEBILITATION[g]
    check(f"{g} debilitated {S[ds]} {dd}deg",
          ds==(es+6)%12 and dd==ed, f"exalt {S[es]}{ed} -> debil {S[ds]}{dd}")

print("\nNodes carry NO dignity (v.50: 'there are different views'):")
for g in ("rahu","ketu"):
    check(f"{g} -> None", dignity_of(g, 123.4) is None)

print("\nStates at the exact doctrinal points:")
for g,(s,d) in EXALTATION.items():
    r = dignity_of(g, s*30+d)
    check(f"{g} at its exact uccha -> exalted", r["state"]=="exalted", r["state"])
    check(f"{g} uccha_distance == 0", abs(r["uccha_distance"])<1e-9, str(r["uccha_distance"]))
    check(f"{g} uccha_bala == 1.0", abs(r["uccha_bala"]-1.0)<1e-9, str(r["uccha_bala"]))
for g,(s,d) in DEBILITATION.items():
    r = dignity_of(g, s*30+d)
    check(f"{g} at its exact nica -> debilitated", r["state"]=="debilitated", r["state"])
    check(f"{g} uccha_bala == 0.0", abs(r["uccha_bala"])<1e-9, str(r["uccha_bala"]))

print("\nvv.51-54 mulatrikona arcs (the partition inside a sign):")
# Sun: Leo 0-20 MT, 20-30 own
check("Sun Leo 10deg -> moolatrikona", dignity_of("sun", 4*30+10)["state"]=="moolatrikona")
check("Sun Leo 25deg -> own",          dignity_of("sun", 4*30+25)["state"]=="own")
# Mars: Aries 0-12 MT, 12-30 own
check("Mars Aries 5deg -> moolatrikona",  dignity_of("mars", 0*30+5)["state"]=="moolatrikona")
check("Mars Aries 20deg -> own",          dignity_of("mars", 0*30+20)["state"]=="own")
check("Mars Scorpio 15deg -> own",        dignity_of("mars", 7*30+15)["state"]=="own")
# Mercury Virgo is explicitly partitioned 0-15 exalt / 15-20 MT / 20-30 own
check("Mercury Virgo 8deg -> exalted",       dignity_of("mercury", 5*30+8)["state"]=="exalted")
check("Mercury Virgo 17deg -> moolatrikona", dignity_of("mercury", 5*30+17)["state"]=="moolatrikona")
check("Mercury Virgo 25deg -> own",          dignity_of("mercury", 5*30+25)["state"]=="own")
# Jupiter: Sagittarius first third
check("Jupiter Sag 5deg -> moolatrikona", dignity_of("jupiter", 8*30+5)["state"]=="moolatrikona")
check("Jupiter Sag 20deg -> own",         dignity_of("jupiter", 8*30+20)["state"]=="own")
# Venus: Libra halves
check("Venus Libra 7deg -> moolatrikona", dignity_of("venus", 6*30+7)["state"]=="moolatrikona")
check("Venus Libra 22deg -> own",         dignity_of("venus", 6*30+22)["state"]=="own")
# Saturn: Aquarius same as Sun in Leo
check("Saturn Aqu 10deg -> moolatrikona", dignity_of("saturn", 10*30+10)["state"]=="moolatrikona")
check("Saturn Aqu 25deg -> own",          dignity_of("saturn", 10*30+25)["state"]=="own")

print("\nv.55 natural relationships — the worked examples in the Notes:")
# "Take for example the case of Mars ... Saturn becomes equal to Mars."
check("Saturn is NEUTRAL to Mars (book's worked example)",
      NATURAL_RELATIONS["mars"]["saturn"]=="neutral", NATURAL_RELATIONS["mars"]["saturn"])
# "He owns the 2nd and 7th from the Moolatrikona of Mars ... Hence he is neutral"
check("Venus is NEUTRAL to Mars (book's worked example)",
      NATURAL_RELATIONS["mars"]["venus"]=="neutral", NATURAL_RELATIONS["mars"]["venus"])
# From the book's table: Sun's friends = Moon, Mars, Jupiter
for f in ("moon","mars","jupiter"):
    check(f"Sun-{f} = friend", NATURAL_RELATIONS["sun"][f]=="friend", NATURAL_RELATIONS["sun"][f])
check("Sun-venus = enemy",  NATURAL_RELATIONS["sun"]["venus"]=="enemy",  NATURAL_RELATIONS["sun"]["venus"])
check("Sun-saturn = enemy", NATURAL_RELATIONS["sun"]["saturn"]=="enemy", NATURAL_RELATIONS["sun"]["saturn"])

print("\nGandanta - BPHS Vol II ch.92 v.3: TIME-based, derived from Moon speed:")
MOON_SPEED = 13.2                      # deg/day, near average
HALF = MOON_SPEED * 2 / 60             # 2 ghatikas = 2/60 day -> ~0.44 deg
r = nakshatra_gandanta(120.0, MOON_SPEED)
check("Moon exactly on Karka|Simha junction -> gandanta", r is not None)
check("half-width ~0deg26' (NOT the 3deg20' navamsa)",
      r and abs(r["half_width"] - HALF) < 1e-6, "got %.4f deg" % r["half_width"])
check("the 3deg20' reading would be ~8x too wide",
      abs((3+1/3)/HALF - 7.58) < 0.1, "ratio %.2fx" % ((3+1/3)/HALF))
for j,label in ((120.0,"Karka|Simha"),(240.0,"Vrischika|Dhanus"),(0.0,"Meena|Mesha")):
    check("junction %s detected" % label, nakshatra_gandanta(j, MOON_SPEED) is not None)
check("Meena|Mesha wraps across 360/0",
      nakshatra_gandanta(359.9, MOON_SPEED) is not None and
      nakshatra_gandanta(0.1, MOON_SPEED) is not None)
others = [s*30.0 for s in range(12) if s*30.0 not in (0.0,120.0,240.0)]
check("NO other sign boundary is gandanta",
      all(nakshatra_gandanta(b, MOON_SPEED) is None for b in others),
      "checked %d boundaries" % len(others))
check("just outside the zone -> None",
      nakshatra_gandanta(120.0 + HALF + 0.01, MOON_SPEED) is None)
check("zone widens with a faster Moon (time-based, not a fixed arc)",
      nakshatra_gandanta(120.0, 15.0)["half_width"] >
      nakshatra_gandanta(120.0, 11.8)["half_width"])
check("sign_landmarks no longer claims gandanta (it cannot know speed)",
      "gandanta_zones" not in sign_landmarks(3))

print("\nsign_landmarks — what a 0-30 ruler needs:")
lm = sign_landmarks(6)   # Libra
print(f"  Libra: exalt={lm['exaltation_points']} debil={lm['debilitation_points']} mt={lm['moolatrikona_arcs']}")
check("Libra holds Saturn's exaltation at 20",
      lm["exaltation_points"]==[{"graha":"saturn","degree":20.0}])
check("Libra holds Sun's debilitation at 10",
      lm["debilitation_points"]==[{"graha":"sun","degree":10.0}])

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
