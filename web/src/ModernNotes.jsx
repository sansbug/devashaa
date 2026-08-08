/**
 * The "K.N. Rao (modern)" pointer bucket — §3b.
 *
 * Not nakṣatra-based, so it lives in its own reference block, never on a nakṣatra
 * card. Same pointer-only discipline as the nakṣatra techniques: attributed
 * gists, a structural-trigger badge, and never a chart verdict. Reuses the
 * modern-technique visual vocabulary (nk-mod-*, compute-*) so it reads as the
 * same tier.
 */

import { useLang } from './LangContext.jsx'

const CB = {
  yes: ['modernnotes.compute.yes.label', 'modernnotes.compute.yes.hint'],
  partly: ['modernnotes.compute.partly.label', 'modernnotes.compute.partly.hint'],
  no: ['modernnotes.compute.no.label', 'modernnotes.compute.no.hint'],
}

function Pointer({ p }) {
  const { t } = useLang()
  const [label, hint] = CB[p.computable] ?? [p.computable, '']
  return (
    <li>
      <span className="nk-mod-gist"><strong>{p.title}.</strong> {p.gist}</span>
      <span className="nk-mod-meta">
        <span className={`src compute compute-${p.computable}`} title={t(hint)}>{t(label)}</span>
        <span className="nk-mod-page" title={p.cite}>p.{p.page}</span>
      </span>
    </li>
  )
}

export default function ModernNotes({ data }) {
  const { t } = useLang()
  if (!data) return null
  const g = data.gajakesari
  const al = data.astrology_lessons
  return (
    <div className="mod-notes">
      <p className="nk-mod-warn">{data.note}</p>

      <section className="mod-topic">
        <h4>{g.topic} <span className="mod-src">{g.source}</span></h4>
        <ol className="nk-mod-list">
          {g.pointers.map((p, i) => <Pointer key={i} p={p} />)}
        </ol>
      </section>

      <section className="mod-topic">
        <h4>{al.topic} <span className="mod-src">{al.source}</span></h4>
        <p className="rc-note">{al.traditional_tables.note}</p>
        {/* Struck through, like the rāśi card's "not in BPHS" chips: these are
            classical tables already in the app's BPHS core, listed only so a
            reader sees what was deliberately NOT re-served from this book. */}
        <div className="mod-chips">
          {al.traditional_tables.items.map((tbl) => (
            <span key={tbl} className="mod-chip trad" title={t('modernnotes.chip.tradTitle')}>{tbl}</span>
          ))}
        </div>
        <p className="rc-note">{al.modern_pointers.note}</p>
        <ul className="nk-mod-list mod-named">
          {al.modern_pointers.items.map((m) => (
            <li key={m.name}><strong>{m.name}</strong> — {m.gist}</li>
          ))}
        </ul>
      </section>
    </div>
  )
}
