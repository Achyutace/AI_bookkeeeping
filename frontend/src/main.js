import { createApp } from 'vue'
import './style.css'
import router from './router'
import { createPinia } from 'pinia'
import App from './App.vue'

import ELementPlus from 'element-plus'
import 'element-plus/dist/index.css'



const pinia = createPinia()
const app = createApp(App)
app.use(router)
app.use(ELementPlus)
app.mount('#app')
