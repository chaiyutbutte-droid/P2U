// stores/user.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,           // ข้อมูลผู้ใช้
    accessToken: null,    // Token สำหรับ API
    loading: false,       // สถานะกำลังโหลด
    error: null           // ข้อผิดพลาดล่าสุด
  }),
  getters: {
    isLoggedIn: (state) => !!state.accessToken,                 // เช็คล็อกอิน
    coinBalance: (state) => state.user?.coin_balance || 0       // จำนวนเหรียญ
  },
  actions: {
    // โหลดข้อมูลโปรไฟล์ผู้ใช้
    async fetchProfile() {
      if (!this.accessToken) return
      this.loading = true
      try {
        const res = await axios.get('http://localhost:5000/api/profile', {
          headers: { Authorization: `Bearer ${this.accessToken}` }
        })
        this.user = res.data
        this.error = null
      } catch (err) {
        console.error('fetchProfile error:', err)
        this.error = err.response?.data?.message || err.message
      } finally {
        this.loading = false
      }
    },

    // Login
    async login(username, password) {
      this.loading = true
      try {
        const res = await axios.post('http://localhost:5000/api/login', {
          username,
          password
        })
        this.accessToken = res.data.access_token
        this.user = res.data.user
        this.error = null
        // เก็บ token และ user ลง localStorage
        localStorage.setItem('token', this.accessToken)
        localStorage.setItem('user', JSON.stringify(this.user))
      } catch (err) {
        console.error('login error:', err)
        this.error = err.response?.data?.message || err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    // Logout
    logout() {
      this.user = null
      this.accessToken = null
      this.error = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    // Top-up coin
    async topupCoin(amount, paymentMethod = 'promptpay', cardToken = null) {
      if (!this.accessToken) throw new Error('User not logged in')
      this.loading = true
      try {
        const payload = { amount, payment_method: paymentMethod }
        if (paymentMethod === 'credit') payload.card_token = cardToken

        // ✅ เปลี่ยน endpoint ให้ตรงกับ backend
        const res = await axios.post(
          'http://localhost:5000/api/coin/topup',
          payload,
          { headers: { Authorization: `Bearer ${this.accessToken}` } }
        )

        // อัปเดต balance หลังเติมเงินสำเร็จ
        await this.fetchProfile()
        this.error = null
        return res.data   // { status, charge_id, payment_method, amount, charge_data }
      } catch (err) {
        console.error('topupCoin error:', err)
        this.error = err.response?.data?.message || err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    // โหลด user จาก localStorage (ใช้ตอน refresh หน้า)
    loadUserFromStorage() {
      const storedUser = localStorage.getItem('user')
      const storedToken = localStorage.getItem('token')
      if (storedUser && storedToken) {
        try {
          this.user = JSON.parse(storedUser)
          this.accessToken = storedToken
        } catch {
          this.user = null
          this.accessToken = null
        }
      }
    }
  }
})
