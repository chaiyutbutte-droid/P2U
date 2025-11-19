<template>
  <div class="layout-full flex min-h-screen bg-gray-900 text-white relative">
    <div v-if="showCartIcon" class="fixed bottom-6 right-6 z-50">
      <button @click="goToProfile" class="relative group">
        
        <!-- Blue Circle Background with Gradient -->
        <div
          class="relative w-16 h-16 bg-gradient-to-br from-black to-pink-950 rounded-full flex items-center justify-center shadow-lg shadow-pink-950 transition-all duration-300 hover:scale-110 hover:shadow-xl hover:shadow-pink-950 border-2 border-white/20">

          <!-- Cart Icon SVG -->
          <svg xmlns="http://www.w3.org/2000/svg"
            class="w-7 h-7 text-white transition-transform duration-300 group-hover:scale-110" viewBox="0 0 24 24">
            <path fill="currentColor"
              d="M7 22q-.825 0-1.412-.587T5 20t.588-1.412T7 18t1.413.588T9 20t-.587 1.413T7 22m10 0q-.825 0-1.412-.587T15 20t.588-1.412T17 18t1.413.588T19 20t-.587 1.413T17 22M6.15 6l2.4 5h7l2.75-5zM5.2 4h14.75q.575 0 .875.513t.025 1.037l-3.55 6.4q-.275.5-.737.775T15.55 13H8.1L7 15h12v2H7q-1.125 0-1.7-.987t-.05-1.963L6.6 11.6L3 4H1V2h3.25z" />
          </svg>

          <!-- Cart Count Badge -->
          <span v-if="cart.length"
            class="absolute -top-1 -right-1 bg-gradient-to-r from-pink-500 to-red-500 text-white text-xs font-bold min-w-[22px] h-[22px] flex items-center justify-center rounded-full px-1.5 shadow-lg shadow-pink-500/50 border-2 border-white animate-pulse">
            {{cart.reduce((sum, item) => sum + item.quantity, 0)}}
          </span>
        </div>

        <!-- Hover Tooltip -->
        <span
          class="absolute right-20 top-1/2 -translate-y-1/2 bg-gray-900 text-white text-sm font-medium px-4 py-2 rounded-lg opacity-0 group-hover:opacity-100 group-hover:right-[75px] transition-all duration-300 whitespace-nowrap shadow-xl pointer-events-none">
          ตะกร้า
          <span
            class="absolute right-[-6px] top-1/2 -translate-y-1/2 w-0 h-0 border-l-[6px] border-l-gray-900 border-t-[6px] border-t-transparent border-b-[6px] border-b-transparent"></span>
        </span>
      </button>
    </div>
    <!-- Main Content -->
    <main class="flex-1 p-8 ">

      <!-- Products Tab -->
      <div v-if="activeTab === 'products'">
        <!-- 🖼️ Banner Carousel -->
        <div class="relative mb-8 mt-8">
          <div class="overflow-hidden rounded-xl shadow-lg">
            <div class="flex transition-transform duration-500"
              :style="{ transform: `translateX(-${currentBanner * 100}%)` }">
              <div v-for="(banner, index) in banners" :key="index"
                class="min-w-full h-60 sm:h-72 md:h-80 bg-gray-700 relative">
                <img :src="banner.image" alt="Banner" class="w-full h-full object-cover"
                  @error="banner.image = defaultImage" />
                <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4">
                  <h3 class="text-lg font-bold">{{ banner.title }}</h3>
                  <p class="text-sm text-gray-300">{{ banner.subtitle }}</p>
                </div>
              </div>
            </div>
          </div>

          
          <!-- Navigation Buttons -->
          <button
            class="absolute top-1/2 -translate-y-1/2 left-2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full"
            @click="prevBanner">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
              <path fill="#ed9bff"
                d="m9.55 12l7.35 7.35q.375.375.363.875t-.388.875t-.875.375t-.875-.375l-7.7-7.675q-.3-.3-.45-.675t-.15-.75t.15-.75t.45-.675l7.7-7.7q.375-.375.888-.363t.887.388t.375.875t-.375.875z" />
            </svg>
          </button>
          <button
            class="absolute top-1/2 -translate-y-1/2 right-2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full"
            @click="nextBanner">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
              <path fill="#ed9bff"
                d="m14.475 12l-7.35-7.35q-.375-.375-.363-.888t.388-.887t.888-.375t.887.375l7.675 7.7q.3.3.45.675t.15.75t-.15.75t-.45.675l-7.7 7.7q-.375.375-.875.363T7.15 21.1t-.375-.888t.375-.887z" />
            </svg>
          </button>

          <!-- Indicators -->
          <div class="absolute bottom-2 left-1/2 -translate-x-1/2 flex space-x-2">
            <span v-for="(banner, index) in banners" :key="'dot-' + index" class="w-3 h-3 rounded-full"
              :class="currentBanner === index ? 'bg-white' : 'bg-gray-400'"></span>
          </div>
        </div>

         <Banner1 v-if="activeTab !== 'profile'" />

        <!-- หมวดหมู่ -->
        <Carta />
        <div class="text-center">
          <h2 class="text-xl font-bold mt-10 mb-5">🛒 สินค้า</h2>
        </div>

        <!-- Products Grid -->
        <div v-if="allProducts.length" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-4">
          <div 
            v-for="product in allProducts" 
            :key="product.id"
            class="bg-gray-800 rounded-lg shadow-lg overflow-hidden cursor-pointer transform transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-pink-500/20 border border-gray-700 hover:border-pink-500"
            @click="openProduct(product)">
            
            <!-- Product Image -->
            <div class="relative h-40 bg-gray-700 overflow-hidden group">
              <img 
                :src="product.image_url || defaultImage" 
                :alt="product.name"
                class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
                @error="product.image_url = defaultImage"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            </div>

            <!-- Product Info -->
            <div class="p-3">
              <h3 class="font-semibold text-sm mb-1 line-clamp-2 text-white">{{ product.name }}</h3>
              <p class="text-xs text-gray-400 mb-2 line-clamp-1">{{ product.description }}</p>
              
              <!-- Price -->
              <div class="flex items-center justify-between mb-2">
                <span class="text-lg font-bold text-pink-400">฿{{ product.price }}</span>
                <div class="flex items-center gap-1 text-yellow-400 text-xs">
                  <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2L9.19 8.63L2 9.24l5.46 4.73L5.82 21z"/>
                  </svg>
                  <span>4.9</span>
                </div>
              </div>

              <!-- Seller Info -->
              <div class="flex items-center gap-1.5 text-xs text-gray-500 border-t border-gray-700 pt-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-3 h-3" viewBox="0 0 24 24">
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
      </div>
        
      <!-- Orders Tab -->
      <div v-if="activeTab === 'orders'">
        <h2 class="text-xl font-bold mb-4">📦 Orders</h2>
        <p class="text-gray-400">ยังไม่มีคำสั่งซื้อ</p>
      </div>

      <!-- Profile Tab / My Cart -->
      <div v-if="activeTab === 'profile'">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-bold">👤 Profile & My Cart</h2>
          <button class="bg-indigo-600 hover:bg-indigo-700 px-3 py-1 rounded-lg font-semibold text-white" @click="
            activeTab = 'products';
          showCartIcon = true;
          ">
            ← Back to Products
          </button>
        </div>

        <div v-if="cart.length" class="space-y-4">
          <div v-for="(item, index) in cart" :key="index"
            class="bg-gray-800 p-4 rounded-lg flex justify-between items-center shadow-inner">
            <div class="flex items-center space-x-3">
              <img :src="item.image_url || defaultImage" class="w-16 h-16 object-cover rounded"
                @error="item.image_url = defaultImage" />
              <div>
                <p class="font-semibold">{{ item.name }}</p>
                <p class="text-sm text-gray-400">Qty: {{ item.quantity }}</p>
              </div>
            </div>
            <div class="flex items-center space-x-4">
              <span class="font-semibold text-pink-400">฿{{ (item.price * item.quantity).toFixed(2) }}</span>
              <button @click="removeFromCart(item)"
                class="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded-lg font-semibold">
                ✕
              </button>
            </div>
          </div>
        </div>
        <p v-else class="text-gray-400 text-center mt-4">Your cart is empty</p>
        <p class="text-right font-bold mt-2">
          Total: ฿{{
            cart
              .reduce((sum, item) => sum + item.price * item.quantity, 0)
              .toFixed(2)
          }}
        </p>
        <!-- Payment button  -->
        <div v-if="cart.length" class="flex justify-end mt-4">
          <NuxtLink to="/payment"
            class="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg shadow-lg transition-all">
            💰 Checkout
          </NuxtLink>
        </div>
      </div>
    </main>

    <!-- Product Modal -->
    <div v-if="selectedProduct" class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-60"
      @click.self="closeProduct">
      <div
        class="bg-gray-900 rounded-2xl shadow-2xl w-[90%] max-w-5xl relative flex flex-col md:flex-row overflow-hidden">
        <!-- ปุ่มปิด -->
        <button class="absolute top-4 right-4 text-gray-400 hover:text-white text-2xl" @click="closeProduct">
          ✕
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
                <div class="w-12 h-12 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
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
              class="flex-1 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-700 hover:to-purple-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-2 shadow-lg shadow-pink-500/30"
              @click="addToCart(selectedProduct)">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24">
                <path fill="currentColor" d="M7 22q-.825 0-1.412-.587T5 20t.588-1.412T7 18t1.413.588T9 20t-.587 1.413T7 22m10 0q-.825 0-1.412-.587T15 20t.588-1.412T17 18t1.413.588T19 20t-.587 1.413T17 22M6.15 6l2.4 5h7l2.75-5zM5.2 4h14.75q.575 0 .875.513t.025 1.037l-3.55 6.4q-.275.5-.737.775T15.55 13H8.1L7 15h12v2H7q-1.125 0-1.7-.987t-.05-1.963L6.6 11.6L3 4H1V2h3.25z"/>
              </svg>
              เพิ่มลงตะกร้า
            </button>
            <button
              class="flex-1 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-bold py-4 px-6 rounded-xl transition-all duration-300 transform hover:scale-105 flex items-center justify-center gap-2 shadow-lg shadow-green-500/30"
              @click="buyNow(selectedProduct)">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 24 24">
                <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.31-8.86c-1.77-.45-2.34-.94-2.34-1.67 0-.84.79-1.43 2.1-1.43 1.38 0 1.9.66 1.94 1.64h1.71c-.05-1.34-.87-2.57-2.49-2.97V5H10.9v1.69c-1.51.32-2.72 1.3-2.72 2.81 0 1.79 1.49 2.69 3.66 3.21 1.95.46 2.34 1.15 2.34 1.87 0 .53-.39 1.39-2.1 1.39-1.6 0-2.23-.72-2.32-1.64H8.04c.1 1.7 1.36 2.66 2.86 2.97V19h2.34v-1.67c1.52-.29 2.72-1.16 2.73-2.77-.01-2.2-1.9-2.96-3.66-3.42z"/>
              </svg>
              ซื้อเลย
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import axios from "axios";

