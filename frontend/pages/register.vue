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

        <label for="" class="text-white ms-3">Email</label>
        <input
          v-model="email"
          type="email"
          placeholder="Email"
          class="input-style bg-white p-3 rounded-lg border-2 border-gray-400 focus:outline-none focus:border-4 focus:border-pink-600"
          autocomplete="email"
        />

        <label for="" class="text-white ms-3">Password</label>
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          class="input-style bg-white p-3 rounded-lg border-2 border-gray-400 focus:border-4 focus:outline-none focus:border-pink-600"
          autocomplete="new-password"
        />

        <label for="" class="text-white ms-3">Confirm Password</label>
        <input
          v-model="confirmPassword"
          type="password"
          placeholder="Confirm Password"
          class="input-style bg-white p-3 rounded-lg border-2 border-gray-400 focus:border-4 focus:outline-none focus:border-pink-600"
          autocomplete="new-password"
        />

        <label for="" class="text-white ms-3">Full Name</label>
        <input
          v-model="full_name"
          placeholder="Full Name"
          class="input-style bg-white p-3 rounded-lg border-2 border-gray-400 focus:outline-none focus:border-4 focus:border-pink-600"
          autocomplete="name"
        />

        <label for="" class="text-white ms-3">Phone Number</label>
        <input
          v-model="phone_number"
          placeholder="Phone Number"
          class="input-style bg-white p-3 rounded-lg border-2 border-gray-400 focus:outline-none focus:border-4 focus:border-pink-600"
          autocomplete="tel"
        />

        <label for="" class="text-white ms-3">Profile Image</label>
        <input
          @change="handleImageUpload"
          type="file"
          class="input-style bg-white p-3 rounded-lg border-2 border-gray-400 focus:outline-none focus:border-4 focus:border-pink-600"
        />
      </div>

      <button
        @click="handleRegister"
        class="bg-pink-600 hover:bg-pink-500 text-white font-semibold py-2 w-full rounded-lg transition duration-200 border border-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:border-white mt-4"
      >
        Register
      </button>

      <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center">
        {{ errorMsg }}
      </p>

      <div class="text-center text-sm text-gray-400 mt-4">
        Already have an account?
        <router-link to="/login" class="text-white underline hover:text-sky-500">Log In here</router-link>
      </div>
    </div>
  </div>
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
  @apply mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white;
}
</style>