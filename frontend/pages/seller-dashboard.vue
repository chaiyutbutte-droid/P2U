<template>
  <div class="min-h-screen ml-20 p-6 text-white bg-[#0b0b0f]">
    <sidebar />
    
    <div class="max-w-6xl mx-auto">
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-white flex items-center gap-2">
          📊 แดชบอร์ดผู้ขาย
        </h1>
        <ClientOnly>
          <p class="text-gray-400 mt-1">ยินดีต้อนรับ, {{ user?.shop_name || user?.username || 'ผู้ขาย' }}</p>
        </ClientOnly>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">ยอดขายรวม</p>
              <p class="text-3xl font-bold text-green-400 mt-1">฿{{ stats.total_sales?.toLocaleString() || 0 }}</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center text-2xl">💰</div>
          </div>
        </div>
        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">สินค้าทั้งหมด</p>
              <p class="text-3xl font-bold text-white mt-1">{{ stats.total_products || 0 }}</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-pink-500/20 flex items-center justify-center text-2xl">📦</div>
          </div>
        </div>
        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">คะแนนเฉลี่ย</p>
              <p class="text-3xl font-bold text-yellow-400 mt-1">{{ stats.rating_avg?.toFixed(1) || 0 }} ⭐</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-yellow-500/20 flex items-center justify-center text-2xl">⭐</div>
          </div>
        </div>
        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-gray-400 text-sm">ระดับ AI</p>
              <p class="text-3xl font-bold mt-1" :class="getLevelColor(stats.ai_level)">{{ stats.ai_level || 'C' }}</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-purple-500/20 flex items-center justify-center text-2xl">🏆</div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="card overflow-hidden">
          <div class="p-4 border-b border-white/10 flex items-center justify-between">
            <h2 class="font-semibold text-white">🛍️ สินค้าของฉัน</h2>
            <NuxtLink to="/AddProduct" class="text-pink-400 text-sm hover:underline">+ เพิ่มสินค้า</NuxtLink>
          </div>
          <div class="divide-y divide-white/5">
            <div v-for="product in products.slice(0, 5)" :key="product.id || product._id" class="p-4 flex items-center gap-3 hover:bg-white/5 transition-colors group">
              <img :src="getImageUrl(product.image_url)" class="w-12 h-12 rounded-lg object-cover" @error="(e) => e.target.src = '/placeholder.png'" />
              <div class="flex-1 min-w-0">
                <p class="text-white font-medium truncate">{{ product.name }}</p>
                <div class="flex items-center gap-2">
                  <p class="text-green-400 text-sm">฿{{ product.price?.toLocaleString() }}</p>
                  <span v-if="product.category" class="text-xs text-gray-400 bg-white/5 px-2 py-0.5 rounded-full">{{ getCategoryIcon(product.category) }} {{ product.category }}</span>
                </div>
              </div>
              <div class="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <NuxtLink :to="`/edit-product/${product.id || product._id}`" class="w-8 h-8 bg-pink-500/20 hover:bg-pink-500 text-pink-400 hover:text-white rounded-lg flex items-center justify-center transition-all" title="แก้ไข">
                  ✏️
                </NuxtLink>
                <button @click="deleteProduct(product.id || product._id)" class="w-8 h-8 bg-red-500/20 hover:bg-red-500 text-red-400 hover:text-white rounded-lg flex items-center justify-center transition-all" title="ลบ">
                  🗑️
                </button>
              </div>
            </div>
            <div v-if="!products.length" class="p-8 text-center text-gray-400">ยังไม่มีสินค้า</div>
          </div>
          <div v-if="products.length > 5" class="p-4 border-t border-white/10 text-center">
            <NuxtLink to="/my-products" class="text-pink-400 text-sm hover:underline">ดูสินค้าทั้งหมด ({{ products.length }} รายการ) →</NuxtLink>
          </div>
        </div>


        <div class="card overflow-hidden">
          <div class="p-4 border-b border-white/10">
            <h2 class="font-semibold text-white">⭐ รีวิวล่าสุด</h2>
          </div>
          <div class="divide-y divide-white/5">
            <div v-for="review in reviews.slice(0, 5)" :key="review.id" class="p-4">
              <div class="flex items-center gap-2 mb-2">
                <span class="text-yellow-400">{{ '⭐'.repeat(review.rating) }}</span>
                <span class="text-gray-400 text-sm">{{ review.user?.username }}</span>
              </div>
              <p class="text-gray-300 text-sm">{{ review.comment }}</p>
              <p class="text-gray-500 text-xs mt-1">{{ review.product?.name }}</p>
            </div>
            <div v-if="!reviews.length" class="p-8 text-center text-gray-400">ยังไม่มีรีวิว</div>
          </div>
        </div>

        <div class="card overflow-hidden lg:col-span-2">
          <div class="p-4 border-b border-white/10 flex justify-between items-center">
            <h2 class="font-semibold text-white">📦 ออเดอร์ล่าสุด</h2>
            <span class="text-[10px] text-pink-400 animate-pulse">คลิกเพื่อดูรายละเอียด / จัดส่ง</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-gray-800/50">
                <tr>
                  <th class="text-left p-4 text-gray-400 text-sm font-medium">ผู้ซื้อ</th>
                  <th class="text-left p-4 text-gray-400 text-sm font-medium">สินค้า</th>
                  <th class="text-left p-4 text-gray-400 text-sm font-medium">ยอด</th>
                  <th class="text-left p-4 text-gray-400 text-sm font-medium">สถานะ</th>
                  <th class="text-left p-4 text-gray-400 text-sm font-medium">วันที่</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in recentOrders" 
                    :key="order.id" 
                    @click="selectedOrder = order"
                    class="border-b border-white/5 hover:bg-white/5 cursor-pointer transition-all">
                  <td class="p-4 text-white font-medium">{{ order.user }}</td>
                  <td class="p-4 text-gray-300 text-sm">{{ order.items_count }} รายการ</td>
                  <td class="p-4 text-green-400 font-bold">฿{{ order.total.toLocaleString() }}</td>
                  <td class="p-4">
                    <span :class="[getStatusClass(order.status), 'px-2 py-0.5 rounded-full font-bold border text-[10px]']">
                      {{ getStatusLabel(order.status) }}
                    </span>
                  </td>
                  <td class="p-4 text-gray-400 text-sm">{{ order.created_at }}</td>
                </tr>
              </tbody>
            </table>
            <div v-if="!recentOrders.length" class="p-8 text-center text-gray-400">ยังไม่มีออเดอร์</div>
          </div>
        </div>
      </div>
    </div>

    <Teleport to="body">
      <Transition name="fade">
        <div v-if="selectedOrder" class="fixed inset-0 bg-black/80 backdrop-blur-md z-50 flex items-center justify-center p-4" @click.self="selectedOrder = null">
          <div class="card border border-white/10 w-full max-w-lg overflow-hidden flex flex-col shadow-2xl animate-modal">
            <div class="p-6 border-b border-white/10 flex items-center justify-between bg-white/5">
              <h2 class="text-lg font-bold text-white flex items-center gap-2">
                📄 รายละเอียดออเดอร์ <span class="text-xs font-mono text-gray-400">#{{ selectedOrder.id.slice(-6) }}</span>
              </h2>
              <button @click="selectedOrder = null" class="text-gray-400 text-2xl hover:text-white transition-colors">&times;</button>
            </div>
            
            <div class="p-6 overflow-y-auto space-y-6 max-h-[70vh]">
              <div class="flex justify-between items-end">
                <div>
                  <p class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">ผู้ซื้อ</p>
                  <p class="text-white text-lg font-medium">{{ selectedOrder.user }}</p>
                </div>
                <div class="text-right">
                  <p class="text-[10px] text-gray-400 uppercase font-bold tracking-wider">สถานะ</p>
                  <span :class="[getStatusClass(selectedOrder.status), 'px-2 py-0.5 rounded-full font-bold border text-[10px]']">
                      {{ getStatusLabel(selectedOrder.status) }}
                  </span>
                </div>
              </div>

              <div class="space-y-3">
                <p class="text-[10px] text-pink-400 uppercase font-bold tracking-wider">รายการสินค้าในร้านของคุณ</p>
                <div v-for="item in selectedOrder.rawItems" :key="item.product_id" class="flex items-center gap-4 bg-white/5 p-3 rounded-2xl border border-white/5">
                  <img :src="getImageUrl(item.image)" class="w-12 h-12 rounded-xl object-cover shadow-lg" />
                  <div class="flex-1 min-w-0">
                    <p class="text-white text-sm font-bold truncate">{{ item.product_name }}</p>
                    <p class="text-gray-400 text-xs">จำนวน: {{ item.quantity }} ชิ้น</p>
                  </div>
                  <p class="text-white font-bold">฿{{ (item.price * item.quantity).toLocaleString() }}</p>
                </div>
              </div>

              <div class="pt-4 border-t border-white/10 flex justify-between items-center">
                <span class="text-gray-300">ยอดรวมของร้านคุณ</span>
                <span class="text-2xl font-black text-green-400">฿{{ selectedOrder.total.toLocaleString() }}</span>
              </div>
            </div>

            <div class="p-6 bg-white/5 border-t border-white/10">
              <button 
                v-if="selectedOrder.status === 'paid'" 
                :disabled="isUpdating"
                @click="updateOrderStatus(selectedOrder.id, 'processing')"
                class="w-full py-4 rounded-2xl bg-pink-500 hover:bg-pink-600 text-white font-bold transition-all shadow-lg shadow-pink-500/20 flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <span v-if="isUpdating">⏳ กำลังดำเนินการ...</span>
                <span v-else>🚚 ยืนยันการจัดส่งสินค้า ✨</span>
              </button>
              
              <button 
                v-else
                @click="selectedOrder = null"
                class="w-full py-4 rounded-2xl bg-white/10 text-white font-bold hover:bg-white/20 transition-all"
              >
                ปิดหน้าต่าง
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const user = ref(null);
const isUpdating = ref(false);
const stats = ref({
  total_sales: 0,
  total_products: 0,
  rating_avg: 0,
  ai_level: 'C'
});
const products = ref([]);
const reviews = ref([]);
const recentOrders = ref([]);
const selectedOrder = ref(null);

