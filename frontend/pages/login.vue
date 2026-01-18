<template>
  <div class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-[#020410] font-sans selection:bg-pink-500 selection:text-white">
    
    <div class="absolute inset-0 pointer-events-none overflow-hidden">
        
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_0%,rgba(50,10,100,0.3),transparent_70%)] z-0"></div>
        <div class="absolute inset-0 bg-[radial-gradient(circle_at_100%_100%,rgba(20,5,50,0.4),transparent_60%)] z-0"></div>
        
        <div class="absolute top-[-10%] left-[-10%] w-[60vw] h-[60vw] bg-indigo-900/20 rounded-full blur-[120px] animate-blob mix-blend-screen"></div>
        <div class="absolute top-[20%] right-[-20%] w-[50vw] h-[50vw] bg-fuchsia-900/20 rounded-full blur-[120px] animate-blob animation-delay-2000 mix-blend-screen"></div>
        <div class="absolute bottom-[-20%] left-[20%] w-[60vw] h-[60vw] bg-cyan-900/10 rounded-full blur-[120px] animate-blob animation-delay-4000 mix-blend-screen"></div>

        <div class="absolute inset-0 z-0">
            <div class="absolute top-1/4 left-1/4 w-1 h-1 bg-white rounded-full animate-twinkle opacity-60"></div>
            <div class="absolute top-1/3 left-2/3 w-0.5 h-0.5 bg-white rounded-full animate-twinkle animation-delay-2000 opacity-50"></div>
            <div class="absolute top-2/3 left-1/5 w-1 h-1 bg-pink-300 rounded-full animate-twinkle animation-delay-4000 opacity-70"></div>
            <div class="absolute bottom-1/4 right-1/4 w-0.5 h-0.5 bg-cyan-300 rounded-full animate-twinkle animation-delay-1000 opacity-60"></div>
            <div class="absolute top-10 right-20 w-1 h-1 bg-white rounded-full animate-twinkle animation-delay-3000 opacity-40"></div>
             <div class="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-10 brightness-150 contrast-150 mix-blend-overlay"></div>
        </div>

        <div class="absolute top-0 right-0 w-[300px] h-[1px] bg-gradient-to-l from-transparent via-white to-transparent opacity-0 animate-shooting-star rotate-[-45deg] origin-right"></div>
        <div class="absolute top-[20%] right-[-10%] w-[200px] h-[1px] bg-gradient-to-l from-transparent via-cyan-300 to-transparent opacity-0 animate-shooting-star animation-delay-4000 rotate-[-45deg] origin-right"></div>
        
        <div class="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:50px_50px] [mask-image:radial-gradient(ellipse_at_center,black_40%,transparent_100%)] z-0 pointer-events-none transform scale-125 opacity-30"></div>
    </div>

    <div class="relative z-20 w-full max-w-5xl animate-in fade-in slide-in-from-bottom-8 duration-700">
      
      <div class="absolute -inset-1 bg-gradient-to-r from-pink-600 via-purple-600 to-cyan-600 rounded-[2.5rem] opacity-40 blur-md group-hover:opacity-100 transition duration-1000 animate-tilt"></div>

      <div class="relative bg-[#09090b]/90 border border-white/10 rounded-[2.3rem] shadow-2xl overflow-hidden grid lg:grid-cols-2 min-h-[600px] backdrop-blur-md">
        
        <div class="relative hidden lg:flex flex-col justify-between p-12 overflow-hidden group">
            
            <div class="absolute top-0 left-0 w-full h-full bg-[radial-gradient(circle_at_0%_0%,rgba(236,72,153,0.1),transparent_60%)] z-0 pointer-events-none"></div>
            
            <div class="absolute inset-0 flex justify-between px-10 z-0 pointer-events-none opacity-20">
                <div class="w-[1px] h-full bg-gradient-to-b from-transparent via-pink-500 to-transparent animate-scan"></div>
                <div class="w-[1px] h-full bg-gradient-to-b from-transparent via-cyan-500 to-transparent animate-scan animation-delay-2000"></div>
            </div>

            <div class="absolute -bottom-20 -left-10 z-0 pointer-events-none select-none mix-blend-overlay opacity-60">
                <h1 class="text-[10rem] font-black text-white/5 leading-none tracking-tighter">
                    KAI<br/>SER
                </h1>
            </div>

            <div class="absolute top-[-80px] right-[-80px] w-[500px] h-[500px] border border-white/5 rounded-full z-0 animate-[spin_60s_linear_infinite] opacity-60"></div>
            <div class="absolute top-[-40px] right-[-40px] w-[400px] h-[400px] border border-dashed border-white/10 rounded-full z-0 animate-[spin_40s_linear_infinite_reverse] opacity-60"></div>

            <div class="relative z-20">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/5 border border-white/10 text-gray-300 text-[10px] font-bold uppercase tracking-wider mb-6 backdrop-blur-md hover:bg-white/10 transition-colors">
                    <span class="w-1.5 h-1.5 rounded-full bg-green-400 animate-pulse"></span>
                    Exclusive Access
                </div>
                <h1 class="text-5xl font-black leading-tight tracking-tight text-white mb-2 drop-shadow-2xl">
                    CURATED <br/>
                    <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 via-purple-400 to-cyan-400 animate-gradient-x">COLLECTION</span>
                </h1>
                <p class="text-gray-300 font-light text-sm leading-relaxed max-w-sm mt-4 border-l-2 border-pink-500/50 pl-4 bg-black/20 backdrop-blur-sm p-2 rounded-r-lg">
                    Discover the rarest vintage pieces. <br/> Authentication guaranteed.
                </p>
            </div>

            <div class="absolute top-[35%] right-[-40px] transform -translate-y-1/2 translate-x-0 z-10">
                 <div class="relative w-60 h-96 transition-all duration-500 transform rotate-[-12deg] hover:rotate-0 perspective-1000 group/card">
                    <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-white/5 border border-white/20 rounded-2xl shadow-2xl backdrop-blur-md overflow-hidden transition-all duration-500 group-hover/card:scale-105 group-hover/card:shadow-[0_0_50px_rgba(236,72,153,0.3)]">
                        <div class="absolute inset-0 bg-gradient-to-tr from-transparent via-white/20 to-transparent rotate-45 translate-y-full group-hover/card:translate-y-[-200%] transition-transform duration-1000 ease-in-out"></div>
                        
                        <div class="p-6 h-full flex flex-col justify-between relative z-10">
                            <div class="flex justify-between items-start">
                                <span class="text-3xl">👑</span>
                                <div class="w-8 h-8 rounded-full border border-white/30 flex items-center justify-center bg-black/20">
                                    <div class="w-2 h-2 bg-pink-500 rounded-full animate-pulse"></div>
                                </div>
                            </div>
                            <div>
                                <div class="text-[9px] text-gray-400 uppercase tracking-widest mb-1">Member</div>
                                <div class="text-lg font-bold font-mono tracking-wider text-white">P2U KAISER</div>
                                <div class="text-[9px] text-gray-500 mt-2 font-mono">ID: 8888-9999</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="relative z-20 flex gap-6">
                 <div class="p-3 rounded-xl bg-black/40 border border-white/10 backdrop-blur-md hover:bg-white/5 transition-colors cursor-pointer">
                    <div class="text-xl font-bold text-white">12k+</div>
                    <div class="text-[10px] text-gray-500 uppercase tracking-wider">Items Sold</div>
                 </div>
                 <div class="p-3 rounded-xl bg-black/40 border border-white/10 backdrop-blur-md hover:bg-white/5 transition-colors cursor-pointer">
                    <div class="text-xl font-bold text-white">4.9★</div>
                    <div class="text-[10px] text-gray-500 uppercase tracking-wider">Rating</div>
                 </div>
            </div>

        </div>

        <div class="relative flex flex-col justify-center p-8 md:p-12 bg-[#09090b]/80 backdrop-blur-xl">
            
            <div class="absolute top-6 right-6 rotate-12 animate-pulse-slow">
                <span class="px-3 py-1 bg-yellow-400 text-black text-[10px] font-black uppercase tracking-widest border border-yellow-200 shadow-[0_0_15px_rgba(250,204,21,0.4)] transform hover:scale-110 transition-transform cursor-default">
                    VERIFIED SELLER
                </span>
            </div>

            <div class="mb-8">
                <div class="flex items-center gap-3 mb-2">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-pink-600 to-purple-600 flex items-center justify-center shadow-lg">
                        <span class="text-lg">👑</span>
                    </div>
                    <h1 class="text-2xl font-black text-white tracking-tight">
                        <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-500 to-purple-500">P2U</span>KAISER
                    </h1>
                </div>
                <p class="text-gray-500 text-xs">Sign in to manage your collection.</p>
            </div>

            <form @submit.prevent="handleLogin" class="space-y-5">
                <div class="group">
                    <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 ml-1 group-focus-within:text-pink-500 transition-colors">Username</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none z-20">
                            <span class="text-gray-500 group-focus-within:text-pink-400 transition-colors">👤</span>
                        </div>
                        <input 
                            v-model="username" 
                            type="text" 
                            class="block w-full pl-11 pr-4 py-3.5 bg-black/40 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20 focus:bg-black/60 transition-all duration-300 sm:text-sm relative z-10" 
                            placeholder="กรอกชื่อผู้ใช้"
                            required
                        />
                    </div>
                </div>

                <div class="group">
                    <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5 ml-1 group-focus-within:text-pink-500 transition-colors">Password</label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none z-20">
                            <span class="text-gray-500 group-focus-within:text-pink-400 transition-colors">🔒</span>
                        </div>
                        <input 
                            v-model="password" 
                            :type="showPassword ? 'text' : 'password'" 
                            class="block w-full pl-11 pr-12 py-3.5 bg-black/40 border border-white/10 rounded-xl text-white placeholder-gray-600 focus:outline-none focus:border-pink-500/50 focus:ring-2 focus:ring-pink-500/20 focus:bg-black/60 transition-all duration-300 sm:text-sm relative z-10" 
                            placeholder="กรอกรหัสผ่าน"
                            required
                        />
                        <button 
                            type="button" 
                            @click="showPassword = !showPassword"
                            class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-500 hover:text-white transition-colors cursor-pointer z-20"
                        >
                            {{ showPassword ? '🙈' : '👁️' }}
                        </button>
                    </div>
                </div>

                <div v-if="errorMessage" class="p-3 rounded-xl bg-red-950/30 border border-red-500/30 backdrop-blur-sm animate-pulse">
                    <p class="text-red-400 text-xs text-center font-medium flex items-center justify-center gap-2">
                        🚫 {{ errorMessage }}
                    </p>
                </div>

                <button 
                    type="submit" 
                    :disabled="isLoading"
                    class="w-full relative group overflow-hidden rounded-xl p-[1px] focus:outline-none focus:ring-2 focus:ring-pink-500 focus:ring-offset-2 focus:ring-offset-black z-10 mt-2"
                >
                    <span class="absolute inset-[-1000%] animate-[spin_3s_linear_infinite] bg-[conic-gradient(from_90deg_at_50%_50%,#E2E8F0_0%,#ec4899_50%,#E2E8F0_100%)] opacity-0 group-hover:opacity-100 transition-opacity duration-500"></span>
                    <span class="relative flex items-center justify-center w-full h-full bg-gradient-to-r from-pink-600 to-purple-700 group-hover:from-pink-500 group-hover:to-purple-600 text-white font-bold py-3.5 rounded-xl transition-all duration-300 shadow-[0_0_20px_rgba(236,72,153,0.3)] group-hover:shadow-[0_0_35px_rgba(236,72,153,0.6)]">
                        <span v-if="isLoading" class="flex items-center gap-2">
                            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                        </span>
                        <span v-else class="flex items-center gap-2 tracking-wide text-sm">
                            LOGIN TO ACCOUNT 
                        </span>
                    </span>
                </button>
            </form>

            <div class="mt-8 flex flex-col gap-4 text-center">
                <div class="relative flex items-center py-2">
                    <div class="flex-grow border-t border-white/10"></div>
                    <span class="flex-shrink-0 mx-4 text-gray-500 text-[10px] uppercase tracking-widest">New User?</span>
                    <div class="flex-grow border-t border-white/10"></div>
                </div>
                
                <NuxtLink to="/register" class="text-sm text-gray-400 hover:text-white transition-colors">
                    Don't have an account? <span class="text-pink-400 font-bold hover:underline">Register Here</span>
                </NuxtLink>
                
                 <NuxtLink to="/admin-login" class="text-[10px] text-gray-600 hover:text-pink-500 transition-colors mt-2">
                    🔐 Administrator Access
                </NuxtLink>
            </div>
        </div>

      </div>
    </div>
    
    <div class="absolute bottom-4 w-full text-center">
        <p class="text-[10px] text-white/20 tracking-widest uppercase">© 2024 P2UKAISER DESIGN</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const username = ref('');
