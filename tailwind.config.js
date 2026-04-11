/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./.ai/skills/**/*.html",
    "./.ai/skills/**/*.md",
    "./.cursor/skills/**/*.html",
    "./.cursor/skills/**/*.md",
    "./.windsurf/skills/**/*.html",
    "./.windsurf/skills/**/*.md",
    "./src/**/*.html",
    "./templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        // Severity colors
        'p0': '#ef4444',
        'p1': '#f59e0b',
        'p2': '#3b82f6',
        'p3': '#10b981',
      },
    },
  },
  plugins: [],
}
