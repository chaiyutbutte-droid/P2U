<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />

    <div class="max-w-5xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-white flex items-center gap-3">
          📜 ประวัติการประมูล
        </h1>
        <p class="text-dark-400 mt-1">ดูการประมูลที่คุณเข้าร่วม</p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <div class="card p-4 text-center">
          <p class="text-3xl font-bold text-white">{{ stats.total_participated }}</p>
          <p class="text-dark-400 text-sm">เข้าร่วมทั้งหมด</p>
        </div>
        <div class="card p-4 text-center">
          <p class="text-3xl font-bold text-green-400">{{ stats.won }}</p>
          <p class="text-dark-400 text-sm">ชนะ 🎉</p>
        </div>
        <div class="card p-4 text-center">
          <p class="text-3xl font-bold text-red-400">{{ stats.lost }}</p>
          <p class="text-dark-400 text-sm">แพ้</p>
        </div>
        <div class="card p-4 text-center">
          <p class="text-3xl font-bold text-yellow-400">{{ stats.active }}</p>
          <p class="text-dark-400 text-sm">กำลังประมูล</p>
        </div>
      </div>

      <!-- Tabs -->
      <div class="flex gap-2 mb-6">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-all"
          :class="activeTab === tab.id 
            ? 'bg-primary-500 text-white' 
            : 'glass text-dark-300 hover:bg-dark-700'"
        >
          {{ tab.icon }} {{ tab.name }}
          <span v-if="getTabCount(tab.id) > 0" class="ml-1 px-1.5 py-0.5 rounded-full text-xs bg-white/20">
            {{ getTabCount(tab.id) }}
          </span>
        </button>
      </div>

      <!-- Active Auctions -->
      <div v-if="activeTab === 'active'" class="space-y-4">
        <div v-if="history.active.length" v-for="auction in history.active" :key="auction.id" 
             class="card p-4 flex gap-4 items-center cursor-pointer hover:ring-2 hover:ring-primary-500/50 transition-all"
             @click="goToAuction(auction.id)">
          <img :src="getImageUrl(auction.image_url)" class="w-20 h-20 rounded-lg object-cover" />
          <div class="flex-1">
            <h3 class="text-white font-semibold">{{ auction.title }}</h3>
            <div class="flex items-center gap-4 mt-2 text-sm">
              <span class="text-dark-400">ราคาปัจจุบัน: <span class="text-primary-400 font-bold">{{ auction.current_price.toLocaleString() }} Token</span></span>
              <span class="text-dark-400">เสนอสูงสุด: <span class="text-accent-400">{{ auction.my_highest_bid.toLocaleString() }} Token</span></span>
            </div>
          </div>
          <div class="text-right">
            <span v-if="auction.is_winning" class="text-green-400 text-sm font-medium">👑 กำลังนำ</span>
            <span v-else class="text-yellow-400 text-sm font-medium">⚠️ มีคนเสนอสูงกว่า</span>
            <p class="text-dark-400 text-xs mt-1">เหลือ {{ formatTime(auction.time_left) }}</p>
          </div>
        </div>
        <div v-else class="card p-10 text-center">
          <p class="text-dark-400">ไม่มีการประมูลที่กำลังดำเนินอยู่</p>
        </div>
      </div>

      <!-- Won Auctions -->
      <div v-if="activeTab === 'won'" class="space-y-4">
        <div v-if="history.won.length" v-for="auction in history.won" :key="auction.id" 
             class="card p-4 flex gap-4 items-center border-l-4 border-green-500">
          <img :src="getImageUrl(auction.image_url)" class="w-20 h-20 rounded-lg object-cover" />
          <div class="flex-1">
            <div class="flex items-center gap-2">
              <h3 class="text-white font-semibold">{{ auction.title }}</h3>
              <span class="text-green-400 text-xl">🎉</span>
            </div>
            <p class="text-dark-400 text-sm mt-1">ราคาที่ชนะ: <span class="text-green-400 font-bold">{{ auction.current_price.toLocaleString() }} Token</span></p>
          </div>
          <NuxtLink :to="`/auction?id=${auction.id}`" class="btn-primary px-4 py-2 text-sm">
            ดูรายละเอียด
          </NuxtLink>
        </div>
        <div v-else class="card p-10 text-center">
          <div class="text-5xl mb-4">🏆</div>
          <p class="text-dark-400">ยังไม่มีการประมูลที่ชนะ</p>
          <NuxtLink to="/auction" class="btn-primary mt-4 inline-block px-6 py-2">
            ไปประมูลเลย!
          </NuxtLink>
        </div>
      </div>

      <!-- Lost Auctions -->
      <div v-if="activeTab === 'lost'" class="space-y-4">
        <div v-if="history.lost.length" v-for="auction in history.lost" :key="auction.id" 
             class="card p-4 flex gap-4 items-center opacity-70">
          <img :src="getImageUrl(auction.image_url)" class="w-20 h-20 rounded-lg object-cover grayscale" />
          <div class="flex-1">
            <h3 class="text-white font-semibold">{{ auction.title }}</h3>
            <div class="text-sm mt-1">
              <span class="text-dark-400">ราคาสุดท้าย: {{ auction.current_price.toLocaleString() }} Token</span>
              <span class="text-dark-500 mx-2">|</span>
              <span class="text-dark-400">เสนอสูงสุดของคุณ: {{ auction.my_highest_bid.toLocaleString() }} Token</span>
            </div>
          </div>
          <span class="text-red-400 text-sm">แพ้</span>
        </div>
        <div v-else class="card p-10 text-center">
          <p class="text-dark-400">ยังไม่มีการประมูลที่แพ้</p>
        </div>
      </div>

      <!-- My Auto-Bids Section -->
      <div v-if="autoBids.length" class="mt-10">
        <h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
          🤖 Auto-Bid ที่ใช้งานอยู่
        </h2>
        <div class="space-y-3">
          <div v-for="ab in autoBids" :key="ab.id" 
               class="card p-4 flex gap-4 items-center bg-gradient-to-r from-primary-500/10 to-transparent border border-primary-500/30">
            <img :src="getImageUrl(ab.auction_image)" class="w-16 h-16 rounded-lg object-cover" />
            <div class="flex-1">
              <h4 class="text-white font-medium">{{ ab.auction_title }}</h4>
              <div class="flex items-center gap-4 text-sm mt-1">
                <span class="text-dark-400">ตั้งไว้สูงสุด: <span class="text-primary-400 font-bold">{{ ab.max_amount.toLocaleString() }} Token</span></span>
                <span class="text-dark-400">ราคาปัจจุบัน: {{ ab.current_price.toLocaleString() }} Token</span>
              </div>
            </div>
            <div class="text-right">
              <span v-if="ab.is_winning" class="text-green-400 text-sm">👑 กำลังนำ</span>
              <span v-else class="text-yellow-400 text-sm">รอ...</span>
              <button @click="cancelAutoBid(ab.auction_id)" class="block mt-2 text-red-400 text-xs hover:underline">
                ยกเลิก Auto-Bid
              </button>
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
  { id: 'active', name: 'กำลังประมูล', icon: '🔥' },
  { id: 'won', name: 'ชนะ', icon: '🏆' },
  { id: 'lost', name: 'แพ้', icon: '💔' },
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

function goToAuction(id) {
  router.push(`/auction?id=${id}`);
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
.card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
}
</style>
