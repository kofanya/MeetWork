<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-brand">
        <RouterLink to="/">
          <h3 class="logo-text">MeetWork</h3>
        </RouterLink>
        <span class="copyright">© 2026 Company, Inc</span>
      </div>
      <ul class="footer-social">
        <li>
          <a href="https://github.com/kofanya/MeetWork" aria-label="GitHub">
            GitHub
          </a>
        </li>
      </ul>
    </div>
  </footer>
</template>

<style scoped>
.logo-text {
  color: #E17801;
  font-size: 32px;
  margin: 0;
}

.footer {
  background-color: rgba(251, 235, 195, 0.6);
  padding: 20px 0;
  min-height: 70px;
  margin-top: 50px;
}

.footer-container {
  max-width: 1250px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 15px;
}

.footer-brand a {
  text-decoration: none;
}

.footer-social {
  list-style: none;
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

@media (max-width: 600px) {
  .footer-container {
    flex-direction: column; 
    gap: 15px;
    text-align: center;
  }

  .footer-brand {
    flex-direction: column;
    gap: 5px;
  }
}
</style>