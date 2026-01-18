<template>
  <div class="verification-badge inline-flex items-center gap-1">
    <!-- Email Verified -->
    <span 
      v-if="emailVerified" 
      class="badge email"
      title="Email ยืนยันแล้ว"
    >
      📧
    </span>

    <!-- Phone Verified -->
    <span 
      v-if="phoneVerified" 
      class="badge phone"
      title="เบอร์โทรยืนยันแล้ว"
    >
      📱
    </span>

    <!-- ID Verified (Trusted Seller) -->
    <span 
      v-if="idVerified" 
      class="badge id"
      title="ผู้ขายที่ได้รับการยืนยัน"
    >
      💎
    </span>

    <!-- Full Badge Display Mode -->
    <template v-if="showLabel">
      <span 
        v-if="verificationLevel === 'full'" 
        class="label-badge full"
      >
        💎 Trusted Seller
      </span>
      <span 
        v-else-if="verificationLevel === 'partial'" 
        class="label-badge partial"
      >
        ✓ Verified
      </span>
      <span 
        v-else-if="verificationLevel === 'basic'" 
        class="label-badge basic"
      >
        📧 Email Verified
      </span>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  emailVerified: {
    type: Boolean,
    default: false
  },
  phoneVerified: {
    type: Boolean,
    default: false
  },
  idVerified: {
    type: Boolean,
    default: false
  },
  showLabel: {
    type: Boolean,
    default: false
  }
});

const verificationLevel = computed(() => {
  if (props.idVerified) return 'full';
  if (props.phoneVerified) return 'partial';
  if (props.emailVerified) return 'basic';
  return 'none';
});
</script>

<style scoped>
.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.25rem;
  height: 1.25rem;
  font-size: 0.7rem;
  border-radius: 50%;
  cursor: help;
}

.badge.email {
  background: rgba(59, 130, 246, 0.2);
}

.badge.phone {
  background: rgba(34, 197, 94, 0.2);
}

.badge.id {
  background: rgba(168, 85, 247, 0.2);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.label-badge {
  font-size: 0.75rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-weight: 500;
}

.label-badge.full {
  background: linear-gradient(135deg, rgba(168, 85, 247, 0.3), rgba(236, 72, 153, 0.3));
  color: #e879f9;
  border: 1px solid rgba(168, 85, 247, 0.5);
}

.label-badge.partial {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.label-badge.basic {
  background: rgba(59, 130, 246, 0.2);
  color: #60a5fa;
  border: 1px solid rgba(59, 130, 246, 0.3);
}
</style>
