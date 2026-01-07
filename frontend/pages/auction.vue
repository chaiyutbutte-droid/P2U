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
        <NuxtLink to="/auction-history" class="btn-secondary">
          📜 ประวัติการประมูล
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
                <p class="text-2xl font-bold text-primary-400">฿{{ auction.current_price.toLocaleString() }}</p>
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
                      <span class="text-3xl font-bold text-primary-400">฿{{ selectedAuction.current_price?.toLocaleString() }}</span>
                    </div>
                    <div class="flex justify-between items-center mt-2">
                      <span class="text-dark-400 text-sm">จำนวนราคา</span>
                      <span class="text-accent-400">{{ selectedAuction.total_bids }} ราคา</span>
                    </div>
                  </div>
                  
                  <!-- Bid Input -->
                  <div class="mb-4">
                    <label class="text-dark-300 text-sm mb-2 block">ใส่ราคาของคุณ (ขั้นต่ำ ฿{{ minBid.toLocaleString() }})</label>
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
                  
                  <!-- Auto-Bid Section -->
                  <div class="mt-4 glass-light rounded-xl p-4">
                    <div class="flex items-center justify-between mb-3">
                      <div class="flex items-center gap-2">
                        <span class="text-lg">🤖</span>
                        <span class="text-white font-medium">Auto-Bid</span>
                      </div>
                      <span v-if="myAutoBid" class="text-green-400 text-xs px-2 py-1 bg-green-500/20 rounded-full">เปิดใช้งาน</span>
                    </div>
                    
                    <!-- Auto-Bid Active Status -->
                    <div v-if="myAutoBid" class="space-y-2">
                      <div class="flex justify-between text-sm">
                        <span class="text-dark-400">ราคาสูงสุด</span>
                        <span class="text-primary-400 font-bold">฿{{ myAutoBid.max_amount?.toLocaleString() }}</span>
                      </div>
                      <div class="flex gap-2">
                        <button @click="showAutoBidModal = true" class="flex-1 py-2 bg-dark-700 hover:bg-dark-600 rounded-lg text-sm text-white transition">
                          แก้ไข
                        </button>
                        <button @click="cancelAutoBid" class="flex-1 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg text-sm transition">
                          ยกเลิก
                        </button>
                      </div>
                    </div>
                    
                    <!-- Set Auto-Bid Button -->
                    <div v-else>
                      <p class="text-dark-400 text-sm mb-3">ตั้งค่าให้ระบบประมูลอัตโนมัติแทนคุณ</p>
                      <button @click="showAutoBidModal = true" class="w-full py-2 bg-accent-500 hover:bg-accent-600 text-white rounded-lg text-sm font-medium transition">
                        ⚡ ตั้ง Auto-Bid
                      </button>
                    </div>
                  </div>
                  
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

      <!-- Auto-Bid Modal -->
      <Teleport to="body">
        <Transition name="fade">
          <div v-if="showAutoBidModal" class="fixed inset-0 bg-black/80 backdrop-blur-sm z-[60] flex items-center justify-center p-4" @click="showAutoBidModal = false">
            <div class="glass rounded-2xl w-full max-w-md p-6 animate-in" @click.stop>
              <div class="flex items-center justify-between mb-6">
                <h3 class="text-xl font-bold text-white flex items-center gap-2">
                  🤖 ตั้งค่า Auto-Bid
                </h3>
                <button @click="showAutoBidModal = false" class="text-dark-400 hover:text-white text-2xl">✕</button>
              </div>
              
              <p class="text-dark-400 text-sm mb-4">
                ระบบจะประมูลอัตโนมัติแทนคุณจนกว่าจะถึงราคาสูงสุดที่กำหนด
              </p>
              
              <div class="mb-4">
                <label class="text-dark-300 text-sm mb-2 block">ราคาสูงสุดที่ต้องการ (฿)</label>
                <input 
                  v-model.number="autoBidAmount" 
                  type="number" 
                  :min="minBid"
                  class="w-full input-glass text-xl font-bold"
                  :placeholder="`ขั้นต่ำ ฿${minBid.toLocaleString()}`"
                />
              </div>
              
              <div class="glass-light rounded-lg p-3 mb-4">
                <div class="flex justify-between text-sm">
                  <span class="text-dark-400">ราคาปัจจุบัน</span>
                  <span class="text-white">฿{{ selectedAuction?.current_price?.toLocaleString() }}</span>
                </div>
                <div class="flex justify-between text-sm mt-1">
                  <span class="text-dark-400">ราคาขั้นต่ำถัดไป</span>
                  <span class="text-primary-400">฿{{ minBid.toLocaleString() }}</span>
                </div>
              </div>
              
              <button 
                @click="setAutoBid" 
                :disabled="autoBidAmount < minBid || isLoading"
                class="btn-primary w-full py-3 font-bold disabled:opacity-50"
              >
                {{ isLoading ? '⏳ กำลังตั้งค่า...' : '⚡ ยืนยัน Auto-Bid' }}
              </button>
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

