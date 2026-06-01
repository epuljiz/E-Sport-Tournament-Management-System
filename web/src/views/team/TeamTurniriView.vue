<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../../services/api';
import { useObavijestiStore } from '../../stores/obavijesti';
import type { Tournament } from '../../types/api';
import Ucitavanje from '../../components/Ucitavanje.vue';
import PraznoStanje from '../../components/PraznoStanje.vue';

const router = useRouter();
const obavijesti = useObavijestiStore();
const turniri = ref<Tournament[]>([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const { data } = await api.get<Tournament[]>('/tournaments');
    turniri.value = data;
  } catch (e) {
    obavijesti.greska('Greška pri dohvaćanju turnira');
  } finally {
    loading.value = false;
  }
});

const formatDatum = (datum: string) => new Date(datum).toLocaleDateString('hr-HR');
</script>

<template>
  <div class="container mt-4">
    <div class="header mb-4">
      <div style="display: flex; align-items: center; gap: 1rem;">
        <button class="btn btn-sm" @click="router.push('/team/pocetna')">← Natrag</button>
        <h2>Dostupni Turniri</h2>
      </div>
    </div>

    <Ucitavanje v-if="loading" />
    <PraznoStanje v-else-if="turniri.length === 0" poruka="Trenutno nema otvorenih turnira." />
    
    <div v-else class="grid">
      <div v-for="t in turniri" :key="t.id" class="card glass">
        <h3>{{ t.name }}</h3>
        <p class="text-secondary">{{ t.game }}</p>
        <div class="mt-2" style="font-size: 0.9rem;">
          <p><strong>Lokacija:</strong> {{ t.location }}</p>
          <p><strong>Početak:</strong> {{ formatDatum(t.start_date) }}</p>
          <p><strong>Rok za prijavu:</strong> <span style="color: var(--danger-color)">{{ formatDatum(t.prelim_deadline) }}</span></p>
        </div>
        <div class="mt-4">
          <button class="btn" style="width: 100%" @click="router.push(`/team/turniri/${t.id}`)">Detalji i Prijava</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}
.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}
</style>
