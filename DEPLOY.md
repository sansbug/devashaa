# Deploying devashaa.com

Architecture: **Cloudflare Pages** serves the React frontend on your domain;
**Render** runs the Flask + Swiss Ephemeris backend in Docker.

The backend cannot run on Cloudflare — Swiss Ephemeris (`pyswisseph`) is a
compiled C library, and Cloudflare Workers run only JS/WASM. Hence the split.

---

## 0. Push to a git repo (both hosts deploy from git)

```bash
cd C:\proj\astrodev
git init
git add .
git commit -m "Vedic astrology engine: BPHS charts, vargas, dashas"
git branch -M main
git remote add origin https://github.com/<you>/devashaa.git
git push -u origin main
```

`.gitignore` already excludes `.venv/`, `node_modules/`, `dist/`. The `.se1`
ephemeris files ARE committed — the backend image needs them.

**AGPL:** keep this repo public and point `VITE_SOURCE_URL` at it (step 2).
That satisfies Swiss Ephemeris' AGPL source-offer for a public site. Buy the
commercial licence only when you want the source closed.

---

## 1. Backend → Render

1. [dashboard.render.com](https://dashboard.render.com) → **New → Blueprint**
2. Connect the repo. Render reads `render.yaml` and creates the `devashaa-api`
   Docker service (builds `api/Dockerfile`).
3. Deploy. Note the URL, e.g. `https://devashaa-api.onrender.com`.
4. Verify: open `https://<your-api>/api/health` — it must report
   `"status": "ok"` and `Swiss Ephemeris .se1 (JPL DE431)`.
   If it says `degraded`, the `.se1` files did not make it into the image.

> **Free tier caveat:** the service sleeps after ~15 min idle, so the first
> request afterwards takes ~30–60 s to wake. For a public site that's a bad
> first impression — either use a paid instance ($7/mo) or ping `/api/health`
> every 10 min from a cron.

---

## 2. Frontend → Cloudflare Pages

1. Cloudflare dashboard → **Workers & Pages → Create → Pages → Connect to Git**
2. Select the repo, then set **build settings**:
   - Framework preset: **Vite**
   - Build command: `npm run build`
   - Build output directory: `dist`
   - **Root directory: `web`**  ← important, the app is in a subfolder
3. **Environment variables (Production)**:
   | Name | Value |
   |---|---|
   | `VITE_API_URL` | your Render URL, no trailing slash |
   | `VITE_SOURCE_URL` | your public repo URL (AGPL) |
4. Save and Deploy. You'll get a `*.pages.dev` URL — check the chart works.

---

## 3. Point devashaa.com at it

Pages project → **Custom domains → Set up a custom domain** → `devashaa.com`
(repeat for `www.devashaa.com`). Since the domain is already in your Cloudflare
account, DNS records are created automatically; SSL is issued in a few minutes.

---

## 4. Lock down CORS (do this last)

On Render → `devashaa-api` → Environment, set:

```
ALLOWED_ORIGINS = https://devashaa.com,https://www.devashaa.com
```

Redeploy. Until you set this it defaults to `*` (any site can call your API).

> **Gotcha:** once `ALLOWED_ORIGINS` is restricted, your *local* dev frontend
> (`http://localhost:5175`) is blocked by the deployed backend. Keep local dev
> pointed at your local backend (which defaults to `*`), or add localhost to the
> list while developing.

---

## Place lookup is fully offline

`/api/places` queries `api/data/geonames.sqlite3` — 69,417 cities from the
GeoNames `cities5000` dump, committed to the repo. No network call, no rate
limit, no API key, ~0.05 ms per lookup. Historical names resolve too (Benares →
Varanasi, Bombay → Mumbai, Madras → Chennai), which matters because birth
records often use them.

Each record carries its own IANA timezone, so a picked place needs no timezone
lookup at all.

To rebuild (e.g. to widen coverage with `cities1000`), download the dumps from
<https://download.geonames.org/export/dump/> and run:

```bash
python api/build_geonames.py <folder-with-dumps>
```

**Attribution is required**: GeoNames is CC BY 4.0 and the site footer credits
it. Keep that credit if you restyle the footer.

## Known limits before real traffic

- **Place coverage**: `cities5000` means towns under ~5,000 people are missing.
  Rebuild with `cities1000` if users report their birth village is absent.
- **Ephemeris range**: the loaded `.se1` files cover **1800–2399**. Births
  outside that are rejected with a clear error; add the adjoining files to widen.
- **Render cold starts** on the free tier (above).

---

## Local development (unchanged)

```bash
# backend
C:\proj\astrodev\.venv\Scripts\python.exe api\app.py     # :5174

# frontend
cd web && npm run dev                                     # :5175
```

With no `VITE_API_URL` set, the frontend falls back to `http://127.0.0.1:5174`.
