<script>
import {Bar} from "vue-chartjs";

export default {
  name: "BarChart",
  extends: Bar,
  props: ["chartdata"],

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
    console.log(this.chartdata);
    this.renderChart(this.chartdata, this.options);
  },
};
</script>

<style>
</style>