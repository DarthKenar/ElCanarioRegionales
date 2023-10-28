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
  plugins: [
    require("tw-elements/dist/plugin.cjs"),
    require("daisyui"),
  ],
  daisyui: {
    themes: [{
      luci: {
      
        "primary": "#a78bfa",
              
        "secondary": "#a5b4fc",
              
        "accent": "#7c3aed",
              
        "neutral": "#6366f1",
              
        "base-100": "#e9d5ff",
              
        "info": "#bae6fd",
              
        "success": "#bbf7d0",
              
        "warning": "#fde68a",
              
        "error": "#fda4af",
      }
    },
    "light", "dark", "valentine","cyberpunk","retro",
  ]},
  
}
// PATH
// npx tailwindcss -i elCanario/elCanario/staticfiles/css/input.css -o elCanario/elCanario/staticfiles/css/output.css --watch
// npx tailwindcss -o elCanario/elCanario/static/css/tailwind.css --watch
// npx tailwindcss -o elCanario/articles/static/css/tailwind.css --watch
// npx tailwindcss -o elCanario/authentication/static/css/tailwind.css --watch
// "elCanario/settings/templates/settings/*.html","elCanario/authentication/templates/authentication/*.html","elCanario/customers/templates/customers/*.html","elCanario/customers/templates/customers/partials/*.html","elCanario/customers/templates/customers/htmx/*.html","elCanario/orders/templates/orders/.html","elCanario/orders/templates/orders/*/*.html"