> Ops reference for keeping devashaa.com reachable on corporate networks and well indexed.
> Compiled 2026-07-23 (web-verified across 12 filter vendors + Google/Bing).
>
> **Already done on-site (commit a553c83, live):** robots.txt, sitemap.xml,
> canonical + robots meta, educational/reference description + keywords, a
> general-audience content rating, Open Graph + Twitter cards, JSON-LD
> (WebSite / Organization / WebApplication = EducationalApplication, free), and a
> <noscript> block of crawlable text. Those are the *on-site* signals; the vendor
> submissions below are actions the site owner must take (the forms need your email).

# devashaa.com — Web-Filter Categorization & Indexing Playbook

## 1. Honest reality check

The true, accurate category of devashaa.com is **astrology / alternative-beliefs** (with a legitimate secondary claim to education / reference / religion-spirituality because it is a scholarly, citation-backed Jyotiṣa reference). A minority of enterprise, K-12/CIPA, government, and faith-based networks block that topic **as a matter of policy** — that is their acceptable-use choice, it is legitimate, and it **cannot and should not be evaded** by asking to be filed under a category the site is not. **However**, that policy block is almost never why a brand-new small site is unreachable. The far more common cause — and the exact symptom of a domain live only since 2026-07-18 — is being tagged **"uncategorized," "newly registered domain (NRD)," or "newly seen domain,"** which many enterprises block by *default*. Submitting devashaa.com for accurate categorization at each major vendor is precisely the fix: it moves the site out of the "unknown/newborn" bucket into a real, mostly-allowed content category. The NRD/newly-seen flags additionally **age out on their own ~30 days after go-live** (roughly 2026-08-17 to 2026-08-19), so a re-check in late August is worthwhile regardless.

## 2. Prioritized vendor table (highest enterprise footprint first)

