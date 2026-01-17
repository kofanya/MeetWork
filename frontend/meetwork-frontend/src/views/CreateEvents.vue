<template>
  <div class="container">
    <h1 class="title">Создание мероприятия</h1>
    <form @submit.prevent="handleSubmit">
      <label>Название мероприятия</label>
      <input v-model="form.title" type="text" class="form-control" required><br>
      <label>Описание</label>
      <textarea  v-model="form.description" class="form-control textarea-scrollable" rows="10" required></textarea><br>
      <label>Требования</label>
      <textarea v-model="form.requirements" class="form-control textarea-scrollable" rows="10" required></textarea><br>
      <label>Место проведения</label>
      <input  v-model="form.location" type="text" class="form-control" required><br>
      <label>Количество участников</label>
      <input v-model.number="form.capacity" type="number"class="form-control" required><br>
      <label>Дата и время проведения</label>
      <input  v-model="form.date" type="datetime-local"class="form-control" required><br>
      <label>Категория</label>
      <select v-model="form.category" class="form-control" required>
        <option v-for="(name, key) in EVENTCATEGORIES" :value="key">{{ name }}</option>
      </select><br>
      <button class="button" type="submit">Создать</button>
      <button class="z-button" type="submit"@click="$router.back()" >Отменить</button>
  </form>
  </div>
</template>

<style scoped>
form {
  width: 100%;
  max-width: 700px; 
  padding: 0 20px;   
}

.button{
    width: 320px;
    margin-right: 20px;
}
.z-button{
    width: 320px;
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
