<template>
  <v-container>
    <h1>{{ t('admin.text_management') }}</h1>
    <v-row>
      <v-col cols="4">
        <v-list>
          <v-list-item
            v-for="text in texts"
            :key="`${text.key}-${text.language}`"
            :active="selectedText?.key === text.key"
            @click="selectText(text)"
          >
            <v-list-item-title>{{ text.key }}</v-list-item-title>
            <v-list-item-subtitle>{{ text.category }}</v-list-item-subtitle>
          </v-list-item>
        </v-list>
      </v-col>
      <v-col cols="8">
        <v-card v-if="selectedText">
          <v-card-title>{{ selectedText.key }}</v-card-title>
          <v-card-text>
            <v-text-field v-model="selectedText.text_short" label="Kurztext" density="compact" />
            <v-textarea v-model="selectedText.text_long" label="Langtext" rows="4" />
            <v-textarea v-model="selectedText.text_html" label="HTML-Version" rows="6" />
            <v-btn color="primary" @click="saveText" class="mt-4">{{ t('button.save') }}</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import axios from 'axios'

const { t } = useI18n()
const texts = ref([])
const selectedText = ref(null)

onMounted(async () => {
  texts.value = (await axios.get('/api/admin/texts')).data
})

const selectText = (text) => {
  selectedText.value = { ...text }
}

const saveText = async () => {
  await axios.put(`/api/admin/texts/${selectedText.value.key}`, selectedText.value)
  texts.value = (await axios.get('/api/admin/texts')).data
}
</script>
