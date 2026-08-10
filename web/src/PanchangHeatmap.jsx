/**
 * Panchāṅga heatmap — a month calendar of chart-tailored auspiciousness for the
 * loaded birth chart. Each day is tinted red→yellow→green on a 0–100 score
 * (tārā-bala + candra-bala + Moon-transit + day-quality, from /api/panchang/
 * calendar); the score is printed on every cell so the encoding is never
 * colour-alone (red↔green is the classic CVD trap). Tapping a day opens its full
 * pañcāṅga + the cited score components + the day's muhūrta windows.
 *
 * Diverging status stops are the validated dataviz palette (good #0ca30c,
 * warning #fab219, critical #d03b3b).
 */
import { useState, useEffect } from 'react'
import { API } from './config.js'
import { useLang } from './LangContext.jsx'

const MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
  'August', 'September', 'October', 'November', 'December']
const WD = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']

// red (0) → yellow (50) → green (100), from the validated status stops.
const STOPS = [[0xd0, 0x3b, 0x3b], [0xfa, 0xb2, 0x19], [0x0c, 0xa3, 0x0c]]
function scoreColor(score) {
  const s = Math.max(0, Math.min(100, score)) / 100
  const seg = s < 0.5 ? 0 : 1
  const t = s < 0.5 ? s / 0.5 : (s - 0.5) / 0.5
  const [a, b] = [STOPS[seg], STOPS[seg + 1]]
  const c = a.map((v, i) => Math.round(v + (b[i] - v) * t))
  return `rgb(${c[0]},${c[1]},${c[2]})`
}

function Row({ label, value, source }) {
  if (value == null || value === '') return null
  return (
    <div className="pc-row">
      <span className="pc-k">{label}</span>
      <span className="pc-v">{value}{source && <em className="pc-src"> — {source}</em>}</span>
    </div>
  )
}

function DayDetail({ day, t, lang }) {
  const d = day.detail
  const H = (en, hi) => (lang === 'hi' && hi) ? hi : en
  const verdict = (x) => t(`panchang.verdict.${x}`, x)
  const win = day.windows || {}
  const w = (x) => (x ? `${x.start}–${x.end}` : '—')
  return (
    <div className="pc-detail">
      <div className="pc-detail-head">
        <strong>{day.date}</strong>
        <span className="pc-band" style={{ background: scoreColor(day.score) }}>{day.score}</span>
        <span>{t(`panchang.band.${d.band}`, d.band)}</span>
      </div>
      <div className="pc-detail-grid">
        <div>
          <h5>{t('panchang.limbs', 'Pañcāṅga')}</h5>
          <Row label={t('panchang.tithi', 'Tithi')} value={`${H(day.tithi, day.tithi_hi)} (${t('panchang.' + day.paksha, day.paksha)})`} />
          <Row label={t('panchang.vara', 'Vāra')} value={H(day.vara, day.vara_hi)} />
          <Row label={t('panchang.nakshatra', 'Nakṣatra')} value={H(day.nakshatra, day.nakshatra_hi)} />
          <Row label={t('panchang.yoga', 'Yoga')} value={H(day.yoga, day.yoga_hi)} />
        </div>
        <div>
          <h5>{t('panchang.foryou', 'For this chart')}</h5>
          <Row label={t('panchang.tarabala', 'Tārā-bala')} value={`${H(d.tarabala.tara, d.tarabala.tara_hi)} · ${verdict(d.tarabala.verdict)}`} source={H(d.tarabala.source, d.tarabala.source_hi)} />
          <Row label={t('panchang.candrabala', 'Candra-bala')} value={`${t('panchang.house', 'house')} ${d.candrabala.house_from_moon} · ${verdict(d.candrabala.verdict)}`} source={H(d.candrabala.source, d.candrabala.source_hi)} />
          <Row label={t('panchang.transit', 'Moon transit')} value={`${t('panchang.bhava', 'bhāva')} ${d.moon_transit.bhava_from_lagna} · ${verdict(d.moon_transit.verdict)}`} source={H(d.moon_transit.source, d.moon_transit.source_hi)} />
          <Row label={t('panchang.dayquality', 'Day quality')} value={((lang === 'hi' && d.day_quality.flags_hi) || d.day_quality.flags).length ? ((lang === 'hi' && d.day_quality.flags_hi) || d.day_quality.flags).join(', ') : verdict('clean')} source={H(d.day_quality.source, d.day_quality.source_hi)} />
        </div>
        <div>
          <h5>{t('panchang.windows', 'Windows')}</h5>
          <Row label={t('panchang.sunrise', 'Sunrise · sunset')} value={win.day_span ? `${win.day_span.sunrise} · ${win.day_span.sunset}` : '—'} />
          <Row label={t('panchang.rahu', 'Rāhu-kāla')} value={w(win.rahu_kala)} />
          <Row label={t('panchang.yama', 'Yama-gaṇḍa')} value={w(win.yama_ganda)} />
          <Row label={t('panchang.gulika', 'Gulika')} value={w(win.gulika_kala)} />
          <Row label={t('panchang.abhijit', 'Abhijit')} value={w(win.abhijit)} />
          <Row label={t('panchang.brahma', 'Brahma-muhūrta')} value={w(win.brahma_muhurta)} />
        </div>
      </div>
      <p className="pc-note">{t('panchang.discl', 'Auspiciousness of the day for this chart — a muhūrta guide from classical measures, not a fated verdict. Rāhu-kāla / Yama-gaṇḍa / Gulika are inauspicious; Abhijit / Brahma-muhūrta are auspicious.')}</p>
    </div>
  )
}

