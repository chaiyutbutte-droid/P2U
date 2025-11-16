<template>
  <footer v-if="!isLoginOrRegisterPage" class="bg-gray-800 text-white text-center p-4 text-sm font-bold">
    By IT Loeitech
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