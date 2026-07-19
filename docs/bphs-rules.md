# BPHS calculation rules — as implemented

Source: *Brihat Parasara Hora Sastra*, Maharshi Parasara, English translation &
commentary by **R. Santhanam**, Ranjan Publications, New Delhi. **Volume I**
(chapters 1–45).

Every rule below is traced to its śloka. Where Santhanam's commentary ("Notes")
adds or qualifies the śloka, that is called out — the commentary is his, not
Parāśara's, and we should be able to tell them apart later.

> The source PDF is a **scan with an OCR text layer**. The prose is legible; the
> speculum tables are OCR noise and were **not** used. Every rule here comes from
> the prose śloka + Notes, and each was checked against the worked example
> Santhanam supplies. The tables in our code are regenerated from the rules, not
> transcribed from the book.

---

## Chapter 6 — The sixteen divisions of a sign (Ṣoḍaśavarga)

**vv. 2–4 — the sixteen names:** Rāśi, Horā, Drekkāṇa, Chaturthāṁśa,
Saptāṁśa, Navāṁśa, Daśāṁśa, Dvādaśāṁśa, Ṣoḍaśāṁśa, Viṁśāṁśa,
Chaturviṁśāṁśa, Saptaviṁśāṁśa, Triṁśāṁśa, Khavedāṁśa, Akṣavedāṁśa,
Ṣaṣṭiāṁśa.

Sign classes used below (0 = Aries … 11 = Pisces):

| class | signs |
|---|---|
| movable (chara) | Aries, Cancer, Libra, Capricorn |
| fixed (sthira) | Taurus, Leo, Scorpio, Aquarius |
| dual (dvisvabhāva) | Gemini, Virgo, Sagittarius, Pisces |
| odd | Aries, Gemini, Leo, Libra, Sagittarius, Aquarius |
| even | Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces |
| fiery | Aries, Leo, Sagittarius |
| earthy | Taurus, Virgo, Capricorn |
| airy | Gemini, Libra, Aquarius |
| watery | Cancer, Scorpio, Pisces |

| Varga | Śloka | Arc | Rule |
|---|---|---|---|
| **D1 Rāśi** | v.5 | 30° | The sign itself. |
| **D2 Horā** | vv.5–6 | 15° | Odd sign: 1st half = Sun's horā, 2nd half = Moon's horā. Even sign: reversed. |
| **D3 Drekkāṇa** | vv.7–8 | 10° | The 1st, 5th and 9th signs from the sign → offsets 0, 4, 8. |
| **D4 Chaturthāṁśa** | v.9 | 7°30′ | The four angles from the sign → offsets 0, 3, 6, 9. |
| **D7 Saptāṁśa** | vv.10–11 | 4°17′08.57″ | Odd: count from the same sign. Even: from the 7th thereof (offset +6). |
| **D9 Navāṁśa** | v.12 | 3°20′ | Movable: from itself. Fixed: from the 9th (+8). Dual: from the 5th (+4). |
| **D10 Daśāṁśa** | vv.13–14 | 3° | Odd: from the same sign. Even: from the 9th (+8). |
| **D12 Dvādaśāṁśa** | v.15 | 2°30′ | Always from the same sign. |
| **D16 Ṣoḍaśāṁśa** | v.16 | 1°52′30″ | Movable → from Aries. Fixed → from Leo. Dual → from Sagittarius. |
| **D20 Viṁśāṁśa** | vv.17–21 | 1°30′ | Movable → Aries. Fixed → **Sagittarius**. Dual → **Leo**. |
| **D24 Siddhāṁśa** | vv.22–23 | 1°15′ | Odd → from Leo. Even → from Cancer. |
| **D27 Bhāṁśa** | vv.24–26 | 1°06′40″ | Fiery → Aries. Earthy → Cancer. Airy → Libra. Watery → Capricorn. |
| **D30 Triṁśāṁśa** | vv.27–28 | *irregular* | See below — **not** equal parts. |
| **D40 Khavedāṁśa** | vv.29–30 | 45′ | Odd → from Aries. Even → from Libra. |
| **D45 Akṣavedāṁśa** | vv.31–32 | 40′ | Movable → Aries. Fixed → Leo. Dual → Sagittarius. |
| **D60 Ṣaṣṭiāṁśa** | vv.33–41 | 30′ | See below — computed, not tabulated. |

