<template>
  <div class="container">
    <h1 class="title">Создание вакансии</h1>
    <form @submit.prevent="handleSubmit">
      <label>Вакансия</label>
      <input v-model="form.title" type="text" class="form-control" required>

      <label>Описание</label>
      <textarea v-model="form.description" class="form-control textarea-scrollable" rows="10" required></textarea>

      <label>Требования</label>
      <textarea v-model="form.requirements" class="form-control textarea-scrollable" rows="10" required></textarea>

      <label>Адрес предприятия</label>
      <input v-model="form.location" type="text" class="form-control" required>

      <div class="salary-group">
        <label>Зарплата</label>
        <div class="salary-inputs">
          <span>От:</span>
          <input v-model="form.salary_min" min="0" type="number" class="form-control" required>
          <span>До:</span>
          <input v-model="form.salary_max" min="0" type="number" class="form-control" required>
        </div>
      </div>

      <label>Категория</label>
      <select v-model="form.category" class="form-control" required>
        <option v-for="(name, key) in CATEGORIES" :value="key" :key="key">{{ name }}</option>
      </select>

      <div class="button-group">
        <button class="button" type="submit">Создать</button>
        <button class="z-button" type="button" @click="$router.back()">Отменить</button>
      </div>
    </form>
  </div>
</template>

<style scoped>

form {
  width: 100%;
  max-width: 700px; 
  padding: 0 20px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 12px; 
}

.button-group {
  display: flex;
  flex-direction: row;
  justify-content: center;
  gap: 16px;              
  margin-top: 12px;
}

.button, .z-button {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;           
  width: 100%;            
  max-width: 400px;       
  border-radius: 12px;
  border: none;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  margin: 0;
}

.button {
  background: #BFC5A9;
  color: #2d3748;
}
.button:hover {
  background: #e5ebce;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.z-button {
  background: #f8edd0;
  color: #2d3748;
}
.z-button:hover {
  background: #fbf5e3;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

@media (max-width: 600px) {
  .button-group {
    flex-direction: column;
    align-items: center;   
  }

  .button, .z-button {
    max-width: 100%;       
  }
}
</style>

<script setup>
import { CATEGORIES } from '@/utils/categories'
import { ref, onMounted, watch} from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
const router = useRouter()
const form = ref({
  title: '',
  description: '',
  requirements: '',
  location: '',
  salary_min: null,
  salary_max: null,
  category: ''
})

onMounted(() => {
  const savedForm = localStorage.getItem('pending_vacancy_data')
  if (savedForm) {
    try {
      form.value = JSON.parse(savedForm)
    } catch (e) {
      console.error("Ошибка парсинга сохраненных данных", e)
    }
  }
})

watch(form, (newVal) => {
  localStorage.setItem('pending_vacancy_data', JSON.stringify(newVal))
}, { deep: true })

const handleSubmit = async () => {
  if (form.value.salary_min < 0 || form.value.salary_max < 0) {
    alert('Зарплата не может быть отрицательной')
    return
  }
  if (form.value.salary_min > form.value.salary_max) {
    alert('Минимальная зарплата не может быть больше максимальной')
    return
  }

  try {
    const response = await fetch('/api/vacancy', {
      method: 'POST',
      credentials: 'include', 
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: form.value.title,
        description: form.value.description,
        requirements: form.value.requirements,
        location: form.value.location,
        salary_min: form.value.salary_min,
        salary_max: form.value.salary_max,
        category: form.value.category
      })
    })

    const responseData = await response.json()

    if (response.ok) {
      alert('Вакансия создана!')
      localStorage.removeItem('pending_vacancy_data')
      router.push('/vacancies')
    } else {
      if (response.status === 400) {
        alert('Пожалуйста, заполните поля компании в личном кабинете')
        router.push('/profile')
      } else {
        alert(responseData.message || 'Ошибка создания вакансии')
      }
    }}
  catch (error) {
    console.error('Ошибка сети:', error)
    alert('Не удалось подключиться к серверу')
  }
}
</script>