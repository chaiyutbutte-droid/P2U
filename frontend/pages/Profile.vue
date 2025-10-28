<template>

  <div
    class="p-6 max-w-8xl mx-auto bg-black rounded-xl shadow-lg text-white mt-1 mb-1 mr-1 transition-all duration-300"
    :class="expandSidebar ? 'ml-64' : 'ml-20'"
  >
    <div class="md:w-1/4 space-y-5">
      <div class="flex items-center justify-center mb-6 relative">
        <h1 class="text-3xl font-extrabold text-center">
          My <span class="text-pink-600">Profile</span>
        </h1>
      </div>

    </div>

    <div>
      <sidebar />
    </div>

    <div v-if="user" class="flex flex-col md:flex-row md:space-x-8 space-y-8 md:space-y-0">
      <!-- Left Sidebar: Profile + Addresses -->
      <div class="md:w-1/4 space-y-5">
        <!-- Profile Info -->
        <div class="flex items-center space-x-6">
          <div class="relative w-28 h-28 flex-shrink-0 z-50">
            <img
              :src="user.profile_image_url || defaultProfile"
              alt="Profile"
              class="w-full h-full rounded-full border-4 border-pink-500 object-cover shadow-md"
            />
            <button
              @click="triggerFileInput"
              class="absolute bottom-0 right-0 z-50 bg-pink-600 hover:bg-pink-700 p-1.5 rounded-full shadow-md transition"
              aria-label="Change profile picture"
              title="Change profile picture"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">

                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                  d="M11 5h6m2 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2h10zM16 3l-1-1m0 0L9 8m7-6v6H9" />
              </svg>
            </button>
            <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="onFileChange" />
          </div>
          <div class="space-y-2">
            <p><span class="font-semibold text-pink-400">{{ t('username') }}:</span> {{ user.username }}</p>
            <p><span class="font-semibold text-pink-400">{{ t('fullName') }}:</span> {{ user.full_name }}</p>
            <p><span class="font-semibold text-pink-400">{{ t('email') }}:</span> {{ user.email }}</p>
            <p><span class="font-semibold text-pink-400">{{ t('phone') }}:</span> {{ user.phone_number }}</p>
          </div>
        </div>

        <!-- Seller Status -->
        <div class="flex items-center space-x-2 mt-4">
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

        <!-- Addresses -->

        <div class="w-full mt-8">
          <h2 class="text-xl font-semibold mb-4 border-b border-gray-700 pb-2">{{ t('addresses') }}</h2>
          <div v-if="user.addresses && user.addresses.length" class="space-y-4">
            <div v-for="(addr, index) in user.addresses" :key="index"
              class="bg-gray-800 rounded-lg p-4 shadow-inner relative">
              <div class="flex items-center justify-between">

                <h3 class="text-lg font-semibold mb-3 border-b border-gray-700 pb-2">{{ isEditing ? t('editAddress') :
                  t('addNewAddress') }}</h3>
                <span v-if="addr.is_default"
                  class="bg-green-500 text-white text-xs font-semibold px-2 py-1 rounded-full">Default</span>
              </div>
              <p><span class="font-semibold text-pink-400">Name:</span> {{ addr.name }}</p>
              <p><span class="font-semibold text-pink-400">Phone:</span> {{ addr.phone }}</p>
              <p><span class="font-semibold text-pink-400">Address:</span> {{ addr.address_line }}, {{ addr.district }},
                {{ addr.province }}, {{ addr.postal_code }}</p>
              <div class="mt-2 flex gap-2">
                <button @click="editAddress(index)"

                  class="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-xs rounded transition">{{ t('editAddress') }}</button>
                <button @click="deleteAddress(index)"
                  class="px-3 py-1 bg-red-600 hover:bg-red-700 text-white text-xs rounded transition">Delete</button>
              </div>
            </div>
          </div>

          <!-- Add/Edit Address Form -->
          <div class="mt-6 bg-gray-800 rounded-lg p-5 shadow-inner">
            <h3 class="text-lg font-semibold mb-3 border-b border-gray-700 pb-2">
              {{ isEditing ? t('editAddress') : t('addNewAddress') }}
            </h3>
            <form @submit.prevent="addOrUpdateAddress">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input v-model="newAddress.name" :placeholder="t('fullName')" type="text" class="input-field" required />
                <input v-model="newAddress.phone" :placeholder="t('phone')" type="text" class="input-field" required />
                <input v-model="newAddress.address_line" placeholder="Address Line" type="text"
                  class="input-field col-span-2" required />
                <input v-model="newAddress.district" placeholder="District" type="text" class="input-field" required />
                <input v-model="newAddress.province" placeholder="Province" type="text" class="input-field" required />
                <input v-model="newAddress.postal_code" placeholder="Postal Code" type="text" class="input-field"
                  required />
              </div>
              <div class="flex items-center mt-4">
                <input v-model="newAddress.is_default" type="checkbox" id="is_default" class="mr-2" />
                <label for="is_default" class="text-sm">Set as default address</label>
              </div>
              <button type="submit"

                class="mt-4 w-full bg-pink-600 hover:bg-pink-700 text-white font-semibold py-2 rounded-lg transition">{{
                  isEditing ? t('updateAddress') : t('addAddress') }}</button>
              <button v-if="isEditing" @click="cancelEdit" type="button"
                class="mt-2 w-full bg-gray-600 hover:bg-gray-700 text-white font-semibold py-2 rounded-lg transition">{{ t('cancel') }}</button>
            </form>
          </div>
        </div>
      </div>

      <!-- Right Content -->
      <div class="md:w-3/4 space-y-6">

        <!-- Track Order -->
        <h2 class="text-xl font-semibold mb-4 border-b border-gray-700 pb-2">{{ t('trackOrder') }}</h2>
        <div class="bg-gray-800 rounded-lg p-4 shadow-inner min-h-48 flex items-center justify-center text-gray-400">
          <p>Tracking information will appear here.</p>
        </div>


        <!-- Cart Items -->
        <h2 class="text-xl font-semibold mb-4 border-b border-gray-700 pb-2">🛒 {{ t('myCart') }}</h2>
        <div v-if="cartItems.length > 0" class="space-y-4">
          <div v-for="(item, index) in cartItems" :key="index"
            class="bg-gray-800 p-4 rounded-lg flex justify-between items-center shadow-inner">
            <div class="flex items-center space-x-3">
              <img :src="formatImageUrl(item.image)" alt="product" class="w-16 h-16 object-cover rounded" />
              <div>
                <p class="font-semibold text-white">{{ item.name }}</p>
                <p class="text-sm text-gray-400">Qty: {{ item.quantity }}</p>
              </div>
            </div>
            <span class="font-semibold text-pink-400">{{ item.price }} ฿</span>
          </div>
          <button class="w-full bg-pink-600 hover:bg-pink-700 text-white py-2 rounded-lg mt-2">Go to Checkout</button>
        </div>
        <div v-else class="text-gray-400 text-sm text-center">Your cart is empty</div>
      </div>
    </div>

    <!-- Logout -->
    <div class="md:w-1/4 space-y-5 mt-4">
      <button @click="handleLogout"
        class="mt-8 w-full bg-pink-600 hover:bg-pink-700 text-white font-semibold py-2 rounded-lg transition">
        Logout
      </button>
      <div v-if="!user" class="text-center text-gray-400 mt-10">Loading...</div>
    </div>

    <p v-if="errorMsg" class="text-red-400 text-center mt-4">{{ errorMsg }}</p>
    <p v-if="successMsg" class="text-green-400 text-center mt-4">{{ successMsg }}</p>

    <!-- Profile Image Preview -->
    <div v-if="previewImageUrl" class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg max-w-sm w-full text-center text-black shadow-xl">
        <h2 class="text-xl font-bold mb-4">Preview <span class="text-pink-600">Image</span></h2>
        <img :src="previewImageUrl" alt="Preview"
          class="w-32 h-32 mx-auto object-cover rounded-full border border-gray-300 mb-4" />
        <div class="flex justify-center gap-4">
          <button @click="uploadConfirmed"

            class="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded font-semibold">
            Upload
          </button>
          <button @click="cancelUpload"
            class="bg-gray-400 hover:bg-gray-500 text-white px-4 py-2 rounded font-semibold">
            Cancel
          </button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, watch, onBeforeUnmount } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import sidebar from '~/components/sidebar.vue'