### Worked examples used as tests (Santhanam's own, Ch. 6 Notes)

- **D9**: "the Navāṁśas of Aries are counted from Aries itself; from Capricorn
  for Taurus and from Libra for Gemini." → Aries (movable) +0; Taurus (fixed)
  +8 = Capricorn; Gemini (dual) +4 = Libra. ✓
- **D7**: "For Aries … Aries, Taurus, Gemini etc., while for Taurus these are
  Scorpio, Sagittarius, Capricorn etc." → Taurus (even) +6 = Scorpio. ✓
- **D60**: "Venus … in Capricorn 13°25′ … 13°25′ × 2 = 26°50′. The degrees i.e.
  26 … divided by 12. The remainder is 2 … increased by 1. Thus we get 3. Count
  3 signs from Capricorn. The resulting Ṣaṣṭiāṁśa position is **Pisces**, whose
  lord is Jupiter." ✓

### D30 Triṁśāṁśa (vv. 27–28) — irregular

Unequal spans; the resulting sign is the ruling planet's own sign. The luminaries
rule no triṁśāṁśa, so **no planet is ever in Cancer or Leo in D30**.

| Odd sign | span | lord | → sign |
|---|---|---|---|
| first | 5° | Mars | Aries |
| next | 5° | Saturn | Aquarius |
| next | 8° | Jupiter | Sagittarius |
| next | 7° | Mercury | Gemini |
| next | 5° | Venus | Libra |

For an **even** sign "the quantum of Triṁśāṁśa, planetary lordship and deities
get reversed" → 5° Venus (Taurus), 7° Mercury (Virgo), 8° Jupiter (Pisces),
5° Saturn (Capricorn), 5° Mars (Scorpio).

Note the odd-sign lords all land in odd signs and the even-sign lords all in even
signs — a useful internal check.

### D60 Ṣaṣṭiāṁśa (v. 33) — computed

> "ignore the sign position of a planet and take the degrees etc. it traversed in
> that sign. Multiply that figure by 2 and divide the degrees by 12. Add 1 to the
> remainder which will indicate the sign…"

`offset = floor(degrees_in_sign × 2) mod 12` → result = sign + offset.
(The "add 1" is inclusive counting from the sign itself, i.e. offset 0 = the sign
itself. Verified against the Capricorn 13°25′ → Pisces example above.)

### D2 Horā — a note on degeneracy

Parāśara's horā yields only *Sun's horā* or *Moon's horā*, conventionally mapped
to **Leo** and **Cancer**. So in D2 every graha sits in one of two signs. This is
the Parāśari horā as given; other schemes (Jaimini etc.) are **not** in this text.

---

## Not specified by BPHS — our choice, must be recorded

- **Ayanāṁśa.** BPHS defines no numeric ayanāṁśa; it is a modern computational
  input. Default: **Lahiri / Chitrapakṣa** (Indian government standard).
- **Mean vs true Rāhu.** Not resolved computationally by the text.

## Viṁśottarī daśā — VALIDATED against BPHS Vol II, Chapter 46

Source: **BPHS Vol II, R. Santhanam**, `C:\Users\sans2\Downloads\BPHS - 2
RSanthanam.pdf` (scan + OCR; prose legible, tables noisy — same as Vol I).
Chapter 46 "Daśās (Periods of Planets)" begins ~PDF p.17 (book p.507).

Every component of `vimshottari.py` is confirmed against the text:

- **Lord order & years** — ch.46 **v.15**: "periods of Daśās of the Sun, Moon,
  Mars, Rāhu, Jupiter, Saturn, Mercury, Ketu, Venus are 6,10,7,18,16,19,17,7,20."
  Engine matches all nine exactly (sum 120). ✓
