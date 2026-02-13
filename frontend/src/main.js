import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { createVuetify } from 'vuetify'
import { i18n, loadDynamicTexts } from './i18n'
import { useSettingsStore } from './stores/settings'

const app = createApp(App)
const pinia = createPinia()
const vuetify = createVuetify({
  theme: {
    defaultTheme: 'school',
    themes: {
      school: {
        dark: false,
        colors: {
          primary: '#0D47A1',
          secondary: '#2E7D32',
          accent: '#FFB300'
        }
      }
    }
  }
})

app.use(pinia)
app.use(router)
app.use(vuetify)
app.use(i18n)

async function initApp() {
  const settingsStore = useSettingsStore()
  await Promise.all([settingsStore.loadPublicSettings(), loadDynamicTexts()])
  app.mount('#app')
}

initApp()
