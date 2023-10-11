/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
  "elCanario/*/templates/*/*.html",
  "elCanario/*/templates/*/*/*.html",
  "elCanario/*/templates/*.html",
  "./node_modules/tw-elements/dist/js/**/*.js"],
  theme: {
    extend: {},
  },
  darkMode: "class",
  plugins: [require("tw-elements/dist/plugin.cjs")],
}
// PATH
// npx tailwindcss -i elCanario/elCanario/staticfiles/css/input.css -o elCanario/elCanario/staticfiles/css/output.css --watch
// npx tailwindcss -o elCanario/elCanario/static/css/tailwind.css --watch
// npx tailwindcss -o elCanario/articles/static/css/tailwind.css --watch
// npx tailwindcss -o elCanario/authentication/static/css/tailwind.css --watch
// "elCanario/settings/templates/settings/*.html","elCanario/authentication/templates/authentication/*.html","elCanario/customers/templates/customers/*.html","elCanario/customers/templates/customers/partials/*.html","elCanario/customers/templates/customers/htmx/*.html","elCanario/orders/templates/orders/.html","elCanario/orders/templates/orders/*/*.html"