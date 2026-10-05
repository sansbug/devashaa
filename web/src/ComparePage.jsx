/**
 * /compare — "Why your chart differs between apps, and which number is right."
 *
 * One real nativity (25 June 1975, 22:30 IST, Kanpur), this engine, NASA's
 * JPL Horizons, and a popular app's printed report of the same birth, laid
 * side by side. Every figure here is pinned in api/test_reference_chart.py,
 * so the page cannot drift from the engine. Where the other app's number is a
 * different convention, the page says so; where it is an error, it shows the
 * ephemeris value and lets the reader see.
 */
const ROWS = [
  ['Sūrya', 'Mithuna 10°00′00″', 'Mithuna 10°00′00″', '0.0″'],
  ['Candra', 'Makara 03°35′57″', 'Makara 03°35′58″', '0.1″'],
  ['Maṅgala', 'Meṣa 02°34′32″', 'Meṣa 02°34′32″', '0.0″'],
  ['Budha', 'Vṛṣabha 21°51′44″', 'Vṛṣabha 21°51′44″', '0.0″'],
  ['Guru', 'Mīna 27°21′21″', 'Mīna 27°21′21″', '0.0″'],
  ['Śukra', 'Karka 25°10′59″', 'Karka 25°10′59″', '0.0″'],
  ['Śani', 'Mithuna 26°25′23″', 'Mithuna 26°25′23″', '0.1″'],
]

