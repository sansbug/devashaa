/**
 * The simple view — what a first-time visitor meets before the full analysis.
 *
 * Nothing here judges the chart. The tiles state placements (which sign rises,
 * where the Moon stands, the Moon's nakṣatra); the "running now" card states
 * which daśā periods are current and when they end. Every reading, strength and
 * verdict stays in the full analysis, where it carries its source.
 */
import { useEffect, useMemo, useState } from 'react'
import { buildWalkthrough, HOUSE } from './walkthrough.js'
import { useLang } from './LangContext.jsx'
import { Bubble } from './DashaGlyphs.jsx'

/** True once `busy` has lasted longer than `ms` — for an honest "this is slow" line. */
export function useSlow(busy, ms = 4000) {
  const [slow, setSlow] = useState(false)
  useEffect(() => {
    if (!busy) { setSlow(false); return }
    const id = setTimeout(() => setSlow(true), ms)
    return () => clearTimeout(id)
  }, [busy, ms])
  return slow
}

export function Tiles({ items, title, tag }) {
  return (
    <div className="sv-tiles-wrap">
      {(title || tag) && (
        <div className="sv-tiles-head">
          {title && <span className="sv-tiles-title">{title}</span>}
          {tag && <span className="sv-tag">{tag}</span>}
        </div>
      )}
      <div className="sv-tiles">
        {items.map((it) => (
          <div className="sv-tile" key={it.label}>
            <span className="sv-tile-label">{it.label}</span>
            <b className="sv-tile-value">{it.value}</b>
            {it.sub && <span className="sv-tile-sub">{it.sub}</span>}
          </div>
        ))}
      </div>
    </div>
  )
}

/** The three placements, for this chart. */
export function chartTiles(chart, namer, t) {
  const moon = chart.grahas.find((g) => g.key === 'moon')
  const out = [{
    label: t('sv.asc', 'Ascendant'),
    value: namer.rasiFull(chart.lagna_rasi),
    sub: `${t('sv.asc.sub', 'Lagna')}`,
  }]
  if (moon) {
    out.push({
      label: t('sv.moon', 'Moon sign'),
      value: namer.rasiFull(moon.rasi),
      sub: `${t('sv.moon.sub', 'Janma rāśi')}`,
    })
    if (moon.nakshatra) {
      out.push({
        label: t('sv.star', 'Birth star'),
        value: namer.nakshatra(moon.nakshatra),
        sub: `${t('sv.star.sub', 'Nakṣatra')} · ${t('deck.pada', 'pada')} ${moon.nakshatra.pada}`,
      })
    }
  }
  return out
}

/** The landing page's headline and an example of what a chart shows. */
export function LandingHero({ namer, nakNames }) {
  const { t } = useLang()
  const example = [
    { label: t('sv.asc', 'Ascendant'), value: namer.rasiFull(4), sub: t('sv.asc.sub', 'Lagna') },
    { label: t('sv.moon', 'Moon sign'), value: namer.rasiFull(1), sub: t('sv.moon.sub', 'Janma rāśi') },
    { label: t('sv.star', 'Birth star'), value: namer.nakshatra(nakNames[3]), sub: t('sv.star.sub', 'Nakṣatra') },
  ]
  return (
    <div className="sv-hero">
      <h2>{t('sv.hero.title', 'Discover your Vedic birth chart')}</h2>
      <p>{t('sv.hero.sub', 'Enter your birth details to see your ascendant, Moon sign, birth star and planetary placements, explained in plain words.')}</p>
      <Tiles items={example} title={t('sv.hero.discover', 'What you will discover')} tag={t('sv.hero.example', 'Example')} />
    </div>
  )
}

const LEVEL = { MD: ['sv.run.md', 'Main period'], AD: ['sv.run.ad', 'Sub-period'], PD: ['sv.run.pd', 'Sub-sub-period'] }

/** Which daśā periods are current, and when each ends. Dates only — no verdict. */
export function RunningCard({ running, namer, onMore }) {
  const { t } = useLang()
  if (!running) return null
  return (
    <section className="dk-card sv-run">
      <h4 className="dk-head"><span>{t('sv.run.title', 'Your current Daśā timelines')}</span></h4>
      <div className="dk-body">
        <p className="sv-note">{t('sv.run.note', 'Vedic astrology divides a life into planetary periods (daśā). These are the ones running today.')}</p>
        {running.levels.map((l) => (
          <div className="sv-run-row" key={l.code}>
            <Bubble lord={l.lord} size="m" />
            <span className="sv-run-text">
              <span className="sv-run-level">{t(LEVEL[l.code][0], LEVEL[l.code][1])}</span>
              <b>{namer.grahaKey(l.lord)}</b>
            </span>
            <span className="sv-run-end">
              {t('sv.run.until', 'until')} {l.ends}
              <i>{l.remaining} {t('sv.run.left', 'left')}</i>
            </span>
            {l.next && (
              <span className="sv-run-next">
                {t('sv.run.next', 'Next')}: <b>{namer.grahaKey(l.next.lord)}</b> {t('sv.run.until', 'until')} {l.next.ends}
              </span>
            )}
          </div>
        ))}
        <button type="button" className="sv-link" onClick={onMore}>{t('sv.run.more', 'See the whole timeline →')}</button>
      </div>
    </section>
  )
}

