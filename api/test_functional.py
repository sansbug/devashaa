import sys
# Quotes and flags carry IAST diacritics (ā, ṣ, ṇ, ś); a cp1252 console would
# raise on them. Reconfigure rather than strip — the diacritics are the point.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
sys.path.insert(0, r"C:\proj\astrodev\api")
from functional import (
    functional_nature, classify_by_lordship, lordship_profile, houses_owned,
    house_of, moolatrikona_house, lagna_profile, node_yogakaraka,
    natural_nature, maraka_houses, maraka_lords, maraka_analysis, maraka_grade,
    disagreements, LAGNA_NATURE, LAGNA_MARAKA, NATURE_UNAVAILABLE,
    NATURE_FROM_NOTE_ONLY, KNOWN_CONFLICTS, INTERNAL_ASYMMETRIES,
    MARAKA_HOUSES, MARAKA_STRONGEST, LONGEVITY_HOUSES, NODES,
    RAHU_PRIMARY_MARAKA_LAGNAS, GRAHAS, SEVEN,
    NATURE_CELL_FLAGS, MARAKA_IS_NOT_A_NATURE, DHANUS_SATURN_AMBIGUOUS,
    ARI_MARS_NOT_INDEPENDENTLY_BENEFIC, MOON_KENDRA_PHASE_DEPENDENT,
    LUMINARY_EXCEPTION_NARROWED_TO_SUN, NODE_EXCLUSION_PRECEDENCE,
    CH44_RAHU_DUSTHANA_GAP,
)

S = ["Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
     "Tula", "Vrishchika", "Dhanus", "Makara", "Kumbha", "Meena"]
ARI, TAU, GEM, CAN, LEO, VIR, LIB, SCO, SAG, CAP, AQU, PIS = range(12)

fails = []
def check(label, cond, detail=""):
    if not cond: fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  '+detail) if detail else ''}")


print("BPHS ch.34 vv.2-7 — the general law, house groups:")
check("lagna is both angle and trine",
      1 in (1, 4, 7, 10) and 1 in (1, 5, 9))
check("houses_owned derives from RASI_LORD, not a typed table: "
      "Mesha lagna -> Saturn owns 10th and 11th",
      houses_owned("saturn", ARI) == (10, 11), str(houses_owned("saturn", ARI)))
check("house_of is whole-sign: Makara from Mesha lagna = 10th",
      house_of(CAP, ARI) == 10)
check("moolatrikona_house comes from dignity.MOOLATRIKONA: "
      "Saturn's Kumbha is the 11th from Mesha",
      moolatrikona_house("saturn", ARI) == 11)


print("\nch.34 note to vv.2-7 (8) — the worked example the notes give for Aries/Saturn:")
# "If we consider Saturn for Aries ascendant, he gets one best house and one
#  worst house, i.e. the 10th and 11th houses. The 11th house being his
#  Moolatrikona, he is predominantly the 11th lord ... and hence very evil."
p = lordship_profile("saturn", ARI)
check("Aries/Saturn owns the 10th (angle) and the 11th (evil)",
      p["kendras_owned"] == (10,) and p["evil_owned"] == (11,))
check("Aries/Saturn moolatrikona is the 11th -> predominantly the 11th lord",
      p["moolatrikona_house"] == 11)
check("Aries/Saturn derived nature = malefic",
      classify_by_lordship("saturn", ARI)["nature"] == "malefic",
      classify_by_lordship("saturn", ARI)["nature"])
check("...and the sloka agrees: 'Saturn, Mercury and Venus are malefics'",
      functional_nature("saturn", ARI)["nature"] == "malefic")

# "Similarly his role for Gemini ascendant in which case the 9th lordship
#  prevails over his 8th lordship and so he is not evil but favourable."
p = lordship_profile("saturn", GEM)
check("Gemini/Saturn owns the 8th and 9th, moolatrikona in the 9th",
      p["houses_owned"] == (8, 9) and p["moolatrikona_house"] == 9,
      str(p["houses_owned"]))
check("Gemini/Saturn derived nature = benefic (9th prevails over 8th)",
      classify_by_lordship("saturn", GEM)["nature"] == "benefic",
      classify_by_lordship("saturn", GEM)["nature"])


print("\nch.34 note to vv.2-7 (1) — kendradhipatya dosha, the book's own example:")
# "For example, for Gemini ascendant the ownership of 4th and 7th goes to
#  Jupiter and hence he is not a benefic for this ascendant."
#  (The scan says 4th/7th; for Gemini lagna Jupiter in fact owns the 7th and
#   10th — Sagittarius and Pisces. The 4th/7th pairing is Jupiter's for VIRGO
#   lagna. Both are kendra-only, so the point stands for both; see report.)
check("Gemini/Jupiter owns two angles only -> kendradhipatya",
      lordship_profile("jupiter", GEM)["kendras_owned"] == (7, 10)
      and not lordship_profile("jupiter", GEM)["trikonas_owned"],
      str(lordship_profile("jupiter", GEM)["houses_owned"]))
check("Gemini/Jupiter derived = malefic, 'hence he is not a benefic'",
      classify_by_lordship("jupiter", GEM)["nature"] == "malefic")
check("...and the sloka agrees: 'Mars, Jupiter and the Sun are malefics'",
      functional_nature("jupiter", GEM)["nature"] == "malefic")
check("Virgo/Jupiter owns the 4th and 7th, also kendra-only -> malefic",
      lordship_profile("jupiter", VIR)["kendras_owned"] == (4, 7)
      and classify_by_lordship("jupiter", VIR)["nature"] == "malefic")
check("Virgo/Jupiter sloka agrees: 'Mars, Jupiter and the Moon are malefics'",
      functional_nature("jupiter", VIR)["nature"] == "malefic")
