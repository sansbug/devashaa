/**
 * The ceremony scripts — every pūjā explained before it is chanted.
 *
 * Purpose first, then the steps. Each step carries the mantra (Devanāgarī and
 * transliteration, where a fixed one is chanted), WHAT IS HAPPENING, WHY, and
 * for the detailed mode what the family does and where the mantra comes from.
 * The same script drives three things: the step-by-step on a ceremony's page,
 * the self-guided mode (an AI voice explains; the device can read the mantra
 * as a pronunciation aid), and the follow-along panel in the live room, where
 * the pandit chants and moves everyone's screen to the step he is on.
 *
 * THREE MODES of explanation: 'detailed' (what · why · what you do · origin),
 * 'short' (what · why), 'none' (the mantra alone).
 *
 * WHAT THIS IS NOT. The explanations say what a step is and why it is done.
 * They are NOT word-for-word translations of the Sanskrit: this project does
 * not translate Sanskrit itself (see CLAUDE.md) — a literal meaning belongs to
 * a published translation or to the pandit, and can be added per mantra in
 * `meaning` with its source. Rites differ by region and family; the pandit's
 * own order of steps always stands above this outline.
 *
 * Mantras included are the commonly chanted ones whose text is settled.
 * Long recitations (the kathā, the Rudra, the Saptaśatī, the Sundarakāṇḍa)
 * are named, not reproduced — the pandit recites them.
 */

import { CHALISA_STEPS, CHALISA_ORDER, CHALISA_ABOUT } from './chalisa.js'

