# Devashaa — Traditional, Modern & Jaimini Rule Book

**Relationships of planets, nakṣatras, rāśis and padas, and their interactions.**

> **Read this first.** Everything in this document sits **outside** the BPHS core
> that the rest of devashaa is built on. Each block below is tagged with a
> provenance **tier**, and the tiers must never be blended in the UI or in prose:
>
> | Tier | What it is | How the site must label it |
> |------|-----------|----------------------------|
> | `traditional` | Classical facts the source books *tabulate* but did **not** invent (nakṣatra lord, deity, symbol, degree range, padas). Predate the books by ~1500 years (Bṛhat Saṁhitā / muhūrta tradition). | **"traditional — not BPHS"** |
> | `modern` | An individual modern author's interpretive *technique* or worked example. Copyrighted expression. | **"modern (author, page)"** |
> | `jaimini` | The Jaimini school's own machinery (chara kārakas, Chara Daśā). A *different school*, sign-based. | **"Jaimini — not Parāśara"** |
>
> **Nothing below is Parāśara / BPHS doctrine.** Do not present any of it as such.
> The BPHS-sourced material lives in `docs/bphs-rules.md` and stays the only tier
> the site may call "BPHS".

---

## 1. How this relates to the BPHS core (one paragraph)

Devashaa already computes, **from BPHS itself**, the pieces of the nakṣatra/rāśi/pada
layer that Parāśara actually states: each body's **nakṣatra** and its **Vimśottarī
lord** (`api/vedic.py`, driving all eight udu daśās), each nakṣatra's **presiding
deity** (`vedic.py` `NAKSHATRAS`, cited to *BPHS ch.6 vv.24–26* — the Bhāṁśa lords
are the presiding deities), and each **pada = one navāṁśa** (`PADA_ARC = 3°20'`, the
same span as a D9 division). Rāśi lordship, exaltation/debilitation, mūlatrikoṇa,
graha aspects and the pañcadhā relationship are likewise BPHS-core and already built
(`dignity.py`, `drishti.py`, `relationships.py`). **Everything in §2–§4 of this
document is a *separate* tier** the site must badge "traditional / not BPHS",
"modern", or "Jaimini" — never as Parāśara. In particular, the extra nakṣatra
attributes (symbol, gaṇa, yoni, nāḍī, etc.) are material on which **BPHS is silent
(ch.3 v.7)** — the app's own current label for this gap — so §2 fills that gap on an
explicitly **non-BPHS, traditional** footing, and §3's interpretive techniques are
one modern author's method, captured only as attributed pointers.

---

## 2. Nakṣatra attributes  ·  tier: `traditional` (NOT BPHS)

These are classical facts (nakṣatra → lord, deity, symbol, degree range, padas) that
the source books *tabulate* from the older Bṛhat-Saṁhitā / muhūrta standard. They are
**older than the books and not copyrightable as data**, so they are extracted in full.
This is exactly the material the site currently marks **"BPHS is silent (ch.3 v.7)"**;
the rows below fill that gap **on a `traditional` footing, not a BPHS one**.

### 2a. Verified rows 1–9 (Aśvinī → Āśleṣā)

Source: *Predicting Through Nakṣatras – Part I*, Saptarishis Publications (ed. Vidhan
Pandya). All **45 data cells (9 rows × 5 attributes)** were cross-checked against the
canonical Bṛhat-Saṁhitā / muhūrta standard: **zero data errors, zero corrections
needed.** The only OCR damage was in the header label row (a label artifact, no data
impact). The lord column doubles as the **Vimśottarī sequence** (position 1→9), which
*is* BPHS-core and matches — an independent confirmation the rows are clean.

