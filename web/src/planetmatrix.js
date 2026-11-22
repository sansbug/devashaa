/**
 * The planet and house matrix (owner, 2026-11-16): one place that shows which planets are friends, which
 * Raashi holds which planets, and which houses each planet aspects, with the helping and the hindering
 * influences on every house.
 *
 * The numbers come whole from the server (api/planet_matrix.py → chart.analysis.planet_matrix), which reads
 * them from the modules that carry the verses. This file holds only the WORDS the reader sees.
 *
 * THE RULE THE OWNER ASKED TO BE CHECKED AGAINST THE TEXT, and what the text says:
 *   - Full aspects: every planet on the 7th; Mangal also on the 4th and 8th, Guru on the 5th and 9th, Shani on
 *     the 3rd and 10th. The text agrees.
 *   - The text also gives part aspects (a quarter on the 3rd and 10th, a half on the 5th and 9th, three quarters
 *     on the 4th and 8th) and none on the 2nd, 6th, 11th and 12th.
 *   - "An aspect on the 3rd, 5th, 7th is good and on the 2nd, 4th, 6th is bad" is NOT in the text. The count
 *     sets how strong an aspect is. The planet that casts it sets whether it helps or harms. So the house table
 *     sorts influences by the planet's nature, never by the count.
 *   - Rahu and Ketu: the text names no aspect for them, so none is shown.
 *
 * CARRIES (what a planet brings at its best and under strain) is the owner's own table. It is OURS, not from a
 * classical text, and the page says so. Sentences follow the site's style; test_planetmatrix.mjs pins it.
 */

export const EN_ORD = (n) => `${n}${n % 10 === 1 && n !== 11 ? 'st' : n % 10 === 2 && n !== 12 ? 'nd' : n % 10 === 3 && n !== 13 ? 'rd' : 'th'}`
export const FRACTION = { 0.25: '¼', 0.5: '½', 0.75: '¾' }

export const NATURE = {
  benefic: { en: 'Benefic', hi: 'शुभ' },
  malefic: { en: 'Malefic', hi: 'पाप' },
  yogakaraka: { en: 'Yog-Kaarak', hi: 'योगकारक' },
  neutral: { en: 'Neutral', hi: 'सम' },
  mixed: { en: 'Mixed', hi: 'मिश्रित' },
  conditional: { en: 'Depends', hi: 'शर्त पर' },
  none: { en: 'Not classed', hi: 'वर्गीकृत नहीं' },
}

/** why the Moon's and Mercury's nature is what it is in this chart (the verse makes both conditional) */
export const WHY = {
  waxing: { en: 'it grows', hi: 'बढ़ता हुआ' },
  waning: { en: 'it wanes', hi: 'घटता हुआ' },
  with_malefic: { en: 'with a malefic', hi: 'पाप ग्रह के साथ' },
  not_with_malefic: { en: 'not with a malefic', hi: 'पाप ग्रह के साथ नहीं' },
}

/** the five-fold relation of one planet towards another in this chart */
export const RELATION = {
  adhimitra: { mark: '++', tone: 'gg', en: 'Great friend', hi: 'अधिमित्र' },
  mitra: { mark: '+', tone: 'g', en: 'Friend', hi: 'मित्र' },
  sama: { mark: '0', tone: 'n', en: 'Neutral', hi: 'सम' },
  satru: { mark: '−', tone: 'b', en: 'Enemy', hi: 'शत्रु' },
  adhisatru: { mark: '−−', tone: 'bb', en: 'Great enemy', hi: 'अधिशत्रु' },
  own: { mark: '●', tone: 'gg', en: 'Its own sign', hi: 'अपनी राशि' },
}
export const RELATION_ORDER = ['adhimitra', 'mitra', 'sama', 'satru', 'adhisatru']

