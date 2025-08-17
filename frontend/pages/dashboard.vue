<template>
  <div class="flex min-h-screen bg-gray-900 text-white">
    <!-- Main Content -->
    <main class="flex-1 p-8">
      <!-- Products -->
      <div v-if="activeTab === 'products'">
        <h2 class="text-xl font-bold mb-4">🛒 Products</h2>
        <div v-if="allProducts.length" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          <div
            v-for="product in allProducts"
            :key="product.id"
            class="bg-gray-800 rounded-lg shadow-md p-4"
          >
            <img
              :src="product.image_url || defaultImage"
              class="w-full h-40 object-cover rounded mb-3"
            />
            <h3 class="font-semibold">{{ product.name }}</h3>
            <p class="text-sm text-gray-400">{{ product.description }}</p>
            <p class="mt-2 font-bold text-indigo-400">฿{{ product.price }}</p>
            <!-- แสดงชื่อร้านและผู้ขาย -->
            <p class="text-sm text-gray-400 mt-1">
              Seller: {{ product.seller.username }} | Shop: {{ product.seller.shop_name || 'N/A' }}
            </p>
          </div>
        </div>
        <p v-else class="text-gray-400 mt-16 text-center">🔍 No products found.</p>
      </div>

      <!-- Orders -->
      <div v-if="activeTab === 'orders'">
        <h2 class="text-xl font-bold mb-4">📦 Orders</h2>
        <p class="text-gray-400">ยังไม่มีคำสั่งซื้อ</p>
      </div>

      <!-- Profile -->
      <div v-if="activeTab === 'profile'">
        <h2 class="text-xl font-bold mb-4">👤 Profile</h2>
        <p class="text-gray-400">ข้อมูลผู้ใช้จะแสดงตรงนี้</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const activeTab = ref("products");
const defaultImage = "/default-item.jpg";
const allProducts = ref([]);

// ดึงสินค้าทุกตัวจาก public API
const fetchProducts = async () => {
  try {
    const res = await axios.get("http://localhost:5000/api/products");
    // แปลงข้อมูลให้ตรงกับ property ที่ใช้ใน template
    allProducts.value = res.data.map(p => ({
      id: p.id || p._id,
      name: p.name,
      description: p.description,
      price: p.price,
      image_url: p.image_url || defaultImage,
      seller: p.seller || { username: "Unknown", shop_name: "" } // fallback ถ้าไม่มี seller
    }));
  } catch (err) {
    console.error("Failed to fetch products:", err);
  }
};

onMounted(() => {
  fetchProducts();
});
</script>
