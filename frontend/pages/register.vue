<template>
  <section class="layout-full relative min-h-screen bg-slate-950 text-white py-12 overflow-hidden">
    <div class="absolute inset-0 bg-linear-to-br from-gray-950 via-slate-950 to-black"></div>
    <div class="absolute inset-0 pointer-events-none opacity-60">
      <div class="absolute -left-24 top-10 w-[520px] h-[520px] bg-pink-600/20 blur-3xl rounded-full"></div>
      <div class="absolute right-0 -bottom-20 w-[480px] h-[480px] bg-indigo-500/15 blur-3xl rounded-full"></div>
    </div>

    <div class="relative z-10 w-full max-w-6xl mx-auto px-4">
      <div class="grid gap-8 lg:grid-cols-[1.05fr_0.95fr] items-stretch">
        <article
          class="rounded-3xl border border-white/10 bg-white/5 backdrop-blur-3xl p-10 flex flex-col gap-10 shadow-[0_35px_90px_rgba(15,23,42,0.65)]">
          <div class="space-y-6">
            <p class="eyebrow text-pink-200">P2U KAISER</p>
            <h1 class="text-4xl lg:text-5xl font-bold leading-tight text-glow">
              ยินดีต้อนรับสู่คอมมูนิตี้นักสะสมยุคใหม่
            </h1>
            <p class="text-gray-100 text-lg">
              ซื้อขายของสะสมและสินค้า preloved ด้วยระบบความปลอดภัยที่ไว้ใจได้ พร้อมบริการช่วยเหลือผู้ขายและผู้ซื้อครบวงจร
            </p>
          </div>

          <div class="space-y-4">
            <div class="flex items-center gap-3 text-gray-100">
              <span class="flex h-10 w-10 items-center justify-center rounded-full bg-white/15 text-xl">✨</span>
              <p>รับเหรียญ P2U Coin และสิทธิพิเศษจากกิจกรรมประจำเดือน</p>
            </div>
            <div class="flex items-center gap-3 text-gray-100">
              <span class="flex h-10 w-10 items-center justify-center rounded-full bg-white/15 text-xl">🛡️</span>
              <p>ระบบยืนยันผู้ใช้และร้านค้าเพื่อเพิ่มความน่าเชื่อถือ</p>
            </div>
            <div class="flex items-center gap-3 text-gray-100">
              <span class="flex h-10 w-10 items-center justify-center rounded-full bg-white/15 text-xl">🚀</span>
              <p>เพิ่มยอดขายได้ไวขึ้นด้วยหน้า Shop และแคมเปญโปรโมต</p>
            </div>
          </div>

          <div class="grid gap-6 sm:grid-cols-3 text-center">
            <div>
              <p class="text-3xl font-bold">+12K</p>
              <p class="text-sm text-gray-300 mt-1">ผู้ใช้เชื่อใจ</p>
            </div>
            <div>
              <p class="text-3xl font-bold">24/7</p>
              <p class="text-sm text-gray-300 mt-1">เจ้าหน้าที่ดูแล</p>
            </div>
            <div>
              <p class="text-3xl font-bold">฿8.5M</p>
              <p class="text-sm text-gray-300 mt-1">มูลค่าสินค้าหมุนเวียน</p>
            </div>
          </div>
        </article>

        <div
          class="rounded-3xl border border-white/10 bg-slate-950/80 backdrop-blur-2xl p-8 sm:p-10 shadow-[0_25px_70px_rgba(2,6,23,0.75)] space-y-6">
          <div class="space-y-2 text-center">
            <p class="text-sm uppercase tracking-[0.45em] text-pink-300">สร้างบัญชีใหม่</p>
            <h2 class="text-3xl font-semibold">เข้าร่วม P2U Kaiser</h2>
            <p class="text-gray-400 text-sm">
              กรอกข้อมูลให้ครบถ้วนเพื่อเริ่มขายและซื้อสินค้าที่คุณรัก
            </p>
          </div>

          <form class="space-y-5" @submit.prevent="handleRegister">
            <div class="grid gap-4 md:grid-cols-2">
              <div>
                <label class="text-sm text-gray-300">ชื่อผู้ใช้</label>
                <input v-model="username" class="input-style" placeholder="username"
                  autocomplete="username" />
              </div>
              <div>
                <label class="text-sm text-gray-300">อีเมล</label>
                <input v-model="email" type="email" class="input-style" placeholder="your@email.com"
                  autocomplete="email" />
              </div>
            </div>

            <div class="grid gap-4 md:grid-cols-2">
              <div>
                <label class="text-sm text-gray-300">รหัสผ่าน</label>
                <input v-model="password" type="password" class="input-style" placeholder="••••••••"
                  autocomplete="new-password" />
              </div>
              <div>
                <label class="text-sm text-gray-300">ยืนยันรหัสผ่าน</label>
                <input v-model="confirmPassword" type="password" class="input-style" placeholder="••••••••"
                  autocomplete="new-password" />
              </div>
            </div>

            <div class="grid gap-4 md:grid-cols-2">
              <div>
                <label class="text-sm text-gray-300">ชื่อ - นามสกุล</label>
                <input v-model="full_name" class="input-style" placeholder="ชื่อ-นามสกุล" autocomplete="name" />
              </div>
              <div>
                <label class="text-sm text-gray-300">เบอร์โทรศัพท์</label>
                <input v-model="phone_number" class="input-style" placeholder="08X-XXX-XXXX" autocomplete="tel" />
              </div>
            </div>

            <div>
              <label class="text-sm text-gray-300">รูปภาพโปรไฟล์</label>
              <label
                class="mt-2 flex items-center justify-between rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-gray-300 cursor-pointer hover:border-pink-400 transition">
                <span>{{ profile_image?.name || 'อัปโหลดไฟล์ .png หรือ .jpg' }}</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24">
                  <path fill="currentColor"
                    d="M12 16q.425 0 .713-.288T13 15v-3h3q.425 0 .713-.288T17 11t-.288-.712T16 10h-3V7q0-.425-.288-.712T12 6t-.712.288T11 7v3H8q-.425 0-.712.288T7 11t.288.712T8 12h3v3q0 .425.288.713T12 16m0 6q-2.075 0-3.9-.788t-3.2-2.137t-2.138-3.2T2 12t.762-3.875t2.138-3.2T8.1 2.788T12 2t3.9.788t3.2 2.137t2.137 3.2T22 12q0 2.05-.762 3.875t-2.138 3.2t-3.2 2.137T12 22" />
                </svg>
                <input type="file" class="sr-only" @change="handleImageUpload" />
              </label>
            </div>

            <button type="submit"
              class="w-full rounded-2xl bg-pink-600/90 hover:bg-pink-500 text-white font-semibold py-3 transition shadow-lg shadow-pink-500/25 focus:outline-none focus:ring-2 focus:ring-pink-300 focus:ring-offset-2 focus:ring-offset-slate-950">
              ลงทะเบียน
            </button>
          </form>

          <p v-if="errorMsg" class="text-center text-sm text-red-300">
            {{ errorMsg }}
          </p>

          <p class="text-center text-sm text-gray-400">
            มีบัญชีอยู่แล้ว?
            <NuxtLink to="/login" class="text-pink-300 font-semibold hover:text-white transition">
              เข้าสู่ระบบ
            </NuxtLink>
          </p>
        </div>
      </div>
    </div>
  </section>
