<template>
  <div class="min-h-screen bg-[#0b0b0f] text-white font-sans selection:bg-red-500/30 relative overflow-x-hidden">
    
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
       <div class="absolute top-[-10%] right-[-5%] w-[600px] h-[600px] bg-red-600/10 rounded-full blur-[120px] mix-blend-screen animate-pulse-slow"></div>
       <div class="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-orange-600/10 rounded-full blur-[100px] mix-blend-screen animate-pulse-slow" style="animation-delay: 2s;"></div>
    </div>

    <div class="relative z-10 max-w-7xl mx-auto p-6 lg:p-10">
      
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-10 animate-fade-in-down">
        <div>
          <h1 class="text-3xl font-bold flex items-center gap-3">
            <span class="w-2 h-8 bg-gradient-to-b from-red-500 to-orange-500 rounded-full"></span>
            Admin Command Center
          </h1>
          <p class="text-gray-400 mt-2 ml-5 text-sm">
            ยินดีต้อนรับ, <span class="text-white font-semibold">{{ adminUser?.username || 'Admin' }}</span>
          </p>
        </div>

        <button 
          @click="handleLogout" 
          class="group flex items-center gap-2 px-5 py-2.5 rounded-xl border border-red-500/30 text-red-400 hover:bg-red-500 hover:text-white transition-all duration-300 hover:shadow-[0_0_15px_rgba(239,68,68,0.4)]"
        >
          <span>🚪</span>
          <span class="font-medium">ออกจากระบบ</span>
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10 animate-fade-in-up">
        <div class="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl hover:border-blue-500/50 transition-colors group">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-400 text-xs uppercase tracking-wider mb-1">ผู้ใช้ทั้งหมด</p>
              <h3 class="text-3xl font-bold text-white group-hover:text-blue-400 transition-colors">{{ stats.total_users || 0 }}</h3>
            </div>
            <div class="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">👥</div>
          </div>
        </div>

        <div class="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl hover:border-purple-500/50 transition-colors group">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-400 text-xs uppercase tracking-wider mb-1">ผู้ขาย</p>
              <h3 class="text-3xl font-bold text-white group-hover:text-purple-400 transition-colors">{{ stats.total_sellers || 0 }}</h3>
            </div>
            <div class="w-12 h-12 rounded-xl bg-purple-500/10 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">🏪</div>
          </div>
        </div>

        <div class="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl hover:border-pink-500/50 transition-colors group">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-400 text-xs uppercase tracking-wider mb-1">สินค้าทั้งหมด</p>
              <h3 class="text-3xl font-bold text-white group-hover:text-pink-400 transition-colors">{{ stats.total_products || 0 }}</h3>
            </div>
            <div class="w-12 h-12 rounded-xl bg-pink-500/10 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">📦</div>
          </div>
        </div>

        <div class="bg-black/40 backdrop-blur-md border border-white/10 p-6 rounded-2xl hover:border-green-500/50 transition-colors group">
          <div class="flex justify-between items-start">
            <div>
              <p class="text-gray-400 text-xs uppercase tracking-wider mb-1">รายได้รวม</p>
              <h3 class="text-3xl font-bold text-green-400 group-hover:text-green-300 transition-colors">฿{{ stats.total_revenue?.toLocaleString() || 0 }}</h3>
            </div>
            <div class="w-12 h-12 rounded-xl bg-green-500/10 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">💰</div>
          </div>
        </div>
      </div>

      <div class="animate-fade-in-up" style="animation-delay: 0.1s;">
        
        <div class="flex flex-wrap gap-2 mb-6 p-1 bg-white/5 rounded-2xl w-fit backdrop-blur-sm border border-white/5">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="activeTab = tab.id"
            class="px-6 py-2.5 rounded-xl text-sm font-medium transition-all duration-300 flex items-center gap-2 relative"
            :class="activeTab === tab.id 
              ? 'bg-gradient-to-r from-red-600 to-orange-600 text-white shadow-lg shadow-red-500/20' 
              : 'text-gray-400 hover:text-white hover:bg-white/5'"
          >
            <span>{{ tab.icon }}</span>
            {{ tab.name }}
            
            <span v-if="tab.id === 'tokens' && tokenStats.pending > 0" class="absolute -top-1 -right-1 w-3 h-3 rounded-full bg-red-500 animate-pulse"></span>
            <span v-if="tab.id === 'verifications' && pendingVerificationsCount > 0" class="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-pink-500 text-[10px] font-bold text-white animate-pulse">
               {{ pendingVerificationsCount }}
            </span>
          </button>
        </div>

        <div class="bg-black/40 backdrop-blur-xl border border-white/10 rounded-3xl overflow-hidden shadow-2xl min-h-[500px]">
          
          <div v-if="activeTab === 'users'">
             <div class="p-6 border-b border-white/10 flex items-center justify-between bg-white/5">
                <h2 class="text-lg font-bold text-white flex items-center gap-2">
                   👥 รายชื่อผู้ใช้ในระบบ
                   <span class="text-xs font-normal text-gray-400 bg-white/10 px-2 py-1 rounded-full">{{ users.length }} users</span>
                </h2>
             </div>
             <div class="overflow-x-auto">
                <table class="w-full">
                   <thead class="bg-black/20 text-gray-400 text-xs uppercase tracking-wider font-semibold">
                      <tr>
                         <th class="text-left p-5">User Info</th>
                         <th class="text-left p-5">Role</th>
                         <th class="text-left p-5">Status</th>
                         <th class="text-left p-5">Balance</th>
                         <th class="text-right p-5">Actions</th>
                      </tr>
                   </thead>
                   <tbody class="divide-y divide-white/5">
                      <tr v-for="user in users" :key="user.id" class="hover:bg-white/5 transition-colors">
                         <td class="p-5">
                            <div class="flex items-center gap-4">
                               <div class="w-10 h-10 rounded-full bg-gradient-to-br from-gray-700 to-gray-600 flex items-center justify-center font-bold text-white shadow-inner border border-white/10">
                                  {{ user.username.charAt(0).toUpperCase() }}
                               </div>
                               <div>
                                  <div class="font-medium text-white">{{ user.username }}</div>
                                  <div class="text-xs text-gray-500">{{ user.email }}</div>
                               </div>
                            </div>
                         </td>
                         <td class="p-5">
                            <span :class="user.is_seller ? 'bg-purple-500/20 text-purple-300 border-purple-500/30' : 'bg-blue-500/20 text-blue-300 border-blue-500/30'" class="px-3 py-1 rounded-full text-xs border font-medium">
                               {{ user.is_seller ? 'Seller' : 'Member' }}
                            </span>
                         </td>
                         <td class="p-5">
                            <span :class="user.is_active ? 'text-green-400' : 'text-red-400'" class="flex items-center gap-1.5 text-sm">
                               <span class="w-1.5 h-1.5 rounded-full" :class="user.is_active ? 'bg-green-400' : 'bg-red-400'"></span>
                               {{ user.is_active ? 'Active' : 'Banned' }}
                            </span>
                         </td>
                         <td class="p-5 font-mono text-yellow-500">
                            🪙 {{ user.coin_balance?.toLocaleString() }}
                         </td>
                         <td class="p-5 text-right space-x-2">
                            <button @click="toggleBanUser(user)" :class="user.is_active ? 'text-yellow-500 hover:bg-yellow-500/10' : 'text-green-500 hover:bg-green-500/10'" class="p-2 rounded-lg transition-colors" :title="user.is_active ? 'Ban User' : 'Unban User'">
                               {{ user.is_active ? '🚫' : '✅' }}
                            </button>
                            <button @click="deleteUser(user)" class="p-2 rounded-lg text-red-500 hover:bg-red-500/10 transition-colors" title="Delete User">
                               🗑️
                            </button>
                         </td>
                      </tr>
                   </tbody>
                </table>
             </div>
          </div>

          <div v-if="activeTab === 'products'">
            <div class="p-6 border-b border-white/10 bg-white/5">
                <h2 class="text-lg font-bold text-white">📦 คลังสินค้า</h2>
             </div>
             <div class="overflow-x-auto">
                <table class="w-full">
                   <thead class="bg-black/20 text-gray-400 text-xs uppercase tracking-wider font-semibold">
                      <tr>
                         <th class="text-left p-5">Product</th>
                         <th class="text-left p-5">Price</th>
                         <th class="text-left p-5">Seller</th>
                         <th class="text-left p-5">Added Date</th>
                         <th class="text-right p-5">Actions</th>
                      </tr>
                   </thead>
                   <tbody class="divide-y divide-white/5">
                      <tr v-for="product in products" :key="product.id" class="hover:bg-white/5 transition-colors">
                         <td class="p-5">
                            <div class="flex items-center gap-4">
                               <img :src="getImageUrl(product.image_url)" class="w-10 h-10 rounded-lg object-cover bg-gray-800" />
                               <span class="font-medium text-white">{{ product.name }}</span>
                            </div>
                         </td>
                         <td class="p-5 font-mono text-green-400">฿{{ product.price.toLocaleString() }}</td>
                         <td class="p-5 text-gray-400">{{ product.seller?.username }}</td>
                         <td class="p-5 text-gray-500 text-sm">{{ new Date(product.created_at).toLocaleDateString() }}</td>
                         <td class="p-5 text-right">
                            <button @click="deleteProduct(product)" class="px-3 py-1.5 rounded-lg border border-red-500/30 text-red-400 hover:bg-red-500 hover:text-white transition-colors text-sm">
                               ลบสินค้า
                            </button>
                         </td>
                      </tr>
                   </tbody>
                </table>
             </div>
          </div>

          <div v-if="activeTab === 'orders'">
             <div class="p-6 border-b border-white/10 bg-white/5">
                <h2 class="text-lg font-bold text-white">🛒 รายการสั่งซื้อ</h2>
             </div>
             <div class="overflow-x-auto">
                <table class="w-full">
                   <thead class="bg-black/20 text-gray-400 text-xs uppercase tracking-wider font-semibold">
                      <tr>
                         <th class="text-left p-5">Order ID</th>
                         <th class="text-left p-5">Customer</th>
                         <th class="text-left p-5">Total</th>
                         <th class="text-left p-5">Status</th>
                         <th class="text-left p-5">Date</th>
                      </tr>
                   </thead>
                   <tbody class="divide-y divide-white/5">
                      <tr v-for="order in orders" :key="order.id" class="hover:bg-white/5 transition-colors">
                         <td class="p-5 font-mono text-gray-400 text-sm">#{{ order.id.slice(0,8) }}...</td>
                         <td class="p-5 text-white">{{ order.user?.username }}</td>
                         <td class="p-5 font-mono text-green-400">฿{{ order.total_price.toLocaleString() }}</td>
                         <td class="p-5">
                            <select 
                               v-model="order.status" 
                               @change="updateOrderStatus(order)"
                               class="bg-black/30 text-sm text-white border border-white/10 rounded-lg px-2 py-1 focus:border-red-500 outline-none cursor-pointer"
                            >
                               <option value="pending">🟡 รอตรวจสอบ</option>
                               <option value="processing">🔵 กำลังดำเนินการ</option>
                               <option value="completed">🟢 สำเร็จ</option>
                               <option value="cancelled">🔴 ยกเลิก</option>
                            </select>
                         </td>
                         <td class="p-5 text-gray-500 text-sm">{{ new Date(order.created_at).toLocaleDateString() }}</td>
                      </tr>
                   </tbody>
                </table>
             </div>
          </div>

          <div v-if="activeTab === 'tokens'">
             <div class="p-6 border-b border-white/10 bg-white/5 flex justify-between items-center">
                <h2 class="text-lg font-bold text-white flex items-center gap-2">
                   🪙 คำขอเติม Token
                </h2>
                <div v-if="tokenStats.pending > 0" class="bg-yellow-500/20 text-yellow-400 border border-yellow-500/30 px-3 py-1 rounded-full text-xs font-medium animate-pulse">
                   {{ tokenStats.pending }} รอการตรวจสอบ
                </div>
             </div>
             <div class="overflow-x-auto">
                <table class="w-full">
                   <thead class="bg-black/20 text-gray-400 text-xs uppercase tracking-wider font-semibold">
                      <tr>
                         <th class="text-left p-5">User</th>
                         <th class="text-left p-5">Amount</th>
                         <th class="text-left p-5">สลิป</th>
                         <th class="text-left p-5">Status</th>
                         <th class="text-left p-5">Date</th>
                         <th class="text-right p-5">Action</th>
                      </tr>
                   </thead>
                   <tbody class="divide-y divide-white/5">
                      <tr v-for="req in tokenRequests" :key="req.id" class="hover:bg-white/5 transition-colors">
                         <td class="p-5">
                            <div class="flex items-center gap-3">
                               <div class="w-8 h-8 rounded-full bg-gradient-to-r from-yellow-600 to-amber-600 flex items-center justify-center text-xs font-bold text-white">
                                  {{ req.user?.username.charAt(0).toUpperCase() }}
                               </div>
                               <div>
                                  <div class="text-white text-sm">{{ req.user?.username }}</div>
                                  <div v-if="req.sender_name" class="text-xs text-gray-500">ผู้โอน: {{ req.sender_name }}</div>
                               </div>
                            </div>
                         </td>
                         <td class="p-5">
                            <div class="font-mono text-xl text-yellow-400 font-bold">
                               +{{ req.amount?.toLocaleString() }}
                            </div>
                            <div v-if="req.is_auto_approved" class="mt-1">
                               <span class="text-[10px] bg-blue-500/20 text-blue-400 px-2 py-0.5 rounded-full">⚡ อัตโนมัติ</span>
                            </div>
                         </td>
                         <td class="p-5">
                            <div v-if="req.payment_proof_url" 
                                 class="relative w-16 h-16 rounded-lg overflow-hidden border border-white/10 cursor-pointer hover:border-yellow-500/50 transition-colors group"
                                 @click="openImageModal(getImageUrl(req.payment_proof_url))">
                               <img :src="getImageUrl(req.payment_proof_url)" class="w-full h-full object-cover" />
                               <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 bg-black/50 transition-opacity">
                                  <span class="text-xs text-white">🔍</span>
                               </div>
                            </div>
                            <span v-else class="text-xs text-gray-500">ไม่มีสลิป</span>
                         </td>
                         <td class="p-5">
                            <span 
                               class="px-2 py-1 rounded-md text-xs font-medium border"
                               :class="{
                                  'bg-yellow-500/10 text-yellow-400 border-yellow-500/20': req.status === 'pending',
                                  'bg-green-500/10 text-green-400 border-green-500/20': req.status === 'approved',
                                  'bg-red-500/10 text-red-400 border-red-500/20': req.status === 'rejected'
                               }"
                            >
                               {{ req.status === 'pending' ? 'รอตรวจสอบ' : req.status === 'approved' ? 'สำเร็จ' : 'ปฏิเสธ' }}
                            </span>
                            <div v-if="req.transaction_ref" class="mt-1 text-[10px] text-gray-500 font-mono">
                               Ref: {{ req.transaction_ref }}
                            </div>
                         </td>
                         <td class="p-5 text-gray-500 text-sm">{{ new Date(req.created_at).toLocaleDateString('th-TH') }}</td>
                         <td class="p-5 text-right">
                            <div v-if="req.status === 'pending'" class="flex gap-2 justify-end">
                               <button @click="approveToken(req)" class="p-2 rounded-lg bg-green-500/10 text-green-400 hover:bg-green-500 hover:text-white transition-all border border-green-500/20" title="Approve">
                                  ✓ อนุมัติ
                               </button>
                               <button @click="rejectToken(req)" class="p-2 rounded-lg bg-red-500/10 text-red-400 hover:bg-red-500 hover:text-white transition-all border border-red-500/20" title="Reject">
                                  ✕ ปฏิเสธ
                               </button>
                            </div>
                            <div v-else class="text-xs text-gray-500">
                               <span v-if="req.admin_note" class="block italic">{{ req.admin_note }}</span>
                            </div>
                         </td>
                      </tr>
                   </tbody>
                </table>
             </div>
          </div>

          <div v-if="activeTab === 'verifications'">
            <div class="p-6 border-b border-white/10 bg-white/5 flex justify-between items-center">
              <div class="flex items-center gap-6">
                 <h2 class="text-lg font-bold text-white flex items-center gap-2">
                   🛡️ ตรวจสอบเอกสารผู้ขาย
                 </h2>
                 
                 <div class="flex gap-2 bg-black/40 p-1 rounded-lg">
                    <button @click="setVerificationFilter('PENDING')" 
                            class="px-4 py-1.5 rounded-md text-xs font-bold transition-all"
                            :class="verificationFilter === 'PENDING' ? 'bg-pink-600 text-white shadow' : 'text-gray-400 hover:text-white'">
                       ⏳ รอตรวจสอบ <span v-if="pendingVerificationsCount > 0">({{ pendingVerificationsCount }})</span>
                    </button>
                    <button @click="setVerificationFilter('HISTORY')" 
                            class="px-4 py-1.5 rounded-md text-xs font-bold transition-all"
                            :class="verificationFilter === 'HISTORY' ? 'bg-gray-700 text-white shadow' : 'text-gray-400 hover:text-white'">
                       📜 ประวัติการอนุมัติ
                    </button>
                 </div>
              </div>
            </div>
            
            <div class="p-6">
              <div v-if="verifications.length === 0" class="text-center py-20 bg-white/5 rounded-2xl border border-dashed border-white/10">
                <span class="text-4xl block mb-2">✅</span>
                <span class="text-gray-400">
                    {{ verificationFilter === 'PENDING' ? 'ไม่มีรายการค้างตรวจสอบ' : 'ยังไม่มีประวัติการอนุมัติ' }}
                </span>
              </div>

              <div v-else class="grid grid-cols-1 gap-6">
                <div v-for="req in verifications" :key="req.id" 
                     class="bg-[#1a1a20] border border-white/10 rounded-2xl p-6 relative overflow-hidden group hover:border-pink-500/30 transition-all">
                  
                  <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 pb-4 border-b border-white/5">
                    <div>
                      <h3 class="text-xl font-bold text-white flex items-center gap-2">
                        🏠 {{ req.shop_name }}
                        <span v-if="req.status === 'PENDING'" class="text-xs bg-yellow-500/20 text-yellow-300 px-2 py-0.5 rounded-full border border-yellow-500/30">รอตรวจสอบ</span>
                        <span v-else-if="req.status === 'APPROVED'" class="text-xs bg-green-500/20 text-green-300 px-2 py-0.5 rounded-full border border-green-500/30">อนุมัติแล้ว ✅</span>
                        <span v-else-if="req.status === 'REJECTED'" class="text-xs bg-red-500/20 text-red-300 px-2 py-0.5 rounded-full border border-red-500/30">ถูกปฏิเสธ ❌</span>
                      </h3>
                      <p class="text-sm text-gray-500 mt-1">Submission ID: <span class="font-mono text-gray-400">#{{ req.id }}</span></p>
                    </div>
                    
                    <div v-if="req.status === 'PENDING'" class="flex gap-3 mt-4 md:mt-0">
                      <button @click="handleRejectSeller(req.id)" 
                              class="px-4 py-2 rounded-lg border border-red-500/30 text-red-400 hover:bg-red-500/10 transition-colors text-sm font-semibold">
                        ไม่อนุมัติ ❌
                      </button>
                      <button @click="handleApproveSeller(req.id)" 
                              class="px-6 py-2 rounded-lg bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-500 hover:to-emerald-500 text-white shadow-lg shadow-green-900/20 transition-all transform hover:scale-105 text-sm font-bold">
                        อนุมัติ ✅
                      </button>
                    </div>
                    
                    <div v-else class="text-right mt-2 md:mt-0">
                        <p class="text-xs text-gray-500">ดำเนินการเมื่อ</p>
                        <p class="text-sm text-white font-mono">{{ new Date(req.processed_at || req.submitted_at).toLocaleString('th-TH') }}</p>
                    </div>
                  </div>

                  <div v-if="req.status === 'REJECTED'" class="bg-red-900/20 border border-red-500/30 p-4 rounded-xl mb-6">
                     <p class="text-red-300 text-sm font-bold">⚠️ เหตุผลที่ปฏิเสธ:</p>
                     <p class="text-gray-300 text-sm mt-1">{{ req.rejection_reason || 'ไม่ระบุ' }}</p>
                  </div>

                  <div class="bg-black/20 rounded-xl p-5 border border-white/5 mb-6">
                    <h4 class="text-gray-400 text-xs font-bold uppercase tracking-wider mb-4 border-l-2 border-pink-500 pl-2">ข้อมูลส่วนตัวผู้สมัคร</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-y-4 gap-x-8">
                        <div>
                            <p class="text-gray-500 text-xs mb-1">ชื่อ-นามสกุล (ตามบัตร)</p>
                            <p class="text-white font-medium text-lg">{{ req.real_name || '-' }}</p>
                        </div>
                        <div>
                            <p class="text-gray-500 text-xs mb-1">เลขบัตรประชาชน</p>
                            <p class="text-white font-mono tracking-wider">{{ req.id_card_number || '-' }}</p>
                        </div>
                        <div>
                            <p class="text-gray-500 text-xs mb-1">บัญชีผู้ใช้ (Username)</p>
                            <div class="flex items-center gap-2">
                                <div class="w-6 h-6 rounded-full bg-gray-700 flex items-center justify-center text-[10px] text-white">
                                    {{ req.user_name?.charAt(0).toUpperCase() }}
                                </div>
                                <span class="text-gray-300">{{ req.user_name }}</span>
                            </div>
                        </div>
                        <div>
                            <p class="text-gray-500 text-xs mb-1">เบอร์โทรศัพท์</p>
                            <p class="text-gray-300">{{ req.phone_number || '-' }}</p>
                        </div>
                        <div class="md:col-span-2">
                            <p class="text-gray-500 text-xs mb-1">ที่อยู่</p>
                            <p class="text-gray-300 bg-white/5 p-2 rounded-lg text-sm leading-relaxed border border-white/5">
                                {{ req.address || '-' }}
                            </p>
                        </div>
                         <div class="md:col-span-2 flex items-center gap-2 text-xs text-gray-500 mt-2">
                            <span>📅 ส่งเมื่อ: {{ new Date(req.submitted_at).toLocaleString('th-TH') }}</span>
                         </div>
                    </div>
                  </div>

                  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="space-y-2">
                      <p class="text-xs text-gray-400 font-semibold uppercase tracking-wider">🪪 ด้านหน้าบัตร</p>
                      <div class="relative h-48 bg-black/50 rounded-lg overflow-hidden border border-white/10 cursor-zoom-in hover:border-pink-500/50 transition-colors" 
                           @click="openImageModal(getImageUrl(req.id_front_url))">
                        <img :src="getImageUrl(req.id_front_url)" class="w-full h-full object-contain" />
                        <div class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 bg-black/40 transition-opacity">
                          <span class="text-xs bg-black/60 px-2 py-1 rounded text-white">🔍 ขยาย</span>
                        </div>
                      </div>
                    </div>
                    
                    <div class="space-y-2">
                      <p class="text-xs text-gray-400 font-semibold uppercase tracking-wider">🔙 ด้านหลังบัตร</p>
                      <div class="relative h-48 bg-black/50 rounded-lg overflow-hidden border border-white/10 cursor-zoom-in hover:border-purple-500/50 transition-colors" 
                           @click="openImageModal(getImageUrl(req.id_back_url))">
                        <img :src="getImageUrl(req.id_back_url)" class="w-full h-full object-contain" />
                         <div class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 bg-black/40 transition-opacity">
                          <span class="text-xs bg-black/60 px-2 py-1 rounded text-white">🔍 ขยาย</span>
                        </div>
                      </div>
                    </div>
                    
                    <div class="space-y-2">
                      <p class="text-xs text-gray-400 font-semibold uppercase tracking-wider">🤳 ภาพเซลฟี่</p>
                      <div class="relative h-48 bg-black/50 rounded-lg overflow-hidden border border-white/10 cursor-zoom-in hover:border-blue-500/50 transition-colors" 
                           @click="openImageModal(getImageUrl(req.selfie_url))">
                        <img :src="getImageUrl(req.selfie_url)" class="w-full h-full object-contain" />
                         <div class="absolute inset-0 flex items-center justify-center opacity-0 hover:opacity-100 bg-black/40 transition-opacity">
                          <span class="text-xs bg-black/60 px-2 py-1 rounded text-white">🔍 ขยาย</span>
                        </div>
                      </div>
                    </div>
                  </div>

                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>

    <Transition name="fade">
      <div v-if="showImageModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/95 backdrop-blur-sm p-4" @click="showImageModal = false">
        <div class="relative max-w-5xl w-full h-full flex items-center justify-center">
          <img :src="currentZoomImage" class="max-w-full max-h-[90vh] rounded-lg shadow-2xl border border-white/20 object-contain" @click.stop />
          <button class="absolute top-4 right-4 bg-white/10 hover:bg-white/20 text-white rounded-full w-10 h-10 flex items-center justify-center text-xl transition-all" @click="showImageModal = false">
            ✕
          </button>
        </div>
      </div>
    </Transition>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

