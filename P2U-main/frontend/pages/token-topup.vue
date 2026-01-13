<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />

    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold text-white flex items-center gap-3">
            🪙 เติม Token
          </h1>
          <p class="text-dark-400 mt-1">เติม Token เพื่อใช้ในการประมูลสินค้า</p>
        </div>
      </div>

      <!-- Token Balance Card -->
      <div class="card p-6 mb-8">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-dark-400 text-sm">Token คงเหลือ</p>
            <p class="text-4xl font-bold text-primary-400 mt-1">{{ tokenBalance.toLocaleString() }}</p>
          </div>
          <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center text-3xl">
            🪙
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Request Form -->
        <div class="card p-6">
          <h2 class="text-xl font-semibold text-white mb-6">📝 ส่งคำขอเติม Token</h2>
          
          <div class="space-y-4">
            <!-- Amount Input -->
            <div>
              <label class="block text-dark-300 text-sm mb-2">จำนวน Token ที่ต้องการ</label>
              <input 
                v-model.number="requestAmount" 
                type="number" 
                min="1"
                class="input-glass w-full text-xl font-bold"
                placeholder="100"
              />
            </div>

            <!-- Quick Amount Buttons -->
            <div class="flex gap-2 flex-wrap">
              <button 
                v-for="amount in [100, 500, 1000, 5000]" 
                :key="amount"
                @click="requestAmount = amount"
                class="px-4 py-2 glass rounded-xl text-sm text-white hover:bg-white/10 transition-colors"
                :class="{ 'bg-primary-500/30 ring-2 ring-primary-500': requestAmount === amount }"
              >
                {{ amount.toLocaleString() }} Token
              </button>
            </div>

            <!-- Price Info -->
            <div class="glass-light rounded-xl p-4">
              <div class="flex justify-between items-center">
                <span class="text-dark-400">ราคาที่ต้องชำระ</span>
                <span class="text-2xl font-bold text-green-400">฿{{ requestAmount?.toLocaleString() || 0 }}</span>
              </div>
              <p class="text-dark-500 text-xs mt-2">* อัตรา 1 Token = 1 บาท</p>
            </div>

            <!-- Submit Button -->
            <button 
              @click="submitRequest"
              :disabled="!requestAmount || requestAmount < 1 || isLoading"
              class="btn-primary w-full py-4 text-lg font-bold disabled:opacity-50"
            >
              {{ isLoading ? '⏳ กำลังส่งคำขอ...' : '📤 ส่งคำขอเติม Token' }}
            </button>

            <p class="text-dark-500 text-xs text-center">
              หลังจากส่งคำขอ Admin จะตรวจสอบและอนุมัติให้ภายใน 24 ชั่วโมง
            </p>
          </div>
        </div>

        <!-- Request History -->
        <div class="card p-6">
          <h2 class="text-xl font-semibold text-white mb-6">📜 ประวัติคำขอ</h2>
          
          <div v-if="requests.length" class="space-y-3 max-h-96 overflow-y-auto pr-2">
            <div 
              v-for="req in requests" 
              :key="req.id"
              class="glass-light rounded-xl p-4"
            >
              <div class="flex items-center justify-between mb-2">
                <span class="text-white font-bold">{{ req.amount.toLocaleString() }} Token</span>
                <span 
                  class="badge"
                  :class="{
                    'badge-warning': req.status === 'pending',
                    'badge-success': req.status === 'approved',
                    'badge-error': req.status === 'rejected'
                  }"
                >
                  {{ statusLabels[req.status] }}
                </span>
              </div>
              <p class="text-dark-500 text-xs">{{ req.created_at }}</p>
              <p v-if="req.admin_note" class="text-dark-400 text-sm mt-2 italic">
                💬 {{ req.admin_note }}
              </p>
            </div>
          </div>

          <div v-else class="text-center py-8">
            <div class="w-16 h-16 rounded-full bg-dark-800 mx-auto mb-3 flex items-center justify-center text-3xl">📋</div>
            <p class="text-dark-400">ยังไม่มีประวัติคำขอ</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const tokenBalance = ref(0);
const requestAmount = ref(100);
const requests = ref([]);
const isLoading = ref(false);

const baseUrl = 'http://localhost:5000';

const statusLabels = {
  pending: '⏳ รอตรวจสอบ',
  approved: '✅ อนุมัติแล้ว',
  rejected: '❌ ปฏิเสธ'
};

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

async function submitRequest() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('กรุณาเข้าสู่ระบบก่อน');
    return;
  }
  
  if (!requestAmount.value || requestAmount.value < 1) {
    alert('กรุณาระบุจำนวน Token');
    return;
  }
  
  isLoading.value = true;
  try {
    await axios.post(`${baseUrl}/api/token/request`, {
      amount: requestAmount.value
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    alert('🎉 ส่งคำขอเติม Token สำเร็จ! รอการอนุมัติจาก Admin');
    requestAmount.value = 100;
    fetchRequests();
  } catch (err) {
    alert(err.response?.data?.msg || 'ส่งคำขอไม่สำเร็จ');
  } finally {
    isLoading.value = false;
  }
}

onMounted(() => {
  fetchTokenBalance();
  fetchRequests();
});
</script>

<style scoped>
.badge-warning {
  background-color: rgba(234, 179, 8, 0.2);
  color: #facc15;
}
.badge-success {
  background-color: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}
.badge-error {
  background-color: rgba(239, 68, 68, 0.2);
  color: #f87171;
}
</style>