/** The fuller purpose of each ceremony — read out first, before any chanting. */
export const ABOUT = {
  satyanarayan: {
    en: 'Satyanārāyaṇa is Viṣṇu worshipped as truth itself — satya. The pūjā is followed by a kathā in five chapters, traditionally told as part of the Skanda Purāṇa, about people who kept this vow and people who forgot it. Families keep it on Pūrṇimā or Ekādaśī, and after a wedding, a birth, a new home or a new job: in thanks for what has come, and as a promise to live truthfully. Its heart is simple — the household sits together, listens, and shares the prasāda with everyone who comes.',
    hi: 'सत्यनारायण भगवान विष्णु का वह रूप हैं जिनकी पूजा स्वयं सत्य के रूप में होती है। पूजन के बाद पाँच अध्यायों की कथा होती है, जो परंपरा से स्कंद पुराण की मानी जाती है — उन लोगों की जिन्होंने यह व्रत रखा और जो इसे भूल गए। परिवार इसे पूर्णिमा या एकादशी पर, और विवाह, संतान-जन्म, नए घर या नए कार्य के बाद रखते हैं: जो मिला उसकी कृतज्ञता में, और सत्य से जीने के संकल्प के रूप में। इसका सार सरल है — घर के सब साथ बैठते हैं, कथा सुनते हैं, और प्रसाद हर आने वाले के साथ बाँटते हैं।',
  },
  ganesh: {
    en: 'Gaṇeśa, the son of Śiva and Pārvatī, is honoured first in every rite as Vighneśvara, the lord who places and removes obstacles. No ceremony, journey or new work traditionally begins without calling on him. This pūjā is his own: he is invited, offered dūrvā grass and the modaka he is fond of, and praised by his names. It is kept at the start of any undertaking, every month on Caturthī, and above all on Gaṇeśa Caturthī.',
    hi: 'शिव-पार्वती के पुत्र गणेश जी हर अनुष्ठान में सबसे पहले पूजे जाते हैं — विघ्नेश्वर के रूप में, जो विघ्न रखते भी हैं और हरते भी हैं। परंपरा में कोई भी अनुष्ठान, यात्रा या नया कार्य उन्हें स्मरण किए बिना आरंभ नहीं होता। यह पूजा उन्हीं की है: उनका आवाहन होता है, उन्हें प्रिय दूर्वा और मोदक अर्पित किए जाते हैं, और उनके नामों से स्तुति होती है। यह किसी भी कार्य के आरंभ में, हर माह चतुर्थी पर, और विशेषकर गणेश चतुर्थी पर की जाती है।',
  },
  lakshmi: {
    en: 'Lakṣmī is the goddess of prosperity, good fortune and well-being, the consort of Viṣṇu. On the new-moon night of Dīpāvalī the home is cleaned and filled with lamps to welcome her, and she is worshipped together with Gaṇeśa in the first hours after sunset. It is the household’s way of giving thanks for what it has and asking that its wealth be rightly earned and rightly used; traders traditionally open their new account books before her on this night.',
    hi: 'लक्ष्मी जी समृद्धि, सौभाग्य और कल्याण की देवी हैं, भगवान विष्णु की अर्धांगिनी। दीपावली की अमावस्या की रात घर स्वच्छ कर दीपों से सजाया जाता है ताकि उनका स्वागत हो, और सूर्यास्त के बाद के पहले पहर में गणेश जी सहित उनकी पूजा होती है। यह गृहस्थ का अपने पास जो है उसके लिए धन्यवाद देने का, और यह माँगने का ढंग है कि उसका धन धर्म से कमाया और धर्म से लगाया जाए; व्यापारी परंपरा से इसी रात नए बही-खाते उनके सामने खोलते हैं।',
  },
  'griha-pravesh': {
    en: 'A home is treated as a living place with a presiding deity of its own, the Vāstu Puruṣa. Before a family lives in a new house it enters at a chosen hour carrying a kalaśa, worships Gaṇeśa and the Vāstu deity, and offers a havan — so that the first act done in the house is an act of worship. Milk is boiled until it rises over the rim as a sign of plenty, and the family eats its first meal there together.',
    hi: 'घर को एक जीवंत स्थान माना जाता है जिसके अपने अधिष्ठाता देवता हैं — वास्तु पुरुष। नए घर में रहने से पहले परिवार चुने हुए समय पर कलश लेकर प्रवेश करता है, गणेश जी और वास्तु देवता का पूजन करता है, और हवन करता है — ताकि उस घर में किया गया पहला कार्य पूजा हो। दूध को तब तक उबाला जाता है जब तक वह उफन न जाए — भरपूरता के संकेत के रूप में, और परिवार वहाँ अपना पहला भोजन साथ करता है।',
  },
  rudrabhishek: {
    en: 'Rudra is the Vedic name of Śiva. In the abhiṣeka the Śivaliṅga is bathed — with water, milk, curd, honey, ghee — while the Rudra hymns of the Yajurveda are chanted. The liṅga is not an image of Śiva so much as his presence without form, and bathing it is the oldest way of honouring him. It is kept on Mondays, in pradoṣa, through the month of Śrāvaṇa, and on Mahāśivarātri.',
    hi: 'रुद्र भगवान शिव का वैदिक नाम है। अभिषेक में शिवलिंग को — जल, दूध, दही, शहद, घी से — स्नान कराया जाता है, और साथ में यजुर्वेद के रुद्र-सूक्तों का पाठ होता है। लिंग शिव की मूर्ति से अधिक उनकी निराकार उपस्थिति है, और उसका अभिषेक उनकी उपासना का सबसे प्राचीन ढंग है। यह सोमवार को, प्रदोष में, पूरे श्रावण मास में, और महाशिवरात्रि पर किया जाता है।',
  },
  mahamrityunjaya: {
    en: 'The Mahāmṛtyuñjaya mantra — the "great conqueror of death" — is a verse of the Ṛgveda addressed to Tryambaka, the three-eyed Śiva. A family has it chanted a set number of times, with a havan, for someone who is ill or in danger: a prayer for health, long life and freedom from fear. It is prayer, and it stands beside medical care — it never takes its place.',
    hi: 'महामृत्युंजय मंत्र — "मृत्यु पर महान विजय पाने वाला" — ऋग्वेद का एक मंत्र है जो त्र्यंबक, त्रिनेत्र शिव को संबोधित है। परिवार किसी अस्वस्थ या संकट में पड़े स्वजन के लिए इसका निश्चित संख्या में जप और हवन कराता है: स्वास्थ्य, दीर्घायु और भय-मुक्ति की प्रार्थना। यह प्रार्थना है, और चिकित्सा के साथ खड़ी होती है — उसकी जगह कभी नहीं लेती।',
  },
  durga: {
    en: 'Durgā is the Devī as protector — the power that the gods together called forth when no one of them could prevail. Her deeds are told in the Durgā Saptaśatī, seven hundred verses from the Mārkaṇḍeya Purāṇa, which is recited through the nine nights of Navarātri and completed with a havan. The family honours her as mother and as strength; on Aṣṭamī or Navamī many households also honour young girls as her living form.',
    hi: 'दुर्गा देवी का रक्षक रूप हैं — वह शक्ति जिसे सब देवताओं ने मिलकर प्रकट किया जब उनमें से कोई अकेला विजय न पा सका। उनके चरित्र दुर्गा सप्तशती में कहे गए हैं — मार्कण्डेय पुराण के सात सौ श्लोक — जिसका पाठ नवरात्रि की नौ रातों में होता है और हवन से पूर्ण होता है। परिवार उन्हें माता और शक्ति के रूप में पूजता है; अष्टमी या नवमी पर अनेक घरों में कन्याओं को उनका जीवित स्वरूप मानकर पूजा जाता है।',
  },
  sundarkand: {
    en: 'The Sundarakāṇḍa is the fifth book of Tulasīdāsa’s Rāmacaritamānasa. It tells how Hanumān leapt the ocean, found Sītā in Laṅkā, gave her Rāma’s ring and returned with her message — the book of courage, devotion and hope restored. Families gather to recite it together, most often on a Tuesday or Saturday, for strength in a difficult time and in gratitude when one has passed.',
    hi: 'सुंदरकांड गोस्वामी तुलसीदास के रामचरितमानस का पाँचवाँ सोपान है। इसमें कथा है कि हनुमान जी ने कैसे समुद्र लाँघा, लंका में सीता जी को खोजा, उन्हें श्रीराम की मुद्रिका दी और उनका संदेश लेकर लौटे — साहस, भक्ति और लौटी हुई आशा का कांड। परिवार इसे साथ बैठकर पढ़ते हैं, प्रायः मंगलवार या शनिवार को — कठिन समय में बल के लिए, और उसके बीत जाने पर कृतज्ञता में।',
  },
  'gayatri-havan': {
    en: 'The Gāyatrī is a verse of the Ṛgveda addressed to Savitṛ, the sun as the source of light and of understanding; it has been recited daily for some three thousand years. In a havan, offerings of ghee and herbs are placed in a consecrated fire as the mantra is chanted, the fire carrying them onward. It is the simplest and most widely kept havan — for a birthday, an anniversary, or any day a family wishes to mark as auspicious.',
    hi: 'गायत्री ऋग्वेद का मंत्र है जो सविता को संबोधित है — सूर्य, प्रकाश और बुद्धि के स्रोत के रूप में; इसका नित्य जप लगभग तीन हज़ार वर्षों से होता आया है। हवन में मंत्रोच्चार के साथ घी और औषधियों की आहुतियाँ प्रतिष्ठित अग्नि में दी जाती हैं, और अग्नि उन्हें आगे ले जाती है। यह सबसे सरल और सबसे अधिक किया जाने वाला हवन है — जन्मदिन, वर्षगाँठ, या किसी भी ऐसे दिन के लिए जिसे परिवार मंगलमय बनाना चाहे।',
  },
  saraswati: {
    en: 'Sarasvatī is the goddess of learning, speech, music and the arts. On Vasant Pañcamī, as spring begins, books, pens and instruments are placed before her and she is worshipped in yellow, the colour of the season. Many families have a young child write the first letters before her — the vidyārambha, the beginning of study.',
    hi: 'सरस्वती विद्या, वाणी, संगीत और कलाओं की देवी हैं। वसंत पंचमी पर, वसंत के आरंभ में, पुस्तकें, कलम और वाद्य उनके सामने रखे जाते हैं और ऋतु के रंग — पीले — में उनकी पूजा होती है। अनेक परिवार छोटे बच्चे से उनके सामने पहले अक्षर लिखवाते हैं — विद्यारंभ, अध्ययन का आरंभ।',
  },
  namakaran: {
    en: 'Nāmakaraṇa is one of the sixteen saṁskāras, the rites that mark the stages of a life. The child is given a name before the sacred fire and the family — traditionally on the eleventh or twelfth day after birth, or later by family custom. The name is whispered first into the child’s ear, then spoken aloud, and the elders give their blessings.',
    hi: 'नामकरण सोलह संस्कारों में से एक है — वे अनुष्ठान जो जीवन के पड़ावों को चिह्नित करते हैं। शिशु को पवित्र अग्नि और परिवार के सामने नाम दिया जाता है — परंपरा से जन्म के ग्यारहवें या बारहवें दिन, या कुल-रीति के अनुसार बाद में। नाम पहले शिशु के कान में कहा जाता है, फिर सबके सामने बोला जाता है, और बड़े आशीर्वाद देते हैं।',
  },
  annaprashan: {
    en: 'Annaprāśana is the saṁskāra of a child’s first solid food, usually in the sixth month or soon after. Food is first offered to the deity, and then the elders feed the child the first morsel — most often khīr, rice cooked in milk. It marks the child’s passage from the mother’s milk to the food of the household.',
    hi: 'अन्नप्राशन शिशु के पहले अन्न-ग्रहण का संस्कार है, प्रायः छठे माह में या उसके कुछ बाद। अन्न पहले देवता को अर्पित होता है, फिर बड़े शिशु को पहला ग्रास खिलाते हैं — प्रायः खीर। यह शिशु के माँ के दूध से घर के अन्न की ओर बढ़ने का चिह्न है।',
  },
  mundan: {
    en: 'Muṇḍana, the cūḍākaraṇa saṁskāra, is a child’s first haircut — traditionally in the first or third year. After pūjā and a short havan the first locks are cut to the chanting of mantras, and the head is then shaved. It is kept as a rite of purification and of prayer for the child’s long life.',
    hi: 'मुंडन, अर्थात चूड़ाकर्म संस्कार, शिशु का पहला केश-कर्तन है — परंपरा से पहले या तीसरे वर्ष में। पूजन और संक्षिप्त हवन के बाद मंत्रोच्चार के साथ पहली लटें काटी जाती हैं, फिर सिर मुंडाया जाता है। इसे शुद्धि के और शिशु की दीर्घायु की प्रार्थना के संस्कार के रूप में रखा जाता है।',
  },
  shraddha: {
    en: 'Śrāddha is what is offered with śraddhā — with faith — to one’s departed ancestors, usually three generations. Water with black sesame is poured out for them (tarpaṇa), and in many families balls of cooked rice (piṇḍa) are offered. It is kept on the tithi of a parent’s passing, on Amāvāsyā, and through Pitṛ Pakṣa, the fortnight of the ancestors. Food is then given away in their name.',
    hi: 'श्राद्ध वह है जो श्रद्धा से अपने दिवंगत पितरों को — प्रायः तीन पीढ़ियों को — अर्पित किया जाता है। काले तिल मिला जल उनके लिए छोड़ा जाता है (तर्पण), और अनेक परिवारों में पके चावल के पिंड अर्पित होते हैं। यह माता-पिता की पुण्यतिथि पर, अमावस्या पर, और पितृ पक्ष में — पितरों के पखवाड़े में — किया जाता है। फिर उनके नाम से भोजन दान किया जाता है।',
  },
  vahan: {
    en: 'A short pūjā for a new vehicle before its first journey. Gaṇeśa is invoked, the vehicle is marked with a svastika and garlanded, and a coconut is broken before it. Many families keep it on Vijayādaśamī, the day on which tools and vehicles are traditionally honoured.',
    hi: 'नए वाहन की पहली यात्रा से पहले की संक्षिप्त पूजा। गणेश जी का आवाहन होता है, वाहन पर स्वस्तिक बनाकर माला पहनाई जाती है, और उसके सामने नारियल फोड़ा जाता है। अनेक परिवार इसे विजयादशमी पर करते हैं — जिस दिन परंपरा से औज़ारों और वाहनों की पूजा होती है।',
  },
  janmadin: {
    en: 'A birthday kept the traditional way — by the tithi of one’s birth where the family follows it. The family deity is worshipped, an āyuṣya havan is offered as a prayer for long life, and the one whose birthday it is receives a tilaka and the blessings of the elders.',
    hi: 'पारंपरिक रीति से मनाया गया जन्मदिन — जहाँ परिवार मानता हो वहाँ जन्म-तिथि के अनुसार। कुलदेवता का पूजन होता है, दीर्घायु की प्रार्थना के रूप में आयुष्य हवन होता है, और जिसका जन्मदिन है उसे तिलक और बड़ों का आशीर्वाद मिलता है।',
  },
}

