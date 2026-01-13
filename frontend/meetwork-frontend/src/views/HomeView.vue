<template>
  <body>
    <main>
    <div class="page">
      <div class="text-column">
        <h1 class="welcome-title">Один клик и работа в кармане!</h1>
        <RouterLink to="/vacancies" class="button" >
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

.button{
  padding: 10px 30px;
  background: #BFC5A9;
  text-align: center;
  text-decoration: none;
  border: none;
  color: rgba(0, 0, 0, 0.8);
  font-size: 32px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.25s ease;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.20);
}
.text-column .button:hover,
.text-column .button:focus {
  background: #AEB494;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-1px);
}

</style>
