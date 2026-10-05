/**
 * Śrī Hanumān Cālīsā — the full text, for the guided pāṭha.
 *
 * Gosvāmī Tulasīdāsa, sixteenth century, in Awadhi: two opening dohās, forty
 * chaupāīs (cālīsa = forty), one closing dohā. The text is his and long out of
 * copyright; it is given whole, in Devanāgarī and in a plain roman reading to
 * say it from.
 *
 * THE TEXT was written out and then checked, verse by verse, against two
 * independent copies (sanskritdocuments.org "shrI hanumAna chAlIsA" and Kavitā
 * Kośa "श्री हनुमान चालीसा"). They agree on every verse; where printings spell
 * a word differently the common reading is kept:
 *   dohā 2    "बल बुधि बिद्या"  (also printed "बल बुद्धि बिद्या")
 *   verse 23  "सम्हारो"         (one copy's "संहारो" is a transliteration slip)
 *   verse 39  "हनुमान चलीसा"    (short, for the metre — as both copies print it)
 * A pandit of the roster should still read it through once before it is led.
 *
 * WHAT THE EXPLANATIONS ARE. Each passage has a line saying what its verses
 * speak of. That is an outline, not a translation: this project does not
 * translate scripture itself (CLAUDE.md). Where the verses say what recitation
 * gives, the outline reports it as the poet's word and promises nothing.
 *
 * The forty chaupāīs are given in five passages of eight, so that each can be
 * followed on one screen and recorded by a pandit as one take.
 */

const doha1 = {
  dev: `श्रीगुरु चरन सरोज रज, निज मनु मुकुरु सुधारि।
बरनउँ रघुबर बिमल जसु, जो दायकु फल चारि॥

बुद्धिहीन तनु जानिके, सुमिरौं पवन-कुमार।
बल बुधि बिद्या देहु मोहिं, हरहु कलेस बिकार॥`,
  roman: `Shri Guru charan saroj raj, nij manu mukuru sudhari
Baranau Raghubar bimal jasu, jo dayaku phal chari

Buddhihin tanu janike, sumirau Pavan-kumar
Bal budhi bidya dehu mohi, harahu kales bikar`,
}

