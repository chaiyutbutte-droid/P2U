<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white p-6">
    <div class="bg-green-600 rounded-full p-4 mb-6 animate-bounce">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
    </div>

    <h1 class="text-3xl font-bold mb-2">ชำระเงินสำเร็จแล้วเพคะ! ✨</h1>
    <p class="text-lg text-gray-300 mb-6 text-center">
      ขอบคุณที่เลือกซื้อสินค้ากับเรา<br />
      เจ้าหญิงสามารถตรวจสอบสถานะการจัดส่งได้ที่หน้าประวัติเพคะ
    </p>

    <div class="flex gap-4">
      <button
        @click="goToOrders"
        class="bg-pink-600 hover:bg-pink-700 text-white px-8 py-3 rounded-2xl font-bold shadow-lg shadow-pink-500/20 transition-all hover:scale-105 active:scale-95"
      >
        📦 ดูคำสั่งซื้อ
      </button>

      <button
        @click="goHome"
        class="bg-gray-700 hover:bg-gray-600 text-white px-8 py-3 rounded-2xl font-bold transition-all hover:scale-105 active:scale-95"
      >
        🏠 กลับหน้าแรก
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "PaymentSuccess",

  mounted() {
    // หน้านี้มาถึงคือสำเร็จแล้วเพคะ ไม่ต้องเรียก API สร้างออเดอร์ซ้ำแล้ว
    console.log("Payment flow completed successfully! ✨");
    
    // เคลียร์เศษซากข้อมูลที่อาจหลงเหลือ (เผื่อไว้เพคะ)
    localStorage.removeItem("checkout_items");
  },

  methods: {
    goHome() {
      this.$router.push("/dashboard");
    },

    goToOrders() {
      this.$router.push("/orders");
    },
  },
};
</script>

<style scoped>
/* เพิ่มอนิเมชั่นนิดหน่อยให้ดูสมกับเป็นหน้าสำเร็จเพคะ */
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.animate-bounce {
  animation: bounce 2s infinite;
}
</style>