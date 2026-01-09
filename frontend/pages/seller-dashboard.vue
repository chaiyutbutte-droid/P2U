<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />
    
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-2xl font-bold text-white flex items-center gap-2">
          📊 แดชบอร์ดผู้ขาย
        </h1>
        <p class="text-dark-400 mt-1">ยินดีต้อนรับ, {{ user?.shop_name || user?.username }}</p>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-dark-400 text-sm">ยอดขายรวม</p>
              <p class="text-3xl font-bold text-green-400 mt-1">฿{{ stats.total_sales?.toLocaleString() || 0 }}</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center text-2xl">
              💰
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-dark-400 text-sm">สินค้าทั้งหมด</p>
              <p class="text-3xl font-bold text-white mt-1">{{ stats.total_products || 0 }}</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-primary-500/20 flex items-center justify-center text-2xl">
              📦
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-dark-400 text-sm">คะแนนเฉลี่ย</p>
              <p class="text-3xl font-bold text-yellow-400 mt-1">{{ stats.rating_avg?.toFixed(1) || 0 }} ⭐</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-yellow-500/20 flex items-center justify-center text-2xl">
              ⭐
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-dark-400 text-sm">ระดับ AI</p>
              <p class="text-3xl font-bold mt-1" :class="getLevelColor(stats.ai_level)">{{ stats.ai_level || 'C' }}</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-accent-500/20 flex items-center justify-center text-2xl">
              🏆
            </div>
          </div>
        </div>
      </div>

      <!-- Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- My Products -->
        <div class="card overflow-hidden">
          <div class="p-4 border-b border-white/10 flex items-center justify-between">
            <h2 class="font-semibold text-white">🛍️ สินค้าของฉัน</h2>
            <NuxtLink to="/AddProduct" class="text-primary-400 text-sm hover:underline">+ เพิ่มสินค้า</NuxtLink>
          </div>
          <div class="divide-y divide-white/5">
            <div v-for="product in products.slice(0, 5)" :key="product.id" class="p-4 flex items-center gap-3">
              <img :src="product.image_url || '/placeholder.png'" class="w-12 h-12 rounded-lg object-cover" />
              <div class="flex-1 min-w-0">
                <p class="text-white font-medium truncate">{{ product.name }}</p>
                <p class="text-green-400 text-sm">฿{{ product.price.toLocaleString() }}</p>
              </div>
            </div>
            <div v-if="!products.length" class="p-8 text-center text-dark-400">
              ยังไม่มีสินค้า
            </div>
          </div>
        </div>

        <!-- Recent Reviews -->
        <div class="card overflow-hidden">
          <div class="p-4 border-b border-white/10">
            <h2 class="font-semibold text-white">⭐ รีวิวล่าสุด</h2>
          </div>
          <div class="divide-y divide-white/5">
            <div v-for="review in reviews.slice(0, 5)" :key="review.id" class="p-4">
              <div class="flex items-center gap-2 mb-2">
                <span class="text-yellow-400">{{ '⭐'.repeat(review.rating) }}</span>
                <span class="text-dark-400 text-sm">{{ review.user?.username }}</span>
              </div>
              <p class="text-dark-300 text-sm">{{ review.comment }}</p>
              <p class="text-dark-500 text-xs mt-1">{{ review.product?.name }}</p>
            </div>
            <div v-if="!reviews.length" class="p-8 text-center text-dark-400">
              ยังไม่มีรีวิว
            </div>
          </div>
        </div>

        <!-- Recent Orders -->
        <div class="card overflow-hidden lg:col-span-2">
          <div class="p-4 border-b border-white/10">
            <h2 class="font-semibold text-white">📦 ออเดอร์ล่าสุด</h2>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead class="bg-dark-800/50">
                <tr>
                  <th class="text-left p-4 text-dark-400 text-sm font-medium">ผู้ซื้อ</th>
                  <th class="text-left p-4 text-dark-400 text-sm font-medium">สินค้า</th>
                  <th class="text-left p-4 text-dark-400 text-sm font-medium">ยอด</th>
                  <th class="text-left p-4 text-dark-400 text-sm font-medium">สถานะ</th>
                  <th class="text-left p-4 text-dark-400 text-sm font-medium">วันที่</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in recentOrders" :key="order.id" class="border-b border-white/5">
                  <td class="p-4 text-white">{{ order.user }}</td>
                  <td class="p-4 text-dark-300">{{ order.items_count }} รายการ</td>
                  <td class="p-4 text-green-400 font-medium">฿{{ order.total.toLocaleString() }}</td>
                  <td class="p-4">
                    <span :class="getStatusClass(order.status)" class="badge">
                      {{ getStatusLabel(order.status) }}
                    </span>
                  </td>
                  <td class="p-4 text-dark-400 text-sm">{{ order.created_at }}</td>
                </tr>
              </tbody>
            </table>
            <div v-if="!recentOrders.length" class="p-8 text-center text-dark-400">
              ยังไม่มีออเดอร์
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

