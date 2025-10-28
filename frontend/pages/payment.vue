<template>
  <div
    class="min-h-screen bg-gray-900 text-white p-6 flex flex-col items-center"
  >
    <!-- Header -->
    <h1 class="text-3xl font-bold mb-6">Payment Checkout</h1>

    <!-- Product Info -->
    <div class="w-full max-w-3xl bg-gray-800 rounded-lg p-6 mb-6">
      <div class="flex items-center gap-4 mb-4">
        <div class="w-20 h-20 object-cover border-8 bg-white rounded" />
        <div>
          <h2 class="font-semibold text-lg">สินค้าสุดโหด</h2>
          <div class="flex gap-2 text-gray-400 text-sm mt-1">
            <span>฿299.50</span>
          </div>
        </div>
      </div>
      <div class="text-gray-300 text-sm">
        <p>รวม: ฿299.50</p>
        <p>รวมทั้งหมด: ฿299.50</p>
      </div>
    </div>

    <!-- Payment Info -->
    <div class="w-full max-w-3xl bg-gray-800 rounded-lg p-6 mb-6">
      <p class="text-gray-400">วิธีชำระเงิน:</p>
      <div class="flex items-center justify-between mb-2">
        <p class="text-green-400 font-semibold">MasterCard</p>
        <NuxtLink
          to="/paymentMethod"
          class="text-blue-400 text-sm hover:underline hover:text-white"
        >
          (เปลี่ยน)
        </NuxtLink>
      </div>
      <p class="text-gray-400 mt-4 mb-2">บัญชีผู้ใช้:</p>
      <p class="text-white font-semibold">maitonru</p>

      <div class="flex items-center mt-4 mb-4">
        <input type="checkbox" id="terms" class="mr-2" />
        <label for="terms" class="text-gray-400 text-sm">
          ฉันยอมรับข้อกำหนดของ
          <a href="#" class="underline text-blue-400">P2UKAISER</a>
        </label>
      </div>

      <NuxtLink to="/payment_success">
        <button
          class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-lg"
        >
          สั่งซื้อ
        </button>
      </NuxtLink>
    </div>

    <!-- Footer Note -->
    <p class="text-gray-500 text-xs text-center mt-4">
      การยืนยันจะถูกส่งไปยังอีเมลของคุณ
    </p>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
const router = useRouter();

const goToPaymentMethod = () => {
  router.push("/payment-method");
};
</script>