</template>


<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const full_name = ref('');
const phone_number = ref('');
const profile_image = ref(null);
const errorMsg = ref('');

const handleImageUpload = (event) => {
  profile_image.value = event.target.files[0];
};

const handleRegister = async () => {
  errorMsg.value = '';
  if (!username.value || !email.value || !password.value || !full_name.value) {
    errorMsg.value = 'Please fill in all required fields.';
    return;
  }

  if (password.value !== confirmPassword.value) {
    errorMsg.value = 'Passwords do not match.';
    return;
  }

  const formData = new FormData();
  formData.append('username', username.value);
  formData.append('email', email.value);
  formData.append('password', password.value);
  formData.append('full_name', full_name.value);
  formData.append('phone_number', phone_number.value);
  if (profile_image.value) {
    formData.append('profile_image', profile_image.value);
  }

  try {
    const response = await axios.post('http://localhost:5000/api/register', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    console.log('Registration successful:', response.data);

    // ✅ นำทางไปหน้ายืนยันอีเมลหลังจากการลงทะเบียนสำเร็จ
    router.push({ name: 'VerifyEmail', query: { email: email.value } });
  } catch (err) {
    console.error('[Register error]', err.response?.data?.msg || err.message);
    errorMsg.value = err.response?.data?.msg || 'Registration failed. Please try again.';
  }
};
</script>

<style scoped lang="postcss">
.input-style {
  @apply w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-white placeholder-gray-400
    focus:outline-none focus:ring-2 focus:ring-pink-400/80 focus:border-transparent transition
    backdrop-blur-md;
}
</style>