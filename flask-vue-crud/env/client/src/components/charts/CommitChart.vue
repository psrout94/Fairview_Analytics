<script>
import { Bar } from 'vue-chartjs';

export default {
  extends: Bar,
  data() {
    return {
      // Overwriting base render method with actual data.
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
      datasets: [
        {
          label: 'GitHub Commits',
          backgroundColor: '#f87979',
          data: [40, 20, 12, 39, 10, 40, 39, 80, 40, 20, 12, 11],
        },
      ],
    };
  },
  mounted() {
    this.renderChart(this.datacollection, this.options);
  },
};
</script>
