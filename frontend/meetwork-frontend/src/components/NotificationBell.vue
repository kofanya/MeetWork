<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue' // Добавлен watch
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const isOpen = ref(false)
const dropdown = ref(null)
const notifications = ref([])

const goToProfile = () => {
  isOpen.value = false
  router.push('/profile')
}

const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  
  if (isNaN(date.getTime())) return dateStr 

  const now = new Date()
  const isToday = date.toDateString() === now.toDateString()

  if (isToday) {
    return `Сегодня в ${date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}`
  }

  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}

let refreshInterval = null

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.is_read).length
})

const loadNotifications = async () => {
  if (!authStore.isAuthenticated) {
    notifications.value = []
    return
  }
  
  try {
    const res = await fetch(`/api/notifications?t=${Date.now()}`, { 
      credentials: 'include' 
    })
    if (res.ok) {
      const data = await res.json()
      notifications.value = data.notifications || []
    }
  } catch (err) {
    console.error('Ошибка загрузки уведомлений:', err)
  }
}

watch(() => authStore.isAuthenticated, (newVal) => {
  if (newVal) {
    loadNotifications()
  } else {
    notifications.value = []
  }
})

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
  if (isOpen.value) {
    loadNotifications()
  }
}

const markAllAsRead = async () => {
  try {
    const res = await fetch('/api/notifications', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' }
    })
    if (res.ok) {
      notifications.value = notifications.value.map(n => ({ ...n, is_read: true }))
    }
  } catch (err) {
    console.error('Ошибка отметки уведомлений:', err)
  }
}

onMounted(() => {
  document.addEventListener('click', (e) => {
    if (dropdown.value && !dropdown.value.contains(e.target)) {
      isOpen.value = false
    }
  })
  loadNotifications()
  refreshInterval = setInterval(loadNotifications, 30000)
})

onUnmounted(() => {
  if (refreshInterval) clearInterval(refreshInterval)
})
</script>

<template>
  <div class="notification-bell" @click.stop="toggleDropdown">
    <div style="position: relative; cursor: pointer;">
      <svg class="bell-icon" xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
        <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
      </svg>
      <span v-if="unreadCount > 0" class="badge"></span>
    </div>

    <div v-if="isOpen" class="dropdown" ref="dropdown" @click.stop>
      <div class="dropdown-header">
        Уведомления
        <button v-if="unreadCount > 0" @click="markAllAsRead" class="mark-read-all-btn">
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

      <div class="dropdown-footer" @click="goToProfile">
        Перейти в личный кабинет
      </div>
    </div>
  </div>
</template>

<style scoped>
.notification-bell {
  position: relative;
  display: inline-block;
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

.notification-bell {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bell-icon {
  color: rgba(0, 0, 0, 0.8); 
  transition: color 0.3s ease, stroke 0.3s ease;
  display: block;
}

.notification-bell:hover .bell-icon {
  color: #E17801;
}

.badge {
  position: absolute;
  top: 0px;
  right: 0px;
  background-color: #ff4d4d;
  border: 2px solid white;
  border-radius: 50%;
  width: 10px;
  height: 10px;
  pointer-events: none;
}

.dropdown-footer {
  padding: 12px;
  text-align: center;
  border-top: 1px solid #eee;
  color: #E17801;
  font-weight: 600;
  font-size: 0.9em;
  cursor: pointer;
  background: #fff;
  transition: background 0.2s;
  border-bottom-left-radius: 8px;
  border-bottom-right-radius: 8px;
}

.dropdown-footer:hover {
  background: #fff8f0;
  text-decoration: underline;
}

.notifications-list {
  padding: 0; 
}
.dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  width: 350px;
  max-width: calc(100vw - 40px);
  background: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  z-index: 1000;
  margin-top: 12px;
  max-height: 450px;
  overflow-y: auto;
}

@media (max-width: 480px) {
  .dropdown {
    width: 300px;
    right: -10px;
  }

  .dropdown-header {
    padding: 10px 12px;
    font-size: 0.9em;
  }

  .notification-item {
    padding: 10px 12px;
  }

  .notif-title {
    font-size: 0.9em;
    line-height: 1.2;
  }

  .notif-message {
    font-size: 0.85em;
    line-height: 1.3;
  }

  .notif-date {
    font-size: 0.75em;
  }

  .mark-read-all-btn {
    padding: 2px 6px;
    font-size: 0.8em;
  }
}

.dropdown {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style> 