| # | Nakṣatra | Range | Padas | Lord (Vimś.) | Deity | Symbol |
|---|----------|-------|-------|--------------|-------|--------|
| 1 | Aśvinī | 0°00'–13°20' Aries | 4 (all Aries) | Ketu | Aśvinī Kumāras | Horse's Head |
| 2 | Bharaṇī | 13°20'–26°40' Aries | 4 (all Aries) | Venus | Yama | Yoni (vulva) / Womb |
| 3 | Kṛttikā | 26°40' Ari – 10°00' Tau | 4 (1 Aries, 3 Taurus) | Sun | Agni | Knife / Blade / Razor |
| 4 | Rohiṇī | 10°00'–23°20' Taurus | 4 (all Taurus) | Moon | Prajāpati / Brahmā | Cart / Chariot |
| 5 | Mṛgaśira | 23°20' Tau – 6°40' Gem | 4 (2 Taurus, 2 Gemini) | Mars | Soma / Chandra | Deer's / Antelope's Head |
| 6 | Ārdrā | 6°40'–20°00' Gemini | 4 (all Gemini) | Rāhu | Rudra | Teardrop / Diamond / Human Head |
| 7 | Punarvasu | 20°00' Gem – 3°20' Can | 4 (3 Gemini, 1 Cancer) | Jupiter | Aditi | Bow & Quiver of Arrows |
| 8 | Puṣya | 3°20'–16°40' Cancer | 4 (all Cancer) | Saturn | Bṛhaspati | Cow's Udder / Lotus / Arrow |
| 9 | Āśleṣā | 16°40'–30°00' Cancer | 4 (all Cancer) | Mercury | Sarpas / Nāgas | Coiled Serpent |

**Caveats carried from verification (do not silently drop these):**

- **Bharaṇī "body part = lower part of feet"** is *not* one of the enumerated canonical
  attributes and **cannot be crisply confirmed**: the rāśi-based Kālapuruṣa puts Aries at
  the *head*, while some Nakṣatra-Puruṣa schemes put early nakṣatras at the feet. It was
  drawn from the author's technique prose, so tag it **`modern` / technique-derived, not
  a confirmed `traditional` fact.** Do not promote it.
- For these 9 nakṣatras the book states **nothing** for tattva, gaṇa, yoni-animal, nāḍī,
  varṇa, guṇa or gender. Those were **left blank** (the book omits them) — do not import.

### 2b. Rows 10–27 (Maghā → Revatī): **MISSING**

*Predicting Through Nakṣatras – Part I* covers **only the first 9 nakṣatras.** Rows
10–27 are entirely absent from that volume and **must be sourced elsewhere** before the
27-row table is complete. See §5 for the recommended cross-check source.

### 2c. Rāśi & pada attributes (supporting, `traditional`)

- **Pada = navāṁśa** is already BPHS-computed (§1); no new data needed. The pada-to-sign
  mapping in the table above (e.g. Kṛttikā = 1 Aries pada + 3 Taurus padas) is a direct
  consequence of the 13°20' span and is self-checking.
- **Rāśi attributes** (element, direction, movable/fixed/dual, gender, mode of rising)
  are tabulated as `traditional` facts in *K.N. Rao — Astrology Lessons, Part A*
  ("Useful Information About Rashis"). Most overlap the BPHS core already in the app;
  treat Rao's table as a **corroborating** `traditional` source, not a new authority.

---

## 3. Planet × Nakṣatra / Nakṣatra × Nakṣatra / Rāśi / Pada interactions
### tier: `modern` — attributed pointer index (summarised, NOT reproduced)

> **These are one modern author-group's interpretive techniques, not doctrine.** They
> are captured as **pointers only** — technique name, one-line neutral gist, author,
> page, computable? — with **no worked examples, no example-native names, dates or
> chart data** (all skipped per the provenance rules). The site must show them as
> *"modern technique — Predicting Through Nakṣatras Part I (Saptarishis, ed. V. Pandya),
> p.N"* and never blend them into the `traditional` table above or into BPHS.

