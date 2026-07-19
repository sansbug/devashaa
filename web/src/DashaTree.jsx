/**
 * Viṁśottarī daśā — collapsible Mahā → Antar → Pratyantar tree.
 *
 * The period running *now* is flagged is_current by the API at every level, so
 * each node defaults open when it is current: the tree auto-drills to today's
 * running Mahā › Antar › Pratyantar on first render.
 */
import { useState, useEffect } from 'react'
import DashaTimeline from './DashaTimeline.jsx'
import { API } from './config.js'

function fmtYears(y, yearDays) {
  const monthDays = yearDays / 12
  const totalDays = y * yearDays
  const yy = Math.floor(totalDays / yearDays)
  const rem = totalDays - yy * yearDays
  const mm = Math.floor(rem / monthDays)
  const dd = Math.round(rem - mm * monthDays)
  return [yy && `${yy}y`, mm && `${mm}m`, dd && `${dd}d`].filter(Boolean).join(' ') || '0d'
}

function DashaNode({ node, nameOf, yearDays }) {
  const [open, setOpen] = useState(node.is_current)
  const hasSub = node.sub && node.sub.length > 0
  const label = nameOf(node.lord) || node.lord_name

  return (
    <div className={`d-node lvl-${node.level}${node.is_current ? ' current' : ''}`}>
      <button
        type="button"
        className="d-row"
        onClick={() => hasSub && setOpen((o) => !o)}
        aria-expanded={hasSub ? open : undefined}
      >
        <span className="d-toggle">{hasSub ? (open ? '▾' : '▸') : '·'}</span>
        <span className="d-lord">{label}</span>
        <span className="d-dates">{node.start} → {node.end}</span>
        <span className="d-dur">{fmtYears(node.years, yearDays)}</span>
        {node.is_current && <span className="d-now">now</span>}
      </button>
      {open && hasSub && (
        <div className="d-children">
          {node.sub.map((s, i) => (
            <DashaNode key={i} node={s} nameOf={nameOf} yearDays={yearDays} />
          ))}
        </div>
      )}
    </div>
  )
}

/**
 * The four states of BPHS Vol II ch.47 vv.5-6. Not a scale — the verse names
 * two branches and nothing in between, so `not stated` is the honest result for
 * any placement it does not name, and it is usually the commonest outcome.
 */
function DashaLegend() {
  return (
    <p className="dt-legend">
      <span className="dt-key"><span className="dt-swatch v-favourable" /> favourable</span>
      <span className="dt-key"><span className="dt-swatch v-adverse" /> adverse</span>
      <span className="dt-key"><span className="dt-swatch v-contested" /> both stated</span>
      <span className="dt-key"><span className="dt-swatch v-not_stated" /> no stated verdict</span>
      <br />
      Bars apply <strong>BPHS Vol II ch.47 vv.5-6</strong>, which names a daśā
      favourable if its lord stands in the Ascendant, in exaltation, in its own
      sign or a friend’s, and unfavourable in the 6th, 8th or 12th, in
      debilitation or an enemy’s sign. It is <em>not</em> a heatmap: the verse
      gives two branches and no scale, no middle band and no rule for when both
      fire — so “both stated” is left unarbitrated and “no stated verdict” means
      the text is silent, which is not the same as neutral. The verdict is read
      from the lord’s natal placement and applies to every band that lord rules.
      Pratyantar bars repeat the mahā lord’s verdict only where that lord is the
      period lord; ch.61’s pratyantar prose is not used.
    </p>
  )
}

