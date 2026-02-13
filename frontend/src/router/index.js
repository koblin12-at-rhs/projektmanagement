import { createRouter, createWebHistory } from 'vue-router'
import SettingsEditor from '@/views/admin/SettingsEditor.vue'
import TextEditor from '@/views/admin/TextEditor.vue'

const routes = [
  { path: '/admin/settings', component: SettingsEditor },
  { path: '/admin/texts', component: TextEditor }
]

export default createRouter({ history: createWebHistory(), routes })