// Auto-Bid State
const showAutoBidModal = ref(false);
const autoBidAmount = ref(0);
const myAutoBid = ref(null);

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
    autoBidAmount.value = res.data.current_price + res.data.min_bid_increment;
    
    // Fetch user's auto-bid status
    await fetchMyAutoBid(auction.id);
  } catch (err) {
    console.error('Failed to get auction details:', err);
  }
}

function closeAuction() {
  selectedAuction.value = null;
  bidHistory.value = [];
  myAutoBid.value = null;
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

// Auto-Bid Functions
async function fetchMyAutoBid(auctionId) {
  const token = localStorage.getItem('token');
  if (!token) return;
  
  try {
    const res = await axios.get(`${baseUrl}/api/auctions/my-auto-bids`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const autoBids = res.data.auto_bids || [];
    myAutoBid.value = autoBids.find(ab => ab.auction_id === auctionId) || null;
  } catch (err) {
    console.error('Failed to fetch auto-bids:', err);
  }
}

async function setAutoBid() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('กรุณาเข้าสู่ระบบก่อน');
    return;
  }
  
  if (autoBidAmount.value < minBid.value) {
    alert(`ราคาสูงสุดต้องไม่น้อยกว่า ฿${minBid.value.toLocaleString()}`);
    return;
  }
  
  isLoading.value = true;
  try {
    await axios.post(`${baseUrl}/api/auctions/${selectedAuction.value.id}/auto-bid`, {
      max_amount: autoBidAmount.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    alert('🤖 ตั้งค่า Auto-Bid สำเร็จ!');
    showAutoBidModal.value = false;
    
    // Refresh auction details and auto-bid status
    await fetchMyAutoBid(selectedAuction.value.id);
    const detailRes = await axios.get(`${baseUrl}/api/auctions/${selectedAuction.value.id}`);
    selectedAuction.value.current_price = detailRes.data.current_price;
    selectedAuction.value.total_bids = detailRes.data.total_bids;
    bidHistory.value = detailRes.data.bid_history || [];
    
    fetchAuctions();
  } catch (err) {
    alert(err.response?.data?.msg || 'ตั้งค่า Auto-Bid ไม่สำเร็จ');
  } finally {
    isLoading.value = false;
  }
}

async function cancelAutoBid() {
  const token = localStorage.getItem('token');
  if (!token) return;
  
  if (!confirm('ยกเลิก Auto-Bid สำหรับการประมูลนี้?')) return;
  
  isLoading.value = true;
  try {
    await axios.delete(`${baseUrl}/api/auctions/${selectedAuction.value.id}/auto-bid`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    alert('ยกเลิก Auto-Bid สำเร็จ');
    myAutoBid.value = null;
  } catch (err) {
    alert(err.response?.data?.msg || 'ยกเลิก Auto-Bid ไม่สำเร็จ');
  } finally {
    isLoading.value = false;
  }
}

// Timer to update time_left
let timer = null;

onMounted(() => {
  fetchAuctions();
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
