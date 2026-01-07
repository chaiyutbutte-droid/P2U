<template>
  <div class="min-h-screen bg-dark-950 text-white p-6 flex flex-col items-center">
    <header class="w-full max-w-3xl flex items-center justify-between mb-8 mt-4">
      <h1 class="text-3xl font-bold bg-gradient-to-r from-white to-pink-300 bg-clip-text text-transparent">
        ชำระเงิน ✨
      </h1>
      <NuxtLink to="/cart" class="text-sm text-pink-400 hover:underline">กลับไปที่ตะกร้า</NuxtLink>
    </header>

    <div class="w-full max-w-3xl space-y-4 mb-6">
      <div
        v-for="(item, index) in cartItems"
        :key="index"
        class="glass p-5 rounded-3xl border border-white/5 flex items-center gap-5 shadow-xl"
      >
        <img
          :src="getImageUrl(item.image_url || item.image)"
          alt="product"
          class="w-20 h-20 object-cover rounded-2xl border border-white/10"
          @error="onImgError($event)"
        />
        <div class="flex-1 min-w-0">
          <h2 class="font-bold text-lg truncate">{{ item.name }}</h2>
          <p class="text-dark-400 text-sm italic">ราคาต่อชิ้น: ฿{{ Number(item.price).toLocaleString() }}</p>
          <p class="text-pink-400 text-sm font-medium mt-1">จำนวน: {{ item.quantity }} ชิ้น</p>
        </div>
        <div class="text-right">
          <p class="text-lg font-black text-white">฿{{ (item.price * item.quantity).toLocaleString() }}</p>
        </div>
      </div>
    </div>

    <div class="w-full max-w-3xl space-y-6">
      <div class="glass p-6 rounded-[2rem] border border-pink-500/20 flex justify-between items-center shadow-lg shadow-pink-500/5">
        <p class="text-lg font-medium text-dark-200">ยอดชำระสุทธิ</p>
        <p class="text-3xl font-black text-pink-500">฿{{ totalPrice.toLocaleString() }}</p>
      </div>

      <div class="glass p-8 rounded-[2rem] border border-white/5 space-y-6">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <p class="text-dark-400 text-xs uppercase tracking-wider mb-1">ช่องทางชำระเงิน</p>
            <div class="flex items-center gap-2">
              <span class="text-green-400 font-bold">{{ paymentMethod }}</span>
              <NuxtLink to="/paymentMethod" class="text-[10px] text-blue-400 hover:underline">(เปลี่ยน)</NuxtLink>
            </div>
          </div>
          <div class="text-right">
            <p class="text-dark-400 text-xs uppercase tracking-wider mb-1">บัญชีผู้ใช้</p>
            <p class="font-semibold text-white truncate">{{ username || 'Guest' }}</p>
          </div>
        </div>

        <div class="h-px bg-white/5"></div>

        <div class="flex items-start gap-3 cursor-pointer" @click="termsAccepted = !termsAccepted">
          <div class="mt-1">
            <input type="checkbox" id="terms" v-model="termsAccepted" class="w-5 h-5 accent-pink-500 rounded-lg cursor-pointer" @click.stop />
          </div>
          <label for="terms" class="text-sm text-dark-300 leading-relaxed cursor-pointer">
            ฉันได้ตรวจสอบรายการสินค้าและยอมรับ <a href="#" class="underline text-pink-400/80">ข้อตกลงการชำระเงิน</a> เรียบร้อยแล้ว
          </label>
        </div>

        <button
          :disabled="!termsAccepted || cartItems.length === 0"
          @click="buyNow"
          class="w-full bg-gradient-to-r from-pink-500 to-rose-600 hover:from-pink-400 hover:to-rose-500 text-white font-bold py-4 rounded-2xl shadow-lg shadow-pink-500/20 transition-all active:scale-[0.98] disabled:opacity-30 disabled:grayscale disabled:cursor-not-allowed text-lg"
        >
          ชำระเงินตอนนี้ 💖
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// ✅ URL ต้องมี /api เพื่อให้ตรงกับโครงสร้าง Backend
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

onMounted(() => {
  const storedCheckout = localStorage.getItem("checkout_items");
  if (storedCheckout) {
    try {
      cartItems.value = JSON.parse(storedCheckout);
      console.log("Items for Payment:", cartItems.value);
    } catch {
      cartItems.value = [];
    }
  } else {
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

    // ✅ ส่ง ID ที่มีอยู่ในข้อมูล (ดึงทั้งจาก _id และ id)
    const itemIds = cartItems.value.map(item => item._id || item.id).filter(id => id);
    
    console.log("Sending IDs to Backend:", itemIds);

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
      alert("ชำระเงินสำเร็จแล้วเพคะ! ✨");

      // ลบรายการที่ซื้อแล้วออกจากตะกร้าหลัก
      const fullCart = JSON.parse(localStorage.getItem("cart") || "[]");
      const remainingCart = fullCart.filter(item => !itemIds.includes(item._id || item.id));
      localStorage.setItem("cart", JSON.stringify(remainingCart));

      // ล้างรายการ checkout
      localStorage.removeItem("checkout_items");

      router.push("/payment_success");
    } else {
      alert(`ขออภัยเพคะ: ${result.msg || 'เกิดข้อผิดพลาด'}`);
    }
  } catch (error) {
    console.error("Error creating order:", error);
    alert("ไม่สามารถติดต่อเซิร์ฟเวอร์ได้ ตรวจสอบว่าเรียก URL /api/orders ถูกต้องหรือไม่นะเพคะ");
  }
};
</script>

<style scoped>
.bg-dark-950 { background-color: #0a0a0a; }
.text-dark-200 { color: #e5e5e5; }
.text-dark-300 { color: #a3a3a3; }
.text-dark-400 { color: #737373; }
.glass { 
  background: rgba(255, 255, 255, 0.03); 
  backdrop-filter: blur(20px); 
  -webkit-backdrop-filter: blur(20px);
}
</style>