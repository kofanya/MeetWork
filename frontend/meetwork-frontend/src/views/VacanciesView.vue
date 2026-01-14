
<template>
  <div class="container-2">
    <h1 class="title">Актуальные вакансии</h1>
    <label>Фильтрация по категориям: </label><br/>
      <select class="form-control"required>
        <option v-for="(name, key) in CATEGORIES" :value="key">{{ name }}</option>
      </select><br>

    <div class="blog-cards">

      <div class="blog-card">
        <div class="card-header">
          <div class="category-wrapper">
            <span class="category-dot"></span>
            <span>Категория</span>
          </div>
          <h2 class="card-title">Название вакансии</h2>
          <div class="meta">
            <span class="date">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 012.25-2.25h13.5A2.25 2.25 0 0121 7.5v11.25m-18 0A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75m-18 0v-7.5A2.25 2.25 0 015.25 9h13.5A2.25 2.25 0 0121 11.25v7.5" />
              </svg>
              Адрес предприятия: Москва
            </span>
             <span>Работодатель</span>
          </div>
        </div>

        <div class="card-content">
          <div class="description">Зарплата От</div>
          <div class="btn-wrapper">
            <RouterLink to="/vacancy" class="read-more">
              Читать далее...
            </RouterLink>
          </div>
        </div>
      </div>

      

    </div>

  </div>
</template>

<script>
import { CATEGORIES } from '@/utils/categories'
</script>

<style scoped>
.container-2 {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.title {
  text-align: center;
  margin: 40px 0 20px;
  color: #333;
}

.form-control {
  width: 100%;
  max-width: 380px;
  margin: 0 auto 24px;
  padding: 10px 16px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: white;
}

.blog-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 24px;
  justify-items: center;
}

.blog-card {
  background-color: #ffffff;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.25s ease, transform 0.2s ease;
  width: 100%;
  max-width: 380px;
  min-height: 260px;
  cursor: pointer;
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
}

.card-title {
  font-size: 1.3rem;
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
  -webkit-line-clamp: 2;
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
  gap: 6px;
  padding: 8px 16px;
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
</style>




