/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./.{ai,cursor,windsurf}/skills/**/*.{html,md}",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        severity: {
          p0: '#ef4444',
          p1: '#f59e0b',
          p2: '#3b82f6',
          p3: '#10b981',
        },
      },
    },
  },
  safelist: [
    {
      pattern: /(bg|text|border)-severity-(p0|p1|p2|p3)/,
    },
  ],
  plugins: [require('@tailwindcss/typography')],
};
