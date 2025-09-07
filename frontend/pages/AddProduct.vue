<template>
  <div class="flex justify-center min-h-screen bg-gradient-to-br from-gray-900 to-black p-6">
    <div class="bg-gray-800 p-8 rounded-xl shadow-xl w-full max-w-lg text-white">
      <h1 class="text-2xl font-bold mb-6">Add New Product</h1>

      <form @submit.prevent="submitProduct" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">Product Name</label>
          <input v-model="name" type="text" required class="w-full p-2 rounded bg-gray-700 border border-gray-600" />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Price</label>
          <input v-model="price" type="number" required class="w-full p-2 rounded bg-gray-700 border border-gray-600" />
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Description</label>
          <textarea v-model="description" class="w-full p-2 rounded bg-gray-700 border border-gray-600"></textarea>
        </div>

        <div>
          <label class="block text-sm font-medium mb-1">Product Image</label>
          <input type="file" @change="handleFileUpload" class="w-full text-gray-300" />
        </div>

        <button type="submit" class="w-full py-2 bg-indigo-600 hover:bg-indigo-700 rounded-lg font-semibold">
          Save Product
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

const router = useRouter();
const baseURL = "http://localhost:5000";

const name = ref("");
const price = ref("");
const description = ref("");
const imageFile = ref(null);

const handleFileUpload = (event) => {
  imageFile.value = event.target.files[0];
};

const submitProduct = async () => {
  const token = localStorage.getItem("token");
  if (!token) {
    router.push("/login");
    return;
  }

  const formData = new FormData();
  formData.append("name", name.value);
  formData.append("price", price.value);
  formData.append("description", description.value);
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
    alert("Product added successfully!");
    router.push("/seller"); // 🔹 กลับไปหน้ารายการสินค้า
  } catch (err) {
    console.error("Failed to add product:", err);
    alert("Failed to add product.");
  }
};
</script>
