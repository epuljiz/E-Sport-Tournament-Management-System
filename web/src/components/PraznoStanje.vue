<script setup lang="ts">
defineProps<{
  poruka?: string;
}>();
</script>

<template>
  <div class="empty-state text-center card glass mt-4">
    <div class="icon">📁</div>
    <h3 class="mt-4">{{ poruka || 'Nema podataka' }}</h3>
    <p class="text-secondary mt-4">Trenutno nema dostupnih zapisa za prikaz.</p>
  </div>
</template>

<style scoped>
.empty-state {
  padding: 3rem 1.5rem;
}
.icon {
  font-size: 3rem;
  opacity: 0.5;
}
.text-secondary {
  color: var(--text-secondary);
}
</style>
