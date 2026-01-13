<template>
  <div class="container">
    <h1 class="title">Вход</h1>
    <form>
      <label>Почта</label>
      <input type="email" class="form-control" required><br>
      <label>Пароль</label>
      <input type="password"class="form-control" required><br>
      <RouterLink to="/register" >
          Нет аккаунта? Зарегистрируйтесь, чтобы 
          продолжить
        </RouterLink><br><br>
      <button class="button" type="submit">Войти</button>
    </form>
  </div>
</template>

<style scoped>

.title{
  margin-top: 20px;
}

.button{
  margin-left: 100px;
  margin-top: 10px;
  padding: 8px 60px;
}

</style>
