<template>
  <nav v-if="!hideNavbar" class="glass sticky top-0 z-50 px-6 py-3 flex items-center shadow-lg">
    <!-- Logo -->
    <NuxtLink to="/dashboard" class="flex items-center gap-2 group">
      <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center transform group-hover:scale-110 transition-transform duration-300">
        <span class="text-2xl">👑</span>
      </div>
      <div class="font-display font-bold text-xl">
        <span class="gradient-text">P2UKAISER</span>
      </div>
    </NuxtLink>

    <!-- Search Bar -->
    <div class="ml-8 flex-1 max-w-xl">
      <div class="relative">
        <input 
          v-model="searchQuery" 
          @keyup.enter="handleSearch" 
          type="text" 
          placeholder="ค้นหาสินค้า..."
          class="w-full input-glass pl-12 pr-4 py-2.5 rounded-xl text-sm"
        />
        <svg class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <button 
          @click="handleSearch" 
          class="absolute right-2 top-1/2 -translate-y-1/2 bg-primary-500 hover:bg-primary-600 text-white px-4 py-1.5 rounded-lg text-sm font-medium transition-colors"
        >
          ค้นหา
        </button>
      </div>
    </div>

    <!-- Right Side -->
    <div class="ml-auto flex items-center gap-4">
      <!-- Notifications -->
      <NuxtLink v-if="user" to="/notifications" class="relative p-2 hover:bg-white/10 rounded-xl transition-colors">
        <svg class="w-6 h-6 text-dark-300 hover:text-primary-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
        </svg>
        <span v-if="notificationCount > 0" class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center animate-pulse">
          {{ notificationCount > 9 ? '9+' : notificationCount }}
        </span>
      </NuxtLink>

      <!-- Chat -->
      <NuxtLink v-if="user" to="/chat" class="relative p-2 hover:bg-white/10 rounded-xl transition-colors">
        <svg class="w-6 h-6 text-dark-300 hover:text-primary-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
        </svg>
        <span v-if="unreadMessages > 0" class="absolute -top-1 -right-1 w-5 h-5 bg-accent-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
          {{ unreadMessages > 9 ? '9+' : unreadMessages }}
        </span>
      </NuxtLink>

      <!-- Wishlist -->
      <NuxtLink v-if="user" to="/wishlist" class="p-2 hover:bg-white/10 rounded-xl transition-colors">
        <svg class="w-6 h-6 text-dark-300 hover:text-red-400 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
        </svg>
      </NuxtLink>

      <!-- Profile Dropdown -->
      <div v-if="user" class="relative">
        <button @click="toggleSettings" class="flex items-center gap-3 p-1.5 hover:bg-white/10 rounded-xl transition-colors">
          <img 
            :src="profileImageUrl" 
            alt="Profile" 
            class="w-9 h-9 rounded-xl object-cover border-2 border-primary-500/50"
          />
          <span class="text-sm font-medium text-white hidden md:block">{{ user.username }}</span>
          <svg class="w-4 h-4 text-dark-400 hidden md:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        <!-- Dropdown Menu -->
        <Transition name="dropdown">
          <div v-if="showSettings" class="absolute right-0 mt-2 w-56 glass rounded-xl shadow-xl overflow-hidden">
            <div class="p-3 border-b border-white/10">
              <p class="text-sm font-semibold text-white">{{ user.full_name || user.username }}</p>
              <p class="text-xs text-dark-400">{{ user.email }}</p>
            </div>
            <div class="py-2">
              <NuxtLink to="/profile" class="flex items-center gap-3 px-4 py-2.5 hover:bg-white/10 transition-colors">
                <span class="text-lg">👤</span>
                <span class="text-sm text-dark-200">โปรไฟล์</span>
              </NuxtLink>
              <NuxtLink to="/orders" class="flex items-center gap-3 px-4 py-2.5 hover:bg-white/10 transition-colors">
                <span class="text-lg">📦</span>
                <span class="text-sm text-dark-200">คำสั่งซื้อ</span>
              </NuxtLink>
              <NuxtLink v-if="user.is_seller" to="/seller-dashboard" class="flex items-center gap-3 px-4 py-2.5 hover:bg-white/10 transition-colors">
                <span class="text-lg">📊</span>
                <span class="text-sm text-dark-200">แดชบอร์ดผู้ขาย</span>
              </NuxtLink>
              <NuxtLink to="/about" class="flex items-center gap-3 px-4 py-2.5 hover:bg-white/10 transition-colors">
                <span class="text-lg">ℹ️</span>
                <span class="text-sm text-dark-200">เกี่ยวกับ</span>
              </NuxtLink>
            </div>
            <div class="border-t border-white/10 py-2">
              <button @click="handleLogout" class="flex items-center gap-3 px-4 py-2.5 w-full hover:bg-red-500/20 transition-colors text-red-400">
                <span class="text-lg">🚪</span>
                <span class="text-sm">ออกจากระบบ</span>
              </button>
            </div>
          </div>
        </Transition>
      </div>

      <!-- Login Button (Guest) -->
      <NuxtLink v-else to="/login" class="btn-primary text-sm">
        เข้าสู่ระบบ
      </NuxtLink>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";

const route = useRoute();
const router = useRouter();
const user = ref(null);
const showSettings = ref(false);
const searchQuery = ref("");
const notificationCount = ref(0);
const unreadMessages = ref(0);

const baseUrl = "http://localhost:5000";

const handleSearch = () => {
  if (!searchQuery.value.trim()) return;
  router.push({
    path: "/dashboard",
    query: { q: searchQuery.value.trim() },
  });
};

const hideNavbar = computed(() => {
  const hiddenPages = ["/login", "/register", "/admin-login"];
  return hiddenPages.includes(route.path);
});

const profileImageUrl = computed(() => {
  if (!user.value || !user.value.profile_image_url) {
    return "/guest-profile.png";
  }
  if (user.value.profile_image_url.startsWith("http")) {
    return user.value.profile_image_url;
  }
  return baseUrl + user.value.profile_image_url;
});

function loadUser() {
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    try {
      user.value = JSON.parse(storedUser);
      fetchNotifications();
    } catch {
      user.value = null;
    }
  } else {
    user.value = null;
  }
}

async function fetchNotifications() {
  const token = localStorage.getItem("token");
  if (!token) return;
  
  try {
    const res = await axios.get(`${baseUrl}/api/notifications`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    notificationCount.value = res.data.unread_count || 0;
  } catch (e) {
    console.error("Failed to fetch notifications:", e);
  }
}

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

// Close dropdown when clicking outside
const handleClickOutside = (e) => {
  if (showSettings.value && !e.target.closest('.relative')) {
    showSettings.value = false;
  }
};

onMounted(() => {
  loadUser();
  window.addEventListener("user-updated", loadUser);
  document.addEventListener("click", handleClickOutside);
});

onBeforeUnmount(() => {
  window.removeEventListener("user-updated", loadUser);
  document.removeEventListener("click", handleClickOutside);
});
</script>

<style scoped>
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
