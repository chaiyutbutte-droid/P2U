<template>
  <div class="min-h-screen ml-20 p-6 text-white bg-dark-950">
    <Navbar />
    <sidebar />
    
    <div class="max-w-4xl mx-auto">
      <header class="flex items-center justify-between mb-8 mt-4">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-white to-pink-300 bg-clip-text text-transparent">
            📦 ประวัติคำสั่งซื้อ
          </h1>
          <p class="text-dark-400 mt-1">เจ้าหญิงสามารถตรวจสอบสถานะการส่งสินค้าได้ที่นี่เพคะ</p>
        </div>
        <NuxtLink to="/dashboard" class="text-sm text-pink-400 hover:text-pink-300">
          กลับไปหน้าหลัก
        </NuxtLink>
      </header>

      <div class="flex gap-3 mb-8 overflow-x-auto pb-2 no-scrollbar">
        <button 
          v-for="filter in filters" 
          :key="filter.value"
          @click="activeFilter = filter.value"
          class="px-5 py-2.5 rounded-2xl text-sm font-medium transition-all whitespace-nowrap border"
          :class="activeFilter === filter.value 
            ? 'bg-pink-500 border-pink-500 text-white shadow-lg shadow-pink-500/20' 
            : 'glass border-white/5 text-dark-300 hover:text-white hover:border-white/10'"
        >
          {{ filter.label }}
        </button>
      </div>

      <div v-if="filteredOrders.length" class="space-y-4">
        <div 
          v-for="order in filteredOrders" 
          :key="order.id" 
          class="glass p-6 rounded-[2rem] border border-white/5 hover:border-pink-500/30 transition-all cursor-pointer group shadow-xl"
          @click="selectedOrder = order"
        >
          <div class="flex items-start justify-between mb-5">
            <div class="space-y-1">
              <p class="text-dark-400 text-[10px] uppercase tracking-widest font-bold">Order ID</p>
              <p class="text-white font-mono text-sm group-hover:text-pink-300 transition-colors">#{{ order.id }}</p>
            </div>
            <span :class="getStatusClass(order.status)" class="px-3 py-1 rounded-full text-[11px] font-bold uppercase tracking-tighter">
              {{ getStatusLabel(order.status) }}
            </span>
          </div>

          <div class="flex items-center gap-3 mb-6">
            <div v-for="(item, idx) in order.items.slice(0, 4)" :key="idx" class="relative">
              <img 
                :src="getImageUrl(item.product_image)" 
                class="w-16 h-16 rounded-2xl object-cover border border-white/10 shadow-lg" 
                @error="onImgError"
              />
              <span v-if="item.quantity > 1" class="absolute -top-2 -right-2 bg-pink-500 text-white text-[10px] font-black w-6 h-6 flex items-center justify-center rounded-full border-2 border-dark-950">
                {{ item.quantity }}
              </span>
            </div>
            <div v-if="order.items.length > 4" class="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center text-dark-400 text-sm border border-dashed border-white/10">
              +{{ order.items.length - 4 }}
            </div>
          </div>

          <div class="flex items-center justify-between pt-5 border-t border-white/5">
            <div class="flex items-center gap-2 text-dark-400 text-xs">
              <span class="opacity-50 text-base">📅</span>
              {{ order.created_at }}
            </div>
            <div class="text-right">
              <p class="text-[10px] text-dark-400 uppercase mb-0.5">ยอดชำระสุทธิ</p>
              <p class="text-2xl font-black text-white">฿{{ order.total_price.toLocaleString() }}</p>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="glass p-20 text-center rounded-[3rem] border border-white/5">
        <div class="text-6xl mb-6 grayscale opacity-50">🏰</div>
        <h3 class="text-xl font-bold text-white mb-2">ไม่มีรายการสั่งซื้อเพคะ</h3>
        <p class="text-dark-400 mb-8 max-w-xs mx-auto">ยังไม่มีประวัติการสั่งซื้อในหมวดหมู่นี้ เจ้าหญิงต้องการไปเลือกซื้อสินค้าเพิ่มไหมเพคะ?</p>
        <NuxtLink to="/dashboard" class="inline-block px-10 py-4 bg-gradient-to-r from-pink-500 to-rose-600 rounded-2xl font-bold text-white shadow-lg shadow-pink-500/20 hover:scale-105 transition-transform">
          🛒 ไปที่หน้าสินค้า ✨
        </NuxtLink>
      </div>

      <Teleport to="body">
        <Transition name="fade">
          <div v-if="selectedOrder" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4" @click.self="selectedOrder = null">
            <div class="glass border border-white/10 rounded-[2.5rem] w-full max-w-lg max-h-[85vh] overflow-hidden flex flex-col shadow-2xl animate-modal">
              <div class="p-8 border-b border-white/5 flex items-center justify-between">
                <h2 class="text-xl font-bold text-white">รายละเอียดคำสั่งซื้อ ✨</h2>
                <button @click="selectedOrder = null" class="w-10 h-10 rounded-full hover:bg-white/5 flex items-center justify-center text-dark-400 text-2xl transition-colors">&times;</button>
              </div>
              
              <div class="p-8 overflow-y-auto space-y-6 flex-1 custom-scrollbar">
                <div class="grid grid-cols-2 gap-4">
                  <div class="space-y-1">
                    <p class="text-[10px] uppercase text-dark-400 font-bold tracking-widest">สถานะปัจจุบัน</p>
                    <span :class="getStatusClass(selectedOrder.status)" class="px-3 py-1 rounded-lg text-xs font-bold uppercase">{{ getStatusLabel(selectedOrder.status) }}</span>
                  </div>
                  <div class="text-right space-y-1">
                    <p class="text-[10px] uppercase text-dark-400 font-bold tracking-widest">วันที่ทำรายการ</p>
                    <p class="text-white text-sm font-medium">{{ selectedOrder.created_at }}</p>
                  </div>
                </div>

                <div class="bg-white/5 p-4 rounded-2xl space-y-3">
                  <p class="text-xs text-pink-400 font-bold uppercase mb-2">รายการสินค้า</p>
                  <div v-for="item in selectedOrder.items" :key="item.product_id" class="flex items-center gap-4">
                    <img :src="getImageUrl(item.product_image)" class="w-12 h-12 rounded-xl object-cover shadow-md" @error="onImgError" />
                    <div class="flex-1 min-w-0">
                      <p class="text-white text-sm font-bold truncate">{{ item.product_name }}</p>
                      <p class="text-dark-400 text-[11px]">จำนวน: {{ item.quantity }} ชิ้น</p>
                    </div>
                    <p class="text-white font-black text-sm">฿{{ (item.price * item.quantity).toLocaleString() }}</p>
                  </div>
                </div>

                <div class="pt-2 flex justify-between items-center">
                  <span class="text-dark-300 font-medium">รวมการสั่งซื้อทั้งสิ้น</span>
                  <span class="text-3xl font-black text-pink-500">฿{{ selectedOrder.total_price.toLocaleString() }}</span>
                </div>
              </div>

              <div class="p-8 bg-white/5 border-t border-white/5">
                <button 
                  v-if="selectedOrder.status === 'paid' || selectedOrder.status === 'pending'" 
                  @click="cancelOrder(selectedOrder)"
                  class="w-full py-4 rounded-2xl bg-red-500/10 text-red-400 font-bold hover:bg-red-500 hover:text-white transition-all border border-red-500/20"
                >
                  💔 ยกเลิกคำสั่งซื้อ
                </button>
                <button 
                  v-else
                  @click="selectedOrder = null"
                  class="w-full py-4 rounded-2xl bg-white/5 text-white font-bold hover:bg-white/10 transition-all border border-white/10"
                >
                  ปิดหน้าต่าง
                </button>
              </div>
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

