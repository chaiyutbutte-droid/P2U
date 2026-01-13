<template>
  <div>
    <span v-for="star in 5" :key="star" class="star cursor-pointer text-xl" :class="{ filled: star <= rating }" @click="setRating(star)">
      ★
    </span>
  </div>
</template>

<script setup>
const props = defineProps({
  rating: { type: Number, default: 0 },
  editable: { type: Boolean, default: false }
});

const emit = defineEmits(['update:rating']);

function setRating(value) {
  if (props.editable) {
    emit('update:rating', value);
  }
}
</script>

<style scoped>
.star {
  color: #475569;
  transition: color 0.2s ease;
}
.star.filled {
  color: #fbbf24;
}
.star:hover {
  color: #fcd34d;
}
</style>
