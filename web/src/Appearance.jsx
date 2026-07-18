import { NAME_STYLES } from './naming.js'

/** Swatch colours are literals, not CSS vars — each swatch must preview ITS OWN
 *  theme while the page is still showing the current one. */
const THEMES = [
  { key: 'ember', label: 'Ember', bg: '#12100e', accent: '#c9a227' },
  { key: 'midnight', label: 'Midnight', bg: '#0a0f1e', accent: '#e8c46a' },
  { key: 'parchment', label: 'Parchment', bg: '#f2e9d5', accent: '#8a4b1c' },
  { key: 'slate', label: 'Slate', bg: '#11151a', accent: '#4fd1c5' },
]

export default function Appearance({ theme, setTheme, nameStyle, setNameStyle }) {
  return (
    <div className="appearance">
      <span className="a-label">Theme</span>
      <div className="swatches" role="group" aria-label="Colour theme">
        {THEMES.map((t) => (
          <button
            key={t.key}
            type="button"
            className={`swatch${theme === t.key ? ' on' : ''}`}
            style={{ background: t.bg, borderColor: t.accent }}
            onClick={() => setTheme(t.key)}
            title={t.label}
            aria-label={t.label}
            aria-pressed={theme === t.key}
          />
        ))}
      </div>

      <span className="a-label">Names</span>
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
    </div>
  )
}
