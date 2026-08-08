import { createContext, useContext } from 'react'

/**
 * The active UI language and its translator, shared to every component so the
 * chrome can be localized without prop-drilling `lang` through 20 panels.
 * `t(key, fallback)` looks the key up in i18n.js for the current language,
 * falling back to English (then the key) so a missing translation never breaks.
 */
export const LangContext = createContext({ lang: 'en', t: (k, f) => f ?? k })

export function useLang() {
  return useContext(LangContext)
}
