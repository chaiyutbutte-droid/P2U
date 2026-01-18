<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-pink-500/30 relative overflow-hidden flex items-center justify-center p-4">
    
    <div class="fixed top-0 left-0 w-[600px] h-[600px] bg-purple-900/20 blur-[120px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[800px] h-[600px] bg-pink-900/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

    <div class="relative z-10 w-full max-w-2xl">
      
      <div class="text-center mb-8">
        <h1 class="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-pink-200 to-purple-200">
          Partner Registration
        </h1>
        <p class="text-gray-400 mt-2 text-sm">สมัครเป็นผู้ขายและยืนยันตัวตนเพื่อเริ่มสร้างรายได้</p>
      </div>

      <div class="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-6 md:p-10 shadow-2xl relative overflow-hidden">
        
        <div class="flex items-center justify-center mb-10 relative">
          <div class="absolute w-full h-0.5 bg-white/10 top-1/2 -translate-y-1/2 z-0 max-w-xs mx-auto"></div>
          
          <div class="flex items-center gap-2 relative z-10">
            <div class="flex flex-col items-center gap-2">
              <div class="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold border-2 transition-all duration-300"
                   :class="currentStage >= 1 ? 'bg-pink-500 border-pink-500 text-white shadow-[0_0_15px_rgba(236,72,153,0.5)]' : 'bg-[#15151a] border-white/20 text-gray-500'">
                1
              </div>
              <span class="text-xs font-medium" :class="currentStage >= 1 ? 'text-pink-400' : 'text-gray-500'">ข้อมูลร้านค้า</span>
            </div>

            <div class="w-24"></div> 

            <div class="flex flex-col items-center gap-2">
              <div class="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold border-2 transition-all duration-300"
                   :class="currentStage >= 2 ? 'bg-purple-500 border-purple-500 text-white shadow-[0_0_15px_rgba(168,85,247,0.5)]' : 'bg-[#15151a] border-white/20 text-gray-500'">
                2
              </div>
              <span class="text-xs font-medium" :class="currentStage >= 2 ? 'text-purple-400' : 'text-gray-500'">ยืนยันตัวตน</span>
            </div>
          </div>
        </div>

        <Transition name="fade" mode="out-in">
          
          <div v-if="currentStage === 1" key="stage1">
            <h2 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
              🏪 ตั้งค่าร้านค้าของคุณ
            </h2>
            
            <div class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="group">
                  <label class="text-xs text-gray-400 mb-1 block ml-1">ชื่อร้านค้า</label>
                  <input v-model="shopName" type="text" placeholder="ระบุชื่อร้านสุดเท่" :class="inputClass" />
                </div>
                <div class="group">
                  <label class="text-xs text-gray-400 mb-1 block ml-1">เบอร์โทรศัพท์</label>
                  <input v-model="phoneNumber" type="tel" placeholder="08x-xxx-xxxx" :class="inputClass" />
                </div>
              </div>

              <div class="group">
                <label class="text-xs text-gray-400 mb-1 block ml-1">เลขบัตรประชาชน (13 หลัก)</label>
                <input v-model="idCardNumber" type="text" maxlength="13" placeholder="x-xxxx-xxxxx-xx-x" :class="inputClass" />
              </div>

              <div class="group">
                <label class="text-xs text-gray-400 mb-1 block ml-1">ที่อยู่</label>
                <input v-model="addressLine" type="text" placeholder="บ้านเลขที่, ซอย, ถนน" :class="inputClass" />
              </div>

              <div class="grid grid-cols-2 gap-4">
                <div class="group">
                  <label class="text-xs text-gray-400 mb-1 block ml-1">เขต/อำเภอ</label>
                  <input v-model="district" type="text" placeholder="เขต..." :class="inputClass" />
                </div>
                <div class="group">
                  <label class="text-xs text-gray-400 mb-1 block ml-1">จังหวัด</label>
                  <input v-model="province" type="text" placeholder="จังหวัด..." :class="inputClass" />
                </div>
              </div>

              <div class="group">
                <label class="text-xs text-gray-400 mb-1 block ml-1">รหัสไปรษณีย์</label>
                <input v-model="postalCode" type="text" placeholder="xxxxx" :class="inputClass" class="md:w-1/2" />
              </div>
            </div>

            <div class="mt-8">
              <button
                @click="handleNextStep"
                class="w-full py-3.5 rounded-xl font-bold text-white shadow-lg bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 transform hover:scale-[1.02] active:scale-[0.98] transition-all flex items-center justify-center gap-2"
              >
                <span>ถัดไป: ยืนยันตัวตน ➜</span>
              </button>
            </div>
          </div>
          
          <div v-else-if="currentStage === 2" key="stage2">
            <div class="text-center mb-6">
              <h2 class="text-2xl font-bold text-white mb-2">eKYC Verification 🛡️</h2>
              <p class="text-sm text-gray-400">
                แนบหลักฐานเพื่อส่งให้ Admin ตรวจสอบ
              </p>
            </div>

            <div class="mb-6">
              <label class="block text-white text-sm font-semibold mb-3 border-l-4 border-pink-500 pl-3">1. ภาพถ่ายบัตรประชาชน</label>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div @click="triggerFileInput('idFront')" :class="[uploadBoxClass, idFrontUrl ? 'border-solid border-green-500/50 bg-black' : '']">
                  <input type="file" ref="fileInputFront" class="hidden" @change="handleFileUpload($event, 'idFront')" accept="image/*" />
                  <img v-if="idFrontUrl" :src="idFrontUrl" class="w-full h-full object-cover" />
                  <div v-else class="flex flex-col items-center justify-center">
                    <span class="text-2xl mb-2">🪪</span>
                    <span class="text-sm font-medium text-gray-300">ด้านหน้าบัตร</span>
                  </div>
                </div>

                <div @click="triggerFileInput('idBack')" :class="[uploadBoxClass, idBackUrl ? 'border-solid border-green-500/50 bg-black' : '']">
                  <input type="file" ref="fileInputBack" class="hidden" @change="handleFileUpload($event, 'idBack')" accept="image/*" />
                  <img v-if="idBackUrl" :src="idBackUrl" class="w-full h-full object-cover" />
                  <div v-else class="flex flex-col items-center justify-center">
                    <span class="text-2xl mb-2">🔙</span>
                    <span class="text-sm font-medium text-gray-300">ด้านหลังบัตร</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="mb-8">
              <label class="block text-white text-sm font-semibold mb-3 border-l-4 border-purple-500 pl-3">2. ภาพเซลฟี่คู่กับบัตร</label>
              <div class="w-full h-48 md:h-56" @click="triggerFileInput('selfie')" :class="[uploadBoxClass, selfieUrl ? 'border-solid border-green-500/50 bg-black' : '']">
                 <input type="file" ref="fileInputSelfie" class="hidden" @change="handleFileUpload($event, 'selfie')" accept="image/*" />
                  <img v-if="selfieUrl" :src="selfieUrl" class="w-full h-full object-cover" />
                  <div v-else class="flex flex-col items-center justify-center">
                    <span class="text-4xl mb-2">🤳</span>
                    <span class="text-sm font-medium text-gray-300">ถ่ายเซลฟี่หน้าตรง</span>
                  </div>
              </div>
            </div>
            
            <div class="flex gap-4">
               <button @click="currentStage = 1" class="w-1/3 py-3.5 rounded-xl font-bold text-gray-300 bg-white/5 hover:bg-white/10 transition-all">
                  ⬅ ย้อนกลับ
               </button>

               <button @click="handleFinalSubmission"
                 :disabled="isLoading"
                 class="w-2/3 py-3.5 rounded-xl font-bold text-white shadow-lg bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 transform hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2">
                 <span v-if="isLoading" class="animate-spin">🔄</span>
                 <span v-else>ส่งใบสมัครให้ตรวจสอบ</span>
               </button>
            </div>

          </div>

        </Transition>

        <div v-if="errorMsg" class="mt-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-center animate-pulse">
          ⚠️ {{ errorMsg }}
        </div>
        <div v-if="successMsg" class="mt-4 p-3 rounded-lg bg-green-500/10 border border-green-500/20 text-green-400 text-sm text-center">
          ✅ {{ successMsg }}
        </div>

        <div class="text-center mt-6 pt-6 border-t border-white/5">
          <router-link to="/profile" class="text-gray-500 hover:text-white text-sm transition-colors flex items-center justify-center gap-1">
            <span>←</span> ยกเลิกและกลับไปหน้าโปรไฟล์
          </router-link>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

