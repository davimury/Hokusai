const colors = require('tailwindcss/colors')
module.exports = {
  purge: {
    mode: 'layers',
    content: ['./public/**/*.html', './src/**/*vue']
  },
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        darkgray: "#121212",
        lightgray: "#1e1e1e",
      }
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
