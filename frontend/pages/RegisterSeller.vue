<template>
  <div class="flex justify-center items-center min-h-screen bg-gradient-to-br from-gray-900 to-black p-4">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-lg">
      
      <!-- Stage 1: Seller Registration Form -->
      <div v-if="currentStage === 1">
        <h1 class="text-2xl font-bold text-white text-center mb-6">Register as Seller</h1>
        
        <input v-model="shopName" placeholder="ชื่อร้านค้า" class="mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white" />
        <input v-model="phoneNumber" placeholder="เบอร์โทรศัพท์" class="mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white" />

        <input v-model="addressLine" placeholder="ที่อยู่" class="mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white" />
        <input v-model="district" placeholder="อำเภอ/เขต" class="mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white" />
        <input v-model="province" placeholder="จังหวัด" class="mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white" />
        <input v-model="postalCode" placeholder="รหัสไปรษณีย์" class="mb-3 p-3 w-full rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-white focus:border-white" />

        <button
          @click="handleRegisterSeller"
          :disabled="isLoading"
          class="bg-black hover:bg-gray-700 text-white font-semibold py-2 w-full rounded-lg transition duration-200 border border-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:border-white disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading">กำลังลงทะเบียน...</span>
          <span v-else>ลงทะเบียนเป็นผู้ขาย</span>
        </button>

        <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center">{{ errorMsg }}</p>
        <p v-if="successMsg" class="text-green-400 text-sm mt-4 text-center">{{ successMsg }}</p>

        <div class="text-center text-sm text-gray-400 mt-4">
          กลับไปยัง
          <router-link to="/profile" class="underline hover:text-white">โปรไฟล์</router-link>
        </div>
      </div>
      
      <!-- Stage 2: eKYC Verification Form -->
      <div v-if="currentStage === 2">
        <h1 class="text-3xl font-bold text-white text-center mb-6">eKYC Verification</h1>
        <p class="text-center text-gray-400 mb-6">
          โปรดอัปโหลดภาพบัตรประชาชนและเซลฟี่เพื่อยืนยันตัวตน และรับ Trust Badge 💎
        </p>

        <!-- ID Card Upload Section -->
        <div class="mb-6">
          <label class="block text-gray-300 text-sm font-semibold mb-2">อัปโหลดบัตรประชาชน</label>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label for="idFront" class="block text-white text-sm font-light mb-1">ด้านหน้าบัตร</label>
              <input type="file" id="idFront" @change="handleFileUpload($event, 'idFront')" class="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100" />
              <div v-if="idFrontUrl" class="mt-2 w-full h-auto rounded-lg overflow-hidden border border-gray-700">
                <img :src="idFrontUrl" alt="ID Card Front" class="object-cover w-full h-auto" />
              </div>
            </div>
            <div>
              <label for="idBack" class="block text-white text-sm font-light mb-1">ด้านหลังบัตร</label>
              <input type="file" id="idBack" @change="handleFileUpload($event, 'idBack')" class="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100" />
              <div v-if="idBackUrl" class="mt-2 w-full h-auto rounded-lg overflow-hidden border border-gray-700">
                <img :src="idBackUrl" alt="ID Card Back" class="object-cover w-full h-auto" />
              </div>
            </div>
          </div>
        </div>

        <!-- Selfie Upload Section -->
        <div class="mb-6">
          <label for="selfie" class="block text-gray-300 text-sm font-semibold mb-2">อัปโหลดเซลฟี่</label>
          <input type="file" id="selfie" @change="handleFileUpload($event, 'selfie')" class="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-violet-50 file:text-violet-700 hover:file:bg-violet-100" />
          <div v-if="selfieUrl" class="mt-2 w-full h-auto rounded-lg overflow-hidden border border-gray-700">
            <img :src="selfieUrl" alt="Selfie" class="object-cover w-full h-auto" />
          </div>
        </div>

        <!-- Submit Button & Messages -->
        <button @click="handleEkycVerification"
          :disabled="isLoading"
          class="bg-black text-white font-semibold py-3 w-full rounded-lg transition duration-200 border border-white/10 focus:outline-none focus:ring-2 focus:ring-white focus:border-white disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-700">
          <span v-if="isLoading">กำลังดำเนินการ...</span>
          <span v-else>ยืนยันตัวตน</span>
        </button>

        <p v-if="errorMsg" class="text-red-400 text-sm mt-4 text-center">{{ errorMsg }}</p>
        <p v-if="successMsg" class="text-green-400 text-sm mt-4 text-center">{{ successMsg }}</p>
        
        <div class="text-center text-sm text-gray-400 mt-4">
          กลับไปยัง
          <router-link to="/profile" class="underline hover:text-white">โปรไฟล์</router-link>
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

