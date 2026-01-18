<template>
  <div class="min-h-screen bg-[#0b0b0f] text-white font-sans selection:bg-pink-500/30 overflow-hidden relative">
    
    <div class="fixed top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div class="absolute top-[20%] right-[10%] w-96 h-96 bg-purple-600/20 rounded-full blur-[120px] mix-blend-screen animate-pulse-slow"></div>
        <div class="absolute bottom-[10%] left-[20%] w-80 h-80 bg-pink-600/20 rounded-full blur-[100px] mix-blend-screen"></div>
    </div>

    <sidebar />

    <div class="ml-20 flex justify-center items-center min-h-screen p-6 relative z-10">
      
      <div class="w-full max-w-2xl transform transition-all">
        
        <div class="mb-8 flex items-end justify-between">
          <div>
            <h1 class="text-3xl font-bold text-white flex items-center gap-3">
              <span class="bg-gradient-to-r from-yellow-400 to-orange-500 w-2 h-8 rounded-full"></span>
              แก้ไขสินค้า
            </h1>
            <p class="text-gray-400 text-sm mt-2 ml-5">อัปเดตข้อมูลสินค้า รหัส: <span class="font-mono text-pink-400">#{{ productId }}</span></p>
          </div>
          <NuxtLink to="/seller-dashboard" class="group flex items-center gap-2 text-gray-500 hover:text-white transition-colors px-4 py-2 rounded-full hover:bg-white/5">
            <span class="text-xs font-medium">กลับ</span>
            <div class="w-6 h-6 rounded-full border border-gray-600 group-hover:border-white flex items-center justify-center transition-all">
               ←
            </div>
          </NuxtLink>
        </div>

        <div class="bg-black/40 backdrop-blur-xl border border-white/10 p-8 rounded-3xl shadow-2xl relative overflow-hidden min-h-[400px]">
          
          <div v-if="loading" class="absolute inset-0 flex flex-col items-center justify-center z-20 bg-black/60 backdrop-blur-sm">
            <div class="w-12 h-12 border-4 border-pink-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <p class="text-gray-300 animate-pulse">กำลังดึงข้อมูลสินค้า...</p>
          </div>

          <form v-else @submit.prevent="submitProduct" class="space-y-8 animate-fade-in-up">
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2 col-span-2 md:col-span-1">
                <label class="text-xs font-bold text-gray-400 uppercase tracking-wider ml-1">ชื่อสินค้า</label>
                <div class="relative group">
                  <input v-model="product.name" type="text" required class="w-full pl-4 pr-4 py-3.5 rounded-2xl bg-white/5 border border-white/10 focus:border-pink-500/50 focus:bg-white/10 text-white placeholder-gray-600 transition-all outline-none focus:ring-4 focus:ring-pink-500/10" placeholder="ชื่อสินค้า" />
                </div>
              </div>

              <div class="space-y-2 col-span-2 md:col-span-1">
                <label class="text-xs font-bold text-gray-400 uppercase tracking-wider ml-1">ราคา</label>
                <div class="relative group">
                  <span class="absolute left-4 top-3.5 text-gray-500 group-focus-within:text-green-400 transition-colors">฿</span>
                  <input v-model="product.price" type="number" required min="0" class="w-full pl-10 pr-4 py-3.5 rounded-2xl bg-white/5 border border-white/10 focus:border-green-500/50 focus:bg-white/10 text-white placeholder-gray-600 transition-all outline-none focus:ring-4 focus:ring-green-500/10 font-mono" placeholder="0.00" />
                </div>
              </div>
            </div>

            <div class="space-y-3">
              <label class="text-xs font-bold text-gray-400 uppercase tracking-wider ml-1">หมวดหมู่</label>
              <div class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3 max-h-48 overflow-y-auto pr-2 custom-scrollbar">
                <button
                  v-for="cat in categories"
                  :key="cat.id"
                  type="button"
                  @click="product.category = cat.id"
                  class="group relative p-3 rounded-2xl border transition-all duration-300 flex flex-col items-center justify-center gap-2 overflow-hidden"
                  :class="product.category === cat.id 
                    ? 'border-pink-500 bg-pink-500/20 text-white shadow-[0_0_15px_rgba(236,72,153,0.3)]' 
                    : 'border-white/5 bg-white/5 text-gray-400 hover:bg-white/10 hover:border-white/20 hover:text-gray-200'"
                >
                  <span class="text-2xl transform group-hover:scale-110 transition-transform">{{ cat.icon }}</span>
                  <span class="text-[10px] font-medium">{{ cat.name }}</span>
                </button>
              </div>
            </div>

            <div class="space-y-2">
              <label class="text-xs font-bold text-gray-400 uppercase tracking-wider ml-1">รายละเอียด</label>
              <textarea v-model="product.description" rows="3" class="w-full p-4 rounded-2xl bg-white/5 border border-white/10 focus:border-purple-500/50 focus:bg-white/10 text-white placeholder-gray-600 transition-all outline-none resize-none focus:ring-4 focus:ring-purple-500/10" placeholder="รายละเอียดสินค้า..."></textarea>
            </div>

            <div class="space-y-4">
              <label class="text-xs font-bold text-gray-400 uppercase tracking-wider ml-1">รูปภาพสินค้า</label>
              
              <div class="flex flex-col md:flex-row gap-6">
                <div class="relative w-full border-2 border-dashed rounded-3xl p-1 transition-all group overflow-hidden cursor-pointer hover:border-pink-500/50 hover:bg-pink-500/5 border-white/10 bg-white/5"
                     @click="$refs.fileInput.click()">
                  
                  <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" class="hidden" />
                  
                  <div class="flex flex-col items-center justify-center py-6">
                    <div v-if="imagePreview" class="relative w-full px-6">
                      <img :src="imagePreview" class="h-40 w-full object-contain rounded-xl shadow-lg" />
                      <div class="absolute top-0 right-8 bg-green-500 text-white text-[10px] font-bold px-2 py-1 rounded-full shadow-lg">New ✨</div>
                      <p class="text-center text-xs text-green-400 mt-3">พร้อมอัปโหลดรูปใหม่</p>
                    </div>

                    <div v-else-if="product.image_url" class="relative w-full px-6">
                      <img :src="getImageUrl(product.image_url)" class="h-40 w-full object-contain rounded-xl opacity-80 group-hover:opacity-100 transition-opacity" />
                      <div class="absolute top-0 right-8 bg-gray-700 text-gray-300 text-[10px] font-bold px-2 py-1 rounded-full border border-gray-600">Current</div>
                      <p class="text-center text-xs text-gray-400 mt-3 group-hover:text-pink-400 transition-colors">คลิกเพื่อเปลี่ยนรูปภาพ</p>
                    </div>

                    <div v-else class="text-center py-4">
                        <span class="text-4xl block mb-2 opacity-50">📷</span>
                        <p class="text-sm text-gray-400">ยังไม่มีรูปภาพ</p>
                        <p class="text-xs text-pink-400 mt-1">คลิกเพื่อเพิ่ม</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="pt-6 border-t border-white/10 flex flex-col-reverse sm:flex-row items-center gap-4">
               
               <button 
                type="button"
                @click="confirmDelete"
                :disabled="isDeleting"
                class="w-full sm:w-auto px-6 py-3.5 rounded-2xl border border-red-500/30 text-red-400 hover:bg-red-500 hover:text-white hover:shadow-[0_0_20px_rgba(239,68,68,0.4)] transition-all duration-300 flex items-center justify-center gap-2 group"
               >
                 <span v-if="isDeleting" class="animate-spin">⏳</span>
                 <span v-else class="text-xl group-hover:rotate-12 transition-transform">🗑️</span>
                 <span class="font-medium">ลบสินค้า</span>
               </button>

               <button 
                type="submit" 
                :disabled="isSubmitting"
                class="w-full flex-1 py-3.5 bg-gradient-to-r from-pink-600 via-purple-600 to-indigo-600 hover:from-pink-500 hover:via-purple-500 hover:to-indigo-500 rounded-2xl font-bold text-white transition-all duration-300 shadow-[0_0_20px_rgba(236,72,153,0.3)] hover:shadow-[0_0_30px_rgba(236,72,153,0.5)] transform hover:-translate-y-0.5 disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <span v-if="isSubmitting" class="animate-spin text-xl">⏳</span>
                <span v-else class="text-lg">บันทึกการเปลี่ยนแปลง 💾</span>
              </button>
            </div>

          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const baseURL = "http://localhost:5000";

