<template>
  <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full" :class="getBadgeClass">
    <span class="text-lg">{{ icon }}</span>
    <span class="font-semibold text-sm">{{ level }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  level: { type: String, default: 'Bronze' }
});

const icon = computed(() => {
  const icons = {
    Bronze: '🥉',
    Silver: '🥈',
    Gold: '🥇',
    Diamond: '💎'
  };
  return icons[props.level] || '🥉';
});

const getBadgeClass = computed(() => {
  const classes = {
    Bronze: 'bg-orange-900/50 text-orange-300 border border-orange-500/30',
    Silver: 'bg-gray-500/30 text-gray-200 border border-gray-400/30',
    Gold: 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30',
    Diamond: 'bg-gradient-to-r from-cyan-500/20 to-purple-500/20 text-cyan-300 border border-cyan-500/30'
  };
  return classes[props.level] || classes.Bronze;
});
</script>
