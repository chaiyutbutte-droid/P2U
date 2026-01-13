import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],

  vite: {
    plugins: [tailwindcss()],
  },

  modules: [],

  app: {
    head: {
      link: [
        { rel: 'stylesheet', href: 'https://cdn.boxicons.com/3.0.3/fonts/basic/boxicons.min.css' }
      ]
    }
  }

});