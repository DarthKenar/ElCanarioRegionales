/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["elCanario/articles/templates/articles/*.html","elCanario/articles/templates/articles/*/*.html","elCanario/authentication/templates/authentication/*.html"],
  theme: {
    extend: {},
  },
  plugins: [],
}

// PATH

// npx tailwindcss -o elCanario/static/css/tailwind.css --watch
// npx tailwindcss -o elCanario/articles/static/css/tailwind.css --watch
// npx tailwindcss -o elCanario/authentication/static/css/tailwind.css --watch