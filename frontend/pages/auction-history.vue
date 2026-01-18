<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-pink-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />
    <div class="fixed top-0 left-0 w-[600px] h-[600px] bg-purple-900/20 blur-[120px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[800px] h-[600px] bg-pink-900/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

    <div class="ml-20 relative z-10 p-6 md:p-10 pb-24">
      <div class="max-w-5xl mx-auto animate-in-fade">
        
        <div class="mb-10">
          <h1 class="text-3xl md:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-pink-200 to-purple-200 flex items-center gap-3">
            📜 ประวัติการประมูล
          </h1>
          <p class="text-gray-400 mt-2">ติดตามสถานะและประวัติการแย่งชิงไอเทมของคุณ</p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
          <div class="bg-white/5 border border-white/10 rounded-2xl p-5 text-center backdrop-blur-sm">
            <p class="text-3xl font-black text-white">{{ stats.total_participated }}</p>
            <p class="text-gray-400 text-xs mt-1 uppercase tracking-wider">เข้าร่วมทั้งหมด</p>
          </div>
          <div class="bg-green-500/10 border border-green-500/20 rounded-2xl p-5 text-center backdrop-blur-sm">
            <p class="text-3xl font-black text-green-400">{{ stats.won }}</p>
            <p class="text-green-200/70 text-xs mt-1 uppercase tracking-wider">ชนะประมูล 🎉</p>
          </div>
          <div class="bg-red-500/10 border border-red-500/20 rounded-2xl p-5 text-center backdrop-blur-sm">
            <p class="text-3xl font-black text-red-400">{{ stats.lost }}</p>
            <p class="text-red-200/70 text-xs mt-1 uppercase tracking-wider">พลาดเป้า</p>
          </div>
          <div class="bg-yellow-500/10 border border-yellow-500/20 rounded-2xl p-5 text-center backdrop-blur-sm">
            <p class="text-3xl font-black text-yellow-400">{{ stats.active }}</p>
            <p class="text-yellow-200/70 text-xs mt-1 uppercase tracking-wider">กำลังแข่งขัน 🔥</p>
          </div>
        </div>

        <div class="flex flex-wrap gap-2 mb-8 bg-black/20 p-1 rounded-2xl w-fit border border-white/5 backdrop-blur-md">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            class="px-6 py-2.5 rounded-xl text-sm font-bold transition-all flex items-center gap-2"
            :class="activeTab === tab.id 
              ? 'bg-gradient-to-r from-pink-600 to-purple-600 text-white shadow-lg shadow-pink-500/20' 
              : 'text-gray-400 hover:bg-white/5 hover:text-white'"
          >
            <span>{{ tab.icon }}</span> {{ tab.name }}
            <span v-if="getTabCount(tab.id) > 0" 
                  :class="activeTab === tab.id ? 'bg-white/20 text-white' : 'bg-white/10 text-gray-400'"
                  class="ml-1 px-2 py-0.5 rounded-md text-[10px]">
              {{ getTabCount(tab.id) }}
            </span>
          </button>
        </div>

        <div class="min-h-[300px]">
          
          <div v-if="activeTab === 'active'" class="space-y-4">
            <TransitionGroup name="list">
              <div v-if="history.active.length" v-for="auction in history.active" :key="auction.id" 
                   class="group relative bg-[#121215]/80 border border-white/10 hover:border-pink-500/50 rounded-2xl p-4 flex flex-col md:flex-row gap-5 items-center transition-all duration-300 hover:shadow-[0_0_20px_rgba(236,72,153,0.1)] cursor-pointer"
                   @click="goToAuction(auction.id)">
                
                <div class="relative w-full md:w-24 h-24 shrink-0 rounded-xl overflow-hidden">
                  <img :src="getImageUrl(auction.image_url)" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                  <div class="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors"></div>
                </div>

                <div class="flex-1 text-center md:text-left w-full">
                  <h3 class="text-white font-bold text-lg group-hover:text-pink-300 transition-colors">{{ auction.title }}</h3>
                  <div class="flex flex-col md:flex-row md:items-center gap-2 md:gap-6 mt-2 text-sm">
                    <div class="bg-white/5 px-3 py-1.5 rounded-lg border border-white/5">
                      <span class="text-gray-400 text-xs">ราคาปัจจุบัน</span>
                      <span class="block text-pink-400 font-bold font-mono text-base">฿{{ auction.current_price.toLocaleString() }}</span>
                    </div>
                    <div class="bg-white/5 px-3 py-1.5 rounded-lg border border-white/5">
                      <span class="text-gray-400 text-xs">เสนอสูงสุดของคุณ</span>
                      <span class="block text-white font-bold font-mono text-base">฿{{ auction.my_highest_bid.toLocaleString() }}</span>
                    </div>
                  </div>
                </div>

                <div class="text-center md:text-right shrink-0 w-full md:w-auto bg-black/20 p-3 rounded-xl border border-white/5">
                  <div v-if="auction.is_winning">
                    <span class="inline-flex items-center gap-1 text-green-400 font-bold bg-green-500/10 px-2 py-0.5 rounded text-xs mb-1">
                      👑 กำลังนำอยู่
                    </span>
                  </div>
                  <div v-else>
                    <span class="inline-flex items-center gap-1 text-red-400 font-bold bg-red-500/10 px-2 py-0.5 rounded text-xs mb-1">
                      ⚠️ โดนแซงแล้ว
                    </span>
                  </div>
                  <p class="text-gray-400 text-xs flex items-center justify-center md:justify-end gap-1">
                    <span>⏳</span> {{ formatTime(auction.time_left) }}
                  </p>
                </div>
              </div>
              
              <div v-else class="flex flex-col items-center justify-center py-16 text-center border-2 border-dashed border-white/5 rounded-3xl">
                <div class="text-4xl mb-4 opacity-50">🔥</div>
                <p class="text-gray-400 font-medium">ไม่มีการประมูลที่กำลังแข่งขัน</p>
                <p class="text-gray-600 text-sm mt-1">ไปหาของแรร์ประมูลกันเถอะ!</p>
                <NuxtLink to="/" class="mt-4 px-6 py-2 bg-white/10 hover:bg-white/20 rounded-full text-sm font-bold text-white transition-colors">
                  ไปที่ลานประมูล
                </NuxtLink>
              </div>
            </TransitionGroup>
          </div>

          <div v-if="activeTab === 'won'" class="space-y-4">
            <div v-if="history.won.length" v-for="auction in history.won" :key="auction.id" 
                 class="group bg-gradient-to-r from-green-900/10 to-[#121215] border border-green-500/30 rounded-2xl p-4 flex flex-col md:flex-row gap-5 items-center relative overflow-hidden">
              
              <div class="absolute -right-10 -top-10 w-32 h-32 bg-green-500/20 blur-[50px] rounded-full pointer-events-none"></div>

              <div class="w-full md:w-24 h-24 shrink-0 rounded-xl overflow-hidden border border-green-500/30">
                <img :src="getImageUrl(auction.image_url)" class="w-full h-full object-cover" />
              </div>

              <div class="flex-1 text-center md:text-left z-10">
                <div class="flex items-center justify-center md:justify-start gap-2">
                  <h3 class="text-white font-bold text-lg">{{ auction.title }}</h3>
                  <span class="bg-green-500 text-black text-[10px] font-bold px-2 py-0.5 rounded-full">WINNER</span>
                </div>
                <p class="text-green-200/60 text-sm mt-1">จบประมูลเมื่อ: {{ formatDate(auction.end_time) }}</p>
                <p class="text-white font-bold mt-2 text-xl">
                  <span class="text-xs text-gray-500 font-normal mr-2">ราคาปิด:</span>
                  ฿{{ auction.current_price.toLocaleString() }}
                </p>
              </div>

              <NuxtLink :to="`/auction/${auction.id}`" class="z-10 bg-white/5 hover:bg-green-500 hover:text-black border border-white/10 text-white px-5 py-2.5 rounded-xl text-sm font-bold transition-all">
                ดูรายละเอียด
              </NuxtLink>
            </div>
            
            <div v-else class="flex flex-col items-center justify-center py-16 text-center border-2 border-dashed border-white/5 rounded-3xl">
               <div class="text-4xl mb-4 grayscale opacity-50">🏆</div>
               <p class="text-gray-400">ยังไม่มีรายการที่ชนะ</p>
               <NuxtLink to="/" class="text-pink-400 hover:text-pink-300 text-sm mt-2 underline">ไปประมูลเพื่อคว้าชัยชนะ!</NuxtLink>
            </div>
          </div>

          <div v-if="activeTab === 'lost'" class="space-y-4">
            <div v-if="history.lost.length" v-for="auction in history.lost" :key="auction.id" 
                 class="bg-[#121215]/40 border border-white/5 rounded-2xl p-4 flex flex-col md:flex-row gap-5 items-center opacity-70 hover:opacity-100 transition-opacity">
              
              <div class="w-full md:w-20 h-20 shrink-0 rounded-xl overflow-hidden grayscale">
                <img :src="getImageUrl(auction.image_url)" class="w-full h-full object-cover" />
              </div>

              <div class="flex-1 text-center md:text-left">
                <h3 class="text-gray-300 font-semibold">{{ auction.title }}</h3>
                <div class="flex items-center justify-center md:justify-start gap-3 text-sm mt-1 text-gray-500">
                   <span>ปิดที่: ฿{{ auction.current_price.toLocaleString() }}</span>
                   <span>|</span>
                   <span>คุณเสนอ: ฿{{ auction.my_highest_bid.toLocaleString() }}</span>
                </div>
              </div>
              
              <span class="text-red-400/50 font-bold text-sm bg-red-500/5 px-3 py-1 rounded border border-red-500/10">
                แพ้ประมูล
              </span>
            </div>
             <div v-else class="flex flex-col items-center justify-center py-16 text-center border-2 border-dashed border-white/5 rounded-3xl">
               <p class="text-gray-500">คุณยังไม่เคยแพ้เลย! สุดยอด 👍</p>
            </div>
          </div>

        </div>

        <div v-if="autoBids.length" class="mt-16 border-t border-white/10 pt-10">
          <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-3">
            <span class="bg-blue-500/20 p-2 rounded-lg text-blue-400">🤖</span> 
            ระบบช่วยประมูล (Auto-Bid)
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="ab in autoBids" :key="ab.id" 
                 class="bg-[#15151a] border border-blue-500/20 rounded-2xl p-4 flex gap-4 items-center relative overflow-hidden group">
              
              <div class="absolute inset-0 bg-gradient-to-r from-blue-600/5 to-transparent pointer-events-none"></div>

              <img :src="getImageUrl(ab.auction_image)" class="w-16 h-16 rounded-lg object-cover border border-white/5" />
              
              <div class="flex-1 z-10">
                <h4 class="text-white font-bold text-sm truncate">{{ ab.auction_title }}</h4>
                <div class="flex flex-col mt-1">
                  <span class="text-gray-400 text-xs">ตั้งงบสูงสุด: <span class="text-blue-400 font-bold">฿{{ ab.max_amount.toLocaleString() }}</span></span>
                  <span class="text-gray-500 text-[10px]">ปัจจุบัน: ฿{{ ab.current_price.toLocaleString() }}</span>
                </div>
              </div>
              
              <div class="text-right z-10">
                <div v-if="ab.is_winning" class="text-green-400 text-xs font-bold bg-green-900/30 px-2 py-1 rounded mb-2 inline-block">นำอยู่</div>
                <div v-else class="text-yellow-400 text-xs font-bold bg-yellow-900/30 px-2 py-1 rounded mb-2 inline-block">รอจังหวะ</div>
                
                <button @click="cancelAutoBid(ab.auction_id)" class="block text-red-400 hover:text-red-300 text-xs font-medium transition-colors hover:underline ml-auto">
                  หยุดทำงาน
                </button>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const baseUrl = 'http://localhost:5000';