// CSS Classes
const inputClass = "w-full bg-[#15151a] border border-white/10 rounded-xl px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-pink-500 focus:ring-1 focus:ring-pink-500 transition-all duration-300";
const uploadBoxClass = "relative h-40 rounded-xl border-2 border-dashed border-white/20 bg-white/5 hover:bg-white/10 hover:border-pink-400 transition-all cursor-pointer overflow-hidden flex items-center justify-center text-center";

// State
const currentStage = ref(1); 
const isLoading = ref(false);
const errorMsg = ref('');
const successMsg = ref('');

// Form Data (Text)
const shopName = ref('');
const phoneNumber = ref('');
const idCardNumber = ref(''); // ✅ เพิ่ม state เลขบัตร
const addressLine = ref('');
const district = ref('');
const province = ref('');
const postalCode = ref('');

// Form Data (Files)
const fileInputFront = ref(null);
const fileInputBack = ref(null);
const fileInputSelfie = ref(null);
const idFront = ref(null);
const idBack = ref(null);
const selfie = ref(null);
const idFrontUrl = ref('');
const idBackUrl = ref('');
const selfieUrl = ref('');

const triggerFileInput = (type) => {
    if (type === 'idFront') fileInputFront.value.click();
    if (type === 'idBack') fileInputBack.value.click();
    if (type === 'selfie') fileInputSelfie.value.click();
};

