<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />
    
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-white mb-2">📅 เช็คอินรายวัน</h1>
        <p class="text-dark-400">เช็คอินทุกวันเพื่อรับ Coins ไว้ลดราคาสินค้า!</p>
      </div>

      <!-- Coins Card -->
      <div class="card p-6 mb-8">
        <div class="flex items-center justify-center gap-4">
          <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center text-4xl">
            🪙
          </div>
          <div class="text-center">
            <p class="text-4xl font-bold text-yellow-400">{{ status.coin_balance?.toLocaleString() || 0 }}</p>
            <p class="text-dark-400">Coins ของคุณ</p>
          </div>
        </div>
        <p class="text-center text-dark-400 text-sm mt-4">💡 ใช้ Coins ลดราคาสินค้าเมื่อชำระเงิน</p>
      </div>

      <!-- Streak & Check-in -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <!-- Streak Card -->
        <div class="card p-6 text-center">
          <div class="text-6xl mb-4">🔥</div>
          <p class="text-4xl font-bold text-orange-400 mb-2">{{ status.streak || 0 }}</p>
          <p class="text-dark-400">วันติดต่อกัน</p>
          <div class="flex justify-center gap-1 mt-4">
            <div 
              v-for="day in 7" 
              :key="day" 
              class="w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold"
              :class="day <= (status.streak % 7 || (status.streak > 0 ? 7 : 0)) ? 'bg-orange-500 text-white' : 'bg-dark-700 text-dark-500'"
            >
              {{ day }}
            </div>
          </div>
        </div>

        <!-- Check-in Button -->
        <div class="card p-6 flex flex-col items-center justify-center">
          <div class="text-6xl mb-4">{{ status.can_check_in ? '🎁' : '✅' }}</div>
          <button 
            @click="doCheckIn"
            :disabled="!status.can_check_in || isLoading"
            class="btn-primary w-full py-4 text-lg font-bold disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isLoading ? 'กำลังเช็คอิน...' : (status.can_check_in ? '📅 เช็คอินเลย!' : '✓ เช็คอินแล้ววันนี้') }}
          </button>
          <p class="text-dark-400 text-sm mt-3">
            {{ status.can_check_in ? 'คลิกเพื่อรับ Coins!' : 'กลับมาพรุ่งนี้นะ' }}
          </p>
        </div>
      </div>

      <!-- Rewards Preview -->
      <div class="card p-6">
        <h3 class="text-lg font-semibold text-white mb-4">🎁 รางวัลพิเศษ</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="glass-light rounded-xl p-4 text-center">
            <p class="text-2xl mb-2">📅</p>
            <p class="text-sm text-white font-medium">เช็คอินทุกวัน</p>
            <p class="text-yellow-400 font-bold">5-19 Coins</p>
          </div>
          <div class="glass-light rounded-xl p-4 text-center">
            <p class="text-2xl mb-2">🔥</p>
            <p class="text-sm text-white font-medium">7 วันติดต่อกัน</p>
            <p class="text-yellow-400 font-bold">+50 Coins</p>
          </div>
          <div class="glass-light rounded-xl p-4 text-center">
            <p class="text-2xl mb-2">🌟</p>
            <p class="text-sm text-white font-medium">30 วันติดต่อกัน</p>
            <p class="text-yellow-400 font-bold">+200 Coins</p>
          </div>
          <div class="glass-light rounded-xl p-4 text-center">
            <p class="text-2xl mb-2">🎯</p>
            <p class="text-sm text-white font-medium">ทำภารกิจ</p>
            <p class="text-yellow-400 font-bold">รับเพิ่ม!</p>
          </div>
        </div>
      </div>

      <!-- Check-in Result Modal -->
      <Teleport to="body">
        <Transition name="fade">
          <div v-if="checkInResult" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click="checkInResult = null">
            <div class="glass rounded-3xl p-8 text-center max-w-sm animate-in" @click.stop>
              <div class="text-6xl mb-4">🎉</div>
              <h2 class="text-2xl font-bold text-white mb-4">เช็คอินสำเร็จ!</h2>
              <div class="space-y-3 mb-6">
                <div class="flex justify-between items-center glass-light rounded-xl p-3">
                  <span class="text-dark-300">🪙 Coins ที่ได้</span>
                  <span class="text-xl font-bold text-yellow-400">+{{ checkInResult.coins_earned }}</span>
                </div>
                <div v-if="checkInResult.milestone_bonus" class="flex justify-between items-center bg-yellow-500/20 rounded-xl p-3 border border-yellow-500/30">
                  <span class="text-yellow-300">🎁 โบนัสพิเศษ!</span>
                  <span class="text-xl font-bold text-yellow-400">+{{ checkInResult.milestone_bonus }}</span>
                </div>
                <div class="flex justify-between items-center glass-light rounded-xl p-3">
                  <span class="text-dark-300">🔥 Streak</span>
                  <span class="text-xl font-bold text-orange-400">{{ checkInResult.streak }} วัน</span>
                </div>
              </div>
              <button @click="checkInResult = null" class="btn-primary w-full">เยี่ยมมาก!</button>
            </div>
          </div>
        </Transition>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const status = ref({});
const checkInResult = ref(null);
const isLoading = ref(false);

const baseUrl = 'http://localhost:5000';

async function fetchStatus() {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    const res = await axios.get(`${baseUrl}/api/check-in/status`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    status.value = res.data;
  } catch (err) {
    console.error('Failed to fetch check-in status:', err);
  }
}

async function doCheckIn() {
  if (!status.value.can_check_in || isLoading.value) return;
  
  isLoading.value = true;
  const token = localStorage.getItem('token');

  try {
    const res = await axios.post(`${baseUrl}/api/check-in`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    checkInResult.value = res.data;
    status.value.can_check_in = false;
    status.value.streak = res.data.streak;
    status.value.coin_balance = res.data.total_coins;
  } catch (err) {
    console.error('Check-in failed:', err);
    alert(err.response?.data?.msg || 'เช็คอินไม่สำเร็จ');
  } finally {
    isLoading.value = false;
  }
}

onMounted(fetchStatus);
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
