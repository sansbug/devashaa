import { profileLabel, profileDetail } from './profiles.js'
import { useLang } from './LangContext.jsx'

/**
 * The saved charts, as one pull-down beside the "Save your charts" button.
 *
 * A select rather than a row of chips: a returning visitor with a dozen charts
 * got a wall of pills that wrapped across three lines. The list is one control
 * now, the active chart is its value, and the remove button acts on that
 * chart alone — nothing is deleted from a list you were not looking at.
 */
export default function Profiles({ profiles, activeId, onPick, onDelete }) {
  const { t } = useLang()
  if (!profiles.length) return null
  const active = profiles.find((p) => p.id === activeId) || null

  return (
    <div className="profile-select">
      <select
        aria-label={t('saved.pick', 'Saved charts')}
        value={active ? active.id : ''}
        onChange={(e) => {
          const p = profiles.find((x) => x.id === e.target.value)
          if (p) onPick(p)
        }}
      >
        <option value="" disabled>{t('saved.pick', 'Saved charts')} ({profiles.length})</option>
        {profiles.map((p) => (
          <option key={p.id} value={p.id}>{p.name ? `${p.name} — ${profileDetail(p)}` : profileDetail(p)}</option>
        ))}
      </select>
      {active && (
        <button
          type="button"
          className="profile-x"
          onClick={() => onDelete(active.id)}
          aria-label={`${t('saved.remove', 'Remove')} ${profileLabel(active)}`}
          title={`${t('saved.remove', 'Remove')} ${profileLabel(active)}`}
        >
          ×
        </button>
      )}
    </div>
  )
}
