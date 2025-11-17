<template>
  <div class="flex min-h-screen bg-gray-900 text-white">
    <!-- Left Side: Upload Section -->
    <main class="flex-1 p-8">
      <div class="border-2 rounded-lg p-8 bg-gray-800 shadow-xl">
        <h2 class="text-2xl font-bold mb-6 text-center">อัปโหลดภาพสินค้า</h2>

        <!-- Upload controls -->
        <div class="flex flex-col items-center">
          <label for="image" class="mb-4 text-lg font-semibold">
            เลือกไฟล์ภาพ
          </label>
          
          <input 
            type="file" 
            id="image"
            accept="image/*" 
            class="mb-4 p-3 bg-gray-700 text-white rounded-md cursor-pointer"
            @change="previewImage"
            :disabled="loading"
          />
          
          <button 
            @click="handleSubmit"
            class="px-6 py-3 bg-indigo-500 text-white font-semibold rounded-lg hover:bg-indigo-400 transition disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="loading || !selectedImage"
          >
            {{ loading ? 'กำลังประมวลผล...' : 'อัปโหลด' }}
          </button>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="mt-4 p-3 bg-red-600 text-white rounded-md text-center">
          {{ error }}
        </div>

        <!-- Image Preview -->
        <div v-if="imagePreview" class="mt-6">
          <h3 class="text-xl font-semibold mb-3 text-center">ภาพที่อัปโหลด:</h3>
          <img :src="imagePreview" alt="Image Preview" class="w-full max-w-md mx-auto rounded-md shadow-lg" />
        </div>
      </div>
    </main>

    <!-- Right Side: Data Display -->
    <div class="bg-gray-800 h-full w-1/3 max-w-xs p-8 m-6 mt-8 border-4 border-pink-500 flex flex-col overflow-auto">
      <h3 class="text-xl font-semibold mb-4">ข้อมูลสินค้า</h3>

      <div v-if="loading" class="flex flex-col items-center justify-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-pink-500 mb-4"></div>
        <p class="text-gray-400">กำลังวิเคราะห์ภาพ...</p>
      </div>
      
      <div v-else-if="productData && productData.success" class="space-y-4">
        <!-- Success indicator -->
        <div class="bg-green-900 bg-opacity-30 border border-green-500 rounded-lg p-3 flex items-center">
          <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
          </svg>
          <span class="text-green-400 text-sm font-semibold">วิเคราะห์สำเร็จ</span>
        </div>

        <!-- Product analysis -->
        <div class="bg-gray-700 rounded-lg p-4">
          <h4 class="text-pink-400 font-bold mb-3 flex items-center">
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z"/>
              <path fill-rule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clip-rule="evenodd"/>
            </svg>
            รายละเอียดและการประเมินราคา
          </h4>
          <div class="text-sm text-gray-200 whitespace-pre-line leading-relaxed">
            {{ productData.productData }}
          </div>
        </div>

        <!-- Summary info -->
        <div v-if="productData.summary" class="bg-gray-700 rounded-lg p-3 text-sm">
          <div class="flex items-center text-gray-400">
            <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>
            {{ productData.summary }}
          </div>
        </div>

        <!-- Timestamp -->
        <div v-if="productData.timestamp" class="text-xs text-gray-500 text-center">
          {{ new Date(productData.timestamp).toLocaleString('th-TH') }}
        </div>
      </div>
      
      <div v-else class="flex flex-col items-center justify-center py-12 text-center">
        <svg class="w-16 h-16 text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/>
        </svg>
        <p class="text-gray-400 mb-2">กรุณาอัปโหลดภาพสินค้า</p>
        <p class="text-gray-500 text-sm">เพื่อรับการวิเคราะห์และประเมินราคา</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Declare reactive variables
const imagePreview = ref(null);
const selectedImage = ref(null);
const productData = ref(null);
const loading = ref(false);
const error = ref(null);

// Handle image preview
const previewImage = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedImage.value = file;
    const reader = new FileReader();
    reader.onload = () => {
      imagePreview.value = reader.result;
    };
    reader.readAsDataURL(file);
  }
};

// Handle form submission
const handleSubmit = async () => {
  if (!selectedImage.value) {
    error.value = 'กรุณาเลือกไฟล์ภาพ';
    return;
  }

  loading.value = true;
  error.value = null;
  productData.value = null; // Clear previous data

  const formData = new FormData();
  formData.append('productImage', selectedImage.value);

  try {
    // Step 1: Upload to n8n
    console.log('📤 Uploading to n8n...');
    const n8nResponse = await fetch('http://localhost:5678/webhook/upload-image', {
      method: 'POST',
      body: formData,
    });

    if (!n8nResponse.ok) {
      throw new Error('เกิดข้อผิดพลาดในการอัปโหลดไปยัง n8n');
    }

    const n8nResult = await n8nResponse.json();
    console.log('✅ n8n result:', n8nResult);
    console.log('🔍 n8n result type:', typeof n8nResult);
    console.log('🔍 n8n result keys:', Object.keys(n8nResult));

    // Try to find the data in various possible fields
    const extractedData = n8nResult.productData || 
                         n8nResult.text || 
                         n8nResult.data || 
                         n8nResult.result ||
                         JSON.stringify(n8nResult);

    console.log('🔍 Extracted data:', extractedData);

    if (!extractedData) {
      throw new Error('ไม่มีข้อมูลจาก n8n');
    }

    // Step 2: Send to internal Nuxt API (use relative path)
    console.log('📤 Sending to API...');
    const apiResponse = await fetch('/api/ai', {  // Changed: Use internal API
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ productDetails: extractedData }),
    });

    if (!apiResponse.ok) {
      const errorText = await apiResponse.text();
      console.error('API Error Response:', errorText);
      throw new Error(`เกิดข้อผิดพลาดในการส่งข้อมูลไปยัง API: ${apiResponse.status}`);
    }

    const apiResult = await apiResponse.json();
    console.log('✅ API Response:', apiResult);
    console.log('🔍 API Response type:', typeof apiResult);
    console.log('🔍 API Response keys:', Object.keys(apiResult));
    console.log('🔍 productData field exists?', 'productData' in apiResult);
    console.log('🔍 productData value:', apiResult.productData);

    // Store the result
    productData.value = apiResult;
    
    // Force update check
    console.log('🔍 Vue productData after setting:', productData.value);
    console.log('🔍 Vue productData is null?', productData.value === null);
  } catch (err) {
    console.error('❌ Error:', err);
    error.value = err.message || 'เกิดข้อผิดพลาดในการประมวลผล';
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.upload-container {
  text-align: center;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  border-radius: 10px;
  background-color: #2d2d2d;
}

.title {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #fff;
}

.upload-form {
  display: inline-block;
  padding: 20px;
  border-radius: 8px;
}

.file-input {
  padding: 10px;
  margin-bottom: 15px;
  background-color: #444;
  color: white;
  border-radius: 8px;
  cursor: pointer;
}

.upload-btn {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
}

.upload-btn:hover {
  background-color: #45a049;
}

.image-preview {
  margin-top: 20px;
}

.preview-img {
  width: 200px;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>

