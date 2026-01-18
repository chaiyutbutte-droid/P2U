<template>
  <div class="min-h-screen bg-[#050505] text-gray-100 font-sans selection:bg-pink-500/30 relative overflow-hidden">
    
    <div class="fixed top-0 left-0 w-[500px] h-[500px] bg-pink-600/10 blur-[150px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[500px] h-[500px] bg-purple-900/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

    <sidebar class="fixed left-0 top-0 h-full z-50" />

    <main class="ml-20 relative z-10 p-6 md:p-10 min-h-screen">
      
      <header class="mb-10 flex flex-col md:flex-row items-start md:items-end justify-between gap-4">
        <div>
          <h1 class="text-4xl md:text-5xl font-black text-white tracking-tight mb-2">
            My <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-500">Profile</span>
          </h1>
          <p class="text-gray-400 text-sm">จัดการข้อมูลส่วนตัว สถานะคำสั่งซื้อ และรายการโปรดของคุณ</p>
        </div>
        
        <button @click="handleLogout"
          class="group flex items-center gap-2 px-5 py-2.5 bg-[#1a1a1a] hover:bg-red-500/10 border border-white/5 hover:border-red-500/50 rounded-full transition-all duration-300">
          <span class="text-sm font-semibold text-gray-300 group-hover:text-red-400">Logout</span>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-500 group-hover:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
          </svg>
        </button>
      </header>

      <div v-if="user" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        <div class="lg:col-span-4 space-y-6">
          
          <div class="relative bg-[#121212]/80 backdrop-blur-xl border border-white/10 rounded-[2rem] p-8 shadow-2xl overflow-hidden group">
            <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-pink-500 via-purple-500 to-pink-500"></div>
            
            <div class="flex flex-col items-center text-center">
              <div class="relative w-32 h-32 mb-6 group-hover:scale-105 transition-transform duration-500">
                <div class="absolute inset-0 bg-gradient-to-tr from-pink-500 to-purple-600 rounded-full blur opacity-40 group-hover:opacity-60 transition-opacity"></div>
                
                <img :src="userProfileImage" alt="Profile"
                  class="relative w-full h-full rounded-full border-4 border-[#121212] object-cover shadow-lg bg-[#121212]" />
                
                <button @click="triggerFileInput"
                  class="absolute bottom-1 right-1 bg-white text-pink-600 p-2 rounded-full shadow-lg hover:bg-gray-100 transition-colors z-10 transform hover:scale-110 active:scale-95">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </button>
                <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange" />
              </div>

              <h2 class="text-2xl font-bold text-white mb-1">{{ user.full_name }}</h2>
              <p class="text-pink-500 font-medium mb-4">@{{ user.username }}</p>

              <div class="w-full space-y-3 bg-white/5 rounded-xl p-4 text-sm border border-white/5 mb-6">
                <div class="flex justify-between border-b border-white/5 pb-2">
                  <span class="text-gray-500">{{ t('email') }}</span>
                  <span class="text-gray-200 truncate max-w-[150px]">{{ user.email }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">{{ t('phone') }}</span>
                  <span class="text-gray-200">{{ user.phone_number }}</span>
                </div>
              </div>

              <div class="w-full grid grid-cols-2 gap-3">
                <button @click="handleSellerAction"
                  :class="sellerButtonClass"
                  class="py-2.5 rounded-xl text-xs font-bold transition-all border shadow-lg flex items-center justify-center gap-1">
                  {{ sellerButtonText }}
                </button>
                
                <button @click="router.push('/ai')"
                  class="py-2.5 rounded-xl text-xs font-bold transition-all bg-gradient-to-r from-purple-600 to-pink-600 hover:to-pink-500 text-white shadow-lg shadow-purple-900/20">
                  🤖 ระบบ AI
                </button>
              </div>
              
              <div v-if="user.verification_status === 'REJECTED'" class="mt-3 text-[10px] text-red-400 bg-red-500/10 p-2 rounded-lg border border-red-500/20 w-full">
                 ⚠️ การสมัครครั้งก่อนถูกปฏิเสธ กรุณาสมัครใหม่
              </div>

            </div>
          </div>

          <div class="bg-[#121212]/80 backdrop-blur-md border border-white/5 rounded-[2rem] p-6 shadow-xl">
            <h3 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
              📍 {{ t('addresses') }}
            </h3>

            <div v-if="user.addresses && user.addresses.length" class="space-y-3 max-h-60 overflow-y-auto custom-scrollbar mb-6 pr-1">
              <div v-for="(addr, index) in user.addresses" :key="index"
                class="bg-white/5 rounded-xl p-3 border border-white/5 hover:border-pink-500/30 transition-colors relative group">
                <div class="flex justify-between items-start mb-1">
                  <span class="text-xs font-bold text-gray-300">{{ addr.name }}</span>
                  <span v-if="addr.is_default" class="text-[10px] bg-green-500/20 text-green-400 px-2 py-0.5 rounded-full border border-green-500/30">Default</span>
                </div>
                <p class="text-[11px] text-gray-500 leading-relaxed">
                  {{ addr.address_line }} {{ addr.district }} {{ addr.province }} {{ addr.postal_code }}
                </p>
                <div class="flex gap-2 mt-2 opacity-0 group-hover:opacity-100 transition-opacity justify-end">
                   <button @click="editAddress(index)" class="text-[10px] text-blue-400 hover:underline">Edit</button>
                   <button @click="deleteAddress(index)" class="text-[10px] text-red-400 hover:underline">Delete</button>
                </div>
              </div>
            </div>

            <div class="pt-4 border-t border-white/10">
              <p class="text-xs font-semibold text-gray-400 mb-3">{{ isEditing ? t('editAddress') : t('addNewAddress') }}</p>
              <form @submit.prevent="addOrUpdateAddress" class="space-y-2">
                <div class="grid grid-cols-2 gap-2">
                  <input v-model="newAddress.name" :placeholder="t('fullName')" 
                    class="bg-[#0b0b0f] border border-gray-700 text-white p-2.5 rounded-lg text-xs outline-none focus:border-pink-500 focus:ring-1 focus:ring-pink-500 transition-all w-full" required />
                  <input v-model="newAddress.phone" :placeholder="t('phone')" 
                    class="bg-[#0b0b0f] border border-gray-700 text-white p-2.5 rounded-lg text-xs outline-none focus:border-pink-500 focus:ring-1 focus:ring-pink-500 transition-all w-full" required />
                </div>
                <input v-model="newAddress.address_line" placeholder="Address / No. / Soi" 
                  class="bg-[#0b0b0f] border border-gray-700 text-white p-2.5 rounded-lg text-xs outline-none focus:border-pink-500 focus:ring-1 focus:ring-pink-500 transition-all w-full" required />
                <div class="grid grid-cols-3 gap-2">
                   <input v-model="newAddress.district" placeholder="District" 
                   class="bg-[#0b0b0f] border border-gray-700 text-white p-2.5 rounded-lg text-xs outline-none focus:border-pink-500 focus:ring-1 focus:ring-pink-500 transition-all w-full" required />
                   <input v-model="newAddress.province" placeholder="Province" 
                   class="bg-[#0b0b0f] border border-gray-700 text-white p-2.5 rounded-lg text-xs outline-none focus:border-pink-500 focus:ring-1 focus:ring-pink-500 transition-all w-full" required />
                   <input v-model="newAddress.postal_code" placeholder="Zip" 
                   class="bg-[#0b0b0f] border border-gray-700 text-white p-2.5 rounded-lg text-xs outline-none focus:border-pink-500 focus:ring-1 focus:ring-pink-500 transition-all w-full" required />
                </div>
                
                <div class="flex items-center gap-2 mt-2">
                  <input v-model="newAddress.is_default" type="checkbox" id="def" class="rounded border-gray-600 bg-gray-700 text-pink-500 focus:ring-pink-500/30" />
                  <label for="def" class="text-xs text-gray-400">Set as Default</label>
                </div>

                <div class="flex gap-2 mt-3">
                  <button type="submit" class="flex-1 py-2 bg-pink-600 hover:bg-pink-500 text-white text-xs font-bold rounded-lg transition shadow-lg shadow-pink-900/20">
                    {{ isEditing ? 'Update' : 'Add Address' }}
                  </button>
                  <button v-if="isEditing" @click="cancelEdit" type="button" class="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white text-xs rounded-lg transition">Cancel</button>
                </div>
              </form>
            </div>
          </div>
        </div>

        <div class="lg:col-span-8 space-y-8">
          
          <div>
             <div class="flex items-center justify-between mb-4">
              <h2 class="text-xl font-bold text-white flex items-center gap-2">
                🚚 <span class="bg-clip-text text-transparent bg-gradient-to-r from-white to-gray-400">สถานะการจัดส่ง</span>
              </h2>
              <button @click="router.push('/orders')" class="text-xs text-pink-400 hover:text-pink-300 transition-colors">ดูประวัติทั้งหมด →</button>
            </div>

            <div v-if="orders && orders.length > 0" class="grid grid-cols-1 gap-4">
              <div v-for="order in orders" :key="order._id" @click="router.push('/orders')"
                class="bg-[#1a1a1e] hover:bg-[#202025] rounded-2xl p-5 border border-white/5 hover:border-pink-500/50 transition-all cursor-pointer group shadow-lg relative overflow-hidden">
                
                <div class="absolute right-0 top-0 w-32 h-32 bg-pink-500/5 blur-[60px] rounded-full group-hover:bg-pink-500/10 transition-all"></div>

                <div class="relative z-10">
                  <div class="flex justify-between items-start mb-4">
                    <div class="flex items-center gap-3">
                      <div class="w-10 h-10 rounded-full bg-pink-500/10 flex items-center justify-center text-lg">📦</div>
                      <div>
                        <p class="text-white font-bold text-sm">Order #{{ order._id.slice(-6) }}</p>
                        <p class="text-xs text-gray-500">{{ formatDate(order.created_at) }}</p>
                      </div>
                    </div>
                    <span :class="getStatusClass(order.status)" class="px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-wider border backdrop-blur-md shadow-sm">
                      {{ getStatusLabel(order.status) }}
                    </span>
                  </div>

                  <div class="bg-black/20 rounded-xl p-3 flex items-center justify-between">
                    <div class="flex -space-x-3 overflow-hidden pl-1">
                      <div v-for="(item, idx) in order.items.slice(0, 4)" :key="idx" class="relative hover:z-10 transition-all hover:scale-110">
                          <img :src="getFullImageUrl(item.product?.image_url)" class="w-10 h-10 rounded-full object-cover border-2 border-[#1a1a1e]" @error="(e) => e.target.src = defaultImage" />
                      </div>
                      <div v-if="order.items.length > 4" class="w-10 h-10 rounded-full bg-gray-800 border-2 border-[#1a1a1e] flex items-center justify-center text-[10px] text-gray-400 font-bold z-10">
                        +{{ order.items.length - 4 }}
                      </div>
                    </div>
                    <div class="text-right">
                        <p class="text-[10px] text-gray-500">Total Amount</p>
                        <p class="text-lg font-black text-pink-500">฿{{ order.total_price?.toLocaleString() }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="bg-[#121212]/50 border border-white/5 border-dashed rounded-2xl p-10 text-center">
              <div class="text-4xl mb-3 opacity-30">📪</div>
              <p class="text-gray-500 text-sm">ไม่มีรายการที่กำลังจัดส่งในขณะนี้</p>
            </div>
          </div>

          <div>
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-xl font-bold text-white flex items-center gap-2">
                ❤️ <span class="bg-clip-text text-transparent bg-gradient-to-r from-pink-400 to-rose-400">รายการโปรด</span>
              </h2>
              <button @click="router.push('/wishlist')" class="text-xs text-pink-400 hover:text-pink-300 transition-colors">จัดการทั้งหมด →</button>
            </div>

            <div v-if="wishlistItems.length > 0" class="grid grid-cols-2 sm:grid-cols-3 xl:grid-cols-4 gap-4">
              <div v-for="item in wishlistItems" :key="item.id"
                class="bg-[#1a1a1e] rounded-xl p-3 border border-white/5 hover:border-pink-500/30 transition-all group relative">
                
                <button @click.stop="removeFromWishlist(item)" class="absolute top-2 right-2 z-20 w-7 h-7 bg-black/60 backdrop-blur rounded-full flex items-center justify-center text-gray-400 hover:text-red-500 hover:bg-white transition-all opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                  </svg>
                </button>

                <div @click="router.push('/wishlist')" class="cursor-pointer overflow-hidden rounded-lg relative aspect-square mb-3">
                  <div class="absolute inset-0 bg-black/20 group-hover:bg-transparent transition-colors z-10"></div>
                  <img :src="getFullImageUrl(item.image_url)" alt="product" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500" />
                </div>

                <div class="space-y-1">
                  <p class="font-medium text-gray-200 text-xs truncate">{{ item.name }}</p>
                  <div class="flex items-center justify-between">
                      <p class="font-bold text-pink-400 text-sm">฿{{ item.price?.toLocaleString() }}</p>
                      <button @click="addToCart(item)" class="text-[10px] bg-white/10 hover:bg-pink-600 hover:text-white px-2 py-1 rounded transition">
                        🛒 Add
                      </button>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-center py-12 bg-[#121212]/50 rounded-2xl border border-white/5 border-dashed">
               <p class="text-gray-500 text-sm">🥀 ยังไม่มีรายการที่ถูกใจ</p>
               <button @click="router.push('/')" class="mt-4 text-xs text-pink-400 border border-pink-500/30 px-4 py-2 rounded-full hover:bg-pink-500/10 transition">ไปเลือกซื้อสินค้า</button>
            </div>
          </div>

        </div>
      </div>

      <div v-if="!user" class="flex flex-col items-center justify-center min-h-[50vh] animate-pulse">
        <div class="w-16 h-16 rounded-full bg-white/5 mb-4"></div>
        <div class="h-4 w-32 bg-white/5 rounded mb-2"></div>
        <p class="text-gray-500 text-xs">Loading Profile...</p>
      </div>

      <div v-if="showCropper" class="fixed inset-0 z-[100] bg-black/80 backdrop-blur-md flex items-center justify-center p-4">
        <div class="bg-[#18181b] rounded-2xl border border-white/10 shadow-2xl w-full max-w-lg overflow-hidden flex flex-col max-h-[90vh]">
          <div class="p-4 border-b border-white/10 flex justify-between items-center">
            <h3 class="text-lg font-bold text-white">Crop Profile Picture</h3>
            <button @click="cancelCrop" class="text-gray-400 hover:text-white">✕</button>
          </div>
          
          <div class="p-4 flex-1 bg-black flex items-center justify-center overflow-hidden">
             <cropper
              class="max-h-[50vh]"
              :src="imageToCrop"
              :stencil-props="{ aspectRatio: 1/1 }"
              ref="cropperRef"
            />
          </div>

          <div class="p-4 border-t border-white/10 bg-[#121212] flex justify-end gap-3">
            <button @click="cancelCrop" class="px-4 py-2 text-sm text-gray-400 hover:text-white transition">Cancel</button>
            <button @click="saveCroppedImage" :disabled="isUploading" class="px-6 py-2 bg-gradient-to-r from-pink-600 to-purple-600 text-white text-sm font-bold rounded-full hover:shadow-lg hover:shadow-pink-500/30 transition-all flex items-center gap-2">
              <span v-if="isUploading" class="animate-spin h-3 w-3 border-2 border-white border-t-transparent rounded-full"></span>
              {{ isUploading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import sidebar from '~/components/sidebar.vue'
import { Cropper } from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'

const router = useRouter()
const baseURL = 'http://localhost:5000'
const defaultProfile = '/guest-profile.png'
const defaultImage = '/default-item.svg'

const user = ref(null)
const orders = ref([]) 
const wishlistItems = ref([])
const fileInput = ref(null)
const imageTimestamp = ref(Date.now())

// Cropper State
const showCropper = ref(false)
const imageToCrop = ref(null)
const cropperRef = ref(null)
const isUploading = ref(false)

// URL Formatter & Computed
const getFullImageUrl = (path) => {
  if (!path) return null
  if (path.startsWith('http')) return path
  return `${baseURL}${path}`
}

const userProfileImage = computed(() => {
  if (!user.value || !user.value.profile_image_url) return defaultProfile
  const url = getFullImageUrl(user.value.profile_image_url)
  return `${url}${url.includes('?') ? '&' : '?'}t=${imageTimestamp.value}`
})

// ✅ Logic: ปุ่มผู้ขาย (คำนวณ Text และ Class ตาม Status)
const sellerButtonText = computed(() => {
  if (user.value?.is_seller) return 'จัดการร้านค้า';
  if (user.value?.verification_status === 'PENDING') return '⏳ รอตรวจสอบ';
  if (user.value?.verification_status === 'REJECTED') return '❌ สมัครใหม่';
  return 'สมัครเป็นผู้ขาย';
});

const sellerButtonClass = computed(() => {
  if (user.value?.is_seller) {
    return 'border-pink-500/30 hover:border-pink-500 bg-pink-500/10 text-pink-400 hover:bg-pink-500 hover:text-white';
  }
  if (user.value?.verification_status === 'PENDING') {
    return 'border-yellow-500/30 bg-yellow-500/10 text-yellow-400 cursor-not-allowed';
  }
  if (user.value?.verification_status === 'REJECTED') {
    return 'border-red-500/30 hover:border-red-500 bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white';
  }
  // Default (สมัครใหม่)
  return 'border-pink-500/30 hover:border-pink-500 bg-pink-500/10 text-pink-400 hover:bg-pink-500 hover:text-white';
});

const handleSellerAction = () => {
  if (user.value?.is_seller) {
    router.push('/seller-dashboard');
  } else if (user.value?.verification_status === 'PENDING') {
    // ไม่ทำอะไร หรือแจ้งเตือน
    alert('เอกสารของคุณกำลังอยู่ในระหว่างการตรวจสอบโดยแอดมิน');
  } else {
    // กรณี REJECTED หรือ ยังไม่เคยสมัคร
    router.push('/Registerseller');
  }
};

// Logic: Wishlist
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
    })).slice(0, 8);
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
    paid: 'เตรียมจัดส่ง', 
    processing: 'กำลังขนส่ง', 
    completed: 'สำเร็จ', 
    cancelled: 'ยกเลิก' 
  };
  return labels[status] || status;
}
const getStatusClass = (status) => {
  const base = ""
  if (status === 'pending') return base + "bg-yellow-500/10 text-yellow-400 border-yellow-500/20"
  if (status === 'paid') return base + "bg-blue-500/10 text-blue-400 border-blue-500/20"
  if (status === 'processing') return base + "bg-pink-500/10 text-pink-400 border-pink-500/20"
  if (status === 'completed') return base + "bg-green-500/10 text-green-400 border-green-500/20"
  return base + "bg-gray-500/10 text-gray-400 border-gray-500/20"
}
const formatDate = (dateStr) => {
  if (!dateStr) return "N/A"
  return new Date(dateStr).toLocaleDateString('th-TH', { day: 'numeric', month: 'short', year: '2-digit', hour: '2-digit', minute: '2-digit' })
}

