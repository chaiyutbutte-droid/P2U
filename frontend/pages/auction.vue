<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-pink-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-0 left-0 w-[600px] h-[600px] bg-purple-900/20 blur-[120px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[800px] h-[600px] bg-pink-900/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

    <div class="ml-20 relative z-10 p-6 md:p-10 pb-24">
      <div class="max-w-7xl mx-auto animate-in-fade">
        
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10">
          <div>
            <h1 class="text-3xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-pink-200 to-purple-200 tracking-tight drop-shadow-sm flex items-center gap-3">
              <span>🔨</span> ลานประมูล
            </h1>
            <p class="text-gray-400 mt-2 text-lg">
              เป็นเจ้าของไอเทมแรร์ ในราคาที่คุณกำหนดเอง
            </p>
          </div>
          
          <div class="flex flex-wrap items-center gap-3">
            <NuxtLink to="/auction-history" class="group relative px-6 py-3 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 transition-all overflow-hidden">
               <div class="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-indigo-500/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
               <span class="relative z-10 font-bold text-gray-200 group-hover:text-white flex items-center gap-2">
                 📜 ประวัติของฉัน
               </span>
            </NuxtLink>

            <NuxtLink v-if="isSeller" to="/auction/create" class="group relative px-6 py-3 rounded-full bg-white/5 border border-white/10 hover:bg-white/10 transition-all overflow-hidden">
                <div class="absolute inset-0 bg-gradient-to-r from-pink-500/10 to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                <span class="relative z-10 font-bold text-pink-400 group-hover:text-pink-300 flex items-center gap-2">
                  ➕ สร้างการประมูล
                </span>
            </NuxtLink>
          </div>
        </div>

        <div class="flex gap-3 mb-8 overflow-x-auto pb-4 scrollbar-hide">
          <button 
            v-for="cat in categories" 
            :key="cat.id"
            @click="selectedCategory = cat.id"
            class="px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 flex items-center gap-2 border border-transparent whitespace-nowrap"
            :class="selectedCategory === cat.id 
              ? 'bg-gradient-to-r from-pink-600 to-purple-600 text-white shadow-lg shadow-pink-500/20 scale-105' 
              : 'bg-white/5 text-gray-400 border-white/5 hover:bg-white/10 hover:text-white'"
          >
            <span>{{ cat.icon }}</span> {{ cat.name }}
          </button>
        </div>

        <div v-if="filteredAuctions.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <div 
            v-for="auction in filteredAuctions" 
            :key="auction.id" 
            class="group relative bg-[#121215]/60 backdrop-blur-md rounded-3xl border border-white/10 overflow-hidden hover:border-pink-500/40 hover:-translate-y-2 transition-all duration-500 shadow-xl hover:shadow-pink-500/10 cursor-pointer"
            @click="openAuction(auction)"
          >
            <div class="relative h-60 overflow-hidden">
              <img 
                :src="getImageUrl(auction.image_url)" 
                class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                @error="handleImageError"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-[#121215] via-transparent to-transparent opacity-80"></div>
              
              <div class="absolute top-4 right-4 bg-black/60 backdrop-blur-md px-3 py-1.5 rounded-full border border-white/10 flex items-center gap-2">
                <span class="relative flex h-2 w-2">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
                </span>
                <span class="text-xs font-mono font-bold text-white tracking-wide">{{ formatTime(auction.time_left) }}</span>
              </div>
              
              <div class="absolute bottom-3 left-4 bg-white/10 backdrop-blur-md px-3 py-1 rounded-lg border border-white/5">
                <span class="text-xs font-bold text-white flex items-center gap-1">
                  🔥 {{ auction.total_bids }} Bid
                </span>
              </div>
            </div>

            <div class="p-5">
              <h3 class="font-bold text-white text-lg truncate mb-1 group-hover:text-pink-300 transition-colors">{{ auction.title }}</h3>
              <p class="text-gray-500 text-xs truncate mb-4">{{ auction.description }}</p>
              
              <div class="bg-white/5 rounded-2xl p-4 border border-white/5 flex justify-between items-end group-hover:bg-white/10 transition-colors">
                <div>
                  <p class="text-[10px] text-gray-400 mb-0.5">ราคาปัจจุบัน</p>
                  <p class="text-xl font-black text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-300">
                    🪙 {{ auction.current_price.toLocaleString() }}
                  </p>
                </div>
                <div class="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-gray-300 group-hover:bg-pink-500 group-hover:text-white transition-all">
                    ➔
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else class="min-h-[400px] flex flex-col items-center justify-center text-center bg-[#121215]/40 backdrop-blur-3xl rounded-[3rem] border border-white/10 p-10 mt-10">
          <div class="w-32 h-32 mb-6 rounded-full bg-gradient-to-tr from-[#121215] to-[#1a1a1f] border border-white/5 flex items-center justify-center shadow-2xl relative group">
              <div class="absolute inset-0 bg-pink-500/20 rounded-full blur-2xl animate-pulse"></div>
              <span class="text-6xl grayscale group-hover:grayscale-0 transition-all duration-500">💤</span>
          </div>
          <h3 class="text-2xl font-bold text-white mb-2">ไม่มีการประมูลในหมวดนี้</h3>
          <p class="text-gray-500">ลองเลือกหมวดหมู่ใหม่ หรือกลับมาเช็คอีกครั้งเร็วๆ นี้นะ!</p>
        </div>

        <Teleport to="body">
          <Transition name="fade">
            <div v-if="selectedAuction" class="fixed inset-0 z-[100] flex items-center justify-center p-4" @click="closeAuction">
              <div class="absolute inset-0 bg-black/90 backdrop-blur-xl"></div>
              
              <div class="relative w-full max-w-5xl bg-[#121215] rounded-[2rem] border border-white/10 shadow-[0_0_100px_rgba(236,72,153,0.15)] flex flex-col md:flex-row overflow-hidden animate-pop h-[85vh] md:h-auto md:max-h-[85vh]" @click.stop>
                
                <button @click="closeAuction" class="absolute top-4 right-4 z-50 md:hidden w-8 h-8 rounded-full bg-black/50 text-white flex items-center justify-center">✕</button>

                <div class="md:w-5/12 bg-[#09090b] relative h-64 md:h-auto shrink-0">
                  <img :src="getImageUrl(selectedAuction.image_url)" class="w-full h-full object-cover opacity-90" />
                  <div class="absolute inset-0 bg-gradient-to-t from-[#121215] via-transparent to-transparent"></div>
                  
                  <div class="absolute bottom-6 left-6 right-6">
                    <div class="inline-flex items-center gap-2 px-3 py-1 bg-red-500/20 border border-red-500/50 backdrop-blur-md rounded-full mb-3">
                       <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
                       <span class="text-[10px] font-bold text-red-100 uppercase tracking-wider">Time Remaining</span>
                    </div>
                    <div class="text-4xl font-mono font-bold text-white tracking-widest drop-shadow-lg">
                      {{ formatTimeDetailed(selectedAuction.time_left) }}
                    </div>
                  </div>
                </div>
                
                <div class="md:w-7/12 flex flex-col bg-[#121215]/95 backdrop-blur-xl border-l border-white/5 relative">
                  
                  <div class="p-6 md:p-8 border-b border-white/5 flex justify-between items-start">
                      <div class="pr-8">
                        <h2 class="text-2xl font-bold text-white leading-tight mb-2">{{ selectedAuction.title }}</h2>
                        <p class="text-gray-400 text-sm line-clamp-2">{{ selectedAuction.description }}</p>
                      </div>
                      <button @click="closeAuction" class="hidden md:flex w-8 h-8 rounded-full bg-white/5 hover:bg-white/10 items-center justify-center text-gray-400 hover:text-white transition-colors shrink-0">✕</button>
                  </div>

                  <div class="flex-1 overflow-y-auto custom-scrollbar p-6 md:p-8 space-y-6">
                    
                    <div class="grid grid-cols-2 gap-4">
                        <div class="bg-gradient-to-br from-pink-500/10 to-transparent p-4 rounded-2xl border border-pink-500/20">
                          <p class="text-gray-400 text-xs mb-1">ราคาปัจจุบัน</p>
                          <p class="text-2xl font-black text-white">🪙 {{ selectedAuction.current_price?.toLocaleString() }}</p>
                        </div>
                        <div class="bg-white/5 p-4 rounded-2xl border border-white/5">
                          <p class="text-gray-400 text-xs mb-1">จำนวนการบิด</p>
                          <p class="text-2xl font-bold text-gray-200">{{ selectedAuction.total_bids }} <span class="text-sm font-normal text-gray-500">ครั้ง</span></p>
                        </div>
                    </div>

                    <div class="bg-white/[0.03] p-5 rounded-2xl border border-white/5">
                        <div class="flex justify-between items-center mb-4">
                          <label class="text-sm font-bold text-gray-300">เสนอราคาของคุณ</label>
                          <div class="text-xs">
                             <span class="text-gray-500">Token คงเหลือ: </span>
                             <span :class="tokenBalance >= minBid ? 'text-green-400 font-bold' : 'text-red-400 font-bold'">
                               🪙 {{ tokenBalance.toLocaleString() }}
                             </span>
                          </div>
                        </div>
                        
                        <div class="flex gap-3">
                          <div class="relative flex-1">
                             <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                                <span class="text-gray-500">🪙</span>
                             </div>
                             <input 
                                v-model.number="bidAmount" 
                                type="number" 
                                :min="minBid"
                                :step="selectedAuction.min_bid_increment"
                                class="w-full bg-[#09090b] border border-white/10 rounded-xl py-3 pl-10 pr-4 text-white font-bold focus:outline-none focus:border-pink-500 transition-colors placeholder-gray-600"
                                placeholder="0"
                             />
                          </div>
                          <button 
                             @click="placeBid" 
                             :disabled="bidAmount < minBid || isLoading"
                             class="bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white font-bold px-6 rounded-xl shadow-lg shadow-pink-600/20 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
                          >
                             {{ isLoading ? '...' : 'ประมูล' }}
                          </button>
                        </div>
                        <p class="text-xs text-gray-500 mt-2 text-center">ขั้นต่ำ: {{ minBid.toLocaleString() }} Token</p>
                    </div>

                    <div>
                        <div class="flex justify-between items-center mb-3">
                          <h4 class="text-sm font-bold text-gray-400 uppercase tracking-wider">ประวัติการประมูล</h4>
                          <span class="text-[10px] bg-white/10 px-2 py-0.5 rounded text-gray-400">{{ bidHistory.length }} รายการ</span>
                        </div>
                        
                        <div class="space-y-2 max-h-40 overflow-y-auto custom-scrollbar pr-2">
                          <div v-if="bidHistory.length === 0" class="text-center py-4 text-gray-600 text-sm italic">
                             ยังไม่มีใครเปิดประมูล เป็นคนแรกเลย!
                          </div>
                          <div 
                             v-for="bid in bidHistory" 
                             :key="bid.id" 
                             class="flex items-center justify-between p-3 rounded-xl border border-transparent transition-all"
                             :class="bid.is_highest ? 'bg-pink-500/10 border-pink-500/20' : 'bg-white/5 hover:bg-white/10'"
                          >
                             <div class="flex items-center gap-3">
                                <div 
                                   class="w-6 h-6 rounded-full flex items-center justify-center text-[10px] font-bold shadow-sm"
                                   :class="{
                                      'bg-gradient-to-b from-yellow-300 to-yellow-600 text-black': bid.rank === 1,
                                      'bg-gradient-to-b from-gray-300 to-gray-500 text-black': bid.rank === 2,
                                      'bg-gradient-to-b from-orange-300 to-orange-600 text-black': bid.rank === 3,
                                      'bg-white/10 text-gray-500': bid.rank > 3
                                   }"
                                >
                                   {{ bid.rank <= 3 ? ['🥇', '🥈', '🥉'][bid.rank - 1] : bid.rank }}
                                </div>
                                <div>
                                   <p class="text-sm font-bold text-gray-200">{{ bid.bidder_username }}</p>
                                   <p class="text-[10px] text-gray-500">{{ bid.date }} • {{ bid.time }}</p>
                                </div>
                             </div>
                             <div class="text-right">
                                <p class="text-sm font-bold text-pink-300">฿{{ bid.amount?.toLocaleString() }}</p>
                                <p v-if="bid.is_highest" class="text-[9px] text-green-400 font-bold uppercase">Leading</p>
                             </div>
                          </div>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import axios from 'axios';

const auctions = ref([]);
const selectedAuction = ref(null);
const selectedCategory = ref('all');
const bidAmount = ref(0);
const bidHistory = ref([]);
const isLoading = ref(false);
const isSeller = ref(false);
const tokenBalance = ref(0);

const baseUrl = 'http://localhost:5000';

const categories = [
  { id: 'all', name: 'ทั้งหมด', icon: '🔨' },
  { id: 'electronics', name: 'อิเล็กทรอนิกส์', icon: '📱' },
  { id: 'fashion', name: 'แฟชั่น', icon: '👗' },
  { id: 'gaming', name: 'เกมมิ่ง', icon: '🎮' },
  { id: 'beauty', name: 'ความงาม', icon: '💄' },
];

const filteredAuctions = computed(() => {
  if (selectedCategory.value === 'all') return auctions.value;
  return auctions.value.filter(a => a.category === selectedCategory.value);
});

const minBid = computed(() => {
  if (!selectedAuction.value) return 0;
  return selectedAuction.value.current_price + selectedAuction.value.min_bid_increment;
});

function getImageUrl(url) {
  if (!url) return '/default-item.jpg';
  return url.startsWith('http') ? url : baseUrl + url;
}

function handleImageError(e) {
  e.target.src = '/default-item.jpg';
}

function formatTime(seconds) {
  if (seconds <= 0) return 'จบแล้ว';
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  if (h > 24) return `${Math.floor(h / 24)} วัน`;
  if (h > 0) return `${h} ชม.`;
  return `${m} นาที`;
}

function formatTimeDetailed(seconds) {
  if (seconds <= 0) return 'จบแล้ว';
  const d = Math.floor(seconds / 86400);
  const h = Math.floor((seconds % 86400) / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  if (d > 0) return `${d} วัน ${h} ชม.`;
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

async function fetchAuctions() {
  try {
    const res = await axios.get(`${baseUrl}/api/auctions`);
    auctions.value = res.data.auctions || [];
  } catch (err) {
    console.error('Failed to fetch auctions:', err);
  }
}

async function openAuction(auction) {
  try {
    const res = await axios.get(`${baseUrl}/api/auctions/${auction.id}`);
    selectedAuction.value = res.data;
    bidHistory.value = res.data.bid_history || [];
    bidAmount.value = res.data.current_price + res.data.min_bid_increment;
  } catch (err) {
    console.error('Failed to get auction details:', err);
  }
}

function closeAuction() {
  selectedAuction.value = null;
  bidHistory.value = [];
}

async function placeBid() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('กรุณาเข้าสู่ระบบก่อน');
    return;
  }
  
  if (bidAmount.value < minBid.value) {
    alert(`ราคาต้องไม่น้อยกว่า ฿${minBid.value.toLocaleString()}`);
    return;
  }
  
  isLoading.value = true;
  try {
    const res = await axios.post(`${baseUrl}/api/auctions/${selectedAuction.value.id}/bid`, {
      amount: bidAmount.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    alert('🎉 ประมูลสำเร็จ!');
    selectedAuction.value.current_price = res.data.current_price;
    selectedAuction.value.total_bids = res.data.total_bids;
    bidAmount.value = res.data.current_price + selectedAuction.value.min_bid_increment;
    
    // Refresh bid history
    const detailRes = await axios.get(`${baseUrl}/api/auctions/${selectedAuction.value.id}`);
    bidHistory.value = detailRes.data.bid_history || [];
    
    // Refresh list
    fetchAuctions();
    fetchTokenBalance(); // อัปเดตยอด Token หลังจากบิด
  } catch (err) {
    alert(err.response?.data?.msg || 'ประมูลไม่สำเร็จ');
  } finally {
    isLoading.value = false;
  }
}

// Timer to update time_left
let timer = null;

async function fetchTokenBalance() {
  const token = localStorage.getItem('token');
  if (!token) return;
  
  try {
    const res = await axios.get(`${baseUrl}/api/token/balance`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    tokenBalance.value = res.data.token_balance || 0;
  } catch (err) {
    console.error('Failed to fetch token balance:', err);
  }
}

onMounted(() => {
  fetchAuctions();
  fetchTokenBalance();
  axios.post(`${baseUrl}/api/auctions/seed`).catch(() => {});
  
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  isSeller.value = user.is_seller || false;
  
  timer = setInterval(() => {
    auctions.value = auctions.value.map(a => ({
      ...a,
      time_left: Math.max(0, a.time_left - 1)
    }));
    if (selectedAuction.value) {
      selectedAuction.value.time_left = Math.max(0, selectedAuction.value.time_left - 1);
    }
  }, 1000);
});

onBeforeUnmount(() => {
  if (timer) clearInterval(timer);
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

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.animate-pop { animation: popIn 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes popIn {
  0% { opacity: 0; transform: scale(0.95); }
  100% { opacity: 1; transform: scale(1); }
}

/* Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

.scrollbar-hide::-webkit-scrollbar {
    display: none;
}
.scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
}
</style>