// ------------------------------------------
// Layout Configuration
// ------------------------------------------
definePageMeta({
  layout: 'admin'
});

const router = useRouter();
const baseUrl = 'http://localhost:5000';

// ------------------------------------------
// State Management
// ------------------------------------------
const adminUser = ref(null);
const activeTab = ref('users');
const stats = ref({});

// Data Arrays
const users = ref([]);
const products = ref([]);
const orders = ref([]);
const tokenRequests = ref([]);
const verifications = ref([]); 

// Filter for Verifications
const verificationFilter = ref('PENDING'); // 'PENDING' or 'HISTORY'
const pendingVerificationsCount = ref(0); // เก็บจำนวนที่รอตรวจสอบ

// Sub-stats
const tokenStats = ref({});

// UI States
const showImageModal = ref(false);
const currentZoomImage = ref('');

// Tabs Configuration
const tabs = [
  { id: 'users', name: 'Users', icon: '👥' },
  { id: 'products', name: 'Products', icon: '📦' },
  { id: 'orders', name: 'Orders', icon: '🛒' },
  { id: 'tokens', name: 'Tokens', icon: '🪙' },
  { id: 'verifications', name: 'Verify Sellers', icon: '🛡️' }, 
];

// ------------------------------------------
// Helper Function
// ------------------------------------------
const getImageUrl = (path) => {
  if (!path) return '/placeholder.png'; // รูปสำรองถ้าไม่มีข้อมูล
  if (path.startsWith('http')) return path; // ถ้าเป็น Full URL อยู่แล้วให้ใช้เลย
  return `${baseUrl}${path}`; // ถ้าเป็น path ย่อ ให้ต่อด้วย http://localhost:5000
};

