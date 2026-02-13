import { defineStore } from 'pinia'
import axios from 'axios'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    publicSettings: {},
    projectsAllowed: true,
    projectsDisabledMessage: '',
    loading: false
  }),
  actions: {
    async loadPublicSettings() {
      this.loading = true
      try {
        const response = await axios.get('/api/settings/public')
        this.publicSettings = response.data

        const projectStatus = await axios.get('/api/settings/project-status')
        this.projectsAllowed = projectStatus.data.allowed
        this.projectsDisabledMessage = projectStatus.data.message
      } finally {
        this.loading = false
      }
    }
  },
  getters: {
    systemName: (state) => state.publicSettings.system_name || 'MakerSpace',
    footerText: (state) => state.publicSettings.footer_text || '',
    canCreateProjects: (state) => state.projectsAllowed
  }
})
