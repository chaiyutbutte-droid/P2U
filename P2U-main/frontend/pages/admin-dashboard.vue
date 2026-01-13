<template>
  <div class="min-h-screen p-6">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-white">Admin Dashboard</h1>
          <p class="text-dark-400 mt-1">ยินดีต้อนรับ, {{ adminUser?.username }}</p>
        </div>
        <button @click="handleLogout" class="btn-glass text-red-400 hover:bg-red-500/20">
          🚪 ออกจากระบบ
        </button>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-dark-400 text-sm">ผู้ใช้ทั้งหมด</p>
              <p class="text-3xl font-bold text-white mt-1">{{ stats.total_users }}</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-primary-500/20 flex items-center justify-center text-2xl">
              👥
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-dark-400 text-sm">ผู้ขาย</p>
              <p class="text-3xl font-bold text-white mt-1">{{ stats.total_sellers }}</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-accent-500/20 flex items-center justify-center text-2xl">
              🏪
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-dark-400 text-sm">สินค้า</p>
              <p class="text-3xl font-bold text-white mt-1">{{ stats.total_products }}</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-green-500/20 flex items-center justify-center text-2xl">
              📦
            </div>
          </div>
        </div>

        <div class="card p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-dark-400 text-sm">รายได้รวม</p>
              <p class="text-3xl font-bold text-green-400 mt-1">฿{{ stats.total_revenue?.toLocaleString() }}</p>
            </div>
            <div class="w-12 h-12 rounded-xl bg-yellow-500/20 flex items-center justify-center text-2xl">
              💰
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="flex gap-2 mb-6">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          @click="activeTab = tab.id"
          class="px-4 py-2 rounded-xl text-sm font-medium transition-colors"
          :class="activeTab === tab.id ? 'bg-primary-500 text-white' : 'glass text-dark-300 hover:text-white'"
        >
          {{ tab.icon }} {{ tab.name }}
        </button>
      </div>

      <!-- Users Table -->
      <div v-if="activeTab === 'users'" class="card overflow-hidden">
        <div class="p-4 border-b border-white/10">
          <h2 class="text-lg font-semibold text-white">จัดการผู้ใช้</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-dark-800/50">
              <tr>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">ผู้ใช้</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">อีเมล</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">บทบาท</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">สถานะ</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">Coins</th>
                <th class="text-right p-4 text-dark-400 text-sm font-medium">การจัดการ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id" class="border-b border-white/5 hover:bg-white/5">
                <td class="p-4">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-white font-bold">
                      {{ user.username.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <p class="text-white font-medium">{{ user.username }}</p>
                      <p class="text-dark-500 text-xs">{{ user.full_name }}</p>
                    </div>
                  </div>
                </td>
                <td class="p-4 text-dark-300">{{ user.email }}</td>
                <td class="p-4">
                  <span :class="user.is_seller ? 'badge-accent' : 'badge-primary'" class="badge">
                    {{ user.is_seller ? '🏪 ผู้ขาย' : '👤 ผู้ใช้' }}
                  </span>
                </td>
                <td class="p-4">
                  <span :class="user.is_active ? 'badge-success' : 'badge-error'" class="badge">
                    {{ user.is_active ? '✓ ใช้งาน' : '✕ ระงับ' }}
                  </span>
                </td>
                <td class="p-4 text-primary-400 font-medium">{{ user.coin_balance?.toLocaleString() }}</td>
                <td class="p-4 text-right">
                  <button 
                    @click="toggleBanUser(user)" 
                    :class="user.is_active ? 'text-yellow-400 hover:bg-yellow-500/20' : 'text-green-400 hover:bg-green-500/20'"
                    class="px-3 py-1.5 rounded-lg text-sm transition-colors"
                  >
                    {{ user.is_active ? '⛔ ระงับ' : '✅ ปลดระงับ' }}
                  </button>
                  <button 
                    @click="deleteUser(user)" 
                    class="px-3 py-1.5 rounded-lg text-sm text-red-400 hover:bg-red-500/20 transition-colors ml-2"
                  >
                    🗑️ ลบ
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Products Table -->
      <div v-if="activeTab === 'products'" class="card overflow-hidden">
        <div class="p-4 border-b border-white/10">
          <h2 class="text-lg font-semibold text-white">จัดการสินค้า</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-dark-800/50">
              <tr>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">สินค้า</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">ราคา</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">ผู้ขาย</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">วันที่เพิ่ม</th>
                <th class="text-right p-4 text-dark-400 text-sm font-medium">การจัดการ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in products" :key="product.id" class="border-b border-white/5 hover:bg-white/5">
                <td class="p-4">
                  <div class="flex items-center gap-3">
                    <img :src="product.image_url || '/placeholder.png'" class="w-12 h-12 rounded-lg object-cover" />
                    <p class="text-white font-medium">{{ product.name }}</p>
                  </div>
                </td>
                <td class="p-4 text-green-400 font-medium">฿{{ product.price.toLocaleString() }}</td>
                <td class="p-4 text-dark-300">{{ product.seller?.username }}</td>
                <td class="p-4 text-dark-400 text-sm">{{ product.created_at }}</td>
                <td class="p-4 text-right">
                  <button 
                    @click="deleteProduct(product)" 
                    class="px-3 py-1.5 rounded-lg text-sm text-red-400 hover:bg-red-500/20 transition-colors"
                  >
                    🗑️ ลบ
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Orders Table -->
      <div v-if="activeTab === 'orders'" class="card overflow-hidden">
        <div class="p-4 border-b border-white/10">
          <h2 class="text-lg font-semibold text-white">คำสั่งซื้อทั้งหมด</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-dark-800/50">
              <tr>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">Order ID</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">ผู้สั่ง</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">ยอดรวม</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">สถานะ</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">วันที่</th>
                <th class="text-right p-4 text-dark-400 text-sm font-medium">การจัดการ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id" class="border-b border-white/5 hover:bg-white/5">
                <td class="p-4 text-dark-300 font-mono text-sm">{{ order.id.slice(-8) }}</td>
                <td class="p-4 text-white">{{ order.user?.username }}</td>
                <td class="p-4 text-green-400 font-medium">฿{{ order.total_price.toLocaleString() }}</td>
                <td class="p-4">
                  <select 
                    v-model="order.status" 
                    @change="updateOrderStatus(order)"
                    class="input-glass text-sm py-1 px-2"
                  >
                    <option value="pending">รอดำเนินการ</option>
                    <option value="processing">กำลังดำเนินการ</option>
                    <option value="completed">สำเร็จ</option>
                    <option value="cancelled">ยกเลิก</option>
                  </select>
                </td>
                <td class="p-4 text-dark-400 text-sm">{{ order.created_at }}</td>
                <td class="p-4 text-right">
                  <button class="px-3 py-1.5 rounded-lg text-sm text-primary-400 hover:bg-primary-500/20 transition-colors">
                    👁️ ดูรายละเอียด
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Token Requests Table -->
      <div v-if="activeTab === 'tokens'" class="card overflow-hidden">
        <div class="p-4 border-b border-white/10 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-white">คำขอเติม Token</h2>
          <div class="flex gap-2">
            <span class="badge badge-warning">{{ tokenStats.pending || 0 }} รอตรวจสอบ</span>
          </div>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-dark-800/50">
              <tr>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">ผู้ใช้</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">จำนวน Token</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">สถานะ</th>
                <th class="text-left p-4 text-dark-400 text-sm font-medium">วันที่</th>
                <th class="text-right p-4 text-dark-400 text-sm font-medium">การจัดการ</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="req in tokenRequests" :key="req.id" class="border-b border-white/5 hover:bg-white/5">
                <td class="p-4">
                  <div class="flex items-center gap-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-yellow-500 to-orange-500 flex items-center justify-center text-white font-bold">
                      {{ req.user?.username?.charAt(0).toUpperCase() }}
                    </div>
                    <div>
                      <p class="text-white font-medium">{{ req.user?.username }}</p>
                      <p class="text-dark-500 text-xs">{{ req.user?.email }}</p>
                    </div>
                  </div>
                </td>
                <td class="p-4 text-primary-400 font-bold text-lg">🪙 {{ req.amount?.toLocaleString() }}</td>
                <td class="p-4">
                  <span 
                    class="badge"
                    :class="{
                      'bg-yellow-500/20 text-yellow-400': req.status === 'pending',
                      'bg-green-500/20 text-green-400': req.status === 'approved',
                      'bg-red-500/20 text-red-400': req.status === 'rejected'
                    }"
                  >
                    {{ req.status === 'pending' ? '⏳ รอตรวจสอบ' : req.status === 'approved' ? '✅ อนุมัติแล้ว' : '❌ ปฏิเสธ' }}
                  </span>
                </td>
                <td class="p-4 text-dark-400 text-sm">{{ req.created_at }}</td>
                <td class="p-4 text-right">
                  <div v-if="req.status === 'pending'" class="flex gap-2 justify-end">
                    <button 
                      @click="approveToken(req)" 
                      class="px-3 py-1.5 rounded-lg text-sm bg-green-500/20 text-green-400 hover:bg-green-500/30 transition-colors"
                    >
                      ✅ อนุมัติ
                    </button>
                    <button 
                      @click="rejectToken(req)" 
                      class="px-3 py-1.5 rounded-lg text-sm bg-red-500/20 text-red-400 hover:bg-red-500/30 transition-colors"
                    >
                      ❌ ปฏิเสธ
                    </button>
                  </div>
                  <span v-else class="text-dark-500 text-sm">{{ req.admin_note || 'ดำเนินการแล้ว' }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const adminUser = ref(null);
const stats = ref({});
const users = ref([]);
const products = ref([]);
const orders = ref([]);
const tokenRequests = ref([]);
const tokenStats = ref({});
const activeTab = ref('users');

const tabs = [
  { id: 'users', name: 'ผู้ใช้', icon: '👥' },
  { id: 'products', name: 'สินค้า', icon: '📦' },
  { id: 'orders', name: 'คำสั่งซื้อ', icon: '🛒' },
  { id: 'tokens', name: 'คำขอ Token', icon: '🪙' },
];

const baseUrl = 'http://localhost:5000';

async function fetchData() {
  const token = localStorage.getItem('admin_token');
  if (!token) {
    router.push('/admin-login');
    return;
  }

  const headers = { Authorization: `Bearer ${token}` };

  try {
    const [statsRes, usersRes, productsRes, ordersRes] = await Promise.all([
      axios.get(`${baseUrl}/api/admin/stats`, { headers }),
      axios.get(`${baseUrl}/api/admin/users`, { headers }),
      axios.get(`${baseUrl}/api/admin/products`, { headers }),
      axios.get(`${baseUrl}/api/admin/orders`, { headers }),
    ]);

    stats.value = statsRes.data;
    users.value = usersRes.data;
    products.value = productsRes.data;
    orders.value = ordersRes.data;
    
    // Fetch token requests separately
    fetchTokenRequests();
  } catch (err) {
    console.error('Failed to fetch admin data:', err);
    if (err.response?.status === 401 || err.response?.status === 403) {
      router.push('/admin-login');
    }
  }
}

async function toggleBanUser(user) {
  const token = localStorage.getItem('admin_token');
  try {
    const res = await axios.put(`${baseUrl}/api/admin/users/${user.id}/toggle-ban`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    user.is_active = res.data.is_active;
  } catch (err) {
    console.error('Failed to toggle ban:', err);
  }
}

async function deleteUser(user) {
  if (!confirm(`ยืนยันการลบผู้ใช้ ${user.username}?`)) return;
  
  const token = localStorage.getItem('admin_token');
  try {
    await axios.delete(`${baseUrl}/api/admin/users/${user.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    users.value = users.value.filter(u => u.id !== user.id);
  } catch (err) {
    console.error('Failed to delete user:', err);
  }
}

async function deleteProduct(product) {
  if (!confirm(`ยืนยันการลบสินค้า ${product.name}?`)) return;
  
  const token = localStorage.getItem('admin_token');
  try {
    await axios.delete(`${baseUrl}/api/admin/products/${product.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    products.value = products.value.filter(p => p.id !== product.id);
  } catch (err) {
    console.error('Failed to delete product:', err);
  }
}

async function updateOrderStatus(order) {
  const token = localStorage.getItem('admin_token');
  try {
    await axios.put(`${baseUrl}/api/admin/orders/${order.id}/status`, 
      { status: order.status },
      { headers: { Authorization: `Bearer ${token}` } }
    );
  } catch (err) {
    console.error('Failed to update order status:', err);
  }
}

function handleLogout() {
  localStorage.removeItem('admin_token');
  localStorage.removeItem('admin_user');
  router.push('/admin-login');
}

async function fetchTokenRequests() {
  const token = localStorage.getItem('admin_token');
  if (!token) return;
  
  try {
    const [requestsRes, statsRes] = await Promise.all([
      axios.get(`${baseUrl}/api/admin/token-requests`, {
        headers: { Authorization: `Bearer ${token}` }
      }),
      axios.get(`${baseUrl}/api/admin/token-stats`, {
        headers: { Authorization: `Bearer ${token}` }
      })
    ]);
    tokenRequests.value = requestsRes.data.requests || [];
    tokenStats.value = statsRes.data || {};
  } catch (err) {
    console.error('Failed to fetch token requests:', err);
  }
}

async function approveToken(req) {
  if (!confirm(`อนุมัติ ${req.amount.toLocaleString()} Token ให้ ${req.user?.username}?`)) return;
  
  const token = localStorage.getItem('admin_token');
  try {
    await axios.put(`${baseUrl}/api/admin/token-requests/${req.id}/approve`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert(`✅ อนุมัติ ${req.amount.toLocaleString()} Token ให้ ${req.user?.username} สำเร็จ!`);
    fetchTokenRequests();
  } catch (err) {
    alert(err.response?.data?.msg || 'อนุมัติไม่สำเร็จ');
  }
}

async function rejectToken(req) {
  const reason = prompt('ระบุเหตุผลในการปฏิเสธ (ถ้ามี):', '');
  if (reason === null) return; // Cancelled
  
  const token = localStorage.getItem('admin_token');
  try {
    await axios.put(`${baseUrl}/api/admin/token-requests/${req.id}/reject`, {
      admin_note: reason || 'ไม่ผ่านการตรวจสอบ'
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert(`❌ ปฏิเสธคำขอของ ${req.user?.username} แล้ว`);
    fetchTokenRequests();
  } catch (err) {
    alert(err.response?.data?.msg || 'ปฏิเสธไม่สำเร็จ');
  }
}

onMounted(() => {
  const storedAdmin = localStorage.getItem('admin_user');
  if (storedAdmin) {
    adminUser.value = JSON.parse(storedAdmin);
  }
  fetchData();
});
</script>

<style scoped>
.badge-warning {
  background-color: rgba(234, 179, 8, 0.2);
  color: #facc15;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.875rem;
}
</style>
