<template>
  <div class="mb-8">
    <h2 class="text-lg font-semibold text-white mb-4">🏷️ หมวดหมู่สินค้า</h2>
    <div class="flex flex-wrap gap-2">
      <button 
        v-for="cat in categories" 
        :key="cat.id"
        @click="selectCategory(cat.id)"
        class="px-4 py-2 rounded-full text-sm font-medium transition-all duration-200"
        :class="selectedCategory === cat.id 
          ? 'bg-gradient-to-r from-pink-500 to-purple-500 border-transparent text-white shadow-lg' 
          : 'bg-gray-700/50 border border-gray-600 text-gray-300 hover:bg-gray-600 hover:border-gray-500'"
      >
        {{ cat.icon }} {{ cat.name }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const emit = defineEmits(['category-change']);

const selectedCategory = ref('all');

// Default categories (จะถูกแทนที่ด้วยข้อมูลจาก API)
const categories = ref([
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
]);

const fetchCategories = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/categories');
    if (res.data && res.data.length > 0) {
      categories.value = res.data;
    }
  } catch (err) {
    console.log('Using default categories');
  }
};

function selectCategory(id) {
  selectedCategory.value = id;
  emit('category-change', id);
}

onMounted(() => {
  fetchCategories();
});
</script>
