<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />

    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-white flex items-center gap-3">
          🏆 อันดับผู้ขาย
        </h1>
        <p class="text-dark-400 mt-1">จัดอันดับตามคะแนน AI Score</p>
      </div>

      <!-- Level Filter Pills -->
      <div class="flex gap-2 mb-6 flex-wrap">
        <button 
          v-for="level in levels" 
          :key="level.id"
          @click="selectedLevel = level.id"
          class="px-4 py-2 rounded-full text-sm font-medium transition-all"
          :class="selectedLevel === level.id 
            ? 'bg-primary-500 text-white' 
            : 'glass text-dark-300 hover:bg-dark-700'"
        >
          {{ level.icon }} {{ level.name }}
        </button>
      </div>

      <!-- Top 3 Podium -->
      <div v-if="!selectedLevel && topSellers.length >= 3" class="mb-10">
        <div class="flex justify-center items-end gap-4">
          <!-- 2nd Place -->
          <div class="text-center animate-in" style="animation-delay: 0.1s">
            <div class="w-24 h-24 rounded-full mx-auto mb-3 ring-4 ring-gray-400 overflow-hidden bg-dark-700">
              <img :src="topSellers[1]?.profile_image || '/default-avatar.png'" class="w-full h-full object-cover" />
            </div>
            <div class="bg-gray-400 text-black px-4 py-2 rounded-t-lg">
              <span class="text-2xl">🥈</span>
            </div>
            <div class="glass rounded-b-lg p-4 w-40">
              <p class="text-white font-semibold truncate">{{ topSellers[1]?.shop_name }}</p>
              <p class="text-primary-400 font-bold">{{ topSellers[1]?.ai_score }} pts</p>
              <span class="text-xs px-2 py-1 rounded-full" :style="{ backgroundColor: topSellers[1]?.badge?.color }">
                {{ topSellers[1]?.badge?.icon }} {{ topSellers[1]?.ai_level }}
              </span>
            </div>
          </div>

          <!-- 1st Place -->
          <div class="text-center animate-in">
            <div class="w-32 h-32 rounded-full mx-auto mb-3 ring-4 ring-yellow-400 overflow-hidden bg-dark-700">
              <img :src="topSellers[0]?.profile_image || '/default-avatar.png'" class="w-full h-full object-cover" />
            </div>
            <div class="bg-yellow-400 text-black px-6 py-3 rounded-t-lg">
              <span class="text-3xl">🥇</span>
            </div>
            <div class="glass rounded-b-lg p-4 w-48">
              <p class="text-white font-bold text-lg truncate">{{ topSellers[0]?.shop_name }}</p>
              <p class="text-primary-400 font-bold text-xl">{{ topSellers[0]?.ai_score }} pts</p>
              <span class="text-sm px-3 py-1 rounded-full" :style="{ backgroundColor: topSellers[0]?.badge?.color }">
                {{ topSellers[0]?.badge?.icon }} {{ topSellers[0]?.ai_level }}
              </span>
            </div>
          </div>

          <!-- 3rd Place -->
          <div class="text-center animate-in" style="animation-delay: 0.2s">
            <div class="w-24 h-24 rounded-full mx-auto mb-3 ring-4 ring-orange-600 overflow-hidden bg-dark-700">
              <img :src="topSellers[2]?.profile_image || '/default-avatar.png'" class="w-full h-full object-cover" />
            </div>
            <div class="bg-orange-600 text-white px-4 py-2 rounded-t-lg">
              <span class="text-2xl">🥉</span>
            </div>
            <div class="glass rounded-b-lg p-4 w-40">
              <p class="text-white font-semibold truncate">{{ topSellers[2]?.shop_name }}</p>
              <p class="text-primary-400 font-bold">{{ topSellers[2]?.ai_score }} pts</p>
              <span class="text-xs px-2 py-1 rounded-full" :style="{ backgroundColor: topSellers[2]?.badge?.color }">
                {{ topSellers[2]?.badge?.icon }} {{ topSellers[2]?.ai_level }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Leaderboard Table -->
      <div class="card overflow-hidden">
        <div class="p-4 border-b border-dark-700 flex justify-between items-center">
          <h2 class="text-lg font-semibold text-white">📊 ตารางอันดับ</h2>
          <span class="text-dark-400 text-sm">ทั้งหมด {{ pagination.total }} ร้าน</span>
        </div>

        <div v-if="loading" class="p-10 text-center">
          <div class="animate-spin w-10 h-10 border-4 border-primary-500 border-t-transparent rounded-full mx-auto"></div>
          <p class="text-dark-400 mt-4">กำลังโหลด...</p>
        </div>

        <div v-else-if="leaderboard.length" class="divide-y divide-dark-700">
          <div 
            v-for="seller in leaderboard" 
            :key="seller.id"
            class="flex items-center justify-between p-4 hover:bg-dark-800/50 transition-colors cursor-pointer"
            @click="openSellerDetail(seller)"
          >
            <div class="flex items-center gap-4">
              <!-- Rank -->
              <div 
                class="w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg"
                :class="getRankClass(seller.rank)"
              >
                {{ seller.rank <= 3 ? ['🥇', '🥈', '🥉'][seller.rank - 1] : seller.rank }}
              </div>

              <!-- Avatar -->
              <div class="w-12 h-12 rounded-full overflow-hidden bg-dark-700 ring-2"
                   :style="{ borderColor: seller.badge?.color }">
                <img :src="seller.profile_image || '/default-avatar.png'" class="w-full h-full object-cover" />
              </div>

              <!-- Info -->
              <div>
                <div class="flex items-center gap-2">
                  <p class="text-white font-semibold">{{ seller.shop_name }}</p>
                  <span v-if="seller.is_verified" class="text-blue-400 text-sm">💎</span>
                  <span v-if="seller.is_phone_verified" class="text-green-400 text-sm">📱</span>
                </div>
                <div class="flex items-center gap-2 text-sm">
                  <span class="px-2 py-0.5 rounded text-xs font-medium" :style="{ backgroundColor: seller.badge?.color + '33', color: seller.badge?.color }">
                    {{ seller.badge?.icon }} {{ seller.badge?.name }}
                  </span>
                  <span class="text-yellow-400">⭐ {{ seller.rating_avg?.toFixed(1) || '0.0' }}</span>
                </div>
              </div>
            </div>

            <!-- Score -->
            <div class="text-right">
              <p class="text-2xl font-bold text-primary-400">{{ seller.ai_score }}</p>
              <p class="text-dark-400 text-xs">points</p>
            </div>
          </div>
        </div>

        <div v-else class="p-10 text-center">
          <p class="text-dark-400">ไม่พบข้อมูลผู้ขาย</p>
        </div>

        <!-- Pagination -->
        <div v-if="pagination.total_pages > 1" class="p-4 border-t border-dark-700 flex justify-center gap-2">
          <button 
            @click="changePage(pagination.page - 1)"
            :disabled="pagination.page <= 1"
            class="px-3 py-1 rounded glass text-dark-300 disabled:opacity-50"
          >
            ←
          </button>
          <span class="px-4 py-1 text-white">{{ pagination.page }} / {{ pagination.total_pages }}</span>
          <button 
            @click="changePage(pagination.page + 1)"
            :disabled="pagination.page >= pagination.total_pages"
            class="px-3 py-1 rounded glass text-dark-300 disabled:opacity-50"
          >
            →
          </button>
        </div>
      </div>

      <!-- Seller Detail Modal -->
      <Teleport to="body">
        <Transition name="fade">
          <div v-if="selectedSeller" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click="selectedSeller = null">
            <div class="glass rounded-2xl w-full max-w-md p-6 animate-in" @click.stop>
              <!-- Header -->
              <div class="flex justify-between items-start mb-6">
                <div class="flex items-center gap-4">
                  <div class="w-16 h-16 rounded-full overflow-hidden bg-dark-700 ring-2" :style="{ borderColor: selectedSeller.badge?.color }">
                    <img :src="selectedSeller.profile_image || '/default-avatar.png'" class="w-full h-full object-cover" />
                  </div>
                  <div>
                    <h3 class="text-xl font-bold text-white">{{ selectedSeller.shop_name }}</h3>
                    <span class="px-3 py-1 rounded-full text-sm" :style="{ backgroundColor: selectedSeller.badge?.color }">
                      {{ selectedSeller.badge?.icon }} {{ selectedSeller.badge?.name }}
                    </span>
                  </div>
                </div>
                <button @click="selectedSeller = null" class="text-dark-400 hover:text-white text-xl">✕</button>
              </div>

              <!-- Stats -->
              <div class="grid grid-cols-2 gap-4 mb-6">
                <div class="glass-light rounded-xl p-4 text-center">
                  <p class="text-3xl font-bold text-primary-400">{{ selectedSeller.ai_score }}</p>
                  <p class="text-dark-400 text-sm">AI Score</p>
                </div>
                <div class="glass-light rounded-xl p-4 text-center">
                  <p class="text-3xl font-bold text-yellow-400">{{ selectedSeller.rating_avg?.toFixed(1) || '0.0' }}</p>
                  <p class="text-dark-400 text-sm">Rating</p>
                </div>
              </div>

              <!-- Verification Status -->
              <div class="mb-6">
                <p class="text-white font-semibold mb-3">✅ การยืนยันตัวตน</p>
                <div class="flex flex-wrap gap-2">
                  <span class="px-3 py-1 rounded-full text-sm" 
                        :class="selectedSeller.verification?.email ? 'bg-green-500/20 text-green-400' : 'bg-dark-700 text-dark-400'">
                    📧 Email {{ selectedSeller.verification?.email ? '✓' : '✗' }}
                  </span>
                  <span class="px-3 py-1 rounded-full text-sm" 
                        :class="selectedSeller.verification?.phone ? 'bg-green-500/20 text-green-400' : 'bg-dark-700 text-dark-400'">
                    📱 Phone {{ selectedSeller.verification?.phone ? '✓' : '✗' }}
                  </span>
                  <span class="px-3 py-1 rounded-full text-sm" 
                        :class="selectedSeller.verification?.id_card ? 'bg-green-500/20 text-green-400' : 'bg-dark-700 text-dark-400'">
                    💎 ID Card {{ selectedSeller.verification?.id_card ? '✓' : '✗' }}
                  </span>
                </div>
              </div>

              <!-- Score Breakdown -->
              <div v-if="selectedSeller.score_breakdown">
                <p class="text-white font-semibold mb-3">📊 รายละเอียดคะแนน</p>
                <div class="space-y-3">
                  <div v-for="(value, key) in selectedSeller.score_breakdown" :key="key">
                    <div class="flex justify-between text-sm mb-1">
                      <span class="text-dark-300 capitalize">{{ getScoreLabel(key) }}</span>
                      <span class="text-white">{{ value.toFixed(0) }}%</span>
                    </div>
                    <div class="h-2 bg-dark-700 rounded-full overflow-hidden">
                      <div class="h-full bg-gradient-to-r from-primary-500 to-accent-500 rounded-full transition-all" 
                           :style="{ width: value + '%' }"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';

const baseUrl = 'http://localhost:5000';

const leaderboard = ref([]);
const loading = ref(true);
const selectedLevel = ref(null);
const selectedSeller = ref(null);
const pagination = ref({ page: 1, per_page: 20, total: 0, total_pages: 1 });

const levels = [
  { id: null, name: 'ทั้งหมด', icon: '🏆' },
  { id: 'S', name: 'Top Seller', icon: '🥇' },
  { id: 'A', name: 'Star Seller', icon: '⭐' },
  { id: 'B', name: 'Verified', icon: '✓' },
  { id: 'C', name: 'Basic', icon: '📦' },
];

const topSellers = computed(() => leaderboard.value.slice(0, 3));

const scoreLabels = {
  sales: '💰 ยอดขาย',
  rating: '⭐ คะแนนรีวิว',
  delivery: '🚚 ความเร็วจัดส่ง',
  response: '💬 อัตราตอบกลับ',
  cancel: '❌ อัตรายกเลิก',
  verification: '✅ การยืนยันตัวตน'
};

function getScoreLabel(key) {
  return scoreLabels[key] || key;
}

function getRankClass(rank) {
  if (rank === 1) return 'bg-yellow-500 text-black';
  if (rank === 2) return 'bg-gray-400 text-black';
  if (rank === 3) return 'bg-orange-600 text-white';
  return 'bg-dark-700 text-dark-300';
}

async function fetchLeaderboard(page = 1) {
  loading.value = true;
  try {
    const params = { page, per_page: 20 };
    if (selectedLevel.value) params.level = selectedLevel.value;
    
    const res = await axios.get(`${baseUrl}/api/seller/rank/leaderboard`, { params });
    leaderboard.value = res.data.leaderboard || [];
    pagination.value = res.data.pagination || { page: 1, total: 0, total_pages: 1 };
  } catch (err) {
    console.error('Failed to fetch leaderboard:', err);
  } finally {
    loading.value = false;
  }
}

async function openSellerDetail(seller) {
  try {
    const res = await axios.get(`${baseUrl}/api/seller/rank/${seller.id}`);
    selectedSeller.value = res.data;
  } catch (err) {
    console.error('Failed to fetch seller details:', err);
    selectedSeller.value = seller;
  }
}

function changePage(page) {
  if (page >= 1 && page <= pagination.value.total_pages) {
    fetchLeaderboard(page);
  }
}

watch(selectedLevel, () => {
  fetchLeaderboard(1);
});

onMounted(() => {
  fetchLeaderboard();
});
</script>

<style scoped>
.animate-in {
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
