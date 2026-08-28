import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import EspecialistasView from '../views/EspecialistasView.vue'
import HorariosView from '../views/HorariosView.vue'
import ConfirmacaoView from '../views/ConfirmacaoView.vue'
import MeusAgendamentosView from '../views/MeusAgendamentosView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/especialistas' },
    { path: '/login', component: LoginView },
    { path: '/registrar', component: RegisterView },
    { path: '/especialistas', component: EspecialistasView, meta: { requiresAuth: true } },
    { path: '/especialistas/:id/horarios', component: HorariosView, meta: { requiresAuth: true }, props: true },
    { path: '/confirmacao/:id', component: ConfirmacaoView, meta: { requiresAuth: true }, props: true },
    { path: '/meus-agendamentos', component: MeusAgendamentosView, meta: { requiresAuth: true } },
  ],
})

router.beforeEach((to) => {
  const isAuth = !!localStorage.getItem('access_token')
  if (to.meta.requiresAuth && !isAuth) return '/login'
})

export default router