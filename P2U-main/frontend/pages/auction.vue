<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />

    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-white flex items-center gap-3">
            🔨 ประมูลสินค้า
          </h1>
          <p class="text-dark-400 mt-1">ประมูลสินค้าสุดพิเศษ ราคาเริ่มต้นต่ำมาก!</p>
        </div>
        <NuxtLink v-if="isSeller" to="/auction/create" class="btn-primary">
          ➕ สร้างการประมูล
        </NuxtLink>
      </div>

      <!-- Category Filter -->
      <div class="flex gap-2 mb-6 overflow-x-auto pb-2">
        <button 
          v-for="cat in categories" 
          :key="cat.id"
          @click="selectedCategory = cat.id"
          class="category-pill whitespace-nowrap"
          :class="{ active: selectedCategory === cat.id }"
        >
          {{ cat.icon }} {{ cat.name }}
        </button>
      </div>

      <!-- Auction Grid -->
      <div v-if="filteredAuctions.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="auction in filteredAuctions" 
          :key="auction.id" 
          class="card overflow-hidden group cursor-pointer"
          @click="openAuction(auction)"
        >
          <!-- Image -->
          <div class="aspect-video relative overflow-hidden">
            <img 
              :src="getImageUrl(auction.image_url)" 
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
              @error="handleImageError"
            />
            <!-- Time Badge -->
            <div class="absolute top-3 right-3 bg-black/70 backdrop-blur px-3 py-1.5 rounded-full flex items-center gap-2">
              <span class="text-red-400 animate-pulse">●</span>
              <span class="text-white text-sm font-medium">{{ formatTime(auction.time_left) }}</span>
            </div>
            <!-- Bids Badge -->
            <div class="absolute bottom-3 left-3 bg-primary-500/90 backdrop-blur px-3 py-1 rounded-full">
              <span class="text-white text-sm font-medium">🔥 {{ auction.total_bids }} ราคา</span>
            </div>
          </div>

          <!-- Info -->
          <div class="p-4">
            <h3 class="font-semibold text-white text-lg truncate">{{ auction.title }}</h3>
            <p class="text-dark-400 text-sm mt-1 truncate">{{ auction.description }}</p>
            
            <div class="flex items-end justify-between mt-4">
              <div>
                <p class="text-dark-400 text-xs">ราคาปัจจุบัน</p>
                <p class="text-2xl font-bold text-primary-400">🪙 {{ auction.current_price.toLocaleString() }} Token</p>
              </div>
              <button class="btn-primary px-4 py-2 text-sm">
                ประมูลเลย
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-20">
        <div class="w-24 h-24 rounded-full bg-dark-800 mx-auto mb-4 flex items-center justify-center text-5xl">🔨</div>
        <h3 class="text-xl font-semibold text-white mb-2">ยังไม่มีการประมูล</h3>
        <p class="text-dark-400">กลับมาใหม่เร็วๆ นี้!</p>
      </div>

      <!-- Auction Detail Modal -->
      <Teleport to="body">
        <Transition name="fade">
          <div v-if="selectedAuction" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click="closeAuction">
            <div class="glass rounded-3xl w-full max-w-3xl max-h-[90vh] overflow-hidden animate-in" @click.stop>
              <div class="flex flex-col md:flex-row h-full">
                <!-- Image -->
                <div class="md:w-1/2">
                  <img :src="getImageUrl(selectedAuction.image_url)" class="w-full h-64 md:h-full object-cover" />
                </div>
                
                <!-- Details -->
                <div class="md:w-1/2 p-6 flex flex-col overflow-y-auto">
                  <button @click="closeAuction" class="self-end text-dark-400 hover:text-white text-2xl mb-2">✕</button>
                  
                  <h2 class="text-2xl font-bold text-white mb-2">{{ selectedAuction.title }}</h2>
                  <p class="text-dark-400 text-sm mb-4">{{ selectedAuction.description }}</p>
                  
                  <!-- Time Left -->
                  <div class="glass-light rounded-xl p-4 mb-4 text-center">
                    <p class="text-dark-400 text-sm">เหลือเวลา</p>
                    <p class="text-2xl font-bold text-red-400">{{ formatTimeDetailed(selectedAuction.time_left) }}</p>
                  </div>
                  
                  <!-- Current Price -->
                  <div class="glass-light rounded-xl p-4 mb-4">
                    <div class="flex justify-between items-center">
                      <span class="text-dark-400">ราคาปัจจุบัน</span>
                      <span class="text-3xl font-bold text-primary-400">🪙 {{ selectedAuction.current_price?.toLocaleString() }}</span>
                    </div>
                    <div class="flex justify-between items-center mt-2">
                      <span class="text-dark-400 text-sm">จำนวนราคา</span>
                      <span class="text-accent-400">{{ selectedAuction.total_bids }} ราคา</span>
                    </div>
                  </div>
                  
                  <!-- Your Token Balance -->
                  <div class="glass-light rounded-xl p-3 mb-4 flex justify-between items-center">
                    <span class="text-dark-400 text-sm">Token ของคุณ</span>
                    <span class="text-lg font-bold" :class="tokenBalance >= minBid ? 'text-green-400' : 'text-red-400'">
                      🪙 {{ tokenBalance.toLocaleString() }}
                    </span>
                  </div>
                  
                  <!-- Bid Input -->
                  <div class="mb-4">
                    <label class="text-dark-300 text-sm mb-2 block">ใส่ Token ของคุณ (ขั้นต่ำ {{ minBid.toLocaleString() }} Token)</label>
                    <input 
                      v-model.number="bidAmount" 
                      type="number" 
                      :min="minBid"
                      :step="selectedAuction.min_bid_increment"
                      class="w-full input-glass text-xl font-bold"
                      placeholder="0"
                    />
                  </div>
                  
                  <button 
                    @click="placeBid" 
                    :disabled="bidAmount < minBid || isLoading"
                    class="btn-primary w-full py-4 text-lg font-bold disabled:opacity-50"
                  >
                    {{ isLoading ? '⏳ กำลังประมูล...' : '🔨 ประมูล!' }}
                  </button>
                  
                  <!-- Bid History -->
                  <div v-if="bidHistory.length" class="mt-4">
                    <div class="flex justify-between items-center mb-3">
                      <p class="text-white font-semibold">📜 ประวัติการประมูล</p>
                      <span class="text-dark-400 text-xs">{{ bidHistory.length }} รายการ</span>
                    </div>
                    <div class="space-y-2 max-h-60 overflow-y-auto pr-1">
                      <div 
                        v-for="bid in bidHistory" 
                        :key="bid.id" 
                        class="flex items-center justify-between text-sm glass-light rounded-lg px-3 py-2.5"
                        :class="{ 'ring-2 ring-primary-500 bg-primary-500/10': bid.is_highest }"
                      >
                        <div class="flex items-center gap-3">
                          <!-- Rank Badge -->
                          <div 
                            class="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold"
                            :class="bid.rank === 1 ? 'bg-yellow-500 text-black' : bid.rank === 2 ? 'bg-gray-400 text-black' : bid.rank === 3 ? 'bg-orange-600 text-white' : 'bg-dark-700 text-dark-400'"
                          >
                            {{ bid.rank <= 3 ? ['🥇', '🥈', '🥉'][bid.rank - 1] : bid.rank }}
                          </div>
                          
                          <!-- User Info -->
                          <div>
                            <p class="text-white font-medium">{{ bid.bidder_username }}</p>
                            <p class="text-dark-500 text-xs">{{ bid.date }} {{ bid.time }}</p>
                          </div>
                        </div>
                        
                        <!-- Bid Amount -->
                        <div class="text-right">
                          <p class="text-primary-400 font-bold">฿{{ bid.amount?.toLocaleString() }}</p>
                          <p v-if="bid.is_highest" class="text-green-400 text-xs">👑 เสนอสูงสุด</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- No bids yet -->
                  <div v-else class="mt-4 text-center py-4">
                    <p class="text-dark-400 text-sm">ยังไม่มีผู้ประมูล เป็นคนแรกเลย!</p>
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
  // Seed auctions if empty
  axios.post(`${baseUrl}/api/auctions/seed`).catch(() => {});
  
  // Check if seller
  const user = JSON.parse(localStorage.getItem('user') || '{}');
  isSeller.value = user.is_seller || false;
  
  // Update time every second
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
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
