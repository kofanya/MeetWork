<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'

onMounted(() => {
  const auth = useAuthStore()
  auth.checkAuth()
})
</script>


<template>
  <div class="page">
    <Header />
    <main class="content">
      <RouterView />
    </main>
    <Footer />
  </div>
</template>

<style>
.page{
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.content{
  flex: 1;
}

</style>
