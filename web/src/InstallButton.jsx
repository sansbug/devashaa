import { useEffect, useRef, useState } from 'react'

/**
 * "Install app" chip. Chrome / Edge / Samsung Internet fire `beforeinstallprompt`
 * only when the PWA is installable (valid manifest + service worker + HTTPS, and
 * not already installed); tapping the chip replays that captured prompt so the
 * user doesn't have to hunt through the browser's ⋮ menu.
 *
 * The event can fire before React mounts, so main.jsx captures it into
 * window.__deferredInstallPrompt and re-dispatches a `pwa-installable` event —
 * this component reads whichever path delivers it. It hides itself once the app
 * is installed or when already running standalone. (iOS Safari never fires the
 * event and has no install API, so the chip simply doesn't appear there — that
 * platform installs via Share → Add to Home Screen.)
 */
const isStandalone = () =>
  window.matchMedia('(display-mode: standalone)').matches
  || window.navigator.standalone === true            // iOS-specific flag

export default function InstallButton() {
  const [deferred, setDeferred] = useState(() => window.__deferredInstallPrompt || null)
  const [installed, setInstalled] = useState(isStandalone)
  const btnRef = useRef(null)

  useEffect(() => {
    const onAvailable = (e) => setDeferred(e.detail || window.__deferredInstallPrompt || null)
    const onBeforePrompt = (e) => {           // in case the event fires after mount
      e.preventDefault()
      window.__deferredInstallPrompt = e
      setDeferred(e)
    }
    const onInstalled = () => {
      setInstalled(true)
      setDeferred(null)
      window.__deferredInstallPrompt = null
    }
    window.addEventListener('pwa-installable', onAvailable)
    window.addEventListener('beforeinstallprompt', onBeforePrompt)
    window.addEventListener('appinstalled', onInstalled)
    return () => {
      window.removeEventListener('pwa-installable', onAvailable)
      window.removeEventListener('beforeinstallprompt', onBeforePrompt)
      window.removeEventListener('appinstalled', onInstalled)
    }
  }, [])

  if (installed || !deferred) return null

  const install = async () => {
    const prompt = deferred
    // Where to send keyboard/AT focus once this button unmounts — the adjacent
    // control in the bar, captured now while the button is still in the DOM.
    const refocus = btnRef.current?.previousElementSibling
    // The captured event is single-use — clear it immediately so a second tap
    // (or a lost race) can never call prompt() twice on the same event.
    setDeferred(null)
    window.__deferredInstallPrompt = null
    try {
      prompt.prompt()
      const choice = await prompt.userChoice
      if (choice && choice.outcome === 'accepted') setInstalled(true)
    } catch {
      /* prompt already consumed or dismissed — nothing to do */
    } finally {
      // The chip has now unmounted; keep focus in the control bar rather than
      // letting it fall to <body> (WCAG 2.4.3), for keyboard and screen-reader users.
      if (refocus && typeof refocus.focus === 'function') refocus.focus()
    }
  }

  return (
    <button ref={btnRef} type="button" className="install-btn" onClick={install}
            title="Install Devashaa as an app on this device">
      <span className="install-ic" aria-hidden="true">⤓</span> Install app
    </button>
  )
}
