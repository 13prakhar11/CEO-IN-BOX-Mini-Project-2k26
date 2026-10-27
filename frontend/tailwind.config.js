export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: { navy: { 900: "#0c1626", 800: "#12223a", 700: "#1c3252" }, paper: "#f3f5f8", teal: { 600: "#0e7c86", 700: "#0b646c" } },
      fontFamily: { sans: ['"IBM Plex Sans"', "system-ui", "sans-serif"], serif: ['"Newsreader"', "Georgia", "serif"] },
    },
  },
  plugins: [],
};
