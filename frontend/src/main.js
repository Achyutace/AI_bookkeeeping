import { createApp } from 'vue'
import './style.css'
import router from './router'
import { createPinia } from 'pinia'
import App from './App.vue'

import ELementPlus from 'element-plus'
import 'element-plus/dist/index.css'




const app = createApp(App)
app.use(router)
app.use(ELementPlus)
app.use(createPinia())
app.mount('#app')
