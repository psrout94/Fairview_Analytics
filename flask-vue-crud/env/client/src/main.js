import 'bootstrap/dist/css/bootstrap.css';
import Vuex from 'vuex';
import Vue from 'vue';
import MarqueeText from 'vue-marquee-text-component';
import Moveable from 'vue-moveable';
import { GChart } from 'vue-google-charts';
import GoogleChart from '@/components/charts/GoogleCharts.vue';
import Snackbar from '@/components/Snackbar.vue';
import router from './router';
import vuetify from './plugins/vuetify';
import store from './store';
import App from './App.vue';

Vue.use(Vuex);
Vue.component('marquee-text', MarqueeText);
Vue.component('Moveable', Moveable);
Vue.component('GChart', GChart);
Vue.component('GoogleChart', GoogleChart);
Vue.component('Snackbar', Snackbar);
// Vue.use(storePlugin);

Vue.prototype.$appName = 'My App';

Vue.config.productionTip = false;

new Vue({
  store,
  router,
  vuetify,
  render: (h) => h(App),
}).$mount('#app');
