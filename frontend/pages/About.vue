<template>
  <div class="bg-gray-900 text-white min-h-screen">
    <!-- ✅ Navbar --- >

    <!-- ✅ Hero Section -->
    <section class="text-center py-16 px-6">
      <h1 class="text-4xl font-extrabold text-indigo-400 mb-4">
        About Our Marketplace
      </h1>
      <p class="text-gray-300 text-lg max-w-3xl mx-auto leading-relaxed">
        แพลตฟอร์มของเราถูกสร้างขึ้นเพื่อเชื่อมโยงผู้ซื้อและผู้ขายเข้าด้วยกัน
        ด้วยระบบที่ปลอดภัย ใช้งานง่าย และมอบประสบการณ์ที่ดีที่สุดในการช้อปปิ้งออนไลน์
      </p>
    </section>

    <!-- ✅ Mission Section -->
    <section class="grid md:grid-cols-2 gap-12 items-center px-8 md:px-20 py-16">
      <div>
        <h2 class="text-3xl font-bold text-indigo-300 mb-4">Our Mission</h2>
        <p class="text-gray-400 leading-relaxed">
          เป้าหมายของเราคือการสร้างชุมชนออนไลน์ที่เชื่อถือได้สำหรับทุกคน
          โดยเน้นความโปร่งใส ความสะดวกสบาย และการสนับสนุนผู้ประกอบการรายย่อยให้เติบโต
          พร้อมมอบประสบการณ์การซื้อขายที่ปลอดภัยและน่าเชื่อถือ
        </p>
      </div>
      <img
        src="https://images.unsplash.com/photo-1581092334107-22c37b2a5f2d"
        alt="Mission"
        class="rounded-2xl shadow-lg object-cover w-full h-80"
      />
    </section>

    <!-- ✅ Vision Section -->
    <section class="grid md:grid-cols-2 gap-12 items-center px-8 md:px-20 py-16 bg-gray-800">
      <img
        src="https://images.unsplash.com/photo-1591696205602-2f950c417cb9"
        alt="Vision"
        class="rounded-2xl shadow-lg object-cover w-full h-80 order-2 md:order-1"
      />
      <div class="order-1 md:order-2">
        <h2 class="text-3xl font-bold text-indigo-300 mb-4">Our Vision</h2>
        <p class="text-gray-400 leading-relaxed">
          เราเชื่อว่าเทคโนโลยีสามารถยกระดับคุณภาพชีวิตของผู้คนได้
          Marketplace ของเราจะเป็นจุดเริ่มต้นของเศรษฐกิจดิจิทัลที่ทุกคนเข้าถึงได้
          และสร้างรายได้อย่างยั่งยืนในอนาคต
        </p>
      </div>
    </section>

    <!-- ✅ Team Section -->
    <section class="text-center py-20 px-8 md:px-20">
      <h2 class="text-3xl font-bold text-indigo-400 mb-10">Meet Our Team</h2>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-10">
        <div class="bg-gray-800 p-6 rounded-xl shadow-lg hover:shadow-indigo-500/20 transition">
          <img
            src="https://randomuser.me/api/portraits/men/75.jpg"
            alt="Team Member"
            class="w-32 h-32 mx-auto rounded-full object-cover mb-4"
          />
          <h3 class="text-xl font-semibold">Achirawit Phungpila</h3>
          <p class="text-indigo-300">Founder & Developer</p>
          <p class="text-gray-400 mt-2 text-sm">
            ผู้สร้างแพลตฟอร์มและระบบหลังบ้าน ดูแลทุกขั้นตอนในการพัฒนาเว็บไซต์
          </p>
        </div>

        <div class="bg-gray-800 p-6 rounded-xl shadow-lg hover:shadow-indigo-500/20 transition">
          <img
            src="https://randomuser.me/api/portraits/women/68.jpg"
            alt="Team Member"
            class="w-32 h-32 mx-auto rounded-full object-cover mb-4"
          />
          <h3 class="text-xl font-semibold">Ploy Sirin</h3>
          <p class="text-indigo-300">UI/UX Designer</p>
          <p class="text-gray-400 mt-2 text-sm">
            ออกแบบประสบการณ์ผู้ใช้ให้สวยงาม ใช้งานง่าย และตอบโจทย์ผู้บริโภค
          </p>
        </div>

        <div class="bg-gray-800 p-6 rounded-xl shadow-lg hover:shadow-indigo-500/20 transition">
          <img
            src="https://randomuser.me/api/portraits/men/22.jpg"
            alt="Team Member"
            class="w-32 h-32 mx-auto rounded-full object-cover mb-4"
          />
          <h3 class="text-xl font-semibold">Napat Chai</h3>
          <p class="text-indigo-300">AI Data Analyst</p>
          <p class="text-gray-400 mt-2 text-sm">
            พัฒนาโมเดล AI สำหรับวิเคราะห์ข้อมูลการขายและการจัดอันดับผู้ขาย
          </p>
        </div>
      </div>
    </section>

    <!-- ✅ Footer -->
    <footer class="text-center border-t border-gray-700 py-6 mt-10 text-gray-400">
      © 2025 Our Marketplace. All rights reserved.
    </footer>
  </div>
</template>

<script setup>
// ไม่มี logic ในหน้านี้ เป็น static layout
</script>

<style scoped>
/* สามารถเพิ่ม transition หรือ animation เพิ่มเติมภายหลังได้ */
</style>
