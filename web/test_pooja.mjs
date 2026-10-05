/**
 * Pūjā — the pieces that can be pinned without a browser or a deployed Worker:
 * the relay credentials (with Cloudflare's API stubbed), the clean-up of a
 * pandit's recording, and the naming of the voice library's clips.
 *
 * Run:  node test_pooja.mjs
 */
import fs from 'node:fs'
import vm from 'node:vm'
import { mintIce } from './pooja-worker.js'
import { trimSilence, encodeWav, peakOf, fadeEdges } from './src/pooja/chantAudio.js'
import { MANTRA_STEPS, ALL_STEPS, ABOUT, scriptFor, romanOf, mantraClip, explainClip, narration, textHash } from './src/pooja/guide.js'
import { CHAUPAIS } from './src/pooja/chalisa.js'
import { RITUALS } from './src/pooja/rituals.js'
import { deviceVoice, genderOf } from './src/pooja/voices.js'

let failed = 0
const ok = (name, cond, detail = '') => { console.log(`  ${cond ? 'OK ' : 'XX '}${name} ${detail}`); if (!cond) failed += 1 }

console.log('\nthe relay (TURN)')
{
  const none = await mintIce({}, () => { throw new Error('must not be called') })
  ok('no key → STUN only, and Cloudflare is not called', none.turn === false && none.iceServers.every((s) => s.urls.every((u) => u.startsWith('stun:'))))

  let seen = null
  const cf = {
    iceServers: [
      { urls: ['stun:stun.cloudflare.com:3478', 'stun:stun.cloudflare.com:53'] },
      { urls: ['turn:turn.cloudflare.com:3478?transport=udp', 'turn:turn.cloudflare.com:53?transport=udp', 'turn:turn.cloudflare.com:80?transport=tcp', 'turns:turn.cloudflare.com:443?transport=tcp'], username: 'u', credential: 'c' },
    ],
  }
  const good = await mintIce({ TURN_KEY_ID: 'kid', TURN_KEY_API_TOKEN: 'tok' }, async (url, init) => { seen = { url, init }; return { ok: true, status: 201, json: async () => cf } })
  ok('calls the key’s generate-ice-servers endpoint', seen.url === 'https://rtc.live.cloudflare.com/v1/turn/keys/kid/credentials/generate-ice-servers' && seen.init.method === 'POST')
  ok('…with the token as a bearer, never in the URL', seen.init.headers.Authorization === 'Bearer tok' && !seen.url.includes('tok'))
  ok('…asking for a credential that outlives a ceremony', JSON.parse(seen.init.body).ttl >= 6 * 3600, String(JSON.parse(seen.init.body).ttl))
  ok('turn: true, with the credential passed through', good.turn === true && good.iceServers[1].username === 'u' && good.iceServers[1].credential === 'c')
  const urls = good.iceServers.flatMap((s) => s.urls)
  ok('port 53 URLs are dropped (browsers block them)', !urls.some((u) => /:53(\?|$)/.test(u)) && urls.length === 4, urls.join(' '))
  ok('the key itself is not in what a browser receives', !JSON.stringify(good).includes('tok') && !JSON.stringify(good).includes('kid'))

  const refused = await mintIce({ TURN_KEY_ID: 'kid', TURN_KEY_API_TOKEN: 'bad' }, async () => ({ ok: false, status: 401, json: async () => ({}) }))
  ok('a refused key → STUN only, with the reason', refused.turn === false && /401/.test(refused.reason) && refused.iceServers.length > 0)
  const down = await mintIce({ TURN_KEY_ID: 'kid', TURN_KEY_API_TOKEN: 'tok' }, async () => { throw new Error('network') })
  ok('Cloudflare unreachable → STUN only, the room still opens', down.turn === false && down.iceServers.length > 0)
  const empty = await mintIce({ TURN_KEY_ID: 'kid', TURN_KEY_API_TOKEN: 'tok' }, async () => ({ ok: true, status: 201, json: async () => ({ iceServers: [{ urls: ['stun:x:3478'] }] }) }))
  ok('an answer with no TURN server is not called a relay', empty.turn === false)
}

