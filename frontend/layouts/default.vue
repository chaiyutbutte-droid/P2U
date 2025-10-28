<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />
    <main class="flex-1">
      <slot />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'  // <-- แก้เป็น relative path
import Footer from '../components/Footer.vue'  // <-- แก้เป็น relative path
</script>