/** OURS (the owner's table), not from a classical text. */
export const CARRIES = {
  sun: { good: { en: 'Authority, confidence, leadership', hi: 'अधिकार, आत्मविश्वास, नेतृत्व' }, hard: { en: 'Ego, dominance, conflict', hi: 'अहंकार, प्रभुत्व, टकराव' } },
  moon: { good: { en: 'A steady mind, care for others', hi: 'स्थिर मन, दूसरों की देखभाल' }, hard: { en: 'Moods that rise and fall', hi: 'मन का उतार-चढ़ाव' } },
  mars: { good: { en: 'Courage, initiative, protection', hi: 'साहस, पहल, रक्षा' }, hard: { en: 'Aggression, disputes, haste', hi: 'आक्रामकता, विवाद, उतावलापन' } },
  mercury: { good: { en: 'Intelligence, speech, trade', hi: 'बुद्धि, वाणी, व्यापार' }, hard: { en: 'Confusion, lack of steadiness', hi: 'भ्रम, अस्थिरता' } },
  jupiter: { good: { en: 'Wisdom, learning, guidance, protection', hi: 'ज्ञान, शिक्षा, मार्गदर्शन, रक्षा' }, hard: { en: 'Excess, too much confidence', hi: 'अति, ज़रूरत से अधिक आत्मविश्वास' } },
  venus: { good: { en: 'Relationships, harmony, comforts', hi: 'संबंध, सामंजस्य, सुख-सुविधा' }, hard: { en: 'Indulgence, attachment', hi: 'भोग, आसक्ति' } },
  saturn: { good: { en: 'Discipline, endurance, responsibility', hi: 'अनुशासन, धैर्य, उत्तरदायित्व' }, hard: { en: 'Delays, limits, burdens', hi: 'देरी, सीमाएँ, बोझ' } },
  rahu: { good: { en: 'Ambition, an unusual way up', hi: 'महत्वाकांक्षा, उन्नति का अलग रास्ता' }, hard: { en: 'Obsession, confusion, lack of steadiness', hi: 'जुनून, भ्रम, अस्थिरता' } },
  ketu: { good: { en: 'Detachment, looking within, spiritual focus', hi: 'वैराग्य, आत्मचिंतन, आध्यात्मिक एकाग्रता' }, hard: { en: 'Separation, loss of connection', hi: 'अलगाव, जुड़ाव का टूटना' } },
}

