// plugins/pinia.js
import { createPinia } from 'pinia'

export default defineNuxtPlugin((nuxtApp) => {
  // สร้าง instance ของ Pinia
  const pinia = createPinia()
  
  // ใช้งาน Pinia กับ Vue app ของ Nuxt
  nuxtApp.vueApp.use(pinia)
})
