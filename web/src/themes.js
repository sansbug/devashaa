/**
 * Colour themes. `key` matches the data-theme value in App.css.
 *
 * Swatch colours are literals, not CSS variables — a swatch must preview ITS OWN
 * theme while the page is still showing the current one. `swatch` overrides the
 * flat colour where a theme is a blend that a single dot can't convey.
 */
export const THEMES = [
  { key: 'ember', label: 'Ember', bg: '#12100e', accent: '#c9a227' },
  { key: 'midnight', label: 'Midnight', bg: '#0a0f1e', accent: '#e8c46a' },
  {
    key: 'blossom',
    label: 'Blossom',
    bg: '#f7e6ea',
    accent: '#a8324a',
    swatch: 'linear-gradient(145deg,#ffe0cd 0%,#fcdde6 45%,#e6d9f4 100%)',
  },
  { key: 'slate', label: 'Slate', bg: '#11151a', accent: '#4fd1c5' },
]

const KEYS = new Set(THEMES.map((t) => t.key))

/** Guard a persisted value — an unknown key would silently fall back to the
 *  base palette with no swatch selected, which just looks broken. */
export const validTheme = (key) => (KEYS.has(key) ? key : 'ember')
