<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-brand">
        <RouterLink to="/">
          <h3 class="logo-text">MeetWork</h3>
        </RouterLink>
        <span>© 2026 Company, Inc</span>
      </div>
      <ul class="footer-social">
        <li>
          <a href="#" aria-label="GitHub">
            <img src="#" alt="GitHub">
          </a>
        </li>
      </ul>
    </div>
  </footer>
</template>

<style>
.logo-text{
  color: #E17801;
  font-size: 32px;
  margin: 0;
  
}
  .footer {
  background-color: rgba(251, 235, 195, 0.6);
  height: 70px;
}

.footer-container {
  max-width: 1250px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-brand {
  display: flex;
  align-items: center;
}
.footer-brand a{
  text-decoration: none;
}

.footer-social {
  list-style: none;
  display: flex;
  gap: 1.5rem;
}
</style>

<script setup>
import { RouterLink } from 'vue-router'
</script>