import Vue from 'vue';
import Router from 'vue-router';
import Alpha from '@/components/AlphaContainer.vue';
import Home from '@/components/HomePage.vue';
import Agriculture from '@/components/AgricultureContainer.vue';
import Economic from '@/components/EconomicContainer.vue';
import SEC from '@/components/SEC.vue';
import Fred from '@/components/FredContainer.vue';
import Account from '@/components/AccountContainer.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  // base: process.env.BASE_URL,
  routes: [
    {
      path: '/alpha',
      name: 'Alpha',
      component: Alpha,
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/agriculture',
      name: 'Agriculture',
      component: Agriculture,
    },
    {
      path: '/economic',
      name: 'Economic',
      component: Economic,
    },
    {
      path: '/sec',
      name: 'SEC',
      component: SEC,
    },
    {
      path: '/fred',
      name: 'Fred',
      component: Fred,
    },
    {
      path: '/account',
      name: 'Account',
      component: Account,
    },
  ],
});
