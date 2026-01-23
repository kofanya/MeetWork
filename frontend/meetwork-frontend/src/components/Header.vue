<template>
  <header class="header">
    <div class="header-container">
      <div class="header-logo">
        <RouterLink to="/">
          <h3 class="logo-text">MeetWork</h3>
        </RouterLink>
      </div>

      <div class="header-right-side">
      <nav class="header-nav" :class="{ 'is-open': isMenuOpen }">
        <ul class="nav-list">
          <li @click="closeMenu"><RouterLink to="/vacancies">Поиск работы</RouterLink></li>
          <li @click="closeMenu"><RouterLink to="/events">Мероприятия</RouterLink></li>
          <li @click="closeMenu"><RouterLink to="/about">О проекте</RouterLink></li>
          <li @click="closeMenu"><RouterLink to="/profile">Личный кабинет</RouterLink></li>

          <li v-if="auth.isAuthenticated && auth.user?.role === 'employer'" @click="closeMenu">
            <RouterLink to="/createvacancies">Создание вакансии</RouterLink>
          </li>

          <li v-if="auth.isAuthenticated && auth.user?.role === 'organizer'" @click="closeMenu">
            <RouterLink to="/createevents">Создание мероприятия</RouterLink>
          </li>

          <li v-if="auth.isAuthenticated" class="user-name">
            Привет, {{ auth.user?.first_name }}!
          </li>
          
          <li v-if="auth.isAuthenticated">
            <button @click="handleLogout" class="login-button">Выход</button>
          </li>

          <template v-else>
            <li @click="closeMenu"><RouterLink to="/register">Регистрация</RouterLink></li>
            <li @click="closeMenu"><RouterLink to="/login" class="login-button">Вход</RouterLink></li>
          </template>
        </ul>
      </nav>

      <div v-if="isMenuOpen" class="overlay" @click="closeMenu"></div>

      <div class="header-controls">
        <div class="notification-wrapper">
          <NotificationBell />
      </div>

      <div>
        <button 
          class="burger-btn" 
          @click="isMenuOpen = !isMenuOpen" 
          :class="{ 'is-active': isMenuOpen }"
          aria-label="Меню">
          <span></span>
          <span></span>
          <span></span>
        </button>
      </div>
    
    </div>
    </div>
  </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import NotificationBell from '@/components/NotificationBell.vue'

const auth = useAuthStore()
const router = useRouter()
const isMenuOpen = ref(false)

const closeMenu = () => {
  isMenuOpen.value = false
}

const handleLogout = async () => {
  closeMenu()
  await auth.logout()
  router.push('/')
}
</script>

<style scoped>

.header {
  background-color: rgba(251, 235, 195, 0.6);
  height: 70px;
  position: relative;
  z-index: 100;
}

.header-container {
  max-width: 1250px;
  margin: 0 auto;
  display: flex;
  justify-content: flex-start;  
  align-items: center;
  height: 100%;
  padding: 0 20px;
}
.header-right-side {
  display: flex;
  align-items: center;
  margin-left: auto;
  gap: 24px; 
}

.logo-text {
  color: #E17801;
  font-size: 32px;
  margin: 0;
}

.header-logo a { text-decoration: none; }

.header-controls {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-list {
  list-style: none;
  display: flex;
  align-items: center;
  gap: 24px;
  margin: 0;
  padding: 0;
}

.header-nav a {
  text-decoration: none;
  color: rgba(0, 0, 0, 0.8);
  transition: color 0.2s;
  white-space: nowrap;
}

.header-nav a:hover { color: #E17801; }

.login-button {
  padding: 6px 28px;
  background: #BFC5A9;
  color: #2d3748;
  font-size: 16px;
  font-weight: 500;
  border: none;
  border-radius: 12px;
  cursor: pointer;
}

.burger-btn {
  display: none;
  flex-direction: column;
  justify-content: space-between;
  width: 30px;
  height: 20px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 1001;
}

.burger-btn span {
  width: 100%;
  height: 3px;
  background-color: rgba(0, 0, 0, 0.8);
  border-radius: 3px;
  transition: 0.3s;
}

.burger-btn:hover span {
  background-color: #E17801; 
}

:deep(.notification-bell-icon) {
  color: rgba(0, 0, 0, 0.8) !important;
  transition: color 0.2s;
}

:deep(.notification-bell-icon:hover) {
  color: #E17801 !important;
}
.header-controls {
  display: flex;
  align-items: center;
  gap: 15px;
  height: 100%;
}

.burger-btn span {
  width: 100%;
  height: 3px;
  background-color: rgba(0, 0, 0, 0.8);
  border-radius: 3px;
  transition: 0.3s ease;
}

.burger-btn:hover span {
  background-color: #E17801;
}

.burger-btn {
  display: none;
  flex-direction: column;
  justify-content: space-around; 
  width: 28px;
  height: 24px; 
  background: none;
  border: none;
  cursor: pointer;
  margin-bottom: 1px;
}

@media (max-width: 1100px) {
  .burger-btn {
    display: flex;
  }
}

@media (max-width: 1100px) {
  .burger-btn {
    display: flex;
  }

  .header-nav {
    position: fixed;
    top: 0;
    right: -100%;
    width: 280px;
    height: 100vh;
    background: #fffcf5;
    padding: 100px 30px;
    transition: 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: -10px 0 30px rgba(0,0,0,0.1);
    z-index: 1000;
  }

  .header-nav.is-open {
    right: 0;
  }

  .nav-list {
    flex-direction: column;
    align-items: flex-start;
    gap: 25px;
  }

  .burger-btn.is-active span {
    background-color: #E17801;
  }
  .burger-btn.is-active span:nth-child(1) { transform: translateY(8.5px) rotate(45deg); }
  .burger-btn.is-active span:nth-child(2) { opacity: 0; }
  .burger-btn.is-active span:nth-child(3) { transform: translateY(-8.5px) rotate(-45deg); }

  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.3);
    z-index: 999;
  }
}
</style>