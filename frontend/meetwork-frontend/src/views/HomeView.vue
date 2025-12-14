<template>
  <main>
    <div class="container">
      <div class="text-column">
        <h1 class="welcome-title">Один клик и работа в кармане!</h1>
      </div>
      <div>
        <img src="/img/man.png" class="welcome-img"></img>
      </div>
    </div>
  </main>
</template>

<style>
.welcome-img{
  height:890px;
  width: 755px;
}

.container{
  display: grid;
  grid-template-columns: 1fr 1fr;
  height: 100vh;
}
.welcome-title{
  padding-top: 280px;
  font-size: 52px;
  font-weight: bold;
}

</style>
