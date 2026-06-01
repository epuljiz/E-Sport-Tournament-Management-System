<script setup lang="ts">
// Komponenta za učitavanje (spinner/skeleton indikator)
</script>

<template>
  <div class="loading-container text-center mt-4 mb-4">
    <div class="spinner"></div>
    <p class="mt-4">Učitavanje podataka...</p>
  </div>
</template>

<style scoped>
.loading-container {
  padding: 2rem;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--primary-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
