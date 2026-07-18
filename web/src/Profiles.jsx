import { profileLabel, profileDetail } from './profiles.js'

/**
 * Saved-profile chooser. Sits above the birth form so returning users pick a
 * chart instead of retyping a birth time they may have to look up.
 */
export default function Profiles({ profiles, activeId, onPick, onDelete }) {
  if (!profiles.length) return null

  return (
    <div className="profiles">
      <div className="profiles-head">
        <span className="a-label">Saved charts</span>
        <span className="profiles-note">stored only in this browser</span>
      </div>
      <ul className="profile-chips">
        {profiles.map((p) => (
          <li key={p.id} className={p.id === activeId ? 'on' : ''}>
            <button
              type="button"
              className="chip"
              onClick={() => onPick(p)}
              title={`${profileLabel(p)} — ${profileDetail(p)}`}
            >
              <span className="chip-name">{profileLabel(p)}</span>
              <span className="chip-detail">{profileDetail(p)}</span>
            </button>
            <button
              type="button"
              className="chip-x"
              onClick={() => onDelete(p.id)}
              aria-label={`Delete ${profileLabel(p)}`}
              title="Remove"
            >
              ×
            </button>
          </li>
        ))}
      </ul>
    </div>
  )
}
