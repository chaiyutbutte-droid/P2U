<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-sm">
      <h1 class="text-2xl font-bold text-white text-center mb-6">Register as Seller</h1>

      <input v-model="shopName" placeholder="Shop Name" class="input-style" />
      
      <input v-model="fullName" placeholder="Full Name" class="input-style" />
      <input v-model="phoneNumber" placeholder="Phone Number" class="input-style" />

      <input v-model="addressName" placeholder="Receiver's Name" class="input-style" />
      <input v-model="addressPhone" placeholder="Receiver's Phone" class="input-style" />
      <input v-model="addressLine" placeholder="Address Line" class="input-style" />
      <input v-model="district" placeholder="District" class="input-style" />
      <input v-model="province" placeholder="Province" class="input-style" />
      <input v-model="postalCode" placeholder="Postal Code" class="input-style" />

      <button
        @click="handleRegisterSeller"
        class="bg-black hover:bg-gray-700 text-white font-semibold py-2 w-full rounded-lg transition duration-200 border border-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:border-white"
      >
        Register Seller
      </button>

      <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center">{{ errorMsg }}</p>
      <p v-if="successMsg" class="text-green-400 text-sm mt-4 text-center">{{ successMsg }}</p>

      <div class="text-center text-sm text-gray-400 mt-4">
        Go back to your 
        <router-link to="/profile" class="underline hover:text-white">profile</router-link>.
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Data for seller registration
const shopName = ref('')
const fullName = ref('')
const phoneNumber = ref('')
const addressName = ref('')
const addressPhone = ref('')
const addressLine = ref('')
const district = ref('')
const province = ref('')
const postalCode = ref('')

const errorMsg = ref('')
const successMsg = ref('')

const handleRegisterSeller = async () => {
  errorMsg.value = ''
  successMsg.value = ''

  if (!shopName.value || !fullName.value || !addressLine.value) {
    errorMsg.value = 'Please fill in all required fields.'
    return
  }
  
  const token = localStorage.getItem('token')
  if (!token) {
    errorMsg.value = 'User not authenticated. Please log in first.'
    return
  }

  try {
    const res = await axios.post('http://localhost:5000/api/register-seller', {
      shop_name: shopName.value,
      full_name: fullName.value,
      phone_number: phoneNumber.value,
      address_name: addressName.value,
      address_phone: addressPhone.value,
      address_line: addressLine.value,
      district: district.value,
      province: province.value,
      postal_code: postalCode.value,
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })

    successMsg.value = res.data.msg || 'Seller registration successful.'
    
    // Update local storage to reflect the new seller status
    const storedUser = JSON.parse(localStorage.getItem('user') || '{}')
    storedUser.is_seller = true
    localStorage.setItem('user', JSON.stringify(storedUser))
    
    setTimeout(() => router.push('/profile'), 1500)
    
  } catch (err) {
    console.error('[Register Seller Error]', err)
    errorMsg.value = err.response?.data?.msg || 'Seller registration failed.'
  }
}
</script>

<style scoped lang="postcss">
.input-style {
  @apply mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white;
}
</style>