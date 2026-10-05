/**
 * A pandit's recording, made ready for every family's device.
 *
 * Browsers record in different containers (WebM/Opus in Chrome, MP4/AAC in
 * Safari) and not every phone can play the other's. So the recording is decoded
 * once, here, in the browser that made it, and saved as plain WAV — which
 * everything plays. On the way it is made mono, the silence before the first
 * syllable and after the last is trimmed, and the level is brought to the same
 * peak for every pandit, so one chant is not twice as loud as the next.
 * Nothing else is done to the voice: no noise gate, no compression, no pitch.
 */

/** The peak absolute sample. */
export function peakOf(x) {
  let p = 0
  for (let i = 0; i < x.length; i++) { const a = x[i] < 0 ? -x[i] : x[i]; if (a > p) p = a }
  return p
}

/**
 * Cut the silence from both ends. "Silence" is a 20 ms window whose RMS is
 * more than ~26 dB below the recording's own peak, so a quiet recording is
 * trimmed as fairly as a loud one. `pad` seconds are kept either side.
 */
export function trimSilence(x, sampleRate, { pad = 0.25, win = 0.02, ratio = 0.05, floor = 0.002 } = {}) {
  const n = x.length
  const w = Math.max(1, Math.round(sampleRate * win))
  const threshold = Math.max(floor, peakOf(x) * ratio)
  const loud = (i0) => {
    const e = Math.min(n, i0 + w)
    let s = 0
    for (let i = i0; i < e; i++) s += x[i] * x[i]
    return Math.sqrt(s / Math.max(1, e - i0)) >= threshold
  }
  let a = 0
  while (a < n && !loud(a)) a += w
  if (a >= n) return x.subarray(0, 0)
  let b = Math.floor((n - 1) / w) * w
  while (b > a && !loud(b)) b -= w
  const p = Math.round(sampleRate * pad)
  return x.subarray(Math.max(0, a - p), Math.min(n, b + w + p))
}

/** Mono 16-bit PCM WAV. */
export function encodeWav(samples, sampleRate) {
  const n = samples.length
  const buf = new ArrayBuffer(44 + n * 2)
  const v = new DataView(buf)
  const str = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)) }
  str(0, 'RIFF'); v.setUint32(4, 36 + n * 2, true); str(8, 'WAVE')
  str(12, 'fmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true)
  v.setUint32(24, sampleRate, true); v.setUint32(28, sampleRate * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true)
  str(36, 'data'); v.setUint32(40, n * 2, true)
  for (let i = 0; i < n; i++) {
    const s = Math.max(-1, Math.min(1, samples[i]))
    v.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true)
  }
  return buf
}

/** A short fade at each end, so a trimmed edge cannot click. */
export function fadeEdges(x, sampleRate, seconds = 0.015) {
  const k = Math.min(Math.floor(x.length / 2), Math.round(sampleRate * seconds))
  for (let i = 0; i < k; i++) { const g = i / k; x[i] *= g; x[x.length - 1 - i] *= g }
  return x
}

const OUT_RATE = 22050
const TARGET_PEAK = 0.89        // about −1 dBFS

/**
 * Decode whatever the browser recorded and return { blob (audio/wav), seconds }.
 * Throws 'silent' if there is no voice in it.
 */
export async function toWav(blob) {
  const AC = window.AudioContext || window.webkitAudioContext
  const ctx = new AC()
  let decoded
  try { decoded = await ctx.decodeAudioData(await blob.arrayBuffer()) } finally { try { ctx.close() } catch { /* closed */ } }
  const n = decoded.length, ch = decoded.numberOfChannels
  const mono = new Float32Array(n)
  for (let c = 0; c < ch; c++) { const d = decoded.getChannelData(c); for (let i = 0; i < n; i++) mono[i] += d[i] / ch }
  const sr = decoded.sampleRate
  const cut = trimSilence(mono, sr)
  if (cut.length < sr * 0.4) throw new Error('silent')
  const voice = fadeEdges(new Float32Array(cut), sr)
  const peak = peakOf(voice)
  const gain = peak > 0 ? Math.min(10, TARGET_PEAK / peak) : 1
  // Resample with the browser's own resampler; if it will not make that rate, keep the recorded one.
  let out = voice, rate = sr
  try {
    const off = new (window.OfflineAudioContext || window.webkitOfflineAudioContext)(1, Math.ceil(voice.length * OUT_RATE / sr), OUT_RATE)
    const src = off.createBufferSource()
    const ab = off.createBuffer(1, voice.length, sr)
    ab.copyToChannel(voice, 0)
    src.buffer = ab
    src.connect(off.destination)
    src.start()
    out = (await off.startRendering()).getChannelData(0)
    rate = OUT_RATE
  } catch { /* some browsers only render at the device rate */ }
  const scaled = new Float32Array(out.length)
  for (let i = 0; i < out.length; i++) scaled[i] = out[i] * gain
  return { blob: new Blob([encodeWav(scaled, rate)], { type: 'audio/wav' }), seconds: out.length / rate, rate }
}
