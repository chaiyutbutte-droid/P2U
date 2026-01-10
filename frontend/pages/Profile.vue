<template>
  <div class="p-6 md:pl-32 max-w-8xl mx-auto bg-black text-white mt-1 mb-1 mr-1 transition-all duration-300 min-h-screen">
    
    <div class="md:w-full space-y-5"> 
      <div class="flex items-center mb-6 relative">
        <h1 class="text-3xl font-extrabold text-center">
          My <span class="text-pink-600">Profile</span>
        </h1>
      </div>
    </div>

    <div>
      <sidebar />
    </div>

    <div v-if="user" class="flex flex-col md:flex-row md:space-x-8 space-y-8 md:space-y-0">
      <div class="md:w-1/3 space-y-5"> 
        <div class="flex items-center space-x-6">
          <div class="relative w-28 h-28 shrink-0">
            <img :src="getFullImageUrl(user.profile_image_url) || defaultProfile" alt="Profile"
              class="w-full h-full rounded-full border-4 border-pink-500 object-cover shadow-md" />
            <button @click="triggerFileInput"
              class="absolute bottom-0 right-0 bg-pink-600 hover:bg-pink-700 p-1.5 rounded-full shadow-md transition">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5h6m2 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2h10zM16 3l-1-1m0 0L9 8m7-6v6H9" />
              </svg>
            </button>
            <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange" />
          </div>
          <div class="space-y-2 text-sm">
            <p><span class="font-semibold text-pink-400">{{ t('username') }}:</span> {{ user.username }}</p>
            <p><span class="font-semibold text-pink-400">{{ t('fullName') }}:</span> {{ user.full_name }}</p>
            <p><span class="font-semibold text-pink-400">{{ t('email') }}:</span> {{ user.email }}</p>
            <p><span class="font-semibold text-pink-400">{{ t('phone') }}:</span> {{ user.phone_number }}</p>
          </div>
        </div>
        
        <div class="flex items-center space-x-2 mt-4 text-sm">
          <span class="font-semibold text-pink-400">{{ t('seller') }}:</span>
          <span>{{ user.is_seller ? t('registered') : t('notRegistered') }}</span>
          <button v-if="user.is_seller" @click="router.push('/seller')"
            class="px-2 py-1 bg-pink-600 hover:bg-pink-700 text-white text-xs font-semibold rounded-lg transition">
            Go to Seller Page
          </button>
          <button v-else @click="router.push('/Registerseller')"
            class="px-2 py-1 bg-pink-600 hover:bg-pink-700 text-white text-xs font-semibold rounded-lg transition">
            Register as Seller
          </button>
        </div>

        <div class="mt-6">
          <button @click="router.push('/ai')"
            class="w-full bg-pink-600 hover:bg-pink-700 text-white font-semibold py-2 rounded-lg transition">
            ไปยังหน้า AI
          </button>
        </div>

        <div class="w-full mt-8">
          <h2 class="text-xl font-semibold mb-4 border-b border-gray-700 pb-2">{{ t('addresses') }}</h2>
          <div v-if="user.addresses && user.addresses.length" class="space-y-4">
            <div v-for="(addr, index) in user.addresses" :key="index"
              class="bg-gray-800 rounded-lg p-4 shadow-inner relative border border-white/5">
              <div class="flex items-center justify-between">
                <h3 class="text-sm font-semibold mb-3 border-b border-gray-700 pb-2 text-pink-300">
                  {{ addr.is_default ? 'Default Address' : 'Address ' + (index + 1) }}
                </h3>
                <span v-if="addr.is_default"
                  class="bg-green-500 text-white text-xs font-semibold px-2 py-1 rounded-full shadow-sm">Default</span>
              </div>
              <div class="text-xs space-y-1">
                <p><span class="font-semibold text-pink-400">Name:</span> {{ addr.name }}</p>
                <p><span class="font-semibold text-pink-400">Phone:</span> {{ addr.phone }}</p>
                <p><span class="font-semibold text-pink-400">Address:</span> {{ addr.address_line }}, {{ addr.district }}, {{ addr.province }}, {{ addr.postal_code }}</p>
              </div>
              <div class="mt-2 flex gap-2">
                <button @click="editAddress(index)" class="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-[10px] rounded transition">{{ t('editAddress') }}</button>
                <button @click="deleteAddress(index)" class="px-3 py-1 bg-red-600 hover:bg-red-700 text-white text-[10px] rounded transition">Delete</button>
              </div>
            </div>
          </div>
          <div class="mt-6 bg-gray-800 rounded-lg p-5 shadow-inner border border-white/5">
            <h3 class="text-sm font-semibold mb-3 border-b border-gray-700 pb-2">{{ isEditing ? t('editAddress') : t('addNewAddress') }}</h3>
            <form @submit.prevent="addOrUpdateAddress">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <input v-model="newAddress.name" :placeholder="t('fullName')" type="text" class="bg-gray-700 text-white p-2 rounded w-full text-xs outline-none focus:ring-1 focus:ring-pink-500" required />
                <input v-model="newAddress.phone" :placeholder="t('phone')" type="text" class="bg-gray-700 text-white p-2 rounded w-full text-xs outline-none focus:ring-1 focus:ring-pink-500" required />
                <input v-model="newAddress.address_line" placeholder="Address Line" type="text" class="bg-gray-700 text-white p-2 rounded w-full text-xs outline-none focus:ring-1 focus:ring-pink-500 col-span-2" required />
                <input v-model="newAddress.district" placeholder="District" type="text" class="bg-gray-700 text-white p-2 rounded w-full text-xs outline-none focus:ring-1 focus:ring-pink-500" required />
                <input v-model="newAddress.province" placeholder="Province" type="text" class="bg-gray-700 text-white p-2 rounded w-full text-xs outline-none focus:ring-1 focus:ring-pink-500" required />
                <input v-model="newAddress.postal_code" placeholder="Postal Code" type="text" class="bg-gray-700 text-white p-2 rounded w-full text-xs outline-none focus:ring-1 focus:ring-pink-500" required />
              </div>
              <div class="flex items-center mt-4">
                <input v-model="newAddress.is_default" type="checkbox" id="is_default" class="mr-2 accent-pink-500" />
                <label for="is_default" class="text-[10px]">Set as default address</label>
              </div>
              <button type="submit" class="mt-4 w-full bg-pink-600 hover:bg-pink-700 text-white font-semibold py-2 rounded-lg text-xs transition shadow-md shadow-pink-600/20">{{ isEditing ? t('updateAddress') : t('addAddress') }}</button>
              <button v-if="isEditing" @click="cancelEdit" type="button" class="mt-2 w-full bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 rounded-lg text-xs transition">{{ t('cancel') }}</button>
            </form>
          </div>
        </div>
      </div>

      <div class="md:w-2/3 space-y-6">
        <div class="flex items-center justify-between border-b border-gray-700 pb-2">
          <h2 class="text-xl font-semibold">🚚 รายการที่กำลังจัดส่ง ✨</h2>
          <button @click="router.push('/orders')" class="text-pink-400 text-xs hover:underline">ดูประวัติทั้งหมด</button>
        </div>
        
        <div v-if="orders && orders.length > 0" class="grid grid-cols-1 gap-4">
          <div v-for="order in orders" :key="order._id" @click="router.push('/orders')"
            class="bg-gray-800/40 backdrop-blur-md rounded-2xl p-5 border border-white/5 hover:border-pink-500/30 transition-all cursor-pointer group shadow-lg">
            <div class="flex justify-between items-start mb-4">
              <div class="space-y-1">
                <p class="text-[10px] text-gray-500 uppercase tracking-widest font-bold">Order ID</p>
                <p class="text-white font-mono text-xs group-hover:text-pink-300 transition-colors">#{{ order._id.slice(-8) }}</p>
              </div>
              <span :class="getStatusClass(order.status)" class="px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-tight shadow-sm border">
                 {{ getStatusLabel(order.status) }}
              </span>
            </div>
            <div class="flex items-center gap-3 mb-4 overflow-x-auto no-scrollbar py-1">
              <div v-for="(item, idx) in order.items" :key="idx" class="relative shrink-0">
                <img :src="getFullImageUrl(item.product?.image_url)" class="w-14 h-14 rounded-xl object-cover border border-white/10 shadow-md" @error="(e) => e.target.src = 'https://via.placeholder.com/150?text=Product'" />
                <span v-if="item.quantity > 1" class="absolute -top-2 -right-2 bg-pink-600 text-white text-[9px] font-black w-5 h-5 flex items-center justify-center rounded-full border-2 border-gray-800">{{ item.quantity }}</span>
              </div>
            </div>
            <div class="flex items-center justify-between pt-4 border-t border-white/5">
              <div class="text-gray-400 text-[10px] flex items-center gap-1"><span class="opacity-50">📅</span> {{ formatDate(order.created_at) }}</div>
              <div class="text-right">
                <p class="text-[9px] text-gray-500 uppercase mb-0.5">ยอดสุทธิ</p>
                <p class="text-lg font-black text-pink-400">฿{{ order.total_price?.toLocaleString() }}</p>
              </div>
            </div>
          </div>
        </div>
        <div v-else class="bg-gray-800/30 rounded-2xl p-12 text-center border border-dashed border-gray-700">
          <p class="text-sm text-gray-400 italic">ไม่มีรายการที่กำลังจัดส่งในขณะนี้เพคะ</p>
        </div>

        <div class="flex items-center justify-between border-b border-gray-700 pb-2 mt-10">
          <h2 class="text-xl font-semibold">❤️ รายการโปรด (Wishlist)</h2>
          <button @click="router.push('/wishlist')" class="text-pink-400 text-xs hover:underline">จัดการทั้งหมด</button>
        </div>

        <div v-if="wishlistItems.length > 0" class="grid grid-cols-2 sm:grid-cols-3 gap-4">
          <div v-for="item in wishlistItems" :key="item.id"
            class="bg-gray-800/50 p-3 rounded-xl border border-white/5 hover:border-pink-500/30 transition-all group relative">
            
            <button @click="removeFromWishlist(item)" class="absolute top-2 right-2 z-10 bg-black/50 p-1.5 rounded-full text-pink-500 hover:bg-pink-600 hover:text-white transition shadow-sm">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="currentColor" viewBox="0 0 24 24"><path d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.5 3c1.263 0 2.426.466 3.322 1.234a4.876 4.876 0 013.356-1.234c2.786 0 5.25 2.322 5.25 5.25 0 3.924-2.438 7.11-4.74 9.273a25.27 25.27 0 01-4.244 3.17 15.237 15.237 0 01-.383.219l-.022.012-.007.004-.003.001z" /></svg>
            </button>

            <div @click="router.push(`/wishlist`)" class="cursor-pointer">
              <img :src="getFullImageUrl(item.image_url)" alt="product" class="w-full aspect-square object-cover rounded-lg shadow-md group-hover:scale-105 transition-transform duration-300" />
              <div class="mt-2">
                <p class="font-semibold text-white text-xs truncate">{{ item.name }}</p>
                <p class="font-bold text-pink-400 text-sm">฿{{ item.price?.toLocaleString() }}</p>
              </div>
            </div>
            
            <button @click="addToCart(item)" class="w-full mt-2 py-1.5 bg-pink-600 hover:bg-pink-700 text-[10px] font-bold rounded-lg transition-colors flex items-center justify-center gap-1">
              <span>ใส่ตะกร้า</span> 🛒
            </button>
          </div>
        </div>
        <div v-else class="text-gray-400 text-sm text-center py-12 bg-gray-800/30 rounded-2xl border border-dashed border-gray-700">
            🥀 ยังไม่มีรายการที่ถูกใจเลยเพคะ
        </div>

        <div class="pt-10 border-t border-gray-800">
           <button @click="handleLogout"
            class="w-full md:w-48 bg-gray-800 hover:bg-red-600/80 text-white font-semibold py-2 rounded-lg transition-all mx-auto block text-sm border border-white/5">
            Logout
          </button>
        </div>
      </div>
    </div>
    <div v-if="!user" class="text-center text-gray-400 mt-20 animate-pulse">Loading Profile...</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import sidebar from '~/components/sidebar.vue'

