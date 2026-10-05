/**
 * The ritual catalogue — sixteen pūjās, havans and saṁskāras a family
 * commonly asks a pandit for.
 *
 * What this is, and is not. Each entry says what the ceremony is for, what
 * happens in outline, how long it usually takes, and what to have ready.
 * Rites differ by region, sampradāya and family custom, so the outline is
 * deliberately general and the sāmagrī list is a starting point: THE PANDIT
 * CONFIRMS BOTH for the family before the day. Nothing here promises an
 * outcome — a pūjā is an act of devotion, not a transaction — and nothing
 * here is prescribed from a horoscope: this section stands apart from the
 * astrology side of the site.
 *
 * `when` names the observances a ceremony is traditionally kept on, by the
 * keys the pañcāṅga engine emits (api/festivals_data.py), so the calendar can
 * suggest it on the right days.
 */

// The things almost every pūjā needs; a ritual lists only what it adds.
export const BASE_SAMAGRI = [
  { en: 'A clean cloth for the altar (red or yellow) and an āsana to sit on', hi: 'चौकी के लिए स्वच्छ वस्त्र (लाल या पीला) और बैठने का आसन' },
  { en: 'Kalaśa (a copper, brass or steel pot) with clean water', hi: 'कलश (ताँबे, पीतल या स्टील का) स्वच्छ जल सहित' },
  { en: 'A coconut and mango leaves (or betel leaves) for the kalaśa', hi: 'कलश के लिए नारियल और आम के पत्ते (या पान के पत्ते)' },
  { en: 'Roli / kumkum, haldī, chandan and akṣata (unbroken rice)', hi: 'रोली / कुमकुम, हल्दी, चंदन और अक्षत' },
  { en: 'Fresh flowers and a garland', hi: 'ताज़े फूल और माला' },
  { en: 'Fruits and a sweet for naivedya', hi: 'फल और नैवेद्य के लिए मिठाई' },
  { en: 'A dīpa with ghee and cotton wicks, incense, camphor', hi: 'घी का दीपक, रुई की बत्तियाँ, धूप / अगरबत्ती, कपूर' },
  { en: 'Betel leaves and nuts, maulī (kalāvā thread)', hi: 'पान, सुपारी, मौली (कलावा)' },
  { en: 'Pañcāmṛta: milk, curd, ghee, honey, sugar', hi: 'पंचामृत: दूध, दही, घी, शहद, शक्कर' },
  { en: 'A bell, a plate for āratī, a spoon and small bowls', hi: 'घंटी, आरती की थाली, चम्मच और कटोरियाँ' },
]

// What a havan adds to the base list.
export const HAVAN_SAMAGRI = [
  { en: 'A havan kuṇḍa (or a safe metal vessel) on a heat-proof base', hi: 'हवन कुंड (या सुरक्षित धातु का पात्र), ताप-रोधी आधार पर' },
  { en: 'Samidhā (dry mango-wood sticks) and camphor to light the fire', hi: 'समिधा (आम की सूखी लकड़ी) और अग्नि प्रज्वलन के लिए कपूर' },
  { en: 'Havan sāmagrī (the herbal mix) and extra ghee for the āhutis', hi: 'हवन सामग्री और आहुतियों के लिए अतिरिक्त घी' },
  { en: 'A whole coconut or supārī for the pūrṇāhuti', hi: 'पूर्णाहुति के लिए पूरा नारियल या सुपारी' },
  { en: 'An open, ventilated space — and water at hand', hi: 'खुला, हवादार स्थान — और पास में जल' },
]

const COMMON_OUTLINE = [
  { en: 'Saṅkalpa — the family states the intention', hi: 'संकल्प — परिवार अपना उद्देश्य कहता है' },
  { en: 'Gaṇeśa pūjana and kalaśa sthāpana', hi: 'गणेश पूजन और कलश स्थापना' },
]
const CLOSING = [
  { en: 'Āratī, puṣpāñjali and the distribution of prasāda', hi: 'आरती, पुष्पांजलि और प्रसाद वितरण' },
]

