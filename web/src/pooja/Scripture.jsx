/**
 * "From the scriptures" — the verses behind an explanation.
 *
 * Each verse is shown as it is: the Sanskrit (checked against an independent
 * text before it was entered — sources.json), a plain roman reading made from
 * it letter by letter, and IN BRIEF what the named edition's translation says,
 * in our own words. The brief is never our translation of the Sanskrit.
 *
 * The scripture and verse are always named. Which edition and translator the
 * brief follows, and its page, are listed on /references — and shown here too
 * when references are switched on there, as everywhere else on the site.
 */
import SOURCES from './sources.json'
import { devToIast, plainRoman } from './guide.js'
import { refsOn } from '../refs.js'

/** The verses for a step ('steps') or a ceremony ('rituals'). */
export function versesFor(kind, key) {
  return (SOURCES[kind][key] || []).map((id) => ({ id, ...SOURCES.verses[id] })).filter((v) => v.dev)
}

export default function Scripture({ verses, lang = 'en', L, className = '' }) {
  if (!verses || !verses.length) return null
  const on = refsOn()
  return (
    <section className={`sh ${className}`} aria-label={L('From the scriptures', 'शास्त्र से')}>
      <p className="sh-h">{L('From the scriptures', 'शास्त्र से')}</p>
      {verses.map((v) => {
        const book = SOURCES.books[v.book]
        const long = v.dev.split('\n').length > 4 || v.prose
        return (
          <figure key={v.id} className="sh-v">
            <p className={`sh-dev${long ? ' long' : ''}`} lang="sa">{v.dev}</p>
            <p className={`sh-roman${long ? ' long' : ''}`}>{plainRoman(devToIast(v.dev))}</p>
            <figcaption>
              <b className="sh-ref">{book.name[lang] || book.name.en} {v.ref}</b>
              <span className="sh-gist"><i>{L('In brief', 'संक्षेप में')}:</i> {v.gist[lang] || v.gist.en}</span>
              {on && (
                <span className="sh-ed">
                  {book.after[lang] || book.after.en} — {book.edition}, {v.book === 'bhagavata' ? `vol ${v.vol}, PDF p.${v.page}` : `p.${v.page}`}
                </span>
              )}
            </figcaption>
          </figure>
        )
      })}
    </section>
  )
}
