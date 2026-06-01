<script setup lang="ts">
import { RouterView } from 'vue-router'
import Obavijesti from './components/Obavijesti.vue'
import NavBar from './components/NavBar.vue'
import AnimatedBackground from './components/AnimatedBackground.vue'
</script>

<template>
  <AnimatedBackground />
  <Obavijesti />
  <NavBar />
  <RouterView />
</template>
