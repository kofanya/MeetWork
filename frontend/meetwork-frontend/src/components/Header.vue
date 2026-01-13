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

          <li><RouterLink to="/createvacancies">Создание вакансии</RouterLink></li>
          
          <li><RouterLink to="/createevents">Создание мероприятия</RouterLink></li>

          <li><RouterLink to="/register">Регистрация</RouterLink></li>
          <li><RouterLink to="/login" class="login-button">Вход</RouterLink></li>


        </ul>
      </nav>
    </div>

  </header>
</template>

<style>

.logo-text{
  color: #E17801;
  font-size: 32px;
  margin: 0;
  
}

.header-logo a{
  text-decoration: none;
}

.header {
  background-color: rgba(251, 235, 195, 0.8); 
  height: 70px;
}

.header-container {
  max-width: 1250px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}


.header-nav ul {
  list-style: none;
  display: flex;
  gap: 25px;
}

.header-nav a {
  text-decoration: none;
  color: rgba(0, 0, 0, 0.8);
  transition: color 0.2s;
}

.header-nav a:hover,
.header-nav a:focus {
  color: #E17801;
}

.login-button{
    padding: 6px 36px;
    background: #BFC5A9;
    border: none;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.25s ease;
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.20);
}

.header-nav .login-button:hover,
.header-nav .login-button:focus {
  background: #AEB494;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}
</style>

<script setup>
import { RouterLink } from 'vue-router'
</script>