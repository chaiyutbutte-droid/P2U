<template>
  <aside
    class="fixed left-4 top-24 z-40 flex flex-col transition-all duration-500 ease-spring"
    :class="expand ? 'w-64' : 'w-20'"
    @mouseenter="expand = true"
    @mouseleave="expand = false"
  >
    <div 
      class="relative flex flex-col h-[calc(100vh-8rem)] bg-[#09090b]/80 backdrop-blur-xl border border-white/10 rounded-3xl shadow-[0_0_40px_-10px_rgba(0,0,0,0.5)] overflow-hidden transition-all duration-300 group hover:border-pink-500/30 hover:shadow-[0_0_40px_-10px_rgba(236,72,153,0.2)]"
    >
      
      <div class="absolute top-0 left-0 w-full h-32 bg-gradient-to-b from-pink-500/10 to-transparent opacity-50 pointer-events-none"></div>

      <div class="relative px-4 pt-6 pb-4 shrink-0">
        <div class="flex flex-col items-center">
          <div class="relative group/avatar cursor-pointer" @click="navigate('/profile')">
            <div 
              class="absolute -inset-0.5 bg-gradient-to-tr from-pink-500 to-cyan-500 rounded-full blur opacity-50 group-hover/avatar:opacity-100 transition duration-500"
              :class="expand ? 'w-[76px] h-[76px]' : 'w-[44px] h-[44px]'"
            ></div>
            
            <div 
              class="relative rounded-full overflow-hidden border-2 border-[#09090b] transition-all duration-300 bg-gray-900"
              :class="expand ? 'w-[72px] h-[72px] mb-3' : 'w-[40px] h-[40px]'"
            >
              <img
                v-if="profileImageUrlLoaded"
                :src="profileImageUrl"
                class="w-full h-full object-cover"
                alt="Profile"
              />
              <div v-else class="w-full h-full bg-gray-800 animate-pulse"></div>
            </div>
            
            <div class="absolute bottom-0 right-0 w-3.5 h-3.5 bg-emerald-500 border-2 border-[#09090b] rounded-full z-10">
               <span class="absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75 animate-ping"></span>
            </div>
          </div>

          <div 
            class="text-center overflow-hidden transition-all duration-300"
            :class="expand ? 'opacity-100 max-h-20' : 'opacity-0 max-h-0'"
          >
            <h3 class="text-white font-bold truncate text-base tracking-wide">{{ username }}</h3>
            <div v-if="coinBalance !== null" class="mt-1 inline-flex items-center px-2 py-0.5 rounded-full bg-gradient-to-r from-amber-500/10 to-yellow-500/10 border border-amber-500/20">
              <span class="text-xs font-medium text-amber-400">🪙 {{ coinBalance.toLocaleString() }}</span>
            </div>
            <div v-if="tokenBalance !== null" class="mt-1 inline-flex items-center px-2 py-0.5 rounded-full bg-gradient-to-r from-yellow-500/10 to-orange-500/10 border border-yellow-500/20">
              <span class="text-xs font-medium text-yellow-400">💰 {{ tokenBalance.toLocaleString() }} Token</span>
            </div>
          </div>
        </div>
      </div>

      <div class="mx-4 h-[1px] bg-gradient-to-r from-transparent via-white/10 to-transparent mb-2"></div>

      <nav class="flex-1 overflow-y-auto no-scrollbar px-3 space-y-1.5 py-2">
        <div
          v-for="item in menuItems"
          :key="item.name"
          @click="navigate(item.route)"
          class="relative flex items-center px-3 py-3 rounded-xl cursor-pointer transition-all duration-300 group/item overflow-hidden"
          :class="[
            isActive(item.route) 
              ? 'bg-white/5 text-white shadow-inner' 
              : 'text-gray-400 hover:text-white hover:bg-white/5'
          ]"
        >
          <div 
            v-if="isActive(item.route)"
            class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-gradient-to-b from-pink-500 to-purple-500 rounded-r-full shadow-[0_0_10px_rgba(236,72,153,0.5)]"
          ></div>

          <span 
            class="relative z-10 text-xl transition-transform duration-300 group-hover/item:scale-110"
            :class="[
               expand ? 'mr-4' : 'mx-auto',
               isActive(item.route) ? 'text-pink-400' : ''
            ]"
          >
            {{ item.icon }}
          </span>

          <span 
            class="relative z-10 whitespace-nowrap font-medium text-sm transition-all duration-300"
            :class="expand ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-4 absolute pointer-events-none'"
          >
            {{ item.name }}
          </span>

          <span 
            v-if="item.badge && item.badge > 0" 
            class="absolute right-2 min-w-[1.25rem] h-5 px-1 flex items-center justify-center bg-red-500 text-white text-[10px] font-bold rounded-full shadow-lg"
            :class="expand ? 'opacity-100' : 'opacity-0 scale-0'"
          >
            {{ item.badge > 99 ? '99+' : item.badge }}
          </span>

          <div class="absolute inset-0 bg-gradient-to-r from-white/0 via-white/5 to-white/0 translate-x-[-100%] group-hover/item:translate-x-[100%] transition-transform duration-700"></div>
        </div>
      </nav>

      <div class="p-3 mt-auto border-t border-white/5 bg-black/20 backdrop-blur-md space-y-2">
         
         <div
          v-if="user?.is_seller"
          class="flex items-center justify-center p-3 rounded-xl cursor-pointer bg-gradient-to-r from-indigo-600/20 to-purple-600/20 border border-indigo-500/30 hover:border-indigo-400/50 hover:from-indigo-600/30 hover:to-purple-600/30 transition-all duration-300 group/seller"
          @click="navigate('/AddProduct')"
        >
          <span class="text-xl group-hover/seller:animate-bounce">➕</span>
          <span 
            class="ml-3 text-sm font-semibold text-indigo-300 whitespace-nowrap overflow-hidden transition-all duration-300"
            :class="expand ? 'w-auto opacity-100' : 'w-0 opacity-0'"
          >
            เพิ่มสินค้า
          </span>
        </div>

        <div
          class="flex items-center justify-center p-3 rounded-xl cursor-pointer hover:bg-red-500/10 text-gray-500 hover:text-red-400 border border-transparent hover:border-red-500/20 transition-all duration-300 group/logout"
          @click="handleLogout"
        >
          <span class="text-xl group-hover/logout:scale-110 transition-transform">🚪</span>
          <span 
            class="ml-3 text-sm font-medium whitespace-nowrap overflow-hidden transition-all duration-300"
            :class="expand ? 'w-auto opacity-100' : 'w-0 opacity-0'"
          >
            ออกจากระบบ
          </span>
        </div>

      </div>

    </div>
  </aside>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";