**Source:** *Predicting Through Nakṣatras – Part I* (Saptarishis Publications; compiled
& edited by Vidhan Pandya with Nidhi Sharma Raj, from the Saptarishis Astrology research
groups). Modern, in-copyright. **46 numbered techniques across the first 9 nakṣatras.**

**Source-name note:** the intake brief called this "Sunil John's nakṣatra book," but the
file contains **no mention of Sunil John** — it is the Saptarishis/Pandya compilation.
Confirm the intended source before citing an author.

**Reading conventions for the index:** *Computable* = `yes` (a clean structural flag:
planet or house-lord in the nakṣatra), `partly` (needs an affliction / house-connection
judgment the engine can approximate), `no` (interpretive, or leans on **non-Parāśara
material** — flagged ⚠). Pages are the printed ToC page (±1 vs. the body heading).

### Aśvinī — travel / transport (lord Ketu)
| # | Gist | Computable |
|---|------|-----------|
| 1 | A planet or house-lord in Aśvinī adds a **travel/transport** theme to what that planet/lord signifies. | yes |
| 2 | A planet **aspecting** Aśvinī reads as a lesson urging self-improvement along that planet's significations. | partly |
| 3 | Aśvinī **afflicted** (occupant or lord) → prone to a **vehicle accident** if other factors concur. | partly |
| 4 | Key planets in Aśvinī can point to a vehicle accident **involving ≥3 people.** | yes |
| 5 | Aśvinī afflicted → chronically **fails to reach places on time** (missing train/flight/bus). | partly |
| 6 | Aśvinī's condition can make the native **instrumental in uniting or separating** other people (couples). | partly |

*(Pages: 1, 11, 16, 28, 35, 40.)*

### Bharaṇī — restraint, sudden reversal (lord Venus, deity Yama)
| # | Gist | Computable |
|---|------|-----------|
| 1 | A planet in Bharaṇī (by lordship/kāraka) marks that relative/matter for **disproportionate punishment / an assured reversal.** | yes |
| 2 | A house-lord in Bharaṇī → the relative signified is **secretive**, sometimes concealing an addiction. | yes |
| 3 | A planet in Bharaṇī can give the relative **ankle / lower-foot ailments**, esp. when afflicted. | partly |
| 4 | Mercury/Rāhu/Moon/Venus/Mars in Bharaṇī tied to 7th/8th/12th → **intense but short-lived affairs** & unwise partner choices. | partly |
| 5 | Any planet in Bharaṇī tends to deliver its results **suddenly.** | yes |
| 6 | A key planet in Bharaṇī → a **woman** (not necessarily a lover) who profoundly, unconventionally changes the native's life. | yes |
| 7 | Any planet in Bharaṇī gives a **major loss/reversal** in that planet's kārakatva or lordship (transformation via Yama's justice). | yes |

*(Pages: 43, 63, 78, 86, 91, 94, 97.)*

### Kṛttikā — cutting / splitting (lord Sun, deity Agni)
| # | Gist | Computable |
|---|------|-----------|
| 1 | Anything in Kṛttikā tends to **split into two** (division of family/property/opinion). | yes |
| 2 | A key planet (7L/8L/Venus/5L) in Kṛttikā → a **love affair where the partner rejects** the native, or a lover whose mind wanders. | partly |
| 3 | A focal planet (Sun/Moon/lagna-lord) in Kṛttikā → a **significant event at age 27.** | yes |
| 4 | 9L or Sun (from asc/Moon), also 5L or Jupiter, in Kṛttikā → **karmic payback between son and father.** | partly |

*(Pages: 105, 110, 113, 119.)*

