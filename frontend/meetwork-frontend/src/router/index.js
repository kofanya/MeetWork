import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import AboutView from '../views/AboutView.vue'
import PersonalView from '../views/PersonalView.vue'
import VacanciesView from '../views/VacanciesView.vue'
import EventsView from '../views/EventsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about', name: 'about',component: AboutView
    },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterView },
    { path: '/vacancies', component: VacanciesView },
    { path: '/events', component: EventsView },
    { path: '/personal', component: PersonalView },

  ],
})

export default router
