<template>
  <div class="card p-4">
    <div class="flex items-start gap-3">
      <img 
        :src="review.user?.profile_image_url || '/guest-profile.png'" 
        class="w-10 h-10 rounded-xl object-cover"
        alt="User"
      />
      <div class="flex-1">
        <div class="flex items-center gap-2 mb-1">
          <span class="font-medium text-white">{{ review.user?.username }}</span>
          <div class="flex text-yellow-400">
            <span v-for="i in 5" :key="i" class="text-sm">
              {{ i <= review.rating ? '★' : '☆' }}
            </span>
          </div>
        </div>
        <p class="text-dark-300 text-sm">{{ review.comment }}</p>
        <p class="text-dark-500 text-xs mt-2">{{ review.created_at }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  review: { type: Object, required: true }
});
</script>
