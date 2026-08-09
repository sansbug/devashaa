# Classical Sources — Provenance & Adaptation Policy

**Status:** foundational. Written *before* any classical content is embedded, the same
way `bphs-rules.md` was written before the BPHS layer. Nothing from Sārāvalī,
Jātaka Pārijāta, Bṛhat Saṁhitā, Phaladīpikā or any other classical text ships until
it has been extracted, cited, and **classified against §5 below**.

The site's founding discipline is **cite-or-refuse**: every judgement traces to a
locus in a named text, and *"the text is silent"* is a valid answer. This document
extends that discipline in two directions the BPHS-only layer did not need:

1. **Many sources** — several classical texts, never blended, each on its own tier.
2. **A temporal/ethical dimension** — these texts are 700–2,000 years old and carry
   social assumptions (caste, gender, slavery, fatal prediction) that must **not** be
   shipped to a modern reader as advice. §5 is how we handle that.

---

## 1. Provenance tiers

A claim's tier says *what kind of authority stands behind it*. Tiers are **never
blended** — a reading is shown under exactly one tier, with its source and citation.

| Tier | Meaning | Sources |
|---|---|---|
| `sloka` | Root Horā authority | **BPHS** (Parāśara, R. Santhanam tr.) — the backbone |
| `classical` | **NEW.** A dated primary/near-primary Sanskrit text with a trusted published translation | Sārāvalī, Jātaka Pārijāta, Bṛhat Saṁhitā, Bṛhat Jātaka, Phaladīpikā |
| `traditional` | Muhūrta/nakṣatra attribute tradition (post-Vedic, multi-witness) | Sunil John, Ram Babu Sao, Komilla Sutton … |
| `jaimini` | Jaimini-system doctrine | Chara daśā etc. |
| `modern` | A named modern author's method or pointer | K.N. Rao, Sarajit Poddar … |

**Rule:** the `classical` tier is for the *primary texts themselves*, cited by
chapter-and-verse. A modern author *summarising* a classical text is `modern`, not
`classical` — the tier tracks the locus we can actually cite, not the ideas' age.

---

## 2. Source registry

Every classical source is registered once, here, before its content is used. A claim
may only cite a registered source.

| id | Text | Author | ~Date | Edition / translator | Citation scheme | Format on hand | Copyright | Status |
|---|---|---|---|---|---|---|---|---|
| `bphs` | Bṛhat Parāśara Horā Śāstra | Parāśara | received | R. Santhanam (Ranjan) | ch.verse | full PDF + in-repo rules | modern tr. © | **live** (`sloka`) |
| `saravali` | Sārāvalī | Kalyāṇa Varma | ~9–10th c. | **R. Santhanam** (Ranjan) | ch.śloka | Vol 1 PDF (auth.) + partial .doc text | modern tr. © | **pilot** |
| `jataka_parijata` | Jātaka Pārijāta | Vaidyanātha Dīkṣita | ~15th c. | V. Subramanya Sastri, 1932 (Ranjan) | adhyāya.śloka | PDF (scanned) | modern tr. © | planned |
| `brihat_samhita` | Bṛhat Saṁhitā | Varāhamihira | ~550 CE | V. Subrahmanya Sastri & Ramakrishna Bhat, 1947 | ch.verse | PDF (scanned) | old tr. | planned (→ nakṣatra) |
| `phaladipika` | Phaladīpikā | Mantreśvara | ~13–15th c. | *Sanskrit e-text only* (sanskritdocuments.org) | ch.verse | Sanskrit, **no translation** | Skt public domain | **blocked** — needs a trusted translation (Ojha/Kapoor) |
| `brihat_jataka` | Bṛhat Jātaka | Varāhamihira | ~550 CE | **B. Suryanarain Row, 1919** | ch.verse | PDF (scanned) | **public domain** (pub. 1919, tr. d. 1936) | on hand |

Notes carried by the registry, not to be forgotten:
- The file first labelled "Brihat Jataka" was **Bṛhat *Saṁhitā*** — a different work. The
  real **Bṛhat Jātaka** is now on hand (Suryanarain Row 1919) and, being public domain,
  is the one text whose full translation we may reproduce.
- Phaladīpikā is **Sanskrit-only**. Translating terse technical ślokas ourselves is the
  exact fabrication risk cite-or-refuse forbids — it stays blocked until paired with a
  published translation.
- The Sārāvalī `.doc` is the Santhanam text but **partial and unverified**; the **Vol 1
  PDF is the source of truth**. The .doc may seed a draft, never the final citation.

---

## 3. Citation rule

Every `classical` claim carries `(source_id, chapter, verse)`. No locus → it does not
ship. Ranges are allowed where the edition groups verses (e.g. `saravali 22.5-6`).
`"the text is silent"` remains a first-class answer; absence is never padded from
general knowledge.

---

## 4. Copyright handling

The translations we hold (Santhanam, Sastri) are **modern copyrighted works**. The
existing BPHS layer already quotes cited verse-effects with attribution — fair dealing
for scholarship/criticism. Scaling to whole books, we tighten this:

