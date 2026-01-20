<template>
  <div class="container">
    <h1 class="title">Создание вакансии</h1>
    <form @submit.prevent="handleSubmit">
      <label>Вакансия</label>
      <input v-model="form.title" type="text" class="form-control" required><br>
      <label>Описание</label>
      <textarea v-model="form.description" class="form-control textarea-scrollable" rows="10" required></textarea><br>
      <label>Требования</label>
      <textarea v-model="form.requirements" class="form-control textarea-scrollable" rows="10" required></textarea><br>
      <label>Адрес предприятия</label>
      <input v-model="form.location" type="text" class="form-control" required><br>
      <label>Зарплата</label><br>
      <label>От:</label><br>
      <input v-model="form.salary_min" type="number"class="form-control" required><br>
      <label>До:</label>
      <input v-model="form.salary_max" type="number"class="form-control" required><br>
      <label>Категория</label>
      <select  v-model="form.category" class="form-control" required>
        <option v-for="(name, key) in CATEGORIES" :value="key">{{ name }}</option>
      </select><br>
      <button class="button" type="submit">Создать</button>
      <button class="z-button" type="submit"  @click="$router.back()">Отменить</button>
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
import { CATEGORIES } from '@/utils/categories'
import { ref } from 'vue'
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

const handleSubmit = async () => {
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