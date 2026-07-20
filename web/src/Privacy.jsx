/**
 * Privacy page, served at /privacy (the Worker's SPA fallback makes the path
 * work without a router).
 *
 * EVERY CLAIM HERE WAS AUDITED AGAINST THE CODE, AND THE FIRST DRAFT FAILED.
 * Eleven statements were false, overstated, or omitted a real data flow —
 * including "we never ask for your name" (there is a name field), "queried
 * locally" (the place search is a live request to our server on every
 * keystroke), and "never transmitted" (re-opening a saved chart re-sends it).
 *
 * So: do not edit this page from memory of how the system works. Check.
 * If you change what leaves the browser, what the API receives, or what the
 * accounts database holds, this page is part of that change.
 *
 * The hedges are load-bearing and were added because the unhedged version was
 * false:
 *   - birth details ARE sent to the chart API; the true claim is that nothing
 *     is written there, not that nothing is sent;
 *   - provider logs DO capture the place text and the user id, because those
 *     travel in the URL;
 *   - the operator CAN mount an offline password guess, because it holds the
 *     userid and the userid is the KDF salt;
 *   - Cloudflare D1 Time Travel is always on and cannot be disabled — 7 days
 *     on the free plan — so "deleted" is not instantly unrecoverable at the
 *     infrastructure level, even though what survives stays unreadable.
 */

