/**
 * The rāśi's lord (swami) and where it sits — one small mark per house, on
 * both chart frames. "→ 3" reads: this sign's lord stands in the 3rd bhāva;
 * when the lord stands in its own sign the mark says "own" and the house is
 * tinted in the lord's colour (the charts draw that tint themselves). The
 * full sentence is in the tooltip. Geometry only — no judgement is drawn from
 * the placement here; that is the hover card's job, with its citations.
 */
import { useLang } from './LangContext.jsx'
import Glyph from './DashaGlyphs.jsx'

export const RASI_LORD = ['mars', 'venus', 'mercury', 'moon', 'sun', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'saturn', 'jupiter']

const ORD = ['', 'ordinal.1st', 'ordinal.2nd', 'ordinal.3rd', 'ordinal.4th', 'ordinal.5th', 'ordinal.6th',
             'ordinal.7th', 'ordinal.8th', 'ordinal.9th', 'ordinal.10th', 'ordinal.11th', 'ordinal.12th']

/** Where the lord of `sign` stands in this varga: its sign, its bhāva from the
 *  lagna, and whether that is the sign itself. */
export function lordPlacement(sign, grahas, vargaKey, lagna) {
  const lord = RASI_LORD[sign]
  const g = grahas.find((x) => x.key === lord)
  const at = g ? g.vargas[vargaKey] : null
  if (at == null) return { lord, at: null, bhava: null, own: false }
  return { lord, at, bhava: ((at - lagna + 12) % 12) + 1, own: at === sign }
}

export default function LordMark({ sign, grahas, vargaKey, lagna, namer, size = 'n' }) {
  const { t } = useLang()
  const p = lordPlacement(sign, grahas, vargaKey, lagna)
  if (p.at == null) return null
  const tip = `${t('deck.swami', 'Swami')} ${namer.rasi(sign)}: ${namer.grahaKey(p.lord)} — ${t(ORD[p.bhava])} (${namer.rasi(p.at)})`
    + (p.own ? ` — ${t('deck.ownHouse', 'own house')}` : '')
  return (
    <span className={`lord-mark lm-${size}${p.own ? ' own' : ''}`}
          style={{ '--g': `var(--pc-${p.lord}, var(--gr-${p.lord}))` }} title={tip}>
      <span className="lord-icon" aria-hidden="true"><Glyph lord={p.lord} size={10} /></span>
      <span className="lord-to">{p.own ? t('deck.own', 'own') : `→ ${p.bhava}`}</span>
    </span>
  )
}
