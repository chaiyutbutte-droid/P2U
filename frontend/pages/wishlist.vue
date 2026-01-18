<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-pink-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-pink-500/10 blur-[150px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[600px] h-[600px] bg-purple-900/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

    <main class="ml-20 relative z-10 p-6 md:p-10 min-h-screen">
      <div class="max-w-6xl mx-auto w-full animate-in-fade">

        <header class="flex flex-col md:flex-row items-start md:items-end justify-between gap-4 mb-10">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-pink-500/10 border border-pink-500/20 mb-3">
              <span class="w-1.5 h-1.5 rounded-full bg-pink-500 animate-pulse"></span>
              <span class="text-[10px] font-bold text-pink-300 uppercase tracking-widest">My Collection</span>
            </div>
            <h1 class="text-4xl md:text-5xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-pink-100 to-rose-400 tracking-tight drop-shadow-sm">
              รายการโปรด 💖
            </h1>
            <p class="text-gray-400 mt-2 text-sm md:text-base">
              รวมสินค้าที่คุณหมายตาเอาไว้ รอให้คุณเป็นเจ้าของ
            </p>
          </div>
          
          <div class="px-5 py-2.5 rounded-2xl bg-white/5 border border-white/10 flex items-center gap-3 backdrop-blur-md">
            <span class="text-sm text-gray-400">จำนวนรายการ</span>
            <span class="text-xl font-bold text-white">{{ wishlist.length }}</span>
            <span class="text-sm text-gray-400">ชิ้น</span>
          </div>
        </header>

        <div v-if="wishlist.length" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 md:gap-6">
          <TransitionGroup name="list">
            <div 
              v-for="product in wishlist" 
              :key="product.id" 
              class="group relative bg-[#121215]/60 backdrop-blur-md rounded-[2rem] border border-white/5 overflow-hidden transition-all duration-500 hover:border-pink-500/40 hover:shadow-[0_10px_40px_-10px_rgba(236,72,153,0.3)] hover:-translate-y-2 cursor-pointer"
              @click="openProduct(product)"
            >
              <div class="aspect-square relative overflow-hidden">
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent z-10 opacity-60 group-hover:opacity-40 transition-opacity"></div>
                
                <img 
                  :src="product.image_url" 
                  class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                  @error="product.image_url = defaultImage"
                />

                <button 
                  @click.stop="removeFromWishlist(product)"
                  class="absolute top-3 right-3 z-20 w-9 h-9 rounded-full bg-black/40 backdrop-blur-md border border-white/10 flex items-center justify-center text-red-500 transition-all duration-300 hover:bg-red-500 hover:text-white hover:scale-110 hover:border-red-400 group/btn"
                  title="ลบจากรายการโปรด"
                >
                  <span class="text-lg group-active/btn:scale-75 transition-transform">💔</span>
                </button>

                <div class="absolute bottom-0 left-0 w-full p-4 z-20 translate-y-full group-hover:translate-y-0 transition-transform duration-300">
                  <button 
                    @click.stop="addToCart(product)"
                    class="w-full py-2.5 rounded-xl bg-white/90 text-black font-bold text-sm hover:bg-white shadow-lg transition-colors flex items-center justify-center gap-2"
                  >
                    🛒 ใส่ตะกร้าทันที
                  </button>
                </div>
              </div>

              <div class="p-5 relative z-10 bg-gradient-to-b from-transparent to-[#0f0f12]">
                <div class="flex items-start justify-between gap-2 mb-1">
                  <h3 class="text-base font-bold text-white truncate group-hover:text-pink-200 transition-colors">{{ product.name }}</h3>
                </div>
                
                <p class="text-xs text-gray-500 truncate mb-3 flex items-center gap-1">
                  <span>🏪</span> {{ product.seller?.shop_name || product.seller?.username || 'ร้านค้าทั่วไป' }}
                </p>

                <div class="flex items-center justify-between">
                  <div class="flex flex-col">
                    <span class="text-[10px] text-gray-500 uppercase font-bold tracking-wider">ราคา</span>
                    <span class="text-lg font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-200 to-yellow-500">
                      ฿{{ product.price?.toLocaleString() }}
                    </span>
                  </div>
                  <div class="w-8 h-8 rounded-lg bg-white/5 flex items-center justify-center text-gray-400 border border-white/5 group-hover:border-pink-500/30 group-hover:text-pink-400 transition-colors">
                    ➔
                  </div>
                </div>
              </div>
            </div>
          </TransitionGroup>
        </div>

        <div v-else class="min-h-[50vh] flex flex-col items-center justify-center text-center animate-in-fade bg-[#121215]/30 rounded-[3rem] border border-white/5 border-dashed relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-b from-pink-500/5 to-transparent pointer-events-none"></div>
          
          <div class="w-24 h-24 rounded-full bg-gradient-to-tr from-gray-800 to-black border border-white/10 flex items-center justify-center text-5xl shadow-2xl mb-6 relative">
            <span class="grayscale opacity-50">💔</span>
            <div class="absolute inset-0 border-2 border-white/5 rounded-full animate-ping opacity-20"></div>
          </div>
          
          <h3 class="text-2xl font-bold text-white mb-2">ยังไม่มีสินค้าที่ถูกใจ</h3>
          <p class="text-gray-500 mb-8 max-w-xs mx-auto">ลองไปเลือกดูสินค้าสวยๆ แล้วกดหัวใจเก็บไว้ดูภายหลังสิคะ</p>
          
          <NuxtLink 
            to="/dashboard" 
            class="px-8 py-3.5 bg-gradient-to-r from-pink-500 to-rose-600 rounded-2xl font-bold text-white shadow-lg shadow-pink-500/20 hover:scale-105 active:scale-95 transition-all flex items-center gap-2"
          >
            <span>🛍️</span> ไปช้อปปิ้งเลย
          </NuxtLink>
        </div>

        <Teleport to="body">
          <Transition name="zoom">
            <div v-if="selectedProduct" class="fixed inset-0 z-[100] flex items-center justify-center p-4" @click="closeProduct">
              <div class="absolute inset-0 bg-black/90 backdrop-blur-xl transition-opacity"></div>
              
              <div class="relative w-full max-w-5xl h-[85vh] md:h-auto bg-[#18181b] rounded-[3rem] border border-white/10 shadow-2xl flex flex-col md:flex-row overflow-hidden animate-modal-slide" @click.stop>
                
                <button @click="closeProduct" class="absolute top-4 right-4 z-50 w-10 h-10 rounded-full bg-black/50 backdrop-blur text-white md:hidden flex items-center justify-center">✕</button>

                <div class="w-full md:w-1/2 h-64 md:h-auto relative bg-[#0f0f12]">
                   <img 
                    :src="selectedProduct.image_url || defaultImage" 
                    class="w-full h-full object-cover"
                   />
                   <div class="absolute inset-0 bg-gradient-to-t from-[#18181b] to-transparent md:bg-gradient-to-r md:from-transparent md:to-[#18181b]/80"></div>
                </div>
                
                <div class="w-full md:w-1/2 p-8 md:p-10 flex flex-col overflow-y-auto custom-scrollbar relative">
                   <button @click="closeProduct" class="hidden md:flex absolute top-6 right-6 w-10 h-10 rounded-full bg-white/5 hover:bg-white/10 text-gray-400 hover:text-white items-center justify-center transition-colors">✕</button>

                   <div class="mb-auto">
                      <div class="flex items-center gap-2 mb-4">
                        <span class="px-3 py-1 rounded-full bg-pink-500/10 text-pink-400 text-xs font-bold border border-pink-500/20 uppercase tracking-wider">
                          {{ selectedProduct.category || 'General' }}
                        </span>
                        <div class="flex items-center text-yellow-400 text-sm gap-1">
                          <span>⭐</span>
                          <span class="font-medium">4.9</span>
                          <span class="text-gray-500 text-xs">(128 reviews)</span>
                        </div>
                      </div>

                      <h2 class="text-3xl md:text-4xl font-black text-white mb-4 leading-tight">
                        {{ selectedProduct.name }}
                      </h2>
                      
                      <div class="h-px w-20 bg-gradient-to-r from-pink-500 to-transparent mb-6"></div>

                      <p class="text-gray-400 leading-relaxed mb-6 font-light text-sm md:text-base">
                        {{ selectedProduct.description || 'ไม่มีคำอธิบายสินค้า... สินค้าชิ้นนี้ได้รับการคัดสรรมาอย่างดีเพื่อเจ้าหญิงโดยเฉพาะ' }}
                      </p>

                      <div class="flex items-center gap-3 p-4 rounded-2xl bg-white/5 border border-white/5 mb-8">
                         <div class="w-10 h-10 rounded-full bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center text-lg">🏪</div>
                         <div>
                            <p class="text-xs text-gray-500 uppercase font-bold">Sold by</p>
                            <p class="text-white font-medium">{{ selectedProduct.seller?.shop_name || selectedProduct.seller?.username || 'Official Store' }}</p>
                         </div>
                      </div>
                   </div>
                   
                   <div class="mt-6 pt-6 border-t border-white/10">
                      <div class="flex items-end justify-between mb-6">
                        <span class="text-gray-400 text-sm">Price Total</span>
                        <span class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-yellow-200 to-yellow-500">
                          ฿{{ selectedProduct.price?.toLocaleString() }}
                        </span>
                      </div>

                      <div class="flex gap-4">
                        <button 
                          @click="addToCart(selectedProduct)" 
                          class="flex-1 py-4 rounded-2xl bg-white/5 text-white font-bold hover:bg-white hover:text-black border border-white/10 transition-all duration-300"
                        >
                          🛒 เพิ่มลงตะกร้า
                        </button>
                        <NuxtLink 
                          to="/payment" 
                          @click.native="addToCart(selectedProduct)"
                          class="flex-[1.5] py-4 rounded-2xl bg-gradient-to-r from-pink-500 to-rose-600 text-white font-bold text-center hover:scale-[1.02] shadow-lg shadow-pink-500/25 transition-all duration-300 flex items-center justify-center gap-2"
                        >
                          💳 ซื้อเลย
                        </NuxtLink>
                      </div>
                   </div>

                </div>
              </div>
            </div>
          </Transition>
        </Teleport>

      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import axios from 'axios';

const wishlist = ref([]);
const selectedProduct = ref(null);
const defaultImage = 'https://via.placeholder.com/400x400?text=No+Image'; // ใช้ Placeholder สวยๆ แทน SVG ก็ได้ครับ
const baseUrl = 'http://localhost:5000';

const cart = ref([]);
if (process.client) {
  cart.value = JSON.parse(localStorage.getItem("cart") || "[]");
  watch(cart, (newVal) => {
    localStorage.setItem("cart", JSON.stringify(newVal));
  }, { deep: true });
}

// ✅ Fetch Wishlist
const fetchWishlist = async () => {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    const res = await axios.get(`${baseUrl}/api/wishlist`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    const data = res.data.wishlist || [];
    wishlist.value = data.map(p => ({
      ...p,
      id: p.id || p._id,
      description: p.description || '', 
      price: parseFloat(p.price) || 0,
      image_url: p.image_url 
        ? (p.image_url.startsWith('http') ? p.image_url : `${baseUrl}${p.image_url}`) 
        : defaultImage,
      seller: p.seller || { username: "Unknown", shop_name: "ร้านค้าทั่วไป" }
    }));
  } catch (err) {
    console.error('Failed to fetch wishlist:', err);
  }
};

// ✅ Remove Logic
const removeFromWishlist = async (product) => {
  // Confirm ก่อนลบเพื่อ UX ที่ดี หรือจะลบเลยก็ได้
  if(!confirm(`ต้องการลบ ${product.name} ออกจากรายการโปรดใช่ไหมคะ?`)) return;

  const token = localStorage.getItem('token');
  try {
    await axios.delete(`${baseUrl}/api/wishlist/${product.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    wishlist.value = wishlist.value.filter(p => p.id !== product.id);
    if (selectedProduct.value?.id === product.id) closeProduct();
  } catch (err) {
    console.error('Error removing:', err);
    alert('ลบไม่สำเร็จ กรุณาลองใหม่ค่ะ');
  }
};

const openProduct = (product) => { selectedProduct.value = product; };
const closeProduct = () => { selectedProduct.value = null; };

const addToCart = (product) => {
  const existing = cart.value.find((item) => item.id === product.id);
  if (existing) existing.quantity++;
  else cart.value.push({ ...product, quantity: 1 });
  
  // Custom Toast แทน Alert ปกติได้จะสวยมาก แต่ใช้ alert ไปก่อนตาม logic เดิม
  alert(`✨ เพิ่ม ${product.name} ลงตะกร้าเรียบร้อยแล้วค่ะ!`);
};

onMounted(fetchWishlist);
</script>

<style scoped>
/* Animations */
.animate-in-fade {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

/* List Transitions */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* Modal Zoom Transition */
.zoom-enter-active {
  animation: zoomIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.zoom-leave-active {
  animation: zoomIn 0.2s reverse ease-in;
}
@keyframes zoomIn {
  0% { opacity: 0; transform: scale(0.95); }
  100% { opacity: 1; transform: scale(1); }
}

/* Scrollbar */
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
</style>