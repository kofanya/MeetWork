import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import LoginView from '../views/LoginView.vue'
import AboutView from '../views/AboutView.vue'
import ProfileView from '../views/ProfileView.vue'
import VacanciesView from '../views/VacanciesView.vue'
import EventsView from '../views/EventsView.vue'
import CreateVacancies from '../views/CreateVacancies.vue'
import EditVacancies from '../views/EditVacancies.vue'
import CreateEvents from '../views/CreateEvents.vue'
import EditEvents from '../views/EditEvents.vue'
import Vacancy from '../views/Vacancy.vue'
import Event from '../views/Event.vue'
import Applicant from '../views/Applicant.vue'
import Employer from '../views/Employer.vue'
import Organizer from '@/views/Organizer.vue'

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
    { path: '/profile', component: ProfileView },

    { path: '/createvacancies', component: CreateVacancies },
    { path: '/editvacancies', component: EditVacancies },
    { path: '/createevents', component: CreateEvents },
    { path: '/editevents', component: EditEvents },

    { path: '/vacancy/:id', component: Vacancy },
    { path: '/event/:id', component: Event },
    { path: '/employer/applications', component: Employer },
    { path: '/applicant/applications', component: Applicant },
    {path: '/organizer/applications', component: Organizer}

  ],
})

export default router
