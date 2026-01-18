<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-yellow-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-[-100px] right-[-100px] w-[600px] h-[600px] bg-purple-900/10 blur-[150px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 left-0 w-[500px] h-[500px] bg-orange-500/5 blur-[120px] rounded-full pointer-events-none z-0"></div>

    <main class="ml-20 relative z-10 p-6 md:p-10 min-h-screen">
      <div class="max-w-5xl mx-auto w-full animate-in-fade">
        
        <header class="flex flex-col md:flex-row items-start md:items-end justify-between gap-4 mb-10">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 mb-3">
               <span class="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"></span>
               <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">My Purchase</span>
            </div>
            <h1 class="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-yellow-100 to-yellow-500 tracking-tight drop-shadow-sm">
              ประวัติคำสั่งซื้อ 📦
            </h1>
            <p class="text-gray-400 mt-2 text-sm md:text-base">
              ตรวจสอบสถานะและประวัติการช้อปปิ้งทั้งหมดของท่านได้ที่นี่
            </p>
          </div>
          
          <NuxtLink 
            to="/profile" 
            class="group flex items-center gap-2 px-5 py-2.5 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 hover:border-yellow-500/30 transition-all duration-300"
          >
            <span class="text-gray-300 text-sm font-medium group-hover:text-white">กลับไปหน้าโปรไฟล์</span>
            <span class="text-lg group-hover:translate-x-1 transition-transform">➔</span>
          </NuxtLink>
        </header>

        <div class="flex gap-2 mb-8 overflow-x-auto pb-4 no-scrollbar">
          <button 
            v-for="filter in filters" 
            :key="filter.value"
            @click="activeFilter = filter.value"
            class="px-5 py-2.5 rounded-xl text-sm font-bold transition-all duration-300 whitespace-nowrap border flex items-center gap-2"
            :class="activeFilter === filter.value 
              ? 'bg-gradient-to-r from-yellow-500 to-orange-600 border-transparent text-black shadow-[0_0_20px_rgba(234,179,8,0.3)] transform scale-105' 
              : 'bg-[#121215]/50 border-white/10 text-gray-400 hover:text-white hover:bg-white/10 hover:border-white/20'"
          >
            {{ filter.label }}
          </button>
        </div>

        <div v-if="loading" class="grid grid-cols-1 gap-4">
           <div v-for="i in 3" :key="i" class="h-40 rounded-[2rem] bg-white/5 animate-pulse border border-white/5"></div>
        </div>

        <div v-else-if="filteredOrders.length" class="space-y-4">
          <TransitionGroup name="list">
            <div 
              v-for="order in filteredOrders" 
              :key="order._id" 
              class="group relative bg-[#121215]/80 backdrop-blur-xl rounded-[2rem] border border-white/10 p-6 md:p-8 cursor-pointer transition-all duration-300 hover:border-yellow-500/40 hover:shadow-[0_0_30px_rgba(0,0,0,0.5)] hover:-translate-y-1"
              @click="selectedOrder = order"
            >
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
                <div class="flex items-center gap-4">
                  <div class="w-12 h-12 rounded-2xl bg-white/5 flex items-center justify-center text-2xl border border-white/5 group-hover:scale-110 transition-transform duration-500">
                    🛍️
                  </div>
                  <div>
                    <p class="text-[10px] uppercase text-gray-500 font-bold tracking-widest mb-0.5">Order ID</p>
                    <p class="text-white font-mono text-base font-medium group-hover:text-yellow-200 transition-colors">#{{ order._id }}</p>
                  </div>
                </div>
                
                <span :class="getStatusClass(order.status)" class="px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider border backdrop-blur-md shadow-lg self-start sm:self-center">
                  {{ getStatusLabel(order.status) }}
                </span>
              </div>

              <div class="mb-6 pl-2">
                <div class="flex items-center -space-x-4 hover:space-x-1 transition-all duration-300 overflow-x-auto pb-2 no-scrollbar">
                  <div v-for="(item, idx) in order.items" :key="idx" class="relative shrink-0 transition-transform hover:scale-110 hover:z-10">
                    <img 
                      :src="getImageUrl(item.product?.image_url)" 
                      class="w-16 h-16 md:w-20 md:h-20 rounded-2xl object-cover border-2 border-[#121215] shadow-xl bg-gray-800" 
                      @error="onImgError"
                    />
                    <div v-if="item.quantity > 1" class="absolute -top-2 -right-2 bg-yellow-500 text-black text-[10px] font-black w-6 h-6 flex items-center justify-center rounded-full border-2 border-[#121215] shadow-lg z-20">
                      {{ item.quantity }}
                    </div>
                  </div>
                </div>
              </div>

              <div class="flex items-center justify-between pt-5 border-t border-white/5">
                <div class="flex items-center gap-2 text-gray-500 text-xs font-medium">
                  <span class="text-lg opacity-50">📅</span>
                  {{ formatDate(order.created_at) }}
                </div>
                <div class="text-right">
                  <p class="text-[10px] text-gray-500 uppercase font-bold tracking-widest mb-1">Total Amount</p>
                  <p class="text-2xl md:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-200 to-yellow-500">
                    ฿{{ order.total_price?.toLocaleString() }}
                  </p>
                </div>
              </div>
            </div>
          </TransitionGroup>
        </div>

        <div v-else class="py-20 text-center animate-in-fade bg-[#121215]/40 rounded-[3rem] border border-white/5 border-dashed">
          <div class="w-24 h-24 rounded-full bg-gradient-to-b from-gray-800 to-black mx-auto mb-6 flex items-center justify-center text-5xl grayscale opacity-30 border border-white/5">
            🧾
          </div>
          <h3 class="text-2xl font-bold text-white mb-2">ไม่พบรายการสั่งซื้อ</h3>
          <p class="text-gray-500 mb-8 max-w-sm mx-auto">ยังไม่มีประวัติการสั่งซื้อในหมวดหมู่นี้ ท่านสามารถเลือกซื้อสินค้าได้ที่หน้า Dashboard</p>
          <NuxtLink to="/dashboard" class="inline-flex items-center gap-2 px-8 py-3.5 bg-white text-black rounded-2xl font-bold hover:bg-gray-200 hover:scale-105 active:scale-95 transition-all shadow-[0_0_20px_rgba(255,255,255,0.2)]">
            <span>🛒</span> ไปเลือกซื้อสินค้า
          </NuxtLink>
        </div>

        <Teleport to="body">
          <Transition name="modal">
            <div v-if="selectedOrder" class="fixed inset-0 z-[100] flex items-center justify-center p-4" @click.self="selectedOrder = null">
              <div class="absolute inset-0 bg-black/90 backdrop-blur-md transition-opacity"></div>
              
              <div class="relative w-full max-w-lg max-h-[90vh] bg-[#18181b] rounded-[2.5rem] border border-white/10 shadow-[0_0_50px_rgba(0,0,0,0.8)] flex flex-col overflow-hidden animate-zoom-in">
                
                <div class="p-6 md:p-8 border-b border-white/5 flex items-center justify-between bg-white/[0.02]">
                  <div>
                    <h2 class="text-xl font-bold text-white flex items-center gap-2">
                      <span>🧾</span> รายละเอียดคำสั่งซื้อ
                    </h2>
                    <p class="text-xs text-gray-500 font-mono mt-1">ID: #{{ selectedOrder._id }}</p>
                  </div>
                  <button @click="selectedOrder = null" class="w-10 h-10 rounded-full bg-white/5 hover:bg-white/10 flex items-center justify-center text-gray-400 hover:text-white transition-colors">
                    ✕
                  </button>
                </div>
                
                <div class="p-6 md:p-8 overflow-y-auto custom-scrollbar flex-1 space-y-6">
                  
                  <div class="grid grid-cols-2 gap-4">
                    <div class="bg-white/5 rounded-2xl p-4 border border-white/5">
                      <p class="text-[10px] uppercase text-gray-500 font-bold tracking-widest mb-2">Status</p>
                      <span :class="getStatusClass(selectedOrder.status)" class="px-3 py-1 rounded-lg text-xs font-bold uppercase border">
                        {{ getStatusLabel(selectedOrder.status) }}
                      </span>
                    </div>
                    <div class="bg-white/5 rounded-2xl p-4 border border-white/5">
                      <p class="text-[10px] uppercase text-gray-500 font-bold tracking-widest mb-2">Date</p>
                      <p class="text-sm font-medium text-white">{{ formatDate(selectedOrder.created_at) }}</p>
                    </div>
                  </div>

                  <div class="space-y-3">
                    <p class="text-xs font-bold text-gray-400 uppercase tracking-wider pl-1">Items List</p>
                    <div v-for="item in selectedOrder.items" :key="item.product?.id" class="flex items-center gap-4 bg-white/[0.03] p-3 rounded-2xl border border-white/5">
                      <img :src="getImageUrl(item.product?.image_url)" class="w-14 h-14 rounded-xl object-cover bg-gray-800" @error="onImgError" />
                      <div class="flex-1 min-w-0">
                        <p class="text-white text-sm font-bold truncate mb-1">{{ item.product?.name || 'สินค้าไม่ระบุชื่อ' }}</p>
                        <p class="text-gray-500 text-xs">จำนวน: <span class="text-white">{{ item.quantity }}</span> ชิ้น</p>
                      </div>
                      <div class="text-right">
                        <p class="text-yellow-400 font-bold text-sm">฿{{ (item.price * item.quantity).toLocaleString() }}</p>
                      </div>
                    </div>
                  </div>

                  <div class="flex justify-between items-center pt-4 border-t border-white/5">
                    <span class="text-gray-400 font-medium">ยอดรวมทั้งสิ้น</span>
                    <span class="text-3xl font-black text-white">฿{{ selectedOrder.total_price?.toLocaleString() }}</span>
                  </div>
                </div>

                <div class="p-6 bg-[#0f0f12] border-t border-white/5 space-y-3">
                  <button 
                    v-if="['pending', 'paid'].includes(selectedOrder.status)" 
                    @click="cancelOrder(selectedOrder)"
                    class="w-full py-3.5 rounded-xl bg-red-500/10 text-red-400 font-bold hover:bg-red-500 hover:text-white transition-all border border-red-500/20 flex items-center justify-center gap-2"
                  >
                    <span>💔</span> ยกเลิกคำสั่งซื้อ
                  </button>

                  <button 
                    @click="selectedOrder = null" 
                    class="w-full py-3.5 rounded-xl bg-white/5 text-gray-300 font-bold hover:bg-white/10 hover:text-white transition-all border border-white/5"
                  >
                    ปิดหน้าต่าง
                  </button>
                </div>
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

// ============ Logic เดิม ============
const orders = ref([]);
const loading = ref(true);
const selectedOrder = ref(null);
const activeFilter = ref('all');
const baseURL = 'http://localhost:5000';

const filters = [
  { label: '🏰 ทั้งหมด', value: 'all' },
  { label: '💰 จ่ายแล้ว', value: 'paid' },
  { label: '🚚 กำลังส่ง', value: 'processing' },
  { label: '✅ สำเร็จ', value: 'completed' },
  { label: '❌ ยกเลิก', value: 'cancelled' },
];

const getImageUrl = (path) => {
  if (!path) return '/no-image.png';
  if (path.startsWith('http')) return path;
  return `${baseURL}${path.startsWith('/') ? '' : '/'}${path}`;
};

const onImgError = (e) => {
  e.target.src = 'https://via.placeholder.com/150?text=No+Image';
};

const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A';
  return new Date(dateStr).toLocaleDateString('th-TH', {
    day: 'numeric', month: 'short', year: '2-digit', hour: '2-digit', minute: '2-digit'
  });
};

