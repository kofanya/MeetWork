<template>
  <body>
    <main>
    <div class="page">
      <div class="text-column">
        <h1 class="welcome-title">Один клик и работа в кармане!</h1>
        <RouterLink to="/vacancies" class="vacancy-button" >
          Смотреть вакансии
        </RouterLink>
      </div>
      <div>
        <img src="/img/man.png" class="welcome-img"></img>
      </div>
    </div>
  </main>

  </body>
  
</template>

<style scoped>
.welcome-img{
  margin-top: -20px;
  height:890px;
  width: 755px;
}

.body{
  background-color: rgba(255, 242, 211, 0.8);
}
.page{
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 100vh;
  max-width: 1250px;
  margin-left: auto;
  margin-right: auto;
}
.welcome-title{
  padding-top: 230px;
  font-size: 52px;
  font-weight: bold;
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
  transition: all 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94); /* более плавная кривая */
}

.vacancy-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background: #e5ebce;
}
.text-column .button:hover,
.text-column .button:focus {
  background: #AEB494;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

</style>
