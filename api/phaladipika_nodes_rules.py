"""
Phaladīpikā of Mantreśvara, Adhyāya 8 ślokas 25-33 — RĀHU and KETU in the twelve
bhāvas. CLASSICAL tier. Complements phaladipika_rules.py (the seven grahas).

Source read: V. Subrahmanya Sastri's translation, 2nd ed. 1950, printed pp.94-97
(the scan's own text layer, PDF pp.129-132), on 2026-11-15. The śloka numbers are
the edition's: Rāhu — śl.25 (bhāvas 1-4), 26 (5-8), 27 (9-12); Ketu — śl.28 (1-2),
29 (3-4), 30 (5-6), 31 (7-8), 32 (9-10), 33 (11-12).

⚠ confidence = "ocr_text": these were read from the scan's text layer, which is
clean for these pages, but NOT checked against the page images (the file is a
mixed-raster scan that could not be rendered on the 2026-11 laptop) and not yet
put through the adversarial verification the seven-graha entries had.

The gists are site-authored renderings of the translation, per
docs/classical-sources-policy.md §5: the whole verdict is kept, favourable and
unfavourable together; gendered terms are neutralised (wife → partner, sons /
issue → children); a caste verdict ("outcast") is rendered as a loss of standing;
disease, poverty and length of life are kept as the text's own dated statement.
The Sanskrit is not re-translated.
"""
SOURCE = {
    "id": "phaladipika", "text": "Phaladīpikā", "author": "Mantreśvara",
    "date": "~13th c. CE", "translator": "V. Subrahmanya Sastri",
    "tier": "classical",
}


def _e(sloka, gist, classes=(), note=""):
    return {
        "citation": f"Phaladīpikā 8.{sloka}",
        "gist": gist,
        "adaptation": {"classes": list(classes), "action": "neutralise" if classes else "clean",
                       "note": note or "Rendered closely from the translation; the whole verdict is kept."},
        "confidence": "ocr_text",
    }


_G = ("gender",)
_H = ("health",)

IN_HOUSE = {
    "rahu": {
        1: _e(25, "Phaladipika reads a native with Rahu in the 1st bhava as short-lived, possessed of wealth and strength, and subject to ailments of the upper body (head, face).", _H),
        2: _e(25, "Phaladipika reads a native with Rahu in the 2nd bhava as doubtful or insincere in speech, subject to ailments of the mouth or face, tender-hearted, gaining wealth through the ruler, quick to anger, and happy.", _H),
        3: _e(25, "Phaladipika reads a native with Rahu in the 3rd bhava as proud, at odds with siblings, strong-willed, long-lived and wealthy.", _G, "'Brothers' rendered as siblings."),
        4: _e(25, "Phaladipika reads a native with Rahu in the 4th bhava as foolish, a cause of sorrow, having friends, short-lived, and happy at one time or another."),
        5: _e(26, "Phaladipika reads a native with Rahu in the 5th bhava as speaking through the nose, childless, hard-hearted, and subject to stomach pain.", _H),
        6: _e(26, "Phaladipika reads a native with Rahu in the 6th bhava as troubled by enemies or oppressed by malefic influences, subject to a rectal ailment, wealthy and long-lived.", _H),
        7: _e(26, "Phaladipika reads a native with Rahu in the 7th bhava as losing wealth through intrigues, suffering separation from the beloved and a loss of vigour, and becoming self-willed and foolish.", _G, "'Intrigues with women' and 'lose his manhood' rendered partner-neutral."),
        8: _e(26, "Phaladipika reads a native with Rahu in the 8th bhava as short-lived, given to impure acts, impaired in a limb, subject to wind-disease, and having few children.", _H + _G, "'Limited issue' rendered as few children."),
        9: _e(27, "Phaladipika reads a native with Rahu in the 9th bhava as contrary in speech, the head of a clan, village or town, and given to unrighteous deeds."),
        10: _e(27, "Phaladipika reads a native with Rahu in the 10th bhava as famous and fearless, having few children, busy in others' affairs, and doing no good act.", _G, "'Limited number of issue' rendered as few children; the whole verdict — fame and fearlessness together with the unfavourable clauses — is kept."),
        11: _e(27, "Phaladipika reads a native with Rahu in the 11th bhava as prosperous, not having many children, long-lived, and subject to an ear ailment.", _H),
        12: _e(27, "Phaladipika reads a native with Rahu in the 12th bhava as intent on wrongdoing in secret, spending much, and subject to a water-borne ailment.", _H),
    },
    "ketu": {
        1: _e(28, "Phaladipika reads a native with Ketu in the 1st bhava as ungrateful, unhappy and tale-bearing, fallen from position and standing, of misshapen body, and keeping bad company.", ("caste",), "'Outcast' rendered as fallen from standing (caste verdict not carried)."),
        2: _e(28, "Phaladipika reads a native with Ketu in the 2nd bhava as without learning or riches, coarse in speech and sinister in look, and always eating at others' tables."),
        3: _e(29, "Phaladipika reads a native with Ketu in the 3rd bhava as given long life, strength, wealth and fame, living happily with a partner and eating well — and as losing a brother.", _G, "'Wife' rendered as partner; the loss clause kept."),
        4: _e(29, "Phaladipika reads a native with Ketu in the 4th bhava as losing lands, vehicles, mother and happiness, leaving the native country to live abroad on another's bounty."),
        5: _e(30, "Phaladipika reads a native with Ketu in the 5th bhava as suffering loss of children, stomach disease and trouble from spirits, and as becoming evil-minded and wicked.", _H),
        6: _e(30, "Phaladipika reads a native with Ketu in the 6th bhava as very magnanimous and of the best qualities, attaining lasting fame, firmness and high authority, overcoming enemies and realising every wish."),
        7: _e(31, "Phaladipika reads a native with Ketu in the 7th bhava as suffering disrespect, seeking bad company, afflicted by a bowel ailment, and suffering loss of wife and of vital power.", _G + _H, "'Bad women' rendered as bad company; the loss clause kept as the text states it."),
        8: _e(31, "Phaladipika reads a native with Ketu in the 8th bhava as short-lived, separated from dear friends, quarrelsome, injured by a weapon, and disappointed in every undertaking."),
        9: _e(32, "Phaladipika reads a native with Ketu in the 9th bhava as following a sinful course and doing unrighteous things, deprived of father, unlucky, poor, and slandering the good."),
        10: _e(32, "Phaladipika reads a native with Ketu in the 10th bhava as meeting obstacles to good acts, impure and engaged in vile acts — and as energetic, bold and widely renowned."),
        11: _e(33, "Phaladipika reads a native with Ketu in the 11th bhava as amassing money, having many good qualities, enjoying life well, commanding every means, and succeeding in obtaining all that is needed."),
        12: _e(33, "Phaladipika reads a native with Ketu in the 12th bhava as doing wrong in secret, spending on unworthy things, destroying wealth, of forbidden conduct, and subject to eye ailments.", _H),
    },
}
