<script setup lang="ts">
// Komponenta za animiranu pozadinu
</script>

<template>
  <div class="animated-background">
    <!-- Plutajuća imena igrica -->
    <div class="game game-1">CS2</div>
    <div class="game game-2">LEAGUE OF LEGENDS</div>
    <div class="game game-3">VALORANT</div>
    <div class="game game-4">DOTA 2</div>
    <div class="game game-5">ROCKET LEAGUE</div>
    <div class="game game-6">OVERWATCH 2</div>
    <div class="game game-7">RAINBOW SIX</div>
    <div class="game game-8">APEX LEGENDS</div>
    
    <!-- Animacija svjetlosnih krugova u pozadini (Glow effects) -->
    <div class="glow glow-1"></div>
    <div class="glow glow-2"></div>
    <div class="glow glow-3"></div>
  </div>
</template>

<style scoped>
.animated-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: -10;
  overflow: hidden;
  background-color: #050b14;
}

/* Tekstovi igrica */
.game {
  position: absolute;
  color: rgba(255, 255, 255, 0.03); /* Vrlo transparentan bijeli tekst */
  font-family: 'Inter', sans-serif;
  font-weight: 900;
  font-style: italic;
  white-space: nowrap;
  user-select: none;
  pointer-events: none;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  will-change: transform;
}

.game-1 { top: 15%; left: -20%; font-size: 8vw; animation: drift 50s linear infinite; }
.game-2 { top: 35%; left: 100%; font-size: 6vw; animation: drift-reverse 65s linear infinite; }
.game-3 { top: 60%; left: -30%; font-size: 9vw; animation: drift 55s linear infinite; }
.game-4 { top: 85%; left: 100%; font-size: 7vw; animation: drift-reverse 45s linear infinite; }
.game-5 { top: 5%; left: 100%; font-size: 5vw; animation: drift-reverse 60s linear infinite; }
.game-6 { top: 45%; left: -10%; font-size: 6.5vw; animation: drift 70s linear infinite; }
.game-7 { top: 75%; left: -40%; font-size: 10vw; animation: drift 80s linear infinite; }
.game-8 { top: 25%; left: -15%; font-size: 5.5vw; animation: drift 48s linear infinite; }

@keyframes drift {
  from { transform: translateX(0); }
  to { transform: translateX(150vw); }
}

@keyframes drift-reverse {
  from { transform: translateX(0); }
  to { transform: translateX(-150vw); }
}

/* Užareni krugovi za dubinu (ambient glow) */
.glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  z-index: -1;
  opacity: 0.4;
  animation: pulse 10s ease-in-out infinite alternate;
}

.glow-1 {
  width: 40vw;
  height: 40vw;
  background: var(--primary-color);
  top: -10vw;
  left: -10vw;
  animation-delay: 0s;
}

.glow-2 {
  width: 35vw;
  height: 35vw;
  background: var(--secondary-color);
  bottom: -10vw;
  right: -5vw;
  animation-delay: -5s;
}

.glow-3 {
  width: 30vw;
  height: 30vw;
  background: #3b82f6; /* Plava */
  top: 40%;
  left: 40%;
  animation-delay: -2s;
  opacity: 0.2;
}

@keyframes pulse {
  0% { transform: scale(1) translate(0, 0); opacity: 0.3; }
  100% { transform: scale(1.1) translate(20px, -20px); opacity: 0.5; }
}
</style>
