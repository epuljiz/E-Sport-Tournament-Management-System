<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api } from '../../services/api';
import { useObavijestiStore } from '../../stores/obavijesti';
import type { Tournament, Registration } from '../../types/api';
import Ucitavanje from '../../components/Ucitavanje.vue';

const route = useRoute();
const router = useRouter();
const obavijesti = useObavijestiStore();

const turnir = ref<Tournament | null>(null);
const prijave = ref<Registration[]>([]);
const loading = ref(true);

const fetchSve = async () => {
  try {
    loading.value = true;
    const tId = route.params.id;
    
    const [tRes, pRes] = await Promise.all([
      api.get<Tournament>(`/tournaments/${tId}`),
      api.get<Registration[]>(`/tournaments/${tId}/registrations`)
    ]);

    turnir.value = tRes.data;
    prijave.value = pRes.data;

  } catch (e) {
    obavijesti.greska('Greška pri učitavanju podataka turnira');
  } finally {
    loading.value = false;
  }
};

onMounted(fetchSve);

const formatDatum = (datum: string) => new Date(datum).toLocaleDateString('hr-HR');
</script>

<template>
  <div class="container mt-4">
    <div style="display: flex; align-items: center; gap: 1rem;" class="mb-4">
      <button class="btn btn-sm" @click="router.push('/admin/turniri')">← Natrag</button>
      <h2>Detalji Turnira (Admin Prikaz)</h2>
    </div>

    <Ucitavanje v-if="loading" />

    <div v-else-if="turnir" class="card glass">
      <h3>{{ turnir.name }}</h3>
      <p class="text-secondary">{{ turnir.game }}</p>
      
      <div class="mt-4" style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
        <div>
          <p><strong>Lokacija:</strong> {{ turnir.location }}</p>
          <p><strong>Početak turnira:</strong> {{ formatDatum(turnir.start_date) }}</p>
        </div>
        <div>
          <p><strong>Preliminarni rok:</strong> {{ formatDatum(turnir.prelim_deadline) }}</p>
          <p><strong>Finalni rok:</strong> {{ formatDatum(turnir.final_deadline) }}</p>
        </div>
      </div>

      <div class="mt-4">
        <h4>Svi prijavljeni timovi ({{ prijave.length }})</h4>
        <ul v-if="prijave.length > 0" class="mt-2" style="list-style-type: none; padding: 0;">
          <li v-for="p in prijave" :key="p.id" style="padding: 0.5rem; background: rgba(255,255,255,0.05); margin-bottom: 0.5rem; border-radius: 4px; display: flex; justify-content: space-between;">
            <span>{{ p.team_name }}</span>
            <span class="text-secondary" style="font-size: 0.85rem;">Prijava zabilježena: {{ formatDatum(p.registration_date) }}</span>
          </li>
        </ul>
        <p v-else class="text-secondary mt-2">Trenutno nema prijavljenih timova na ovaj turnir.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}
</style>
