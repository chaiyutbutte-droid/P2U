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
      <div v-if="!hideNavbar" ref="searchWrapper" class="absolute left-1/2 transform -translate-x-1/2 flex items-center bg-white rounded-2xl overflow-hidden w-1/2 shadow-lg relative">
        <input 
          v-model="searchQuery" 
          @keyup.enter="handleSearch" 
          @focus="openHistory"
          type="text" 
          placeholder="ค้นหาสินค้า, ร้านค้า, หมวดหมู่..."
          class="w-full px-4 py-2 text-black outline-none placeholder:text-gray-400" 
          autocomplete="off"
        />
        <button 
          @click="handleSearch()" 
          class="bg-pink-600 text-white px-6 py-2 hover:bg-pink-700 transition transform hover:scale-105 font-semibold flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24">
            <path fill="currentColor" d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5A6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5S14 7.01 14 9.5S11.99 14 9.5 14"/>
          </svg>
          <span>ค้นหา</span>
        </button>

        <!-- Suggestion Dropdown -->
        <transition name="fade">
          <div v-if="isSuggestionOpen" class="absolute top-full left-0 right-0 mt-2 bg-white text-black rounded-2xl shadow-2xl border border-gray-200 overflow-hidden z-50">
            <div v-if="isFetchingSuggestions" class="p-4 text-center text-sm text-gray-500">
              กำลังค้นหา...
            </div>
            <template v-else>
              <div v-if="suggestions.length" class="divide-y divide-gray-100">
                <button 
                  v-for="item in suggestions" 
                  :key="item.id" 
                  class="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-50 transition text-left"
                  @mousedown.prevent="handleSuggestionClick(item)">
                  <img :src="item.image" alt="" class="w-10 h-10 rounded-lg object-cover bg-gray-100" />
                  <div class="flex-1">
                    <p class="font-semibold text-sm text-gray-900 line-clamp-1">{{ item.name }}</p>
                    <p class="text-xs text-pink-500 font-medium">฿{{ item.price }}</p>
                  </div>
                  <span class="text-xs text-gray-400">ดูรายละเอียด</span>
                </button>
              </div>
              <div v-if="recentSearches.length" class="border-t border-gray-100">
                <div class="flex items-center justify-between px-4 py-2 text-xs uppercase tracking-widest text-gray-400">
                  <span>ค้นหาล่าสุด</span>
                  <button class="text-pink-500 hover:text-pink-600" @mousedown.prevent="clearRecentSearches">ล้าง</button>
                </div>
                <div class="flex flex-wrap gap-2 px-4 pb-4">
                  <button 
                    v-for="item in recentSearches" 
                    :key="item" 
                    class="px-3 py-1.5 bg-gray-100 text-gray-700 rounded-full text-xs font-medium hover:bg-pink-50 hover:text-pink-600 transition"
                    @mousedown.prevent="handleSearch(item)">
                    {{ item }}
                  </button>
                </div>
              </div>
            </template>
          </div>
        </transition>
      </div>

      <div class="ml-auto flex items-center gap-4 relative">
        <!-- Profile Picture -->
        <NuxtLink v-if="!hideNavbar && user" to="/profile"
          class="w-10 h-10 rounded-full overflow-hidden border-2 border-pink-400 hover:scale-105 transition bg-white hover:border-pink-300"
          title="My Profile">
          <img :src="profileImageUrl" alt="Profile" class="w-full h-full object-cover" />
        </NuxtLink>

        <!-- Settings Menu -->
        <div v-if="!hideNavbar && user" class="relative">
          <button @click="toggleSettings" class="text-pink-300 hover:scale-110 hover:text-pink-200 text-2xl transition" title="Settings">
            ⚙️
          </button>
          <div v-if="showSettings" class="absolute right-0 mt-2 w-40 bg-white text-black rounded-lg shadow-xl z-50 overflow-hidden border border-gray-200">
            <NuxtLink to="/about">
              <button class="w-full text-left px-4 py-3 hover:bg-gray-100 transition flex items-center gap-2">
                <span>📋</span>
                <span>About</span>
              </button>
            </NuxtLink>
            <button @click="handleLogout" class="w-full text-left px-4 py-3 hover:bg-red-50 transition flex items-center gap-2 text-red-600">
              <span>🚪</span>
              <span>Logout</span>
            </button>
          </div>
        </div>
      </div>
    </nav>

    <!-- Secondary Navigation Bar with Active State -->
    <nav v-if="!hideNavbar" class="bg-pink-900 text-white px-6 py-3 flex justify-center items-center gap-10 shadow-md">
      <NuxtLink 
        to="/dashboard" 
        class="relative py-2 hover:text-pink-200 transform transition font-semibold group"
        :class="{ 'text-pink-200': isActive('/dashboard') }">
        <span>หน้าแรก</span>
        <span 
          class="absolute bottom-0 left-0 w-full h-0.5 bg-pink-300 transform transition-all duration-300"
          :class="isActive('/dashboard') ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'">
        </span>
      </NuxtLink>

      <NuxtLink 
        to="/shop" 
        class="relative py-2 hover:text-pink-200 transform transition font-semibold group"
        :class="{ 'text-pink-200': isActive('/shop') }">
        <span>สินค้า</span>
        <span 
          class="absolute bottom-0 left-0 w-full h-0.5 bg-pink-300 transform transition-all duration-300"
          :class="isActive('/shop') ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'">
        </span>
      </NuxtLink>

      <NuxtLink 
        to="/about" 
        class="relative py-2 hover:text-pink-200 transform transition font-semibold group"
        :class="{ 'text-pink-200': isActive('/about') }">
        <span>เกี่ยวกับ</span>
        <span 
          class="absolute bottom-0 left-0 w-full h-0.5 bg-pink-300 transform transition-all duration-300"
          :class="isActive('/about') ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'">
        </span>
      </NuxtLink>

      <NuxtLink 
        to="/help" 
        class="relative py-2 hover:text-pink-200 transform transition font-semibold group"
        :class="{ 'text-pink-200': isActive('/help') }">
        <span>ช่วยเหลือ</span>
        <span 
          class="absolute bottom-0 left-0 w-full h-0.5 bg-pink-300 transform transition-all duration-300"
          :class="isActive('/help') ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'">
        </span>
      </NuxtLink>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, watch } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";

