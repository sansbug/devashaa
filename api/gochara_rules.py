"""
Gochara-phala (transit effects) from Phaladipika ch.26, transits counted FROM
THE MOON SIGN (Chandra lagna) - CLASSICAL tier, COMPLETE 9x12 grid.

Source: the ORIGINAL HINDI edition - Phaladipika (Bhavartha Bodhini), vyakhya by
Pandit Gopesh Kumar Ojha, Motilal Banarsidass, 1st ed. 1946 (complete library
scan). Extracted from Ojha's HINDI artha under each sloka (the Sanskrit itself is
never self-translated); every cell verified adversarially against the rendered
pages. `hi` gists condense Ojha's own wording; `en` gists are site renderings OF
THE HINDI, per the section-5 adaptation policy (gender-neutralised, 'raja'
glossed as authority/government, disease/poverty kept as the text's dated view).
The Sun row of the favourable table is independently corroborated by the
surviving page of the 2008 English edition (sloka 3, printed p.581 there).
"""

SOURCE = {
    "id": "phaladipika_gochara", "text": "Phaladīpikā (Bhāvārtha Bodhinī)",
    "author": "Mantreśvara",
    "date": "~13th c. CE",
    "translator": "Paṇḍit Gopesh Kumar Ojha (Hindi vyākhyā)",
    "edition": "Motilal Banarsidass, Delhi, 1st ed. 1946",
    "tier": "classical",
    "note": "English gists are site renderings of Ojha's Hindi artha; Hindi gists condense his own wording.",
}

COVERAGE_NOTE = (
    "Complete: all nine grahas x twelve houses from the Moon sign (ch.26 ślokas 2-28), "
    "with the favourable/vedha tables and the text's own vedha exemptions."
)

# graha -> favourable transit houses FROM THE MOON SIGN. Each favourable house
# maps to its vedha (obstruction) house per the text, or None where the text
# names no vedha for that graha (Rāhu/Ketu). A planet standing in the vedha house
# voids the favourable transit — counted from the Moon sign (Nārada's method, as
# Ojha adopts). vedha_exempt: the text's mutual father-son exemptions.
FAVOURABLE = {
    "sun": {
        "houses": {3: 9, 6: 12, 10: 4, 11: 5},
        "vedha_exempt": ['saturn'],
        "citation": "Phaladīpikā ch.26 śl.2 & vedha śl. (printed p.623)",
        "confidence": "corroborated",
    },
    "moon": {
        "houses": {1: 5, 3: 9, 6: 12, 7: 2, 10: 4, 11: 8},
        "vedha_exempt": ['mercury'],
        "citation": "Phaladīpikā ch.26 śl.2 & vedha śl. (printed p.624)",
        "confidence": "corroborated",
    },
    "mars": {
        "houses": {3: 12, 6: 9, 11: 5},
        "vedha_exempt": [],
        "citation": "Phaladīpikā ch.26 śl.2 & vedha śl. (printed p.624)",
        "confidence": "corroborated",
    },
    "mercury": {
        "houses": {2: 5, 4: 3, 6: 9, 8: 1, 10: 8, 11: 12},
        "vedha_exempt": ['moon'],
        "citation": "Phaladīpikā ch.26 śl.2 & vedha śl. (printed p.625)",
        "confidence": "corroborated",
    },
    "jupiter": {
        "houses": {2: 12, 5: 4, 7: 3, 9: 10, 11: 8},
        "vedha_exempt": [],
        "citation": "Phaladīpikā ch.26 śl.2 & vedha śl. (printed p.625)",
        "confidence": "corroborated",
    },
    "venus": {
        "houses": {1: 8, 2: 7, 3: 1, 4: 10, 5: 9, 8: 5, 9: 11, 11: 3, 12: 6},
        "vedha_exempt": [],
        "citation": "Phaladīpikā ch.26 śl.2 & vedha śl. (printed p.625)",
        "confidence": "corroborated",
    },
    "saturn": {
        "houses": {3: 12, 6: 9, 11: 5},
        "vedha_exempt": ['sun'],
        "citation": "Phaladīpikā ch.26 śl.2 & vedha śl. (printed p.624)",
        "confidence": "corroborated",
    },
    "rahu": {
        "houses": {3: None, 6: None, 10: None, 11: None},
        "vedha_exempt": [],
        "citation": "Phaladīpikā ch.26 śl.2 (printed p.621)",
        "confidence": "corroborated",
    },
    "ketu": {
        "houses": {3: None, 6: None, 10: None, 11: None},
        "vedha_exempt": [],
        "citation": "Phaladīpikā ch.26 śl.2 (printed p.621)",
        "confidence": "corroborated",
    },
}

