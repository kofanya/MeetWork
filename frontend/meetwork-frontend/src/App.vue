<script setup>
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
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

</style>


