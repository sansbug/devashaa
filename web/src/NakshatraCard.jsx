/**
 * A nakṣatra reference card — the muhūrta-tradition attributes BPHS itself does
 * not carry, shown on their own `traditional` tier and never as Parāśara.
 *
 * This is the deliberate complement to the rāśi card's dṛṣṭi panel, which states
 * flatly that "BPHS contains no marriage matching by sign: no kūṭa, no
 * guṇa-milan, no gaṇa, yoni or nāḍī." That gap is real — and rather than leave a
 * reader to fill it from a site that presents 20th-century material as ancient
 * doctrine, this card fills it from named sources, with the provenance attached.
 *
 * So every cell carries a CONFIDENCE, not just a value:
 *   corroborated  — two independent sources agree
 *   single_source — one book states it (the honest ceiling for the whole
 *                   gaṇa/yoni/… layer: it is one OCR'd book)
 *   uncertain     — the stored value may itself be wrong; the note says why
 *   absent        — no source states it (nāḍī, for all 27) — a first-class gap
 *
 * The BPHS deity and Viṁśottarī lord ARE shown, up top, but under their own
 * śloka badge — the two tiers sit side by side and are never blended.
 */

import { useState } from 'react'

/** Confidence badge. Mirrors the rāśi card's source badges: an absent/uncertain
    cell must read visually differently from a corroborated one, because the
    difference in how sure we are IS the information. */
const CONF = {
  corroborated: ['2 sources', 'Two independent sources agree'],
  single_source: ['1 source', 'Stated by a single source'],
  uncertain: ['uncertain', 'The stored value may itself be wrong — see the note'],
  absent: ['not sourced', 'No source states this; a deliberate gap, never guessed'],
}

function Conf({ c }) {
  const [label, hint] = CONF[c.confidence] ?? [c.confidence, '']
  const title = [hint, ...(c.sources || []), c.note].filter(Boolean).join('\n\n')
  return <span className={`src conf conf-${c.confidence}`} title={title}>{label}</span>
}

/** One attribute cell. An absent value is content ("not sourced on this tier"),
    an uncertain one wears a ⚠ that opens its note — the value is shown, the
    doubt is shown beside it, neither is hidden. */
function AttrCell({ label, gloss, c }) {
  const absent = c.confidence === 'absent'
  return (
    <div className={`rc-cell nk-cell${absent ? ' is-absent' : ''}`}>
      <span className="rc-key" title={gloss}>{label}</span>
      <span className="rc-val">
        {absent ? 'not sourced on this tier' : c.value}
      </span>
      <Conf c={c} />
      {c.confidence === 'uncertain' && (
        <span className="rc-conflict" title={c.note}>⚠</span>
      )}
      {c.note && c.confidence !== 'uncertain' && (
        <span className="nk-info" title={c.note}>ⓘ</span>
      )}
    </div>
  )
}

/** The `modern`-tier interaction techniques — one author-group's pointers, NOT
    BPHS and NOT a verdict. Collapsed by default and styled deliberately unlike
    the tiered cells above it, with the disclaimer ABOVE the list, mirroring the
    rāśi card's translator sketch. The computable badge says only whether the app
    could detect the STRUCTURAL trigger; the interpretation stays the author's,
    and the three non-Parāśara techniques are fenced, never presented as results. */
const COMPUTABLE_BADGE = {
  yes: ['trigger detectable', 'The structural trigger (a graha or house-lord in the nakṣatra) is cleanly detectable.'],
  partly: ['trigger approximate', 'Needs an affliction / house-connection judgment the app can only approximate.'],
  no: ['interpretive', 'Interpretive, or leans on non-Parāśara material — not a structural flag the app computes.'],
}

