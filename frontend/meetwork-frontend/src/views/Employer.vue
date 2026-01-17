<template>
  <div class="container-2">
    <h1>Отклики на мои вакансии</h1>

    <div v-if="vacancies.length === 0">
      <p>Нет активных вакансий с откликами.</p>
    </div>

    <div v-for="vac in vacancies" :key="vac.vacancy_id" class="vacancy-section">
      <h2>{{ vac.title }}</h2>

      <div v-if="vac.applicants.length === 0">
        <p>Откликов нет.</p>
      </div>

      <div v-else>
        <div v-for="app in vac.applicants" :key="app.sign_id" class="card">
          <h3>{{ app.applicant_name }}</h3>
          
          <p>Возраст: {{ app.age || 'Не указан' }}</p>
          <p>Телефон:{{ app.contact_phone || 'Не указан' }}</p>
          <p>Email: {{ app.email || 'Не указан' }}</p>
          
          <p>Резюме:</p>
          <p class="resume-text">{{ app.resume || 'Резюме не заполнено' }}</p>
          
          <p>Образование:</p>
          <p class="education-text">{{ app.education || 'Не указано' }}</p>
          
          <p>Статус отклика: {{ statusLabels[app.status] || app.status }}</p>
          
          <div class="control">
            <label>Изменить статус:</label><br/>
            <select class="form-control"
              :value="app.status"
              @change="updateStatus(app.sign_id, $event.target.value)">
              <option value="pending">В ожидании</option>
              <option value="accepted">Принять</option>
              <option value="rejected">Отклонить</option>
            </select>
          </div>
          
          <hr />
        </div>
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
const vacancies = ref([])

const statusLabels = {
  pending: 'Ожидание',
  accepted: 'Принят',
  rejected: 'Отклонён'
}

const loadDashboard = async () => {
  try {
    const res = await fetch('/api/employer/dashboard', { credentials: 'include' })
    if (res.status === 401) {
      authStore.logoutLocal()
      router.push('/login')
      return
    }
    if (res.ok) {
      const data = await res.json()
      vacancies.value = (data.my_vacancies || []).filter(vac => vac.is_active)
    } else {
      alert('Не удалось загрузить отклики')
    }
  } catch (error) {
    console.error('Ошибка загрузки откликов:', error)
    alert('Ошибка подключения к серверу')
  }
}

const updateStatus = async (signId, newStatus) => {
  try {
    const res = await fetch('/api/employer/dashboard', {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sign_id: signId, status: newStatus })
    })

    if (!res.ok) {
      const err = await res.json()
      alert(err.message || 'Не удалось обновить статус')
      return
    }

    loadDashboard()
  } catch (error) {
    console.error('Ошибка обновления статуса:', error)
    alert('Ошибка сети')
  }
}

onMounted(() => {
  loadDashboard()
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
.form-control{
    width: 400px;
}
</style>



 