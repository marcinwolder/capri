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
          '--tw-shadow-color': 'rgba(99, 102, 241, 0.8)', // This is the rgba value for indigo-500 at 50% opacity
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

