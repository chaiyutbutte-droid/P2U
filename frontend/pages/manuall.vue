<template>
  <div class="container mx-auto p-6">
    <!-- Header with Category Name -->
    <div class="mb-8">
      <button 
        @click="goBack" 
        class="mb-4 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg flex items-center"
      >
        <span class="mr-2">←</span> กลับ
      </button>
      <h1 class="text-3xl font-bold text-white">{{ categoryName }}</h1>
    </div>

    <!-- Category Image -->
    <div class="mb-8">
      <img 
        v-if="categoryImage" 
        :src="categoryImage" 
        :alt="categoryName"
        class="w-full h-64 object-cover rounded-lg shadow-lg"
      />
    </div>

    <!-- Products Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div
        v-for="product in products"
        :key="product.id"
        class="bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow cursor-pointer"
        @click="viewProduct(product)"
      >
        <!-- Product Image -->
        <img
          v-if="product.image"
          :src="product.image"
          :alt="product.name"
          class="w-full h-48 object-cover"
        />
        <div v-else class="w-full h-48 bg-gray-700 flex items-center justify-center">
          <p class="text-gray-400">ไม่มีภาพ</p>
        </div>

        <!-- Product Info -->
        <div class="p-4">
          <h3 class="text-lg font-semibold text-white mb-2">{{ product.name }}</h3>
          <p class="text-gray-300 text-sm mb-3">{{ product.description }}</p>
          
          <!-- Price -->
          <div class="flex justify-between items-center mb-3">
            <span class="text-2xl font-bold text-green-400">฿{{ product.price }}</span>
            <span class="text-sm text-gray-400">{{ product.stock }} ชิ้น</span>
          </div>

          <!-- Rating -->
          <div class="flex items-center mb-4">
            <span class="text-yellow-400">★</span>
            <span class="text-gray-300 ml-1">{{ product.rating }} ({{ product.reviews }} รีวิว)</span>
          </div>

          <!-- Action Button -->
          <button 
            @click.stop="addToCart(product)"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg transition-colors"
          >
            เพิ่มลงตะกร้า
          </button>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="products.length === 0" class="text-center py-12">
      <p class="text-gray-400 text-lg">ไม่มีสินค้าในหมวดหมู่นี้</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categoryId: null,
      categoryName: '',
      categoryImage: '',
      products: [],
      // ตัวอย่างสินค้าสำหรับแต่ละหมวดหมู่
      categoryProducts: {
        1: { // ความงามและของใช้ส่วนตัว
          name: 'ความงามและของใช้ส่วนตัว',
          image: 'https://kengklongkwang.com/assets/image/typeshop/shop02.jpg',
          products: [
            {
              id: 1,
              name: 'ครีมบำรุงผิว',
              description: 'ครีมบำรุงผิวแบบหนักสำหรับผิวแห้ง',
              price: 399,
              stock: 45,
              rating: 4.5,
              reviews: 123,
              image: 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400'
            },
            {
              id: 2,
              name: 'เซรั่มหน้า',
              description: 'เซรั่มเข้มข้นลดริ้วรอย',
              price: 599,
              stock: 32,
              rating: 4.8,
              reviews: 87,
              image: 'https://images.unsplash.com/photo-1556228541-2ba06a5beds9?w=400'
            },
            {
              id: 3,
              name: 'มาสก์หน้า',
              description: 'มาสก์ทำความสะอาดลึก',
              price: 249,
              stock: 60,
              rating: 4.3,
              reviews: 156,
              image: 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400'
            }
          ]
        },
        2: { // เสื้อผ้า
          name: 'เสื้อผ้า',
          image: 'https://inwfile.com/s-a/ykvfac.jpg',
          products: [
            {
              id: 4,
              name: 'เสื้อยืดสีดำ',
              description: 'เสื้อยืดคุณภาพดี 100% cotton',
              price: 299,
              stock: 120,
              rating: 4.6,
              reviews: 234,
              image: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400'
            },
            {
              id: 5,
              name: 'กางเกง Jeans',
              description: 'กางเกงยีนส์สีฟ้าคลาสสิก',
              price: 799,
              stock: 85,
              rating: 4.7,
              reviews: 198,
              image: 'https://images.unsplash.com/photo-1542272604-787c62d465d1?w=400'
            },
            {
              id: 6,
              name: 'เสื้อเชิ้ตสีขาว',
              description: 'เสื้อเชิ้ตฟอร์มัล',
              price: 549,
              stock: 65,
              rating: 4.4,
              reviews: 102,
              image: 'https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=400'
            }
          ]
        },
        3: { // กระเป๋า
          name: 'กระเป๋า',
          image: 'https://jellybunny.com/cdn/shop/products/B23WBHI100_BLK000_1.jpg?v=1728372713',
          products: [
            {
              id: 7,
              name: 'กระเป๋าเป้สไตล์ทุกวัน',
              description: 'กระเป๋าเป้ใบใหญ่พร้อมช่องเยอะ',
              price: 899,
              stock: 40,
              rating: 4.7,
              reviews: 145,
              image: 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400'
            },
            {
              id: 8,
              name: 'กระเป๋าสะพายข้าง',
              description: 'กระเป๋าหนัง PU สีดำ',
              price: 1299,
              stock: 25,
              rating: 4.8,
              reviews: 89,
              image: 'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=400'
            },
            {
              id: 9,
              name: 'กระเป๋าคลัตช์',
              description: 'กระเป๋าคลัตช์สำหรับงานปาร์ตี้',
              price: 599,
              stock: 50,
              rating: 4.5,
              reviews: 76,
              image: 'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400'
            }
          ]
        },
        4: { // รองเท้า
          name: 'รองเท้า',
          image: 'https://www.central.co.th/_next/image?url=https%3A%2F%2Fassets.central.co.th%2Ffile-assets%2FCDSPIM%2Fweb%2FImage%2FMKP1855%2FELLE-WomenSandalsELSM002BLBlack-MKP1855913-1.webp&w=1080&q=75',
          products: [
            {
              id: 10,
              name: 'รองเท้าผ้าใบสีขาว',
              description: 'รองเท้าผ้าใบคลาสสิก',
              price: 1499,
              stock: 78,
              rating: 4.6,
              reviews: 201,
              image: 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400'
            },
            {
              id: 11,
              name: 'รองเท้าส้นสูง',
              description: 'รองเท้าส้นสูง 7 ซม.',
              price: 1999,
              stock: 35,
              rating: 4.7,
              reviews: 112,
              image: 'https://images.unsplash.com/photo-1514707502007-3177e70ab26e?w=400'
            },
            {
              id: 12,
              name: 'รองเท้าแตะ',
              description: 'รองเท้าแตะสะบัก',
              price: 399,
              stock: 150,
              rating: 4.4,
              reviews: 234,
              image: 'https://images.unsplash.com/photo-1503541273019-a5a31904d7fd?w=400'
            }
          ]
        },
        5: { // นาฬิกาและแว่นตา
          name: 'นาฬิกาและแว่นตา',
          image: 'https://www.10อันดับรุ่นไหนดี.com/wp-content/uploads/Garmin-Venu-3-series.jpg',
          products: [
            {
              id: 13,
              name: 'นาฬิกาข้อมือสไตล์',
              description: 'นาฬิกาควอตซ์ สีดำ',
              price: 2499,
              stock: 30,
              rating: 4.7,
              reviews: 98,
              image: 'https://images.unsplash.com/photo-1523170335258-f5ed11844a49?w=400'
            },
            {
              id: 14,
              name: 'แว่นตากันแดด',
              description: 'แว่นตากันแดด UV400',
              price: 999,
              stock: 55,
              rating: 4.6,
              reviews: 167,
              image: 'https://images.unsplash.com/photo-1513527282212-8f6c34652b41?w=400'
            },
            {
              id: 15,
              name: 'แว่นตาอ่านหนังสือ',
              description: 'แว่นสายตา prescription',
              price: 1299,
              stock: 42,
              rating: 4.5,
              reviews: 134,
              image: 'https://images.unsplash.com/photo-1508296695146-367ee2ab691b?w=400'
            }
          ]
        },
        6: { // อุปกรณ์อิเล็กทรอนิกส์
          name: 'อุปกรณ์อิเล็กทรอนิกส์',
          image: 'https://klang-ic.com/assets/upload/1660096813.jpg',
          products: [
            {
              id: 16,
              name: 'หูฟังไร้สาย',
              description: 'หูฟัง Bluetooth สำหรับเพลง',
              price: 1999,
              stock: 48,
              rating: 4.7,
              reviews: 223,
              image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400'
            },
            {
              id: 17,
              name: 'แบตเตอรี่สำรอง',
              description: 'Power bank 20000 mAh',
              price: 699,
              stock: 92,
              rating: 4.6,
              reviews: 189,
              image: 'https://images.unsplash.com/photo-1609042231488-6a73db45b4c4?w=400'
            },
            {
              id: 18,
              name: 'สายชาร์จ USB-C',
              description: 'สายชาร์จขาว 2 เมตร',
              price: 199,
              stock: 180,
              rating: 4.4,
              reviews: 301,
              image: 'https://images.unsplash.com/photo-1625948515291-69613efd103f?w=400'
            }
          ]
        },
        7: { // มือถือและแท็บเล็ต
          name: 'มือถือและแท็บเล็ต',
          image: 'https://www.ktc.co.th/pub/media/Article/01/Tablet_TeclastP80.webp',
          products: [
            {
              id: 19,
              name: 'ฟิล์มกระจกมือถือ',
              description: 'ฟิล์มกระจกนิรภัย 9H',
              price: 149,
              stock: 250,
              rating: 4.5,
              reviews: 456,
              image: 'https://images.unsplash.com/photo-1591493814101-718b4c5a8580?w=400'
            },
            {
              id: 20,
              name: 'เคสมือถือ',
              description: 'เคสซิลิโคนสีดำ',
              price: 299,
              stock: 210,
              rating: 4.6,
              reviews: 334,
              image: 'https://images.unsplash.com/photo-1592286927505-1fed6c3d379c?w=400'
            },
            {
              id: 21,
              name: 'ขาตั้งแท็บเล็ต',
              description: 'ขาตั้งปรับได้หลายมุม',
              price: 399,
              stock: 75,
              rating: 4.7,
              reviews: 145,
              image: 'https://images.unsplash.com/photo-1527814050087-3793815479db?w=400'
            }
          ]
        }
      }
    };
  },
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    viewProduct(product) {
      this.$router.push({
        path: '/product-detail',
        query: { id: product.id, name: product.name }
      });
    },
    addToCart(product) {
      alert(`เพิ่ม "${product.name}" ลงในตะกร้าแล้ว!`);
      // TODO: เพิ่มลงใน Vuex store หรือ Pinia store
    }
  },
  mounted() {
    // ดึงข้อมูล categoryId จาก URL query
    const categoryId = parseInt(this.$route.query.id);
    const categoryName = this.$route.query.name;
    const categoryImage = this.$route.query.image;
    
    this.categoryId = categoryId;
    this.categoryName = categoryName;
    this.categoryImage = categoryImage;
    
    // โหลดสินค้าตามหมวดหมู่
    if (this.categoryProducts[categoryId]) {
      const category = this.categoryProducts[categoryId];
      this.products = category.products;
    }
  }
};
</script>

<style scoped>
.container {
  background-color: #1a1a1a;
  min-height: 100vh;
}
</style>