print(chr(10) + "ch.34 notes to vv.2-7 (1) vs (2) — the Moon's kendra verdict is "
      "PHASE-DEPENDENT and the module refuses to guess the phase:")
# note (1): "Natural benefics are increasing Moon, Mercury, Jupiter and Venus
#  ... the Moon is the least malefic ... by such ownership."
# note (2): "weak Moon by virtue of angular lordship remains just neutral."
# The three lagnas where the Moon owns a kendra and nothing else:
moon_kendra_only = [lg for lg in range(12)
                    if set(houses_owned("moon", lg)) & {4, 7, 10}
                    and not set(houses_owned("moon", lg)) & {1, 5, 9}]
check("the Moon owns a kendra and nothing else for exactly Mesha, Tula, Makara",
      moon_kendra_only == [ARI, LIB, CAP], str(moon_kendra_only))
for lg in moon_kendra_only:
    check(f"{S[lg]}/Moon, phase UNKNOWN -> refuses a nature (None)",
          classify_by_lordship("moon", lg)["nature"] is None,
          str(classify_by_lordship("moon", lg)["nature"]))
    check(f"{S[lg]}/Moon, INCREASING -> malefic (note 1, 'least malefic')",
          classify_by_lordship("moon", lg, moon_waxing=True)["nature"] == "malefic",
          str(classify_by_lordship("moon", lg, moon_waxing=True)["nature"]))
    check(f"{S[lg]}/Moon, WEAK -> neutral (note 2, 'remains just neutral')",
          classify_by_lordship("moon", lg, moon_waxing=False)["nature"] == "neutral",
          str(classify_by_lordship("moon", lg, moon_waxing=False)["nature"]))
check("the refusal carries the phase flag, naming BOTH notes",
      MOON_KENDRA_PHASE_DEPENDENT in classify_by_lordship("moon", CAP)["reasons"])
check("...and the luminary-narrowing flag, since the note's word is plural",
      LUMINARY_EXCEPTION_NARROWED_TO_SUN
      in classify_by_lordship("moon", CAP)["reasons"])
check("Cancer/Moon is the LAGNA lord, so the phase rule never reaches her",
      classify_by_lordship("moon", CAN)["nature"] == "benefic",
      classify_by_lordship("moon", CAN)["nature"])
check("a phase-less derivation is labelled 'no_derived_verdict', NOT agreement",
      {r["graha"]: r["agreement"] for r in lagna_profile(CAP)["grahas"]}["moon"]
      == "no_derived_verdict")


print("\nch.34 v.13 — YOGAKARAKA = one graha owning an angle AND a trine.")
print("The six the notes name explicitly, plus the two more the law yields:")
book_yogakarakas = {
    (LIB, "saturn"): (4, 5),   # "For Libra ascendant, Saturn is classified as
    (LEO, "mars"):   (4, 9),   #  unsullied yogakaraka because he owns the 4th
    (CAN, "mars"):   (5, 10),  #  (an angle) and the 5th (a trine)."
    (CAP, "venus"):  (5, 10),  # "the former is the best yogakaraka for this
    (AQU, "venus"):  (4, 9),   #  ascendant, for he is the lord of the 5th and 10th"
    (TAU, "saturn"): (9, 10),  # "Saturn owns the best trine and best angle"
}
for (lg, g), owned in book_yogakarakas.items():
    got = houses_owned(g, lg)
    check(f"{S[lg]} lagna: {g} owns {owned}", got == owned, str(got))
    check(f"{S[lg]} lagna: {g} -> yogakaraka",
          classify_by_lordship(g, lg)["nature"] == "yogakaraka",
          classify_by_lordship(g, lg)["nature"])
all_yk = {(lg, g) for lg in range(12) for g in SEVEN
          if classify_by_lordship(g, lg)["nature"] == "yogakaraka"}
check("the general law yields exactly the six classical yogakarakas "
      "(no more, no less)",
      all_yk == set(book_yogakarakas), str(sorted(all_yk)))

print("\nch.34 v.14 — a malefic gains from angular lordship ONLY with a trine:")
# "The same Mars for Capricorn ascendant by virtue of angular lordship is not
#  that auspicious, because he does not simultaneously own a trine. Similarly
#  his role for Aquarius ascendant."
check("Capricorn/Mars owns the 4th and 11th — angle but no trine",
      houses_owned("mars", CAP) == (4, 11), str(houses_owned("mars", CAP)))
check("Capricorn/Mars is NOT auspicious (derived malefic, 11th lordship)",
      classify_by_lordship("mars", CAP)["nature"] == "malefic")
check("Capricorn/Mars sloka agrees: 'Mars, Jupiter and the Moon are malefics'",
      functional_nature("mars", CAP)["nature"] == "malefic")
check("Aquarius/Mars owns the 3rd and 10th — angle but no trine",
      houses_owned("mars", AQU) == (3, 10), str(houses_owned("mars", AQU)))
check("Aquarius/Mars sloka agrees: 'Jupiter, the Moon and Mars are malefics'",
      functional_nature("mars", AQU)["nature"] == "malefic")

print("\nch.34 note to vv.2-7 (4) — 'Jupiter is doubly evil for Libra "
      "ascendant as he owns the 3rd and 6th':")
check("Libra/Jupiter owns the 3rd and 6th",
      houses_owned("jupiter", LIB) == (3, 6), str(houses_owned("jupiter", LIB)))
check("Libra/Jupiter derived = malefic", classify_by_lordship("jupiter", LIB)["nature"] == "malefic")
check("Libra/Jupiter sloka agrees: 'Jupiter, the Sun and Mars are malefics'",
      functional_nature("jupiter", LIB)["nature"] == "malefic")

