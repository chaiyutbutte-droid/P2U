<template>
  <div
    class="min-h-screen flex flex-col items-center bg-gray-900 text-white p-6"
  >
    <!-- หัวข้อ -->
    <div
      class="text-center text-4xl font-semibold mb-10 hover:scale-110 underline"
    >
      Creator
    </div>

    <!-- แถวบน: 1 คน -->
    <div class="flex justify-center mb-10"></div>

    <!-- แถวกลาง: 2 คน -->
    <div class="flex flex-row flex-wrap justify-center gap-10 mb-10">
      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://scontent-bkk1-2.xx.fbcdn.net/v/t39.30808-1/548008636_2544388382627251_858633228946711615_n.jpg?stp=cp6_dst-jpg_s200x200_tt6&_nc_cat=100&ccb=1-7&_nc_sid=1d2534&_nc_eui2=AeHEQNo8723T0PJWKj9lLcccvL2XADkEONm8vZcAOQQ42VExKLG4ubjzUmQTGnH0vsF4PRLoAgPuhFJKrsBvpg7M&_nc_ohc=1CL6wTd3W0IQ7kNvwHzihVK&_nc_oc=Adk6Ld_b0tmtY2469HhEx1tNoLvrc6fwIWHp4YRqtYKVf6aeDVkffUHgbuiiBzMWXnY&_nc_zt=24&_nc_ht=scontent-bkk1-2.xx&_nc_gid=cKKQWKEgqCpKiln7umsJUw&oh=00_AfdTRrakeM1eCyidHxNx_VVfC1lkDzBHud0xdHKXywEHEQ&oe=690786C4"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">artuchicabo</p>
        <p class="text-gray-400 text-sm">Backend Engineer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://scontent-bkk1-2.xx.fbcdn.net/v/t39.30808-1/429816394_900921248434020_7135155605498280752_n.jpg?stp=dst-jpg_s200x200_tt6&_nc_cat=104&ccb=1-7&_nc_sid=1d2534&_nc_eui2=AeG5e89Lnl5kwImRYc2fz060_PoOUPfUdWP8-g5Q99R1Y_Mjte-1f8XgXBnzwJHORnf4y9izXVr_OsmuwMfzPRkU&_nc_ohc=3JEEmNj0r10Q7kNvwFwf5oW&_nc_oc=AdkJzFhQHywzYaqCaup2pUB6FZ9akCkmjYyOH5I9gcYXEllQc8aCNB7KjIwhFXSLRdM&_nc_zt=24&_nc_ht=scontent-bkk1-2.xx&_nc_gid=ma9wk5FULvj0cyTmAOiBwQ&oh=00_Afd0OYbSBWx_haoD6AAs9zUKUhntFIavDiswIZDZBzz-Eg&oe=69078EA1"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">Siranat Sribura </p>
        <p class="text-gray-400 text-sm">Frontend Developer</p>
      </div>
      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://scontent-bkk1-1.xx.fbcdn.net/v/t39.30808-6/503720930_122128294892836980_415354766661668842_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=a5f93a&_nc_eui2=AeHlW0Z2pbtNygZ3pilt-ax6gpci123hUriClyLXbeFSuOCZ9c-6hdhdbQy9qxw9B6rU0FPxXjfe_eibkXFGcSf8&_nc_ohc=Meaor4itlE0Q7kNvwEtVcOg&_nc_oc=Adn90yyj_G5wik3fhm5_I_IOqfCHChXnqKaYoZHoDHAJnnCFspKhwnjyAaeXBMUY8BI&_nc_zt=23&_nc_ht=scontent-bkk1-1.xx&_nc_gid=yOxwMf_WUYZg-zi6vHCETg&oh=00_AfdtMGIWFKpNkTcOjQwGvdMPkwLEyVIRb_buQbIbsAl-ew&oe=69077A35"
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
          src="https://scontent-bkk1-1.xx.fbcdn.net/v/t39.30808-6/486053140_674111098604536_4310822804207048139_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=94e2a3&_nc_eui2=AeFaNlefUUoYwuIG1CLTwkTrD-pzPrQZ5XAP6nM-tBnlcAVpZTdaAICKiMtZ5XZ5YGBrDhbzuguRydG4LXBLyGqn&_nc_ohc=t-LOudn3_cYQ7kNvwHk9wpj&_nc_oc=AdmWxxOEYKIgg3jfUPEClxU95F7H6vGKgTs7HDIFYQw9OoWhlvjnSE1f8iN0wSPTECE&_nc_zt=23&_nc_ht=scontent-bkk1-1.xx&_nc_gid=FdBlZAjF643BmPlXDpcpxw&oh=00_Afen9ifAEkZHm3o3CNJgEXIGvYB3J_BVTME02WRa0xLolQ&oe=69077B22"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">Baramee Pawalung</p>
        <p class="text-gray-400 text-sm">UI/UX Designer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://scontent-bkk1-2.xx.fbcdn.net/v/t39.30808-1/504754276_710683794701117_6879929705778053044_n.jpg?stp=dst-jpg_s200x200_tt6&_nc_cat=105&ccb=1-7&_nc_sid=e99d92&_nc_eui2=AeEH1AV3UnmBka2VaW3nQvj9jwwa8u2kIGKPDBry7aQgYm529LFKKMZeJ2VG3orr2MhBkE-zb-GmPcjG6o_Wicn3&_nc_ohc=D7_8yMG4f14Q7kNvwEmmLHL&_nc_oc=AdmivfHTXS5MI4h0gjEJybE-K6rKEM3IQ7D-s7XNTzdcw33HzQctCjo1M0fRfEq5Rek&_nc_zt=24&_nc_ht=scontent-bkk1-2.xx&_nc_gid=RrQCKtP7HJ-Ps0UMUFqWxw&oh=00_Afe-OKmsAdXbXfXfTLGYgK3sWUI635MlrKpPD7rvg0RmQQ&oe=69079105"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">Wirot Namwongsa </p>
        <p class="text-gray-400 text-sm">Backend Engineer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://scontent-bkk1-2.xx.fbcdn.net/v/t39.30808-1/387755162_343191124759000_597277197217838969_n.jpg?stp=dst-jpg_s200x200_tt6&_nc_cat=100&ccb=1-7&_nc_sid=1d2534&_nc_eui2=AeGkjtl5iWwJ6YguQnH8bXYy4GlDjo6rh23gaUOOjquHbfMzF0tgNCXwhdWPjNhf85hFMrWuM1stsTVINRIqQ0sS&_nc_ohc=IysSs9mQSXQQ7kNvwGBOAor&_nc_oc=Adnuds_Hy51Tu6LZEQc1DsuL3Mr-SBIJwb7KaXUQIEFUz4c2JMRSafdtKroAM04nnt4&_nc_zt=24&_nc_ht=scontent-bkk1-2.xx&_nc_gid=99d_KlGK617XhJGZzg_hsw&oh=00_AfdyI9fH6I798YOujNzmgvOf1KzymMf8mjjeLlgnqDk9Xg&oe=69077D72"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">Chetsada Suthong</p>
        <p class="text-gray-400 text-sm">Frontend Developer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://scontent-bkk1-1.xx.fbcdn.net/v/t39.30808-1/428597236_408098305205818_583484129208727829_n.jpg?stp=dst-jpg_s200x200_tt6&_nc_cat=109&ccb=1-7&_nc_sid=e99d92&_nc_eui2=AeHL0U5NnUv9OYwuRCpRV6UV4PjwDmAy1q_g-PAOYDLWr6iM9TrKspLBENjcuaF6lWe7Lq1c53KeymVtvhxi97HE&_nc_ohc=94iZ3KEu6TQQ7kNvwEi1o0q&_nc_oc=Adlp2zOaMQG6pSokkwKqBOAYBZagxRL50UAbnDbKe80OBU3xKpmX7V_RVaat5oguaL0&_nc_zt=24&_nc_ht=scontent-bkk1-1.xx&_nc_gid=DKVIh1j0CMVEJcmEtGMISQ&oh=00_Afd1s4PR1oO_7Tf5rO0Hzs_ZVlK-qISyfZPWttsqpAZ1gQ&oe=6907A221"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">Achirawit Phuangpila </p>
        <p class="text-gray-400 text-sm">UI/UX Designer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://scontent-bkk1-2.xx.fbcdn.net/v/t39.30808-6/497399332_682849621124436_1572872299627005691_n.jpg?_nc_cat=105&ccb=1-7&_nc_sid=a5f93a&_nc_eui2=AeErr14wyUna4E0c4i1k8FGs6lt9I119kg_qW30jXX2SD_d3QJXN81SSsSr_dNkaBvchKCfLAF22bwEyJLm3asE7&_nc_ohc=7phG1sNY0kEQ7kNvwFp4giM&_nc_oc=AdnlNtQ2g11CF-cE89mW1TnY47wIr_UGjCmYuWsKuteMM0nv_1f_PdJpsvujLOqnV6Q&_nc_zt=23&_nc_ht=scontent-bkk1-2.xx&_nc_gid=dudT5uzwUuygnX4_aAO7Ag&oh=00_AfdIEyy_W5kH7e2Xj7d87_hYQWuiJjLlsaHcFcGBdMWzLw&oe=69078971"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">Ynam Sod </p>
        <p class="text-gray-400 text-sm">UI/UX Designer</p>
      </div>

      <div class="flex flex-col items-center">
        <img
          class="w-40 h-40 rounded-full bg-gray-800 object-cover transition-all duration-300 ease-in-out hover:scale-110 hover:shadow-lg hover:shadow-blue-500/40"
          src="https://scontent-bkk1-1.xx.fbcdn.net/v/t39.30808-1/447697635_1519546438943923_959043828505910984_n.jpg?stp=dst-jpg_s100x100_tt6&_nc_cat=108&ccb=1-7&_nc_sid=1d2534&_nc_eui2=AeGRczQ7WlByzb0ZxYUL8tWVkOXKu9QgomGQ5cq71CCiYUB1xIOgQF07YzJvVZfa98DkZ6qM0ZIPLsV7cDIl173p&_nc_ohc=oj2gyOaBRYAQ7kNvwGeN-33&_nc_oc=AdnEEWP3ytoF9QTmGZ3JGxtRAIsol6KXyXZH8t5CUsnk4Q0Na76UntVmXDQiqKZex6M&_nc_ad=z-m&_nc_cid=0&_nc_zt=24&_nc_ht=scontent-bkk1-1.xx&_nc_gid=T2ToyGGf50gvOUfL4TkESg&oh=00_AfdNXS-EP87z7tGzjQQceAj28C2vh0lHCo9hIop0fdYZvw&oe=6907AB57"
          alt="profile image"
        />
        <p class="mt-4 text-xl font-semibold">F'film Patcharapon</p>
        <p class="text-gray-400 text-sm">UI/UX Designer</p>
      </div>
    </div>


  </div>
</template>