// ✅ แก้ import ให้ถูกต้อง
import Carta from "~/components/Carta.vue";
import Banner1 from "~/components/banner1.vue";

// -----------------------------
// State
// -----------------------------
const activeTab = ref("products");
const defaultImage = "/default-product.svg";
const allProducts = ref([]);
const selectedProduct = ref(null);
const showCartIcon = ref(true);

// -----------------------------
// buy now
// -----------------------------
const buyNow = (product) => {
  // เพิ่มสินค้าลงตะกร้าก่อน
  const existing = cart.value.find((item) => item.id === product.id);
  if (existing) {
    existing.quantity = (existing.quantity || 1) + 1;
  } else {
    cart.value.push({ ...product, quantity: 1 });
  }
  
  // บันทึกลง localStorage
  if (process.client) {
    localStorage.setItem("cart", JSON.stringify(cart.value));
  }
  
  // ไปหน้า payment
  closeProduct();
  navigateTo('/payment');
};

// -----------------------------
// Cart - Client only
// -----------------------------
const cart = ref([]);
if (process.client) {
  cart.value = JSON.parse(localStorage.getItem("cart") || "[]");
  watch(
    cart,
    (newVal) => {
      localStorage.setItem("cart", JSON.stringify(newVal));
    },
    { deep: true }
  );
}