// ======================
// Logic Script (คงเดิมตามโค้ดของคุณ)
// ======================
const router = useRouter();
const route = useRoute();
const expand = ref(false); 
const user = ref(null);
const profileImageUrlLoaded = ref(false);
const coinBalance = ref(null);
const tokenBalance = ref(null);

const baseUrl = "http://localhost:5000";

// คำนวณ URL รูปภาพ
const profileImageUrl = computed(() => {
  if (!user.value || !user.value.profile_image_url) return "/guest-profile.png";
  return user.value.profile_image_url.startsWith("http")
    ? user.value.profile_image_url
    : baseUrl + user.value.profile_image_url;
});

const username = computed(() => user.value?.username || "ผู้ใช้งาน");

// รายการเมนู (ใส่ครบทุกอันตามที่คุณส่งมา)
const menuItems = computed(() => [
  { name: "ร้านค้า", icon: "🏠", route: "/dashboard" },
  { name: "ตระกร้าสินค้า", icon: "🛒", route: "/cart" },
  { name: "ประมูล", icon: "🔨", route: "/auction" },
  { name: "เช็คอิน", icon: "📅", route: "/check-in" },
  { name: "ภารกิจ", icon: "🎯", route: "/missions" },
  ...(user.value?.is_seller ? [{ name: "แดชบอร์ดผู้ขาย", icon: "📊", route: "/seller-dashboard" }] : []),
  { name: "เติม Token", icon: "🪙", route: "/token-topup" },
]);

// เช็คว่าหน้าปัจจุบันตรงกับเมนูไหน
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
    
    // Fetch coin balance and token balance
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
      
      // Fetch token balance
      try {
        const tokenRes = await axios.get(`${baseUrl}/api/token/balance`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        tokenBalance.value = tokenRes.data.token_balance || 0;
      } catch (e) {
        console.error("Failed to fetch token balance:", e);
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
/* ซ่อน Scrollbar แต่ยังเลื่อนได้ */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

/* Custom Easing for cleaner animation (การเคลื่อนไหวแบบสปริง) */
.ease-spring {
  transition-timing-function: cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
</style>