const chaupai = [
  [
    ['जय हनुमान ज्ञान गुन सागर। जय कपीस तिहुँ लोक उजागर॥', 'Jay Hanuman gyan gun sagar · Jay Kapis tihu lok ujagar'],
    ['राम दूत अतुलित बल धामा। अंजनि-पुत्र पवनसुत नामा॥', 'Ram doot atulit bal dhama · Anjani-putra Pavansut nama'],
    ['महाबीर बिक्रम बजरंगी। कुमति निवार सुमति के संगी॥', 'Mahabir bikram Bajrangi · Kumati nivar sumati ke sangi'],
    ['कंचन बरन बिराज सुबेसा। कानन कुंडल कुंचित केसा॥', 'Kanchan baran biraj subesa · Kanan kundal kunchit kesa'],
    ['हाथ बज्र औ ध्वजा बिराजै। काँधे मूँज जनेऊ साजै॥', 'Hath bajra au dhvaja birajai · Kandhe munj janeu sajai'],
    ['संकर सुवन केसरीनंदन। तेज प्रताप महा जग बंदन॥', 'Sankar suvan Kesarinandan · Tej pratap maha jag bandan'],
    ['बिद्यावान गुनी अति चातुर। राम काज करिबे को आतुर॥', 'Bidyavan guni ati chatur · Ram kaj karibe ko atur'],
    ['प्रभु चरित्र सुनिबे को रसिया। राम लखन सीता मन बसिया॥', 'Prabhu charitra sunibe ko rasiya · Ram Lakhan Sita man basiya'],
  ],
  [
    ['सूक्ष्म रूप धरि सियहिं दिखावा। बिकट रूप धरि लंक जरावा॥', 'Sukshma roop dhari Siyahi dikhava · Bikat roop dhari Lank jarava'],
    ['भीम रूप धरि असुर सँहारे। रामचंद्र के काज सँवारे॥', 'Bhim roop dhari asur sanhare · Ramchandra ke kaj sanvare'],
    ['लाय सजीवन लखन जियाये। श्रीरघुबीर हरषि उर लाये॥', 'Laay sajivan Lakhan jiyaye · Shri Raghubir harashi ur laye'],
    ['रघुपति कीन्ही बहुत बड़ाई। तुम मम प्रिय भरतहि सम भाई॥', 'Raghupati kinhi bahut badai · Tum mam priya Bharatahi sam bhai'],
    ['सहस बदन तुम्हरो जस गावैं। अस कहि श्रीपति कंठ लगावैं॥', 'Sahas badan tumharo jas gavai · As kahi Shripati kanth lagavai'],
    ['सनकादिक ब्रह्मादि मुनीसा। नारद सारद सहित अहीसा॥', 'Sanakadik Brahmadi munisa · Narad Sarad sahit Ahisa'],
    ['जम कुबेर दिगपाल जहाँ ते। कबि कोबिद कहि सके कहाँ ते॥', 'Jam Kuber digpal jahan te · Kabi kobid kahi sake kahan te'],
    ['तुम उपकार सुग्रीवहिं कीन्हा। राम मिलाय राज पद दीन्हा॥', 'Tum upkar Sugrivahi kinha · Ram milay raj pad dinha'],
  ],
  [
    ['तुम्हरो मंत्र बिभीषन माना। लंकेस्वर भए सब जग जाना॥', 'Tumharo mantra Bibhishan mana · Lankeshvar bhae sab jag jana'],
    ['जुग सहस्र जोजन पर भानू। लील्यो ताहि मधुर फल जानू॥', 'Jug sahasra jojan par bhanu · Lilyo tahi madhur phal janu'],
    ['प्रभु मुद्रिका मेलि मुख माहीं। जलधि लाँघि गये अचरज नाहीं॥', 'Prabhu mudrika meli mukh mahi · Jaladhi langhi gaye acharaj nahi'],
    ['दुर्गम काज जगत के जेते। सुगम अनुग्रह तुम्हरे तेते॥', 'Durgam kaj jagat ke jete · Sugam anugrah tumhare tete'],
    ['राम दुआरे तुम रखवारे। होत न आज्ञा बिनु पैसारे॥', 'Ram duare tum rakhvare · Hot na agya binu paisare'],
    ['सब सुख लहै तुम्हारी सरना। तुम रच्छक काहू को डर ना॥', 'Sab sukh lahai tumhari sarna · Tum rachchhak kahu ko dar na'],
    ['आपन तेज सम्हारो आपै। तीनों लोक हाँक तें काँपै॥', 'Aapan tej samharo aapai · Tino lok hank te kanpai'],
    ['भूत पिसाच निकट नहिं आवै। महाबीर जब नाम सुनावै॥', 'Bhoot pisach nikat nahi avai · Mahabir jab nam sunavai'],
  ],
  [
    ['नासै रोग हरै सब पीरा। जपत निरंतर हनुमत बीरा॥', 'Nasai rog harai sab pira · Japat nirantar Hanumat bira'],
    ['संकट तें हनुमान छुड़ावै। मन क्रम बचन ध्यान जो लावै॥', 'Sankat te Hanuman chhudavai · Man kram bachan dhyan jo lavai'],
    ['सब पर राम तपस्वी राजा। तिन के काज सकल तुम साजा॥', 'Sab par Ram tapasvi raja · Tin ke kaj sakal tum saja'],
    ['और मनोरथ जो कोई लावै। सोई अमित जीवन फल पावै॥', 'Aur manorath jo koi lavai · Soi amit jivan phal pavai'],
    ['चारों जुग परताप तुम्हारा। है परसिद्ध जगत उजियारा॥', 'Charo jug partap tumhara · Hai parasiddh jagat ujiyara'],
    ['साधु संत के तुम रखवारे। असुर निकंदन राम दुलारे॥', 'Sadhu sant ke tum rakhvare · Asur nikandan Ram dulare'],
    ['अष्ट सिद्धि नौ निधि के दाता। अस बर दीन जानकी माता॥', 'Asht siddhi nau nidhi ke data · As bar din Janaki mata'],
    ['राम रसायन तुम्हरे पासा। सदा रहो रघुपति के दासा॥', 'Ram rasayan tumhare pasa · Sada raho Raghupati ke dasa'],
  ],
  [
    ['तुम्हरे भजन राम को पावै। जनम जनम के दुख बिसरावै॥', 'Tumhare bhajan Ram ko pavai · Janam janam ke dukh bisravai'],
    ['अंत काल रघुबर पुर जाई। जहाँ जन्म हरिभक्त कहाई॥', 'Ant kal Raghubar pur jai · Jahan janma Haribhakt kahai'],
    ['और देवता चित्त न धरई। हनुमत सेइ सर्ब सुख करई॥', 'Aur devta chitt na dharai · Hanumat sei sarb sukh karai'],
    ['संकट कटै मिटै सब पीरा। जो सुमिरै हनुमत बलबीरा॥', 'Sankat katai mitai sab pira · Jo sumirai Hanumat balbira'],
    ['जै जै जै हनुमान गोसाईं। कृपा करहु गुरुदेव की नाईं॥', 'Jai jai jai Hanuman gosai · Kripa karahu gurudev ki nai'],
    ['जो सत बार पाठ कर कोई। छूटहि बंदि महा सुख होई॥', 'Jo sat bar path kar koi · Chhutahi bandi maha sukh hoi'],
    ['जो यह पढ़ै हनुमान चलीसा। होय सिद्धि साखी गौरीसा॥', 'Jo yah padhai Hanuman Chalisa · Hoy siddhi sakhi Gaurisa'],
    ['तुलसीदास सदा हरि चेरा। कीजै नाथ हृदय महँ डेरा॥', 'Tulsidas sada Hari chera · Kijai nath hriday mah dera'],
  ],
]

