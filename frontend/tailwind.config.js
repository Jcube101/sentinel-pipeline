/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        'bg-primary': '#0a0a0f',
        'bg-secondary': '#111118',
        'bg-card': '#16161f',
        'border-color': '#2a2a3a',
        'text-muted': '#7070a0',
        accent: '#f97316',
        fire: '#ef4444',
        flood: '#3b82f6',
        cyclone: '#8b5cf6',
        earthquake: '#f59e0b',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
