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
            สแกน QR Code เพื่อเติม Token เข้าสู่ระบบอัตโนมัติ สะดวก รวดเร็ว พร้อมประมูลทันที
          </p>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
          
          <div class="lg:col-span-7 space-y-6">
            
            <div class="relative overflow-hidden rounded-[2rem] bg-gradient-to-br from-[#1e1e24] to-[#121215] border border-amber-500/20 p-8 shadow-2xl group">
              <div class="absolute top-0 right-0 w-32 h-32 bg-amber-500/20 blur-[50px] rounded-full group-hover:bg-amber-500/30 transition-all duration-500"></div>
              
              <div class="relative z-10 flex items-center justify-between">
                <div>
                  <p class="text-amber-500/80 font-bold text-sm uppercase tracking-wider mb-2">My Balance</p>
                  <div class="flex items-baseline gap-2">
                    <span class="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-amber-100 to-amber-400 tracking-tighter">
                      {{ tokenBalance.toLocaleString() }}
                    </span>
                    <span class="text-xl text-gray-500 font-medium">Tokens</span>
                  </div>
                </div>
                <div class="w-20 h-20 rounded-2xl bg-gradient-to-br from-amber-500/20 to-transparent border border-amber-500/30 flex items-center justify-center text-4xl shadow-[0_0_30px_rgba(245,158,11,0.2)]">
                  🪙
                </div>
              </div>
            </div>

            <div class="bg-[#121215]/60 backdrop-blur-xl border border-white/5 rounded-[2rem] p-8 shadow-lg">
              <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
                📲 เติม Token ด้วย QR Code
              </h2>
              
              <div class="flex flex-col md:flex-row gap-8">
                <div class="flex-shrink-0 text-center">
                  <div class="bg-white p-3 rounded-2xl inline-block shadow-lg mb-3">
                    <img 
                      src="/promptpay-qr.png" 
                      alt="PromptPay QR" 
                      class="w-40 h-40 object-contain"
                      @error="handleQrError"
                    />
                  </div>
                  <div class="space-y-1">
                     <p class="text-white font-bold text-sm">นาย ศิระณัฐ ศรีบุระ</p>
                     <p class="text-amber-500 font-mono text-xs">xxx-xxx-5414</p>
                     <div class="inline-block px-2 py-1 bg-white/5 rounded text-[10px] text-gray-400 mt-1">
                        1 บาท = 1 Token
                     </div>
                  </div>
                </div>

                <div class="hidden md:block w-px bg-white/10 my-2"></div>

                <div class="flex-1 space-y-4">
                  <div 
                    class="border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer transition-all relative overflow-hidden group"
                    :class="[
                      isDragging 
                        ? 'border-amber-500 bg-amber-500/10' 
                        : 'border-white/10 bg-[#0b0b0f] hover:border-amber-500/50 hover:bg-white/5'
                    ]"
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
                    
                    <div v-if="!slipPreview" class="py-4">
                      <div class="w-12 h-12 rounded-full bg-white/5 flex items-center justify-center mx-auto mb-3 text-2xl group-hover:scale-110 transition-transform">
                        📎
                      </div>
                      <p class="text-gray-300 font-medium text-sm">คลิกเพื่อแนบสลิป</p>
                      <p class="text-gray-600 text-xs mt-1">หรือลากไฟล์มาวางที่นี่</p>
                    </div>

                    <div v-else class="relative h-40 flex items-center justify-center">
                      <img :src="slipPreview" class="max-h-full rounded-lg shadow-lg" />
                      <button 
                        @click.stop="clearSlip"
                        class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full w-6 h-6 flex items-center justify-center hover:bg-red-600 shadow-lg z-10"
                      >
                        ×
                      </button>
                    </div>
                  </div>

                  <button 
                    @click="verifySlip"
                    :disabled="!slipFile || isVerifying"
                    class="w-full py-4 rounded-2xl font-bold text-lg shadow-lg shadow-amber-900/20 transition-all duration-300 relative overflow-hidden group disabled:opacity-50 disabled:cursor-not-allowed"
                    :class="!slipFile ? 'bg-gray-800 text-gray-500' : 'bg-gradient-to-r from-amber-500 to-yellow-600 text-black hover:scale-[1.02]'"
                  >
                    <span class="relative z-10 flex items-center justify-center gap-2">
                       <span v-if="isVerifying" class="animate-spin text-xl">⏳</span>
                       {{ isVerifying ? 'กำลังตรวจสอบสลิป...' : '🔍 ยืนยันการเติมเงิน' }}
                    </span>
                    <div v-if="slipFile && !isVerifying" class="absolute inset-0 bg-white/20 translate-y-full group-hover:translate-y-0 transition-transform duration-300"></div>
                  </button>
                </div>
              </div>

              <div v-if="verifyResult" class="mt-6 animate-in-fade">
                <div class="rounded-xl p-4 border flex items-start gap-4"
                  :class="verifyResult.success ? 'bg-green-500/10 border-green-500/20' : 'bg-red-500/10 border-red-500/20'"
                >
                  <div class="text-2xl mt-1">{{ verifyResult.success ? '🎉' : '⚠️' }}</div>
                  <div class="flex-1">
                    <h3 class="font-bold" :class="verifyResult.success ? 'text-green-400' : 'text-red-400'">
                      {{ verifyResult.msg }}
                    </h3>
                    <div v-if="verifyResult.success" class="mt-2 space-y-1 text-sm text-gray-400">
                      <div class="flex justify-between">
                        <span>ยอดเงิน:</span>
                        <span class="text-white">{{ verifyResult.amount?.toLocaleString() }} THB</span>
                      </div>
                      <div class="flex justify-between">
                         <span>ผู้โอน:</span>
                         <span class="text-white">{{ verifyResult.sender_name }}</span>
                      </div>
                       <div class="flex justify-between pt-2 border-t border-white/10 mt-2">
                         <span class="text-amber-500">Token ใหม่:</span>
                         <span class="text-amber-400 font-bold text-lg">{{ verifyResult.new_balance?.toLocaleString() }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <div class="lg:col-span-5 h-full">
            <div class="bg-[#121215]/60 backdrop-blur-xl border border-white/5 rounded-[2rem] p-6 shadow-lg h-full flex flex-col">
              <div class="flex items-center justify-between mb-6 px-2">
                <h2 class="text-xl font-bold text-white flex items-center gap-2">
                  📜 ประวัติรายการ
                </h2>
                <span class="text-xs text-gray-500 bg-white/5 px-2 py-1 rounded-md">{{ requests.length }} รายการ</span>
              </div>
              
              <div class="flex-1 overflow-y-auto custom-scrollbar pr-2 space-y-3 max-h-[600px]">
                <div 
                  v-for="req in requests" 
                  :key="req.id"
                  class="group p-4 rounded-2xl border transition-all hover:bg-white/5 relative overflow-hidden"
                  :class="getStatusBorderColor(req.status)"
                >
                  <div class="flex justify-between items-start mb-2 relative z-10">
                    <div>
                      <span class="block text-lg font-bold text-white tracking-wide flex items-center gap-2">
                        {{ req.amount.toLocaleString() }} <span class="text-xs font-normal text-gray-500">Token</span>
                        <span v-if="req.is_auto_approved" class="text-[10px] bg-blue-500/20 text-blue-400 px-1.5 py-0.5 rounded border border-blue-500/30">⚡ Auto</span>
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

                  <div v-if="req.payment_proof_url" class="mt-3 relative z-10">
                    <img 
                      :src="`${baseUrl}${req.payment_proof_url}`" 
                      class="h-12 w-auto rounded border border-white/10 hover:border-amber-500/50 cursor-zoom-in transition-colors object-cover"
                      @click="showSlipModal(req.payment_proof_url)"
                      title="ดูสลิป"
                    />
                  </div>

                  <div v-if="req.admin_note" class="mt-3 pt-3 border-t border-white/5 flex gap-2 items-start relative z-10">
                    <span class="text-xs">💬</span>
                    <p class="text-xs text-gray-400 italic leading-relaxed">"{{ req.admin_note }}"</p>
                  </div>

                  <div class="absolute -right-4 -top-4 w-20 h-20 blur-[40px] rounded-full opacity-20 pointer-events-none" :class="getStatusGlowColor(req.status)"></div>
                </div>

                <div v-if="!requests.length" class="h-64 flex flex-col items-center justify-center text-center opacity-50">
                  <div class="w-16 h-16 rounded-full bg-white/5 flex items-center justify-center text-2xl mb-3 grayscale">📋</div>
                  <p class="text-gray-400 text-sm">ยังไม่มีประวัติการทำรายการ</p>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </main>

    <div v-if="slipModalUrl" class="fixed inset-0 bg-black/90 backdrop-blur-sm flex items-center justify-center z-[100] p-4 animate-in-fade" @click="slipModalUrl = null">
      <div class="relative max-w-lg w-full">
         <button class="absolute -top-12 right-0 text-white hover:text-amber-500 transition-colors text-xl">ปิด X</button>
         <img :src="`${baseUrl}${slipModalUrl}`" class="w-full h-auto rounded-2xl shadow-2xl border border-white/10" />
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// -- Config & State --
const baseUrl = 'http://localhost:5000';
const tokenBalance = ref(0);
const requests = ref([]);

// -- Upload & Verify State --
const isVerifying = ref(false);
const slipFile = ref(null);
const slipPreview = ref(null);
const isDragging = ref(false);
const verifyResult = ref(null);
const slipModalUrl = ref(null);

const statusLabels = {
  pending: 'รอตรวจสอบ',
  approved: 'สำเร็จ',
  rejected: 'ปฏิเสธ'
};

// -- Style Helpers --
const getStatusBadgeClass = (status) => {
  const classes = {
    pending: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    approved: 'bg-green-500/10 text-green-400 border-green-500/20',
    rejected: 'bg-red-500/10 text-red-400 border-red-500/20'
  };
  return classes[status] || 'bg-gray-500/10 text-gray-400';
};

const getStatusBorderColor = (status) => {
  const classes = {
    pending: 'bg-white/5 border-white/5 hover:border-yellow-500/30',
    approved: 'bg-[#0f1812]/50 border-green-900/30 hover:border-green-500/30',
    rejected: 'bg-[#180f0f]/50 border-red-900/30 hover:border-red-500/30'
  };
  return classes[status] || 'border-white/5';
};

const getStatusGlowColor = (status) => {
  const classes = {
    pending: 'bg-yellow-500',
    approved: 'bg-green-500',
    rejected: 'bg-red-500'
  };
  return classes[status] || 'bg-gray-500';
};

// -- Core Logic --
function formatDate(dateStr) {
  if(!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleDateString('th-TH', {
    year: '2-digit', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit'
  });
}

function handleQrError(e) {
  e.target.src = 'https://via.placeholder.com/256x256?text=QR+Error';
}

// File Handling
function handleFileSelect(event) {
  const file = event.target.files[0];
  if (file) processFile(file);
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
  verifyResult.value = null; // Clear old result
}

function clearSlip() {
  slipFile.value = null;
  slipPreview.value = null;
  verifyResult.value = null;
}

// Show Full Image Modal
function showSlipModal(url) {
  slipModalUrl.value = url;
}

// API Calls
async function fetchTokenBalance() {
  const token = localStorage.getItem('token');
  if (!token) return;
  try {
    const res = await axios.get(`${baseUrl}/api/token/balance`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    tokenBalance.value = res.data.token_balance || 0;
  } catch (err) {
    console.error('Failed to fetch balance:', err);
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

async function verifySlip() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('กรุณาเข้าสู่ระบบก่อน');
    return;
  }
  if (!slipFile.value) return;

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
      // Refresh Data
      fetchTokenBalance();
      fetchRequests();
      // Auto clear after 5s
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

onMounted(() => {
  fetchTokenBalance();
  fetchRequests();
});
</script>

<style scoped>
.animate-in-fade {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

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
</style>