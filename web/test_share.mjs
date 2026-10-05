/**
 * Sharing a chart WITHOUT its birth details: what the link carries, and that
 * the date, the time and the place are provably not in it.
 *
 * Run:  node test_share.mjs
 * With the local API up (api/app.py on :5174) it also checks a real chart —
 * the reference one — end to end; without it that part is skipped, and says so.
 */
import { snapshotOf, snapshotPayload, detailsPayload, birthTraces, checkPayload, seal, unseal, b64u, unb64u, SNAPSHOT_KEYS } from './src/shareCodec.js'

let failed = 0
const ok = (name, cond, detail = '') => { console.log(`  ${cond ? 'OK ' : 'XX '}${name} ${detail}`); if (!cond) failed += 1 }

// A chart in the API's shape, with a birth detail planted at every depth a careless change could put one.
const BIRTH = { date: '1975-06-25', time: '22:30', place: 'Kanpur', lat: 26.4609, lon: 80.3218, tz: 'Asia/Kolkata', jd: 2442589.2083333335 }
const chart = {
  name: 'Reference', zodiac: 'Sidereal', ayanamsa: 'Lahiri (Chitrapakṣa)', ayanamsa_value: 23.518865693394027, bhava_system: 'Whole sign',
  jd_ut: BIRTH.jd, local_time: `${BIRTH.date} ${BIRTH.time}:00`, utc: '1975-06-25 17:00:00 UTC', utc_offset_hours: 5.5,
  timezone: BIRTH.tz, latitude: BIRTH.lat, longitude: BIRTH.lon,
  lagna_rasi: 10, lagna_longitude: 307.3197906538448, lagna_nakshatra: { index: 22, pada: 4 }, lagna_vargas: { D1: 10, D9: 3 },
  grahas: [
    { key: 'sun', rasi: 2, longitude: 70.05, latitude: 0.0001, nakshatra: { index: 6, fraction: 0.25 } },
    { key: 'moon', rasi: 8, longitude: 251.7, latitude: -4.9, nakshatra: { index: 18, fraction: 0.88 } },
  ],
  landmarks: [{ rasi: 0 }], gandanta: null, warnings: [],
  navamsa: { vargottama: ['sun'] },
  motion: { grahas: [{ key: 'sun', speed: 0.954 }] },
  shadbala: { grahas: { sun: { total: 412.5 } }, sunrise: '05:18', sunset: '18:59', birth: { weekday: 'Wednesday' } },
  analysis: {
    grahas: { sun: { dignity: 'neutral' } },
    classical: { readings: [{ sources: [{ source: { title: 'Phaladīpikā', date: 'c. 14th century' } }] }] },
    // things that must not survive, wherever they are put
    timezone: BIRTH.tz, deep: { jd_ut: BIRTH.jd, born: `${BIRTH.date}T${BIRTH.time}`, clock: BIRTH.time, zone: 'Asia/Kolkata' },
  },
  dasha: { default_year_days: 360, variants: { 360: { timezone: BIRTH.tz, mahadashas: [{ lord: 'saturn', start: '1972-05-28 20:25', end: '1978-04-27 20:25', is_current: false }] } } },
  some_future_field: { born_at: BIRTH.place },
}

console.log('\nwhat a details-free share carries')
const snap = snapshotOf(chart)
const text = JSON.stringify(snap)
ok('the date is not in it', !text.includes(BIRTH.date) && !text.includes('1975'))
ok('the clock time is not in it', !text.includes(BIRTH.time) && !text.includes('17:00'))
ok('the place, its coordinates and its time zone are not in it', !text.includes(BIRTH.place) && !text.includes('26.4609') && !text.includes('80.3218') && !text.includes('Kolkata'))
ok('the Julian day and the offset are not in it', !text.includes('2442589') && !('utc_offset_hours' in snap) && !('jd_ut' in snap))
ok('the ayanāṁśa is named, but not given to eight places (that would date the chart)', snap.ayanamsa === chart.ayanamsa && !('ayanamsa_value' in snap) && !text.includes('23.5188'))
ok('no dated period is in it — the daśā is left out whole', !('dasha' in snap) && !text.includes('1972-05-28') && !text.includes('mahadashas'))
ok('sunrise and sunset are stripped wherever they sit', !text.includes('05:18') && !text.includes('18:59') && !('sunrise' in snap.shadbala) && !('birth' in snap.shadbala))
ok('a birth detail planted deep under another name is blanked', snap.analysis.deep.born === null && snap.analysis.deep.clock === null && snap.analysis.deep.zone === null && !('jd_ut' in snap.analysis.deep) && !('timezone' in snap.analysis))
ok('a field the list does not know is left out, not let through', !('some_future_field' in snap) && Object.keys(snap).every((k) => k === 'snapshot' || SNAPSHOT_KEYS.includes(k)))
ok('nothing in it still reads like a date, a time, a zone or a Julian day', birthTraces(snap).length === 0, birthTraces(snap).join('; '))
ok('…and that check does see them in the chart it was made from', birthTraces(chart).length >= 8)

