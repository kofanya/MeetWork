<template>
  <div class="container">
    <h1 class="title">Вход</h1>
    <form @submit.prevent="login">
      <label>Почта</label>
      <input v-model="email" type="email" class="form-control" required><br>
      <label>Пароль</label>
      <input v-model="password" type="password"class="form-control" required><br>
      <div class="back">
        <RouterLink to="/register" >
          Нет аккаунта? Зарегистрируйтесь, чтобы 
          продолжить
        </RouterLink>
      </div><br><br>
      <button class="button" type="submit">Войти</button>
    </form>
  </div>
</template>

<style scoped>

.title{
  margin-top: 50px;
  font-size: 52px;
}

.button{
  margin-left: 125px;
  margin-top: 10px;
  padding: 8px 60px;
}

</style>

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