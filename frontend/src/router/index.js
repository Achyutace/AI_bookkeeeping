import { createRouter, createWebHistory } from 'vue-router'


const routes = [
    {path: '/table', component: () => import('../views/TableView.vue')},
    {path: '/calendar', component: () => import('../views/CalendarView.vue')},
    {path: '/profile', component: () => import('../views/ProfileView.vue')},
]
const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router;