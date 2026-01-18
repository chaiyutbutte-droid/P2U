<template>
  <div class="min-h-screen bg-[#0b0b0f] text-white font-sans selection:bg-pink-500/30 overflow-hidden relative">
    
    <div class="fixed top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
        <div class="absolute top-[10%] right-[20%] w-96 h-96 bg-pink-600/20 rounded-full blur-[120px] mix-blend-screen animate-pulse-slow"></div>
        <div class="absolute bottom-[10%] left-[10%] w-80 h-80 bg-purple-600/20 rounded-full blur-[100px] mix-blend-screen"></div>
    </div>

    <sidebar />

    <div class="ml-20 flex justify-center items-center min-h-screen p-6 relative z-10">
      
      <div class="w-full max-w-2xl transform transition-all">
        
        <div class="mb-8 flex items-end justify-between">
          <div>
            <h1 class="text-3xl font-bold text-white flex items-center gap-3">
              <span class="bg-gradient-to-r from-pink-500 to-purple-500 w-2 h-8 rounded-full"></span>
              เพิ่มสินค้าใหม่
            </h1>
            <p class="text-gray-400 text-sm mt-2 ml-5">กรอกข้อมูลสินค้าของคุณให้ครบถ้วนเพื่อลงขาย</p>
          </div>
          <NuxtLink to="/seller-dashboard" class="group flex items-center gap-2 text-gray-500 hover:text-white transition-colors px-4 py-2 rounded-full hover:bg-white/5">
            <span class="text-xs font-medium">ยกเลิก</span>
            <div class="w-6 h-6 rounded-full border border-gray-600 group-hover:border-white flex items-center justify-center transition-all">
               ✕
            </div>
          </NuxtLink>
        </div>

        <div class="bg-black/40 backdrop-blur-xl border border-white/10 p-8 rounded-3xl shadow-2xl relative overflow-hidden">
          
          <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-pink-500/50 via-purple-500/50 to-transparent opacity-50"></div>

          <form @submit.prevent="submitProduct" class="space-y-8">
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-2 col-span-2 md:col-span-1">
                <label class="text-xs font-bold text-gray-400 uppercase tracking-wider ml-1">ชื่อสินค้า</label>
                <div class="relative group">
                  <input 
                    v-model="name" 
                    type="text" 
                    required 
                    class="w-full pl-4 pr-4 py-3.5 rounded-2xl bg-white/5 border border-white/10 focus:border-pink-500/50 focus:bg-white/10 text-white placeholder-gray-600 transition-all outline-none focus:ring-4 focus:ring-pink-500/10" 
                    placeholder="เช่น หูฟังไร้สาย Gen 2" 
                  />
                  <div class="absolute right-3 top-3.5 text-gray-500 group-focus-within:text-pink-400 transition-colors">✨</div>
                </div>
              </div>

              <div class="space-y-2 col-span-2 md:col-span-1">
                <label class="text-xs font-bold text-gray-400 uppercase tracking-wider ml-1">ราคา</label>
                <div class="relative group">
                  <span class="absolute left-4 top-3.5 text-gray-500 font-sans group-focus-within:text-green-400 transition-colors">฿</span>
                  <input 
                    v-model="price" 
                    type="number" 
                    required 
                    min="0" 
                    class="w-full pl-10 pr-4 py-3.5 rounded-2xl bg-white/5 border border-white/10 focus:border-green-500/50 focus:bg-white/10 text-white placeholder-gray-600 transition-all outline-none focus:ring-4 focus:ring-green-500/10 font-mono" 
                    placeholder="0.00" 
                  />
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
                  @click="selectedCategory = cat.id"
                  class="group relative p-3 rounded-2xl border transition-all duration-300 flex flex-col items-center justify-center gap-2 overflow-hidden"
                  :class="selectedCategory === cat.id 
                    ? 'border-pink-500 bg-pink-500/20 text-white shadow-[0_0_15px_rgba(236,72,153,0.3)]' 
                    : 'border-white/5 bg-white/5 text-gray-400 hover:bg-white/10 hover:border-white/20 hover:text-gray-200'"
                >
                  <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
                  <span class="text-2xl transform group-hover:scale-110 transition-transform duration-300">{{ cat.icon }}</span>
                  <span class="text-[10px] font-medium tracking-wide">{{ cat.name }}</span>
                </button>
              </div>
            </div>

            <div class="space-y-2">
              <label class="text-xs font-bold text-gray-400 uppercase tracking-wider ml-1">รายละเอียด</label>
              <textarea 
                v-model="description" 
                rows="4" 
                class="w-full p-4 rounded-2xl bg-white/5 border border-white/10 focus:border-purple-500/50 focus:bg-white/10 text-white placeholder-gray-600 transition-all outline-none resize-none focus:ring-4 focus:ring-purple-500/10 leading-relaxed" 
                placeholder="บอกเล่าเรื่องราวสินค้าของคุณ..."
              ></textarea>
            </div>

            <div class="space-y-2">
              <label class="text-xs font-bold text-gray-400 uppercase tracking-wider ml-1">รูปภาพ</label>
              <div 
                class="relative w-full border-2 border-dashed rounded-3xl p-1 transition-all group overflow-hidden"
                :class="imagePreview ? 'border-pink-500/50 bg-pink-500/5' : 'border-white/10 hover:border-white/30 hover:bg-white/5'"
                @click="$refs.fileInput.click()"
              >
                <input type="file" ref="fileInput" @change="handleFileUpload" accept="image/*" class="hidden" />
                
                <div class="flex flex-col items-center justify-center py-8 cursor-pointer relative z-10">
                  <div v-if="imagePreview" class="relative w-full px-8 group-hover:opacity-90 transition-opacity">
                    <img :src="imagePreview" class="h-48 w-full object-contain rounded-xl shadow-2xl" />
                    <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity bg-black/50 backdrop-blur-sm rounded-xl mx-8">
                       <p class="text-white font-medium flex items-center gap-2">📸 เปลี่ยนรูปภาพ</p>
                    </div>
                  </div>
                  
                  <div v-else class="text-center space-y-3">
                    <div class="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center mx-auto group-hover:scale-110 group-hover:bg-pink-500/20 transition-all duration-300">
                      <span class="text-3xl filter drop-shadow-lg">📷</span>
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-300 group-hover:text-white transition-colors">คลิกเพื่ออัปโหลดรูปภาพ</p>
                      <p class="text-[10px] text-gray-500 mt-1">PNG, JPG, GIF (Max 5MB)</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="pt-4 border-t border-white/10 flex items-center gap-4">
               <button 
                type="submit" 
                :disabled="isSubmitting"
                class="flex-1 py-4 bg-gradient-to-r from-pink-600 via-purple-600 to-indigo-600 hover:from-pink-500 hover:via-purple-500 hover:to-indigo-500 rounded-2xl font-bold text-white transition-all duration-300 shadow-[0_0_20px_rgba(236,72,153,0.3)] hover:shadow-[0_0_30px_rgba(236,72,153,0.5)] transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 group relative overflow-hidden"
              >
                <div class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                <span v-if="isSubmitting" class="animate-spin text-xl">⏳</span>
                <span v-else class="text-lg relative z-10">บันทึกสินค้า ✨</span>
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
import { useRouter } from "vue-router";

