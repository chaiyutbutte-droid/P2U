<template>
  <div class="min-h-screen bg-[#050505] text-white p-6 flex flex-col items-center font-sans relative overflow-hidden">
    
    <div class="fixed top-0 left-0 w-[600px] h-[600px] bg-pink-600/10 blur-[150px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[600px] h-[600px] bg-purple-900/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

    <header class="w-full max-w-3xl flex items-center justify-between mb-8 mt-4 relative z-10">
      <h1 class="text-3xl font-black tracking-tight text-white flex items-center gap-2">
        <span class="bg-clip-text text-transparent bg-gradient-to-r from-pink-400 to-purple-400">Checkout</span>
        <span>✨</span>
      </h1>
      <button @click="router.push('/cart')" class="text-sm text-gray-400 hover:text-white transition-colors flex items-center gap-1 group">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transform group-hover:-translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        กลับไปที่ตะกร้า
      </button>
    </header>

    <div class="w-full max-w-3xl space-y-4 mb-8 relative z-10">
      <div
        v-for="(item, index) in cartItems"
        :key="index"
        class="bg-[#121212]/80 backdrop-blur-xl p-4 rounded-2xl border border-white/5 flex items-center gap-5 shadow-lg group hover:border-pink-500/30 transition-all duration-300"
      >
        <div class="relative w-20 h-20 shrink-0">
          <div class="absolute inset-0 bg-gradient-to-tr from-pink-500/20 to-purple-600/20 rounded-xl blur-sm opacity-0 group-hover:opacity-100 transition-opacity"></div>
          <img
            :src="getImageUrl(item.image_url || item.image)"
            alt="product"
            class="relative w-full h-full object-cover rounded-xl border border-white/10 shadow-inner"
            @error="onImgError($event)"
          />
        </div>

        <div class="flex-1 min-w-0">
          <h2 class="font-bold text-lg text-gray-100 truncate mb-1">{{ item.name }}</h2>
          <div class="flex items-center gap-3 text-sm">
            <span class="text-gray-500">฿{{ Number(item.price).toLocaleString() }} / ชิ้น</span>
            <span class="bg-white/5 px-2 py-0.5 rounded text-pink-400 text-xs font-medium border border-pink-500/20">x{{ item.quantity }}</span>
          </div>
        </div>

        <div class="text-right px-2">
          <p class="text-lg font-bold text-white tracking-wide">฿{{ (item.price * item.quantity).toLocaleString() }}</p>
        </div>
      </div>
    </div>

    <div class="w-full max-w-3xl relative z-10">
      <div class="bg-[#1a1a1e]/90 backdrop-blur-xl p-6 md:p-8 rounded-[2rem] border border-white/10 shadow-2xl space-y-6">
        
        <div class="flex justify-between items-center border-b border-white/5 pb-6">
          <p class="text-gray-400 text-sm uppercase tracking-wider font-medium">ยอดชำระสุทธิ</p>
          <p class="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-pink-300 to-purple-300">
            ฿{{ totalPrice.toLocaleString() }}
          </p>
        </div>

        <div class="grid grid-cols-2 gap-4 py-2">
          <div class="bg-black/20 rounded-xl p-4 border border-white/5">
            <p class="text-gray-500 text-[10px] uppercase tracking-wider mb-2">ช่องทางชำระเงิน</p>
            <div class="flex flex-col sm:flex-row sm:items-center gap-2">
              <span class="text-green-400 font-bold flex items-center gap-1">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/></svg>
                {{ paymentMethod }}
              </span>
              <button @click="router.push('/paymentMethod')" class="text-[10px] text-blue-400 hover:text-blue-300 underline underline-offset-2 decoration-blue-500/30">เปลี่ยน</button>
            </div>
          </div>

          <div class="bg-black/20 rounded-xl p-4 border border-white/5 text-right">
            <p class="text-gray-500 text-[10px] uppercase tracking-wider mb-2">บัญชีผู้ใช้</p>
            <p class="font-semibold text-white truncate text-sm">{{ username || 'Guest' }}</p>
          </div>
        </div>

        <div class="flex items-start gap-3 p-3 rounded-xl hover:bg-white/5 transition-colors cursor-pointer group" @click="termsAccepted = !termsAccepted">
          <div class="mt-0.5 relative">
            <input type="checkbox" id="terms" v-model="termsAccepted" class="peer appearance-none w-5 h-5 border-2 border-gray-600 rounded bg-transparent checked:bg-pink-500 checked:border-pink-500 transition-all cursor-pointer" @click.stop />
            <svg class="w-3.5 h-3.5 absolute top-1 left-1 text-white opacity-0 peer-checked:opacity-100 pointer-events-none transition-opacity" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
              <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <label for="terms" class="text-sm text-gray-400 leading-relaxed cursor-pointer select-none group-hover:text-gray-300 transition-colors">
            ฉันได้ตรวจสอบรายการสินค้าและยอมรับ <span class="text-pink-400 underline underline-offset-2 decoration-pink-500/30">ข้อตกลงการชำระเงิน</span> เรียบร้อยแล้ว
          </label>
        </div>

        <button
          :disabled="!termsAccepted || cartItems.length === 0"
          @click="buyNow"
          class="w-full relative group overflow-hidden rounded-2xl p-[1px] disabled:opacity-50 disabled:cursor-not-allowed transition-all active:scale-[0.98]"
        >
          <div class="absolute inset-0 bg-gradient-to-r from-pink-600 to-purple-600 group-hover:from-pink-500 group-hover:to-purple-500 transition-all"></div>
          <div class="relative bg-[#1a1a1e] group-hover:bg-transparent transition-all h-full rounded-2xl py-4 flex items-center justify-center gap-2">
            <span class="text-white font-bold text-lg tracking-wide group-hover:drop-shadow-md">ชำระเงินตอนนี้</span>
            <span class="text-xl group-hover:scale-125 transition-transform duration-300">💖</span>
          </div>
        </button>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const baseURL = "http://localhost:5000/api"; 
