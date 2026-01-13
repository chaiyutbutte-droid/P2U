<template>
  <div class="mb-8">
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-xl font-bold text-white flex items-center gap-2">
        {{ title }}
      </h2>
      <NuxtLink v-if="showMore" :to="showMore" class="text-primary-400 text-sm hover:underline">
        ดูทั้งหมด →
      </NuxtLink>
    </div>

    <div class="relative">
      <!-- Scroll Container -->
      <div 
        ref="scrollContainer"
        class="flex gap-4 overflow-x-auto pb-4 scroll-smooth hide-scrollbar"
      >
        <div 
          v-for="product in products" 
          :key="product.id"
          class="flex-shrink-0 w-48 card overflow-hidden group cursor-pointer"
          @click="$emit('product-click', product)"
        >
          <div class="aspect-square relative overflow-hidden">
            <img 
              :src="product.image_url || '/placeholder.png'" 
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
            />
            <div v-if="product.rating" class="absolute bottom-2 left-2 flex items-center gap-1 bg-black/60 backdrop-blur px-2 py-1 rounded-full">
              <span class="text-yellow-400 text-xs">⭐</span>
              <span class="text-white text-xs font-medium">{{ product.rating }}</span>
            </div>
          </div>
          <div class="p-3">
            <h3 class="text-sm font-medium text-white truncate">{{ product.name }}</h3>
            <p class="text-lg font-bold text-primary-400 mt-1">฿{{ product.price?.toLocaleString() }}</p>
            <p v-if="product.seller" class="text-xs text-dark-400 truncate mt-1">
              {{ product.seller.shop_name || product.seller.username }}
            </p>
          </div>
        </div>

        <!-- Loading skeleton -->
        <template v-if="loading">
          <div v-for="i in 4" :key="'skeleton-' + i" class="flex-shrink-0 w-48">
            <div class="aspect-square skeleton rounded-lg mb-3"></div>
            <div class="h-4 skeleton rounded w-3/4 mb-2"></div>
            <div class="h-5 skeleton rounded w-1/2"></div>
          </div>
        </template>

        <!-- Empty state -->
        <div v-if="!loading && !products.length" class="w-full text-center py-8">
          <p class="text-dark-400">ไม่มีสินค้าแนะนำ</p>
        </div>
      </div>

      <!-- Scroll Buttons -->
      <button 
        v-if="products.length > 4"
        @click="scrollLeft"
        class="absolute left-0 top-1/2 -translate-y-1/2 w-10 h-10 bg-dark-800/90 backdrop-blur rounded-full flex items-center justify-center text-white hover:bg-primary-500 transition-colors shadow-lg"
      >
        ←
      </button>
      <button 
        v-if="products.length > 4"
        @click="scrollRight"
        class="absolute right-0 top-1/2 -translate-y-1/2 w-10 h-10 bg-dark-800/90 backdrop-blur rounded-full flex items-center justify-center text-white hover:bg-primary-500 transition-colors shadow-lg"
      >
        →
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  title: { type: String, default: '🔥 สินค้าแนะนำ' },
  products: { type: Array, default: () => [] },
  loading: { type: Boolean, default: false },
  showMore: { type: String, default: '' }
});

defineEmits(['product-click']);

const scrollContainer = ref(null);

function scrollLeft() {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: -400, behavior: 'smooth' });
  }
}

function scrollRight() {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: 400, behavior: 'smooth' });
  }
}
</script>

<style scoped>
.hide-scrollbar::-webkit-scrollbar {
  display: none;
}
.hide-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
