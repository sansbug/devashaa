# Science of Light (Course 1) mapped to devashaa's gap map

2026-11-21. Freedom Cole's *Science of Light* Course 1 (scienceoflight.net) follows his book, which
he says is built on Parāśara's text. Its lessons are behind a paid login, and none of their
content is used here. This map uses only the **public syllabus (topic names)**. It asks, for each
topic: where is it in BPHS (Santhanam), and does devashaa already register it?

Status: **have** = registered and cited · **part** = some of it · **gap** = nothing registered ·
**out** = left out by site policy.

| # | Course topic | BPHS locus (Santhanam Vol I unless noted) | devashaa today | Status |
|---|---|---|---|---|
| 1 | Introduction, chapter 1 | (overview) | n/a | — |
| 2 | Vedic foundations | (background) | n/a | — |
| 3 | Planets, kārakas | ch.3 (natures v.11, dignity vv.49-55); ch.32 cara kārakas | natures, dignity, relationships; cara kārakas (`karakas.py`, ch.32) | have |
| 4 | Devatā (deities) | ch.6 (division deities, nakshatra deities vv.24-26) | all division deities D3–D60 (`varga_rules.py`), nakshatra deities | have (planet deities: locus not yet checked) |
| 5 | Rāśi | ch.4 | `rasis.py` | have |
| 6 | Rāśi divisions | chs 6–7 | calculation, deities, uses, hora, thirds, D60/D16 lord rule | part: no planet-in-division-sign reading |
| 7 | Bhāva | ch.11 (significations), chs 12–23 (house effects) | 54 + 5 verses matched on their conditions | have (ch.19 longevity left out on purpose) |
| 8 | Bhāveśa (house lords) | ch.24 | all 144 lord-in-house cells | have |
| 9 | Strengths and status | ch.7 Viṁśopaka; ch.27 Ṣaḍbala; ch.45 avasthās; ch.34 functional natures | all four | have |
| 10 | Pañcāṅga, Pañcāṅga doṣa | muhūrta tradition (not BPHS) | `panchang.py`, `muhurta.py` (traditional tier) | have |
| 11 | **Ārūḍha** | **ch.29** (padas of houses and planets; PDF from p.292); **ch.30** Upapada (from p.302) | DONE 2026-11-21: 12 bhava padas + 18 result verses (`arudha_argala.py`); Upapada left out | have (part) |
| 12 | **Argalā** | **ch.31** (PDF pp.310–316) | DONE 2026-11-21: Argala on every house, the AL and its 7th; vv.2-9 and v.10 shown side by side; effects vv.11-18 | have |
| 13 | Sambandha and yogas | ch.3 relationships; chs 35–41 yogas | 88 yogas catalogued | part: nīca-bhaṅga, sign exchange, Pravrajyā (BJ ch.15) missing (see the web pilot) |
| 14 | Nakṣatra | ch.6 deities; Vol II ch.46 lords | facts; Moon in 20/27 nakshatras (Bṛhat Jātaka ch.16) | part |
| 15 | Daśā (timing) | Vol II chs 46–60 | Viṁśottarī + others, ch.47 verdicts, chs 52–60 antardaśā | have (Chara Daśā: lengths only) |
| 16 | Divisional charts (2 lessons) | chs 6–7 | as row 6 | part |
| 17 | **Kārakāṁśa** (inside the kāraka lessons) | **ch.33** | Kārakāṁśa computed (ch.33 v.1), no results registered | **gap** |
| 18 | Remedies | various | excluded site-wide (classical-sources-policy §8) | out |
| 19 | Interpretation, practicum | — | the study view (`/study`) | have |
| 20 | Research project (10 charts) | — | `study_backtest.py` (hit rates vs controls) | have (no data yet) |

## What this adds to the plan

The course covers three BPHS topics that devashaa has not touched. All three are in the
Santhanam volume already on hand, so no new book is needed:

1. **Ārūḍha padas, ch.29.** Calculation first (the house pada and its exceptions), then the
   results stated from the Ārūḍha Lagna. Upapada (ch.30) is mostly about spouse and children,
   so most of it will fall under the sensitive rules.
2. **Argalā, ch.31.** Calculation (planets in the 2nd, 4th, 11th and 5th intervene; the 12th,
   10th, 3rd and 9th obstruct) and its stated effects.
3. **Kārakāṁśa results, ch.33.** The engine already finds the Kārakāṁśa; the chapter's results
   for it are not registered.

These are now silent rows in the gap map (`/study` → Gap map), with the chapter as the lead.
Each would follow the same method as steps A and C: read the page images, register the verses,
check twice, and add tests.

## What is not taken from the course

None of the paid lessons, recordings or book text. If the book is bought, it can be cited by page
on the `modern` tier (like Patel on D9). It never replaces the BPHS verse it explains.

## Done 2026-11-21: Ārūḍha and Argalā (`api/arudha_argala.py`)

- The 12 bhava padas with the verse's exceptions (ch.29 vv.4-5). **Santhanam's printed Ārūḍha chart
  skips the 7th-house exception in houses 9 and 10**, and his note 2 gives a third answer. The verse is
  followed, and the plain count is shown beside it. The tests pin both his worked chart and this difference.
- 18 result verses from the Ārūḍha Lagna (ch.29 vv.8-36, ch.30 v.39), each returned whole with the
  clause that fired. Left out: v.24 (a sexual verdict on the body), v.29 (the frame for counting from
  the Kārakāṁśa is not stated) and the clauses that need a planet's strength.
- Argalā (ch.31): formation and obstruction by vv.2-9 (by number of planets; strength is not
  evaluated) and by v.10 (quarters of the sign), both shown and never merged; Vipareeta; grades. For
  the effects of vv.11-17 the planet must also aspect the house, as the translation states.
- Read from the page images, then re-read at zoom. The re-read caught one logic error (v.16 means
  a conjunct benefic and malefic *aspecting* the 12th), which is fixed and pinned by a test.
