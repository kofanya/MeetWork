<template>
  <div class="container">
    <h1 class="title">Вход</h1>
    <form>
      <label>Почта</label>
      <input type="email" class="form-control" required><br>
      <label>Пароль</label>
      <input type="password"class="form-control" required><br>
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