| Vendor | Enterprise footprint | Lookup URL | Submit / dispute URL | Likely auto-category | Block-prone | Verification needed |
|---|---|---|---|---|---|---|
| **Zscaler (ZIA / ThreatLabz)** | Very large (SSE leader; Fortune 500, finance, gov) | https://sitereview.zscaler.com/ | https://sitereview.zscaler.com/ (same page) | Alt/New Age (super-cat: Religion) | Medium | None — public tool; email optional (status updates) |
| **Cisco Talos** (Umbrella / SWA / Secure Access) | Very large (Umbrella, WSA, Secure Access, Secure Firewall) | https://talosintelligence.com/reputation_center | https://talosintelligence.com/reputation_center/web_categorization | Astrology | Low | Free Cisco.com (CCO) / guest account required to submit & track |
| **Palo Alto Networks (PAN-DB)** | Very high (NGFW + Prisma Access SASE) | https://urlfiltering.paloaltonetworks.com/ | https://urlfiltering.paloaltonetworks.com/ (Request Change link, same page) | Reference and Research | Low | None for single URL (email + CAPTCHA); free CSP login skips CAPTCHA |
| **Broadcom / Symantec (Blue Coat WebPulse / BCWF)** | Very large (ProxySG / Edge SWG / Cloud SWG) | https://sitereview.bluecoat.com/#/ | https://sitereview.bluecoat.com/#/ (Submit for Review, same page) | Alternative Spirituality/Belief | Low | None for single URL; requires email + CAPTCHA |
| **Forcepoint** (Web Security / ONE SWG / NGFW) | High (large corp, gov, K-12/higher-ed; OEM'd into WatchGuard) | https://csi.forcepoint.com | https://support.forcepoint.com/s/site-lookup | Non-Traditional Religions and Occult and Folklore | Medium | None for single request (guest access); Customer Hub login only for bulk |
| **Fortinet (FortiGuard Labs)** | Very large (FortiGate / FortiProxy web filtering) | https://www.fortiguard.com/webfilter | https://www.fortiguard.com/faq/wfratingsubmit | Folklore | Low | None — public form (Name, Email, Company required); no account |
| **Netskope** (One SWG / Web Content Filtering) | High (SSE Leader) | https://www.netskope.com/url-lookup | https://www.netskope.com/url-lookup (Report Miscategorization, same page) | Education | Low | None for public page; valid email required; no customer login needed |
| **Trellix / Skyhigh (TrustedSource)** | Very large (Trellix Web Gateway + Skyhigh SWG; ex-McAfee) | https://trustedsource.org/en/feedback/url?action=checksingle | https://trustedsource.org/en/feedback/url | Education/Reference | Low | Lookup anonymous; **free TrustedSource.org account required to submit** |
| **Sophos** (Firewall / UTM / Central Web Control / DNS) | Moderate-to-significant (strong in SMB/mid-market, education) | https://intelix.sophos.com/ | https://www.sophos.com/reporturl (→ support.sophos.com/support/s/filesubmission) | Religion | Low | Free Sophos ID for lookup portal & appeal |
| **Barracuda** (Web Security Gateway / Content Shield / CloudGen) | Mid-tier but common in SMB, K-12, higher-ed | https://www.barracudacentral.org/lookups | https://www.barracudacentral.org/report | Horoscope, Astrology, or Fortune Telling | Medium | None — public form + CAPTCHA |
| **Cloudflare** (Gateway / Radar / 1.1.1.1 for Families) | Very large (Gateway/Zero Trust; blocks no content category by default) | https://radar.cloudflare.com/domains/domain/devashaa.com | https://radar.cloudflare.com/domains/feedback | Astrology (ID 72) | Low | None for public feedback form; email optional; free CF account for Security Center path |
| **Google & Bing** (indexing + Safe Browsing / SmartScreen — *not a topic filter*) | Enormous but indirect (safety/reputation, not category) | https://transparencyreport.google.com/safe-browsing/search | https://search.google.com/search-console (indexing) | N/A — clean safety verdict, no topic label | Low | Free account + domain-ownership verification (DNS TXT via Cloudflare) for indexing |

*Block-prone reflects the **target/likely** category. The overriding near-term risk for all vendors is the newly-registered / uncategorized state, which is why simply getting classified into any legitimate category is the win.*

## 3. "Do this first" checklist (highest leverage)

1. **Zscaler** → https://sitereview.zscaler.com/ — check current state, then suggest **Reference Sites (Education) + Alt/New Age (Religion)** (up to 3 allowed; add Traditional Religion). Highest-impact because Zscaler blocks NRD/unknown by default across huge enterprise footprint.
2. **Cisco Talos** → create a free Cisco ID, file a **Content** categorization request (NOT Security) at https://talosintelligence.com/reputation_center/web_categorization — lead with **Astrology**, note educational/reference nature in comments.
3. **Palo Alto Test-A-Site** → https://urlfiltering.paloaltonetworks.com/ — search, click **Request Change**, propose **Reference and Research (primary) + Religion (secondary)**.
4. **Broadcom / Symantec Blue Coat** → https://sitereview.bluecoat.com/#/ — look up, then **Submit for Review** with **Alternative Spirituality/Belief + Reference (or Education)**.
5. **Fortinet FortiGuard** → https://www.fortiguard.com/faq/wfratingsubmit — request **Folklore** (astrology's home category, default-allow). **Explicitly do NOT accept "Alternative Beliefs"** (that one sits under Adult/Mature Content and is far more block-prone).
6. **Cloudflare Radar** → https://radar.cloudflare.com/domains/feedback — propose **Education (ID 6) + Astrology (ID 72)** (max 2 content categories; use Religion ID 19 as the alternate secondary).
7. **Google Search Console** (https://search.google.com/search-console) + **Bing Webmaster Tools** (https://www.bing.com/webmasters) — add devashaa.com as a **Domain property**, verify via a **DNS TXT record at Cloudflare**, submit `https://devashaa.com/sitemap.xml`, and Request Indexing on the homepage + key reference pages. In Bing, use "Import from Google Search Console." Confirm a clean Safe Browsing status at https://transparencyreport.google.com/safe-browsing/search?url=devashaa.com (no submission needed unless flagged).

*After the top 6 filter vendors, repeat the same accurate submission at the remaining ones (Forcepoint, Netskope, Trellix/Skyhigh, Sophos, Barracuda) — each maintains an independent database, so a fix at one does not carry to the others.*

## 4. Which categories to REQUEST (where the taxonomy allows a choice)

Guiding rule: **request the most accurate label that is least likely to be blocked** — prefer **Education / Reference / Religion / Society** over "Occult"-flavored buckets — but **never claim a category the site is not.** Most vendors accept 2–4 categories, so pair an accurate scholarly label with the honest topical one.

- **Zscaler (up to 3):** Reference Sites (Education) + Alt/New Age (Religion) + optionally Traditional Religion. (Zscaler has no astrology category; Alt/New Age is where it maps.)
- **Cisco Talos:** Astrology is the label most likely to stick (Talos categorizes by primary topic and has an explicit *Astrology* category). Lead with it, but argue Education / Reference / Religion in the comment box.
- **Palo Alto (up to 4):** **Reference and Research (primary) + Religion (secondary)**. No astrology category exists in PAN-DB; these are the accurate fits. Avoid "Personal Sites and Blogs."
- **Broadcom/Symantec (up to 2):** Alternative Spirituality/Belief (the honest topical fit — Symantec reserves "Religion" for organized religions) + Reference or Education.
- **Forcepoint:** Argue **Educational Materials** or **Reference Materials** as primary (cite Swiss Ephemeris + BPHS scholarship). If reviewers insist on a religion bucket, push for **Traditional Religions** (Hindu/Vedic scriptural basis) over the default "Non-Traditional Religions and Occult and Folklore."
- **Fortinet:** Request **Folklore** (astrology/horoscopes live here, default-allow) and/or **Reference / Education**. **Actively argue against "Alternative Beliefs"** (Adult/Mature Content parent, commonly blocked).
- **Netskope:** Education (primary) + Religion (topical secondary); add Reference and Research / Lifestyle if offered. No astrology category exists.
- **Trellix/Skyhigh:** Education/Reference (primary, near-zero block rate) + Religion/Ideology (accurate secondary). Submit to **both** the Trellix Real-Time DB and Skyhigh SWG (now separate databases).
- **Sophos:** Actively request **Education / Reference** (default-allow); Religion is the likely auto-label but Education/Reference reduce block risk.
- **Barracuda:** The exact-match label "Horoscope, Astrology, or Fortune Telling" is accurate and analysts will likely assign it; request **Reference / Education** as primary and note the scholarly, non-commercial nature to lower block risk.
- **Cloudflare (max 2):** Education (ID 6) + Astrology (ID 72), or Education + Religion (ID 19). Avoid Personal Blogs (ID 129).

## 5. Caveats

**URLs not directly confirmable by the automated fetcher this run** (all corroborated via official docs/search, but flagged for honesty — re-verify in a browser before relying on them):
- **Forcepoint** — `csi.forcepoint.com` failed DNS resolution from the fetch tool, and the Salesforce-hosted `support.forcepoint.com/s/site-lookup` returned CSS/JS load errors; existence corroborated only by search results and Forcepoint KB references, not a successful direct fetch.
- **Cisco Talos** — `talosintelligence.com` pages returned HTTP 403 (anti-bot) to the fetcher; the host/paths resolved and are corroborated by Cisco/Umbrella docs, but the pages were not directly readable this run.
- **Cloudflare Radar** — the Radar HTML pages (`radar.cloudflare.com/domains/...`) returned HTTP 403 to the fetcher; URLs/IDs were confirmed against Cloudflare's official developer docs and category reference rather than a live page fetch.
- Minor: Zscaler's `help.zscaler.com` articles rendered empty (JS-only) so field wording came from help-doc snippets + the downloadable URL-categories CSV; the `sitereview.zscaler.com` tool itself is a well-known public page. Several portals (Blue Coat, Netskope, Radar) are JavaScript SPAs that render blank to simple fetchers even when live.

**"Ask IT to allowlist" path (for orgs that block the category by policy):** Some enterprises, schools (CIPA), governments, and faith-based networks deliberately block astrology / Alt-New-Age / Occult / Folklore categories as acceptable-use policy. That is legitimate and must not be circumvented by requesting a false category. The honest remedy is per-organization: an affected user asks **their own IT/security team** to add `devashaa.com` (or `*.devashaa.com`) to the organization's **URL allowlist / policy exception**, supplying the accurate description — *"free, non-commercial educational Vedic astrology (Jyotiṣa) birth-chart calculator and BPHS reference; sidereal charts via Swiss Ephemeris; no ads, no gambling, no adult content, no payments; optional encrypted profile-save is the only account feature."* This is the correct, above-board channel and it works even where the category is intentionally blocked.

**Categorization ≠ indexing.** None of the filter-vendor submissions affect Google/Bing search visibility, and vice versa. Handle indexing separately (Search Console + Bing Webmaster Tools + sitemap + Schema.org structured data such as WebSite / EducationalOrganization / Article). Because the frontend is a Cloudflare Worker static-asset / React app, **ensure the Worker serves crawlable HTML** (title, meta description, visible scholarly text, robots.txt allowing crawl) — a thin JS-only shell can push a site toward "Insufficient Content"/"Unknown" with both filter crawlers and search engines; consider prerendering/SSR for key reference pages.

**Timing:** Palo Alto's NRD flag clears ~32 days after go-live (~2026-08-19); Cloudflare's New Domains / Newly Seen Domains flags clear ~30 days after first registration/resolution (~2026-08-17). Re-check every portal in **late August 2026** to confirm the new categories propagated and the newborn-domain flags have aged out; resubmit with clarifying comments where still wrong.


---

## 6. Ready-to-paste submission blocks — top 4 vendors

Justification text is plain ASCII (no diacritics) so older enterprise forms do not mangle it.
For each: open the URL, enter the domain, tick the listed categories, paste the block into the
comment / justification box, submit.

### 1. Zscaler — https://sitereview.zscaler.com/  (no login)
Enter `devashaa.com`; tick up to 3: **Reference Sites** + **Alt/New Age** + **Traditional Religion**; add email for status.

```
devashaa.com is a free, non-commercial educational Vedic astrology (Jyotisha)
birth-chart calculator and reference. It computes sidereal charts using the Swiss
Ephemeris and follows the classical Sanskrit text Brhat Parasara Hora Sastra with
scholarly citations. There are no ads, no gambling, no adult content, and no
payments; an optional encrypted profile-save is the only account feature. Please
categorize it under Reference Sites (Education), Alt/New Age, and Traditional Religion.
```

### 2. Cisco Talos — https://talosintelligence.com/reputation_center/web_categorization  (free Cisco ID)
Enter `devashaa.com` -> Get Category Data; ticket type = **Content** (NOT Security); suggest **Astrology**.

```
devashaa.com is a free, non-commercial educational Vedic astrology (Jyotisha)
birth-chart calculator and reference. It computes sidereal charts using the Swiss
Ephemeris and follows the classical Sanskrit text Brhat Parasara Hora Sastra with
scholarly citations. There are no ads, no gambling, no adult content, and no
payments; an optional encrypted profile-save is the only account feature. Its
primary topic is Astrology; it also fits Education, Reference, and Religion. Please
assign the Astrology content category.
```

### 3. Palo Alto (PAN-DB) — https://urlfiltering.paloaltonetworks.com/  (email + CAPTCHA, or free CSP login)
Search `devashaa.com` -> Request Change; suggest up to 4: **Reference and Research** (primary) + **Religion**.

```
devashaa.com is a free, non-commercial educational Vedic astrology (Jyotisha)
birth-chart calculator and reference. It computes sidereal charts using the Swiss
Ephemeris and follows the classical Sanskrit text Brhat Parasara Hora Sastra with
scholarly citations. There are no ads, no gambling, no adult content, and no
payments; an optional encrypted profile-save is the only account feature. PAN-DB has
no astrology category, so please categorize it as Reference and Research (primary)
and Religion (secondary).
```

### 4. Broadcom / Symantec (Blue Coat) — https://sitereview.bluecoat.com/#/  (email + CAPTCHA)
Check `https://devashaa.com` -> Submit for Review; suggest up to 2: **Alternative Spirituality/Belief** + **Reference** (or **Education**).

```
devashaa.com is a free, non-commercial educational Vedic astrology (Jyotisha)
birth-chart calculator and reference. It computes sidereal charts using the Swiss
Ephemeris and follows the classical Sanskrit text Brhat Parasara Hora Sastra with
scholarly citations. There are no ads, no gambling, no adult content, and no
payments; an optional encrypted profile-save is the only account feature. Please
categorize it under Alternative Spirituality/Belief plus Reference (or Education).
```

*Reminders: Cisco needs the free account before submitting; Palo Alto and Broadcom require a
CAPTCHA. Re-look-up each domain after a few days to confirm the change took, and resubmit with
more detail if not. Each vendor is a separate database — repeat per vendor for full coverage.*
