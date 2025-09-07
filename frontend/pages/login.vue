<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black " style="background-image: url(https://wallpapers-clan.com/wp-content/uploads/2024/03/nezuko-glowing-eyes-demon-slayer-gif-desktop-wallpaper-preview.gif);">
    <div class="bg-gray-800/50 backdrop-blur-sm p-8 rounded-3xl shadow-xl w-full max-w-sm">
      <h1 class="text-2xl font-bold text-white text-center font-serif">Welcome to</h1>
      <h1 class="text-2xl font-bold text-pink-500 text-center font-serif">P2UKaoser</h1>
      <p class="text-sm text-gray-400 text-center mb-6 mt-2">Sign in to your account</p>

      <div class="flex flex-col">
        <label for="" class="text-white ms-3">Username</label>
        <input
          v-model="username"
          placeholder="Username"
          class="input-style bg-white p-3 rounded-lg border-2 border-gray-400 focus:outline-none focus:border-4 focus:border-pink-600"
          autocomplete="username"
        />

        <label for="" class="text-white ms-3">Password</label>
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="input-style bg-white p-3 rounded-lg border-2 border-gray-400 focus:border-4 focus:outline-none focus:border-pink-600"
          autocomplete="current-password"
        />
      </div>
      
      <button
        @click="handleLogin"
        class="bg-pink-600 hover:bg-pink-500 text-white font-semibold py-2 w-full rounded-lg transition duration-200 border border-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:border-white mt-4"
      >
        Log In
      </button>

      <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center">
        {{ errorMsg }}
      </p>

      <div class="text-center text-sm text-gray-400 mt-4">
        Don’t have an account?
        <router-link to="/register" class="text-white underline hover:text-sky-500">Register here</router-link>
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
const router = useRouter();

const handleLogin = async () => {
  errorMsg.value = '';
  if (!username.value || !password.value) {
    errorMsg.value = 'Please enter a username and password.';
    return;
  }

  try {
    const res = await axios.post('http://localhost:5000/api/login', {
      username: username.value,
      password: password.value
    });

    const user = res.data.user;

    // ✅ กรณีที่ล็อกอินสำเร็จ แต่ Backend ส่งสถานะ is_email_verified = false กลับมา
    if (user && !user.is_email_verified) {
      router.push({ name: 'VerifyEmail', query: { email: user.email } });
      return;
    }

    localStorage.setItem('token', res.data.access_token);

    if (user) {
      localStorage.setItem('user', JSON.stringify({
        id: user.id,
        username: user.username,
        email: user.email,
        full_name: user.full_name,
        profile_image_url: user.profile_image_url,
        is_seller: user.is_seller
      }));
      window.dispatchEvent(new Event('user-updated'));
    }

    console.log('Login successful. Redirecting to dashboard.');
    router.push('/dashboard');

  } catch (err) {
    console.error('[Login error]', err.response?.data?.msg || err.message);
    
    // ✅ ส่วนนี้คือการจัดการ Error ที่ Backend บอกว่า "Please verify your email before logging in"
    // โค้ดจะพยายามดึงอีเมลจาก username เพื่อเปลี่ยนเส้นทางไปยังหน้ายืนยัน
    if (err.response?.status === 403 && err.response?.data?.msg === 'Please verify your email before logging in') {
      errorMsg.value = err.response.data.msg;
      try {
        const userEmailRes = await axios.post('http://localhost:5000/api/check-email-from-username', { 
            username: username.value 
        });

        if (userEmailRes.data.email) {
          router.push({ name: 'VerifyEmail', query: { email: userEmailRes.data.email } });
        }
      } catch (checkErr) {
        console.error('[Check Email error]', checkErr);
        // แสดงข้อความ Error นี้เมื่อไม่สามารถดึงอีเมลจาก username ได้
        errorMsg.value = 'Could not find user email. Please try registering again.';
      }
    } else {
      // สำหรับข้อผิดพลาดอื่นๆ ที่ไม่ใช่เรื่องการยืนยันอีเมล
      errorMsg.value = err.response?.data?.msg || 'Login failed. Please try again.';
    }
  }
};
</script>

<style lang="postcss" scoped>
.input-style {
  @apply mb-4 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400
    focus:outline-none focus:ring-2 focus:ring-white focus:border-white;
}
</style>