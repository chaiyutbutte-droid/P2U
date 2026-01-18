<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-yellow-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[600px] bg-orange-500/10 blur-[130px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[600px] h-[600px] bg-purple-900/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

    <main class="ml-20 relative z-10 p-6 md:p-10 min-h-screen flex flex-col justify-center">
      
      <div class="max-w-5xl mx-auto w-full animate-in-fade">
        
        <header class="text-center mb-10">
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-yellow-500/10 border border-yellow-500/20 mb-4">
             <span class="animate-pulse w-2 h-2 rounded-full bg-yellow-400"></span>
             <span class="text-xs font-bold text-yellow-200 uppercase tracking-widest">Daily Rewards</span>
          </div>
          <h1 class="text-4xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-yellow-200 to-orange-200 tracking-tight drop-shadow-sm mb-4">
            เช็คอินรายวัน 📅
          </h1>
          <p class="text-gray-400 text-lg max-w-xl mx-auto">
            สะสม Coins ทุกวัน เพื่อใช้เป็นส่วนลดและแลกของรางวัลสุดพิเศษ
          </p>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8">
          
          <div class="lg:col-span-7 space-y-6">
            
            <div class="relative bg-[#121215]/60 backdrop-blur-xl rounded-[2.5rem] border border-white/10 p-8 overflow-hidden group hover:border-yellow-500/30 transition-all duration-500">
               <div class="absolute top-0 right-0 w-64 h-64 bg-yellow-500/10 blur-[80px] rounded-full group-hover:bg-yellow-500/20 transition-all duration-700"></div>
               
               <div class="relative z-10 flex flex-col sm:flex-row items-center sm:items-start gap-6 text-center sm:text-left">
                  <div class="w-24 h-24 rounded-3xl bg-gradient-to-br from-yellow-400 via-orange-500 to-red-500 flex items-center justify-center text-5xl shadow-2xl shadow-orange-500/30 transform group-hover:scale-110 group-hover:rotate-6 transition-all duration-500">
                     🪙
                  </div>
                  <div>
                     <p class="text-gray-400 font-medium mb-1">Coins ของคุณ</p>
                     <p class="text-5xl md:text-6xl font-black text-transparent bg-clip-text bg-gradient-to-b from-white to-gray-300 tracking-tight">
                        {{ status.coin_balance?.toLocaleString() || 0 }}
                     </p>
                     <p class="text-yellow-500/80 text-sm mt-2 font-bold flex items-center justify-center sm:justify-start gap-2">
                        <span>✨</span> ใช้ลดราคาสินค้าได้ทันที
                     </p>
                  </div>
               </div>
            </div>

            <div class="bg-[#121215]/60 backdrop-blur-xl rounded-[2.5rem] border border-white/10 p-8 flex flex-col items-center justify-center text-center relative overflow-hidden">
               
               <button 
                  @click="doCheckIn"
                  :disabled="!status.can_check_in || isLoading"
                  class="relative group w-full py-6 rounded-2xl overflow-hidden transition-all duration-300 transform hover:-translate-y-1 active:translate-y-1 disabled:cursor-not-allowed disabled:transform-none disabled:opacity-90"
               >
                  <div class="absolute inset-0 transition-all duration-300"
                    :class="status.can_check_in 
                      ? 'bg-gradient-to-r from-yellow-500 via-orange-500 to-yellow-500 bg-[length:200%_auto] animate-shimmer shadow-[0_0_30px_rgba(234,179,8,0.4)]' 
                      : 'bg-[#1a1a20] border border-green-500/30'"
                  ></div>
                  
                  <div class="relative flex items-center justify-center gap-3">
                     <span class="text-3xl filter drop-shadow-md">
                        {{ isLoading ? '⏳' : (status.can_check_in ? '👆' : '🎉') }}
                     </span>
                     <span class="text-xl md:text-2xl font-bold"
                        :class="status.can_check_in ? 'text-white' : 'text-green-400'"
                     >
                        {{ isLoading ? 'กำลังประมวลผล...' : (status.can_check_in ? 'กดปุ่มเพื่อเช็คอิน!' : 'เช็คอินวันนี้เรียบร้อย') }}
                     </span>
                  </div>
               </button>

               <p class="mt-4 text-gray-500 text-sm">
                 {{ status.can_check_in ? 'อย่าลืมกลับมาเช็คอินพรุ่งนี้นะ!' : 'กลับมาใหม่พรุ่งนี้เพื่อรับ Coins เพิ่ม' }}
               </p>
            </div>
          </div>

          <div class="lg:col-span-5 space-y-6">
             
             <div class="bg-gradient-to-br from-[#1a1a20] to-[#121215] backdrop-blur-xl rounded-[2.5rem] border border-white/10 p-8 text-center relative overflow-hidden">
                <div class="absolute top-[-20px] right-[-20px] text-[10rem] opacity-[0.03] grayscale pointer-events-none">🔥</div>
                
                <h3 class="text-gray-400 text-sm font-bold uppercase tracking-wider mb-2">Current Streak</h3>
                <div class="flex items-center justify-center gap-3 mb-6">
                   <span class="text-5xl animate-bounce-slow">🔥</span>
                   <span class="text-6xl font-black text-white">{{ status.streak || 0 }}</span>
                   <span class="text-xl text-gray-500 self-end mb-2">วัน</span>
                </div>

                <div class="flex justify-between items-center px-2">
                   <div 
                      v-for="day in 7" 
                      :key="day"
                      class="flex flex-col items-center gap-2 group"
                   >
                      <div 
                        class="w-10 h-10 md:w-11 md:h-11 rounded-full flex items-center justify-center border-2 transition-all duration-300 relative z-10"
                        :class="day <= (status.streak % 7 || (status.streak > 0 ? 7 : 0)) 
                           ? 'bg-orange-500 border-orange-500 shadow-[0_0_15px_rgba(249,115,22,0.5)] text-white scale-110' 
                           : 'border-white/10 bg-white/5 text-gray-600'"
                      >
                         <span class="text-sm font-bold">{{ day }}</span>
                         <div v-if="day === (status.streak % 7) + 1" class="absolute inset-0 rounded-full border border-orange-500 animate-ping"></div>
                      </div>
                      </div>
                </div>
             </div>

             <div class="bg-[#121215]/60 backdrop-blur-xl rounded-[2.5rem] border border-white/10 p-6 md:p-8">
                <h3 class="text-white font-bold mb-4 flex items-center gap-2">
                   <span>🎁</span> รางวัลพิเศษ
                </h3>
                <div class="grid grid-cols-2 gap-3">
                   <div class="bg-white/5 rounded-2xl p-4 border border-white/5 text-center hover:bg-white/10 transition-colors">
                      <p class="text-2xl mb-1">📅</p>
                      <p class="text-[10px] text-gray-400 mb-1">ทุกวัน</p>
                      <p class="text-yellow-400 font-bold text-sm">5-19 Coins</p>
                   </div>
                   <div class="bg-white/5 rounded-2xl p-4 border border-white/5 text-center hover:bg-white/10 transition-colors">
                      <p class="text-2xl mb-1">🔥</p>
                      <p class="text-[10px] text-gray-400 mb-1">ครบ 7 วัน</p>
                      <p class="text-orange-400 font-bold text-sm">+50 Coins</p>
                   </div>
                   <div class="bg-white/5 rounded-2xl p-4 border border-white/5 text-center hover:bg-white/10 transition-colors">
                      <p class="text-2xl mb-1">🌟</p>
                      <p class="text-[10px] text-gray-400 mb-1">ครบ 30 วัน</p>
                      <p class="text-purple-400 font-bold text-sm">+200 Coins</p>
                   </div>
                   <div class="bg-gradient-to-br from-pink-500/20 to-purple-500/20 rounded-2xl p-4 border border-pink-500/30 text-center hover:brightness-110 cursor-pointer group">
                      <p class="text-2xl mb-1 group-hover:scale-110 transition-transform">🎯</p>
                      <p class="text-[10px] text-pink-200 mb-1">ภารกิจลับ</p>
                      <p class="text-white font-bold text-sm">เร็วๆ นี้</p>
                   </div>
                </div>
             </div>

          </div>
        </div>

        <Teleport to="body">
          <Transition name="bounce">
            <div v-if="checkInResult" class="fixed inset-0 z-[100] flex items-center justify-center p-4" @click="checkInResult = null">
              <div class="absolute inset-0 bg-black/80 backdrop-blur-xl transition-opacity"></div>
              
              <div class="relative w-full max-w-sm bg-[#18181b] rounded-[3rem] border border-yellow-500/30 shadow-[0_0_80px_rgba(234,179,8,0.2)] p-8 text-center overflow-hidden" @click.stop>
                 
                 <div class="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-gradient-to-b from-yellow-500/10 to-transparent pointer-events-none"></div>
                 
                 <div class="relative w-24 h-24 mx-auto mb-6 bg-gradient-to-tr from-yellow-400 to-orange-500 rounded-full flex items-center justify-center shadow-2xl animate-bounce-slow">
                    <span class="text-5xl">🎉</span>
                 </div>

                 <h2 class="text-3xl font-black text-white mb-2">เช็คอินสำเร็จ!</h2>
                 <p class="text-gray-400 mb-6 text-sm">ยินดีด้วย คุณได้รับรางวัลประจำวันแล้ว</p>

                 <div class="space-y-3 mb-8">
                    <div class="flex justify-between items-center bg-white/5 rounded-2xl p-4 border border-white/5 relative overflow-hidden">
                       <div class="absolute inset-0 bg-yellow-500/5"></div>
                       <span class="text-gray-300 font-medium flex items-center gap-2 relative z-10">🪙 Coins ที่ได้</span>
                       <span class="text-2xl font-black text-yellow-400 relative z-10 drop-shadow-sm">+{{ checkInResult.coins_earned }}</span>
                    </div>

                    <div v-if="checkInResult.milestone_bonus" class="flex justify-between items-center bg-gradient-to-r from-yellow-500/20 to-orange-500/20 rounded-2xl p-4 border border-yellow-500/30 animate-pulse">
                       <span class="text-yellow-200 font-bold flex items-center gap-2">🎁 โบนัสพิเศษ!</span>
                       <span class="text-xl font-bold text-white">+{{ checkInResult.milestone_bonus }}</span>
                    </div>
                    
                    <div class="flex justify-between items-center bg-white/5 rounded-2xl p-4 border border-white/5">
                       <span class="text-gray-300 font-medium flex items-center gap-2">🔥 Streak</span>
                       <span class="text-xl font-bold text-orange-400">{{ checkInResult.streak }} วัน</span>
                    </div>
                 </div>

                 <button 
                    @click="checkInResult = null" 
                    class="w-full py-4 bg-white text-black font-bold rounded-2xl hover:bg-gray-200 hover:scale-[1.02] active:scale-95 transition-all shadow-lg"
                 >
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
import { ref, onMounted } from 'vue';
import axios from 'axios';

// ============ Logic ชุดเดิม ============
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
/* Page Entrance Animation */
.animate-in-fade {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

/* Button Shimmer Effect (ทำให้ปุ่มดูน่ากด) */
@keyframes shimmer {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}
.animate-shimmer {
  animation: shimmer 3s linear infinite;
}

/* Modal Bounce Animation */
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

/* Icon Floating Animation */
@keyframes bounce-slow {
  0%, 100% { transform: translateY(-5%); }
  50% { transform: translateY(5%); }
}
.animate-bounce-slow {
  animation: bounce-slow 3s infinite ease-in-out;
}
</style>