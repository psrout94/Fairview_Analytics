<template>
  <v-app id='app'>
    <router-view></router-view>
    <!-- <trading-vue v-if="showtrade" :data="this.$data"></trading-vue> -->
    <!-- <D3BarChart v-if="showbar" :config="chart_config" :datum="chart_datum"></D3BarChart> -->
    <!-- <bar-graph v-if="showbar" :points="points"/> -->
  </v-app>
</template>

<script>
// import TradingVue from 'trading-vue-js';
// import { D3BarChart } from 'vue-d3-charts';

export default {
  name: 'App',

  components: {
    // TradingVue,
    // D3BarChart,
  },

  data: () => ({
    showtrade: false,
    showmonth: false,
  }),
};
</script>

<style>
.flow_chart {
  position: absolute !important;
  top: 70% !important;
  left: 50% !important;
  /* bring your own prefixes */
  transform: translate(-50%, -50%) !important;
  width: 70% !important;
  height: 100% !important;
}

.drag_icon {
  cursor: move;
}
</style>
