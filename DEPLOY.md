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

## Known limits before real traffic

- **Geocoding**: `/api/places` uses the free public Nominatim endpoint, which
  OSM's policy forbids for production load (~1 req/s). Before you promote the
  site, swap in an offline GeoNames `cities15000` dump or a paid geocoder —
  only `api/geocode.py::search()` has to change.
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
