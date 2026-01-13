<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-sm text-white">
      <h1 class="text-2xl font-bold text-center mb-4">Verify Your Email</h1>
      <p class="text-center text-gray-400 mb-6">
        A verification code has been sent to **{{ email }}**. Please enter it below.
      </p>

      <!-- ✅ ใช้ v-model ที่ถูกต้อง -->
      <input v-model="code" type="text" placeholder="6-digit code" class="input-style" />

      <button
        @click="handleVerify"
        class="bg-black hover:bg-gray-700 text-white font-semibold py-2 w-full rounded-lg transition duration-200 border border-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:border-white"
      >
        Verify
      </button>

      <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center">{{ errorMsg }}</p>
      <p v-if="successMsg" class="text-green-400 text-sm mt-4 text-center">{{ successMsg }}</p>

      <div class="text-center text-sm text-gray-400 mt-4">
        Didn't receive the code?
        <button @click="resendCode" class="underline hover:text-white">Resend</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// ✅ รับค่าอีเมลจาก URL
const email = ref(route.query.email || '')
const code = ref('')
const errorMsg = ref('')
const successMsg = ref('')

// ✅ หากไม่มีอีเมลใน URL ให้กลับไปหน้า register
onMounted(() => {
  if (!email.value) {
    router.push('/register')
  }
})

const handleVerify = async () => {
  errorMsg.value = ''
  successMsg.value = ''

  if (!email.value || !code.value) {
    errorMsg.value = 'Please enter both email and verification code.'
    return
  }

  try {
    const res = await axios.post('http://localhost:5000/api/verify-code', {
      email: email.value,
      code: code.value
    })
    
    successMsg.value = res.data.msg
    // ✅ นำทางไปหน้า login หลังจากยืนยันสำเร็จ
    setTimeout(() => router.push('/login'), 2000)
    
  } catch (err) {
    console.error('[Verify Code error]', err)
    errorMsg.value = err.response?.data?.msg || 'Verification failed.'
  }
}

const resendCode = async () => {
  errorMsg.value = ''
  successMsg.value = ''

  if (!email.value) {
    errorMsg.value = 'Email is missing. Please return to the registration page.'
    return
  }
  
  try {
    const res = await axios.post('http://localhost:5000/api/resend-verification-code', {
      email: email.value
    })

    successMsg.value = res.data.msg
  } catch (err) {
    console.error('[Resend Code error]', err)
    errorMsg.value = err.response?.data?.msg || 'Failed to resend code.'
  }
}
</script>

<style scoped lang="postcss">
.input-style {
  @apply mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white;
}
</style>