// ------------------------------------------
// Data Fetching
// ------------------------------------------
async function fetchData() {
  const token = localStorage.getItem('admin_token');
  if (!token) {
    router.push('/admin-login');
    return;
  }

  const headers = { Authorization: `Bearer ${token}` };

  try {
    // Parallel fetching for performance
    const [statsRes, usersRes, productsRes, ordersRes] = await Promise.all([
      axios.get(`${baseUrl}/api/admin/stats`, { headers }),
      axios.get(`${baseUrl}/api/admin/users`, { headers }),
      axios.get(`${baseUrl}/api/admin/products`, { headers }),
      axios.get(`${baseUrl}/api/admin/orders`, { headers }),
    ]);

    stats.value = statsRes.data;
    users.value = usersRes.data;
    products.value = productsRes.data;
    orders.value = ordersRes.data;
    
    // Fetch specialized data
    fetchTokenRequests(headers);
    fetchVerifications(headers);
    
  } catch (err) {
    console.error('Failed to fetch admin data:', err);
    if (err.response?.status === 401 || err.response?.status === 403) {
      router.push('/admin-login');
    }
  }
}

async function fetchTokenRequests(headers) {
  try {
    const [requestsRes, statsRes] = await Promise.all([
      axios.get(`${baseUrl}/api/admin/token-requests`, { headers }),
      axios.get(`${baseUrl}/api/admin/token-stats`, { headers })
    ]);
    tokenRequests.value = requestsRes.data.requests || [];
    tokenStats.value = statsRes.data || {};
  } catch (err) {
    console.error('Failed to fetch token data', err);
  }
}