const C = {
  en: {
    back: '← back to the chart',
    title: 'Why your chart differs between apps',
    lede: 'Cast the same birth in two apps and the numbers rarely match to the second: a planet a few minutes of arc away, a daśā that starts a day — or seven months — apart, a strength total that disagrees. Here is one real birth, this engine, NASA’s ephemeris, and a popular app’s printed report of the same chart, side by side — with the cause of every difference and, where there is one, the right number.',
    birth: 'The birth: 25 June 1975, 22:30 IST, Kanpur (26.46523 N, 80.34975 E) — Julian Day 2442589.2083, sidereal (Lahiri). Every figure below is pinned in the engine’s test suite, so this page cannot drift from what the site computes.',
    s1h: '1. Planet positions: check them against the ephemeris',
    s1p: 'A position is not a matter of opinion. NASA’s JPL Horizons publishes the apparent geocentric longitude of every planet for any instant; subtract the ayanāṁśa and you have the sidereal degree every Jyotiṣa app should print. This engine’s seven bodies agree with JPL to a tenth of an arcsecond:',
    tbl1: ['Graha', 'This site', 'JPL Horizons', 'Difference'],
    s1q: 'The other app’s report prints six of the seven within 20″ of JPL — and Saturn at Mithuna 26°29′50″, which is 4.5 arcminutes from the ephemeris (JPL and this site: 26°25′23″). That is not a convention; it is their ephemeris. 4.5′ is small on a birth chart, but it is the kind of difference that moves a planet across a navāṁśa boundary, and it is why we show the JD and ayanāṁśa on every chart: you can repeat the check yourself.',
    s2h: '2. The ayanāṁśa: true or mean Lahiri',
    s2p: 'Both apps use Lahiri. This site prints the true value (mean + nutation) — 23°31′08″ at this birth — the other prints the mean, 23°30′53″. The difference is the nutation in longitude, about 15″; both engines apply it to the positions, so the degrees agree either way. Only the printed ayanāṁśa differs. Where apps differ by whole arcminutes in their positions, it is never this: look for a different ayanāṁśa entirely (Raman, KP, Fagan–Bradley) or an ephemeris error.',
    s3h: '3. Daśā dates: the length of a year',
    s3p: 'Viṁśottarī runs 120 years from the Moon’s nakṣatra. The one choice that moves every date is how long a "year" is. This site’s default is the 365.25-day year; the labelled alternative is the 360-day sāvana year some apps use. On this birth:',
    tbl3: ['Period', '365.25-day year (this site)', 'The other app', '360-day year'],
    r3: [
      ['Balance at birth', '2y 10m 17d', '2y 10m 17d', '2y 10m 17d'],
      ['Guru mahādaśā', '2013-05-12 → 2029-05-12', '2013-05-13 → 2029-05-13', '2012-10-25 → 2028-08-02'],
      ['Maṅgala antardaśā', '2026-01-11 → 2026-12-18', '2026-01-13 → 2026-12-19', '2025-04-20 → 2026-03-22'],
    ],
    s3q: 'Same convention, one day apart: the other app starts each period a day later than this engine, a rounding of the balance at birth. A different convention, seven months apart: an app on the 360-day year will tell you Guru began in October 2012, not May 2013. When two daśā tables disagree by months, this is almost always the reason — and a reader should know which year their app uses. The Daśā tab here shows both.',
    s4h: '4. Ṣaḍbala: where the texts leave a choice',
    s4p: 'The six strengths add up differently between apps, and most of the gap is two rules the texts state in a way that two careful readers can take two ways. This engine documents its choice on each:',
    r4: [
      ['Horā bala', 'Equal twenty-fourths from sunrise (Raman, Art. 68–70) — the horā lord here is Guru, who takes the 60 virūpa.', 'Day and night each divided into twelve unequal parts — the horā lord becomes Śani.'],
      ['Dṛk bala (Śani)', 'Aspects netted with their sign (Art. 120): −9.5 virūpa.', 'A different netting convention: +13.3.'],
      ['Sthāna bala (Sūrya)', '244.4 virūpa.', '199.4 virūpa — see §5: the Sun sits on a cusp.'],
    ],
    tbl4: ['Component', 'This site', 'The other app'],
    s4q: 'Four of the six components — dik, naisargika, and the cheṣṭā of Maṅgala and Śani, and the sthāna of every body but the Sun — agree between the two engines to a tenth of a virūpa. The differences are choices, and we show ours on the Strength tab beside the total.',
    s5h: '5. A planet on a boundary: when neither app is wrong',
    s5p: 'This Sun stands at Mithuna 9.999977° — 0.08 arcseconds before 10°00′, which is both a drekkāṇa boundary and a navāṁśa boundary. That is two seconds of birth time. This engine puts the Sun in the first drekkāṇa and the Dhanu navāṁśa; an engine whose Sun lands 18″ later puts it in the second drekkāṇa and Makara. Three sthāna-bala rules flip on that, 44 virūpa in all — the whole of the Sun’s difference in §4. The birth time is not known to two seconds; neither number is wrong. An honest engine should flag a body that close to a cusp, and this one will.',
    s6h: '6. The annual chart: the first Mudda period',
    s6p: 'In Varṣaphala, the first Mudda daśā period is prorated by the un-traversed part of the janma nakṣatra (Charak, ch. V) — this site’s default — or left whole, which some software does. The nine boundaries of the year shift by about 25 days between the two. The Varṣaphala tab shows both; the unprorated variant matches the other app’s nine dates to the day.',
    s7h: 'How to check any chart yourself',
    s7: [
      'Read the JD and ayanāṁśa off the chart’s header; every app should print them, and a chart that hides them cannot be checked.',
      'Enter the instant at JPL Horizons (ssd.jpl.nasa.gov/horizons) as an observer at the Earth’s centre; take the apparent ecliptic longitude of date.',
      'Subtract the ayanāṁśa. That is the sidereal longitude. If an app’s planet is more than an arcminute away, it is the app.',
      'For daśā dates, find which year length the app uses. For strengths, ask which horā rule and which aspect netting — the texts allow both.',
    ],
    foot: 'Every number on this page is pinned in the engine’s test suite (api/test_reference_chart.py, open source); the external values come from JPL Horizons, retrieved 29 Sep 2026, and from a printed report of 1 Jan 2026. The site’s own checks are on "How we check the math".',
  },
  hi: {
    back: '← कुंडली पर वापस',
    title: 'अलग-अलग ऐप में आपकी कुंडली क्यों भिन्न होती है',
    lede: 'एक ही जन्म दो ऐप में डालें — अंक शायद ही मिलें: कोई ग्रह कुछ कला दूर, कोई दशा एक दिन — या सात महीने — आगे-पीछे, बल का योग अलग। यहाँ एक वास्तविक जन्म, यह इंजन, नासा की एफ़ेमेरिस और एक लोकप्रिय ऐप की उसी कुंडली की छपी रिपोर्ट आमने-सामने हैं — हर अंतर के कारण के साथ, और जहाँ सही अंक है, वह भी।',
    birth: 'जन्म: 25 जून 1975, 22:30 IST, कानपुर (26.46523 उ., 80.34975 पू.) — जूलियन दिन 2442589.2083, निरयण (लाहिड़ी)। नीचे का हर अंक इंजन के परीक्षण-सूट में पिन है, अतः यह पृष्ठ साइट की गणना से कभी नहीं भटक सकता।',
    s1h: '1. ग्रह-स्थितियाँ: एफ़ेमेरिस से जाँचें',
    s1p: 'ग्रह की स्थिति राय का विषय नहीं है। नासा का JPL Horizons किसी भी क्षण के लिए हर ग्रह का भूकेन्द्रीय आभासी भोगांश देता है; अयनांश घटाइए और वही निरयण अंश मिलता है जो हर ज्योतिष ऐप को छापना चाहिए। इस इंजन के सातों ग्रह JPL से एक विकला के दसवें भाग तक मिलते हैं:',
    tbl1: ['ग्रह', 'यह साइट', 'JPL Horizons', 'अंतर'],
    s1q: 'दूसरे ऐप की रिपोर्ट सात में से छह ग्रह JPL के 20″ के भीतर छापती है — और शनि मिथुन 26°29′50″ पर, जो एफ़ेमेरिस से 4.5 कला दूर है (JPL और यह साइट: 26°25′23″)। यह कोई परिपाटी नहीं, उनकी एफ़ेमेरिस है। जन्म-कुंडली में 4.5′ छोटा लगता है, पर इतना अंतर ग्रह को नवांश की सीमा पार करा सकता है — इसीलिए हम हर कुंडली पर JD और अयनांश दिखाते हैं: आप स्वयं जाँच दोहरा सकते हैं।',
    s2h: '2. अयनांश: सत्य या मध्यम लाहिड़ी',
    s2p: 'दोनों ऐप लाहिड़ी अयनांश लेते हैं। यह साइट सत्य मान छापती है (मध्यम + विचलन) — इस जन्म पर 23°31′08″ — दूसरा ऐप मध्यम मान 23°30′53″। अंतर भोगांश का विचलन है, लगभग 15″; दोनों इंजन उसे स्थितियों में लगाते हैं, अतः अंश दोनों ओर मिलते हैं। जहाँ ऐप पूरी कलाओं से भिन्न हों, कारण यह कभी नहीं होता: वहाँ कोई और ही अयनांश (रमण, KP, फ़ेगन–ब्रैडली) या एफ़ेमेरिस की त्रुटि देखिए।',
    s3h: '3. दशा-तिथियाँ: वर्ष की लंबाई',
    s3p: 'विंशोत्तरी चन्द्र-नक्षत्र से 120 वर्ष चलती है। जो एक चुनाव हर तिथि को हिलाता है, वह है “वर्ष” कितना लंबा है। इस साइट का डिफ़ॉल्ट 365.25 दिन का वर्ष है; लेबल-सहित विकल्प 360 दिन का सावन वर्ष, जो कुछ ऐप लेते हैं। इस जन्म पर:',
    tbl3: ['अवधि', '365.25-दिन वर्ष (यह साइट)', 'दूसरा ऐप', '360-दिन वर्ष'],
    r3: [
      ['जन्म-शेष', '2व 10मा 17दि', '2व 10मा 17दि', '2व 10मा 17दि'],
      ['गुरु महादशा', '2013-05-12 → 2029-05-12', '2013-05-13 → 2029-05-13', '2012-10-25 → 2028-08-02'],
      ['मंगल अंतर्दशा', '2026-01-11 → 2026-12-18', '2026-01-13 → 2026-12-19', '2025-04-20 → 2026-03-22'],
    ],
    s3q: 'एक ही परिपाटी, एक दिन का अंतर: दूसरा ऐप हर अवधि एक दिन बाद शुरू करता है — जन्म-शेष की गोलाई। भिन्न परिपाटी, सात महीने का अंतर: 360-दिन वर्ष वाला ऐप कहेगा कि गुरु अक्टूबर 2012 में शुरू हुए, मई 2013 में नहीं। जब दो दशा-तालिकाएँ महीनों से भिन्न हों, कारण लगभग सदा यही होता है — और पाठक को पता होना चाहिए कि उसका ऐप कौन-सा वर्ष लेता है। यहाँ दशा टैब दोनों दिखाता है।',
    s4h: '4. षड्बल: जहाँ ग्रन्थ विकल्प छोड़ते हैं',
    s4p: 'छह बलों का योग ऐप-ऐप में भिन्न आता है, और अधिकांश अंतर दो ऐसे नियमों से है जिन्हें ग्रन्थ इस तरह कहते हैं कि दो सावधान पाठक दो तरह ले सकते हैं। यह इंजन हर एक पर अपना चुनाव दर्ज करता है:',
    r4: [
      ['होरा बल', 'सूर्योदय से समान चौबीसवें भाग (रमण, आर्टिकल 68–70) — यहाँ होरेश गुरु, 60 विरूप उन्हें।', 'दिन और रात बारह-बारह असमान भागों में — होरेश शनि हो जाते हैं।'],
      ['दृक् बल (शनि)', 'दृष्टियाँ चिह्न-सहित जोड़ी गईं (आर्ट. 120): −9.5 विरूप।', 'भिन्न जोड़-परिपाटी: +13.3।'],
      ['स्थान बल (सूर्य)', '244.4 विरूप।', '199.4 विरूप — देखें §5: सूर्य सीमा पर है।'],
    ],
    tbl4: ['घटक', 'यह साइट', 'दूसरा ऐप'],
    s4q: 'छह में से चार घटक — दिक्, नैसर्गिक, मंगल-शनि का चेष्टा, और सूर्य को छोड़ हर ग्रह का स्थान बल — दोनों इंजनों में एक विरूप के दसवें भाग तक मिलते हैं। अंतर चुनाव हैं, और हम अपने चुनाव बल टैब पर योग के पास दिखाते हैं।',
    s5h: '5. सीमा पर ग्रह: जब कोई ऐप ग़लत नहीं',
    s5p: 'यह सूर्य मिथुन 9.999977° पर है — 10°00′ से 0.08 विकला पहले, जो द्रेष्काण की भी सीमा है और नवांश की भी। यह जन्म-समय के दो सेकंड हैं। यह इंजन सूर्य को प्रथम द्रेष्काण और धनु नवांश में रखता है; जिस इंजन का सूर्य 18″ आगे पड़े, वह द्वितीय द्रेष्काण और मकर में। तीन स्थान-बल नियम इस पर पलटते हैं, कुल 44 विरूप — §4 का सूर्य का पूरा अंतर। जन्म-समय दो सेकंड तक ज्ञात नहीं; कोई अंक ग़लत नहीं। ईमानदार इंजन को सीमा के इतने निकट ग्रह को चिह्नित करना चाहिए, और यह करेगा।',
    s6h: '6. वर्ष-कुंडली: पहली मुद्दा अवधि',
    s6p: 'वर्षफल में पहली मुद्दा-दशा अवधि जन्म-नक्षत्र के शेष भाग से प्रोरेट की जाती है (चरक, अध्याय V) — इस साइट का डिफ़ॉल्ट — या पूरी रखी जाती है, जो कुछ सॉफ़्टवेयर करते हैं। वर्ष की नौ सीमाएँ दोनों में लगभग 25 दिन खिसकती हैं। वर्षफल टैब दोनों दिखाता है; अप्रोरेटेड विकल्प दूसरे ऐप की नौ तिथियों से दिन-दिन मिलता है।',
    s7h: 'कोई भी कुंडली स्वयं कैसे जाँचें',
    s7: [
      'कुंडली के शीर्ष से JD और अयनांश पढ़ें; हर ऐप को ये छापने चाहिए — जो छिपाए, वह जाँची नहीं जा सकती।',
      'वह क्षण JPL Horizons (ssd.jpl.nasa.gov/horizons) में पृथ्वी-केन्द्र के प्रेक्षक के रूप में डालें; तिथि का आभासी क्रान्ति-भोगांश लें।',
      'अयनांश घटाएँ। यही निरयण भोगांश है। ऐप का ग्रह एक कला से अधिक दूर हो, तो दोष ऐप का है।',
      'दशा-तिथियों के लिए देखें कि ऐप कौन-सी वर्ष-लंबाई लेता है। बलों के लिए पूछें कौन-सा होरा नियम और कौन-सा दृष्टि-जोड़ — ग्रन्थ दोनों की अनुमति देते हैं।',
    ],
    foot: 'इस पृष्ठ का हर अंक इंजन के परीक्षण-सूट में पिन है (api/test_reference_chart.py, ओपन सोर्स); बाहरी मान JPL Horizons (29 सित. 2026) और 1 जन. 2026 की छपी रिपोर्ट से हैं। साइट की अपनी जाँचें “हम गणित की जाँच कैसे करते हैं” पर हैं।',
  },
}

