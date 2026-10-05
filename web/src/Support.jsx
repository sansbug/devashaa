/**
 * /support — "Keep Devashaa free & independent", the same ask as the
 * globalmacrolens.com Support page by the same person: one donate button
 * through a Stripe Payment Link, what the money funds, no ads, nothing sold.
 *
 * The link comes from VITE_SUPPORT_URL at build time (see the deploy line in
 * CLAUDE.md). A Stripe TEST link is never shown on the live host — a donate
 * button that quietly accepts nothing is worse than none — so the page says
 * "opening soon" instead.
 */
import { useLang } from './LangContext.jsx'

const SUPPORT_URL = (import.meta.env.VITE_SUPPORT_URL || '').trim()
const onLiveHost = () => typeof location !== 'undefined' && /(^|\.)devashaa\.com$/.test(location.hostname)
const liveUrl = () => (SUPPORT_URL && !(onLiveHost() && SUPPORT_URL.includes('/test_')) ? SUPPORT_URL : '')

export default function Support({ onBack, lang = 'en' }) {
  const { t } = useLang()
  const url = liveUrl()
  const hi = lang === 'hi'
  const Card = ({ ic, title, body }) => (
    <div className="sup-card"><span className="sup-ic" aria-hidden="true">{ic}</span><b>{title}</b><span>{body}</span></div>
  )
  return (
    <div className="page privacy methodology support" lang={lang}>
      <div className="method-top">
        <button type="button" className="privacy-back" onClick={onBack}>{hi ? '← कुंडली पर वापस' : '← back to the chart'}</button>
      </div>
      <section className="sup-hero dk-card">
        <div className="dk-body">
          <div className="sup-badge">♥ {t('support.badge', 'Support us')}</div>
          <h1>{t('support.title', 'Keep Devashaa free & independent')}</h1>
          <p className="sup-lead">{t('support.lead', 'Devashaa is an independent, ad-free Jyotiṣa reference: positions verified against the ephemeris, readings cited to the texts, no remedies, no consultations, nothing to sell you. If it is useful to you, a donation keeps it running and free for everyone.')}</p>
          {url ? (
            <a className="sup-btn" href={url} target="_blank" rel="noopener noreferrer">♥ {t('support.donate', 'Donate via Stripe')}</a>
          ) : (
            <button type="button" className="sup-btn sup-btn-off" disabled title={t('support.soon', 'Donation link coming soon')}>{t('support.soonBtn', 'Donations opening soon')}</button>
          )}
          <p className="sup-sec">🔒 {t('support.secure', 'Payments are handled by Stripe — we never see or store your card details. Any amount is appreciated; choose yours at checkout.')}</p>
        </div>
      </section>
      <section className="dk-card sup-what">
        <h4 className="dk-head"><span>{t('support.funds', 'What your support funds')}</span></h4>
        <div className="dk-body">
          <div className="sup-grid">
            <Card ic="🪐" title={t('support.f1', 'Ephemeris & sources')} body={t('support.f1b', 'The Swiss Ephemeris files, the place database, and the texts and editions the readings are drawn from.')} />
            <Card ic="☁️" title={t('support.f2', 'Hosting')} body={t('support.f2b', 'The API that casts every chart, the edge that serves the site, the encrypted store behind accounts and shared links.')} />
            <Card ic="🛠️" title={t('support.f3', 'Development')} body={t('support.f3b', 'New frames, new systems, the verification suite — and the things you ask for.')} />
            <Card ic="🚫" title={t('support.f4', 'No ads, no remedies, nothing sold')} body={t('support.f4b', 'Donations keep the site independent: no advertising, no gemstones, no consultations, no paywall on a chart.')} />
          </div>
        </div>
      </section>
      <p className="sup-thanks">{t('support.thanks', 'Thank you — every contribution, big or small, genuinely keeps this going.')} 🙏</p>
    </div>
  )
}
