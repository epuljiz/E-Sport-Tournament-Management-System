<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../../services/api';
import { useObavijestiStore } from '../../stores/obavijesti';

const router = useRouter();
const obavijesti = useObavijestiStore();

const name = ref('');
const game = ref('');
const startDate = ref('');
const location = ref('');
const prelimDeadline = ref('');
const finalDeadline = ref('');
const loading = ref(false);

const submit = async () => {
  try {
    loading.value = true;
    
    // Konvertiranje datetime-local u ISO format
    const formatDateTime = (dt: string) => {
      const d = new Date(dt);
      return d.toISOString();
    };

    await api.post('/tournaments/', {
      name: name.value,
      game: game.value,
      start_date: startDate.value,
      location: location.value,
      prelim_deadline: formatDateTime(prelimDeadline.value),
      final_deadline: formatDateTime(finalDeadline.value),
    });
    
    obavijesti.uspjeh('Turnir uspješno kreiran');
    router.push('/admin/turniri');
  } catch (e: any) {
    obavijesti.greska(e.message || 'Greška pri kreiranju turnira');
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="container mt-4">
    <div style="display: flex; align-items: center; gap: 1rem;" class="mb-4">
      <button class="btn btn-sm" @click="router.push('/admin/turniri')">← Natrag</button>
      <h2>Kreiraj Novi Turnir</h2>
    </div>

    <form @submit.prevent="submit" class="card glass" style="max-width: 600px; margin: 0 auto;">
      <div class="form-group mb-4">
        <label>Naziv Turnira</label>
        <input v-model="name" type="text" class="form-control" required />
      </div>
      <div class="form-group mb-4">
        <label>Igra (npr. CS2, LoL)</label>
        <input v-model="game" type="text" class="form-control" required />
      </div>
      <div class="form-group mb-4">
        <label>Lokacija</label>
        <input v-model="location" type="text" class="form-control" required />
      </div>
      <div class="form-group mb-4">
        <label>Datum Početka</label>
        <input v-model="startDate" type="date" class="form-control" required />
      </div>
      <div class="form-group mb-4">
        <label>Preliminarni Rok za Prijavu (Vrijeme)</label>
        <input v-model="prelimDeadline" type="datetime-local" class="form-control" required />
      </div>
      <div class="form-group mb-4">
        <label>Finalni Rok za Prijavu (Vrijeme)</label>
        <input v-model="finalDeadline" type="datetime-local" class="form-control" required />
      </div>
      
      <button type="submit" class="btn" style="width: 100%" :disabled="loading">
        {{ loading ? 'Spremanje...' : 'Kreiraj Turnir' }}
      </button>
    </form>
  </div>
</template>

<style scoped>
.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}
</style>
