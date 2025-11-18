<template>
  <div class="flex justify-center min-h-screen bg-linear-to-br from-gray-900 to-black p-6">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-lg text-white">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-2xl font-bold">Edit Product</h1>
        <button @click="router.back()" class="px-3 py-1 rounded bg-gray-700 hover:bg-gray-600 text-sm font-semibold">
          ← Back
        </button>
      </div>

      <div v-if="loading" class="text-center text-gray-400">Loading product...</div>
      <div v-else-if="error" class="text-center text-red-400">{{ error }}</div>

      <form v-else @submit.prevent="submitProduct" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Product Name</label>
          <input v-model="name" type="text" required class="w-full p-2 rounded bg-gray-700 border border-gray-600" />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Price</label>
          <input v-model.number="price" type="number" min="0" step="0.01" required class="w-full p-2 rounded bg-gray-700 border border-gray-600" />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Description</label>
          <textarea v-model="description" class="w-full p-2 rounded bg-gray-700 border border-gray-600"></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium mb-2">Current Image</label>
          <img v-if="currentImage" :src="currentImage" alt="Current product image" class="w-full h-48 object-cover rounded mb-2 border border-gray-700" />
          <p v-else class="text-gray-400 text-sm">No image uploaded.</p>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Upload New Image (optional)</label>
          <input type="file" accept="image/*" @change="handleFileUpload" class="w-full text-gray-300" />
          <img v-if="previewImage" :src="previewImage" alt="New image preview" class="w-full h-48 object-cover rounded mt-2 border border-gray-600" />
        </div>

        <button type="submit" class="w-full py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg font-semibold transition">
          Save Changes
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const baseURL = 'http://localhost:5000';
const router = useRouter();
const route = useRoute();

const name = ref('');
const price = ref(0);
const description = ref('');
const currentImage = ref('');
const newImageFile = ref(null);
const previewImage = ref('');
const loading = ref(true);
const error = ref(null);

const productId = route.params.id;

const fetchProduct = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    router.push('/login');
    return;
  }
  try {
    const res = await axios.get(`${baseURL}/api/seller/products/${productId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    name.value = res.data.name;
    price.value = res.data.price;
    description.value = res.data.description || '';
    currentImage.value = res.data.image_url ? `${baseURL}${res.data.image_url}` : '';
  } catch (err) {
    console.error('Failed to fetch product:', err);
    error.value = 'Unable to load product. Please try again.';
  } finally {
    loading.value = false;
  }
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (!file) {
    newImageFile.value = null;
    previewImage.value = '';
    return;
  }
  newImageFile.value = file;
  previewImage.value = URL.createObjectURL(file);
};

const submitProduct = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    router.push('/login');
    return;
  }

  try {
    await axios.put(
      `${baseURL}/api/seller/products/${productId}`,
      {
        name: name.value,
        price: price.value,
        description: description.value
      },
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    );

    if (newImageFile.value) {
      const formData = new FormData();
      formData.append('image', newImageFile.value);
      await axios.put(`${baseURL}/api/seller/products/${productId}/image`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        }
      });
    }

    alert('Product updated successfully!');
    router.push('/seller');
  } catch (err) {
    console.error('Failed to update product:', err);
    alert('Failed to update product. Please try again.');
  }
};

onMounted(() => {
  fetchProduct();
});
</script>