// -----------------------------
// Fetch products จาก API
// -----------------------------
const normalizeImage = (src) => {
  if (!src) return defaultImage
  if (/^https?:\/\//i.test(src)) return src
  const base = "http://localhost:5000"
  const normalizedBase = base.replace(/\/$/, "")
  const normalizedPath = src.startsWith("/") ? src : `/${src}`
  return `${normalizedBase}${normalizedPath}`
}

const fetchProducts = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/products")
    allProducts.value = (res.data || []).map((p) => ({
      id: p.id || p._id,
      name: p.name,
      description: p.description,
      price: parseFloat(p.price),
      image_url: normalizeImage(p.image_url),
      seller: p.seller || { username: "Unknown", shop_name: "" },
    }))
  } catch (err) {
    console.error("Failed to fetch products:", err)
    allProducts.value = []
  }
}

// -----------------------------
// Modal control
// -----------------------------
const openProduct = (product) => {
  selectedProduct.value = product;
};
const closeProduct = () => {
  selectedProduct.value = null;
};

// -----------------------------
// Cart functions
// -----------------------------
const addToCart = (product) => {
  const existing = cart.value.find((item) => item.id === product.id);
  if (existing) {
    existing.quantity = (existing.quantity || 1) + 1;
  } else {
    cart.value.push({ ...product, quantity: 1 });
  }
  closeProduct();
};