// ── the step library ─────────────────────────────────────────────────────────
// mantra: { dev, iast } · what · why · more (detailed mode) — each { en, hi }
const S = {
  pavitra: {
    title: { en: 'Purification', hi: 'पवित्रीकरण' },
    mantra: { dev: 'ॐ अपवित्रः पवित्रो वा सर्वावस्थां गतोऽपि वा।\nयः स्मरेत्पुण्डरीकाक्षं स बाह्याभ्यन्तरः शुचिः॥', iast: 'Oṁ apavitraḥ pavitro vā sarvāvasthāṁ gato’pi vā |\nyaḥ smaret puṇḍarīkākṣaṁ sa bāhyābhyantaraḥ śuciḥ ||' },
    what: { en: 'Water is sprinkled on oneself and on the things laid out for the pūjā.', hi: 'अपने ऊपर और पूजा की सामग्री पर जल छिड़का जाता है।' },
    why: { en: 'One sits down to worship clean in body and settled in mind; the verse turns the mind to Viṣṇu before anything else is done.', hi: 'पूजा में शरीर से स्वच्छ और मन से स्थिर होकर बैठा जाता है; यह श्लोक कुछ भी करने से पहले मन को विष्णु की ओर मोड़ता है।' },
    more: { en: 'Take a little water in the left palm and sprinkle it with the fingers of the right — over your head, then over the altar and the sāmagrī.', hi: 'बाएँ हाथ की हथेली में थोड़ा जल लें और दाएँ हाथ की उँगलियों से छिड़कें — पहले अपने सिर पर, फिर चौकी और सामग्री पर।' },
  },
  achamana: {
    title: { en: 'Ācamana', hi: 'आचमन' },
    mantra: { dev: 'ॐ केशवाय नमः। ॐ नारायणाय नमः। ॐ माधवाय नमः।', iast: 'Oṁ Keśavāya namaḥ | Oṁ Nārāyaṇāya namaḥ | Oṁ Mādhavāya namaḥ |' },
    what: { en: 'Three small sips of water are taken, one with each name of Viṣṇu.', hi: 'जल के तीन छोटे घूँट लिए जाते हैं, विष्णु के एक-एक नाम के साथ।' },
    why: { en: 'It is the inward purification that begins every rite — as the sprinkling cleans what is outside, the sipped water is for what is within.', hi: 'यह वह आंतरिक शुद्धि है जिससे हर अनुष्ठान आरंभ होता है — जैसे छिड़काव बाहर को शुद्ध करता है, वैसे आचमन का जल भीतर के लिए है।' },
    more: { en: 'Pour a few drops into the hollow of the right palm and sip from the base of the thumb, three times; then rinse the hand.', hi: 'दाईं हथेली के गड्ढे में कुछ बूँदें डालें और अँगूठे के मूल से पिएँ, तीन बार; फिर हाथ धो लें।' },
  },
  deepa: {
    title: { en: 'Lighting the lamp', hi: 'दीप प्रज्वलन' },
    mantra: { dev: 'शुभं करोति कल्याणम् आरोग्यं धनसम्पदा।\nशत्रुबुद्धिविनाशाय दीपज्योतिर्नमोऽस्तु ते॥', iast: 'Śubhaṁ karoti kalyāṇam ārogyaṁ dhana-sampadā |\nśatru-buddhi-vināśāya dīpa-jyotir namo’stu te ||' },
    what: { en: 'The lamp is lit and saluted.', hi: 'दीपक जलाया जाता है और उसे प्रणाम किया जाता है।' },
    why: { en: 'The flame is the witness of the ceremony. It is lit first and kept burning until the end.', hi: 'ज्योति अनुष्ठान की साक्षी है। वह सबसे पहले जलाई जाती है और अंत तक जलती रहती है।' },
    more: { en: 'Use ghee or sesame oil and a cotton wick; place the lamp to the right of the deity, on a few grains of rice.', hi: 'घी या तिल का तेल और रुई की बत्ती लें; दीपक देवता के दाईं ओर, थोड़े अक्षत पर रखें।' },
  },
  sankalpa: {
    title: { en: 'Saṅkalpa — the intention', hi: 'संकल्प' },
    what: { en: 'The pandit recites the saṅkalpa: where and when by the pañcāṅga, the family’s name and gotra, and what this pūjā is for.', hi: 'पंडित जी संकल्प पढ़ते हैं: पंचांग के अनुसार स्थान और समय, परिवार का नाम और गोत्र, और यह पूजा किस उद्देश्य से है।' },
    why: { en: 'A rite is done with a stated intention. The saṅkalpa places this household, on this day, before the deity and says plainly why it has come.', hi: 'अनुष्ठान घोषित उद्देश्य के साथ होता है। संकल्प इस परिवार को, इस दिन, देवता के सामने रखता है और साफ़ कहता है कि वह क्यों आया है।' },
    more: { en: 'Hold water, a few grains of rice and a flower in the right palm while it is recited, and let them fall into a plate at the end. Tell the pandit your gotra beforehand; if it is not known, he will tell you what is said instead.', hi: 'पाठ के समय दाईं हथेली में जल, थोड़े अक्षत और एक फूल रखें, और अंत में उन्हें थाली में छोड़ दें। अपना गोत्र पंडित जी को पहले बता दें; ज्ञात न हो तो वे बताएँगे कि उसकी जगह क्या कहा जाता है।' },
  },
  ganesha: {
    title: { en: 'Gaṇeśa pūjana', hi: 'गणेश पूजन' },
    mantra: { dev: 'ॐ गं गणपतये नमः॥\n\nवक्रतुण्ड महाकाय सूर्यकोटिसमप्रभ।\nनिर्विघ्नं कुरु मे देव सर्वकार्येषु सर्वदा॥', iast: 'Oṁ gaṁ Gaṇapataye namaḥ ||\n\nVakratuṇḍa mahākāya sūrya-koṭi-samaprabha |\nnirvighnaṁ kuru me deva sarva-kāryeṣu sarvadā ||' },
    what: { en: 'Invocation of Lord Gaṇeśa.', hi: 'भगवान गणेश का आवाहन।' },
    why: { en: 'Traditionally performed before beginning an auspicious ceremony, so that it may be completed without obstacle.', hi: 'परंपरा से हर शुभ अनुष्ठान के आरंभ से पहले किया जाता है, ताकि वह निर्विघ्न पूर्ण हो।' },
    more: { en: 'Offer akṣata, a flower and dūrvā to Gaṇeśa — or to a supārī placed on rice to stand for him — and join your palms.', hi: 'गणेश जी को — या उनके स्थान पर अक्षत पर रखी सुपारी को — अक्षत, फूल और दूर्वा अर्पित करें, और हाथ जोड़ें।' },
  },
  kalasha: {
    title: { en: 'Kalaśa sthāpana', hi: 'कलश स्थापना' },
    mantra: { dev: 'कलशस्य मुखे विष्णुः कण्ठे रुद्रः समाश्रितः।\nमूले तत्र स्थितो ब्रह्मा मध्ये मातृगणाः स्मृताः॥', iast: 'Kalaśasya mukhe Viṣṇuḥ kaṇṭhe Rudraḥ samāśritaḥ |\nmūle tatra sthito Brahmā madhye mātṛ-gaṇāḥ smṛtāḥ ||' },
    what: { en: 'The kalaśa is established: filled with water, crowned with leaves and a coconut, and worshipped.', hi: 'कलश स्थापित किया जाता है: जल से भरकर, पत्तों और नारियल से सजाकर, उसका पूजन होता है।' },
    why: { en: 'The kalaśa is the seat into which the deities and the sacred rivers are invited for the length of the pūjā.', hi: 'कलश वह आसन है जिसमें पूजा की अवधि के लिए देवताओं और पवित्र नदियों का आवाहन होता है।' },
    more: { en: 'Set the pot on a small heap of rice; put in water, a coin, a supārī and a flower; arrange five leaves at the mouth and place the coconut on them, wrapped in maulī.', hi: 'पात्र को अक्षत की छोटी ढेरी पर रखें; उसमें जल, सिक्का, सुपारी और फूल डालें; मुख पर पाँच पत्ते सजाएँ और उन पर मौली लिपटा नारियल रखें।' },
  },
  svasti: {
    title: { en: 'Svasti vācana', hi: 'स्वस्ति वाचन' },
    mantra: { dev: 'ॐ स्वस्ति न इन्द्रो वृद्धश्रवाः स्वस्ति नः पूषा विश्ववेदाः।\nस्वस्ति नस्तार्क्ष्यो अरिष्टनेमिः स्वस्ति नो बृहस्पतिर्दधातु॥', iast: 'Oṁ svasti na Indro vṛddhaśravāḥ svasti naḥ Pūṣā viśvavedāḥ |\nsvasti nas Tārkṣyo ariṣṭanemiḥ svasti no Bṛhaspatir dadhātu ||' },
    what: { en: 'The benediction for well-being is chanted over everyone present.', hi: 'सबके कल्याण के लिए मंगल-वचन का पाठ होता है।' },
    why: { en: 'Before the main worship begins, auspiciousness is asked for the family and the home.', hi: 'मुख्य पूजन से पहले परिवार और घर के लिए मंगल की कामना की जाती है।' },
    more: { en: 'A verse of the Ṛgveda. The family sits with joined palms; the pandit may sprinkle akṣata over those present.', hi: 'ऋग्वेद का मंत्र। परिवार हाथ जोड़कर बैठता है; पंडित जी उपस्थित जनों पर अक्षत छिड़क सकते हैं।' },
  },
  vishnu: {
    title: { en: 'Dhyāna and pūjā of Satyanārāyaṇa', hi: 'सत्यनारायण का ध्यान एवं पूजन' },
    mantra: { dev: 'शान्ताकारं भुजगशयनं पद्मनाभं सुरेशं\nविश्वाधारं गगनसदृशं मेघवर्णं शुभाङ्गम्।\nलक्ष्मीकान्तं कमलनयनं योगिभिर्ध्यानगम्यं\nवन्दे विष्णुं भवभयहरं सर्वलोकैकनाथम्॥\n\nॐ नमो भगवते वासुदेवाय॥', iast: 'Śāntākāraṁ bhujaga-śayanaṁ padmanābhaṁ sureśaṁ\nviśvādhāraṁ gagana-sadṛśaṁ megha-varṇaṁ śubhāṅgam |\nLakṣmī-kāntaṁ kamala-nayanaṁ yogibhir dhyāna-gamyaṁ\nvande Viṣṇuṁ bhava-bhaya-haraṁ sarva-lokaika-nātham ||\n\nOṁ namo bhagavate Vāsudevāya ||' },
    what: { en: 'Viṣṇu is brought to mind in the dhyāna verse, then worshipped with water, pañcāmṛta, sandal, flowers and tulasī.', hi: 'ध्यान-श्लोक से विष्णु का स्मरण किया जाता है, फिर जल, पंचामृत, चंदन, पुष्प और तुलसी से उनका पूजन होता है।' },
    why: { en: 'The deity is first held in the mind and then honoured as a guest is honoured — with a seat, water, a bath, clothing, fragrance, flowers, light and food.', hi: 'देवता को पहले मन में धारण किया जाता है, फिर अतिथि की तरह उनका सत्कार होता है — आसन, जल, स्नान, वस्त्र, गंध, पुष्प, दीप और नैवेद्य से।' },
    more: { en: 'Offer each thing as the pandit names it. Tulasī leaves are offered to Viṣṇu in particular.', hi: 'जैसे-जैसे पंडित जी नाम लें, वह वस्तु अर्पित करें। विष्णु को विशेष रूप से तुलसी दल अर्पित होते हैं।' },
  },
  katha: {
    title: { en: 'The kathā', hi: 'कथा' },
    what: { en: 'The pandit tells the Satyanārāyaṇa kathā in its five chapters.', hi: 'पंडित जी पाँच अध्यायों में सत्यनारायण कथा सुनाते हैं।' },
    why: { en: 'Listening is the vow. Each chapter tells of someone who kept their word to the Lord, or forgot it, and what followed.', hi: 'सुनना ही व्रत है। हर अध्याय किसी ऐसे की कथा है जिसने भगवान को दिया वचन निभाया, या भुला दिया, और फिर क्या हुआ।' },
    more: { en: 'Sit together until it ends; at the close of each chapter the conch or bell is sounded and all say the Lord’s name.', hi: 'समाप्ति तक साथ बैठें; हर अध्याय के अंत में शंख या घंटी बजती है और सब भगवान का नाम लेते हैं।' },
  },
  shiva: {
    title: { en: 'Dhyāna of Śiva', hi: 'शिव ध्यान' },
    mantra: { dev: 'कर्पूरगौरं करुणावतारं संसारसारं भुजगेन्द्रहारम्।\nसदा वसन्तं हृदयारविन्दे भवं भवानीसहितं नमामि॥\n\nॐ नमः शिवाय॥', iast: 'Karpūra-gauraṁ karuṇāvatāraṁ saṁsāra-sāraṁ bhujagendra-hāram |\nsadā vasantaṁ hṛdayāravinde Bhavaṁ Bhavānī-sahitaṁ namāmi ||\n\nOṁ namaḥ Śivāya ||' },
    what: { en: 'Śiva is brought to mind and saluted with the five-syllable mantra.', hi: 'शिव का ध्यान किया जाता है और पंचाक्षर मंत्र से उन्हें नमन किया जाता है।' },
    why: { en: 'The worship begins by holding Śiva, with Pārvatī, in the heart before anything is offered.', hi: 'पूजन का आरंभ पार्वती सहित शिव को हृदय में धारण करने से होता है, कुछ भी अर्पित करने से पहले।' },
    more: { en: 'The family repeats "Oṁ namaḥ Śivāya" with the pandit.', hi: 'परिवार पंडित जी के साथ "ॐ नमः शिवाय" दोहराता है।' },
  },
  abhisheka: {
    title: { en: 'Abhiṣeka', hi: 'अभिषेक' },
    mantra: { dev: 'ॐ नमः शिवाय॥', iast: 'Oṁ namaḥ Śivāya ||' },
    what: { en: 'The liṅga is bathed — with water, then milk, curd, ghee, honey and sugar, and water again — while the pandit chants the Rudra.', hi: 'लिंग का अभिषेक होता है — जल से, फिर दूध, दही, घी, शहद और शक्कर से, और पुनः जल से — जबकि पंडित जी रुद्र-पाठ करते हैं।' },
    why: { en: 'Bathing the liṅga to the sound of the Rudra hymns is the oldest form of Śiva’s worship; each substance is offered in turn and washed away.', hi: 'रुद्र-सूक्तों की ध्वनि में लिंग का अभिषेक शिव-उपासना का सबसे प्राचीन रूप है; हर द्रव्य क्रम से अर्पित होकर धुल जाता है।' },
    more: { en: 'Pour in a thin, steady stream. The Rudra is long and the pandit chants it; the family keeps "Oṁ namaḥ Śivāya" going. Afterwards the liṅga is dried, marked with bhasma and sandal, and bilva leaves are offered.', hi: 'पतली, अटूट धार से अर्पित करें। रुद्र-पाठ लंबा है और पंडित जी करते हैं; परिवार "ॐ नमः शिवाय" का जप चलाए रखता है। बाद में लिंग को पोंछकर भस्म और चंदन लगाया जाता है और बिल्वपत्र अर्पित होते हैं।' },
  },
  mrityunjaya: {
    title: { en: 'Mahāmṛtyuñjaya japa', hi: 'महामृत्युंजय जप' },
    mantra: { dev: 'ॐ त्र्यम्बकं यजामहे सुगन्धिं पुष्टिवर्धनम्।\nउर्वारुकमिव बन्धनान् मृत्योर्मुक्षीय माऽमृतात्॥', iast: 'Oṁ tryambakaṁ yajāmahe sugandhiṁ puṣṭi-vardhanam |\nurvārukam iva bandhanān mṛtyor mukṣīya mā’mṛtāt ||' },
    what: { en: 'The mantra is repeated the agreed number of times, counted on a rudrākṣa mālā.', hi: 'मंत्र का निश्चित संख्या में जप होता है, रुद्राक्ष माला पर गिनकर।' },
    why: { en: 'It is the family’s prayer to Śiva for the health and long life of the one it is offered for.', hi: 'यह जिसके लिए किया जा रहा है उसके स्वास्थ्य और दीर्घायु के लिए परिवार की शिव जी से प्रार्थना है।' },
    more: { en: 'A verse of the Ṛgveda (7.59.12). One round of the mālā is 108 repetitions; the family may join for a round. Name the person it is for in the saṅkalpa.', hi: 'ऋग्वेद का मंत्र (7.59.12)। माला का एक फेरा 108 जप है; परिवार एक फेरे में साथ दे सकता है। जिसके लिए है उसका नाम संकल्प में लें।' },
  },
  lakshmi: {
    title: { en: 'Lakṣmī pūjana', hi: 'लक्ष्मी पूजन' },
    mantra: { dev: 'ॐ श्रीं महालक्ष्म्यै नमः॥\n\nॐ महालक्ष्म्यै च विद्महे विष्णुपत्न्यै च धीमहि।\nतन्नो लक्ष्मीः प्रचोदयात्॥', iast: 'Oṁ śrīṁ Mahālakṣmyai namaḥ ||\n\nOṁ Mahālakṣmyai ca vidmahe Viṣṇu-patnyai ca dhīmahi |\ntan no Lakṣmīḥ pracodayāt ||' },
    what: { en: 'Lakṣmī is invited and worshipped with flowers, sandal, kumkum, coins and sweets.', hi: 'लक्ष्मी जी का आवाहन होता है और पुष्प, चंदन, कुमकुम, सिक्कों और मिठाई से उनका पूजन होता है।' },
    why: { en: 'The household welcomes her and gives thanks for what it has.', hi: 'गृहस्थ उनका स्वागत करता है और जो उसके पास है उसके लिए धन्यवाद देता है।' },
    more: { en: 'Gaṇeśa sits to her right and is worshipped first. Place coins or the account books before her; lamps are then carried through the house.', hi: 'गणेश जी उनके दाईं ओर विराजते हैं और पहले पूजे जाते हैं। सिक्के या बही-खाते उनके सामने रखें; फिर दीपक घर भर में ले जाए जाते हैं।' },
  },
  durga: {
    title: { en: 'Devī pūjana and the pāṭha', hi: 'देवी पूजन एवं पाठ' },
    mantra: { dev: 'सर्वमङ्गलमाङ्गल्ये शिवे सर्वार्थसाधिके।\nशरण्ये त्र्यम्बके गौरि नारायणि नमोऽस्तु ते॥\n\nॐ दुं दुर्गायै नमः॥', iast: 'Sarva-maṅgala-māṅgalye Śive sarvārtha-sādhike |\nśaraṇye Tryambake Gauri Nārāyaṇi namo’stu te ||\n\nOṁ duṁ Durgāyai namaḥ ||' },
    what: { en: 'The Devī is worshipped, and the pandit recites the Durgā Saptaśatī — in full or the chapters chosen.', hi: 'देवी का पूजन होता है, और पंडित जी दुर्गा सप्तशती का पाठ करते हैं — पूर्ण या चुने हुए अध्याय।' },
    why: { en: 'The Saptaśatī is the telling of her deeds; to hear it through is the worship of Navarātri.', hi: 'सप्तशती उनके चरित्रों का वर्णन है; उसे पूरा सुनना ही नवरात्रि की उपासना है।' },
    more: { en: 'Offer the red chunarī, flowers and śṛṅgāra to the Devī. The verse here is from the Saptaśatī itself and is repeated by all.', hi: 'देवी को लाल चुनरी, पुष्प और श्रृंगार अर्पित करें। यह श्लोक स्वयं सप्तशती का है और सब इसे दोहराते हैं।' },
  },
  saraswati: {
    title: { en: 'Sarasvatī pūjana', hi: 'सरस्वती पूजन' },
    mantra: { dev: 'सरस्वति नमस्तुभ्यं वरदे कामरूपिणि।\nविद्यारम्भं करिष्यामि सिद्धिर्भवतु मे सदा॥\n\nॐ ऐं सरस्वत्यै नमः॥', iast: 'Sarasvati namas tubhyaṁ varade kāma-rūpiṇi |\nvidyārambhaṁ kariṣyāmi siddhir bhavatu me sadā ||\n\nOṁ aiṁ Sarasvatyai namaḥ ||' },
    what: { en: 'Sarasvatī is worshipped, with books, pens and instruments placed before her.', hi: 'सरस्वती जी का पूजन होता है; पुस्तकें, कलम और वाद्य उनके सामने रखे जाते हैं।' },
    why: { en: 'Study and the arts are begun with her blessing.', hi: 'अध्ययन और कलाओं का आरंभ उनके आशीर्वाद से होता है।' },
    more: { en: 'Offer yellow or white flowers. Where the family keeps vidyārambha, the child writes the first letters in a plate of rice after this verse.', hi: 'पीले या सफ़ेद फूल अर्पित करें। जहाँ विद्यारंभ की परंपरा हो, बच्चा इस श्लोक के बाद चावल की थाली में पहले अक्षर लिखता है।' },
  },
  hanuman: {
    title: { en: 'Hanumān and the pāṭha', hi: 'हनुमान जी एवं पाठ' },
    mantra: { dev: 'मनोजवं मारुततुल्यवेगं जितेन्द्रियं बुद्धिमतां वरिष्ठम्।\nवातात्मजं वानरयूथमुख्यं श्रीरामदूतं शरणं प्रपद्ये॥', iast: 'Manojavaṁ māruta-tulya-vegaṁ jitendriyaṁ buddhimatāṁ variṣṭham |\nvātātmajaṁ vānara-yūtha-mukhyaṁ Śrī-Rāma-dūtaṁ śaraṇaṁ prapadye ||' },
    what: { en: 'Rāma-darbār and Hanumān are worshipped, and the Sundarakāṇḍa is recited from beginning to end.', hi: 'राम दरबार और हनुमान जी का पूजन होता है, और सुंदरकांड का आदि से अंत तक पाठ होता है।' },
    why: { en: 'The recitation itself is the offering; the family reads along and takes heart from Hanumān’s courage and devotion.', hi: 'पाठ ही अर्पण है; परिवार साथ पढ़ता है और हनुमान जी के साहस और भक्ति से बल लेता है।' },
    more: { en: 'Keep a copy for each reader. The pāṭha is in Awadhi; the pandit leads and all join in the dohās. It closes with the Hanumān Cālīsā.', hi: 'हर पढ़ने वाले के लिए एक प्रति रखें। पाठ अवधी में है; पंडित जी आगे पढ़ते हैं और दोहों में सब साथ देते हैं। समापन हनुमान चालीसा से होता है।' },
  },
  vastu: {
    title: { en: 'Vāstu pūjā', hi: 'वास्तु पूजा' },
    mantra: { dev: 'वास्तोष्पते प्रति जानीह्यस्मान् स्वावेशो अनमीवो भवा नः।\nयत्त्वेमहे प्रति तन्नो जुषस्व शं नो भव द्विपदे शं चतुष्पदे॥', iast: 'Vāstoṣpate prati jānīhy asmān svāveśo anamīvo bhavā naḥ |\nyat tvemahe prati tan no juṣasva śaṁ no bhava dvipade śaṁ catuṣpade ||' },
    what: { en: 'The deity of the dwelling, Vāstoṣpati, is worshipped at the centre of the house.', hi: 'घर के अधिष्ठाता देवता, वास्तोष्पति, का घर के मध्य में पूजन होता है।' },
    why: { en: 'The family asks the lord of the house to accept them and to make the dwelling a good one for all who live in it.', hi: 'परिवार घर के स्वामी से प्रार्थना करता है कि वे उन्हें स्वीकार करें और घर को उसमें रहने वाले सबके लिए शुभ बनाएँ।' },
    more: { en: 'A verse of the Ṛgveda (7.54.1), the oldest prayer for a home. Offerings are made at the centre and, in many families, at the corners.', hi: 'ऋग्वेद का मंत्र (7.54.1), घर के लिए सबसे प्राचीन प्रार्थना। आहुति-अर्पण मध्य में, और अनेक परिवारों में कोनों पर भी, होता है।' },
  },
  dvara: {
    title: { en: 'The threshold and the entry', hi: 'द्वार पूजन एवं प्रवेश' },
    what: { en: 'The main door is worshipped, and the family enters carrying the kalaśa, the lady of the house first.', hi: 'मुख्य द्वार का पूजन होता है, और परिवार कलश लेकर प्रवेश करता है — गृहलक्ष्मी सबसे आगे।' },
    why: { en: 'The first step into the home is taken as part of the rite, at the chosen hour.', hi: 'घर में पहला कदम अनुष्ठान के अंग के रूप में, चुने हुए मुहूर्त पर रखा जाता है।' },
    more: { en: 'Hang the toraṇa, draw a svastika at the door, break a coconut at the threshold, and step in with the right foot.', hi: 'तोरण बाँधें, द्वार पर स्वस्तिक बनाएँ, देहली पर नारियल फोड़ें, और दायाँ पैर पहले रखकर प्रवेश करें।' },
  },
  agni: {
    title: { en: 'Kindling the fire', hi: 'अग्नि स्थापना' },
    mantra: { dev: 'ॐ अग्नये स्वाहा। इदमग्नये इदं न मम॥', iast: 'Oṁ Agnaye svāhā | idam Agnaye idaṁ na mama ||' },
    what: { en: 'The fire is lit in the kuṇḍa with camphor and samidhā, and the first offerings of ghee are made.', hi: 'कुंड में कपूर और समिधा से अग्नि प्रज्वलित की जाती है, और घी की पहली आहुतियाँ दी जाती हैं।' },
    why: { en: 'Agni is the one who carries what is offered. Each offering is given with the words that it is his, not mine.', hi: 'अग्नि वह हैं जो अर्पित को आगे ले जाते हैं। हर आहुति इन शब्दों के साथ दी जाती है कि यह उनकी है, मेरी नहीं।' },
    more: { en: 'Keep the kuṇḍa on a heat-proof base in a ventilated place, with water at hand. Offer ghee with a spoon at each "svāhā".', hi: 'कुंड को ताप-रोधी आधार पर, हवादार स्थान में रखें, पास में जल हो। हर "स्वाहा" पर चम्मच से घी अर्पित करें।' },
  },
  ahutiGayatri: {
    title: { en: 'Āhutis with the Gāyatrī', hi: 'गायत्री मंत्र से आहुतियाँ' },
    mantra: { dev: 'ॐ भूर्भुवः स्वः तत्सवितुर्वरेण्यं\nभर्गो देवस्य धीमहि धियो यो नः प्रचोदयात् स्वाहा॥', iast: 'Oṁ bhūr bhuvaḥ svaḥ tat savitur vareṇyaṁ\nbhargo devasya dhīmahi dhiyo yo naḥ pracodayāt svāhā ||' },
    what: { en: 'The mantra is chanted and, at each "svāhā", ghee and havan sāmagrī are offered into the fire.', hi: 'मंत्र का उच्चारण होता है और हर "स्वाहा" पर घी और हवन सामग्री अग्नि में अर्पित होती है।' },
    why: { en: 'The offering and the mantra go together — the fire carries the one while the other is spoken.', hi: 'आहुति और मंत्र साथ चलते हैं — एक को अग्नि ले जाती है जब दूसरा बोला जाता है।' },
    more: { en: 'The Gāyatrī is a verse of the Ṛgveda (3.62.10). Everyone at the fire offers a pinch of sāmagrī together; 11, 21 or 108 āhutis as the pandit sets.', hi: 'गायत्री ऋग्वेद का मंत्र है (3.62.10)। अग्नि के पास बैठे सब एक साथ चुटकी भर सामग्री अर्पित करते हैं; 11, 21 या 108 आहुतियाँ, जैसा पंडित जी तय करें।' },
  },
  ahutiMain: {
    title: { en: 'Āhutis with the mantra of the ceremony', hi: 'अनुष्ठान के मंत्र से आहुतियाँ' },
    what: { en: 'The pandit chants the mantra of this ceremony and, at each "svāhā", the family offers ghee and sāmagrī into the fire.', hi: 'पंडित जी इस अनुष्ठान के मंत्र का उच्चारण करते हैं और हर "स्वाहा" पर परिवार घी और सामग्री अग्नि में अर्पित करता है।' },
    why: { en: 'What was prayed in the pūjā is now offered through the fire.', hi: 'पूजन में जो प्रार्थना की गई, वह अब अग्नि के माध्यम से अर्पित होती है।' },
    more: { en: 'Offer together, a pinch at a time, at the word "svāhā". The number of āhutis is the pandit’s to set.', hi: 'सब साथ, चुटकी-चुटकी, "स्वाहा" शब्द पर अर्पित करें। आहुतियों की संख्या पंडित जी तय करते हैं।' },
  },
  purnahuti: {
    title: { en: 'Pūrṇāhuti — the full offering', hi: 'पूर्णाहुति' },
    mantra: { dev: 'ॐ पूर्णमदः पूर्णमिदं पूर्णात्पूर्णमुदच्यते।\nपूर्णस्य पूर्णमादाय पूर्णमेवावशिष्यते॥', iast: 'Oṁ pūrṇam adaḥ pūrṇam idaṁ pūrṇāt pūrṇam udacyate |\npūrṇasya pūrṇam ādāya pūrṇam evāvaśiṣyate ||' },
    what: { en: 'The final offering — a whole coconut or supārī with ghee — is placed in the fire, everyone standing.', hi: 'अंतिम आहुति — घी सहित पूरा नारियल या सुपारी — अग्नि में दी जाती है, सब खड़े होकर।' },
    why: { en: 'It completes the havan: whatever was left unsaid or undone is offered in this one act.', hi: 'इससे हवन पूर्ण होता है: जो कुछ कहने या करने से रह गया, वह इस एक आहुति में अर्पित हो जाता है।' },
    more: { en: 'All who are present touch the offering or the one who holds it as it is given. The verse is the invocation of the Īśāvāsya Upaniṣad.', hi: 'आहुति देते समय उपस्थित सब उसे या उसे थामने वाले को स्पर्श करते हैं। यह मंत्र ईशावास्य उपनिषद् का शांति-पाठ है।' },
  },
  naivedya: {
    title: { en: 'Naivedya — the offering of food', hi: 'नैवेद्य' },
    mantra: { dev: 'ॐ प्राणाय स्वाहा। ॐ अपानाय स्वाहा। ॐ व्यानाय स्वाहा।\nॐ उदानाय स्वाहा। ॐ समानाय स्वाहा॥', iast: 'Oṁ prāṇāya svāhā | Oṁ apānāya svāhā | Oṁ vyānāya svāhā |\nOṁ udānāya svāhā | Oṁ samānāya svāhā ||' },
    what: { en: 'Fruit, sweets and the prasāda are offered to the deity.', hi: 'फल, मिठाई और प्रसाद देवता को अर्पित किए जाते हैं।' },
    why: { en: 'Food is offered first and eaten after; what the family then shares is prasāda — what has been received back.', hi: 'भोजन पहले अर्पित होता है और बाद में ग्रहण किया जाता है; परिवार फिर जो बाँटता है वह प्रसाद है — जो लौटकर मिला।' },
    more: { en: 'Sprinkle a little water around the plate, place a tulasī leaf on it where it is for Viṣṇu, and offer with the five mantras.', hi: 'थाली के चारों ओर थोड़ा जल छिड़कें, विष्णु के लिए हो तो उस पर तुलसी दल रखें, और पाँच मंत्रों से अर्पित करें।' },
  },
  aarti: {
    title: { en: 'Āratī', hi: 'आरती' },
    what: { en: 'The lamp is waved before the deity while everyone sings the āratī.', hi: 'देवता के सामने दीपक घुमाया जाता है और सब मिलकर आरती गाते हैं।' },
    why: { en: 'It is the joyful close of the worship; the light that was offered is then taken by each person with both hands.', hi: 'यह पूजन का आनंदमय समापन है; जो ज्योति अर्पित हुई उसे फिर हर व्यक्ति दोनों हाथों से ग्रहण करता है।' },
    more: { en: 'Light camphor or a ghee lamp on the āratī plate, stand, and move it in circles before the deity; ring the bell. Pass the plate so each may take the warmth of the flame.', hi: 'आरती की थाली में कपूर या घी का दीपक जलाएँ, खड़े हों, और उसे देवता के सामने गोल घुमाएँ; घंटी बजाएँ। थाली सबके पास ले जाएँ ताकि हर कोई ज्योति ले सके।' },
  },
  kshama: {
    title: { en: 'Kṣamā prārthanā — asking pardon', hi: 'क्षमा प्रार्थना' },
    mantra: { dev: 'आवाहनं न जानामि न जानामि विसर्जनम्।\nपूजां चैव न जानामि क्षमस्व परमेश्वर॥\n\nमन्त्रहीनं क्रियाहीनं भक्तिहीनं सुरेश्वर।\nयत्पूजितं मया देव परिपूर्णं तदस्तु मे॥', iast: 'Āvāhanaṁ na jānāmi na jānāmi visarjanam |\npūjāṁ caiva na jānāmi kṣamasva Parameśvara ||\n\nMantra-hīnaṁ kriyā-hīnaṁ bhakti-hīnaṁ Sureśvara |\nyat pūjitaṁ mayā deva paripūrṇaṁ tad astu me ||' },
    what: { en: 'Pardon is asked for anything left out or done imperfectly.', hi: 'जो कुछ छूट गया या त्रुटिपूर्ण हुआ उसके लिए क्षमा माँगी जाती है।' },
    why: { en: 'No worship is perfect; it is completed by asking that it be accepted as it was offered.', hi: 'कोई पूजा पूर्ण नहीं होती; वह इस प्रार्थना से पूर्ण होती है कि जैसी अर्पित हुई वैसी स्वीकार हो।' },
    more: { en: 'Said with joined palms by everyone, after the āratī.', hi: 'आरती के बाद सब हाथ जोड़कर कहते हैं।' },
  },
  shanti: {
    title: { en: 'Śānti pāṭha', hi: 'शांति पाठ' },
    mantra: { dev: 'ॐ सर्वे भवन्तु सुखिनः सर्वे सन्तु निरामयाः।\nसर्वे भद्राणि पश्यन्तु मा कश्चिद्दुःखभाग्भवेत्॥\n\nॐ शान्तिः शान्तिः शान्तिः॥', iast: 'Oṁ sarve bhavantu sukhinaḥ sarve santu nirāmayāḥ |\nsarve bhadrāṇi paśyantu mā kaścid duḥkha-bhāg bhavet ||\n\nOṁ śāntiḥ śāntiḥ śāntiḥ ||' },
    what: { en: 'The prayer for peace and for the well-being of all is chanted.', hi: 'शांति और सबके कल्याण की प्रार्थना का पाठ होता है।' },
    why: { en: 'The ceremony ends by turning outward — its good is wished not for this household alone but for everyone.', hi: 'अनुष्ठान बाहर की ओर मुड़कर समाप्त होता है — उसका मंगल केवल इस घर के लिए नहीं, सबके लिए चाहा जाता है।' },
    more: { en: '"Śāntiḥ" is said three times at the end, by everyone together.', hi: 'अंत में "शान्तिः" तीन बार कहा जाता है, सब मिलकर।' },
  },
  prasada: {
    title: { en: 'Prasāda', hi: 'प्रसाद' },
    what: { en: 'The pandit is honoured, and the prasāda is shared with everyone present — and sent to those who could not come.', hi: 'पंडित जी का सम्मान किया जाता है, और प्रसाद सब उपस्थित जनों में बाँटा जाता है — और जो न आ सके उन्हें भेजा जाता है।' },
    why: { en: 'What was offered is received back and shared; no one leaves without it.', hi: 'जो अर्पित हुआ वह लौटकर मिलता है और बाँटा जाता है; कोई उसके बिना नहीं लौटता।' },
    more: { en: 'Where the pandit joins by video, the family gives dakṣiṇā as it wishes afterwards.', hi: 'जहाँ पंडित जी वीडियो से जुड़ते हैं, परिवार बाद में स्वेच्छा से दक्षिणा देता है।' },
  },
  naming: {
    title: { en: 'The name is given', hi: 'नाम दिया जाता है' },
    what: { en: 'The father or an elder whispers the name into the child’s right ear, then says it aloud; it is written in a plate of rice.', hi: 'पिता या कोई बड़े शिशु के दाएँ कान में नाम कहते हैं, फिर सबके सामने बोलते हैं; नाम चावल की थाली में लिखा जाता है।' },
    why: { en: 'The child hears its own name first, before the world does.', hi: 'शिशु अपना नाम सबसे पहले स्वयं सुनता है, संसार से पहले।' },
    more: { en: 'Decide the name beforehand and tell the pandit. Everyone then calls the child by it once.', hi: 'नाम पहले से तय कर पंडित जी को बता दें। फिर सब एक-एक बार शिशु को उसी नाम से पुकारते हैं।' },
  },
  firstFood: {
    title: { en: 'The first morsel', hi: 'पहला ग्रास' },
    what: { en: 'The elders feed the child a little khīr from a clean new spoon.', hi: 'बड़े शिशु को नए स्वच्छ चम्मच से थोड़ी खीर खिलाते हैं।' },
    why: { en: 'The first food the child eats is food that has first been offered.', hi: 'शिशु जो पहला अन्न ग्रहण करता है वह पहले अर्पित किया हुआ अन्न होता है।' },
    more: { en: 'The father or maternal uncle usually feeds first, then the others in turn — a taste each, no more.', hi: 'प्रायः पिता या मामा पहले खिलाते हैं, फिर बाक़ी क्रम से — बस एक-एक स्वाद।' },
  },
  tonsure: {
    title: { en: 'The first locks', hi: 'पहली लटें' },
    what: { en: 'The father cuts the first locks as the pandit chants; the barber then completes the tonsure.', hi: 'पंडित जी के मंत्रोच्चार के साथ पिता पहली लटें काटते हैं; फिर नाई मुंडन पूरा करता है।' },
    why: { en: 'The hair of birth is given up, and the child’s long life is prayed for.', hi: 'जन्म के केश त्यागे जाते हैं, और शिशु की दीर्घायु की प्रार्थना की जाती है।' },
    more: { en: 'Hold the child in the mother’s lap facing east. Collect the hair in a cloth; afterwards haldī and curd are applied to the head.', hi: 'शिशु को माँ की गोद में पूर्वमुख बैठाएँ। केश वस्त्र में एकत्र करें; बाद में सिर पर हल्दी और दही लगाया जाता है।' },
  },
  tarpana: {
    title: { en: 'Tarpaṇa', hi: 'तर्पण' },
    what: { en: 'Water mixed with black sesame is poured out for each ancestor by name, the pandit leading the words.', hi: 'काले तिल मिला जल हर पितर के नाम से अर्पित किया जाता है; शब्द पंडित जी बुलवाते हैं।' },
    why: { en: 'It is the offering of water to those who came before — father, grandfather and great-grandfather, and the mother’s line.', hi: 'यह पूर्वजों को जल का अर्पण है — पिता, पितामह और प्रपितामह, और मातृ-कुल को।' },
    more: { en: 'Face south, hold kuśa grass, and let the water fall between the thumb and forefinger. Tell the pandit the names and gotra beforehand.', hi: 'दक्षिण की ओर मुख करें, कुश धारण करें, और जल अँगूठे और तर्जनी के बीच से गिरने दें। नाम और गोत्र पंडित जी को पहले बता दें।' },
  },
  pinda: {
    title: { en: 'Piṇḍa-dāna and giving', hi: 'पिंडदान एवं दान' },
    what: { en: 'Where the family keeps it, balls of cooked rice are offered; food is then set aside and given away in the ancestors’ name.', hi: 'जहाँ परंपरा हो, पके चावल के पिंड अर्पित किए जाते हैं; फिर भोजन निकालकर पितरों के नाम से दान किया जाता है।' },
    why: { en: 'The ancestors are fed through what is offered and through what is given to others.', hi: 'पितर उससे तृप्त होते हैं जो अर्पित होता है और जो दूसरों को दिया जाता है।' },
    more: { en: 'Portions are traditionally set out for a cow, a crow and a dog before the family eats.', hi: 'परिवार के भोजन से पहले परंपरा से गाय, कौए और कुत्ते के लिए अंश निकाले जाते हैं।' },
  },
  vehicle: {
    title: { en: 'Blessing the vehicle', hi: 'वाहन का पूजन' },
    what: { en: 'A svastika is drawn on the vehicle, it is garlanded and given a tilaka, and a coconut is broken before it.', hi: 'वाहन पर स्वस्तिक बनाया जाता है, माला पहनाकर तिलक लगाया जाता है, और उसके सामने नारियल फोड़ा जाता है।' },
    why: { en: 'What will carry the family is first offered and blessed.', hi: 'जो परिवार को ले जाएगा, वह पहले अर्पित और पूजित होता है।' },
    more: { en: 'Where the family keeps it, lemons are placed under the wheels and the vehicle is driven a little way over them.', hi: 'जहाँ परंपरा हो, पहियों के नीचे नींबू रखे जाते हैं और वाहन उन पर से थोड़ा चलाया जाता है।' },
  },
  blessing: {
    title: { en: 'The blessings of the elders', hi: 'बड़ों का आशीर्वाद' },
    what: { en: 'A tilaka is applied, akṣata is showered, and each elder blesses in turn.', hi: 'तिलक लगाया जाता है, अक्षत बरसाए जाते हैं, और हर बड़े बारी-बारी से आशीर्वाद देते हैं।' },
    why: { en: 'The rite ends in the family’s own words of good wishes.', hi: 'अनुष्ठान परिवार की अपनी शुभकामनाओं के शब्दों में समाप्त होता है।' },
    more: { en: 'Relatives joining by video give their blessings one home at a time.', hi: 'वीडियो से जुड़े स्वजन एक-एक घर करके आशीर्वाद देते हैं।' },
  },
}

