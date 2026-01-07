<template>
  <div class="min-h-screen ml-20 p-6 text-white bg-dark-950">
    <Navbar />
    <sidebar />

    <div class="max-w-5xl mx-auto mt-8">
      <header class="flex items-center justify-between mb-10">
        <div>
          <h1 class="text-3xl font-bold bg-gradient-to-r from-white to-pink-300 bg-clip-text text-transparent">
            รถเข็นของเจ้าหญิง ✨
          </h1>
          <p class="text-dark-400 mt-1">มีสินค้าทั้งหมด {{ totalItems }} ชิ้นในตระกร้า</p>
        </div>
        <NuxtLink to="/dashboard" class="text-sm text-pink-400 hover:text-pink-300 flex items-center gap-2 transition-colors">
          <span>←</span> กลับไปช้อปต่อ
        </NuxtLink>
      </header>

      <div v-if="cart.length > 0" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2 space-y-4">
          <div v-for="item in cart" :key="item.id" 
               class="glass p-5 rounded-3xl flex items-center gap-6 border border-white/5 hover:border-pink-500/30 transition-all duration-300 group">
            
            <img :src="item.image_url" class="w-24 h-24 object-cover rounded-2xl shadow-xl" />
            
            <div class="flex-1 min-w-0">
              <h3 class="text-lg font-bold text-white truncate">{{ item.name }}</h3>
              <p class="text-sm text-dark-400 mt-0.5">ร้าน: {{ item.seller?.shop_name || 'General Store' }}</p>
              <p class="text-xl font-black text-pink-400 mt-2">฿{{ item.price?.toLocaleString() }}</p>
            </div>

            <div class="flex flex-col items-end gap-3">
              <div class="flex items-center bg-dark-800/50 rounded-xl border border-white/10 p-1">
                <button @click="updateQty(item, -1)" class="w-8 h-8 hover:text-pink-400">-</button>
                <span class="w-8 text-center font-bold">{{ item.quantity }}</span>
                <button @click="updateQty(item, 1)" class="w-8 h-8 hover:text-pink-400">+</button>
              </div>
              <button @click="removeItem(item)" class="text-xs text-red-400/60 hover:text-red-400">ลบสินค้า</button>
            </div>
          </div>
        </div>

        <div class="lg:col-span-1">
          <div class="glass p-8 rounded-[2rem] border border-pink-500/20 sticky top-28">
            <h2 class="text-xl font-bold mb-6">สรุปยอดชำระ ✨</h2>
            <div class="space-y-4 mb-8">
              <div class="flex justify-between text-dark-400">
                <span>ยอดรวม</span>
                <span>฿{{ totalPrice.toLocaleString() }}</span>
              </div>
              <div class="h-px bg-white/10 my-2"></div>
              <div class="flex justify-between items-end">
                <span class="text-lg">ยอดสุทธิ</span>
                <span class="text-3xl font-black text-pink-500">฿{{ totalPrice.toLocaleString() }}</span>
              </div>
            </div>
            <button @click="checkout" class="w-full py-4 bg-gradient-to-r from-pink-500 to-rose-600 rounded-2xl font-bold text-lg hover:scale-[1.02] transition-all shadow-lg shadow-pink-500/20">
              ชำระเงินตอนนี้ 💖
            </button>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-32 glass rounded-[3rem] border border-white/5 animate-in">
        <div class="text-8xl mb-6">🏰</div>
        <h2 class="text-2xl font-bold text-white mb-2">ตะกร้าว่างเปล่าเพคะ</h2>
        <NuxtLink to="/dashboard" class="mt-6 inline-block px-8 py-3 bg-white/10 hover:bg-white/20 rounded-xl border border-white/10 transition-all">
          ไปเลือกสินค้ากัน ✨
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';

const cart = ref([]);

// ✅ โหลดข้อมูลจาก localStorage ทันทีที่เข้าหน้า
const loadCart = () => {
  if (process.client) {
    const savedCart = localStorage.getItem("cart");
    cart.value = savedCart ? JSON.parse(savedCart) : [];
  }
};

// ✅ เซฟลง localStorage ทุกครั้งที่ตะกร้าเปลี่ยน (เช่น กดเพิ่ม/ลด/ลบ)
watch(cart, (newCart) => {
  localStorage.setItem("cart", JSON.stringify(newCart));
}, { deep: true });

const totalPrice = computed(() => cart.value.reduce((sum, item) => sum + (item.price * item.quantity), 0));
const totalItems = computed(() => cart.value.reduce((sum, item) => sum + item.quantity, 0));

const updateQty = (item, change) => {
  const newQty = item.quantity + change;
  if (newQty >= 1) {
    item.quantity = newQty;
  }
};

const removeItem = (item) => {
  cart.value = cart.value.filter(i => i.id !== item.id);
};

const checkout = () => {
  alert("ฟีเจอร์นี้จะเปิดใช้งานเมื่อรถม้าฟักทองมารับนะเพคะ! 🎃");
};

onMounted(loadCart);
</script>

<style scoped>
.glass { background: rgba(18, 18, 18, 0.7); backdrop-filter: blur(20px); }
.animate-in { animation: slideUp 0.5s ease-out; }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>