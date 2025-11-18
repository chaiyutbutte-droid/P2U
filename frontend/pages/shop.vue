<template>
  <div class="layout-full min-h-screen bg-gray-900 text-white">
    <!-- Cart Floating Button -->
    <div v-if="showCartIcon" class="fixed bottom-6 right-6 z-50">
      <button @click="goToCart" class="relative group">
        <div
          class="relative w-16 h-16 bg-linear-to-br from-black to-pink-950 rounded-full flex items-center justify-center shadow-lg shadow-pink-950 transition-all duration-300 hover:scale-110 hover:shadow-xl hover:shadow-pink-950 border-2 border-white/20">
          <!-- Cart Icon -->
          <svg xmlns="http://www.w3.org/2000/svg" class="w-7 h-7 text-white transition-transform duration-300 group-hover:scale-110" viewBox="0 0 24 24">
            <path fill="currentColor" d="M7 22q-.825 0-1.412-.587T5 20t.588-1.412T7 18t1.413.588T9 20t-.587 1.413T7 22m10 0q-.825 0-1.412-.587T15 20t.588-1.412T17 18t1.413.588T19 20t-.587 1.413T17 22M6.15 6l2.4 5h7l2.75-5zM5.2 4h14.75q.575 0 .875.513t.025 1.037l-3.55 6.4q-.275.5-.737.775T15.55 13H8.1L7 15h12v2H7q-1.125 0-1.7-.987t-.05-1.963L6.6 11.6L3 4H1V2h3.25z" />
          </svg>
          
          <!-- Cart Badge -->
          <span v-if="cart.length"
            class="absolute -top-1 -right-1 bg-linear-to-r from-pink-500 to-red-500 text-white text-xs font-bold min-w-[22px] h-[22px] flex items-center justify-center rounded-full px-1.5 shadow-lg shadow-pink-500/50 border-2 border-white animate-pulse">
            {{ cart.reduce((sum, item) => sum + item.quantity, 0) }}
          </span>
        </div>

        <!-- Tooltip -->
        <span
          class="absolute right-20 top-1/2 -translate-y-1/2 bg-gray-900 text-white text-sm font-medium px-4 py-2 rounded-lg opacity-0 group-hover:opacity-100 group-hover:right-[75px] transition-all duration-300 whitespace-nowrap shadow-xl pointer-events-none">
          ตะกร้า
          <span class="absolute right-[-6px] top-1/2 -translate-y-1/2 w-0 h-0 border-l-[6px] border-l-gray-900 border-t-[6px] border-t-transparent border-b-[6px] border-b-transparent"></span>
        </span>
      </button>
    </div>

    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-5xl font-bold mb-4 bg-linear-to-r from-pink-400 to-purple-500 bg-clip-text text-transparent">
          🛍️ สินค้าทั้งหมด
        </h1>
        <p class="text-gray-400 text-lg">เลือกซื้อสินค้าคุณภาพจากร้านค้าชั้นนำ</p>
      </div>

      <!-- Search & Filter -->
      <div class="max-w-4xl mx-auto mb-8">
        <div class="flex gap-4">
          <div class="flex-1 relative">
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="ค้นหาสินค้า..."
              class="w-full bg-gray-800 text-white px-6 py-4 rounded-xl border border-gray-700 focus:border-pink-500 focus:outline-none transition-all"
            />
            <svg xmlns="http://www.w3.org/2000/svg" class="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" viewBox="0 0 24 24">
              <circle cx="11" cy="11" r="8" fill="none" stroke="currentColor" stroke-width="2"/>
              <path d="m21 21-4.35-4.35" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <select 
            v-model="sortBy"
            class="bg-gray-800 text-white px-6 py-4 rounded-xl border border-gray-700 focus:border-pink-500 focus:outline-none transition-all cursor-pointer">
            <option value="default">เรียงตาม</option>
            <option value="price-asc">ราคา: ต่ำ-สูง</option>
            <option value="price-desc">ราคา: สูง-ต่ำ</option>
            <option value="name">ชื่อสินค้า</option>
          </select>
        </div>
      </div>

      <!-- Products Grid -->
      <div v-if="filteredProducts.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
        <div 
          v-for="product in filteredProducts" 
          :key="product.id"
          class="bg-gray-800 rounded-xl shadow-lg overflow-hidden cursor-pointer transform transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-pink-500/20 border border-gray-700 hover:border-pink-500"
          @click="openProduct(product)">
          
          <!-- Product Image -->
          <div class="relative h-56 bg-gray-700 overflow-hidden group">
            <img 
              :src="product.image_url || defaultImage" 
              :alt="product.name"
              class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
              @error="product.image_url = defaultImage"
            />
            <div class="absolute inset-0 bg-linear-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
          </div>

          <!-- Product Info -->
          <div class="p-4">
            <h3 class="font-bold text-lg mb-2 line-clamp-2 text-white">{{ product.name }}</h3>
            <p class="text-sm text-gray-400 mb-3 line-clamp-2">{{ product.description }}</p>
            
            <!-- Price -->
            <div class="flex items-center justify-between mb-3">
              <span class="text-2xl font-bold text-pink-400">฿{{ product.price }}</span>
              <div class="flex items-center gap-1 text-yellow-400 text-sm">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2L9.19 8.63L2 9.24l5.46 4.73L5.82 21z"/>
                </svg>
                <span>4.9</span>
              </div>
            </div>

            <!-- Seller Info -->
            <div class="flex items-center gap-2 text-xs text-gray-500 border-t border-gray-700 pt-3">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" viewBox="0 0 24 24">
                <path fill="currentColor" d="M12 12q-1.65 0-2.825-1.175T8 8t1.175-2.825T12 4t2.825 1.175T16 8t-1.175 2.825T12 12m-8 8v-2.8q0-.85.438-1.562T5.6 14.55q1.55-.775 3.15-1.162T12 13t3.25.388t3.15 1.162q.725.375 1.163 1.088T20 17.2V20z"/>
              </svg>
              <span class="truncate">{{ product.seller.username }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- No Products Found -->
      <div v-else class="text-center py-20">
        <div class="text-6xl mb-4">🔍</div>
        <p class="text-gray-400 text-xl">ไม่พบสินค้าที่ค้นหา</p>
      </div>
    </main>

    <!-- Product Modal -->
    <div 
      v-if="selectedProduct" 
      class="fixed inset-0 flex items-center justify-center z-50 bg-black/70 backdrop-blur-sm px-4"
      @click.self="closeProduct">
      <div class="bg-gray-900 rounded-2xl shadow-2xl w-full max-w-5xl relative flex flex-col md:flex-row overflow-hidden border border-gray-800 max-h-[90vh] overflow-y-auto">
        
        <!-- Close Button -->
        <button 
          class="absolute top-4 right-4 z-10 bg-gray-800 hover:bg-gray-700 text-white w-10 h-10 rounded-full flex items-center justify-center transition-all" 
          @click="closeProduct">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" viewBox="0 0 24 24">
            <path fill="currentColor" d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12z"/>
          </svg>
        </button>

        <!-- Product Image Section -->
        <div class="w-full md:w-1/2 bg-gray-800 p-8 flex items-center justify-center">
          <img 
            :src="selectedProduct.image_url || defaultImage" 
            :alt="selectedProduct.name"
            class="w-full h-auto max-h-96 object-contain rounded-lg"
            @error="selectedProduct.image_url = defaultImage"
          />
        </div>

        <!-- Product Details Section -->
        <div class="flex-1 p-8 flex flex-col justify-between">
          <div>
            <!-- Title -->
            <h2 class="text-3xl font-bold mb-4 text-white">{{ selectedProduct.name }}</h2>
            
            <!-- Description -->
            <p class="text-gray-300 mb-6 leading-relaxed">{{ selectedProduct.description }}</p>

            <!-- Rating -->
            <div class="flex items-center gap-3 mb-6">
              <div class="flex text-yellow-400 text-xl">
                <span v-for="i in 5" :key="i">★</span>
              </div>
              <span class="text-gray-400 text-sm">4.9 (3.2k รีวิว)</span>
            </div>

            <!-- Price -->
            <div class="bg-gray-800 rounded-xl p-6 mb-6">
              <p class="text-gray-400 text-sm mb-2">ราคา</p>
              <p class="text-4xl font-extrabold text-pink-400">฿{{ selectedProduct.price }}</p>
            </div>

            <!-- Seller Info -->
            <div class="bg-gray-800 rounded-xl p-4 mb-6">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-linear-to-br from-pink-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
                  {{ selectedProduct.seller.username.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <p class="font-semibold text-white">{{ selectedProduct.seller.username }}</p>
                  <p class="text-sm text-gray-400">{{ selectedProduct.seller.shop_name || 'ร้านค้า' }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex gap-4">
            <button 
              class="flex-1 bg-linear-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-2 shadow-lg shadow-pink-500/30"
              @click="addToCart(selectedProduct)">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24">
                <path fill="currentColor" d="M7 22q-.825 0-1.412-.587T5 20t.588-1.412T7 18t1.413.588T9 20t-.587 1.413T7 22m10 0q-.825 0-1.412-.587T15 20t.588-1.412T17 18t1.413.588T19 20t-.587 1.413T17 22M6.15 6l2.4 5h7l2.75-5zM5.2 4h14.75q.575 0 .875.513t.025 1.037l-3.55 6.4q-.275.5-.737.775T15.55 13H8.1L7 15h12v2H7q-1.125 0-1.7-.987t-.05-1.963L6.6 11.6L3 4H1V2h3.25z"/>
              </svg>
              เพิ่มลงตะกร้า
            </button>
            <NuxtLink 
              to="/payment"
              class="flex-1 bg-linear-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-2 shadow-lg shadow-green-500/30">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24">
                <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.31-8.86c-1.77-.45-2.34-.94-2.34-1.67 0-.84.79-1.43 2.1-1.43 1.38 0 1.9.66 1.94 1.64h1.71c-.05-1.34-.87-2.57-2.49-2.97V5H10.9v1.69c-1.51.32-2.72 1.3-2.72 2.81 0 1.79 1.49 2.69 3.66 3.21 1.95.46 2.34 1.15 2.34 1.87 0 .53-.39 1.39-2.1 1.39-1.6 0-2.23-.72-2.32-1.64H8.04c.1 1.7 1.36 2.66 2.86 2.97V19h2.34v-1.67c1.52-.29 2.72-1.16 2.73-2.77-.01-2.2-1.9-2.96-3.66-3.42z"/>
              </svg>
              ซื้อเลย
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'

// State
const defaultImage = '/default-product.svg'
const allProducts = ref([])
const selectedProduct = ref(null)
const showCartIcon = ref(true)
const searchQuery = ref('')
const sortBy = ref('default')

// Cart - Client only
const cart = ref([])
if (process.client) {
  cart.value = JSON.parse(localStorage.getItem('cart') || '[]')
  watch(cart, (newVal) => {
    localStorage.setItem('cart', JSON.stringify(newVal))
  }, { deep: true })
}

// Fetch products from API
const fetchProducts = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/products')
    allProducts.value = (res.data || []).map(p => ({
      id: p.id || p._id,
      name: p.name,
      description: p.description,
      price: parseFloat(p.price),
      image_url: p.image_url ? `http://localhost:5000${p.image_url}` : defaultImage,
      seller: p.seller || { username: 'Unknown', shop_name: '' }
    }))
  } catch (err) {
    console.error('Failed to fetch products:', err)
    allProducts.value = []
  }
}

// Filtered and Sorted Products
const filteredProducts = computed(() => {
  let products = [...allProducts.value]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    products = products.filter(p => 
      p.name.toLowerCase().includes(query) || 
      p.description.toLowerCase().includes(query)
    )
  }

  // Sort
  if (sortBy.value === 'price-asc') {
    products.sort((a, b) => a.price - b.price)
  } else if (sortBy.value === 'price-desc') {
    products.sort((a, b) => b.price - a.price)
  } else if (sortBy.value === 'name') {
    products.sort((a, b) => a.name.localeCompare(b.name))
  }

  return products
})

// Modal control
const openProduct = (product) => {
  selectedProduct.value = product
}

const closeProduct = () => {
  selectedProduct.value = null
}

// Cart functions
const addToCart = (product) => {
  const existing = cart.value.find(item => item.id === product.id)
  if (existing) {
    existing.quantity = (existing.quantity || 1) + 1
  } else {
    cart.value.push({ ...product, quantity: 1 })
  }
  closeProduct()
}

const goToCart = () => {
  // Navigate to cart page or show cart modal
  navigateTo('/cart') // หรือแสดง cart modal
}

// Lifecycle
onMounted(() => {
  fetchProducts()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-clamp: 2;
  overflow: hidden;
}
</style>