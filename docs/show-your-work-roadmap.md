# "Show Your Work" — the Provenance-Explorer roadmap

*A prioritized plan for Devashaa's single most defensible differentiator: that
every claim is one tap from its source. Working document — English.*

## The thesis

The strategy is not to out-feature AstroSage or out-supply AstroTalk. It is to
own the one thing their business models forbid: **provenance you can inspect.**
Today that is already true at the *data* layer — claims carry a tier
(`sloka` / `traditional` / `modern` / `jaimini`) and a citation. But the
*experience* is uneven: some claims expand, some are hover-only tooltips, some
numbers show no derivation at all. The goal of this roadmap is to make
"show your work" the **hero interaction** of the site — any statement, one tap,
the full chain: **verse → tier → computation → ephemeris source.**

## Where we already are

- Tiered `.src` provenance chips across ~20 panels.
- `title=` tooltips carrying verse refs, combustion orbs, and method notes
  (Motion, Ṣaḍbala, Yoga, Bhāva).
- **Ṣaḍbala panel** — sub-component tooltips (Kāla/Sthāna breakdown) and the two
  honest method caveats (Cheṣṭā mean elements, Ayana β=0) surfaced.
- **Yoga panel** — cited śloka effect + the Ṣaḍbala strength resolution.
- **Bhāva-phala** — per-house cited rule + a *sourced* refusal where BPHS is silent.
- **Reading guide** — teaches how to read the signal stack.
- **Methodology** + **Validation** pages — state the doctrine and the proof.

The raw material is here. What is missing is a *consistent, drill-downable*
surface over it.

## The gaps (why it is not yet "show your work")

1. **Inconsistent affordance.** Some citations expand, some are hover-only
   tooltips, some are chips. There is no single, predictable "tap to see the
   source" pattern a user can learn once.
2. **Numbers hide their computation.** The Ṣaḍbala total, dignity state, and
   daśā dates appear as *results*; the arithmetic — the very thing the tests
   validate — is hidden or tooltip-only.
3. **Citations are refs, not text.** "Ch. 11 v. 3" is shown; the actual śloka
   (Devanagari/IAST + translation) is not inline.
4. **No unified "why" surface.** You cannot click an arbitrary statement and get
   its whole provenance chain in one place.
5. **Tooltips are desktop-only.** Hover does not exist on touch, so mobile users
   — the majority — cannot see the provenance at all. This is an *integrity*
   gap, not just a polish gap.

## Prioritized phases

### P1 — One provenance affordance, everywhere · foundation · **high impact / medium effort**
- Standardize a single interaction: every cited claim gets the same tappable
  provenance control — not hover-only, works on touch and keyboard.
- Replace hover-only `title` tooltips with an accessible popover (click/focus).
- **Why first:** it fixes the mobile-provenance integrity gap *and* gives every
  later phase a consistent place to hang detail. Biggest trust-per-effort win.

### P2 — Show the computation for numeric results · **high impact / medium effort**
- Ṣaḍbala: expand the existing sub-component tooltips into a full drill-down —
  six balas → each sub-component → its formula, inputs, and arithmetic (exactly
  what `test_shadbala.py` checks). The data already exists on the payload.
- Dignity, daśā balance, aspects: a "how this was computed" expansion.
- **Payoff:** the *validated* math becomes visible per-chart — the Validation
  page's claims made tangible on the user's own numbers.

### P3 — Inline verse text, not just refs · **high impact / higher effort (content)**
- Show the actual śloka (Devanagari + IAST) and a translation beside the ref,
  tiered as always.
- Needs a verse store keyed by chapter/verse. Large content task — do it
  incrementally, starting with the most-shown verses.
- **Payoff:** "Ch. 11 v. 3" *becomes the verse*. The deepest form of the doctrine.

### P4 — The Provenance Explorer (the "why" panel) · flagship · **high effort**
- A unified side panel: click ANY statement → its full chain — verse → tier →
  computation → ephemeris source → a link to the test/code that proves it.
- Ties P1–P3 into one signature surface. **This is the thing no competitor can
  build**, because their content is uncited and their math is closed.

### P5 — Export a cited reading · practitioner angle · **medium effort**
- Export/share a reading in which every line carries its citation — a citable,
  verifiable artifact a practitioner can stand behind, and a link others can check.

## Sequencing

**P1 → P2 → (P3 ∥ P4) → P5.** P1 is the foundation and the mobile-integrity fix;
do it first. P2 turns the validated math visible with data you already have.
P3 (content) and P4 (the flagship panel) are the deep investments and can run in
parallel once P1 lands. P5 is the practitioner payoff.

## Guardrails — do not betray the doctrine while doing this

- **Never show a computation you cannot justify.** Where a step is a modern or
  traditional choice, label it — exactly as Cheṣṭā and Ayana already do.
- **Never fabricate verse text.** If a verse is not in the store yet, show the
  ref, not an invented quote.
- **Keep "the text is silent" first-class** inside the explorer too — a refusal
  with its reason is a valid leaf of the provenance chain, not a dead end.
- **No new tooltip that only works on hover.** Every provenance detail added
  from here must be reachable by tap and by keyboard.

## One-line north star

*Any number or judgement on the screen is one tap from the śloka, the tier, the
arithmetic, and the line of code that proves it — on every device.*
