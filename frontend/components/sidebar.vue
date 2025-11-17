<template>
  <div
    class="fixed left-0 top-1/2 transform -translate-y-1/2 flex flex-col items-center p-2 z-50 shadow-lg rounded-3xl transition-all duration-300"
    :class="[
      expand ? 'w-56 p-4' : 'w-16 p-2',
      isProfilePage ? 'bg-gray-100 text-gray-800' : 'bg-pink-100 text-pink-800'
    ]"
    @mouseenter="expand = true"
    @mouseleave="expand = false"
  >
    <!-- Profile Image -->
    <div
      class="relative transition-all duration-300"
      :class="expand ? 'w-12 h-12 mb-2' : 'w-10 h-10 mb-1'"
    >
      <img
        v-if="profileImageUrlLoaded"
        :src="profileImageUrl"
        class="w-full h-full rounded-full border-2 border-gray-300 object-cover transition-all duration-300"
        alt="Profile"
      />
      <div
        v-else
        class="w-full h-full rounded-full border-2 border-gray-300 bg-gray-200 animate-pulse"
      ></div>
    </div>

    <!-- Username -->
    <span
      v-if="expand"
      class="text-sm font-semibold mb-4 truncate w-full text-center transition-all duration-300"
      :class="isProfilePage ? 'text-gray-800' : 'text-pink-800'"
    >
      {{ username }}
    </span>

    <!-- Menu Items -->
    <nav class="flex-1 w-full space-y-2 mt-2">
      <div
        v-for="item in menuItems"
        :key="item.name"
        class="flex items-center p-2 rounded-xl hover:bg-gray-200 cursor-pointer transition-all duration-300 w-full"
        @click="navigate(item.route)"
        :class="isProfilePage ? 'text-gray-800' : 'text-pink-800'"
      >
        <span class="text-lg">{{ item.icon }}</span>
        <span v-if="expand" class="ml-3 text-sm truncate">{{ item.name }}</span>
      </div>
    </nav>

    <!-- Logout -->
    <div
      class="w-full mt-auto flex items-center p-2 rounded-xl hover:bg-gray-300 cursor-pointer transition-all duration-300"
      @click="handleLogout"
      :class="isProfilePage ? 'text-gray-800' : 'text-pink-800'"
    >
      <span class="text-lg">🚪</span>
      <span v-if="expand" class="ml-3 text-sm">ออกระบบ</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const expand = ref(false);
const user = ref(null);
const profileImageUrlLoaded = ref(false);

const baseUrl = "http://localhost:5000";

const profileImageUrl = computed(() => {
  if (!user.value || !user.value.profile_image_url) return "/default-profile.png";
  return user.value.profile_image_url.startsWith("http")
    ? user.value.profile_image_url
    : baseUrl + user.value.profile_image_url;
});

const username = computed(() => user.value?.username || "ผู้ใช้งาน");

const menuItems = [
  { name: "ร้านค้า", icon: "🏠", route: "/dashboard" },
  { name: "โปรไฟล์", icon: "👤", route: "/profile" },
  { name: "ตั้งค่า", icon: "⚙️", route: "/settings" },
];

// ตรวจสอบหน้า profile
const isProfilePage = computed(() => route.path === "/profile");

function navigate(route) {
  router.push(route);
}

function handleLogout() {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  user.value = null;
  router.push("/login");
  window.dispatchEvent(new Event("user-updated"));
}

function fetchUserProfile() {
  profileImageUrlLoaded.value = false;
  const storedUser = localStorage.getItem("user");
  if (storedUser) user.value = JSON.parse(storedUser);
  else user.value = null;

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

<style>
/* เพิ่ม shadow อ่อนเพื่อให้ดูละมุน */
.bg-pink-100 {
  box-shadow: 0 4px 15px rgba(219, 112, 147, 0.2);
}
.bg-gray-100 {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}
</style>
