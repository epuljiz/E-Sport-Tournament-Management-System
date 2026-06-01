<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { api } from '../../services/api';
import { useObavijestiStore } from '../../stores/obavijesti';
import Ucitavanje from '../../components/Ucitavanje.vue';
import PraznoStanje from '../../components/PraznoStanje.vue';

const obavijesti = useObavijestiStore();
const turniri = ref<any[]>([]);
const loading = ref(true);

const fetchTurniri = async () => {
  try {
    loading.value = true;
    const { data } = await api.get('/tournaments');
    turniri.value = data;
  } catch (e: any) {
    obavijesti.greska('Greška pri dohvaćanju turnira');
  } finally {
    loading.value = false;
  }
};


onMounted(fetchTurniri);
</script>

<template>
  <div class="container mt-4">
    <div class="header">
      <h2>Upravljanje Turnirima</h2>
      <button class="btn" @click="$router.push('/admin/turniri/novi')">Novi Turnir</button>
    </div>

    <Ucitavanje v-if="loading" />
    <PraznoStanje v-else-if="turniri.length === 0" poruka="Nema kreiranih turnira" />
    
    <div v-else class="grid mt-4">
      <div v-for="t in turniri" :key="t.id" class="card glass">
        <h3>{{ t.name }}</h3>
        <p class="text-secondary">{{ t.game }}</p>
        <p>Lokacija: {{ t.location }}</p>
        <div class="actions mt-4">
          <button class="btn btn-sm" @click="$router.push(`/admin/turniri/${t.id}`)">Detalji turnira</button>
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
.btn-danger {
  background-color: var(--danger-color);
}
.btn-danger:hover {
  background-color: #dc2626;
}
</style>
