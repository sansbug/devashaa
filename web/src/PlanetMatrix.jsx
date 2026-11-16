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
import { CARRIES, EN_ORD, FRACTION, NATURE, OURS, RELATION, RELATION_ORDER, WHY, houseLine, nakshatraLord, notes } from './planetmatrix.js'

const SEVEN = ['sun', 'moon', 'mars', 'mercury', 'jupiter', 'venus', 'saturn']

export default function PlanetMatrix({ data, namer, grahas }) {
  const { lang } = useLang()
  const L = lang === 'hi' ? 'hi' : 'en'
  const W = (en, hi) => (L === 'hi' ? hi : en)
  if (!data || data.error || !Array.isArray(data.planets) || !Array.isArray(data.houses)) return null
  const n = (k) => namer.grahaKey(k)
  const list = (a) => (a && a.length ? a.map(n).join(', ') : '·')
  const nature = (k) => (NATURE[k || 'none'] || NATURE.none)[L]
  const tone = (k) => (k === 'benefic' || k === 'yogakaraka' ? 'pm-g' : k === 'malefic' ? 'pm-b' : 'pm-n')
  const ord = (h) => (L === 'hi' ? h : EN_ORD(h))
  const refs = refsOn()
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
  const relMark = (k, title) => {
    const r = k && RELATION[k]
    return r ? <i className={'pm-rel pm-' + r.tone} title={title ? `${title}: ${r[L]}` : r[L]}>{r.mark}</i> : null
  }
  const P = Object.fromEntries(data.planets.map((p) => [p.graha, p]))

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

      <h4 className="pm-h">{W('2. Each house', '2. हर भाव')}</h4>
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
      <p className="pm-key">{W('The mark after a planet in a house shows how it stands towards the lord of that sign. The mark after a Nakshatr lord shows how the planet stands towards that lord.', 'भाव में बैठे ग्रह के बाद का चिह्न बताता है कि वह उस राशि के स्वामी के प्रति कैसा है। नक्षत्र स्वामी के बाद का चिह्न बताता है कि ग्रह उस स्वामी के प्रति कैसा है।')}</p>

      <h4 className="pm-h">{W('3. Friends and enemies in this chart', '3. इस कुंडली में मित्र और शत्रु')}</h4>
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
                  return <td key={b} className={'pm-' + r.tone} title={`${n(a)} → ${n(b)}: ${r[L]}`}>{r.mark}</td>
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="pm-legend">
        {RELATION_ORDER.map((k) => <span key={k}><i className={'pm-rel pm-' + RELATION[k].tone}>{RELATION[k].mark}</i> {RELATION[k][L]}</span>)}
      </p>

      <h4 className="pm-h">{W('4. What each planet carries', '4. हर ग्रह क्या लाता है')}</h4>
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
