"""Yogas registered by hand from page images, 2026-11-22: the ones the web comparison
(_reading/study/web-vs-devashaa-28.md) found popular sites using but devashaa lacking.

Each verse was read on the printed page. Nothing is blended across texts:
  * BPHS (Santhanam tr.) Vol I ch.36 vv.27-28 — Lakshmi Yoga. tier "sloka", effect quoted
    like the rest of yoga_rules.YOGAS.
  * Phaladipika (Mantresvara; V. Subrahmanya Sastri tr., 2nd ed. 1950) — tier "classical".
    Adh.6 v.57 + vv.63/65/69: Harsha, Sarala, Vimala (what web sites call "Viparita Raja
    Yoga"). Adh.7 vv.26-29: nicabhanga raja yogas. Effects are site-authored GISTS of the
    translation (as phaladipika_rules.py does), not quotations; "king" rendered as
    "authority" and "sons" as "children" (section 5).
    NOT read: Adh.7 v.30 (its English is missing from the scan's text layer and the page
    images are JBIG2, which this toolchain cannot decode). The other nine yogas of
    Adh.6 v.57 (Ava, Nisswa, Mriti, Kuhu, Pamara, Dushkriti, Nirbhagya, Duryoga, Daridra)
    sit in the same verse and are not registered yet.
  * Brhat Jataka (Varahamihira; B. Suryanarain Row tr., 1919) ch.15 stanzas 1-2 —
    Pravrajya (renunciation) yoga, tier "classical". Row's Notes are not used.
    Stanzas 3-4 (the Janma-rasi lord / Saturn routes) are not registered yet.
"""

PD = "Phaladīpikā (V. Subrahmanya Sastri tr., 2nd ed. 1950)"
BJ = "Bṛhat Jātaka (B. Suryanarain Row tr., 1919)"

_V57 = ("Adh.6 v.57 states the condition for each house in one sentence: its lord in the 6th, "
        "8th or 12th, OR the house joined or aspected by malefics. devashaa reports which of the "
        "two clauses holds. Popular sites' 'Viparita Raja Yoga' is the first clause only. "
        "Malefics here are the seven-planet set (waning Moon, Sun, Mars, Saturn, afflicted "
        "Mercury); 'aspected' is a full graha drishti. Rahu and Ketu are not counted.")

_NB_NOTE = ("Sastri's note to Adh.7 v.26: some read 'the lord of the exaltation sign' as the "
            "planet that is EXALTED in the debilitation sign. devashaa evaluates both readings, "
            "labels which one holds, and chooses neither. Kendra = whole-sign 1st/4th/7th/10th.")

