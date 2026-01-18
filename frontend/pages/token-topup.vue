<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-amber-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-20 right-0 w-[500px] h-[500px] bg-amber-600/10 blur-[150px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 left-0 w-[600px] h-[600px] bg-yellow-900/10 blur-[120px] rounded-full pointer-events-none z-0"></div>

    <main class="ml-20 relative z-10 p-6 md:p-10 min-h-screen flex justify-center">
      <div class="w-full max-w-6xl animate-in-fade">
        
        <header class="mb-10">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 mb-3">
            <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
            <span class="text-[10px] font-bold text-amber-300 uppercase tracking-widest">Auction Currency</span>
          </div>
          <h1 class="text-4xl font-extrabold text-white flex items-center gap-3">
            🪙 Token Management
          </h1>
          <p class="text-gray-400 mt-2 max-w-xl">
            เติม Token เพื่อใช้ในการประมูลสินค้าที่คุณต้องการ ยิ่งมีมาก ยิ่งมีโอกาสชนะการประมูลสูง
          </p>
          
          <!-- Token Balance Display -->
          <div class="mt-6 inline-flex items-center gap-4 px-6 py-4 rounded-2xl bg-gradient-to-r from-amber-500/10 to-yellow-500/10 border border-amber-500/20">
            <div class="flex items-center justify-center w-14 h-14 rounded-xl bg-amber-500/20">
              <span class="text-3xl">🪙</span>
            </div>
            <div>
              <p class="text-xs text-amber-400/80 uppercase tracking-wider font-medium">Token คงเหลือ</p>
              <p class="text-3xl font-bold text-amber-400">{{ tokenBalance.toLocaleString() }}</p>
            </div>
          </div>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- QR Code & Upload Section -->
          <div class="space-y-6">
            <!-- PromptPay QR Code -->
            <div class="card p-6">
              <h2 class="text-xl font-semibold text-white mb-4">📱 สแกน QR Code เพื่อชำระเงิน</h2>
              <div class="bg-white rounded-2xl p-4 mx-auto w-fit">
                <img 
                  src="/promptpay-qr.png" 
                  alt="PromptPay QR Code" 
                  class="w-64 h-64 object-contain"
                  @error="handleQrError"
                />
              </div>
              <div class="mt-4 text-center">
                <p class="text-white font-semibold">นาย ศิระณัฐ ศรีบุระ</p>
                <p class="text-dark-400 text-sm">พร้อมเพย์: xxx-xxx-5414</p>
                <p class="text-dark-500 text-xs mt-2">💡 อัตรา 1 Token = 1 บาท</p>
              </div>
            </div>

            <!-- Slip Upload -->
            <div class="card p-6">
              <h2 class="text-xl font-semibold text-white mb-4">📤 อัปโหลดสลิปการโอนเงิน</h2>
              
              <!-- Drag & Drop Zone -->
              <div 
                class="border-2 border-dashed border-dark-600 rounded-2xl p-8 text-center cursor-pointer transition-all hover:border-primary-500 hover:bg-dark-800/50"
                :class="{ 'border-primary-500 bg-primary-500/10': isDragging }"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="handleDrop"
                @click="$refs.fileInput.click()"
              >
                <input 
                  ref="fileInput"
                  type="file" 
                  accept="image/*"
                  class="hidden"
                  @change="handleFileSelect"
                />
                
                <div v-if="!slipPreview">
                  <div class="text-5xl mb-3">📎</div>
                  <p class="text-dark-300 font-medium">ลากไฟล์มาวางที่นี่</p>
                  <p class="text-dark-500 text-sm mt-1">หรือคลิกเพื่อเลือกไฟล์</p>
                  <p class="text-dark-600 text-xs mt-2">รองรับ: JPG, PNG, WEBP</p>
                </div>
                
                <div v-else class="relative">
                  <img :src="slipPreview" alt="Slip Preview" class="max-h-64 mx-auto rounded-xl" />
                  <button 
                    @click.stop="clearSlip"
                    class="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600"
                  >
                    ✕
                  </button>
                </div>
              </div>

              <!-- Verify Button -->
              <button 
                @click="verifySlip"
                :disabled="!slipFile || isVerifying"
                class="btn-primary w-full py-4 text-lg font-bold mt-4 disabled:opacity-50"
              >
                <span v-if="isVerifying" class="flex items-center justify-center gap-2">
                  <svg class="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  กำลังตรวจสอบสลิป...
                </span>
                <span v-else>🔍 ตรวจสอบสลิปและเติม Token</span>
              </button>

              <!-- Verification Result -->
              <div v-if="verifyResult" class="mt-4 rounded-xl p-4" :class="verifyResult.success ? 'bg-green-500/20' : 'bg-red-500/20'">
                <div class="flex items-start gap-3">
                  <span class="text-2xl">{{ verifyResult.success ? '✅' : '❌' }}</span>
                  <div>
                    <p class="font-bold" :class="verifyResult.success ? 'text-green-400' : 'text-red-400'">
                      {{ verifyResult.msg }}
                    </p>
                    <div v-if="verifyResult.success" class="text-dark-300 text-sm mt-2">
                      <p>💰 ยอดเงิน: {{ verifyResult.amount?.toLocaleString() }} บาท</p>
                      <p>🧾 เลขอ้างอิง: {{ verifyResult.transaction_ref }}</p>
                      <p>👤 ผู้โอน: {{ verifyResult.sender_name }}</p>
                      <p class="text-primary-400 font-bold mt-2">Token ใหม่: {{ verifyResult.new_balance?.toLocaleString() }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column: History -->
          <div class="card p-6">
            <h2 class="text-xl font-semibold text-white mb-6">📜 ประวัติการเติม Token</h2>
            
            <div v-if="requests.length" class="space-y-3 max-h-[600px] overflow-y-auto pr-2">
              <div 
                v-for="req in requests" 
                :key="req.id"
                class="glass-light rounded-xl p-4 relative overflow-hidden"
              >
                <div class="flex justify-between items-start mb-2 relative z-10">
                  <div>
                    <span class="block text-lg font-bold text-white tracking-wide">
                      {{ req.amount.toLocaleString() }} <span class="text-xs font-normal text-gray-500">Token</span>
                    </span>
                    <span class="text-[10px] text-gray-500 font-mono">{{ formatDate(req.created_at) }}</span>
                  </div>
                  <span 
                    class="px-3 py-1 rounded-full text-xs font-bold border backdrop-blur-md"
                    :class="getStatusBadgeClass(req.status)"
                  >
                    {{ statusLabels[req.status] }}
                  </span>
                </div>

                <!-- Show slip preview if available -->
                <div v-if="req.payment_proof_url" class="mt-2">
                  <img 
                    :src="`http://localhost:5000${req.payment_proof_url}`" 
                    alt="Slip" 
                    class="h-20 rounded-lg cursor-pointer hover:opacity-80"
                    @click="showSlipModal(req.payment_proof_url)"
                  />
                </div>
                
                <!-- Auto-approved badge -->
                <span v-if="req.is_auto_approved" class="inline-block mt-2 text-xs bg-blue-500/20 text-blue-400 px-2 py-1 rounded-full">
                  ⚡ อนุมัติอัตโนมัติ
                </span>
                
                <div v-if="req.admin_note" class="mt-3 pt-3 border-t border-white/5 flex gap-2 items-start">
                  <span class="text-xs">💬</span>
                  <p class="text-xs text-gray-400 italic leading-relaxed">"{{ req.admin_note }}"</p>
                </div>

                <div class="absolute -right-4 -top-4 w-20 h-20 blur-[40px] rounded-full opacity-20 pointer-events-none" :class="getStatusGlowColor(req.status)"></div>
              </div>
            </div>

            <div v-else class="h-64 flex flex-col items-center justify-center text-center opacity-50">
              <div class="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center text-2xl mb-3 grayscale">📋</div>
              <p class="text-gray-400 text-sm">ยังไม่มีประวัติการทำรายการ</p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Slip Modal -->
    <div v-if="slipModalUrl" class="fixed inset-0 bg-black/80 flex items-center justify-center z-50" @click="slipModalUrl = null">
      <div class="max-w-2xl max-h-[90vh] p-4">
        <img :src="`http://localhost:5000${slipModalUrl}`" alt="Slip" class="max-h-full rounded-xl" />
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const tokenBalance = ref(0);
const requests = ref([]);
const isVerifying = ref(false);

const slipFile = ref(null);
const slipPreview = ref(null);
const isDragging = ref(false);
const verifyResult = ref(null);
const slipModalUrl = ref(null);

const baseUrl = 'http://localhost:5000';

const statusLabels = {
  pending: 'รอตรวจสอบ',
  approved: 'สำเร็จ',
  rejected: 'ปฏิเสธ'
};

const getStatusBadgeClass = (status) => {
  const classes = {
    pending: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    approved: 'bg-green-500/10 text-green-400 border-green-500/20',
    rejected: 'bg-red-500/10 text-red-400 border-red-500/20'
  };
  return classes[status] || 'bg-gray-500/10 text-gray-400';
};

const getStatusGlowColor = (status) => {
  const classes = {
    pending: 'bg-yellow-500',
    approved: 'bg-green-500',
    rejected: 'bg-red-500'
  };
  return classes[status] || 'bg-gray-500';
};

function formatDate(dateStr) {
  if(!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('th-TH', {
    year: '2-digit', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
}

function handleQrError(e) {
  // If QR image fails to load, use placeholder
  e.target.src = 'https://via.placeholder.com/256x256?text=QR+Code';
}

function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) {
    processFile(file);
  }
}

function handleDrop(event) {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) {
    processFile(file);
  }
}

function processFile(file) {
  slipFile.value = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    slipPreview.value = e.target.result;
  };
  reader.readAsDataURL(file);
  verifyResult.value = null;
}

function clearSlip() {
  slipFile.value = null;
  slipPreview.value = null;
  verifyResult.value = null;
}

async function verifySlip() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('กรุณาเข้าสู่ระบบก่อน');
    return;
  }
  
  if (!slipFile.value) {
    alert('กรุณาเลือกไฟล์สลิป');
    return;
  }
  
  isVerifying.value = true;
  verifyResult.value = null;
  
  try {
    const formData = new FormData();
    formData.append('slip', slipFile.value);
    
    const res = await axios.post(`${baseUrl}/api/token/verify-slip`, formData, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      }
    });
    
    verifyResult.value = res.data;
    
    if (res.data.success) {
      // Refresh data
      fetchTokenBalance();
      fetchRequests();
      // Clear slip after success
      setTimeout(() => {
        clearSlip();
      }, 5000);
    }
  } catch (err) {
    verifyResult.value = {
      success: false,
      msg: err.response?.data?.msg || 'เกิดข้อผิดพลาดในการตรวจสอบสลิป'
    };
  } finally {
    isVerifying.value = false;
  }
}

function showSlipModal(url) {
  slipModalUrl.value = url;
}

async function fetchTokenBalance() {
  const token = localStorage.getItem('token');
  if (!token) return;
  
  try {
    const res = await axios.get(`${baseUrl}/api/token/balance`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    tokenBalance.value = res.data.token_balance || 0;
  } catch (err) {
    console.error('Failed to fetch token balance:', err);
  }
}

async function fetchRequests() {
  const token = localStorage.getItem('token');
  if (!token) return;
  
  try {
    const res = await axios.get(`${baseUrl}/api/token/my-requests`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    requests.value = res.data.requests || [];
  } catch (err) {
    console.error('Failed to fetch requests:', err);
  }
}

onMounted(() => {
  fetchTokenBalance();
  fetchRequests();
});
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

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Card Styles */
.card {
  background: rgba(18, 18, 21, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 1.5rem;
}

.glass-light {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.btn-primary {
  background: linear-gradient(to right, #f59e0b, #d97706);
  color: black;
  border-radius: 1rem;
  transition: all 0.3s;
}

.btn-primary:hover:not(:disabled) {
  transform: scale(1.02);
}
</style>