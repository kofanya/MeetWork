<template>
  <div class="container-2">
    <h1>Мои отклики и мероприятия</h1>

    <h2>Отклики на вакансии</h2>
    <div v-if="applications.length === 0">
      <p>Нет откликов</p>
    </div>
    <div v-else>
      <div v-for="(app, index) in applications" :key="index" class="card">
        <h3>{{ app.vacancy_title }}</h3>
        <p><strong>Компания:</strong> {{ app.company }}</p>
        <p>
          <strong>Статус:</strong>
          <span :class="`status-badge status-${app.my_status}`">
            {{ statusLabels[app.my_status] || app.my_status }}
          </span>
        </p>
        <p><strong>Состояние вакансии:</strong> {{ app.vacancy_state }}</p>

        <div v-if="app.my_status === 'accepted'" class="success-message">
          Ваш отклик принят работодателем. В скором времени с вами свяжутся — проверяйте почту.
        </div>

        <div v-if="app.my_status === 'accepted'" class="employer-contact">
          <p><strong>Контакты работодателя:</strong></p>
          <p>Сайт работодателя: {{ app.employer_website || 'Не указан' }}</p>
        </div>
      </div>
    </div>

     <h2>Записи на мероприятия</h2>
    <div v-if="events.length === 0">
      <p>Нет записей на мероприятия</p>
    </div>
    <div v-else>
       <div v-for="(event, index) in events" :key="index" class="card">
        <h3>{{ event.event_title }}</h3>
        <p>Дата проведения: {{ formatDate(event.event_date) }}</p>
        <p>Место проведения: {{ event.location || 'Не указано' }}</p>
        <p>
          <strong>Статус:</strong>
          <span :class="`status-badge status-${event.my_status}`">
            {{ statusLabels[event.my_status] || event.my_status }}
          </span>
        </p>
        <p><strong>Состояние:</strong> {{ event.event_state }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const applications = ref([])
const events = ref([])

const statusLabels = {
  pending: 'В ожидании',
  accepted: 'Принят',
  rejected: 'Отклонён',
  confirmed: 'Подтверждена'
}
const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}


const loadApplications = async () => {
  try {
    const res = await fetch('/api/applicant/dashboard', { credentials: 'include' })
    if (res.status === 401) {
      authStore.logoutLocal()
      router.push('/login')
      return
    }
    if (res.ok) {
      const data = await res.json()
      console.log('Полученные данные:', data) 
      applications.value = data.applications || []
      events.value = data.events || []
    } else {
      alert('Не удалось загрузить данные')
    }
  } catch (error) {
    console.error('Ошибка загрузки:', error)
    alert('Ошибка подключения к серверу')
  }
}

onMounted(() => {
  loadApplications()
})
</script>

<style scoped>
.card {
  background-color: #fff;
  padding: 16px;
  margin-bottom: 16px;
  border-radius: 8px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.25s ease, transform 0.2s ease;
  height: auto;
}
.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85em;
  font-weight: bold;
}

.status-pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-confirmed,
.status-accepted {
  background-color: #d4edda;
  color: #155724;
}

.status-rejected {
  background-color: #f8d7da;
  color: #721c24;
}
</style>
