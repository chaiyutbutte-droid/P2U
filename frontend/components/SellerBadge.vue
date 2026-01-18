<template>
  <span 
    class="seller-badge inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium"
    :class="badgeClass"
    :title="badgeInfo.name"
  >
    <span>{{ badgeInfo.icon }}</span>
    <span v-if="showName">{{ badgeInfo.name }}</span>
  </span>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  level: {
    type: String,
    default: 'C',
    validator: (value) => ['S', 'A', 'B', 'C'].includes(value.toUpperCase())
  },
  showName: {
    type: Boolean,
    default: false
  }
});

const badges = {
  S: { icon: '🥇', name: 'Top Seller', bgClass: 'bg-yellow-500/20', textClass: 'text-yellow-400', borderClass: 'border-yellow-500/50' },
  A: { icon: '⭐', name: 'Star Seller', bgClass: 'bg-purple-500/20', textClass: 'text-purple-400', borderClass: 'border-purple-500/50' },
  B: { icon: '✓', name: 'Verified Seller', bgClass: 'bg-blue-500/20', textClass: 'text-blue-400', borderClass: 'border-blue-500/50' },
  C: { icon: '📦', name: 'Basic Seller', bgClass: 'bg-gray-500/20', textClass: 'text-gray-400', borderClass: 'border-gray-500/50' }
};

const badgeInfo = computed(() => {
  return badges[props.level.toUpperCase()] || badges.C;
});

const badgeClass = computed(() => {
  const info = badgeInfo.value;
  return [info.bgClass, info.textClass, 'border', info.borderClass];
});
</script>

<style scoped>
.seller-badge {
  transition: all 0.2s ease;
}

.seller-badge:hover {
  transform: scale(1.05);
}
</style>