function ModernTechniques({ t }) {
  const [open, setOpen] = useState(false)
  if (!t) return null
  return (
    <section className="nk-modern">
      <button type="button" className="nk-mod-toggle" aria-expanded={open}
              onClick={() => setOpen(!open)}>
        {open ? '−' : '+'} Modern techniques
        {t.available && <span className="nk-mod-count">{t.techniques.length}</span>}
        <span className="nk-mod-byline">one modern author-group's index — not Parāśara</span>
      </button>
      {open && (
        <div className="nk-mod-body">
          <p className="nk-mod-warn">
            Interpretive techniques from a single modern book
            {t.source ? ` (${t.source})` : ''} — shown as attributed pointers, not
            BPHS, not the traditional canon, and <strong>not a verdict on any
            chart.</strong> The badge says only whether the app could detect the
            structural trigger; the reading stays the author's.
          </p>
          {!t.available ? (
            <p className="rc-note">{t.reason}</p>
          ) : (
            <>
              <p className="nk-mod-theme">
                Theme (author's framing): <strong>{t.theme}</strong>
              </p>
              <ol className="nk-mod-list">
                {t.techniques.map((tech) => {
                  const [label, hint] = COMPUTABLE_BADGE[tech.computable] ?? [tech.computable, '']
                  return (
                    <li key={tech.n} className={tech.non_parashara ? 'is-np' : ''}>
                      <span className="nk-mod-gist">{tech.gist}</span>
                      <span className="nk-mod-meta">
                        <span className={`src compute compute-${tech.computable}`} title={hint}>{label}</span>
                        <span className="nk-mod-page" title={tech.cite}>p.{tech.page}</span>
                        {tech.non_parashara && (
                          <span className="src np-tag" title={tech.non_parashara}>⚠ non-Parāśara</span>
                        )}
                      </span>
                    </li>
                  )
                })}
              </ol>
            </>
          )}
        </div>
      )}
    </section>
  )
}

const FIELD_ORDER = ['symbol', 'gana', 'yoni', 'body_part', 'purushartha',
  'quality', 'shakti', 'nadi']
const FALLBACK_META = {
  symbol: ['Symbol', 'The classical emblem / asterism figure'],
  gana: ['Gaṇa', 'Temperament — Deva / Manuṣya / Rākṣasa'],
  yoni: ['Yoni (animal)', 'Sexual-compatibility animal (Aṣṭakūṭa)'],
  body_part: ['Kālapuruṣa aṅga', 'Body part in the cosmic-person scheme'],
  purushartha: ['Puruṣārtha', 'Life-aim — Dharma / Artha / Kāma / Mokṣa'],
  quality: ['Guṇa / activity', 'Muhūrta activity-type'],
  shakti: ['Śakti', "The nakṣatra's animating power"],
  nadi: ['Nāḍī', 'Ādi / Madhya / Antya (compatibility)'],
}

export default function NakshatraCard({ n, fieldMeta, namer }) {
  if (!n) return null
  const meta = fieldMeta || FALLBACK_META
  const label = (f) => (meta[f]?.[0] ?? f)
  const gloss = (f) => (meta[f]?.[1] ?? '')
  const b = n.bphs
  const v = n.deity_variant

  return (
    <article className="rasi-card nk-card">
      <header className="rc-head">
        <div>
          <h3>{namer.nakshatra(n)}</h3>
          <p className="rc-sub">
            nakṣatra {n.index} of 27 · {n.name} / {n.name_iast}
          </p>
        </div>
        {b && (
          <div className="rc-limb">
            <span className="rc-limb-label">BPHS deity · Viṁśottarī lord</span>
            <strong>{b.deity_iast} · {namer.grahaKey(b.lord)}</strong>
            <span className="src src-sloka" title={`BPHS — ${b.cite}`}>śloka</span>
          </div>
        )}
      </header>

      {v && (
        <p className="rc-conflict-strip">
          <strong>Deity variance flagged.</strong> {v.source === 'S2' ? 'Sunil John' : v.source}{' '}
          gives {v.nakshatra} = <strong>{v.traditional}</strong>, where the app's
          BPHS-cited data gives <strong>{v.bphs_app}</strong>. The BPHS-tier value
          is left standing; the traditional variant is recorded, not applied.
        </p>
      )}

      <section>
        <h4>Attributes on the traditional tier</h4>
        <div className="rc-grid">
          {FIELD_ORDER.map((f) => (
            <AttrCell key={f} label={label(f)} gloss={gloss(f)} c={n.cells[f]} />
          ))}
        </div>
        <p className="rc-note">
          These are <strong>not BPHS.</strong> Bṛhat Parāśara Horā Śāstra assigns
          no gaṇa, yoni or nāḍī to a nakṣatra — the rāśi cards say as much. They
          belong to the older Bṛhat-Saṁhitā / muhūrta tradition and ship here on a{' '}
          <strong>traditional</strong> footing, beside the BPHS deity above, never
          blended into it. Every cell names its source and how sure we are of it.
        </p>
      </section>

      {/* Last on the card, always. A different tier (modern), a different look,
          and never above the tiered attributes. */}
      <ModernTechniques t={n.techniques} />
    </article>
  )
}
