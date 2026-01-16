<template>
  <div class="container">
    <h1 class="title">Редактирование мероприятия</h1>
    <form>
      <label>Название мероприятия</label>
      <input type="text" class="form-control" required><br>
      <label>Описание</label>
      <textarea class="form-control textarea-scrollable" rows="10" required></textarea><br>
      <label>Требования</label>
      <textarea class="form-control textarea-scrollable" rows="10" required></textarea><br>
      <label>Место проведения</label>
      <input type="text" class="form-control" required><br>
      <label>Количество участников</label>
      <input type="number"class="form-control" required><br>
      <label>Дата и время проведения</label>
      <input type="datetime-local" class="form-control" required><br>
      <label>Категория</label>
      <select class="form-control" required>
        <option v-for="(name, key) in EVENTCATEGORIES" :value="key">{{ name }}</option>
      </select><br>
      <button class="button" type="submit">Сохранить</button>
      <button class="z-button" type="submit">Отменить</button>
  </form>
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
import { EVENTCATEGORIES } from '@/utils/eventcategories'
</script>