import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index'
import './style.css'
import { useAuthStore } from './stores/auth'

const pinia = createPinia()
const app = createApp(App)

app.use(pinia)

async function bootstrap() {
  if (localStorage.getItem('access_token')) {
    try {
      await useAuthStore(pinia).dohvatiMene()
    } catch {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }

  app.use(router)
  app.mount('#app')
}

bootstrap()