/** The rules, in the site's sentence style. `n(key)` gives a planet's name in the reader's spelling. */
export function notes(n, L, conjunct = []) {
  const en = [
    'Each planet has a full aspect on the 7th house from itself.',
    `${n('mars')} also has a full aspect on the 4th and 8th houses from itself.`,
    `${n('jupiter')} also has a full aspect on the 5th and 9th houses from itself.`,
    `${n('saturn')} also has a full aspect on the 3rd and 10th houses from itself.`,
    'The other planets have a part aspect on those houses. It is a quarter on the 3rd and 10th, a half on the 5th and 9th, and three quarters on the 4th and 8th.',
    'No planet has an aspect on the 2nd, 6th, 11th or 12th house from itself.',
    'The count of houses sets how strong an aspect is. It does not make the aspect good or bad.',
    'The planet that casts the aspect decides if it helps or harms. So each house lists benefic and malefic influences by the planet.',
    `The text names no aspect for ${n('rahu')} and ${n('ketu')}. This table shows none for them.`,
    'A planet has two natures here. The first is its nature in all charts. The second is its nature for your Lagn, from the houses it rules.',
    'The two natures can differ. They are shown side by side and are not mixed.',
    `${n('moon')} is a benefic when it grows and a malefic when it wanes. ${n('mercury')} is a malefic when it sits with a malefic.`,
    'Friendship has two parts. One is fixed for all charts. One comes from where the planets sit in this chart. The table shows the two together.',
    'An enemy by nature that is a friend by place counts as neutral. A friend by nature that is an enemy by place counts as neutral too.',
    'Friendship is not always the same in both directions. One planet can count the other an enemy while the other counts it neutral.',
  ]
  const hi = [
    'हर ग्रह की अपने से सातवें भाव पर पूर्ण दृष्टि होती है।',
    `${n('mars')} की अपने से चौथे और आठवें भाव पर भी पूर्ण दृष्टि होती है।`,
    `${n('jupiter')} की अपने से पाँचवें और नौवें भाव पर भी पूर्ण दृष्टि होती है।`,
    `${n('saturn')} की अपने से तीसरे और दसवें भाव पर भी पूर्ण दृष्टि होती है।`,
    'बाकी ग्रहों की इन भावों पर आंशिक दृष्टि होती है। तीसरे और दसवें पर चौथाई, पाँचवें और नौवें पर आधी, चौथे और आठवें पर तीन-चौथाई।',
    'किसी ग्रह की अपने से दूसरे, छठे, ग्यारहवें या बारहवें भाव पर दृष्टि नहीं होती।',
    'भावों की गिनती से दृष्टि का बल तय होता है। इससे दृष्टि अच्छी या बुरी नहीं बनती।',
    'दृष्टि डालने वाला ग्रह तय करता है कि वह सहायक है या बाधक। इसलिए हर भाव में शुभ और पाप प्रभाव ग्रह के अनुसार दिए हैं।',
    `ग्रंथ ${n('rahu')} और ${n('ketu')} की कोई दृष्टि नहीं बताता। इस तालिका में उनकी दृष्टि नहीं दिखाई गई है।`,
    'यहाँ हर ग्रह के दो स्वभाव हैं। पहला सभी कुंडलियों में उसका स्वभाव है। दूसरा आपके लग्न के लिए है, उन भावों से जिनका वह स्वामी है।',
    'दोनों स्वभाव अलग हो सकते हैं। उन्हें साथ-साथ दिखाया गया है, मिलाया नहीं गया।',
    `${n('moon')} बढ़ते समय शुभ और घटते समय पाप होता है। ${n('mercury')} पाप ग्रह के साथ बैठने पर पाप होता है।`,
    'मित्रता के दो भाग हैं। एक सभी कुंडलियों के लिए स्थिर है। दूसरा इस कुंडली में ग्रहों की स्थिति से बनता है। तालिका दोनों को मिलाकर दिखाती है।',
    'स्वभाव से शत्रु और स्थान से मित्र मिलकर सम गिना जाता है। स्वभाव से मित्र और स्थान से शत्रु भी सम गिना जाता है।',
    'मित्रता दोनों दिशाओं में हमेशा एक जैसी नहीं होती। एक ग्रह दूसरे को शत्रु मान सकता है जबकि दूसरा उसे सम मानता है।',
  ]
  en.push('Each planet sits in a Nakshatr, and each Nakshatr has a lord.',
    'A modern author, Komilla Sutton, reads each planet through the lord of its Nakshatr. Whether the planet counts that lord a friend, an enemy or neutral shows whether it is at ease in that Nakshatr or in conflict there. She uses this most for the planet whose Dasha is running.',
    'So the matrix shows where that lord sits, how strong it is by sign, and its nature.',
    'It also shows how the planet and the lord stand towards each other in this chart.',
    'This site takes one more step, which is ours and not hers.',
    'A lord that the planet counts a friend by nature supports it. A lord it counts an enemy by nature reduces its strength.',
    'This uses the fixed friendship only, not the place in the chart. A planet in its own Nakshatr is supported.',
    'The classical texts on this site do not state this teaching. So the lord does not change the benefic and malefic columns.',
    `No friendship is given for ${n('rahu')} and ${n('ketu')}. So no mark shows when one of them is the planet or the lord.`,
    `No strength by sign is given for ${n('rahu')} and ${n('ketu')} either.`)
  hi.push('हर ग्रह एक नक्षत्र में बैठा है, और हर नक्षत्र का एक स्वामी है।',
    'आधुनिक लेखिका कोमिला सटन हर ग्रह को उसके नक्षत्र के स्वामी के साथ पढ़ती हैं। ग्रह उस स्वामी को मित्र, शत्रु या सम मानता है, इससे पता चलता है कि वह उस नक्षत्र में सहज है या उलझन में। वे इसे सबसे अधिक उस ग्रह के लिए देखती हैं जिसकी दशा चल रही है।',
    'इसलिए तालिका दिखाती है कि वह स्वामी कहाँ बैठा है, राशि से कितना बलवान है, और उसका स्वभाव क्या है।',
    'यह भी दिखता है कि इस कुंडली में ग्रह और वह स्वामी एक-दूसरे के प्रति कैसे हैं।',
    'यह साइट एक कदम आगे जाती है। यह कदम हमारा है, उनका नहीं।',
    'जिस स्वामी को ग्रह स्वभाव से मित्र मानता है, वह उसे बल देता है। जिसे वह शत्रु मानता है, वह उसका बल घटाता है।',
    'इसमें केवल स्थिर मित्रता ली जाती है, कुंडली में स्थान नहीं। अपने ही नक्षत्र में बैठे ग्रह को बल मिलता है।',
    'इस साइट के शास्त्रीय ग्रंथ यह शिक्षा नहीं बताते। इसलिए यह स्वामी शुभ और पाप प्रभाव के स्तंभ नहीं बदलता।',
    `${n('rahu')} और ${n('ketu')} की कोई मित्रता नहीं दी गई है। इसलिए जब ग्रह या स्वामी इनमें से एक हो, तब कोई चिह्न नहीं दिखता।`,
    `${n('rahu')} और ${n('ketu')} का राशि से बल भी नहीं दिया गया है।`)
  if (conjunct.length) {
    en.push('Planets that share a sign count as enemies for the part that comes from this chart. The verse lists six friendly houses and the same sign is not one of them. Some books count such planets as friends.')
    hi.push('एक ही राशि में बैठे ग्रह इस कुंडली वाले भाग में शत्रु गिने जाते हैं। श्लोक छह मित्र भाव बताता है और वही राशि उनमें नहीं है। कुछ पुस्तकें ऐसे ग्रहों को मित्र गिनती हैं।')
  }
  return L === 'hi' ? hi : en
}

