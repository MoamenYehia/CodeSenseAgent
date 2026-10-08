/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        crimson: '#790D16',
        'crimson-deep': '#4E0A10',
        'crimson-tint': '#F3DEDF',
        sand: '#E5D3AF',
        cream: '#F5EFE1',
        mist: '#AEC4D4',
        ink: '#231416',
        'ink-soft': '#5A4A4C',
        paper: '#FBF8F0',
        line: '#DCCFB4',
        success: '#2F6B4F',
        warning: '#B7791F',
        error: '#B42318',
      },
      fontFamily: {
        display: ['Fraunces', 'serif'],
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        card: '0 1px 2px rgba(35,20,22,.06), 0 8px 24px rgba(35,20,22,.06)',
      },
      borderRadius: {
        card: '1rem',
      },
    },
  },
  plugins: [],
}
