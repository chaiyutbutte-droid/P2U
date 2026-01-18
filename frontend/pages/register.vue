<template>
  <div class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-[#020410] font-sans selection:bg-pink-500 selection:text-white">
    
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

    <div class="relative z-20 w-full max-w-5xl animate-in fade-in slide-in-from-bottom-8 duration-700">
        
        <div class="absolute -inset-1 bg-gradient-to-r from-pink-600 via-purple-600 to-cyan-600 rounded-[2.5rem] opacity-40 blur-md animate-tilt"></div>

        <div class="relative bg-[#09090b]/90 border border-white/10 rounded-[2.3rem] shadow-2xl overflow-hidden grid lg:grid-cols-2 min-h-[600px] backdrop-blur-xl">
            
            <div class="relative hidden lg:flex flex-col justify-between p-12 overflow-hidden bg-gradient-to-br from-white/5 to-transparent relative group">
                
                <div class="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_0%_0%,rgba(236,72,153,0.15),transparent_50%)] z-0 pointer-events-none"></div>
                
                <div class="absolute top-[-50px] left-[-50px] w-64 h-64 bg-pink-500/20 rounded-full blur-3xl mix-blend-screen animate-pulse-slow"></div>

                <div class="relative z-10">
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-pink-300 text-[10px] font-bold uppercase tracking-wider mb-6 backdrop-blur-md">
                        <span class="w-1.5 h-1.5 rounded-full bg-pink-400 animate-pulse"></span>
                        Join the Revolution
                    </div>
                    <h1 class="text-5xl font-black leading-tight tracking-tight text-white mb-4 drop-shadow-2xl">
                        START YOUR <br/>
                        <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 via-purple-400 to-cyan-400 animate-gradient-x">LEGACY HERE</span>
                    </h1>
                    <p class="text-gray-400 font-light text-sm leading-relaxed max-w-sm">
                        Create an account to access exclusive collections, track your portfolio, and join the elite P2U community.
                    </p>
                </div>

                <div class="absolute top-[60%] left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full flex justify-center pointer-events-none">
                    <div class="relative w-64 h-40 bg-gradient-to-br from-white/10 to-transparent border border-white/20 rounded-2xl backdrop-blur-sm transform rotate-[-12deg] group-hover:rotate-[-5deg] transition-all duration-700 shadow-2xl">
                        <div class="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700 rounded-2xl"></div>
                        
                        <div class="p-5 flex flex-col justify-between h-full relative z-10">
                            <div class="flex justify-between items-center">
                                <div class="w-8 h-8 rounded-full bg-pink-500/20 flex items-center justify-center border border-pink-500/30">
                                    <span class="text-xs">🚀</span>
                                </div>
                                <div class="h-2 w-16 bg-white/10 rounded-full"></div>
                            </div>
                            <div>
                                <div class="text-[10px] text-gray-400 uppercase tracking-widest">New Member</div>
                                <div class="h-3 w-32 bg-white/20 rounded-full mt-2 animate-pulse"></div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="relative z-10">
                    <div class="flex items-center gap-4 text-xs text-gray-500 font-mono">
                        <div class="flex -space-x-2">
                            <div class="w-8 h-8 rounded-full bg-gray-800 border-2 border-black"></div>
                            <div class="w-8 h-8 rounded-full bg-gray-700 border-2 border-black"></div>
                            <div class="w-8 h-8 rounded-full bg-gray-600 border-2 border-black flex items-center justify-center text-[8px] text-white font-bold">+2k</div>
                        </div>
                        <p>Join 2,000+ collectors today.</p>
                    </div>
                </div>
            </div>

            <div class="relative flex flex-col justify-center p-8 md:p-12 bg-[#09090b]/80 backdrop-blur-xl">
                
                <div class="mb-6">
                    <h2 class="text-2xl font-bold text-white mb-1">Create Account</h2>
                    <p class="text-gray-500 text-xs">Fill in your details to get started.</p>
                </div>

                <form @submit.prevent="handleRegister" class="space-y-4 relative z-10">
                    
                    <div class="space-y-3">
                        <div class="group">
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 ml-1">Username</label>
                            <input
                                v-model="username"
                                type="text"
                                placeholder="Choose a username"
                                class="block w-full px-4 py-3 bg-black/40 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20 focus:bg-black/60 transition-all duration-300 text-sm"
                            />
                        </div>

                        <div class="group">
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 ml-1">Email</label>
                            <input
                                v-model="email"
                                type="email"
                                placeholder="Enter your email"
                                class="block w-full px-4 py-3 bg-black/40 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20 focus:bg-black/60 transition-all duration-300 text-sm"
                            />
                        </div>
                    </div>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div class="group">
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 ml-1">Full Name</label>
                            <input
                                v-model="fullName"
                                type="text"
                                placeholder="Your full name"
                                class="block w-full px-4 py-3 bg-black/40 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20 focus:bg-black/60 transition-all duration-300 text-sm"
                            />
                        </div>

                        <div class="group">
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 ml-1">Phone</label>
                            <input
                                v-model="phoneNumber"
                                type="tel"
                                placeholder="Optional"
                                class="block w-full px-4 py-3 bg-black/40 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20 focus:bg-black/60 transition-all duration-300 text-sm"
                            />
                        </div>
                    </div>

                    <div class="space-y-3">
                        <div class="group relative">
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 ml-1">Password</label>
                            <div class="relative">
                                <input
                                    v-model="password"
                                    :type="showPassword ? 'text' : 'password'"
                                    placeholder="Min 6 characters"
                                    class="block w-full px-4 py-3 bg-black/40 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20 focus:bg-black/60 transition-all duration-300 text-sm pr-10"
                                />
                                <button 
                                    type="button" 
                                    @click="showPassword = !showPassword"
                                    class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-500 hover:text-white transition-colors cursor-pointer"
                                >
                                    {{ showPassword ? '🙈' : '👁️' }}
                                </button>
                            </div>
                        </div>

                        <div class="group">
                            <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1 ml-1">Confirm Password</label>
                            <input
                                v-model="confirmPassword"
                                :type="showPassword ? 'text' : 'password'"
                                placeholder="Re-enter password"
                                class="block w-full px-4 py-3 bg-black/40 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20 focus:bg-black/60 transition-all duration-300 text-sm"
                            />
                        </div>
                    </div>

                    <Transition name="fade">
                        <div v-if="message" :class="[
                            'p-3 rounded-xl border backdrop-blur-sm flex items-center gap-3',
                            isSuccess ? 'bg-green-950/30 border-green-500/30' : 'bg-red-950/30 border-red-500/30'
                        ]">
                            <div :class="['w-2 h-2 rounded-full animate-pulse', isSuccess ? 'bg-green-400' : 'bg-red-400']"></div>
                            <p :class="['text-xs font-medium', isSuccess ? 'text-green-400' : 'text-red-400']">{{ message }}</p>
                        </div>
                    </Transition>

                    <button 
                        type="submit" 
                        :disabled="isLoading"
                        class="w-full relative group overflow-hidden rounded-xl p-[1px] focus:outline-none focus:ring-2 focus:ring-pink-500 z-10 mt-2"
                    >
                        <span class="absolute inset-[-1000%] animate-[spin_3s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2E8F0_0%,#ec4899_50%,#E2E8F0_100%)] opacity-0 group-hover:opacity-100 transition-opacity duration-500"></span>
                        <span class="relative flex items-center justify-center w-full h-full bg-gradient-to-r from-pink-600 to-purple-700 group-hover:from-pink-500 group-hover:to-purple-600 text-white font-bold py-3.5 rounded-xl transition-all duration-300 shadow-lg group-hover:shadow-pink-500/25">
                            <span v-if="isLoading" class="flex items-center gap-2">
                                <svg class="animate-spin h-5 w-5 text-white" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                            </span>
                            <span v-else class="tracking-wide text-sm flex items-center gap-2">
                                SIGN UP
                            </span>
                        </span>
                    </button>
                </form>

                <div class="text-center mt-6">
                    <NuxtLink to="/login" class="text-xs text-gray-400 hover:text-white transition-colors group">
                        Already have an account? 
                        <span class="text-pink-400 font-bold group-hover:underline ml-1">Log in</span>
                    </NuxtLink>
                </div>
            </div>

        </div>
    </div>
    
    <div class="absolute bottom-4 w-full text-center pointer-events-none">
        <p class="text-[10px] text-white/20 tracking-widest uppercase">© 2024 P2UKAISER DESIGN</p>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

