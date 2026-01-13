<template>
  <div class="container">
    <h1 class="title">Редактирование вакансии</h1>
    <form>
      <label>Вакансия</label>
      <input type="text" class="form-control" required><br>
      <label>Описание</label>
      <textarea class="form-control textarea-scrollable" rows="10" required></textarea><br>
      <label>Требования</label>
      <textarea class="form-control textarea-scrollable" rows="10" required></textarea><br>
      <label>Адрес предприятия</label>
      <input type="text" class="form-control" required><br>
      <label>Зарплата</label><br>
      <label>От:</label><br>
      <input type="number"class="form-control" required><br>
      <label>До:</label>
      <input type="number"class="form-control" required><br>
      <label>Категория</label>
      <select class="form-control" required>
        <option v-for="(name, key) in CATEGORIES" :value="key">{{ name }}</option>
      </select><br>
      <button class="button" type="submit">Сохранить</button>
      <button class="z-button" type="submit">Отменить</button>
  </form><h1></h1>
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
import { CATEGORIES } from '@/utils/categories'
</script>