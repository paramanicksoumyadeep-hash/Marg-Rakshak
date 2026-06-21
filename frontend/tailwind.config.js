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
        background: "#ffffff",
        foreground: "#111111",
        panel: "#222222",
        "panel-foreground": "#ffffff",
        primary: "#DF1B12", // TomTom Red
        "primary-hover": "#C0160F",
        secondary: "#5E0035", // Deep Purple
        accent: "#F0EFEF",
        muted: "#717171",
        border: "#E0E0E0",
        severity: {
          high: "#DF1B12", // Red
          medium: "#E36C0A", // Orange
          low: "#E8B00C", // Yellow
        }
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
      }
    },
  },
  plugins: [],
}