// Sidebar hover detection
const expandSidebar = ref(false)
onMounted(() => {
  const sidebarEl = document.querySelector('.fixed.left-0')
  if (sidebarEl) {
    sidebarEl.addEventListener('mouseenter', () => expandSidebar.value = true)
    sidebarEl.addEventListener('mouseleave', () => expandSidebar.value = false)
  }
})

const router = useRouter()
const baseURL = 'http://localhost:5000'
const defaultProfile = '/default-profile.png'

const user = ref(null)
const errorMsg = ref('')
const successMsg = ref('')
const fileInput = ref(null)
const previewImageUrl = ref(null)
let selectedFile = null


// Address
const newAddress = ref({ name:'', phone:'', address_line:'', district:'', province:'', postal_code:'', is_default:false })
const isEditing = ref(false)
const editingIndex = ref(null)

// Cart
const cartItems = ref(JSON.parse(localStorage.getItem('cart') || '[]'))

const formatImageUrl = (url) => url ? (url.startsWith('http') ? url : baseURL + url) : '/no-image.png'
watch(cartItems, val => localStorage.setItem('cart', JSON.stringify(val)), { deep:true })

// Fetch profile
onMounted(async ()=>{
  try{
    const token = localStorage.getItem('token')
    if(!token) throw new Error('No token found')
    const res = await axios.get(baseURL+'/api/profile',{ headers:{ Authorization:`Bearer ${token}` } })
    if(res.data.profile_image_url && !res.data.profile_image_url.startsWith('http')) res.data.profile_image_url = baseURL+res.data.profile_image_url
    user.value = res.data
  }catch(e){ console.error(e); router.push('/login') }
})