// Fetch Verifications based on current filter
async function fetchVerifications(headers) {
  try {
    // 1. Fetch Pending Count (always update this)
    const pendingRes = await axios.get(`${baseUrl}/api/admin/verifications?status=PENDING`, { headers });
    pendingVerificationsCount.value = pendingRes.data.length;

    // 2. Fetch Data based on filter
    // ถ้า Filter เป็น PENDING ก็ใช้ข้อมูลที่ดึงมาแล้วได้เลย ไม่ต้องยิงซ้ำ
    if (verificationFilter.value === 'PENDING') {
       verifications.value = pendingRes.data;
    } else {
       // ถ้าเป็น HISTORY ให้ดึงใหม่
       const historyRes = await axios.get(`${baseUrl}/api/admin/verifications?status=HISTORY`, { headers });
       verifications.value = historyRes.data;
    }

  } catch (err) {
    console.error('Failed to fetch verifications:', err);
  }
}

// Toggle Filter Function
async function setVerificationFilter(filter) {
    verificationFilter.value = filter;
    const token = localStorage.getItem('admin_token');
    const headers = { Authorization: `Bearer ${token}` };
    await fetchVerifications(headers);
}

// ------------------------------------------
// Actions: Users & Products
// ------------------------------------------
async function toggleBanUser(user) {
  const token = localStorage.getItem('admin_token');
  try {
    const res = await axios.put(`${baseUrl}/api/admin/users/${user.id}/toggle-ban`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    user.is_active = res.data.is_active;
  } catch (err) {
    console.error('Failed to toggle ban:', err);
  }
}

async function deleteUser(user) {
  if (!confirm(`ยืนยันการลบผู้ใช้ ${user.username}?`)) return;
  const token = localStorage.getItem('admin_token');
  try {
    await axios.delete(`${baseUrl}/api/admin/users/${user.id}`, { headers: { Authorization: `Bearer ${token}` } });
    users.value = users.value.filter(u => u.id !== user.id);
  } catch (err) {
    console.error('Failed to delete user:', err);
  }
}

async function deleteProduct(product) {
  if (!confirm(`ยืนยันการลบสินค้า ${product.name}?`)) return;
  const token = localStorage.getItem('admin_token');
  try {
    await axios.delete(`${baseUrl}/api/admin/products/${product.id}`, { headers: { Authorization: `Bearer ${token}` } });
    products.value = products.value.filter(p => p.id !== product.id);
  } catch (err) {
    console.error('Failed to delete product:', err);
  }
}

// ------------------------------------------
// Actions: Orders
// ------------------------------------------
async function updateOrderStatus(order) {
  const token = localStorage.getItem('admin_token');
  try {
    await axios.put(`${baseUrl}/api/admin/orders/${order.id}/status`, 
      { status: order.status },
      { headers: { Authorization: `Bearer ${token}` } }
    );
  } catch (err) {
    console.error('Failed to update order status:', err);
  }
}

// ------------------------------------------
// Actions: Token Requests
// ------------------------------------------
async function approveToken(req) {
  if (!confirm(`อนุมัติ ${req.amount.toLocaleString()} Token ให้ ${req.user?.username}?`)) return;
  const token = localStorage.getItem('admin_token');
  const headers = { Authorization: `Bearer ${token}` };
  
  try {
    await axios.put(`${baseUrl}/api/admin/token-requests/${req.id}/approve`, {}, { headers });
    alert(`✅ อนุมัติสำเร็จ!`);
    fetchTokenRequests(headers);
  } catch (err) {
    alert(err.response?.data?.msg || 'อนุมัติไม่สำเร็จ');
  }
}

async function rejectToken(req) {
  const reason = prompt('ระบุเหตุผลในการปฏิเสธ (ถ้ามี):', '');
  if (reason === null) return;
  
  const token = localStorage.getItem('admin_token');
  const headers = { Authorization: `Bearer ${token}` };
  
  try {
    await axios.put(`${baseUrl}/api/admin/token-requests/${req.id}/reject`, { admin_note: reason || 'ไม่ผ่านการตรวจสอบ' }, { headers });
    alert(`❌ ปฏิเสธคำขอเรียบร้อยแล้ว`);
    fetchTokenRequests(headers);
  } catch (err) {
    alert(err.response?.data?.msg || 'ปฏิเสธไม่สำเร็จ');
  }
}

// ------------------------------------------
// Actions: Seller Verification
// ------------------------------------------
async function handleApproveSeller(id) {
  if (!confirm('ยืนยันที่จะอนุมัติร้านค้านี้?')) return;
  
  const token = localStorage.getItem('admin_token');
  const headers = { Authorization: `Bearer ${token}` };

  try {
    await axios.post(`${baseUrl}/api/admin/verify/${id}/approve`, {}, { headers });
    
    // Refresh List
    await fetchVerifications(headers);
    // Update stats immediately if possible
    stats.value.total_sellers = (stats.value.total_sellers || 0) + 1;
    
    alert('อนุมัติเรียบร้อย! ร้านค้าเปิดใช้งานได้แล้ว');
  } catch (error) {
    console.error(error);
    alert('เกิดข้อผิดพลาดในการอนุมัติ');
  }
}

async function handleRejectSeller(id) {
  const reason = prompt('กรุณาระบุเหตุผลที่ไม่อนุมัติ:');
  if (reason === null) return;

  const token = localStorage.getItem('admin_token');
  const headers = { Authorization: `Bearer ${token}` };

  try {
    await axios.post(`${baseUrl}/api/admin/verify/${id}/reject`, { reason }, { headers });
    
    // Refresh List
    await fetchVerifications(headers);
    alert('ปฏิเสธคำขอเรียบร้อย');
  } catch (error) {
    console.error(error);
    alert('เกิดข้อผิดพลาดในการปฏิเสธ');
  }
}

const openImageModal = (url) => {
  currentZoomImage.value = url;
  showImageModal.value = true;
};

// ------------------------------------------
// Lifecycle
// ------------------------------------------
function handleLogout() {
  localStorage.removeItem('admin_token');
  localStorage.removeItem('admin_user');
  router.push('/admin-login');
}

onMounted(() => {
  const storedAdmin = localStorage.getItem('admin_user');
  if (storedAdmin) {
    adminUser.value = JSON.parse(storedAdmin);
  }
  fetchData();
});
</script>

<style scoped>
/* Animations */
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-down {
  animation: fadeInDown 0.6s ease-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
  opacity: 0;
}

@keyframes pulse-slow {
  0%, 100% { opacity: 0.1; transform: scale(1); }
  50% { opacity: 0.2; transform: scale(1.1); }
}
.animate-pulse-slow {
  animation: pulse-slow 8s infinite ease-in-out;
}

/* Modal Fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Custom Scrollbar for tables */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>