/**
 * Panchāṅga heatmap — a month calendar of chart-tailored auspiciousness for the
 * loaded birth chart. Each day is tinted red→yellow→green on a 0–100 score
 * (tārā-bala + candra-bala + Moon-transit + daśā-fit + day-quality, from
 * /api/panchang/calendar); the score is printed on every cell so the encoding is
 * never colour-alone (red↔green is the classic CVD trap), and each component
 * shows its own weight so the tint is transparent. Tapping a day opens its full
 * pañcāṅga + the cited score components + the day's muhūrta windows.
 *
 * Festival/observance days carry a corner dot (major/notable/observance); the
 * "Special days this month" list answers "when is Diwali / Ekādaśī / Amāvāsyā".
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
  const win_ = (x) => (x ? `${x.start}–${x.end}` : '—')
  const wt = d.weights || {}
  // A component label that carries its own weight, so the scoring is transparent.
  const wl = (key, fallback, wkey) => wt[wkey] != null
    ? `${t(key, fallback)} · ${Math.round(wt[wkey] * 100)}%` : t(key, fallback)
  const df = d.dasha_fit
  const fests = day.festivals || []
  // "YYYY-MM-DD HH:MM" → "HH:MM" (or "HH:MM (DD)" if it ends the next day).
  const endTime = (s) => {
    if (!s) return null
    const [d0, hm] = s.split(' ')
    return d0 === day.date ? hm : `${hm} (${d0.slice(-2)})`
  }
  return (
    <div className="pc-detail">
      <div className="pc-detail-head">
        <strong>{day.date}</strong>
        <span className="pc-band" style={{ background: scoreColor(day.score) }}>{day.score}</span>
        <span>{t(`panchang.band.${d.band}`, d.band)}</span>
      </div>
      {fests.length > 0 && (
        <div className="pc-fest-day">
          {fests.map((f) => (
            <span key={f.key} className={`pc-fest-tag imp-${f.importance}`}
                  title={H(f.significance, f.significance_hi)}>{H(f.name, f.name_hi)}</span>
          ))}
        </div>
      )}
      <div className="pc-detail-grid">
        <div>
          <h5>{t('panchang.limbs', 'Pañcāṅga')}</h5>
          <Row label={t('panchang.tithi', 'Tithi')} value={`${H(day.tithi, day.tithi_hi)} (${t('panchang.' + day.paksha, day.paksha)})${day.tithi_end ? ` · → ${endTime(day.tithi_end)}` : ''}`} />
          <Row label={t('panchang.masa', 'Lunar month')} value={day.masa ? H(day.masa, day.masa_hi) : null} />
          <Row label={t('panchang.vara', 'Vāra')} value={H(day.vara, day.vara_hi)} />
          <Row label={t('panchang.nakshatra', 'Nakṣatra')} value={H(day.nakshatra, day.nakshatra_hi)} />
          <Row label={t('panchang.yoga', 'Yoga')} value={H(day.yoga, day.yoga_hi)} />
        </div>
        <div>
          <h5>{t('panchang.foryou', 'For this chart')}</h5>
          <Row label={wl('panchang.tarabala', 'Tārā-bala', 'tarabala')} value={`${H(d.tarabala.tara, d.tarabala.tara_hi)} · ${verdict(d.tarabala.verdict)}`} source={H(d.tarabala.source, d.tarabala.source_hi)} />
          <Row label={wl('panchang.candrabala', 'Candra-bala', 'candrabala')} value={`${t('panchang.house', 'house')} ${d.candrabala.house_from_moon} · ${verdict(d.candrabala.verdict)}`} source={H(d.candrabala.source, d.candrabala.source_hi)} />
          <Row label={wl('panchang.transit', 'Moon transit', 'moon_transit')} value={`${t('panchang.bhava', 'bhāva')} ${d.moon_transit.bhava_from_lagna} · ${verdict(d.moon_transit.verdict)}`} source={H(d.moon_transit.source, d.moon_transit.source_hi)} />
          {df && (
            <Row label={wl('panchang.dasha', 'Daśā fit', 'dasha')}
                 value={`${H(df.maha_name, df.maha_name_hi)}${df.antar ? ' / ' + H(df.antar_name, df.antar_name_hi) : ''} → ${H(df.vara_lord_name, df.vara_lord_name_hi)} · ${verdict(df.verdict)}`}
                 source={H(df.source, df.source_hi)} />
          )}
          <Row label={wl('panchang.dayquality', 'Day quality', 'day_quality')} value={((lang === 'hi' && d.day_quality.flags_hi) || d.day_quality.flags).length ? ((lang === 'hi' && d.day_quality.flags_hi) || d.day_quality.flags).join(', ') : verdict('clean')} source={H(d.day_quality.source, d.day_quality.source_hi)} />
        </div>
        <div>
          <h5>{t('panchang.windows', 'Windows')}</h5>
          <Row label={t('panchang.sunrise', 'Sunrise · sunset')} value={win.day_span ? `${win.day_span.sunrise} · ${win.day_span.sunset}` : '—'} />
          <Row label={t('panchang.rahu', 'Rāhu-kāla')} value={win_(win.rahu_kala)} />
          <Row label={t('panchang.yama', 'Yama-gaṇḍa')} value={win_(win.yama_ganda)} />
          <Row label={t('panchang.gulika', 'Gulika')} value={win_(win.gulika_kala)} />
          <Row label={t('panchang.abhijit', 'Abhijit')} value={win_(win.abhijit)} />
          <Row label={t('panchang.brahma', 'Brahma-muhūrta')} value={win_(win.brahma_muhurta)} />
        </div>
      </div>
      <p className="pc-note">{t('panchang.discl', 'Auspiciousness of the day for this chart — a muhūrta guide from classical measures, not a fated verdict. Rāhu-kāla / Yama-gaṇḍa / Gulika are inauspicious; Abhijit / Brahma-muhūrta are auspicious.')}</p>
    </div>
  )
}

// A scannable "special days this month" list — the answer to "when is Diwali /
// Ekādaśī / Amāvāsyā this month". Majors first within each day.
function MonthFestivals({ days, t, lang }) {
  const H = (en, hi) => (lang === 'hi' && hi) ? hi : en
  const rows = (days || []).filter((dy) => (dy.festivals || []).length)
  if (!rows.length) return null
  return (
    <details className="pc-festlist" open>
      <summary>{t('panchang.monthFestivals', 'Special days this month')}</summary>
      <ul>
        {rows.map((dy) => (
          <li key={dy.date}>
            <span className="pc-fl-date">{dy.date.slice(-2)}</span>
            <span className="pc-fl-names">
              {(dy.festivals).map((f) => (
                <span key={f.key} className={`pc-fest-tag imp-${f.importance}`}
                      title={H(f.significance, f.significance_hi)}>{H(f.name, f.name_hi)}</span>
              ))}
            </span>
          </li>
        ))}
      </ul>
    </details>
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
      .then((j) => {
        if (!alive) return
        if (j.error) { setErr(j.error); return }
        setData(j)
        // Open on today when the shown month is the current one; else the 1st.
        const now = new Date()
        const todayIso = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`
        const days = j.days || []
        setSel(days.find((d) => d.date === todayIso) || days[0] || null)
      })
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
      <div className="pc-calwrap">
      <div className="pc-cal" role="grid">
        {WD.map((w) => <div key={w} className="pc-wd">{t(`wd.${w}`, w)}</div>)}
        {cells.map((c, i) => c == null ? <div key={i} className="pc-cell pc-blank" />
          : c.empty ? <div key={i} className="pc-cell pc-na" title="—">{+c.date.slice(-2)}</div>
          : (() => {
            const fs = c.festivals || []
            const imp = fs.some((f) => f.importance === 'major') ? 'major'
              : fs.some((f) => f.importance === 'notable') ? 'notable'
              : fs.length ? 'observance' : null
            const names = fs.map((f) => (lang === 'hi' && f.name_hi) ? f.name_hi : f.name).join(', ')
            return (
              <button key={i}
                className={`pc-cell${sel && sel.date === c.date ? ' pc-sel' : ''}`}
                style={{ background: scoreColor(c.score) }}
                onClick={() => setSel(c)}
                title={`${c.date}: ${c.score} (${t(`panchang.band.${c.band}`, c.band)}) · ${(lang === 'hi' && c.nakshatra_hi) ? c.nakshatra_hi : c.nakshatra}${names ? ' · ' + names : ''}`}>
                <span className="pc-d">{+c.date.slice(-2)}</span>
                <span className="pc-s">{c.score}</span>
                {imp && <span className={`pc-fest-dot imp-${imp}`} aria-hidden="true" />}
              </button>
            )
          })())}
      </div>
      <MonthFestivals days={data?.days} t={t} lang={lang} />
      </div>
      {sel && !sel.empty && <DayDetail day={sel} t={t} lang={lang} />}
    </section>
  )
}
