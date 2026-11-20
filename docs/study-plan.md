# Study agent — gap map, study view, testing plan

Status 2026-11-19: steps 1–3 are built locally (not committed, not deployed). Step 4's harness is
built and runs on made-up data only. **Nothing below §4 is downloaded, OCR'd or extracted until
the owner approves it.**

## 1. What was built

| Piece | File | What it does |
|---|---|---|
| Gap map | `api/study.py` `gap_map()` · `GET /api/study/gaps` | Every relation axis, the registered sources that cover it, cells each covers, and what is silent. Counts are read from the corpora at run time. |
| Study ledger | `api/study.py` `ledger()` · `POST /api/study` | For one chart (+ an optional `transit_date`): one row per cited relation that fires, with source, tier, locus and confidence. A **silence row** for each factor the chart has and no text reads (every D2–D60 placement, every planet's nakṣatra, nodes in signs, transits from the Lagn). |
| Study page | `api/study_page.py OUT.html --date … --time … --lat … --lon … [--transit …]` | One local HTML page: gap map, then the chart's lines grouped by division, then its silences. Nothing leaves the machine. |
| Hit-rate harness | `api/study_backtest.py SUBJECTS.json` | Timing rules on dated events against two controls (§5). |
| Tests | `api/test_study.py` | One source, one tier and a locus on every row. No score, net or composite key. Every division is either answered or refused. Sensitive text is held back unless asked for. The Python SENSITIVE pattern must match `web/src/findings.js`. |

The rules hold: each row is one source's line; rows are never added or ranked; sensitive
passages (death, lifespan, bereavement, fidelity) are flagged and their text is withheld by default.

## 2. Gap map (from the corpora, 2026-11-19)

| Relation | Status | Registered coverage |
|---|---|---|
| graha × rāshi (D1) | partial (7 of 9 grahas) | Sārāvalī 84/84 · Bṛhat Jātaka 84/84 (`classical`). Nodes: no text. |
| graha × bhaav (D1) | partial | Sārāvalī 84 · BJ 44 · Phaladīpikā 78 + nodes 24 (ocr_text) · Chamatkāra 68 |
| bhaav lord × bhaav | covered | BPHS ch.24, 144/144 |
| bhaav conditions | listed | BPHS chs 12–23: 54 verses · ch.13: 5 groups |
| Lagn rāshi | covered | Phaladīpikā 9.1–12 (ocr_text) · BPHS ch.34 natures (no phala) |
| yoga | listed | 88 catalogued |
| **graha × nakshatra** | **silent** (0/243) | — |
| nakshatra as a place | covered (facts) | BPHS deity + lord · traditional attributes 27 · modern techniques 18/27 |
| nakshatra lord × graha | silent | fact only (planet matrix) |
| graha × degree | listed | Bāladi / Jāgradādi (ch.45), exaltation degrees (ch.3), uccha bala (ch.27), Moon gaṇḍānta (Vol II ch.92); Pushkara / 64th navāṁśa (modern). **No result for an exact degree.** |
| **graha × rāshi in D2, D3, D4, D7, D10, D12, D16, D20, D24, D27, D30, D40, D45, D60** | **silent** (0/108 each) | Only the division rule (ch.6) and Vimśopaka strength (ch.7) |
| graha × rāshi in D9 | partial, modern only | Patel: vargottama 9, bhāva-sūchaka 12 |
| transit × bhaav from Moon | covered | Phaladīpikā ch.26, 108/108 + vedha |
| transit × bhaav from Lagn · transit × natal degree · transit × nakshatra (tārā) | silent | geometry only |
| transit × aṣṭakavarga bindus | silent | tables registered; `transit_potency` is our synthesis, not a text |
| dasha lord · antar-dasha | covered | BPHS Vol II ch.47 (9) · chs 52–60 (81) |
| annual chart | covered (modern) | Charak 108 |

**Summary: 7 covered · 4 partial · 3 listed · 20 silent.** As expected, D2–D60 is the thinnest: 14
of 15 divisions have no reading at all, and D9 has only a modern one.

## 3. Plan to fill the gaps (needs approval, by step)

Ordered by value for the least copyright exposure. Every step follows policy §7: extract from the
page image → our own short gist + locus → §5 classification → an independent check → register.

| # | Fills | Source on hand (`C:\books\astro`) | Copyright | Work |
|---|---|---|---|---|
| A | **D2–D60: what each division is read for, and its deities** (e.g. the 60 Ṣaṣṭyāṁśa deities, benefic or malefic) | BPHS Vol I ch.6 (Santhanam) | modern tr. © → facts + short gists only | Read ~10–15 page images. If the chapter names a deity for each part of each division (to confirm on the page), this gives a cited line for every graha in those divisions and closes most of the D2–D60 gap in one step. |
| B | Vaiśeṣikāṁśa grades (a graha well placed in 2, 3, 4 … divisions) | BPHS ch.7; Phaladīpikā ch.3 | © → facts | ~6–8 pages |
| C | **D3**: the 36 drekkāṇa forms · **Moon × nakshatra** (27 cells, the first graha × nakshatra row) | Bṛhat Jātaka, Suryanarain Row 1919 | **public domain**: may be shown in full | ~15–20 pages. No copyright limit. |
| D | D9 / D30 classical readings (planets in navāṁśas, triṁśāṁśas) | Sārāvalī (Santhanam) | © → gists | ~20–30 pages. Check which chapters before committing. |
| E | Transit by aṣṭakavarga bindus | BPHS Vol II, Aṣṭakavarga chapters | © → gists | ~15 pages |
| F | Nakshatra and degree results | Hora Sara (Santhanam) | © → gists | Survey first (~5 pages), then decide |

No downloads are needed for A–F: every book is already on the workstation. The cost is reading page
images (pypdf + Pillow → Read), the same method used for `bhava_effects.py`. No OCR tool is installed,
and none is proposed. Each step lands as its own `*_rules.py` + test, with `confidence` stated.

Not proposed: anything from Bhṛgu Saṁhitā (fated verdicts, image-only, 638 pp); self-translating
the Sanskrit Phaladīpikā; web machine translations.

## 4. Birth data for testing (needs approval before any collection)

- **Who:** public figures only, with a Rodden rating of **AA** (birth certificate or record) or
  **A** (quoted from the person or family). Nothing rated B, C, DD or X. **No private person's
  chart, nothing from forums.**
- **Where:** Astro-Databank (astro.com) is the standard register of rated data. **Its terms of use
  must be checked before any reading.** The proposal is to read entries by hand (no scraping). For
  each person we record only date, time, place, rating and the record it cites. Where the record
  itself is public (a birth certificate, a published biography), cite that.
- **Size:** about 100 people × about 5 dated events = about 500 events. A rule needs roughly 200
  events in its category to detect a 10-point lift over a 50% base rate (80% power). Fewer people
  means wider intervals, and the report will say so.
- **Events:** dated facts from the public record (Wikipedia with its references, official bios),
  coded into fixed categories **before any chart is cast**: election won or lost, appointment,
  resignation or dismissal, major award, marriage, birth of a first child, imprisonment or legal
  defeat, bankruptcy.
  **Never used:** the person's death, any lifespan, a bereavement, a partner's fidelity
  (CLAUDE.md rule 2). The harness refuses these categories. *Divorce and illness are left out
  unless the owner says otherwise.*
- **Storage:** the subject file stays **outside this public repo** (e.g. `C:\proj\_reading\study\`).

## 5. How rules are tested

- **Timing rules** (first round): Phaladīpikā ch.26 transit-from-Moon status per graha · the
  ch.47 verdict of the running maha-dasha and antar-dasha lord. A hit is a rule whose state on the
  event date agrees with the event's polarity.
- **Two controls, reported side by side and never merged:** (a) *within*: random dates in the
  same person's life; (b) *swapped*: the same event dates read against other people's charts.
- **Reported per rule:** hits/n, a Wilson 95% interval, the control rates, the difference, a
  permutation p, and a Benjamini-Hochberg q across all rules. **No pooled score.** Rules that do
  no better than chance are reported as such and stay on the site as what the text says.
- **Natal (static) rules** such as yogas, lord-in-house and the D2–D60 deities come in a second
  round. They need blind coding (someone who has not seen the chart codes each claim against the
  biography) and are not attempted in round one.
- **Rules are fixed before the data is read.** A failed rule is not re-tuned on the same set.
  Any change is tested on a fresh hold-out set.

## 5b. Done 2026-11-19: steps A and C

**A, BPHS I chs 6–7** (`api/varga_rules.py`, read from page images, PDF pp.67–94):
- what each of the 16 divisions is read for (ch.7 vv.1-5);
- the presiding deity of every part of D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D40, D45
  and D60 (ch.6), with the even-sign reversals the translation states;
- D60: the verse's 60 names, plus the benefic or malefic mark. The mark comes from Santhanam's
  NOTE, so those rows are tier `note`;
- ch.7 v.13: which grahas give effects in which hora;
- ch.7 vv.14-15: full, medium or nil effects by the third of a hora, decanate, turyāṁśa or navāṁśa;
- ch.7 vv.6-8: a house lord in a malefic D60 part (the house diminishes) or a benefic D16 part
  (the house flourishes). Both depend on a note, so both are tier `note`.
- Not registered: the D2 deities (the Sanskrit names them, the English does not); the D60
  glosses; Vaiśeṣikāṁśa (ch.6 vv.42-53, needs the Āruḍha lagna); ch.7 v.16, which would apply
  sign results to D30.

**C, Bṛhat Jātaka, Row 1919** (`api/bj_varga_rules.py`):
- the Moon in 20 of 27 nakshatras (ch.16). Printed p.186 is missing from the scan, so Aśvinī to
  Punarvasu are not read;
- 26 of 36 drekkāṇa forms (ch.27). Printed p.262 is missing (stanzas 13–19). Stanza 27 has no
  text in the printing, and stanzas 30–31 run together. Ch.27 describes the drekkāṇas and gives
  no result for a person. Row's note applies the forms to journeys and lost-article questions,
  and the study view labels them as descriptions.
- Five lines were neutralised under §5 (wife or husband → spouse or partner); "royal servant" is
  glossed and "servants" historicised. Each change keeps Row's printed words beside it.

Gap map now: 24 covered · 6 partial · 3 listed · 20 silent. D2–D60 now has a cited deity line for
every planet in 14 of the 15 divisions (D2 is the exception). It still has **no planet-in-sign
reading** in any division.

Checks: read once, then re-read word by word at zoom against the page images on 2026-11-19
(`confidence: page_image_checked`). All BPHS lists and quotations matched. For Bṛhat Jātaka the
words of all 20 nakshatra lines and 26 drekkāṇa forms matched. Two printer's slips are recorded
(`printed`: "Konwing", "valture's"). One added comma was removed (Pubba). The D60 #60 name now
carries the page's alias "(Indurekha)". Punctuation on the low-resolution Bṛhat Jātaka scan is not
always certain. The second pass was done in this same session, not by a separate reader. Tests: `api/test_varga_rules.py`, `api/test_study.py`.

Next leads found while reading: Bṛhat Jātaka ch.19 (Row, about printed p.204) reads the **Moon in
each navāṁśa**, a classical D9 reading in a public-domain edition. The Sastri edition of Bṛhat
Jātaka could fill the missing stanzas.

## 6. Decisions for the owner

1. Approve extraction steps A–F (or a subset). **A + C** are recommended first.
2. Approve Astro-Databank as the birth-data register after a terms check, read by hand, AA/A only.
3. Divorce and publicly documented illness as event categories: yes or no.
4. Should the study view become a page on devashaa.com (owner-only, or public), or stay a local tool?
