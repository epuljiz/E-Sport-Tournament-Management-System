<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from '../../services/api';
import { useObavijestiStore } from '../../stores/obavijesti';
import type { Team } from '../../types/api';
import Ucitavanje from '../../components/Ucitavanje.vue';
import PraznoStanje from '../../components/PraznoStanje.vue';

const obavijesti = useObavijestiStore();
const timovi = ref<Team[]>([]);
const loading = ref(true);

const fetchTimovi = async () => {
  try {
    loading.value = true;
    const { data } = await api.get<Team[]>('/teams');
    timovi.value = data;
  } catch (e: any) {
    obavijesti.greska('Greška pri dohvaćanju timova');
  } finally {
    loading.value = false;
  }
};

onMounted(fetchTimovi);

const formatDatum = (datum: string) => new Date(datum).toLocaleDateString('hr-HR');
</script>

<template>
  <div class="container mt-4">
    <div class="header">
      <div style="display: flex; align-items: center; gap: 1rem;">
        <button class="btn btn-sm" @click="$router.push('/admin/pocetna')">← Natrag</button>
        <h2>Upravljanje Timovima</h2>
      </div>
      <button class="btn" @click="$router.push('/admin/timovi/novi')">Kreiraj Tim</button>
    </div>

    <Ucitavanje v-if="loading" />
    <PraznoStanje v-else-if="timovi.length === 0" poruka="Nema kreiranih timova" />
    
    <div v-else class="grid mt-4">
      <div v-for="t in timovi" :key="t.id" class="card glass">
        <h3>{{ t.name }}</h3>
        <p class="text-secondary">{{ t.organization_name }}</p>
        <div class="mt-4" style="font-size: 0.9rem;">
          <p><strong>Admin korisnik:</strong> {{ t.admin_username }}</p>
          <p><strong>Datum kreiranja:</strong> {{ formatDatum(t.created_at) }}</p>
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
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}
.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}
</style>
