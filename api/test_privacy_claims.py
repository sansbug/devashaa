"""Guards for the promises published at https://devashaa.com/privacy.

Run: python api/test_privacy_claims.py

WHY THIS FILE EXISTS
--------------------
The privacy page's boldest claim — "nothing from that request is written to
disk or to any database" — is protected by nothing except the current absence
of code. Every other claim has something structural behind it: the encryption
key is non-extractable and never exists server-side, the places database is
opened with SQLite's own `mode=ro`, the no-third-party-scripts claim is guarded
by a two-dependency package.json.

That one is guarded by a habit, and habits decay silently. It fails to a
one-line change nobody would flag as a privacy decision:

    logging.info(f"chart for {lat},{lon}")     while chasing a timezone bug
    --access-logfile -                          while chasing a Render timeout
    import sentry_sdk                           after an error report

Each is a normal engineering reflex, none touches a file named privacy, and
each makes a published promise false in production while every other test still
passes.

This is not hypothetical. The header comment in web/src/profiles.js asserted
"this app has no accounts and no user database" long after accounts shipped,
and that stale comment is where the first draft of the privacy page got its
false "never transmitted" wording. A comment could not stop that. A failing
build can.

IF ONE OF THESE FAILS, the fix is not to weaken the test. It is to decide
whether the code change is wanted, and if it is, to update /privacy in the same
commit.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(os.path.dirname(HERE), "web")

fails = []


def check(label, cond, detail=""):
    if not cond:
        fails.append(label)
    print(f"  {'PASS' if cond else '**FAIL**'}  {label}{('  ' + detail) if detail else ''}")


def read(*parts):
    with open(os.path.join(*parts), encoding="utf-8") as fh:
        return fh.read()


def code_only(src, sql=False):
    """Strip comments and prose so the checks match CODE, not commentary.

    The first version of this file matched raw text and produced three false
    failures: the privacy page's own sentence "no analytics", worker.js's
    header explaining the password derivation, and — best of all — the schema
    comment stating that the profile_id column MUST NOT hold birth data. A test
    that fires on the comment warning against a thing, rather than the thing,
    is not a strict test; it is a broken one that trains people to ignore it.
    """
    src = re.sub(r"/\*[\s\S]*?\*/", "", src)          # /* block */
    src = re.sub(r"^\s*//.*$", "", src, flags=re.M)     # // line
    src = re.sub(r"\{/\*[\s\S]*?\*/\}", "", src)      # {/* jsx */}
    if sql:
        src = re.sub(r"--.*$", "", src, flags=re.M)
    return src


# Modules reachable from a chart request. build_geonames.py is an offline build
# script app.py never imports, so it is deliberately excluded.
REQUEST_PATH = ["app.py", "vedic.py", "vargas.py", "geocode.py", "dignity.py",
                "analysis.py", "dasha_effects.py", "antardasa.py", "drishti.py",
                "functional.py", "vimsopaka.py", "avastha.py", "karakas.py",
                "relationships.py", "dashas.py", "vimshottari.py", "rasis.py"]

print('"Nothing from that request is written to disk or to any database":')
for mod in REQUEST_PATH:
    path = os.path.join(HERE, mod)
    if not os.path.exists(path):
        continue
    src = read(path)
    # Strip comments and docstrings crudely — this file's own prose mentions
    # `open(` and `logging`, and so do several module docstrings.
    code = re.sub(r'"""[\s\S]*?"""', "", src)
    code = re.sub(r"^\s*#.*$", "", code, flags=re.M)
    bad = []
    if re.search(r"\bopen\s*\(", code) and "geonames" not in mod:
        bad.append("open(")
    if re.search(r"\.write\s*\(", code):
        bad.append(".write(")
    if re.search(r"\b(INSERT|UPDATE|DELETE)\s+(INTO|FROM|\w)", code, re.I):
        bad.append("SQL write")
    if re.search(r"^\s*import\s+logging|^\s*from\s+logging\b", code, re.M):
        bad.append("logging")
    check(f"{mod} performs no write and no logging", not bad, ", ".join(bad))

print("\nThe chart API can reach no third party, even by accident:")
NET = r"^\s*(import|from)\s+(requests|httpx|urllib|urllib3|http\.client|socket|aiohttp)\b"
for mod in REQUEST_PATH:
    path = os.path.join(HERE, mod)
    if os.path.exists(path):
        code = re.sub(r'"""[\s\S]*?"""', "", read(path))
        check(f"{mod} imports no HTTP client", not re.search(NET, code, re.M))
reqs = read(HERE, "requirements.txt").lower()
check("requirements.txt installs no HTTP client library",
      not any(p in reqs for p in ("requests", "httpx", "aiohttp", "urllib3")),
      reqs.replace("\n", " ")[:80])
check("...and no error-reporting SDK that would ship request data offsite",
      not any(p in reqs for p in ("sentry", "bugsnag", "rollbar", "datadog")))

print('\n"The places database is opened strictly read-only":')
geo = read(HERE, "geocode.py")
check("sqlite is opened with mode=ro, enforced by the driver",
      "mode=ro" in geo and "uri=True" in geo)

print("\nThe server keeps no access log of its own:")
docker = read(HERE, "Dockerfile")
check("gunicorn is not started with --access-logfile", "--access-logfile" not in docker)
check("...and Flask debug is not enabled in the image", "FLASK_DEBUG" not in docker)

print('\n"No cookies, no analytics, no trackers, no third-party scripts":')
html = read(WEB, "index.html")
offsite = re.findall(r'(?:src|href)="(https?://[^"]+)"', html)
check("index.html loads nothing from another origin", not offsite, str(offsite))
pkg = read(WEB, "package.json")
deps = re.search(r'"dependencies"\s*:\s*\{([^}]*)\}', pkg)
names = re.findall(r'"([^"]+)"\s*:', deps.group(1)) if deps else []
check("the app has exactly two runtime dependencies: react, react-dom",
      sorted(names) == ["react", "react-dom"], str(names))
src_all = "".join(code_only(read(WEB, "src", f))
                  for f in os.listdir(os.path.join(WEB, "src"))
                  if f.endswith((".js", ".jsx")))
check("nothing anywhere writes a cookie", "document.cookie" not in src_all)
# Match CALLS and IMPORTS, not bare words. The privacy page's own sentence is
# "no analytics, no trackers" — a substring test flags the page for promising
# the very thing it is checking, which is how a guard earns a reputation for
# crying wolf and stops being read.
TRACKERS = r"""(?xi)
    \bgtag\s*\(          | \bfbq\s*\(        | \bga\s*\(
  | googletagmanager     | google-analytics
  | \banalytics\s*[.(]   | \bposthog\s*[.(]  | \bmixpanel\s*[.(]
  | \bhotjar\s*[.(]      | \bSentry\s*[.(]
  | from\s+['"][^'"]*(analytics|posthog|mixpanel|sentry|hotjar)
"""
hits = re.findall(TRACKERS, src_all)
check("no analytics or tracker call anywhere in the client", not hits, str(hits[:3]))

print("\nThe four browser storage keys the page enumerates, and no more:")
keys = set(re.findall(r"localStorage\.(?:set|get|remove)Item\(\s*['\"`]([^'\"`]+)", src_all))
# Two are held in constants rather than literals; resolve those the same way a
# reader of the page would have to.
consts = dict(re.findall(r"const\s+(REMEMBER|KEY)\s*=\s*'([^']+)'", src_all))
keys |= set(consts.values())
EXPECTED = {"theme", "nameStyle", "devashaa.acct", "devashaa.profiles"}
check("localStorage keys are exactly the documented four",
      keys == EXPECTED, f"found {sorted(keys)}")
check("no sessionStorage", "sessionStorage" not in src_all)
check("no IndexedDB", "indexedDB" not in src_all)
check("no service worker (which could cache chart responses offline)",
      "serviceWorker" not in src_all)

print("\nThe account server never receives a key or a password:")
acct = read(WEB, "src", "account.js")
check("the encryption key is imported non-extractable",
      re.search(r"importKey\(\s*'raw',\s*encBits,[^)]*false", acct) is not None)
check("...and so is the profile-id key",
      re.search(r"importKey\(\s*'raw',\s*idBits,[^)]*false", acct) is not None)
worker = code_only(read(WEB, "worker.js"))
# The point is that the Worker never RECEIVES or handles a password value —
# not that the word is absent. It legitimately appears in the login failure
# message, and a check that forbade that would be forbidding good UX.
check("the Worker never reads a password from a request",
      not re.search(r"""(?xi)
          body\s*[?.]?\.\s*password        # body.password
        | \bpassword\s*[:=]               # a password field or variable
        | ['"]password['"]\s*\]           # body["password"]
      """, worker),
      "|".join(re.findall(r"(?i)\bpassword\b\s*[:=\]]", worker))[:60])
check("...and the only mention of the word is the login failure message",
      worker.lower().count("password") == 1)
_profiles_table = code_only(read(WEB, "schema.sql"), sql=True) \
    .split("CREATE TABLE IF NOT EXISTS profiles")[1].split(";")[0]
check("the profiles table has no column that could hold plaintext birth data",
      not re.search(r"\b(name|birth|date|time|lat|lon|place)\b", _profiles_table, re.I),
      " ".join(_profiles_table.split())[:70])

print("\n" + ("ALL PASS" if not fails else f"FAILURES: {fails}"))
if fails:
    print("\nA published promise at https://devashaa.com/privacy may now be false.")
    print("Do not weaken this test. Decide whether the change is wanted, and if")
    print("it is, update web/src/Privacy.jsx in the same commit.")
sys.exit(1 if fails else 0)
