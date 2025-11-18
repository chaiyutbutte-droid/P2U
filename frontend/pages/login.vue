<template>
  <section class="layout-full relative min-h-screen bg-slate-950 text-white overflow-hidden">
    <div class="absolute inset-0 bg-linear-to-br from-slate-950 via-slate-900 to-black"></div>
    <div class="absolute inset-0 opacity-70 pointer-events-none">
      <div class="absolute -right-16 top-10 w-[420px] h-[420px] bg-pink-600/30 blur-3xl rounded-full"></div>
      <div class="absolute left-0 bottom-0 w-[520px] h-[520px] bg-indigo-500/25 blur-3xl rounded-full"></div>
    </div>

    <div class="relative z-10 flex flex-col items-center justify-center min-h-screen px-4 py-12">
      <div class="w-full max-w-[420px] rounded-3xl border border-white/10 bg-white/5 backdrop-blur-2xl p-10 shadow-[0_30px_80px_rgba(2,6,23,0.65)] space-y-8">
        <div class="text-center space-y-3">
          <p class="eyebrow text-pink-200">P2U Kaiser</p>
          <h1 class="text-3xl font-semibold text-glow">ยินดีต้อนรับกลับ</h1>
          <p class="text-sm text-gray-300">เข้าสู่ระบบเพื่อจัดการสินค้าที่คุณรัก</p>
        </div>

        <form class="space-y-6" @submit.prevent="handleLogin">
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <label class="form-label">ชื่อผู้ใช้</label>
              <span class="form-hint">ใช้ชื่อที่จดจำง่าย</span>
            </div>
            <div
              class="group relative rounded-2xl bg-linear-to-r from-white/15 via-transparent to-white/5 p-px transition">
              <div
                class="relative flex items-center rounded-[1.1rem] bg-slate-950/70 px-3 py-1 shadow-[inset_0_12px_40px_rgba(15,23,42,0.65)] group-focus-within:bg-slate-900/70">
                <span class="login-icon group-focus-within:text-white">
                  <i class="bx bxs-user text-lg"></i>
                </span>
                <input v-model="username" placeholder="username" class="input-style pl-12 pr-2" autocomplete="username" />
              </div>
            </div>
          </div>

          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <label class="form-label">รหัสผ่าน</label>
              <span class="form-hint">เก็บข้อมูลของคุณให้ปลอดภัย</span>
            </div>
            <div
              class="group relative rounded-2xl bg-linear-to-r from-white/15 via-transparent to-white/5 p-px transition">
              <div
                class="relative flex items-center rounded-[1.1rem] bg-slate-950/70 px-3 py-1 shadow-[inset_0_12px_40px_rgba(15,23,42,0.65)] group-focus-within:bg-slate-900/70">
                <span class="login-icon group-focus-within:text-white">
                  <i class="bxs-lock-keyhole bx-rotate-90 text-lg"></i>
                </span>
                <input v-model="password" type="password" placeholder="••••••••" class="input-style pl-12 pr-2"
                  autocomplete="current-password" />
              </div>
            </div>
          </div>

          <button type="submit"
            class="w-full rounded-2xl bg-pink-600/90 hover:bg-pink-500 text-white font-semibold py-3 transition shadow-lg shadow-pink-500/30 focus:outline-none focus:ring-2 focus:ring-pink-300 focus:ring-offset-2 focus:ring-offset-slate-950 relative overflow-hidden group"
            :disabled="loading">
            <span class="absolute inset-0 bg-white/20 scale-0 group-hover:scale-110 transition-transform duration-300 rounded-2xl"></span>
            <span class="relative">เข้าสู่ระบบ</span>
          </button>
        </form>

        <p v-if="errorMsg" class="text-center text-sm text-red-300">
          {{ errorMsg }}
        </p>

        <p class="text-center text-sm text-gray-400">
          ไม่มีบัญชี?
          <NuxtLink to="/register" class="text-pink-300 font-semibold hover:text-white transition">
            ลงทะเบียน
          </NuxtLink>
        </p>
      </div>
    </div>
  </section>

  <Loading v-if="loading" />
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import Loading from '@/components/loading.vue';  // นำเข้า Loading.vue

const username = ref('');
const password = ref('');
const errorMsg = ref('');
const loading = ref(false);  // ตัวแปรสำหรับควบคุมการแสดงผลของแอนิเมชัน
const router = useRouter();

const handleLogin = async () => {
  errorMsg.value = '';
  if (!username.value || !password.value) {
    errorMsg.value = 'Please enter a username and password.';
    return;
  }

  loading.value = true;  // เริ่มแอนิเมชันโหลด

  try {
    const res = await axios.post('http://localhost:5000/api/login', {
      username: username.value,
      password: password.value
    });

    const user = res.data.user;

    // ✅ กรณีที่ล็อกอินสำเร็จ
    if (user) {
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('user', JSON.stringify({
        id: user.id,
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        profile_image_url: user.profile_image_url,
        is_seller: user.is_seller
      }));
      window.dispatchEvent(new Event('user-updated'));

      router.push('/dashboard');
    }

  } catch (err) {
    errorMsg.value = err.response?.data?.msg || 'Login failed. Please try again.';
  } finally {
    loading.value = false;  // หยุดแอนิเมชันโหลดเมื่อเสร็จสิ้น
  }
};
</script>

<style lang="postcss" scoped>
.input-style {
  @apply w-full rounded-2xl border-0 bg-transparent px-4 py-4 text-white placeholder-gray-400
    focus:outline-none focus:ring-0 transition;
}

.login-icon {
  @apply absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none transition;
}

.form-label {
  @apply text-xs uppercase tracking-[0.4em] text-gray-300;
}

.form-hint {
  @apply text-[0.65rem] text-gray-500;
}
</style>