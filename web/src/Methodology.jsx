/**
 * "How Devashaa is different" — the methodology / doctrine page, served at
 * /methodology. It states the site's actual working rules: cite-or-refuse,
 * provenance tiers, validated math, no fate / no fear / nothing to sell.
 *
 * Bilingual (English + Devanagari Hindi), driven by the global `lang` choice in
 * the Appearance bar. Every claim here must stay TRUE of the code — the same
 * standard as the Privacy page. If the doctrine changes, this page changes.
 */

// Content is parallel per language so the two never drift in structure. Each
// section is { h: heading, p: [paragraphs…] }; paragraphs may be JSX.
const CONTENT = {
  en: {
    back: '← back to the chart',
    title: 'How Devashaa is different',
    lede: (
      <>
        Devashaa is a sidereal Jyotiṣa birth-chart reference built on a single
        rule: <strong>show the source, or say nothing</strong>. It follows the{' '}
        <em>Bṛhat Parāśara Horā Śāstra</em>, cites chapter and verse, and tells
        you plainly where the text is silent.
      </>
    ),
    sections: [
      {
        h: 'Cite, or refuse',
        p: [
          <>Every reading drawn from the classical text traces to a specific
            śloka — chapter and verse; anything from another source is labelled
            as such (see below). When the text does not answer a question,
            Devashaa does not invent an answer to fill the gap.</>,
          <><strong>“The text is silent” is a real, first-class answer here</strong>,
            not a failure. That single discipline is what separates a reference
            from a fortune-teller.</>,
        ],
      },
      {
        h: 'Provenance, labelled',
        p: [
          <>Not everything in astrology carries the same weight, so Devashaa
            never pretends it does. Every claim is tagged by where it comes
            from, and you always know which you are reading:</>,
        ],
        list: [
          ['śloka', 'directly from the Bṛhat Parāśara Horā Śāstra.'],
          ['traditional', 'long-standing classical usage not in BPHS itself.'],
          ['modern', 'a named modern author’s method (e.g. Raman, Patel), marked as such.'],
          ['jaimini', 'from the Jaimini system — a distinct school, kept separate.'],
        ],
      },
      {
        h: 'The mathematics is verified',
        p: [
          <>The astronomy uses the Swiss Ephemeris (JPL DE431). The Jyotiṣa
            computations are tested against the classics’ own worked examples —
            the daśās against BPHS, and the <em>Ṣaḍbala</em> (six-fold strength)
            reproduced <strong>to the virūpa, component by component</strong>,
            against B. V. Raman’s Standard Horoscope.</>,
          <>In doing so we even found and documented arithmetic slips in Raman’s
            printed tables. Every calculation can be read in the source code and
            re-run.</>,
        ],
      },
      {
        h: 'No fate. No fear. Nothing to sell.',
        p: [
          <>Devashaa does not tell you what <em>will</em> happen as if it were
            settled, and it will never frighten you into buying a gemstone, a
            ritual, or a consultation. <strong>There are no products here.</strong></>,
          <>Where the text gives remedies, they are shown as the text’s —
            tiered by source, never prescribed as a cure.</>,
        ],
      },
      {
        h: 'Built to be read, not to create dependence',
        p: [
          <>The aim is to help you read your own chart — to see its structure
            and reason about it — rather than to make you depend on a paid
            reading. The signal is shown; <strong>the conclusion is yours</strong>.</>,
        ],
      },
      {
        h: 'Open and checkable',
        p: [
          <>The entire site, including the engine and its tests, is open source
            (AGPL). Every claim on this page can be verified in the code rather
            than taken on trust —{' '}
            <a href="https://github.com/sansbug/devashaa" rel="noreferrer">
              github.com/sansbug/devashaa</a>.</>,
        ],
      },
    ],
  },

  hi: {
    back: '← कुंडली पर वापस',
    title: 'देवाशा किस तरह अलग है',
    lede: (
      <>
        देवाशा एक निरयन ज्योतिष जन्म-कुंडली संदर्भ है, जो एक ही नियम पर बना है:{' '}
        <strong>स्रोत दिखाओ, अन्यथा कुछ मत कहो</strong>। यह{' '}
        <em>बृहत् पराशर होरा शास्त्र</em> का अनुसरण करता है, अध्याय और श्लोक का
        हवाला देता है, और जहाँ शास्त्र मौन है वहाँ स्पष्ट रूप से यही कहता है।
      </>
    ),
    sections: [
      {
        h: 'स्रोत दो, या इनकार करो',
        p: [
          <>शास्त्र से लिया गया हर निर्णय किसी विशिष्ट श्लोक से — अध्याय और श्लोक
            संख्या सहित — जुड़ा होता है; किसी अन्य स्रोत से ली गई बात उसी रूप में
            स्पष्ट रूप से अंकित होती है (नीचे देखें)। जब शास्त्र किसी प्रश्न का
            उत्तर नहीं देता, तो देवाशा उस रिक्ति को भरने के लिए उत्तर नहीं गढ़ता।</>,
          <><strong>यहाँ “शास्त्र मौन है” एक वास्तविक और पूर्ण उत्तर है</strong>,
            कोई विफलता नहीं। यही एक अनुशासन एक संदर्भ को भविष्यवक्ता से अलग करता है।</>,
        ],
      },
      {
        h: 'उद्गम, स्पष्ट रूप से अंकित',
        p: [
          <>ज्योतिष में हर बात का महत्त्व समान नहीं होता, इसलिए देवाशा कभी ऐसा
            दिखावा नहीं करता। हर कथन इस आधार पर चिह्नित है कि वह कहाँ से आता है,
            और आप हमेशा जानते हैं कि आप क्या पढ़ रहे हैं:</>,
        ],
        list: [
          ['श्लोक', 'सीधे बृहत् पराशर होरा शास्त्र से।'],
          ['पारम्परिक', 'दीर्घकालीन शास्त्रीय प्रयोग, जो स्वयं बीपीएचएस में नहीं है।'],
          ['आधुनिक', 'किसी नामित आधुनिक लेखक (जैसे रमन, पटेल) की पद्धति, स्पष्ट रूप से अंकित।'],
          ['जैमिनि', 'जैमिनि पद्धति से — एक भिन्न परम्परा, अलग रखी गई।'],
        ],
      },
      {
        h: 'गणित सत्यापित है',
        p: [
          <>खगोलीय गणना स्विस एफ़ेमेरिस (JPL DE431) से होती है। ज्योतिषीय गणनाएँ
            शास्त्रों के अपने हल किए गए उदाहरणों से परखी जाती हैं — दशाएँ बीपीएचएस
            के अनुसार, और <em>षड्बल</em> (छह-गुना बल) बी. वी. रमन की “स्टैंडर्ड
            होरोस्कोप” से घटक-दर-घटक <strong>विरूप तक</strong> मिलाया गया।</>,
          <>ऐसा करते हुए हमें रमन की छपी तालिकाओं में गणना की कुछ त्रुटियाँ भी
            मिलीं, जिन्हें हमने दर्ज किया। हर गणना स्रोत-कोड में पढ़ी और फिर से
            चलाई जा सकती है।</>,
        ],
      },
      {
        h: 'कोई भाग्य नहीं। कोई भय नहीं। बेचने को कुछ नहीं।',
        p: [
          <>देवाशा आपको यह नहीं बताता कि क्या <em>होगा</em>, मानो वह निश्चित हो,
            और यह आपको डराकर कभी कोई रत्न, अनुष्ठान या परामर्श खरीदने के लिए विवश
            नहीं करेगा।{' '}
            <strong>यहाँ बेचने के लिए कुछ नहीं है।</strong></>,
          <>जहाँ शास्त्र उपाय देता है, उन्हें शास्त्र के रूप में दिखाया जाता है —
            स्रोत के अनुसार स्तरित, कभी इलाज की तरह निर्धारित नहीं।</>,
        ],
      },
      {
        h: 'पढ़ने के लिए बना, निर्भरता के लिए नहीं',
        p: [
          <>उद्देश्य यह है कि आप अपनी कुंडली स्वयं पढ़ सकें — उसकी संरचना देखें
            और उस पर विचार करें — न कि किसी सशुल्क पठन पर निर्भर रहें। संकेत
            दिखाया जाता है; <strong>निष्कर्ष आपका है</strong>।</>,
        ],
      },
      {
        h: 'मुक्त और जाँचने योग्य',
        p: [
          <>पूरी वेबसाइट, इंजन और उसके परीक्षणों सहित, मुक्त स्रोत (AGPL) है। इस
            पृष्ठ का हर दावा विश्वास पर लेने के बजाय कोड में सत्यापित किया जा
            सकता है —{' '}
            <a href="https://github.com/sansbug/devashaa" rel="noreferrer">
              github.com/sansbug/devashaa</a>।</>,
        ],
      },
    ],
  },
}

export default function Methodology({ onBack, lang = 'en', setLang }) {
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
          {s.list && (
            <ul className="method-tiers">
              {s.list.map(([term, desc]) => (
                <li key={term}><span className="method-tier">{term}</span> — {desc}</li>
              ))}
            </ul>
          )}
        </section>
      ))}
    </div>
  )
}
