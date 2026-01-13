<template>
  <div class="flex min-h-screen bg-gray-900 text-white">
    <!-- Left Side: Upload Section -->
    <main class="flex-1 p-8">
      <div class="upload-container border-2">
        <h2 class="title">Upload product images</h2>
        <form @submit.prevent="handleSubmit" class="upload-form">
          <input type="file" ref="image" accept="image/*" class="file-input" @change="previewImage" />
          <button type="submit" class="upload-btn">Upload</button>
        </form>
        <div v-if="imagePreview" class="image-preview">
          <h3>images:</h3>
          <img :src="imagePreview" alt="Image Preview" class="preview-img" />
        </div>
      </div>

      <div v-if="activeTab === 'products'">
        <div class="product-container">
          <div class="relative mb-8 mt-8">
            <!-- 🖼️ Banner Carousel -->
            <div class="overflow-hidden rounded-xl shadow-lg">
              <div
                class="flex transition-transform duration-500"
                :style="{ transform: `translateX(-${currentBanner * 100}%)` }"
              >
                <div
                  v-for="(banner, index) in banners"
                  :key="index"
                  class="min-w-full h-60 sm:h-72 md:h-80 bg-gray-700 relative"
                >
                  <img
                    :src="banner.image"
                    alt="Banner"
                    class="w-full h-full object-cover"
                    @error="banner.image = defaultImage"
                  />
                  <div
                    class="absolute bottom-0 left-0 right-0 bg-linear-to-t from-black/70 to-transparent p-4"
                  >
                    <h3 class="text-lg font-bold">{{ banner.title }}</h3>
                    <p class="text-sm text-gray-300">{{ banner.subtitle }}</p>
                  </div>
                </div>
              </div>
            </div>

            <button
              class="absolute top-1/2 -translate-y-1/2 left-2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full"
              @click="prevBanner"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path
                  fill="#ed9bff"
                  d="m9.55 12l7.35 7.35q.375.375.363.875t-.388.875t-.875.375t-.875-.375l-7.7-7.675q-.3-.3-.45-.675t-.15-.75t.15-.75t.45-.675l7.7-7.7q.375-.375.888-.363t.887.388t.375.875t-.375.875z"
                />
              </svg>
            </button>
            <button
              class="absolute top-1/2 -translate-y-1/2 right-2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full"
              @click="nextBanner"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <path
                  fill="#ed9bff"
                  d="m14.475 12l-7.35-7.35q-.375-.375-.363-.888t.388-.887t.888-.375t.887.375l7.675 7.7q.3.3.45.675t.15.75t-.15.75t-.45.675l-7.7 7.7q-.375.375-.875.363T7.15 21.1t-.375-.888t.375-.887z"
                />
              </svg>
            </button>

            <div
              class="absolute bottom-2 left-1/2 -translate-x-1/2 flex space-x-2"
            >
              <span
                v-for="(banner, index) in banners"
                :key="'dot-' + index"
                class="w-3 h-3 rounded-full"
                :class="currentBanner === index ? 'bg-white' : 'bg-gray-400'"
              ></span>
            </div>
          </div>

          <div
            v-if="allProducts.length"
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6"
          >
            <div
              v-for="product in allProducts"
              :key="product.id"
              class="bg-gray-800 rounded-lg shadow-md p-4 cursor-pointer hover:bg-gray-700 transition"
              @click="openProduct(product)"
            >
              <img
                :src="product.image_url || defaultImage"
                class="w-full h-40 object-cover rounded mb-3"
                @error="product.image_url = defaultImage"
              />
              <h3 class="font-semibold">{{ product.name }}</h3>
              <p class="text-sm text-gray-400">{{ product.description }}</p>
              <p class="mt-2 font-bold text-indigo-400">฿{{ product.price }}</p>
              <p class="text-sm text-gray-400 mt-1">
                Seller: {{ product.seller.username }} | Shop:
                {{ product.seller.shop_name || "N/A" }}
              </p>
            </div>
          </div>
          <p v-else class="text-gray-400 mt-16 text-center">
            🔍 No products found.
          </p>
        </div>
      </div>
    </main>

    <!-- Right Side: n8n Data Display -->
    <div class="bg-gray-800 h-full w-1/3 max-w-xs p-8 m-6 mt-8 border-4 border-pink-500 flex flex-col justify-between">
      <h3 class="text-xl font-semibold mb-4">Data</h3>
      <div v-if="productData">
        <p><strong>ประเมินราคา:</strong> ฿{{ productData.price }}</p>
        <p><strong>ประเภทสินค้า:</strong>{{ productData.category }}</p>
      </div>
      <p v-else class="text-gray-400">กรุณาอัปโหลดภาพสินค้าเพื่อรับข้อมูล</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import axios from "axios";

const imagePreview = ref(null);
const selectedImage = ref(null);
const productData = ref(null);

// Handle file selection and preview
const previewImage = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedImage.value = file;
    const reader = new FileReader();
    reader.onload = () => {
      imagePreview.value = reader.result;
    };
    reader.readAsDataURL(file);
  }
};

// Handle form submission and upload to n8n
const handleSubmit = async () => {
  const formData = new FormData();
  if (selectedImage.value) {
    formData.append('productImage', selectedImage.value);
    await uploadImageToN8n(formData);
  }
};

// Upload image to n8n webhook
const uploadImageToN8n = async (formData) => {
  try {
    const response = await fetch('http://localhost:5678/webhook-test/upload-image', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();
      console.log('Upload successful', result);
      
      // Set product data for display
      productData.value = result;
    } else {
      alert('เกิดข้อผิดพลาดในการประเมิน');
    }
  } catch (error) {
    console.error('Error uploading image:', error);
    alert('เกิดข้อผิดพลาดในการอัปโหลด');
  }
};
</script>

<style scoped>
.upload-container {
  text-align: center;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.title {
  font-size: 1.8rem;
  margin-bottom: 20px;
}

.upload-form {
  display: inline-block;
  padding: 20px;
  border-radius: 8px;
}

.file-input {
  padding: 10px;
  margin-bottom: 15px;
}

.upload-btn {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
}

.upload-btn:hover {
  background-color: #45a049;
}

.image-preview {
  margin-top: 20px;
}

.preview-img {
  width: 200px
}

.bg-gray-800 {
};
</style>
