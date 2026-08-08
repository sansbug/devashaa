/**
 * "How we check the math" — the validation / trust page, served at /validation.
 * It presents the actual, verifiable claims about calculation correctness:
 * the Ṣaḍbala reproduced to the virūpa against Raman's Standard Horoscope, the
 * errata found in his printed tables, the daśās checked against BPHS, and the
 * two honest method divergences (Cheṣṭā mean elements, Ayana β=0 kranti).
 *
 * Held to the Privacy-page standard: every number here must be TRUE of the test
 * suite (api/test_shadbala*.py). If a validated figure changes, this page does.
 * Bilingual (English + Devanagari Hindi), driven by the global `lang` choice.
 */
const CONTENT = {
  en: {
    back: '← back to the chart',
    title: 'How we check the math',
    lede: (
      <>
        Most astrology software is a black box you are asked to trust. Devashaa’s
        calculations are checked against the classical texts’ <em>own worked
        examples</em> — and the tests are open for anyone to run.
      </>
    ),
    sections: [
      {
        h: 'Tested against the classics’ own examples',
        p: [
          <>The <em>Ṣaḍbala</em> (six-fold strength) engine reproduces B. V.
            Raman’s worked “Standard Horoscope” <strong>to the virūpa, component
            by component</strong> — 123 checks in all. The final six-fold total
            reconciles to within a single virūpa: the tolerance that absorbs
            Raman’s own printed slips (below).</>,
          <>The daśā systems are validated against the BPHS’ own examples, and
            planetary positions come from the Swiss Ephemeris (JPL DE431) — the
            same data professional astronomy uses.</>,
        ],
      },
      {
        h: 'We correct the source — and say so',
        p: [
          <>Checking against Raman turned up three arithmetic slips in his{' '}
            <em>printed</em> tables. For instance, Mars’s Ochcha bala prints as{' '}
            <strong>37.06</strong>, but his own stated longitude yields{' '}
            <strong>37.17</strong>. Devashaa computes the correct value and
            records the discrepancy.</>,
          <>We neither silently copy an error, nor silently diverge from the
            text.</>,
        ],
      },
      {
        h: 'Where a method differs, we tell you why',
        p: [
          <>Two honest choices are stated on every chart. <em>Cheṣṭā</em> bala
            uses modern mean longitudes — the <em>Seeghrocha</em> the classical
            text never tabulates. <em>Ayana</em> bala takes its declination from
            Raman’s traditional method (a fixed 24° tilt), not the true
            declination. You always know which convention produced a figure.</>,
        ],
      },
      {
        h: 'Check us — don’t trust us',
        p: [
          <>The entire engine and its test suite are open source (AGPL). Every
            figure on this page can be re-run from the code —{' '}
            <a href="https://github.com/sansbug/devashaa" rel="noreferrer">
              github.com/sansbug/devashaa</a>.</>,
        ],
      },
    ],
  },

  hi: {
    back: '← कुंडली पर वापस',
    title: 'हम गणित की जाँच कैसे करते हैं',
    lede: (
      <>
        अधिकतर ज्योतिष सॉफ़्टवेयर एक “ब्लैक बॉक्स” होता है, जिस पर आपसे भरोसा करने
        को कहा जाता है। देवाशा की गणनाएँ शास्त्रों के <em>अपने हल किए गए
        उदाहरणों</em> से जाँची जाती हैं — और परीक्षण सबके लिए खुले हैं, कोई भी
        उन्हें चला सकता है।
      </>
    ),
    sections: [
      {
        h: 'शास्त्रों के अपने उदाहरणों से परखा गया',
        p: [
          <><em>षड्बल</em> (छह-गुना बल) इंजन बी. वी. रमन की हल की गई “स्टैंडर्ड
            होरोस्कोप” को घटक-दर-घटक <strong>विरूप तक</strong> पुनः प्रस्तुत करता
            है — कुल 123 जाँचें। अंतिम छह-गुना योग एक विरूप के भीतर मिलता है — वह
            छूट जो रमन की अपनी छपी गणना-त्रुटियों को समाहित करती है (नीचे देखें)।</>,
          <>दशा पद्धतियाँ बीपीएचएस के अपने उदाहरणों से सत्यापित हैं, और ग्रहों की
            स्थितियाँ स्विस एफ़ेमेरिस (JPL DE431) से आती हैं — वही आँकड़े जो
            पेशेवर खगोलशास्त्र प्रयोग करता है।</>,
        ],
      },
      {
        h: 'हम स्रोत को सुधारते हैं — और यह बताते भी हैं',
        p: [
          <>रमन से मिलान करते समय उनकी <em>छपी</em> तालिकाओं में गणना की तीन
            त्रुटियाँ मिलीं। उदाहरण के लिए, मंगल का उच्चबल <strong>37.06</strong>{' '}
            छपा है, पर उनकी ही बताई गई स्थिति से <strong>37.17</strong> आता है।
            देवाशा सही मान की गणना करता है और इस अंतर को दर्ज करता है।</>,
          <>हम न तो चुपचाप किसी त्रुटि की नकल करते हैं, न ही चुपचाप शास्त्र से
            हटते हैं।</>,
        ],
      },
      {
        h: 'जहाँ पद्धति भिन्न है, वहाँ कारण बताते हैं',
        p: [
          <>दो ईमानदार निर्णय हर कुंडली पर अंकित रहते हैं। <em>चेष्टा</em> बल
            आधुनिक मध्यम देशांतर का उपयोग करता है — वह <em>शीघ्रोच्च</em> जिसे
            शास्त्र कभी तालिकाबद्ध नहीं करता। <em>अयन</em> बल के लिए क्रांति रमन
            की पारम्परिक पद्धति (स्थिर 24° झुकाव) से ली जाती है, वास्तविक क्रांति
            से नहीं। किसी भी मान के पीछे कौन-सी परिपाटी है, यह आप हमेशा जानते हैं।</>,
        ],
      },
      {
        h: 'हम पर भरोसा मत कीजिए — हमें जाँचिए',
        p: [
          <>पूरा इंजन और उसका परीक्षण-समूह मुक्त स्रोत (AGPL) है। इस पृष्ठ का हर
            आँकड़ा कोड से फिर से चलाया जा सकता है —{' '}
            <a href="https://github.com/sansbug/devashaa" rel="noreferrer">
              github.com/sansbug/devashaa</a>।</>,
        ],
      },
    ],
  },
}

export default function ValidationPage({ onBack, lang = 'en', setLang }) {
  const c = CONTENT[lang] || CONTENT.en
  return (
    <div className="page privacy methodology" lang={lang}>
      <div className="method-top">
        <button type="button" className="privacy-back" onClick={onBack}>{c.back}</button>
        {setLang && (
          <div className="lang-switch" role="group" aria-label="Language">
            <button type="button" className={`lang-btn${lang === 'en' ? ' on' : ''}`}
                    onClick={() => setLang('en')} aria-pressed={lang === 'en'} lang="en">EN</button>
            <button type="button" className={`lang-btn${lang === 'hi' ? ' on' : ''}`}
                    onClick={() => setLang('hi')} aria-pressed={lang === 'hi'} lang="hi">हिं</button>
          </div>
        )}
      </div>
      <h1>{c.title}</h1>
      <p className="privacy-lede">{c.lede}</p>
      {c.sections.map((s, i) => (
        <section key={i}>
          <h2>{s.h}</h2>
          {s.p.map((para, j) => <p key={j}>{para}</p>)}
        </section>
      ))}
    </div>
  )
}
