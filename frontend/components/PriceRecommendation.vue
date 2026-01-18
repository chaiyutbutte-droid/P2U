<template>
  <div class="price-recommendation">
    <!-- Price Input Card -->
    <div class="glass rounded-xl p-4 mb-4">
      <div class="flex items-center justify-between mb-3">
        <label class="text-white font-medium">💰 ตั้งราคาสินค้า</label>
        <span v-if="hasData" class="text-xs px-2 py-1 rounded-full" :class="positionClass">
          {{ pricePosition.label }}
        </span>
      </div>
      
      <div class="relative">
        <span class="absolute left-4 top-1/2 -translate-y-1/2 text-dark-400 text-lg">฿</span>
        <input 
          type="number"
          :value="modelValue"
          @input="$emit('update:modelValue', Number($event.target.value))"
          class="w-full input-glass text-2xl font-bold pl-10"
          placeholder="0"
          :min="0"
        />
      </div>

      <!-- Quick Price Buttons -->
      <div v-if="recommendation" class="flex gap-2 mt-3 flex-wrap">
        <button 
          @click="setPrice(recommendation.competitive_price)"
          class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all bg-green-500/20 text-green-400 hover:bg-green-500/30"
        >
          💚 ราคาแข่งขัน ฿{{ formatNumber(recommendation.competitive_price) }}
        </button>
        <button 
          @click="setPrice(recommendation.average_price)"
          class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all bg-yellow-500/20 text-yellow-400 hover:bg-yellow-500/30"
        >
          💛 ราคาเฉลี่ย ฿{{ formatNumber(recommendation.average_price) }}
        </button>
        <button 
          @click="setPrice(recommendation.premium_price)"
          class="px-3 py-1.5 rounded-lg text-sm font-medium transition-all bg-purple-500/20 text-purple-400 hover:bg-purple-500/30"
        >
          💎 พรีเมียม ฿{{ formatNumber(recommendation.premium_price) }}
        </button>
      </div>
    </div>

    <!-- Market Analysis Card -->
    <div v-if="hasData" class="glass rounded-xl p-4">
      <h4 class="text-white font-medium mb-3 flex items-center gap-2">
        📊 วิเคราะห์ราคาตลาด
        <span class="text-xs text-dark-400">(หมวด {{ category }})</span>
      </h4>

      <!-- Price Range Slider Visual -->
      <div class="relative h-8 mb-4">
        <div class="absolute inset-x-0 top-1/2 -translate-y-1/2 h-2 bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 rounded-full"></div>
        
        <!-- Min/Max Labels -->
        <span class="absolute left-0 -bottom-5 text-xs text-dark-400">฿{{ formatNumber(stats.min_price) }}</span>
        <span class="absolute right-0 -bottom-5 text-xs text-dark-400">฿{{ formatNumber(stats.max_price) }}</span>
        
        <!-- Current Price Indicator -->
        <div 
          v-if="modelValue > 0"
          class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-4 h-4 bg-white rounded-full ring-2 ring-primary-500 shadow-lg transition-all duration-300"
          :style="{ left: pricePercentage + '%' }"
        >
          <div class="absolute -top-8 left-1/2 -translate-x-1/2 whitespace-nowrap bg-dark-800 px-2 py-1 rounded text-xs text-white">
            ฿{{ formatNumber(modelValue) }}
          </div>
        </div>

        <!-- Average Marker -->
        <div 
          class="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-1 h-5 bg-white/50"
          :style="{ left: avgPercentage + '%' }"
        ></div>
      </div>

      <!-- Stats Grid -->
      <div class="grid grid-cols-3 gap-3 mt-8">
        <div class="text-center">
          <p class="text-green-400 font-bold">฿{{ formatNumber(stats.min_price) }}</p>
          <p class="text-xs text-dark-400">ราคาต่ำสุด</p>
        </div>
        <div class="text-center">
          <p class="text-yellow-400 font-bold">฿{{ formatNumber(stats.avg_price) }}</p>
          <p class="text-xs text-dark-400">ราคาเฉลี่ย</p>
        </div>
        <div class="text-center">
          <p class="text-red-400 font-bold">฿{{ formatNumber(stats.max_price) }}</p>
          <p class="text-xs text-dark-400">ราคาสูงสุด</p>
        </div>
      </div>

      <!-- Tips -->
      <div v-if="tips.length" class="mt-4 space-y-2">
        <div v-for="(tip, i) in tips" :key="i" class="text-xs text-dark-300 flex items-start gap-2">
          <span>{{ tip }}</span>
        </div>
      </div>

      <!-- Price Distribution Chart -->
      <div v-if="stats.price_distribution" class="mt-4">
        <p class="text-sm text-dark-300 mb-2">📈 การกระจายราคา</p>
        <div class="flex items-end gap-1 h-16">
          <div 
            v-for="(bucket, key) in stats.price_distribution" 
            :key="key"
            class="flex-1 rounded-t transition-all hover:opacity-80"
            :class="getDistributionClass(key)"
            :style="{ height: getDistributionHeight(bucket.count) }"
            :title="`${key}: ${bucket.count} สินค้า`"
          ></div>
        </div>
        <div class="flex text-xs text-dark-400 mt-1">
          <span class="flex-1 text-center">Budget</span>
          <span class="flex-1 text-center">Mid</span>
          <span class="flex-1 text-center">Premium</span>
        </div>
      </div>
    </div>

    <!-- No Data State -->
    <div v-else-if="!loading" class="glass rounded-xl p-4 text-center">
      <p class="text-dark-400">ยังไม่มีข้อมูลราคาในหมวดหมู่นี้</p>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="glass rounded-xl p-4 text-center">
      <div class="animate-spin w-6 h-6 border-2 border-primary-500 border-t-transparent rounded-full mx-auto"></div>
      <p class="text-dark-400 text-sm mt-2">กำลังโหลดข้อมูลราคา...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import axios from 'axios';

