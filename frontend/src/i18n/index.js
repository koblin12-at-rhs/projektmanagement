import axios from 'axios'
import { createI18n } from 'vue-i18n'
import de from './de.json'
import en from './en.json'

const messages = { de, en }

export const i18n = createI18n({
  legacy: false,
  locale: 'de',
  fallbackLocale: 'de',
  messages
})

export async function loadDynamicTexts() {
  const response = await axios.get('/api/admin/texts')
  const dynamicTexts = {}

  response.data.forEach((text) => {
    dynamicTexts[text.key] = text.text_short || text.text_long || text.text_html
  })

  i18n.global.mergeLocaleMessage('de', dynamicTexts)
}
