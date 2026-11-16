# devashaa — working notes for Claude

Vedic astrology (jyotiṣa) engine. **Live: https://devashaa.com** · API:
`https://devashaa-api.onrender.com`

Python/Flask + Swiss Ephemeris backend, React (Vite) frontend, bilingual
English/Hindi. Read `DEPLOY.md` for the hosting split and `docs/` for doctrine.

## The two rules that govern everything

1. **Cite or refuse.** Every judgement traces to a locus in a named text; *"the
   text is silent"* is a valid, preferred answer. Never fabricate a classical
   rule, never paraphrase a śloka into a meaning it does not state, never fill a
   missing cell from general knowledge of the classics. Provenance tiers stay
   separated and are never blended: `sloka` (BPHS) · `jaimini` · `classical`
   (other texts, each on its own tier) · `synthesis` (our weights/heuristics).
   See `docs/classical-sources-policy.md` §5 for the adaptation rules
   (gender-neutralise, gloss archaic "rāja" as authority, keep disease/poverty
   as the text's own dated view, drop caste verdicts).
2. **Indication, not fate.** Windows and directions, never fated events or
   dates. Two sensitive readings — a partner's fidelity, loss of a loved one —
   ship only as opt-in ♥ *care-signals*, never as verdicts. **Lifespan is never
   dated**, for the native or anyone else, past or future.

**Never self-translate Sanskrit.** Extract from a published translation (or, for
Phaladīpikā, Ojha's Hindi *artha*) and label whose words they are.

## Layout

- `api/` — Flask app (`app.py`) + ~79 engine modules. Key ones: `matrix.py`
  (the projection engine: natal matrix → 4-clock ensemble → events → change
  engine → life arc), `explain.py` (the "Ask your chart" router), `vedic.py`
  (chart computation), `*_rules.py` (extracted, cited text corpora — treat as
  generated data, not prose to edit by hand).
- `web/src/` — React. `App.jsx` (shell/sections), `RasiChart.jsx` (South+North
  charts, bhāva hover cards), `SkyWheel.jsx`, `MatrixPanel.jsx`,
  `ExplainPanel.jsx`, `i18n.js` (every user string, `en` + `hi`).
- `docs/` — doctrine and policy. Read before touching classical content.
  `docs/projection-reference.html` is the engineering reference for the whole
  projection stack + Ask feature (mirror of the claude.ai artifact; open it in a
  browser). Keep it in step with the artifact when either is updated.

## Running locally

```bash
# backend (venv at .venv; PYTHONUTF8=1 matters on Windows)
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe api/app.py   # :5199
# frontend
npm run dev --prefix web
```

**Tests: there is no pytest in the venv.** Run them by importing:

```bash
cd api && PYTHONUTF8=1 ../.venv/Scripts/python.exe -c "
import test_matrix_ensemble as T, test_ashtakavarga as A
for m in (T, A):
    for n in dir(m):
        if n.startswith('test_'): getattr(m, n)()
print('ok')"
```

## Pūjā & Havan (`/pooja`)

A separate section: guided ceremonies, muhūrta, family rooms, a pandit roster.
Frontend `web/src/pooja/`, Worker `web/pooja-worker.js` (D1 + a Durable Object
per room + R2 `devashaa-recordings`), engine `api/muhurta.py`.

- **Voice is human.** Mantras (and explanations) are played from the voice
  library a pandit records at `/pooja/desk`; the device voice never reads a
  mantra unless the family switches the "pronunciation aid" on. A clip id
  carries a hash of its text (`guide.js clipId`), so editing a mantra or an
  explanation orphans its recording — it must be re-recorded, by design.
- **The explanations are not translations** (rule above): they say what a step
  is and why it is done.
- **Scripture behind them**: `web/src/pooja/sources.json` — each verse's
  Sanskrit, a brief IN OUR WORDS of what the named edition's translation says
  (Gītā: Swami B.G. Narasingha; Bhāgavata: Gita Press Hindi), and which steps /
  ceremonies cite it. Shown in the guide's Detailed mode and on each ceremony
  page; edition and page only on /references (or with references switched on).
  ⚠ A verse's Sanskrit is entered only after it is checked against an
  independent text (`C:\proj\_reading\sanatan\tools\refs_verify.py`, GRETIL /
  sanskritdocuments.org); its `checked` fingerprint makes the test fail if the
  text is later edited without re-checking. The Gita Press e-book has typos.
  Every ceremony has at least one verse (the test checks it). Where the books do
  not describe a ceremony (annaprāśana, muṇḍana, gṛha-praveśa, a vehicle pūjā),
  its verse carries a `note` saying so plainly and what the verse is instead —
  never presented as the rite's own authority.
- **The Hanumān Cālīsā** (`chalisa.js`): every one of its 43 verses carries a
  Hindi gist in our own words, after the *bhāva* of Dr. Ramak Lakshmana
  Murty's commentary (Hindi tr. Dr. Shiv Satyanarayana, 1999 — `BHAV_SOURCE`,
  page per verse). A verse on what recitation brings is reported as the poet's
  word ("कवि कहते हैं कि …"). The gists are display-only: the chanted text and
  its clip ids are unchanged (the test checks the verses join back exactly).
- **A pandit is public by `pid`, never by `userid`** (which may be an email).
- **TURN relay**: on when the Worker has secrets `TURN_KEY_ID` and
  `TURN_KEY_API_TOKEN` (Cloudflare Realtime TURN key); STUN-only otherwise.
- Tests: `node web/test_pooja.mjs` (relay, audio clean-up, clip ids, service
  worker) and, against a local Worker, `node web/test_pooja_worker.mjs` (see
  its header). `api/test_muhurta.py` for the engine.
- ⚠ `public/sw.js` must never answer for `/api/*` — a cache is keyed by URL,
  not by who is signed in.
- A machine (device) voice is off unless the family asks for it, and the wrong
  gender is never played (`voices.js`). The owner wants human voices: the admin
  can add a "voice" (a pandit with no account) and record or upload for him.

## Planetary Positions table (`ChartDeck.jsx`, `PositionsCard`)

Each graha's nakṣatra, pāda and degree in the nakṣatra, in two orders (planets, or
houses 1–12 with empty houses shown; the choice stays in localStorage). The nakṣatra's
colour comes from its muhūrta class (`nakshatra.quality` in the chart payload, from
`api/nakshatra_attrs.py`): Soft/Light/Fixed/Mutable green (the owner's call), Mixed neutral, Fierce/Sharp
red. ⚠ The seven classes are the tradition's (`traditional` tier, not BPHS); the
three-way grouping (`NAK_TONE`) is OURS, and it describes the nakṣatra, not the planet
in it. No registered text gives planet-in-nakṣatra results. The word for the class is
shown under the name so the colour is never the only cue.
- ⚠ With references off, `t()` runs `scrubProse`, which strips hedges such as "not a
  prediction" from UI strings: state the fact instead.
- A chart shared before this existed has no `quality`: no colour, nothing breaks.

## "Explain my chart" (the plain-words walkthrough)

The owner asked (2026-11-11) for the format of simple explainer reels: one topic at
a time, "the houses that matter", then numbered lines about the reader's own chart.
`web/src/walkthrough.js` builds it from the chart payload alone: the basics, then
one topic per house (sign, its lord and where the lord sits — "so your X is tied to
Y" — the lord's dignity and nakṣatra class, planets in the house, full and ¾
aspects, the natural kāraka), then what is running now (daśā), then "Signs, not
promises". `ChartWalkthrough.jsx` plays it on its own animated North chart (the
house outlined solid, the lord's house dashed — never tinted; a line to the lord,
the aspects), EN/HI, a topic row, an opt-in labelled device voice, "Copy the
script" (one paragraph a topic, for a narrator or a HeyGen-style presenter).
- Planet topics (`graha_<key>`, the Lagna's lord first, between the basics and the houses): the
  owner's brief of 2026-11-16, after ASD-STE100 — fixed sentence patterns, one idea a sentence,
  at most 25 words, no semicolon or dash, a line left out when the chart has no value for it.
  Place and house · what it rules and what that ties together · sign standing · retrograde ·
  degree, Bālādi stage and the text's grade (ch.45 vv.3-4, from `analysis.grahas`) · companions
  · the great-person yoga (said only when the engine detected it; a near miss names the missing
  condition). ⚠ ONE line per planet is OURS (the owner's choice, "Our words, labelled"): it
  opens "Our reading, not from a classical text:" and says what the planet usually stands for
  (`NATURE`) and the area its house holds. Every sentence of it carries "usually"; qualities
  only, never an event or a verdict; a planet word never repeats a house word. No other planet
  sentence states a trait. The nodes get no sign-standing and no yoga line. The test pins all of this.
- The same style holds for EVERY topic since 2026-11-16 (opening, houses, timing, close): the
  test splits every English line into sentences and fails on more than 25 words, a semicolon
  or a dash. A house lord sitting in its own house is named once, not again as an occupant.
- House labels (`HOUSE`) are BPHS ch.11's significations, shortened; longevity
  (8th) and one's own death (12th) are left out of the plain labels on purpose.
- ⚠ The BPHS ch.24 lord-in-house rule is NEVER in the plain lines: it is behind a
  click, word for word, and only when it passes `CARE` (no death, lost child,
  childlessness, wives, vice…; EN and HI regexes must agree); otherwise the click
  points to Bhāvas & Yogas. No book is named in `say`; `cite` shows only with refs
  on. `node web/test_walkthrough.mjs` pins all of this (and walks the reference
  chart in both languages when the local API is up).
- Popular "combination" rules (e.g. 5th–7th lord link = love marriage) are NOT in
  the registered texts and are not used.
- A chart shared without birth details has no daśā: that topic is dropped.

## The site's sentence style (owner, 2026-11-16, after ASD-STE100)

Every sentence WE write for a reader, in the walkthrough and in every simple-view section
(findings, life areas, daśā reading, the backend's "why this verse applies" lines): one idea
a sentence, at most 25 words, no semicolon and no dash, each term used one way, a line left
out when the chart has no value for it. A passage quoted from a text is the text's and is
left exactly as registered. `test_walkthrough.mjs`, `test_findings.mjs`,
`test_lifeareas.mjs` and `test_dashareading.mjs` each split our English lines into sentences
and fail on a break (`styleBreak`). Hindi follows the same shape but is not machine-checked.
The full analysis follows it too: `node web/test_style.mjs` checks every English entry of the
interface table (`i18n.js` + `i18n-chrome.js`; a range of numbers is not a dash; the few
fragments a panel joins to something else are listed in its `FRAGMENTS`). NOT restyled, on
purpose: passages and renderings of the texts, citation lines ("… — Parāśara, tr. …"),
labels such as "Meen (Pisces) — 13°55′", the provenance / scan-audit flags and the
`adaptation.note` fields of the generated corpora (`*_rules.py`), the Pūjā section (an
edited explanation orphans its recording) and the static pages (Compare, References,
Methodology, Privacy, Support).
Before shipping new wording, print it for a real chart and read it.

## Chart findings (the simple view's "What would you like to understand?")

`web/src/findings.js` builds them from the chart payload alone; `Findings.jsx` shows them;
`node web/test_findings.mjs` pins the rules (with the local API up it checks the reference
chart). The owner's provenance rules for them (2026-11-15) — interpretation is wanted, with
its source beside it:

1. **Direct**: a passage is shown when it is in the registered library (BPHS ch.24 lord-in-house,
   ch.34 by ascendant, the yoga chapters; the classical concordance for a graha in a house or a
   sign), its condition matches the calculated chart, and its text, translator and locus are
   named. It is always "what the text says" (`texts`), never a fact about the person.
2. **Derived**: only with its chain of cited steps and the factors on both sides, labelled
   "our inference" (`inference`). No chain, no inference (the nodes get none).
3. **Modern**: only from a registered author and passage, on its own tier, never mixed in.
4. **Unsupported**: left out. A placement with no registered passage says so.
- Each finding reads: what your chart shows · what the classical texts say (+ why each applies)
  · how the placement is read · what other factors must be considered · our inference · exact
  references (the last only with References on — see below).
- ⚠ `SENSITIVE` (a death, a lifespan, a bereavement, a partner's fidelity) is never shown
  unasked — rule 2 at the top of this file still governs. The passage is listed with its
  reference and a "Show the whole passage" button (opt-in). It is shown WHOLE or not at all:
  never cut down to its favourable clause.
- ⚠ The reading ORDER and its weights are ours (synthesis), and the panel says so.
- Registered 2026-11-15 from the scans in `C:\books\astro` (the source books now live there):
  - `api/dhana_bhava.py` — BPHS ch.13 vv.1-7 (2nd house / wealth), Santhanam's words read
    from the PAGE IMAGES; each verse is matched on its own stated conditions and returned
    WHOLE with the clause that fired (`analysis.dhana_bhava`). Its docstring lists what is
    deliberately not evaluated (vv.4-5 when one planet rules both houses; v.5's ambiguous
    alternative; v.7's combustion, which has no orb in the text). `test_dhana_bhava.py`.
  - `api/phaladipika_nodes_rules.py` — Phaladīpikā 8.25-33, Rāhu and Ketu in the bhāvas, with
    śloka numbers. ⚠ confidence `ocr_text`: read from the scan's text layer, not yet checked
    against the page images (the Sastri PDF is mixed-raster and nothing here can render it —
    no poppler / PyMuPDF) nor adversarially verified like the seven-graha entries.
  - The running daśā lords' findings carry BPHS Vol II ch.47 vv.5-6 (`dasha.verdicts`).
  - `api/bhava_effects.py` — BPHS chs 12, 14–18, 20–23: 54 verses read from the PAGE IMAGES,
    each matched on its own condition and returned whole with the clause that fired and a
    "why it applies" line in EN + HI (`analysis.bhava_effects`; graha names travel as
    `{g:key}` placeholders the page fills). Its docstring is the register of what is NOT
    there and why: ch.19 (longevity), every verse that dates an event to an age, verses on
    a spouse's character / fidelity / number of wives / illegitimate birth, verses needing
    "strength", a navāṁśa, Māndi or combustion, the counting verses, and ch.15 v.3 (the
    translation prints "5th lord" where the Sanskrit on the page has the 4th lord).
    "Aspected" = a FULL graha dṛṣṭi; benefic/malefic = natural (ch.3 v.11).
    `test_bhava_effects.py`.
  - `api/phaladipika_lagna_rules.py` — Phaladīpikā 9.1-13: the description of each sign
    rising, and (śl.13) the same description for the Moon's sign (`analysis.character`). It
    feeds the simple view's "Who you are" card (`WhoCard` in SimpleView.jsx), which also
    lists the registered Moon-in-sign readings. ⚠ confidence `ocr_text`, like the node
    verses. ⚠ The descriptions are shown WHOLE — these texts are often unflattering
    ("a doer of wrong in secret"); do not trim them into praise. English only so far.
- References: Settings › References (off by default; the same `refs` switch as /references).
  Off — a passage carries NO attribution line at all (the owner asked for the "A classical
  text" label to go), no tier names and no reference list; on — everything is named. Either
  way a passage sits under a "What the classical texts say" heading, never as ours.
- Daśā reading (`web/src/dashareading.js` + `DashaReading.jsx`, `node web/test_dashareading.mjs`):
  the simple view's "Your periods (daśā): now, next, and what it means" — how to read a
  daśā · the running main and sub-period · the next sub-period and the next main period (each:
  dates, which houses its planet rules and sits in, and the lean by BPHS Vol II ch.47 vv.5-6
  from `dasha.verdicts`) · the verse itself · what is going to change · practical notes.
  "What changes" and the notes are OURS, under the life-area notes' rules.
  The running and the next sub-period also show the text's own result lists (chs 52-60),
  from `POST /api/antardasa/plain` (`api/antardasa_plain.py`, `test_antardasa_plain.py`):
  the cell's rows grouped into BRANCHES (a row with its own list + the rows marked "as
  above"), a branch applying only when an alternative AND every required conjunct is met;
  the four plain sign-dignity conditions are tested there (the raw engine marks them
  unavailable); the māraka clause and the remedy never travel. Still no verdict, and neither
  "what changes" nor the notes draw on these lists. ⚠ The ch.52-60 result texts carry OCR
  slips from the original mining ("acquidtion", "rl'ife"); they are shown as registered —
  re-verify against the Vol II page images (now in `C:\books\astro`) rather than hand-fix. ⚠ Its CSS classes are `dsr-*` — `dr-*` is the
  dṛṣṭi ledger's and clashes.
- Life areas (`web/src/lifeareas.js` + `LifeAreas.jsx`, `node web/test_lifeareas.mjs`): the
  simple view's "Your life, area by area" — you, career, wealth, marriage, home, children
  and learning. Per area: what the chart shows · the registered passages tied to its houses
  (each passage carries `house`) · the factors on the house lords · when a period tied to
  the area runs or next begins · PRACTICAL NOTES. ⚠ The notes are OURS, the owner's choice
  for "what you can do" (2026-11-16) over the texts' remedies: attention, planning and
  timing only — never a ritual, gem or charity (the site still says "No remedies"), never
  medical / legal / financial instructions, never what will happen. No health area; the
  8th house is in no area. The test pins all of this.
- Not yet registered: ch.13 vv.8+; verse numbers for the seven grahas in Phaladīpikā ch.8
  (still cited to the chapter); Phaladīpikā's daśā chapters (19–21). A web page's machine translation is not a source:
  extract from the registered edition, verify, then register.
- To read a scanned page: extract its image with pypdf + Pillow and Read the image (see the
  BPHS extraction); `Read` on a PDF needs poppler, which is not installed.

## Sharing a chart (`/c/<id>#<key>`)

By default a link carries the finished chart WITHOUT its birth details
(`shareCodec.js snapshotOf`: an allowlist of chart fields, then a sweep for
anything that reads like a date, time, zone or Julian day). A new top-level
field in `/api/chart` is NOT shared until it is added to `SNAPSHOT_KEYS`. The
recipient's view (`snap` in `App.jsx`) hides every panel that needs the birth
details. Test: `node web/test_share.mjs` (with the local API up it checks the
real reference chart).

## Deploying

- **Backend → Render**: `git push origin main`. Render redeploys automatically
  (~2–3 min). Verify with a real request before claiming it is live.
- **Frontend → Cloudflare**: from `web/`,
  `VITE_API_URL=https://devashaa-api.onrender.com VITE_SOURCE_URL=https://github.com/sansbug/devashaa VITE_SUPPORT_URL=https://donate.stripe.com/6oU28t3KwcdRg3YasQ9Ve00 npm run deploy`
  (`VITE_SUPPORT_URL` is the Stripe Payment Link behind /support — the same link as globalmacrolens.com's Support page; a `/test_` link is never shown on the live host.)
  ⚠ Copy that line exactly — a typo in `VITE_API_URL` bakes a dead API into the
  live site.
- ⚠ **Frontend-only work still needs `git push`.** Cloudflare deploys from the
  build, not from git, so commits can silently pile up unpushed.
- Only stage specific paths (`git add api/x.py web/src/y.jsx`), never `git add
  -A` — a dev server from another session may share this working tree. Run
  `git add` from the repo root, not from `web/`.

## Gotchas that have cost real time

- `matrix.py` has **two** copies of the ensemble math (`timeline()` and
  `_project_at()`). A parity test pins them bit-for-bit — change both or it fails.
- Yoga catalog keys contain **spaces** ("Gajakesari Yoga"); rāśi indexes are
  0-based, houses 1-based; graha keys are lowercase English (`jupiter`, not
  `guru`).
- Transit payloads from `/api/gochara` carry **keys only, no display names** —
  use `namer.grahaKey(key)`.
- React's synthetic `onPointerEnter` fires from bubbling `pointerover`;
  dispatching a non-bubbling `pointerenter` in a test does nothing.
- FRED-style parallel probing of upstream APIs is not a concern here, but
  Render cold-starts: allow ~60s on the first request after idle.

## Not in this repo

Source-book PDFs (extraction inputs), the Python venv, and Render/Cloudflare
credentials live only on the desktop workstation. Extraction workflows that need
a PDF cannot run from a cloud session without that file.
