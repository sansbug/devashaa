"""
Phaladīpikā of Mantreśvara, Adhyāya 9 ślokas 1-13 — the results of each of the
twelve signs rising (lagna-phala), and śloka 13's statement that the same results
hold for the sign the Moon occupies. CLASSICAL tier.

Source read: V. Subrahmanya Sastri's translation, 2nd ed. 1950, printed pp.98-102
(the scan's own text layer, PDF pp.133-137), on 2026-11-16.

⚠ confidence = "ocr_text": read from the scan's text layer (clean for these
pages; a few letters repaired: "sous" → sons, "Simba" → Simha, "plurapy" → plump),
NOT yet checked against the page images (the file is a mixed-raster scan nothing
on the 2026-11 laptop can render) and not yet adversarially verified.

The gists are site-authored renderings of the translation, per
docs/classical-sources-policy.md §5. The WHOLE description is kept — flattering
and unflattering traits together; nothing is softened into praise. Gendered terms
are neutralised ("long for women" → amorous; "wife" → spouse; "sons" → children),
"Brahmins" is glossed as the learned, and one clause is set aside and SAID to be
set aside (Makara: a verdict on attachment to women "of the prohibited class").
The Sanskrit is not re-translated. No book is named inside a gist, so the
references-off view needs no scrubbing.
"""
SOURCE = {
    "id": "phaladipika", "text": "Phaladīpikā", "author": "Mantreśvara",
    "date": "~13th c. CE", "translator": "V. Subrahmanya Sastri",
    "tier": "classical",
}


def _e(sloka, gist, note=""):
    return {"citation": f"Phaladīpikā 9.{sloka}", "gist": gist, "confidence": "ocr_text",
            "adaptation_note": note or "Rendered closely from the translation; the whole description is kept."}


# sign index 0-11 (Meṣa … Mīna)
BY_SIGN = [
    _e(1, "Round eyes and weak knees; fierce; afraid of water; a sparing eater; amorous; always on the move; fickle; given to untruth; limbs that carry bruises.", "'Long for women' rendered as amorous."),
    _e(2, "Plump thighs and a broad face; engaged in agriculture; happy in the middle and later parts of life; amorous; liberal in gifts; forgiving; able to endure hardship; an owner of cattle; marks or moles on the back, face and sides.", "'Fond of young women' rendered as amorous."),
    _e(3, "Dark eyes and curled hair; fond of amorous sport; skilled at reading the thoughts of others; a raised nose; a liking for music and dancing; a keeper to the home.", "'Sporting with women' rendered as amorous sport."),
    _e(4, "Led by the spouse; a fleshy neck; surrounded by friends; an owner of many houses; prominent hips; rich; short in stature; crooked in views; quick in walking; intelligent; fond of water; very few children.", "'Henpecked' rendered as led by the spouse; 'sons' as children."),
    _e(5, "Reddish eyes, a large chin and a broad face; arrogant and powerful; angry at trifles; drawn to forests and hills; obedient to the mother; firm-minded."),
    _e(6, "Drooping shoulders and arms; standing gained through the houses and wealth of others; truthful and kind in speech; a look made faint by modesty; fond of sensual enjoyment; a knower of the meaning of the śāstras; very few children."),
    _e(7, "A lean and frail body; few children; devoted to the worship of the gods and of the learned; wandering; known by two names; tall; clever in trade; brave; unsparing; impartial in argument.", "'Brahmins' glossed as the learned; 'merciless' rendered as unsparing."),
    _e(8, "Round thighs and knees, broad eyes and chest; ill at a very early age; separated from parents and teachers; a doer of cruel acts; honoured by the ruler; hands and feet that carry the lotus mark."),
    _e(9, "A long face and neck, large ears and nose; intent on work; short in stature; a favourite of the ruler; eloquent; liberal in gifts; an overcomer of enemies; won over only by kindness; of great strength."),
    _e(10, "Weak in the lower limbs; of great strength or courage; one who finishes what is undertaken; indolent; a religious hypocrite; fortunate; always on the move; subject to wind-disease; without shame.",
       "One clause is set aside under the policy on gender and caste verdicts (an attachment to old women 'of the prohibited class'); everything else is kept."),
    _e(11, "A doer of wrong in secret; a body shaped like a water-pot; skilled at striking down others; able to endure long marches; of very limited means; covetous, and free with the wealth of others; money both lost and gained; fond of perfumes and flowers.", "'Clever in hitting or killing others' rendered as skilled at striking down others."),
    _e(12, "Drinks much water; a well-proportioned, shining body; fond of the spouse; gains from selling pearls and other produce of the sea; learned; grateful for favours done; an overcomer of enemies; very good eyes; fortunate.", "'Wife' rendered as spouse."),
]

# śl.13 — why the same description is shown for the Moon's sign
MOON_RULE = {
    "citation": "Phaladīpikā 9.13",
    "gist": "Whatever is stated as the result of a sign being the ascendant is also to be said of the sign the Moon occupies.",
    "confidence": "ocr_text",
}


def character(lagna: int, moon_sign: int | None) -> dict:
    """The text's description for the rising sign and, by śl.13, for the Moon's sign."""
    out = {"source": SOURCE, "lagna": {"sign": lagna, **BY_SIGN[lagna]}}
    if moon_sign is not None:
        out["moon"] = {"sign": moon_sign, **BY_SIGN[moon_sign], "basis": MOON_RULE}
    return out
