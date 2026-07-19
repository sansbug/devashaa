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

---

# What BPHS does and does not contain

A systematic audit of both Santhanam volumes (1,034 pages), twelve doctrines,
each claim independently re-checked against the text by a second reader. This
section exists so that a deliberate omission is never mistaken for an oversight
and "fixed" by someone importing popular astrology.

## Absent from BPHS entirely — do NOT implement without an outside citation

- **Per-nakṣatra character.** No gaṇa (deva/manuṣya/rākṣasa), no yoni, no nāḍī,
  no varṇa, no dhruva/chara/ugra classification, no per-nakṣatra symbol, śakti
  or result. Zero hits across both volumes under every spelling. Vol I **ch.3
  v.7** is Parāśara declining the topic outright: *"Details (of astronomical
  nature) of stars be understood by general rules while I narrate to you about
  the effects of planets and signs."* Nakṣatras in BPHS are for daśā, for D9,
  and for identification — not for character. Our UI says so.
  → Would need Varāhamihira's *Bṛhat Saṁhitā*; gaṇa/yoni/nāḍī are Muhūrta
  literature (*Muhūrta Chintāmaṇi*), not Horā.
- **Vargottama.** The word occurs four times, never with a defining śloka. The
  "same rāśi in D1 and D9" definition exists only in a Santhanam note (Vol I pdf
  383) which is itself self-contradictory. Ch.36 vv.38-39 uses "Vargothama" as a
  *dignity name* for a different concept entirely (ch.6's Uttama, 3 good vargas).
  → If shown, must be labelled as the translator's note, not doctrine.
- **Viparīta Rāja Yoga** (Santhanam imports it openly from *Phaladīpikā*),
  **Nīcha Bhaṅga** (word appears once, no rules), the popular 2nd/11th-lord
  Dhana yoga, **Kāla Sarpa**, **Sade Sati**, and the entire sphuṭa family
  (Trisphuṭa, Bīja/Kṣetra, Yogi/Avayogi, Sahams — zero occurrences).

**Reverse correction:** *Kuja/Maṅgala doṣa* **is** BPHS — Vol II **ch.80 v.47**
as śloka (Mars in 12/4/7/8 from lagna, unaspected by a benefic), with explicit
cancellation in vv.48-49. Only the name "Mangalik" is Santhanam's.

## Present but blocked — the constants this printing does not supply

- **Seeghrocha (śīghrocca).** Ch.27 vv.24-25 instructs deducting a longitude
  "from the Seeghrocha of the planet" and **no value, table or formula is ever
  given** — the word appears three times in 1,034 pages. Santhanam's gloss
  "(or apogee)" is wrong; śīghrocca is the fast apex.
  **This blocks Cheṣṭā bala, hence Ṣaḍbala, hence Iṣṭa/Kaṣṭa phala for five of
  the seven grahas.** Sūrya and Chandra are computable (ch.28 vv.3-4).
- **No worked Ṣaḍbala example** exists in either volume — so unlike the vargas
  (ch.6) and daśās (Vol II ch.46), there is nothing to validate against.
- **Iṣṭa/Kaṣṭa Saptavargaja Śubhāṅka** (ch.28 vv.7-9, pdf 289) reads
  `60, 45, 30, 22, 15, t, 4, 2, 0` — the sixth value is a bare letter.
- **Dṛk bala assembly** (ch.27 v.19) is one sentence; "Dṛṣṭi Piṇḍa" appears
  exactly once in 1,034 pages and is never defined. **Yuddha bala** is listed as
  a sub-component of Kāla bala yet requires the finished Ṣaḍbala (v.20) —
  circular.
- **Combustion orbs** exist only in a Santhanam note (Vol I pdf 99), which he
  himself scopes to āyurdāya, and whose retrograde column is OCR-damaged.
  BPHS's own doctrine is the ch.7 vv.28-29 **rule-of-three proportion** across
  0-180° from Sūrya — that is what we implement; any orb table is out-of-BPHS.
- **Badhaka** (Vol II ch.50 vv.20-21) is defined only for the four movable
  rāśis, and only as a rāśi-daśā modifier — never as a natal classification,
  despite the contents page promising all three modalities.

## Why the strength number is Viṁśopaka, not Ṣaḍbala

Ṣaḍbala is the famous answer and, from this text, the wrong one: blocked on
Seeghrocha, resting on an undefined term for Dṛk bala, circular for Yuddha, and
with no worked example to check. **Viṁśopaka bala (ch.7 vv.17-27)** is the only
graha-level scalar here that is complete, self-interpreting (the verdict bands
are *in the śloka*), validatable (Venus = 16.8 at Vol I pdf 98) and buildable
from the 16 vargas already implemented.

## Bhāva madhya — a tension inside BPHS, not an OCR problem

There is **no cusp formula anywhere in either volume**, yet ch.27 vv.26-29
instructs deducting the descendant/nadir from *the bhāva* — meaningful only if a
bhāva is a longitude — and ch.28 vv.15-20 says outright *"If a bhava extends to
two Rasis, the rectification will be done as per both the lords."* Santhanam
asserts Śrīpati in his preface and silently uses cusps in worked examples.

**Our position stands: whole-sign for all rāśi-level judgement.** If bhāva bala
is ever built, compute a true MC and trisect the Asc-MC quadrants for *bala
purposes only*, keeping whole-sign everywhere else. Equal-houses-from-lagna is
not an acceptable substitute: it collapses the nadir/meridian distinction and
makes bhāva digbala a pure function of house number, so latitude and obliquity
drop out and every chart with the same lagna degree scores identically.

## Books that would close these gaps

1. **B. V. Raman, *Graha and Bhava Balas*** — closes Seeghrocha, the missing
   worked example, the Śubhāṅka table and the Dṛk bala assembly at once.
2. **Girish Chand Sharma's BPHS (Sagar, Devanāgarī + translation)** — repairs
   *this printing's* OCR damage against the Sanskrit rather than importing
   foreign doctrine.
3. **Varāhamihira, *Bṛhat Saṁhitā*** — the only honest route to nakṣatra
   character.

Also named by Santhanam himself in-text: *Horā Sāra* of Pṛthuyaśas (his own
translation, pp.183-187) for fuller bhāva significations.

---

## Vol II ch.47 vv.5-6 — the daśā verdict (`api/dasha_effects.py`) — BUILT

> "5-6. The effects are favourable if, at the commencernent [commencement] of the
> Dasa, the Dasa lord be in the Ascendant, in his sign of exaltation, in his own
> sign or in a friend's sign. The results are unfavourable if the Dasa lord be in
> the 6th, the 8th, or the l2th [12th] house, in his sign of debilitation or in
> an inimical .sign."
> — PDFPAGE 87, **mūla**, numbered in the verse stream

**Why a daśā may carry a verdict when a graha may not.** We refuse an uncited
good/bad score on a GRAHA because BPHS supplies seven overlapping judgements and
never combines them. That objection does not apply here: Parāśara states a
*named* verdict and names the inputs that drive it, and every one of those
inputs is something this engine already computes. Mined from ch.47-65 by ten
agents, each adversarially audited; this verse drew no challenge from any of the
eight verifiers who examined it.

### It is NOT a heatmap, and the text is why

- **No middle band.** "Medium effects" occurs **exactly once** in the 265-page
  effects section (ch.52 vv.1-3) and is scoped to a single cell — the Sun's
  antardaśā within the Sun's own daśā. No carrier clause generalises it, and all
  eight remaining antardaśā chapters open with two branches and no residual.
  A placement matching neither branch therefore has **no stated verdict**. That
  is `not_stated`, *not* "medium" — filling it as medium is the uncited score in
  a new costume.
- **No rank.** "Extremely favourable" and "extremely beneficial" each occur once,
  both describing the same kendra/trikoṇa configuration. Two hapax intensifiers
  are not a scale.
- **No combination rule.** Nothing states what happens when a favourable and an
  adverse condition both fire (exalted *and* in the 8th). That case ships as
  `contested` and is left unarbitrated. The only combination rule anywhere in
  the volume sits under "Notes :" — Santhanam, not Parāśara.
- **Polarity words attach to a minority of branches** across ch.52-60 (five
  explicit valence labels in ch.54's 76 verses; four in ch.57's fourteen pages),
  so per-antardaśā shading is NOT derived from whether the listed outcomes sound
  pleasant.
- **Remedy-presence is not a polarity marker.** Remedies appear in 8 of 9
  sub-sections and sit *after both branches*. Wiring them as an "evil" flag
  would paint śloka-labelled beneficial branches as adverse.

### Deliberate limits in our implementation

- **Read from the lord's NATAL placement.** The verse says "at the commencement
  of the Dasa"; BPHS gives no transit machinery in these chapters. Flagged in
  every payload rather than assumed silently.
- **The nodes are evaluated partially.** Rāhu and Ketu own no rāśi and have no
  dignity (ch.3 v.50), so only the two HOUSE conditions are evaluable for them.
  Stated in the payload rather than silently skipped.
- **Mūlatrikoṇa is not one of the six conditions** and is not treated as
  own-sign. Candra is the only graha whose mūlatrikoṇa is not her own sign
  (Vṛṣabha belongs to Śukra) — and since that sign is also her exaltation, no
  verdict ever actually turns on the distinction.
- **Viṁśopaka is NOT used to colour a daśā**, though it is the one numeric
  graded quantity this project owns and would produce exactly the smooth ramp a
  heatmap wants. ch.47 v.3 says results follow the lord's "strength" but never
  names a bala, and the daśā chapters never cite ch.7. Mapping one onto the
  other would be a project decision wearing a citation.
- **ch.34 is NOT used either.** ch.34 classifies *grahas*; ch.48 classifies
  *daśās by lordship*, and they disagree — Santhanam flags the conflict himself
  (PDFPAGE 102, a note). Merging them fabricates an agreement the book denies.

**Not yet built:** ch.48 vv.1-8 (a second, per-house-lordship verdict axis at
mahādaśā level, all twelve lordships), the 9×9 antardaśā matrix of ch.52-60, and
bhāva-from-the-daśā-lord — the workhorse frame of those chapters, stated ~50
times, and the single biggest gap in the current engine.

---

## Vol II ch.52-60 — the 81-cell antardaśā matrix (`api/antardasa.py`) — BUILT

Nine chapters, one per mahādaśā lord, each with nine sub-sections: 81 cells and
**559 conditions**, mined by nine agents and adversarially verified.
`api/antardasa_rules.py` is GENERATED from that extraction, never retyped.

### It is a CONDITION-FIRING engine, not a verdict engine

Two censuses over the corpus forced this, and neither was a judgement call.

**FRAMES.** 326 conditions reference a house:

| frame | count | share |
|---|---:|---:|
| from the lagna | 111 | 34% |
| **from the daśā lord** | 107 | 33% |
| from the Moon | 1 | 0.3% |
| **UNSTATED** | **107** | **33%** |

Two thirds are computable, so refusing to compute would discard most of the
corpus. But **one house condition in three names no reference frame at all**,
and that third is adversarially placed: it clusters on the *opening
kendra/trikoṇa branch* of a cell — the branch a real chart most often lands on.
Roughly 25-30 of the 81 cells have their headline favourable branch
unevaluable, and ch.54's entire Mars-in-Mars cell is frameless, which is the
first cell any engine reaches.

So unframed conditions are returned **unavailable and counted**, never omitted.
An engine that quietly skips them reports "nothing fires" on charts where BPHS
does state something — it simply does not say from where. **No default frame.**
Adjacency supplies none either: ch.55's Mercury vv.36-38 sits immediately after
a verse glossed "from the lord of the Dasa" and its Moon vv.68-70 immediately
before one.

**POLARITY.** Only about **one branch in five** carries a valence word, and the
labels are skewed adverse and clustered — ch.55 has two in 83 verses, ch.57 has
four in 82. More decisively, the extraction does not record whether a valence
word governs the whole branch ("will be the **evil** effects") or merely names
one item in an outcome list ("...**loss** of position, quarrels ... will be
realised"). The verifiers found most are the latter — one counted 19 of 24 in
its chapter. Treating a result-list noun as a verdict is keyword-driven
inference, the same uncited judgement refused for grahas.

**Therefore no antardaśā band is coloured.** Rail 2 of the timeline carries a
count of what fires and a ⊘ for what cannot be evaluated. The mahādaśā verdict
of ch.47 vv.5-6 still colours rail 1, because that verse genuinely states one.

### Deliberate refusals

- **No OCR salvage.** ch.56's "the 6th or the6rh" is *probably* 6/8/12 and
  ch.60's "8th, llth, 12th" *probably* 6/8/12, but a damaged numeral list
  poisons the whole condition rather than yielding its legible parts — parsing
  "8th, llth, 12th" as (8, 12) would silently drop the 11th and give a
  confident, partial, wrong answer.
- **No mahā × antar composite.** BPHS states no combination rule at any join.
- **No pratyantar layer.** ch.52-60 cover the antardaśā only; the tree has three
  levels because Viṁśottarī *arithmetic* does, not because the effects chapters
  follow it down. Rail 3 gets nothing.
- **No remedy engine.** Remedies sit *after* both branches, are not polarity
  markers, and at least two are the translator's own conjecture ("Though
  remedial measure is not mentioned, **we believe**…"). Stored and displayed,
  never recommended.
- **No death prediction.** Māraka clauses are stored and cited as text. The
  corpus is not even uniform on what the 2nd/7th clause yields — death in some
  cells, "physical distress" in many, "fear of fever" in others. Normalising
  those to death would be the most harmful thing this module could do.
- **No matrix filling by inheritance.** Every cell is independent.
  `maraka=None` means the cell *has* no death clause — ch.52's Jupiter cell is
  the only one in its chapter without one. Absent is not empty.