print("\nch.34 note to vv.27-28 — '11th lord for a movable sign is a malefic':")
# "i.e. Saturn for Aries, Venus for Cancer, the Sun for Libra and Mars for
#  Capricorn ascendants."
for lg, g in ((ARI, "saturn"), (CAN, "venus"), (LIB, "sun"), (CAP, "mars")):
    check(f"{S[lg]} lagna: {g} is the 11th lord",
          11 in houses_owned(g, lg), str(houses_owned(g, lg)))
    check(f"{S[lg]} lagna: {g} -> malefic (both text and law)",
          functional_nature(g, lg)["nature"] == "malefic"
          and classify_by_lordship(g, lg)["nature"] == "malefic")

print("\nch.34 note to vv.23-24 — the LUMINARY exception to v.14 (a NOTE):")
# "The Sun though a malefic by virtue of owning an angle proves auspicious.
#  The rule that a malefic owning an angle should own a trine also ... is
#  naturally not applicable to the luminaries as they own only one sign each."
check("Taurus/Sun owns the 4th only", houses_owned("sun", TAU) == (4,))
check("Taurus/Sun sloka: 'Saturn and the Sun are auspicious'",
      functional_nature("sun", TAU)["nature"] == "benefic")
check("Taurus/Sun derived benefic ONLY via the luminary note",
      classify_by_lordship("sun", TAU)["nature"] == "benefic"
      and "note" in classify_by_lordship("sun", TAU)["rule"],
      classify_by_lordship("sun", TAU)["rule"])
# "The Sun's beneficence to Taurus ascendant cannot be compared to Saturn's
#  for Libra, because the Sun has only one house which is angular."
check("...but Libra/Saturn outranks him: yogakaraka vs plain benefic",
      classify_by_lordship("saturn", LIB)["nature"] == "yogakaraka"
      and classify_by_lordship("sun", TAU)["nature"] == "benefic")

print("\nch.34 note to vv.35-36 — 'Jupiter though ruling the 2nd (and the 5th) "
      "is auspicious just as Mercury for Taurus ruling the 2nd and the 5th':")
check("Scorpio/Jupiter owns the 2nd and 5th",
      houses_owned("jupiter", SCO) == (2, 5), str(houses_owned("jupiter", SCO)))
check("Taurus/Mercury owns the 2nd and 5th (the book's own comparison)",
      houses_owned("mercury", TAU) == (2, 5), str(houses_owned("mercury", TAU)))
check("Scorpio/Jupiter sloka: auspicious",
      functional_nature("jupiter", SCO)["nature"] == "benefic")
check("Taurus/Mercury is 'mixed' — but that is the NOTE's word, not the "
      "sloka's ('Mercury is somewhat auspicious,')",
      functional_nature("mercury", TAU)["nature"] == "mixed"
      and functional_nature("mercury", TAU)["source"] == "note",
      str(functional_nature("mercury", TAU)["source"]))
check("...and the sloka's own word is preserved in the quote",
      "somewhat auspicious" in functional_nature("mercury", TAU)["quote"])

print("\nch.34 note to vv.25-26 — 'Mercury for Libra ascendant is considered "
      "favourable although he owns the 12th, which is his Moolatrikona':")
check("Libra/Mercury owns the 9th and 12th",
      houses_owned("mercury", LIB) == (9, 12), str(houses_owned("mercury", LIB)))
check("Libra/Mercury moolatrikona (Kanya) is the 12th",
      moolatrikona_house("mercury", LIB) == 12)
check("Libra/Mercury sloka: 'Auspicious are Saturn and Mercury'",
      functional_nature("mercury", LIB)["nature"] == "benefic")

print("\nch.34 vv.11-12/17 — the yoga example, and the nodes:")
# "(1) exchange between an angular lord and a trinal lord. For example Gemini
#  ascendant having Mercury in Aquarius and Saturn in Virgo."
check("Gemini lagna: Mercury is an angular lord (1st, 4th)",
      set(houses_owned("mercury", GEM)) & {4, 7, 10} == {4})
check("Gemini lagna: Saturn is a trinal lord (9th) — hence the exchange yoga",
      9 in houses_owned("saturn", GEM))
# v.17: node in an angle related to a trinal lord, or in a trine related to
# an angular lord.
check("v.17: node in the 4th with a 9th lord -> yogakaraka",
      node_yogakaraka(4, [9]) is True)
check("v.17: node in the 5th with a 10th lord -> yogakaraka",
      node_yogakaraka(5, [10]) is True)
check("v.17: node in the 3rd with a 9th lord -> NOT yogakaraka",
      node_yogakaraka(3, [9]) is False)
check("v.17: node in an angle with an angular lord -> NOT yogakaraka",
      node_yogakaraka(4, [10]) is False)

print("\nch.34 v.16 — the nodes get NO per-lagna nature (24 cells absent):")
for lg in range(12):
    for n in NODES:
        r = functional_nature(n, lg)
        if r["nature"] is not None or r["source"] is not None:
            check(f"{S[lg]}/{n} unclassified", False, str(r["nature"]))
check("all 24 node cells return nature=None, source=None, is_node=True",
      all(functional_nature(n, lg)["nature"] is None
          and functional_nature(n, lg)["source"] is None
          and functional_nature(n, lg)["is_node"]
          for lg in range(12) for n in NODES))
check("nodes own no rasi, so houses_owned is empty",
      all(houses_owned(n, lg) == () for lg in range(12) for n in NODES))


print("\n=== THE SOURCE TAG — every cell says whether a SLOKA or a NOTE gave it ===")
check("all 84 non-nodal cells present (12 lagnas x 7 grahas)",
      sum(len(LAGNA_NATURE[lg]) for lg in range(12)) == 84,
      str(sum(len(LAGNA_NATURE[lg]) for lg in range(12))))
