<template>
  <Sidebar />
  <div class="flex min-h-screen bg-gray-900 text-white relative">
    <!-- Cart Icon -->
    <div class="absolute top-4 right-6 z-90 bg-slate-500 rounded-[50%] p-2 flex-shrink-0 transition transform hover:scale-110">
      <button class="relative " @click="activeTab = 'profile'">
        <span class="text-3xl">🛒</span>
        <span
          v-if="cart.length"
          class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded-full"
        >
          {{ cart.reduce((sum, item) => sum + item.quantity, 0) }}
        </span>
      </button>
    </div>

    <!-- Main Content -->
    <main class="flex-1 p-8">
      <!-- Products Tab -->
      <div v-if="activeTab === 'products'">
        

        <!-- 🖼️ Banner Carousel -->
        <div class="relative mb-8">
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
                />
                <div
                  class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4"
                >
                  <h3 class="text-lg font-bold">{{ banner.title }}</h3>
                  <p class="text-sm text-gray-300">{{ banner.subtitle }}</p>
                </div>
              </div>
            </div>
          </div>
  <h2 class="text-xl font-bold mb-4">🛒 Products</h2>
          <!-- Navigation Buttons -->
          <button
            class="absolute top-1/2 -translate-y-1/2 left-2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full"
            @click="prevBanner"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#ed9bff" d="m9.55 12l7.35 7.35q.375.375.363.875t-.388.875t-.875.375t-.875-.375l-7.7-7.675q-.3-.3-.45-.675t-.15-.75t.15-.75t.45-.675l7.7-7.7q.375-.375.888-.363t.887.388t.375.875t-.375.875z"/></svg>
          </button>
          <button
            class="absolute top-1/2 -translate-y-1/2 right-2 bg-black/50 hover:bg-black/70 text-white p-2 rounded-full"
            @click="nextBanner"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path fill="#ed9bff" d="m14.475 12l-7.35-7.35q-.375-.375-.363-.888t.388-.887t.888-.375t.887.375l7.675 7.7q.3.3.45.675t.15.75t-.15.75t-.45.675l-7.7 7.7q-.375.375-.875.363T7.15 21.1t-.375-.888t.375-.887z"/></svg>
          </button>

          <!-- Indicators -->
          <div class="absolute bottom-2 left-1/2 -translate-x-1/2 flex space-x-2">
            <span
              v-for="(banner, index) in banners"
              :key="'dot-' + index"
              class="w-3 h-3 rounded-full"
              :class="currentBanner === index ? 'bg-white' : 'bg-gray-400'"
            ></span>
          </div>
        </div>

        <!-- Product Grid -->
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
            />
            <h3 class="font-semibold">{{ product.name }}</h3>
            <p class="text-sm text-gray-400">{{ product.description }}</p>
            <p class="mt-2 font-bold text-indigo-400">฿{{ product.price }}</p>
            <p class="text-sm text-gray-400 mt-1">
              Seller: {{ product.seller.username }} | Shop: {{ product.seller.shop_name || 'N/A' }}
            </p>
          </div>
        </div>

        <p v-else class="text-gray-400 mt-16 text-center">🔍 No products found.</p>
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
          <button
            class="bg-indigo-600 hover:bg-indigo-700 px-3 py-1 rounded-lg font-semibold text-white"
            @click="activeTab = 'products'"
          >
            ← Back to Products
          </button>
        </div>

        <div v-if="cart.length" class="space-y-4">
          <div
            v-for="(item, index) in cart"
            :key="index"
            class="bg-gray-800 p-4 rounded-lg flex justify-between items-center shadow-inner"
          >
            <div class="flex items-center space-x-3">
              <img :src="item.image_url || defaultImage" class="w-16 h-16 object-cover rounded" />
              <div>
                <p class="font-semibold">{{ item.name }}</p>
                <p class="text-sm text-gray-400">Qty: {{ item.quantity }}</p>
              </div>
            </div>
            <span class="font-semibold text-pink-400">฿{{ (item.price * item.quantity).toFixed(2) }}</span>
          </div>
          <p class="text-right font-bold mt-2">
            Total: ฿{{ cart.reduce((sum, item) => sum + item.price * item.quantity, 0).toFixed(2) }}
          </p>
        </div>
        <p v-else class="text-gray-400 text-center mt-4">Your cart is empty</p>
      </div>
    </main>

    <!-- Product Modal -->
    <div
      v-if="selectedProduct"
      class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50"
      @click.self="closeProduct"
    >
      <div class="bg-gray-800 p-6 rounded-lg shadow-lg w-full max-w-lg relative">
        <button
          class="absolute top-2 right-2 text-gray-400 hover:text-white"
          @click="closeProduct"
        >
          ✖
        </button>

        <img
          :src="selectedProduct.image_url || defaultImage"
          class="w-full h-60 object-cover rounded mb-4"
        />
        <h2 class="text-2xl font-bold mb-2">{{ selectedProduct.name }}</h2>
        <p class="text-gray-300 mb-2">{{ selectedProduct.description }}</p>
        <p class="text-lg font-bold text-indigo-400 mb-3">฿{{ selectedProduct.price }}</p>
        <p class="text-sm text-gray-400">
          Seller: {{ selectedProduct.seller.username }} | Shop: {{ selectedProduct.seller.shop_name || 'N/A' }}
        </p>

        <button
          class="mt-5 bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-lg font-semibold"
          @click="addToCart(selectedProduct)"
        >
          🛒 Add to Cart
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";
import Sidebar from '~/components/sidebar.vue'
// -----------------------------
// State
// -----------------------------
const activeTab = ref("products");
const defaultImage = "/default-item.jpg";
const allProducts = ref([]);
const selectedProduct = ref(null);

// ✅ Cart - ป้องกัน SSR
const cart = ref([]);

if (process.client) {
  cart.value = JSON.parse(localStorage.getItem("cart") || "[]");
}

// ✅ Sync cart กับ localStorage (client only)
if (process.client) {
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
      image_url: p.image_url ? `http://localhost:5000${p.image_url}` : defaultImage,
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

// -----------------------------
// Banner Carousel
// -----------------------------
const banners = ref([
  {
    image: "/banners/banner1.jpg",
    title: "SPRING / SUMMER COLLECTION 2025",
    subtitle: "Explore new digital art collections",
  },
  {
    image: "/banners/banner2.jpg",
    title: "LIMITED EDITION ITEMS",
    subtitle: "Grab exclusive deals before they're gone!",
  },
  {
    image: "/banners/banner3.jpg",
    title: "TOP SELLERS THIS WEEK",
    subtitle: "Check out the most popular items",
  },
]);

const currentBanner = ref(0);

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

  // ✅ Start Auto Slide only if client
  setInterval(nextBanner, 5000);
});
</script>
