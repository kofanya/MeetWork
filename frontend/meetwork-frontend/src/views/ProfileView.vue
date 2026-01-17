<template>
  <div class="container">
    <h1 class="title">Личный кабинет</h1>

    <form @submit.prevent="submitProfile" v-if="!loading">
      <label>Имя</label>
      <input v-model="formData.first_name" type="text" class="form-control" required><br>

      <label>Отчество</label>
      <input v-model="formData.second_name" type="text" class="form-control"><br>

      <label>Фамилия</label>
      <input v-model="formData.last_name" type="text" class="form-control" required><br>

      <label>Возраст</label>
      <input v-model.number="formData.age" type="number" min="14" max="100" class="form-control" required><br>

      <label>Телефон</label>
      <input v-model="formData.contact_phone" type="tel" class="form-control" required><br>

      <label>Email</label>
      <input v-model="formData.email" type="email" class="form-control" disabled><br>

      <template v-if="formData.role === 'employer'">
        <h3>Информация о компании</h3>
        <label>Название компании</label>
        <input v-model="formData.company_name" type="text" class="form-control" required><br>

        <label>Сайт компании</label>
        <input v-model="formData.contact_website" type="url" class="form-control"><br>
      </template>

      <template v-else-if="formData.role === 'applicant'">
        <h3>Информация о соискателе</h3>
        <label>Резюме</label>
        <textarea v-model="formData.resume" class="form-control textarea-scrollable" rows="5"></textarea><br>

        <label>Образование</label>
        <textarea v-model="formData.education" class="form-control textarea-scrollable" rows="4"></textarea><br>
      </template>

      <button type="submit" class="button">Сохранить изменения</button>
      <button type="button" class="z-button" @click="$router.back()">Назад</button>
    </form>
    
    <div class="back" v-if="formData.role === 'organizer'">
        <RouterLink to="/">Смотреть записи на мероприятия</RouterLink>
    </div>
    <div class="back" v-if="formData.role === 'employer'">
        <RouterLink to="/employer/applications">Смотреть отклики на вакансии</RouterLink>
    </div>

    <div class="back" v-if="formData.role === 'applicant'">
        <RouterLink to="/applicant/applications">Мои отклики и мероприятия</RouterLink>
    </div>

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
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const loading = ref(true)
const formData = ref({
  first_name: '',
  second_name: '',
  last_name: '',
  age: null,
  contact_phone: '',
  email: '',
  role: '',

  company_name: '',
  contact_website: '',

  resume: '',
  education: ''
})

const loadProfile = async () => {
  try {
    const res = await fetch('/api/profile', {
      credentials: 'include'
    })

    if (res.status === 401) {
      authStore.logoutLocal()
      router.push('/login')
      return
    }

    if (!res.ok) {
      throw new Error('Не удалось загрузить профиль')
    }

    const data = await res.json()

    formData.value.first_name = data.data_user.first_name || ''
    formData.value.second_name = data.data_user.second_name || ''
    formData.value.last_name = data.data_user.last_name || ''
    formData.value.age = data.data_user.age || null
    formData.value.contact_phone = data.data_user.contact_phone || ''
    formData.value.email = data.data_user.email || ''
    formData.value.role = data.data_user.role || ''

    if (data.information) {
      if (formData.value.role === 'employer') {
        formData.value.company_name = data.information.company_name || ''
        formData.value.contact_website = data.information.contact_website || ''
      } else if (formData.value.role === 'applicant') {
        formData.value.resume = data.information.resume || ''
        formData.value.education = data.information.education || ''
      }
    }
  } catch (error) {
    console.error('Ошибка загрузки профиля:', error)
    alert('Не удалось загрузить данные профиля')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProfile()
})

const submitProfile = async () => {
  const payload = {
    first_name: formData.value.first_name,
    second_name: formData.value.second_name,
    last_name: formData.value.last_name,
    age: formData.value.age,
    contact_phone: formData.value.contact_phone
  }

  if (formData.value.role === 'employer') {
    payload.company_name = formData.value.company_name
    payload.contact_website = formData.value.contact_website
  } else if (formData.value.role === 'applicant') {
    payload.resume = formData.value.resume
    payload.education = formData.value.education
  }

  try {
    const res = await fetch('/api/profile', {
      method: 'PUT',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    })

    if (res.status === 401) {
      authStore.logoutLocal()
      router.push('/login')
      return
    }

    if (res.ok) {
      alert('Профиль успешно обновлён!')
    } else {
      const err = await res.json()
      alert(err.message || 'Ошибка при сохранении профиля')
    }
  } catch (error) {
    console.error('Ошибка сети:', error)
    alert('Не удалось подключиться к серверу')
  }
}
</script>