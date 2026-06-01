<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useAuthStore } from '../../stores/auth';
import { useRouter } from 'vue-router';
import { api } from '../../services/api';
import type { Team } from '../../types/api';
import Ucitavanje from '../../components/Ucitavanje.vue';

const auth = useAuthStore();
const router = useRouter();
const tim = ref<Team | null>(null);
const loading = ref(true);

const fetchTeam = async () => {
  try {
    const { data } = await api.get<Team[]>('/teams');
    if (data.length > 0) {
      tim.value = data[0];
    }
  } catch (e) {
    console.error(e);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchTeam);
</script>

<template>
  <div class="container mt-4">
    <div class="header mb-4">
      <h2>Nadzorna Ploča Tima</h2>
    </div>
    
    <Ucitavanje v-if="loading" />
    
    <div v-else-if="tim">
      <p class="text-secondary mb-4" style="font-size: 1.1rem;">
        Dobrodošli, <strong>{{ auth.user?.username }}</strong>! Upravljate timom <span style="color: var(--primary-color); font-weight: bold;">{{ tim.name }}</span> ({{ tim.organization_name }}).
      </p>
      
      <div class="dashboard-grid">
        <div class="dashboard-card glass" @click="router.push('/team/igraci')">
          <div class="icon">🎮</div>
          <h3>Moj Roster</h3>
          <p class="text-secondary mt-2">Upravljajte svojim igračima. Dodajte nove talente u tim ili uklonite one koji više nisu aktivni.</p>
        </div>

        <div class="dashboard-card glass" @click="router.push('/team/turniri')">
          <div class="icon">⚔️</div>
          <h3>Prijave na Turnire</h3>
          <p class="text-secondary mt-2">Pregledajte sve dostupne turnire i prijavite svoj tim za natjecanja i borbu za nagrade.</p>
        </div>
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
  background: rgba(236, 72, 153, 0.1); /* Secondary color hint */
  border-color: var(--secondary-color);
  box-shadow: 0 15px 30px -10px rgba(236, 72, 153, 0.3);
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