export default function DashaTree({
  dasha, chartMeta, nameOf = () => null, verdicts, positions, lagna,
}) {
  const [systemKey, setSystemKey] = useState('vimshottari')
  // ch.52-60's conditions for whichever mahādaśā the timeline is showing.
  // Fetched per mahādaśā rather than with the chart: the whole 81-cell matrix
  // with its quoted ślokas is ~650 KB, one mahādaśā's slice is a fraction.
  const [antarMaha, setAntarMaha] = useState(null)
  const [antarCells, setAntarCells] = useState(null)
  const [data, setData] = useState(dasha)   // {default_year_days, variants}
  const [variant, setVariant] = useState('360')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (!antarMaha || !positions || lagna === undefined || lagna === null) return
    let cancelled = false
    fetch(`${API}/api/antardasa`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ maha_lord: antarMaha, positions, lagna }),
    })
      .then((r) => r.json())
      .then((j) => { if (!cancelled) setAntarCells(j.error ? null : j.cells) })
      .catch(() => { if (!cancelled) setAntarCells(null) })
    return () => { cancelled = true }
  }, [antarMaha, positions, lagna])

  // A fresh chart resets to the (precomputed) Viṁśottarī that came with it.
  useEffect(() => {
    setSystemKey('vimshottari')
    setData(dasha)
    if (dasha && !dasha.error) setVariant(String(dasha.default_year_days).replace('.0', ''))
  }, [dasha])

  // Non-default systems are fetched on demand from the Moon-nakṣatra data the
  // chart already carries — no full recompute.
  useEffect(() => {
    if (systemKey === 'vimshottari') { setData(dasha); return }
    let cancelled = false
    setLoading(true)
    fetch(`${API}/api/dasha`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ system: systemKey, ...chartMeta }),
    })
      .then((r) => r.json())
      .then((d) => { if (!cancelled) setData(d) })
      .catch(() => { if (!cancelled) setData({ error: 'Daśā fetch failed' }) })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [systemKey, dasha, chartMeta])

  if (!dasha) return null
  if (dasha.error) return <div className="error">{dasha.error}</div>

  const systems = dasha.available_systems || []
  if (data.error) return <div className="error">{data.error}</div>
  const tree = data.variants[variant] || Object.values(data.variants)[0]

  // Walk the is_current chain for the summary line.
  const chain = []
  let list = tree.mahadashas
  while (list) {
    const cur = list.find((n) => n.is_current)
    if (!cur) break
    chain.push(cur)
    list = cur.sub
  }

  return (
    <div className="dasha">
      <div className="dasha-controls">
        <span className="d-label">System</span>
        <select
          className="dasha-select"
          value={systemKey}
          onChange={(e) => setSystemKey(e.target.value)}
        >
          {systems.map((s) => (
            <option key={s.key} value={s.key} title={s.applicability}>
              {s.name} · {s.total_years}y
            </option>
          ))}
        </select>
        {loading && <span className="d-loading">loading…</span>}

        <span className="d-label" style={{ marginLeft: 'auto' }}>Year</span>
        <button
          type="button"
          className={variant === '360' ? 'on' : ''}
          onClick={() => setVariant('360')}
          title="360-day sāvana year — matches BPHS Ch.46's worked example"
        >
          360 · BPHS
        </button>
        <button
          type="button"
          className={variant === '365.25' ? 'on' : ''}
          onClick={() => setVariant('365.25')}
          title="365.25-day Julian year — matches Jagannātha Hora & most modern software"
        >
          365.25 · modern
        </button>
      </div>

      <div className="dasha-head">
        <div>
          <span className="d-label">System</span>
          {tree.system} · {tree.total_years}-year cycle
        </div>
        <div>
          <span className="d-label">Balance at birth</span>
          {nameOf(tree.starting_lord) || tree.starting_lord_name} — {tree.balance_at_birth}
        </div>
        <div className="running">
          <span className="d-label">Running now</span>
          {chain.length
            ? chain.map((c, i) => (
                <span key={i}>
                  {i > 0 && <span className="sep"> › </span>}
                  {nameOf(c.lord) || c.lord_name}
                </span>
              ))
            : '—'}
        </div>
      </div>
      {tree.applicability && (
        <p className="dasha-applies">
          <strong>When applied:</strong> {tree.applicability}
        </p>
      )}
      <DashaTimeline
        dasha={tree}
        namer={{ grahaKey: (k) => nameOf(k) || k }}
        verdictOf={verdicts ? (lord) => verdicts[lord] : undefined}
        conditionsOf={antarCells ? (lord) => antarCells[lord] : undefined}
        onMahaChange={setAntarMaha}
        legend={verdicts ? <DashaLegend /> : null}
      />

      <div className="dasha-tree">
        {tree.mahadashas.map((m, i) => (
          <DashaNode key={i} node={m} nameOf={nameOf} yearDays={tree.year_days} />
        ))}
      </div>
      <p className="dasha-note">
        Dates in birth-place local time ({tree.timezone}). {tree.system} per{' '}
        {tree.citation}; {tree.year_system} year for calendar projection.
      </p>
    </div>
  )
}