/** The lord of a Nakshatr, by its number 1-27 (Ashwini = 1): the nine Dasha lords, three times over. */
export const NAKSHATRA_LORDS = ['ketu', 'venus', 'sun', 'moon', 'mars', 'rahu', 'jupiter', 'saturn', 'mercury']
export const nakshatraLord = (number) => (Number.isInteger(number) && number >= 1 && number <= 27 ? NAKSHATRA_LORDS[(number - 1) % 9] : null)

/** A planet's strength by sign, in a few words (the chart's own dignity state). */
export const SIGN_STATE = {
  exalted: { tone: 'gg', en: 'Exalted', hi: 'उच्च' },
  moolatrikona: { tone: 'gg', en: 'Mul-Trikon', hi: 'मूलत्रिकोण' },
  own: { tone: 'g', en: 'Own sign', hi: 'अपनी राशि' },
  friend: { tone: 'g', en: 'Friend’s sign', hi: 'मित्र राशि' },
  neutral: { tone: 'n', en: 'Neutral sign', hi: 'सम राशि' },
  enemy: { tone: 'b', en: 'Enemy’s sign', hi: 'शत्रु राशि' },
  debilitated: { tone: 'bb', en: 'Debilitated', hi: 'नीच' },
}

/**
 * The two parts behind the relation one planet holds towards another: the fixed one (the same in all charts) and
 * the one from where the two sit in this chart. The matrix shows their sum; a reader who knows only the fixed
 * one ("Guru and Budh are enemies") needs to see both, or the sum looks wrong. null when either is a node.
 */
export function parts(from, to, P) {
  const row = P[from]
  if (!row || from === to || !row.in_chart || !row.in_chart[to]) return null
  const natural = (row.friends || []).includes(to) ? 'friend' : (row.enemies || []).includes(to) ? 'enemy' : (row.neutrals || []).includes(to) ? 'neutral' : null
  const temporary = row.in_chart[to].temporary || null
  return natural && temporary ? { natural, temporary } : null
}
export const PART = {
  friend: { en: 'friend', hi: 'मित्र' }, neutral: { en: 'neutral', hi: 'सम' }, enemy: { en: 'enemy', hi: 'शत्रु' },
}
/** "enemy by nature, friend by place" */
export const partsLine = (p, L) => (!p ? '' : L === 'hi'
  ? `स्वभाव से ${PART[p.natural].hi}, स्थान से ${PART[p.temporary].hi}`
  : `${PART[p.natural].en} by nature, ${PART[p.temporary].en} by place`)

/**
 * What the Nakshatr lord does to the strength of the planet in its Nakshatr (owner, 2026-11-16: Guru in its own
 * sign Meen but in Revati, whose lord Budh is Guru's enemy, "reduces the strength of Guru").
 *
 * THE RULE, which is the owner's and belongs to the later teaching, not to the registered classical texts:
 *   the planet's FIXED friendship towards the lord decides (the owner's "Budh and Guru are enemies"), not the
 *   chart's five-fold sum (which for that Guru is neutral):
 *     the planet is its own Nakshatr lord, or counts the lord a friend  → 'support'
 *     counts the lord an enemy                                           → 'reduce'
 *     counts the lord neutral                                            → 'none'
 *     the planet or the lord is Rahu or Ketu (no friendship is given)    → null
 * It is a statement about the planet's strength. It never moves the planet between the benefic and malefic
 * columns: Guru weakened is still Guru.
 */
