<template>
  <div class="min-h-screen bg-[#050505] text-white flex flex-col items-center justify-center p-6 relative overflow-hidden font-sans">
    
    <div class="fixed top-0 left-0 w-[500px] h-[500px] bg-pink-600/10 blur-[150px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[500px] h-[500px] bg-purple-900/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

    <header class="relative z-10 mb-8 text-center">
      <h1 class="text-3xl md:text-4xl font-black tracking-tight mb-2">
        <span class="bg-clip-text text-transparent bg-gradient-to-r from-white via-pink-200 to-white">
          Payment Method
        </span>
      </h1>
      <p class="text-gray-400 text-sm">เลือกช่องทางการชำระเงินที่คุณสะดวกที่สุด</p>
    </header>

    <div class="w-full max-w-5xl bg-[#121212]/80 backdrop-blur-2xl border border-white/10 rounded-[2.5rem] p-6 md:p-10 shadow-2xl relative z-10 flex flex-col md:flex-row gap-10">
      
      <div class="md:w-3/5 flex flex-col justify-center">
        <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
          <span class="w-2 h-8 bg-pink-500 rounded-full"></span>
          ช่องทางที่รองรับ
        </h2>

        <div class="space-y-3">
          <button
            v-for="method in paymentMethods"
            :key="method.id"
            @click="selectMethod(method)"
            :class="[
              'w-full flex items-center justify-between p-4 rounded-xl border transition-all duration-300 group relative overflow-hidden',
              selected === method.name 
                ? 'bg-pink-500/10 border-pink-500 shadow-[0_0_20px_rgba(236,72,153,0.3)]' 
                : 'bg-[#1a1a1a] border-white/5 hover:border-pink-500/50 hover:bg-[#202020]'
            ]"
          >
            <div class="absolute inset-0 bg-gradient-to-r from-pink-500/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"></div>

            <div class="flex items-center gap-4 relative z-10">
              <div class="w-10 h-10 rounded-lg bg-white/10 flex items-center justify-center text-xl">
                {{ method.icon }}
              </div>
              <span :class="selected === method.name ? 'text-white font-bold' : 'text-gray-300 font-medium'">
                {{ method.name }}
              </span>
            </div>

            <div class="relative z-10">
              <div :class="[
                'w-5 h-5 rounded-full border flex items-center justify-center transition-all',
                selected === method.name ? 'border-pink-500 bg-pink-500' : 'border-gray-600'
              ]">
                <svg v-if="selected === method.name" class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>
          </button>
        </div>

        <button
          @click="confirmPayment"
          :disabled="!selected"
          class="mt-8 w-full py-4 bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white rounded-2xl font-bold shadow-lg shadow-pink-900/30 transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:shadow-none"
        >
          ยืนยันการเลือก
        </button>
      </div>

      <div class="md:w-2/5 flex flex-col items-center justify-center bg-black/20 rounded-3xl p-6 border border-white/5 relative overflow-hidden">
        
        <div class="absolute top-0 right-0 w-64 h-64 bg-pink-500/20 blur-[80px] rounded-full pointer-events-none"></div>

        <div class="w-full aspect-[1.586/1] bg-gradient-to-br from-gray-800 to-black rounded-2xl p-6 border border-white/10 shadow-2xl relative mb-8 transform transition-transform hover:scale-105 duration-500 group">
          <div class="absolute inset-0 bg-gradient-to-br from-pink-500/20 to-purple-600/20 opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl"></div>
          
          <div class="flex justify-between items-start mb-8 relative z-10">
            <div class="w-12 h-8 bg-yellow-500/20 rounded border border-yellow-500/50 flex items-center justify-center">
              <div class="w-8 h-5 border border-yellow-500/30 rounded-sm"></div>
            </div>
            <span class="text-white font-mono italic font-bold text-lg">VISA</span>
          </div>
          
          <div class="mb-4 relative z-10">
            <div class="flex gap-3">
              <span class="h-2 w-2 bg-gray-600 rounded-full"></span>
              <span class="h-2 w-2 bg-gray-600 rounded-full"></span>
              <span class="h-2 w-2 bg-gray-600 rounded-full"></span>
              <span class="h-2 w-2 bg-gray-600 rounded-full"></span>
            </div>
          </div>

          <div class="flex justify-between items-end relative z-10">
            <div>
              <p class="text-[10px] text-gray-500 uppercase tracking-wider mb-1">Card Holder</p>
              <p class="text-sm text-gray-300 font-mono tracking-wide">{{ username || 'PRINCESS MEMBER' }}</p>
            </div>
            <div>
               <p class="text-[10px] text-gray-500 uppercase tracking-wider mb-1 text-right">Expires</p>
               <p class="text-sm text-gray-300 font-mono">12/28</p>
            </div>
          </div>
        </div>

        <div class="text-center space-y-4 relative z-10">
          <h3 class="text-white font-semibold">Secure Payment</h3>
          <p class="text-xs text-gray-500 leading-relaxed">
            ข้อมูลการชำระเงินของคุณได้รับการเข้ารหัสด้วยมาตรฐานความปลอดภัยสูงสุด (SSL/TLS) เราไม่เก็บข้อมูลบัตรเครดิตของคุณ
          </p>
          
          <div class="flex flex-wrap justify-center gap-3 pt-4">
             <div class="bg-white p-1.5 rounded h-8 w-12 flex items-center justify-center opacity-80 hover:opacity-100 transition-opacity"><img src="https://upload.wikimedia.org/wikipedia/commons/0/04/Visa.svg" class="max-h-full"></div>
             <div class="bg-white p-1.5 rounded h-8 w-12 flex items-center justify-center opacity-80 hover:opacity-100 transition-opacity"><img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Mastercard-logo.svg" class="max-h-full"></div>
             <div class="bg-white p-1.5 rounded h-8 w-12 flex items-center justify-center opacity-80 hover:opacity-100 transition-opacity"><img src="https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg" class="max-h-full"></div>
             <div class="bg-white p-1.5 rounded h-8 w-12 flex items-center justify-center opacity-80 hover:opacity-100 transition-opacity"><img src="https://upload.wikimedia.org/wikipedia/commons/d/d3/PromptPay_Logo.png" class="max-h-full object-contain"></div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";