const props = defineProps({
  modelValue: {
    type: Number,
    default: 0
  },
  category: {
    type: String,
    default: 'all'
  }
});

const emit = defineEmits(['update:modelValue']);

const baseUrl = 'http://localhost:5000';

const loading = ref(false);
const stats = ref({});
const recommendation = ref(null);
const tips = ref([]);

const hasData = computed(() => stats.value && stats.value.total_products > 0);

const pricePercentage = computed(() => {
  if (!hasData.value || props.modelValue <= 0) return 0;
  const range = stats.value.max_price - stats.value.min_price;
  if (range <= 0) return 50;
  const percent = ((props.modelValue - stats.value.min_price) / range) * 100;
  return Math.max(0, Math.min(100, percent));
});

const avgPercentage = computed(() => {
  if (!hasData.value) return 50;
  const range = stats.value.max_price - stats.value.min_price;
  if (range <= 0) return 50;
  return ((stats.value.avg_price - stats.value.min_price) / range) * 100;
});

const pricePosition = computed(() => {
  if (!hasData.value || props.modelValue <= 0) {
    return { label: '', class: '' };
  }
  
  const avg = stats.value.avg_price;
  const price = props.modelValue;
  
  if (price < avg * 0.8) {
    return { label: '🟢 ราคาดี', position: 'below' };
  } else if (price > avg * 1.2) {
    return { label: '🔴 ราคาสูง', position: 'above' };
  } else {
    return { label: '🟡 ราคาปกติ', position: 'average' };
  }
});

const positionClass = computed(() => {
  const pos = pricePosition.value.position;
  if (pos === 'below') return 'bg-green-500/20 text-green-400';
  if (pos === 'above') return 'bg-red-500/20 text-red-400';
  return 'bg-yellow-500/20 text-yellow-400';
});

function formatNumber(num) {
  if (!num) return '0';
  return Math.round(num).toLocaleString();
}

function setPrice(price) {
  emit('update:modelValue', Math.round(price));
}

function getDistributionClass(key) {
  const classes = {
    budget: 'bg-green-500',
    mid: 'bg-yellow-500',
    premium: 'bg-purple-500'
  };
  return classes[key] || 'bg-primary-500';
}

function getDistributionHeight(count) {
  if (!stats.value.total_products || count === 0) return '10%';
  const percent = (count / stats.value.total_products) * 100;
  return Math.max(10, percent) + '%';
}

async function fetchPriceData() {
  loading.value = true;
  try {
    const res = await axios.post(`${baseUrl}/api/price/recommendation`, {
      category: props.category
    });
    
    if (res.data.has_data) {
      stats.value = res.data.stats || {};
      recommendation.value = res.data.recommendation;
      tips.value = res.data.tips || [];
    } else {
      stats.value = {};
      recommendation.value = null;
      tips.value = [];
    }
  } catch (err) {
    console.error('Failed to fetch price data:', err);
  } finally {
    loading.value = false;
  }
}

watch(() => props.category, () => {
  fetchPriceData();
});

onMounted(() => {
  fetchPriceData();
});
</script>

<style scoped>
.input-glass {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 0.75rem;
  padding: 0.75rem 1rem;
  color: white;
  transition: all 0.2s;
}

.input-glass:focus {
  outline: none;
  border-color: var(--primary-500, #6366f1);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
}

.input-glass::placeholder {
  color: rgba(255, 255, 255, 0.3);
}
</style>