const orders = ref([]);
const selectedOrder = ref(null);
const activeFilter = ref('all');

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
  return `http://localhost:5000/${path.replace(/^\/+/, '')}`;
};

const onImgError = (e) => {
  e.target.src = '/no-image.png';
};

const filteredOrders = computed(() => {
  if (activeFilter.value === 'all') return orders.value;
  return orders.value.filter(o => o.status === activeFilter.value);
});

function getStatusClass(status) {
  const classes = {
    pending: 'bg-amber-500/10 text-amber-500 border border-amber-500/20',
    paid: 'bg-pink-500/10 text-pink-500 border border-pink-500/20',
    processing: 'bg-blue-500/10 text-blue-500 border border-blue-500/20',
    completed: 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20',
    cancelled: 'bg-red-500/10 text-red-500 border border-red-500/20',
  };
  return classes[status] || 'bg-white/10 text-white';
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

async function fetchOrders() {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    // ✅ แก้ไข URL ให้มี /api นำหน้าเพื่อให้ตรงกับ Blueprint
    const res = await axios.get('http://localhost:5000/api/orders', {
      headers: { Authorization: `Bearer ${token}` }
    });
    orders.value = res.data.orders || [];
  } catch (err) {
    console.error('Failed to fetch orders:', err);
  }
}

async function cancelOrder(order) {
  if (!confirm('ยืนยันการยกเลิกคำสั่งซื้อนะเพคะ?')) return;
  
  const token = localStorage.getItem('token');
  try {
    // ✅ แก้ไข URL ให้มี /api นำหน้า
    await axios.put(`http://localhost:5000/api/orders/${order.id}/cancel`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    order.status = 'cancelled';
    selectedOrder.value = null;
    alert('ยกเลิกสำเร็จแล้วเพคะ ✨');
    await fetchOrders(); // ดึงข้อมูลใหม่
  } catch (err) {
    console.error('Failed to cancel order:', err);
    alert(err.response?.data?.msg || 'ไม่สามารถยกเลิกได้');
  }
}

onMounted(fetchOrders);
</script>

<style scoped>
.glass { 
  background: rgba(255, 255, 255, 0.03); 
  backdrop-filter: blur(20px); 
  -webkit-backdrop-filter: blur(20px);
}
.bg-dark-950 { background-color: #050505; }
.text-dark-300 { color: #9ca3af; }
.text-dark-400 { color: #6b7280; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.animate-modal { animation: zoomIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
@keyframes zoomIn {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}

.no-scrollbar::-webkit-scrollbar { display: none; }
.custom-scrollbar::-webkit-scrollbar { width: 6px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
</style>