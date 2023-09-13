/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [,"elCanario/*/templates/*/*.html","elCanario/*/*/*/*/*.html",],
  theme: {
    extend: {},
  },
  plugins: [],
}

// PATH

// npx tailwindcss -o elCanario/static/css/tailwind.css --watch
// npx tailwindcss -o elCanario/articles/static/css/tailwind.css --watch
// npx tailwindcss -o elCanario/authentication/static/css/tailwind.css --watch
// "elCanario/settings/templates/settings/*.html","elCanario/authentication/templates/authentication/*.html","elCanario/customers/templates/customers/*.html","elCanario/customers/templates/customers/partials/*.html","elCanario/customers/templates/customers/htmx/*.html","elCanario/orders/templates/orders/.html","elCanario/orders/templates/orders/*/*.html"