const OPEN = ['pavitra', 'achamana', 'deepa', 'sankalpa', 'ganesha']
const CLOSE = ['aarti', 'kshama', 'shanti', 'prasada']
const HAVAN = ['agni', 'ahutiMain', 'purnahuti']
const ORDER = {
  satyanarayan: [...OPEN, 'kalasha', 'vishnu', 'katha', 'naivedya', ...CLOSE],
  ganesh: ['pavitra', 'achamana', 'deepa', 'sankalpa', 'ganesha', 'naivedya', ...CLOSE],
  lakshmi: [...OPEN, 'kalasha', 'lakshmi', 'naivedya', ...CLOSE],
  'griha-pravesh': ['dvara', ...OPEN, 'kalasha', 'vastu', 'agni', 'ahutiGayatri', 'purnahuti', ...CLOSE],
  rudrabhishek: [...OPEN, 'shiva', 'abhisheka', 'naivedya', ...CLOSE],
  mahamrityunjaya: [...OPEN, 'shiva', 'mrityunjaya', ...HAVAN, ...CLOSE],
  durga: [...OPEN, 'kalasha', 'durga', ...HAVAN, ...CLOSE],
  sundarkand: ['pavitra', 'deepa', 'sankalpa', 'ganesha', 'hanuman', 'aarti', 'shanti', 'prasada'],
  'gayatri-havan': [...OPEN, 'svasti', 'agni', 'ahutiGayatri', 'purnahuti', 'shanti', 'prasada'],
  saraswati: [...OPEN, 'saraswati', 'naivedya', ...CLOSE],
  namakaran: [...OPEN, 'agni', 'ahutiGayatri', 'naming', 'blessing', 'shanti', 'prasada'],
  annaprashan: [...OPEN, 'naivedya', 'firstFood', 'blessing', 'shanti', 'prasada'],
  mundan: [...OPEN, 'agni', 'ahutiGayatri', 'tonsure', 'blessing', 'shanti', 'prasada'],
  shraddha: ['pavitra', 'achamana', 'sankalpa', 'tarpana', 'pinda', 'kshama', 'shanti'],
  vahan: ['sankalpa', 'ganesha', 'vehicle', 'aarti'],
  janmadin: [...OPEN, 'svasti', 'agni', 'ahutiGayatri', 'purnahuti', 'blessing', 'aarti', 'shanti', 'prasada'],
}

