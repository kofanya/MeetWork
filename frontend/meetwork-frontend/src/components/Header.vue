<template>
  <header class="header">
    <div class="header-container">
      <div class="header-logo">
        <RouterLink to="/">
          <h3 class="logo-text">MeetWork</h3>
        </RouterLink>
      </div>

      <nav class="header-nav">
        <ul class="nav-list">
          <li><RouterLink to="/vacancies">Поиск работы</RouterLink></li>
          <li><RouterLink to="/events">Мероприятия</RouterLink></li>
          <li><RouterLink to="/about">О проекте</RouterLink></li>
          <li><RouterLink to="/personal">Личный кабинет</RouterLink></li>
          <li><RouterLink to="/register">Регистрация</RouterLink></li>
          <li><RouterLink to="/login">Вход</RouterLink></li>
        </ul>
      </nav>
    </div>

  </header>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>