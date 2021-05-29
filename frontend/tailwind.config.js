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
        lightergray: "#3b3b3b",
      }
    },
    minWidth: {
      '0': '0',
      '1/4': '25%',
      '1/2': '50%',
      '3/4': '75%',
      'full': '100%',
     },
    maxHeight: {
      '0': '0',
      '1/4': '25%',
      '1/2': '50%',
      '3/4': '75%',
      'full': '100%',
      '70vh':'70vh',
      '38r':'38rem'
     }
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
