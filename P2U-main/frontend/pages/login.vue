<template>
  <div class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950">
      <div class="absolute top-1/4 left-1/4 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl animate-pulse"></div>
      <div class="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent-500/20 rounded-full blur-3xl animate-pulse" style="animation-delay: 2s;"></div>
    </div>

    <!-- Login Card -->
    <div class="relative glass rounded-3xl p-8 w-full max-w-md animate-in">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 mb-4">
          <span class="text-3xl">👑</span>
        </div>
        <h1 class="text-2xl font-bold text-white">ยินดีต้อนรับกลับ</h1>
        <p class="text-dark-400 mt-2">เข้าสู่ระบบเพื่อใช้งาน P2UKAISER</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleLogin" class="space-y-5">
        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-2">ชื่อผู้ใช้</label>
          <div class="relative">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-dark-400">👤</span>
            <input 
              v-model="username" 
              type="text" 
              placeholder="กรอกชื่อผู้ใช้"
              class="w-full input-glass pl-12"
              required
            />
          </div>
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-2">รหัสผ่าน</label>
          <div class="relative">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-dark-400">🔒</span>
            <input 
              v-model="password" 
              :type="showPassword ? 'text' : 'password'" 
              placeholder="กรอกรหัสผ่าน"
              class="w-full input-glass pl-12 pr-12"
              required
            />
            <button 
              type="button" 
              @click="showPassword = !showPassword"
              class="absolute right-4 top-1/2 -translate-y-1/2 text-dark-400 hover:text-white"
            >
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="text-red-400 text-sm text-center">{{ errorMessage }}</p>

        <!-- Submit -->
        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full btn-primary py-3 text-lg"
        >
          {{ isLoading ? '⏳ กำลังเข้าสู่ระบบ...' : '🚀 เข้าสู่ระบบ' }}
        </button>
      </form>

      <!-- Divider -->
      <div class="flex items-center my-6">
        <div class="flex-1 h-px bg-white/10"></div>
        <span class="px-4 text-dark-400 text-sm">หรือ</span>
        <div class="flex-1 h-px bg-white/10"></div>
      </div>

      <!-- Links -->
      <div class="text-center space-y-3">
        <p class="text-dark-400 text-sm">
          ยังไม่มีบัญชี? 
          <NuxtLink to="/register" class="text-primary-400 hover:text-primary-300 font-medium">สมัครสมาชิก</NuxtLink>
        </p>
        <NuxtLink to="/admin-login" class="text-accent-400 hover:text-accent-300 text-sm">
          Admin Login
        </NuxtLink>
      </div>
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