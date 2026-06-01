<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../../services/api';
import { useObavijestiStore } from '../../stores/obavijesti';

const router = useRouter();
const obavijesti = useObavijestiStore();

const name = ref('');
const orgName = ref('');
const password = ref('');
const loading = ref(false);

const submit = async () => {
  try {
    loading.value = true;
    await api.post('/teams/', {
      name: name.value,
      organization_name: orgName.value || null,
      password: password.value,
    });
    
    obavijesti.uspjeh('Tim i administratorski korisnik uspješno kreirani');
    router.push('/admin/timovi');
  } catch (e: any) {
    obavijesti.greska(e.message || 'Greška pri kreiranju tima');
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="container mt-4">
    <div style="display: flex; align-items: center; gap: 1rem;" class="mb-4">
      <button class="btn btn-sm" @click="router.push('/admin/timovi')">← Natrag</button>
      <h2>Kreiraj Novi E-sport Tim</h2>
    </div>

    <form @submit.prevent="submit" class="card glass" style="max-width: 500px; margin: 0 auto;">
      <div class="form-group mb-4">
        <label>Naziv Tima</label>
        <input v-model="name" type="text" class="form-control" placeholder="npr. G2 Esports" required />
      </div>
      <div class="form-group mb-4">
        <label>Naziv Organizacije</label>
        <input v-model="orgName" type="text" class="form-control" placeholder="npr. G2 Esports GmbH" />
      </div>
      
      <div class="mt-4 mb-4 p-4" style="background: rgba(255,255,255,0.05); border-radius: 8px;">
        <h4 style="margin-bottom: 1rem; color: var(--primary-color);">Team Admin Pristup</h4>
        <p style="font-size: 0.85rem; color: #aaa; margin-bottom: 1rem;">
          Sustav će automatski generirati korisničko ime za upravitelja tima na temelju naziva tima (npr. g2esports_admin). Molimo postavite mu lozinku za prijavu:
        </p>
        <div class="form-group">
          <label>Lozinka</label>
          <input v-model="password" type="password" class="form-control" required minlength="6" />
        </div>
      </div>
      
      <button type="submit" class="btn" style="width: 100%" :disabled="loading">
        {{ loading ? 'Spremanje...' : 'Kreiraj Tim' }}
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
