<template>
  <footer v-if="!isLoginOrRegisterPage" class="bg-gray-800 text-white text-center p-4 text-sm font-bold">
<div class="border-1"></div>
<div class="flex p-5  text-2xl">
   <span class="text-white">P2U</span>
      <span class="text-pink-500  ">KAISER</span>
</div>

<div class="flex  gap-50 p-5">
  <div class="text-left">
    <div class="font-bold text-xl mt-2 ">ติดต่อเราได้ที่</div>
    <div class="mt-2">📞  01 108 8531</div>
    <div class="mt-2">📩  P2ukaiser.official@Gmail.com</div>
  </div>
  <div class="text-left" >
 <div class="font-bold text-xl mt-2  ">ติดตามได้</div>
      <a href="https://www.facebook.com/profile.php?id=61584117531266" target="_blank" >
      <button class="p-2 rounded-full overflow-hidden">
       <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" class="w-8 h-8 object-cover" />

      </button>
      </a>
</div>
  </div>
  </footer>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();

// เพิ่มการตรวจสอบค่า route.path
onMounted(() => {
  console.log('Current route path:', route.path); // ตรวจสอบค่า route.path
});

// ตรวจสอบว่าเป็นหน้า login หรือ register หรือไม่
const isLoginOrRegisterPage = computed(() => {
  return route.path === "/login" || route.path === "/register";
});
</script>