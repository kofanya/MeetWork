import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: null 
  }),

  actions: {
    async login(email, password) {
      const response = await fetch('/api/login', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      if (response.ok) {
        const data = await response.json()
        this.isAuthenticated = true
        this.user = {
          first_name: data.first_name,
          role: data.role
        }
        return true
      } else {
        const err = await response.json()
        throw new Error(err.message || 'Ошибка входа')
      }
    },

    async checkAuth() {
      try {
        const res = await fetch('/api/profile', { credentials: 'include' })
        if (res.ok) {
          const data = await res.json()
          this.isAuthenticated = true
          this.user = {
            first_name: data.data_user.first_name,
            role: data.data_user.role
          }
        } else {
          this.logoutLocal()
        }
      } catch (err) {
        console.warn('Auth check failed:', err)
        this.logoutLocal()
      }
    },

    logoutLocal() {
      this.isAuthenticated = false
      this.user = null
    },

    async logout() {
      try {
        await fetch('/api/logout', { method: 'GET', credentials: 'include' })
      } catch (err) {
        console.warn('Logout API error:', err)
      } finally {
        this.logoutLocal()
      }
    }
  }
})