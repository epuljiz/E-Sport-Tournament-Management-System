<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../../services/api';
import { useObavijestiStore } from '../../stores/obavijesti';
import type { Team } from '../../types/api';

const router = useRouter();
const obavijesti = useObavijestiStore();
const tim = ref<Team | null>(null);

const nickname = ref('');
const firstName = ref('');
const lastName = ref('');
const position = ref('');
const birthDate = ref('');
const nationality = ref('');

onMounted(async () => {
  try {
    const { data } = await api.get<Team[]>('/teams');
    if (data.length > 0) tim.value = data[0];
  } catch (e) {
    obavijesti.greska('Greška pri dohvaćanju tima');
  }
});

const submit = async () => {
  if (!tim.value) return;
  try {
    await api.post(`/teams/${tim.value.id}/players`, {
      nickname: nickname.value,
      first_name: firstName.value,
      last_name: lastName.value,
      position: position.value,
      birth_date: birthDate.value,
      nationality: nationality.value || null,
    });
    obavijesti.uspjeh('Igrač uspješno dodan');
    router.push('/team/igraci');
  } catch (e: any) {
    obavijesti.greska(e.message || 'Greška pri dodavanju igrača');
  }
};
</script>

<template>
  <div class="container mt-4">
    <div style="display: flex; align-items: center; gap: 1rem;" class="mb-4">
      <button class="btn btn-sm" @click="router.push('/team/igraci')">← Natrag</button>
      <h2>Dodaj Novog Igrača</h2>
    </div>

    <form @submit.prevent="submit" class="card glass" style="max-width: 500px; margin: 0 auto;">
      <div class="form-group mb-4">
        <label>In-game Ime (Nickname)</label>
        <input v-model="nickname" type="text" class="form-control" required />
      </div>
      <div class="form-group mb-4">
        <label>Ime</label>
        <input v-model="firstName" type="text" class="form-control" required />
      </div>
      <div class="form-group mb-4">
        <label>Prezime</label>
        <input v-model="lastName" type="text" class="form-control" required />
      </div>
      <div class="form-group mb-4">
        <label>Pozicija (Role)</label>
        <input v-model="position" type="text" class="form-control" placeholder="npr. IGL, AWPer, Entry" required />
      </div>
      <div class="form-group mb-4">
        <label>Datum rođenja</label>
        <input v-model="birthDate" type="date" class="form-control" required />
      </div>
      <div class="form-group mb-4">
        <label>Nacionalnost</label>
        <input v-model="nationality" type="text" class="form-control" placeholder="npr. Croatia" />
      </div>
      
      <button type="submit" class="btn" style="width: 100%">Dodaj Igrača</button>
    </form>
  </div>
</template>

<style scoped>
.btn-sm {
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
}
</style>
