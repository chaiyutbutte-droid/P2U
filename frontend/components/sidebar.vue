<template>
  <div
    @mouseenter="expand = true"
    @mouseleave="expand = false"
    class="fixed left-0 top-0 h-screen bg-gray-900 text-white shadow-lg flex flex-col transition-all duration-300 z-50"
    :class="expand ? 'w-64' : 'w-20'"
  >
    <!-- Logo -->
    <div class="flex items-center justify-center h-16 border-b border-gray-700">
      <span class="text-white transition-colors duration-300">P2U</span>
      <span v-if="expand" class="ml-2 text-xl font-semibold whitespace-nowrap text-pink-500">KAISER</span>
    </div>

    <!-- เมนู -->
    <nav class="flex-1 flex flex-col p-2">
      <!-- Profile ด้านบน -->
      <div
        v-for="item in topMenuItems"
        :key="item.name"
        @click="navigate(item.route)"
        class="flex items-center p-3 rounded-lg hover:bg-gray-800 cursor-pointer transition-all duration-200"
      >
        <span class="text-xl w-6 text-center">{{ item.icon }}</span>
        <span v-if="expand" class="ml-3 text-sm font-medium">{{ item.name }}</span>
      </div>

      <!-- Settings ด้านล่างสุด -->
      <div class="mt-auto">
        <div
          v-for="item in bottomMenuItems"
          :key="item.name"
          @click="navigate(item.route)"
          class="flex items-center p-3 rounded-lg hover:bg-gray-800 cursor-pointer transition-all duration-200"
        >
          <span class="text-xl w-6 text-center">{{ item.icon }}</span>
          <span v-if="expand" class="ml-3 text-sm font-medium">{{ item.name }}</span>
        </div>

        <!-- Logout -->
        <div
          class="flex items-center hover:bg-red-600 bg-red-500 rounded-lg p-2 cursor-pointer transition-all mt-2"
          @click="logout"
        >
          <span class="text-xl w-6 text-center">🚪</span>
          <span v-if="expand" class="ml-2">ออกจากระบบ</span>
        </div>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const expand = ref(false)
const router = useRouter()

// เมนูด้านบน
const topMenuItems = [
  { name: 'Profile', icon: '👤', route: '/profile' },
]

// เมนูด้านล่าง (อยู่ติดล่างสุดของ sidebar)
const bottomMenuItems = [
  { name: 'Settings', icon: '⚙️', route: '/settings' },
]

function navigate(route) {
  router.push(route)
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  localStorage.removeItem('cart')
  router.push('/login')
}
</script>
