<template>
  <div class="p-6 max-w-2xl mx-auto bg-gray-900 rounded-xl shadow-lg text-white relative min-h-screen">
    <div class="flex items-center justify-between mb-6">
      <button @click="goBack" class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded text-sm font-semibold transition">
        ← Back
      </button>
      <h1 class="text-3xl font-extrabold text-center flex-grow">Seller Dashboard</h1>
      <button @click="router.push('/add-product')" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 rounded text-sm font-semibold transition">
        Add New Product
      </button>
    </div>

    <div v-if="loading" class="text-center text-gray-400 mt-10">
      Loading products...
    </div>

    <div v-if="error" class="text-center text-red-400 mt-10">
      {{ error }}
    </div>

    <div v-if="products.length > 0" class="space-y-4">
      <h2 class="text-2xl font-bold border-b border-gray-700 pb-2">My Products ({{ products.length }})</h2>
      <div v-for="product in products" :key="product.id" class="bg-gray-800 rounded-lg p-4 shadow-md flex items-center space-x-4">
        <img :src="product.image_url" alt="Product Image" class="w-20 h-20 object-cover rounded-md" />
        <div class="flex-grow">
          <h3 class="text-lg font-semibold">{{ product.name }}</h3>
          <p class="text-indigo-400 font-bold mt-1">฿{{ product.price }}</p>
          <p class="text-gray-400 text-sm mt-1">Stock: {{ product.stock_quantity }}</p>
        </div>
        <div class="flex space-x-2">
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
        <button @click="router.push('/add-product')" class="mt-4 px-6 py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg font-semibold transition">
            Start Selling Now!
        </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const baseURL = 'http://localhost:5000'

const products = ref([])
const loading = ref(true)
const error = ref(null)

const fetchProducts = async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    router.push('/login')
    return
  }

  try {
    const res = await axios.get(`${baseURL}/api/seller/products`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    products.value = res.data.map(p => ({
        ...p,
        image_url: p.image_url ? `${baseURL}${p.image_url}` : '/default-product.png'
    }))
  } catch (err) {
    console.error('Failed to fetch seller products:', err)
    error.value = 'Failed to load products. Please try again.'
  } finally {
    loading.value = false
  }
}

const editProduct = (productId) => {
  // Logic to navigate to a product editing page
  router.push(`/edit-product/${productId}`)
}

const deleteProduct = async (productId) => {
  if (confirm('Are you sure you want to delete this product?')) {
    const token = localStorage.getItem('token')
    try {
      await axios.delete(`${baseURL}/api/seller/products/${productId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      products.value = products.value.filter(p => p.id !== productId)
      alert('Product deleted successfully.')
    } catch (err) {
      console.error('Failed to delete product:', err)
      alert('Failed to delete product.')
    }
  }
}

const goBack = () => {
  router.back()
}

onMounted(() => {
  fetchProducts()
})
</script>