// Address functions
const addOrUpdateAddress = async ()=>{
  errorMsg.value=''; successMsg.value=''
  try{
    const token = localStorage.getItem('token')
    const endpoint = isEditing.value ? `${baseURL}/api/profile/address/${editingIndex.value}` : `${baseURL}/api/profile/address`
    const method = isEditing.value ? 'put' : 'post'
    const res = await axios({method,url:endpoint,data:newAddress.value,headers:{Authorization:`Bearer ${token}`}})
    user.value.addresses = res.data.addresses
    successMsg.value = isEditing.value ? 'Address updated successfully.' : 'Address added successfully.'
    resetForm()
  }catch(err){ console.error(err); errorMsg.value = err.response?.data?.msg || 'Failed to save address.' }
}
const editAddress = (i)=>{ newAddress.value={...user.value.addresses[i]}; isEditing.value=true; editingIndex.value=i }
const cancelEdit = ()=>resetForm()
const deleteAddress = async(i)=>{
  if(confirm('Are you sure to delete this address?')){
    errorMsg.value=''; successMsg.value=''
    try{
      const token = localStorage.getItem('token')
      const res = await axios.delete(`${baseURL}/api/profile/address/${i}`,{ headers:{Authorization:`Bearer ${token}`}})
      user.value.addresses = res.data.addresses
      successMsg.value='Address deleted successfully.'
    }catch(err){ console.error(err); errorMsg.value=err.response?.data?.msg || 'Failed to delete address.' }
  }
}
const resetForm = ()=>{ newAddress.value={name:'', phone:'', address_line:'', district:'', province:'', postal_code:'', is_default:false}; isEditing.value=false; editingIndex.value=null }

// Profile image
const triggerFileInput=()=>fileInput.value.click()
const onFileChange=(e)=>{
  const file=e.target.files[0]
  if(!file) return
  if(previewImageUrl.value) URL.revokeObjectURL(previewImageUrl.value)
  selectedFile=file
  previewImageUrl.value=URL.createObjectURL(file)
}
const uploadConfirmed=async ()=>{
  errorMsg.value=''; successMsg.value=''
  if(!selectedFile) return
  const formData=new FormData(); formData.append('profile_image',selectedFile)
  try{
    const token = localStorage.getItem('token')
    const res = await axios.put(baseURL+'/api/profile/image',formData,{ headers:{Authorization:`Bearer ${token}`, 'Content-Type':'multipart/form-data'} })
    let imageUrl=res.data.profile_image_url; if(imageUrl && !imageUrl.startsWith('http')) imageUrl=baseURL+imageUrl
    user.value.profile_image_url=imageUrl
    const storedUser=JSON.parse(localStorage.getItem('user')||'{}')
    storedUser.profile_image_url=imageUrl
    localStorage.setItem('user',JSON.stringify(storedUser))
    successMsg.value='Profile image updated successfully.'
    window.dispatchEvent(new Event('user-updated'))
  }catch(err){ console.error(err); errorMsg.value=err.response?.data?.msg || 'Failed to update profile image.' }
  finally{ if(previewImageUrl.value) URL.revokeObjectURL(previewImageUrl.value); previewImageUrl.value=null; selectedFile=null }
}
const cancelUpload=()=>{ if(previewImageUrl.value) URL.revokeObjectURL(previewImageUrl.value); previewImageUrl.value=null; selectedFile=null }

// Cart
const addToCart=(p)=>{
  const ex = cartItems.value.find(i=>i.id===p.id)
  if(ex) ex.quantity+=1
  else { let img=p.image||'/no-image.png'; if(!img.startsWith('http')) img=baseURL+img; cartItems.value.push({...p,image:img,quantity:1}) }
}
const cancelUpload = () => { previewImageUrl.value = null; selectedFile = null }

// Logout

const handleLogout=()=>{
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('user')
  localStorage.removeItem('cart')
  router.push('/login')
  window.dispatchEvent(new Event('user-updated'))
}


// Language
const currentLanguage = ref('th')
const t=(key)=>{
  const translations={
    th:{ username:'ชื่อผู้ใช้', fullName:'ชื่อเต็ม', email:'อีเมล', phone:'เบอร์โทร', seller:'ผู้ขาย', registered:'ลงทะเบียนแล้ว', notRegistered:'ยังไม่ลงทะเบียน', addresses:'ที่อยู่', addNewAddress:'เพิ่มที่อยู่ใหม่', editAddress:'แก้ไขที่อยู่', addAddress:'เพิ่มที่อยู่', updateAddress:'อัปเดตที่อยู่', cancel:'ยกเลิก', trackOrder:'ติดตามคำสั่งซื้อ', myCart:'ตะกร้าของฉัน' },
    en:{ username:'Username', fullName:'Full Name', email:'Email', phone:'Phone', seller:'Seller', registered:'Registered', notRegistered:'Not Registered', addresses:'Addresses', addNewAddress:'Add New Address', editAddress:'Edit Address', addAddress:'Add Address', updateAddress:'Update Address', cancel:'Cancel', trackOrder:'Track Order', myCart:'My Cart' }
  }
  return translations[currentLanguage.value][key]||key
}
</script>