- **Do not reproduce a translator's full prose wholesale.** For each verse we ship a
  **concise, site-authored gist** in our own words + the citation — a *rendering*, not a
  reproduction. (This doubles as the §5 adaptation.)
- **Sanskrit originals are public domain** and may be shown in full where we have a
  clean source (e.g. the Phaladīpikā e-text). Prefer *Sanskrit verse + our cited gist*
  over reproducing a copyrighted English paragraph.
- One-quote discipline, attribution always, source and translator named.

---

## 5. Adaptation policy — "the times have changed"

Classical phala encodes the social order of its age. Some of it is neutral and ages
fine; some would be false, discriminatory, or harmful presented to a modern person as
advice. **Every extracted verse is classified before it can ship**, into one of three
actions per content-class:

| Content class | Typical wording | Action |
|---|---|---|
| **Caste** (varṇa/jāti) | "will be a śūdra / serve low people" | **omit** the caste verdict; keep only non-caste substance, flagged |
| **Gender & marriage** | "number of wives", wife's character, widowhood | **neutralise** to partner-neutral where the *principle* survives; **refuse** value-laden/gendered judgements |
| **Slavery / servitude / rank** | "owns slaves", "master of servants" | **omit** or **historicise** |
| **Occupation status** | professions ranked high/low | keep the theme ("livelihood via X"); **drop** the status judgement |
| **Death / disease / poverty timing** | "will die at X", "will be blind/poor" | present as *the text's stated effect*, cited + dated — **never** as fate; **refuse** outright death-timing; health disclaimer (not medical advice) |
| **Remedies / ritual / gemstones** | mantra, yantra, dāna, stone | **exclude** (site-wide policy, unchanged) |
| **Archaic referent** | king, minister, elephant, specific rite | **preserve + gloss** ("rāja-yoga = authority in its context") |

**Actions defined:** `omit` = not shown; `historicise` = shown with a historical-context
badge and neutral framing; `refuse` = shown as an explicit refusal *with the reason*
(the cite-or-refuse move); `neutralise` = the underlying structural principle is kept,
the value-laden social claim dropped; `gloss` = original preserved, archaic referent
explained.

### Governing principles

1. **Attribution over endorsement.** Everything is *"Sārāvalī 22.4 states…"* — cited,
   **dated**, never the site asserting it as truth or as *your* destiny.
2. **The date is always visible.** The reader knows they are reading a ~10th-century
   (or older) view, so a modern claim is never implied.
3. **Refusal stays first-class.** Where content is harmful or we choose not to
   reproduce it, we say so *with the reason* — exactly like "the text is silent".
4. **This policy is published.** It ships as a Methodology-page section, "How we handle
   historical material." Transparency is the point; it is a trust signal, not a hedge.

### The historical-context badge

One new UI badge joins the existing provenance/confidence badges. It marks any reading
carrying `historicise`d content, and on tap explains: *"This reflects the social world
of its time (~Nth c.); shown for completeness, not as a judgement."*

Every stored classical entry therefore carries: `adaptation: { classes: [...],
action: omit|historicise|refuse|neutralise|gloss|clean, note }`. `clean` = no dated
content; ships plainly.

---

## 6. Serving model — the classical concordance

Classical readings are served as a **concordance**, never a blend. For a placement
(e.g. Sun in Siṁha) the panel shows each source's cited line **side by side**:

- BPHS (`sloka`) · Sārāvalī (`classical`) · Jātaka Pārijāta (`classical`) …
- each tier-badged, source-named, chapter/verse-cited, date-shown;
- **agreements and disagreements left visible** — the concordance's honesty is the
  feature. No composite, no averaged verdict (same rule as the Signal Stack).

This is deliberately hard to copy: verse-cited, multi-source, with a stated adaptation
policy. That combination is the moat.

---

## 7. Extraction & verification protocol

1. **Source of truth is the published edition** (the PDF), not a convenience text. A
   machine-readable `.doc`/e-text may *seed* a draft; the citation and final wording are
   verified against the edition.
2. **Extract** per verse: `{source, chapter, verse, sanskrit?, literal_sense,
   topic_tags}`.
3. **Render** a concise site-authored gist (§4) — our words, not the translator's.
4. **Classify** against §5 — assign content-classes + action.
5. **Adversarially verify** — an independent pass checks: does the gist match the verse,
   is the citation right, are the §5 flags correct? Disagreement → the entry is held,
   not shipped (same discipline that moved doubtful antardaśā conditions to
   `unavailable`).
6. **Confidence** per entry: `corroborated` (checked against edition) / `single_source`
   / `uncertain`. `uncertain` never ships as fact.

---

## 8. Deliberate exclusions (recorded so they are not "fixed" later)

- **No remedies** — mantras/yantras/stones/dāna are out, site-wide, including from these
  texts' remedy sections.
- **No death-timing, no medical/financial/legal directives** — historical statements
  only, framed and disclaimed.
- **No tier-blending** — a classical line is never merged into a BPHS statement or a
  composite score.
- **No self-translation of untranslated Sanskrit** — Phaladīpikā stays blocked until a
  trusted translation is paired to it.
- **No Western material presented as Vedic** — unchanged from the existing doctrine.