const defaultImage = "/no-image.png";

const cartItems = ref([]);
const username = ref("");
const paymentMethod = ref("MasterCard");
const termsAccepted = ref(false);

const getImageUrl = (path) => {
  if (!path) return defaultImage;
  if (path.startsWith("http")) return path;
  return `http://localhost:5000/${path.replace(/^\/+/, "")}`;
};

const onImgError = (event) => {
  event.target.src = defaultImage;
};

const getCartKey = () => {
  if (!process.client) return 'cart_guest';
  const user = localStorage.getItem('user');
  if (user) {
    try {
        const userData = JSON.parse(user);
        return `cart_${userData.id || userData._id || userData.email}`;
    } catch (e) { return 'cart_guest' }
  }
  return 'cart_guest';
};

onMounted(() => {
  if (!process.client) return;
  
  const storedCheckout = localStorage.getItem("checkout_items");
  if (storedCheckout) {
    try {
      cartItems.value = JSON.parse(storedCheckout);
    } catch {
      cartItems.value = [];
    }
  } else {
    // ถ้าไม่มีของที่จะ Checkout ให้เด้งกลับตะกร้า
    router.push("/cart");
  }

  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    try {
      const user = JSON.parse(storedUser);
      username.value = user.username || user.name || "";
    } catch {
      username.value = "";
    }
  }

  const storedMethod = localStorage.getItem("paymentMethod");
  if (storedMethod) paymentMethod.value = storedMethod;
});

const totalPrice = computed(() =>
  cartItems.value.reduce(
    (sum, item) => sum + (Number(item.price) || 0) * (Number(item.quantity) || 0),
    0
  )
);

const buyNow = async () => {
  if (!termsAccepted.value) return;

  try {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("กรุณาเข้าสู่ระบบก่อนนะเพคะ ✨");
      return;
    }

    const itemIds = cartItems.value.map(item => item._id || item.id).filter(id => id);
    
    // --- STEP 1: สร้างคำสั่งซื้อ ---
    const response = await fetch(`${baseURL}/orders`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      },
      body: JSON.stringify({
        cart_items: itemIds
      })
    });

    const result = await response.json();

    if (response.ok) {
      const newOrderId = result.order_id;

      // --- STEP 2: อัปเดตสถานะเป็น 'paid' ทันที ---
      if (newOrderId) {
        try {
          await fetch(`${baseURL}/orders/${newOrderId}/pay`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`
            }
          });
        } catch (payErr) {
          console.error("Auto-pay update failed:", payErr);
        }
      }

      // ลบรายการที่ซื้อแล้วออกจากตะกร้าหลัก
      const cartKey = getCartKey();
      const fullCart = JSON.parse(localStorage.getItem(cartKey) || "[]");
      const remainingCart = fullCart.filter(item => !itemIds.includes(item._id || item.id));
      localStorage.setItem(cartKey, JSON.stringify(remainingCart));
      
      // Trigger update event เพื่อให้ Navbar อัปเดตเลขตะกร้า
      window.dispatchEvent(new Event('storage'));

      // ล้างรายการ checkout
      localStorage.removeItem("checkout_items");

      // ไปหน้าสำเร็จ
      router.push("/payment_success");
    } else {
      alert(`ขออภัยเพคะ: ${result.msg || 'เกิดข้อผิดพลาด'}`);
    }
  } catch (error) {
    console.error("Error creating order:", error);
    alert("ไม่สามารถติดต่อเซิร์ฟเวอร์ได้นะเพคะ");
  }
};
</script>

<style scoped>
/* ไม่มี Custom CSS เพราะใช้ Tailwind ทั้งหมดเพื่อป้องกันปัญหา */
</style>