EXTRA = {
    "Lakshmi Yoga": {
        "family": "other", "source": "bphs",
        "citation": "BPHS (Santhanam) Vol I, Ch.36, v.27-28 (printed p.377)",
        "effect": "The native with this yoga will be charming, virtuous, kingly in status, "
                  "endowed with many sons and abundant wealth, be famous and be of high moral merits.",
        "condition": "9th lord in a kendra, in its own, mula-trikona or exaltation sign; "
                     "the ascendant lord endowed with strength.",
        "computability": "strength_gated",
        "strength_note": "Gated on 'the ascendant lord endowed with strength' — resolved against "
                         "the Shadbala engine (lagna lord at or above its minimum).",
        "tier": "sloka"},

    "Harsha Yoga": {
        "family": "dusthana", "source": "phaladipika",
        "citation": f"{PD}, Adh.6 v.57 (condition), v.63 (effect)",
        "effect": "Phaladipika gives happiness and enjoyment, good fortune and a strong "
                  "constitution; the person overcomes opponents, shrinks from wrongdoing, is a "
                  "friend of prominent people, and has wealth, standing, friends, fame and children.",
        "condition": "6th lord in the 6th, 8th or 12th; or the 6th joined or aspected by malefics.",
        "computability": "clean", "strength_note": _V57, "tier": "classical"},
    "Sarala Yoga": {
        "family": "dusthana", "source": "phaladipika",
        "citation": f"{PD}, Adh.6 v.57 (condition), v.65 (effect)",
        "effect": "Phaladipika gives a long life, resolve and fearlessness, prosperity, learning, "
                  "children and riches; the person succeeds in what they undertake, overcomes "
                  "opponents, and is upright and widely known.",
        "condition": "8th lord in the 6th, 8th or 12th; or the 8th joined or aspected by malefics.",
        "computability": "clean", "strength_note": _V57, "tier": "classical"},
    "Vimala Yoga": {
        "family": "dusthana", "source": "phaladipika",
        "citation": f"{PD}, Adh.6 v.57 (condition), v.69 (effect)",
        "effect": "Phaladipika gives one who spends little and saves much, is good to everyone, "
                  "happy and independent, has a respectable occupation or conduct, and is known "
                  "for good qualities.",
        "condition": "12th lord in the 6th, 8th or 12th; or the 12th joined or aspected by malefics.",
        "computability": "clean", "strength_note": _V57, "tier": "classical"},

    "Nicabhanga: a lord in a kendra": {
        "family": "nicabhanga", "source": "phaladipika",
        "citation": f"{PD}, Adh.7 v.26 and v.29",
        "effect": "Phaladipika (v.26): the person rises to authority and governs justly. "
                  "(v.29, same condition): high standing with full riches, virtue, the respect "
                  "of peers, power, fame and affluence.",
        "condition": "A planet in its debilitation sign, and the lord of that sign or the lord of "
                     "the planet's exaltation sign in a kendra from the Lagn or the Moon.",
        "computability": "clean", "strength_note": _NB_NOTE, "tier": "classical"},
    "Nicabhanga: the two lords in mutual kendras": {
        "family": "nicabhanga", "source": "phaladipika",
        "citation": f"{PD}, Adh.7 v.27",
        "effect": "Phaladipika: the person reaches the highest standing, respected by others "
                  "who themselves hold authority.",
        "condition": "A planet in its debilitation sign, and the lord of that sign and the lord "
                     "of the planet's exaltation sign in kendras from each other.",
        "computability": "clean", "strength_note": _NB_NOTE, "tier": "classical"},
    "Nicabhanga: aspected by its sign's lord": {
        "family": "nicabhanga", "source": "phaladipika",
        "citation": f"{PD}, Adh.7 v.28",
        "effect": "Phaladipika: the person holds authority and is famous; the text adds there is "
                  "no doubt of it when the debilitated planet is outside the 6th, 8th and 12th.",
        "condition": "A planet in its debilitation sign, aspected by the lord of that sign.",
        "computability": "clean",
        "strength_note": "v.28's stronger form (outside the 6th/8th/12th) is reported in the detail.",
        "tier": "classical"},

    "Pravrajya Yoga": {
        "family": "pravrajya", "source": "brihat_jataka",
        "citation": f"{BJ}, ch.15 stanza 1 (printed pp.182-183), stanza 2 (pp.183-184)",
        "effect": "Brihat Jataka: four or more powerful planets in one sign incline the person to "
                  "renounce worldly life; the most powerful of them names the order followed "
                  "(Mars Sakya, Mercury Ajivika, Jupiter Bhikshu, Moon Vriddha, Venus Charaka, "
                  "Saturn Nirgrantha, Sun Vanyasana). If those planets are combust, the person "
                  "honours renunciates instead of renouncing (stanza 2).",
        "condition": "Four or more of the seven planets in one sign, powerful.",
        "computability": "strength_gated",
        "strength_note": "'Powerful' is resolved against the Shadbala engine: the yoga fructifies "
                         "when four or more of the planets in that sign are strong. Planetary war "
                         "('defeat', stanza 1) is not evaluated. Rahu and Ketu are not counted.",
        "tier": "classical"},
}
