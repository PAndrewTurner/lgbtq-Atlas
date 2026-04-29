import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg:           'var(--bg)',
        surface:      'var(--surface)',
        'surface-alt':'var(--surface-alt)',
        border:       'var(--border)',
      },
      fontFamily: {
        display: ['DM Serif Display', 'serif'],
        body:    ['Outfit', 'sans-serif'],
        mono:    ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
} satisfies Config
