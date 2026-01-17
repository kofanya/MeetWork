<template>
  <div v-if="vacancy" class="container-2">
    <h1>{{ vacancy.title }}</h1>
    <div class="meta" style="margin: 15px 0; color: #666; font-size: 0.95em;">
    <span>Категория: {{ CATEGORIES[vacancy.category] || vacancy.category }}</span><br />
    <span>Дата публикации: {{ new Date(vacancy.date).toLocaleDateString() }}</span><br />
    <span>Работодатель: {{ vacancy.company_name }}</span><br />
    <span>адрес предприятия: {{ vacancy.location }}</span><br />
    </div>
    <span>Зарплата: от {{ vacancy.salary_min }} до {{ vacancy.salary_max }}</span>
    <div class="vacancy-text" style="line-height: 1.7; margin-top: 20px;">
      {{ vacancy.description }}
    </div>
    <div class="vacancy-text" style="line-height: 1.7; margin-top: 20px;">
       <h3>Требования:</h3>
      <p>{{ vacancy.requirements }}</p>
    </div>

    <div v-if="authStore.isAuthenticated && authStore.user?.role === 'applicant'">
      <div style="margin-top: 20px;">
        <button @click="applyToVacancy" class="button" style="background: #c4fab6;">
          Откликнуться
        </button>
      </div>
    </div>

    <div v-else-if="!authStore.isAuthenticated">
      <div style="margin-top: 20px;">
        <RouterLink to="/login" class="button" style="background: #c4fab6;">
          Откликнуться
        </RouterLink>
      </div>
    </div>

    <div v-if="authStore.isAuthenticated && authStore.user?.role === 'employer'&& vacancy?.employer_id == authStore.user?.id">
      <button @click="deleteVacancy" type="button" class="delete-button">
        Удалить
      </button>
    </div>

    <div  class="container-2">
      <h3>Вы работник этой компании? Оставьте отзыв!</h3>
      <form @submit.prevent="submitComment" style="margin-top: 10px;">
        <textarea
         v-model="commentText"
          placeholder="Ваш отзыв..."
          class="form-control"
          rows="4"
          required
        ></textarea>
        <button type="submit" class="button">Отправить</button>
      </form>
    </div>

    <div style="margin-top: 40px;">
      <h3>Отзывы на работодателя ({{ comments.length }})</h3>
      <div v-if="comments.length === 0">
        <p>Пока нет отзывов.</p>
      </div>
      <div v-else>
        <div
          v-for="comment in comments"
          :key="comment.id"
          style="margin-top: 15px; padding: 10px; background: #f9f9f9; border-radius: 6px;"
        >
          <div style="font-weight: bold; color: #333;">{{ comment.author_name }}</div>
          <div style="font-size: 0.9em; color: #777; margin: 5px 0;">
            {{ new Date(comment.date).toLocaleDateString() }}
          </div>
          <div style="margin-top: 8px;">{{ comment.text }}</div>
              <div style="margin-top: 8px;">
            <button @click="deleteComment(comment.id)" class="delete-button" style="font-size: 0.9em; padding: 4px 8px;">
              Удалить отзыв
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Кнопка "Назад" -->
    <div class="back" style="margin-top: 30px;">
      <RouterLink to="/vacancies">← Вернуться к списку вакансий</RouterLink>
    </div>
  </div>

  <div v-else>
    <p>Загрузка вакансии...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { CATEGORIES } from '@/utils/categories'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const vacancy = ref(null)
const comments = ref([])
const commentText = ref('')

const loadComments = async () => {
  try {
    const res = await fetch(`/api/comment?vacancy_id=${route.params.id}`)
    if (res.ok) {
      const data = await res.json()
      comments.value = data.comments || []
    } else {
      console.error('Не удалось загрузить комментарии:', await res.json())
    }
  } catch (err) {
    console.error('Сетевая ошибка при загрузке комментариев:', err)
  }
}
onMounted(async () => {
  try {
    const res = await fetch(`/api/vacancy/${route.params.id}`)
    if (!res.ok) {
      console.error('Ошибка загрузки вакансии:', await res.json())
      return
    }
    const data = await res.json()
    vacancy.value = data

    await loadComments()
  } catch (err) {
    console.error('Сетевая ошибка:', err)
  }
})

const deleteComment = async (commentId) => {
  if (!confirm('Вы уверены, что хотите удалить этот отзыв?')) return

  try {
    const response = await fetch('/api/comment', {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id: commentId,
        type: 'vacancy'
      })
    })

    if (response.ok) {
      await loadComments()
    } else {
      const data = await response.json()
      alert(data.message || 'Ошибка удаления отзыва')
    }
  } catch (error) {
    console.error('Ошибка сети при удалении комментария:', error)
    alert('Не удалось подключиться к серверу')
  }
}

// Удаление вакансии
const deleteVacancy = async () => {
  if (!confirm('Вы уверены, что хотите удалить эту вакансию?')) return

  try {
    const res = await fetch('/api/vacancy', {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ id: route.params.id })
    })

    if (res.ok) {
      alert('Вакансия удалена')
      router.push('/vacancies')
    } else {
      const data = await res.json()
      alert(data.message || 'Ошибка удаления')
    }
  } catch (err) {
    console.error('Ошибка сети:', err)
    alert('Не удалось подключиться к серверу')
  }
}

const submitComment = async () => {
  try {
    const response = await fetch('/api/comment', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        text: commentText.value,
        vacancy_id: route.params.id 
      })
    })

    if (response.ok) {
      commentText.value = '' 
      await loadComments()
    } else {
      const data = await response.json()
      alert(data.message || 'Ошибка добавления комментария')
    }
  } catch (error) {
    console.error('Ошибка сети:', error)
    alert('Не удалось подключиться к серверу')
  }
}

const applyToVacancy = async () => {
  if (!authStore.isAuthenticated || authStore.user?.role !== 'applicant') {
    alert('Только соискатели могут откликаться на вакансии')
    return
  }

  try {
    const response = await fetch('/api/vacancy/apply', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ vacancy_id: route.params.id })
    })

    if (response.ok) {
      const data = await response.json()
      alert(data.message)
    } else if (response.status === 409) {
      alert('Вы уже откликнулись на эту вакансию')
    } else if (response.status === 401) {
      authStore.logoutLocal()
      router.push('/login')
    } else {
      const err = await response.json()
      alert(err.message || 'Ошибка при отклике')
    }
  } catch (error) {
    console.error('Ошибка сети:', error)
    alert('Не удалось подключиться к серверу')
  }
}
</script>

<style>
.container-2{
    max-width: 1250px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 100px;
    margin-top: 50px;
}

.delete-button {
  padding: 12px 28px;
  background: #f1a18b;
  color: #2d3748;
  font-size: 18px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  transition: all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.delete-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background: #f3bba8;}

</style>