/** @type {import('tailwindcss').Config} */
const defaultTheme = require('tailwindcss/defaultTheme');
module.exports = {
  mode: 'jit',
  content: ['./route_planning/templates/**/*.{html,js}'],
  theme: {
    extend: {
      container: { center: true },
        fontFamily: {
            sans: ['Inter var', ...defaultTheme.fontFamily.sans],
        },
    },
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography')],
};