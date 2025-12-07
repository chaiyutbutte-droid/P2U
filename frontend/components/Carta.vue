<template>
  <div class="category-container text-center mt-12">
    <h1 class="text-2xl font-bold mb-6">หมวดหมู่</h1>

    <div class="category grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6 p-6">
      <div
        v-for="(item, index) in categories"
        :key="index"
        class="item bg-gray-800 hover:bg-gray-700  border-2 p-4 rounded-xl shadow-lg text-center relative cursor-pointer"
        @click="goToCategory(item)"
      >
        <!-- แสดงภาพจาก URL หรือข้อความ "ไม่มีภาพ" -->
        <img
          v-if="item.image"
          :src="item.image"
          alt="Category Image"
          class="w-full h-32 object-cover mb-4 rounded-md"
        />
        <p v-else class="text-white text-xs">ไม่มีภาพ</p>

        <p class="mt-3 text-md text-white font-semibold">{{ item.name }}</p>
     
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categories: [
        {
          id: 1,
          name: 'ความงามและของใช้ส่วนตัว',
   
          image: 'https://kengklongkwang.com/assets/image/typeshop/shop02.jpg',
        },
        {
          id: 2,
          name: 'เสื้อผ้า',
         
          image: 'https://inwfile.com/s-a/ykvfac.jpg', 
        },
        {
          id: 3,
          name: 'กระเป๋า',
          
          image: 'https://jellybunny.com/cdn/shop/products/B23WBHI100_BLK000_1.jpg?v=1728372713',
        },
        {
          id: 4,
          name: 'รองเท้า',
  
          image: 'https://www.central.co.th/_next/image?url=https%3A%2F%2Fassets.central.co.th%2Ffile-assets%2FCDSPIM%2Fweb%2FImage%2FMKP1855%2FELLE-WomenSandalsELSM002BLBlack-MKP1855913-1.webp&w=1080&q=75',
        },
        {
          id: 5,
          name: 'นาฬิกาและแว่นตา',
         
          image: 'https://www.10อันดับรุ่นไหนดี.com/wp-content/uploads/Garmin-Venu-3-series.jpg',
        },
        {
          id: 6,
          name: 'อุปกรณ์อิเล็กทรอนิกส์',
        
          image: 'https://klang-ic.com/assets/upload/1660096813.jpg',
        },
        {
          id: 7,
          name: 'มือถือและแท็บเล็ต',
        
          image: 'https://www.ktc.co.th/pub/media/Article/01/Tablet_TeclastP80.webp',
        }
      ]
    };
  },
  methods: {
    goToCategory(item) {
      this.$router.push({
        path: '/manuall',
        query: { 
          id: item.id, 
          name: item.name,
          image: item.image
        }
      });
    }
  }
};
</script>

<style scoped>
.category-container {
  margin-top: 50px;
}

.category {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 30px;
  justify-content: center;
  padding: 20px;
}

.item {
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  text-align: center;
  color: white;
  transition: transform 0.2s ease;
}

.item:hover {
  transform: scale(1.1);
}

</style>