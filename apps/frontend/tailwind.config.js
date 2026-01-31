/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin')

module.exports = {
  content: [
    "./src/**/*.{html,ts}",
  ],
  theme: {
    extend: {
      height: {
        screen: ['100vh /* fallback */', '100dvh'],
      },
      animation: {
        'spin-slow': 'spin 2s linear infinite',
      },
      textShadow: {
        sm: '0 1px 2px var(--tw-shadow-color)',
        DEFAULT: '0 2px 4px var(--tw-shadow-color)',
        lg: '0 8px 16px var(--tw-shadow-color)',
      },
    },
  },
  plugins: [
    plugin(function ({ addBase, matchUtilities, theme }) {
      addBase({
        // Applying the default shadow color globally
        ':root': {
          '--tw-shadow-color': 'rgba(15, 31, 46, 0.35)',
        },
      });

      matchUtilities(
        {
          'text-shadow': (value) => ({
            textShadow: value,
          }),
        },
        { values: theme('textShadow') }
      );
    }),
],
  future: {
    hoverOnlyWhenSupported: true,
  },
}