const fetchMyOrders = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    const res = await axios.get(`${baseURL}/api/orders/my-orders`, { 
      headers: { Authorization: `Bearer ${token}` } 
    })
    
    const allOrders = Array.isArray(res.data) ? res.data : []
    const shippingStatuses = ['processing', 'paid']
    
    orders.value = allOrders
      .filter(order => shippingStatuses.includes(order.status))
      .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      .slice(0, 5)
      
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
    
    updateLocalStorageUser(user.value);
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
      
      updateLocalStorageUser(user.value);
      
    } catch (err) { console.error(err) }
  }
}

const resetForm = () => { 
  newAddress.value = { name: '', phone: '', address_line: '', district: '', province: '', postal_code: '', is_default: false }
  isEditing.value = false; editingIndex.value = null 
}
const cancelEdit = () => resetForm()

// ================= Logic: Image Crop & Upload =================
const triggerFileInput = () => fileInput.value.click()

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return

  if (imageToCrop.value) {
    URL.revokeObjectURL(imageToCrop.value)
  }
  imageToCrop.value = URL.createObjectURL(file)
  showCropper.value = true
  e.target.value = ''
}

const cancelCrop = () => {
  showCropper.value = false
  imageToCrop.value = null
}

const saveCroppedImage = () => {
  const { canvas } = cropperRef.value.getResult()
  if (!canvas) return

  isUploading.value = true
  
  canvas.toBlob(async (blob) => {
    const formData = new FormData()
    formData.append('profile_image', blob, 'profile-cropped.png')

    try {
      const token = localStorage.getItem('token')
      const res = await axios.put(baseURL + '/api/profile/image', formData, { 
        headers: { 
          Authorization: `Bearer ${token}`, 
          'Content-Type': 'multipart/form-data' 
        } 
      })
      
      user.value.profile_image_url = res.data.profile_image_url
      imageTimestamp.value = Date.now() 

      const updatedUser = { ...user.value, profile_image_url: res.data.profile_image_url };
      updateLocalStorageUser(updatedUser);

      showCropper.value = false
    } catch (err) { 
      console.error(err); 
      alert('เกิดข้อผิดพลาดในการอัปโหลดรูปภาพ')
    } finally { 
      isUploading.value = false 
    }
  }, 'image/png')
}