const doha2 = {
  dev: `पवनतनय संकट हरन, मंगल मूरति रूप।
राम लखन सीता सहित, हृदय बसहु सुर भूप॥`,
  roman: `Pavan-tanay sankat haran, mangal murati roop
Ram Lakhan Sita sahit, hriday basahu sur bhoop`,
}

const verse = (v) => ({ ...v, lang: 'awa', iast: '' })
const passage = (k) => verse({ dev: chaupai[k].map((c) => c[0]).join('\n'), roman: chaupai[k].map((c) => c[1]).join('\n') })
const HIS = {
  en: 'These are the poet’s own words; they are given here as his. The recitation is an act of devotion, and nothing is promised of it.',
  hi: 'ये कवि के अपने शब्द हैं; यहाँ उन्हीं के रूप में दिए गए हैं। पाठ भक्ति का कार्य है, और इसका कोई फल वादा नहीं किया जाता।',
}

/** The seven passages, keyed as steps of the ceremony script (see guide.js). */
export const CHALISA_STEPS = {
  hcDoha1: {
    title: { en: 'The opening dohās', hi: 'आरंभ के दोहे' },
    mantra: verse(doha1),
    what: { en: 'The two dohās that open the Cālīsā: the poet bows at his guru’s feet before he tells of Rāma’s glory, and, calling on Hanumān the son of the Wind, asks for strength, understanding and knowledge.', hi: 'चालीसा के आरंभ के दो दोहे: कवि श्रीराम का यश कहने से पहले गुरु के चरणों में नमन करता है, और पवनकुमार हनुमान जी का स्मरण कर बल, बुद्धि और विद्या माँगता है।' },
    why: { en: 'Every recitation begins here — with humility before the guru, and with what is asked of Hanumān.', hi: 'हर पाठ यहीं से आरंभ होता है — गुरु के प्रति विनय से, और हनुमान जी से जो माँगा जाता है उससे।' },
    more: { en: 'Sit before the picture of Hanumān with the lamp lit; fold your hands and begin together, at an even pace.', hi: 'हनुमान जी के चित्र के सामने बैठें, दीपक जला हो; हाथ जोड़ें और सब एक लय में साथ आरंभ करें।' },
  },
  hcChaupai1: {
    title: { en: 'Chaupāīs 1–8 — who Hanumān is', hi: 'चौपाई १–८ — हनुमान जी का स्वरूप' },
    mantra: passage(0),
    what: { en: 'The praise opens with Hanumān himself: ocean of wisdom and virtue; Rāma’s messenger, of matchless strength; son of Añjanī, called son of the Wind; his golden form, the thunderbolt and the banner in his hands; learned, skilful, ever eager for Rāma’s work and to hear the Lord’s story.', hi: 'स्तुति हनुमान जी के स्वरूप से आरंभ होती है: ज्ञान और गुणों के सागर; श्रीराम के दूत, अतुलित बल के धाम; अंजनी के पुत्र, पवनसुत कहलाने वाले; उनका स्वर्ण-वर्ण, हाथ में वज्र और ध्वजा; विद्वान, गुणी, राम-काज के लिए सदा आतुर और प्रभु का चरित्र सुनने के रसिक।' },
    why: { en: 'To praise is to bring to mind: the recitation first sets before the family who it is they are calling on.', hi: 'स्तुति करना स्मरण करना है: पाठ सबसे पहले परिवार के सामने यह रखता है कि वे किसे पुकार रहे हैं।' },
    more: { en: 'Each line is one chaupāī. Where the family is reading together, one voice may lead the first half of the line and all join the second.', hi: 'हर पंक्ति एक चौपाई है। जहाँ परिवार साथ पढ़ रहा हो, एक स्वर पंक्ति का पहला भाग कहे और दूसरा भाग सब मिलकर।' },
  },
  hcChaupai2: {
    title: { en: 'Chaupāīs 9–16 — what he did', hi: 'चौपाई ९–१६ — उनके कार्य' },
    mantra: passage(1),
    what: { en: 'His deeds in Rāma’s story: the tiny form in which he came before Sītā, and the fearsome one in which he burned Laṅkā; the Sañjīvanī brought to revive Lakṣmaṇa; Rāma’s embrace and his praise — dear to him as his brother Bharata; the sages and gods who cannot tell his glory; and Sugrīva brought to Rāma, and to his kingdom.', hi: 'रामकथा में उनके कार्य: वह सूक्ष्म रूप जिसमें वे सीता जी के सामने आए, और वह विकट रूप जिसमें लंका जलाई; लक्ष्मण जी को जिलाने के लिए लाई गई संजीवनी; श्रीराम का उन्हें हृदय से लगाना और सराहना — भरत के समान प्रिय भाई; मुनि और देवता जो उनका यश नहीं कह पाते; और सुग्रीव, जिन्हें उन्होंने श्रीराम से मिलाया और राज्य दिलाया।' },
    why: { en: 'The Cālīsā tells the Rāmāyaṇa’s Hanumān in a few lines, so that the whole story is remembered in the saying of it.', hi: 'चालीसा कुछ ही पंक्तियों में रामायण के हनुमान जी को कह देती है, ताकि कहते-कहते पूरी कथा स्मरण हो आए।' },
  },
  hcChaupai3: {
    title: { en: 'Chaupāīs 17–24 — his power, and his keeping', hi: 'चौपाई १७–२४ — उनका सामर्थ्य और रक्षा' },
    mantra: passage(2),
    what: { en: 'Vibhīṣaṇa, who took his counsel and became lord of Laṅkā; the sun he leapt at, taking it for a sweet fruit; the ocean crossed with Rāma’s ring in his mouth; every hard task of the world made easy by his grace; he who keeps Rāma’s door; those in his refuge, who fear nothing; and the spirits that do not come near where his name is spoken.', hi: 'विभीषण, जिन्होंने उनका मंत्र माना और लंकेश्वर हुए; सूर्य, जिसे उन्होंने मधुर फल जानकर निगल लिया; प्रभु की मुद्रिका मुख में रखकर लाँघा गया समुद्र; जगत के हर दुर्गम कार्य का उनकी कृपा से सुगम होना; श्रीराम के द्वार के रखवाले; उनकी शरण में आए जन, जिन्हें किसी का डर नहीं; और भूत-पिशाच, जो उनका नाम सुनते ही पास नहीं आते।' },
    why: { en: 'Here the praise turns from what he did to what he is for those who call on him: a protector.', hi: 'यहाँ स्तुति उनके किए से हटकर इस पर आती है कि पुकारने वालों के लिए वे क्या हैं: रक्षक।' },
  },
  hcChaupai4: {
    title: { en: 'Chaupāīs 25–32 — what his remembrance gives', hi: 'चौपाई २५–३२ — उनके स्मरण का फल' },
    mantra: passage(3),
    what: { en: 'The poet tells what comes to one who keeps Hanumān in mind: illness and pain removed for the one who repeats his name; release from trouble for the one who holds him in thought, deed and word; his glory in all four ages; guardian of the good and the saintly; giver of the eight siddhis and the nine nidhis, by Mother Jānakī’s boon; and for ever the servant of Raghupati.', hi: 'कवि बताता है कि हनुमान जी को मन में रखने वाले को क्या मिलता है: उनके नाम का निरंतर जप करने वाले के रोग और पीड़ा का नाश; मन, कर्म और वचन से उनका ध्यान करने वाले का संकट से छूटना; चारों युगों में उनका प्रताप; साधु-संतों के रखवाले; माता जानकी के वरदान से अष्ट सिद्धि और नौ निधि के दाता; और सदा रघुपति के दास।' },
    why: HIS,
  },
  hcChaupai5: {
    title: { en: 'Chaupāīs 33–40 — the close', hi: 'चौपाई ३३–४० — समापन' },
    mantra: passage(4),
    what: { en: 'The last eight: through devotion to him one comes to Rāma; whoever remembers Hanumān has every trouble cut away; “victory, victory, victory to Lord Hanumān — be gracious as a guru is”; what the poet says of the one who recites this Cālīsā; and his own name — Tulasīdāsa, ever Hari’s servant — asking the Lord to dwell in his heart.', hi: 'अंतिम आठ: उनके भजन से श्रीराम की प्राप्ति; जो हनुमान जी का स्मरण करे उसके सब संकट कट जाते हैं; "जय जय जय हनुमान गोसाईं — गुरुदेव की भाँति कृपा कीजिए"; इस चालीसा का पाठ करने वाले के विषय में कवि का कथन; और कवि का अपना नाम — तुलसीदास, सदा हरि के दास — जो प्रभु से अपने हृदय में वास करने की प्रार्थना करता है।' },
    why: HIS,
  },
  hcDoha2: {
    title: { en: 'The closing dohā', hi: 'समापन का दोहा' },
    mantra: verse(doha2),
    what: { en: 'The dohā that closes the Cālīsā: Hanumān, son of the Wind, remover of troubles, is asked to dwell in the heart — together with Rāma, Lakṣmaṇa and Sītā.', hi: 'चालीसा का समापन-दोहा: संकट हरने वाले पवनतनय हनुमान जी से प्रार्थना है कि वे श्रीराम, लक्ष्मण और सीता जी सहित हृदय में वास करें।' },
    why: { en: 'The recitation ends as it began, with a prayer — no longer for strength, but for his presence.', hi: 'पाठ वैसे ही समाप्त होता है जैसे आरंभ हुआ था, प्रार्थना से — अब बल के लिए नहीं, उनकी उपस्थिति के लिए।' },
    more: { en: 'Where the Cālīsā is being said more than once, begin again from the opening dohās; after the last time, go on to the āratī.', hi: 'जहाँ चालीसा एक से अधिक बार पढ़ी जा रही हो, वहाँ आरंभ के दोहों से फिर शुरू करें; अंतिम बार के बाद आरती करें।' },
  },
}

