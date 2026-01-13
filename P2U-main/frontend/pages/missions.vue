<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />
    
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold text-white flex items-center gap-2">
            🎯 ภารกิจ
          </h1>
          <p class="text-dark-400 mt-1">ทำภารกิจรับ Coins ไว้ลดราคาสินค้า!</p>
        </div>
        <NuxtLink to="/check-in" class="btn-accent">
          📅 เช็คอิน
        </NuxtLink>
      </div>

      <!-- Mission Tabs -->
      <div class="flex gap-2 mb-6">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-4 py-2 rounded-xl text-sm font-medium transition-colors"
          :class="activeTab === tab.id ? 'bg-primary-500 text-white' : 'glass text-dark-300 hover:text-white'"
        >
          {{ tab.icon }} {{ tab.name }}
        </button>
      </div>

      <!-- Missions List -->
      <div class="space-y-4">
        <div 
          v-for="mission in filteredMissions" 
          :key="mission.id" 
          class="card p-5 transition-all"
          :class="{ 'border-l-4 border-green-500': mission.is_completed && !mission.is_claimed }"
        >
          <div class="flex items-start gap-4">
            <div class="w-12 h-12 rounded-xl glass flex items-center justify-center text-2xl">
              {{ getMissionIcon(mission.requirement_type) }}
            </div>
            <div class="flex-1">
              <div class="flex items-center gap-2 mb-1">
                <h3 class="font-semibold text-white">{{ mission.title }}</h3>
                <span v-if="mission.is_claimed" class="badge badge-success text-xs">✓ รับแล้ว</span>
                <span v-else-if="mission.is_completed" class="badge badge-primary text-xs animate-pulse">พร้อมรับ!</span>
              </div>
              <p class="text-dark-400 text-sm mb-3">{{ mission.description }}</p>

              <!-- Progress Bar -->
              <div class="mb-3">
                <div class="flex justify-between text-xs text-dark-400 mb-1">
                  <span>ความคืบหน้า</span>
                  <span>{{ mission.progress }} / {{ mission.requirement_value }}</span>
                </div>
                <div class="h-2 bg-dark-700 rounded-full overflow-hidden">
                  <div 
                    class="h-full bg-gradient-to-r from-yellow-500 to-orange-500 rounded-full transition-all duration-300"
                    :style="{ width: `${Math.min((mission.progress / mission.requirement_value) * 100, 100)}%` }"
                  ></div>
                </div>
              </div>

              <!-- Reward -->
              <div class="flex items-center gap-2">
                <span class="text-sm text-yellow-400 font-medium">🪙 {{ mission.coin_reward }} Coins</span>
              </div>
            </div>

            <!-- Claim Button -->
            <button 
              v-if="mission.is_completed && !mission.is_claimed"
              @click="claimMission(mission)"
              class="btn-primary px-6 animate-pulse"
            >
              รับ Coins
            </button>
            <div v-else-if="mission.is_claimed" class="text-green-400 text-2xl">✓</div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="!filteredMissions.length" class="card p-12 text-center">
          <div class="w-20 h-20 rounded-full bg-dark-700 mx-auto mb-4 flex items-center justify-center text-4xl">
            🎯
          </div>
          <h3 class="text-lg font-semibold text-white mb-2">ไม่มีภารกิจ</h3>
          <p class="text-dark-400">ยังไม่มีภารกิจในหมวดนี้</p>
        </div>
      </div>

      <!-- Claim Result Modal -->
      <Teleport to="body">
        <Transition name="fade">
          <div v-if="claimResult" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click="claimResult = null">
            <div class="glass rounded-3xl p-8 text-center max-w-sm animate-in" @click.stop>
              <div class="text-6xl mb-4">🎉</div>
              <h2 class="text-2xl font-bold text-white mb-4">รับ Coins สำเร็จ!</h2>
              <div class="space-y-3 mb-6">
                <div class="flex justify-between items-center glass-light rounded-xl p-3">
                  <span class="text-dark-300">🪙 Coins ที่ได้</span>
                  <span class="text-xl font-bold text-yellow-400">+{{ claimResult.coins_earned }}</span>
                </div>
                <div class="flex justify-between items-center glass-light rounded-xl p-3">
                  <span class="text-dark-300">💰 Coins ทั้งหมด</span>
                  <span class="text-xl font-bold text-yellow-400">{{ claimResult.total_coins }}</span>
                </div>
              </div>
              <button @click="claimResult = null" class="btn-primary w-full">เยี่ยมมาก!</button>
            </div>
          </div>
        </Transition>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

const missions = ref([]);
const activeTab = ref('daily');
const claimResult = ref(null);

const tabs = [
  { id: 'daily', name: 'รายวัน', icon: '📅' },
  { id: 'weekly', name: 'รายสัปดาห์', icon: '📆' },
  { id: 'achievement', name: 'ความสำเร็จ', icon: '🏆' },
];

const filteredMissions = computed(() => {
  return missions.value.filter(m => m.type === activeTab.value);
});

function getMissionIcon(type) {
  const icons = {
    check_in: '📅',
    purchase: '🛒',
    spend: '💰',
    review: '⭐',
    order_count: '📦'
  };
  return icons[type] || '🎯';
}

async function fetchMissions() {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    const res = await axios.get('http://localhost:5000/api/missions', {
      headers: { Authorization: `Bearer ${token}` }
    });
    missions.value = res.data.missions || [];
  } catch (err) {
    console.error('Failed to fetch missions:', err);
  }
}

async function claimMission(mission) {
  const token = localStorage.getItem('token');

  try {
    const res = await axios.post(`http://localhost:5000/api/missions/${mission.id}/claim`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    claimResult.value = res.data;
    mission.is_claimed = true;
  } catch (err) {
    console.error('Failed to claim mission:', err);
    alert(err.response?.data?.msg || 'รับรางวัลไม่สำเร็จ');
  }
}

onMounted(() => {
  fetchMissions();
  // Seed missions if first load
  axios.post('http://localhost:5000/api/missions/seed').catch(() => {});
});
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
