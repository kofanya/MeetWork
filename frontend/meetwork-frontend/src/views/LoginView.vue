<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'


const email = ref('')
const password = ref('')
const router = useRouter()
const auth = useAuthStore()

const login = async () => {
  try {
    await auth.login(email.value, password.value)
    router.push('/')
  } catch (error) {
    alert("Зарегистрируйтесь, чтобы продолжить")
  }
}
</script>


<template>
  <div class="container">
    <h1 class="title">Вход</h1>
    <form @submit.prevent="login" class="login-form">
      <label>Почта</label>
      <input v-model="email" type="email" class="form-control" required>
      
      <label>Пароль</label>
      <input v-model="password" type="password" class="form-control" required>
      
      <div class="back">
        <RouterLink to="/register">
          Нет аккаунта? Зарегистрируйтесь, чтобы продолжить
        </RouterLink>
      </div>

      <button class="button" type="submit">Войти</button>
    </form>
  </div>
</template>

<style scoped>
.container {
  margin: 0 auto;
  padding: 0 20px;
}

.title {
  margin-top: 50px;
  font-size: 52px;
  text-align: center;
  margin-bottom: 30px;
}

.login-form {
  display: flex;
  flex-direction: column; 
}

.form-control {
  width: 100%;
  margin-bottom: 15px; 
  padding: 10px;
  box-sizing: border-box;
}

.back {
  text-align: center;
  margin-bottom: 20px;
}

.button {
  display: block;     
  margin: 10px auto 0;  
  
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