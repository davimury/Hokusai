<script>
import { Bar } from "vue-chartjs";

export default {
  name: "BarChart",
  extends: Bar,
  props: ["chartdata", "labels", "label"],

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
    this.renderChart(
      {
        labels: this.labels,
        datasets: [
          {
            label: this.label,
            data: this.chartdata,
            backgroundColor: "#8B5CF6",
          },
        ],
      },
      this.options
    );
  },
};
</script>

<style>
</style>