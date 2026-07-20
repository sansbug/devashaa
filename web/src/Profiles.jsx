import { profileLabel, profileDetail } from './profiles.js'

/**
 * The saved-chart chips.
 *
 * Renders inline beside the "Save your charts" button rather than in a panel of
 * its own: the charts already in this browser are the thing a returning visitor
 * wants first, so they stay one click away while the account controls — which
 * most people will never open — fold away behind the button.
 */
export default function Profiles({ profiles, activeId, onPick, onDelete }) {
  if (!profiles.length) return null

  return (
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
  )
}