// The Hanumān Cālīsā — its full text lives in its own file (chalisa.js).
Object.assign(S, CHALISA_STEPS)
ORDER['hanuman-chalisa'] = CHALISA_ORDER
ABOUT['hanuman-chalisa'] = CHALISA_ABOUT

/** The ordered steps of a ceremony. */
export function scriptFor(ritualKey) {
  return (ORDER[ritualKey] || []).map((id) => ({ id, ...S[id] }))
}

export const MODES = [
  { key: 'detailed', en: 'Detailed', hi: 'विस्तार से' },
  { key: 'short', en: 'Short', hi: 'संक्षेप में' },
  { key: 'none', en: 'Mantras only', hi: 'केवल मंत्र' },
]
export const VOICE_LANGS = [
  { key: 'en', label: 'English', bcp: ['en-IN', 'en-GB', 'en-US'] },
  { key: 'hi', label: 'हिन्दी', bcp: ['hi-IN'] },
]

/** What is spoken or shown for a step in a mode and language. */
export function explain(step, mode, lang) {
  const g = (o) => (o ? (o[lang] || o.en) : '')
  if (mode === 'none') return []
  const out = [
    { k: 'what', label: lang === 'hi' ? 'क्या हो रहा है' : 'What is happening', text: g(step.what) },
    { k: 'why', label: lang === 'hi' ? 'क्यों' : 'Why', text: g(step.why) },
  ]
  if (mode === 'detailed' && step.more) out.push({ k: 'more', label: lang === 'hi' ? 'आप क्या करें' : 'What you do', text: g(step.more) })
  return out.filter((x) => x.text)
}

