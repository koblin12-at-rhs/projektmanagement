<template>
  <div>
    <v-btn color="primary" @click="handleNewProject" :disabled="!settingsStore.canCreateProjects">
      {{ t('button.new_project') }}
    </v-btn>

    <v-alert v-if="!settingsStore.canCreateProjects" type="warning" class="mt-4" prominent>
      {{ settingsStore.projectsDisabledMessage }}
    </v-alert>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useSettingsStore } from '@/stores/settings'

const { t } = useI18n()
const settingsStore = useSettingsStore()
const router = useRouter()

const handleNewProject = () => {
  if (settingsStore.canCreateProjects) {
    router.push('/projects/new')
  }
}
</script>
