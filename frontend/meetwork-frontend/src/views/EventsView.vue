
<template>
  <div class="container">
    <h1 class="title">Актуальные мероприятия</h1>
    <label>Категория</label>
      <select class="form-control"required>
        <option v-for="(name, key) in EVENTCATEGORIES" :value="key">{{ name }}</option>
      </select><br>
    <div class="blog-cards">
      <div class="blog-card">
        <div class="card-header">
          <div class="category-wrapper">
            <span class="category-dot"></span>
            <span>Категория</span>
          </div>
          <h2 class="card-title">Название мероприятия</h2>
          <div class="meta">
            <span class="date">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
              </svg>
              Место проведения: Москва
            </span>
            <span class="date">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
              </svg>
              Дата проведения: 15 января 2026
            </span>
             <span>Организатор </span>
          </div>
        </div>

        <div class="card-content">
          <div class="description">Краткое описание мероприятия.</div>
          <div class="btn-wrapper">
            <RouterLink to="/event" class="read-more">
              Читать далее
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="arrow-icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M17.25 8.25L21 12m0 0l-3.75 3.75M21 12H3" />
              </svg>
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { EVENTCATEGORIES } from '@/utils/eventcategories'
</script>

<style scoped>
.blog-cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

.blog-card {
  background-color: #f9f4f4;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  height: auto;
  width: 840px;
  min-height: 220px;
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
}


.card-title {
  font-size: 1.4rem;
  font-weight: 700;
  margin: 8px 0 12px;
  color: #222;
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
  border-radius: 50px;
  font-weight: 600;
  font-size: 0.9rem;
  color: #E17801; 
  background: transparent;
  text-decoration: none;
  box-shadow: none; 
  transition: color 0.2s;
}

.read-more:hover {
  color: #c96801;
  background: transparent; 
}

.arrow-icon {
  width: 16px;
  height: 16px;
}

.bookmark-btn {
  width: 36px;
  height: 36px;
  border: none;
  border-radius: 50%;
  background: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.2s;
}

.bookmark-btn:hover {
  background: #e0e0e0;
}

.bookmark-btn svg {
  width: 18px;
  height: 18px;
  color: #666;
}
</style>