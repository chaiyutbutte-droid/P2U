<template>
  <div class="flex min-h-screen bg-gray-900 text-white relative">
    <!-- Cart Icon -->
    <div class="absolute top-4 right-6">
      <button class="relative" @click="activeTab = 'profile'">
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
        <h2 class="text-xl font-bold mb-4">🛒 Products</h2>

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
          <!-- ปุ่มกลับไปดูสินค้า -->
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
              <img
                :src="item.image_url || defaultImage"
                class="w-16 h-16 object-cover rounded"
              />
              <div>
                <p class="font-semibold">{{ item.name }}</p>
                <p class="text-sm text-gray-400">Qty: {{ item.quantity }}</p>
              </div>
            </div>
            <span class="font-semibold text-pink-400"
              >฿{{ (item.price * item.quantity).toFixed(2) }}</span
            >
          </div>
          <p class="text-right font-bold mt-2">
            Total: ฿{{
              cart
                .reduce((sum, item) => sum + item.price * item.quantity, 0)
                .toFixed(2)
            }}
          </p>
        </div>
        <p v-else class="text-gray-400 text-center mt-4">Your cart is empty</p>
      </div>
    </main>

    <!-- Product Modal -->
    <!-- <div
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
          class="mt-4 bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-lg font-semibold"
          @click="addToCart(selectedProduct)"
        >
          🛒 Add to Cart
        </button>
      </div>
    </div> -->
    <div
      v-if="selectedProduct"
      class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50 p-4"
      @click.self="closeProduct"
    >
      <div
        class="bg-gray-800 rounded-lg shadow-lg w-full max-w-4xl p-6 sm:p-12 flex flex-col sm:flex-row gap-6 relative"
      >
        <!-- Close button -->
        <button
          class="absolute top-4 right-4 text-gray-400 hover:text-white text-lg"
          @click="closeProduct"
        >
          ✖
        </button>

        <!-- Left: Product Image -->
        <div class="flex-shrink-0 sm:w-1/2">
          <img
            :src="selectedProduct.image_url || defaultImage"
            class="w-full h-80 object-cover rounded-lg"
          />
        </div>

        <!-- Right: Product Info -->
        <div class="flex-1 flex flex-col justify-between">
          <div>
            <!-- Product Name & Description -->
            <h2 class="text-2xl font-bold mb-2">{{ selectedProduct.name }}</h2>
            <p class="text-gray-300 mb-2">{{ selectedProduct.description }}</p>
            <p class="text-lg font-bold text-indigo-400 mb-3">
              ฿{{ selectedProduct.price }}
            </p>
            <p class="text-sm text-gray-400 mb-3">
              Seller: {{ selectedProduct.seller.username }} | Shop:
              {{ selectedProduct.seller.shop_name || "N/A" }}
            </p>

            <!-- Ratings / Reviews -->
            <div class="flex items-center mb-2">
              <span v-for="i in 5" :key="i" class="text-yellow-400 mr-1"
                >★</span
              >
              <span class="text-gray-400 ml-2 text-sm">
                ({{ selectedProduct.reviews?.length || 0 }} reviews)
              </span>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex flex-col gap-3 mt-4 w-full">
            <button
              class="w-full bg-indigo-600 hover:bg-indigo-700 px-4 py-3 rounded-lg font-semibold text-white text-center"
              @click="addToCart(selectedProduct)"
            >
              🛒 Add to Cart
            </button>

            <button
              class="w-full bg-green-600 hover:bg-green-700 px-4 py-3 rounded-lg font-semibold text-white text-center"
            >
              💰 Buy Now
            </button>

            <NuxtLink
              :to="`/product/${selectedProduct.id}/reviews`"
              class="w-full bg-gray-700 hover:bg-gray-600 px-4 py-3 rounded-lg font-semibold text-white text-center"
              @click="closeProduct"
            >
              ⭐ Reviews
            </NuxtLink>

            <div class="relative w-full">
              <button
                class="w-full bg-gray-800 hover:bg-gray-700 px-4 py-3 rounded-lg font-semibold text-white text-center"
              >
                ⋮ More
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import axios from "axios";

// -----------------------------
// State
// -----------------------------
const activeTab = ref("products");
const defaultImage = "/default-item.jpg";
const allProducts = ref([]);
const selectedProduct = ref(null);

// 🛒 Cart state + localStorage
const cart = ref(JSON.parse(localStorage.getItem("cart") || "[]"));

// Sync cart กับ localStorage
watch(
  cart,
  (newVal) => {
    localStorage.setItem("cart", JSON.stringify(newVal));
  },
  { deep: true }
);

// -----------------------------
// Fetch products จาก API
// -----------------------------
const fetchProducts = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/products");
    allProducts.value = res.data.map((p) => ({
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
// Lifecycle
// -----------------------------
onMounted(() => {
  fetchProducts();
});
</script>
