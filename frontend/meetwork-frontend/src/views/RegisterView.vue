<template>
  <div class="container">
    <h1 clacc="title">Регистрация</h1>
    <form @submit="register">
      <label>Имя</label>
      <input type="text" v-model="registerForm.first_name" class="form-control" required><br/>
      <label>Фамилия</label>
      <input type="text" v-model="registerForm.second_name" class="form-control" required><br/>
      <label>Отчество</label>
      <input type="text" v-model="registerForm.last_name"class="form-control" required><br/>
      <label>Возраст</label>
      <input type="number" v-model="registerForm.age" class="form-control" required><br/>
      <label>Номер телефона</label>
      <input type="tel" v-model="registerForm.contact_phone"class="form-control" required><br/>
      <label>Роль</label>
      <select v-model="registerForm.role" class="form-control" required>
        <option v-for="(name, key) in ROLES" :value="key">{{ name }}</option>
      </select><br/>
      <label>Почта</label>
      <input type="email"  v-model="registerForm.email"class="form-control" required><br/>
      <label>Пароль</label>
      <input type="password" v-model="registerForm.password" class="form-control" required><br/>
      <div class="back">
        <RouterLink to="/login">
          Уже зарегистрированы? Войдите, чтобы продолжить
        </RouterLink>
      </div><br/><br/>
      
      <button class="button" type="submit">Зарегистрироваться</button>
  </form>
  </div>
</template>

<style scoped>
.title{
  text-align: center; 
  margin-top: 50px;
}
.button{
  margin-left: 85px;
}
</style>

<script setup>
import { ROLES } from '@/utils/roles'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)

const registerForm = ref({
  first_name: '',
  second_name: '',
  last_name: '',
  age: null,
  contact_phone: '',
  role: '',
  email: '',
  password: ''
})

const register = async (e) => {
  e.preventDefault()
  if (loading.value) return

  loading.value = true
  try {
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(registerForm.value)
    })

    const data = await res.json()

    if (res.ok) {
      alert('Регистрация успешна!')
      router.push('/login')
    } else {
      alert(data.message || 'Ошибка регистрации')
    }
  } catch (err) {
    alert('Не удалось подключиться к серверу')
  } finally {
    loading.value = false
  }
}
</script>

