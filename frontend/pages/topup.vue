<template>
  <div class="min-h-screen bg-gray-900 text-white p-8">
    <h1 class="text-2xl font-bold mb-6">💰 Top-up</h1>

    <div class="bg-gray-800 p-6 rounded-lg max-w-md mx-auto space-y-4">
      
      <!-- Currency Selection -->
      <div class="flex space-x-2 mb-4">
        <button 
          @click="currency = 'coin'"
          class="flex-1 py-2 rounded font-bold transition-colors"
          :class="currency === 'coin' ? 'bg-indigo-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
        >
          Coin (Discount)
        </button>
        <button 
          @click="currency = 'token'"
          class="flex-1 py-2 rounded font-bold transition-colors"
          :class="currency === 'token' ? 'bg-pink-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'"
        >
          Token (Auction)
        </button>
      </div>

      <!-- แสดงยอดปัจจุบัน -->
      <p class="text-gray-300">
        Your current {{ currency }} balance: 
        <span class="font-bold" :class="currency === 'coin' ? 'text-indigo-400' : 'text-pink-400'">
          {{ currency === 'coin' ? userStore.coinBalance : userStore.tokenBalance }}
        </span>
      </p>

      <!-- กรอกจำนวนเงิน -->
      <label class="block text-gray-300 font-semibold mb-1">Amount (THB):</label>
      <input
        type="number"
        v-model.number="amount"
        min="1"
        class="w-full p-2 rounded bg-gray-700 text-white focus:outline-indigo-500"
        placeholder="Enter amount to top-up"
      />

      <!-- ปุ่มสร้าง QR -->
      <button
        class="w-full bg-indigo-600 hover:bg-indigo-700 py-2 rounded font-bold"
        @click="createTopup"
        :disabled="loading || amount < 1"
      >
        {{ loading ? 'Processing...' : 'Generate QR / Top-up' }}
      </button>

      <!-- ข้อความ error -->
      <p v-if="error" class="text-red-400">{{ error }}</p>

      <!-- แสดง QR หลังสร้างสำเร็จ -->
      <div v-if="qrData" class="text-center mt-4">
        <p class="mb-2">Scan this QR to pay:</p>
        <img :src="qrData.qr_url" alt="Topup QR" class="mx-auto w-64 h-64 object-contain rounded-lg shadow-lg" />
        <p class="mt-2 text-gray-400">Amount: {{ qrData.amount }} THB</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/user";

const userStore = useUserStore();

const amount = ref(0);
const loading = ref(false);
const error = ref(null);
const qrData = ref(null);

/**
 * ฟังก์ชันเรียก API backend เพื่อสร้าง Topup QR
 */
const createTopup = async () => {
  if (amount.value < 1) return;

  loading.value = true;
  error.value = null;
  qrData.value = null;

  try {
    // เรียก action topupCoin ใน store
    const res = await userStore.topupCoin(amount.value, 'promptpay', null, currency.value);

    // ตัวอย่าง response: { qr_url: "...", amount: 100 }
    qrData.value = res;

    // อัปเดตยอด Coin (ถ้ามีการเพิ่มทันทีหลังชำระเสร็จ)
    userStore.loadUser();
  } catch (err) {
    error.value = err.response?.data?.msg || err.message || "Top-up failed";
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* เพิ่ม style เล็กน้อยให้สวยงาม */
</style>