- **Nakṣatra → lord** — ch.46 **vv.12-14** + Table of Daśās: counted from
  Kṛttikā the lords are Sun, Moon, Mars, Rāhu, Jupiter, Saturn, Mercury, Ketu,
  Venus. Engine's `(nakṣatra_number − 1) mod 9` reproduces all 27 assignments
  in the book's table exactly. ✓
- **Balance at birth** — ch.46 **v.16**: expired = `dasa_years × (expired_stay /
  total_stay)`; balance = `dasa_years − expired`. Engine's
  `dasa_years × (1 − fraction)` is identical. ✓
- **Method note** (Santhanam, p.18-19): the *older* method uses Pañcāṅga
  ghaṭi/pala (time of the Moon's stay in the nakṣatra); "modern researchers"
  use the **Moon's longitude** (arc fraction). We use the longitude method —
  the one Santhanam endorses and that Lahiri's ephemeris tables use.

### OPEN — year length for projecting daśā-years to calendar dates

BPHS does **not** state the days-per-year for converting daśā years to dates.
But its own worked example pins it down better than I expected:

> ch.46 example (p.20-23): Moon at sidereal Sagittarius 13°00' → Mūla pada 4 →
> Ketu, balance **"2 months 3 days"**.

That balance is `7 × (1 − 0.975) = 0.175` years. Converting:
- **360-day year** (30-day months): 0.175 × 360 = **63.0 d = 2m 3d** ✓ matches BPHS
- 365.25-day year (our current default): 0.175 × 365.25 = 63.9 d = 2m 4d
- 365.2422 tropical: 63.9 d = 2m 4d

So **BPHS's own worked example uses the 360-day sāvana year**, not the 365.25
Julian year I defaulted to (which came from Jagannātha Hora). This is a real
doctrinal fork — flagged to the user; default may change to 360.

### Aṣṭottarī daśā — captured for later (ch.46 vv.17-22, PDF p.23-24)

- **Applicability** (v.17-20): recommended "when Rāhu is in a kendra or trikoṇa
  **from the lord of the Ascendant**, but not in the Lagna itself." (First real
  daśā-applicability rule from the text.)
- Reckoning starts 4 nakṣatras from Ārdrā; **8 lords only, Ketu excluded**.
- Durations (Sun, Moon, Mars, Mercury, Saturn, Jupiter, Rāhu, Venus):
  6, 15, 8, 17, 10, 19, 12, 21 — **sum 108** (hence "Aṣṭottarī").

## Other nakṣatra ('udu') daśās — BUILT & example-validated (ch.46)

`dashas.py` generalizes the Viṁśottarī machinery (same balance = `lord_years ×
(1 − fraction)`, same proportional nesting) to the whole nakṣatra-daśā family.
Each system differs only in its lord list / year-total and the reference nakṣatra
the lord-count starts from: `lord_index = ((janma − ref) mod 27) mod N`.

Each system stores its BPHS worked example; `validated_systems()` ships only
those that reproduce it, and `/api/dasha` refuses the rest.

| Daśā | Total | Lords | Ref nak | Citation | Example |
|---|---|---|---|---|---|
| Viṁśottarī | 120 | 9 | Aśvinī | vv.12-16 | Mṛgaśira→Mars ✓ |
| Ṣoḍaśottarī | 116 | 8 | Puṣya | vv.24-26 | Rohiṇī→Venus ✓ (balance 15y2m3d to the day) |
| Dvādaśottarī | 112 | 8 | Revatī | vv.27-28 | (none) |
| Pañcottarī | 105 | 7 | Anurādhā | vv.29-31 | (none) |
| Śatābdikā | 100 | 7 | Revatī | vv.32-34 | Mṛgaśira→Mars ✓ |
| Dvisaptati-sama | 72 | 8 | Mūla | vv.37-39 | (none) |
| Ṣaṭtriṁśat-sama | 36 | 8 | Śravaṇa | vv.42-43 | (none) |

