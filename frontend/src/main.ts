import { createApp } from "vue"
import { createPinia } from "pinia"

import { createVuetify } from "vuetify"
import * as components from "vuetify/components"
import * as directives from "vuetify/directives"

import "vuetify/styles"
import "@mdi/font/css/materialdesignicons.css"

import piniaPluginPersistedstate from "pinia-plugin-persistedstate"

import App from "./App.vue"
import router from "./router/index"

const app = createApp(App)

const vuetify = createVuetify({
    components,
    directives,
})
app.use(vuetify)

const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)

app.use(router)

app.mount("#app")