check("every source tag is exactly 'sloka', 'note' or None",
      all(c[1] in ("sloka", "note", None)
          for lg in range(12) for c in LAGNA_NATURE[lg].values()))
check("a cell with no nature has no source, and vice versa",
      all((c[0] is None) == (c[1] is None)
          for lg in range(12) for c in LAGNA_NATURE[lg].values()))
check("every cell carries a citation and a quote",
      all(c[2] and c[3] for lg in range(12) for c in LAGNA_NATURE[lg].values()))

print("\nThe three cells Santhanam HIMSELF flags as sage-silent:")
# "The Moon's role is not discussed by the sage."
check("Aries/Moon comes from a NOTE",
      functional_nature("moon", ARI)["source"] == "note",
      str(functional_nature("moon", ARI)["source"]))
check("Aries/Moon quote records the silence",
      "not discussed by the sage" in functional_nature("moon", ARI)["quote"])
# "There is no hint on Saturn's role"
check("Gemini/Saturn comes from a NOTE",
      functional_nature("saturn", GEM)["source"] == "note")
check("Gemini/Saturn quote records the silence — and reproduces the scan's "
      "own lower-case 'saturn', unrepaired, since nothing is missing",
      "no hint on saturn's role" in functional_nature("saturn", GEM)["quote"])
# "There is no hint in the text about Saturn's role."
check("Virgo/Saturn comes from a NOTE",
      functional_nature("saturn", VIR)["source"] == "note")
check("Virgo/Saturn quote records the silence",
      "no hint in the text about Saturn's role" in functional_nature("saturn", VIR)["quote"])

print("\nThe full note-only census (nature supplied ONLY by Santhanam):")
expected_note_only = {
    (ARI, "moon"), (TAU, "mercury"), (GEM, "saturn"),
    (VIR, "saturn"), (SAG, "moon"), (CAP, "saturn"),
}
for lg, g in sorted(expected_note_only):
    print(f"    {S[lg]:<10} {g:<8} -> {LAGNA_NATURE[lg][g][0]:<8} [note]")
check("exactly 6 cells are note-only",
      set(NATURE_FROM_NOTE_ONLY) == expected_note_only,
      str(sorted(set(NATURE_FROM_NOTE_ONLY) ^ expected_note_only)))

print("\nAnd the cells where NEITHER sloka NOR note gives a nature — "
      "refused, not guessed:")
expected_unavailable = {
    (GEM, "moon"), (GEM, "mercury"), (LEO, "moon"), (AQU, "sun"),
    (TAU, "mars"), (SAG, "saturn"),
}
for lg, g in sorted(expected_unavailable):
    print(f"    {S[lg]:<10} {g:<8} -> nature is None")
check("exactly 6 cells are unavailable",
      set(NATURE_UNAVAILABLE) == expected_unavailable,
      str(sorted(set(NATURE_UNAVAILABLE) ^ expected_unavailable)))
check("12 of 84 cells are NOT supplied by a per-lagna sloka (6 note + 6 none)",
      len(NATURE_FROM_NOTE_ONLY) + len(NATURE_UNAVAILABLE) == 12)
check("the other 72 cells are sloka-sourced",
      sum(1 for lg in range(12) for c in LAGNA_NATURE[lg].values()
          if c[1] == "sloka") == 72)
check("functional_nature NEVER silently substitutes the derivation",
      all(functional_nature(g, lg)["nature"] is None
          for lg, g in NATURE_UNAVAILABLE))


print("\n=== ch.34 vv.19-44 — every planet the twelve verses actually name ===")
verses = {
    ARI: {"saturn": "malefic", "mercury": "malefic", "venus": "malefic",
          "jupiter": "benefic", "sun": "benefic", "mars": "conditional"},
    TAU: {"jupiter": "malefic", "venus": "malefic", "moon": "malefic",
          "saturn": "yogakaraka", "sun": "benefic"},
    GEM: {"mars": "malefic", "jupiter": "malefic", "sun": "malefic",
          "venus": "benefic"},
    CAN: {"venus": "malefic", "mercury": "malefic", "mars": "yogakaraka",
          "jupiter": "benefic", "moon": "benefic",
          "sun": "conditional", "saturn": "conditional"},
    LEO: {"mercury": "malefic", "venus": "malefic", "saturn": "malefic",
          "mars": "benefic", "jupiter": "benefic", "sun": "benefic"},
    VIR: {"mars": "malefic", "jupiter": "malefic", "moon": "malefic",
          "mercury": "benefic", "venus": "benefic", "sun": "conditional"},
    LIB: {"jupiter": "malefic", "sun": "malefic", "mars": "malefic",
          "saturn": "benefic", "mercury": "benefic", "moon": "benefic",
          "venus": "neutral"},
    SCO: {"venus": "malefic", "mercury": "malefic", "saturn": "malefic",
          "jupiter": "benefic", "moon": "yogakaraka", "sun": "yogakaraka",
          "mars": "neutral"},
    SAG: {"venus": "malefic", "mars": "benefic", "sun": "benefic",
          "mercury": "benefic", "jupiter": "neutral"},
    CAP: {"mars": "malefic", "jupiter": "malefic", "moon": "malefic",
          "venus": "yogakaraka", "mercury": "benefic", "sun": "neutral"},
    AQU: {"jupiter": "malefic", "moon": "malefic", "mars": "malefic",
          "venus": "yogakaraka", "saturn": "benefic", "mercury": "mixed"},
    PIS: {"saturn": "malefic", "venus": "malefic", "sun": "malefic",
          "mercury": "malefic", "mars": "benefic", "moon": "benefic",
          "jupiter": "benefic"},
}
for lg in range(12):
    got = {g: c[0] for g, c in LAGNA_NATURE[lg].items() if c[1] == "sloka"}
    check(f"{S[lg]:<10} sloka cells match the verse verbatim",
          got == verses[lg], f"got {got}")


