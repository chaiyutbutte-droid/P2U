<template>
  <div class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-[#0b0b0f] font-sans selection:bg-red-500/30">
    
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-red-600/20 rounded-full blur-[120px] mix-blend-screen animate-pulse-slow"></div>
      <div class="absolute bottom-[-10%] right-[-10%] w-[500px] h-[500px] bg-orange-600/10 rounded-full blur-[100px] mix-blend-screen animate-pulse-slow" style="animation-delay: 2s;"></div>
      
      <div class="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_60%_at_50%_50%,#000_70%,transparent_100%)]"></div>
    </div>

    <div class="relative w-full max-w-md z-10 animate-fade-in-up">
      <div class="bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl relative overflow-hidden group">
        
        <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-red-500 via-orange-500 to-transparent opacity-70"></div>

        <div class="text-center mb-10">
          <div class="relative inline-block mb-4">
            <div class="absolute inset-0 bg-red-500 blur-xl opacity-20 animate-pulse"></div>
            <div class="relative w-20 h-20 rounded-2xl bg-gradient-to-br from-red-600 to-orange-600 flex items-center justify-center shadow-lg shadow-red-500/20">
              <span class="text-4xl filter drop-shadow-md">🛡️</span>
            </div>
          </div>
          <h1 class="text-3xl font-bold text-white tracking-wide">Admin Portal</h1>
          <p class="text-gray-400 text-sm mt-2 font-medium">ระบบจัดการและดูแลความเรียบร้อย</p>
        </div>

        <form @submit.prevent="handleAdminLogin" class="space-y-6">
          
          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-500 uppercase tracking-wider ml-1">บัญชีผู้ดูแล</label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-500 group-focus-within:text-red-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
              <input
                v-model="username"
                type="text"
                class="w-full pl-11 pr-4 py-3.5 rounded-xl bg-white/5 border border-white/10 focus:border-red-500/50 focus:bg-white/10 text-white placeholder-gray-600 transition-all outline-none focus:ring-4 focus:ring-red-500/10"
                placeholder="Admin Username"
                autocomplete="username"
              />
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-xs font-bold text-gray-500 uppercase tracking-wider ml-1">รหัสผ่าน</label>
            <div class="relative group">
              <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-500 group-focus-within:text-orange-500 transition-colors" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                v-model="password"
                type="password"
                class="w-full pl-11 pr-4 py-3.5 rounded-xl bg-white/5 border border-white/10 focus:border-orange-500/50 focus:bg-white/10 text-white placeholder-gray-600 transition-all outline-none focus:ring-4 focus:ring-orange-500/10"
                placeholder="Admin Password"
                autocomplete="current-password"
              />
            </div>
          </div>

          <Transition name="fade">
            <div v-if="errorMsg" class="flex items-center gap-3 p-4 bg-red-500/10 border border-red-500/20 rounded-xl">
              <div class="flex-shrink-0 w-8 h-8 rounded-full bg-red-500/20 flex items-center justify-center">
                <svg class="w-4 h-4 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <p class="text-sm text-red-200">{{ errorMsg }}</p>
            </div>
          </Transition>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full py-4 bg-gradient-to-r from-red-600 to-orange-600 hover:from-red-500 hover:to-orange-500 rounded-xl font-bold text-white transition-all duration-300 shadow-[0_0_20px_rgba(220,38,38,0.3)] hover:shadow-[0_0_30px_rgba(220,38,38,0.5)] transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 group relative overflow-hidden"
          >
             <div class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
            <span v-if="!isLoading" class="relative z-10 flex items-center gap-2">
              เข้าสู่ระบบ System
              <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </span>
            <span v-else class="flex items-center gap-2 relative z-10">
              <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              กำลังตรวจสอบสิทธิ์...
            </span>
          </button>
        </form>

        <div class="mt-8 pt-6 border-t border-white/5 text-center">
           <NuxtLink to="/login" class="inline-flex items-center gap-2 text-gray-500 hover:text-white transition-colors text-sm group">
            <span class="group-hover:-translate-x-1 transition-transform">←</span>
            <span>กลับสู่หน้า Login ปกติ</span>
          </NuxtLink>
        </div>

      </div>
      
      <div class="text-center mt-6 opacity-30">
        <p class="text-[10px] tracking-[0.3em] font-mono text-gray-500">SECURE SYSTEM V.2.0.4</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const errorMsg = ref('');
const isLoading = ref(false);
const router = useRouter();

const handleAdminLogin = async () => {
  errorMsg.value = '';
  
  if (!username.value || !password.value) {
    errorMsg.value = 'กรุณากรอก Username และ Password';
    return;
  }

  isLoading.value = true;

  try {
    const res = await axios.post('http://localhost:5000/api/admin/login', {
      username: username.value,
      password: password.value
    });

    localStorage.setItem('admin_token', res.data.access_token);
    localStorage.setItem('admin_user', JSON.stringify(res.data.user));

    router.push('/admin-dashboard');

  } catch (err) {
    console.error('[Admin Login error]', err.response?.data?.msg || err.message);
    errorMsg.value = err.response?.data?.msg || 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Animation Utilities */
.animate-fade-in-up {
  animation: fadeInUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse-slow {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.1); }
}
.animate-pulse-slow {
  animation: pulse-slow 6s ease-in-out infinite;
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