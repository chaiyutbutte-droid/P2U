<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white p-6 transition-all duration-300">
    <div class="max-w-7xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-10">
        <h1 class="text-4xl md:text-5xl font-extrabold bg-gradient-to-r from-pink-500 to-purple-600 bg-clip-text text-transparent">
          My Profile
        </h1>
        <p class="text-gray-400 mt-2">จัดการข้อมูลส่วนตัวและที่อยู่ของคุณ</p>
      </div>

      <div>
        <sidebar />
      </div>

      <div v-if="user" class="flex flex-col lg:flex-row gap-8">
        <!-- Left Sidebar -->
        <div class="lg:w-1/3 space-y-6">
          <!-- Profile Card -->
          <div class="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-6 shadow-2xl border border-gray-700 hover:border-pink-500 transition-all duration-300">
            <div class="flex flex-col items-center">
              <!-- Profile Image -->
              <div class="relative mb-4">
                <div class="w-32 h-32 rounded-full bg-gradient-to-br from-pink-500 to-purple-600 p-1">
                  <img :src="user.profile_image_url || defaultProfile" alt="Profile"
                    class="w-full h-full rounded-full object-cover bg-gray-800" />
                </div>
                <button @click="triggerFileInput"
                  class="absolute bottom-0 right-0 bg-pink-600 hover:bg-pink-700 p-2 rounded-full shadow-lg transform hover:scale-110 transition-all duration-200"
                  aria-label="Change profile picture">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </button>
                <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange" />
              </div>

              <!-- User Info -->
              <div class="w-full space-y-3">
                <div class="bg-gray-900/50 rounded-lg p-3 border border-gray-700">
                  <p class="text-xs text-gray-400">{{ t('username') }}</p>
                  <p class="text-white font-semibold">{{ user.username }}</p>
                </div>
                <div class="bg-gray-900/50 rounded-lg p-3 border border-gray-700">
                  <p class="text-xs text-gray-400">{{ t('fullName') }}</p>
                  <p class="text-white font-semibold">{{ user.full_name }}</p>
                </div>
                <div class="bg-gray-900/50 rounded-lg p-3 border border-gray-700">
                  <p class="text-xs text-gray-400">{{ t('email') }}</p>
                  <p class="text-white font-semibold text-sm">{{ user.email }}</p>
                </div>
                <div class="bg-gray-900/50 rounded-lg p-3 border border-gray-700">
                  <p class="text-xs text-gray-400">{{ t('phone') }}</p>
                  <p class="text-white font-semibold">{{ user.phone_number }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Seller Status Card -->
          <div class="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-6 shadow-2xl border border-gray-700">
            <div class="flex items-center justify-between mb-4">
              <span class="text-gray-400 text-sm">{{ t('seller') }}</span>
              <span v-if="user.is_seller" class="px-3 py-1 bg-green-500/20 text-green-400 text-xs font-semibold rounded-full border border-green-500">
                {{ t('registered') }}
              </span>
              <span v-else class="px-3 py-1 bg-gray-500/20 text-gray-400 text-xs font-semibold rounded-full border border-gray-500">
                {{ t('notRegistered') }}
              </span>
            </div>
            <button v-if="user.is_seller" @click="router.push('/seller')"
              class="w-full bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white font-semibold py-3 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg">
              Go to Seller Page
            </button>
            <button v-else @click="router.push('/register-seller')"
              class="w-full bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white font-semibold py-3 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg">
              Register as Seller
            </button>
          </div>

          <!-- AI Evaluation Button -->
          <button @click="router.push('/ai')"
            class="w-full bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold py-3 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg">
            🤖 ไปยังหน้าประเมินสินค้า
          </button>

          <!-- Logout Button -->
          <button @click="handleLogout"
            class="w-full bg-gradient-to-r from-red-600 to-red-700 hover:from-red-700 hover:to-red-800 text-white font-semibold py-3 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg">
            🚪 ออกจากระบบ
          </button>
        </div>

        <!-- Right Content -->
        <div class="lg:w-2/3 space-y-6">
          <!-- Addresses Section -->
          <div class="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-6 shadow-2xl border border-gray-700">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-2">
              📍 {{ t('addresses') }}
            </h2>
            
            <!-- Address List -->
            <div v-if="addresses.length" class="space-y-4 mb-6">
              <div v-for="(addr, index) in addresses" :key="index"
                class="bg-gray-900/50 rounded-xl p-4 border border-gray-700 hover:border-pink-500 transition-all duration-300">
                <div class="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between mb-2">
                  <div>
                    <h3 class="font-semibold text-lg">{{ addr.name }}</h3>
                    <p class="text-sm text-pink-300">{{ addr.phone }}</p>
                  </div>
                  <label class="flex items-center gap-2 text-sm cursor-pointer">
                    <input type="radio" name="defaultAddress" :checked="pendingDefaultIndex === index" :value="index"
                      @change="queueDefaultSelection(index)" class="text-pink-500 focus:ring-pink-500" />
                    <span :class="index === selectedAddressIndex ? 'text-green-400 font-semibold' : 'text-gray-400'">
                      {{ index === selectedAddressIndex ? t('defaultAddress') : t('selectAddress') }}
                    </span>
                  </label>
                </div>
                <div class="space-y-1 text-sm text-gray-300">
                  <p>📍 {{ addr.address_line }}</p>
                  <p>🏙️ {{ addr.district }}, {{ addr.province }} {{ addr.postal_code }}</p>
                </div>
                <div class="mt-4 flex gap-2">
                  <button @click="editAddress(index)"
                    class="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold py-2 rounded-lg transition-all duration-200">
                    ✏️ {{ t('editAddress') }}
                  </button>
                  <button @click="deleteAddress(index)"
                    class="flex-1 bg-red-600 hover:bg-red-700 text-white text-sm font-semibold py-2 rounded-lg transition-all duration-200">
                    🗑️ {{ t('delete') }}
                  </button>
                </div>
              </div>
              <div v-if="isDefaultDirty" class="flex justify-end pt-2">
                <button @click="confirmDefaultSelection" :disabled="isSettingDefault"
                  class="px-4 py-2 bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 disabled:opacity-60 disabled:cursor-not-allowed text-white text-sm font-semibold rounded-lg transition-all duration-200">
                  {{ t('confirmDefault') }}
                </button>
              </div>
            </div>
            <div v-else class="mb-6 bg-gray-900/50 rounded-xl p-6 border border-dashed border-gray-700 text-center text-gray-400">
              <p class="mb-2 text-base">ยังไม่มีที่อยู่จัดส่ง</p>
              <p class="text-sm">เพิ่มที่อยู่แรกของคุณเพื่อใช้งานในการสั่งซื้อ</p>
            </div>

            <!-- Add/Edit Address Form -->
            <div class="bg-gray-900/50 rounded-xl p-5 border border-gray-700">
              <h3 class="text-lg font-semibold mb-4">
                {{ isEditing ? '✏️ ' + t('editAddress') : '➕ ' + t('addNewAddress') }}
              </h3>
              <form @submit.prevent="addOrUpdateAddress" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <input v-model="newAddress.name" :placeholder="t('fullName')" type="text"
                    class="bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-pink-500 transition-colors" required />
                  <input v-model="newAddress.phone" :placeholder="t('phone')" type="text"
                    class="bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-pink-500 transition-colors" required />
                </div>
                <input v-model="newAddress.address_line" placeholder="Address Line" type="text"
                  class="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-pink-500 transition-colors" required />
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <input v-model="newAddress.district" placeholder="District" type="text"
                    class="bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-pink-500 transition-colors" required />
                  <input v-model="newAddress.province" placeholder="Province" type="text"
                    class="bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-pink-500 transition-colors" required />
                  <input v-model="newAddress.postal_code" placeholder="Postal Code" type="text"
                    class="bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-pink-500 transition-colors" required />
                </div>
                <div class="flex items-center">
                  <input v-model="newAddress.is_default" type="checkbox" id="is_default"
                    class="w-4 h-4 text-pink-600 bg-gray-800 border-gray-600 rounded focus:ring-pink-500" />
                  <label for="is_default" class="ml-2 text-sm text-gray-300">{{ t('setDefault') }}</label>
                </div>
                <div class="flex gap-2">
                  <button type="submit" :disabled="isAddressSaving"
                    class="flex-1 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 disabled:opacity-60 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg transition-all duration-300">
                    {{ isEditing ? t('updateAddress') : t('addAddress') }}
                  </button>
                  <button v-if="isEditing" @click="cancelEdit" type="button"
                    class="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 rounded-lg transition-all duration-300">
                    {{ t('cancel') }}
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Track Order Section -->
          <div class="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-6 shadow-2xl border border-gray-700">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-2">
              📦 {{ t('trackOrder') }}
            </h2>
            <div class="bg-gray-900/50 rounded-xl p-8 border border-gray-700 flex items-center justify-center min-h-[200px]">
              <p class="text-gray-400 text-center">ข้อมูลการติดตามจะปรากฏที่นี่</p>
            </div>
          </div>

          <!-- Cart Items Section -->
          <div class="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-6 shadow-2xl border border-gray-700">
            <h2 class="text-2xl font-bold mb-6 flex items-center gap-2">
              🛒 {{ t('myCart') }}
            </h2>
            <div v-if="cartItems.length > 0" class="space-y-4">
              <div v-for="(item, index) in cartItems" :key="index"
                class="bg-gray-900/50 rounded-xl p-4 border border-gray-700 hover:border-pink-500 transition-all duration-300">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-4">
                    <div class="w-20 h-20 rounded-lg overflow-hidden bg-gray-800">
                      <img :src="formatImageUrl(item.image)" alt="product" class="w-full h-full object-cover" />
                    </div>
                    <div>
                      <p class="font-semibold text-white">{{ item.name }}</p>
                      <p class="text-sm text-gray-400">จำนวน: {{ item.quantity }}</p>
                    </div>
                  </div>
                  <span class="font-bold text-xl text-pink-400">{{ item.price }} ฿</span>
                </div>
              </div>
              <NuxtLink to="/payment">
                <button class="w-full bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white font-semibold py-4 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg">
                  💳 ไปที่หน้าชำระเงิน
                </button>
              </NuxtLink>
            </div>
            <div v-else class="bg-gray-900/50 rounded-xl p-8 border border-gray-700 flex items-center justify-center min-h-[200px]">
              <p class="text-gray-400 text-center">🛒 รถเข็นของคุณว่างเปล่า</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!user" class="text-center text-gray-400 mt-10">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500"></div>
        <p class="mt-4">กำลังโหลด...</p>
      </div>
    </div>

    <!-- Messages -->
    <div v-if="errorMsg || successMsg" class="fixed bottom-4 right-4 z-50">
      <div v-if="errorMsg" class="bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg animate-bounce">
        ❌ {{ errorMsg }}
      </div>
      <div v-if="successMsg" class="bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg animate-bounce">
        ✅ {{ successMsg }}
      </div>
    </div>

    <!-- Profile Image Preview Modal -->
    <div v-if="previewImageUrl" class="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 backdrop-blur-sm">
      <div class="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-2xl max-w-md w-full text-center shadow-2xl border border-gray-700">
        <h2 class="text-2xl font-bold mb-6">
          Preview <span class="text-pink-600">Image</span>
        </h2>
        <div class="mb-6">
          <div class="w-40 h-40 mx-auto rounded-full bg-gradient-to-br from-pink-500 to-purple-600 p-1">
            <img :src="previewImageUrl" alt="Preview" class="w-full h-full rounded-full object-cover bg-gray-800" />
          </div>
        </div>
        <div class="flex gap-4">
          <button @click="uploadConfirmed"
            class="flex-1 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white font-semibold py-3 rounded-lg transition-all duration-300">
            ✅ Upload
          </button>
          <button @click="cancelUpload"
            class="flex-1 bg-gray-600 hover:bg-gray-700 text-white font-semibold py-3 rounded-lg transition-all duration-300">
            ❌ Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({ middleware: 'auth' })
import { ref, onMounted, watch, computed, onBeforeUnmount } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import sidebar from '~/components/sidebar.vue'

// Sidebar hover detection
const expandSidebar = ref(false)
let sidebarEl = null
const handleSidebarEnter = () => expandSidebar.value = true
const handleSidebarLeave = () => expandSidebar.value = false
onMounted(() => {
  sidebarEl = document.querySelector('.fixed.left-0')
  if (sidebarEl) {
    sidebarEl.addEventListener('mouseenter', handleSidebarEnter)
    sidebarEl.addEventListener('mouseleave', handleSidebarLeave)
  }
  fetchProfile()
})

const router = useRouter()
const baseURL = 'http://localhost:5000'
const defaultProfile = '/default-profile.png'

const isClient = process.client
const getToken = () => {
  if (!isClient) return null
  const storedToken = localStorage.getItem('token')
  if (!storedToken || storedToken === 'undefined' || storedToken === 'null') return null
  return storedToken
}

const user = ref(null)
const errorMsg = ref('')
const successMsg = ref('')
const fileInput = ref(null)
const previewImageUrl = ref(null)
let selectedFile = null
let messageTimer = null

const selectedAddressIndex = ref(null)
const pendingDefaultIndex = ref(null)
const isAddressSaving = ref(false)
const isSettingDefault = ref(false)
const addresses = computed(() => user.value?.addresses || [])
const isDefaultDirty = computed(() =>
  pendingDefaultIndex.value !== null &&
  pendingDefaultIndex.value !== selectedAddressIndex.value
)

// Address
const newAddress = ref({ name: '', phone: '', address_line: '', district: '', province: '', postal_code: '', is_default: false })
const isEditing = ref(false)
const editingIndex = ref(null)

const applyAddressResponse = (list = []) => {
  const normalized = Array.isArray(list) ? list : []
  if (!user.value) user.value = {}
  user.value.addresses = normalized
  const defaultIndex = normalized.findIndex(addr => addr.is_default)
  selectedAddressIndex.value = defaultIndex >= 0 ? defaultIndex : null
  pendingDefaultIndex.value = selectedAddressIndex.value
}

const clearMessages = () => {
  errorMsg.value = ''
  successMsg.value = ''
}

const showMessage = (type, message) => {
  if (messageTimer) clearTimeout(messageTimer)
  if (type === 'success') {
    successMsg.value = message
    errorMsg.value = ''
  } else {
    errorMsg.value = message
    successMsg.value = ''
  }
  messageTimer = setTimeout(() => {
    successMsg.value = ''
    errorMsg.value = ''
  }, 4000)
}

// Cart
const cartItems = ref([])
if (isClient) {
  cartItems.value = JSON.parse(localStorage.getItem('cart') || '[]')
}

const formatImageUrl = (url) => url ? (url.startsWith('http') ? url : baseURL + url) : '/default-product.svg'
watch(cartItems, val => {
  if (isClient) localStorage.setItem('cart', JSON.stringify(val))
}, { deep: true })

const fetchProfile = async () => {
  try {
    clearMessages()
    const token = getToken()
    if (!token) return handleLogout()
    const res = await axios.get(baseURL + '/api/profile', { headers: { Authorization: `Bearer ${token}` } })
    if (res.data.profile_image_url && !res.data.profile_image_url.startsWith('http')) res.data.profile_image_url = baseURL + res.data.profile_image_url
    user.value = res.data
    applyAddressResponse(res.data.addresses || [])
    showMessage('success', 'โหลดข้อมูลโปรไฟล์สำเร็จ')
  } catch (e) {
    console.error(e)
    showMessage('error', e.response?.data?.msg || 'ไม่สามารถโหลดโปรไฟล์ได้')
    if (e.response?.status === 401 || e.response?.status === 403) return handleLogout()
    router.push('/login')
  }
}

onBeforeUnmount(() => {
  if (sidebarEl) {
    sidebarEl.removeEventListener('mouseenter', handleSidebarEnter)
    sidebarEl.removeEventListener('mouseleave', handleSidebarLeave)
  }
  if (messageTimer) clearTimeout(messageTimer)
  if (previewImageUrl.value) URL.revokeObjectURL(previewImageUrl.value)
})

// Address functions
const addOrUpdateAddress = async () => {
  if (isAddressSaving.value) return
  clearMessages()
  isAddressSaving.value = true
  try {
    const token = getToken()
    if (!token) return handleLogout()
    const isUpdate = isEditing.value && editingIndex.value !== null
    const endpoint = isUpdate ? `${baseURL}/api/profile/address/${editingIndex.value}` : `${baseURL}/api/profile/address`
    const method = isUpdate ? 'put' : 'post'
    const res = await axios({ method, url: endpoint, data: newAddress.value, headers: { Authorization: `Bearer ${token}` } })
    applyAddressResponse(res.data.addresses)
    showMessage('success', isUpdate ? 'อัปเดตที่อยู่เรียบร้อยแล้ว' : 'เพิ่มที่อยู่ใหม่เรียบร้อยแล้ว')
    resetForm()
  } catch (err) {
    console.error(err)
    showMessage('error', err.response?.data?.msg || 'บันทึกที่อยู่ไม่สำเร็จ')
  } finally {
    isAddressSaving.value = false
  }
}

const editAddress = (i) => {
  const addr = addresses.value[i]
  if (!addr) return
  newAddress.value = { ...addr }
  isEditing.value = true
  editingIndex.value = i
}

const cancelEdit = () => resetForm()

const deleteAddress = async (i) => {
  if (!confirm('Are you sure to delete this address?')) return
  clearMessages()
  try {
    const token = getToken()
    if (!token) return handleLogout()
    const res = await axios.delete(`${baseURL}/api/profile/address/${i}`, { headers: { Authorization: `Bearer ${token}` } })
    applyAddressResponse(res.data.addresses)
    showMessage('success', 'ลบที่อยู่เรียบร้อยแล้ว')
    if (isEditing.value && editingIndex.value === i) resetForm()
  } catch (err) {
    console.error(err)
    showMessage('error', err.response?.data?.msg || 'ลบที่อยู่ไม่สำเร็จ')
  }
}

const resetForm = () => {
  newAddress.value = { name: '', phone: '', address_line: '', district: '', province: '', postal_code: '', is_default: false }
  isEditing.value = false
  editingIndex.value = null
}

const queueDefaultSelection = (i) => {
  pendingDefaultIndex.value = i
}

const confirmDefaultSelection = async () => {
  if (!isDefaultDirty.value || pendingDefaultIndex.value === null) return
  clearMessages()
  isSettingDefault.value = true
  try {
    const token = getToken()
    if (!token) return handleLogout()
    const res = await axios.patch(`${baseURL}/api/profile/address/default/${pendingDefaultIndex.value}`, {}, { headers: { Authorization: `Bearer ${token}` } })
    applyAddressResponse(res.data.addresses)
    showMessage('success', 'ตั้งค่าที่อยู่หลักเรียบร้อยแล้ว')
  } catch (err) {
    console.error(err)
    showMessage('error', err.response?.data?.msg || 'ตั้งค่าที่อยู่หลักไม่สำเร็จ')
  } finally {
    isSettingDefault.value = false
  }
}

// Profile image
const triggerFileInput = () => fileInput.value.click()
const onFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return
  if (previewImageUrl.value) URL.revokeObjectURL(previewImageUrl.value)
  selectedFile = file
  previewImageUrl.value = URL.createObjectURL(file)
}
const uploadConfirmed = async () => {
  errorMsg.value = ''; successMsg.value = ''
  if (!selectedFile) return
  const formData = new FormData(); formData.append('profile_image', selectedFile)
  try {
    const token = getToken()
    if (!token) return handleLogout()
    const res = await axios.put(baseURL + '/api/profile/image', formData, { headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' } })
    let imageUrl = res.data.profile_image_url; if (imageUrl && !imageUrl.startsWith('http')) imageUrl = baseURL + imageUrl
    user.value.profile_image_url = imageUrl
    const storedUser = JSON.parse(localStorage.getItem('user') || '{}')
    storedUser.profile_image_url = imageUrl
    localStorage.setItem('user', JSON.stringify(storedUser))
    successMsg.value = 'Profile image updated successfully.'
    window.dispatchEvent(new Event('user-updated'))
  } catch (err) { console.error(err); errorMsg.value = err.response?.data?.msg || 'Failed to update profile image.' }
  finally { if (previewImageUrl.value) URL.revokeObjectURL(previewImageUrl.value); previewImageUrl.value = null; selectedFile = null }
}
const cancelUpload = () => { if (previewImageUrl.value) URL.revokeObjectURL(previewImageUrl.value); previewImageUrl.value = null; selectedFile = null }

// Logout
const handleLogout = () => {
  if (isClient) {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    localStorage.removeItem('user')
    localStorage.removeItem('cart')
  }
  router.push('/login')
  if (isClient) window.dispatchEvent(new Event('user-updated'))
}

// Language
const currentLanguage = ref('th')
const t = (key) => {
  const translations = {
    th: {
      username: 'ชื่อผู้ใช้',
      fullName: 'ชื่อเต็ม',
      email: 'อีเมล',
      phone: 'เบอร์โทร',
      seller: 'ผู้ขาย',
      registered: 'ลงทะเบียนแล้ว',
      notRegistered: 'ยังไม่ลงทะเบียน',
      addresses: 'ที่อยู่',
      addNewAddress: 'เพิ่มที่อยู่ใหม่',
      editAddress: 'แก้ไขที่อยู่',
      addAddress: 'เพิ่มที่อยู่',
      updateAddress: 'อัปเดตที่อยู่',
      cancel: 'ยกเลิก',
      delete: 'ลบ',
      setDefault: 'ตั้งเป็นที่อยู่หลัก',
      defaultAddress: 'ที่อยู่หลัก',
      selectAddress: 'เลือกเป็นที่อยู่หลัก',
      confirmDefault: 'ยืนยันที่อยู่หลัก',
      trackOrder: 'ติดตามคำสั่งซื้อ',
      myCart: 'ตะกร้าของฉัน'
    },
    en: {
      username: 'Username',
      fullName: 'Full Name',
      email: 'Email',
      phone: 'Phone',
      seller: 'Seller',
      registered: 'Registered',
      notRegistered: 'Not Registered',
      addresses: 'Addresses',
      addNewAddress: 'Add New Address',
      editAddress: 'Edit Address',
      addAddress: 'Add Address',
      updateAddress: 'Update Address',
      cancel: 'Cancel',
      delete: 'Delete',
      setDefault: 'Set as default address',
      defaultAddress: 'Default address',
      selectAddress: 'Select as default',
      confirmDefault: 'Confirm default',
      trackOrder: 'Track Order',
      myCart: 'My Cart'
    }
  }
  return translations[currentLanguage.value][key] || key
}
</script>