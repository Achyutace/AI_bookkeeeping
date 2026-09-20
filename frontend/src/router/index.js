import { createRouter, createWebHistory } from 'vue-router'


const routes = [
    {path: '/table', component: () => import('../views/TableView.vue')},
    {path: '/calender', component: () => import('../views/CalenderView.vue')},
    {path: '/profile', component: () => import('../views/ProfileView.vue')},
]
const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;