// General state
const currentStage = ref(1); // 1: Registration, 2: eKYC
const isLoading = ref(false);
const errorMsg = ref('');
const successMsg = ref('');

// Data for seller registration (Stage 1)
const shopName = ref('');
const phoneNumber = ref('');
const addressPhone = ref('');
const addressLine = ref('');
const district = ref('');
const province = ref('');
const postalCode = ref('');

// Data for eKYC verification (Stage 2)
const idFront = ref(null);
const idBack = ref(null);
const selfie = ref(null);
const idFrontUrl = ref('');
const idBackUrl = ref('');
const selfieUrl = ref('');

// --- Stage 1: Seller Registration Logic ---
const handleRegisterSeller = async () => {
  errorMsg.value = '';
  successMsg.value = '';
  isLoading.value = true;

  if (!shopName.value || !addressLine.value) {
    errorMsg.value = 'กรุณากรอกข้อมูลที่จำเป็นให้ครบถ้วน';
    isLoading.value = false;
    return;
  }
  
  const token = localStorage.getItem('token');
  if (!token) {
    errorMsg.value = 'User not authenticated. Please log in first.';
    isLoading.value = false;
    return;
  }

  try {
    const res = await axios.post('http://localhost:5000/api/register-seller', {
      shop_name: shopName.value,
      phone_number: phoneNumber.value,
      address_phone: addressPhone.value,
      address_line: addressLine.value,
      district: district.value,
      province: province.value,
      postal_code: postalCode.value,
    }, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    successMsg.value = res.data.msg || 'การลงทะเบียนผู้ขายสำเร็จแล้ว กรุณาดำเนินการยืนยันตัวตน';
    
    const storedUser = JSON.parse(localStorage.getItem('user') || '{}');
    storedUser.is_seller = true;
    localStorage.setItem('user', JSON.stringify(storedUser));
    
    // Move to the next stage: eKYC verification
    setTimeout(() => {
      currentStage.value = 2;
      successMsg.value = '';
    }, 1500);
    
  } catch (err) {
    console.error('[Register Seller Error]', err);
    errorMsg.value = err.response?.data?.msg || 'การลงทะเบียนผู้ขายล้มเหลว';
  } finally {
    isLoading.value = false;
  }
};

// --- Stage 2: eKYC Verification Logic ---
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

const handleEkycVerification = async () => {
  errorMsg.value = '';
  successMsg.value = '';
  isLoading.value = true;

  if (!idFront.value || !idBack.value || !selfie.value) {
    errorMsg.value = 'กรุณาอัปโหลดภาพบัตรประชาชนทั้งด้านหน้าและด้านหลัง พร้อมด้วยภาพเซลฟี่';
    isLoading.value = false;
    return;
  }

  const token = localStorage.getItem('token');
  if (!token) {
    errorMsg.value = 'User not authenticated. Please log in first.';
    isLoading.value = false;
    return;
  }

  const formData = new FormData();
  formData.append('id_front_image', idFront.value);
  formData.append('id_back_image', idBack.value);
  formData.append('selfie_image', selfie.value);

  try {
    // This is a placeholder API call. You need to create this endpoint on your backend.
    const res = await axios.post('http://localhost:5000/api/verify-ekyc', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Authorization: `Bearer ${token}`
      }
    });

    successMsg.value = res.data.msg || 'การยืนยันตัวตนสำเร็จแล้ว! คุณได้รับ Trust Badge';
    
    const storedUser = JSON.parse(localStorage.getItem('user') || '{}');
    storedUser.is_seller_verified = true;
    localStorage.setItem('user', JSON.stringify(storedUser));
    
    // Use Vue Router to navigate to the profile page
    setTimeout(() => router.push('/profile'), 2000);
    
  } catch (err) {
    console.error('[eKYC Verification Error]', err);
    errorMsg.value = err.response?.data?.msg || 'การยืนยันตัวตนล้มเหลว. กรุณาลองใหม่อีกครั้ง.';
  } finally {
    isLoading.value = false;
  }
};

</script>

