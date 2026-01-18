<template>
  <div class="product-gallery">
    <!-- Main Image Display -->
    <div class="main-image-container relative aspect-square rounded-xl overflow-hidden bg-dark-800 mb-3">
      <!-- Video Player -->
      <video 
        v-if="activeMedia.type === 'video'" 
        :src="activeMedia.url"
        class="w-full h-full object-contain"
        controls
        autoplay
      />
      
      <!-- Image with Zoom -->
      <div 
        v-else
        class="relative w-full h-full cursor-zoom-in"
        @mousemove="handleZoom"
        @mouseleave="resetZoom"
        @click="openLightbox"
      >
        <img 
          :src="activeMedia.url" 
          :alt="productName"
          class="w-full h-full object-contain transition-transform duration-200"
          :style="zoomStyle"
          @error="handleImageError"
        />
        
        <!-- Zoom Lens Indicator -->
        <div 
          v-if="isZooming" 
          class="absolute w-24 h-24 border-2 border-white/50 rounded-full pointer-events-none"
          :style="lensStyle"
        />
      </div>

      <!-- 360° Mode Indicator -->
      <div v-if="is360Mode" class="absolute top-4 left-4 bg-black/70 backdrop-blur px-3 py-1.5 rounded-full flex items-center gap-2">
        <span class="text-white text-sm">🔄 หมุนดูสินค้า</span>
      </div>

      <!-- Navigation Arrows -->
      <button 
        v-if="allMedia.length > 1"
        @click="prevMedia"
        class="absolute left-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/50 hover:bg-primary-500 flex items-center justify-center text-white transition-colors"
      >
        ←
      </button>
      <button 
        v-if="allMedia.length > 1"
        @click="nextMedia"
        class="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-black/50 hover:bg-primary-500 flex items-center justify-center text-white transition-colors"
      >
        →
      </button>

      <!-- Image Counter -->
      <div v-if="allMedia.length > 1" class="absolute bottom-3 right-3 bg-black/70 backdrop-blur px-2 py-1 rounded text-white text-sm">
        {{ activeIndex + 1 }} / {{ allMedia.length }}
      </div>
    </div>

    <!-- Thumbnail Strip -->
    <div v-if="allMedia.length > 1" class="flex gap-2 overflow-x-auto pb-2">
      <button
        v-for="(media, index) in allMedia"
        :key="index"
        @click="activeIndex = index"
        class="flex-shrink-0 w-16 h-16 rounded-lg overflow-hidden border-2 transition-all"
        :class="activeIndex === index ? 'border-primary-500 ring-2 ring-primary-500/50' : 'border-transparent hover:border-dark-500'"
      >
        <!-- Video Thumbnail -->
        <div v-if="media.type === 'video'" class="w-full h-full bg-dark-700 flex items-center justify-center">
          <span class="text-2xl">🎬</span>
        </div>
        
        <!-- 360 Thumbnail -->
        <div v-else-if="media.type === '360'" class="w-full h-full bg-dark-700 flex items-center justify-center">
          <span class="text-2xl">🔄</span>
        </div>
        
        <!-- Image Thumbnail -->
        <img 
          v-else
          :src="media.url" 
          class="w-full h-full object-cover"
          @error="handleImageError"
        />
      </button>
    </div>

    <!-- 360° View Slider (when active) -->
    <div v-if="is360Mode && view360Images.length > 0" class="mt-3">
      <input 
        type="range" 
        :min="0" 
        :max="view360Images.length - 1"
        v-model.number="rotation360Index"
        class="w-full accent-primary-500"
      />
      <p class="text-center text-dark-400 text-sm mt-1">เลื่อนเพื่อหมุนสินค้า</p>
    </div>

    <!-- Lightbox -->
    <Teleport to="body">
      <Transition name="fade">
        <div 
          v-if="lightboxOpen" 
          class="fixed inset-0 bg-black/95 z-50 flex items-center justify-center"
          @click="lightboxOpen = false"
        >
          <button 
            @click="lightboxOpen = false"
            class="absolute top-4 right-4 text-white text-3xl hover:text-primary-400 z-10"
          >
            ✕
          </button>
          
          <button 
            v-if="allMedia.length > 1"
            @click.stop="prevMedia"
            class="absolute left-4 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/10 hover:bg-primary-500 flex items-center justify-center text-white text-xl"
          >
            ←
          </button>

          <img 
            :src="activeMedia.url" 
            class="max-w-[90vw] max-h-[90vh] object-contain"
            @click.stop
          />

          <button 
            v-if="allMedia.length > 1"
            @click.stop="nextMedia"
            class="absolute right-4 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/10 hover:bg-primary-500 flex items-center justify-center text-white text-xl"
          >
            →
          </button>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  mainImage: {
    type: String,
    default: ''
  },
  images: {
    type: Array,
    default: () => []
  },
  videoUrl: {
    type: String,
    default: ''
  },
  view360Images: {
    type: Array,
    default: () => []
  },
  productName: {
    type: String,
    default: 'Product'
  }
});

