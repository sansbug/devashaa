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
  {
    key: 'aarti',
    label: 'Aarti',
    bg: '#0b0810',
    accent: '#ffb547',
    swatch: 'radial-gradient(125% 100% at 50% 112%,#ffb547 0%,#3f2409 40%,#0b0810 80%)',
  },
  { key: 'ember', label: 'Ember', bg: '#12100e', accent: '#c9a227' },
  { key: 'midnight', label: 'Midnight', bg: '#0a0f1e', accent: '#e8c46a' },
  { key: 'slate', label: 'Slate', bg: '#11151a', accent: '#4fd1c5' },
  {
    key: 'lotus',
    label: 'Lotus',
    bg: '#f3edf7',
    accent: '#a8135a',
    swatch: 'radial-gradient(120% 110% at 50% -10%,#fff6e3 0%,#fbe6f1 48%,#dff3f2 100%)',
  },
  {
    key: 'blossom',
    label: 'Blossom',
    bg: '#f7e6ea',
    accent: '#a8324a',
    swatch: 'linear-gradient(145deg,#ffe0cd 0%,#fcdde6 45%,#e6d9f4 100%)',
  },
]

/** New visitors land on the luminous theme. */
export const DEFAULT_THEME = 'aarti'

const KEYS = new Set(THEMES.map((t) => t.key))

/** Guard a persisted value — an unknown key (e.g. the retired "parchment")
 *  would silently fall back to the base palette with no swatch selected, which
 *  just looks broken. */
export const validTheme = (key) => (KEYS.has(key) ? key : DEFAULT_THEME)
