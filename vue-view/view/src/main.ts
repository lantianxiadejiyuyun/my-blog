import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "@/css/style.css"
import "@flaticon/flaticon-uicons/css/all/all.css"

const app = createApp(App)

app.use(router)

app.mount('#app')