**Chaturaśīti-sama (84, ref Svātī, vv.35-36) — NOT shipped.** Its stated example
(Mṛgaśira→Mars) does not reproduce with the count convention that validates all
the others (gives Mercury). Either the OCR'd example or its reference nakṣatra is
off; excluded until the book's own arithmetic is re-checked.

## Aṣṭottarī daśā — BUILT (group method), ch.46 vv.17-23

`build_ashtottari` in `dashas.py`. Not a udu daśā: each lord rules a CONSECUTIVE
group and it uses 28 nakṣatras (Abhijit carved out), so it has its own path.

- **Lords / years** (v.15-analogue in vv.17-20): Sun 6, Moon 15, Mars 8, Mercury
  17, Saturn 10, Jupiter 19, Rāhu 12, Venus 21 = **108**; 8 lords, **no Ketu**.
- **Groups from Ārdrā**, sizes 4,3,4,3,4,3,4,3 (malefics rule 4, benefics 3 —
  v.21). Venus rules Kṛttikā/Rohiṇī/Mṛgaśira; Saturn rules P.Aṣāḍhā/U.Aṣāḍhā/
  Abhijit/Śravaṇa.
- **Abhijit** = 4th pāda of U.Aṣāḍhā (276°40'–280°) + first 1/15 of Śravaṇa
  (280°–280°53'20"); handled by longitude, so U.Aṣāḍhā (Aṣṭottarī span 10°) and
  Śravaṇa are shortened accordingly.
- **Balance** (v.16-analogue, vv.21-22): `lord_years × (1 − (j + fraction)/k)`,
  j = slot in the lord's group, k = group size.

Validated against BPHS's own examples: Venus/Mṛgaśira start → **7y** (v.16 note);
Saturn/U.Aṣāḍhā 2nd pāda → **6y 2m 26d** vs the book's 6y 2m 25d (1-day rounding
of the ghaṭi/pala fraction). Abhijit → Saturn's 3rd slot.

**Not yet built:**
- **Shashtihayani** — also uses Abhijit; OCR of its year-counts is ambiguous.
- **Sign-based daśās**: Kālachakra (vv.52+, Savya/Apsavya chakras), Chara,
  Sthira, Chakra (10y/sign), Kāla (Sandhyā-based) — structurally different, need
  a rāśi-daśā engine.
- **Daśā effects / interpretation** (ch.47-65).

---

## Chapter 3 — Dignity (`api/dignity.py`) — BUILT & example-validated

### vv.49–50 Exaltation and debilitation

> "For the seven planets from the Sun on, the signs of exaltation are respectively
> Aries, Taurus, Capricorn, Virgo, Cancer, Pisces and Libra. The deepest exaltation
> degrees are respectively 10, 3, 28, 15, 5, 27 and 20 in those signs. And in the
> seventh sign from the said exaltation sign each planet has its own debilitation.
> The same degrees of deep exaltation apply to deep fall."

Debilitation is **derived** in code (`exaltation sign + 6`, same degree), never
typed out, so the two tables cannot drift apart.

**Rāhu and Ketu carry no dignity.** v.50's note says only that "there are
different views" on the nodes' exaltation. `dignity_of()` returns `None` for
them, and the UI states that absence is a finding rather than a gap.

### vv.51–54 Mūlatrikoṇa arcs

Sun Leo 0–20° · Mars Aries 0–12° · Mercury Virgo 15–20° · Jupiter Sagittarius
0–10° · Venus Libra 0–15° · Saturn Aquarius 0–20°.

Virgo is the one sign the text **partitions**: "the first 15 degrees are
exaltation zone, the next 5 degrees Moolatrikona and the last 10 degrees are own
house." So Mercury is *not* exalted throughout Virgo, and `EXALTATION_ARC`
encodes that as the only exception.

**⚠ Candra's arc is UNVERIFIED.** The śloka is OCR-damaged in our scan on the
line after the Sun's. The classical reading (Vṛṣabha 4°–30°) is used, flagged in
`MOOLATRIKONA_UNVERIFIED`, and the chart draws that bracket **dashed** so the
rendering never claims a confidence the source does not support.

### v.55 Natural relationships

Friends = lords of the 2nd, 4th, 5th, 8th, 9th and 12th from the graha's
mūlatrikoṇa, plus the lord of its exaltation sign; the rest are enemies;
friend-and-enemy at once resolves to neutral. Computed, not tabulated.
Validated against Santhanam's own worked examples in the ch.3 Notes: Saturn and
Venus both come out **neutral** to Mars.

### uccha bala

1.0 at the exact deep-exaltation point, 0.0 at the exact debilitation point,
linear across the 180° between. This is what the cell ruler's chevron encodes —
BPHS locates peak strength at a **point**, not across a whole sign.

---

## Chapter 92 (Vol II) — Gaṇḍānta — PARTIALLY BUILT

Parāśara names **three kinds** (v.1): Tithi, Nakṣatra and Lagna. All three are
measured in **ghaṭikās of TIME, never in degrees of arc**.

> v.3 "the last two ghatikas of Revti and first two [ghatikas] of Aswini, the last
> two ghatikas of Ashlesha and [fir]st two ghatikas of Makha and the last two
> g[h]atikas of [Jy]estha and first two ghatikas of Moola (total 4 ghatikas) are
> known as Nakshatra Gandanta."

> v.4 "The last half ghatika of Pisces and first half ghatika of Aries, the last
> half gha[tik]a of Cancer and first half ghatika of Leo, the last half ghatika of
> Scorpio and first half ghatika of Sagittarius, are known as Lagna Gandanta."

Both verses name the **same three junctions**, because those nakṣatras end
exactly on sign boundaries: Āśleṣā at 120°, Jyeṣṭhā at 240°, Revatī at 360°.
Three junctions only — **not** every sign boundary.

### The 3°20′ figure is NOT Parāśara's

It comes from Santhanam's *note* to Vol I ch.9 v.13 — "The last Navamsas of
Cancer, of Scorpio and of Pisces are called as Gandanta" — which he expressly
attributes to "**a host of authors**", i.e. later tradition. It also gives only
the water-sign half.

Two ghaṭikās is 48 minutes, in which Candra moves ≈ **0°26′**. The navāṁśa
reading is therefore roughly **eight times too wide**. We follow the śloka:
`nakshatra_gandanta()` derives the half-width from the Moon's *actual* speed on
the day, so it varies with her rate as the text's time-based definition
requires.

**Scope.** The three kinds are the three components of the birth *moment* —
tithi, birth nakṣatra (Candra), lagna. Parāśara never places an arbitrary graha
"in gaṇḍānta", so neither do we. Note also that Vol I ch.9 v.13 attaches a
condition Parāśara's own words require — "while the Moon and malefics occupy
angles from the ascendant" — so gaṇḍānta alone is not the ariṣṭa; only the
commentary makes it sufficient.

**Not built:**
- **Lagna-gaṇḍānta (v.4)** — needs the *ascendant's* rate of change (half a
  ghaṭikā of it), which varies sharply with latitude and rising sign. Not
  computed rather than approximated at 3°20′.
- **Tithi-gaṇḍānta (v.2)** — purely calendrical (last 2 ghaṭikās of a Pūrṇā
  tithi + first 2 of a Nandā); no zodiacal longitude, needs a pañcāṅga.
- **Abhukta Mūla (v.5)**, and the śānti chapters 93–94.

---

## Bhāva cusps — a standing decision, recorded before it is asked for

This engine is **whole-sign only**. No Śrīpati, no Placidus, no bhāva-chalita.
The cell ruler measures longitude *within a rāśi*; the moment unequal houses
ship, its legend ("a graha at 29° is wholly in its own house") becomes false.
If cusps are ever added they need their own frame, not a reinterpretation of
this one.
