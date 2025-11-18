<template>
  <div class="help-page">
    <!-- Header Section -->
    <section class="hero">
      <div class="container">
        <h1 class="title">ศูนย์ช่วยเหลือ</h1>
        <p class="subtitle">ยินดีต้อนรับสู่ศูนย์ช่วยเหลือของเรา เรายินดีที่จะช่วยเหลือคุณ</p>
        
        <!-- Search Box -->
        <div class="search-box">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="ค้นหาคำถามที่พบบ่อย..."
            class="search-input"
          />
          <button class="search-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
          </button>
        </div>
      </div>
    </section>

    <!-- FAQ Accordion -->
    <section class="faq-section">
      <div class="container">
        <h2 class="section-title">คำถามที่พบบ่อย (FAQ)</h2>
        <div class="faq-list">
          <div 
            v-for="(faq, index) in filteredFaqs" 
            :key="index"
            class="faq-item"
          >
            <div 
              class="faq-question"
              @click="toggleFaq(index)"
            >
              <h3>{{ faq.question }}</h3>
              <span class="faq-icon">{{ openFaq === index ? '−' : '+' }}</span>
            </div>
            <transition name="fade">
              <div v-if="openFaq === index" class="faq-answer">
                <p>{{ faq.answer }}</p>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const searchQuery = ref('')
const openFaq = ref(null)
const selectedCategory = ref(null)

const faqs = [
  {
    question: 'จะสมัครสมาชิกได้อย่างไร?',
    answer: 'คุณสามารถสมัครสมาชิกได้โดยคลิกที่ปุ่ม "สมัครสมาชิก" ที่มุมขวาบนของหน้าเว็บ จากนั้นกรอกข้อมูลที่จำเป็นและยืนยันอีเมลของคุณ',
    category: 1
  },
  {
    question: 'ลืมรหัสผ่านต้องทำอย่างไร?',
    answer: 'คลิกที่ "ลืมรหัสผ่าน" ในหน้าเข้าสู่ระบบ แล้วป้อนอีเมลที่ใช้สมัครสมาชิก เราจะส่งลิงก์รีเซ็ตรหัสผ่านไปให้คุณทางอีเมล',
    category: 3
  },
  {
    question: 'มีวิธีการชำระเงินอะไรบ้าง?',
    answer: 'เรารับชำระเงินผ่านบัตรเครดิต/เดบิต, โอนเงินผ่านธนาคาร, พร้อมเพย์ และ TrueMoney Wallet',
    category: 2
  },
  {
    question: 'ข้อมูลของฉันปลอดภัยหรือไม่?',
    answer: 'ข้อมูลของคุณได้รับการเข้ารหัสและปกป้องด้วยมาตรฐาน SSL 256-bit เราปฏิบัติตามมาตรฐาน PDPA อย่างเคร่งครัด',
    category: 4
  },
  {
    question: 'สามารถยกเลิกบริการได้หรือไม่?',
    answer: 'คุณสามารถยกเลิกบริการได้ทุกเมื่อจากหน้าตั้งค่าบัญชี โดยไม่มีค่าธรรมเนียมการยกเลิก',
    category: 3
  }
]

const filteredFaqs = computed(() => {
  let filtered = faqs
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(faq => 
      faq.question.toLowerCase().includes(query) ||
      faq.answer.toLowerCase().includes(query)
    )
  }
  return filtered
})
const toggleFaq = (index) => {
  openFaq.value = openFaq.value === index ? null : index
}

</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Hero Section */
.hero {
  background:rgb(28, 27, 41);
  color: white;
  padding: 80px 20px;
  text-align: center;
}

.title {
  font-size: 3rem;
  margin-bottom: 15px;
  font-weight: 700;
}

.subtitle {
  font-size: 1.2rem;
  margin-bottom: 40px;
  opacity: 0.95;
}

.search-box {
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  background: white;
  border-radius: 50px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

.search-input {
  flex: 1;
  padding: 18px 30px;
  border: none;
  font-size: 1rem;
  outline: none;
  color: #333;
}

.search-btn {
  background: #d32f66;
  border: none;
  padding: 0 30px;
  cursor: pointer;
  color: white;
  transition: background 0.3s;
}

.search-btn:hover {
  background: rgb(232, 62, 133);
}

/* Section Title */
.section-title {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 50px;
  color: #ffffff;
  font-weight: 600;
}

/* FAQ Section */
.faq-section {
  padding: 80px 20px;
  background: #7b133b;
}

.faq-list {
  max-width: 900px;
  margin: 0 auto;
}

.faq-item {
  background: rgb(255, 255, 255);
  margin-bottom: 15px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.faq-question {
  padding: 25px 30px;
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: background 0.3s;
}

.faq-question:hover {
  background: #f8f9fa;
}

.faq-question h3 {
  font-size: 1.1rem;
  color: #2c3e50;
  font-weight: 600;
}

.faq-icon {
  font-size: 1.5rem;
  color: #667eea;
  font-weight: 300;
}

.faq-answer {
  padding: 0 30px 25px 30px;
  color: #6c757d;
  line-height: 1.8;
  animation: fadeIn 0.3s;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

</style>