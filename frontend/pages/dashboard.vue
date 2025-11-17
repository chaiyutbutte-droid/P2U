<template>
  <div class="flex min-h-screen bg-gray-900 text-white relative">
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
          My Cart
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
                <div class="absolute bottom-0 left-0 right-0 bg-linear-to-t from-black/70 to-transparent p-4">
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
        <center>
          <h2 class="text-xl font-bold mb-4  mt-10 mb-5">🛒 Products</h2>
        </center>
        <!-- Product Grid -->
        <div v-if="allProducts.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          <div v-for="product in allProducts" :key="product.id"
            class="bg-gray-800 rounded-lg shadow-md p-4 cursor-pointer hover:bg-gray-700 transition"
            @click="openProduct(product)">
            <img :src="product.image_url || defaultImage" class="w-full h-40 object-cover rounded mb-3"
              @error="product.image_url = defaultImage" />
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

        <!-- ส่วนรูปสินค้า -->
        <div class="w-full md:w-1/2 flex flex-col items-center bg-gray-800 p-6">
          <img :src="selectedProduct.image_url || defaultImage" alt="Product"
            class="w-full h-96 object-contain rounded-lg bg-gray-700"
            @error="selectedProduct.image_url = defaultImage" />

          <div class="flex gap-2 mt-4">
            <img v-for="(img, i) in [selectedProduct.image_url]" :key="i"
              :src="selectedProduct.image_url || defaultImage"
              class="w-20 h-20 rounded-lg object-cover cursor-pointer border border-gray-600 hover:border-pink-400" />
          </div>
        </div>

        <!-- ส่วนรายละเอียดสินค้า -->
        <div class="flex-1 p-6 text-white flex flex-col justify-between">
          <div>
            <h2 class="text-3xl font-bold mb-2">{{ selectedProduct.name }}</h2>
            <p class="text-gray-300 mb-4">{{ selectedProduct.description }}</p>

            <div class="flex items-center gap-3 mb-4">
              <span class="text-yellow-400 text-xl">★★★★★</span>
              <span class="text-gray-400 text-sm">4.9 (3.2k รีวิว)</span>
            </div>

            <p class="text-4xl text-pink-400 font-extrabold mb-6">
              ฿{{ selectedProduct.price }}
            </p>
          </div>

          <div class="flex gap-4">
            <button class="bg-pink-600 hover:bg-white text-white hover:text-black font-bold py-3 px-8 rounded-lg flex-1"
              @click="addToCart(selectedProduct)">
              🛒 Add to Cart
            </button>
            <NuxtLink to="/payment"
              class="flex-1 flex items-center justify-center bg-green-600 hover:bg-white text-white hover:text-black font-bold py-3 px-8 rounded-lg">
              💰 Buy Now
            </NuxtLink>
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
const defaultImage = "/default-item.jpg";
const allProducts = ref([]);
const selectedProduct = ref(null);
const showCartIcon = ref(true);

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
const fetchProducts = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/products");
    allProducts.value = (res.data || []).map((p) => ({
      id: p.id || p._id,
      name: p.name,
      description: p.description,
      price: parseFloat(p.price),
      image_url: p.image_url
        ? `http://localhost:5000${p.image_url}`
        : defaultImage,
      seller: p.seller || { username: "Unknown", shop_name: "" },
    }));
  } catch (err) {
    console.error("Failed to fetch products:", err);
    allProducts.value = [];
  }
};

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
