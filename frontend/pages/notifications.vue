<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-purple-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-0 right-0 w-[600px] h-[600px] bg-purple-600/10 blur-[150px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 left-0 w-[500px] h-[500px] bg-blue-600/5 blur-[120px] rounded-full pointer-events-none z-0"></div>

    <main class="ml-20 relative z-10 p-6 md:p-10 min-h-screen flex justify-center">
      <div class="w-full max-w-3xl animate-in-fade">
        
        <header class="flex items-end justify-between mb-8">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 mb-3">
              <span class="w-1.5 h-1.5 rounded-full bg-purple-400 animate-pulse"></span>
              <span class="text-[10px] font-bold text-purple-300 uppercase tracking-widest">Updates</span>
            </div>
            <h1 class="text-3xl md:text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-purple-100 to-indigo-400 tracking-tight drop-shadow-sm">
              การแจ้งเตือน 🔔
            </h1>
            <p class="text-gray-400 mt-2 text-sm">
              <span class="text-white font-bold">{{ unreadCount }}</span> รายการใหม่ที่ยังไม่ได้อ่าน
            </p>
          </div>

          <div class="flex gap-2">
            <button 
              @click="markAllAsRead" 
              :disabled="unreadCount === 0"
              class="px-4 py-2 rounded-xl text-xs font-bold transition-all border border-white/5 flex items-center gap-2"
              :class="unreadCount > 0 
                ? 'bg-white/5 text-white hover:bg-white/10 hover:border-white/20' 
                : 'opacity-50 cursor-not-allowed text-gray-500'"
            >
              <span>✓</span> อ่านทั้งหมด
            </button>
            
            <button 
              @click="clearAll" 
              :disabled="notifications.length === 0"
              class="px-4 py-2 rounded-xl text-xs font-bold transition-all border border-white/5 flex items-center gap-2"
              :class="notifications.length > 0
                ? 'bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white hover:border-red-500/50' 
                : 'opacity-50 cursor-not-allowed text-gray-500'"
            >
              <span>🗑️</span> ล้าง
            </button>
          </div>
        </header>

        <div v-if="notifications.length" class="space-y-3 relative">
          <div class="absolute left-6 top-4 bottom-4 w-px bg-gradient-to-b from-white/10 via-white/5 to-transparent z-0 hidden md:block"></div>

          <TransitionGroup name="list">
            <div 
              v-for="notif in notifications" 
              :key="notif.id" 
              class="group relative z-10 pl-0 md:pl-12"
              @click="handleNotifClick(notif)"
            >
              <div 
                class="absolute left-[21px] top-6 w-1.5 h-1.5 rounded-full border border-[#0b0b0f] transition-colors duration-300 hidden md:block"
                :class="!notif.is_read ? 'bg-purple-400 shadow-[0_0_10px_rgba(192,132,252,0.8)] scale-125' : 'bg-gray-700'"
              ></div>

              <div 
                class="relative p-5 rounded-[1.5rem] border transition-all duration-300 cursor-pointer overflow-hidden"
                :class="!notif.is_read 
                  ? 'bg-[#18181b]/80 border-purple-500/30 shadow-[0_4px_20px_-5px_rgba(168,85,247,0.15)] hover:border-purple-400/50' 
                  : 'bg-[#121215]/40 border-white/5 hover:bg-[#121215]/80 hover:border-white/10'"
              >
                <div v-if="!notif.is_read" class="absolute top-0 right-0 w-32 h-32 bg-purple-500/10 blur-[40px] rounded-full pointer-events-none -translate-y-1/2 translate-x-1/2"></div>

                <div class="flex items-start gap-4 relative z-10">
                  <div 
                    class="w-12 h-12 rounded-2xl flex items-center justify-center text-xl shrink-0 border border-white/5 shadow-inner"
                    :class="getTypeClass(notif.type)"
                  >
                    {{ getTypeIcon(notif.type) }}
                  </div>

                  <div class="flex-1 min-w-0 pt-0.5">
                    <div class="flex items-start justify-between gap-2">
                      <h3 
                        class="text-sm md:text-base transition-colors pr-6"
                        :class="!notif.is_read ? 'font-bold text-white' : 'font-medium text-gray-400'"
                      >
                        {{ notif.title }}
                      </h3>
                      
                      <button 
                        @click.stop="deleteNotif(notif)" 
                        class="w-6 h-6 rounded-full flex items-center justify-center text-gray-600 hover:bg-red-500 hover:text-white transition-all opacity-0 group-hover:opacity-100 absolute top-0 right-0 md:static"
                        title="ลบการแจ้งเตือนนี้"
                      >
                        ✕
                      </button>
                    </div>

                    <p 
                      class="text-sm mt-1 leading-relaxed line-clamp-2"
                      :class="!notif.is_read ? 'text-gray-300' : 'text-gray-500'"
                    >
                      {{ notif.message }}
                    </p>

                    <div class="flex items-center gap-2 mt-3">
                      <span class="text-[10px] text-gray-600 font-mono bg-white/5 px-2 py-0.5 rounded-md border border-white/5">
                        {{ formatDate(notif.created_at) }}
                      </span>
                      <span v-if="!notif.is_read" class="text-[10px] text-purple-400 font-bold uppercase tracking-wider animate-pulse">New</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </TransitionGroup>
        </div>

        <div v-else class="py-20 text-center animate-in-fade bg-[#121215]/40 rounded-[2.5rem] border border-white/5 border-dashed relative overflow-hidden">
          <div class="absolute inset-0 bg-gradient-to-t from-purple-500/5 to-transparent pointer-events-none"></div>
          
          <div class="w-20 h-20 rounded-full bg-gradient-to-br from-gray-800 to-black mx-auto mb-5 flex items-center justify-center text-4xl shadow-xl border border-white/5">
            💤
          </div>
          <h3 class="text-xl font-bold text-white mb-2">ไม่มีการแจ้งเตือน</h3>
          <p class="text-gray-500 text-sm">พักผ่อนให้สบาย เจ้าหญิงยังไม่มีเรื่องด่วนอะไรเพคะ</p>
        </div>

      </div>
    </main>
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
    alert: '🚨'
  };
  return icons[type] || '🔔';
}

function getTypeClass(type) {
  const classes = {
    order: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20',
    review: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/20',
    promo: 'bg-pink-500/10 text-pink-400 border-pink-500/20',
    system: 'bg-gray-700/30 text-gray-300 border-gray-600/30',
    info: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
    alert: 'bg-red-500/10 text-red-400 border-red-500/20',
  };
  return classes[type] || 'bg-white/5 text-gray-300 border-white/10';
}

const formatDate = (dateStr) => {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now = new Date();
  const diff = (now - date) / 1000; // seconds

  // ถ้าเพิ่งผ่านไปไม่นาน (น้อยกว่า 24 ชม)
  if (diff < 60) return 'เมื่อสักครู่';
  if (diff < 3600) return `${Math.floor(diff / 60)} นาทีที่แล้ว`;
  if (diff < 86400) return `${Math.floor(diff / 3600)} ชั่วโมงที่แล้ว`;

  // ถ้าผ่านไปนานแล้ว
  return date.toLocaleDateString('th-TH', {
    day: 'numeric', month: 'short', year: '2-digit', hour: '2-digit', minute: '2-digit'
  });
};

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

<style scoped>
/* Page Entrance */
.animate-in-fade {
  animation: fadeIn 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}

/* List Item Transition */
.list-enter-active,
.list-leave-active {
  transition: all 0.4s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>