console.log('\na pandit’s recording')
{
  const sr = 48000
  const x = new Float32Array(sr * 4)
  for (let i = 0; i < x.length; i++) x[i] = (Math.sin(i * 12.9898) * 43758.5453 % 1) * 0.0006     // a second of room noise each side
  for (let i = sr; i < sr * 3; i++) x[i] += 0.3 * Math.sin(2 * Math.PI * 180 * i / sr)             // two seconds of voice
  const cut = trimSilence(x, sr)
  const secs = cut.length / sr
  ok('silence is trimmed, a quarter-second kept each side', secs > 2.4 && secs < 2.65, `${secs.toFixed(2)} s from 4.00 s`)
  ok('nothing of the voice is cut', cut.byteOffset / 4 <= sr && cut.byteOffset / 4 + cut.length >= sr * 3)

  const quiet = new Float32Array(sr * 3)
  for (let i = sr; i < sr * 2; i++) quiet[i] = 0.02 * Math.sin(2 * Math.PI * 180 * i / sr)
  ok('a quiet voice is kept — the threshold follows the recording’s own peak', Math.abs(trimSilence(quiet, sr).length / sr - 1.5) < 0.1)
  ok('an empty take trims to nothing', trimSilence(new Float32Array(sr), sr).length === 0)

  const f = fadeEdges(new Float32Array(4000).fill(1), 48000)
  ok('the edges fade from zero over 15 ms; the voice between is untouched', f[0] === 0 && f[3999] === 0 && f[360] > 0.45 && f[360] < 0.55 && f[2000] === 1)

  const wav = new DataView(encodeWav(new Float32Array([0, 0.5, -0.5, 1, -1, 2]), 22050))
  const tag = (o) => String.fromCharCode(wav.getUint8(o), wav.getUint8(o + 1), wav.getUint8(o + 2), wav.getUint8(o + 3))
  ok('WAV header: RIFF/WAVE, PCM, mono, 16-bit, 22050 Hz', tag(0) === 'RIFF' && tag(8) === 'WAVE' && tag(12) === 'fmt ' && tag(36) === 'data'
    && wav.getUint16(20, true) === 1 && wav.getUint16(22, true) === 1 && wav.getUint32(24, true) === 22050 && wav.getUint16(34, true) === 16)
  ok('WAV sizes agree with the samples', wav.getUint32(40, true) === 12 && wav.getUint32(4, true) === 36 + 12 && wav.byteLength === 44 + 12)
  ok('samples are scaled and clipped, not wrapped', wav.getInt16(44 + 2, true) === 16383 && wav.getInt16(44 + 6, true) === 32767 && wav.getInt16(44 + 8, true) === -32768 && wav.getInt16(44 + 10, true) === 32767)
  ok('peakOf', Math.abs(peakOf(new Float32Array([0.1, -0.7, 0.3])) - 0.7) < 1e-6)
}

console.log('\nthe voice library’s clips')
{
  const CLIP_ID = /^[a-z](?:[A-Za-z0-9-]|\.(?!\.)){2,90}$/            // the Worker's own rule
  const ids = MANTRA_STEPS.map(mantraClip)
  for (const lang of ['en', 'hi']) for (const mode of ['short', 'detailed']) {
    for (const s of ALL_STEPS) ids.push(explainClip(null, s, mode, lang))
    for (const r of RITUALS) ids.push(explainClip(r, null, mode, lang))
  }
  ok('every clip id is accepted by the Worker', ids.every((i) => CLIP_ID.test(i)), `${ids.length} clips`)
  ok('no two clips share an id', new Set(ids).size === ids.length)
  const g = ALL_STEPS.find((s) => s.id === 'ganesha')
  ok('a clip is bound to its text: change the text, the id changes', mantraClip(g) !== mantraClip({ ...g, mantra: { ...g.mantra, dev: `${g.mantra.dev} ` } }))
  ok('…and the same text always gives the same id', mantraClip(g) === mantraClip({ ...g }) && textHash('ॐ') === textHash('ॐ'))
  ok('English and Hindi explanations are different clips', explainClip(null, g, 'short', 'en') !== explainClip(null, g, 'short', 'hi'))
  ok('“mantras only” has nothing to narrate', narration(RITUALS[0], g, 'none', 'en') === '')
  ok('the Gaṇeśa step is explained as the user specified', narration(null, g, 'short', 'en').includes('What is happening: Invocation of Lord Gaṇeśa.') && narration(null, g, 'short', 'en').includes('Why: Traditionally performed before beginning an auspicious ceremony'))
}