print("\n=== THE NOTES' CLOSED LISTS - an independent cross-check on the table ===")
print("Santhanam repeatedly enumerates a lagna's benefics or malefics EXHAUSTIVELY.")
print("These lists come from the prose notes, not from the verse transcription")
print("above, so they can contradict it - and they are the check that fails if a")
print("cell is misread.")

def cells_with(lg, *natures):
    return {g for g in SEVEN if LAGNA_NATURE[lg][g][0] in natures}

# Note to vv.19-22: "As r[e]gards other unsullied benefic planets for this
#  ascendant we have only two. These are Jupiter and the Sun."
check("Mesha: the notes allow EXACTLY TWO benefics - Jupiter and the Sun",
      cells_with(ARI, "benefic", "yogakaraka") == {"jupiter", "sun"},
      str(sorted(cells_with(ARI, "benefic", "yogakaraka"))))
check("...so Mars is NOT among them ('He cannot be independently auspicious')",
      LAGNA_NATURE[ARI]["mars"][0] == "conditional",
      str(LAGNA_NATURE[ARI]["mars"][0]))

# vv.23-24 + notes: "Jupiter, Venus and the Moon are malefics." Jupiter "the
#  first-rate adversary", "The Moon being the 3rd lord is not auspicious",
#  "Venus is also classified here as an evil planet". Mars is absent.
check("Vrishabha: the malefic list is EXACTLY Jupiter, Venus, the Moon",
      cells_with(TAU, "malefic") == {"jupiter", "venus", "moon"},
      str(sorted(cells_with(TAU, "malefic"))))

# Note to vv.25-26: "The three planets, viz. Jupiter, the Sun and Mars are
#  adverse for Gemini ascendant."
check("Mithuna: 'The three planets, viz. Jupiter, the Sun and Mars are adverse'",
      cells_with(GEM, "malefic") == {"jupiter", "sun", "mars"},
      str(sorted(cells_with(GEM, "malefic"))))

# Note to vv.27-28: "The best planet for this ascendant is Mars ... The other
#  two favourable planets are Jupiter and the Moon. ... The order of
#  preference is Mars, Jupiter and the lvloon."
check("Karka: exactly three favourable - Mars, Jupiter, the Moon",
      cells_with(CAN, "benefic", "yogakaraka") == {"mars", "jupiter", "moon"},
      str(sorted(cells_with(CAN, "benefic", "yogakaraka"))))

# Note to vv.29-30: "Mars is again the best pranet for Leo ascendant foilowed
#  by favourable roles to. be enacted by Jupiter and the sun."
check("Simha: exactly three favourable - Mars, Jupiter, the Sun",
      cells_with(LEO, "benefic", "yogakaraka") == {"mars", "jupiter", "sun"},
      str(sorted(cells_with(LEO, "benefic", "yogakaraka"))))

# Note to vv.33-34: "These three planets, viz. Jupiter, Mars and the Sun are
#  morc malefic if mutually related..."
check("Tula: 'These three planets, viz. Jupiter, Mars and the Sun'",
      cells_with(LIB, "malefic") == {"jupiter", "mars", "sun"},
      str(sorted(cells_with(LIB, "malefic"))))

# vv.37-38: "Only Venus is[ ]inauspicious." + note: "The sage hints that none
#  is akin to venus in giving marefic effects for this ascendant."
check("Dhanus: 'Only Venus is inauspicious' - EXACTLY ONE malefic",
      cells_with(SAG, "malefic") == {"venus"},
      str(sorted(cells_with(SAG, "malefic"))))
check("...so Saturn is not a second malefic, despite 'straightaway a killer'",
      LAGNA_NATURE[SAG]["saturn"][0] is None)

# Note to vv.41-42: "The 2nd and llth lordJupiterisadiremalefic followed by
#  the Moon (the 6th lord) and Mars (ruring the 3rd and l0th)."
check("Kumbha: exactly three malefics - Jupiter, the Moon, Mars",
      cells_with(AQU, "malefic") == {"jupiter", "moon", "mars"},
      str(sorted(cells_with(AQU, "malefic"))))

# Note to vv.43-44: Saturn "two evir houses", Venus "the 3rd and 8th--again
#  two evil houses", "The sun ruling the 6th will prove adverse", + Mercury.
check("Meena: exactly four malefics - Saturn, Venus, the Sun, Mercury",
      cells_with(PIS, "malefic") == {"saturn", "venus", "sun", "mercury"},
      str(sorted(cells_with(PIS, "malefic"))))


print("\n=== POLICY: a MARAKA verdict is never promoted to a NATURE ===")
# note to vv.45-46: "A killer is a killer irrespective of his havi[n]g become a
#  Rajayogakaraka or so. Killer and Yogakaraka should not be mixed together in
#  respect of o[n]e and the same planet."
maraka_only = [(TAU, "mars"), (GEM, "moon"), (LEO, "moon"),
               (AQU, "sun"), (SAG, "saturn")]
for lg, g in maraka_only:
    check(f"{S[lg]}/{g}: only a killer verdict in the text -> nature is None",
          functional_nature(g, lg)["nature"] is None,
          str(functional_nature(g, lg)["nature"]))
    check(f"{S[lg]}/{g}: carries the MARAKA_IS_NOT_A_NATURE flag",
          MARAKA_IS_NOT_A_NATURE in functional_nature(g, lg)["flags"])