# graha -> house-from-Moon (1-12) -> the text's transit effect for that station.
# en renders Ojha's Hindi; hi condenses Ojha's own wording. Cited per cell.
PHALA = {
    "sun": {
        1: {
            "en": "Brings toil and fatigue; money gets spent; anger arises when circumstances run against the mind; causes travel — or, if no journey occurs, much moving about in one's own place.",
            "hi": "श्रम कराता है, धन खर्च होता है; मन के प्रतिकूल परिस्थिति होने से क्रोध आता है; यात्रा कराता है, या यात्रा न हो तो अपने ही स्थान में खूब चलना पड़ता है।",
            "citation": "Phaladīpikā ch.26 śl.9 (printed p.626)",
            "confidence": "clear",
        },
        2: {
            "en": "Loss of wealth and no comfort; the person turns obstinate, and others get their work done from him by deception.",
            "hi": "धन का नाश, सुख नहीं होता; मनुष्य ज़िद्दी हो जाता है और लोग उसे धोखा देकर उससे काम निकालते हैं।",
            "citation": "Phaladīpikā ch.26 śl.9 (printed p.626)",
            "confidence": "clear",
        },
        3: {
            "en": "Gain of position; joy from accumulating wealth; good news arrives or gladdening auspicious works take place; destruction of enemies and victory over them.",
            "hi": "स्थान-प्राप्ति; धन-संग्रह से हर्ष; शुभ समाचार मिलें या हर्ष उत्पन्न करने वाले शुभ कार्य हों; शत्रुओं का नाश और उन पर विजय।",
            "citation": "Phaladīpikā ch.26 śl.9 (printed p.626)",
            "confidence": "clear",
        },
        4: {
            "en": "Illness arises; obstruction in undertakings that bring happiness.",
            "hi": "रोग उत्पन्न हो; सुख के कार्यों में बाधा हो।",
            "citation": "Phaladīpikā ch.26 śl.9 (printed p.626)",
            "confidence": "clear",
        },
        5: {
            "en": "Agitation of mind; illness, and mental distress arising from infatuation and the like.",
            "hi": "मन में क्षोभ हो; रोग तथा मोह आदि के कारण मानसिक विकलता।",
            "citation": "Phaladīpikā ch.26 śl.10 (printed p.626)",
            "confidence": "clear",
        },
        6: {
            "en": "Diseases are destroyed and enemies are conquered; the states that breed grief, delusion and mental distress are dispelled — the mind remains healthy.",
            "hi": "रोगों का नाश हो, शत्रुओं पर विजय हो; शोक, मोह या मानसिक विकलता उत्पन्न करने वाले भावों का नाश हो — अर्थात् चित्त स्वस्थ रहे।",
            "citation": "Phaladīpikā ch.26 śl.10 (printed p.626)",
            "confidence": "clear",
        },
        7: {
            "en": "Wearisome travel on the road; pain in the belly or anus (piles and the like); abasement — loss of honour and want of respect cause the mind to experience anguish.",
            "hi": "रास्ता चलना पड़े; पेट में या गुदा में (बवासीर आदि) पीड़ा हो; दीनता-हीनता — सम्मान की हानि और आदर की कमी के कारण मन में क्लेश का अनुभव हो।",
            "citation": "Phaladīpikā ch.26 śl.10 (printed p.626)",
            "confidence": "clear",
        },
        8: {
            "en": "Produces illness and fear; mental burning (anxiety); quarrels — fights and disputes; fear of authority (the text's 'raja' — government or the official class) and apprehension of their displeasure.",
            "hi": "रोग और भय उत्पन्न करे; मन में ताप (चिन्ता); कलह — लड़ाई, झगड़ा, विवाद; राजा या सरकार, अधिकारी वर्ग से भय और उनकी नाराज़गी का अन्देशा।",
            "citation": "Phaladīpikā ch.26 śl.10 (printed p.627)",
            "confidence": "clear",
        },
        9: {
            "en": "Calamity and abasement; separation from one's dear ones; failure in whatever efforts are undertaken.",
            "hi": "आपत्ति, दीनता; अपने प्रिय लोगों से विरह; जो उद्योग किये जावें उनमें असफलता।",
            "citation": "Phaladīpikā ch.26 śl.11 (printed p.627)",
            "confidence": "clear",
        },
        10: {
            "en": "Success in the work one is striving to accomplish; if some big undertaking has been taken up, it is carried to completion.",
            "hi": "जिस कार्य की सिद्धि के लिये काम कर रहे हों उसमें सफलता; कोई बड़ा कार्य उठाया गया हो तो वह पूरा हो।",
            "citation": "Phaladīpikā ch.26 śl.11 (printed p.627)",
            "confidence": "clear",
        },
        11: {
            "en": "Gain of position, increase of honour, gain of money, release from illness; financial and bodily well-being.",
            "hi": "स्थान-प्राप्ति, सम्मान-वृद्धि, द्रव्य-लाभ, रोग से छुटकारा; आर्थिक तथा शारीरिक स्वास्थ्य।",
            "citation": "Phaladīpikā ch.26 śl.11 (printed p.627)",
            "confidence": "clear",
        },
        12: {
            "en": "Distress; squandering of wealth; fever and other illness; friends turn hostile.",
            "hi": "क्लेश; धन की बर्बादी; ज्वर आदि रोग; दोस्त दुश्मनी करें।",
            "citation": "Phaladīpikā ch.26 śl.11 (printed p.627)",
            "confidence": "clear",
        },
    },
    "moon": {
        1: {
            "en": "Rise of fortune — when the transiting Moon is in the natal Moon sign itself, fortune dawns.",
            "hi": "भाग्योदय — जन्मकालीन चन्द्र राशि में ही गोचर का चन्द्र हो तो भाग्योदय होता है।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
        2: {
            "en": "Loss of wealth.",
            "hi": "धनहानि।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
        3: {
            "en": "Victory.",
            "hi": "जय।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
        4: {
            "en": "Fear — when the transiting Moon reaches the fourth sign from the natal Moon sign, fear arises.",
            "hi": "भय — जन्मकालीन चन्द्र राशि से चौथी राशि में गोचर का चन्द्र आये तब भय।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
        5: {
            "en": "Grief.",
            "hi": "शोक।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
        6: {
            "en": "Freedom from disease.",
            "hi": "अरोगता।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
        7: {
            "en": "Happiness and comfort.",
            "hi": "सुख।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
        8: {
            "en": "Unfavourable results.",
            "hi": "अनिष्ट फल।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
        9: {
            "en": "Illness.",
            "hi": "रोग।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
        10: {
            "en": "Accomplishment of what is desired — success in one's work.",
            "hi": "इष्ट-सिद्धि — कार्य में सफलता।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
        11: {
            "en": "Gladness and cheer.",
            "hi": "प्रसन्नता।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
        12: {
            "en": "Expenditure.",
            "hi": "व्यय।",
            "citation": "Phaladīpikā ch.26 śl.12 (printed p.630)",
            "confidence": "clear",
        },
    },
    "mars": {
        1: {
            "en": "Inner grief — the mind stays sorrowful or anxious within itself; separation from one's family members; blood-related illness or bile-born pain; fever or other heat-producing ailments.",
            "hi": "अन्तःशोक — मन के भीतर ही भीतर शोकाकुल या चिन्तायुक्त रहना; अपने कुटुम्बियों से वियोग; रक्त सम्बन्धी रोग या पित्त-जनित पीड़ा; ज्वर या अन्य उष्णता उत्पन्न करने वाले रोग।",
            "citation": "Phaladīpikā ch.26 śl.13 (printed p.631)",
            "confidence": "clear",
        },
        2: {
            "en": "Fear, loss of wealth, and harshness of speech (bitter words, quarrels).",
            "hi": "भय, धनहानि, वाक्-पारुष्य (कठोर वाणी, झगड़ा)।",
            "citation": "Phaladīpikā ch.26 śl.13 (printed p.632)",
            "confidence": "clear",
        },
        3: {
            "en": "Victory, success, gain of wealth, and joy.",
            "hi": "जय, सफलता, धन-प्राप्ति, आनन्द।",
            "citation": "Phaladīpikā ch.26 śl.13 (printed p.632)",
            "confidence": "clear",
        },
        4: {
            "en": "Displacement from one's position (loss of place or job), illness, stomach ailments, and sorrow on account of relatives.",
            "hi": "स्थान-भ्रंश (जगह या नौकरी छूट जाय), रोग, पेट की बीमारी, तथा बन्धुओं के कारण दुःख।",
            "citation": "Phaladīpikā ch.26 śl.13 (printed p.632)",
            "confidence": "clear",
        },
        5: {
            "en": "Fever, worry without cause, trouble concerning children, agitation, and quarrels with one's own people.",
            "hi": "ज्वर, बिना कारण चिन्ता, सन्तति-कष्ट, उद्वेग, अपने लोगों से कलह।",
            "citation": "Phaladīpikā ch.26 śl.14 (printed p.632)",
            "confidence": "clear",
        },
        6: {
            "en": "End of strife with enemies (victory over them or a settlement), relief from illness, victory, gain of wealth, and favourable success in all undertakings.",
            "hi": "शत्रुओं से कलह की निवृत्ति (उन पर विजय या समझौता), रोग-शान्ति, विजय, धन-प्राप्ति तथा सब कामों में अनुकूलता (सफलता)।",
            "citation": "Phaladīpikā ch.26 śl.14 (printed p.632)",
            "confidence": "clear",
        },
        7: {
            "en": "Quarrel with one's spouse (text: wife), eye disease, and abdominal illness.",
            "hi": "अपनी स्त्री से कलह, नेत्र-रोग, उदर-रोग।",
            "citation": "Phaladīpikā ch.26 śl.15 (printed p.632)",
            "confidence": "clear",
        },
        8: {
            "en": "Fever, pain from injury or wounds, loss of wealth, and loss of honour.",
            "hi": "ज्वर, चोट या घाव से पीड़ा, धन-नाश, मान-नाश।",
            "citation": "Phaladīpikā ch.26 śl.15 (printed p.632)",
            "confidence": "clear",
        },
        9: {
            "en": "Humiliation or defeat, loss of money, bodily weakness, signs of debility such as a slowed gait, and depletion of the body's vital constituents.",
            "hi": "दीनता या पराजय, अर्थनाश, शरीर में निर्बलता, विलम्ब से चलना आदि अशक्तता के लक्षण, धातु-क्षय आदि।",
            "citation": "Phaladīpikā ch.26 śl.15 (printed p.632)",
            "confidence": "clear",
        },
        10: {
            "en": "Failure or obstacles in work, hard toil, and misdirected effort (doing what ought not to be done, or loss from whatever work is undertaken).",
            "hi": "कार्य में असफलता या विघ्न, परिश्रम, दुश्चेष्टा (ऐसा कार्य जो नहीं करना चाहिये, अथवा जो कार्य किया जाय उससे हानि)।",
            "citation": "Phaladīpikā ch.26 śl.16 (printed p.632)",
            "confidence": "clear",
        },
        11: {
            "en": "Gain of money, good health, gains in land and property, and other auspicious results.",
            "hi": "द्रव्य-लाभ, आरोग्य, जमीन-जायदाद में लाभ आदि शुभ फल।",
            "citation": "Phaladīpikā ch.26 śl.16 (printed p.632)",
            "confidence": "clear",
        },
        12: {
            "en": "Loss of wealth, various illnesses from heat or fever, worry, and agitation.",
            "hi": "धन-नाश, उष्णता या ताप से विविध रोग, चिन्ता, उद्वेग आदि।",
            "citation": "Phaladīpikā ch.26 śl.16 (printed p.632)",
            "confidence": "clear",
        },
    },
    "mercury": {
        1: {
            "en": "Loss of wealth.",
            "hi": "धन-हानि।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
        2: {
            "en": "Gain of wealth.",
            "hi": "धन-लाभ।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
        3: {
            "en": "Fear from enemies.",
            "hi": "शत्रुओं से भय।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
        4: {
            "en": "Acquisition of wealth.",
            "hi": "धन-प्राप्ति।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
        5: {
            "en": "Quarrels with one's spouse (text: wife) and children.",
            "hi": "अपने स्त्री-पुत्रों से कलह।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
        6: {
            "en": "Victory.",
            "hi": "विजय।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
        7: {
            "en": "Opposition and quarrels.",
            "hi": "विरोध, झगड़ा।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
        8: {
            "en": "Happiness through a child, and gain of wealth.",
            "hi": "पुत्र से खुशी, धन-लाभ।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
        9: {
            "en": "Obstacles.",
            "hi": "विघ्न।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
        10: {
            "en": "Happiness of every kind.",
            "hi": "सब प्रकार से सुख।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
        11: {
            "en": "Increase of wealth and gains.",
            "hi": "धनवृद्धि, लाभ।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
        12: {
            "en": "Defeat and humiliation.",
            "hi": "पराजय, दीनता।",
            "citation": "Phaladīpikā ch.26 śl.17 (printed p.633)",
            "confidence": "clear",
        },
    },
    "jupiter": {
        1: {
            "en": "Leaving one's country or home place; very heavy expenditure or loss of wealth; enmity — adverse results.",
            "hi": "देश या अपने स्थान से बाहर जाना, धन का अत्यन्त व्यय या नाश, शत्रुता आदि अनिष्ट फल।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
        2: {
            "en": "Gain of wealth; family happiness; one's speech bears the desired fruit — people listen attentively, or wealth comes through one's own words.",
            "hi": "धन प्राप्ति, कुटुम्ब सुख, अपनी वाणी का इष्ट फल — लोग उसकी बात ध्यान से सुनें या वाणी द्वारा धन प्राप्त हो।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
        3: {
            "en": "Loss of position — one's place is lost or one's material/social standing suffers a setback; separation from dear ones; obstacles in work; illness — bad results.",
            "hi": "स्थिति-नाश — जगह या स्थान छूटे, आर्थिक या सामाजिक स्थिति में अंतर आये; इष्ट जनों से वियोग, कार्य में विघ्न, रोग आदि दुष्ट फल।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
        4: {
            "en": "Sorrow through relatives; wretchedness; danger from quadrupeds (animals).",
            "hi": "बन्धुओं से दुःख, दीनता, चौपायों से भय।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
        5: {
            "en": "Birth of a child; happiness from children; the company of good people; favour of the ruler (i.e. those in authority) — auspicious results.",
            "hi": "पुत्र की उत्पत्ति, सन्तान सुख, सज्जनों से समागम, राजा की कृपा आदि शुभ फल।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
        6: {
            "en": "Trouble from co-heirs and kinsmen (cousins and the like) and from enemies; illness — inauspicious results.",
            "hi": "अपने दायादों (चचेरे भाई आदि) तथा शत्रुओं से पीड़ा, रोग आदि अशुभ फल।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
        7: {
            "en": "A journey for some auspicious purpose; happiness with one's spouse; gain of a child — auspicious results.",
            "hi": "किसी शुभ कार्य से यात्रा, अपनी स्त्री से सुख, पुत्र प्राप्ति आदि शुभ फल।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
        8: {
            "en": "Hardship on the road — toil and fatigue from travel; loss of wealth; sufferings of various kinds — inauspicious.",
            "hi": "मार्ग-क्लेश — यात्रा से परिश्रम, अशुभ फल, धन नाश, विविध प्रकार के कष्ट।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
        9: {
            "en": "All-round good fortune and accomplishment — rise of fortune; success in undertakings — auspicious results.",
            "hi": "सर्व सौभाग्य, सिद्धि — भाग्योदय, कार्य में सफलता आदि शुभ फल।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
        10: {
            "en": "Distress over wealth and over position (a reduction in one's job or office, or a dent in one's honour); trouble to one's children — inauspicious results.",
            "hi": "धन कष्ट, स्थान कष्ट (नौकरी या ओहदे में कमी या सम्मान में बट्टा), संतान पीड़ा आदि अशुभ फल।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
        11: {
            "en": "Gain of a child; gain of position (a new place or office is obtained, or one's standing rises where one already is); growth of honour — auspicious results.",
            "hi": "पुत्र लाभ, स्थान लाभ (नयी जगह या ओहदा मिले, या अपनी ही जगह में इज्जत बढ़े), सम्मान वृद्धि आदि शुभ फल।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
        12: {
            "en": "Grief concerning money; fear, anxiety and agitation — inauspicious results.",
            "hi": "द्रव्य सम्बन्धी दुःख, भय, चिन्ता, उद्वेग आदि अशुभ फल।",
            "citation": "Phaladīpikā ch.26 śl.18-20 (printed p.634)",
            "confidence": "clear",
        },
    },
    "venus": {
        1: {
            "en": "Enjoyments and comforts of every kind.",
            "hi": "सब प्रकार का भोग।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.634)",
            "confidence": "clear",
        },
        2: {
            "en": "Inflow of wealth.",
            "hi": "धनागम।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.634)",
            "confidence": "clear",
        },
        3: {
            "en": "Increase of wealth; gain of fine articles and equipment.",
            "hi": "धन वृद्धि, सुन्दर उपकरण आदि का लाभ।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.635)",
            "confidence": "clear",
        },
        4: {
            "en": "Happiness; an increase of friends.",
            "hi": "सुख, मित्रों में वृद्धि।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.635)",
            "confidence": "clear",
        },
        5: {
            "en": "Gain of a child; happiness from children.",
            "hi": "पुत्र प्राप्ति, सन्तान सुख।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.635)",
            "confidence": "clear",
        },
        6: {
            "en": "Adversity and suffering.",
            "hi": "विपत्ति, कष्ट।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.635)",
            "confidence": "clear",
        },
        7: {
            "en": "Trouble on account of the spouse.",
            "hi": "स्त्री के कारण पीड़ा।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.635)",
            "confidence": "clear",
        },
        8: {
            "en": "Acquisition of property and wealth.",
            "hi": "सम्पत्ति।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.635)",
            "confidence": "clear",
        },
        9: {
            "en": "Attainment of happiness.",
            "hi": "सुख प्राप्ति।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.635)",
            "confidence": "clear",
        },
        10: {
            "en": "Quarrels.",
            "hi": "कलह।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.635)",
            "confidence": "clear",
        },
        11: {
            "en": "Fear.",
            "hi": "भय।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.635)",
            "confidence": "clear",
        },
        12: {
            "en": "Gain of money — auspicious results.",
            "hi": "अर्थप्राप्ति आदि शुभ फल।",
            "citation": "Phaladīpikā ch.26 śl.21 (printed p.635)",
            "confidence": "clear",
        },
    },
    "saturn": {
        1: {
            "en": "Saturn transiting the Moon sign itself brings illness, and inauspicious results such as ritual impurity (ashaucha) occasioned by a death in one's circle.",
            "hi": "जन्मकालीन चन्द्र राशि में ही गोचर से शनि भ्रमण करें तो रोग, तथा किसी की मृत्यु के कारण अशौच आदि अशुभ फल होते हैं।",
            "citation": "Phaladīpikā ch.26 śl.22 (printed p.635)",
            "confidence": "clear",
        },
        2: {
            "en": "In the 2nd from the Moon sign: trouble concerning children and loss of wealth — inauspicious results.",
            "hi": "जन्म राशि से द्वितीय शनि हों तो संतान कष्ट, धन नाश आदि अशुभ फल होते हैं।",
            "citation": "Phaladīpikā ch.26 śl.22 (printed p.635)",
            "confidence": "clear",
        },
        3: {
            "en": "In the 3rd: gain of position (a new place or new employment), livelihood, authority of one's own, having many subordinates, and gain of wealth — favourable results.",
            "hi": "तृतीय शनि हों तो स्थान लाभ (नयी जगह या नौकरी की प्राप्ति) या रोजगार, अपनी हुकूमत, बहुत से नौकरों का होना, धन लाभ आदि शुभ फल होते हैं।",
            "citation": "Phaladīpikā ch.26 śl.22 (printed p.636)",
            "confidence": "clear",
        },
        4: {
            "en": "In the 4th, unfavourable: loss of wealth; loss of, or quarrels with, the spouse; and trouble from relatives or on their account.",
            "hi": "चौथे शनि अशुभ फलकारक हैं — धन नाश, स्त्री नाश (या स्त्री से कलह), बन्धुओं से या उनके कारण कष्ट आदि।",
            "citation": "Phaladīpikā ch.26 śl.22 (printed p.636)",
            "confidence": "clear",
        },
        5: {
            "en": "In the 5th: shortage or outright loss of money; trouble regarding children; and impaired judgment — no peace of mind, with restlessness from all manner of worries and agitation.",
            "hi": "पंचम शनि हों तो धन की कमी या घाटा लगे; सन्तान कष्ट; बुद्धिनाश — मन में शांति न रहे, नाना प्रकार की चिन्ताओं तथा उद्वेगों से अशांति रहे।",
            "citation": "Phaladīpikā ch.26 śl.22 (printed p.636)",
            "confidence": "clear",
        },
        6: {
            "en": "In the 6th Saturn gives favourable results: every kind of comfort, and victory over enemies.",
            "hi": "छठे शनि शुभ फल देते हैं — सब प्रकार का सुख, शत्रुओं पर विजय आदि शुभ फल होते हैं।",
            "citation": "Phaladīpikā ch.26 śl.22 (printed p.636)",
            "confidence": "clear",
        },
        7: {
            "en": "In the 7th, afflicting: suffering concerning the spouse (their illness, or quarrels with them), many kinds of fear, and futile, painful journeys.",
            "hi": "सप्तम शनि पीड़ाकारक होते हैं — स्त्री कष्ट (स्त्री को रोग या उससे कलह), अनेक प्रकार का भय, व्यर्थ की कष्टप्रद यात्राएँ।",
            "citation": "Phaladīpikā ch.26 śl.22 (printed p.636)",
            "confidence": "clear",
        },
        8: {
            "en": "In the 8th, wholly inauspicious: loss of or suffering through children; severe distress concerning animals, friends and money — friends are lost, animals die, wealth suffers marked loss; anxiety over health arises, with particular bodily suffering from a painful disease (the text's own dated stated-effects).",
            "hi": "अष्टम शनि पूर्ण अशुभ फल देते हैं — संतान नाश या कष्ट; पशु, मित्र, धन आदि के कारण घोर पीड़ा; मित्र नष्ट हों, पशु मरें, धन की विशेष हानि; स्वास्थ्य की चिन्ता तथा किसी पीड़ाकारक रोग से विशेष शरीर कष्ट।",
            "citation": "Phaladīpikā ch.26 śl.22 (printed p.636)",
            "confidence": "clear",
        },
        9: {
            "en": "In the 9th it makes for poverty; obstacles arise in religious works; an elder who stands in a father's place (a teacher or an uncle) dies, and some cause of sorrow keeps persisting (the text's own dated stated-effects).",
            "hi": "नवें शनि दरिद्रता कारक होते हैं; धर्म कार्य में विघ्न; पिता के समान किसी श्रेष्ठ व्यक्ति (गुरु, चाचा, मामा आदि) की मृत्यु होती है और कुछ-न-कुछ दुःख का कारण बना रहता है।",
            "citation": "Phaladīpikā ch.26 śl.23 (printed p.636)",
            "confidence": "clear",
        },
        10: {
            "en": "In the 10th: loss of honour and standing; a particularly painful illness; involvement in a venture that meets failure and loss, or a wrong act comes about that brings disgrace.",
            "hi": "दशम शनि हों तो सम्मान भंग (इज्जत में बट्टा लगे); कोई विशेष पीड़ाकारक रोग हो; ऐसे व्यापार (कार्य) में प्रवृत्ति हो जिसमें असफलता व घाटा हो, या ऐसा दुष्ट कर्म बन आवे जिससे अप्रतिष्ठा हो।",
            "citation": "Phaladīpikā ch.26 śl.23 (printed p.636)",
            "confidence": "clear",
        },
        11: {
            "en": "Transiting the 11th, Saturn is favourable: every kind of happiness and excellent renown.",
            "hi": "एकादश स्थान में शनि भ्रमण करें तो शुभ फलकारक — सब प्रकार के सुख, उत्कृष्ट कीर्ति आदि शुभ फल होते हैं।",
            "citation": "Phaladīpikā ch.26 śl.23 (printed p.636)",
            "confidence": "clear",
        },
        12: {
            "en": "In the 12th: fruitless toil from staying engaged in useless undertakings — effort yields only hardship since success does not come; loss of wealth through enemies; and illness afflicts spouse and children.",
            "hi": "बारहवें शनि हों तो वृथा कार्यों में लगे रहने से व्यर्थ का परिश्रम — उद्योग में सिद्धि या सफलता न मिलने से केवल कष्ट प्राप्ति; शत्रुओं द्वारा धन नाश; स्त्री और पुत्रों को रोग-पीड़ा होती है।",
            "citation": "Phaladīpikā ch.26 śl.23 (printed p.637)",
            "confidence": "clear",
        },
    },
    "rahu": {
        1: {
            "en": "Illness, and decline of bodily strength.",
            "hi": "बीमारी, शारीरिक शक्ति का क्षय।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
        2: {
            "en": "Loss of wealth.",
            "hi": "धन नाश।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
        3: {
            "en": "Happiness.",
            "hi": "सुख।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
        4: {
            "en": "Sorrow.",
            "hi": "दुःख।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
        5: {
            "en": "Loss of wealth.",
            "hi": "धन नाश।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
        6: {
            "en": "Happiness.",
            "hi": "सुख।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
        7: {
            "en": "Loss and ruin (the Hindi gives the single word 'nash').",
            "hi": "नाश।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
        8: {
            "en": "Suffering as severe as death (the text's own dated stated-effect).",
            "hi": "मृत्यु तुल्य कष्ट।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
        9: {
            "en": "Loss.",
            "hi": "हानि।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
        10: {
            "en": "Gain.",
            "hi": "लाभ।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
        11: {
            "en": "Good fortune.",
            "hi": "सौभाग्य।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
        12: {
            "en": "Expenditure.",
            "hi": "व्यय।",
            "citation": "Phaladīpikā ch.26 śl.24 (printed p.637)",
            "confidence": "clear",
        },
    },
    "ketu": {
        1: {
            "en": "Loss, and fear of disease.",
            "hi": "हानि, रोगभय।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.639)",
            "confidence": "clear",
        },
        2: {
            "en": "Enmity, and loss of wealth.",
            "hi": "वैर, वित्तनाश।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.639)",
            "confidence": "clear",
        },
        3: {
            "en": "Gain of happiness, and increase (prosperity).",
            "hi": "सुखलाभ, वृद्धि।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.639)",
            "confidence": "clear",
        },
        4: {
            "en": "Fear, and affliction.",
            "hi": "भीति, पीड़ा।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.639)",
            "confidence": "clear",
        },
        5: {
            "en": "Grief, and loss of money.",
            "hi": "शोक, अर्थनाश।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.639)",
            "confidence": "clear",
        },
        6: {
            "en": "Happiness, and bestowal of wealth.",
            "hi": "सुख, वित्तद (धन देने वाला)।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.639)",
            "confidence": "ocr-partial",
        },
        7: {
            "en": "Misfortune, and affliction.",
            "hi": "दुर्गति, पीड़ा च।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.639)",
            "confidence": "clear",
        },
        8: {
            "en": "Fear of affliction, and loss.",
            "hi": "पीड़ाभय, हानिश्च।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.640)",
            "confidence": "clear",
        },
        9: {
            "en": "Sinful inclination, and wretchedness (want).",
            "hi": "पाप, दैन्य च।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.640)",
            "confidence": "clear",
        },
        10: {
            "en": "Fear, and grief.",
            "hi": "भय, शोकश्च।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.640)",
            "confidence": "clear",
        },
        11: {
            "en": "Good renown, and gain of wealth.",
            "hi": "सुयश, अर्थलाभ।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.640)",
            "confidence": "clear",
        },
        12: {
            "en": "Affliction, and enmity.",
            "hi": "पीड़ा, वैरं च।",
            "citation": "Phaladīpikā ch.26 śl.commentary (printed p.640)",
            "confidence": "clear",
        },
    },
}


def transit_judgment(graha: str, house_from_moon: int, occupants_from_moon) -> dict | None:
    """The cited ch.26 judgment + per-house phala for ``graha`` transiting
    ``house_from_moon`` from the natal Moon. ``occupants_from_moon`` maps
    house-from-Moon (1-12) -> transiting graha keys standing there (vedha check).
    Returns None when the text does not cover the graha (cite-or-refuse)."""
    fav = FAVOURABLE.get(graha)
    cell = PHALA.get(graha, {}).get(house_from_moon)
    if not fav and not cell:
        return None
    out = {"tier": "classical"}
    if cell:
        out["phala"] = {"en": cell["en"], "hi": cell["hi"], "citation": cell["citation"],
                        "confidence": cell["confidence"]}
    if not fav:
        return out
    if house_from_moon not in fav["houses"]:
        out.update({"status": "not-favourable", "citation": fav["citation"]})
        return out
    vedha_house = fav["houses"][house_from_moon]
    if vedha_house is None:
        out.update({"status": "favourable", "citation": fav["citation"]})
        return out
    blockers = [g for g in (occupants_from_moon.get(vedha_house) or [])
                if g not in fav["vedha_exempt"] and g != graha]
    if blockers:
        out.update({"status": "obstructed", "vedhaHouse": vedha_house,
                    "blockers": blockers, "citation": fav["citation"]})
    else:
        out.update({"status": "favourable", "vedhaHouse": vedha_house,
                    "citation": fav["citation"]})
    return out


# Back-compat shim for the earlier Sun-only wiring.
def sun_transit_judgment(house_from_moon: int, occupants_from_moon) -> dict | None:
    return transit_judgment("sun", house_from_moon, occupants_from_moon)
