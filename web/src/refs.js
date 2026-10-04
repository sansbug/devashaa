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

export function scrubProse(text) {
  if (typeof text !== 'string' || !text || !ANY.test(text)) return text
  let s = text.replace(PAREN_ASIDE, '')
  s = s.replace(PRESENTED, '').replace(AS_STATES, '')
  s = s.replace(NAME, 'the text')
  s = s.replace(READS_AS, (m, a, x) => `${a} ${x} is`)
  s = s.replace(ASSIGNS, 'the native is assigned ')
  s = s.replace(VERB, '')
  s = s.replace(TEXTS, 'the tradition').replace(TEXT_POS, (m, t) => `${t}he tradition’s`).replace(TEXT, (m, t) => `${t}he tradition`)
  s = s.replace(/\s*\((?:the text|the tradition|the source)\)/g, '')
  s = s.replace(/[ \t]{2,}/g, ' ').replace(/\s+([,;.:])/g, '$1').replace(/\(\s+/g, '(').replace(/,\s*,/g, ',')
  s = s.replace(/^[\s,;:—–-]+/, '').replace(/\.\s*\./g, '.')
  s = s.replace(SENT_START, (m, lead, c) => lead + c.toUpperCase())
  return s.trim()
}