const filteredOrders = computed(() => {
  if (activeFilter.value === 'all') return orders.value;
  return orders.value.filter(o => o.status === activeFilter.value);
});

// Update Styling for Luxury Theme
function getStatusClass(status) {
  const classes = {
    pending: 'bg-yellow-500/10 text-yellow-500 border-yellow-500/20 shadow-[0_0_10px_rgba(234,179,8,0.1)]',
    paid: 'bg-blue-500/10 text-blue-400 border-blue-500/20 shadow-[0_0_10px_rgba(59,130,246,0.1)]',
    processing: 'bg-purple-500/10 text-purple-400 border-purple-500/20 shadow-[0_0_10px_rgba(168,85,247,0.1)]',
    completed: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20 shadow-[0_0_10px_rgba(16,185,129,0.1)]',
    cancelled: 'bg-red-500/10 text-red-400 border-red-500/20',
  };
  return classes[status] || 'bg-gray-500/10 text-gray-400 border-gray-500/20';
}

function getStatusLabel(status) {
  const labels = {
    pending: 'รอตรวจสอบ',
    paid: 'ชำระเงินแล้ว',
    processing: 'กำลังจัดส่ง',
    completed: 'สำเร็จ',
    cancelled: 'ยกเลิกแล้ว',
  };
  return labels[status] || status;
}