/** Every step that has a fixed mantra — the chant library a pandit can record. */
export const MANTRA_STEPS = Object.keys(S).filter((id) => S[id].mantra).map((id) => ({ id, ...S[id] }))

// A plain roman reading of the scholarly transliteration, for reading aloud:
// "Oṁ gaṁ Gaṇapataye namaḥ" → "Om gam Ganapataye namaha".
const PLAIN = {
  ā: 'a', ī: 'i', ū: 'u', ṛ: 'ri', ṝ: 'ri', ḷ: 'li', ṁ: 'm', ṃ: 'm', ṅ: 'n', ñ: 'n', ṭ: 't', ḍ: 'd', ṇ: 'n', ś: 'sh', ṣ: 'sh',
  Ā: 'A', Ī: 'I', Ū: 'U', Ṛ: 'Ri', Ṁ: 'M', Ṅ: 'N', Ñ: 'N', Ṭ: 'T', Ḍ: 'D', Ṇ: 'N', Ś: 'Sh', Ṣ: 'Sh',
}
export function plainRoman(iast) {
  let out = ''
  const s = String(iast || '')
  for (let k = 0; k < s.length; k++) {
    const ch = s[k], next = s[k + 1] || ''
    if (ch === 'ḥ') {
      // the visarga echoes the vowel before it at the end of a word: namaḥ → namaha
      const prev = (out.match(/[aeiou]$/i) || ['a'])[0].toLowerCase()
      out += /[a-zāīūṛṁśṣṭḍṇñṅ]/i.test(next) ? 'h' : `h${prev}`
    } else if (ch === 'c' && next !== 'h') out += 'ch'
    else if (ch === 'C' && next !== 'h') out += 'Ch'
    else if (ch === '|') out += ''          // the daṇḍa belongs to the Devanāgarī line
    else out += PLAIN[ch] ?? ch
  }
  return out.replace(/[ 	]+$/gm, '')
}

