/**
 * The device's own (machine) voices — which one, if any, may read for a family
 * that asked for a man's or a woman's voice.
 *
 * A browser lists its voices by name and language and says nothing of gender,
 * so the common ones are known here by name. The rule that matters: if the
 * family asked for a man's voice and the device has only a woman's (or the
 * reverse), the wrong one is NOT played — the guide says the device has none.
 */

// "female" is tested first: every name with "female" in it also contains "male".
const FEMALE = /female|woman|swara|neerja|heera|kalpana|ananya|aditi|lekha|veena|sangeeta|zira|aria|jenny|michelle|sonia|libby|hazel|susan|samantha|victoria|allison|ava|karen|moira|tessa|fiona|kate|serena|nicky|catherine|google हिन्दी|google us english/i
const MALE = /(^|[^e])male|\bman\b|madhur|prabhat|ravi|hemant|rishi|david|mark|guy|ryan|george|james|daniel|oliver|thomas|alex|aaron|fred|arthur|gordon|tom\b|google uk english male/i

/** 'm', 'f', or '' when the name does not tell. */
export const genderOf = (voice) => {
  const n = String((voice && voice.name) || '')
  return FEMALE.test(n) ? 'f' : MALE.test(n) ? 'm' : ''
}

const speaks = (v, tag) => String(v.lang || '').replace('_', '-').toLowerCase().startsWith(tag.toLowerCase())
const best = (list) => list.find((v) => /natural|neural/i.test(v.name)) || list.find((v) => /google/i.test(v.name)) || list[0]

/**
 * → { voice, how }
 *   'exact'   — a voice the device names as that gender;
 *   'unknown' — it has voices for the language but does not say which is a man's and which a woman's;
 *   'other'   — it has only the OTHER gender. `voice` is null: the wrong one is not played;
 *   'none'    — it has no voice for the language at all.
 * Every tag is searched for the gender before anything else is settled for — a
 * device with only a woman's en-IN voice may well have a man's en-GB one.
 */
export function deviceVoice(voices, tags, gender) {
  const all = []
  for (const tag of tags) for (const v of voices || []) if (speaks(v, tag) && !all.includes(v)) all.push(v)
  if (!all.length) return { voice: null, how: 'none' }
  const exact = all.filter((v) => genderOf(v) === gender)
  if (exact.length) return { voice: best(exact), how: 'exact' }
  const unknown = all.filter((v) => !genderOf(v))
  if (unknown.length) return { voice: best(unknown), how: 'unknown' }
  return { voice: null, how: 'other' }
}