const handleFileUpload = (event, type) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      if (type === 'idFront') {
        idFront.value = file;
        idFrontUrl.value = e.target.result;
      } else if (type === 'idBack') {
        idBack.value = file;
        idBackUrl.value = e.target.result;
      } else if (type === 'selfie') {
        selfie.value = file;
        selfieUrl.value = e.target.result;
      }
    };
    reader.readAsDataURL(file);
  }
};

// --- Logic ---

// Step 1: แค่ตรวจสอบข้อมูลเบื้องต้น แล้วไปหน้า 2 (ยังไม่ส่ง API)
const handleNextStep = () => {
  errorMsg.value = '';
  
  if (!shopName.value || !addressLine.value || !phoneNumber.value || !idCardNumber.value) { // ✅ เช็ค idCardNumber ด้วย
    errorMsg.value = 'กรุณากรอกข้อมูลที่จำเป็นให้ครบถ้วน';
    return;
  }
  
  // ผ่านแล้ว ไปหน้าอัปโหลดรูป
  currentStage.value = 2;
};

// Step 2: รวมร่างข้อมูลทั้งหมด แล้วส่ง API ทีเดียว
const handleFinalSubmission = async () => {
  errorMsg.value = '';
  successMsg.value = '';
  isLoading.value = true;

  // ตรวจสอบว่ามีรูปครบไหม
  if (!idFront.value || !idBack.value || !selfie.value) {
    errorMsg.value = 'กรุณาอัปโหลดภาพหลักฐานให้ครบทั้ง 3 รายการ';
    isLoading.value = false;
    return;
  }

  const token = localStorage.getItem('token');
  if (!token) {
     errorMsg.value = 'ไม่พบข้อมูลผู้ใช้ กรุณาเข้าสู่ระบบใหม่';
     isLoading.value = false;
     return;
  }

  // เตรียม FormData รวมทุกอย่าง
  const formData = new FormData();
  
  // 1. ข้อมูลร้านค้า (Text)
  formData.append('shop_name', shopName.value);
  formData.append('phone_number', phoneNumber.value);
  formData.append('id_card_number', idCardNumber.value); // ✅ ส่งเลขบัตรไปที่ API
  formData.append('address_line', addressLine.value);
  formData.append('district', district.value);
  formData.append('province', province.value);
  formData.append('postal_code', postalCode.value);
  
  // 2. ข้อมูลรูปภาพ (Files)
  formData.append('id_front_image', idFront.value);
  formData.append('id_back_image', idBack.value);
  formData.append('selfie_image', selfie.value);

  try {
    // ยิงไปที่ Endpoint เดียว (เช่น /api/seller-application)
    // Backend ต้องเขียนรับทั้ง body และ files
    await axios.post('http://localhost:5000/api/register-seller-application', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${token}`
      }
    });

    successMsg.value = 'ส่งใบสมัครเรียบร้อย! กรุณารอแอดมินตรวจสอบ (24 ชม.)';
    
    // Redirect กลับไป Profile หลังจาก 2 วินาที
    setTimeout(() => {
        router.push('/profile');
    }, 2000);

  } catch (err) {
    console.error(err);
    errorMsg.value = err.response?.data?.msg || 'เกิดข้อผิดพลาดในการส่งข้อมูล';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>