const productId = route.params.id;
const product = ref({
  name: "",
  price: "",
  description: "",
  category: "electronics",
  image_url: ""
});
const imageFile = ref(null);
const imagePreview = ref(null);
const isSubmitting = ref(false);
const isDeleting = ref(false);
const loading = ref(true);

const categories = ref([
  { id: "electronics", name: "อิเล็กทรอนิกส์", icon: "📱" },
  { id: "fashion", name: "แฟชั่น", icon: "👗" },
  { id: "gaming", name: "เกมมิ่ง", icon: "🎮" },
  { id: "beauty", name: "ความงาม", icon: "💄" },
  { id: "home", name: "บ้าน", icon: "🏠" },
  { id: "sports", name: "กีฬา", icon: "⚽" },
  { id: "food", name: "อาหาร", icon: "🍔" },
  { id: "books", name: "หนังสือ", icon: "📚" },
  { id: "toys", name: "ของเล่น", icon: "🧸" },
  { id: "pets", name: "สัตว์เลี้ยง", icon: "🐶" },
  { id: "automotive", name: "ยานยนต์", icon: "🚗" },
]);

const getImageUrl = (url) => {
  if (!url) return 'https://via.placeholder.com/300?text=No+Image'; // Placeholder สวยๆ
  if (url.startsWith('http')) return url;
  return `${baseURL}${url.startsWith('/') ? '' : '/'}${url}`;
};

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    imagePreview.value = URL.createObjectURL(file);
  }
};

