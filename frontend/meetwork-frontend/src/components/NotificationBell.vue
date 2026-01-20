<template>
  <div class="notification-bell" @click.stop="toggleDropdown">
    <div style="position: relative; cursor: pointer;">
      <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
      </svg>
      <span v-if="unreadCount > 0" class="badge"></span>
    </div>

    <div v-if="isOpen" class="dropdown" ref="dropdown">
      <div class="dropdown-header">
        Уведомления
        <button v-if="unreadCount > 0" @click.stop="markAllAsRead" class="mark-read-all-btn">
          Отметить всё
        </button>
      </div>
      
      <div v-if="notifications.length === 0" class="empty">Нет уведомлений</div>
      
      <div v-else class="notifications-list">
        <div 
          v-for="notif in notifications" 
          :key="notif.id" 
          class="notification-item"
          :class="{ 'unread': !notif.is_read }"
        >
          <div class="notif-title">{{ notif.title }}</div>
          <div class="notif-message">{{ notif.message }}</div>
          <div class="notif-date">{{ formatDate(notif.date) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isOpen = ref(false)
const dropdown = ref(null)
const notifications = ref([])

// Количество непрочитанных
const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.is_read).length
})

// Форматирование даты
const formatDate = (dateStr) => {
  const date = new Date(dateStr)
  const now = new Date()
  const diffMs = now - date
  const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
  if (diffHours < 1) return 'только что'
  if (diffHours < 24) return `${diffHours} ч назад`
  return date.toLocaleDateString('ru-RU')
}

// Загрузка уведомлений
const loadNotifications = async () => {
  if (!authStore.isAuthenticated) return
  
  try {
    const res = await fetch('/api/notifications', { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      notifications.value = data.notifications || []
    }
  } catch (err) {
    console.error('Ошибка загрузки уведомлений:', err)
  }
}

// Отметить всё как прочитанное
const markAllAsRead = async () => {
  try {
    const res = await fetch('/api/notifications', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      // Обновляем локальное состояние
      notifications.value = notifications.value.map(n => ({ ...n, is_read: true }))
    }
  } catch (err) {
    console.error('Ошибка отметки уведомлений:', err)
  }
}

// Переключение выпадающего меню
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    loadNotifications()
  }
}

// Закрытие по клику вне
const handleClickOutside = (event) => {
  if (dropdown.value && !dropdown.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.notification-bell {
  position: relative;
  display: inline-block;
}

.badge {
  position: absolute;
  top: -2px;
  right: -2px;
  background-color: #ff4d4d;
  border-radius: 50%;
  width: 12px;
  height: 12px;
  padding: 0;
  min-width: 0;
}

.dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 320px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  z-index: 9999;
  margin-top: 8px;
  max-height: 400px;
  overflow-y: auto;
}

.dropdown-header {
  padding: 12px 16px;
  font-weight: bold;
  border-bottom: 1px solid #eee;
  background: #f9f9f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mark-read-all-btn {
  background: #e6f4ea;
  border: 1px solid #34a853;
  color: #34a853;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85em;
  cursor: pointer;
}

.mark-read-all-btn:hover {
  background: #d0e8d6;
}

.empty {
  padding: 16px;
  color: #888;
  text-align: center;
}

.notifications-list {
  padding: 8px 0;
}

.notification-item {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 0.95em;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item.unread {
  background-color: #f8f9fa;
  border-left: 3px solid #34a853;
}

.notif-title {
  font-weight: bold;
  margin-bottom: 4px;
}

.notif-message {
  color: #555;
  margin-bottom: 4px;
  word-break: break-word;
}

.notif-date {
  font-size: 0.8em;
  color: #999;
}
</style>