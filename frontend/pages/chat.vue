<template>
  <div class="min-h-screen bg-[#0b0b0f] text-gray-100 font-sans selection:bg-pink-500/30 relative overflow-hidden">
    <sidebar class="fixed left-0 top-0 h-full z-40" />

    <div class="fixed top-1/2 left-0 -translate-y-1/2 w-[500px] h-[500px] bg-blue-600/10 blur-[150px] rounded-full pointer-events-none z-0"></div>
    <div class="fixed bottom-0 right-0 w-[600px] h-[600px] bg-pink-600/10 blur-[150px] rounded-full pointer-events-none z-0"></div>

    <main class="ml-20 relative z-10 p-4 md:p-8 h-screen flex flex-col box-border">
      
      <div class="flex-1 max-w-7xl mx-auto w-full bg-[#121215]/60 backdrop-blur-xl border border-white/10 rounded-[2rem] overflow-hidden shadow-2xl grid grid-cols-12 relative animate-in-fade">
        
        <div class="col-span-12 md:col-span-4 border-r border-white/5 flex flex-col bg-[#121215]/40">
          
          <div class="p-6 border-b border-white/5">
            <h2 class="text-2xl font-bold text-white flex items-center gap-3 mb-4">
              <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">Messages</span> 💬
            </h2>
            <div class="relative">
              <input 
                type="text" 
                placeholder="ค้นหาแชท..." 
                class="w-full bg-white/5 border border-white/10 rounded-xl py-2.5 px-4 pl-10 text-sm text-gray-300 focus:outline-none focus:bg-white/10 focus:border-pink-500/50 transition-all placeholder:text-gray-600"
              />
              <span class="absolute left-3 top-2.5 text-gray-500 text-sm">🔍</span>
            </div>
          </div>
          
          <div class="flex-1 overflow-y-auto custom-scrollbar p-3 space-y-1">
            <div 
              v-for="conv in conversations" 
              :key="conv.id"
              @click="selectConversation(conv)"
              class="group p-3 rounded-2xl flex items-center gap-4 cursor-pointer transition-all duration-300 relative overflow-hidden"
              :class="selectedConv?.id === conv.id ? 'bg-white/10 shadow-lg' : 'hover:bg-white/5'"
            >
              <div v-if="selectedConv?.id === conv.id" class="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-pink-500 rounded-r-full"></div>

              <div class="relative shrink-0">
                <img 
                  :src="conv.other_user?.profile_image_url || defaultAvatar" 
                  class="w-12 h-12 rounded-full object-cover border-2 transition-colors"
                  :class="selectedConv?.id === conv.id ? 'border-pink-500' : 'border-white/10 group-hover:border-white/30'"
                />
                <div v-if="conv.unread_count" class="absolute -top-0.5 -right-0.5 w-5 h-5 bg-gradient-to-r from-pink-500 to-rose-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center shadow-lg border border-[#121215]">
                  {{ conv.unread_count }}
                </div>
              </div>

              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-0.5">
                  <p class="font-bold text-sm truncate" :class="selectedConv?.id === conv.id ? 'text-white' : 'text-gray-300'">
                    {{ conv.other_user?.username }}
                  </p>
                  <span class="text-[10px] text-gray-500">{{ formatTime(conv.last_message_at) }}</span>
                </div>
                <p class="text-sm truncate" :class="conv.unread_count ? 'text-white font-medium' : 'text-gray-500'">
                  {{ conv.last_message || 'เริ่มการสนทนา...' }}
                </p>
              </div>
            </div>

            <div v-if="!conversations.length" class="py-10 text-center text-gray-500 text-sm">
              ยังไม่มีการสนทนา
            </div>
          </div>
        </div>

        <div class="col-span-12 md:col-span-8 flex flex-col bg-[#0f0f12]/50 relative">
          
          <div class="absolute inset-0 opacity-[0.02] bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] pointer-events-none"></div>

          <template v-if="selectedConv">
            <div class="p-4 border-b border-white/5 bg-[#121215]/80 backdrop-blur-md flex items-center gap-4 sticky top-0 z-20">
              <img :src="selectedConv.other_user?.profile_image_url || defaultAvatar" class="w-10 h-10 rounded-full object-cover border border-white/10" />
              <div>
                <h3 class="font-bold text-white leading-tight">{{ selectedConv.other_user?.username }}</h3>
                <p v-if="selectedConv.other_user?.shop_name" class="text-xs text-pink-400 flex items-center gap-1">
                  <span>🏪</span> {{ selectedConv.other_user?.shop_name }}
                </p>
                <p v-else class="text-xs text-green-400 flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-green-500"></span> Online
                </p>
              </div>
              
              <div class="ml-auto flex gap-2">
                <button class="w-8 h-8 rounded-full hover:bg-white/5 flex items-center justify-center text-gray-400">📞</button>
                <button class="w-8 h-8 rounded-full hover:bg-white/5 flex items-center justify-center text-gray-400">⋮</button>
              </div>
            </div>

            <div ref="messagesContainer" class="flex-1 overflow-y-auto custom-scrollbar p-6 space-y-6 scroll-smooth">
              <div 
                v-for="(msg, index) in messages" 
                :key="msg.id"
                class="flex w-full"
                :class="msg.is_mine ? 'justify-end' : 'justify-start'"
              >
                <div 
                  class="max-w-[75%] md:max-w-[60%] relative group"
                  :class="msg.is_mine ? 'items-end flex flex-col' : 'items-start flex flex-col'"
                >
                  <div 
                    class="px-5 py-3 text-sm md:text-base leading-relaxed break-words shadow-lg"
                    :class="[
                      msg.is_mine 
                        ? 'bg-gradient-to-br from-pink-600 to-rose-600 text-white rounded-[1.2rem] rounded-tr-none' 
                        : 'bg-[#27272a] text-gray-200 border border-white/5 rounded-[1.2rem] rounded-tl-none'
                    ]"
                  >
                    {{ msg.content }}
                  </div>
                  
                  <span class="text-[10px] text-gray-500 mt-1 opacity-0 group-hover:opacity-100 transition-opacity px-1">
                    {{ formatTime(msg.created_at) }}
                  </span>
                </div>
              </div>
            </div>

            <div class="p-4 border-t border-white/5 bg-[#121215]/80 backdrop-blur-md">
              <form @submit.prevent="sendMessage" class="flex gap-3 items-end max-w-4xl mx-auto">
                <button type="button" class="w-10 h-10 rounded-full bg-white/5 hover:bg-white/10 text-gray-400 flex items-center justify-center transition-colors shrink-0">
                  📎
                </button>
                
                <div class="flex-1 relative">
                  <input 
                    v-model="newMessage"
                    type="text"
                    placeholder="พิมพ์ข้อความของคุณ..."
                    class="w-full bg-[#1e1e24] border border-white/10 rounded-2xl py-3 px-5 text-white focus:outline-none focus:border-pink-500/50 focus:ring-1 focus:ring-pink-500/20 transition-all placeholder:text-gray-600"
                  />
                  <button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-yellow-400 transition-colors">😊</button>
                </div>

                <button 
                  type="submit" 
                  :disabled="!newMessage.trim()"
                  class="w-12 h-12 rounded-full bg-gradient-to-r from-pink-500 to-rose-600 text-white flex items-center justify-center shadow-lg shadow-pink-500/20 hover:scale-105 active:scale-95 disabled:opacity-50 disabled:scale-100 transition-all shrink-0"
                >
                  ➤
                </button>
              </form>
            </div>
          </template>

          <div v-else class="flex-1 flex flex-col items-center justify-center text-center p-8">
            <div class="w-32 h-32 relative mb-6">
               <div class="absolute inset-0 bg-pink-500/20 blur-2xl rounded-full animate-pulse"></div>
               <div class="relative w-full h-full bg-[#18181b] rounded-full border border-white/10 flex items-center justify-center text-6xl shadow-2xl">
                 💌
               </div>
            </div>
            <h3 class="text-2xl font-bold text-white mb-2">เริ่มการสนทนา</h3>
            <p class="text-gray-500 max-w-xs">เลือกรายชื่อจากด้านซ้ายเพื่อพูดคุยกับร้านค้าหรือเพื่อนของคุณ</p>
          </div>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import axios from 'axios';

