<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-pink-500/30">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <main class="ml-20 p-6 md:p-8 max-w-[1600px] mx-auto pb-24">
      
      <div class="relative w-full h-[220px] md:h-[300px] rounded-2xl overflow-hidden shadow-2xl border border-white/5 group mb-10">
        <div class="flex h-full transition-transform duration-700 ease-[cubic-bezier(0.25,1,0.5,1)]" :style="{ transform: `translateX(-${currentBanner * 100}%)` }">
          <div v-for="(banner, index) in banners" :key="index" class="min-w-full h-full relative">
            <img :src="banner.image" alt="Banner" class="w-full h-full object-cover transform scale-105" @error="banner.image = defaultImage" />
            <div class="absolute inset-0 bg-gradient-to-r from-[#09090b] via-transparent to-transparent"></div>
            
            <div class="absolute bottom-8 left-8 md:left-12 max-w-xl">
              <span class="px-3 py-1 bg-pink-600/20 text-pink-400 border border-pink-500/20 text-[10px] md:text-xs font-bold rounded-full uppercase tracking-wider mb-3 inline-block backdrop-blur-md">
                 Recommended
              </span>
              <h3 class="text-3xl md:text-5xl font-extrabold text-white mb-2 drop-shadow-lg leading-tight">
                {{ banner.title }}
              </h3>
              <p class="text-sm md:text-base text-gray-200 font-medium opacity-90">
                {{ banner.subtitle }}
              </p>
            </div>
          </div>
        </div>

        <button @click="prevBanner" class="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-black/30 hover:bg-white/10 backdrop-blur border border-white/10 rounded-full flex items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-opacity">
          ←
        </button>
        <button @click="nextBanner" class="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-black/30 hover:bg-white/10 backdrop-blur border border-white/10 rounded-full flex items-center justify-center text-white opacity-0 group-hover:opacity-100 transition-opacity">
          →
        </button>
        
        <div class="absolute bottom-4 right-6 flex gap-2">
          <button v-for="(_, index) in banners" :key="'dot-' + index" @click="currentBanner = index" class="w-2 h-2 rounded-full transition-all duration-300" :class="currentBanner === index ? 'bg-white w-6' : 'bg-white/40'"></button>
        </div>
      </div>

      <div class="mb-8 bg-[#121215] rounded-2xl border border-white/5 p-4 shadow-lg">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
          
          <div class="flex-1 w-full overflow-hidden">
             <ProductCategories @category-change="filterByCategory" />
          </div>

          <div class="flex items-center gap-3 shrink-0 border-t md:border-t-0 md:border-l border-white/5 pt-4 md:pt-0 md:pl-6">
             <span class="text-xs text-gray-500 hidden xl:block">เรียงตาม:</span>
             <div class="flex bg-[#09090b] rounded-lg p-1 border border-white/5">
                <button @click="sortBy = 'latest'" class="px-3 py-1.5 text-xs font-medium rounded-md transition-all" :class="sortBy === 'latest' ? 'bg-white/10 text-white' : 'text-gray-500 hover:text-gray-300'">ใหม่</button>
                <button @click="sortBy = 'price-low'" class="px-3 py-1.5 text-xs font-medium rounded-md transition-all" :class="sortBy === 'price-low' ? 'bg-white/10 text-white' : 'text-gray-500 hover:text-gray-300'">ราคาต่ำ</button>
                <button @click="sortBy = 'price-high'" class="px-3 py-1.5 text-xs font-medium rounded-md transition-all" :class="sortBy === 'price-high' ? 'bg-white/10 text-white' : 'text-gray-500 hover:text-gray-300'">ราคาสูง</button>
             </div>
          </div>
        </div>
      </div>

      <div v-if="searchQuery" class="flex items-center gap-3 mb-6 animate-pulse">
        <h2 class="text-2xl font-bold text-white">ผลลัพธ์: <span class="text-pink-400">"{{ searchQuery }}"</span></h2>
        <button @click="clearSearch" class="text-sm text-gray-500 hover:text-white underline">ล้างค่า</button>
      </div>

      <div v-if="!filteredProducts.length && searchQuery" class="text-center py-24 opacity-50">
        <div class="text-6xl mb-4">🌪️</div>
        <h3 class="text-xl font-bold">ไม่พบสินค้า</h3>
      </div>

      <div v-else-if="filteredProducts.length" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-5">
        <div 
          v-for="product in filteredProducts" 
          :key="product.id" 
          class="group relative bg-[#121215] rounded-xl border border-white/5 hover:border-pink-500/30 overflow-hidden cursor-pointer transition-all duration-300 hover:-translate-y-1 hover:shadow-xl" 
          @click="openProduct(product)"
        >
          <div class="aspect-[4/5] relative overflow-hidden bg-[#09090b]">
            <img :src="product.image_url || defaultImage" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" @error="product.image_url = defaultImage" />
            <div class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity"></div>
            <button @click.stop="toggleWishlist(product)" class="absolute top-2 right-2 w-8 h-8 rounded-full bg-black/40 backdrop-blur flex items-center justify-center text-white/50 hover:text-pink-500 hover:bg-black/60 transition-all opacity-0 group-hover:opacity-100">❤</button>
          </div>

          <div class="p-4">
            <h3 class="text-sm font-medium text-gray-200 truncate group-hover:text-pink-300">{{ product.name }}</h3>
            <div class="flex items-center justify-between mt-2">
               <span class="text-base font-bold text-white">฿{{ product.price?.toLocaleString() }}</span>
               <span class="text-[10px] text-gray-500 border border-white/10 px-1.5 py-0.5 rounded">{{ product.category }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="fixed bottom-8 right-8 z-[60]">
        <NuxtLink to="/cart" class="group relative flex items-center justify-center">
          <div class="absolute inset-0 bg-pink-500 rounded-full blur-xl opacity-20 group-hover:opacity-50 transition-all duration-500"></div>
          <button class="relative w-16 h-16 bg-[#121215] rounded-full border border-white/10 flex items-center justify-center text-2xl shadow-2xl transition-all duration-300 group-hover:border-pink-500/50 group-hover:scale-110 text-white">
            🛒
          </button>
          <span v-if="totalCartItems > 0" class="absolute -top-1 -right-1 bg-red-500 text-white text-[10px] font-bold min-w-[20px] h-[20px] px-1 rounded-full flex items-center justify-center border-2 border-[#09090b] animate-bounce">
            {{ totalCartItems }}
          </span>
        </NuxtLink>
      </div>

      <Teleport to="body">
        <Transition name="fade">
          <div v-if="selectedProduct" class="fixed inset-0 z-[100] flex items-center justify-center p-4" @click="closeProduct">
            <div class="absolute inset-0 bg-black/80 backdrop-blur-md"></div>
            
            <div class="relative w-full max-w-5xl bg-[#121215] rounded-3xl border border-white/10 shadow-[0_0_50px_rgba(0,0,0,0.5)] flex flex-col md:flex-row overflow-hidden animate-in" @click.stop>
              
              <div class="md:w-1/2 bg-[#09090b] relative h-72 md:h-auto group">
                <img :src="selectedProduct.image_url || defaultImage" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-105" />
                <div class="absolute inset-0 bg-gradient-to-t from-[#121215] via-transparent to-transparent md:bg-gradient-to-r"></div>
                <button @click="closeProduct" class="absolute top-4 left-4 md:hidden w-8 h-8 bg-black/50 rounded-full text-white flex items-center justify-center">✕</button>
              </div>
              
              <div class="md:w-1/2 p-6 md:p-10 flex flex-col bg-[#121215] max-h-[90vh] overflow-y-auto custom-scrollbar">
                
                <div class="flex justify-between items-start mb-4">
                   <div>
                     <h2 class="text-3xl md:text-4xl font-bold text-white mb-2 leading-tight">{{ selectedProduct.name }}</h2>
                     <div class="flex items-center gap-3">
                        <div class="flex text-yellow-500 text-sm">★★★★★</div>
                        <span class="text-xs text-gray-400 border-l border-white/10 pl-3">4.9 (123 รีวิว) | ขายแล้ว 500+ ชิ้น</span>
                     </div>
                   </div>
                   <button @click="closeProduct" class="hidden md:flex w-8 h-8 rounded-full bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white items-center justify-center transition-colors">✕</button>
                </div>

                <div class="my-6 p-5 bg-gradient-to-r from-white/5 to-transparent rounded-2xl border border-white/5 flex items-center justify-between">
                   <div>
                     <p class="text-xs text-gray-400 mb-1">ราคาพิเศษ</p>
                     <p class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                        ฿{{ selectedProduct.price?.toLocaleString() }}
                     </p>
                   </div>
                   <div class="text-right">
                      <span class="block text-xs text-gray-400 mb-1">ผู้ขาย</span>
                      <div class="flex items-center justify-end gap-2">
                         <div class="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-[10px]">🏪</div>
                         <span class="text-sm font-medium text-white">{{ selectedProduct.seller?.shop_name || selectedProduct.seller?.username }}</span>
                      </div>
                   </div>
                </div>

                <div class="flex-1 mb-6">
                  <h4 class="text-sm font-bold text-gray-300 mb-2 uppercase tracking-wide border-b border-white/5 pb-2">รายละเอียดสินค้า</h4>
                  <p class="text-gray-400 leading-relaxed font-light text-sm md:text-base whitespace-pre-line">
                    {{ selectedProduct.description || 'ไม่มีรายละเอียดสินค้าเพิ่มเติม... สินค้านี้คุณภาพดีเยี่ยม เหมาะสำหรับการใช้งานทั่วไป' }}
                  </p>
                </div>

                <div class="mt-auto pt-6 border-t border-white/10 flex flex-col sm:flex-row gap-3">
                  <button 
                    @click="addToCart(selectedProduct)" 
                    class="flex-1 py-3.5 rounded-xl border border-white/10 text-white font-bold hover:bg-white/5 transition-all flex items-center justify-center gap-2 group/btn"
                  >
                    <span class="group-hover/btn:scale-110 transition-transform">🛒</span> เพิ่มลงตะกร้า
                  </button>
                  <button 
                    @click="buyNow(selectedProduct)" 
                    class="flex-1 py-3.5 rounded-xl bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white font-bold shadow-lg shadow-purple-900/20 hover:shadow-purple-500/40 transition-all transform hover:-translate-y-1 flex items-center justify-center gap-2"
                  >
                    <span>⚡</span> ซื้อเลย
                  </button>
                </div>
              </div>

            </div>
          </div>
        </Transition>
      </Teleport>

    </main>
  </div>
</template>

<script setup>
// สคริปต์เดิม 100%
import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";
import axios from "axios";
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();
const defaultImage = "/default-item.svg";
const allProducts = ref([]);
const selectedProduct = ref(null);
const selectedCategory = ref('all');
const sortBy = ref('latest');
const searchQuery = ref('');

const getCartKey = () => {
  if (process.client) {
    const user = localStorage.getItem('user');
    if (user) {
      const userData = JSON.parse(user);
      return `cart_${userData.id || userData._id || userData.email}`;
    }
  }
  return 'cart_guest';
};

const cart = ref([]);

const loadCart = () => {
  if (process.client) {
    const key = getCartKey();
    const saved = localStorage.getItem(key);
    cart.value = saved ? JSON.parse(saved) : [];
  }
};

const totalCartItems = computed(() => {
  return cart.value.reduce((total, item) => total + item.quantity, 0);
});

watch(cart, (newVal) => {
  if (process.client) {
    const key = getCartKey();
    localStorage.setItem(key, JSON.stringify(newVal));
  }
}, { deep: true });

const addToCart = (product) => {
  const existing = cart.value.find((item) => item.id === product.id);
  if (existing) {
    existing.quantity++;
  } else {
    cart.value.push({ ...product, quantity: 1, selected: true });
  }
  closeProduct();
};

const buyNow = (product) => {
  addToCart(product);
  router.push('/cart');
};

const banners = ref([
  { image: "https://media.discordapp.net/attachments/1089887523020480544/1461399560713933054/P2U_kaiser_1.png?ex=696a69e6&is=69691866&hm=c8f4838915fb6ffac9c2cce2d582e023355652bd82b750fdbfeaac399e21b3c2&=&format=webp&quality=lossless&width=1679&height=839", title: "🎉 MEGA SALE 21.1", subtitle: "ลดสูงสุด 50% ทุกหมวดหมู่!" },
  { image: "https://affiliate.priceza.com/wp-content/uploads/2020/11/4.png", title: "💎 สินค้า Limited Edition", subtitle: "ของหายากราคาพิเศษ" },
  { image: "https://www.umipro.com/pub/media/wysiwyg/news-2024/NocNoc-8.8-_-__duragres_1440x365.jpg", title: "🔥 Flash Sale", subtitle: "เฉพาะวันนี้เท่านั้น!" },
]);
const currentBanner = ref(0);
let bannerInterval = null;

const nextBanner = () => { currentBanner.value = (currentBanner.value + 1) % banners.value.length; };
const prevBanner = () => { currentBanner.value = (currentBanner.value - 1 + banners.value.length) % banners.value.length; };

const filteredProducts = computed(() => {
  let products = [...allProducts.value];
  if (selectedCategory.value !== 'all') products = products.filter(p => p.category === selectedCategory.value);
  if (sortBy.value === 'price-low') products.sort((a, b) => a.price - b.price);
  else if (sortBy.value === 'price-high') products.sort((a, b) => b.price - a.price);
  return products;
});

const filterByCategory = (cat) => { selectedCategory.value = cat; };

const fetchProducts = async () => {
  try {
    const params = searchQuery.value ? { q: searchQuery.value } : {};
    const res = await axios.get("http://localhost:5000/api/products", { params });
    allProducts.value = (res.data || []).map((p) => ({
      id: p.id || p._id,
      name: p.name,
      description: p.description,
      price: parseFloat(p.price),
      category: p.category || 'all',
      image_url: p.image_url ? `http://localhost:5000${p.image_url}` : defaultImage,
      seller: p.seller || { username: "Unknown", shop_name: "" },
    }));
  } catch (err) {
    allProducts.value = [];
  }
};

const clearSearch = () => {
  router.push('/dashboard');
};

watch(() => route.query.q, (newQuery) => {
  searchQuery.value = newQuery || '';
  fetchProducts();
}, { immediate: true });

const openProduct = (product) => { selectedProduct.value = product; };
const closeProduct = () => { selectedProduct.value = null; };

const toggleWishlist = async (product) => {
  const token = localStorage.getItem('token');
  if (!token) return;
  try {
    await axios.post(`http://localhost:5000/api/wishlist/${product.id}`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
  } catch (err) { console.error(err); }
};

onMounted(() => {
  fetchProducts();
  loadCart(); 
  bannerInterval = setInterval(nextBanner, 5000);
});

onBeforeUnmount(() => { if (bannerInterval) clearInterval(bannerInterval); });
</script>

<style scoped>
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

.animate-in { animation: modal-pop 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes modal-pop {
  0% { opacity: 0; transform: scale(0.95) translateY(10px); }
  100% { opacity: 1; transform: scale(1) translateY(0); }
}

.custom-scrollbar::-webkit-scrollbar { width: 5px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 10px; }
</style>