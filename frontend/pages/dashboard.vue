<template>
  <div class="min-h-screen ml-20">
    <Navbar />
    <sidebar />

    <main class="p-6">
      <div class="fixed bottom-8 right-8 z-50">
        <NuxtLink to="/cart" class="group relative flex items-center justify-center">
          <div class="absolute inset-0 bg-primary-500 rounded-full blur-xl opacity-40 group-hover:opacity-70 group-hover:scale-125 transition-all duration-500"></div>
          
          <button class="relative w-16 h-16 bg-gradient-to-br from-pink-400 to-primary-600 rounded-full shadow-[0_0_20px_rgba(236,72,153,0.5)] border-2 border-white/30 flex items-center justify-center text-2xl transition-all duration-300 group-hover:scale-110 group-hover:-rotate-12 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full group-hover:animate-shimmer"></div>
            <span class="relative z-10 filter drop-shadow-md">🛒</span>
          </button>

          <span 
            v-if="totalCartItems > 0"
            class="absolute -top-1 -right-1 bg-white text-primary-600 text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center shadow-lg border-2 border-primary-500 animate-bounce"
          >
            {{ totalCartItems }}
          </span>
          
          <span class="absolute right-20 bg-dark-800 text-white text-xs py-2 px-3 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none border border-white/10 whitespace-nowrap">
            ดูตะกร้าสินค้า ✨
          </span>
        </NuxtLink>
      </div>

      <div class="relative mb-8 rounded-2xl overflow-hidden shadow-lg">
        <div class="flex transition-transform duration-500" :style="{ transform: `translateX(-${currentBanner * 100}%)` }">
          <div v-for="(banner, index) in banners" :key="index" class="min-w-full h-64 md:h-80 relative">
            <img :src="banner.image" alt="Banner" class="w-full h-full object-cover" @error="banner.image = defaultImage" />
            <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
            <div class="absolute bottom-6 left-6">
              <h3 class="text-2xl font-bold text-white mb-1">{{ banner.title }}</h3>
              <p class="text-dark-300">{{ banner.subtitle }}</p>
            </div>
          </div>
        </div>
        
        <button @click="prevBanner" class="absolute left-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-black/50 hover:bg-primary-500 rounded-full flex items-center justify-center text-white transition-colors"> ← </button>
        <button @click="nextBanner" class="absolute right-4 top-1/2 -translate-y-1/2 w-10 h-10 bg-black/50 hover:bg-primary-500 rounded-full flex items-center justify-center text-white transition-colors"> → </button>
        
        <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-2">
          <span v-for="(_, index) in banners" :key="'dot-' + index" class="w-2 h-2 rounded-full transition-colors" :class="currentBanner === index ? 'bg-primary-500' : 'bg-white/50'"></span>
        </div>
      </div>

      <ProductCategories @category-change="filterByCategory" />

      <div class="flex items-center justify-between mb-6">
        <h2 class="text-xl font-bold text-white">
          🛍️ สินค้าทั้งหมด
          <span class="text-dark-400 text-sm font-normal ml-2">({{ filteredProducts.length }} รายการ)</span>
        </h2>
        <div class="flex gap-2">
          <button @click="sortBy = 'latest'" class="px-3 py-1.5 rounded-lg text-sm" :class="sortBy === 'latest' ? 'bg-primary-500 text-white' : 'glass text-dark-300'">ล่าสุด</button>
          <button @click="sortBy = 'price-low'" class="px-3 py-1.5 rounded-lg text-sm" :class="sortBy === 'price-low' ? 'bg-primary-500 text-white' : 'glass text-dark-300'">ราคาต่ำ</button>
          <button @click="sortBy = 'price-high'" class="px-3 py-1.5 rounded-lg text-sm" :class="sortBy === 'price-high' ? 'bg-primary-500 text-white' : 'glass text-dark-300'">ราคาสูง</button>
        </div>
      </div>

      <div v-if="filteredProducts.length" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
        <div v-for="product in filteredProducts" :key="product.id" class="product-card cursor-pointer group" @click="openProduct(product)">
          <div class="aspect-square relative overflow-hidden">
            <img :src="product.image_url || defaultImage" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300" @error="product.image_url = defaultImage" />
            <button @click.stop="toggleWishlist(product)" class="absolute top-2 right-2 w-8 h-8 rounded-full bg-black/50 flex items-center justify-center text-white hover:bg-red-500 transition-colors"> 💖 </button>
          </div>
          <div class="p-3">
            <h3 class="text-sm font-medium text-white truncate">{{ product.name }}</h3>
            <p class="text-xs text-dark-400 truncate mt-0.5">{{ product.seller?.shop_name || product.seller?.username }}</p>
            <p class="text-lg font-bold text-primary-400 mt-2">฿{{ product.price?.toLocaleString() }}</p>
          </div>
        </div>
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
                <p class="text-dark-400 mb-4">{{ selectedProduct.description }}</p>
                
                <div class="flex items-center gap-2 mb-4">
                  <span class="text-yellow-400">⭐⭐⭐⭐⭐</span>
                  <span class="text-dark-400 text-sm">4.9 (123 รีวิว)</span>
                </div>
                
                <p class="text-3xl font-bold text-primary-400 mb-6">฿{{ selectedProduct.price?.toLocaleString() }}</p>
                
                <div class="text-sm text-dark-400 mb-6">
                  <p>ร้าน: {{ selectedProduct.seller?.shop_name || selectedProduct.seller?.username }}</p>
                </div>
                
                <div class="mt-auto flex gap-3">
                  <button @click="addToCart(selectedProduct)" class="flex-1 btn-primary">
                    🛒 เพิ่มลงตะกร้า
                  </button>
                  <button @click="buyNow(selectedProduct)" class="flex-1 btn-accent">
                    💳 ซื้อเลย
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
import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";
import axios from "axios";
import { useRouter } from 'vue-router';

const router = useRouter();
const defaultImage = "/default-item.svg";
const allProducts = ref([]);
const selectedProduct = ref(null);
const selectedCategory = ref('all');
const sortBy = ref('latest');

// --- 🛒 ระบบตระกร้าแบบแยก User (Logic ใหม่ที่เสถียรขึ้น) ---

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

// นับจำนวนชิ้นทั้งหมด (เพื่อให้เลขที่ Badge เด้งตามจริง)
const totalCartItems = computed(() => {
  return cart.value.reduce((total, item) => total + item.quantity, 0);
});

// Watch และบันทึกลง LocalStorage ตาม User Key
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
    // ใส่ selected: true เพื่อให้ในหน้า Cart ติ๊กถูกให้อัตโนมัติ
    cart.value.push({ ...product, quantity: 1, selected: true });
  }
  closeProduct();
};

const buyNow = (product) => {
  addToCart(product);
  router.push('/cart');
};

// --- 🖼️ ระบบ Banner & การดึงข้อมูล ---

const banners = ref([
  { image: "https://affiliate.priceza.com/wp-content/uploads/2020/11/11.11_HotDealHotItem_HeroBanner.jpg", title: "🎉 MEGA SALE 11.11", subtitle: "ลดสูงสุด 90% ทุกหมวดหมู่!" },
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
    const res = await axios.get("http://localhost:5000/api/products");
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
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>