function T({ head, rows, prose }) {
  return (
    <div className="dk-table-wrap">
      <table className={`dk-table cmp-table${prose ? ' cmp-prose' : ''}`}>
        <thead><tr>{head.map((h) => <th key={h}>{h}</th>)}</tr></thead>
        <tbody>{rows.map((r, i) => <tr key={i}>{r.map((c, j) => <td key={j} className={j === 0 ? 'cmp-k' : ''}>{c}</td>)}</tr>)}</tbody>
      </table>
    </div>
  )
}

export default function ComparePage({ onBack, lang = 'en' }) {
  const c = C[lang] || C.en
  return (
    <div className="page privacy methodology compare" lang={lang}>
      <div className="method-top">
        <button type="button" className="privacy-back" onClick={onBack}>{c.back}</button>
      </div>
      <h1>{c.title}</h1>
      <p className="privacy-lede">{c.lede}</p>
      <p className="cmp-birth">{c.birth}</p>
      <section><h2>{c.s1h}</h2><p>{c.s1p}</p><T head={c.tbl1} rows={ROWS} /><p>{c.s1q}</p></section>
      <section><h2>{c.s2h}</h2><p>{c.s2p}</p></section>
      <section><h2>{c.s3h}</h2><p>{c.s3p}</p><T head={c.tbl3} rows={c.r3} /><p>{c.s3q}</p></section>
      <section><h2>{c.s4h}</h2><p>{c.s4p}</p><T head={c.tbl4} rows={c.r4} prose /><p>{c.s4q}</p></section>
      <section><h2>{c.s5h}</h2><p>{c.s5p}</p></section>
      <section><h2>{c.s6h}</h2><p>{c.s6p}</p></section>
      <section><h2>{c.s7h}</h2><ol className="cmp-steps">{c.s7.map((s, i) => <li key={i}>{s}</li>)}</ol></section>
      <p className="cmp-foot">{c.foot}</p>
    </div>
  )
}