const fetchProduct = async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    router.push("/login");
    return;
  }

  try {
    const res = await axios.get(`${baseURL}/api/seller/products/${productId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    product.value = res.data;
  } catch (err) {
    console.error("Failed to fetch product:", err);
    alert("ไม่พบสินค้าหรือไม่มีสิทธิ์เข้าถึง");
    router.push("/seller-dashboard");
  } finally {
    loading.value = false;
  }
};

const fetchCategories = async () => {
  try {
    const res = await axios.get(`${baseURL}/api/categories`);
    if (res.data && res.data.length > 0) {
       categories.value = res.data.filter(cat => cat.id !== 'all');
    }
  } catch (err) {
    console.log("Using default categories");
  }
};

const submitProduct = async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    router.push("/login");
    return;
  }

  isSubmitting.value = true;

  try {
    // Update product info
    await axios.put(`${baseURL}/api/seller/products/${productId}`, {
      name: product.value.name,
      price: product.value.price,
      description: product.value.description,
      category: product.value.category
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });

    // Upload new image if selected
    if (imageFile.value) {
      const formData = new FormData();
      formData.append("image", imageFile.value);
      
      await axios.put(`${baseURL}/api/seller/products/${productId}/image`, formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "multipart/form-data"
        }
      });
    }

    // Success styling could be better with toast, but for now:
    alert("อัปเดตสินค้าสำเร็จ! ✨");
    router.push("/seller-dashboard");
  } catch (err) {
    console.error("Failed to update product:", err);
    alert("ไม่สามารถอัพเดตสินค้าได้ กรุณาลองใหม่อีกครั้ง");
  } finally {
    isSubmitting.value = false;
  }
};

const confirmDelete = async () => {
  if (!confirm("❗ คำเตือน: คุณต้องการลบสินค้านี้ใช่หรือไม่?")) {
    return;
  }

  const token = localStorage.getItem("token");
  isDeleting.value = true;

  try {
    await axios.delete(`${baseURL}/api/seller/products/${productId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert("ลบสินค้าสำเร็จ!");
    router.push("/seller-dashboard");
  } catch (err) {
    console.error("Failed to delete product:", err);
    alert("ไม่สามารถลบสินค้าได้");
  } finally {
    isDeleting.value = false;
  }
};

onMounted(() => {
  fetchProduct();
  fetchCategories();
});
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse-slow {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}
.animate-pulse-slow {
  animation: pulse-slow 8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>