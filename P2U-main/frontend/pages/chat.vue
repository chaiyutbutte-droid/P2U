<template>
  <div class="min-h-screen ml-20 p-6">
    <Navbar />
    <sidebar />
    
    <div class="max-w-6xl mx-auto">
      <div class="grid grid-cols-12 gap-6 h-[calc(100vh-8rem)]">
        <!-- Conversations List -->
        <div class="col-span-4 card flex flex-col overflow-hidden">
          <div class="p-4 border-b border-white/10">
            <h2 class="font-semibold text-white flex items-center gap-2">
              💬 ข้อความ
            </h2>
          </div>
          
          <div class="flex-1 overflow-y-auto">
            <div 
              v-for="conv in conversations" 
              :key="conv.id"
              @click="selectConversation(conv)"
              class="p-4 flex items-center gap-3 hover:bg-white/5 cursor-pointer transition-colors border-b border-white/5"
              :class="{ 'bg-primary-500/10 border-l-4 border-primary-500': selectedConv?.id === conv.id }"
            >
              <div class="relative">
                <img :src="conv.other_user?.profile_image_url || '/guest-profile.png'" class="w-12 h-12 rounded-xl object-cover" />
                <div v-if="conv.unread_count" class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs font-bold rounded-full flex items-center justify-center">
                  {{ conv.unread_count }}
                </div>
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-white truncate">{{ conv.other_user?.username }}</p>
                <p class="text-dark-400 text-sm truncate">{{ conv.last_message || 'ยังไม่มีข้อความ' }}</p>
              </div>
              <span class="text-dark-500 text-xs">{{ formatTime(conv.last_message_at) }}</span>
            </div>

            <div v-if="!conversations.length" class="p-8 text-center">
              <p class="text-dark-400">ยังไม่มีการสนทนา</p>
            </div>
          </div>
        </div>

        <!-- Chat Area -->
        <div class="col-span-8 card flex flex-col overflow-hidden">
          <template v-if="selectedConv">
            <!-- Chat Header -->
            <div class="p-4 border-b border-white/10 flex items-center gap-3">
              <img :src="selectedConv.other_user?.profile_image_url || '/guest-profile.png'" class="w-10 h-10 rounded-xl object-cover" />
              <div>
                <p class="font-medium text-white">{{ selectedConv.other_user?.username }}</p>
                <p v-if="selectedConv.other_user?.shop_name" class="text-dark-400 text-sm">{{ selectedConv.other_user?.shop_name }}</p>
              </div>
            </div>

            <!-- Messages -->
            <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 space-y-4">
              <div 
                v-for="msg in messages" 
                :key="msg.id"
                :class="msg.is_mine ? 'flex justify-end' : 'flex justify-start'"
              >
                <div :class="msg.is_mine ? 'chat-bubble sent' : 'chat-bubble received'">
                  <p>{{ msg.content }}</p>
                  <p class="text-xs mt-1" :class="msg.is_mine ? 'text-white/70' : 'text-dark-500'">
                    {{ formatTime(msg.created_at) }}
                  </p>
                </div>
              </div>
            </div>

            <!-- Input -->
            <div class="p-4 border-t border-white/10">
              <form @submit.prevent="sendMessage" class="flex gap-3">
                <input 
                  v-model="newMessage"
                  type="text"
                  placeholder="พิมพ์ข้อความ..."
                  class="flex-1 input-glass"
                />
                <button 
                  type="submit" 
                  :disabled="!newMessage.trim()"
                  class="btn-primary px-6"
                >
                  ส่ง
                </button>
              </form>
            </div>
          </template>

          <template v-else>
            <div class="flex-1 flex items-center justify-center">
              <div class="text-center">
                <div class="w-20 h-20 rounded-full bg-dark-700 mx-auto mb-4 flex items-center justify-center text-4xl">
                  💬
                </div>
                <h3 class="text-lg font-semibold text-white mb-2">เลือกการสนทนา</h3>
                <p class="text-dark-400">เลือกแชทจากรายการด้านซ้ายเพื่อเริ่มสนทนา</p>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
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

const baseUrl = 'http://localhost:5000';

function formatTime(dateStr) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  return date.toLocaleTimeString('th-TH', { hour: '2-digit', minute: '2-digit' });
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
    messages.value = res.data.messages || [];
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

  try {
    const res = await axios.post(`${baseUrl}/api/chat`, {
      recipient_id: selectedConv.value.other_user.id,
      content
    }, {
      headers: { Authorization: `Bearer ${token}` }
    });

    messages.value.push({
      id: res.data.message.id,
      content,
      is_mine: true,
      created_at: res.data.message.created_at
    });

    selectedConv.value.last_message = content;
    
    await nextTick();
    scrollToBottom();
  } catch (err) {
    console.error('Failed to send message:', err);
  }
}

function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
}

onMounted(fetchConversations);
</script>
