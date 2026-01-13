<template>
  <div class="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
    <!-- Animated Background -->
    <div class="absolute inset-0 bg-gradient-to-br from-dark-950 via-dark-900 to-dark-950">
      <div class="absolute top-1/4 right-1/4 w-96 h-96 bg-accent-500/20 rounded-full blur-3xl animate-pulse-slow"></div>
      <div class="absolute bottom-1/4 left-1/4 w-96 h-96 bg-primary-500/20 rounded-full blur-3xl animate-pulse-slow" style="animation-delay: 2s;"></div>
    </div>

    <!-- Register Card -->
    <div class="relative glass rounded-3xl p-8 w-full max-w-md animate-in">
      <!-- Logo -->
      <div class="text-center mb-6">
        <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-accent-500 to-primary-500 mb-4">
          <span class="text-white font-bold text-xl">P2</span>
        </div>
        <h1 class="text-2xl font-bold text-white">สร้างบัญชีใหม่</h1>
        <p class="text-dark-400 mt-2">เริ่มต้นใช้งาน P2UKAISER</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleRegister" class="space-y-4">
        <!-- Username -->
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-1.5">ชื่อผู้ใช้</label>
          <input
            v-model="username"
            type="text"
            placeholder="กรอกชื่อผู้ใช้ 4-20 ตัวอักษร"
            class="w-full input-glass"
            autocomplete="username"
          />
        </div>

        <!-- Email -->
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-1.5">อีเมล</label>
          <input
            v-model="email"
            type="email"
            placeholder="example@email.com"
            class="w-full input-glass"
            autocomplete="email"
          />
        </div>

        <!-- Full Name -->
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-1.5">ชื่อ-นามสกุล</label>
          <input
            v-model="fullName"
            type="text"
            placeholder="กรอกชื่อ-นามสกุล"
            class="w-full input-glass"
            autocomplete="name"
          />
        </div>

        <!-- Phone -->
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-1.5">เบอร์โทรศัพท์ (ไม่บังคับ)</label>
          <input
            v-model="phoneNumber"
            type="tel"
            placeholder="0812345678"
            class="w-full input-glass"
            autocomplete="tel"
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-1.5">รหัสผ่าน</label>
          <div class="relative">
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="กรอกรหัสผ่าน 6 ตัวขึ้นไป"
              class="w-full input-glass pr-12"
              autocomplete="new-password"
            />
            <button 
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-4 top-1/2 -translate-y-1/2 text-dark-500 hover:text-dark-300 transition-colors"
            >
              <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
              </svg>
              <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
            </button>
          </div>
        </div>

        <!-- Confirm Password -->
        <div>
          <label class="block text-sm font-medium text-dark-300 mb-1.5">ยืนยันรหัสผ่าน</label>
          <input
            v-model="confirmPassword"
            :type="showPassword ? 'text' : 'password'"
            placeholder="กรอกรหัสผ่านอีกครั้ง"
            class="w-full input-glass"
            autocomplete="new-password"
          />
        </div>

        <!-- Error/Success Message -->
        <Transition name="fade">
          <div v-if="message" :class="[
            'flex items-center gap-2 p-3 rounded-xl',
            isSuccess ? 'bg-green-500/20 border border-green-500/30' : 'bg-red-500/20 border border-red-500/30'
          ]">
            <svg :class="['w-5 h-5', isSuccess ? 'text-green-400' : 'text-red-400']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path v-if="isSuccess" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p :class="['text-sm', isSuccess ? 'text-green-400' : 'text-red-400']">{{ message }}</p>
          </div>
        </Transition>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full btn-accent py-3.5 text-center font-semibold mt-2"
        >
          <span v-if="!isLoading">สมัครสมาชิก</span>
          <span v-else class="flex items-center justify-center gap-2">
            <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            กำลังสมัคร...
          </span>
        </button>
      </form>

      <!-- Login Link -->
      <div class="text-center mt-6">
        <p class="text-dark-400 text-sm">
          มีบัญชีอยู่แล้ว?
          <NuxtLink to="/login" class="text-primary-400 hover:text-primary-300 font-medium transition-colors">
            เข้าสู่ระบบ
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

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