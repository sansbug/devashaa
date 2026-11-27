/**
 * A dated verse's age as calendar months of this native's life (api/bhava_effects.py `age` on a clause).
 * Owner, 2026-11-26: "dated event is fine". The verse's own words decide the window:
 *   year  "in his 32nd year"        → from the 31st birthday to the 32nd;
 *   age   "at the age of 30"        → from the 30th birthday to the 31st;
 *   after "after the 20th year"     → from the 20th birthday on.
 * The dates are arithmetic on the birth date; the statement is the text's, and it is not a promise.
 */
const MONTHS = { en: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], hi: ['जनवरी', 'फ़रवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'] }
const EN_ORD = (n) => `${n}${n % 10 === 1 && n !== 11 ? 'st' : n % 10 === 2 && n !== 12 ? 'nd' : n % 10 === 3 && n !== 13 ? 'rd' : 'th'}`
const HI_ORD = (n) => `${n}वें`

/** birth "YYYY-MM-DD …" → { y, m } (m 0-based), or null */
export function birthOf(chart) {
  const x = /^(\d{4})-(\d{2})/.exec(String((chart && chart.local_time) || ''))
  return x ? { y: +x[1], m: +x[2] - 1 } : null
}
const at = (b, years, l) => `${MONTHS[l][b.m]} ${b.y + years}`

/** One sentence per age the clause names, in language l. Empty when the birth date is unknown. */
export function ageSentence(age, chart, l, now = Date.now()) {
  const b = birthOf(chart)
  if (!age || !b) return ''
  const nowY = new Date(now).getFullYear() + new Date(now).getMonth() / 12
  const tense = (endYears) => (b.y + b.m / 12 + endYears <= nowY ? 'past' : 'open')
  const parts = age.n.map((n) => {
    if (age.kind === 'after') {
      return l === 'hi' ? `आपके ${HI_ORD(n)} जन्मदिन (${at(b, n, l)}) से आगे` : `from your ${EN_ORD(n)} birthday (${at(b, n, l)}) on`
    }
    const s = age.kind === 'year' ? n - 1 : n
    const span = l === 'hi' ? `${at(b, s, l)} से ${at(b, s + 1, l)}` : `${at(b, s, l)} to ${at(b, s + 1, l)}`
    const what = age.kind === 'year'
      ? (l === 'hi' ? `आपका ${n}वाँ वर्ष` : `your ${EN_ORD(n)} year`)
      : (l === 'hi' ? `आपके ${HI_ORD(n)} जन्मदिन के बाद का वर्ष` : `the year after your ${EN_ORD(n)} birthday`)
    const past = tense(s + 1) === 'past'
    return l === 'hi' ? `${what}: ${span}${past ? ' (बीत चुका)' : ''}` : `${what}: ${span}${past ? ' (already past)' : ''}`
  })
  const lead = age.n.length > 1 ? (l === 'hi' ? 'श्लोक की आयु, आपकी तारीखों में (कोई एक): ' : 'The verse’s age, in your dates (either): ') : (l === 'hi' ? 'श्लोक की आयु, आपकी तारीखों में: ' : 'The verse’s age, in your dates: ')
  return lead + parts.join(l === 'hi' ? '; ' : '; ') + (l === 'hi' ? '।' : '.')
}
