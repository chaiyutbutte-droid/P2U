<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-pink-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-pink-500/10 blur-[120px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed top-0 right-0 w-[500px] h-[500px] bg-purple-500/10 blur-[100px] rounded-full pointer-events-none z-0"></div>

    <main class="ml-20 relative z-10 min-h-screen p-6 md:p-10 pt-8 pb-24">
      
      <div class="max-w-6xl w-full mx-auto animate-in-fade">
        
        <header class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8">
          <div>
            <h1 class="text-3xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-pink-200 to-purple-200 tracking-tight drop-shadow-sm">
              ตะกร้าของคุณ
            </h1>
            <p class="text-gray-400 mt-2 flex items-center gap-2">
              <span class="inline-block w-2 h-2 rounded-full bg-pink-500 animate-pulse"></span>
              มีสินค้า {{ totalItems }} รายการ พร้อมชำระเงิน
            </p>
          </div>
          
          <NuxtLink to="/dashboard" class="group flex items-center gap-2 text-sm font-medium text-gray-400 hover:text-white transition-colors px-4 py-2 rounded-full hover:bg-white/5">
            <span class="group-hover:-translate-x-1 transition-transform">←</span> เลือกซื้อสินค้าต่อ
          </NuxtLink>
        </header>

        <div v-if="cart.length > 0" class="bg-[#121215]/80 backdrop-blur-3xl rounded-[2.5rem] border border-white/10 shadow-2xl overflow-hidden">
          <div class="flex flex-col lg:flex-row">
            
            <div class="flex-1 p-6 md:p-8 relative">
              
              <div class="flex items-center justify-between pb-4 border-b border-white/5 mb-6">
                 <label class="inline-flex items-center cursor-pointer group">
                    <input type="checkbox" :checked="isAllSelected" @change="toggleSelectAll" class="peer sr-only" />
                    <div class="w-5 h-5 border-2 border-gray-600 rounded-[6px] peer-checked:bg-pink-500 peer-checked:border-pink-500 transition-all flex items-center justify-center group-hover:border-pink-400">
                      <svg class="w-3 h-3 text-white opacity-0 peer-checked:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg>
                    </div>
                    <span class="ml-3 text-sm font-medium text-gray-300 group-hover:text-white transition-colors">เลือกทั้งหมด ({{ cart.length }})</span>
                 </label>
                 <button v-if="selectedItemsCount > 0" @click="removeSelected" class="text-xs text-red-400 hover:text-red-300 transition-colors py-1 px-3 hover:bg-red-500/10 rounded-full">ลบที่เลือก</button>
              </div>

              <div class="space-y-2">
                <TransitionGroup name="list">
                  <div 
                    v-for="item in cart" 
                    :key="item.id" 
                    class="group relative p-4 rounded-2xl border border-transparent hover:border-white/5 hover:bg-white/5 transition-all duration-300 flex gap-4 sm:gap-6"
                    :class="{'bg-white/[0.02]': !item.selected}"
                  >
                     <div class="flex items-center gap-4 shrink-0">
                        <label class="relative flex items-center cursor-pointer">
                          <input type="checkbox" v-model="item.selected" class="peer sr-only" />
                          <div class="w-5 h-5 border-2 border-gray-600 rounded-[6px] peer-checked:bg-gradient-to-r peer-checked:from-pink-500 peer-checked:to-purple-500 peer-checked:border-transparent transition-all flex items-center justify-center">
                            <svg class="w-3 h-3 text-white opacity-0 peer-checked:opacity-100" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" /></svg>
                          </div>
                        </label>
                        
                        <div class="w-20 h-20 md:w-28 md:h-28 rounded-xl bg-[#09090b] overflow-hidden border border-white/5 relative shadow-sm group-hover:shadow-md transition-all">
                           <img :src="item.image_url" class="w-full h-full object-cover" />
                        </div>
                     </div>

                     <div class="flex-1 min-w-0 flex flex-col justify-between py-1">
                        <div>
                          <div class="flex justify-between items-start">
                             <h3 class="text-base md:text-lg font-bold text-white truncate pr-4">{{ item.name }}</h3>
                             <button @click="removeItem(item)" class="text-gray-500 hover:text-red-400 transition-colors p-1 hover:bg-red-500/10 rounded-lg">✕</button>
                          </div>
                          <p class="text-xs text-gray-500 mt-1 flex items-center gap-1">
                            <span class="opacity-50">🏪</span> {{ item.seller?.shop_name || 'ร้านค้าทั่วไป' }}
                          </p>
                        </div>

                        <div class="flex items-end justify-between mt-2">
                           <p class="text-lg md:text-2xl font-bold text-white">
                              ฿{{ item.price?.toLocaleString() }}
                           </p>
                           
                           <div class="flex items-center bg-[#09090b]/50 rounded-lg border border-white/10 p-1">
                             <button @click="updateQty(item, -1)" class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-white hover:bg-white/10 rounded-md transition-colors" :class="{'opacity-30 cursor-not-allowed': item.quantity <= 1}">-</button>
                             <span class="w-8 text-center text-sm font-bold text-white">{{ item.quantity }}</span>
                             <button @click="updateQty(item, 1)" class="w-8 h-8 flex items-center justify-center text-gray-400 hover:text-white hover:bg-white/10 rounded-md transition-colors">+</button>
                          </div>
                        </div>
                     </div>
                  </div>
                </TransitionGroup>
              </div>
            </div>

            <div class="lg:w-[400px] bg-white/[0.02] border-t lg:border-t-0 lg:border-l border-white/5 relative">
               <div class="sticky top-0 p-6 md:p-10 h-full flex flex-col">
                 
                 <div class="absolute top-0 right-0 w-full h-64 bg-gradient-to-b from-pink-500/5 to-transparent pointer-events-none"></div>

                 <h2 class="text-xl font-bold text-white mb-6 relative">สรุปยอดชำระ</h2>

                 <div class="space-y-4 mb-8 relative flex-1">
                    <div class="flex justify-between text-gray-400 text-sm">
                       <span>ยอดรวม ({{ selectedItemsCount }} ชิ้น)</span>
                       <span class="text-white font-medium">฿{{ totalPrice.toLocaleString() }}</span>
                    </div>
                    <div class="flex justify-between text-gray-400 text-sm">
                       <span>ค่าจัดส่ง</span>
                       <span class="text-green-400">ฟรี</span>
                    </div>
                    
                    <div class="h-px bg-gradient-to-r from-white/5 via-white/20 to-white/5 my-6"></div>
                    
                    <div class="flex justify-between items-end">
                       <span class="text-gray-300 font-medium">ยอดสุทธิ</span>
                       <div class="text-right">
                          <span class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-300 tracking-tight">
                            ฿{{ totalPrice.toLocaleString() }}
                          </span>
                          <p class="text-[10px] text-gray-500 mt-1">รวมภาษีมูลค่าเพิ่มแล้ว</p>
                       </div>
                    </div>
                 </div>

                 <button 
                    @click="checkout" 
                    :disabled="selectedItemsCount === 0"
                    class="w-full relative group overflow-hidden rounded-2xl disabled:opacity-50 disabled:cursor-not-allowed shadow-xl shadow-pink-500/10 mt-auto"
                 >
                    <div class="absolute inset-0 bg-gradient-to-r from-pink-600 via-purple-600 to-pink-600 bg-[length:200%_auto] animate-shimmer transition-all duration-300 group-hover:brightness-110"></div>
                    <div class="relative py-4 flex items-center justify-center gap-3 text-white font-bold text-lg">
                       <span>ชำระเงิน</span>
                       <svg v-if="selectedItemsCount > 0" class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3" /></svg>
                    </div>
                 </button>
               </div>
            </div>

          </div>
        </div>

        <div v-else class="mt-10 flex flex-col items-center justify-center text-center bg-[#121215]/40 backdrop-blur-3xl rounded-[2.5rem] border border-white/10 p-16 animate-in-fade">
           <div class="w-40 h-40 mb-8 rounded-full bg-gradient-to-tr from-[#121215] to-[#1a1a1f] border border-white/5 flex items-center justify-center shadow-2xl relative group">
              <div class="absolute inset-0 bg-pink-500/20 rounded-full blur-2xl animate-pulse group-hover:bg-pink-500/30 transition-all"></div>
              <span class="text-7xl relative z-10 grayscale group-hover:grayscale-0 transition-all duration-500">🛒</span>
           </div>
           <h2 class="text-3xl font-bold text-white mb-3">ตะกร้าของคุณว่างเปล่า</h2>
           <p class="text-gray-500 mb-8 max-w-md mx-auto leading-relaxed">
             ยังไม่มีสินค้าในตะกร้า ลองออกไปสำรวจสินค้าสุดพิเศษที่เราคัดสรรมาเพื่อคุณโดยเฉพาะ
           </p>
           <NuxtLink to="/dashboard" class="px-10 py-4 bg-white text-black font-bold rounded-2xl hover:bg-gray-100 hover:scale-105 transition-all shadow-lg shadow-white/10 flex items-center gap-2">
              ไปช้อปปิ้งกันเถอะ <span class="text-xl">🛍️</span>
           </NuxtLink>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
// ================= Logic เดิม 100% =================
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const cart = ref([]);

const getCartKey = () => {
  if (process.client) {
    const user = localStorage.getItem('user');
    if (user) {
      const userData = JSON.parse(user);
      const id = userData.id || userData._id || userData.email;
      return `cart_${id}`;
    }
  }
  return 'cart_guest';
};

const loadCart = () => {
  if (process.client) {
    const cartKey = getCartKey();
    const savedCart = localStorage.getItem(cartKey);
    const parsed = savedCart ? JSON.parse(savedCart) : [];
    
    cart.value = parsed.map(item => ({
      ...item,
      selected: item.selected !== undefined ? item.selected : true
    }));
  }
};

watch(cart, (newCart) => {
  if (process.client) {
    const cartKey = getCartKey();
    localStorage.setItem(cartKey, JSON.stringify(newCart));
  }
}, { deep: true });

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

const removeSelected = () => {
  cart.value = cart.value.filter(i => !i.selected);
};

const checkout = () => {
  const selectedItems = cart.value.filter(i => i.selected);
  if (selectedItems.length > 0) {
    localStorage.setItem("checkout_items", JSON.stringify(selectedItems));
    router.push("/payment");
  } else {
    alert("กรุณาเลือกสินค้าที่ต้องการชำระเงินก่อนนะเพคะ! 👑");
  }
};

onMounted(loadCart);
</script>

<style scoped>
/* Animation สำหรับการแสดงผล */
.animate-in-fade {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

/* Shimmer Animation for Button */
@keyframes shimmer {
  0% { background-position: 0% 50%; }
  100% { background-position: 200% 50%; }
}
.animate-shimmer {
  animation: shimmer 3s linear infinite;
}

/* List Transition */
.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-20px);
  height: 0;
  margin: 0;
  padding: 0;
  overflow: hidden;
}
</style>