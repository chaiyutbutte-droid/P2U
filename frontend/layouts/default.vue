<template>
  <div class="app-frame">
    <div class="app-frame__bg-grid" aria-hidden="true"></div>
    <div class="app-frame__glow app-frame__glow--pink" aria-hidden="true"></div>
    <div class="app-frame__glow app-frame__glow--indigo" aria-hidden="true"></div>

    <div class="app-frame__content">
      <Navbar />
      <main class="app-frame__main">
        <slot />
      </main>
      <Footer />
    </div>
  </div>
</template>

<script setup>
import Navbar from '~/components/Navbar.vue'
import Footer from '~/components/Footer.vue'
</script>