const baseUrl = 'http://localhost:5000';

function getImageUrl(url) {
  if (!url) return '/placeholder.png';
  if (url.startsWith('http')) return url;
  return `${baseUrl}${url.startsWith('/') ? '' : '/'}${url}`;
}

function getLevelColor(level) {
  const colors = { S: 'text-yellow-400', A: 'text-green-400', B: 'text-pink-400', C: 'text-gray-400' };
  return colors[level] || 'text-gray-400';
}

function getCategoryIcon(category) {
  const icons = {
    electronics: '📱', fashion: '👗', gaming: '🎮', beauty: '💄',
    home: '🏠', sports: '⚽', food: '🍔', books: '📚',
    toys: '🧸', pets: '🐶', automotive: '🚗', all: '🛍️'
  };
  return icons[category] || '📦';
}

async function deleteProduct(productId) {
  if (!confirm('❗ คุณต้องการลบสินค้านี้ใช่หรือไม่? การกระทำนี้ไม่สามารถยกเลิกได้')) return;
  
  const token = localStorage.getItem('token');
  try {
    await axios.delete(`${baseUrl}/api/seller/products/${productId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert('ลบสินค้าสำเร็จ! 🗑️');
    await fetchData();
  } catch (err) {
    console.error('Delete error:', err);
    alert('ไม่สามารถลบสินค้าได้');
  }
}

function getStatusClass(status) {
  const classes = { 
    pending: 'bg-amber-500/10 text-amber-500 border border-amber-500/20', 
    paid: 'bg-pink-500/10 text-pink-400 border border-pink-500/20', 
    processing: 'bg-blue-500/10 text-blue-400 border border-blue-500/20', 
    completed: 'bg-green-500/10 text-green-400 border border-green-500/20', 
    cancelled: 'bg-red-500/10 text-red-500 border border-red-500/20' 
  };
  return classes[status] || 'bg-white/10 text-white';
}

function getStatusLabel(status) {
  const labels = { pending: '⏳ รอชำระ', paid: '💰 ชำระแล้ว', processing: '🚚 กำลังส่ง', completed: '✅ สำเร็จ', cancelled: '❌ ยกเลิก' };
  return labels[status] || status;
}

async function updateOrderStatus(orderId, newStatus) {
  if (isUpdating.value) return;
  const token = localStorage.getItem('token');
  if (!confirm(`ยืนยันการจัดส่งสินค้าสำหรับออเดอร์นี้หรือไม่เพคะ?`)) return;

  isUpdating.value = true;
  try {
    await axios.put(`${baseUrl}/api/orders/${orderId}/status`, 
      { status: newStatus },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    
    alert('อัปเดตสถานะการจัดส่งเรียบร้อยแล้วเพคะ! 🚚✨');
    selectedOrder.value = null;
    await fetchData(); 
  } catch (err) {
    console.error('Update status error:', err);
    alert(err.response?.data?.msg || 'ไม่สามารถอัปเดตสถานะได้');
  } finally {
    isUpdating.value = false;
  }
}

async function fetchOrders() {
  const token = localStorage.getItem('token');
  const sellerId = user.value?.id || user.value?._id;
  
  if (!token || !sellerId) return;

  try {
    const res = await axios.get(`${baseUrl}/api/orders/seller/${sellerId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const ordersData = res.data.orders || [];
    recentOrders.value = ordersData.map(order => ({
      id: order.id || order._id, 
      user: order.buyer?.username || 'ไม่ทราบชื่อ',
      items_count: order.items_count || (order.items ? order.items.length : 0),
      total: order.total_price || 0,
      status: order.status,
      created_at: order.created_at || '-',
      rawItems: order.items || [] 
    }));
  } catch (err) {
    console.error('ดึงออเดอร์ไม่สำเร็จ:', err);
  }
}

async function fetchData() {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    const profileRes = await axios.get(`${baseUrl}/api/profile`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    user.value = profileRes.data;
    const currentId = user.value.id || user.value._id;

    stats.value = {
      ...stats.value,
      total_sales: profileRes.data.total_sales || 0,
      rating_avg: profileRes.data.rating_avg || 0,
      ai_level: profileRes.data.ai_level || 'C',
    };

    const productsRes = await axios.get(`${baseUrl}/api/products`);
    products.value = productsRes.data.filter(p => {
      const pSellerId = p.seller?.id || p.seller?._id || p.seller;
      return String(pSellerId) === String(currentId);
    });
    stats.value.total_products = products.value.length;

    const reviewsRes = await axios.get(`${baseUrl}/api/reviews/seller/${currentId}`);
    reviews.value = reviewsRes.data.reviews || [];

    await fetchOrders();
  } catch (err) {
    console.error('Failed to fetch seller data:', err);
  }
}

onMounted(fetchData);
</script>

<style scoped>
/* เลิกใช้ @apply ใน style block แล้วใช้ Standard CSS หรือย้ายไปที่ Template แทน */

.card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border-radius: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.animate-modal { animation: zoomIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }

@keyframes zoomIn {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
</style>