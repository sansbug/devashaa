"""Prose without the footnotes.

The readings keep their loci in the data — every gist still carries its
citation — but the SENTENCES were written with the source as their subject:
"Bṛhat Jātaka (18.1) reads the Sun-in-Taurus native as …", "the text adds:
promotion in job", "(the text: royal favours)". A reader who has chosen not to
see references should not meet the book's name mid-sentence either.

scrub() rewrites those constructions without touching the substance:

  * a parenthetical aside about the text is dropped
  * a source name (with its chapter/verse/page) becomes "the text", then
  * "the text reads the X native as …"  →  "The X native is …"
    "the text assigns (the native) …"    →  "The native is assigned …"
    "the text states / says / adds …"    →  "…"
    "Presented as the text's … reading, not as fate."  →  (dropped)
  * whatever "the text" is left becomes "the tradition"
  * spacing, punctuation and sentence capitals are tidied

scrub_payload() walks a JSON-able structure and scrubs every string value
except the ones that ARE references (citation, source, rule, …), which the
client hides by class and keeps for the references view.

Applied in app.py as an after_request step unless the request says
X-Refs: 1 — the switch on /references. Nothing is scrubbed at rest.
"""
from __future__ import annotations

import re

SOURCES = (
    r"(?:Bṛhat Parāśara Horā Śāstra|Brihat Parashara Hora Shastra|Bṛhat Parāśara|BPHS|Parāśara|"
    r"Bṛhat Jātaka|Brihat Jataka|Sārāvalī|Saravali|Jātaka Pārijāta|Jataka Parijata|"
    r"Phaladīpikā|Phaladipika|Bṛhat Saṁhitā|Brihat Samhita|Tājika-Nīlakaṇṭhī|Tajika-Nilakanthi|"
    r"Nīlakaṇṭha(?: Daivajña)?|Chamatk[āa]ra(?: C(?:h)?int[āa]ma[ṇn]i)?|Brihat(?: Jataka)?|Jaimini Sūtra|Jaimini Sutra|"
    r"K\. ?S\. Charak|Charak|B\. ?V\. Raman|Raman|K\. ?N\. Rao|C\. ?S\. Patel|Patel|"
    r"Mantreśvara|Varāhamihira|Kalyāṇa Varma|Santhanam|Ojha)"
)
# an optional locus after the name: "(18.1)", "22.4-5", "ch.11 v.2 (p.121)", "Vol I ch.26 vv.2-5"
LOCUS = (
    r"(?:\s*\(\s*[\d][\d.,:–\- ]*\s*\))?"
    r"(?:\s*(?:Vol\.?\s*[IVX]+,?\s*)?(?:ch\.|Ch\.|chapter|v\.|vv\.|śl\.|sl\.|p\.|pp\.)?\s*\d[\d.,:–\- ]*"
    r"(?:\s*(?:v\.|vv\.|p\.|pp\.)\s*\d[\d.,–\-]*)?(?:\s*\(p\.\s*\d+\))?)?"
)

_ANY = re.compile(r"(?:" + SOURCES + r"|[Tt]he texts?\b|[Ff]ootnote)")
_PAREN_ASIDE = re.compile(r"\s*\((?:[Tt]he text|[Tt]he source|[Ff]ootnote|p\.\s*\d+\s*footnote)[^()]*\)")
_PAREN_BARE = re.compile(r"\s*\((?:the text|the tradition|the source)\)")
_NAME = re.compile(r"\b" + SOURCES + LOCUS + r"(?=[\s,;:.)'’]|$)")
_PRESENTED = re.compile(r"\s*Presented as the text['’]s[^.]*\.")
_AS_STATES = re.compile(r",?\s*as the (?:dated )?text (?:states|says|has it|puts it),?")
_READS_AS = re.compile(r"\b[Tt]he text (?:reads|describes|sees|casts) (a|an|the) (.+?) as\b")
_ASSIGNS = re.compile(r"\b[Tt]he text (?:assigns|grants) (?:the native |a native )?")
_VERB = re.compile(
    r"\b[Tt]he text (?:states|says|holds|notes|adds|declares|specifies|lists|calls|names|reads|stipulates|"
    r"carries .{0,80}?note that|carries .{0,80}?note)(?: that)?[:,]?\s*"
)
_TEXTS = re.compile(r"\b[Tt]he texts\b")
_TEXT_POS = re.compile(r"\b([Tt])he text['’]s\b")
_TEXT = re.compile(r"\b([Tt])he text\b")
_SENT_START = re.compile(r"(^|[.!?]\s+|\n\s*)([a-zà-ž])")
_SPACES = re.compile(r"[ \t]{2,}")

EXCLUDE_KEYS = {
    "citation", "citations", "cite", "source", "source_id", "sources_note", "rule", "validation",
    "verification", "tier", "provenance", "translator", "adaptation", "confidence", "edition",
    "key", "id", "lord", "graha", "sign", "house",
}


def scrub(text: str) -> str:
    if not text or not _ANY.search(text):
        return text
    s = _PAREN_ASIDE.sub("", text)
    s = _PRESENTED.sub("", s)
    s = _AS_STATES.sub("", s)
    s = _NAME.sub("the text", s)
    s = _READS_AS.sub(lambda m: f"{m.group(1)} {m.group(2)} is", s)
    s = _ASSIGNS.sub("the native is assigned ", s)
    s = _VERB.sub("", s)
    s = _TEXTS.sub("the tradition", s)
    s = _TEXT_POS.sub(lambda m: m.group(1) + "he tradition’s", s)
    s = _TEXT.sub(lambda m: m.group(1) + "he tradition", s)
    s = _PAREN_BARE.sub("", s)
    # tidy
    s = _SPACES.sub(" ", s)
    s = re.sub(r"\s+([,;.:])", r"\1", s)
    s = re.sub(r"\(\s+", "(", s)
    s = re.sub(r",\s*,", ",", s)
    s = re.sub(r"^[\s,;:—–-]+", "", s)
    s = re.sub(r"\.\s*\.", ".", s)
    s = _SENT_START.sub(lambda m: m.group(1) + m.group(2).upper(), s)
    return s.strip()


def scrub_payload(obj, _key: str | None = None):
    """Scrub every prose string in a JSON-able structure, skipping the
    reference fields themselves. Returns a new structure; scalars pass
    through."""
    if isinstance(obj, str):
        return obj if _key in EXCLUDE_KEYS else scrub(obj)
    if isinstance(obj, list):
        return [scrub_payload(x, _key) for x in obj]
    if isinstance(obj, dict):
        return {k: (v if k in EXCLUDE_KEYS else scrub_payload(v, k)) for k, v in obj.items()}
    return obj
