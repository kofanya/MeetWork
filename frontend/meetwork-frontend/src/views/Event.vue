<template>
  <div v-if="event" class="container-2">
    <h1>{{ event.title }}</h1>
    <div class="meta" style="margin: 15px 0; color: #666; font-size: 0.95em;">
      <span>Организатор: {{ event.organizer?.first_name }} {{ event.organizer?.last_name }}</span><br />
      <span>Категория: {{ EVENTCATEGORIES[event.category] || event.category || 'Без категории' }}</span><br />
      <span>Дата проведения:  {{ formatDate(event.date) }}</span><br/>
      <span>Место проведения:  {{ event.location || 'Не указано' }}</span>
    </div>
    <div class="event-text" style="line-height: 1.7; margin-top: 20px;">
      {{ event.description || 'Описание отсутствует' }}  
    </div>
    <div class="event-text" style="line-height: 1.7; margin-top: 20px;">
      {{ event.requirements|| 'Требования отсутствуют' }}  
    </div>

    <div v-if="authStore.isAuthenticated && authStore.user?.role != 'organizer' && authStore.user?.role === 'applicant'">
      <div style="margin-top: 20px;">
        <button @click="joinEvent" class="button" style="background: #c4fab6;">
          Записаться на мероприятие
        </button>
      </div>
    </div>

    <div v-else-if="!authStore.isAuthenticated">
      <div style="margin-top: 20px;">
        <RouterLink to="/login" class="button" style="background: #c4fab6;">
          Записаться на мероприятие
        </RouterLink>
      </div>
    </div>

    <div v-if="authStore.isAuthenticated && authStore.user?.role === 'organizer'&& event?.organizer_id == authStore.user?.id">
      <button @click="deleteEvent" type="button" class="delete-button">
        Удалить
      </button>
    </div>

    <div  class="container-2">
      <h3>Оставить комментарий</h3>
      <form @submit.prevent="submitComment" style="margin-top: 10px;">
        <textarea
         v-model="commentText"
          placeholder="Ваш комментарий..."
          class="form-control"
          rows="4"
          required
        ></textarea>
        <button type="submit" class="button">Отправить</button>
      </form>
    </div>

    <div style="margin-top: 40px;">
      <h3>Комментарии ({{ comments.length }})</h3>
      <div v-if="comments.length === 0">
        <p>Пока нет комментариев.</p>
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
              <button @click="deleteComment(comment.id)" class="delete-comment">
                Удалить комментарий
              </button>
          </div>
        </div>
      </div>
    </div>

    <div class="back" style="margin-top: 30px;">
      <RouterLink to="/events">← Вернуться к списку мероприятий</RouterLink>
    </div>
  </div>

  <div v-else>
    <p>Загрузка мероприятия...</p>
  </div>
   
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { EVENTCATEGORIES } from '@/utils/eventcategories'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const event = ref(null)
const comments = ref([])
const commentText = ref('')

// Форматирование даты
const formatDate = (dateStr) => {
  if (!dateStr) return '—'
  const date = new Date(dateStr)
  return date.toLocaleDateString('ru-RU', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadComments = async () => {
  try {
    const res = await fetch(`/api/comment?event_id=${route.params.id}`)
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
    const res = await fetch(`/api/event/${route.params.id}`)
    if (!res.ok) {
      console.error('Ошибка загрузки мероприятия:', await res.json())
      return
    }
    const data = await res.json()
    event.value = data

    await loadComments()
  } catch (err) {
    console.error('Сетевая ошибка:', err)
  }
})

const deleteComment = async (commentId) => {
  if (!confirm('Вы уверены, что хотите удалить этот комментарий?')) return

  try {
    const response = await fetch('/api/comment', {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        id: commentId,
        type: 'event'
      })
    })

    if (response.ok) {
      await loadComments()
    } else {
      const data = await response.json()
      alert(data.message || 'Ошибка удаления комментария')
    }
  } catch (error) {
    console.error('Ошибка сети при удалении комментария:', error)
    alert('Не удалось подключиться к серверу')
  }
}

const deleteEvent = async () => {
  if (!confirm('Вы уверены, что хотите удалить это мероприятие?')) return

  try {
    const res = await fetch('/api/event', {
      method: 'DELETE',
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ id: route.params.id })
    })

    if (res.ok) {
      alert('Мероприятие удалено')
      router.push('/events')
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
        event_id: route.params.id 
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

const joinEvent = async () => {
  if (!authStore.isAuthenticated || authStore.user?.role !== 'applicant') {
    alert('Только соискатели могут записываться на мероприятия')
    return
  }

  try {
    const response = await fetch('/api/event/join', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ event_id: route.params.id })
    })

    if (response.ok) {
      const data = await response.json()
      alert(data.message)
    } else if (response.status === 409) {
      alert('Вы уже записаны на это мероприятие')
    } else if (response.status === 401) {
      authStore.logoutLocal()
      router.push('/login')
    } else {
      const err = await response.json()
      alert(err.message || 'Ошибка при записи')
    }
  } catch (error) {
    console.error('Ошибка сети:', error)
    alert('Не удалось подключиться к серверу')
  }
}
</script>


<style scoped>

.container-2{
    max-width: 1250px;
    margin-left: auto;
    margin-right: auto;
    margin-bottom: 100px;
    margin-top: 50px;
}
</style>