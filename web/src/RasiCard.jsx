/**
 * A rāśi reference card — what BPHS says about one sign, and what it doesn't.
 *
 * NO DATE RANGE, deliberately. BPHS has no sun-sign: there is not one statement
 * of the form "one born with the Sun in X" in either volume, and ch.34 — the
 * closest thing to "what your sign means" — is keyed to the LAGNA throughout.
 * Printing tropical dates would also contradict this site's own sidereal
 * engine (someone born 10 August is a tropical Leo but sidereal Karka), and
 * printing *sidereal* dates would fix the arithmetic while leaving the
 * conceptual import intact. So the cards are reference pages, and users reach
 * their own signs by casting a chart.
 *
 * NO ANIMAL. BPHS gives an emblem to five signs only, and Siṁha is not one of
 * them — there is no ram, bull, lion, scorpion or goat anywhere in the text.
 * The card is built from geometry the text actually supports: the degree band
 * of the sign, its dignities, its nakṣatra spans, its aspects.
 *
 * Every value carries a source badge. The one panel that must look as good as
 * any other is "What BPHS does not say" — that panel is the product.
 */

import { useState } from 'react'
import { useLang } from './LangContext.jsx'

const SRC_LABEL = {
  sloka: 'rasi.src.sloka', note: 'rasi.src.note', table: 'rasi.src.table',
  derived: 'rasi.src.derived', absent: 'rasi.src.absent', ocr_lost: 'rasi.src.ocrLost',
}

/** Source badge. `note` is visually distinct from `sloka` on purpose: the
    difference between Parāśara and his translator is the site's whole claim. */
function Src({ src, cite, title }) {
  const { t } = useLang()
  if (!src) return null
  return (
    <span className={`src src-${src}`} title={title || cite || ''}>
      {SRC_LABEL[src] ? t(SRC_LABEL[src]) : src}
    </span>
  )
}

function Cell({ label, c }) {
  const { t } = useLang()
  if (!c) return null
  const absent = c.src === 'absent' || c.src === 'ocr_lost'
  return (
    <div className={`rc-cell${absent ? ' is-absent' : ''}`}>
      <span className="rc-key">{label}</span>
      <span className="rc-val">
        {absent
          ? (c.src === 'absent' ? t('rasi.cell.silent') : t('rasi.cell.lostInScan'))
          : String(c.value)}
      </span>
      <Src src={c.src} cite={c.ref} title={c.ocr || c.note || c.ref} />
      {c.conflict && <span className="rc-conflict" title={c.conflict}>⚠</span>}
    </div>
  )
}

/** The sign's own 0-30° band: mūlatrikoṇa arcs, exaltation and fall points.
    Reuses the degree-ruler vocabulary from the D1 chart so the two read as
    one instrument rather than two decorations. */
function DignityBand({ d, namer }) {
  const { t } = useLang()
  const x = (deg) => deg * 10
  return (
    <div className="rc-band">
      <svg viewBox="0 0 300 44" className="rc-band-svg" aria-hidden="true">
        <line x1="0" y1="30" x2="300" y2="30" className="rl-axis" />
        <line x1="0.5" y1="26" x2="0.5" y2="34" className="rl-axis" />
        <line x1="299.5" y1="26" x2="299.5" y2="34" className="rl-axis" />
        {[10, 20].map((tick) => (
          <line key={tick} x1={x(tick)} y1="30" x2={x(tick)} y2="35" className="rl-pada" />
        ))}
        {d.moolatrikona.map((a) => (
          <g key={`m${a.graha}`}>
            <rect x={x(a.from)} y="22" width={x(a.to - a.from)} height="8"
                  className="rc-mt-arc" />
            <text x={x((a.from + a.to) / 2)} y="20" className="rc-band-label">
              {namer.grahaKey(a.graha)} {t('rasi.band.moolatrikona')}
            </text>
          </g>
        ))}
        {d.exaltation.map((p) => (
          <g key={`u${p.graha}`}>
            <path d={`M ${x(p.degree) - 5},38 L ${x(p.degree)},30 L ${x(p.degree) + 5},38`}
                  className="rl-uccha" />
            <text x={x(p.degree)} y="44" className="rc-band-label">
              {namer.grahaKey(p.graha)} ↑ {p.degree}°
            </text>
          </g>
        ))}
        {d.debilitation.map((p) => (
          <g key={`n${p.graha}`}>
            <path d={`M ${x(p.degree) - 5},30 L ${x(p.degree)},38 L ${x(p.degree) + 5},30`}
                  className="rl-nica" />
            <text x={x(p.degree)} y="44" className="rc-band-label">
              {namer.grahaKey(p.graha)} ↓ {p.degree}°
            </text>
          </g>
        ))}
      </svg>
      {d.empty && (
        // A real, citable fact rather than an empty panel — and it is true of
        // exactly four signs, which makes it informative rather than filler.
        <p className="rc-note">{t('rasi.dignity.emptyNote')} <Src src="sloka" cite="ch.3 vv.49-50" /></p>
      )}
      {d.debilitation.length > 0 && (
        <p className="rc-note">{t('rasi.dignity.fallDerived')}</p>
      )}
    </div>
  )
}

