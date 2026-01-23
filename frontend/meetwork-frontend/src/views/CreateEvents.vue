<template>
  <div class="container">
    <h1 class="title">Создание мероприятия</h1>
    <form @submit.prevent="handleSubmit">
      <label>Название мероприятия</label>
      <input v-model="form.title" type="text" class="form-control" required>
      
      <label>Описание</label>
      <textarea v-model="form.description" class="form-control textarea-scrollable" rows="10" required></textarea>
      
      <label>Требования</label>
      <textarea v-model="form.requirements" class="form-control textarea-scrollable" rows="10" required></textarea>
      
      <label>Место проведения</label>
      <input v-model="form.location" type="text" class="form-control" required>
      
      <label>Количество участников</label>
      <input v-model.number="form.capacity" type="number" class="form-control" required>
      
      <label>Дата и время проведения</label>
      <input v-model="form.date" type="datetime-local" class="form-control" required>
      
      <label>Категория</label>
      <select v-model="form.category" class="form-control" required>
        <option v-for="(name, key) in EVENTCATEGORIES" :value="key" :key="key">{{ name }}</option>
      </select>

      <div class="button-group">
        <button class="button submit-btn" type="submit">Создать</button>
        <button class="button cancel-btn" type="button" @click="$router.back()">Отменить</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
form {
  width: 100%;
  max-width: 700px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0 auto; 
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;             
}

.button {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  padding: 12px 28px;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s ease;
  
  width: 100%;
  max-width: 400px; 
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.submit-btn {
  background: #BFC5A9;
  color: #2d3748;
}
.submit-btn:hover {
  background: #e5ebce;
}

.cancel-btn {
  background: #f8edd0;
  color: #2d3748;
}
.cancel-btn:hover {
  background: #fbf5e3;
}

@media (max-width: 600px) {
  .button-group {
    flex-direction: column; 
    align-items: center;    
  }
  
  .button {
    max-width: 100%;
  }
}
</style>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { EVENTCATEGORIES } from '@/utils/eventcategories'

const authStore = useAuthStore()
const router = useRouter()

const canCreate = computed(() => {
  return authStore.isAuthenticated && authStore.user?.role === 'organizer'
})

const form = ref({
  title: '',
  description: '',
  requirements: '',
  location: '',
  max_participants: null,
  date: '',
  category: ''
})
const handleSubmit = async () => {
  const eventDate = new Date(form.value.date).toISOString()

  const payload = {
    title: form.value.title,
    description: form.value.description,
    requirements: form.value.requirements,
    location: form.value.location,
    capacity: form.value.capacity,
    date: eventDate, 
    category: form.value.category
  }

  try {
    const response = await fetch('/api/event', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (response.status === 401) {
      authStore.logoutLocal()
      router.push('/login')
      return
    }

     if (response.ok) {
      alert('Мероприятие успешно создано!')
      router.push('/events')
    } else {
      const data = await response.json()
      alert(data.message || 'Ошибка при создании мероприятия')
    }
  } catch (error) {
    console.error('Ошибка сети:', error)
    alert('Не удалось подключиться к серверу')
  }
}
</script>