const password = ref('');
const showPassword = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

async function handleLogin() {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    const res = await axios.post('http://localhost:5000/api/login', {
      username: username.value,
      password: password.value
    });

    if (res.data.msg === 'Please verify your email first.') {
      errorMessage.value = 'กรุณายืนยันอีเมลก่อนเข้าสู่ระบบ';
      return;
    }

    localStorage.setItem('token', res.data.access_token);
    localStorage.setItem('user', JSON.stringify(res.data.user));
    window.dispatchEvent(new Event('user-updated'));
    router.push('/dashboard');
  } catch (err) {
    errorMessage.value = err.response?.data?.msg || 'เข้าสู่ระบบไม่สำเร็จ';
  } finally {
    isLoading.value = false;
  }
}
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

.animation-delay-2000 {
  animation-delay: 2s;
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

.perspective-1000 {
  perspective: 1000px;
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

.animation-delay-1000 {
  animation-delay: 1s;
}

.animation-delay-3000 {
  animation-delay: 3s;
}

@keyframes scan {
  0% { top: -100%; }
  100% { top: 100%; }
}

.animate-scan {
  position: relative;
  overflow: hidden;
}

.animate-scan::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 50px;
  background: linear-gradient(to bottom, transparent, rgba(255,255,255,0.5), transparent);
  animation: scan-move 4s linear infinite;
}

@keyframes scan-move {
  0% { transform: translateY(-100%); opacity: 0; }
  10% { opacity: 1; }
  90% { opacity: 1; }
  100% { transform: translateY(800px); opacity: 0; }
}
</style>