const router = useRouter();
const selected = ref("");
const username = ref("");

// รายการช่องทางชำระเงิน พร้อม Emoji หรือ Icon (สามารถเปลี่ยนเป็น <img> ได้)
const paymentMethods = [
  { id: 'mastercard', name: 'MasterCard / Visa', icon: '💳' },
  { id: 'truemoney', name: 'TrueMoney Wallet', icon: '📱' },
  { id: 'promptpay', name: 'PromptPay (QR Code)', icon: '💠' },
  { id: 'paypal', name: 'PayPal', icon: '🅿️' },
  { id: 'scb', name: 'Mobile Banking (SCB)', icon: '🏦' }
]

onMounted(() => {
  // ดึงชื่อ User มาโชว์บนบัตร (สวยงามเฉยๆ)
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    try {
      const u = JSON.parse(storedUser);
      username.value = u.name || u.username || "MEMBER";
    } catch { /* ignore */ }
  }
  
  // ดึงค่าเดิมถ้าเคยเลือกไว้
  const prevMethod = localStorage.getItem("paymentMethod");
  if (prevMethod) {
    selected.value = prevMethod;
  }
});

const selectMethod = (method) => {
  selected.value = method.name;
};

const confirmPayment = () => {
  if (!selected.value) {
    alert("กรุณาเลือกวิธีชำระเงินก่อนเพคะ ✨");
    return;
  }

  // Save to localStorage so Checkout page can read it
  localStorage.setItem("paymentMethod", selected.value);

  // Navigate back to checkout/payment page
  router.push("/payment");
};
</script>

<style scoped>
/* No custom CSS needed, pure Tailwind */
</style>