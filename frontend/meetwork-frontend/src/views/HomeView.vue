<template>
  <main class="main-bg">
    <div class="page">
      <div class="text-column">
        <h1 class="welcome-title">Один клик и работа в кармане!</h1>
        <RouterLink to="/vacancies" class="vacancy-button">
          Смотреть вакансии
        </RouterLink>
      </div>
      <div class="image-column">
        <img src="/img/man.png" class="welcome-img" alt="Welcome image" />
      </div>
    </div>
  </main>
</template>

<style scoped>
.main-bg {
  background-color: rgba(255, 242, 211, 0.2);
  min-height: calc(100vh - 70px); 
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.page {
  display: grid;
  grid-template-columns: 1fr 1fr;
  width: 100%;
  max-width: 1250px;
  margin: 0 auto;
  align-items: center; 
  padding: 20px;
  box-sizing: border-box;
}

.welcome-title {
  font-size: 52px;
  font-weight: bold;
  margin-bottom: 24px;
  line-height: 1.2;
}

.text-column {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.welcome-img {
  width: 100%;
  height: auto;
  max-width: 755px;
  object-fit: contain;
  display: block;
}

.image-column {
  display: flex;
  justify-content: center;
  align-items: center;
}

.vacancy-button {
  padding: 12px 28px;
  background: #BFC5A9;
  color: #2d3748;
  font-size: 18px;
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  transition: all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  display: inline-block;
  width: fit-content;
}

.vacancy-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background: #e5ebce;
}

@media (max-width: 1024px) {
  .welcome-title {
    font-size: 42px;
  }
}

@media (max-width: 900px) {
  .page {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 0;
  }

  .text-column {
    align-items: center;
    order: 2;
    padding-top: 0;
  }

  .image-column {
    order: 1;
    margin-bottom: -30px;
  }

  .welcome-title {
    font-size: 32px;
    margin-top: 10px;
  }

  .welcome-img {
    max-height: 400px;
    width: auto;
    max-width: 80%;
    margin: 0 auto;
  }
}
</style>
