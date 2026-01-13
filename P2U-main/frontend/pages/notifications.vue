<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />
    
    <div class="max-w-2xl mx-auto">
      <!-- Header -->
      <div class="flex items-center justify-between mb-6">
        <div>
          <h1 class="text-2xl font-bold text-white flex items-center gap-2">
            🔔 การแจ้งเตือน
          </h1>
          <p class="text-dark-400 mt-1">{{ unreadCount }} รายการที่ยังไม่ได้อ่าน</p>
        </div>
        <div class="flex gap-2">
          <button @click="markAllAsRead" class="btn-glass text-sm" :disabled="unreadCount === 0">
            ✓ อ่านทั้งหมด
          </button>
          <button @click="clearAll" class="btn-glass text-red-400 text-sm" :disabled="notifications.length === 0">
            🗑️ ล้างทั้งหมด
          </button>
        </div>
      </div>

      <!-- Notifications List -->
      <div v-if="notifications.length" class="space-y-3">
        <div 
          v-for="notif in notifications" 
          :key="notif.id" 
          class="card p-4 transition-all hover:shadow-glow-sm cursor-pointer"
          :class="{ 'border-l-4 border-primary-500': !notif.is_read }"
          @click="handleNotifClick(notif)"
        >
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl flex items-center justify-center text-2xl" :class="getTypeClass(notif.type)">
              {{ getTypeIcon(notif.type) }}
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-2">
                <h3 class="font-medium text-white" :class="{ 'font-semibold': !notif.is_read }">
                  {{ notif.title }}
                </h3>
                <button @click.stop="deleteNotif(notif)" class="text-dark-500 hover:text-red-400 transition-colors">
                  ✕
                </button>
              </div>
              <p class="text-dark-400 text-sm mt-1">{{ notif.message }}</p>
              <p class="text-dark-500 text-xs mt-2">{{ notif.created_at }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="card p-12 text-center">
        <div class="w-20 h-20 rounded-full bg-dark-700 mx-auto mb-4 flex items-center justify-center text-4xl">
          🔔
        </div>
        <h3 class="text-lg font-semibold text-white mb-2">ไม่มีการแจ้งเตือน</h3>
        <p class="text-dark-400">เมื่อมีการแจ้งเตือนใหม่ จะแสดงที่นี่</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const notifications = ref([]);

const unreadCount = computed(() => notifications.value.filter(n => !n.is_read).length);

function getTypeIcon(type) {
  const icons = {
    order: '📦',
    review: '⭐',
    promo: '🎉',
    system: '⚙️',
    info: 'ℹ️',
  };
  return icons[type] || 'ℹ️';
}

function getTypeClass(type) {
  const classes = {
    order: 'bg-green-500/20',
    review: 'bg-yellow-500/20',
    promo: 'bg-accent-500/20',
    system: 'bg-dark-700',
    info: 'bg-primary-500/20',
  };
  return classes[type] || 'bg-primary-500/20';
}

async function fetchNotifications() {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    const res = await axios.get('http://localhost:5000/api/notifications', {
      headers: { Authorization: `Bearer ${token}` }
    });
    notifications.value = res.data.notifications || [];
  } catch (err) {
    console.error('Failed to fetch notifications:', err);
  }
}

async function handleNotifClick(notif) {
  if (!notif.is_read) {
    const token = localStorage.getItem('token');
    try {
      await axios.put(`http://localhost:5000/api/notifications/${notif.id}/read`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      notif.is_read = true;
    } catch (err) {
      console.error('Failed to mark as read:', err);
    }
  }
  
  if (notif.link) {
    router.push(notif.link);
  }
}

async function markAllAsRead() {
  const token = localStorage.getItem('token');
  try {
    await axios.put('http://localhost:5000/api/notifications/read-all', {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    notifications.value.forEach(n => n.is_read = true);
  } catch (err) {
    console.error('Failed to mark all as read:', err);
  }
}

async function deleteNotif(notif) {
  const token = localStorage.getItem('token');
  try {
    await axios.delete(`http://localhost:5000/api/notifications/${notif.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    notifications.value = notifications.value.filter(n => n.id !== notif.id);
  } catch (err) {
    console.error('Failed to delete notification:', err);
  }
}

async function clearAll() {
  if (!confirm('ยืนยันการล้างการแจ้งเตือนทั้งหมด?')) return;
  
  const token = localStorage.getItem('token');
  try {
    await axios.delete('http://localhost:5000/api/notifications/clear', {
      headers: { Authorization: `Bearer ${token}` }
    });
    notifications.value = [];
  } catch (err) {
    console.error('Failed to clear notifications:', err);
  }
}

onMounted(fetchNotifications);
</script>
