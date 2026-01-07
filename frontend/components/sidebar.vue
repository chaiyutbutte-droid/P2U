<template>
  <div
    class="fixed left-4 top-1/2 transform -translate-y-1/2 flex flex-col items-center z-50 transition-all duration-300 group"
    :class="expand ? 'w-52' : 'w-16'"
    @mouseenter="expand = true"
    @mouseleave="expand = false"
  >
    <div class="glass rounded-2xl p-3 shadow-lg w-full">
      <!-- Profile Section -->
      <div class="flex flex-col items-center mb-4 pb-4 border-b border-white/10">
        <div
          class="relative transition-all duration-300"
          :class="expand ? 'w-16 h-16 mb-3' : 'w-10 h-10'"
        >
          <img
            v-if="profileImageUrlLoaded"
            :src="profileImageUrl"
            class="w-full h-full rounded-xl object-cover border-2 border-primary-500/50 transition-all duration-300"
            alt="Profile"
          />
          <div
            v-else
            class="w-full h-full rounded-xl border-2 border-primary-500/30 skeleton"
          ></div>
          <!-- Online indicator -->
          <div class="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-dark-800"></div>
        </div>

        <Transition name="fade">
          <div v-if="expand" class="text-center">
            <p class="text-sm font-semibold text-white truncate w-full">{{ username }}</p>
            <p v-if="coinBalance !== null" class="text-xs text-primary-400 flex items-center justify-center gap-1 mt-1">
              <span>💰</span>
              <span>{{ coinBalance.toLocaleString() }} Coins</span>
            </p>
          </div>
        </Transition>
      </div>

      <!-- Menu Items -->
      <nav class="space-y-1">
        <div
          v-for="item in menuItems"
          :key="item.name"
          class="flex items-center p-2.5 rounded-xl cursor-pointer transition-all duration-300"
          :class="[
            isActive(item.route) 
              ? 'bg-primary-500/20 text-primary-400' 
              : 'hover:bg-white/10 text-dark-300 hover:text-white'
          ]"
          @click="navigate(item.route)"
        >
          <span class="text-xl" :class="expand ? '' : 'mx-auto'">{{ item.icon }}</span>
          <Transition name="slide">
            <span v-if="expand" class="ml-3 text-sm font-medium truncate">{{ item.name }}</span>
          </Transition>
          <!-- Badge for notifications/orders -->
          <span 
            v-if="item.badge && item.badge > 0" 
            class="ml-auto px-2 py-0.5 bg-red-500 text-white text-xs font-bold rounded-full"
            :class="expand ? '' : 'hidden'"
          >
            {{ item.badge > 99 ? '99+' : item.badge }}
          </span>
        </div>
      </nav>

      <!-- Divider -->
      <div class="my-3 border-t border-white/10"></div>

      <!-- Quick Actions -->
      <div class="space-y-1">
        <div
          v-if="user?.is_seller"
          class="flex items-center p-2.5 rounded-xl cursor-pointer hover:bg-accent-500/20 text-accent-400 transition-all duration-300"
          @click="navigate('/AddProduct')"
        >
          <span class="text-xl" :class="expand ? '' : 'mx-auto'">➕</span>
          <Transition name="slide">
            <span v-if="expand" class="ml-3 text-sm font-medium">เพิ่มสินค้า</span>
          </Transition>
        </div>

        <!-- Logout -->
        <div
          class="flex items-center p-2.5 rounded-xl cursor-pointer hover:bg-red-500/20 text-red-400 transition-all duration-300"
          @click="handleLogout"
        >
          <span class="text-xl" :class="expand ? '' : 'mx-auto'">🚪</span>
          <Transition name="slide">
            <span v-if="expand" class="ml-3 text-sm font-medium">ออกจากระบบ</span>
          </Transition>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";

const router = useRouter();
const route = useRoute();
const expand = ref(false);
const user = ref(null);
const profileImageUrlLoaded = ref(false);
const coinBalance = ref(null);

const baseUrl = "http://localhost:5000";

const profileImageUrl = computed(() => {
  if (!user.value || !user.value.profile_image_url) return "/guest-profile.png";
  return user.value.profile_image_url.startsWith("http")
    ? user.value.profile_image_url
    : baseUrl + user.value.profile_image_url;
});

const username = computed(() => user.value?.username || "ผู้ใช้งาน");

const menuItems = computed(() => [
  { name: "ร้านค้า", icon: "🏠", route: "/dashboard" },
  { name: "ตระกร้าสินค้า", icon: "🛒", route: "/cart" },
  { name: "ประมูล", icon: "🔨", route: "/auction" },
  { name: "เช็คอิน", icon: "📅", route: "/check-in" },
  { name: "ภารกิจ", icon: "🎯", route: "/missions" },
  { name: "โปรไฟล์", icon: "👤", route: "/profile" },
  { name: "คำสั่งซื้อ", icon: "📦", route: "/orders" },
  { name: "รายการโปรด", icon: "❤️", route: "/wishlist" },
  { name: "แจ้งเตือน", icon: "🔔", route: "/notifications" },
  { name: "แชท", icon: "💬", route: "/chat" },
  ...(user.value?.is_seller ? [{ name: "แดชบอร์ดผู้ขาย", icon: "📊", route: "/seller-dashboard" }] : []),
  { name: "เติมเหรียญ", icon: "💰", route: "/topup" },
]);

const isActive = (path) => route.path === path;

function navigate(path) {
  router.push(path);
}

function handleLogout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  user.value = null;
  router.push("/login");
  window.dispatchEvent(new Event("user-updated"));
}

async function fetchUserProfile() {
  profileImageUrlLoaded.value = false;
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    user.value = JSON.parse(storedUser);
    
    // Fetch coin balance
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const res = await axios.get(`${baseUrl}/api/profile`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        coinBalance.value = res.data.coin_balance || 0;
      } catch (e) {
        console.error("Failed to fetch profile:", e);
      }
    }
  } else {
    user.value = null;
  }

  const img = new Image();
  img.src = profileImageUrl.value;
  img.onload = () => (profileImageUrlLoaded.value = true);
  img.onerror = () => {
    if (user.value) user.value.profile_image_url = null;
    profileImageUrlLoaded.value = true;
  };
}

onMounted(() => {
  fetchUserProfile();
  window.addEventListener("user-updated", fetchUserProfile);
});

onBeforeUnmount(() => {
  window.removeEventListener("user-updated", fetchUserProfile);
});
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.2s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}
</style>