check("Dhanus/Saturn additionally carries the AMBIGUOUS flag naming BOTH "
      "readings and saying the text does not decide",
      DHANUS_SATURN_AMBIGUOUS in functional_nature("saturn", SAG)["flags"]
      and "does not decide" in DHANUS_SATURN_AMBIGUOUS)
check("Mesha/Mars carries the flag explaining the demotion from 'benefic'",
      ARI_MARS_NOT_INDEPENDENTLY_BENEFIC
      in functional_nature("mars", ARI)["flags"])

print("\nNothing was LOST by the demotions - the killer verdicts survive "
      "in LAGNA_MARAKA:")
check("Vrishabha/Mars: nature removed, maraka 'primary' retained",
      functional_nature("mars", TAU)["nature"] is None
      and functional_nature("mars", TAU)["maraka"] == "primary")
check("Dhanus/Saturn: nature removed, maraka 'primary' retained",
      functional_nature("saturn", SAG)["nature"] is None
      and functional_nature("saturn", SAG)["maraka"] == "primary")
check("Karka/Sun and Karka/Saturn share one sloka clause, so one verdict: "
      "'give effects according to association' -> conditional, for BOTH",
      functional_nature("sun", CAN)["nature"] == "conditional"
      and functional_nature("saturn", CAN)["nature"] == "conditional"
      and functional_nature("sun", CAN)["source"] == "sloka"
      and functional_nature("saturn", CAN)["source"] == "sloka")
check("...matching Kanya/Sun, the identical formula elsewhere in the chapter",
      functional_nature("sun", VIR)["nature"] == "conditional")


print("\n=== TEXT vs THE GENERAL LAW — reported, never silently resolved ===")
conf = {(d["lagna"], d["graha"]): d for d in disagreements("conflict")}
check("exactly 2 outright sign-flips between verse and general law",
      len(conf) == 2, str(sorted(conf)))
check("Cancer/Jupiter is one of them (verse says benefic, law says malefic)",
      conf.get((CAN, "jupiter"), {}).get("text_nature") == "benefic"
      and conf[(CAN, "jupiter")]["derived_nature"] == "malefic")
check("Sagittarius/Mercury is the other (verse benefic, law kendradhipatya)",
      conf.get((SAG, "mercury"), {}).get("text_nature") == "benefic"
      and conf[(SAG, "mercury")]["derived_nature"] == "malefic")
check("both are documented in KNOWN_CONFLICTS with the sage's own get-out",
      set(KNOWN_CONFLICTS) == set(conf), str(set(KNOWN_CONFLICTS) ^ set(conf)))
for k, v in sorted(KNOWN_CONFLICTS.items()):
    print(f"    CONFLICT {S[k[0]]}/{k[1]}: {v.split('.')[0]}.")

print("\nInternal asymmetries INSIDE the slokas (same lordships, opposite verdict):")
# Taurus/Venus 1+6 malefic vs Scorpio/Mars 1+6 neutral.
check("Taurus/Venus and Scorpio/Mars own the identical pair (1st, 6th)",
      houses_owned("venus", TAU) == (1, 6) == houses_owned("mars", SCO))
check("both have their moolatrikona in the 6th",
      moolatrikona_house("venus", TAU) == 6 == moolatrikona_house("mars", SCO))
check("yet the verses say malefic (Taurus/Venus) vs neutral (Scorpio/Mars)",
      functional_nature("venus", TAU)["nature"] == "malefic"
      and functional_nature("mars", SCO)["nature"] == "neutral")
check("the derivation refuses to pick a side — 'mixed' for both",
      classify_by_lordship("venus", TAU)["nature"] == "mixed"
      and classify_by_lordship("mars", SCO)["nature"] == "mixed")
# Aries/Mars 1+8 vs Libra/Venus 1+8.
check("Aries/Mars and Libra/Venus own the identical pair (1st, 8th)",
      houses_owned("mars", ARI) == (1, 8) == houses_owned("venus", LIB))
check("yet: Mars only 'help[f]ul to (other) auspicious planets' "
      "(conditional) vs Venus flatly 'neutral'",
      functional_nature("mars", ARI)["nature"] == "conditional"
      and functional_nature("venus", LIB)["nature"] == "neutral")
check("all three asymmetries are documented",
      len(INTERNAL_ASYMMETRIES) == 3, str(sorted(INTERNAL_ASYMMETRIES)))


print("\n=== ch.34 vv.8-10 — natural benefics and malefics ===")
check("Jupiter and Venus are benefics", natural_nature("jupiter") == "benefic"
      and natural_nature("venus") == "benefic")
check("Sun, Saturn, Mars are malefics",
      all(natural_nature(g) == "malefic" for g in ("sun", "saturn", "mars")))
check("full Moon benefic, weak Moon malefic",
      natural_nature("moon", moon_waxing=True) == "benefic"
      and natural_nature("moon", moon_waxing=False) == "malefic")
check("Mercury alone is neutral", natural_nature("mercury") == "neutral")
check("Mercury with a malefic turns malefic",
      natural_nature("mercury", mercury_with_malefic=True) == "malefic")
check("Mercury with a benefic turns benefic",
      natural_nature("mercury", mercury_with_malefic=False) == "benefic")
check("nodes stay unclassified (v.16)",
      natural_nature("rahu") == "unclassified")


