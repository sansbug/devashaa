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

const KIND_LABEL = {
  uccha: 'exalted · uccha',
  neecha: 'debilitated · nīca',
  swakshetra: 'own sign · svakṣetra',
  ordinary: 'vargottama',
  subha: 'śubha — benefic sign',
  papa: 'pāpa — malefic sign',
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
  yes: ['trigger detectable', 'The structural trigger — a D9 sign, a navāṁśa index, a dispositor — is cleanly detectable from the chart.'],
  partly: ['partly detectable', 'The trigger is partly detectable but leans on something not computed (D9-internal aspects, an ariṣṭa/timing or death judgment).'],
  no: ['not computed', 'Not a structural flag the app computes (e.g. a navāṁśa Aṣṭakavarga).'],
}

/** Patel's Part-II interpretive techniques — a MODERN pointer index. Collapsed,
    styled unlike the computed signals above, disclaimer first: each entry names
    the method + its classical source + page, and reproduces none of his result
    tables. Never a verdict. */
function Part2Techniques({ data }) {
  const [open, setOpen] = useState(false)
  if (!data || !data.techniques?.length) return null
  return (
    <section className="nk-modern nv-part2">
      <button type="button" className="nk-mod-toggle" aria-expanded={open} onClick={() => setOpen(!open)}>
        {open ? '−' : '+'} Part II techniques
        <span className="nk-mod-count">{data.count}</span>
        <span className="nk-mod-byline">Patel's interpretive index — named, not reproduced</span>
      </button>
      {open && (
        <div className="nk-mod-body">
          <p className="nk-mod-warn">
            An attributed <strong>pointer index</strong> of C. S. Patel's Part II
            (Ch.XVI–XX): each technique is <em>named</em> with its classical source
            and page — <strong>none of his result tables are reproduced.</strong>{' '}
            Modern tier, not BPHS, and <strong>not a verdict on any chart.</strong>{' '}
            The badge says only whether the app could detect the structural trigger.
          </p>
          <ol className="nk-mod-list">
            {data.techniques.map((t) => {
              const [label, hint] = COMPUTABLE[t.computable] ?? [t.computable, '']
              return (
                <li key={t.n}>
                  <span className="nk-mod-gist">
                    <strong>{t.technique}.</strong> {t.gist}
                  </span>
                  <span className="nk-mod-meta">
                    <span className={`src compute compute-${t.computable}`} title={hint}>{label}</span>
                    <span className="nv-src" title={`Ch.${t.chapter} — ${t.source}`}>{t.source}</span>
                    <span className="nk-mod-page" title={`Patel Ch.${t.chapter}, p.${t.page}`}>p.{t.page}</span>
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
  if (!data || data.error) return null
  const nameOf = (key) => (key === 'lagna' ? 'Lagna' : namer.grahaKey(key))
  const v = data.vargottama
  const p = data.pushkara
  const k = data.khara
  const b = data.bhava_suchaka

  return (
    <section className="rasi-card nv-panel" aria-label="Navāṁśa (D9) analysis">
      <header className="rc-head">
        <div>
          <h3>Navāṁśa (D9) analysis</h3>
          <p className="rc-sub">{data.source}</p>
        </div>
        <span className="src np-tag" title={data.note}>modern · C. S. Patel</span>
      </header>
      <p className="rc-note">{data.note}</p>

      <Group title="Vargottama" citation={v.citation} gloss={v.gloss}
             count={v.items.length}
             empty="No vargottama here — nothing occupies the same sign in the D1 and the D9.">
        {v.items.map((it) => (
          <li key={it.key}>
            <strong>{nameOf(it.key)}</strong> in <em>{namer.rasi(it.sign)}</em>
            <span className={`nv-kind nv-k-${it.kind}`}>{KIND_LABEL[it.kind] ?? it.kind}</span>
            {it.result && <span className="nv-note"> — {it.result}</span>}
          </li>
        ))}
      </Group>

      <Group title="Pushkara navāṁśa" citation={p.citation} gloss={p.gloss}
             count={p.items.length}
             empty="No graha falls in a pushkara navāṁśa.">
        {p.items.map((it) => (
          <li key={it.key}>
            <strong>{nameOf(it.key)}</strong>
            <span className="nv-note"> — {ORD[it.navamsa_index]} navāṁśa of {namer.rasi(it.sign)} → {namer.rasi(it.navamsa_sign)}</span>
          </li>
        ))}
      </Group>

      <Group title="The 64th navāṁśa · Khara" citation={k.citation} gloss={k.gloss}
             count={k.items.length} empty="—">
        {k.items.map((it) => (
          <li key={it.key}>
            From <strong>{nameOf(it.key)}</strong> <span className="nv-karaka">({it.karaka})</span> →{' '}
            <em>{namer.rasi(it.navamsa_sign)}</em> navāṁśa in {namer.rasi(it.rasi_8th)} <span className="nv-dim">(the 8th rāśi)</span>
            {it.lord && <>, lord <strong>{namer.grahaKey(it.lord)}</strong>
              {it.lord_house && <span className="nv-dim"> in the {ORD[it.lord_house]} house</span>}
              {it.lord_in_dusthana && <span className="nv-warn">lord in a dusthāna</span>}</>}
          </li>
        ))}
      </Group>

      <section className="nv-group">
        <h4>Bhāva-sūchaka navāṁśa <span className="nv-cite" title={`C. S. Patel — ${b.citation}`}>{b.citation}</span></h4>
        <p className="nv-gloss">{b.gloss}</p>
        <div className="nv-tally" role="group" aria-label="prosperity tally">
          <span className="nv-t-good">{b.tally.prosperous} prosperous</span>
          <span className="nv-t-neutral">{b.tally.neutral} neutral</span>
          <span className="nv-t-bad">{b.tally.difficult} difficult</span>
        </div>
        <ul className="nv-list nv-bhava">
          {b.items.map((it) => (
            <li key={it.key}
                className={it.favourable === true ? 'is-good' : it.favourable === false ? 'is-bad' : ''}>
              <strong>{nameOf(it.key)}</strong> → <span className="nv-label">{it.label}</span>
              <span className="nv-dim"> ({ORD[it.house]} house)</span>
              <span className="nv-note"> — {it.meaning}</span>
            </li>
          ))}
        </ul>
      </section>

      <Part2Techniques data={data.patel_part2} />
    </section>
  )
}
