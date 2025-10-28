<template>
  <nav class="bg-gradient-to-r from-black to-pink-950 text-white px-6 py-4 flex items-center shadow-md relative">
    <!-- ชื่อแอป -->
    <NuxtLink to="/dashboard" class="font-bold text-2xl flex-shrink-0 transition transform hover:scale-110">
      <span class="text-white transition-colors duration-300">P2U</span>
      <span class="text-pink-500 transition-colors duration-300">KAISER</span>
    </NuxtLink>

    <!-- ช่อง search -->
    <div v-if="!hideNavbar" class="ml-auto flex items-center bg-white rounded-md overflow-hidden w-1/2">
      <input
        v-model="searchQuery"
        @keyup.enter="handleSearch"
        type="text"
        placeholder="ค้นหาสินค้า"
        class="w-full px-4 py-2 text-black outline-none"
      />
      <button @click="handleSearch" class="bg-pink-600 text-white px-4 py-2 hover:bg-pink-700 transition">
        🔍
      </button>
    </div>

    <div class="ml-auto flex items-center gap-4 relative">
      <!-- Coin Indicator -->
      <div
        v-if="user"
        class="flex items-center space-x-1 bg-yellow-500/20 px-3 py-1 rounded-lg font-semibold cursor-pointer hover:bg-yellow-500/30 transition"
        @click="showTopupModal = true"
        title="เติม Coin"
      >
        <span>{{ coinBalance }}</span>
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-yellow-400" fill="currentColor" viewBox="0 0 24 24">
          <path
            d="M12 2a10 10 0 1 0 10 10A10.011 10.011 0 0 0 12 2zm1 14.93V17h-2v-.07A8.014 8.014 0 0 1 4.07 13H7v-2H4.07A8.014 8.014 0 0 1 11 4.07V7h2V4.07A8.014 8.014 0 0 1 19.93 11H17v2h2.93A8.014 8.014 0 0 1 13 16.93z"
          />
        </svg>
      </div>

      <!-- รูปโปรไฟล์ -->
      <NuxtLink
        v-if="user"
        to="/profile"
        class="w-9 h-9 rounded-full overflow-hidden border-2 border-white hover:scale-105 transition"
        title="My Profile"
      >
        <img :src="profileImageUrl" alt="Profile" class="w-full h-full object-cover" />
      </NuxtLink>

      <!-- เมนูฟันเฟือง -->
      <div v-if="user" class="relative">
        <button @click="toggleSettings" class="text-white hover:scale-110 text-xl" title="Settings">
          ⚙️
        </button>
        <div v-if="showSettings" class="absolute right-0 mt-2 w-32 bg-white text-black rounded shadow-lg z-50">
          <NuxtLink to="/about">
            <button class="rounded-xl w-full text-left px-4 py-2 hover:bg-gray-100 transition">About</button>
          </NuxtLink>
          <button @click="handleLogout" class="w-full text-left px-4 py-2 hover:bg-gray-100 transition">Logout</button>
        </div>
      </div>

      <!-- ปุ่ม Register ถ้าไม่ได้ล็อกอิน -->
      <NuxtLink
        v-else
        to="/register"
        class="text-white font-semibold px-4 py-2 border border-white rounded hover:bg-white hover:text-black transition"
      >
        Register
      </NuxtLink>
    </div>

    <!-- Topup Modal Inline -->
    <div
      v-if="showTopupModal"
      class="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      @click.self="showTopupModal = false"
    >
      <div class="bg-gray-900 text-white p-6 rounded-lg w-96 space-y-4">
        <h2 class="text-xl font-bold">💰 Top-up Coins</h2>
        <p>Current balance: <span class="font-bold text-yellow-400">{{ coinBalance }}</span> coins</p>

        <input
          type="number"
          v-model.number="topupAmount"
          min="1"
          placeholder="Enter amount (THB)"
          class="w-full p-2 rounded bg-gray-800 text-white focus:outline-indigo-500"
        />

        <button
          class="w-full bg-indigo-600 hover:bg-indigo-700 py-2 rounded font-bold"
          @click="handleTopup"
          :disabled="loading || topupAmount < 1"
        >
          {{ loading ? "Processing..." : "Generate QR / Top-up" }}
        </button>

        <p v-if="topupError" class="text-red-400">{{ topupError }}</p>

        <div v-if="qrData" class="text-center mt-4">
          <p class="mb-2">Scan this QR to pay:</p>
          <img :src="qrData.qr_url" alt="Topup QR" class="mx-auto w-64 h-64 object-contain rounded-lg shadow-lg" />
          <p class="mt-2 text-gray-400">Amount: {{ qrData.amount }} THB</p>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useUserStore } from "../stores/user"; // <-- path แก้ให้เป็น relative

const router = useRouter();
const route = useRoute();
const userStore = useUserStore();

const user = ref(null);
const showSettings = ref(false);
const searchQuery = ref("");
const coinBalance = ref(0);

// Topup modal state
const showTopupModal = ref(false);
const topupAmount = ref(0);
const loading = ref(false);
const topupError = ref(null);
const qrData = ref(null);

// ฟังก์ชันค้นหา
const handleSearch = () => {
  if (!searchQuery.value.trim()) return;
  router.push({ path: "/dashboard", query: { q: searchQuery.value.trim() } });
};

// ซ่อน Navbar หน้า login/register
const hideNavbar = computed(() => {
  const hiddenPages = ["/login", "/register"];
  return hiddenPages.includes(route.path);
});

// โหลดข้อมูลผู้ใช้จาก store
function loadUser() {
  userStore.loadUserFromStorage(); // โหลดจาก localStorage
  user.value = userStore.user;
  coinBalance.value = userStore.coinBalance;
}

// Profile Image
const baseUrl = "http://localhost:5000";
const profileImageUrl = computed(() => {
  if (!user.value || !user.value.profile_image_url) return "/guest-profile.png";
  return user.value.profile_image_url.startsWith("http")
    ? user.value.profile_image_url
    : baseUrl + user.value.profile_image_url;
});

const toggleSettings = () => {
  showSettings.value = !showSettings.value;
};

// Logout
const handleLogout = () => {
  userStore.logout();
  user.value = null;
  coinBalance.value = 0;
  showSettings.value = false;
  router.push("/login");
  window.dispatchEvent(new Event("user-updated"));
};

// Handle topup QR generation
const handleTopup = async () => {
  if (topupAmount.value < 1) return;

  loading.value = true;
  topupError.value = null;
  qrData.value = null;

  try {
    const res = await userStore.topupCoin(topupAmount.value);
    qrData.value = res;
    user.value = userStore.user;
    coinBalance.value = userStore.coinBalance;
  } catch (err) {
    topupError.value = err.response?.data?.msg || err.message || "Top-up failed";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadUser();
  window.addEventListener("user-updated", loadUser);
});
onBeforeUnmount(() => {
  window.removeEventListener("user-updated", loadUser);
});
</script>