const user = ref(null);
const stats = ref({});
const products = ref([]);
const reviews = ref([]);
const recentOrders = ref([]);

const baseUrl = 'http://localhost:5000';

function getLevelColor(level) {
  const colors = {
    S: 'text-yellow-400',
    A: 'text-green-400',
    B: 'text-primary-400',
    C: 'text-dark-400',
  };
  return colors[level] || 'text-dark-400';
}

function getStatusClass(status) {
  const classes = {
    pending: 'badge-warning',
    processing: 'badge-primary',
    completed: 'badge-success',
    cancelled: 'badge-error',
    paid: 'badge-primary',
  };
  return classes[status] || 'badge-primary';
}

function getStatusLabel(status) {
  const labels = {
    pending: '⏳ รอ',
    processing: '🔄 กำลังดำเนินการ',
    completed: '✓ สำเร็จ',
    cancelled: '✕ ยกเลิก',
    paid: '💰 ชำระแล้ว',
  };
  return labels[status] || status;
}
async function fetchOrders() {
  const token = localStorage.getItem('token');
  if (!token || !user.value?.id) return;

  try {
    const res = await axios.get(
  `${baseUrl}/api/orders/seller/${user.value.id}`,
  {
    headers: { Authorization: `Bearer ${token}` },
  }
);

console.log('RAW ORDER RESPONSE 👉', res.data);


    // ✅ ตรงนี้คือหัวใจ
    const orders = res.data.orders || [];

    recentOrders.value = orders.map(order => ({
      id: order.id,
      user: order.buyer?.username || 'ไม่ทราบชื่อ',
      items_count: order.items_count || order.items?.length || 0,
      total: order.total_price || 0,
      status: order.status,
      created_at: order.created_at
        ? new Date(order.created_at).toLocaleDateString()
        : '-',
    }));

    console.log('📦 seller orders:', recentOrders.value);
  } catch (err) {
    console.error('ดึงออเดอร์ไม่สำเร็จ:', err);
  }
}


async function fetchData() {
  const token = localStorage.getItem('token');
  if (!token) return;

  const storedUser = localStorage.getItem('user');
  if (storedUser) {
    user.value = JSON.parse(storedUser);
  }

  try {
    const profileRes = await axios.get(`${baseUrl}/api/profile`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    stats.value = {
      total_sales: profileRes.data.total_sales,
      rating_avg: profileRes.data.rating_avg,
      ai_level: profileRes.data.ai_level,
    };

    const productsRes = await axios.get(`${baseUrl}/api/products`);
    products.value = productsRes.data.filter(
      p => p.seller?.id === user.value?.id
    );
    stats.value.total_products = products.value.length;

    if (user.value?.id) {
      const reviewsRes = await axios.get(
        `${baseUrl}/api/reviews/seller/${user.value.id}`
      );
      reviews.value = reviewsRes.data.reviews || [];
    }

    // ✅ ดึงออเดอร์ของ seller
    await fetchOrders();
  } catch (err) {
    console.error('Failed to fetch seller data:', err);
  }
}

onMounted(fetchData);
</script>
