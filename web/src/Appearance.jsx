import { useState } from 'react'
import { NAME_STYLES } from './naming.js'
import { THEMES } from './themes.js'
import InstallButton from './InstallButton.jsx'
import { useLang } from './LangContext.jsx'

const LANGS = [
  { key: 'en', label: 'English', short: 'EN' },
  { key: 'hi', label: 'हिंदी', short: 'हिं' },
]

/** The language switch is always in reach; theme and name style sit behind one
    Settings button, so the top of the page is not a row of controls. */
export default function Appearance({ theme, setTheme, nameStyle, setNameStyle, lang, setLang, refs, setRefs }) {
  const { t } = useLang()
  const [open, setOpen] = useState(false)
  return (
    <div className="appearance">
      <div className="lang-switch" role="group" aria-label={t('appearance.language')}>
        {LANGS.map((l) => (
          <button
            key={l.key}
            type="button"
            className={`lang-btn${lang === l.key ? ' on' : ''}`}
            onClick={() => setLang(l.key)}
            title={l.label}
            aria-pressed={lang === l.key}
            lang={l.key}
          >
            {l.short}
          </button>
        ))}
      </div>

      <button type="button" className={`a-settings${open ? ' on' : ''}`} aria-expanded={open}
              onClick={() => setOpen((o) => !o)}>
        <span aria-hidden="true">⚙</span> {t('appearance.settings', 'Settings')}
      </button>

      {/* Appears only when the browser reports the PWA is installable. */}
      <InstallButton />

      {open && (
        <div className="a-panel">
          <span className="a-label">{t('appearance.theme')}</span>
          <div className="swatches" role="group" aria-label="Colour theme">
            {THEMES.map((th) => (
              <button
                key={th.key}
                type="button"
                className={`swatch${theme === th.key ? ' on' : ''}`}
                style={{ background: th.swatch || th.bg, borderColor: th.accent }}
                onClick={() => setTheme(th.key)}
                title={th.label}
                aria-label={th.label}
                aria-pressed={theme === th.key}
              />
            ))}
          </div>

          <span className="a-label">{t('appearance.names')}</span>
          <select
            className="name-select"
            value={nameStyle}
            onChange={(e) => setNameStyle(e.target.value)}
            aria-label="Name style"
          >
            {NAME_STYLES.map((s) => (
              <option key={s.key} value={s.key} title={s.example}>
                {s.label} — {s.example}
              </option>
            ))}
          </select>

          {/* Book names, chapter-and-verse and page numbers: off for a plain reading, on for the sources. */}
          {setRefs && (<>
            <span className="a-label">{t('appearance.refs', 'References')}</span>
            <div className="lang-switch" role="group" aria-label={t('appearance.refs', 'References')}>
              <button type="button" className={`lang-btn${!refs ? ' on' : ''}`} aria-pressed={!refs} onClick={() => setRefs(false)}>{t('appearance.refs.off', 'Off')}</button>
              <button type="button" className={`lang-btn${refs ? ' on' : ''}`} aria-pressed={!!refs} onClick={() => setRefs(true)}>{t('appearance.refs.on', 'On')}</button>
            </div>
          </>)}
        </div>
      )}
    </div>
  )
}
