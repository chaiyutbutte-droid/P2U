<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white p-6">
    <!-- ไอคอนสำเร็จ -->
    <div class="bg-green-600 rounded-full p-4 mb-6">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
    </div>

    <!-- ข้อความหลัก -->
    <h1 class="text-3xl font-bold mb-2">ชำระเงินสำเร็จ!</h1>
    <p class="text-lg text-gray-300 mb-6 text-center">
      ขอบคุณที่ใช้บริการกับเรา<br />
      ระบบได้รับการชำระเงินของคุณเรียบร้อยแล้ว
    </p>

    <!-- ปุ่มทางเลือก -->
    <div class="flex gap-4">
      <button
        @click="goToOrders"
        class="bg-pink-600 hover:bg-pink-700 text-white px-6 py-2 rounded-lg transition"
      >
        ดูคำสั่งซื้อ
      </button>

      <button
        @click="goHome"
        class="bg-gray-700 hover:bg-gray-600 text-white px-6 py-2 rounded-lg transition"
      >
        กลับไปหน้าแรก
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "PaymentSuccess",

  async mounted() {
    // สร้างออเดอร์ให้ผู้ขายทันทีหลังชำระเงินสำเร็จ
    await this.createOrderForSeller();
  },

  methods: {
    async createOrderForSeller() {
      try {
        await axios.post("/api/orders", {
          sellerId: this.$route.query.sellerId, // หรือดึงจาก store
          items: this.$route.query.items,
          totalPrice: this.$route.query.total,
          status: "paid",
        });
      } catch (error) {
        console.error("ส่งออเดอร์ให้ผู้ขายไม่สำเร็จ", error);
      }
    },

    goHome() {
      this.$router.push("/dashboard");
    },

    goToOrders() {
      this.$router.push("/orders");
    },
  },
};
</script>
