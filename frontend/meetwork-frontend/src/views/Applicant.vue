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
        <p><strong>Статус:</strong> {{ statusLabels[app.my_status] || app.my_status }}</p>
        <p><strong>Состояние вакансии:</strong> {{ app.vacancy_state }}</p>

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
        <p><strong>Статус:</strong> {{ event.my_status }}</p>
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
  rejected: 'Отклонён'
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

</style>
