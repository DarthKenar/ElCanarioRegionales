/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["elCanario/articles/templates/*.html","elCanario/articles/templates/*/*.html","elCanario/authentication/templates/*.html","elCanario/authentication/templates/*/*.html"],
  theme: {
    extend: {},
  },
  plugins: [],
}
// npx tailwindcss -o elCanario/static/css/tailwind.css --watch
// npx tailwindcss -o elCanario/articles/static/css/tailwind.css --watch
// npx tailwindcss -o elCanario/authentication/static/css/tailwind.css --watch