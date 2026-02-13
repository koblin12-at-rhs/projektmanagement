<template>
  <v-container>
    <h1>{{ t('admin.system_settings') }}</h1>
    <v-expansion-panels>
      <v-expansion-panel v-for="category in categories" :key="category">
        <v-expansion-panel-title>{{ category }}</v-expansion-panel-title>
        <v-expansion-panel-text>
          <div v-for="setting in getSettingsByCategory(category)" :key="setting.key" class="mb-4">
            <v-switch
              v-if="setting.value_type === 'BOOLEAN'"
              v-model="setting.value"
              :label="setting.description"
              @change="updateSetting(setting)"
            />
            <v-text-field
              v-else
              v-model="setting.value"
              :label="setting.description"
              @blur="updateSetting(setting)"
            />
          </div>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import axios from 'axios'

const { t } = useI18n()
const settings = ref([])
const categories = ref([])

onMounted(async () => {
  const response = await axios.get('/api/admin/settings')
  settings.value = response.data
  categories.value = [...new Set(settings.value.map((s) => s.category))]
})

const getSettingsByCategory = (category) => settings.value.filter((s) => s.category === category)

const updateSetting = async (setting) => {
  await axios.put(`/api/admin/settings/${setting.key}`, { value: setting.value })
}
</script>