const activeTab = ref('active');
const history = ref({ won: [], lost: [], active: [] });
const stats = ref({ total_participated: 0, won: 0, lost: 0, active: 0 });
const autoBids = ref([]);
const loading = ref(true);

const tabs = [
  { id: 'active', name: 'กำลังแข่งขัน', icon: '🔥' },
  { id: 'won', name: 'ชนะประมูล', icon: '🏆' },
  { id: 'lost', name: 'พลาดเป้า', icon: '💔' },
];

function getTabCount(tabId) {
  return history.value[tabId]?.length || 0;
}

function getImageUrl(url) {
  if (!url) return '/default-item.jpg';
  return url.startsWith('http') ? url : baseUrl + url;
}

function formatTime(seconds) {
  if (seconds <= 0) return 'หมดเวลา';
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (h > 24) return `${Math.floor(h / 24)} วัน`;
  if (h > 0) return `${h} ชม. ${m} นาที`;
  return `${m} นาที`;
}

function formatDate(dateString) {
    if(!dateString) return '-';
    return new Date(dateString).toLocaleDateString('th-TH', {
        day: 'numeric', month: 'short', year: '2-digit'
    });
}

function goToAuction(id) {
    // สมมติว่าหน้าหลักคือ index และรับ query id หรือจะไปหน้า detail แยกก็ได้
    router.push('/'); 
    // หรือ router.push(`/auction/${id}`); ถ้ามีหน้าแยก
}

