<template>
  <main class="h-screen">
    <Header></Header>
    <div class="mx-auto w-full md:max-w-4xl bg-lightgray pb-6 rounded-lg">
      <h1 class="text-white font-bold text-xl mb-5 p-5">Estatísticas</h1>
      <div class="my-10">
        <BarChart
          v-if="loadedUpchart"
          :chartdata="dataUpvotes"
          :labels="labels"
          :label="'Upvotes'"
        ></BarChart>
      </div>
      <div class="my-10">
        <BarChart
          v-if="loadedDownchart"
          :chartdata="dataDownvotes"
          :labels="labels"
          :label="'Downvotes'"
        ></BarChart>
      </div>
    </div>
    <Footer></Footer>
  </main>
</template>

<script>
import Header from "./Header.vue";
import Footer from "./Footer.vue";
import BarChart from "./BarChart.vue";
import axios from "axios";
export default {
  name: "Statistics",
  components: {
    Header,
    Footer,
    BarChart,
  },
  data: () => ({
    loadedUpchart: false,
    loadedDownchart: false,
    dataUpvotes: [],
    dataDownvotes: [],
    domingoUp: 0,
    segundaUp: 0,
    tercaUp: 0,
    quartaUp: 0,
    quintaUp: 0,
    sextaUp: 0,
    sabadoUp: 0,
    domingoDown: 0,
    segundaDown: 0,
    tercaDown: 0,
    quartaDown: 0,
    quintaDown: 0,
    sextaDown: 0,
    sabadoDown: 0,
    labels: [
      "Domingo",
      "Segunda",
      "Terça",
      "Quarta",
      "Quinta",
      "Sexta",
      "Sábado",
    ],
  }),

  async mounted() {
    await axios.get("/post/statistics").then((response) => {
      let upvotes = response["data"].upvotes_week_ago;
      let downvotes = response["data"].downvotes_week_ago;

      upvotes.forEach((upvote) => {
        switch (upvote) {
          case 0:
            this.domingoUp++;
            break;
          case 1:
            this.segundaUp++;
            break;
          case 2:
            this.tercaUp++;
            break;
          case 3:
            this.quartaUp++;
            break;
          case 4:
            this.quintaUp++;
            break;
          case 5:
            this.sextaUp++;
            break;
          case 6:
            this.sabadoUp++;
            break;

          default:
            break;
        }
      });

      downvotes.forEach((downvote) => {
        switch (downvote) {
          case 0:
            this.domingoDown++;
            break;
          case 1:
            this.segundaDown++;
            break;
          case 2:
            this.tercaDown++;
            break;
          case 3:
            this.quartaDown++;
            break;
          case 4:
            this.quintaDown++;
            break;
          case 5:
            this.sextaDown++;
            break;
          case 6:
            this.sabadoDown++;
            break;

          default:
            break;
        }
      });
      this.dataUpvotes = [
        this.domingoUp,
        this.segundaUp,
        this.tercaUp,
        this.quartaUp,
        this.quintaUp,
        this.sextaUp,
        this.sabadoUp,
      ];
      this.dataDownvotes = [
        this.domingoDown,
        this.segundaDown,
        this.tercaDown,
        this.quartaDown,
        this.quintaDown,
        this.sextaDown,
        this.sabadoDown,
      ];

      this.loadedUpchart = true;
      this.loadedDownchart = true;
    });
  },
};
</script>

<style>
</style>