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
 *   corroborated  — two independent sources agree (yoni, puruṣārtha, symbols
 *                   1-18, and — since Komilla Sutton — nāḍī)
 *   single_source — one book states it (gaṇa, body-part, activity, śakti rest on
 *                   the one S3 book; dosha and guṇa on Komilla)
 *   uncertain     — the stored value may itself be wrong; the note says why
 *   absent        — no source states it — a first-class gap, never guessed
 *
 * Nāḍī used to read "not sourced on this tier" for all 27 — the honest gap the
 * first three books left. Komilla Sutton's Ayurvedic-dosha column closed it:
 * it reproduces the canonical Aṣṭakūṭa Ādi/Madhya/Antya assignment exactly, so
 * nāḍī and dosha now both ship, corroborated.
 *
 * The BPHS deity and Viṁśottarī lord ARE shown, up top, but under their own
 * śloka badge — the two tiers sit side by side and are never blended.
 */

import { useState } from 'react'
import Cite from './Cite.jsx'
import { useLang } from './LangContext.jsx'

/** Confidence badge. Mirrors the rāśi card's source badges: an absent/uncertain
    cell must read visually differently from a corroborated one, because the
    difference in how sure we are IS the information. */
const CONF = {
  corroborated: ['nakshatra.conf.corroborated.label', 'nakshatra.conf.corroborated.hint'],
  single_source: ['nakshatra.conf.single.label', 'nakshatra.conf.single.hint'],
  uncertain: ['nakshatra.conf.uncertain.label', 'nakshatra.conf.uncertain.hint'],
  absent: ['nakshatra.conf.absent.label', 'nakshatra.conf.absent.hint'],
}

function Conf({ c }) {
  const { t } = useLang()
  const [label, hint] = CONF[c.confidence] ?? [c.confidence, '']
  const title = [t(hint), ...(c.sources || []), c.note].filter(Boolean).join('\n\n')
  return <span className={`src conf conf-${c.confidence}`} title={title}>{t(label)}</span>
}

/** One attribute cell. An absent value is content ("not sourced on this tier"),
    an uncertain one wears a ⚠ that opens its note — the value is shown, the
    doubt is shown beside it, neither is hidden. */
function AttrCell({ label, gloss, c }) {
  const { t } = useLang()
  const absent = c.confidence === 'absent'
  return (
    <div className={`rc-cell nk-cell${absent ? ' is-absent' : ''}`}>
      <span className="rc-key" title={gloss}>{label}</span>
      <span className="rc-val">
        {absent ? t('nakshatra.cell.notSourcedTier') : c.value}
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
  yes: ['nakshatra.compute.yes.label', 'nakshatra.compute.yes.hint'],
  partly: ['nakshatra.compute.partly.label', 'nakshatra.compute.partly.hint'],
  no: ['nakshatra.compute.no.label', 'nakshatra.compute.no.hint'],
}

function ModernTechniques({ t }) {
  const { t: tr } = useLang()
  const [open, setOpen] = useState(false)
  if (!t) return null
  return (
    <section className="nk-modern">
      <button type="button" className="nk-mod-toggle" aria-expanded={open}
              onClick={() => setOpen(!open)}>
        {open ? '−' : '+'} {tr('nakshatra.modern.toggle')}
        {t.available && <span className="nk-mod-count">{t.techniques.length}</span>}
        <span className="nk-mod-byline">{tr('nakshatra.modern.byline')}</span>
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
              {t.theme && (
                <p className="nk-mod-theme">
                  {tr('nakshatra.modern.theme')} <strong>{t.theme}</strong>
                </p>
              )}
              <ol className="nk-mod-list">
                {t.techniques.map((tech) => {
                  const [label, hint] = COMPUTABLE_BADGE[tech.computable] ?? [tech.computable, '']
                  return (
                    <li key={tech.n} className={tech.non_parashara ? 'is-np' : ''}>
                      <span className="nk-mod-gist">{tech.gist}</span>
                      <span className="nk-mod-meta">
                        <span className={`src compute compute-${tech.computable}`} title={tr(hint)}>{tr(label)}</span>
                        <span className="nk-mod-page" title={tech.cite}>{tr('nakshatra.modern.page')}{tech.page}</span>
                        {tech.non_parashara && (
                          <Cite className="src np-tag" detail={tech.non_parashara}>⚠ {tr('nakshatra.modern.nonParashara')}</Cite>
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

const FIELD_ORDER = ['symbol', 'gana', 'guna', 'yoni', 'body_part', 'purushartha',
  'quality', 'shakti', 'dosha', 'nadi']
const FALLBACK_META = {
  symbol: ['nakshatra.meta.symbol.label', 'nakshatra.meta.symbol.gloss'],
  gana: ['nakshatra.meta.gana.label', 'nakshatra.meta.gana.gloss'],
  guna: ['nakshatra.meta.guna.label', 'nakshatra.meta.guna.gloss'],
  yoni: ['nakshatra.meta.yoni.label', 'nakshatra.meta.yoni.gloss'],
  body_part: ['nakshatra.meta.bodyPart.label', 'nakshatra.meta.bodyPart.gloss'],
  purushartha: ['nakshatra.meta.purushartha.label', 'nakshatra.meta.purushartha.gloss'],
  quality: ['nakshatra.meta.quality.label', 'nakshatra.meta.quality.gloss'],
  shakti: ['nakshatra.meta.shakti.label', 'nakshatra.meta.shakti.gloss'],
  dosha: ['nakshatra.meta.dosha.label', 'nakshatra.meta.dosha.gloss'],
  nadi: ['nakshatra.meta.nadi.label', 'nakshatra.meta.nadi.gloss'],
}

export default function NakshatraCard({ n, fieldMeta, namer }) {
  const { t } = useLang()
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
            <span className="rc-limb-label">{t('nakshatra.head.deityLord')}</span>
            <strong>{b.deity_iast} · {namer.grahaKey(b.lord)}</strong>
            <Cite className="src src-sloka" detail={`BPHS — ${b.cite}`}>{t('nakshatra.head.sloka')}</Cite>
          </div>
        )}
      </header>

      {v && (
        <p className="rc-conflict-strip">
          <strong>{t('nakshatra.variance.flagged')}</strong> {v.source === 'S2' ? 'Sunil John' : v.source}{' '}
          gives {v.nakshatra} = <strong>{v.traditional}</strong>, where the app's
          BPHS-cited data gives <strong>{v.bphs_app}</strong>. {t('nakshatra.variance.standing')}
        </p>
      )}

      <section>
        <h4>{t('nakshatra.section.attributes')}</h4>
        <div className="rc-grid">
          {/* Guard on n.cells[f]: tolerate an older API payload that predates a
              field (dosha/guṇa) so the card never crashes mid-deploy. */}
          {FIELD_ORDER.filter((f) => n.cells[f]).map((f) => (
            <AttrCell key={f} label={t(label(f))} gloss={t(gloss(f))} c={n.cells[f]} />
          ))}
        </div>
        <p className="rc-note">{t('nakshatra.attributes.note')}</p>
      </section>

      {/* Last on the card, always. A different tier (modern), a different look,
          and never above the tiered attributes. */}
      <ModernTechniques t={n.techniques} />
    </article>
  )
}
