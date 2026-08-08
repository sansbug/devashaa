import { NAME_STYLES } from './naming.js'
import { THEMES } from './themes.js'
import InstallButton from './InstallButton.jsx'
import { useLang } from './LangContext.jsx'

const LANGS = [
  { key: 'en', label: 'English', short: 'EN' },
  { key: 'hi', label: 'हिन्दी', short: 'हिं' },
]

export default function Appearance({ theme, setTheme, nameStyle, setNameStyle, lang, setLang }) {
  const { t } = useLang()
  return (
    <div className="appearance">
      <span className="a-label">{t('appearance.language')}</span>
      <div className="lang-switch" role="group" aria-label="Language">
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

      <span className="a-label">{t('appearance.theme')}</span>
      <div className="swatches" role="group" aria-label="Colour theme">
        {THEMES.map((t) => (
          <button
            key={t.key}
            type="button"
            className={`swatch${theme === t.key ? ' on' : ''}`}
            style={{ background: t.swatch || t.bg, borderColor: t.accent }}
            onClick={() => setTheme(t.key)}
            title={t.label}
            aria-label={t.label}
            aria-pressed={theme === t.key}
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

      {/* Appears only when the browser reports the PWA is installable. */}
      <InstallButton />
    </div>
  )
}