### Rohiṇī — growth, attachment (lord Moon, deity Prajāpati/Brahmā)
| # | Gist | Computable |
|---|------|-----------|
| 1 | A key planet in Rohiṇī, afflicted → native is **blamed at least once for an act he did not commit.** | partly |
| 2 | ⚠ **Pluto or Neptune** in Rohiṇī → death-like situation / water problem at ages 38–50 or 65–75. **(non-Parāśara: outer planets.)** | no |
| 3 | Key planets in Rohiṇī → tendency to **compare the spouse with previous partners** (looks/habits/cooking). | partly |
| 4 | Key planets in Rohiṇī → tendency toward **incest-type relationships** (uncle/aunt/cousin). | partly |
| 5 | Key planets in Rohiṇī → **plagiarism / forgery** theme (as perpetrator, victim, or copyright/false-signature dispute). | partly |

*(Pages: 121, 126, 135, 136, 147.)*

### Mṛgaśira — searching, direction (lord Mars, deity Soma)
| # | Gist | Computable |
|---|------|-----------|
| 1 | Key planets in Mṛgaśira → the native's **children may find fortune late in life.** | partly |
| 2 | Key planets in Mṛgaśira → **friction with one's children**, esp. during their upbringing. | partly |
| 3 | Key planets in Mṛgaśira → involvement in **sports requiring chasing/running** (football, boxing). | partly |
| 4 | A planet in Mṛgaśira connected to the 6th house → that relative habitually has **left-over / junk food.** | partly |
| 5 | Relative signified by a Mṛgaśira planet has a **strong sense of direction/maps** if unafflicted; if afflicted, **always gets lost** / late. | partly |
| 6 | 5L in Mṛgaśira → a **division of property brings a grievance** (a child unhappy with their share/facing). | partly |
| 7 | ⚠ **Vāstu:** a Mṛgaśira planet afflicted (or Mars afflicted) → the **north-east (Īśānya) corner** of the house is afflicted. **(non-Parāśara: Vāstu.)** | no |

*(Pages: 157, 159, 164, 170, 177, 182, 182.)*

### Ārdrā — storms, animals, sacrifice (lord Rāhu, deity Rudra)
| # | Gist | Computable |
|---|------|-----------|
| 1 | A planet in Ārdrā → the relative it signifies has a strong link (love/hate/story) with **animals.** | partly |
| 2 | Key planet(s) in Ārdrā → a **self-sacrifice** theme (in life as in the "hero sacrifices himself" film trope). | partly |
| 3 | "**Storm**" theme — key planets in Ārdrā tied to upheaval / whistle-blowing / exposure (often via 10th house/lord or a 6th-house aspect). | partly |

*(Pages: 185, 196, 200.)*

### Punarvasu — return, renewal (lord Jupiter, deity Aditi)
| # | Gist | Computable |
|---|------|-----------|
| 1 | Key planets in Punarvasu (esp. **Rāhu**) → **fascination with technology** / tech-field work / constant gadget upgrading. | yes |
| 2 | Key planets in Punarvasu → **fortune & stability arrive only after much searching / repetition.** | partly |
| 3 | Key planets in Punarvasu → fixation on **healthy food / fitness**, later lapsing into junk food. | partly |
| 4 | When such a native cares for someone, they become the **mother/father figure** for that person. | partly |

*(Pages: 203, 217, 220, 222.)*

