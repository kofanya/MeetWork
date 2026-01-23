<script setup>
import { ref, computed, onMounted } from 'vue'
import { EVENTCATEGORIES } from '@/utils/eventcategories'

const events = ref([])
const loading = ref(true)
const selectedCategory = ref('')

const loadEvents = async () => {
  try {
    const res = await fetch('/api/event')
    if (res.ok) {
      const data = await res.json()
      events.value = data.events || []
    }
  } catch (error) {
    console.error('Ошибка загрузки мероприятий:', error)
  } finally {
    loading.value = false
  }
}

const filteredEvents = computed(() => {
  if (!selectedCategory.value) {
    return events.value
  }
  return events.value.filter(event => event.category === selectedCategory.value)
})
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

onMounted(() => {
  loadEvents()
})
</script>
<template>
  <div class="content-wrapper">
    <h1 class="title">Актуальные мероприятия</h1>

    <div class="filter-container">
      <label for="category-select">Фильтрация по категориям:</label>
      <select id="category-select" v-model="selectedCategory" class="form-control" required>
        <option value="">Все категории</option> <option v-for="(name, key) in EVENTCATEGORIES" :value="key" :key="key">{{ name }}</option>
      </select>
    </div>

    <div v-if="loading" class="loading">Загрузка...</div>
    <div v-else-if="filteredEvents.length === 0" class="no-events">
      Мероприятия не найдены.
    </div>
    
    <div v-else class="blog-cards">
       <div v-for="event in filteredEvents" :key="event.id" class="blog-card">
          <div class="card-header">
            <div class="category-wrapper">
              <span class="category-dot"></span>
              <span>{{ EVENTCATEGORIES[event.category] || event.category || 'Без категории' }}</span>
            </div>
            <h2 class="card-title">{{ event.title }}</h2>
            <div class="meta">
              <span class="location">
                Место проведения: {{ event.location || 'Не указано' }}
              </span>
              <span class="date">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
                </svg>
                Дата проведения: {{ formatDate(event.date) }}
              </span>
            </div>
          </div>

          <div class="card-content">
            <div class="description">{{ event.description || 'Описание отсутствует' }}</div>
            <div class="btn-wrapper">
              <RouterLink :to="`/event/${event.id}`" class="read-more">
                Читать далее...
              </RouterLink>
            </div>
          </div>
       </div>
    </div>
  </div>
</template>

<style scoped>
.content-wrapper {
  max-width: 840px; 
  width: 100%;
  margin: 0 auto;
  padding: 0 16px; 
  box-sizing: border-box;
  min-height: calc(100vh - 150px); 
  display: flex;
  flex-direction: column;
}

.title {
  margin-top: 20px;
  margin-bottom: 20px;
  font-size: 2rem;
}

/* --- Фильтр --- */
.filter-container {
  margin-bottom: 24px;
}

.filter-container label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

.form-control {
  width: 100%;
  max-width: 300px; 
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-size: 16px;
  background-color: #fff;
}

/* --- Сетка карточек --- */
.blog-cards {
  display: grid;
  grid-template-columns: 1fr; /* Одна колонка */
  gap: 24px;
  margin-bottom: 40px;
}


.blog-card {
  background-color: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.25s ease, transform 0.2s ease;
  width: 100%; 
  height: auto;
  min-height: 220px;
}

.blog-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px); 
}

.card-header {
  padding: 20px 20px 10px;
  color: #333;
}

.category-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.category-dot {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background-color: #9733EE;
  display: inline-block;
  flex-shrink: 0;
}

.card-title {
  font-size: 1.4rem;
  font-weight: 700;
  margin: 8px 0 12px;
  color: #222;
  word-wrap: break-word;
}

.meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 0.9rem;
  color: #555;
}

.date {
  display: flex;
  align-items: center;
  gap: 6px;
}

.icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.card-content {
  padding: 0 20px 20px;
}

.description {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #000;
  margin-bottom: 16px;
  
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.btn-wrapper {
  display: flex;
  gap: 12px;
  align-items: center;
}

.read-more {
  display: inline-flex;
  align-items: center;
  border: none;
  font-weight: 600;
  font-size: 0.9rem;
  color: #E17801; 
  background: transparent;
  text-decoration: none;
  transition: color 0.2s;
}

.read-more:hover {
  color: #c96801;
}

.loading, .no-events {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.1rem;
}

@media (max-width: 600px) {
  .title {
    font-size: 1.5rem;
    text-align: center;
  }

  .content-wrapper {
    padding: 0 12px;
  }

  .form-control {
    max-width: 100%;
  }
  
  .blog-card {
    border-radius: 8px; 
  }

  .card-header {
    padding: 15px 15px 5px;
  }
  
  .card-content {
    padding: 0 15px 15px;
  }

  .card-title {
    font-size: 1.2rem; 
  }

  .description {
    font-size: 0.9rem;
    -webkit-line-clamp: 4;
  }
}
</style>