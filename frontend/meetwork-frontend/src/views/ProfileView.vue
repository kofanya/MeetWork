<template>
  <div class="container">
    <h1 class="title">Личный кабинет</h1>
    <form >
      <label>Имя</label>
      <input type="text"  class="form-control" required><br>
      <label>Фамилия</label>
      <input type="text"  class="form-control" required><br>
      <label>Отчество</label>
      <input type="text"class="form-control" required><br>
      <label>Возраст</label>
      <input type="number" class="form-control" required><br>
      <label>Номер телефона</label>
      <input type="tel" class="form-control" required><br>
      <label>Почта</label>
      <input type="email"  class="form-control" required><br>
      <button class="button" type="submit">Сохранить</button>
      <button class="z-button" type="submit">Отменить</button>
  </form>

  <div class="back">
      <RouterLink to="/vacancies">Смотреть отклики на вакансии</RouterLink>
  </div>
  <div class="back">
      <RouterLink to="/vacancies">Смотреть записи на мероприятия</RouterLink>
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
<script>

</script>