/**
 * The planet and house matrix — four tables from chart.analysis.planet_matrix (api/planet_matrix.py):
 *   1. each planet: its Raashi and Bhaav, its nature, and the houses it aspects fully
 *   2. each house: its Raashi and lord, the planets in it, the aspects on it, and the benefic and malefic
 *      influences (sorted by the planet's nature, never by the house count)
 *   3. friends and enemies in this chart (the five-fold relation, row towards column)
 *   4. what each planet carries (the owner's table: ours, and labelled so)
 * The rules sit under the tables in plain sentences. See planetmatrix.js for what the text does and does not say.
 */
import { useLang } from './LangContext.jsx'
import { refsOn } from './refs.js'
import { HOUSE, STAGE, GRADE } from './walkthrough.js'
import { SUTTON, BAND, LAYERS_LEAD, aspectBand, houseLayers, EFFECT, effectLine, CARRIES, EN_ORD, FRACTION, NATURE, OURS, RELATION, RELATION_ORDER, SIGN_STATE, WHY, houseLine, lordState, nakshatraLord, notes, parts, partsLine } from './planetmatrix.js'

const SEVEN = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn']

// The helpers the matrix and the house cards share (the cards are also printed in the full report).
function kit(data, namer, grahas, chart, L) {
  const n = (k) => namer.grahaKey(k)
  const list = (a) => (a && a.length ? a.map(n).join(', ') : '·')
  const nature = (k) => (NATURE[k || 'none'] || NATURE.none)[L]
  const tone = (k) => (k === 'benefic' || k === 'yogakaraka' ? 'pm-g' : k === 'malefic' ? 'pm-b' : 'pm-n')
  const ord = (h) => (L === 'hi' ? h : EN_ORD(h))
  const refs = refsOn()
  const P = Object.fromEntries(data.planets.map((p) => [p.graha, p]))
  // the Nakshatr's name comes from the chart's own planet rows (the matrix carries its index and lord)
  const G = Object.fromEntries((grahas || []).map((g) => [g.key, g]))
  const nakName = (k) => (G[k] && G[k].nakshatra ? namer.nakshatra(G[k].nakshatra) : null)
  // The lord and the relation come with the matrix. A chart cast before the server carried them still has its
  // Nakshatr, so the lord is read from that and the relation from the friendship table: a row never shows a
  // Nakshatr without its lord.
  const nakLord = (row) => row.nakshatra_lord || (G[row.graha] && G[row.graha].nakshatra ? nakshatraLord(G[row.graha].nakshatra.index) : null)
  const nakRel = (row) => {
    if (row.to_nakshatra_lord !== undefined) return row.to_nakshatra_lord
    const lord = nakLord(row), me = P[row.graha]
    if (!lord || !me) return null
    if (lord === row.graha) return 'own'
    return (me.in_chart && me.in_chart[lord] && me.in_chart[lord].compound) || null
  }
  const state = (row) => lordState(row.graha, nakLord(row), P, G)
  const signState = (k) => (k && SIGN_STATE[k] ? <span className={'pm-rel pm-' + SIGN_STATE[k].tone}>{SIGN_STATE[k][L]}</span> : '·')
  const ctx = { P, G, signals: chart && chart.analysis ? chart.analysis.grahas : null,
    shadbala: chart && chart.shadbala && !chart.shadbala.error ? chart.shadbala.grahas : null,
    motion: chart && chart.motion && !chart.motion.error ? chart.motion.grahas : null }
  const deg = (x) => (x && x.degree != null ? `${x.degree}°${x.minute != null ? `${String(x.minute).padStart(2, '0')}′` : ''}` : '')
  const nat = (k) => (k ? <span className={'pm-rel ' + tone(k)}>{nature(k)}</span> : null)
  const relMark = (k, title) => {
    const r = k && RELATION[k]
    return r ? <i className={'pm-rel pm-' + r.tone} title={title ? `${title}: ${r[L]}` : r[L]}>{r.mark}</i> : null
  }
  return { n, list, nature, tone, ord, refs, P, G, nakName, nakLord, nakRel, state, signState, ctx, deg, nat, relMark }
}

