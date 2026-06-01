<script setup lang="ts">
import { useObavijestiStore } from '../stores/obavijesti';

const obavijesti = useObavijestiStore();
</script>

<template>
  <Transition name="fade">
    <div
      v-if="obavijesti.vidljivo"
      class="obavijest-toast"
      :class="obavijesti.tip"
    >
      <div class="sadrzaj">
        {{ obavijesti.poruka }}
      </div>
      <button @click="obavijesti.zatvori" class="zatvori-btn">&times;</button>
    </div>
  </Transition>
</template>

<style scoped>
.obavijest-toast {
  position: fixed;
  top: 1rem;
  right: 1rem;
  min-width: 300px;
  padding: 1rem;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 9999;
  color: white;
}

.info { background-color: var(--surface-hover); }
.greska { background-color: var(--danger-color); }
.uspjeh { background-color: var(--success-color); }

.sadrzaj {
  flex-grow: 1;
  margin-right: 1rem;
}

.zatvori-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  opacity: 0.8;
}

.zatvori-btn:hover {
  opacity: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>
