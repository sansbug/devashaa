import { NAME_STYLES } from './naming.js'
import { THEMES } from './themes.js'

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
            style={{ background: t.swatch || t.bg, borderColor: t.accent }}
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