export default function PlanetMatrix({ data, namer, grahas, chart }) {
  const { lang } = useLang()
  const L = lang === 'hi' ? 'hi' : 'en'
  const W = (en, hi) => (L === 'hi' ? hi : en)
  if (!data || data.error || !Array.isArray(data.planets) || !Array.isArray(data.houses)) return null
  const { n, list, nature, tone, ord, refs, P, G, nakName, nakLord, nakRel, state, signState, ctx, deg, nat, relMark } = kit(data, namer, grahas, chart, L)

  return (
    <section className="table-panel pm-panel" id="rg-planetmatrix">
      <h3>{W('Planet and house matrix', 'ग्रह और भाव की तालिका')}</h3>
      <p className="rc-note">{W('This shows where each planet sits, which houses it aspects, and which planets are its friends. Then it shows what helps and what hinders each house.',
        'यहाँ दिखता है कि हर ग्रह कहाँ बैठा है, किन भावों पर उसकी दृष्टि है, और कौन-से ग्रह उसके मित्र हैं। फिर दिखता है कि हर भाव को क्या सहायता देता है और क्या बाधा।')}</p>

      <h4 className="pm-h">{W('1. Each planet', '1. हर ग्रह')}</h4>
      <div className="pm-wrap">
        <table className="pm-table">
          <thead>
            <tr>
              <th>{W('Planet', 'ग्रह')}</th>
              <th>{W('Raashi', 'राशि')}</th>
              <th>{W('Bhaav', 'भाव')}</th>
              <th>{W('Nakshatr', 'नक्षत्र')}</th>
              <th>{W('Nakshatr lord', 'नक्षत्र स्वामी')}</th>
              <th>{W('Nature', 'स्वभाव')}</th>
              <th>{W('For your Lagn', 'आपके लग्न के लिए')}</th>
              <th>{W('Full aspect on Bhaav', 'पूर्ण दृष्टि वाले भाव')}</th>
              <th>{W('Friends', 'मित्र')}</th>
              <th>{W('Neutral', 'सम')}</th>
              <th>{W('Enemies', 'शत्रु')}</th>
            </tr>
          </thead>
          <tbody>
            {data.planets.map((p) => (
              <tr key={p.graha}>
                <td className="pm-name">{n(p.graha)}</td>
                <td>{namer.rasi(p.sign)}</td>
                <td className="pm-num">{p.house}</td>
                <td>{nakName(p.graha) || '·'}</td>
                <td className="pm-name">{nakLord(p) ? <>{n(nakLord(p))}{relMark(nakRel(p), W(`${n(p.graha)} towards ${n(nakLord(p))}`, `${n(p.graha)} का ${n(nakLord(p))} से संबंध`))}</> : '·'}</td>
                <td className={tone(p.natural)}>{nature(p.natural)}{p.natural_why && WHY[p.natural_why] ? <small> ({WHY[p.natural_why][L]})</small> : null}</td>
                <td className={tone(p.functional)}>{nature(p.functional)}</td>
                <td>{p.is_node
                  ? <small>{W('none in the text', 'ग्रंथ में नहीं')}</small>
                  : p.aspect_houses.map((h, i) => <span key={h} className="pm-chip" title={W(`the ${EN_ORD(p.aspect_rule[i])} from itself`, `अपने से ${p.aspect_rule[i]}वाँ`)}>{h}</span>)}</td>
                <td>{p.is_node ? '·' : list(p.friends)}</td>
                <td>{p.is_node ? '·' : list(p.neutrals)}</td>
                <td>{p.is_node ? '·' : list(p.enemies)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <h4 className="pm-h">{W('2. The Nakshatr lord behind each planet', '2. हर ग्रह के पीछे नक्षत्र स्वामी')}</h4>
      <p className="pm-key">{W('A modern author, Komilla Sutton, reads each planet through the lord of its Nakshatr: a friend means the planet is at ease there, an enemy means conflict. The effect on strength is this site’s own step. This table shows the state of that lord.', 'आधुनिक लेखिका कोमिला सटन हर ग्रह को उसके नक्षत्र के स्वामी के साथ पढ़ती हैं: मित्र हो तो ग्रह वहाँ सहज है, शत्रु हो तो उलझन। बल पर असर इस साइट का अपना कदम है। यह तालिका उस स्वामी की स्थिति दिखाती है।')}{refs ? <small> ({SUTTON.label[L]}: {SUTTON.cite})</small> : null}</p>
      <div className="pm-wrap">
        <table className="pm-table">
          <thead>
            <tr>
              <th>{W('Planet', 'ग्रह')}</th>
              <th>{W('Nakshatr', 'नक्षत्र')}</th>
              <th>{W('Nakshatr lord', 'नक्षत्र स्वामी')}</th>
              <th>{W('Lord sits in', 'स्वामी कहाँ बैठा है')}</th>
              <th>{W('Lord by sign', 'राशि से स्वामी का बल')}</th>
              <th>{W('Lord’s nature', 'स्वामी का स्वभाव')}</th>
              <th>{W('Lord for your Lagn', 'आपके लग्न के लिए स्वामी')}</th>
              <th>{W('Planet towards lord', 'ग्रह का स्वामी से संबंध')}</th>
              <th>{W('Lord towards planet', 'स्वामी का ग्रह से संबंध')}</th>
              <th>{W('Effect on the planet', 'ग्रह के बल पर प्रभाव')}</th>
            </tr>
          </thead>
          <tbody>
            {data.planets.map((p) => {
              const st = state(p)
              if (!st) return <tr key={p.graha}><td className="pm-name">{n(p.graha)}</td><td>{nakName(p.graha) || '·'}</td><td colSpan={8}>·</td></tr>
              const tw = st.towards && RELATION[st.towards], bk = st.back && RELATION[st.back]
              return (
                <tr key={p.graha}>
                  <td className="pm-name">{n(p.graha)}</td>
                  <td>{nakName(p.graha) || '·'}</td>
                  <td className="pm-name">{n(st.lord)}</td>
                  <td>{namer.rasi(st.sign)}, {W(`the ${ord(st.house)} Bhaav`, `भाव ${st.house}`)}{st.same_house && st.lord !== p.graha ? <small> ({W('with the planet', 'ग्रह के साथ')})</small> : null}</td>
                  <td>{signState(st.dignity)}</td>
                  <td className={tone(st.natural)}>{nature(st.natural)}</td>
                  <td className={tone(st.functional)}>{nature(st.functional)}</td>
                  <td className={tw ? 'pm-' + tw.tone : ''}>{tw ? tw[L] : '·'}{st.towards_parts ? <div><small>{partsLine(st.towards_parts, L)}</small></div> : null}</td>
                  <td className={bk ? 'pm-' + bk.tone : ''}>{bk ? bk[L] : '·'}{st.back_parts ? <div><small>{partsLine(st.back_parts, L)}</small></div> : null}</td>
                  <td className={st.effect ? 'pm-' + EFFECT[st.effect].tone : ''}>{st.effect ? <b>{EFFECT[st.effect][L]}</b> : '·'}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      <h4 className="pm-h">{W('3. Each house', '3. हर भाव')}</h4>
      <div className="pm-wrap">
        <table className="pm-table">
          <thead>
            <tr>
              <th>{W('Bhaav', 'भाव')}</th>
              <th>{W('Raashi', 'राशि')}</th>
              <th>{W('Raashi lord', 'राशि स्वामी')}</th>
              <th>{W('Planets in it', 'इसमें बैठे ग्रह')}</th>
              <th>{W('Nakshatr and its lord', 'नक्षत्र और उसका स्वामी')}</th>
              <th>{W('Full aspect from', 'पूर्ण दृष्टि')}</th>
              <th>{W('Part aspect from', 'आंशिक दृष्टि')}</th>
              <th>{W('Benefic influence', 'शुभ प्रभाव')}</th>
              <th>{W('Malefic influence', 'पाप प्रभाव')}</th>
            </tr>
          </thead>
          <tbody>
            {data.houses.map((h) => {
              const line = houseLine(h, n, L)
              return (
                <tr key={h.house}>
                  <td className="pm-num">{h.house}</td>
                  <td>{namer.rasi(h.sign)}</td>
                  <td className="pm-name">{n(h.lord)}{h.lord_house ? <small> ({W(`in the ${ord(h.lord_house)}`, `भाव ${h.lord_house} में`)})</small> : null}</td>
                  <td>{h.occupants.length ? h.occupants.map((o, i) => {
                    const r = o.to_lord && RELATION[o.to_lord]
                    return <span key={o.graha} title={r ? W(`${n(o.graha)} towards the lord of this sign: ${r.en}`, `${n(o.graha)} का इस राशि के स्वामी से संबंध: ${r.hi}`) : ''}>{i ? ', ' : ''}{n(o.graha)}{r ? <i className={'pm-rel pm-' + r.tone}>{r.mark}</i> : null}</span>
                  }) : '·'}</td>
                  <td>{h.occupants.length ? h.occupants.map((o) => (
                    <div key={o.graha} className="pm-nak">
                      {W(`${n(o.graha)} in ${nakName(o.graha) || '·'}`, `${n(o.graha)} ${nakName(o.graha) || '·'} में`)}{nakLord(o) ? <>, {W('its lord', 'उसका स्वामी')} <b>{n(nakLord(o))}</b>{relMark(nakRel(o), W(`${n(o.graha)} towards ${n(nakLord(o))}`, `${n(o.graha)} का ${n(nakLord(o))} से संबंध`))}</> : null}
                      {(() => {
                        const st = state(o)
                        if (!st) return null
                        return <div className="pm-lord"><small>{W(`${n(st.lord)} is in the ${ord(st.house)} Bhaav`, `${n(st.lord)} भाव ${st.house} में`)}{st.dignity && SIGN_STATE[st.dignity] ? `, ${SIGN_STATE[st.dignity][L]}` : ''}{st.natural ? `, ${nature(st.natural)}` : ''}</small>{st.effect && st.effect !== 'none' ? <div className={'pm-effect pm-' + EFFECT[st.effect].tone}>{effectLine(st.effect, st.lord === o.graha, n(o.graha), n(st.lord), L)}</div> : null}</div>
                      })()}
                    </div>
                  )) : '·'}</td>
                  <td>{list(h.full_aspects)}</td>
                  <td className="pm-dim">{h.partial_aspects.length ? h.partial_aspects.map((a) => `${n(a.graha)} ${FRACTION[a.fraction] || a.fraction}`).join(', ') : '·'}</td>
                  <td className={line.benefic ? 'pm-g' : ''}>{line.benefic || '·'}</td>
                  <td className={line.malefic ? 'pm-b' : ''}>{line.malefic || '·'}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
      <p className="pm-key">{W('The mark after a planet in a house shows how it stands towards the lord of that sign. The mark after a Nakshatr lord shows how the planet stands towards that lord. The small line under it shows the state of that lord.', 'भाव में बैठे ग्रह के बाद का चिह्न बताता है कि वह उस राशि के स्वामी के प्रति कैसा है। नक्षत्र स्वामी के बाद का चिह्न बताता है कि ग्रह उस स्वामी के प्रति कैसा है। उसके नीचे की छोटी पंक्ति उस स्वामी की स्थिति बताती है।')}</p>

      <h4 className="pm-h">{W('4. Each house, part by part', '4. हर भाव, भाग-भाग करके')}</h4>
      <HouseCards data={data} namer={namer} grahas={grahas} chart={chart} />

      <h4 className="pm-h">{W('5. Friends and enemies in this chart', '5. इस कुंडली में मित्र और शत्रु')}</h4>
      <p className="pm-key">{W('Read across. Each row shows how that planet stands towards the planet in the column.', 'पंक्ति के साथ पढ़ें। हर पंक्ति बताती है कि वह ग्रह स्तंभ वाले ग्रह के प्रति कैसा है।')}</p>
      <div className="pm-wrap">
        <table className="pm-table pm-grid">
          <thead>
            <tr><th />{SEVEN.map((g) => <th key={g}>{n(g)}</th>)}</tr>
          </thead>
          <tbody>
            {SEVEN.filter((a) => P[a]).map((a) => (
              <tr key={a}>
                <td className="pm-name">{n(a)}</td>
                {SEVEN.map((b) => {
                  if (a === b) return <td key={b} className="pm-self">–</td>
                  const c = P[a].in_chart && P[a].in_chart[b]
                  const r = c && RELATION[c.compound]
                  if (!r) return <td key={b}>·</td>
                  return <td key={b} className={'pm-' + r.tone} title={`${n(a)} → ${n(b)}: ${r[L]}${parts(a, b, P) ? ` (${partsLine(parts(a, b, P), L)})` : ''}`}>{r.mark}</td>
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="pm-legend">
        {RELATION_ORDER.map((k) => <span key={k}><i className={'pm-rel pm-' + RELATION[k].tone}>{RELATION[k].mark}</i> {RELATION[k][L]}</span>)}
      </p>

      <h4 className="pm-h">{W('6. What each planet carries', '6. हर ग्रह क्या लाता है')}</h4>
      <div className="pm-wrap">
        <table className="pm-table">
          <thead>
            <tr><th>{W('Planet', 'ग्रह')}</th><th>{W('At its best', 'अच्छी स्थिति में')}</th><th>{W('Under strain', 'दबाव में')}</th></tr>
          </thead>
          <tbody>
            {data.planets.map((p) => (
              <tr key={p.graha}>
                <td className="pm-name">{n(p.graha)}</td>
                <td>{CARRIES[p.graha].good[L]}</td>
                <td>{CARRIES[p.graha].hard[L]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="pm-key">{OURS[L]}</p>

      <h4 className="pm-h">{W('How to read this', 'इसे कैसे पढ़ें')}</h4>
      <ul className="pm-notes">
        {notes(n, L, data.conjunction_affected || []).map((s, i) => <li key={i}>{s}</li>)}
      </ul>
      {refs && data.citations && (
        <p className="pm-key">
          {W('Nature', 'स्वभाव')}: {data.citations.natural} · {W('For the Lagn', 'लग्न के लिए')}: {data.citations.functional} · {W('Friendship', 'मित्रता')}: {data.citations.friendship} · {W('Aspects', 'दृष्टि')}: {data.citations.aspects} · {W('Nakshatr lord', 'नक्षत्र स्वामी')}: {data.citations.nakshatra_lord}
        </p>
      )}
    </section>
  )
}

/** Section 4, each house part by part: twelve cards, never netted. Also printed in the full report (Report.jsx). */
export function HouseCards({ data, namer, grahas, chart }) {
  const { lang } = useLang()
  const L = lang === 'hi' ? 'hi' : 'en'
  const W = (en, hi) => (L === 'hi' ? hi : en)
  if (!data || data.error || !Array.isArray(data.planets) || !Array.isArray(data.houses)) return null
  const { n, nature, nakName, signState, ctx, deg, nat } = kit(data, namer, grahas, chart, L)
  return (
    <>
    <p className="pm-key">{LAYERS_LEAD[L].join(' ')}</p>
    <div className="pm-cards">
      {data.houses.map((h) => {
        const y = houseLayers(h, ctx)
        const ld = y.lord, nk = y.nakshatra, st = nk && nk.state
        return (
          <div className="pm-card" key={h.house}>
            <h5>{W(`Bhaav ${h.house}`, `भाव ${h.house}`)} · {namer.rasi(h.sign)}{HOUSE[h.house] ? <span> · {HOUSE[h.house].title[L]}</span> : null}</h5>

            <h6>{W('In the house', 'भाव में')}</h6>
            <ul>
              {y.itself.occupants.length
                ? y.itself.occupants.map((o) => <li key={o.graha}><b>{n(o.graha)}</b> {W(`sits here at ${deg(o)}`, `यहाँ ${deg(o)} पर बैठा है`)}{nakName(o.graha) ? W(`, in ${nakName(o.graha)}`, `, ${nakName(o.graha)} में`) : ''} {nat(o.natural)}</li>)
                : <li>{W('No planet sits here.', 'यहाँ कोई ग्रह नहीं बैठा है।')}</li>}
              {y.itself.full.length
                ? <li>{W('Full aspect from', 'पूर्ण दृष्टि')}: {y.itself.full.map((a, i) => <span key={a.graha}>{i ? ', ' : ''}{n(a.graha)} {nat(a.natural)}</span>)}</li>
                : <li>{W('No planet has a full aspect on it.', 'इस पर किसी ग्रह की पूर्ण दृष्टि नहीं है।')}</li>}
              {y.itself.partial.length ? <li className="pm-dim">{W('Part aspect from', 'आंशिक दृष्टि')}: {y.itself.partial.map((a) => `${n(a.graha)} ${FRACTION[a.fraction] || a.fraction}`).join(', ')}</li> : null}
            </ul>

            <h6>{W('Its lord', 'इसका स्वामी')}: {n(h.lord)}</h6>
            {ld ? (
              <ul>
                <li>{ld.in_own_house
                  ? W(`${n(h.lord)} sits in this house, in ${namer.rasi(ld.sign)}, at ${deg(ld)}.`, `${n(h.lord)} इसी भाव में, ${namer.rasi(ld.sign)} में, ${deg(ld)} पर बैठा है।`)
                  : W(`${n(h.lord)} sits in Bhaav ${ld.house}, in ${namer.rasi(ld.sign)}, at ${deg(ld)}.`, `${n(h.lord)} भाव ${ld.house} में, ${namer.rasi(ld.sign)} में, ${deg(ld)} पर बैठा है।`)}</li>
                <li>{W('Strength by sign', 'राशि से बल')}: {signState(ld.dignity)}</li>
                {ld.stage && STAGE[ld.stage] ? <li>{W('Stage by degree', 'अंश से अवस्था')}: <b>{STAGE[ld.stage][L]}</b>{ld.grade && GRADE[ld.grade] ? W(` (gives ${GRADE[ld.grade].en})`, ` (${GRADE[ld.grade].hi})`) : ''}</li> : null}
                {ld.shadbala ? <li>{W('Six-fold strength', 'षड्बल')}: <b>{ld.shadbala.ratio.toFixed(2)}</b> {W('times the amount it needs', 'गुना, आवश्यक मात्रा का')} <span className={'pm-rel ' + (ld.shadbala.strong ? 'pm-g' : 'pm-b')}>{ld.shadbala.strong ? W('strong', 'बलवान') : W('weak', 'दुर्बल')}</span></li> : null}
                {ld.retrograde ? <li>{W('It is retrograde.', 'यह वक्री है।')}</li> : null}
                {ld.combust ? <li>{W('It is combust (too near Surya).', 'यह अस्त है (सूर्य के बहुत पास)।').replace('Surya', n('sun'))}</li> : null}
              </ul>
            ) : null}

            <h6>{W('The lord’s Nakshatr', 'स्वामी का नक्षत्र')}</h6>
            {nk && nk.lord ? (
              <ul>
                <li>{W(`${n(h.lord)} is in ${nakName(h.lord) || '·'}${nk.pada ? `, quarter ${nk.pada}` : ''}. Its lord is `, `${n(h.lord)} ${nakName(h.lord) || '·'} में है${nk.pada ? `, चरण ${nk.pada}` : ''}। उसका स्वामी `)}<b>{n(nk.lord)}</b>{W('.', ' है।')}</li>
                {st && nk.lord !== h.lord ? <li>{W(`${n(nk.lord)} sits in Bhaav ${st.house}, in ${namer.rasi(st.sign)}.`, `${n(nk.lord)} भाव ${st.house} में, ${namer.rasi(st.sign)} में बैठा है।`)} {st.dignity ? signState(st.dignity) : null} {nat(st.natural)}</li> : null}
                {st && st.effect && st.effect !== 'none'
                  ? <li><span className={'pm-effect pm-' + EFFECT[st.effect].tone}>{effectLine(st.effect, nk.lord === h.lord, n(h.lord), n(nk.lord), L)}</span></li>
                  : st && st.effect === 'none' ? <li className="pm-dim">{W(`${n(nk.lord)} is neutral to ${n(h.lord)} by nature. No change.`, `${n(nk.lord)} स्वभाव से ${n(h.lord)} के लिए सम है। कोई बदलाव नहीं।`)}</li> : null}
              </ul>
            ) : <ul><li>·</li></ul>}

            <h6>{W('Aspects on the lord', 'स्वामी पर दृष्टि')}</h6>
            <ul>
              {y.aspects == null ? <li>·</li>
                : y.aspects.length ? y.aspects.map((a) => (
                  <li key={a.graha}><b>{n(a.graha)}</b>: {W(`${Math.round(a.virupa)} of 60`, `60 में से ${Math.round(a.virupa)}`)} <small>({BAND[aspectBand(a.virupa)][L]})</small> {nat(a.natural)}{a.functional ? <small> · {W('for your Lagn', 'आपके लग्न के लिए')}: {nature(a.functional)}</small> : null}</li>
                ))
                  : <li>{W(`No planet aspects ${n(h.lord)}.`, `${n(h.lord)} पर किसी ग्रह की दृष्टि नहीं है।`)}</li>}
            </ul>
          </div>
        )
      })}
    </div>
    <p className="pm-key">{W('An aspect on the lord is measured by degree, from 0 to 60. An aspect on the house is counted by sign.', 'स्वामी पर दृष्टि अंश से मापी जाती है, 0 से 60 तक। भाव पर दृष्टि राशि से गिनी जाती है।')}</p>
    </>
  )
}
