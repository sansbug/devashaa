"""
Bṛhat Jātaka of Varāhamihira (~550 CE), B. Suryanarain Row tr. (1919) — CLASSICAL tier.

The Sun in the 12 rāśis (Bṛhat Jātaka ch.18, Rāśiśīlādhyāya). The 1919 translation is
public domain. Each entry is a concise site-authored, cited, adaptation-classified GIST
per docs/classical-sources-policy.md, verified against the edition and independently
checked for faithfulness, policy (§5), and non-fatalism. Varāhamihira is terse; gists stay terse.
"""
SOURCE = {
    "id": "brihat_jataka", "text": "Bṛhat Jātaka", "author": "Varāhamihira",
    "date": "~550 CE", "translator": "B. Suryanarain Row, 1919 (public domain)",
    "tier": "classical",
}

# graha key -> sign index (0=Meṣa … 11=Mīna) -> entry. Sun-in-sign complete (12/12).
SUN_IN_SIGN = {
    0: {  # Aries
        "citation": 'Bṛhat Jātaka 18.1',
        "gist": 'Bṛhat Jātaka reads a native with the Sun in Aries as renowned, clever, much-travelled, and a "bearer of arms" (glossed: a soldierly / martial vocation) — and, as the dated text states, of little wealth. In the Sun\'s deep exaltation the text raises the same signature: very famous, clever, wealthy, and a "commander of men bearing arms" (glossed: a martial leadership role).',
        "adaptation": {"classes": ['archaic', 'health'], "action": 'historicise',
                        "note": "Two martial referents are GLOSSED, not dropped: 'bearer of arms' = a soldierly/martial vocation; 'commander of men bearing arms' = a martial leadership role (§5 archaic-referent → gloss). The 'little wealth' clause is HISTORICISED — carried as the text's dated stated-effect, cited and dated, never as fate or a financial claim; it triggers the historical-context badge. Single `action` recorded as 'historicise' because that is the badge-driving, more-protective operation of the two; the gloss is spelled out here. Whole verse ships; framing attributed and non-fatalistic ('the text reads the native as…'); pronoun neutralised to 'the native'. No caste, gender/marriage, servitude, occupation-ranking, or remedy content present, so nothing omitted, refused, or neutralised."},
        "confidence": "corroborated",
    },
    1: {  # Taurus
        "citation": 'Bṛhat Jātaka 18.1',
        "gist": "Bṛhat Jātaka (18.1) reads the Sun-in-Taurus native as earning a livelihood through trade in scents and clothing, and as gifted in drumming and music. One clause — a blanket dislike of women — is refused as a value-laden gendered judgement with no structural principle to preserve. Presented as the text's ~550 CE stated reading, not as fate.",
        "adaptation": {"classes": ['occupation', 'gender'], "action": 'refuse',
                        "note": "Terse one-liner, mixed handling. Occupation clause ('sell scents and clothes') KEPT as the livelihood theme (trade in perfumes/clothing) — §5 Occupation-status says keep the theme, drop any high/low rank; the verse states no rank, so nothing to drop. Gender clause ('hate females') REFUSED under §5 Gender & marriage: a pure value-laden gendered judgement with no surviving structural principle to neutralise; shown as an explicit refusal-with-reason (cite-or-refuse). Music clause ('clever in drumming and music') is CLEAN and kept as a talent for percussion/music. No caste, servitude, death-timing, poverty, archaic-referent, or remedy content present. Framed by attribution + ~550 CE date, non-fatalistic."},
        "confidence": "corroborated",
    },
    2: {  # Gemini
        "citation": 'Bṛhat Jātaka 18.2',
        "gist": "Bṛhat Jātaka states that the Sun in Gemini makes the native educated and learned, earning a livelihood through astrology, and wealthy — given as the text's stated effect, not as the reader's fate.",
        "adaptation": {"classes": ['occupation'], "action": 'clean',
                        "note": "No caste, gender/marriage, servitude, remedy, or death-timing content. The astrologer theme is kept as a plain livelihood (livelihood via astrology); it carries no high/low ranking, so the occupation-STATUS class is not triggered and nothing is dropped, and it needs no archaic gloss (astrologer is still a recognizable calling). 'Wealthy' is a positive effect — not the negative poverty class — and ships with the standard cited, dated, non-fatalistic framing (the text's stated effect, never the reader's destiny). Nets to clean."},
        "confidence": "corroborated",
    },
    3: {  # Cancer
        "citation": 'Bṛhat Jātaka 18.2',
        "gist": "Bṛhat Jātaka reads the Sun-in-Cancer native as quick to anger and worn by fatigue from travel and other cares, labouring at others' behest — and, as the text's dated view (not fate), of poor means.",
        "adaptation": {"classes": ['health', 'slavery'], "action": 'historicise',
                        "note": "Poverty ('poor') kept as the text's dated stated-effect, not fate and not financial advice (§5 poverty → historicise; refuse is reserved for death-timing, absent here). 'Doing others' work' historicised/neutralised to status-neutral 'labouring at others' behest' — the dependent-labour theme survives, no servile rank imported (the verse names no servant/slave term). Anger and fatigue-through-travel are clean and kept plainly (no §5 class). No caste, gender, marriage, remedy, or death-timing content in this verse; nothing refused. Carry the historical-context badge for the dated poverty/dependent-labour framing."},
        "confidence": "corroborated",
    },
    4: {  # Leo
        "citation": 'Bṛhat Jātaka 18.2',
        "gist": 'Bṛhat Jātaka assigns the Sun in Leo a love of forests, mountains and cattle, and reads the native as courageous and dull-witted.',
        "adaptation": {"classes": [], "action": 'clean',
                        "note": "The one-liner triggers none of the protected classes. No caste, gender/marriage, slavery/rank, death/disease/poverty, remedy, or archaic referent. The 'cattle' reference is an affinity, not a ranked or low livelihood, so it is not an occupation-status flag. 'Courageous' and 'dull(-witted)' are gender-neutral character traits kept faithfully under 'else -> clean'. The source's fatalistic 'causes' is reframed as the text's stated reading ('Bṛhat Jātaka assigns...', 'reads the native as...'). Kept terse to match the terse source. Public-domain text, so no §4 reproduction concern either."},
        "confidence": "corroborated",
    },
    5: {  # Virgo
        "citation": 'Bṛhat Jātaka 18.2',
        "gist": 'Bṛhat Jātaka reads the Sun-in-Virgo native as skilled in writing, painting, poetry, philosophy and mathematics, and of a delicate physical form.',
        "adaptation": {"classes": ['gender'], "action": 'neutralise',
                        "note": "The skill list (writing, painting, poetry, philosophy, mathematics) is neutral, non-dated content and is kept verbatim. 'Possesses a feminine body' is the only §5-flagged element (Gender & marriage). A structural principle survives — Virgo is a feminine, Mercurial, earthy sign whose classical physical signature is a soft, delicate build — so per §5 it is neutralised: the gendered wrapper 'feminine' is dropped and the surviving structural descriptor ('a delicate physical form') is kept, rather than refused. No caste, occupation-status, slavery/rank, death/disease/poverty, remedy, or archaic-referent content is present."},
        "confidence": "corroborated",
    },
    6: {  # Libra
        "citation": 'Bṛhat Jātaka 18.3',
        "gist": 'Bṛhat Jātaka 18.3 reads the Sun in Libra as assigning the native a livelihood tied to the drink trade and to goldsmithing (metal-craft), an inclination to drink, and a traveller\'s life. Shown as the text\'s dated (~550 CE) reading, not as fate. Its "mean" moral ranking is dropped.',
        "adaptation": {"classes": ['occupation', 'archaic'], "action": 'drop-status + gloss (remainder clean)',
                        "note": "Two §5 classes apply. OCCUPATION-STATUS (drop-status): 'toddy-seller' and 'goldsmith' are kept as livelihood themes (the drink trade; goldsmithing/metal-craft) with their low/mean status ranking DROPPED, and the standalone value-word 'mean' is dropped as a moral/status verdict — the §5 occupation-status action is drop-status (keep the livelihood, drop the ranking), NOT historicise, since no death/disease/poverty content is present to keep-cited-not-fated. ARCHAIC-REFERENT (gloss): the era-specific trades are glossed in context — 'toddy' as the drink/alcohol trade, 'goldsmith' as metal-craft — kept legible without inventing modern specifics. Remainder CLEAN: 'drunkard' ships plainly as an inclination to drink (a character trait, no protected class), and 'traveller' as a traveller's/wandering life. No caste, gender/marriage, slavery/servitude/rank, death/disease/poverty, or remedy content is present, so nothing is omitted, refused, or neutralised. Framed by attribution ('the text reads…') and dated to ~550 CE, never as the reader's fate."},
        "confidence": "corroborated",
    },
    7: {  # Scorpio
        "citation": 'Bṛhat Jātaka 18.3',
        "gist": "Bṛhat Jātaka reads the Sun-in-Scorpio native as cruel, adventurous, rash, and a destroyer — skilled with weapons (martial skill in its ~6th-century context), earning a livelihood by trade in poisonous substances, and (in the text's dated view) prone to losing wealth to thieves. Presented as the text's reading of the placement, not a prediction about you.",
        "adaptation": {"classes": ['archaic', 'occupation', 'health'], "action": 'gloss (archaic weapons) + drop-status/keep-livelihood (occupation) + keep-cited-not-fated (poverty); remaining character traits clean',
                        "note": "§5 classes present: archaic-referent, occupation-status (precautionary), and the poverty sub-element of death/disease/poverty; the rest is clean. ARCHAIC (gloss): 'skilled in military weapons' kept and glossed as martial skill / weapon-handling in its ~6th-c. context, not modernised. OCCUPATION-STATUS (drop-status): 'profits by sale of poisonous substances' kept as the livelihood theme (trade in poisonous substances); the verse states no explicit high/low rank, so the status flag is precautionary and no moral ranking is implied. DEATH/DISEASE/POVERTY (keep-cited-not-fated): 'losing wealth by robbers' kept as the text's dated stated-effect, framed as the ~6th-c. reading, not as fate and not as financial advice. CLEAN, shipped plainly as the text's dated, unendorsed character (else→clean, NOT softened): 'cruel', 'adventurous', 'rash' and 'a destroyer' — none carry a policy class, so per §5 and consistent with the sister Sārāvalī-Scorpio entry (which ships 'cruel' plainly), they are retained in sense as the text's character reading rather than bowdlerised. No caste, gender/marriage, slavery/servitude, or remedy content is present in this verse, so nothing was omitted or refused; framed throughout by attribution ('the text reads…'), dated, never as the reader's fate."},
        "confidence": "corroborated",
    },
    8: {  # Sagittarius
        "citation": 'Bṛhat Jātaka 18.3',
        "gist": 'Bṛhat Jātaka reads the Sun-in-Sagittarius native as respected and wealthy, with an angry temperament, and assigns a livelihood in healing (physician) and skilled craft (artisan).',
        "adaptation": {"classes": ['archaic', 'occupation'], "action": 'gloss',
                        "note": '"Doctor" and "artisan" are archaic occupation referents, glossed in context as physician/healer and skilled craftsman; the livelihood theme is kept and no high/low status ranking is present, so nothing is dropped. "Rich" ships as the text\'s dated, attributed stated-effect (non-fatalistic), and "respected"/"angry" are neutral traits that ship clean. No caste, gender/marriage, slavery/servitude, remedy, or death-timing content is present, so nothing is omitted, neutralised, or refused.'},
        "confidence": "corroborated",
    },
    9: {  # Capricorn
        "citation": 'Bṛhat Jātaka 18.3',
        "gist": "Bṛhat Jātaka (18.3) reads the Sun-in-Capricorn native as earning a livelihood through trade, of a covetous bent inclined to enjoy at others' expense — and assigns them little wealth of their own.",
        "adaptation": {"classes": ['occupation', 'health'], "action": 'neutralise',
                        "note": "Occupation-status: dropped the status/moral ranking ('mean', 'ignorant', 'low articles') and kept the surviving structural theme, livelihood-via-trade (keep theme, drop ranking). Death/disease/poverty: 'of little wealth' retained as the text's dated stated-effect, framed as the text's reading ('reads as'/'assigns them') rather than fate, not financial advice. 'Covetous' and 'enjoying at others' cost' are character-disposition terms with no social-order claim, kept clean. No caste/gender/remedy content present. (Single action label 'neutralise' names the operative adaptation; the poverty theme is retained-as-stated rather than transformed.)"},
        "confidence": "corroborated",
    },
    10: {  # Aquarius
        "citation": 'Bṛhat Jātaka 18.4',
        "gist": 'Bṛhat Jātaka assigns the Sun in Aquarius a hard material lot: the text reads the native as separated from children and from wealth, and as poor.',
        "adaptation": {"classes": ['occupation', 'health'], "action": 'omit',
                        "note": 'The character-verdict "mean" is a bare moral/status ranking (occupation-status/rank class) with no livelihood theme underneath to retain, so it is OMITTED per §5 ("keep the theme, drop the status judgement" — here there is no theme to keep). The surviving substance — "separated from children and wealth, and poor" — is death/disease/poverty content: it is NOT omitted but retained and framed as Bṛhat Jātaka\'s DATED STATED-EFFECT via "the text reads the native as…" / "assigns…", cited and dated (~550 CE per the always-visible-date principle), never as fate, prediction, or financial advice; no death-timing is present. No caste, gender/marriage value-judgement (generic-masculine "makes a man" neutralised to "the native"), servitude, remedy, or archaic-referent content present.'},
        "confidence": "corroborated",
    },
    11: {  # Pisces
        "citation": 'Bṛhat Jātaka 18.4',
        "gist": 'Bṛhat Jātaka 18.4 assigns the Sun in Pisces wealth through articles found in water, and reads the native as cherished and fondly indulged by a partner.',
        "adaptation": {"classes": ['gender'], "action": 'neutralise',
                        "note": "'Fondled by women' neutralised to the partner-neutral 'cherished and fondly indulged by a partner' — the structural affection/indulgence principle survives, so neutralise not refuse; the gendered value-framing is dropped. 'Wealth through articles found in water' is kept as the text's dated stated-effect (water-sourced livelihood), phrased non-fatalistically ('assigns'/'reads'). The source carries no high/low status ranking, so nothing is dropped and no occupation-status adaptation applies. No caste, remedy, health, or death content."},
        "confidence": "corroborated",
    },
}
