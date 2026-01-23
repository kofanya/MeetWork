<template>
  <div class="container-2">
    <h1>Панель организатора</h1>

    <div v-if="loading" class="loading">Загрузка...</div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="!myEvents || myEvents.length === 0">
      <p>У вас пока нет созданных мероприятий.</p>
    </div>

    <div v-else>
      <div v-for="event in myEvents" :key="event.event_id" class="event-card">
        <h2>{{ event.event_title }}</h2>
        <p><strong>Записавшихся:</strong> {{ event.applicants.length }}</p>

        <div v-if="event.applicants.length === 0" class="no-applicants">
          Нет заявок
        </div>

        <table v-else class="applicants-table">
          <thead>
            <tr>
              <th>Имя</th>
              <th>Телефон</th>
              <th>Email</th>
              <th>Статус</th>
              <th>Действие</th>
            </tr>
          </thead>
                    <tbody>
            <tr v-for="applicant in event.applicants" :key="applicant.sign_id">
              <td data-label="Имя">{{ applicant.applicant_name }}</td>
              <td data-label="Телефон">{{ applicant.contact_phone || '—' }}</td>
              <td data-label="Email">{{ applicant.email || '—' }}</td>
              <td data-label="Статус">
                <span :class="`status-badge status-${applicant.status}`">
                  {{ statusLabels[applicant.status] }}
                </span>
              </td>
              <td data-label="Действие">
                <select
                  v-model="applicant.newStatus"
                  @change="updateStatus(applicant)"
                  class="form-control"
                >
                  <option value="pending">В ожидании</option>
                  <option value="confirmed">Подтверждён</option>
                  <option value="rejected">Отклонён</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
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

const myEvents = ref([])
const loading = ref(false)
const error = ref(null)

const statusLabels = {
  pending: 'В ожидании',
  confirmed: 'Подтверждён',
  rejected: 'Отклонён'
}

const loadDashboard = async () => {
  loading.value = true
  error.value = null

  try {
    const res = await fetch('/api/organizer/dashboard', {
      credentials: 'include'
    })

    if (res.status === 403) {
      error.value = 'Доступ запрещён. Только организаторы могут просматривать эту страницу.'
      return
    }

    if (!res.ok) {
      throw new Error('Не удалось загрузить данные')
    }

    const data = await res.json()
    myEvents.value = (data.my_events || []).map(event => ({
      ...event,
      applicants: (event.applicants || []).map(app => ({
        ...app,
        newStatus: app.status 
      }))
    }))
  } catch (err) {
    console.error('Ошибка загрузки панели организатора:', err)
    error.value = 'Не удалось подключиться к серверу'
  } finally {
    loading.value = false
  }
}

const updateStatus = async (applicant) => {
  try {
    const res = await fetch('/api/organizer/dashboard', {
      method: 'PUT',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        sign_id: applicant.sign_id,
        status: applicant.newStatus
      })
    })

    if (res.ok) {
      alert('Статус обновлён')
    } else {
      const errData = await res.json()
      alert(errData.message || 'Ошибка при обновлении статуса')
      applicant.newStatus = applicant.status
    }
  } catch (err) {
    console.error('Ошибка сети:', err)
    alert('Не удалось подключиться к серверу')
    applicant.newStatus = applicant.status
  }
}

onMounted(() => {
  if (!authStore.isAuthenticated || authStore.user?.role !== 'organizer') {
    router.push('/login')
    return
  }
  loadDashboard()
})
</script>

<style scoped>
.container {
  max-width: 1000px;
  margin: 40px auto;
  padding: 0 20px;
}

.loading, .error {
  text-align: center;
  padding: 20px;
}

.error {
  color: #d32f2f;
}

.event-card {
  background: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

.event-card h2 {
  margin-top: 0;
  color: #333;
}

.no-applicants {
  color: #888;
  font-style: italic;
  padding: 12px 0;
}

.applicants-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 12px;
}

.applicants-table th,
.applicants-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.applicants-table th {
  background-color: #f9f9f9;
  font-weight: 600;
  color: #555;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.85em;
  font-weight: bold;
}

.status-pending {
  background-color: #fff3cd;
  color: #856404;
}

.status-confirmed {
  background-color: #d4edda;
  color: #155724;
}

.status-rejected {
  background-color: #f8d7da;
  color: #721c24;
}

@media (max-width: 768px) {
  .container-2 {
    padding: 0 10px;
  }

  .applicants-table thead {
    display: none;
  }

  .applicants-table, 
  .applicants-table tbody, 
  .applicants-table tr, 
  .applicants-table td {
    display: block;
    width: 100%;
  }

  .applicants-table tr {
    margin-bottom: 15px;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 10px;
    background: #fafafa;
  }

  .applicants-table td {
    text-align: right;
    padding: 10px 5px;
    border-bottom: 1px solid #eee;
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .applicants-table td:last-child {
    border-bottom: none;
  }

  .applicants-table td::before {
    content: attr(data-label);
    font-weight: bold;
    text-transform: uppercase;
    font-size: 0.75rem;
    color: #777;
    margin-right: 15px;
  }

  .status-select {
    width: auto;
    max-width: 150px;
  }
}
</style>