function NakshatraBand({ n }) {
  const { t } = useLang()
  const x = (deg) => deg * 10
  return (
    <div className="rc-band">
      <svg viewBox="0 0 300 30" className="rc-band-svg" aria-hidden="true">
        {n.spans.map((s, i) => {
          // A rāśi's first or last segment can be a single pāda — 3°20′, a
          // ninth of the strip — and a centred label there overhangs the band.
          // Anchor those to the near edge instead of clamping the text, so the
          // label still points at its own segment.
          const mid = (s.from + s.to) / 2
          const anchor = mid < 4 ? 'start' : mid > 26 ? 'end' : 'middle'
          const tx = anchor === 'start' ? 2 : anchor === 'end' ? 298 : x(mid)
          return (
            <g key={s.nakshatra}>
              <rect x={x(s.from)} y="6" width={x(s.to - s.from) - 1} height="14"
                    className={`rc-nak-seg seg-${i % 2}`} />
              <text x={tx} y="16" textAnchor={anchor} className="rc-nak-label">
                {s.nakshatra}
              </text>
              <text x={tx} y="27" textAnchor={anchor} className="rc-band-label">
                {t('rasi.band.pada')} {s.padas.join(',')}
              </text>
            </g>
          )
        })}
      </svg>
      <p className="rc-note">
        {t('rasi.nakshatra.note')}
        <Src src="table" cite="Vol II ch.46" title={n.note} />
        <br /><em>{n.note}</em>
      </p>
    </div>
  )
}

/** Rāśi dṛṣṭi as a ring of chords — the visual satisfaction of a
    compatibility wheel with none of the fabrication. */
function DrishtiRing({ sign, aspects, names }) {
  const { t } = useLang()
  const R = 46, C = 56
  const pt = (i) => {
    const a = ((i - sign) * 30 - 90) * Math.PI / 180
    return [C + R * Math.cos(a), C + R * Math.sin(a)]
  }
  return (
    <div className="rc-ring">
      <svg viewBox="0 0 112 112" aria-hidden="true">
        <circle cx={C} cy={C} r={R} className="rc-ring-circle" />
        {aspects.map((target) => {
          const [x1, y1] = pt(sign), [x2, y2] = pt(target)
          return <line key={target} x1={x1} y1={y1} x2={x2} y2={y2} className="rc-chord" />
        })}
        {Array.from({ length: 12 }, (_, k) => {
          const i = (sign + k) % 12
          const [cx, cy] = pt(i)
          const on = i === sign || aspects.includes(i)
          return <circle key={i} cx={cx} cy={cy} r={i === sign ? 3.6 : 2.4}
                         className={`rc-node${i === sign ? ' self' : on ? ' on' : ''}`} />
        })}
      </svg>
      <div>
        <p className="rc-ring-text">
          {t('rasi.drishti.aspectsLabel')} <strong>{aspects.map((i) => names[i]).join(', ')}</strong>
        </p>
        <p className="rc-note">
          {t('rasi.drishti.note')} <Src src="sloka" cite="Vol I ch.8 vv.1-5" />
        </p>
      </div>
    </div>
  )
}

/**
 * Santhanam's ascendant sketch — Vol II ch.78.
 *
 * The only block on this card that is not Parāśara, and the rules around it are
 * the reason it can exist at all:
 *
 *  - COLLAPSED by default, and last on the card. A reader must choose to open
 *    it; it can never be mistaken for the śloka panels above.
 *  - Styled deliberately unlike them — dashed, no accent, a byline instead of a
 *    citation badge.
 *  - The disclaimer sits ABOVE the text, not under it as a footnote.
 *  - The raw scan is available, so a reader can see exactly what was repaired.
 *
 * The argument for including it at all: a reader who wants personality traits
 * will otherwise go and get them from a site that presents the same 20th-century
 * material as ancient doctrine. Here they get it with the provenance attached.
 */
