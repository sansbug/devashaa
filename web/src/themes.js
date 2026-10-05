/**
 * Colour themes. `key` matches the data-theme value in App.css.
 *
 * Swatch colours are literals, not CSS variables — a swatch must preview ITS OWN
 * theme while the page is still showing the current one. `swatch` overrides the
 * flat colour where a theme is a blend that a single dot can't convey.
 *
 * Ordered dark-first, then light.
 */
export const THEMES = [
  { key: 'midnight', label: 'Midnight', bg: '#0a0f1e', accent: '#e8c46a' },
  {
    key: 'lotus',
    label: 'Lotus',
    bg: '#f3edf7',
    accent: '#a8135a',
    swatch: 'radial-gradient(120% 110% at 50% -10%,#fff6e3 0%,#fbe6f1 48%,#dff3f2 100%)',
  },
  {
    key: 'tulasi',
    label: 'Tulasi',
    bg: '#f6f5f0',
    accent: '#2f5d4a',
    swatch: 'radial-gradient(120% 110% at 50% -10%,#fffdf3 0%,#e3efe2 52%,#f8e9dc 100%)',
  },
  {
    key: 'blossom',
    label: 'Blossom',
    bg: '#f7e6ea',
    accent: '#a8324a',
    swatch: 'linear-gradient(145deg,#ffe0cd 0%,#fcdde6 45%,#e6d9f4 100%)',
  },
]

/** New visitors land on Tulasi. Keep in step with the first-paint script in index.html. */
export const DEFAULT_THEME = 'tulasi'

/** The default before Tulasi. A browser still holding it was never asked — see App.jsx. */
export const OLD_DEFAULT_THEME = 'midnight'

const KEYS = new Set(THEMES.map((t) => t.key))

/** Guard a persisted value — an unknown key (e.g. the retired "parchment")
 *  would silently fall back to the base palette with no swatch selected, which
 *  just looks broken. */
export const validTheme = (key) => (KEYS.has(key) ? key : DEFAULT_THEME)