export const CHALISA_ORDER = ['deepa', 'hcDoha1', 'hcChaupai1', 'hcChaupai2', 'hcChaupai3', 'hcChaupai4', 'hcChaupai5', 'hcDoha2', 'aarti', 'prasada']

export const CHALISA_ABOUT = {
  en: 'The Hanumān Cālīsā is forty verses in praise of Hanumān — cālīsa means forty — composed in Awadhi by Gosvāmī Tulasīdāsa, the poet of the Rāmacaritamānasa, in the sixteenth century. Two dohās open it and one closes it. It tells who Hanumān is, what he did in Rāma’s story, and what he is to those who call on him: strength, courage, and a guard against fear. It is among the most recited of all devotional texts — said daily in many homes, on Tuesdays and Saturdays, on Hanumān Jayantī, and whenever steadiness is needed. A single recitation takes under ten minutes, and needs nothing but a lamp and the text.',
  hi: 'हनुमान चालीसा हनुमान जी की स्तुति के चालीस छंद हैं, जिन्हें रामचरितमानस के कवि गोस्वामी तुलसीदास ने सोलहवीं शताब्दी में अवधी में रचा। दो दोहों से यह आरंभ होती है और एक दोहे से समाप्त। यह बताती है कि हनुमान जी कौन हैं, रामकथा में उन्होंने क्या किया, और पुकारने वालों के लिए वे क्या हैं: बल, साहस, और भय से रक्षा। यह सबसे अधिक पढ़े जाने वाले भक्ति-पाठों में है — अनेक घरों में प्रतिदिन, मंगलवार और शनिवार को, हनुमान जयंती पर, और जब भी धैर्य की आवश्यकता हो। एक पाठ में दस मिनट से कम लगते हैं, और एक दीपक तथा पाठ के अतिरिक्त कुछ नहीं चाहिए।',
}

/** Every chaupāī, in order — for the count that gives the Cālīsā its name. */
export const CHAUPAIS = chaupai.flat()
