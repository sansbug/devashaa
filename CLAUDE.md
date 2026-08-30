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

## Deploying

- **Backend → Render**: `git push origin main`. Render redeploys automatically
  (~2–3 min). Verify with a real request before claiming it is live.
- **Frontend → Cloudflare**: from `web/`,
  `VITE_API_URL=https://devashaa-api.onrender.com VITE_SOURCE_URL=https://github.com/sansbug/devashaa npm run deploy`
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
