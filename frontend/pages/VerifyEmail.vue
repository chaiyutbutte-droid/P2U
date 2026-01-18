<template>
  <div class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-[#020410] font-sans selection:bg-pink-500 selection:text-white z-50">
    
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(50,10,100,0.3),transparent_70%)] z-0"></div>
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_100%_100%,rgba(20,5,50,0.4),transparent_60%)] z-0"></div>
        <div class="absolute top-[-10%] left-[-10%] w-[60vw] h-[60vw] bg-indigo-900/20 rounded-full blur-[120px] animate-blob mix-blend-screen"></div>
        <div class="absolute bottom-[-20%] right-[-10%] w-[60vw] h-[60vw] bg-pink-900/10 rounded-full blur-[120px] animate-blob animation-delay-4000 mix-blend-screen"></div>

        <div class="absolute inset-0 z-0">
            <div class="absolute top-1/4 left-1/4 w-1 h-1 bg-white rounded-full animate-twinkle opacity-60"></div>
            <div class="absolute top-2/3 left-1/5 w-1 h-1 bg-pink-300 rounded-full animate-twinkle animation-delay-4000 opacity-70"></div>
            <div class="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10 brightness-150 contrast-150 mix-blend-overlay"></div>
        </div>

        <div class="absolute top-0 right-0 w-[300px] h-[1px] bg-gradient-to-l from-transparent via-white to-transparent opacity-0 animate-shooting-star rotate-[-45deg] origin-right"></div>
    </div>

    <div class="relative z-20 w-full max-w-md animate-in fade-in zoom-in duration-500">
        
        <div class="absolute -inset-0.5 bg-gradient-to-r from-pink-600 via-purple-600 to-cyan-600 rounded-[2rem] opacity-40 blur-md animate-tilt"></div>

        <div class="relative bg-[#09090b]/90 border border-white/10 rounded-[1.8rem] shadow-2xl p-8 backdrop-blur-xl overflow-hidden">
            
            <div class="absolute top-0 right-0 p-4 opacity-20">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="1">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
            </div>

            <div class="text-center mb-8 relative z-10">
                <div class="w-16 h-16 mx-auto bg-gradient-to-br from-pink-500/20 to-purple-500/20 rounded-full flex items-center justify-center mb-4 border border-pink-500/30 shadow-[0_0_15px_rgba(236,72,153,0.3)]">
                    <span class="text-2xl animate-pulse">🔐</span>
                </div>
                <h1 class="text-3xl font-black text-white mb-2 tracking-tight">VERIFY IDENTITY</h1>
                <p class="text-gray-400 text-xs font-light">
                    Security code sent to <br/>
                    <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-cyan-400 font-bold text-sm">{{ email }}</span>
                </p>
            </div>

            <div class="space-y-6 relative z-10">
                
                <div class="group">
                    <label class="block text-[10px] font-bold text-center text-gray-500 uppercase tracking-[0.2em] mb-2">Enter 6-Digit Code</label>
                    <input 
                        v-model="code" 
                        type="text" 
                        maxlength="6"
                        placeholder="• • • • • •" 
                        class="block w-full px-4 py-4 bg-black/40 border border-white/10 rounded-xl text-white text-center text-2xl font-mono tracking-[0.5em] placeholder-gray-700 focus:outline-none focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20 focus:bg-black/60 transition-all duration-300 shadow-inner" 
                    />
                </div>

                <button 
                    @click="handleVerify"
                    class="w-full relative group overflow-hidden rounded-xl p-[1px] focus:outline-none focus:ring-2 focus:ring-pink-500"
                >
                    <span class="absolute inset-[-1000%] animate-[spin_3s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2E8F0_0%,#ec4899_50%,#E2E8F0_100%)] opacity-0 group-hover:opacity-100 transition-opacity duration-500"></span>
                    <span class="relative flex items-center justify-center w-full h-full bg-gradient-to-r from-gray-900 to-black group-hover:from-gray-800 group-hover:to-gray-900 text-white font-bold py-3.5 rounded-xl transition-all duration-300 border border-white/10 group-hover:border-transparent">
                        <span class="tracking-widest text-sm">CONFIRM</span>
                    </span>
                </button>

                <Transition name="fade">
                    <div v-if="errorMsg" class="p-3 rounded-lg bg-red-950/30 border border-red-500/30 flex items-center justify-center gap-2">
                        <span class="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse"></span>
                        <p class="text-xs text-red-400 font-medium">{{ errorMsg }}</p>
                    </div>
                </Transition>
                <Transition name="fade">
                    <div v-if="successMsg" class="p-3 rounded-lg bg-green-950/30 border border-green-500/30 flex items-center justify-center gap-2">
                        <span class="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></span>
                        <p class="text-xs text-green-400 font-medium">{{ successMsg }}</p>
                    </div>
                </Transition>

                <div class="text-center pt-2">
                    <p class="text-[10px] text-gray-500 uppercase tracking-wider mb-2">Code not received?</p>
                    <button 
                        @click="resendCode" 
                        class="text-xs text-gray-400 hover:text-pink-400 transition-colors underline decoration-dotted underline-offset-4 hover:decoration-solid"
                    >
                        Resend Verification Email
                    </button>
                </div>

            </div>
        </div>
        
        <div class="text-center mt-6 opacity-30 hover:opacity-100 transition-opacity duration-500">
             <p class="text-[10px] text-white tracking-[0.3em] uppercase">Secured by P2UKaiser</p>
        </div>

    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// ==========================================
// ✅ จุดสำคัญ: สั่งปิด Layout (Navbar/Footer)
// ==========================================
definePageMeta({
  layout: false 
  // หรือใช้ layout: 'empty' หากคุณมีไฟล์ layouts/empty.vue
})

// =======================
// Logic Script เดิม 100%
// =======================
const router = useRouter()
const route = useRoute()

// รับค่าอีเมลจาก URL
const email = ref(route.query.email || '')
const code = ref('')
const errorMsg = ref('')
const successMsg = ref('')

// หากไม่มีอีเมลใน URL ให้กลับไปหน้า register
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
    // นำทางไปหน้า login หลังจากยืนยันสำเร็จ
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

<style scoped>
/* Reuse Animations from Register Page */
.animate-blob {
  animation: blob 10s infinite;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}

@keyframes shooting-star {
  0% { transform: translateX(0) translateY(0); opacity: 1; }
  70% { opacity: 1; }
  100% { transform: translateX(-300px) translateY(300px); opacity: 0; }
}

.animate-shooting-star {
  animation: shooting-star 5s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1.2); box-shadow: 0 0 10px white; }
}

.animate-twinkle {
  animation: twinkle 3s ease-in-out infinite;
}

.animate-tilt {
  animation: tilt 10s infinite linear;
}

@keyframes tilt {
  0%, 50%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(0.5deg); }
  75% { transform: rotate(-0.5deg); }
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>