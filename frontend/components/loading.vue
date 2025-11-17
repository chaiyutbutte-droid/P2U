<template>
  <div class="transition-overlay">
    <div class="transition-content">
      <!-- Simple elegant animation -->
      <div class="icon-container">
        <div class="success-checkmark">
          <div class="check-icon">
            <span class="icon-line line-tip"></span>
            <span class="icon-line line-long"></span>
            <div class="icon-circle"></div>
            <div class="icon-fix"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const message = ref('Login Successful!');

onMounted(() => {
  // This component will be shown for just 2-3 seconds
  // The parent component controls when to hide it and redirect
});
</script>

<style scoped>
.transition-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgb(55, 1, 30) 0%, rgb(35, 1, 20) 100%);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.transition-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Success Checkmark Animation */
.icon-container {
  margin-bottom: 1rem;
}

.success-checkmark {
  width: 100px;
  height: 100px;
  margin: 0 auto;
}

.check-icon {
  width: 100px;
  height: 100px;
  position: relative;
  border-radius: 50%;
  box-sizing: content-box;
  border: 4px solid rgba(236, 72, 153, 0.3);
}

.icon-line {
  height: 5px;
  background-color: #ec4899;
  display: block;
  border-radius: 2px;
  position: absolute;
  z-index: 10;
}

.line-tip {
  top: 46px;
  left: 14px;
  width: 25px;
  transform: rotate(45deg);
  animation: icon-line-tip 0.75s;
}

.line-long {
  top: 38px;
  right: 8px;
  width: 47px;
  transform: rotate(-45deg);
  animation: icon-line-long 0.75s;
}

.icon-circle {
  top: -4px;
  left: -4px;
  z-index: 10;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  position: absolute;
  box-sizing: content-box;
  border: 4px solid #ec4899;
  animation: icon-circle 1s ease-in-out;
}

.icon-fix {
  top: 8px;
  width: 5px;
  left: 26px;
  z-index: 1;
  height: 85px;
  position: absolute;
  transform: rotate(-45deg);
  background-color: rgb(55, 1, 30);
}

@keyframes icon-line-tip {
  0% {
    width: 0;
    left: 1px;
    top: 19px;
  }
  54% {
    width: 0;
    left: 1px;
    top: 19px;
  }
  70% {
    width: 50px;
    left: -8px;
    top: 37px;
  }
  84% {
    width: 17px;
    left: 21px;
    top: 48px;
  }
  100% {
    width: 25px;
    left: 14px;
    top: 46px;
  }
}

@keyframes icon-line-long {
  0% {
    width: 0;
    right: 46px;
    top: 54px;
  }
  65% {
    width: 0;
    right: 46px;
    top: 54px;
  }
  84% {
    width: 55px;
    right: 0px;
    top: 35px;
  }
  100% {
    width: 47px;
    right: 8px;
    top: 38px;
  }
}

@keyframes icon-circle {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Text Styles */
.transition-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  margin: 0;
  animation: textFadeIn 0.6s ease-out 0.3s both;
}

.transition-subtitle {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0;
  animation: textFadeIn 0.6s ease-out 0.5s both;
}

@keyframes textFadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .transition-title {
    font-size: 2rem;
  }
  
  .transition-subtitle {
    font-size: 1rem;
  }
  
  .success-checkmark {
    width: 80px;
    height: 80px;
  }
  
  .check-icon {
    width: 80px;
    height: 80px;
  }
  
  .icon-circle {
    width: 80px;
    height: 80px;
  }
}
</style>