export function lordEffect(graha, lord, P) {
  if (!lord || !P[graha] || !P[lord]) return null
  if (graha === lord) return P[graha].is_node ? null : 'support'
  const row = P[graha]
  if ((row.friends || []).includes(lord)) return 'support'
  if ((row.enemies || []).includes(lord)) return 'reduce'
  if ((row.neutrals || []).includes(lord)) return 'none'
  return null
}
export const EFFECT = {
  support: { tone: 'g', en: 'Supports', hi: 'बल देता है' },
  reduce: { tone: 'b', en: 'Reduces', hi: 'बल घटाता है' },
  none: { tone: 'n', en: 'No change', hi: 'कोई बदलाव नहीं' },
}
/** One short sentence for a house row. `P`, `Ld` are the planet's and the lord's names. */
export function effectLine(effect, own, P, Ld, L) {
  if (effect === 'support' && own) return L === 'hi' ? `${P} अपने ही नक्षत्र में है। इससे ${P} को बल मिलता है।` : `${P} is in its own Nakshatr. This supports ${P}.`
  if (effect === 'support') return L === 'hi' ? `${Ld} स्वभाव से ${P} का मित्र है। इससे ${P} को बल मिलता है।` : `${Ld} is a friend of ${P} by nature. This supports ${P}.`
  if (effect === 'reduce') return L === 'hi' ? `${Ld} स्वभाव से ${P} का शत्रु है। इससे यहाँ ${P} का बल घटता है।` : `${Ld} is an enemy of ${P} by nature. This reduces the strength of ${P} here.`
  return ''
}

/**
 * The state of the lord of the Nakshatr a planet sits in (owner, 2026-11-16: "a Nakshatr draws its energy from
 * its lord, not the Raashi lord"). That teaching is LATER than the registered classical texts, which use the
 * Nakshatr lord for the Dasha only. So this reports chart facts about the lord and decides nothing: it never
 * moves a planet between the benefic and malefic columns.
 *   P: planet rows of the matrix by key. G: the chart's own planet rows by key (for the strength by sign).
 */
export function lordState(graha, lord, P, G) {
  const lp = lord && P[lord]
  if (!lp) return null
  const me = P[graha]
  const rel = (from, to) => (from === to ? 'own' : (P[from] && P[from].in_chart && P[from].in_chart[to] && P[from].in_chart[to].compound) || null)
  return {
    lord, sign: lp.sign, house: lp.house,
    natural: lp.natural || null, functional: lp.functional || null,
    dignity: (G && G[lord] && G[lord].dignity && G[lord].dignity.state) || null,
    same_house: !!me && me.house === lp.house,
    towards: rel(graha, lord), back: rel(lord, graha),
    towards_parts: parts(graha, lord, P), back_parts: parts(lord, graha, P),
    effect: lordEffect(graha, lord, P),
  }
}

/**
 * ONE HOUSE, LAYER BY LAYER (owner, 2026-11-16). The owner's instruction, which is the design:
 *   "we cant net all and say net impact after all considerations. we have to associate dynamics of aspects on
 *    house lord than its own lord dynamics with its nakshatra and its lord. with their degree and other
 *    constituents deciding strength of impact"
 * So a house is read in FOUR PARTS THAT ARE NEVER ADDED TOGETHER, each with the measure of its own strength:
 *   itself      the planets in the house (with their degree) and the aspects on the house (by sign count)
 *   lord        where the house lord sits, its degree, and the measures of ITS strength: strength by sign, the
 *               stage by degree, the six-fold strength, retrograde, combust
 *   nakshatra   the lord's Nakshatr, that Nakshatr's lord and its state, and the support / reduce effect
 *   aspects     the aspects ON THE LORD, each with its strength by degree (0-60) and the caster's two natures
 * There is no `net`, `score` or `verdict` key here and none may be added: test_planetmatrix.mjs pins that.
 *   ctx: { P, G, signals (chart.analysis.grahas), shadbala (chart.shadbala.grahas), motion (chart.motion.grahas) }
 */