// =======================
// Logic Script เดิม 100%
// =======================
const username = ref('');
const email = ref('');
const fullName = ref('');
const phoneNumber = ref('');
const password = ref('');
const confirmPassword = ref('');
const message = ref('');
const isSuccess = ref(false);
const isLoading = ref(false);
const showPassword = ref(false);
const router = useRouter();

const handleRegister = async () => {
  message.value = '';
  
  if (!username.value || !email.value || !fullName.value || !password.value) {
    message.value = 'กรุณากรอกข้อมูลให้ครบ';
    isSuccess.value = false;
    return;
  }

  if (password.value.length < 6) {
    message.value = 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร';
    isSuccess.value = false;
    return;
  }

  if (password.value !== confirmPassword.value) {
    message.value = 'รหัสผ่านไม่ตรงกัน';
    isSuccess.value = false;
    return;
  }

  isLoading.value = true;

  try {
    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('email', email.value);
    formData.append('full_name', fullName.value);
    formData.append('phone_number', phoneNumber.value);
    formData.append('password', password.value);

    const res = await axios.post('http://localhost:5000/api/register', formData);
    
    message.value = 'สมัครสมาชิกสำเร็จ! กรุณาตรวจสอบอีเมลเพื่อยืนยัน';
    isSuccess.value = true;

    setTimeout(() => {
      router.push({ name: 'VerifyEmail', query: { email: email.value } });
    }, 2000);

  } catch (err) {
    console.error('[Register error]', err.response?.data?.msg || err.message);
    message.value = err.response?.data?.msg || 'สมัครสมาชิกไม่สำเร็จ';
    isSuccess.value = false;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Animations Custom */
.animate-pulse-slow {
  animation: pulse 6s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

.animate-tilt {
  animation: tilt 10s infinite linear;
}

@keyframes tilt {
  0%, 50%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(0.5deg); }
  75% { transform: rotate(-0.5deg); }
}

@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}

.animate-blob {
  animation: blob 10s infinite;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

@keyframes gradient-x {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.animate-gradient-x {
  background-size: 200% 200%;
  animation: gradient-x 5s ease infinite;
}

/* NEW ANIMATIONS: Shooting Star & Twinkle */
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