const router = useRouter();
const baseURL = "http://localhost:5000";

const name = ref("");
const price = ref("");
const description = ref("");
const imageFile = ref(null);
const imagePreview = ref(null);
const selectedCategory = ref("electronics");
const isSubmitting = ref(false);

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

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;
    imagePreview.value = URL.createObjectURL(file);
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

  if (!name.value || !price.value) {
    alert("กรุณากรอกชื่อสินค้าและราคา");
    return;
  }

  isSubmitting.value = true;

  const formData = new FormData();
  formData.append("name", name.value);
  formData.append("price", price.value);
  formData.append("description", description.value);
  formData.append("category", selectedCategory.value);
  if (imageFile.value) {
    formData.append("image", imageFile.value);
  }

  try {
    await axios.post(`${baseURL}/api/seller/products`, formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "multipart/form-data"
      }
    });
    // เปลี่ยน alert เป็นการ redirect ทันที (หรือใช้ Toast library จะสวยกว่า)
    router.push("/seller-dashboard");
  } catch (err) {
    console.error("Failed to add product:", err);
    alert(err.response?.data?.msg || "ไม่สามารถเพิ่มสินค้าได้ กรุณาลองใหม่อีกครั้ง");
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(() => {
  fetchCategories();
});
</script>

<style scoped>
/* Custom Scrollbar for Categories */
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

/* Background Animation */
@keyframes pulse-slow {
  0%, 100% { opacity: 0.5; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.1); }
}
.animate-pulse-slow {
  animation: pulse-slow 8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>