// Function ดึงข้อมูล
async function fetchOrders() {
  const token = localStorage.getItem('token');
  if (!token) return;

  loading.value = true;
  try {
    const res = await axios.get(`${baseURL}/api/orders/my-orders`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    orders.value = Array.isArray(res.data) ? res.data : (res.data.orders || []);
  } catch (err) {
    console.error('Failed to fetch orders:', err);
  } finally {
    loading.value = false;
  }
}

// Function ยกเลิกคำสั่งซื้อ
async function cancelOrder(order) {
  if (!confirm('ยืนยันการยกเลิกคำสั่งซื้อนะเพคะ?')) return;
  
  const token = localStorage.getItem('token');
  try {
    await axios.put(`${baseURL}/api/orders/${order._id}/cancel`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    alert('ยกเลิกสำเร็จแล้วเพคะ ✨');
    selectedOrder.value = null; 
    await fetchOrders(); 
  } catch (err) {
    console.error('Failed to cancel order:', err);
    alert(err.response?.data?.msg || 'ไม่สามารถยกเลิกได้ในขณะนี้เพคะ');
  }
}

onMounted(fetchOrders);
</script>

<style scoped>
/* Page Entrance */
.animate-in-fade {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

/* Modal Animations */
.modal-enter-active, .modal-leave-active { transition: opacity 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }

.animate-zoom-in {
  animation: zoomIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}
@keyframes zoomIn {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

/* List Transitions */
.list-enter-active, .list-leave-active { transition: all 0.4s ease; }
.list-enter-from, .list-leave-to { opacity: 0; transform: translateY(10px); }

/* Utilities */
.no-scrollbar::-webkit-scrollbar { display: none; }
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
</style>