export function houseLayers(h, ctx) {
  const { P, G } = ctx
  const lord = h.lord, lp = P[lord], lg = (G && G[lord]) || null
  const sig = ((ctx.signals && ctx.signals[lord]) || []).find((x) => x && x.name === 'baladi' && x.available !== false)
  const sb = ctx.shadbala && ctx.shadbala[lord]
  const mo = (ctx.motion || []).find((x) => x && x.key === lord)
  const nakLord = lp ? (lp.nakshatra_lord || (lg && lg.nakshatra ? nakshatraLord(lg.nakshatra.index) : null)) : null
  const place = (g) => {
    const c = (G && G[g]) || null
    return { graha: g, degree: c ? c.degree : null, minute: c ? c.minute : null }
  }
  return {
    house: h.house, sign: h.sign,
    itself: {
      occupants: h.occupants.map((o) => ({ ...place(o.graha), natural: P[o.graha] ? P[o.graha].natural : null })),
      full: h.full_aspects.map((g) => ({ graha: g, natural: P[g] ? P[g].natural : null })),
      partial: h.partial_aspects.map((a) => ({ graha: a.graha, fraction: a.fraction, natural: P[a.graha] ? P[a.graha].natural : null })),
    },
    lord: lp ? {
      ...place(lord), house: lp.house, sign: lp.sign,
      in_own_house: lp.house === h.house,
      dignity: (lg && lg.dignity && lg.dignity.state) || null,
      stage: sig ? sig.value : null,
      grade: sig ? ((sig.detail && sig.detail.grade) || null) : null,
      shadbala: sb && typeof sb.ratio === 'number' ? { ratio: sb.ratio, strong: !!sb.strong } : null,
      retrograde: !!(lg && lg.retrograde),
      combust: !!(mo && mo.combustion && mo.combustion.combust),
    } : null,
    nakshatra: lp ? {
      pada: lg && lg.nakshatra ? lg.nakshatra.pada : null,
      lord: nakLord,
      state: lordState(lord, nakLord, P, G),
    } : null,
    aspects: lp && Array.isArray(lp.aspected_by)
      // an aspect under half a point of 60 would print as "0 of 60": it is left out
      ? lp.aspected_by.filter((a) => a.virupa >= 0.5).map((a) => ({ graha: a.graha, virupa: a.virupa, fraction: a.fraction, natural: P[a.graha] ? P[a.graha].natural : null, functional: P[a.graha] ? P[a.graha].functional : null }))
      : null,
  }
}
/** how strong an aspect by degree is, in a word (the number is shown beside it) */
export const aspectBand = (v) => (v >= 45 ? 'strong' : v >= 20 ? 'medium' : 'weak')
export const BAND = {
  strong: { en: 'strong', hi: 'प्रबल' }, medium: { en: 'medium', hi: 'मध्यम' }, weak: { en: 'weak', hi: 'हल्की' },
}
export const LAYERS_LEAD = {
  en: ['Each house is read in four parts.', 'The parts are shown apart. They are not added into one result.', 'Each part has its own measure of strength.'],
  hi: ['हर भाव चार भागों में पढ़ा जाता है।', 'ये भाग अलग-अलग दिखाए गए हैं। इन्हें जोड़कर एक परिणाम नहीं बनाया गया है।', 'हर भाग के बल का अपना माप है।'],
}

export const OURS = { en: 'Our words, not from a classical text.', hi: 'ये हमारे शब्द हैं, किसी शास्त्रीय ग्रंथ के नहीं।' }

/** One sentence per house: what helps and what hinders it, by the planets' nature. */
export function houseLine(h, n, L) {
  const list = (a) => a.map(n).join(', ')
  const part = (side) => {
    const o = side.occupants, a = side.aspects
    if (L === 'hi') return [o.length ? `${list(o)} (बैठे)` : '', a.length ? `${list(a)} (दृष्टि)` : ''].filter(Boolean).join(', ')
    return [o.length ? `${list(o)} (in it)` : '', a.length ? `${list(a)} (aspect)` : ''].filter(Boolean).join(', ')
  }
  return { benefic: part(h.benefic), malefic: part(h.malefic) }
}

