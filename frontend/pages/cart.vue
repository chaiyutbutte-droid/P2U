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
          
          <div class="flex items-center gap-3 px-5 py-2 bg-white/5 rounded-2xl border border-white/5">
            <input 
              type="checkbox" 
              :checked="isAllSelected" 
              @change="toggleSelectAll"
              class="w-5 h-5 accent-pink-500 cursor-pointer rounded-lg"
            />
            <span class="text-sm font-medium text-dark-200">เลือกสินค้าทั้งหมด</span>
          </div>

          <div v-for="item in cart" :key="item.id" 
               class="glass p-5 rounded-3xl flex items-center gap-4 border border-white/5 hover:border-pink-500/30 transition-all duration-300 group"
               :class="{'border-pink-500/40 bg-pink-500/5': item.selected}">
            
            <input 
              type="checkbox" 
              v-model="item.selected" 
              class="w-5 h-5 accent-pink-500 cursor-pointer rounded-lg"
            />
            
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
              <button @click="removeItem(item)" class="text-xs text-red-400/60 hover:text-red-400 transition-colors">ลบสินค้า</button>
            </div>
          </div>
        </div>

        <div class="lg:col-span-1">
          <div class="glass p-8 rounded-[2rem] border border-pink-500/20 sticky top-28">
            <h2 class="text-xl font-bold mb-6">สรุปยอดชำระ ✨</h2>
            <div class="space-y-4 mb-8">
              <div class="flex justify-between text-dark-400">
                <span>เลือกแล้ว {{ selectedItemsCount }} ชิ้น</span>
                <span>฿{{ totalPrice.toLocaleString() }}</span>
              </div>
              <div class="h-px bg-white/10 my-2"></div>
              <div class="flex justify-between items-end">
                <span class="text-lg">ยอดสุทธิ</span>
                <span class="text-3xl font-black text-pink-500">฿{{ totalPrice.toLocaleString() }}</span>
              </div>
            </div>
            
            <button 
              @click="checkout" 
              :disabled="selectedItemsCount === 0"
              class="w-full py-4 bg-gradient-to-r from-pink-500 to-rose-600 rounded-2xl font-bold text-lg hover:scale-[1.02] active:scale-[0.98] transition-all shadow-lg shadow-pink-500/20 disabled:opacity-40 disabled:grayscale disabled:hover:scale-100"
            >
              {{ selectedItemsCount > 0 ? 'ชำระเงินตอนนี้ 💖' : 'กรุณาเลือกสินค้า' }}
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
import { useRouter } from 'vue-router'; // ✅ นำเข้า useRouter

const router = useRouter(); // ✅ ใช้งาน router
const cart = ref([]);

// ✅ โหลดข้อมูลและเพิ่มสถานะ selected
const loadCart = () => {
  if (process.client) {
    const savedCart = localStorage.getItem("cart");
    const parsed = savedCart ? JSON.parse(savedCart) : [];
    // เพิ่ม property selected: true ให้ทุกรายการที่โหลดขึ้นมา (ถ้ายังไม่มี)
    cart.value = parsed.map(item => ({
      ...item,
      selected: item.selected !== undefined ? item.selected : true
    }));
  }
};

watch(cart, (newCart) => {
  localStorage.setItem("cart", JSON.stringify(newCart));
}, { deep: true });

// ✅ คำนวณยอดรวมเฉพาะชิ้นที่ถูกติ๊กถูก
const totalPrice = computed(() => {
  return cart.value
    .filter(item => item.selected)
    .reduce((sum, item) => sum + (item.price * item.quantity), 0);
});

const totalItems = computed(() => cart.value.reduce((sum, item) => sum + item.quantity, 0));

const selectedItemsCount = computed(() => {
  return cart.value.filter(item => item.selected).length;
});

const isAllSelected = computed(() => {
  return cart.value.length > 0 && cart.value.every(item => item.selected);
});

// --- ฟังก์ชันจัดการ ---

const toggleSelectAll = (e) => {
  const isChecked = e.target.checked;
  cart.value.forEach(item => item.selected = isChecked);
};

const updateQty = (item, change) => {
  const newQty = item.quantity + change;
  if (newQty >= 1) {
    item.quantity = newQty;
  }
};

const removeItem = (item) => {
  cart.value = cart.value.filter(i => i.id !== item.id);
};

// ✅ แก้ไขฟังก์ชันชำระเงิน
const checkout = () => {
  const selectedItems = cart.value.filter(i => i.selected);
  
  if (selectedItems.length > 0) {
    // 1. เก็บสินค้าที่เลือกไว้ใน checkout_items เพื่อให้หน้า payment ดึงไปใช้
    localStorage.setItem("checkout_items", JSON.stringify(selectedItems));
    
    // 2. ไปที่หน้าชำระเงิน
    router.push("/payment");
  } else {
    alert("กรุณาเลือกสินค้าที่ต้องการชำระเงินก่อนนะเพคะ! 👑");
  }
};

onMounted(loadCart);
</script>

<style scoped>
.glass { background: rgba(18, 18, 18, 0.7); backdrop-filter: blur(20px); }
.animate-in { animation: slideUp 0.5s ease-out; }
@keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

input[type="checkbox"] {
  border-radius: 6px;
  background-color: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
</style>