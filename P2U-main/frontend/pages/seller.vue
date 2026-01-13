<template>
  <div class="flex justify-center min-h-screen bg-gradient-to-br from-gray-900 to-black p-4">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-2xl text-white">
      
      <!-- Profile Header and Trust Badge -->
      <div class="flex items-start justify-between mb-8 pb-4 border-b border-gray-700">
        <div>
          <h1 class="text-3xl font-extrabold">{{ sellerProfile.shop_name || 'My Shop' }}</h1>
          <p class="text-gray-400 mt-1">{{ sellerProfile.full_name || 'N/A' }}</p>
          <div v-if="sellerProfile.is_seller_verified" class="flex items-center mt-2 text-indigo-400">
            <span class="text-xl mr-2">💎</span>
            <span class="text-sm font-semibold">Verified Seller (Trust Badge)</span>
          </div>
          <p v-else class="text-gray-400 text-sm mt-2">Not verified. <router-link to="/register-seller" class="text-indigo-400 underline">Get verified!</router-link></p>
        </div>
        <button @click="goBack" class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm font-semibold transition">
          ← Back
        </button>
      </div>

      <!-- Actions Section -->
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-xl font-bold">My Products</h2>
        <button @click="router.push('/AddProduct')" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg text-sm font-semibold transition">
          Add New Product
        </button>
      </div>

      <!-- Loading and Error States -->
      <div v-if="loading" class="text-center text-gray-400 mt-10">
        Loading products...
      </div>

      <div v-if="error" class="text-center text-red-400 mt-10">
        {{ error }}
      </div>

      <!-- Product List -->
      <div v-if="products.length > 0 && !loading" class="space-y-4">
        <div v-for="product in products" :key="product.id" class="bg-gray-800 rounded-lg p-4 shadow-md flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-4 border border-gray-700">
          <img :src="product.image_url" alt="Product Image" class="w-full md:w-20 h-20 object-cover rounded-md" />
          <div class="flex-grow w-full md:w-auto">
            <h3 class="text-lg font-semibold">{{ product.name }}</h3>
            <p class="text-indigo-400 font-bold mt-1">฿{{ product.price }}</p>
            <p class="text-gray-400 text-sm mt-1">Stock: {{ product.stock_quantity }}</p>
          </div>
          <div class="flex space-x-2 mt-4 md:mt-0">
            <button @click="editProduct(product.id)" class="p-2 bg-yellow-600 hover:bg-yellow-700 rounded text-white transition">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" />
                <path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" />
              </svg>
            </button>
            <button @click="deleteProduct(product.id)" class="p-2 bg-red-600 hover:bg-red-700 rounded text-white transition">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      
      <div v-else-if="!loading" class="text-center text-gray-400 mt-10">
        <p>You haven't listed any products yet.</p>
        <button @click="router.push('/AddProduct')" class="mt-4 px-6 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg font-semibold transition">
          Start Selling Now!
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const baseURL = 'http://localhost:5000';

const products = ref([]);
const sellerProfile = ref({});
const loading = ref(true);
const error = ref(null);

const fetchSellerProfile = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    router.push('/login');
    return;
  }
  try {
    const res = await axios.get(`${baseURL}/api/seller/profile`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    sellerProfile.value = res.data;
  } catch (err) {
    console.error('Failed to fetch seller profile:', err);
    // Continue loading products even if profile fetch fails
  }
};

const fetchProducts = async () => {
  const token = localStorage.getItem('token');
  if (!token) {
    router.push('/login');
    return;
  }
  try {
    const res = await axios.get(`${baseURL}/api/seller/products`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    products.value = res.data.map(p => ({
      ...p,
      image_url: p.image_url ? `${baseURL}${p.image_url}` : '/default-product.png'
    }));
  } catch (err) {
    console.error('Failed to fetch seller products:', err);
    error.value = 'Failed to load products. Please try again.';
  } finally {
    loading.value = false;
  }
};

const editProduct = (productId) => {
  router.push(`/edit-product/${productId}`);
};

const deleteProduct = async (productId) => {
  if (confirm('Are you sure you want to delete this product?')) {
    const token = localStorage.getItem('token');
    try {
      await axios.delete(`${baseURL}/api/seller/products/${productId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      products.value = products.value.filter(p => p.id !== productId);
      alert('Product deleted successfully.');
    } catch (err) {
      console.error('Failed to delete product:', err);
      alert('Failed to delete product.');
    }
  }
};

const goBack = () => {
  router.back();
};

onMounted(() => {
  fetchSellerProfile();
  fetchProducts();
});
</script>

<style scoped>
/* Added mobile responsiveness */
@media (max-width: 768px) {
  .flex-col {
    flex-direction: column;
  }
  .md\:w-20 {
    width: 100%;
    max-height: 12rem;
  }
  .md\:space-y-0 {
    margin-top: 1rem;
    margin-right: 0;
  }
}
</style>

