<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api } from '../../services/api';
import { useObavijestiStore } from '../../stores/obavijesti';
import type { Tournament, Registration, Team } from '../../types/api';
import Ucitavanje from '../../components/Ucitavanje.vue';

const route = useRoute();
const router = useRouter();
const obavijesti = useObavijestiStore();

const turnir = ref<Tournament | null>(null);
const prijave = ref<Registration[]>([]);
const mojTim = ref<Team | null>(null);
const loading = ref(true);
const actionLoading = ref(false);

const isPrijavljen = computed(() => {
  if (!mojTim.value || !prijave.value.length) return false;
  return prijave.value.some(r => r.team_id === mojTim.value!.id);
});

const mojaPrijava = computed(() => {
  if (!mojTim.value || !prijave.value.length) return null;
  return prijave.value.find(r => r.team_id === mojTim.value!.id);
});

const fetchSve = async () => {
  try {
    loading.value = true;
    const tId = route.params.id;
    
    const [tRes, pRes, timRes] = await Promise.all([
      api.get<Tournament>(`/tournaments/${tId}`),
      api.get<Registration[]>(`/tournaments/${tId}/registrations`),
      api.get<Team[]>('/teams')
    ]);

    turnir.value = tRes.data;
    prijave.value = pRes.data;
    if (timRes.data.length > 0) mojTim.value = timRes.data[0];

  } catch (e) {
    obavijesti.greska('Greška pri učitavanju podataka');
  } finally {
    loading.value = false;
  }
};

const prijava = async () => {
  try {
    actionLoading.value = true;
    await api.post(`/tournaments/${turnir.value!.id}/registrations`);
    obavijesti.uspjeh('Tim je uspješno prijavljen na turnir!');
    await fetchSve();
  } catch (e: any) {
    obavijesti.greska(e.message || 'Greška pri prijavi');
  } finally {
    actionLoading.value = false;
  }
};

const odjava = async () => {
  if (!confirm('Jeste li sigurni da želite povući prijavu tima?')) return;
  try {
    actionLoading.value = true;
    await api.post(`/tournaments/${turnir.value!.id}/registrations/${mojaPrijava.value!.id}/withdraw`);
    obavijesti.uspjeh('Prijava uspješno povučena.');
    await fetchSve();
  } catch (e: any) {
    obavijesti.greska(e.message || 'Greška pri odjavi');
  } finally {
    actionLoading.value = false;
  }
};

onMounted(fetchSve);

const formatDatum = (datum: string) => new Date(datum).toLocaleDateString('hr-HR');
</script>

<template>
  <div class="container mt-4">
    <div style="display: flex; align-items: center; gap: 1rem;" class="mb-4">
      <button class="btn btn-sm" @click="router.push('/team/turniri')">← Natrag</button>
      <h2>Detalji Turnira</h2>
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

      <div class="mt-4 p-4" style="background: rgba(255,255,255,0.05); border-radius: 8px;">
        <h4>Status Prijave</h4>
        <div v-if="isPrijavljen" class="mt-2">
          <p style="color: var(--primary-color)"><strong>✓ Vaš tim je prijavljen!</strong></p>
          <button class="btn btn-danger mt-2" @click="odjava" :disabled="actionLoading">Odjavi tim s turnira</button>
        </div>
        <div v-else class="mt-2">
          <p class="text-secondary">Vaš tim trenutno nije prijavljen na ovaj turnir.</p>
          <button class="btn mt-2" @click="prijava" :disabled="actionLoading">Prijavi moj tim</button>
        </div>
      </div>

      <div class="mt-4">
        <h4>Prijavljeni Timovi ({{ prijave.length }})</h4>
        <ul v-if="prijave.length > 0" class="mt-2" style="list-style-type: none; padding: 0;">
          <li v-for="p in prijave" :key="p.id" style="padding: 0.5rem; background: rgba(255,255,255,0.05); margin-bottom: 0.5rem; border-radius: 4px;">
            {{ p.team_name }}
            <span v-if="p.team_id === mojTim?.id" style="font-size: 0.8rem; color: var(--primary-color); margin-left: 0.5rem;">(Vaš tim)</span>
          </li>
        </ul>
        <p v-else class="text-secondary mt-2">Još nema prijavljenih timova.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}
.btn-danger {
  background-color: var(--danger-color);
}
.btn-danger:hover {
  background-color: #dc2626;
}
</style>