/**
 * The registered modern source for reading a planet through its Nakshatr lord (owner, 2026-11-21: "Nakshatr lord,
 * cited"). Tier `modern`: named and paged, never blended with the classical texts, and never the source of the
 * strength rule above (lordEffect), which is the owner's. POINTERS ONLY: the gist is in our own words.
 *   PDF p.123 — the reading of a Nakshatr starts from its ruling planet, where it sits and what it rules.
 *   PDF p.153 — the planet whose Dasha runs at birth: see how it stands towards its Nakshatr's lord.
 *   PDF p.155 — the Dasha lord and its Nakshatr's lord as friend, enemy or neutral: at ease or in conflict.
 *   PDF p.157 — the same applied to each Dasha lord (Mars in a Saturn Nakshatr as her example).
 * She names friend, enemy or neutral without saying which friendship; the site uses the fixed one, as lordEffect.
 */
export const SUTTON = {
  cite: 'Komilla Sutton, The Essentials of Vedic Astrology, PDF pp.123, 153, 155, 157',
  label: { en: 'A modern author’s reading, not a classical text', hi: 'आधुनिक लेखिका की व्याख्या, शास्त्रीय ग्रंथ नहीं' },
}

/**
 * How a planet stands towards the lord of its own Nakshatr, by FIXED friendship.
 * Returns { lord, nak, rel } with rel 'own' | 'friend' | 'enemy' | 'neutral' | null (a node on either side), or
 * null when the chart has no Nakshatr for the planet.
 */
export function nakshatraTie(graha, chart) {
  const g = ((chart && chart.grahas) || []).find((x) => x.key === graha)
  if (!g || !g.nakshatra) return null
  const lord = nakshatraLord(g.nakshatra.index)
  if (!lord) return null
  const pm = chart.analysis && chart.analysis.planet_matrix
  const me = pm && Array.isArray(pm.planets) ? pm.planets.find((x) => x.graha === graha) : null
  let rel = null
  if (lord === graha) rel = graha === 'rahu' || graha === 'ketu' ? null : 'own'
  else if (me && (me.friends || []).includes(lord)) rel = 'friend'
  else if (me && (me.enemies || []).includes(lord)) rel = 'enemy'
  else if (me && (me.neutrals || []).includes(lord)) rel = 'neutral'
  return { lord, nak: g.nakshatra, rel }
}

/** One plain sentence for a Dasha row. `n` names a planet, `nakName` names a Nakshatr. */
export function tieLine(graha, t, n, nakName, L) {
  if (!t) return ''
  const P = n(graha), Ld = n(t.lord), K = nakName(t.nak)
  const hi = L === 'hi'
  const head = hi ? `${P} ${K} नक्षत्र में है, जिसका स्वामी ${Ld} है।` : `${P} is in ${K}, whose lord is ${Ld}.`
  if (t.rel === 'own') return head + (hi ? ` यह ${P} का अपना नक्षत्र है, इसलिए यहाँ कोई टकराव नहीं।` : ` It is ${P}’s own Nakshatr, so there is no conflict here.`)
  if (t.rel === 'friend') return head + (hi ? ` ${P} स्वभाव से ${Ld} को मित्र मानता है। इस तरह पढ़ें तो यह दशा अपने नक्षत्र के साथ सहज रहती है।` : ` ${P} counts ${Ld} a friend by nature. Read this way, the period sits at ease with its Nakshatr.`)
  if (t.rel === 'enemy') return head + (hi ? ` ${P} स्वभाव से ${Ld} को शत्रु मानता है। इस तरह पढ़ें तो इस दशा में भीतर गहरी उलझन रहती है।` : ` ${P} counts ${Ld} an enemy by nature. Read this way, there is a conflict at a deep level in this period.`)
  if (t.rel === 'neutral') return head + (hi ? ` ${P} स्वभाव से ${Ld} को सम मानता है: न सहज, न टकराव।` : ` ${P} counts ${Ld} neutral by nature: neither at ease nor in conflict.`)
  return head + (hi ? ` ${n('rahu')} और ${n('ketu')} की कोई मित्रता नहीं दी गई है, इसलिए यह नहीं पढ़ा जाता।` : ` No friendship is given for ${n('rahu')} and ${n('ketu')}, so this is not read.`)
}
