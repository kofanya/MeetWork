<template>
  <div class="container-2">
    <h1>название вакансии #</h1>
    <div class="meta" style="margin: 15px 0; color: #666; font-size: 0.95em;">
    <span>Категория: #</span><br />
    <span>Дата публикации: #</span><br />
    <span>Работодатель#</span><br />
    <span>адрес предприятия#</span><br />
    </div>
    <span>ЗАРПЛАТА ОТ#</span>
    <div class="vacancy-text" style="line-height: 1.7; margin-top: 20px;">
      Описание#
    </div>
    <div class="vacancy-text" style="line-height: 1.7; margin-top: 20px;">
      Требования: #
    </div>

    <div >
      <div style="margin-top: 20px;">
        <RouterLink to="/editevents" class="button" style="background: #c4fab6;">
          Откликнуться
        </RouterLink>
      </div>
    </div>

    <div >
      <div style="margin-top: 20px;">
        <RouterLink to="/editevents" class="button" style="margin-right: 40px;">
          Редактировать
        </RouterLink>
        <button type="button" class="button" style="background: #fc8b8b;">
          Удалить
        </button>
      </div>
    </div>

    <div  class="container-2">
      <h3>Вы работник этой компании? Оставьте отзыв!</h3>
      <form style="margin-top: 10px;">
        <textarea
          placeholder="Ваш отзыв..."
          class="form-control"
          rows="4"
          required
        ></textarea>
        <button type="submit" class="button">Отправить</button>
      </form>
    </div>

    <div style="margin-top: 40px;">
      <h3>Отзывы на работодателя (#)</h3>
      <div>
        <p>Пока нет отзывов.</p>
      </div>
      <!-- <div
         v-for="comment in comments"
        :key="comment.id"
        style="margin-top: 15px; padding: 10px; background: #f9f9f9; border-radius: 6px;"
      >
        <div style="font-weight: bold; color: #333;">{{ comment.author_name }}</div>
        <div style="font-size: 0.9em; color: #777; margin: 5px 0;">
          {{ formatRussianDate(comment.created_date) }}
        </div>
        <div style="margin-top: 8px;">{{ comment.text }}</div>
        <div
          v-if="authStore.isAuthenticated && comment.user_id === authStore.user.id"
          style="margin-top: 10px; display: flex; gap: 10px;"
        >
          <button @click="editComment(comment)" class="button">Редактировать</button>
          <button @click="deleteComment(comment.id)" class="button">Удалить</button> 
         </div> 
      </div> -->
    </div>

    <div class="back">
      <RouterLink to="/vacancies">← Вернуться к списку вакансий</RouterLink>
    </div>
  </div>

</template>

<style>
.container-2{
    max-width: 1250px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 100px;
    margin-top: 50px;
}

</style>