<template>
  <div>
    <!-- Top Navigation Bar -->
    <nav class="bg-gradient-to-r from-black to-pink-950 text-white px-6 py-4 flex items-center shadow-md relative">
      <!-- Logo -->
      <NuxtLink :to="hideNavbar ? '#' : '/dashboard'" class="font-bold text-2xl flex-shrink-0 transition transform hover:scale-110">
        <span class="text-white transition-colors duration-300">P2U</span>
        <span class="text-pink-500 transition-colors duration-300">KAISER</span>
      </NuxtLink>
      
      <!-- Search Bar (Centered) -->
      <div v-if="!hideNavbar" class="absolute left-1/2 transform -translate-x-1/2 flex items-center bg-white rounded-2xl overflow-hidden w-1/2 ">
        <input v-model="searchQuery" @keyup.enter="handleSearch" type="text" placeholder="ค้นหาสินค้า"
          class="w-full px-4 py-2 text-black outline-none" />
        <button @click="handleSearch" class="bg-pink-600 text-white px-4 py-2 hover:bg-pink-700 transition transform hover:scale-110">
          🔍
        </button>
      </div>

      <div class="ml-auto flex items-center gap-4 relative">
        <!-- Profile Picture -->
        <NuxtLink v-if="!hideNavbar && user" to="/profile"
          class="w-10 h-10 rounded-full overflow-hidden border-2 border-amber-900 hover:scale-105 transition bg-white"
          title="My Profile">
          <img :src="profileImageUrl" alt="Profile" class="w-full h-full object-cover" />
        </NuxtLink>

        <!-- Settings Menu -->
        <div v-if="!hideNavbar && user" class="relative">
          <button @click="toggleSettings" class="text-amber-900 hover:scale-110 text-2xl" title="Settings">
            ⚙️
          </button>
          <div v-if="showSettings" class="absolute right-0 mt-2 w-32 bg-white text-black rounded shadow-lg z-50">
            <NuxtLink to="/about">
              <button class="rounded-xl w-full text-left px-4 py-2 hover:bg-gray-100 transition">
                About
              </button>
            </NuxtLink>
            <button @click="handleLogout" class="w-full text-left px-4 py-2 hover:bg-gray-100 transition">
              Logout
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Secondary Brown Navigation Bar -->
    <nav v-if="!hideNavbar" class="bg-pink-900 text-white  text-1xl px-6 py-3 flex justify-center items-center gap-10 shadow-md   ">
      <NuxtLink to="/dashboard" class=" hover:scale-140   transform  transition font-semibold">
        หน้าแรก
      </NuxtLink>
      <NuxtLink to="/books" class="  hover:scale-140 transform transition font-semibold">
        สินค้า
      </NuxtLink>
      <NuxtLink to="/about" class=" hover:scale-140 transform transition font-semibold">
        เกี่ยวกับ
      </NuxtLink>
      <NuxtLink to="/help" class=" hover:scale-140 transform transition font-semibold">
        ช่วยเหลือ
      </NuxtLink>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter, useRoute } from "vue-router";

const route = useRoute();
const router = useRouter();
const user = ref(null);
const showSettings = ref(false);
const searchQuery = ref("");

const handleSearch = () => {
  if (!searchQuery.value.trim()) return;
  router.push({
    path: "/dashboard",
    query: { q: searchQuery.value.trim() },
  });
};

const hideNavbar = computed(() => {
  const hiddenPages = ["/login", "/register"];
  return hiddenPages.includes(route.path);
});

function loadUser() {
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    try {
      user.value = JSON.parse(storedUser);
    } catch {
      user.value = null;
    }
  } else {
    user.value = null;
  }
}

const baseUrl = "http://localhost:5000";
const profileImageUrl = computed(() => {
  if (!user.value || !user.value.profile_image_url) {
    return "/guest-profile.png";
  }
  if (user.value.profile_image_url.startsWith("http")) {
    return user.value.profile_image_url;
  }
  return baseUrl + user.value.profile_image_url;
});

const toggleSettings = () => {
  showSettings.value = !showSettings.value;
};

const handleLogout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  localStorage.removeItem("user");
  user.value = null;
  showSettings.value = false;
  router.push("/login");
  window.dispatchEvent(new Event("user-updated"));
};

onMounted(() => {
  loadUser();
  window.addEventListener("user-updated", loadUser);
});

onBeforeUnmount(() => {
  window.removeEventListener("user-updated", loadUser);
});
</script>