/** The roman reading of a mantra or verse: its own where it has one (the Cālīsā is Awadhi, written out plainly), else from the IAST. */
export const romanOf = (m) => (m ? (m.roman || plainRoman(m.iast)) : '')

/** The verse under the motto. Shown as written; this site does not translate Sanskrit itself. */
export const HERO_SHLOKA = {
  dev: ['त्वमेव माता च पिता त्वमेव', 'त्वमेव बन्धुश्च सखा त्वमेव ।', 'त्वमेव विद्या द्रविणं त्वमेव', 'त्वमेव सर्वं मम देवदेव ॥'],
  iast: 'tvam eva mātā ca pitā tvam eva · tvam eva bandhuś ca sakhā tvam eva · tvam eva vidyā draviṇaṁ tvam eva · tvam eva sarvaṁ mama deva-deva',
}

/** Every step of every ceremony, once — the explanations a pandit can record. */
export const ALL_STEPS = Object.keys(S).map((id) => ({ id, ...S[id] }))

// ── the voice library ────────────────────────────────────────────────────────
// A recording is filed under what it is AND a fingerprint of the exact text it
// was read from. If a mantra or an explanation is ever corrected, its old
// recording simply stops matching and is no longer played — a voice is never
// laid over words it did not say.

/** FNV-1a (32-bit) of a text, as six hex characters. */
export function textHash(s) {
  let h = 0x811c9dc5
  const t = String(s)
  for (let i = 0; i < t.length; i++) { h ^= t.charCodeAt(i); h = Math.imul(h, 0x01000193) }
  return (h >>> 0).toString(16).padStart(8, '0').slice(0, 6)
}

/** What is read aloud to explain a step — or, with no step, the purpose of the ceremony. */
export function narration(ritual, step, mode, lang) {
  if (mode === 'none') return ''
  const g = (o) => (o ? (o[lang] || o.en) : '')
  if (!step) return (mode === 'detailed' ? g(ABOUT[ritual.key]) : '') || g(ritual.purpose)
  return `${g(step.title)}. ${explain(step, mode, lang).map((p) => `${p.label}: ${p.text}`).join(' ')}`
}

export const mantraClip = (step) => `m.${step.id}.${textHash(step.mantra.dev)}`
export const explainClip = (ritual, step, mode, lang) => {
  const h = textHash(narration(ritual, step, mode, lang))
  return step ? `x.${step.id}.${lang}.${mode}.${h}` : `p.${ritual.key}.${lang}.${mode}.${h}`
}