export const RITUALS = [
  {
    key: 'satyanarayan', kind: 'puja', minutes: 120,
    name: { en: 'Satyanārāyaṇa Pūjā & Kathā', hi: 'श्री सत्यनारायण पूजा एवं कथा' },
    purpose: { en: 'Worship of Viṣṇu as Satyanārāyaṇa with the reading of the kathā — kept in thanksgiving, at a new beginning, or simply every month.', hi: 'सत्यनारायण रूप में भगवान विष्णु की पूजा और कथा-पाठ — कृतज्ञता में, नए आरंभ पर, या हर माह नियम से।' },
    outline: [...COMMON_OUTLINE,
      { en: 'Pūjā of Satyanārāyaṇa with tulasī, flowers and pañcāmṛta', hi: 'तुलसी, पुष्प और पंचामृत से सत्यनारायण पूजन' },
      { en: 'The kathā in five chapters, the family listening together', hi: 'पाँच अध्यायों की कथा, परिवार साथ बैठकर सुनता है' },
      ...CLOSING],
    samagri: [
      { en: 'A picture or mūrti of Satyanārāyaṇa / Viṣṇu', hi: 'सत्यनारायण / विष्णु जी का चित्र या मूर्ति' },
      { en: 'Tulasī leaves; banana leaves or small banana stems for the maṇḍapa', hi: 'तुलसी दल; मंडप के लिए केले के पत्ते या तने' },
      { en: 'Prasāda: pañjīrī or sūjī halvā (śīrā), and bananas', hi: 'प्रसाद: पंजीरी या सूजी का हलवा (शीरा), और केले' },
    ],
    when: ['purnima', 'ekadashi-shukla', 'ekadashi-krishna', 'sharad-purnima', 'guru-purnima'],
  },
  {
    key: 'ganesh', kind: 'puja', minutes: 60,
    name: { en: 'Gaṇeśa Pūjā', hi: 'गणेश पूजा' },
    purpose: { en: 'Worship of Gaṇeśa, the remover of obstacles — at the start of any undertaking, and on Caturthī.', hi: 'विघ्नहर्ता गणेश जी की पूजा — किसी भी कार्य के आरंभ में, और चतुर्थी पर।' },
    outline: [...COMMON_OUTLINE.slice(0, 1),
      { en: 'Āvāhana and ṣoḍaśopacāra pūjā of Gaṇeśa', hi: 'गणेश जी का आवाहन और षोडशोपचार पूजन' },
      { en: 'Offering of dūrvā and modaka; Gaṇeśa Atharvaśīrṣa or 108 names', hi: 'दूर्वा और मोदक अर्पण; गणपति अथर्वशीर्ष या 108 नाम' },
      ...CLOSING],
    samagri: [
      { en: 'A Gaṇeśa mūrti or picture', hi: 'गणेश जी की मूर्ति या चित्र' },
      { en: 'Dūrvā grass (21 blades), red flowers', hi: 'दूर्वा (21), लाल फूल' },
      { en: 'Modaka or laḍḍū', hi: 'मोदक या लड्डू' },
    ],
    when: ['ganesh-chaturthi', 'vinayaka-chaturthi', 'sankashti-chaturthi'],
  },
  {
    key: 'lakshmi', kind: 'puja', minutes: 90,
    name: { en: 'Lakṣmī Pūjā', hi: 'लक्ष्मी पूजा' },
    purpose: { en: 'Worship of Lakṣmī with Gaṇeśa — the Dīpāvalī evening pūjā, and a household’s act of gratitude for what it has.', hi: 'गणेश जी सहित माँ लक्ष्मी की पूजा — दीपावली की संध्या का पूजन, और जो है उसके लिए गृहस्थ की कृतज्ञता।' },
    outline: [...COMMON_OUTLINE,
      { en: 'Pūjā of Gaṇeśa and Lakṣmī; Śrī Sūkta or Lakṣmī stotra', hi: 'गणेश-लक्ष्मी पूजन; श्री सूक्त या लक्ष्मी स्तोत्र' },
      { en: 'Lighting of the lamps through the home', hi: 'घर भर में दीप प्रज्वलन' },
      ...CLOSING],
    samagri: [
      { en: 'Mūrtis or pictures of Lakṣmī and Gaṇeśa', hi: 'लक्ष्मी-गणेश की मूर्तियाँ या चित्र' },
      { en: 'Lotus or other fresh flowers; coins; khīl and batāśe', hi: 'कमल या अन्य ताज़े फूल; सिक्के; खील-बताशे' },
      { en: 'Earthen dīyās, oil or ghee, and wicks for the house', hi: 'मिट्टी के दीये, तेल या घी, और बत्तियाँ' },
    ],
    when: ['diwali', 'dhanteras', 'sharad-purnima'],
  },
  {
    key: 'griha-pravesh', kind: 'havan', minutes: 180,
    name: { en: 'Gṛha Praveśa & Vāstu Pūjā', hi: 'गृह प्रवेश एवं वास्तु पूजा' },
    purpose: { en: 'The first entry into a new home: worship at the threshold, Vāstu pūjā and a havan, before the household begins to live there.', hi: 'नए घर में प्रथम प्रवेश: द्वार पूजन, वास्तु पूजा और हवन, गृहस्थी बसाने से पहले।' },
    outline: [
      { en: 'Dvāra pūjā at the threshold and the entry with the kalaśa', hi: 'द्वार पूजन और कलश सहित प्रवेश' },
      ...COMMON_OUTLINE,
      { en: 'Vāstu pūjā and navagraha pūjana', hi: 'वास्तु पूजा और नवग्रह पूजन' },
      { en: 'Havan with pūrṇāhuti; boiling of milk in the new kitchen', hi: 'पूर्णाहुति सहित हवन; नई रसोई में दूध उबालना' },
      ...CLOSING],
    samagri: [
      { en: 'A toraṇa (mango-leaf festoon) for the main door', hi: 'मुख्य द्वार के लिए तोरण (आम के पत्तों का)' },
      { en: 'Milk and a new vessel for the kitchen', hi: 'रसोई के लिए दूध और नया पात्र' },
      { en: 'Navadhānya (nine grains), and a picture of the family deity', hi: 'नवधान्य, और कुलदेवता का चित्र' },
    ],
    havan: true, when: ['akshaya-tritiya', 'vasant-panchami'],
  },
  {
    key: 'rudrabhishek', kind: 'puja', minutes: 105,
    name: { en: 'Rudrābhiṣeka', hi: 'रुद्राभिषेक' },
    purpose: { en: 'The bathing of the Śivaliṅga with water, milk and pañcāmṛta to the chanting of the Rudra — kept on Mondays, Pradoṣa and Śivarātri.', hi: 'रुद्र-पाठ के साथ जल, दूध और पंचामृत से शिवलिंग का अभिषेक — सोमवार, प्रदोष और शिवरात्रि पर।' },
    outline: [...COMMON_OUTLINE,
      { en: 'Abhiṣeka of the liṅga with the Rudrāṣṭādhyāyī or Rudra-sūkta', hi: 'रुद्राष्टाध्यायी या रुद्र-सूक्त से लिंग का अभिषेक' },
      { en: 'Offering of bilva leaves, flowers and bhasma', hi: 'बिल्वपत्र, पुष्प और भस्म अर्पण' },
      ...CLOSING],
    samagri: [
      { en: 'A Śivaliṅga with a tray to collect the abhiṣeka', hi: 'शिवलिंग और अभिषेक एकत्र करने की थाली' },
      { en: 'Bilva leaves; plenty of water and milk; gaṅgājala if at hand', hi: 'बिल्वपत्र; पर्याप्त जल और दूध; गंगाजल हो तो' },
      { en: 'Bhasma, white flowers, and fruit', hi: 'भस्म, सफ़ेद फूल, और फल' },
    ],
    when: ['maha-shivaratri', 'masik-shivaratri', 'pradosha-shukla', 'pradosha-krishna'],
  },
  {
    key: 'mahamrityunjaya', kind: 'havan', minutes: 150,
    name: { en: 'Mahāmṛtyuñjaya Japa & Havan', hi: 'महामृत्युंजय जप एवं हवन' },
    purpose: { en: 'Japa of the Mahāmṛtyuñjaya mantra to Śiva with a havan — a family’s prayer for someone’s health and long life.', hi: 'शिव जी के महामृत्युंजय मंत्र का जप और हवन — किसी के स्वास्थ्य और दीर्घायु के लिए परिवार की प्रार्थना।' },
    outline: [...COMMON_OUTLINE,
      { en: 'Śiva pūjana and the japa (the count agreed with the pandit)', hi: 'शिव पूजन और जप (संख्या पंडित जी से तय)' },
      { en: 'Havan with the mantra and pūrṇāhuti', hi: 'मंत्र से हवन और पूर्णाहुति' },
      ...CLOSING],
    samagri: [
      { en: 'A Śivaliṅga or picture of Śiva; bilva leaves', hi: 'शिवलिंग या शिव जी का चित्र; बिल्वपत्र' },
      { en: 'A rudrākṣa mālā for the japa', hi: 'जप के लिए रुद्राक्ष माला' },
    ],
    havan: true, when: ['maha-shivaratri', 'masik-shivaratri', 'pradosha-shukla', 'pradosha-krishna'],
  },
  {
    key: 'durga', kind: 'havan', minutes: 180,
    name: { en: 'Durgā Pūjā · Caṇḍī Pāṭha & Havan', hi: 'दुर्गा पूजा · चंडी पाठ एवं हवन' },
    purpose: { en: 'Worship of the Devī with the Durgā Saptaśatī and a havan — the pūjā of Navarātri, Aṣṭamī and Navamī.', hi: 'दुर्गा सप्तशती के पाठ और हवन के साथ देवी की उपासना — नवरात्रि, अष्टमी और नवमी का पूजन।' },
    outline: [...COMMON_OUTLINE,
      { en: 'Devī pūjana; Durgā Saptaśatī (in full or the chosen chapters)', hi: 'देवी पूजन; दुर्गा सप्तशती (पूर्ण या चुने हुए अध्याय)' },
      { en: 'Havan and pūrṇāhuti; kanyā pūjana where the family keeps it', hi: 'हवन और पूर्णाहुति; जहाँ परंपरा हो वहाँ कन्या पूजन' },
      ...CLOSING],
    samagri: [
      { en: 'A picture or mūrti of Durgā; a red chunarī and śṛṅgāra items', hi: 'माँ दुर्गा का चित्र या मूर्ति; लाल चुनरी और श्रृंगार सामग्री' },
      { en: 'Red flowers; jau (barley) if the family sows it at Navarātri', hi: 'लाल फूल; नवरात्रि में जौ बोने की परंपरा हो तो जौ' },
    ],
    havan: true, when: ['navaratri', 'durga-ashtami', 'maha-navami', 'vijayadashami'],
  },
  {
    key: 'sundarkand', kind: 'path', minutes: 150,
    name: { en: 'Sundarakāṇḍa Pāṭha', hi: 'सुंदरकांड पाठ' },
    purpose: { en: 'The recitation of the Sundarakāṇḍa of the Rāmacaritamānasa, in praise of Hanumān — often kept on Tuesdays and Saturdays.', hi: 'रामचरितमानस के सुंदरकांड का पाठ, हनुमान जी की स्तुति में — प्रायः मंगलवार और शनिवार को।' },
    outline: [...COMMON_OUTLINE.slice(0, 1),
      { en: 'Pūjana of Rāma-darbār and Hanumān', hi: 'राम दरबार और हनुमान जी का पूजन' },
      { en: 'The pāṭha, the family reciting along; Hanumān Cālīsā', hi: 'पाठ, परिवार साथ में दोहराता है; हनुमान चालीसा' },
      ...CLOSING],
    samagri: [
      { en: 'A picture of Rāma-darbār and of Hanumān', hi: 'राम दरबार और हनुमान जी का चित्र' },
      { en: 'Copies of the Sundarakāṇḍa for the family', hi: 'परिवार के लिए सुंदरकांड की प्रतियाँ' },
      { en: 'Sindūra and jasmine oil (where offered); būndī or laḍḍū', hi: 'सिंदूर और चमेली का तेल (जहाँ चढ़ाते हों); बूंदी या लड्डू' },
    ],
    when: ['hanuman-jayanti', 'rama-navami'],
  },
  {
    key: 'gayatri-havan', kind: 'havan', minutes: 90,
    name: { en: 'Gāyatrī Havan', hi: 'गायत्री हवन' },
    purpose: { en: 'A simple, auspicious havan with the Gāyatrī mantra — for a birthday, an anniversary, or any day the family wants to mark.', hi: 'गायत्री मंत्र से सरल, मंगलमय हवन — जन्मदिन, वर्षगाँठ या किसी भी शुभ दिन के लिए।' },
    outline: [...COMMON_OUTLINE,
      { en: 'Agni sthāpana and āhutis with the Gāyatrī mantra', hi: 'अग्नि स्थापना और गायत्री मंत्र से आहुतियाँ' },
      { en: 'Pūrṇāhuti and śānti-pāṭha', hi: 'पूर्णाहुति और शांति-पाठ' },
      ...CLOSING],
    samagri: [],
    havan: true, when: ['purnima', 'akshaya-tritiya', 'guru-purnima', 'vasant-panchami'],
  },
  {
    key: 'saraswati', kind: 'puja', minutes: 60,
    name: { en: 'Sarasvatī Pūjā', hi: 'सरस्वती पूजा' },
    purpose: { en: 'Worship of Sarasvatī, of learning and the arts — on Vasant Pañcamī, and when a child begins to study.', hi: 'विद्या और कला की देवी सरस्वती की पूजा — वसंत पंचमी पर, और जब बच्चा पढ़ना आरंभ करे।' },
    outline: [...COMMON_OUTLINE,
      { en: 'Sarasvatī pūjana; books, pens and instruments placed before her', hi: 'सरस्वती पूजन; पुस्तकें, कलम और वाद्य उनके सामने रखे जाते हैं' },
      { en: 'Sarasvatī vandanā; the child writes the first letters (vidyārambha) where kept', hi: 'सरस्वती वंदना; जहाँ परंपरा हो वहाँ विद्यारंभ' },
      ...CLOSING],
    samagri: [
      { en: 'A picture or mūrti of Sarasvatī', hi: 'सरस्वती जी का चित्र या मूर्ति' },
      { en: 'Yellow or white flowers; yellow sweets', hi: 'पीले या सफ़ेद फूल; पीली मिठाई' },
      { en: 'Books, notebooks, pens, instruments', hi: 'पुस्तकें, कॉपियाँ, कलम, वाद्य' },
    ],
    when: ['vasant-panchami'],
  },
  {
    key: 'namakaran', kind: 'samskara', minutes: 60,
    name: { en: 'Nāmakaraṇa — the naming', hi: 'नामकरण संस्कार' },
    purpose: { en: 'The saṁskāra in which a child is given a name, before the family and the fire.', hi: 'वह संस्कार जिसमें परिवार और अग्नि के समक्ष शिशु को नाम दिया जाता है।' },
    outline: [...COMMON_OUTLINE,
      { en: 'Pūjana and a short havan', hi: 'पूजन और संक्षिप्त हवन' },
      { en: 'The father or an elder whispers the name to the child', hi: 'पिता या बड़े-बुज़ुर्ग शिशु के कान में नाम कहते हैं' },
      { en: 'Blessings of the elders', hi: 'बड़ों का आशीर्वाद' },
      ...CLOSING],
    samagri: [
      { en: 'New clothes for the child; honey', hi: 'शिशु के लिए नए वस्त्र; शहद' },
      { en: 'A plate of rice on which the name is written', hi: 'चावल की थाली जिस पर नाम लिखा जाता है' },
    ],
    havan: true, when: [],
  },
  {
    key: 'annaprashan', kind: 'samskara', minutes: 60,
    name: { en: 'Annaprāśana — the first food', hi: 'अन्नप्राशन संस्कार' },
    purpose: { en: 'The saṁskāra of a child’s first solid food, usually in the sixth month or after.', hi: 'शिशु के पहले अन्न-ग्रहण का संस्कार, प्रायः छठे माह या उसके बाद।' },
    outline: [...COMMON_OUTLINE,
      { en: 'Pūjana; the food is offered first to the deity', hi: 'पूजन; अन्न पहले देवता को अर्पित' },
      { en: 'The child is fed the first morsel of khīr by the elders', hi: 'बड़े शिशु को खीर का पहला ग्रास खिलाते हैं' },
      ...CLOSING],
    samagri: [
      { en: 'Khīr (rice cooked in milk) in a silver or clean new bowl', hi: 'खीर, चाँदी या नई स्वच्छ कटोरी में' },
      { en: 'New clothes for the child', hi: 'शिशु के लिए नए वस्त्र' },
    ],
    when: [],
  },
  {
    key: 'mundan', kind: 'samskara', minutes: 60,
    name: { en: 'Muṇḍana — the first haircut', hi: 'मुंडन (चूड़ाकर्म) संस्कार' },
    purpose: { en: 'The cūḍākaraṇa saṁskāra, a child’s first tonsure. Over video the pandit leads the rite while the family and the barber are together at home.', hi: 'चूड़ाकर्म संस्कार, शिशु का पहला मुंडन। वीडियो पर पंडित जी विधि कराते हैं; परिवार और नाई घर पर साथ रहते हैं।' },
    outline: [...COMMON_OUTLINE,
      { en: 'Pūjana and a short havan', hi: 'पूजन और संक्षिप्त हवन' },
      { en: 'The first locks are cut to the mantras; the tonsure follows', hi: 'मंत्रों के साथ पहली लटें काटी जाती हैं; फिर मुंडन' },
      ...CLOSING],
    samagri: [
      { en: 'New clothes for the child; a clean cloth and a plate for the hair', hi: 'शिशु के नए वस्त्र; केशों के लिए स्वच्छ वस्त्र और थाली' },
      { en: 'Haldī and curd for the head afterwards', hi: 'बाद में सिर पर लगाने के लिए हल्दी और दही' },
    ],
    havan: true, when: [],
  },
  {
    key: 'shraddha', kind: 'puja', minutes: 90,
    name: { en: 'Śrāddha · Pitṛ Tarpaṇa', hi: 'श्राद्ध · पितृ तर्पण' },
    purpose: { en: 'The offering of water, sesame and piṇḍa to the ancestors — on the tithi of a passing, on Amāvāsyā, and through Pitṛ Pakṣa.', hi: 'पितरों को जल, तिल और पिंड का अर्पण — पुण्यतिथि पर, अमावस्या पर, और पितृ पक्ष में।' },
    outline: [
      { en: 'Saṅkalpa naming the ancestors and the gotra', hi: 'पितरों और गोत्र के नाम सहित संकल्प' },
      { en: 'Tarpaṇa with water, black sesame and kuśa', hi: 'जल, काले तिल और कुश से तर्पण' },
      { en: 'Piṇḍa-dāna where the family keeps it; food set aside and given', hi: 'जहाँ परंपरा हो वहाँ पिंडदान; भोजन निकालकर दान' },
    ],
    samagri: [
      { en: 'Black sesame, barley, kuśa grass', hi: 'काले तिल, जौ, कुश' },
      { en: 'Cooked rice (for piṇḍa), milk, honey, ghee', hi: 'पके चावल (पिंड हेतु), दूध, शहद, घी' },
      { en: 'A copper vessel and a plate; white flowers', hi: 'ताँबे का पात्र और थाली; सफ़ेद फूल' },
    ],
    base: false, when: ['amavasya'],
  },
  {
    key: 'vahan', kind: 'puja', minutes: 30,
    name: { en: 'Vāhana Pūjā', hi: 'वाहन पूजा' },
    purpose: { en: 'A short pūjā for a new vehicle before its first journey.', hi: 'नए वाहन की पहली यात्रा से पहले संक्षिप्त पूजा।' },
    outline: [
      { en: 'Saṅkalpa and Gaṇeśa pūjana', hi: 'संकल्प और गणेश पूजन' },
      { en: 'Svastika and tilaka on the vehicle; a garland; a coconut broken before it', hi: 'वाहन पर स्वस्तिक और तिलक; माला; सामने नारियल फोड़ना' },
      { en: 'Āratī; the vehicle is driven over lemons where the family keeps it', hi: 'आरती; जहाँ परंपरा हो वहाँ नींबू पर से वाहन चलाना' },
    ],
    samagri: [
      { en: 'A coconut, a garland, roli, akṣata, incense, a dīpa', hi: 'नारियल, माला, रोली, अक्षत, अगरबत्ती, दीपक' },
      { en: 'Four lemons, sweets', hi: 'चार नींबू, मिठाई' },
    ],
    base: false, when: ['vijayadashami', 'akshaya-tritiya', 'dhanteras'],
  },
  {
    key: 'janmadin', kind: 'havan', minutes: 90,
    name: { en: 'Janmadina Pūjā & Āyuṣya Havan', hi: 'जन्मदिन पूजा एवं आयुष्य हवन' },
    purpose: { en: 'A birthday kept the traditional way: pūjā, a havan for long life, and the blessings of the elders.', hi: 'पारंपरिक रीति से जन्मदिन: पूजन, दीर्घायु के लिए हवन, और बड़ों का आशीर्वाद।' },
    outline: [...COMMON_OUTLINE,
      { en: 'Pūjana of the family deity', hi: 'कुलदेवता का पूजन' },
      { en: 'Āyuṣya havan and pūrṇāhuti', hi: 'आयुष्य हवन और पूर्णाहुति' },
      { en: 'Tilaka and blessings', hi: 'तिलक और आशीर्वाद' },
      ...CLOSING],
    samagri: [
      { en: 'New clothes for the one whose birthday it is', hi: 'जिसका जन्मदिन है उसके लिए नए वस्त्र' },
    ],
    havan: true, when: [],
  },
]

export const KIND_LABEL = {
  puja: { en: 'Pūjā', hi: 'पूजा' }, havan: { en: 'Havan', hi: 'हवन' },
  path: { en: 'Pāṭha', hi: 'पाठ' }, samskara: { en: 'Saṁskāra', hi: 'संस्कार' },
}

export const ritualByKey = (k) => RITUALS.find((r) => r.key === k) || null
/** Rituals traditionally kept on an observance the calendar emits. */
export const ritualsFor = (festivalKey) => RITUALS.filter((r) => r.when.includes(festivalKey))
export const samagriFor = (r) => [...(r.base === false ? [] : BASE_SAMAGRI), ...(r.havan ? HAVAN_SAMAGRI : []), ...r.samagri]
export const durationLabel = (m, hi) => {
  const h = Math.floor(m / 60), mm = m % 60
  return hi ? `${h ? `${h} घं ` : ''}${mm ? `${mm} मि` : ''}`.trim() : `${h ? `${h} h ` : ''}${mm ? `${mm} min` : ''}`.trim()
}
