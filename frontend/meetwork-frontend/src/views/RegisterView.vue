<template>
  <div class="container">
    <h1 class="title">Регистрация</h1>
    
    <form @submit.prevent="register" class="registration-form">
      <label>Имя</label>
      <input type="text" v-model="registerForm.first_name" class="form-control" required>

      <label>Фамилия</label>
      <input type="text" v-model="registerForm.second_name" class="form-control" required>

      <label>Отчество</label>
      <input type="text" v-model="registerForm.last_name" class="form-control" required>

      <label>Возраст</label>
      <input type="number" v-model="registerForm.age" class="form-control" required>

      <label>Номер телефона</label>
      <input type="tel" v-model="registerForm.contact_phone" class="form-control" required>

      <label>Роль</label>
      <select v-model="registerForm.role" class="form-control" required>
        <option v-for="(name, key) in ROLES" :key="key" :value="key">{{ name }}</option>
      </select>

      <label>Почта</label>
      <input type="email" v-model="registerForm.email" class="form-control" required>

      <label>Пароль</label>
      <input type="password" v-model="registerForm.password" class="form-control" required>

      <div class="back">
        <RouterLink to="/login">
          Уже зарегистрированы? Войдите, чтобы продолжить
        </RouterLink>
      </div>
      
      <button class="button" type="submit">Зарегистрироваться</button>
    </form>
  </div>
</template>

<style scoped>
.container {
  margin: 0 auto;
  padding: 20px;
}

.title {
  text-align: center;
  margin-top: 50px;
  margin-bottom: 30px;
}

.registration-form {
  display: flex;
  flex-direction: column;
}

.form-control {
  width: 100%;
  margin-bottom: 15px;
  padding: 8px;
  box-sizing: border-box;
}

.back {
  text-align: center;
  margin-bottom: 20px;
}

.button {
  display: block;    
  margin: 20px auto 0;  
  width: 100%;
  max-width: 250px;
  padding: 12px 28px;
  background: #BFC5A9;
  color: #2d3748;
  font-size: 16px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background: #e5ebce;
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