const router = useRouter()
const baseURL = 'http://localhost:5000'
const defaultProfile = '/guest-profile.png'
const defaultImage = '/default-item.svg'

const user = ref(null)
const orders = ref([]) 
const wishlistItems = ref([])
const fileInput = ref(null)
let selectedFile = null

// URL Formatter
const getFullImageUrl = (path) => {
  if (!path) return null
  if (path.startsWith('http')) return path
  return `${baseURL}${path}`
}

// Logic: Wishlist (ดึงจาก API เหมือนหน้า Wishlist หลัก)
const fetchWishlist = async () => {
  const token = localStorage.getItem('token');
  if (!token) return;
  try {
    const res = await axios.get(`${baseURL}/api/wishlist`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = res.data.wishlist || [];
    wishlistItems.value = data.map(p => ({
      ...p,
      id: p.id || p._id,
      price: parseFloat(p.price) || 0,
      image_url: p.image_url
    })).slice(0, 6); // แสดงแค่ 6 รายการในหน้า Profile
  } catch (err) {
    console.error('Failed to fetch wishlist:', err);
  }
};

const removeFromWishlist = async (product) => {
  const token = localStorage.getItem('token');
  try {
    await axios.delete(`${baseURL}/api/wishlist/${product.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    wishlistItems.value = wishlistItems.value.filter(p => p.id !== product.id);
  } catch (err) {
    console.error('Error removing:', err);
  }
};

const addToCart = (product) => {
  if (!process.client) return;
  const cart = JSON.parse(localStorage.getItem("cart") || "[]");
  const existing = cart.find((item) => item.id === product.id);
  if (existing) existing.quantity++;
  else cart.push({ ...product, quantity: 1 });
  localStorage.setItem("cart", JSON.stringify(cart));
  window.dispatchEvent(new Event('storage'));
  alert(`เพิ่ม ${product.name} ลงตะกร้าแล้ว!`);
};

// Logic: Orders & Status
const getStatusLabel = (status) => {
  const labels = { 
    pending: 'รอตรวจสอบ', 
    paid: 'เตรียมการจัดส่ง 📦', 
    processing: 'สินค้ากำลังเดินทาง 🚚', 
    completed: 'สำเร็จ ✅', 
    cancelled: 'ยกเลิกแล้ว ❌' 
  };
  return labels[status] || status;
}
const getStatusClass = (status) => {
  const base = "bg-opacity-10 "
  if (status === 'pending') return base + "bg-yellow-500 text-yellow-500 border-yellow-500/20"
  if (status === 'paid') return base + "bg-pink-500 text-pink-500 border-pink-500/20"
  if (status === 'processing') return base + "bg-blue-500 text-blue-500 border-blue-500/20"
  if (status === 'completed') return base + "bg-green-500 text-green-500 border-green-500/20"
  return base + "bg-gray-500 text-gray-400 border-gray-500/20"
}
const formatDate = (dateStr) => {
  if (!dateStr) return "N/A"
  return new Date(dateStr).toLocaleDateString('th-TH', { day: 'numeric', month: 'short', year: '2-digit', hour: '2-digit', minute: '2-digit' })
}

// แก้ไขฟังก์ชันนี้ให้กรองเฉพาะสินค้าที่กำลังส่ง
const fetchMyOrders = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    const res = await axios.get(`${baseURL}/api/orders/my-orders`, { 
      headers: { Authorization: `Bearer ${token}` } 
    })
    
    const allOrders = Array.isArray(res.data) ? res.data : []
    
    // กำหนดสถานะที่ถือว่า "กำลังจัดส่ง" (ชำระแล้วเตรียมส่ง หรือ กำลังส่งอยู่บนรถ)
    const shippingStatuses = ['processing', 'paid']
    
    // กรองและเรียงลำดับจากใหม่สุดไปเก่าสุด
    orders.value = allOrders
      .filter(order => shippingStatuses.includes(order.status))
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      .slice(0, 5) // แสดงหน้าละ 5 รายการที่กำลังส่ง
      
  } catch (err) { 
    console.error("Fetch orders failed:", err) 
  }
}

// Logic: Address Management
const newAddress = ref({ name: '', phone: '', address_line: '', district: '', province: '', postal_code: '', is_default: false })
const isEditing = ref(false)
const editingIndex = ref(null)

const addOrUpdateAddress = async () => {
  try {
    const token = localStorage.getItem('token')
    const endpoint = isEditing.value ? `${baseURL}/api/profile/address/${editingIndex.value}` : `${baseURL}/api/profile/address`
    const method = isEditing.value ? 'put' : 'post'
    const res = await axios({ method, url: endpoint, data: newAddress.value, headers: { Authorization: `Bearer ${token}` } })
    user.value.addresses = res.data.addresses
    resetForm()
  } catch (err) { console.error(err) }
}

const editAddress = (i) => { 
  newAddress.value = { ...user.value.addresses[i] }; isEditing.value = true; editingIndex.value = i 
}

const deleteAddress = async (i) => {
  if (confirm('คุณต้องการลบที่อยู่นี้ใช่หรือไม่?')) {
    try {
      const token = localStorage.getItem('token')
      const res = await axios.delete(`${baseURL}/api/profile/address/${i}`, { headers: { Authorization: `Bearer ${token}` } })
      user.value.addresses = res.data.addresses
    } catch (err) { console.error(err) }
  }
}

const resetForm = () => { 
  newAddress.value = { name: '', phone: '', address_line: '', district: '', province: '', postal_code: '', is_default: false }
  isEditing.value = false; editingIndex.value = null 
}
const cancelEdit = () => resetForm()

// Logic: Profile Image
const triggerFileInput = () => fileInput.value.click()
const onFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return
  selectedFile = file
  uploadConfirmed() 
}
const uploadConfirmed = async () => {
  if (!selectedFile) return
  const formData = new FormData()
  formData.append('profile_image', selectedFile)
  try {
    const token = localStorage.getItem('token')
    const res = await axios.put(baseURL + '/api/profile/image', formData, { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' } })
    user.value.profile_image_url = res.data.profile_image_url
    window.dispatchEvent(new Event('user-updated'))
  } catch (err) { console.error(err); } finally { selectedFile = null }
}

const handleLogout = () => {
  localStorage.clear(); router.push('/login'); window.dispatchEvent(new Event('user-updated'))
}

// Translations
const currentLanguage = ref('th')
const t = (key) => {
  const trans = {
    th: { username: 'ชื่อผู้ใช้', fullName: 'ชื่อเต็ม', email: 'อีเมล', phone: 'เบอร์โทร', seller: 'ผู้ขาย', registered: 'ลงทะเบียนแล้ว', notRegistered: 'ยังไม่ลงทะเบียน', addresses: 'ที่อยู่', addNewAddress: 'เพิ่มที่อยู่ใหม่', editAddress: 'แก้ไขที่อยู่', addAddress: 'เพิ่มที่อยู่', updateAddress: 'อัปเดตที่อยู่', cancel: 'ยกเลิก' },
    en: { username: 'Username', fullName: 'Full Name', email: 'Email', phone: 'Phone', seller: 'Seller', registered: 'Registered', notRegistered: 'Not Registered', addresses: 'Addresses', addNewAddress: 'Add New Address', editAddress: 'Edit Address', addAddress: 'Add Address', updateAddress: 'Update Address', cancel: 'Cancel' }
  }
  return trans[currentLanguage.value][key] || key
}

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) { router.push('/login'); return }
    const res = await axios.get(baseURL + '/api/profile', { headers: { Authorization: `Bearer ${token}` } })
    user.value = res.data
    fetchMyOrders()
    fetchWishlist()
  } catch (e) { console.error(e); router.push('/login') }
})
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar { display: none; }
.no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
</style>