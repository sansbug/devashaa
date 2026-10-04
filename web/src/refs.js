/**
 * The references switch and the prose scrubber's JS twin.
 *
 * References (chapter-and-verse, page numbers, provenance chips) are hidden
 * unless the switch on /references is on; that state lives in localStorage
 * ("refs") and on <html data-refs>. The API scrubs the SENTENCES it sends
 * when the request says X-Refs: 0 (see api/prose.py); the UI's own strings
 * — section leads, labels, notes written with a text as their subject — go
 * through scrubProse() here, the same rules in the same order, so the two
 * halves of a page read alike.
 */
export const REFS_KEY = 'refs'
export const refsOn = () => { try { return localStorage.getItem(REFS_KEY) === '1' } catch { return false } }
export const applyRefs = (on) => { if (typeof document !== 'undefined') document.documentElement.dataset.refs = on ? '1' : '0' }

const SOURCES = '(?:Bṛhat Parāśara Horā Śāstra|Brihat Parashara Hora Shastra|Bṛhat Parāśara|BPHS|Parāśara|'
  + 'Bṛhat Jātaka|Brihat Jataka|Sārāvalī|Saravali|Jātaka Pārijāta|Jataka Parijata|'
  + 'Phaladīpikā|Phaladipika|Bṛhat Saṁhitā|Brihat Samhita|Tājika-Nīlakaṇṭhī|Tajika-Nilakanthi|'
  + 'Nīlakaṇṭha(?: Daivajña)?|Chamatk[āa]ra(?: C(?:h)?int[āa]ma[ṇn]i)?|Brihat(?: Jataka)?|Jaimini Sūtra|Jaimini Sutra|'
  + 'K\\. ?S\\. Charak|Charak|B\\. ?V\\. Raman|Raman|K\\. ?N\\. Rao|C\\. ?S\\. Patel|Patel|'
  + 'Mantreśvara|Varāhamihira|Kalyāṇa Varma|Santhanam|Ojha)'
const LOCUS = '(?:\\s*\\(\\s*[\\d][\\d.,:–\\- ]*\\s*\\))?'
  + '(?:\\s*(?:Vol\\.?\\s*[IVX]+,?\\s*)?(?:ch\\.|Ch\\.|chapter|v\\.|vv\\.|śl\\.|sl\\.|p\\.|pp\\.)?\\s*\\d[\\d.,:–\\- ]*'
  + '(?:\\s*(?:v\\.|vv\\.|p\\.|pp\\.)\\s*\\d[\\d.,–\\-]*)?(?:\\s*\\(p\\.\\s*\\d+\\))?)?'