print("\n=== BPHS ch.44 — MARAKA ===")
# v.2: "the 3rd and 8th are the two houses of longevity. The houses related to
#  death are the 12th from each of these, i.e. the 2nd and 7th."
check("longevity houses are the 3rd and 8th", LONGEVITY_HOUSES == (3, 8))
check("2nd is DERIVED as the 12th from the 3rd", ((3 - 1 + 11) % 12) + 1 == 2)
check("7th is DERIVED as the 12th from the 8th", ((8 - 1 + 11) % 12) + 1 == 7)
check("maraka houses are the 2nd and 7th", MARAKA_HOUSES == (2, 7))
# v.3 + note: "the 2nd is a powerful Maraka house (as against the 7th) ... For
#  the 2nd house acquires an additional qualification of being in the 7th from
#  the 8th house."
check("v.3: the 2nd is the stronger maraka", MARAKA_STRONGEST == 2)
check("note: the 2nd is also the 7th from the 8th", ((2 - 8) % 12) + 1 == 7)

mh = maraka_houses(ARI)
check("Aries lagna maraka houses: 2nd = Vrishabha (Venus), 7th = Tula (Venus)",
      mh[2]["lord"] == "venus" and mh[7]["lord"] == "venus",
      f"{mh[2]['lord']}/{mh[7]['lord']}")
check("...hence ch.34 vv.19-22 'Venus is a direct (or independent) killer'",
      functional_nature("venus", ARI)["maraka"] == "primary"
      and functional_nature("venus", ARI)["maraka_source"] == "sloka")
check("Aries: Venus lords BOTH maraka houses",
      maraka_lords(ARI)["venus"] == [2, 7])

# ch.34 note to vv.23-24: "Mars is a killer for he owns the 7th and 12th."
check("Taurus lagna: Mars owns the 7th (a maraka house) and the 12th",
      houses_owned("mars", TAU) == (7, 12), str(houses_owned("mars", TAU)))
check("Taurus/Mars is a maraka per ch.34 vv.23-24",
      functional_nature("mars", TAU)["maraka"] == "primary")
# ch.34 note to vv.41-42: "The Sun is termed as a killer as he rules the 7th."
check("Aquarius lagna: the Sun owns the 7th -> maraka",
      houses_owned("sun", AQU) == (7,)
      and functional_nature("sun", AQU)["maraka"] == "primary")
# ch.34 note to vv.29-30: "(Saturn plays a similar role for Leo ascendant
#  owning the 7th in Moolatrikona)."
check("Leo lagna: Saturn owns the 7th, and it is his moolatrikona",
      7 in houses_owned("saturn", LEO) and moolatrikona_house("saturn", LEO) == 7)
check("Leo/Saturn is a maraka per ch.34 vv.29-30",
      functional_nature("saturn", LEO)["maraka"] == "conditional")
# ch.34 note to vv.37-38: "Saturn is straightaway a killer, ruling the 2nd and
#  the 3rd."
check("Sagittarius lagna: Saturn owns the 2nd and 3rd",
      houses_owned("saturn", SAG) == (2, 3), str(houses_owned("saturn", SAG)))
check("Sagittarius/Saturn is a primary maraka ('Saturn is a killer')",
      functional_nature("saturn", SAG)["maraka"] == "primary")
# ch.34 note to vv.43-44: Venus "owns the 8th house" -> maraka, NOTE only.
check("Pisces/Venus maraka comes from a NOTE, not the sloka",
      functional_nature("venus", PIS)["maraka_source"] == "note",
      str(functional_nature("venus", PIS)["maraka_source"]))
check("Pisces/Mars is a maraka but is exempted from killing independently",
      functional_nature("mars", PIS)["maraka"] == "conditional")

print("\nch.44 vv.3-5 applied to a chart (Aries lagna):")
positions = {
    "sun": TAU,       # 2nd house
    "moon": CAN,      # 4th
    "mars": VIR,      # 6th
    "mercury": TAU,   # 2nd — with Venus, the maraka lord
    "jupiter": SAG,   # 9th
    "venus": TAU,     # 2nd — 2nd lord, in the 2nd
    "saturn": LIB,    # 7th
    "rahu": SCO,      # 8th
    "ketu": TAU,      # 2nd
}
a = maraka_analysis(ARI, positions, moon_waxing=True, saturn_ill_disposed=True)
lordship = {d["graha"] for d in a["by_lordship"]}
check("by lordship: Venus (2nd AND 7th lord)", lordship == {"venus"}, str(lordship))
occupants = {d["graha"] for d in a["malefics_in_maraka_houses"]}
check("malefics IN the maraka houses: Sun (2nd) and Saturn (7th)",
      occupants == {"sun", "saturn"}, str(occupants))
withlords = {d["graha"] for d in a["malefics_with_maraka_lords"]}
check("malefics conjoined the maraka lord Venus: the Sun",
      withlords == {"sun"}, str(withlords))
check("Mercury alone is NOT counted (v.8-10: Mercury is neutral)",
      "mercury" not in occupants | withlords)
check("v.9: ill-disposed Saturn related to a maraka kills FIRST",
      a["saturn_precedence"] is not None
      and a["saturn_precedence"]["precedence"] == "first")
check("v.9 does not fire when Saturn is well-disposed",
      maraka_analysis(ARI, positions, saturn_ill_disposed=False)["saturn_precedence"] is None)
check("vv.6-7 secondary killers reported separately: 8th and 12th lords",
      a["secondary"]["eighth_lord"] == "mars"
      and a["secondary"]["twelfth_lord"] == "jupiter",
      f"{a['secondary']['eighth_lord']}/{a['secondary']['twelfth_lord']}")
check("v.8 antardasa rule is carried, not applied silently",
      "will not cause death in the" in a["antardasa_rule"]["quote"])
check("a benefic occupying a maraka house is NOT a maraka "
      "(note: 'a benefic will not be so')",
      "jupiter" not in occupants)

