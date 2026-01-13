<template>
  <div class="mb-8">
    <h2 class="text-lg font-semibold text-white mb-4">🏷️ หมวดหมู่สินค้า</h2>
    <div class="flex flex-wrap gap-2">
      <button 
        v-for="cat in categories" 
        :key="cat.id"
        @click="selectCategory(cat.id)"
        class="category-pill"
        :class="{ active: selectedCategory === cat.id }"
      >
        {{ cat.icon }} {{ cat.name }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['category-change']);

const selectedCategory = ref('all');

const categories = [
  { id: 'all', name: 'ทั้งหมด', icon: '🛍️' },
  { id: 'electronics', name: 'อิเล็กทรอนิกส์', icon: '📱' },
  { id: 'fashion', name: 'แฟชั่น', icon: '👗' },
  { id: 'gaming', name: 'เกมมิ่ง', icon: '🎮' },
  { id: 'beauty', name: 'ความงาม', icon: '💄' },
  { id: 'home', name: 'บ้าน & สวน', icon: '🏠' },
  { id: 'sports', name: 'กีฬา', icon: '⚽' },
  { id: 'food', name: 'อาหาร', icon: '🍔' },
  { id: 'books', name: 'หนังสือ', icon: '📚' },
  { id: 'toys', name: 'ของเล่น', icon: '🧸' },
  { id: 'pets', name: 'สัตว์เลี้ยง', icon: '🐶' },
  { id: 'automotive', name: 'ยานยนต์', icon: '🚗' },
];

function selectCategory(id) {
  selectedCategory.value = id;
  emit('category-change', id);
}
</script>
