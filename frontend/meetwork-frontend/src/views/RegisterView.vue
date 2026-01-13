<template>
  <div class="container">
    <h1 clacc="title">Регистрация</h1>
    <form>
      <label>Имя</label>
      <input type="text" class="form-control" required><br>
      <label>Фамилия</label>
      <input type="text" class="form-control" required><br>
      <label>Отчество</label>
      <input type="text" class="form-control" required><br>
      <label>Возраст</label>
      <input type="number" class="form-control" required><br>
      <label>Номер телефона</label>
      <input type="tel" class="form-control" required><br>
      <label>Роль</label>
      <select class="form-control" required>
        <option v-for="(name, key) in ROLES" :value="key">{{ name }}</option>
      </select><br>
      <label>Почта</label>
      <input type="email"  class="form-control" required><br>
      <label>Пароль</label>
      <input type="password" class="form-control" required><br>
      <RouterLink to="/login" >
          Уже зарегистрированы? Войдите, чтобы продолжить
        </RouterLink><br><br>
      <button class="button" type="submit">Зарегистрироваться</button>
  </form>
  </div>
</template>

<style>
.container{
  align-items: center;
  display: flex;
  flex-direction: column;
  gap: 24px;
  max-width: 1250px;
  margin-left: auto;
  margin-right: auto;
}
.title{
  text-align: center; 
  margin: 0;
}

</style>

<script>
import { ROLES } from '@/utils/roles'
</script>