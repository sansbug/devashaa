/**
 * Account panel — register, sign in, and save each chart on its own.
 *
 * Three things this UI is responsible for getting right:
 *
 *  1. SAYING THERE IS NO RECOVERY *BEFORE* REGISTRATION, not after. No email is
 *     collected, so a forgotten password cannot be reset by anyone, including
 *     us. That is the same property that stops us reading the data, and a user
 *     deserves to weigh it before they rely on it.
 *  2. ENFORCING A PASSWORD FLOOR rather than suggesting one. There is no reset
 *     and the data identifies a real person.
 *  3. PER-PROFILE CONTROLS. Each saved chart is its own row with its own save
 *     and remove, so nothing is ever all-or-nothing.
 */

import { useEffect, useState } from 'react'
import {
  deriveAccount, register, login, isTaken, deleteAccount, fetchProfiles,
  saveProfile, removeProfile, profileIdFor, passwordProblem,
  normaliseUserid, USERID_RE,
} from './account.js'

const REMEMBER = 'devashaa.acct'

export default function Account({ profiles, onMerged, onAccount }) {
  // Only the userid is remembered between visits. The password is not stored
  // anywhere — the derived key lives in memory for this tab and nowhere else.
  const [saved] = useState(() => localStorage.getItem(REMEMBER) || '')
  const [mode, setMode] = useState(saved ? 'signin' : 'signup')
  const [userid, setUserid] = useState(saved)
  const [password, setPassword] = useState('')
  const [acct, setAcct] = useState(null)
  const [remote, setRemote] = useState([])
  const [broken, setBroken] = useState([])
  const [pids, setPids] = useState({})            // local signature -> profile id
  const [busy, setBusy] = useState('')
  const [err, setErr] = useState(null)
  const [msg, setMsg] = useState(null)
  const [taken, setTaken] = useState(null)
  const [confirmDelete, setConfirmDelete] = useState(false)

  const idProblem = userid && !USERID_RE.test(normaliseUserid(userid))
    ? '3–32 characters: lowercase letters, digits, and . _ - after the first.'
    : null
  const pwProblem = password ? passwordProblem(password) : null

  // Availability is a courtesy for the form; the server's PRIMARY KEY is what
  // actually decides, and register() can still lose a race.
  useEffect(() => {
    if (mode !== 'signup' || idProblem || !userid) { setTaken(null); return }
    let dead = false
    const t = setTimeout(() => {
      isTaken(userid).then((x) => { if (!dead) setTaken(x) }).catch(() => {})
    }, 350)
    return () => { dead = true; clearTimeout(t) }
  }, [userid, mode, idProblem])

  /** Map every local profile to its opaque id, so the rows can be compared. */
  async function indexLocal(a, list) {
    const out = {}
    for (const p of list) out[p.id ?? JSON.stringify(p)] = await profileIdFor(a.idKey, p)
    return out
  }

  async function pull(a) {
    const { profiles: got, broken: bad } = await fetchProfiles(a)
    setRemote(got)
    setBroken(bad)
    setPids(await indexLocal(a, profiles))
    // Merge remote into local so the charts are usable immediately. Never the
    // other way: restoring must not delete anything already on this device.
    const extra = got.filter((p) => !profiles.some(
      (q) => q.date === p.date && q.time === p.time
             && q.place?.latitude === p.place?.latitude))
    if (extra.length) onMerged?.([...profiles, ...extra])
    return { got, bad, extra }
  }

  async function go(kind) {
    setBusy(kind); setErr(null); setMsg(null)
    try {
      const a = await deriveAccount(userid, password)
      if (kind === 'signup') {
        await register(a.userid, a.authId)
      } else {
        await login(a.userid, a.authId)
      }
      localStorage.setItem(REMEMBER, a.userid)
      setAcct(a)
      onAccount?.(a)          // so a local delete can also reach the server
      setPassword('')
      const { extra } = await pull(a)
      setMsg(kind === 'signup'
        ? 'Account created. Save your charts below.'
        : extra.length
          ? `Signed in — ${extra.length} chart${extra.length === 1 ? '' : 's'} restored.`
          : 'Signed in.')
    } catch (e) {
      setErr(e.message)
    } finally {
      setBusy('')
    }
  }

  async function saveOne(p) {
    setBusy(`save:${p.id}`); setErr(null); setMsg(null)
    try {
      const pid = await saveProfile(acct, p)
      setPids((m) => ({ ...m, [p.id ?? JSON.stringify(p)]: pid }))
      await pull(acct)
      setMsg(`Saved ${p.name || 'chart'}.`)
    } catch (e) { setErr(e.message) } finally { setBusy('') }
  }

  async function removeOne(p) {
    setBusy(`del:${p.id}`); setErr(null); setMsg(null)
    try {
      await removeProfile(acct, await profileIdFor(acct.idKey, p))
      await pull(acct)
      setMsg(`Removed ${p.name || 'chart'} from your account. It is still on this device.`)
    } catch (e) { setErr(e.message) } finally { setBusy('') }
  }

  async function wipe() {
    setBusy('wipe'); setErr(null)
    try {
      await deleteAccount(acct.userid, acct.authId)
      localStorage.removeItem(REMEMBER)
      setAcct(null); setRemote([]); setConfirmDelete(false); onAccount?.(null)
      setMsg('Account and all stored charts deleted. This device is untouched.')
    } catch (e) { setErr(e.message) } finally { setBusy('') }
  }

  const onServer = new Set(remote.map((p) => p._pid))
  const canSubmit = userid && password && !idProblem && !pwProblem
    && !(mode === 'signup' && taken)

  /* ------------------------------ signed out ---------------------------- */
  if (!acct) {
    return (
      <section className="acct">
        <h3>Save your charts to an account</h3>
        <p className="acct-lead">
          Optional. Your charts already live in this browser — an account lets
          you reach them from another device. They are encrypted here, before
          they are sent; <strong>the server stores data it has no key for and
          cannot read.</strong> No email, no name, nothing that identifies you.
        </p>

        <div className="acct-tabs">
          <button type="button" className={mode === 'signup' ? 'on' : ''}
                  onClick={() => { setMode('signup'); setErr(null) }}>Create account</button>
          <button type="button" className={mode === 'signin' ? 'on' : ''}
                  onClick={() => { setMode('signin'); setErr(null) }}>Sign in</button>
        </div>

        <div className="acct-form">
          <label htmlFor="acct-id">User id</label>
          <input id="acct-id" value={userid} autoComplete="username" spellCheck={false}
                 placeholder="e.g. ravi.k"
                 onChange={(e) => setUserid(e.target.value)} />
          {idProblem && <p className="acct-err">{idProblem}</p>}
          {mode === 'signup' && taken === true && !idProblem && (
            <p className="acct-err">That user id is taken.</p>
          )}
          {mode === 'signup' && taken === false && !idProblem && (
            <p className="acct-ok">Available.</p>
          )}

          <label htmlFor="acct-pw">Password</label>
          <input id="acct-pw" type="password" value={password}
                 autoComplete={mode === 'signup' ? 'new-password' : 'current-password'}
                 onChange={(e) => setPassword(e.target.value)}
                 onKeyDown={(e) => e.key === 'Enter' && canSubmit && go(mode)} />
          {mode === 'signup' && pwProblem && <p className="acct-err">{pwProblem}</p>}

          {/* Said BEFORE the button that creates the account, not after. */}
          {mode === 'signup' && (
            <p className="acct-warn">
              <strong>There is no password reset.</strong> We hold no email, so
              if you forget this password nobody can recover your charts —
              not you, and not us. That is the same property that stops us
              reading them. The copies in this browser are unaffected.
            </p>
          )}

          <button type="button" className="go" disabled={!canSubmit || !!busy}
                  onClick={() => go(mode)}>
            {busy ? 'working…' : mode === 'signup' ? 'Create account' : 'Sign in'}
          </button>
        </div>

        {err && <p className="acct-err">{err}</p>}
        {msg && <p className="acct-ok">{msg}</p>}
      </section>
    )
  }

  /* ------------------------------- signed in ---------------------------- */
  return (
    <section className="acct">
      <div className="acct-head">
        <h3>Signed in as <code>{acct.userid}</code></h3>
        <button type="button"
                onClick={() => { setAcct(null); setRemote([]); onAccount?.(null) }}>
          sign out
        </button>
      </div>

      <p className="acct-lead">
        {remote.length} chart{remote.length === 1 ? '' : 's'} stored, encrypted.
        Each one is saved separately — nothing here is all-or-nothing.
      </p>

      {broken.length > 0 && (
        <p className="acct-err">
          {broken.length} stored record{broken.length === 1 ? '' : 's'} could not
          be decrypted and {broken.length === 1 ? 'is' : 'are'} not shown. Nothing
          has been deleted.
        </p>
      )}

      <ul className="acct-rows">
        {profiles.map((p) => {
          const pid = pids[p.id ?? JSON.stringify(p)]
          const up = pid && onServer.has(pid)
          return (
            <li key={p.id ?? `${p.date}${p.time}`} className="acct-row">
              <span className="acct-name">{p.name || 'Unnamed'}</span>
              <span className="acct-meta">
                {p.date} {p.time} · {p.place?.name?.split(',')[0]}
              </span>
              <span className={`acct-state${up ? ' on' : ''}`}>
                {up ? 'saved' : 'this device only'}
              </span>
              {up ? (
                <button type="button" disabled={!!busy} onClick={() => removeOne(p)}>
                  {busy === `del:${p.id}` ? '…' : 'remove'}
                </button>
              ) : (
                <button type="button" className="go" disabled={!!busy}
                        onClick={() => saveOne(p)}>
                  {busy === `save:${p.id}` ? '…' : 'save'}
                </button>
              )}
            </li>
          )
        })}
        {profiles.length === 0 && (
          <li className="acct-empty">Cast a chart and it will appear here to save.</li>
        )}
      </ul>

      <div className="acct-actions">
        {!confirmDelete ? (
          <button type="button" className="acct-danger" disabled={!!busy}
                  onClick={() => setConfirmDelete(true)}>Delete account</button>
        ) : (
          <>
            <span className="acct-confirm">
              Delete the account and every stored chart? The copies in this
              browser stay.
            </span>
            <button type="button" className="acct-danger" disabled={!!busy} onClick={wipe}>
              {busy === 'wipe' ? 'deleting…' : 'Yes, delete'}
            </button>
            <button type="button" onClick={() => setConfirmDelete(false)}>cancel</button>
          </>
        )}
      </div>

      {err && <p className="acct-err">{err}</p>}
      {msg && <p className="acct-ok">{msg}</p>}
    </section>
  )
}