const conversations = ref([]);
const selectedConv = ref(null);
const messages = ref([]);
const newMessage = ref('');
const messagesContainer = ref(null);
const defaultAvatar = 'https://via.placeholder.com/150?text=User'; // Placeholder
const baseUrl = 'http://localhost:5000';

function formatTime(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  const now = new Date();
  
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' });
  } else {
    return date.toLocaleDateString('th-TH', { day: 'numeric', month: 'short' });
  }
}

async function fetchConversations() {
  const token = localStorage.getItem('token');
  if (!token) return;

  try {
    const res = await axios.get(`${baseUrl}/api/chat/conversations`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    conversations.value = res.data.conversations || [];
  } catch (err) {
    console.error('Failed to fetch conversations:', err);
  }
}

async function selectConversation(conv) {
  selectedConv.value = conv;
  const token = localStorage.getItem('token');
  
  try {
    const res = await axios.get(`${baseUrl}/api/chat/${conv.id}`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    // Transform messages if needed, here assuming API returns simple structure
    messages.value = res.data.messages || [];
    
    // Reset local unread count
    conv.unread_count = 0;
    
    await nextTick();
    scrollToBottom();
  } catch (err) {
    console.error('Failed to fetch messages:', err);
  }
}

async function sendMessage() {
  if (!newMessage.value.trim() || !selectedConv.value) return;
  
  const token = localStorage.getItem('token');
  const content = newMessage.value.trim();
  newMessage.value = '';

  // Optimistic UI update (optional: show immediately before API confirms)
  // But here we follow the standard logic provided
  
  try {
    const res = await axios.post(`${baseUrl}/api/chat`, {
      recipient_id: selectedConv.value.other_user.id,
      content
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });

    const sentMsg = {
      id: res.data.message.id,
      content,
      is_mine: true,
      created_at: res.data.message.created_at || new Date().toISOString()
    };

    messages.value.push(sentMsg);
    selectedConv.value.last_message = content;
    selectedConv.value.last_message_at = new Date().toISOString();
    
    await nextTick();
    scrollToBottom();
  } catch (err) {
    console.error('Failed to send message:', err);
    alert('ส่งข้อความไม่สำเร็จ');
  }
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
}

onMounted(fetchConversations);
</script>

<style scoped>
/* Page Entrance Animation */
.animate-in-fade {
  animation: fadeIn 0.6s cubic-bezier(0.16, 1, 0.3, 1);
}
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(15px); }
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
</style>