async function fetchHistory() {
  const token = localStorage.getItem('token');
  if (!token) {
    router.push('/login');
    return;
  }

  try {
    const res = await axios.get(`${baseUrl}/api/auctions/my-history`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    history.value = res.data.history || { won: [], lost: [], active: [] };
    stats.value = res.data.stats || {};
  } catch (err) {
    console.error('Failed to fetch auction history:', err);
  }
}

async function fetchAutoBids() {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    const res = await axios.get(`${baseUrl}/api/auctions/my-auto-bids`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    autoBids.value = res.data.auto_bids || [];
  } catch (err) {
    console.error('Failed to fetch auto-bids:', err);
  }
}

async function cancelAutoBid(auctionId) {
  const token = localStorage.getItem('token');
  if (!token) return;

  if (!confirm('ยืนยันยกเลิก Auto-Bid?')) return;

  try {
    await axios.delete(`${baseUrl}/api/auctions/${auctionId}/auto-bid`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    autoBids.value = autoBids.value.filter(ab => ab.auction_id !== auctionId);
    alert('ยกเลิก Auto-Bid สำเร็จ');
  } catch (err) {
    alert('ไม่สามารถยกเลิกได้');
  }
}

onMounted(async () => {
  await Promise.all([fetchHistory(), fetchAutoBids()]);
  loading.value = false;
});
</script>

<style scoped>
/* Animation */
.animate-in-fade {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
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
</style>