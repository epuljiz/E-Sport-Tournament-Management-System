<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const router = useRouter();

const username = ref('');
const password = ref('');
const errorMsg = ref('');
const loading = ref(false);

const handleLogin = async () => {
  errorMsg.value = '';
  loading.value = true;
  try {
    await auth.login(username.value, password.value);
    if (auth.isAdmin) {
      router.push('/admin/pocetna');
    } else {
      router.push('/team/pocetna');
    }
  } catch (err: any) {
    errorMsg.value = err.response?.data?.message || 'Greška pri prijavi';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="login-container">
    <div class="card glass">
      <h2 class="text-center mb-4">E-Sport Turniri - Prijava</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label>Korisničko ime</label>
          <input v-model="username" type="text" required />
        </div>
        <div class="mb-4">
          <label>Lozinka</label>
          <input v-model="password" type="password" required />
        </div>
        <p v-if="errorMsg" class="error-text">{{ errorMsg }}</p>
        <button type="submit" class="btn mt-4" :disabled="loading" style="width: 100%">
          {{ loading ? 'Prijava u tijeku...' : 'Prijavi se' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 1rem;
}
.card {
  width: 100%;
  max-width: 400px;
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}
</style>