const removeFromCart = (product) => {
  if (product && product.id) {
    const existingIndex = cart.value.findIndex(
      (item) => item.id === product.id
    );
    if (existingIndex !== -1) {
      if (cart.value[existingIndex].quantity > 1) {
        cart.value[existingIndex].quantity -= 1;
      } else {
        cart.value.splice(existingIndex, 1);
      }
    }
  } else {
    console.error("Invalid product:", product);
  }
};

// -----------------------------
// Show cart
// -----------------------------
function goToProfile() {
  activeTab.value = "profile";
  showCartIcon.value = false;
}

// -----------------------------
// Banner Carousel
// -----------------------------
const banners = ref([
  {
    image:
      "https://affiliate.priceza.com/wp-content/uploads/2020/11/11.11_HotDealHotItem_HeroBanner.jpg",
    title: "SPRING / SUMMER COLLECTION 2025",
    subtitle: "Explore new digital art collections",
  },
  {
    image: "https://affiliate.priceza.com/wp-content/uploads/2020/11/4.png",
    title: "LIMITED EDITION ITEMS",
    subtitle: "Grab exclusive deals before they're gone!",
  },
  {
    image:
      "https://www.umipro.com/pub/media/wysiwyg/news-2024/NocNoc-8.8-_-__duragres_1440x365.jpg",
    title: "TOP SELLERS THIS WEEK",
    subtitle: "Check out the most popular items",
  },
]);

const currentBanner = ref(0);
let bannerInterval = null;

const nextBanner = () => {
  if (banners.value.length) {
    currentBanner.value = (currentBanner.value + 1) % banners.value.length;
  }
};
const prevBanner = () => {
  if (banners.value.length) {
    currentBanner.value =
      (currentBanner.value - 1 + banners.value.length) % banners.value.length;
  }
};

// -----------------------------
// Lifecycle
// -----------------------------
onMounted(() => {
  fetchProducts();
  if (process.client) {
    bannerInterval = setInterval(nextBanner, 5000);
  }
});

onBeforeUnmount(() => {
  if (bannerInterval) clearInterval(bannerInterval);
});
</script>