console.log('\na man’s voice or a woman’s — and never the wrong one')
{
  const V = (name, lang) => ({ name, lang })
  const EN = ['en-IN', 'en-GB', 'en-US'], HI = ['hi-IN'], SA = ['sa', 'hi-IN', 'hi']
  const chromeWin = [V('Microsoft David - English (United States)', 'en-US'), V('Microsoft Mark - English (United States)', 'en-US'), V('Microsoft Zira - English (United States)', 'en-US'),
    V('Google US English', 'en-US'), V('Google UK English Female', 'en-GB'), V('Google UK English Male', 'en-GB'), V('Google हिन्दी', 'hi-IN'), V('Google Deutsch', 'de-DE')]
  const edge = [V('Microsoft Neerja Online (Natural) - English (India)', 'en-IN'), V('Microsoft Prabhat Online (Natural) - English (India)', 'en-IN'),
    V('Microsoft Swara Online (Natural) - Hindi (India)', 'hi-IN'), V('Microsoft Madhur Online (Natural) - Hindi (India)', 'hi-IN'), V('Microsoft Sonia Online (Natural) - English (United Kingdom)', 'en-GB')]
  const android = [V('English India', 'en_IN'), V('Hindi India', 'hi_IN'), V('English United States', 'en_US')]
  const iphone = [V('Rishi', 'en-IN'), V('Veena', 'en-IN'), V('Lekha', 'hi-IN'), V('Samantha', 'en-US'), V('Daniel', 'en-GB')]
  const onlyHerEnIn = [V('Microsoft Heera - English (India)', 'en-IN'), V('Microsoft David - English (United States)', 'en-US')]

  ok('names tell: Female before Male, since "Female" contains "male"', genderOf(V('Google UK English Female')) === 'f' && genderOf(V('Google UK English Male')) === 'm'
    && genderOf(V('Microsoft Madhur Online (Natural) - Hindi (India)')) === 'm' && genderOf(V('Microsoft Swara Online (Natural) - Hindi (India)')) === 'f' && genderOf(V('English India')) === '')
  ok('Chrome on Windows, English: Male → a man, Female → a woman', genderOf(deviceVoice(chromeWin, EN, 'm').voice) === 'm' && genderOf(deviceVoice(chromeWin, EN, 'f').voice) === 'f')
  const hiM = deviceVoice(chromeWin, HI, 'm')
  ok('Chrome on Windows, Hindi: it has only a woman’s voice — Male plays NOTHING, and says why', hiM.voice === null && hiM.how === 'other')
  ok('…and Female plays her', deviceVoice(chromeWin, HI, 'f').voice.name === 'Google हिन्दी')
  ok('…and the mantra aid follows the same rule', deviceVoice(chromeWin, SA, 'm').voice === null && deviceVoice(chromeWin, SA, 'f').how === 'exact')
  ok('Edge: both languages have both, and the natural voices are chosen', deviceVoice(edge, EN, 'm').voice.name.includes('Prabhat') && deviceVoice(edge, EN, 'f').voice.name.includes('Neerja')
    && deviceVoice(edge, HI, 'm').voice.name.includes('Madhur') && deviceVoice(edge, HI, 'f').voice.name.includes('Swara'))
  ok('a man is found in another English before a woman is settled for', deviceVoice(onlyHerEnIn, EN, 'm').voice.name.includes('David') && deviceVoice(onlyHerEnIn, EN, 'f').voice.name.includes('Heera'))
  const a = deviceVoice(android, EN, 'm')
  ok('Android names say nothing of gender: the voice is used, and reported as unknown — not passed off as male', a.how === 'unknown' && a.voice.name === 'English India')
  ok('iPhone: Rishi for Male, Veena for Female; Hindi has only Lekha', deviceVoice(iphone, EN, 'm').voice.name === 'Rishi' && deviceVoice(iphone, EN, 'f').voice.name === 'Veena'
    && deviceVoice(iphone, HI, 'm').voice === null && deviceVoice(iphone, HI, 'f').voice.name === 'Lekha')
  ok('no voice for the language at all', deviceVoice([V('Google Deutsch', 'de-DE')], HI, 'm').how === 'none' && deviceVoice([], EN, 'f').how === 'none')
  ok('a voice of another language is never borrowed', deviceVoice(chromeWin, HI, 'f').voice.lang === 'hi-IN' && deviceVoice(chromeWin, EN, 'm').voice.lang.startsWith('en'))
}

