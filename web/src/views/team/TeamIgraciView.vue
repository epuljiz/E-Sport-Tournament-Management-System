<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from '../../services/api';
import { useObavijestiStore } from '../../stores/obavijesti';
import type { Player, Team } from '../../types/api';
import Ucitavanje from '../../components/Ucitavanje.vue';
import PraznoStanje from '../../components/PraznoStanje.vue';

const obavijesti = useObavijestiStore();
const igraci = ref<Player[]>([]);
const tim = ref<Team | null>(null);
const loading = ref(true);

const fetchData = async () => {
  try {
    loading.value = true;
    const teamRes = await api.get<Team[]>('/teams');
    if (teamRes.data.length > 0) {
      tim.value = teamRes.data[0];
      const playersRes = await api.get<Player[]>(`/teams/${tim.value.id}/players`);
      igraci.value = playersRes.data;
    }
  } catch (e: any) {
    obavijesti.greska('Greška pri dohvaćanju igrača');
  } finally {
    loading.value = false;
  }
};

const izbrisiIgraca = async (id: number) => {
  if (!tim.value) return;
  if (!confirm('Jeste li sigurni da želite ukloniti ovog igrača iz tima?')) return;
  try {
    await api.delete(`/teams/${tim.value.id}/players/${id}`);
    obavijesti.uspjeh('Igrač uspješno uklonjen');
    await fetchData();
  } catch (e: any) {
    obavijesti.greska('Greška pri brisanju igrača');
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="container mt-4">
    <div class="header">
      <div style="display: flex; align-items: center; gap: 1rem;">
        <button class="btn btn-sm" @click="$router.push('/team/pocetna')">← Natrag</button>
        <h2>Roster Tima</h2>
      </div>
      <button class="btn" @click="$router.push('/team/igraci/novi')">Dodaj Igrača</button>
    </div>

    <Ucitavanje v-if="loading" />
    <PraznoStanje v-else-if="igraci.length === 0" poruka="Trenutno nemate dodanih igrača u tim." />
    
    <div v-else class="grid mt-4">
      <div v-for="p in igraci" :key="p.id" class="card glass">
        <h3>{{ p.nickname }}</h3>
        <p class="text-secondary">{{ p.first_name }} {{ p.last_name }}</p>
        <div class="mt-2" style="display: flex; justify-content: space-between; align-items: center;">
          <span style="padding: 0.2rem 0.5rem; background: var(--primary-color); border-radius: 4px; font-size: 0.8rem;">
            {{ p.position }}
          </span>
          <button class="btn btn-sm btn-danger" @click="izbrisiIgraca(p.id)">Ukloni</button>
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
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}
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
