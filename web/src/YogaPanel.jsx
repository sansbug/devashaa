/**
 * Yogas — the named BPHS combinations the chart forms. A yoga is shown only when
 * its geometric condition is met. Strength-gated yogas (Kahala, Sankha, Bheri,
 * Adhi, the strong-vargottama Moon) are now RESOLVED against the Ṣaḍbala engine:
 * "fructifies" when the gating graha is strong, "does not fructify" when the
 * geometry is present but that strength is lacking — and Adhi shows the office's
 * balakramat (strength order). When the Ṣaḍbala is unavailable a yoga falls back
 * to the honest "strength unverified" flag. Each card shows the cited śloka
 * effect, never asserted as fate.
 */
import { useState } from 'react'
import { useLang } from './LangContext.jsx'
import { yogaName } from './naming.js'
import { SENSITIVE } from './findings.js'

// A passage that speaks of a death, a lifespan or a bereavement is shown only on request, whole.
const sensitive = (s) => SENSITIVE.en.test(String(s || '')) || SENSITIVE.hi.test(String(s || ''))

const FAMILY = {
  nabhasa: 'Nābhasa', mahapurusha: 'Mahāpuruṣa', lunar: 'yoga.family.lunar',
  solar: 'yoga.family.solar', other: 'ch.36', raja: 'Rāja',
  dusthana: 'Phaladīpikā 6.57', nicabhanga: 'Nīcabhaṅga', pravrajya: 'Pravrajyā',
}
// Non-BPHS yogas name their book on the chip (BPHS is the panel's default).
const BOOK = { phaladipika: 'Phaladīpikā', brihat_jataka: 'Bṛhat Jātaka' }
// Long provenance string → the chapter/verse tail for the chip.
const shortCite = (c, source) => {
  const m = (c || '').match(/(Ch|Adh)\.\s?\d+.*/i)
  const tail = m ? m[0].replace(/\s*\(printed[^)]*\)/g, '').trim() : c
  return BOOK[source] ? `${BOOK[source]}, ${tail}` : tail
}
// Drop a leading verse-number label ("20-22. ") the extraction sometimes keeps.
const effectText = (t) => (t || '').replace(/^\d+\s*[-–]?\s*\d*\.\s*/, '')

// The Ṣaḍbala resolution of a strength-gated yoga: the verdict chip, the gating
// role, and each gating graha with its rūpa and strong/weak mark.
function Strength({ s, namer }) {
  const { t } = useLang()
  const isAdhi = /balakramat/.test(s.role || '')
  return (
    <div className="yoga-strength">
      <span className={`yoga-str ${s.fructifies ? 'ok' : 'no'}`} title={s.basis}>
        {isAdhi ? t('yoga.str.ranked') : s.fructifies ? t('yoga.str.fructifies') : t('yoga.str.notFructify')}
      </span>
      <span className="yoga-str-role">{s.role}</span>
      {(s.grahas || []).map((gr) => (
        <span key={gr.graha} className={`yoga-str-g ${gr.strong ? 'strong' : 'weak'}`}
              title={`${gr.rupa} rūpa vs minimum ${gr.min} → ${gr.strong ? 'strong' : 'weak'}`}>
          {namer ? namer.grahaKey(gr.graha) : gr.graha} {gr.rupa}r {gr.strong ? '✓' : '✕'}
        </span>
      ))}
    </div>
  )
}

function Effect({ text }) {
  const { lang } = useLang()
  const [asked, setAsked] = useState(false)
  const W = (en, hi) => (lang === 'hi' ? hi : en)
  if (sensitive(text) && !asked) {
    return (
      <p className="yoga-effect fd-held">
        {W('The text’s effect for this Yog speaks of a death, a lifespan or a bereavement, so it is not shown unasked.',
           'इस योग का ग्रंथोक्त फल मृत्यु, आयु या वियोग की बात करता है, इसलिए बिना पूछे नहीं दिखाया जाता।')}
        {' '}<button type="button" className="sv-link" onClick={() => setAsked(true)}>{W('Show the whole passage', 'पूरा अंश दिखाएँ')}</button>
      </p>
    )
  }
  return <p className="yoga-effect">{effectText(text)}</p>
}

export default function YogaPanel({ data, namer }) {
  const { t } = useLang()
  if (!data || data.error || !data.detected) return null
  const dt = data.detected
  return (
    <section className="table-panel yoga-panel" id="rg-yoga">
      <h3>{t('yoga.title')}</h3>
      <p className="rc-note">
        {dt.length} of {data.catalogued} catalogued Yogs are present (BPHS, with a few from Phaladīpikā and Bṛhat Jātaka, each cited). A Yog is
        listed only when its geometric condition is met. The effect is the cited
        śloka, not a fated prediction. There is no per-Yog score.{' '}
        {data.strength_resolved
          ? t('yoga.note.resolved')
          : t('yoga.note.unresolved')}
      </p>
      {dt.length === 0 ? (
        <p className="yoga-none">{t('yoga.none')}</p>
      ) : (
        <div className="yoga-list">
          {dt.map((y) => (
            <div key={y.name}
                 className={`yoga-card fam-${y.family}`
                   + (y.strength && !y.strength.fructifies ? ' yoga-dormant' : '')}>
              <div className="yoga-head">
                <span className="yoga-name">{yogaName(y.name)}</span>
                <span className="yoga-fam">{t(FAMILY[y.family] || y.family)}</span>
                {y.computability === 'strength_gated' && !y.strength && (
                  <span className="yoga-sg" title={y.strength_note || t('yoga.sg.title')}>
                    {t('yoga.sg.unverified')}
                  </span>
                )}
              </div>
              <Effect text={y.effect} />
              {y.strength && <Strength s={y.strength} namer={namer} />}
              <span className="src">{shortCite(y.citation, y.source)}</span>
            </div>
          ))}
        </div>
      )}
    </section>
  )
}