function TranslatorSketch({ s, sign }) {
  const { t } = useLang()
  const [open, setOpen] = useState(false)
  const [raw, setRaw] = useState(false)
  if (!s?.excerpt) return null
  return (
    <section className="rc-translator">
      <button type="button" className="rc-tr-toggle" aria-expanded={open}
              onClick={() => setOpen(!open)}>
        {open ? '−' : '+'} Santhanam's sketch of the {sign} ascendant
        <span className="rc-tr-byline">{t('rasi.sketch.byline')}</span>
      </button>
      {open && (
        <div className="rc-tr-body">
          <p className="rc-tr-warn">{s.disclaimer}</p>
          {s.confidence === 'low' && (
            <p className="rc-tr-warn low">
              {t('rasi.sketch.lowConf')}
            </p>
          )}
          <blockquote className="rc-tr-quote">{s.excerpt}</blockquote>
          <p className="rc-note">
            {s.ref} · {t('rasi.sketch.pdfPage')}{s.pdf_page}. {t('rasi.sketch.ocrNote')}
            <button type="button" className="rc-tr-raw" onClick={() => setRaw(!raw)}>
              {raw ? t('rasi.sketch.hide') : t('rasi.sketch.show')} {t('rasi.sketch.unrepairedScan')}
            </button>
          </p>
          {raw && <blockquote className="rc-tr-quote scan">{s.scan}</blockquote>}
          {raw && s.uncertain?.length > 0 && (
            <p className="rc-note">
              {t('rasi.sketch.uncertainTokens')} {s.uncertain.map((u) => `“${u}”`).join(', ')}
            </p>
          )}
        </div>
      )}
    </section>
  )
}

