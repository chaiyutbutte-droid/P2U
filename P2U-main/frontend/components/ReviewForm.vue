<template>
  <div class="glass rounded-xl p-4">
    <h3 class="text-white font-semibold mb-4">เขียนรีวิว</h3>
    <form @submit.prevent="submitReview">
      <!-- Rating -->
      <div class="mb-4">
        <p class="text-dark-400 text-sm mb-2">ให้คะแนน</p>
        <div class="flex gap-1">
          <button 
            v-for="i in 5" 
            :key="i" 
            type="button"
            @click="rating = i"
            class="text-2xl transition-colors"
            :class="i <= rating ? 'text-yellow-400' : 'text-dark-600 hover:text-yellow-300'"
          >
            ★
          </button>
        </div>
      </div>

      <!-- Comment -->
      <div class="mb-4">
        <textarea 
          v-model="comment"
          placeholder="เขียนความคิดเห็นของคุณ..."
          rows="3"
          class="w-full input-glass resize-none"
        ></textarea>
      </div>

      <!-- Submit -->
      <button 
        type="submit" 
        :disabled="!rating || isSubmitting"
        class="btn-primary w-full"
      >
        {{ isSubmitting ? 'กำลังส่ง...' : 'ส่งรีวิว' }}
      </button>

      <p v-if="message" :class="isError ? 'text-red-400' : 'text-green-400'" class="text-sm mt-3 text-center">
        {{ message }}
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const props = defineProps({
  productId: { type: String, required: true }
});

const emit = defineEmits(['review-submitted']);

const rating = ref(0);
const comment = ref('');
const isSubmitting = ref(false);
const message = ref('');
const isError = ref(false);

async function submitReview() {
  if (!rating.value) return;
  
  isSubmitting.value = true;
  message.value = '';
  
  const token = localStorage.getItem('token');
  
  try {
    const res = await axios.post('http://localhost:5000/api/reviews', {
      product_id: props.productId,
      rating: rating.value,
      comment: comment.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    message.value = 'รีวิวสำเร็จ!';
    isError.value = false;
    rating.value = 0;
    comment.value = '';
    emit('review-submitted', res.data.review);
  } catch (err) {
    message.value = err.response?.data?.msg || 'เกิดข้อผิดพลาด';
    isError.value = true;
  } finally {
    isSubmitting.value = false;
  }
}
</script>
