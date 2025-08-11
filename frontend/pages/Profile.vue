<template>
  <div class="p-6 max-w-2xl mx-auto bg-gray-900 rounded-xl shadow-lg text-white relative my-20 ">
    <div class="flex items-center justify-center mb-6 relative">
      <button
        @click="goBack"
        class="absolute left-0 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm font-semibold transition"
      >
        ← Back
      </button>
      <h1 class="text-3xl font-extrabold text-center">My <span class="text-pink-600">Profile</span></h1>
    </div>

    <div v-if="user" class="space-y-5">
      <div class="flex justify-center relative w-28 h-28 mx-auto">
        <img
          :src="user.profile_image_url || defaultProfile"
          alt="Profile"
          class="w-28 h-28 rounded-full border-4 border-pink-500 object-cover shadow-md"
        />
        <button 
          @click="triggerFileInput"
          class="absolute bottom-0 right-0 bg-pink-600 hover:bg-pink-700 p-1.5 rounded-full shadow-md transition"
          aria-label="Change profile picture"
          title="Change profile picture"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M11 5h6m2 2v10a2 2 0 01-2 2H7a2 2 0 01-2-2V7a2 2 0 012-2h10zM16 3l-1-1m0 0L9 8m7-6v6H9" />
          </svg>
        </button>
        <input
          ref="fileInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="onFileChange"
        />
      </div>

      <div class="flex flex-col md:flex-row md:space-x-8 space-y-5 md:space-y-0">
        <div class="space-y-3 md:w-1/2">
          <p><span class="font-semibold text-pink-400">Username:</span> {{ user.username }}</p>
          <p><span class="font-semibold text-pink-400">Full Name:</span> {{ user.full_name }}</p>
          <p><span class="font-semibold text-pink-400">Email:</span> {{ user.email }}</p>
          <p><span class="font-semibold text-pink-400">Phone:</span> {{ user.phone_number }}</p>
          
          <div class="flex items-center space-x-2">
            <span class="font-semibold text-pink-400">Seller:</span>
            <span>{{ user.is_seller ? 'Registered' : 'Not Registered' }}</span>
            <button
              v-if="user.is_seller"
              @click="router.push('/seller')"
              class="px-2 py-1 bg-pink-600 hover:bg-pink-700 text-white text-xs font-semibold rounded-lg transition"
            >
              Go to Seller Page
            </button>

            <button
              v-else
              @click="router.push('/Registerseller')"
              class="px-2 py-1 bg-pink-600 hover:bg-pink-700 text-white text-xs font-semibold rounded-lg transition"
            >
              Register as Seller
            </button>
          </div>
          </div> 

        <div v-if="user.addresses && user.addresses.length" class="mt-6 md:mt-0 md:w-1/2">
          <h2 class="text-xl font-semibold mb-2 border-b border-gray-700 pb-1">Addresses</h2>
          <ul class="space-y-2 text-gray-300">
            <li
              v-for="(addr, index) in user.addresses"
              :key="index"
              class="bg-gray-800 rounded-md p-3 shadow-inner"
            >
              <p><span class="font-semibold text-pink-400">Name:</span> {{ addr.name }}</p>
              <p><span class="font-semibold text-pink-400">Phone:</span> {{ addr.phone }}</p>
              <p><span class="font-semibold text-pink-400">Address:</span> {{ addr.address_line }}, {{ addr.district }}, {{ addr.province }}, {{ addr.postal_code }}</p>
            </li>
          </ul>
        </div>
      </div>
      
      <button
        @click="handleLogout"
        class="mt-8 w-full bg-pink-600 hover:bg-pink-700 text-white font-semibold py-2 rounded-lg transition"
      >
        Logout
      </button>
    </div>

    <div v-else class="text-center text-gray-400 mt-10">
      Loading...
    </div>

    <p v-if="errorMsg" class="text-red-400 text-center mt-4">{{ errorMsg }}</p>
    <p v-if="successMsg" class="text-green-400 text-center mt-4">{{ successMsg }}</p>

    <div v-if="previewImageUrl" class="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded-lg max-w-sm w-full text-center text-black shadow-xl">
        <h2 class="text-xl font-bold mb-4">Preview <span class="text-pink-600">Image</span></h2>
        <img :src="previewImageUrl" alt="Preview" class="w-32 h-32 mx-auto object-cover rounded-full border border-gray-300 mb-4" />
        <div class="flex justify-center gap-4">
          <button
            @click="uploadConfirmed"
            class="bg-pink-600 hover:bg-pink-700 text-white px-4 py-2 rounded font-semibold"
          >
            Upload
          </button>
          <button
            @click="cancelUpload"
            class="bg-gray-400 hover:bg-gray-500 text-white px-4 py-2 rounded font-semibold"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// โค้ดส่วน script ไม่มีการเปลี่ยนแปลง
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const baseURL = 'http://localhost:5000'
const defaultProfile = '/default-profile.png'

const user = ref(null)
const errorMsg = ref('')
const successMsg = ref('')
const fileInput = ref(null)

const previewImageUrl = ref(null)
let selectedFile = null

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) throw new Error('No token found')

    const res = await axios.get(baseURL + '/api/profile', {
      headers: { Authorization: `Bearer ${token}` }
    })

    if (res.data.profile_image_url && !res.data.profile_image_url.startsWith('http')) {
      res.data.profile_image_url = baseURL + res.data.profile_image_url
    }

    user.value = res.data
  } catch (error) {
    console.error(error)
    window.location.href = '/login'
  }
})

const triggerFileInput = () => {
  fileInput.value.click()
}

const onFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return
  selectedFile = file
  previewImageUrl.value = URL.createObjectURL(file)
}

const uploadConfirmed = async () => {
  errorMsg.value = ''
  successMsg.value = ''
  if (!selectedFile) return

  const formData = new FormData()
  formData.append('profile_image', selectedFile)

  try {
    const token = localStorage.getItem('token')
    if (!token) throw new Error('No token found')

    const res = await axios.put(baseURL + '/api/profile/image', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      }
    })

    let imageUrl = res.data.profile_image_url
    if (imageUrl && !imageUrl.startsWith('http')) {
      imageUrl = baseURL + imageUrl
    }

    user.value.profile_image_url = imageUrl
    const storedUser = JSON.parse(localStorage.getItem('user') || '{}')
    storedUser.profile_image_url = imageUrl
    localStorage.setItem('user', JSON.stringify(storedUser))

    successMsg.value = 'Profile image updated successfully.'
    window.dispatchEvent(new Event('user-updated'))
  } catch (err) {
    console.error(err)
    errorMsg.value = err.response?.data?.msg || 'Failed to update profile image.'
  } finally {
    previewImageUrl.value = null
    selectedFile = null
  }
}

const cancelUpload = () => {
  previewImageUrl.value = null
  selectedFile = null
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('user')
  router.push('/login')
  window.dispatchEvent(new Event('user-updated'))
}

const goBack = () => {
  router.back()
}
</script>