<template>
  <div class="min-h-screen bg-gray-900 text-white flex flex-col items-center py-10">
    <h1 class="text-3xl font-bold mb-10">วิธีชำระเงิน</h1>

    <div class="w-full max-w-4xl bg-gray-800 p-8 rounded-lg shadow-lg flex flex-col md:flex-row justify-between">
      <!-- ซ้าย -->
      <div class="md:w-2/3 mb-6 md:mb-0">
        <h2 class="text-xl font-semibold mb-4">โปรดเลือกวิธีชำระเงิน</h2>
        <select
          v-model="selected"
          class="w-full bg-gray-700 text-white p-3 rounded border border-gray-600 mb-4"
        >
          <option disabled value="">-- กรุณาเลือก --</option>
          <option>MasterCard</option>
          <option>Visa</option>
          <option>PayPal</option>
          <option>TrueMoney</option>
          <option>ธนาคารไทยพาณิชย์ (SCB)</option>
          <option>PromptPay</option>
        </select>

        <button
          @click="goToPayment"
          class="bg-pink-500 hover:bg-pink-600 text-black font-semibold px-6 py-3 rounded transition"
        >
          ดำเนินการต่อ
        </button>

        <p v-if="selected" class="mt-4 text-green-400 font-semibold">
          ✅ คุณเลือก: {{ selected }}
        </p>
      </div>

      <!-- ขวา -->
      <div class="md:w-1/3 bg-gray-700 rounded ml-5 p-4">
        <h3 class="text-lg font-semibold mb-4">วิธีชำระเงินที่รองรับ</h3>
        <div class="flex flex-wrap gap-2">
          <img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg" class="w-14 h-8 bg-white p-1 rounded" />
          <img src="https://upload.wikimedia.org/wikipedia/commons/0/04/Visa.svg" class="w-14 h-8 bg-white p-1 rounded" />
          <img src="https://upload.wikimedia.org/wikipedia/commons/0/0e/Mastercard-logo.png" class="w-14 h-8 bg-white p-1 rounded" />
          <img src="https://upload.wikimedia.org/wikipedia/commons/a/a4/TrueMoney_Wallet_Logo.png" class="w-14 h-8 bg-white p-1 rounded" />
          <img src="https://upload.wikimedia.org/wikipedia/commons/d/d3/PromptPay_Logo.png" class="w-14 h-8 bg-white p-1 rounded" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref } from "vue";

const router = useRouter();
const selected = ref("");

const goToPayment = () => {
  if (!selected.value) {
    alert("กรุณาเลือกวิธีชำระเงินก่อน");
    return;
  }

  // ส่งค่าที่เลือกไปหน้าชำระเงิน
  router.push({
    path: "/payment",
    query: { method: selected.value }
  });
};
</script>