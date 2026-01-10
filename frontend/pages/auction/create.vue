<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />

    <div class="max-w-3xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-white flex items-center gap-3">
            🔨 สร้างการประมูลใหม่
          </h1>
          <p class="text-dark-400 mt-1">เพิ่มสินค้าใหม่เข้าสู่ระบบประมูล</p>
        </div>
        <NuxtLink to="/Profile" class="btn-secondary">
          ← กลับ
        </NuxtLink>
      </div>

      <!-- Form Card -->
      <div class="card p-6">
        <form @submit.prevent="createAuction" class="space-y-6">
          <!-- Product Image -->
          <div>
            <label class="block text-white font-medium mb-2">รูปภาพสินค้า</label>
            <div class="flex items-center gap-4">
              <div 
                class="w-40 h-40 rounded-xl bg-dark-800 border-2 border-dashed border-dark-600 flex items-center justify-center overflow-hidden cursor-pointer hover:border-primary-500 transition-colors"
                @click="triggerFileInput"
              >
                <img 
                  v-if="previewImage" 
                  :src="previewImage" 
                  class="w-full h-full object-cover"
                />
                <div v-else class="text-center text-dark-400">
                  <span class="text-4xl">📷</span>
                  <p class="text-sm mt-2">อัปโหลดรูป</p>
                </div>
              </div>
              <input 
                ref="fileInput" 
                type="file" 
                accept="image/*" 
                class="hidden" 
                @change="onFileChange"
              />
              <div class="text-dark-400 text-sm">
                <p>รองรับไฟล์ JPG, PNG, GIF</p>
                <p>ขนาดไม่เกิน 5MB</p>
              </div>
            </div>
          </div>

          <!-- Title -->
          <div>
            <label class="block text-white font-medium mb-2">ชื่อสินค้า *</label>
            <input 
              v-model="form.title" 
              type="text" 
              class="input-glass w-full"
              placeholder="เช่น iPhone 15 Pro Max สภาพใหม่"
              required
            />
          </div>

          <!-- Description -->
          <div>
            <label class="block text-white font-medium mb-2">รายละเอียด</label>
            <textarea 
              v-model="form.description" 
              rows="4"
              class="input-glass w-full resize-none"
              placeholder="อธิบายสภาพสินค้า อุปกรณ์ที่มา ฯลฯ"
            ></textarea>
          </div>

          <!-- Category -->
          <div>
            <label class="block text-white font-medium mb-2">หมวดหมู่</label>
            <div class="flex flex-wrap gap-2">
              <button 
                v-for="cat in categories" 
                :key="cat.id"
                type="button"
                @click="form.category = cat.id"
                class="category-pill"
                :class="{ active: form.category === cat.id }"
              >
                {{ cat.icon }} {{ cat.name }}
              </button>
            </div>
          </div>

          <!-- Price Section -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-white font-medium mb-2">ราคาเริ่มต้น (Token) *</label>
              <input 
                v-model.number="form.starting_price" 
                type="number" 
                min="1"
                class="input-glass w-full"
                placeholder="1000"
                required
              />
            </div>
            <div>
              <label class="block text-white font-medium mb-2">ราคาขั้นต่ำที่เพิ่ม (Token)</label>
              <input 
                v-model.number="form.min_bid_increment" 
                type="number" 
                min="1"
                class="input-glass w-full"
                placeholder="100"
              />
            </div>
          </div>

          <!-- Duration -->
          <div>
            <label class="block text-white font-medium mb-2">ระยะเวลาประมูล</label>
            <div class="flex flex-wrap gap-3">
              <button 
                v-for="duration in durations" 
                :key="duration.hours"
                type="button"
                @click="form.duration_hours = duration.hours"
                class="px-4 py-2 rounded-lg transition-colors"
                :class="form.duration_hours === duration.hours ? 'bg-primary-500 text-white' : 'bg-dark-800 text-dark-300 hover:bg-dark-700'"
              >
                {{ duration.label }}
              </button>
            </div>
          </div>

          <!-- Preview Card -->
          <div v-if="form.title" class="glass-light rounded-xl p-4">
            <p class="text-dark-400 text-sm mb-3">👀 Preview</p>
            <div class="flex gap-4">
              <div class="w-24 h-24 rounded-lg bg-dark-700 overflow-hidden">
                <img 
                  v-if="previewImage" 
                  :src="previewImage" 
                  class="w-full h-full object-cover"
                />
                <div v-else class="w-full h-full flex items-center justify-center text-3xl">📦</div>
              </div>
              <div class="flex-1">
                <h4 class="text-white font-semibold">{{ form.title }}</h4>
                <p class="text-dark-400 text-sm truncate">{{ form.description || 'ไม่มีรายละเอียด' }}</p>
                <div class="flex items-center justify-between mt-2">
                  <span class="text-primary-400 font-bold">{{ form.starting_price?.toLocaleString() || 0 }} Token</span>
                  <span class="text-dark-500 text-sm">{{ form.duration_hours }} ชม.</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit" 
            :disabled="isLoading || !form.title || !form.starting_price"
            class="btn-primary w-full py-4 text-lg font-bold disabled:opacity-50"
          >
            {{ isLoading ? '⏳ กำลังสร้าง...' : '🔨 สร้างการประมูล' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const baseUrl = 'http://localhost:5000';

const form = ref({
  title: '',
  description: '',
  category: 'all',
  starting_price: null,
  min_bid_increment: 100,
  duration_hours: 24,
  image_url: ''
});

const previewImage = ref(null);
const fileInput = ref(null);
const isLoading = ref(false);

const categories = [
  { id: 'all', name: 'ทั้งหมด', icon: '📦' },
  { id: 'electronics', name: 'อิเล็กทรอนิกส์', icon: '📱' },
  { id: 'fashion', name: 'แฟชั่น', icon: '👗' },
  { id: 'gaming', name: 'เกมมิ่ง', icon: '🎮' },
  { id: 'beauty', name: 'ความงาม', icon: '💄' },
];

const durations = [
  { hours: 6, label: '6 ชม.' },
  { hours: 12, label: '12 ชม.' },
  { hours: 24, label: '1 วัน' },
  { hours: 48, label: '2 วัน' },
  { hours: 72, label: '3 วัน' },
  { hours: 168, label: '7 วัน' },
];

const imageFile = ref(null);

function triggerFileInput() {
  fileInput.value?.click();
}

async function onFileChange(e) {
  const file = e.target.files[0];
  if (!file) return;
  
  // Preview
  if (previewImage.value) URL.revokeObjectURL(previewImage.value);
  previewImage.value = URL.createObjectURL(file);
  
  // Store file for later upload
  imageFile.value = file;
}

async function createAuction() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('กรุณาเข้าสู่ระบบก่อน');
    router.push('/login');
    return;
  }
  
  if (!form.value.title || !form.value.starting_price) {
    alert('กรุณากรอกชื่อและราคาเริ่มต้น');
    return;
  }
  
  isLoading.value = true;
  
  try {
    const formData = new FormData();
    formData.append('title', form.value.title);
    formData.append('description', form.value.description);
    formData.append('category', form.value.category);
    formData.append('starting_price', form.value.starting_price);
    formData.append('min_bid_increment', form.value.min_bid_increment || 100);
    formData.append('duration_hours', form.value.duration_hours);
    
    if (imageFile.value) {
      formData.append('image', imageFile.value);
    }

    const res = await axios.post(`${baseUrl}/api/auctions`, formData, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    
    alert('🎉 สร้างการประมูลสำเร็จ!');
    router.push('/auction');
  } catch (err) {
    console.error(err);
    alert(err.response?.data?.msg || 'สร้างการประมูลไม่สำเร็จ');
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.category-pill {
  @apply px-4 py-2 rounded-full bg-dark-800 text-dark-300 text-sm font-medium transition-all;
}
.category-pill:hover {
  @apply bg-dark-700 text-white;
}
.category-pill.active {
  @apply bg-primary-500 text-white;
}
</style>
