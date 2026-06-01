import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import PrijavaView from '../views/PrijavaView.vue';
import NepoznatoView from '../views/NepoznatoView.vue';
import AdminPocetnaView from '../views/admin/AdminPocetnaView.vue';
import AdminTurniriView from '../views/admin/AdminTurniriView.vue';
import AdminTurnirFormaView from '../views/admin/AdminTurnirFormaView.vue';
import AdminTimoviView from '../views/admin/AdminTimoviView.vue';
import AdminTimFormaView from '../views/admin/AdminTimFormaView.vue';
import TeamPocetnaView from '../views/team/TeamPocetnaView.vue';
import TeamIgraciView from '../views/team/TeamIgraciView.vue';
import TeamIgracFormaView from '../views/team/TeamIgracFormaView.vue';
import TeamTurniriView from '../views/team/TeamTurniriView.vue';
import TeamTurnirDetaljiView from '../views/team/TeamTurnirDetaljiView.vue';

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: () => {
        const auth = useAuthStore();
        if (!auth.isAuthenticated) return '/prijava';
        return auth.isAdmin ? '/admin/pocetna' : '/team/pocetna';
      },
    },
    {
      path: '/prijava',
      component: PrijavaView,
      meta: { javno: true },
    },
    {
      path: '/admin',
      meta: { uloga: 'admin' },
      children: [
        { path: 'pocetna', component: AdminPocetnaView },
        { path: 'turniri', component: AdminTurniriView },
        { path: 'turniri/novi', component: AdminTurnirFormaView },
        { path: 'turniri/:id', component: () => import('../views/admin/AdminTurnirDetaljiView.vue') },
        { path: 'timovi', component: AdminTimoviView },
        { path: 'timovi/novi', component: AdminTimFormaView },
      ],
    },
    {
      path: '/team',
      meta: { uloga: 'team_admin' },
      children: [
        { path: 'pocetna', component: TeamPocetnaView },
        { path: 'igraci', component: TeamIgraciView },
        { path: 'igraci/novi', component: TeamIgracFormaView },
        { path: 'turniri', component: TeamTurniriView },
        { path: 'turniri/:id', component: TeamTurnirDetaljiView },
      ],
    },
    {
      path: '/:catchAll(.*)*',
      component: NepoznatoView,
      meta: { javno: true },
    },
  ],
});

router.beforeEach((to) => {
  const auth = useAuthStore();

  if (to.meta.javno) {
    if (auth.isAuthenticated) return auth.isAdmin ? '/admin/pocetna' : '/team/pocetna';
    return true;
  }

  if (!auth.isAuthenticated) return '/prijava';

  if (to.meta.uloga === 'admin' && !auth.isAdmin) return '/team/pocetna';
  if (to.meta.uloga === 'team_admin' && !auth.isClub) return '/admin/pocetna';

  return true;
});

export default router;
