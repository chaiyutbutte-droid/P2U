<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />

    <div class="max-w-4xl mx-auto">
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-2xl font-bold text-white flex items-center gap-2">
            💖 รายการโปรด
          </h1>
          <p class="text-dark-400 mt-1">{{ wishlist.length }} รายการ</p>
        </div>
      </div>

      <div v-if="wishlist.length" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-3 gap-4">
        <div 
          v-for="product in wishlist" 
          :key="product.id" 
          class="product-card cursor-pointer group"
          @click="openProduct(product)"
        >
          <div class="aspect-square relative overflow-hidden rounded-t-xl">
            <img 
              :src="product.image_url" 
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
              @error="product.image_url = defaultImage"
            />
            <button 
              @click.stop="removeFromWishlist(product)"
              class="absolute top-2 right-2 w-8 h-8 rounded-full bg-black/50 flex items-center justify-center text-red-500 hover:bg-red-500 hover:text-white transition-colors z-10"
            >
              💖
            </button>
          </div>

          <div class="p-3">
            <h3 class="text-sm font-medium text-white truncate">{{ product.name }}</h3>
            <p class="text-xs text-dark-500 truncate mt-0.5">{{ product.description || 'ไม่มีคำอธิบายสินค้า' }}</p>
            <p class="text-xs text-dark-400 truncate mt-1">
              {{ product.seller?.shop_name || product.seller?.username || 'ร้านค้าทั่วไป' }}
            </p>
            <div class="flex items-center justify-between mt-2">
              <p class="text-lg font-bold text-primary-400">฿{{ product.price?.toLocaleString() }}</p>
              <button 
                @click.stop="addToCart(product)"
                class="bg-primary-500/20 hover:bg-primary-500 text-primary-400 hover:text-white p-2 rounded-lg transition-colors"
              >
                🛒
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-20">
        <div class="w-20 h-20 rounded-full bg-dark-800 mx-auto mb-4 flex items-center justify-center text-4xl">🔍</div>
        <p class="text-dark-400">ยังไม่มีสินค้าที่คุณถูกใจ</p>
        <NuxtLink to="/dashboard" class="btn-primary mt-4 inline-block px-6 py-2">ไปเลือกช้อปเลย</NuxtLink>
      </div>

      <Teleport to="body">
        <Transition name="fade">
          <div v-if="selectedProduct" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4" @click="closeProduct">
            <div class="glass rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col md:flex-row animate-in" @click.stop>
              
              <div class="md:w-1/2 bg-dark-900">
                <img :src="selectedProduct.image_url || defaultImage" class="w-full h-64 md:h-full object-cover" />
              </div>
              
              <div class="md:w-1/2 p-6 flex flex-col">
                <button @click="closeProduct" class="self-end text-dark-400 hover:text-white text-2xl mb-4">✕</button>
                
                <h2 class="text-2xl font-bold text-white mb-2">{{ selectedProduct.name }}</h2>
                <p class="text-dark-400 mb-4 line-clamp-4">{{ selectedProduct.description || 'ไม่มีคำอธิบายสินค้า' }}</p>
                
                <div class="flex items-center gap-2 mb-4">
                  <span class="text-yellow-400">⭐⭐⭐⭐⭐</span>
                  <span class="text-dark-400 text-sm">4.9 (123 รีวิว)</span>
                </div>
                
                <p class="text-3xl font-bold text-primary-400 mb-6">฿{{ selectedProduct.price?.toLocaleString() }}</p>
                
                <div class="text-sm text-dark-400 mb-6 font-light">
                  <p>ร้าน: {{ selectedProduct.seller?.shop_name || selectedProduct.seller?.username }}</p>
                  <p>หมวดหมู่: {{ selectedProduct.category || 'ทั่วไป' }}</p>
                </div>
                
                <div class="mt-auto flex gap-3">
                  <button @click="addToCart(selectedProduct)" class="flex-1 btn-primary py-3 rounded-xl font-bold">
                    🛒 เพิ่มลงตะกร้า
                  </button>
                  <NuxtLink to="/payment" class="flex-1 btn-accent text-center py-3 rounded-xl font-bold" @click="addToCart(selectedProduct)">
                    💳 ซื้อเลย
                  </NuxtLink>
                </div>
              </div>
            </div>
          </div>
        </Transition>
      </Teleport>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';

const wishlist = ref([]);
const selectedProduct = ref(null);
const defaultImage = '/default-item.svg';
const baseUrl = 'http://localhost:5000';

const cart = ref([]);
if (process.client) {
  cart.value = JSON.parse(localStorage.getItem("cart") || "[]");
  watch(cart, (newVal) => {
    localStorage.setItem("cart", JSON.stringify(newVal));
  }, { deep: true });
}

const fetchWishlist = async () => {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    const res = await axios.get(`${baseUrl}/api/wishlist`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    const data = res.data.wishlist || [];
    wishlist.value = data.map(p => ({
      ...p,
      id: p.id || p._id,
      // บังคับให้เก็บค่า description ไว้ในตัวแปร product
      description: p.description || '', 
      price: parseFloat(p.price) || 0,
      image_url: p.image_url 
        ? (p.image_url.startsWith('http') ? p.image_url : `${baseUrl}${p.image_url}`) 
        : defaultImage,
      seller: p.seller || { username: "Unknown", shop_name: "ร้านค้าทั่วไป" }
    }));
  } catch (err) {
    console.error('Failed to fetch wishlist:', err);
  }
};

const removeFromWishlist = async (product) => {
  const token = localStorage.getItem('token');
  try {
    await axios.delete(`${baseUrl}/api/wishlist/${product.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    wishlist.value = wishlist.value.filter(p => p.id !== product.id);
    if (selectedProduct.value?.id === product.id) closeProduct();
  } catch (err) {
    console.error('Error removing:', err);
  }
};

const openProduct = (product) => { selectedProduct.value = product; };
const closeProduct = () => { selectedProduct.value = null; };

const addToCart = (product) => {
  const existing = cart.value.find((item) => item.id === product.id);
  if (existing) existing.quantity++;
  else cart.value.push({ ...product, quantity: 1 });
  alert(`เพิ่ม ${product.name} ลงตะกร้าแล้ว!`);
};

onMounted(fetchWishlist);
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
.animate-in { animation: modalIn 0.3s ease-out; }
@keyframes modalIn {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.glass {
  background: rgba(23, 23, 23, 0.8);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
</style>