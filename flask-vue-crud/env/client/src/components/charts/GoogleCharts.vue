<template>
  <div class="flow_chart" v-if="showchart">
    <Moveable
      v-if="showchart"
      v-bind="moveable"
      @drag="handleDrag">
      <v-card elevation=24 v-if="showchart">
        <v-app-bar
          dense
          dark
          color="blue"
          class="drag_icon"
        >
          <v-toolbar-title>{{ title }}</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-menu offset-y>
            <template v-slot:activator="{ on }">
                <v-icon
                v-on="on">mdi-chevron-down</v-icon>
            </template>
            <v-list>
              <v-list-item
                v-for="(item, index) in graphOptions"
                :key="index"
                @click="changeGraph(item)"
              >
                <v-list-item-title>{{ item }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
          <v-icon @click="close">mdi-close</v-icon>
        </v-app-bar>
        <GChart
          :type="typeString"
          :data="chartData"
        />
      </v-card>
    </Moveable>
  </div>
</template>

<script>
export default {
  props: {
    title: String,
    chartData: Array,
  },
  data() {
    return {
      showchart: true,
      typeString: 'LineChart',
      graphOptions: ['BarChart', 'ColumnChart'],
      removedChartOption: 'LineChart',
      moveable: {
        draggable: true,
      },
    };
  },
  methods: {
    handleDrag({ target, transform }) {
      // eslint-disable-next-line
      console.log('onDrag left, top', transform);
      target.style.transform = transform; // eslint-disable-line no-param-reassign
    },
    close() {
      this.showchart = false;
      this.$parent.showchart = false;
      this.$parent.chartData = [['Date', 'High', 'Low']]; // Array of Arrays;
    },
    changeGraph(item) {
      const removedIndex = this.graphOptions.indexOf(item);
      // eslint-disable-next-line
      const temp = this.graphOptions.splice(removedIndex, 1);
      if (this.typeString !== '') {
        this.graphOptions.push(this.removedChartOption);
      }
      this.removedChartOption = item;
      this.typeString = item;
      this.$parent.clearChart();
    },
  },
};
</script>