### Puṣya — nourishment, priesthood (lord Saturn, deity Bṛhaspati)
| # | Gist | Computable |
|---|------|-----------|
| 1 | Key planets in Puṣya → may **indulge in, or be attacked by, sorcery / spells / left-hand tantra** (more so with nodes / 8L / Venus / 5L involved). | partly |
| 2 | ⚠ **Remedy pointer:** recitation of the **Nārāyaṇa Kavaca** is offered as the best remedy for focal planets in Puṣya. **(non-Parāśara: remedial mantra.)** | no |
| 3 | Focal planets or lagna-nakṣatra in Puṣya → may **play politics / manipulate** others for gain, or be the victim of it. | partly |
| 4 | **Foster-parenting** theme (Bṛhaspati accepting Tārā's child Budha) — fostering or being fostered. | partly |

*(Pages: 223, 230, 231, 239.)*

### Āśleṣā — the serpent's coil (lord Mercury, deity Nāgas)
| # | Gist | Computable |
|---|------|-----------|
| 1 | Any planet in Āśleṣā tends to deliver its result **between ages 18 and 20.** | yes |
| 2 | **Ethic (gaṇḍānta):** being a nāga star at the end of Cancer, the native's chief lesson is to **never gossip / speak ill** of anyone. | no |
| 3 | Key/focal planets in Āśleṣā → **psychic experiences / encounters with spirits.** | partly |
| 4 | If Āśleṣā is afflicted → the native may **destroy the reputation/career** of a few people. | partly |
| 5 | "**Plastic surgery of Āśleṣā**" — wherever it sits, a **major transformation** in that area (good↔worse). | yes |
| 6 | Sexual planets (Venus/Mars) in Āśleṣā, if afflicted → **sexual imbalance** (perversion, excess, or too little). | partly |

*(Pages: 241, 255, 261, 268, 274, 283.)*

### 3b. Adjacent modern pointers — K.N. Rao (separate books, `modern`)

Not nakṣatra-based, but the same tier and the same pointer-only discipline. Keep in a
distinct "K.N. Rao (modern)" bucket; do not merge with the Saptarishis nakṣatra set.

**K.N. Rao — *Enigmas in Astrology* (Gajakesari-yoga assessment).** Pointers only:
- *Three/four-fold assessment* — judge the yoga from lagna, from Moon, and via the 10th
  house/10th lord counted from each, weighing aspects & associations (p.23). *partly*
- *Too common to read naively* — the Moon forms it ~⅓ of each month + by rising lagna, so
  a large share of people carry it; never apply its promise blindly (p.14,23). *no*
- *Sign-type parity constraint* — Moon & Jupiter in mutual kendras always share
  movable/fixed/dual modality; both cannot be exalted or both debilitated (p.13–14). *yes*
- *Jupiter primary, Moon secondary* — Jupiter's sign/ownership/condition carries more
  weight (p.14). *no*
- *Seven schemes of modification* — degraders (retro/combust/malefic-hit Jupiter; Moon in
  gaṇḍānta/kemadruma/heavy affliction) + examine full daśā/antardaśā of both (p.16). *no*
- *Grading good/better/best* — by whether Jupiter or Moon is merely unafflicted, in
  mūlatrikoṇa, or exalted & benefic-joined (p.36). *partly*
- *Strength check* — graha bala, an aṣṭakavarga method, vargottama status (p.36). *partly*
- *Timing by daśā* — full results in Moon/Jupiter mahādaśās; certain following yogakāraka
  daśās can exceed them (p.36–37). *no*
- *Per-lagna significance* — the identical yoga means different things by ascendant,
  through the specific houses Moon & Jupiter own (p.21–22). *partly*
- *Damage-control in dusthāna axes* — on a 6/8/12 axis, read it as protective not
  glorifying (3rd house an exception favouring artistic work) (p.45). *partly*

**K.N. Rao — *Astrology Lessons* (Part A).** The **fact tables** it reproduces (weekday
rulers, nakṣatra Vimśottarī lords/years, rāśi lordships, exaltation/debilitation/
mūlatrikoṇa/own-house, graha aspects, kendra/trikoṇa house categories, rāśi attributes,
natural kārakas, house significations, maraka lords) are **`traditional`** and almost all
**already in the BPHS core** — use only to cross-check. His **mnemonics** *P.A.C.*
(Position-Aspect-Conjunction) and *D.A.R.E.S.* (→ *P.A.C.D.A.R.E.S.*), his spiritual-house
framework, his Ariṣṭa/health checklist and his modern-profession significations are
**`modern`** pointers only.

---

## 4. Jaimini Chara Daśā  ·  tier: `jaimini` (a DIFFERENT school — NOT Parāśara)

> **This is the Jaimini school, not Parāśara.** It is a **sign-based (rāśi) daśā**, so it
> needs a **rāśi-daśā engine the project does not yet have** (all eight daśās currently
> built are the Vimśottarī *nakṣatra*-daśā family). The related **chara kārakas are
> already built** — `api/karakas.py`, on the BPHS 7-kāraka scheme (AK/AmK/BK/MK/PK/GK/DK),
> which matches the seven Rao advertises "not eight". So the *kāraka* half exists; only
> the *daśā* half is missing. Label everything here **"Jaimini — not Parāśara."**

**Source:** *Predicting Through Jaimini's Chara Daśā* — K.N. Rao (Vani Publications).
The excerpt read is **Chapter 6 "Calculation of Jaimini Chara Daśā" (book pp.40–45)** and
Chapter 14 (pp.96–105). **The calculation algorithm is captured in full; it is a
procedure, extractable as `jaimini`.** Chapters 2 (Kārakas), 3 (Daśā Order), 4
(Antardaśā), 5 (Jaimini aspects) are **cross-referenced but NOT in the excerpt** — two
consequences are flagged as gaps below.

### 4a. Ordered procedure (as the book gives it)

1. **Daśā order.** First write the mahādaśā order of the signs. *The book defers this to
   Chapter 3, which is not in the excerpt.* In both worked examples the order runs
   **zodiacally forward from the lagna sign** and is labelled *"direct"* (Aries lagna →
   Aries, Taurus, Gemini…; Virgo lagna → Virgo, Libra, Scorpio…). The "direct" label
   implies Ch.3 also defines a **reverse-order** case the excerpt does not show. **⚠ GAP —
   the direct-vs-reverse ordering rule must be recovered from Chapter 3.**

2. **Split the 12 rāśis into two fixed groups of six:**
   - **DIRECT** (count *forward*/zodiacally): **Aries, Taurus, Gemini, Libra, Scorpio, Sagittarius.**
   - **INDIRECT** (count *backward*): **Cancer, Leo, Virgo, Capricorn, Aquarius, Pisces.**
   - Mnemonic (author's): signs 1–3 direct, 4–6 indirect, 7–9 direct, 10–12 indirect.

3. **Length of each sign's daśā.** Count **inclusively** from that sign to the sign
   occupied by **its lord** (the sign itself = 1), **forward** if the sign is in the
   DIRECT group, **backward** if INDIRECT; then **subtract 1 year.**
   - **Own-sign lord = the exception: full 12 years, no deduction.**
   - **Bounds:** minimum 1, maximum 12; **whole years only.**

4. **Dual-lord signs.** **Scorpio (Mars + Ketu)** and **Aquarius (Saturn + Rāhu)** have
   two lords. The book gives **four placement cases** and a **four-tier strength test** to
   pick the operative lord. **⚠ GAP — the four cases and the four-tier tie-break were
   truncated in the extraction; recover the exact steps from the full Chapter 6 before
   implementing. Do not substitute a remembered "standard" rule; use Rao's own.**

5. **Author's explicit rejections** (method choices, `jaimini`):
   - Do **NOT** add/deduct a year for an **exalted/debilitated lord** (the commentators'
     rule) — Rao found it mistimes and can zero-out a sign, making it "non-functional".
   - Do **NOT** use fractional / expired-portion lengths (Dr. P.S. Sastri's method) —
     **full years only.**

6. **Accumulate** the computed lengths from the birth year to get each period's
   start/end. After all 12 signs the cycle **repeats identically.**

7. **Sub-periods (antardaśā)** are Chapter 4, **Jaimini aspects** Chapter 5 — **both
   referenced but not in the excerpt.** Not yet capturable.

### 4b. Chara kārakas (already built — `api/karakas.py`)

The book uses and confirms the **seven-kāraka** scheme: **AK** Ātmakāraka, **AmK**
Amātyakāraka, **BK** Bhrātṛkāraka, **MK** Mātṛkāraka, **PK** Putrakāraka, **GK**
Gnātikāraka, **DK** Dārakāraka. **Rāhu is shown on the charts but is NOT used as a
kāraka** — this is the "seven (not eight)" distinction on the cover; the 8-kāraka scheme
would add a Pitṛkāraka/Rāhu, which Rao rejects. The assignment rule itself (highest
longitude-within-sign = Ātmakāraka, descending) lives in Chapter 2, **not in the
excerpt** — but it is the same rule already implemented in `api/karakas.py` from BPHS
ch.32. **The kāraka layer needs no new build for Chara Daśā; only the rāśi-daśā engine
does.**

---

## 5. What is buildable, ranked

**A. Ship now — clean, self-contained data.**
1. **Nakṣatra attribute table, rows 1–9 (§2a).** 45 verified `traditional` cells. Drop
   them straight into the nakṣatra display as a **"traditional — not BPHS"** panel that
   sits *beside*, never inside, the BPHS ch.6 deity the app already computes. This is the
   single highest-value, lowest-risk item — it directly fills the "BPHS silent (ch.3 v.7)"
   gap on the correct footing.

**B. Buildable with modest work.**
2. **Chara Daśā engine (§4).** The length rule, the two fixed groups, the own-sign
   exception and the two rejections are fully specified and implementable. It needs a
   **new rāśi-daśā engine** (the project has none) and it **reuses the existing
   `karakas.py`.** **Blocked on two recoverable gaps:** the Chapter-3 order rule and the
   Chapter-6 dual-lord tie-break (Scorpio/Aquarius). Recover both from the full book
   before coding, and validate against the book's three illustration tables.

**C. Display-only — pointers, never engines.**
3. **The 46 nakṣatra techniques (§3) and the Rao pointers (§3b).** Surface as attributed,
   collapsible **"modern technique"** cards (name, gist, author, page, computable-badge).
   The `yes`/`partly` badge tells the reader whether the engine *could* flag the structural
   condition (planet/lord in nakṣatra) — but the **interpretation stays the author's**, and
   the cards must never be reproduced as prose or presented as chart verdicts. **Do not
   auto-render the ⚠ non-Parāśara techniques** (Rohiṇī T2 outer planets, Mṛgaśira T7 Vāstu,
   Puṣya T2 remedy) as computed results — they lean on material outside both BPHS *and* the
   traditional canon; show them, if at all, as clearly quarantined "non-Parāśara" notes.

**D. Needs more sources before anything ships.**
4. **Nakṣatra rows 10–27 (§2b).** Absent from the Part-I book. Source them before the
   27-row table is claimed complete.
5. **Cross-check the `traditional` claims against a primary.** Rows 1–9 verified clean
   against the canonical standard, **but the standard itself should be confirmed against
   Bṛhat Saṁhitā (ch.98, Nakṣatra-based) / a primary muhūrta text directly**, not trusted
   from a modern secondary. Same for any rows 10–27 you add.
6. **Chara Daśā Chapters 2–5** (kāraka rule text, order rule, antardaśā, Jaimini aspects) —
   obtain to close the §4a gaps and to add sub-periods and Jaimini dṛṣṭi.

---

## 6. Copyright note (one paragraph)

The four source books are **modern and in copyright** (K.N. Rao, b.1931; the Saptarishis/
Pandya compilation, contemporary). What was taken and what was not follows a bright line
that holds in law and is preserved throughout this document: **classical FACTS** (a
nakṣatra's lord, deity, symbol, degree range, padas; rāśi and dignity tables) are data the
books *tabulate* from a ~1500-year-old tradition (Bṛhat Saṁhitā / muhūrta) — **not their
invention, and not copyrightable** — so they are extracted **in full** and tiered
`traditional`. **ALGORITHMS** (the Chara Daśā calculation, the chara-kāraka assignment) are
procedures/methods, likewise **extractable as steps** and tiered `jaimini`. But the authors'
**interpretive expression** — their techniques' prose, their reasoning, and every **worked
chart example** (example-native names, birth dates, chart data) — **is copyrighted and was
NOT reproduced**: those survive here only as short, attributed **pointers** (name + neutral
one-line gist + author + page). Where it was unclear whether something was a bare fact or the
author's expression (e.g. Bharaṇī's "body part"), it was **treated as expression** and
pointer-summarised, not promoted to a `traditional` fact. Quotation was held to at most a
short phrase needed to anchor a stated fact; no paragraph of method is quoted anywhere.

---

## BUILT 2026-07-19 — the two engines this document supported

Two of the six sections above were implementable and are now code. Both are
NON-BPHS tiers and are labelled as such at every layer.

### Nakṣatra symbols (`api/nakshatra_attrs.py`) — tier `traditional`

The classical symbol of each nakṣatra (Aśvinī = a horse's head, …). NOT in
BPHS — the rāśi cards correctly mark this whole layer "BPHS is silent (ch.3
v.7)"; this fills it on a `traditional` footing, beside the BPHS ch.6 deity the
app already carries, never as Parāśara.

**Sourced for 9 of 27 only.** The source volume is *Part I* (Aśvinī → Āśleṣā).
All nine were cross-checked against the canonical standard: zero corrections.
Rows 10–27 are returned as explicit not-yet-sourced gaps — **not guessed.**
Inventing the other eighteen from memory is exactly the fabrication this project
refuses, and completing the table needs a primary source (Bṛhat Saṁhitā ch.98,
or Parts II–III of the series). The book states no gaṇa/yoni/nāḍī for any
nakṣatra, so none is carried. Served at `/api/nakshatra-symbols`.

### Jaimini Chara Daśā length engine (`api/charadasha.py`) — tier `jaimini`

A SIGN-based daśā from the Jaimini school — a different school from the eight
Viṁśottarī-family nakṣatra daśās already built. Source: K.N. Rao, *Predicting
Through Jaimini's Chara Daśā*, ch.6.

**Complete and validated:** the per-sign length — inclusive count to the sign's
lord, the direction of that count fixed by the sign's group (Aries/Taurus/
Gemini/Libra/Scorpio/Sagittarius count forward; the rest backward), minus one
year, the own-sign 12-year exception, the 1–12 bounds, and the dual-lord
strength tie-break for Scorpio (Mars/Ketu) and Aquarius (Saturn/Rāhu) recovered
verbatim from ch.6:
  (a) one lord in the sign → count to the other;
  (c) both in the sign → 12 years;
  (d) both elsewhere → association beats solitude, else higher
      longitude-within-sign wins.
Validated end-to-end against the book's worked Illustrations One (86 years) and
Two (56 years): the engine reproduces every per-sign year AND independently
makes the dual-lord choices the book states, from graha positions reconstructed
out of the book's own `counted` columns (not the copyrighted charts). Rao's two
method rejections (no exalt/debil year adjustment; whole years, no fractions)
are recorded.

**One thing deliberately NOT built: the sequence DIRECTION.** The rule that
decides whether the daśā runs forward or reverse from the lagna is in the book's
Chapter 3, which is not in the available scan. Both worked examples run "direct",
but the selection criterion is not shown — so `chara_dasha()` takes the
direction as an explicit argument and refuses to guess it. A remembered
"standard" rule was NOT substituted. The engine computes correct LENGTHS for any
chart; only the ordering needs Chapter 3.

Chara kārakas are already built (`api/karakas.py`, the 7-kāraka scheme Rao uses).
The per-sign lengths ride on the chart payload at `dasha.chara`.

**Not yet built:** a rāśi-daśā TIMELINE (the existing timeline is graha-lord
shaped; Chara Daśā bands are signs), antardaśās (ch.4, not in the scan), the
direction rule (ch.3), and rows 10–27 of the symbol table.
