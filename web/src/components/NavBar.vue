<script setup lang="ts">
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const router = useRouter();

const handleLogout = () => {
  auth.logout();
  router.push('/prijava');
};
</script>

<template>
  <nav v-if="auth.isAuthenticated" class="navbar glass">
    <div class="container navbar-content">
      <div class="brand" @click="router.push('/')">
        <span class="brand-text">⚡ E-Sports</span> Manager
      </div>
      <div class="nav-actions">
        <span class="user-greeting">Bok, <strong>{{ auth.user?.username }}</strong></span>
        <button @click="handleLogout" class="btn btn-sm btn-logout">Odjava</button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 2rem;
  background: rgba(15, 23, 42, 0.8) !important;
}
.navbar-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}
.brand {
  font-size: 1.25rem;
  font-weight: 800;
  cursor: pointer;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}
.brand-text {
  color: var(--secondary-color);
}
.nav-actions {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.user-greeting {
  color: var(--text-secondary);
  font-size: 0.9rem;
}
.btn-logout {
  background-color: transparent;
  border: 1px solid var(--danger-color);
  color: var(--danger-color);
}
.btn-logout:hover {
  background-color: var(--danger-color);
  color: white;
}
</style>
