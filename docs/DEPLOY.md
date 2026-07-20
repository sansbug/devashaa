
## Accounts (Cloudflare D1)

`web/worker.js` serves `/api/account*` from D1 `devashaa-accounts`
(`79419998-8d92-4b28-9bc0-cddd7bd0d193`). Schema in `web/schema.sql`; apply with

    npx wrangler d1 execute devashaa-accounts --remote --file=./schema.sql

**The database holds no personal data.** A userid, a hash of a password
verifier, and AES-GCM ciphertext. The encryption key is derived on the client
and never transmitted, so the server cannot read a profile — architecturally,
not by policy. There is no password reset because there is no email on file.

Storage is on the Worker rather than the Python API because Render's free plan
has an ephemeral filesystem: anything written there is destroyed on redeploy.
D1 rather than KV because a unique userid needs a real PRIMARY KEY — KV has no
atomic check-and-set, so two simultaneous registrations could both see "free".

**Gotcha:** with `assets` configured, Cloudflare answers from the asset layer
first, and `not_found_handling: single-page-application` serves index.html with
a 200 for any unmatched path — including `/api/*`. `assets.run_worker_first`
must list the API prefixes or the Worker never runs. This behaves correctly
under `wrangler dev` and fails only once deployed.