const route = useRoute();
const router = useRouter();
const user = ref(null);
const showSettings = ref(false);
const searchQuery = ref("");
const suggestions = ref([]);
const isSuggestionOpen = ref(false);
const isFetchingSuggestions = ref(false);
const recentSearches = ref([]);
const searchWrapper = ref(null);
let suggestionTimer = null;
const MIN_QUERY_LENGTH = 2;
const SEARCH_HISTORY_KEY = "p2u-search-history";

// ฟังก์ชันค้นหา
const baseApiUrl = "http://localhost:5000/api";

const resolveSearchTerm = (value) => {
  if (typeof value === "string") return value
  if (value == null) return searchQuery.value || ""
  if (typeof value === "object" && "target" in value) return searchQuery.value || ""
  try {
    return String(value)
  } catch (_) {
    return searchQuery.value || ""
  }
}

const handleSearch = (term) => {
  const query = resolveSearchTerm(term).trim()
  if (!query) return

  searchQuery.value = query;
  saveRecentSearch(query);
  toggleSuggestions(false);

  router.push({
    path: "/shop",
    query: { search: query },
  });

  window.dispatchEvent(new CustomEvent("search-products", { detail: query }));
};

const fetchSuggestions = async () => {
  const query = searchQuery.value.trim();
  if (!query || query.length < MIN_QUERY_LENGTH) {
    suggestions.value = [];
    return;
  }
  isFetchingSuggestions.value = true;
  try {
    const res = await axios.get(`${baseApiUrl}/products`, {
      params: { search: query, limit: 6 },
    });
    suggestions.value = (res.data || []).map((item) => ({
      id: item.id || item._id,
      name: item.name,
      price: item.price,
      image: normalizeImage(item.image_url),
    }));
    toggleSuggestions(true);
  } catch (err) {
    console.error("Failed to fetch suggestions:", err);
  } finally {
    isFetchingSuggestions.value = false;
  }
};

const normalizeImage = (src) => {
  if (!src) return "/default-product.svg";
  if (/^https?:\/\//i.test(src)) return src;
  const normalizedBase = baseUrl.replace(/\/$/, "");
  const normalizedPath = src.startsWith("/") ? src : `/${src}`;
  return `${normalizedBase}${normalizedPath}`;
};

const queueSuggestionFetch = () => {
  if (suggestionTimer) clearTimeout(suggestionTimer);
  suggestionTimer = setTimeout(() => {
    fetchSuggestions();
  }, 250);
};

const toggleSuggestions = (state) => {
  const shouldOpen =
    state &&
    (!searchQuery.value || searchQuery.value.trim().length === 0
      ? recentSearches.value.length > 0
      : true);
  isSuggestionOpen.value = shouldOpen;
};

const handleSuggestionClick = (suggestion) => {
  if (!suggestion) return;
  searchQuery.value = suggestion.name;
  handleSearch(suggestion.name);
};

const saveRecentSearch = (term) => {
  if (typeof window === "undefined") return;
  const existing = recentSearches.value.filter((item) => item !== term);
  recentSearches.value = [term, ...existing].slice(0, 6);
  window.localStorage.setItem(
    SEARCH_HISTORY_KEY,
    JSON.stringify(recentSearches.value)
  );
};

const loadRecentSearches = () => {
  if (typeof window === "undefined") return;
  try {
    const stored = JSON.parse(
      window.localStorage.getItem(SEARCH_HISTORY_KEY) || "[]"
    );
    recentSearches.value = Array.isArray(stored) ? stored : [];
  } catch {
    recentSearches.value = [];
  }
};

const clearRecentSearches = () => {
  recentSearches.value = [];
  if (typeof window !== "undefined") {
    window.localStorage.removeItem(SEARCH_HISTORY_KEY);
  }
};

const openHistory = () => {
  if (recentSearches.value.length) {
    isSuggestionOpen.value = true;
  }
};

const handleOutsideClick = (event) => {
  if (
    searchWrapper.value &&
    !searchWrapper.value.contains(event.target)
  ) {
    isSuggestionOpen.value = false;
  }
};

watch(searchQuery, (value) => {
  if (!value || value.trim().length < MIN_QUERY_LENGTH) {
    suggestions.value = [];
    if (!value) {
      toggleSuggestions(true);
    }
    return;
  }
  queueSuggestionFetch();
});

// ตรวจสอบว่าอยู่ในหน้าไหน
const isActive = (path) => {
  return route.path === path;
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

  const imagePath = user.value.profile_image_url;
  if (/^https?:\/\//i.test(imagePath)) {
    return imagePath;
  }

  const normalizedBase = baseUrl.replace(/\/$/, "");
  const normalizedPath = imagePath.startsWith("/") ? imagePath : `/${imagePath}`;
  return `${normalizedBase}${normalizedPath}`;
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
  loadRecentSearches();
  window.addEventListener("user-updated", loadUser);
  window.addEventListener("click", handleOutsideClick);
});

onBeforeUnmount(() => {
  window.removeEventListener("user-updated", loadUser);
  window.removeEventListener("click", handleOutsideClick);
  if (suggestionTimer) clearTimeout(suggestionTimer);
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 150ms ease, transform 150ms ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>