print("\nch.44 vv.22-24 — the nodes as marakas:")
nodemap = {d["graha"]: d for d in a["nodes"]}
check("Rahu in the 8th qualifies", "rahu" in nodemap, str(sorted(nodemap)))
check("Ketu in the 2nd qualifies — but only by the NOTE",
      "ketu" in nodemap and "note" in nodemap["ketu"]["sources"],
      str(nodemap.get("ketu", {}).get("sources")))
check("Rahu is a primary maraka for Makara and Vrishchika lagnas",
      set(RAHU_PRIMARY_MARAKA_LAGNAS) == {CAP, SCO})
cap = maraka_analysis(CAP, {"rahu": (CAP + 6) % 12}, )
check("Capricorn lagna, Rahu in the 7th -> maraka named for this lagna",
      any("primary maraka for this lagna" in r
          for d in cap["nodes"] for r in d["reasons"]))
check("a node in the 9th is NOT a maraka (note: 3rd, 9th, 5th, 11th)",
      maraka_analysis(ARI, {"rahu": (ARI + 8) % 12})["nodes"] == [])

print("\n...and when the two note-sentences COLLIDE, the loser is reported, "
      "not dropped:")
# The note says both "They will not be Marakas if they are in the 3rd, 9th,
# 5th and llth houses" AND "lf a node joins a Maraka planet ... it will act as
# a Maraka" - without saying which wins. This module gives the exclusion
# precedence and surfaces the suppressed qualification.
# Mesha lagna: Venus lords both maraka houses; put Venus and Rahu together in
# Kumbha, the 11th - an EXCLUDED house that nonetheless qualifies.
coll = maraka_analysis(ARI, {"venus": AQU, "rahu": AQU})
check("Mesha, Rahu conjoined the maraka lord Venus but in the 11th: "
      "not returned as a maraka",
      [d["graha"] for d in coll["nodes"]] == [], str(coll["nodes"]))
sup = {d["graha"]: d for d in coll["nodes_suppressed"]}
check("...but it IS returned under nodes_suppressed, with its reason intact",
      "rahu" in sup
      and any("conjoined the maraka lord venus" in r for r in sup["rahu"]["reasons"]),
      str(sup.get("rahu", {}).get("reasons")))
check("...and names the sentence that suppressed it",
      "will not be Marakas" in sup["rahu"]["suppressed_by"])
check("...and carries the precedence flag saying the choice is the module's",
      sup["rahu"]["precedence_flag"] == NODE_EXCLUSION_PRECEDENCE)
# Makara: the sloka names Rahu a PRIMARY maraka for this lagna outright, yet
# the 3rd is an excluded house. Same collision, higher stakes.
cap3 = maraka_analysis(CAP, {"rahu": (CAP + 2) % 12})
check("Makara, Rahu in the 3rd: the sloka's 'primary maraka for this lagna' "
      "is suppressed by the note's house exclusion",
      cap3["nodes"] == []
      and any("primary maraka for this lagna" in r
              for d in cap3["nodes_suppressed"] for r in d["reasons"]),
      str(cap3["nodes_suppressed"]))
check("the analysis carries the precedence choice at top level too",
      coll["node_exclusion_precedence"] == NODE_EXCLUSION_PRECEDENCE)
check("vv.22-24's Rahu-in-6th/8th/12th DIFFICULTY clause is declared "
      "unimplemented, not silently omitted (it needs aspect data)",
      CH44_RAHU_DUSTHANA_GAP in coll["unimplemented"]
      and "aspected by or conjunct a bene[f]ic" in CH44_RAHU_DUSTHANA_GAP)

print("\nch.44 note to vv.6-7 — Santhanam's three grades (tagged as a NOTE):")
for h, want in ((2, "primary"), (7, "primary"), (8, "primary"), (3, "primary"),
                (12, "primary"), (6, "second_grade"), (11, "second_grade"),
                (1, "least"), (9, "least"), (10, "least")):
    check(f"the {h}th grades as {want}", maraka_grade(h) == want, maraka_grade(h))

print("\nEvery lagna's maraka lords derive from RASI_LORD, never typed:")
for lg in range(12):
    ml = maraka_lords(lg)
    second = maraka_houses(lg)[2]["lord"]
    seventh = maraka_houses(lg)[7]["lord"]
    check(f"{S[lg]:<10} 2nd lord {second:<8} 7th lord {seventh:<8}",
          second in ml and seventh in ml)
check("Aries and Libra are the two lagnas where ONE graha lords both "
      "maraka houses (Venus and Mars respectively)",
      sorted(lg for lg in range(12)
             if any(len(h) == 2 for h in maraka_lords(lg).values())) == [ARI, LIB])


print("\nlagna_profile() — the assembled view, no silent substitution:")
prof = lagna_profile(GEM)
by = {r["graha"]: r for r in prof["grahas"]}
check("all 9 grahas present", len(prof["grahas"]) == 9)
check("Gemini/Mercury shows nature=None but derived_nature='benefic'",
      by["mercury"]["nature"] is None
      and by["mercury"]["derived_nature"] == "benefic",
      str((by["mercury"]["nature"], by["mercury"]["derived_nature"])))
check("...and is labelled 'no_text_verdict', not 'exact'",
      by["mercury"]["agreement"] == "no_text_verdict", by["mercury"]["agreement"])
check("Gemini has no yogakaraka by the general law",
      prof["yogakarakas"] == [], str(prof["yogakarakas"]))
check("Libra's yogakaraka is Saturn",
      lagna_profile(LIB)["yogakarakas"] == ["saturn"])
check("every graha row carries its citation",
      all(r["citation"] for r in prof["grahas"]))
check("no exception for any lagna x graha",
      all(lagna_profile(lg) for lg in range(12)))


print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
sys.exit(1 if fails else 0)
