<template>
  <div
    class="min-h-screen flex flex-col items-center bg-gray-900 text-white p-6"
  >
    <!-- หัวข้อ -->
    <div
      class="text-center text-4xl font-semibold mb-10 hover:scale-110 underline"
    >
      ผู้จัดทำ
    </div>

    <!-- แถวบน: 1 คน -->
    <div class="flex justify-center mb-10"></div>

    <!-- แถวกลาง: 2 คน -->
    <div class="flex flex-row flex-wrap justify-center gap-10 mb-10">
      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://preview.redd.it/dsewiphvdro61.jpg?width=640&crop=smart&auto=webp&s=a86be7602aafcb495b4b3c22a5dc370bb84f1d2e"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">artuchicabo</p>
        <p class="text-gray-400 text-sm">UI/UX Designer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://th.bing.com/th/id/OIP.7YRpGFsh-vOHh9oN9GgKuwHaEK?o=7rm=3&rs=1&pid=ImgDetMain&o=7&rm=3"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">au import</p>
        <p class="text-gray-400 text-sm">UI/UX Designer</p>
      </div>
      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://th.bing.com/th/id/OIP.vO7NLMlS5eGQzc2dUJyk8QHaEz?o=7rm=3&rs=1&pid=ImgDetMain&o=7&rm=3"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">frame kaiser</p>
        <p class="text-gray-400 text-sm">Frontend Developer</p>
      </div>
    </div>

    <!-- แถวล่าง: 7 คน -->
    <div class="flex flex-row flex-wrap justify-center gap-10">
      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://m.yodycdn.com/blog/jerry-meme-yodyvn36.jpg"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">Jane Smith</p>
        <p class="text-gray-400 text-sm">UI/UX Designer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://voz.vn/attachments/1652677583826-png.1160639/"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">Alex Carter</p>
        <p class="text-gray-400 text-sm">Backend Engineer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://tse1.mm.bing.net/th/id/OIP.2mnv-xaJUjEbdT3BLkhmuwAAAA?rs=1&pid=ImgDetMain&o=7&rm=3"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">John Doe</p>
        <p class="text-gray-400 text-sm">Frontend Developer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://tse3.mm.bing.net/th/id/OIP.OoDnLBISEFAHNPFkq3CKtwAAAA?rs=1&pid=ImgDetMain&o=7&rm=3"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">Jane Smith</p>
        <p class="text-gray-400 text-sm">UI/UX Designer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://i.pinimg.com/originals/af/be/4c/afbe4c043ea771adb6e3efdff15a6602.jpg"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">Jane Smith</p>
        <p class="text-gray-400 text-sm">UI/UX Designer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://th.bing.com/th/id/OIP.SPPf_fRlCy3Le5XJLEPwwwHaD4?o=7rm=3&rs=1&pid=ImgDetMain&o=7&rm=3"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">Jane Smith</p>
        <p class="text-gray-400 text-sm">UI/UX Designer</p>
      </div>
    </div>

    <!-- ข้อความตอนท้าย -->
    <div class="max-w-3xl mt-12 text-center">
      <p class="text-gray-300 text-lg leading-relaxed italic">
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Repellat et
        cupiditate autem nulla velit distinctio iste in similique? Et laudantium
        doloremque modi corporis perferendis, quae fugit aperiam animi aliquam
        blanditiis.
      </p>
    </div>
  </div>
</template>