const ANY = new RegExp('(?:' + SOURCES + '|[Tt]he texts?\\b|[Ff]ootnote)')
const PAREN_ASIDE = /\s*\((?:[Tt]he text|[Tt]he source|[Ff]ootnote|p\.\s*\d+\s*footnote)[^()]*\)/g
const NAME = new RegExp('\\b' + SOURCES + LOCUS + "(?=[\\s,;:.)'’]|$)", 'g')
const PRESENTED = /\s*Presented as the text['’]s[^.]*\./g
const AS_STATES = /,?\s*as the (?:dated )?text (?:states|says|has it|puts it),?/g
const READS_AS = /\b[Tt]he text (?:reads|describes|sees|casts) (a|an|the) (.+?) as\b/g
const ASSIGNS = /\b[Tt]he text (?:assigns|grants) (?:the native |a native )?/g
const VERB = /\b[Tt]he text (?:states|says|holds|notes|adds|declares|specifies|lists|calls|names|reads|stipulates|carries .{0,80}?note that|carries .{0,80}?note)(?: that)?[:,]?\s*/g
const TEXTS = /\b[Tt]he texts\b/g
const TEXT_POS = /\b([Tt])he text['’]s\b/g
const TEXT = /\b([Tt])he text\b/g
const SENT_START = /(^|(?<!\bc)(?<!\bch)(?<!\bp)(?<!\bpp)(?<!\bv)(?<!\bvv)(?<!\bvs)(?<!\betc)(?<!\be\.g)(?<!\bi\.e)[.!?]\s+|\n\s*)([a-zà-ž])/g

// ── the hedges — the policy's in-line commentary, dropped (prose.py's _soften) ──
const HW = "(?:not (?:as )?fate|not a fate|not a prediction|not any prediction|not (?:as )?(?:the reader['’]s|the native['’]s) fate|"
  + "not medical advice|not advice|not a verdict|not a diagnosis|dated|stated[- ]effects?|neutralis\\w*|historicis\\w*|"
  + "kept (?:as|progeny|only|rather|plainly)|rendered partner-neutral\\w*|progeny-neutral\\w*|cited|the verse['’]s|much-qualified|omitted)"
const HEDGE_ANY = new RegExp(HW + '|\\[|kept faithfully|of its era|classical author|not a forecast|\\b[Ii]t (?:also )?(?:reads|describes|sees|casts|assigns)\\b|[Ii]n its own (?:idiom|words|terms)|[Tt]he verse\\b')
const DASH = '(?:\\s+-\\s+|\\s*[—–]\\s*)'
const H_PAREN = new RegExp('\\s*\\((?:[^()]*\\b' + HW + '\\b[^()]*)\\)', 'g')
const H_BRACKET = /\s*\[[^\]]*\]/g
const H_DASH_ENCLOSED = new RegExp(DASH + '(?:[^—–.;]*?\\b' + HW + '\\b[^—–.;]*?)' + DASH, 'g')
const H_DASH_TRAILING = new RegExp(DASH + '(?:[^—–.]*?\\b' + HW + '\\b[^—–.]*)(?=\\.|;|$)', 'g')
const H_INLINE = /,?\s*(?:as|given as|kept as|shown as|presented as|framed as)\s+(?:a |an |the |its |the tradition['’]s |the tradition['’]s own )?(?:own )?(?:dated|stated|classical|~\d+(?:th|st|nd|rd)[- ]c(?:entury|\.)?|~\d+ CE|somatic)[^,.;—]*?(?:effects?|view|reading|note|marker|clause|telling)\b(?:,? (?:and )?not [^,.;—]*)?,?|,?\s*in its own dated (?:telling|view|words|terms),?|,?\s*of its era(?:,? (?:and )?not [^,.;—]*)?/gi
const H_SENTENCE = /(?:^|(?<=[.!?;]\s))[^.!?;]*\b(?:is dropped|are dropped|ranking(?: is)? dropped|is refused|are refused|is omitted|are omitted|ship plainly|shipped faithfully|glossed and kept|kept plainly|kept faithfully|kept as a livelihood|no count asserted|not (?:as )?(?:the native['’]s |the reader['’]s )?fate|rather than fate|not a forecast|not a medical judgement|not a prediction|not a verdict|not (?:as )?medical advice|no dated social content|its dated|the tradition['’]s (?:own )?(?:dated|stated)|classical author['’]s|stated[- ]effects?|stated reading|cited|year-old text|neutralis\w*|partner-neutral\w*|progeny-neutral\w*|kept progeny|[Nn]o dated social content|gendered|[Ii]ts clause on|[Tt]he verse['’]s|framed as)\b[^.!?;]*[.!?;]\s*/g
const H_IDIOM = /\b[Ii]n its own (?:idiom|words|terms),?\s*/g
const IT_READS_AS = /\b[Ii]t (?:also )?(?:reads|describes|sees|casts) (a|an|the) (.+?) as\b/g
const IT_ASSIGNS = /\b[Ii]t (?:also )?assigns (?:the native |a native )?/g
const H_CITED = /,\s*cited(?=[,.;)])/g
const H_STUB = /(?:^|(?<=[.;]\s))(?:[^.;]*\b(?:reading|clause|remark|note|effect) (?:is|are)\s*;\s*|(?:This|That|It) (?:is|are),?\s*(?:cited)?\.\s*)/g
const H_VERSE = /\b([Tt])he verse\b/g
function soften(s) {
  s = s.replace(H_BRACKET, '').replace(H_PAREN, '').replace(H_INLINE, ',')
  s = s.replace(H_DASH_ENCLOSED, ' ').replace(H_DASH_TRAILING, '').replace(H_SENTENCE, '').replace(H_IDIOM, '')
  s = s.replace(IT_READS_AS, (m, a, x) => `${a} ${x} is`).replace(IT_ASSIGNS, 'the native is assigned ')
  s = s.replace(H_CITED, '').replace(H_STUB, '').replace(H_VERSE, (m, t) => `${t}he tradition`)
  return s
}

export function scrubProse(text) {
  if (typeof text !== 'string' || !text || !(ANY.test(text) || HEDGE_ANY.test(text))) return text
  let s = text.replace(PAREN_ASIDE, '')
  s = s.replace(PRESENTED, '').replace(AS_STATES, '')
  s = s.replace(NAME, 'the text')
  s = s.replace(READS_AS, (m, a, x) => `${a} ${x} is`)
  s = s.replace(ASSIGNS, 'the native is assigned ')
  s = s.replace(VERB, '')
  s = s.replace(TEXTS, 'the tradition').replace(TEXT_POS, (m, t) => `${t}he tradition’s`).replace(TEXT, (m, t) => `${t}he tradition`)
  s = s.replace(/\s*\((?:the text|the tradition|the source)\)/g, '')
  s = soften(s)
  s = s.replace(/[ \t]{2,}/g, ' ').replace(/\s+([,;.:])/g, '$1').replace(/\(\s+/g, '(').replace(/\(\s*\)/g, '').replace(/,\s*,/g, ',')
  s = s.replace(/,\s*([.;])/g, '$1').replace(/\.\s*,\s*/g, '. ').replace(/\s+(?:and|or|but)\s*([.;])/g, '$1').replace(/[—–]\s*([.;,])/g, '$1').replace(/[;,]\s*$/, '.')
  s = s.replace(/\b(and|or|but|yet),\s*,?\s*(?=[—–]|[a-zà-ž])/g, '$1 ').replace(/,\s*[—–]\s*/g, ' — ')
  s = s.replace(/([;,])\s*(?:and|or|but|yet)\s*[—–]\s*/g, '$1 ').replace(/(?:^|(?<=[.!?]\s))(?:Stated|Shown|Presented|Framed|Given|Kept|Cited)\.\s*/g, '')
  s = s.replace(/\b(states|says|adds|holds|notes|assigns|gives|calls|reads|makes|is|are),\s+(?=[a-zà-ž])/g, '$1 ').replace(/\s+([,;.:])/g, '$1')
  s = s.replace(/^[\s,;:—–-]+/, '').replace(/\.\s*\./g, '.').replace(/\s{2,}/g, ' ')
  s = s.replace(SENT_START, (m, lead, c) => lead + c.toUpperCase())
  return s.trim()
}