export default function Privacy({ onBack }) {
  return (
    <div className="page privacy">
      <button type="button" className="privacy-back" onClick={onBack}>← back to the chart</button>

      <h1>Privacy</h1>
      <p className="privacy-lede">
        Devashaa is a birth-chart calculator. Birth data is unusually
        identifying — a date, an exact time and a place is roughly one person
        per minute per town — so this page says exactly what is kept, where,
        what is sent, and what is not kept at all.
      </p>

      <section>
        <h2>The short version</h2>
        <ul className="privacy-list">
          <li>There are <strong>no cookies</strong>, no analytics, no trackers
            and no third-party scripts of any kind.</li>
          <li>Your saved charts live <strong>in your browser</strong>.</li>
          <li>If you create an account, your charts are <strong>encrypted on
            your device before they are sent</strong>. The server stores data it
            has no key for and cannot read.</li>
          <li>We never ask for an email or phone number, and never for your own
            identity. The chart form has an optional <em>name</em> field — that
            is a label for the chart. Leave it blank or put anything you like;
            it travels and is stored with the chart's other details.</li>
        </ul>
      </section>

      <section>
        <h2>What is stored in your browser</h2>
        <p>Four things, in <code>localStorage</code> — not cookies:</p>
        <ul className="privacy-list">
          <li><strong>Your saved charts</strong> — the name you typed, birth
            date, time and place.</li>
          <li><strong>Your user id</strong>, if you made an account, so you do
            not have to retype it. Never your password.</li>
          <li><strong>Your theme</strong> and <strong>name style</strong>.</li>
        </ul>
        <p>
          Nothing here is sent anywhere on its own. Two of them travel when you
          act: re-opening a saved chart sends its birth details to the
          calculation server exactly as casting a new one does, and your user id
          goes to the accounts server when you sign in, which is what it is for.
          Your password never does.
        </p>
        <p>
          Signing in also <strong>copies the charts in your account into this
          browser</strong>, so they work offline. On a shared or borrowed
          machine they stay there until you clear the site data.
        </p>
        <p className="privacy-hedge">
          Your browser's own password manager may offer to save your password.
          That is your browser, not us.
        </p>
      </section>

      <section>
        <h2>What an account holds</h2>
        <p>Your user id, a hash of a verifier derived from your password —
          not the password — your charts as encrypted ciphertext, and two
          timestamps: when the account was created and when each chart was last
          saved. Those timestamps, and how many charts you have, are the only
          things about you the server can read.</p>
        <p>
          The encryption key is derived from your password <em>on your device</em>{' '}
          and is never transmitted. The value the server does receive comes from
          a separate, independent derivation, so there is no shortcut from what
          we store to your key.
        </p>
        <p className="privacy-strong">
          This means we cannot read your charts. Not "we choose not to" — we do
          not have the key.
        </p>
        <p>
          What we store <em>does</em> allow offline password guessing. Each
          guess costs 600,000 hashing rounds and must be repeated separately for
          every account, because your user id salts it — but{' '}
          <strong>your password strength is what actually protects the data.
          Choose a long one.</strong>
        </p>
        <p>
          Each chart is stored under an opaque identifier derived from your key,
          so the row names reveal nothing about a birth date or place, and two
          accounts holding the same birth data produce different identifiers —
          they cannot be matched to each other. The ciphertext is not padded, so
          its size hints at how long the name and place name are, though not
          what they say.
        </p>
        <p className="privacy-hedge">
          Encryption protects the contents, not the bookkeeping: we could still
          lose a record, or restore an older copy of one.
        </p>
        <p>
          Your user id is stored in the clear, and anyone can check whether a
          given one is registered — the signup form needs that to tell you an id
          is taken. <strong>Pick a user id that is not your real name.</strong>
        </p>
      </section>

      <section>
        <h2>What is sent to our calculation server</h2>
        <p>
          The birth details you enter are <strong>sent to our calculation
          server</strong> — they have to be, because that is where the
          astronomical engine runs. That request contains the name you typed,
          the date, the time, and the coordinates and time zone of the place.
        </p>
        <p>
          It is not the only request. <strong>The place box searches as you
          type</strong>, so the text you type there reaches that server before
          you cast anything. Your browser also checks that the server is up
          whenever you open the site — including this page. And exploring a
          chart sends more: switching daśā system re-sends the birth moment, and
          opening a daśā period sends the computed planetary positions.
        </p>
        <p>
          <strong>Nothing from any of those requests is written to disk or to
          any database.</strong> Charts are computed and returned; the places
          database is opened strictly read-only. Recent place searches are held
          in memory for speed and vanish when the server restarts.
        </p>
        <p className="privacy-hedge">
          One honest caveat: our hosting providers keep their own standard
          server logs — an IP address, a timestamp, the URL requested — the way
          every website does. We do not control those. Your birth date, time and
          coordinates travel in the request body and do not appear there. Two
          things do: the place text you type, because searching puts it in the
          URL, and your user id, because account requests put it in the path.
          So those logs can associate an IP address with a user id and with a
          place you searched for.
        </p>
      </section>

      <section>
        <h2>Who else is involved</h2>
        <ul className="privacy-list">
          <li><strong>Cloudflare</strong> serves the site and stores accounts.</li>
          <li><strong>Render</strong> runs the calculation server. Your browser
            contacts it directly, so it sees your IP address.</li>
          <li><strong>GeoNames</strong> supplied the place database. We host our
            own copy, so searching never contacts GeoNames or any geocoding
            company — but the search does run on our server, as above.</li>
        </ul>
      </section>

      <section>
        <h2>Deleting your data</h2>
        <ul className="privacy-list">
          <li><strong>One chart</strong> — the × removes it from this browser,
            and from your account too if you are signed in. If you are not
            signed in, the encrypted copy stays on the server and will return
            the next time you sign in; use “remove” in the account panel to
            clear it for good.</li>
          <li><strong>Everything on this device</strong> — clear the site data
            in your browser.</li>
          <li><strong>Your whole account</strong> — “Delete account” removes the
            account and every stored chart immediately. There is no soft-delete
            and no approval step.</li>
        </ul>
        <p className="privacy-hedge">
          One caveat we cannot engineer away: Cloudflare keeps an automatic
          change log of our database that is always on and cannot be switched
          off — seven days on our current plan. A deletion could in principle be
          rolled back at that level. What would come back is your user id and
          the same unreadable ciphertext, never the contents of your charts,
          because the key has never been on our servers.
        </p>
      </section>

      <section>
        <h2>Forgetting your password</h2>
        <p>
          There is no reset, because there is no email to send one to. Without
          your password the key cannot be re-derived and the stored charts stay
          permanently unreadable — <strong>including to us</strong>. The copies
          in your browser are unaffected.
        </p>
      </section>

      <section>
        <h2>Children</h2>
        <p>
          This is not a service aimed at children. Note that a chart cast for a
          child contains that child's birth date, time and place, which — as
          above — is identifying. Charts stay in your browser unless you save
          them to an account, where they are encrypted before they leave the
          device.
        </p>
      </section>

      <section>
        <h2>Checking any of this</h2>
        <p>
          The whole site is open source, including the encryption and the server
          that stores your data. Every claim here can be read in the code rather
          than taken on trust —{' '}
          <a href="https://github.com/sansbug/devashaa" rel="noreferrer">
            github.com/sansbug/devashaa
          </a>.
        </p>
        <p className="privacy-hedge">
          The first draft of this page was audited against that code and eleven
          of its claims were wrong or incomplete. They are corrected above. If
          you find another, the repository is the place to raise it.
        </p>
      </section>
    </div>
  )
}
