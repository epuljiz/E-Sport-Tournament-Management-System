<script setup lang="ts">
import { useAuthStore } from '../../stores/auth';
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const router = useRouter();
</script>

<template>
  <div class="container mt-4">
    <div class="header mb-4">
      <h2>Admin Nadzorna Ploča</h2>
    </div>
    
    <p class="text-secondary mb-4" style="font-size: 1.1rem;">
      Dobrodošli, <strong>{{ auth.user?.username }}</strong>! Odaberite modul za upravljanje sustavom:
    </p>

    <div class="dashboard-grid">
      <div class="dashboard-card glass" @click="router.push('/admin/turniri')">
        <div class="icon">🏆</div>
        <h3>Upravljanje Turnirima</h3>
        <p class="text-secondary mt-2">Kreirajte nove e-sport turnire, pregledavajte prijave timova i organizirajte natjecanja.</p>
      </div>

      <div class="dashboard-card glass" @click="router.push('/admin/timovi')">
        <div class="icon">👥</div>
        <h3>Upravljanje Timovima</h3>
        <p class="text-secondary mt-2">Dodajte nove organizacije u sustav, dodijelite im pristupne podatke i pregledajte postojeće baze timova.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.dashboard-card {
  padding: 2rem;
  border-radius: var(--border-radius);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.dashboard-card:hover {
  transform: translateY(-8px);
  background: rgba(99, 102, 241, 0.1);
  border-color: var(--primary-color);
  box-shadow: 0 15px 30px -10px rgba(99, 102, 241, 0.3);
}

.icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  filter: drop-shadow(0 0 10px rgba(255, 255, 255, 0.2));
}

.dashboard-card h3 {
  font-size: 1.4rem;
  color: white;
}
</style>