/** The way into everything else. */
export function FullCta({ onFull }) {
  const { t } = useLang()
  return (
    <section className="sv-cta">
      <div>
        <h3>{t('sv.cta.title', 'There is much more in this chart')}</h3>
        <p>{t('sv.cta.body', 'Planetary positions and strengths, houses and yogas, the daśā timeline, the yearly chart, all sixteen divisional charts and the classical readings.')}</p>
      </div>
      <button type="button" className="go" onClick={onFull}>{t('sv.cta.go', 'Open the full analysis →')}</button>
    </section>
  )
}

/** Simple | Full analysis. */
export function ModeSwitch({ mode, setMode }) {
  const { t } = useLang()
  return (
    <span className="sv-mode" role="group" aria-label={t('sv.mode', 'How much to show')}>
      {[['simple', t('sv.mode.simple', 'Simple')], ['full', t('sv.mode.full', 'Full analysis')]].map(([k, label]) => (
        <button type="button" key={k} className={mode === k ? 'on' : ''} aria-pressed={mode === k} onClick={() => setMode(k)}>{label}</button>
      ))}
    </span>
  )
}

/** The plain-words story of a chart — the same one "Explain my chart" plays, built
 *  from the chart alone (walkthrough.js): the chart's facts and the method that
 *  reads them, never a rule's verdict. Null without a chart. */
export function useStory(chart, namer) {
  return useMemo(() => {
    if (!chart) return null
    try {
      const { steps } = buildWalkthrough(chart, namer)
      return { basics: steps.find((s) => s.key === 'basics') || null,
               houses: Object.fromEntries(steps.filter((s) => /^house\d+$/.test(s.key)).map((s) => [Number(s.key.slice(5)), s])) }
    } catch { return null }
  }, [chart, namer.style])  // eslint-disable-line react-hooks/exhaustive-deps
}

/** The chart in a few plain sentences. */
export function ChartSummary({ story }) {
  const { t, lang } = useLang()
  const step = story && story.basics
  if (!step) return null
  const L = lang === 'hi' ? 'hi' : 'en'
  return (
    <section className="dk-card sv-sum">
      <h4 className="dk-head"><span>{t('sv.sum.title', 'Your personal chart summary')}</span></h4>
      <div className="dk-body">
        <ul className="sv-lines">
          {step.lines[L].map((ln, i) => <li key={i}>{ln}</li>)}
        </ul>
      </div>
    </section>
  )
}

/** The twelve houses, one at a time: what the house stands for, and what this
 *  chart has there. Picked here or by tapping the house on the chart. */
export function HouseExplorer({ story, house, setHouse, onFull }) {
  const { t, lang } = useLang()
  if (!story || !Object.keys(story.houses).length) return null
  const L = lang === 'hi' ? 'hi' : 'en'
  const step = story.houses[house] || story.houses[1]
  return (
    <section className="dk-card sv-houses">
      <h4 className="dk-head">
        <span>{t('sv.houses.title', 'Your twelve houses')}</span>
        <span className="dk-head-right">{t('sv.houses.hint', 'tap a house here or on the chart')}</span>
      </h4>
      <div className="dk-body">
        <div className="sv-house-tabs" role="tablist">
          {Array.from({ length: 12 }, (_, i) => i + 1).map((h) => (
            <button type="button" key={h} role="tab" aria-selected={house === h}
                    className={house === h ? 'on' : ''} onClick={() => setHouse(h)}
                    title={HOUSE[h].title[L]}>
              <b>{h}</b><span>{HOUSE[h].title[L]}</span>
            </button>
          ))}
        </div>
        {step && (
          <div className="sv-house-body" role="tabpanel">
            <h5>{house}. {step.title[L]}</h5>
            <p className="sv-house-chips">
              {step.chips[L].map((c, i) => <span key={i}><b>{c.label}</b> {c.text}</span>)}
            </p>
            <ul className="sv-lines">
              {step.lines[L].map((ln, i) => <li key={i}>{ln}</li>)}
            </ul>
            <button type="button" className="sv-link" onClick={onFull}>{t('sv.houses.more', 'The classical reading for each house →')}</button>
          </div>
        )}
      </div>
    </section>
  )
}
