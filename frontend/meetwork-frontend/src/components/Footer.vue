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
      </ul>
    </div>
  </footer>
</template>

<style>
  .footer {
  background-color: #FBEBC3;
  height: 70px;
  margin-top: 100px;
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