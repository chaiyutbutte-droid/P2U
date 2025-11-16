<template>
  <div class="  flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black  " style="background-image: url(https://artistic-scarlet-erufq5zade.edgeone.app/1.gif);  background-size: 100% 140%; height: 400px ; ">
    <div class="bg-gray-800/50 backdrop-blur-sm p-8 rounded-3xl shadow-xl w-full max-w-sm  border-1 border-white">
      <h1 class="text-2xl font-bold text-white text-center font-serif">Welcome to</h1>
      <h1 class="text-2xl font-bold text-pink-500 text-center font-serif">P2UKaiser</h1>
      <p class="text-sm text-gray-400 text-center mb-6 mt-2">Log in to your account</p>

      
      <div class="flex flex-col ">
        <label for="" class="text-white ms-3">Username</label>
         <div class="relative">
        <input
          v-model="username"
          placeholder="Username"
          class="input-style  p-3 rounded-2xl border-0 border-b-2 bg-white border-gray-400 hover:bg-pink-200 focus:outline-none focus:border-b-4  focus:border-pink-600  "
          autocomplete="username"
          style="width: 100%"  
   
        />
            <i class="bx bxs-user  absolute right-3 top-1/2 transform -translate-y-1/2 "></i>
        </div>


        <label for="" class="text-white ms-3">Password</label>
        <div class="relative">
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="input-style  p-3 rounded-2xl border-0 border-b-2 bg-white border-gray-400  hover:bg-pink-200 focus:outline-none focus:border-b-4 focus:border-pink-600"
          autocomplete="current-password"
          style="width: 100%" 
        />
        <i class=" bxs-lock-keyhole bx-rotate-90'  absolute right-3 top-1/2 transform -translate-y-1/2   "></i>
      </div>
      </div>
      
      <button
        @click="handleLogin"
        class="bg-pink-600 group font-semibold py-2 w-full rounded-lg  focus:outline-none focus:ring-2 focus:ring-white focus:border-white mt-4 overflow-hidden relative "
      >
        <span class="absolute inset-0 rounded-full bg-white 0 scale-0  group-hover:scale-110 transition-transform duration-100 origin-center"></span>
        <span class="text-white relative group-hover:text-black  transition duration-500">Log In</span>
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