console.log('\nwhat it must keep')
ok('every graha keeps its longitude and latitude (the sky’s, not the birthplace’s)', snap.grahas[0].longitude === 70.05 && snap.grahas[1].latitude === -4.9 && snap.grahas.length === 2)
ok('the lagna, its degree, its nakṣatra and every varga', snap.lagna_rasi === 10 && snap.lagna_longitude === chart.lagna_longitude && snap.lagna_vargas.D9 === 3 && snap.lagna_nakshatra.pada === 4)
ok('strengths, motion, navāṁśa and the readings', snap.shadbala.grahas.sun.total === 412.5 && snap.motion.grahas[0].speed === 0.954 && snap.navamsa.vargottama[0] === 'sun' && snap.analysis.grahas.sun.dignity === 'neutral')
ok('a cited text keeps its date', snap.analysis.classical.readings[0].sources[0].source.date === 'c. 14th century')
ok('the chart it was made from is not altered', chart.jd_ut === BIRTH.jd && chart.analysis.deep.born.startsWith('1975') && !!chart.dasha)

console.log('\nthe link')
{
  const p = snapshotPayload({ name: 'Reference', lang: 'hi', chart })
  ok('the payload says what it is, and has no birth fields of its own', p.kind === 'snapshot' && p.v === 2 && !('date' in p) && !('time' in p) && !('place' in p))
  const a = await seal(p), b = await seal(p)
  ok('sealed, it is two base64url parts the Worker accepts', /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(a.blob))
  ok('the same chart sealed twice gives two unrelated links', a.blob !== b.blob && a.key !== b.key)
  ok('nothing of the chart can be read in the blob', !a.blob.includes('Reference') && !unb64u(a.blob.split('.')[1]).some((_, i, u) => u[i] === 0x67 && u[i + 1] === 0x72 && u[i + 2] === 0x61 && u[i + 3] === 0x68 && u[i + 4] === 0x61 && u[i + 5] === 0x73))
  const back = await unseal(a.blob, a.key)
  ok('with its key it opens to exactly what was sealed', JSON.stringify(back) === JSON.stringify(p) && checkPayload(back) === 'snapshot')
  let threw = false
  try { await unseal(a.blob, b.key) } catch { threw = true }
  ok('with any other key it does not open', threw)
  const d = await seal(detailsPayload({ name: 'R', date: BIRTH.date, time: BIRTH.time, place: { name: 'Kanpur, India', latitude: BIRTH.lat, longitude: BIRTH.lon, timezone: BIRTH.tz } }))
  const dBack = await unseal(d.blob, d.key)
  ok('a share WITH the details still round-trips, as before', dBack.date === BIRTH.date && dBack.place.timezone === BIRTH.tz && checkPayload(dBack) === 'details')
  let bad = false
  try { checkPayload({ kind: 'snapshot', chart: { grahas: 'x' } }) } catch { bad = true }
  ok('a payload that is neither is refused', bad)
  const big = new Uint8Array(300000).map((_, i) => i % 251)
  ok('base64url copes with a chart-sized buffer', unb64u(b64u(big)).every((x, i) => x === big[i]))
}

console.log('\na real chart (the reference one, from the local API)')
try {
  const r = await fetch('http://127.0.0.1:5174/api/chart', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: 'Reference', date: BIRTH.date, time: BIRTH.time, lang: 'en', latitude: BIRTH.lat, longitude: BIRTH.lon, timezone: BIRTH.tz }),
  })
  const real = await r.json()
  const s = snapshotOf(real)
  const t = JSON.stringify(s)
  ok('no trace of a date, a time, a zone or a Julian day', birthTraces(s).length === 0, birthTraces(s).slice(0, 3).join('; '))
  ok('none of the inputs appears anywhere in it', ![BIRTH.date, '22:30', 'Kolkata', '26.4609', '80.3218', '2442589', '17:00:00'].some((x) => t.includes(x)))
  ok('all nine grahas, with their degrees', s.grahas.length === 9 && s.grahas.every((g) => typeof g.longitude === 'number'))
  ok('the readings and strengths came through', !!s.analysis && !!s.analysis.yogas && !!s.shadbala && !!s.navamsa)
  const sealed = await seal(snapshotPayload({ name: 'Reference', lang: 'en', chart: real }))
  ok('sealed, it fits well inside the Worker’s limit', sealed.blob.length < 256 * 1024, `${Math.round(sealed.blob.length / 1024)} KB of ${256} KB (the chart itself is ${Math.round(JSON.stringify(real).length / 1024)} KB)`)
} catch (e) {
  console.log(`  --  skipped: the local API is not running (${e.cause?.code || e.message})`)
}

console.log(failed ? `\n${failed} FAILED ✗` : '\nALL PASS ✓')
process.exit(failed ? 1 : 0)
