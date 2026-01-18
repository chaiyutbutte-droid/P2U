<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-[#050505] text-white p-6 relative overflow-hidden font-sans">
    
    <div class="fixed top-1/4 left-1/4 w-[500px] h-[500px] bg-pink-600/20 blur-[120px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-1/4 right-1/4 w-[500px] h-[500px] bg-purple-900/20 blur-[120px] rounded-full pointer-events-none z-0"></div>

    <div class="relative z-10 bg-[#121212]/80 backdrop-blur-2xl border border-white/10 rounded-[2.5rem] p-8 md:p-12 max-w-md w-full text-center shadow-2xl shadow-pink-900/20 group">
      
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-1/3 h-1 bg-gradient-to-r from-transparent via-pink-500 to-transparent"></div>

      <div class="mb-8 relative flex justify-center">
        <div class="absolute w-24 h-24 bg-pink-500/30 rounded-full animate-ping opacity-75"></div>
        <div class="absolute w-24 h-24 bg-pink-500/20 rounded-full blur-xl"></div>
        
        <div class="relative w-24 h-24 bg-gradient-to-tr from-pink-600 to-purple-600 rounded-full flex items-center justify-center shadow-lg shadow-pink-500/40 z-10 transform transition-transform hover:scale-110 duration-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-white drop-shadow-md" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
          </svg>
        </div>
      </div>

      <h1 class="text-3xl md:text-4xl font-black mb-3 tracking-tight">
        <span class="bg-clip-text text-transparent bg-gradient-to-r from-white via-pink-200 to-white">
          ชำระเงินสำเร็จ!
        </span> ✨
      </h1>
      
      <p class="text-gray-400 text-sm md:text-base mb-10 leading-relaxed font-light">
        ขอบคุณที่เลือกซื้อสินค้ากับเราเพคะ<br />
        เจ้าหญิงสามารถตรวจสอบสถานะการจัดส่ง<br/>ได้ที่หน้าประวัติคำสั่งซื้อ
      </p>

      <div class="flex flex-col gap-3">
        <button
          @click="goToOrders"
          class="w-full py-3.5 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white rounded-xl font-bold shadow-lg shadow-pink-500/25 transition-all hover:scale-[1.02] hover:shadow-pink-500/40 active:scale-95 flex items-center justify-center gap-2 group/btn"
        >
          <span>📦</span> ดูคำสั่งซื้อ
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform group-hover/btn:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
          </svg>
        </button>

        <button
          @click="goHome"
          class="w-full py-3.5 bg-[#1a1a1a] hover:bg-[#252525] text-gray-300 hover:text-white border border-white/5 hover:border-white/20 rounded-xl font-bold transition-all active:scale-95 flex items-center justify-center gap-2"
        >
          <span>🏠</span> กลับหน้าแรก
        </button>
      </div>
    </div>
    
    <p class="absolute bottom-6 text-[#333] text-xs font-mono uppercase tracking-widest">Transaction Completed</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push("/dashboard")
}

const goToOrders = () => {
  router.push("/orders")
}

onMounted(() => {
  console.log("Payment flow completed successfully! ✨")
  // เคลียร์เศษซากข้อมูลที่อาจหลงเหลือ
  if (process.client) {
    localStorage.removeItem("checkout_items")
  }
})
</script>

<style scoped>
/* ไม่มี style พิเศษเพราะใช้ Tailwind class ทั้งหมด เพื่อป้องกันปัญหา @apply */
</style>