export default function RasiCard({ r, namer, names }) {
  const [showAll, setShowAll] = useState(false)
  const { t } = useLang()
  if (!r) return null
  const a = r.attributes
  const lagna = r.as_lagna.grahas.filter((g) => !g.is_node)
  const good = lagna.filter((g) => g.nature === 'benefic')
  const bad = lagna.filter((g) => g.nature === 'malefic')
  const killers = lagna.filter((g) => g.maraka)

  return (
    <article className="rasi-card">
      <header className="rc-head">
        <div>
          <h3>{namer.style === 'devanagari' ? namer.rasi(r.sign) : r.name}</h3>
          <p className="rc-sub">
            {namer.style !== 'devanagari' && <>{r.name_en} · </>}
            {t('rasi.head.ruledBy')} {namer.grahaKey(r.lord)} · {r.modality.value}
          </p>
        </div>
        <div className="rc-limb">
          <span className="rc-limb-label">{t('rasi.head.limb')}</span>
          <strong>{r.kalapurusha_limb.value}</strong>
          <Src src="sloka" cite="ch.4 vv.1-2" title={r.kalapurusha_limb.note} />
        </div>
      </header>

      {r.conflict && (
        <p className="rc-conflict-strip"><strong>{t('rasi.conflict.strip')}</strong> {r.conflict}</p>
      )}

      <section>
        <h4>{t('rasi.section.glance')}</h4>
        <div className="rc-grid">
          <Cell label={t('rasi.attr.element')} c={a.element} />
          <Cell label={t('rasi.attr.dosha')} c={a.dosha} />
          <Cell label={t('rasi.attr.guna')} c={a.guna} />
          <Cell label={t('rasi.attr.varna')} c={a.varna} />
          <Cell label={t('rasi.attr.rises')} c={a.rising} />
          <Cell label={t('rasi.attr.strongBy')} c={a.strong} />
          <Cell label={t('rasi.attr.direction')} c={a.direction} />
          <Cell label={t('rasi.attr.complexion')} c={a.complexion} />
          <Cell label={t('rasi.attr.build')} c={a.build} />
          <Cell label={t('rasi.attr.habitat')} c={a.habitat} />
          <Cell label={t('rasi.attr.feet')} c={a.feet} />
        </div>
      </section>

      <section>
        <h4>{t('rasi.section.dignityMap')}</h4>
        <DignityBand d={r.dignities} namer={namer} />
      </section>

      <section>
        <h4>{t('rasi.section.nakshatrasPadas')}</h4>
        <NakshatraBand n={r.nakshatras} />
      </section>

      <section>
        <h4>{t('rasi.section.rasiDrishti')}</h4>
        <DrishtiRing sign={r.sign} aspects={r.rasi_drishti.aspects} names={names} />
      </section>

      <section>
        <h4>{t('rasi.section.grahasForLagna')}</h4>
        {/* The single most genuinely-BPHS thing on the card, and nothing on a
            Western sign card resembles it: mūla śloka, per ascendant. */}
        <div className="rc-lagna">
          <div><span className="rc-key">{t('rasi.lagna.auspicious')}</span>
            <strong>{good.map((g) => namer.grahaKey(g.graha)).join(', ') || '—'}</strong></div>
          <div><span className="rc-key">{t('rasi.lagna.malefic')}</span>
            <strong>{bad.map((g) => namer.grahaKey(g.graha)).join(', ') || '—'}</strong></div>
          <div><span className="rc-key">{t('rasi.lagna.maraka')}</span>
            <strong>{killers.map((g) => namer.grahaKey(g.graha)).join(', ') || '—'}</strong></div>
        </div>
        {lagna.some((g) => g.nature === null) && (
          <p className="rc-note">
            BPHS states no nature for{' '}
            {lagna.filter((g) => g.nature === null).map((g) => namer.grahaKey(g.graha)).join(', ')}
            {' '}at this lagna. A māraka verdict is kept strictly apart from a
            benefic/malefic nature — ch.34's own note forbids mixing them.
          </p>
        )}
      </section>

      <section>
        <h4>{t('rasi.section.whereUsed')}</h4>
        <div className="rc-grid">
          <Cell label={t('rasi.tech.bhavaBala')} c={r.technical.bhava_bala_deduction} />
          <Cell label={t('rasi.tech.rasimana')} c={r.technical.rasimana} />
          <Cell label={t('rasi.tech.sthiraDasha')} c={r.technical.sthira_dasha_years} />
          <div className={`rc-cell${r.technical.badhaka_of.value === null ? ' is-absent' : ''}`}>
            <span className="rc-key">{t('rasi.tech.badhaka')}</span>
            <span className="rc-val">
              {r.technical.badhaka_of.value === null
                ? t('rasi.tech.noBadhakaRule')
                : names[r.technical.badhaka_of.value]}
            </span>
            <Src src={r.technical.badhaka_of.src} cite={r.technical.badhaka_of.ref}
                 title={r.technical.badhaka_of.note} />
          </div>
          {r.technical.is_badhaka_for.value !== null && (
            <div className="rc-cell">
              <span className="rc-key">{t('rasi.tech.isBadhakaFor')}</span>
              <span className="rc-val">{names[r.technical.is_badhaka_for.value]}</span>
              <Src src={r.technical.is_badhaka_for.src}
                   cite={r.technical.is_badhaka_for.ref}
                   title={r.technical.is_badhaka_for.note} />
            </div>
          )}
        </div>
        <p className="rc-note">{r.technical.badhaka_of.note}</p>
      </section>

      {/* The differentiator. Styled to be as good-looking as anything above it,
          because it is the reason a serious reader trusts the rest. */}
      <section className="rc-absent-panel">
        <h4>What BPHS does not say about {r.name}</h4>
        <div className="rc-chips">
          {r.not_in_bphs.attributes.map((t) => <span key={t} className="rc-chip">{t}</span>)}
        </div>
        <p className="rc-note">{r.not_in_bphs.note}</p>
        <p className="rc-note">{r.not_in_bphs.symbol_note}</p>
        {(r.absent.length > 0 || r.ocr_lost.length > 0) && (
          <p className="rc-note">
            <strong>Specific to {r.name}:</strong>{' '}
            {r.absent.length > 0 && <>the text states no {r.absent.join(', ')}. </>}
            {r.ocr_lost.length > 0 && (
              <>Its {r.ocr_lost.join(', ')} is present in the book but destroyed
                in this scan, so it is left blank rather than guessed.</>
            )}
          </p>
        )}
        <button type="button" className="rc-toggle" onClick={() => setShowAll(!showAll)}>
          {showAll ? t('rasi.absent.hide') : t('rasi.absent.whyToggle')}
        </button>
        {showAll && (
          <p className="rc-note rc-why">{t('rasi.absent.why')}</p>
        )}
      </section>

      {/* Last on the card, always. Never above the fold. */}
      <TranslatorSketch s={r.translator_sketch} sign={r.name} />
    </article>
  )
}
