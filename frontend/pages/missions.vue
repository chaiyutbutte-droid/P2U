<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-yellow-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-20 left-10 w-[500px] h-[500px] bg-blue-500/10 blur-[120px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[600px] h-[600px] bg-orange-500/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

    <main class="ml-20 relative z-10 p-6 md:p-10 min-h-screen">
      <div class="max-w-4xl mx-auto w-full animate-in-fade">
        
        <div class="flex flex-col md:flex-row items-start md:items-end justify-between gap-4 mb-10">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-yellow-500/10 border border-yellow-500/20 mb-3">
              <span class="w-1.5 h-1.5 rounded-full bg-yellow-400 animate-pulse"></span>
              <span class="text-[10px] font-bold text-yellow-200 uppercase tracking-widest">Earn Coins</span>
            </div>
            <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-yellow-100 to-yellow-500 tracking-tight">
              ภารกิจพิชิตรางวัล 🎯
            </h1>
            <p class="text-gray-400 mt-2 text-sm md:text-base">
              ทำภารกิจให้สำเร็จเพื่อรับ Coins สะสมไว้ลดราคาสินค้าได้ทันที
            </p>
          </div>
          
          <NuxtLink 
            to="/check-in" 
            class="group flex items-center gap-2 px-6 py-3 rounded-2xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-yellow-500/30 transition-all duration-300"
          >
            <span class="text-xl group-hover:scale-110 transition-transform duration-300">📅</span>
            <span class="font-bold text-gray-200 group-hover:text-yellow-400 transition-colors">ไปหน้าเช็คอิน</span>
          </NuxtLink>
        </div>

        <div class="flex flex-wrap gap-3 mb-8 p-1.5 bg-white/5 backdrop-blur-md rounded-2xl border border-white/5 w-fit">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            class="relative px-6 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 flex items-center gap-2 overflow-hidden"
            :class="activeTab === tab.id ? 'text-black shadow-lg shadow-orange-500/20' : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            <div v-if="activeTab === tab.id" class="absolute inset-0 bg-gradient-to-r from-yellow-400 to-orange-500"></div>
            
            <span class="relative z-10 text-lg">{{ tab.icon }}</span>
            <span class="relative z-10">{{ tab.name }}</span>
          </button>
        </div>

        <div class="space-y-4">
          <TransitionGroup name="list">
            <div 
              v-for="mission in filteredMissions" 
              :key="mission.id" 
              class="group relative bg-[#121215]/60 backdrop-blur-xl rounded-[1.5rem] border border-white/10 p-1 overflow-hidden transition-all duration-300 hover:border-yellow-500/30 hover:bg-[#1a1a20]/80"
              :class="{ 'ring-1 ring-green-500/50 shadow-[0_0_20px_rgba(34,197,94,0.1)]': mission.is_completed && !mission.is_claimed }"
            >
              <div class="relative p-5 flex flex-col md:flex-row items-center gap-6 z-10">
                
                <div class="shrink-0 w-16 h-16 rounded-2xl bg-gradient-to-br from-gray-800 to-black border border-white/10 flex items-center justify-center text-3xl shadow-inner group-hover:scale-105 transition-transform duration-500">
                  {{ getMissionIcon(mission.requirement_type) }}
                </div>

                <div class="flex-1 text-center md:text-left w-full">
                  <div class="flex flex-col md:flex-row md:items-center gap-2 mb-2 justify-center md:justify-start">
                    <h3 class="font-bold text-lg text-white group-hover:text-yellow-100 transition-colors">{{ mission.title }}</h3>
                    
                    <span v-if="mission.is_claimed" class="px-2 py-0.5 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 text-[10px] font-bold uppercase tracking-wider w-fit mx-auto md:mx-0">
                      ✓ Completed
                    </span>
                    <span v-else-if="mission.is_completed" class="px-2 py-0.5 rounded-lg bg-yellow-500/20 border border-yellow-500/40 text-yellow-300 text-[10px] font-bold uppercase tracking-wider animate-pulse w-fit mx-auto md:mx-0">
                      Ready to Claim
                    </span>
                  </div>
                  
                  <p class="text-gray-400 text-sm mb-4">{{ mission.description }}</p>

                  <div class="w-full max-w-md mx-auto md:mx-0">
                    <div class="flex justify-between text-xs font-medium text-gray-500 mb-1.5">
                      <span>Progress</span>
                      <span :class="mission.is_completed ? 'text-green-400' : 'text-gray-300'">
                        {{ mission.progress }} / {{ mission.requirement_value }}
                      </span>
                    </div>
                    <div class="h-2 bg-gray-800 rounded-full overflow-hidden border border-white/5">
                      <div 
                        class="h-full rounded-full transition-all duration-700 ease-out relative"
                        :class="mission.is_completed ? 'bg-gradient-to-r from-green-400 to-emerald-600 shadow-[0_0_10px_rgba(52,211,153,0.5)]' : 'bg-gradient-to-r from-yellow-600 to-orange-600'"
                        :style="{ width: `${Math.min((mission.progress / mission.requirement_value) * 100, 100)}%` }"
                      >
                         <div class="absolute inset-0 bg-white/20 w-full h-full skew-x-12 -translate-x-full animate-shine"></div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="shrink-0 flex flex-col items-center gap-2 min-w-[120px]">
                  <div class="text-sm font-bold text-yellow-500/80 mb-1">Reward</div>
                  <div class="flex items-center gap-1.5 text-yellow-400 font-bold text-xl mb-3 filter drop-shadow-sm">
                    <span>🪙</span>
                    <span>{{ mission.coin_reward }}</span>
                  </div>

                  <button 
                    v-if="mission.is_completed && !mission.is_claimed"
                    @click="claimMission(mission)"
                    class="relative group/btn w-full px-6 py-2.5 rounded-xl overflow-hidden shadow-lg shadow-yellow-500/20 hover:scale-105 active:scale-95 transition-all duration-300"
                  >
                    <div class="absolute inset-0 bg-gradient-to-r from-yellow-400 to-orange-600 animate-shimmer bg-[length:200%_auto]"></div>
                    <span class="relative z-10 text-white font-bold text-sm flex items-center justify-center gap-2">
                       <span>🎁</span> รับรางวัล
                    </span>
                  </button>

                  <div v-else-if="mission.is_claimed" class="w-10 h-10 rounded-full bg-green-500/10 border border-green-500/30 flex items-center justify-center text-green-400 text-lg">
                    ✓
                  </div>

                  <button v-else class="px-6 py-2.5 rounded-xl border border-white/10 bg-white/5 text-gray-500 text-sm font-medium cursor-not-allowed opacity-50">
                    กำลังทำ
                  </button>
                </div>
              </div>
            </div>
          </TransitionGroup>

          <div v-if="!filteredMissions.length" class="py-20 text-center animate-in-fade">
            <div class="w-24 h-24 rounded-3xl bg-white/5 border border-white/10 mx-auto mb-6 flex items-center justify-center text-5xl grayscale opacity-50">
              📭
            </div>
            <h3 class="text-xl font-bold text-white mb-2">ยังไม่มีภารกิจ</h3>
            <p class="text-gray-500">ลองกลับมาดูใหม่ในภายหลังนะ</p>
          </div>
        </div>

        <Teleport to="body">
          <Transition name="bounce">
            <div v-if="claimResult" class="fixed inset-0 z-[100] flex items-center justify-center p-4" @click="claimResult = null">
              <div class="absolute inset-0 bg-black/80 backdrop-blur-xl transition-opacity"></div>
              
              <div class="relative w-full max-w-sm bg-[#18181b] rounded-[3rem] border border-yellow-500/30 shadow-[0_0_80px_rgba(234,179,8,0.2)] p-8 text-center overflow-hidden" @click.stop>
                
                <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-gradient-to-b from-yellow-500/10 to-transparent pointer-events-none"></div>

                <div class="relative w-20 h-20 mx-auto mb-5 bg-gradient-to-tr from-yellow-400 to-orange-500 rounded-full flex items-center justify-center shadow-xl animate-bounce-slow">
                  <span class="text-4xl">🎉</span>
                </div>

                <h2 class="text-2xl font-black text-white mb-2">รับรางวัลสำเร็จ!</h2>
                
                <div class="space-y-3 my-8">
                  <div class="flex justify-between items-center bg-white/5 rounded-2xl p-4 border border-white/5 relative overflow-hidden">
                    <div class="absolute inset-0 bg-yellow-500/5"></div>
                    <span class="text-gray-300 font-medium relative z-10">🪙 Coins ที่ได้</span>
                    <span class="text-2xl font-black text-yellow-400 relative z-10 drop-shadow-sm">+{{ claimResult.coins_earned }}</span>
                  </div>
                  <div class="flex justify-between items-center bg-[#1a1a20] rounded-2xl p-4 border border-white/5">
                     <span class="text-gray-400 text-sm">💰 Balance ใหม่</span>
                     <span class="text-lg font-bold text-white">{{ claimResult.total_coins?.toLocaleString() }}</span>
                  </div>
                </div>

                <button @click="claimResult = null" class="w-full py-3.5 bg-white text-black font-bold rounded-2xl hover:bg-gray-200 transition-all shadow-lg transform active:scale-95">
                  เยี่ยมมาก!
                </button>
              </div>
            </div>
          </Transition>
        </Teleport>

      </div>
    </main>
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
  // Seed missions if first load (Optional logic from prompt)
  axios.post('http://localhost:5000/api/missions/seed').catch(() => {});
});
</script>

<style scoped>
/* Page Animations */
.animate-in-fade {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(15px); }
  100% { opacity: 1; transform: translateY(0); }
}

/* List Transitions */
.list-enter-active,
.list-leave-active {
  transition: all 0.4s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}

/* Shimmer/Shine Animations */
@keyframes shimmer {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}
.animate-shimmer {
  animation: shimmer 3s linear infinite;
}

@keyframes shine {
  0% { transform: translateX(-150%) skewX(12deg); }
  100% { transform: translateX(150%) skewX(12deg); }
}
.animate-shine {
  animation: shine 2s infinite;
}

/* Modal Bounce */
.bounce-enter-active {
  animation: bounce-in 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
.bounce-leave-active {
  animation: bounce-in 0.3s reverse;
}
@keyframes bounce-in {
  0% { transform: scale(0.8); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}

/* Icon Float */
@keyframes bounce-slow {
  0%, 100% { transform: translateY(-5%); }
  50% { transform: translateY(5%); }
}
.animate-bounce-slow {
  animation: bounce-slow 3s infinite ease-in-out;
}
</style>