const activeIndex = ref(0);
const lightboxOpen = ref(false);
const isZooming = ref(false);
const zoomPosition = ref({ x: 50, y: 50 });
const rotation360Index = ref(0);

// Combine all media into single array
const allMedia = computed(() => {
  const media = [];
  
  // Main image first
  if (props.mainImage) {
    media.push({ type: 'image', url: props.mainImage });
  }
  
  // Additional images
  if (props.images && props.images.length) {
    props.images.forEach(url => {
      if (url && url !== props.mainImage) {
        media.push({ type: 'image', url });
      }
    });
  }
  
  // Video
  if (props.videoUrl) {
    media.push({ type: 'video', url: props.videoUrl });
  }
  
  // 360° view
  if (props.view360Images && props.view360Images.length > 0) {
    media.push({ type: '360', url: props.view360Images[0] });
  }
  
  // Fallback
  if (media.length === 0) {
    media.push({ type: 'image', url: '/default-item.svg' });
  }
  
  return media;
});

const activeMedia = computed(() => {
  const media = allMedia.value[activeIndex.value];
  
  // Handle 360° view specially
  if (media?.type === '360' && props.view360Images.length > 0) {
    return {
      type: '360',
      url: props.view360Images[rotation360Index.value] || props.view360Images[0]
    };
  }
  
  return media || { type: 'image', url: '/default-item.svg' };
});

const is360Mode = computed(() => activeMedia.value.type === '360');

const zoomStyle = computed(() => {
  if (!isZooming.value) return {};
  return {
    transform: 'scale(2)',
    transformOrigin: `${zoomPosition.value.x}% ${zoomPosition.value.y}%`
  };
});

const lensStyle = computed(() => {
  return {
    left: `${zoomPosition.value.x}%`,
    top: `${zoomPosition.value.y}%`,
    transform: 'translate(-50%, -50%)'
  };
});

function handleZoom(e) {
  if (activeMedia.value.type !== 'image') return;
  
  const rect = e.currentTarget.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;
  
  zoomPosition.value = { x, y };
  isZooming.value = true;
}

function resetZoom() {
  isZooming.value = false;
}

function openLightbox() {
  if (activeMedia.value.type === 'image') {
    lightboxOpen.value = true;
  }
}

function prevMedia() {
  activeIndex.value = (activeIndex.value - 1 + allMedia.value.length) % allMedia.value.length;
}

function nextMedia() {
  activeIndex.value = (activeIndex.value + 1) % allMedia.value.length;
}

function handleImageError(e) {
  e.target.src = '/default-item.svg';
}

// Reset 360 rotation when switching away
watch(activeIndex, () => {
  rotation360Index.value = 0;
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Custom range slider */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  height: 8px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--primary-500, #6366f1);
  cursor: pointer;
}
</style>
