<script>
import {Bar} from "vue-chartjs";

export default {
  name: "BarChart",
  extends: Bar,
  props: ["data"],

  data: () => ({
    
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
            },
          },
        ],
      },
    },
  }),

  mounted() {
    this.renderChart(this.data, this.options);
  },
};
</script>

<style>
</style>