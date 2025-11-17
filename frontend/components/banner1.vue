<template>
  <div v-if="isDashboard" class="banner-container">
    <span v-text="currentText"></span>
  </div>
</template>

<script>
export default {
  data() {
    return {
      fullText: [
        
        'สินค้าคุณภาพมือสอง ราคาสุดคุ้ม ที่  P2U KAISER',
        'ใครว่า ของมือสองไม่ดี? ที่ P2U KAISER ของมือสองก็มีคุณภาพ!',
        'มุ่งเน้นไปที่การคัดเลือกสินค้ามือสองที่มีคุณภาพ'
      ],
      currentText: '',
      textIndex: 0,
      letterIndex: 0,
      typingSpeed: 100, // delay between typing characters (in milliseconds)
      pauseDuration: 1000, // delay before switching to the next sentence
    };
  },
  computed: {
    // ตรวจสอบว่าอยู่ในหน้า dashboard หรือไม่
    isDashboard() {
      return this.$route.path === '/dashboard';
    }
  },
  mounted() {
    if (this.isDashboard) {
      this.typeText(); // เริ่มพิมพ์ข้อความเมื่ออยู่ในหน้า dashboard
    }
  },
  methods: {
    typeText() {
      const currentLine = this.fullText[this.textIndex];
      const nextLetter = currentLine[this.letterIndex];

      this.currentText += nextLetter;
      this.letterIndex++;

      if (this.letterIndex < currentLine.length) {
        setTimeout(this.typeText, this.typingSpeed);
      } else {
        setTimeout(this.changeText, this.pauseDuration);
      }
    },
    changeText() {
      this.textIndex = (this.textIndex + 1) % this.fullText.length;
      this.letterIndex = 0;
      this.currentText = ''; // Reset the current text
      this.typeText(); // Start typing the next line
    }
  }
};
</script>

<style scoped>
.banner-container {
  font-size: 2.5vw;
  font-weight: bold;
  color: white;
  background-color:rgb(55, 2, 35);
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  padding: 20px;
  height: 20vh; /* Adjust container height */
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;  
}

span {
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7); /* Optional: adds shadow for readability */
}
</style>
