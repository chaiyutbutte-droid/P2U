<template>
  <div class="flex justify-center items-center min-h-screen p-4" style="background-image: url('https://wallpapercave.com/wp/wp10855314.png'); background-size: cover; background-position: center; background-repeat: no-repeat;">
    <div class="w-full max-w-sm rounded-3xl bg-gray-800/50 p-8 shadow-2xl backdrop-blur-sm transition-all duration-300 hover:bg-gray-800/70 hover:shadow-gray-700/50">
      <h1 class="mb-2 text-center font-serif text-3xl font-bold text-white drop-shadow-md">Welcome to P2UKaiser</h1>
      <p class="mb-8 text-center text-gray-400">Sign in to your account</p>

      <div class="space-y-4">
        <div class="relative">
          <input
            v-model="username"
            placeholder=" "
            id="username"
            class="peer block w-full rounded-lg border border-white/10 bg-gray-700 p-4 text-white placeholder-transparent ring-white/20 transition-all duration-300 focus:border-white focus:outline-none focus:ring-2 invalid:border-red-500 valid:border-green-500"
            autocomplete="username"
          />
          <label
            for="username"
            class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 transition-all duration-300 peer-placeholder-shown:top-1/2 peer-placeholder-shown:text-base peer-focus:-top-3.5 peer-focus:text-sm peer-focus:text-white peer-valid:-top-3.5 peer-valid:text-sm peer-valid:text-white"
          >
            Username
          </label>
        </div>

        <div class="relative mt-6">
          <input
            v-model="password"
            type="password"
            placeholder=" "
            id="password"
            class="peer block w-full rounded-lg border border-white/10 bg-gray-700 p-4 text-white placeholder-transparent ring-white/20 transition-all duration-300 focus:border-white focus:outline-none focus:ring-2 invalid:border-red-500 valid:border-green-500"
            autocomplete="current-password"
          />
          <label
            for="password"
            class="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 transition-all duration-300 peer-placeholder-shown:top-1/2 peer-placeholder-shown:text-base peer-focus:-top-3.5 peer-focus:text-sm peer-focus:text-white peer-valid:-top-3.5 peer-valid:text-sm peer-valid:text-white"
          >
            Password
          </label>
        </div>
      </div>

      <button
        @click="handleLogin"
        class="mt-6 w-full rounded-lg border border-white/20 bg-gray-900 py-3 font-semibold text-white shadow-lg transition-all duration-300 hover:scale-105 hover:bg-white/10 hover:shadow-xl focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-900"
      >
        Log In
      </button>

      <p v-if="errorMsg" class="mt-4 text-center text-sm text-red-400">
        {{ errorMsg }}
      </p>

      <div class="mt-8 text-center text-sm text-gray-400">
        Don’t have an account?
        <router-link to="/register" class="font-medium text-white underline decoration-2 decoration-white/50 underline-offset-4 transition-colors duration-300 hover:text-white hover:decoration-white">
          Register here
        </router-link>
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

    router.push('/dashboard');
  } catch (err) {
    errorMsg.value = err.response?.data?.msg || 'Login failed. Please try again.';
  }
};
</script>

<style lang="postcss" scoped>
/* You can add custom styles here if needed, but Tailwind CSS handles most of the styling. */
</style>