/**
 * Passphrase sync — the UI.
 *
 * Three rules this component exists to hold:
 *
 *  1. THE PASSPHRASE IS GENERATED, NEVER INVENTED. There is no "choose your
 *     own" box. A fixed KDF salt is only safe against precomputation if the
 *     phrase carries real entropy, and a human-chosen one carries perhaps 20
 *     bits where a generated one carries 80. The box below accepts a phrase
 *     only to RESTORE one that was generated earlier.
 *  2. THE TRADE IS STATED BEFORE IT IS MADE. Lose the phrase and the data is
 *     unrecoverable — there is no reset link, because there is no email to send
 *     one to. That has to be said where someone will read it, not in a footer.
 *  3. MERGE, NEVER CLOBBER. Two devices editing offline is the normal case.
 *     Profiles union by birth signature; the local copy wins a name clash.
 */

import { useState } from 'react'
import {
  generatePassphrase, deriveKeys, looksLikePassphrase, unknownWords,
  pushProfiles, pullProfiles, forgetProfiles, mergeProfiles, WORDLIST,
} from './sync.js'

const KEY = 'devashaa.syncPhrase'

export default function Sync({ profiles, onMerged }) {
  // Remembered on THIS device only, so a return visit does not have to retype
  // it. It is the same class of secret as the profiles it protects, and it
  // lives in the same place they do.
  const [phrase, setPhrase] = useState(() => localStorage.getItem(KEY) || '')
  const [typed, setTyped] = useState('')
  const [open, setOpen] = useState(false)
  const [busy, setBusy] = useState('')
  const [msg, setMsg] = useState(null)
  const [err, setErr] = useState(null)
  const [confirmForget, setConfirmForget] = useState(false)

  const remember = (p) => { localStorage.setItem(KEY, p); setPhrase(p) }

  async function withKeys(p, fn, label) {
    setBusy(label); setErr(null); setMsg(null)
    try {
      const { syncId, key } = await deriveKeys(p)
      await fn(syncId, key)
    } catch (e) {
      setErr(e.message === 'DECRYPT_FAILED'
        ? 'That passphrase does not open the data stored under it. Check for a '
          + 'mistyped word — nothing has been changed.'
        : e.message)
    } finally {
      setBusy('')
    }
  }

  const create = () => { const p = generatePassphrase(); remember(p); setOpen(true); setMsg(null) }

  const upload = () => withKeys(phrase, async (id, key) => {
    // Merge before writing, so a device that has been offline cannot erase what
    // another one saved in the meantime.
    const remote = await pullProfiles(id, key).catch((e) => {
      if (e.message === 'DECRYPT_FAILED') throw e
      return null
    })
    const merged = mergeProfiles(profiles, remote || [])
    await pushProfiles(id, key, merged)
    if (remote && merged.length !== profiles.length) onMerged?.(merged)
    setMsg(`Saved ${merged.length} chart${merged.length === 1 ? '' : 's'}.`)
  }, 'saving')

  const download = (p) => withKeys(p, async (id, key) => {
    const remote = await pullProfiles(id, key)
    if (remote === null) {
      setMsg('Nothing has been saved under that passphrase yet.')
      return
    }
    const merged = mergeProfiles(profiles, remote)
    onMerged?.(merged)
    remember(p)
    setTyped('')
    setMsg(`Restored — you now have ${merged.length} chart${merged.length === 1 ? '' : 's'}.`)
  }, 'restoring')

  const forget = () => withKeys(phrase, async (id) => {
    await forgetProfiles(id)
    localStorage.removeItem(KEY)
    setPhrase('')
    setConfirmForget(false)
    setMsg('Deleted from the server. The charts on this device are untouched.')
  }, 'deleting')

  const bad = typed && !looksLikePassphrase(typed) ? unknownWords(typed) : []

  return (
    <section className="sync">
      <h3>Carry your charts to another device</h3>
      <p className="sync-lead">
        Your saved charts live in this browser only. A passphrase lets you copy
        them to another device — <strong>without an account and without telling
        us who you are</strong>. They are encrypted here, on your machine; the
        server stores a blob it has no key for and cannot read.
      </p>

      {!phrase ? (
        <>
          <button type="button" className="go" onClick={create}>
            Create a passphrase
          </button>
          <p className="sync-note">
            Ten words, chosen at random by your browser. You cannot pick your
            own — an invented phrase is far easier to guess, and the encryption
            is only as strong as the phrase behind it.
          </p>
        </>
      ) : (
        <div className="sync-have">
          <div className="sync-phrase-row">
            <code className={`sync-phrase${open ? '' : ' hidden'}`}>
              {open ? phrase : '•••• •••• •••• •••• ••••'}
            </code>
            <button type="button" onClick={() => setOpen((o) => !o)}>
              {open ? 'hide' : 'show'}
            </button>
            <button type="button" onClick={() => navigator.clipboard?.writeText(phrase)}>
              copy
            </button>
          </div>
          {/* Said at the moment of creation, not buried. There is no reset
              link because there is no email to send one to. */}
          <p className="sync-warn">
            <strong>Write this down.</strong> It is the only key to your charts.
            We cannot reset it, email it to you, or recover your data without it
            — that is the same property that stops us reading your data.
          </p>
          <div className="sync-actions">
            <button type="button" className="go" onClick={upload} disabled={!!busy}>
              {busy === 'saving' ? 'saving…' : `Save ${profiles.length} chart${profiles.length === 1 ? '' : 's'}`}
            </button>
            <button type="button" onClick={() => download(phrase)} disabled={!!busy}>
              {busy === 'restoring' ? 'restoring…' : 'Restore from server'}
            </button>
            {!confirmForget ? (
              <button type="button" className="sync-danger"
                      onClick={() => setConfirmForget(true)} disabled={!!busy}>
                Delete from server
              </button>
            ) : (
              <>
                <button type="button" className="sync-danger" onClick={forget} disabled={!!busy}>
                  {busy === 'deleting' ? 'deleting…' : 'Yes, delete it'}
                </button>
                <button type="button" onClick={() => setConfirmForget(false)}>cancel</button>
              </>
            )}
          </div>
        </div>
      )}

      <details className="sync-restore">
        <summary>I already have a passphrase</summary>
        <label htmlFor="sync-in">Enter your ten words</label>
        <textarea
          id="sync-in" rows={2} value={typed} spellCheck={false}
          placeholder="able acid aged also area army away baby back ball"
          onChange={(e) => setTyped(e.target.value)}
        />
        {/* Point at the wrong word rather than saying "invalid" — a ten-word
            phrase is almost always right except for one transcription slip. */}
        {bad.length > 0 && (
          <p className="sync-err">
            Not in the word list: {bad.map((w) => <code key={w}>{w}</code>)}
          </p>
        )}
        <button type="button" className="go" disabled={!looksLikePassphrase(typed) || !!busy}
                onClick={() => download(typed)}>
          {busy === 'restoring' ? 'restoring…' : 'Restore my charts'}
        </button>
        <p className="sync-note">
          Restoring <em>merges</em> — it adds the charts stored on the server to
          the ones already here, and never deletes anything on this device.
        </p>
      </details>

      {msg && <p className="sync-ok">{msg}</p>}
      {err && <p className="sync-err">{err}</p>}

      <p className="sync-note sync-how">
        How it works: your passphrase derives two independent values. One names
        your data on the server; the other encrypts it and never leaves this
        page. Knowing every name in the store reveals nothing about any key, so
        the server holds ciphertext it has no way to open. {WORDLIST.length} words,
        ten of them, is about 80 bits — far past guessing.
      </p>
    </section>
  )
}