// ฟังก์ชัน helper สำหรับอัปเดต LocalStorage และส่ง Event ไปยัง Navbar
const updateLocalStorageUser = (updatedUser) => {
  localStorage.setItem('user', JSON.stringify(updatedUser));
  window.dispatchEvent(new CustomEvent('user-updated', { detail: updatedUser }));
}

const handleLogout = () => {
  localStorage.clear(); 
  router.push('/login'); 
  window.dispatchEvent(new Event('user-updated'))
}

// Translations
const currentLanguage = ref('th')
const t = (key) => {
  const trans = {
    th: { username: 'ชื่อผู้ใช้', fullName: 'ชื่อเต็ม', email: 'อีเมล', phone: 'เบอร์โทร', seller: 'สถานะผู้ใช้', registered: 'ผู้ขาย', notRegistered: 'ผู้ใช้ทั่วไป', addresses: 'ที่อยู่จัดส่ง', addNewAddress: 'เพิ่มที่อยู่ใหม่', editAddress: 'แก้ไขที่อยู่', addAddress: 'เพิ่มที่อยู่', updateAddress: 'อัปเดตที่อยู่', cancel: 'ยกเลิก' },
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
    // Update local storage to ensure fresh data
    localStorage.setItem('user', JSON.stringify(user.value));
    
    fetchMyOrders()
    fetchWishlist()
  } catch (e) { console.error(e); router.push('/login') }
})
</script>

<style scoped>
/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(236, 72, 153, 0.3);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(236, 72, 153, 0.6);
}
</style>