console.log('\nthe Hanumān Cālīsā — the whole text, in both scripts')
{
  const DEV = /[ऀ-ॿ]/, LATIN = /[A-Za-z]/
  ok('forty chaupāīs — the count that gives it its name', CHAUPAIS.length === 40)
  ok('each chaupāī is two halves: one । and a closing ॥', CHAUPAIS.every(([d]) => (d.match(/।/g) || []).length === 1 && d.endsWith('॥') && (d.match(/॥/g) || []).length === 1))
  ok('each has its roman reading, two halves likewise', CHAUPAIS.every(([, r]) => r.split(' · ').length === 2 && !DEV.test(r) && LATIN.test(r)))
  ok('no Latin letter has strayed into the Devanāgarī', CHAUPAIS.every(([d]) => !LATIN.test(d)))
  ok('no chaupāī is given twice', new Set(CHAUPAIS.map(([d]) => d)).size === 40 && new Set(CHAUPAIS.map(([, r]) => r)).size === 40)
  ok('it opens and closes where it should', CHAUPAIS[0][0].startsWith('जय हनुमान ज्ञान गुन सागर।') && CHAUPAIS[39][0].startsWith('तुलसीदास सदा हरि चेरा।') && CHAUPAIS[38][0].includes('हनुमान चलीसा'))
  ok('the readings the two checked copies agree on', CHAUPAIS[22][0].includes('सम्हारो') && !CHAUPAIS[22][0].includes('संहारो') && CHAUPAIS[5][0].startsWith('संकर सुवन केसरीनंदन') && CHAUPAIS[31][0].includes('सदा रहो रघुपति के दासा') && CHAUPAIS[37][0].startsWith('जो सत बार पाठ कर कोई'))
  const sc = scriptFor('hanuman-chalisa')
  const hc = sc.filter((s) => s.id.startsWith('hc'))
  ok('the pāṭha is in the catalogue, with its purpose and its script', !!RITUALS.find((r) => r.key === 'hanuman-chalisa') && !!ABOUT['hanuman-chalisa'] && sc.length === 10 && sc[0].id === 'deepa' && sc[sc.length - 1].id === 'prasada')
  ok('two opening dohās, five passages of eight, one closing dohā — in order', hc.map((s) => s.id).join() === 'hcDoha1,hcChaupai1,hcChaupai2,hcChaupai3,hcChaupai4,hcChaupai5,hcDoha2')
  const lines = (t) => t.split('\n').filter((x) => x.trim())
  ok('the opening dohās are four lines, the closing one two', lines(hc[0].mantra.dev).length === 4 && lines(hc[6].mantra.dev).length === 2 && hc[0].mantra.dev.startsWith('श्रीगुरु चरन सरोज रज') && hc[6].mantra.dev.includes('हृदय बसहु सुर भूप॥'))
  ok('every passage has as many roman lines as Devanāgarī ones', hc.every((s) => lines(s.mantra.dev).length === lines(romanOf(s.mantra)).length))
  ok('the five passages together are the forty, in order', hc.slice(1, 6).flatMap((s) => lines(s.mantra.dev)).join('|') === CHAUPAIS.map(([d]) => d).join('|'))
  ok('each passage says what its verses speak of, and why — in English and Hindi', hc.every((s) => s.what.en && s.what.hi && s.why.en && s.why.hi && s.title.en && s.title.hi))
  ok('where the verses speak of results, they are reported as the poet’s — nothing is promised', hc[4].why.en.includes('nothing is promised') && hc[5].why.en.includes('poet’s own words'))
  ok('each passage can be recorded by a pandit as its own clip', hc.every((s) => MANTRA_STEPS.some((m) => m.id === s.id)) && new Set(hc.map(mantraClip)).size === 7)
}

console.log('\nthe offline cache (service worker)')
{
  // Run public/sw.js against a stand-in for the worker scope and see which requests it takes over.
  const handlers = {}
  const scope = {
    self: { addEventListener: (t, f) => { handlers[t] = f }, location: { origin: 'https://devashaa.com' }, skipWaiting() {}, clients: { claim() {} } },
    caches: { match: async () => undefined, open: async () => ({ put() {}, addAll: async () => {} }), keys: async () => [] },
    fetch: async () => ({ clone() { return this }, status: 200, type: 'basic' }),
    URL,
  }
  vm.runInNewContext(fs.readFileSync(new URL('./public/sw.js', import.meta.url), 'utf8'), scope)
  const takes = (path, mode = 'cors', method = 'GET') => {
    let handled = false
    handlers.fetch({ request: { method, url: `https://devashaa.com${path}`, mode }, respondWith(p) { handled = true; Promise.resolve(p).catch(() => {}) } })
    return handled
  }
  ok('it never answers for the API — a signed-in answer must not be replayed to the next person',
    !takes('/api/pooja/desk') && !takes('/api/pooja/me') && !takes('/api/pooja/bookings/0123456789abcdef0123456789abcdef') && !takes('/api/account/someone/profiles') && !takes('/api/share/abc'))
  ok('…nor hand out a relay credential it kept from yesterday', !takes('/api/pooja/room/0123456789abcdef0123456789abcdef/ice'))
  ok('it still serves the hashed assets and the app shell', takes('/assets/index-abc123.js') && takes('/pooja', 'navigate') && takes('/favicon.svg'))
  ok('it leaves writes and the cross-origin API alone', !takes('/assets/x.js', 'cors', 'POST') && (() => { let h = false; handlers.fetch({ request: { method: 'GET', url: 'https://devashaa-api.onrender.com/api/health', mode: 'cors' }, respondWith() { h = true } }); return !h })())
}

console.log(failed ? `\n${failed} FAILED ✗` : '\nALL PASS ✓')
process.exit(failed ? 1 : 0)