export default function PanchangHeatmap({ date, time, place }) {
  const { t, lang } = useLang()
  const today = new Date()
  const [ym, setYm] = useState({ y: today.getFullYear(), m: today.getMonth() + 1 })
  const [data, setData] = useState(null)
  const [busy, setBusy] = useState(false)
  const [err, setErr] = useState('')
  const [sel, setSel] = useState(null)

  useEffect(() => {
    if (!date || !time || !place) return
    let alive = true
    setBusy(true); setErr(''); setSel(null)
    fetch(`${API}/api/panchang/calendar`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        date, time, latitude: place.latitude, longitude: place.longitude,
        timezone: place.timezone, year: ym.y, month: ym.m,
      }),
    })
      .then((r) => r.json())
      .then((j) => { if (!alive) return; if (j.error) setErr(j.error); else { setData(j); setSel((j.days || [])[0] || null) } })
      .catch((e) => alive && setErr(String(e)))
      .finally(() => alive && setBusy(false))
    return () => { alive = false }
  }, [date, time, place, ym])

  if (!date || !time || !place) return null
  const byDate = {}
  ;(data?.days || []).forEach((d) => { byDate[d.date] = d })
  const first = new Date(ym.y, ym.m - 1, 1)
  const lead = first.getDay()
  const nDays = new Date(ym.y, ym.m, 0).getDate()
  const cells = []
  for (let i = 0; i < lead; i++) cells.push(null)
  for (let d = 1; d <= nDays; d++) {
    const iso = `${ym.y}-${String(ym.m).padStart(2, '0')}-${String(d).padStart(2, '0')}`
    cells.push(byDate[iso] || { date: iso, empty: true })
  }
  const shift = (delta) => setYm(({ y, m }) => {
    const nm = m + delta
    return nm < 1 ? { y: y - 1, m: 12 } : nm > 12 ? { y: y + 1, m: 1 } : { y, m: nm }
  })

  return (
    <section className="table-panel panchang-panel" id="rg-panchang">
      <h3>{t('panchang.title', 'Pañcāṅga — auspicious days')}</h3>
      <div className="pc-head">
        <button className="pc-nav" onClick={() => shift(-1)} aria-label="previous month">‹</button>
        <strong>{t(`month.${ym.m}`, MONTHS[ym.m - 1])} {ym.y}</strong>
        <button className="pc-nav" onClick={() => shift(1)} aria-label="next month">›</button>
        <span className="pc-legend" aria-hidden="true">
          <i style={{ background: scoreColor(15) }} />{t('panchang.band.inauspicious', 'inauspicious')}
          <i style={{ background: scoreColor(50) }} />{t('panchang.band.mixed', 'mixed')}
          <i style={{ background: scoreColor(90) }} />{t('panchang.band.auspicious', 'auspicious')}
        </span>
      </div>
      {data?.birth && (
        <p className="rc-note">{t('panchang.birthline', 'Scored for your chart — birth Moon in')} {data.birth.moon_nakshatra}.</p>
      )}
      {busy && <p className="rc-note">{t('panchang.loading', 'Computing the month…')}</p>}
      {err && <p className="rc-note pc-err">{err}</p>}
      <div className="pc-cal" role="grid">
        {WD.map((w) => <div key={w} className="pc-wd">{t(`wd.${w}`, w)}</div>)}
        {cells.map((c, i) => c == null ? <div key={i} className="pc-cell pc-blank" />
          : c.empty ? <div key={i} className="pc-cell pc-na" title="—">{+c.date.slice(-2)}</div>
          : (
            <button key={i}
              className={`pc-cell${sel && sel.date === c.date ? ' pc-sel' : ''}`}
              style={{ background: scoreColor(c.score) }}
              onClick={() => setSel(c)}
              title={`${c.date}: ${c.score} (${t(`panchang.band.${c.band}`, c.band)}) · ${(lang === 'hi' && c.nakshatra_hi) ? c.nakshatra_hi : c.nakshatra}`}>
              <span className="pc-d">{+c.date.slice(-2)}</span>
              <span className="pc-s">{c.score}</span>
            </button>
          ))}
      </div>
      {sel && !sel.empty && <DayDetail day={sel} t={t} lang={lang} />}
    </section>
  )
}
