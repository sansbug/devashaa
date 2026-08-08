/**
 * Navāṁśa (D9) analysis — tier `modern`, C. S. Patel (*Navamsa in Astrology*).
 *
 * Shown only when the D9 is the selected varga. Everything here is COMPUTED from
 * the D9 the app already draws (BPHS ch.6 v.12); the *readings* — vargottama,
 * pushkara, the 64th navāṁśa, the bhāva-sūchaka nomenclature — are Patel's modern
 * synthesis, on their own tier, never blended with the BPHS layer. The structural
 * fact ("Jupiter is vargottama") is certain; the meaning beside it is attributed.
 */

import { useState } from 'react'
import Cite from './Cite.jsx'
import { useLang } from './LangContext.jsx'

const KIND_LABEL = {
  uccha: 'navamsa.kind.exalted',
  neecha: 'navamsa.kind.debilitated',
  swakshetra: 'navamsa.kind.ownSign',
  ordinary: 'navamsa.kind.vargottama',
  subha: 'navamsa.kind.subha',
  papa: 'navamsa.kind.papa',
}

const ORD = ['', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th',
  '10th', '11th', '12th']

function Group({ title, citation, gloss, empty, children, count }) {
  return (
    <section className="nv-group">
      <h4>{title} <span className="nv-cite" title={`C. S. Patel — ${citation}`}>{citation}</span></h4>
      {gloss && <p className="nv-gloss">{gloss}</p>}
      {count === 0
        ? <p className="nv-empty">{empty}</p>
        : <ul className="nv-list">{children}</ul>}
    </section>
  )
}

const COMPUTABLE = {
  yes: ['navamsa.compute.yes.label', 'navamsa.compute.yes.hint'],
  partly: ['navamsa.compute.partly.label', 'navamsa.compute.partly.hint'],
  no: ['navamsa.compute.no.label', 'navamsa.compute.no.hint'],
}

/** Patel's Part-II interpretive techniques — a MODERN pointer index. Collapsed,
    styled unlike the computed signals above, disclaimer first: each entry names
    the method + its classical source + page, and reproduces none of his result
    tables. Never a verdict. */
function Part2Techniques({ data }) {
  const [open, setOpen] = useState(false)
  const { t } = useLang()
  if (!data || !data.techniques?.length) return null
  return (
    <section className="nk-modern nv-part2">
      <button type="button" className="nk-mod-toggle" aria-expanded={open} onClick={() => setOpen(!open)}>
        {open ? '−' : '+'} {t('navamsa.part2.toggle')}
        <span className="nk-mod-count">{data.count}</span>
        <span className="nk-mod-byline">{t('navamsa.part2.byline')}</span>
      </button>
      {open && (
        <div className="nk-mod-body">
          <p className="nk-mod-warn">{t('navamsa.part2.warn')}</p>
          <ol className="nk-mod-list">
            {data.techniques.map((tech) => {
              const [label, hint] = COMPUTABLE[tech.computable] ?? [tech.computable, '']
              return (
                <li key={tech.n}>
                  <span className="nk-mod-gist">
                    <strong>{tech.technique}.</strong> {tech.gist}
                  </span>
                  <span className="nk-mod-meta">
                    <Cite className={`src compute compute-${tech.computable}`} detail={t(hint)}>{t(label)}</Cite>
                    <Cite className="nv-src" detail={`Ch.${tech.chapter} — ${tech.source}`}>{tech.source}</Cite>
                    <span className="nk-mod-page" title={`Patel Ch.${tech.chapter}, p.${tech.page}`}>{t('navamsa.page.abbr')}{tech.page}</span>
                  </span>
                </li>
              )
            })}
          </ol>
        </div>
      )}
    </section>
  )
}

export default function NavamsaPanel({ data, namer }) {
  const { t } = useLang()
  if (!data || data.error) return null
  const nameOf = (key) => (key === 'lagna' ? t('navamsa.lagna') : namer.grahaKey(key))
  const v = data.vargottama
  const p = data.pushkara
  const k = data.khara
  const b = data.bhava_suchaka

  return (
    <section className="rasi-card nv-panel" aria-label={t('navamsa.title')}>
      <header className="rc-head">
        <div>
          <h3>{t('navamsa.title')}</h3>
          <p className="rc-sub">{data.source}</p>
        </div>
        <Cite className="src np-tag" detail={data.note}>{t('navamsa.tierTag')}</Cite>
      </header>
      <p className="rc-note">{data.note}</p>

      <Group title={t('navamsa.group.vargottama')} citation={v.citation} gloss={v.gloss}
             count={v.items.length}
             empty={t('navamsa.vargottama.empty')}>
        {v.items.map((it) => (
          <li key={it.key}>
            <strong>{nameOf(it.key)}</strong> in <em>{namer.rasi(it.sign)}</em>
            <span className={`nv-kind nv-k-${it.kind}`}>{t(KIND_LABEL[it.kind] ?? it.kind)}</span>
            {it.result && <span className="nv-note"> — {it.result}</span>}
          </li>
        ))}
      </Group>

      <Group title={t('navamsa.group.pushkara')} citation={p.citation} gloss={p.gloss}
             count={p.items.length}
             empty={t('navamsa.pushkara.empty')}>
        {p.items.map((it) => (
          <li key={it.key}>
            <strong>{nameOf(it.key)}</strong>
            <span className="nv-note"> — {ORD[it.navamsa_index]} navāṁśa of {namer.rasi(it.sign)} → {namer.rasi(it.navamsa_sign)}</span>
          </li>
        ))}
      </Group>

      <Group title={t('navamsa.group.khara')} citation={k.citation} gloss={k.gloss}
             count={k.items.length} empty="—">
        {k.items.map((it) => (
          <li key={it.key}>
            From <strong>{nameOf(it.key)}</strong> <span className="nv-karaka">({it.karaka})</span> →{' '}
            <em>{namer.rasi(it.navamsa_sign)}</em> navāṁśa in {namer.rasi(it.rasi_8th)} <span className="nv-dim">(the 8th rāśi)</span>
            {it.lord && <>, lord <strong>{namer.grahaKey(it.lord)}</strong>
              {it.lord_house && <span className="nv-dim"> in the {ORD[it.lord_house]} house</span>}
              {it.lord_in_dusthana && <span className="nv-warn">{t('navamsa.khara.dusthana')}</span>}</>}
          </li>
        ))}
      </Group>

      <section className="nv-group">
        <h4>{t('navamsa.group.bhavaSuchaka')} <span className="nv-cite" title={`C. S. Patel — ${b.citation}`}>{b.citation}</span></h4>
        <p className="nv-gloss">{b.gloss}</p>
        <div className="nv-tally" role="group" aria-label={t('navamsa.tally.aria')}>
          <span className="nv-t-good">{b.tally.prosperous} {t('navamsa.tally.prosperous')}</span>
          <span className="nv-t-neutral">{b.tally.neutral} {t('navamsa.tally.neutral')}</span>
          <span className="nv-t-bad">{b.tally.difficult} {t('navamsa.tally.difficult')}</span>
        </div>
        <ul className="nv-list nv-bhava">
          {b.items.map((it) => (
            <li key={it.key}
                className={it.favourable === true ? 'is-good' : it.favourable === false ? 'is-bad' : ''}>
              <strong>{nameOf(it.key)}</strong> → <span className="nv-label">{it.label}</span>
              <span className="nv-dim"> ({ORD[it.house]} {t('navamsa.house')})</span>
              <span className="nv-note"> — {it.meaning}</span>
            </li>
          ))}
        </ul>
      </section>

      <Part2Techniques data={data.patel_part2} />
    </section>
  )
}
