/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        background: '#0B0F19',
        card: '#111827',
        'card-border': '#1F2937',
        'card-hover': '#1E293B',
        accent: '#3B82F6',
        'accent-cyan': '#06B6D4',
        'accent-emerald': '#10B981',
        'accent-amber': '#F59E0B',
        'accent-rose': '#F43F5E',
      }
    },
  },
  plugins: [],
}
