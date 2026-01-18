<template>
  <div class="flex flex-col min-h-screen">
    <Navbar />
    <!-- <sidebar /> -->
    <main class="flex-1">
      <slot />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from '~/components/Navbar.vue'
import Footer from '~/components/Footer.vue'
import sidebar from '~/components/sidebar.vue';

</script>
