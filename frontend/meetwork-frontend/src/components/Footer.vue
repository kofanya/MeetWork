<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-brand">
        <RouterLink to="/">
          <h3 class="logo-text">MeetWork</h3>
        </RouterLink>
        <span>© 2025 Company, Inc</span>
      </div>
      <ul class="footer-social">
        <li>
          <a href="#" aria-label="GitHub">
            <img src="#" alt="GitHub">
          </a>
        </li>
        <li>
          <a href="#" aria-label="Telegram">
            <img src="#" alt="Telegram">
          </a>
        </li>
      </ul>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>