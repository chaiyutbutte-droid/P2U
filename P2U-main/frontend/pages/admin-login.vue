<template>
  <div class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Animated Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950">
      <div class="absolute top-1/3 left-1/3 w-64 h-64 bg-red-500/20 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute bottom-1/3 right-1/3 w-64 h-64 bg-orange-500/20 rounded-full blur-3xl animate-pulse-slow" style="animation-delay: 1s;"></div>
    </div>

    <!-- Admin Login Card -->
    <div class="relative glass rounded-3xl p-8 w-full max-w-md animate-in">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-red-500 to-orange-500 mb-4">
          <span class="text-white font-bold text-2xl">👑</span>
        </div>
        <h1 class="text-2xl font-bold text-white">Admin Panel</h1>
        <p class="text-dark-400 mt-2">เข้าสู่ระบบผู้ดูแลระบบ</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleAdminLogin" class="space-y-5">
        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-2">Username</label>
          <input
            v-model="username"
            type="text"
            placeholder="Admin username"
            class="w-full input-glass"
            autocomplete="username"
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-2">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="Admin password"
            class="w-full input-glass"
            autocomplete="current-password"
          />
        </div>

        <!-- Error Message -->
        <Transition name="fade">
          <div v-if="errorMsg" class="flex items-center gap-2 p-3 bg-red-500/20 border border-red-500/30 rounded-xl">
            <svg class="w-5 h-5 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-sm text-red-400">{{ errorMsg }}</p>
          </div>
        </Transition>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full bg-gradient-to-r from-red-500 to-orange-500 hover:from-red-600 hover:to-orange-600 text-white py-3.5 rounded-xl font-semibold transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5"
        >
          <span v-if="!isLoading">เข้าสู่ระบบ Admin</span>
          <span v-else class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            กำลังตรวจสอบ...
          </span>
        </button>
      </form>

      <!-- Back to User Login -->
      <div class="text-center mt-6">
        <NuxtLink to="/login" class="text-dark-400 hover:text-dark-300 text-sm transition-colors">
          ← กลับไปหน้า Login ปกติ
        </NuxtLink>
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
    errorMsg.value = 'กรุณากรอก username และ password';
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
    errorMsg.value = err.response?.data?.msg || 'รหัสผ่าน Admin ไม่ถูกต้อง';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
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
