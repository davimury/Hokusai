<template>
  <main class="h-screen">
    <Header></Header>
    <div class="mx-auto w-full md:max-w-4xl bg-lightgray pb-6 rounded-lg">
      <h1 class="text-white font-bold text-xl mb-5 p-5">Estatísticas</h1>
      <div class="my-10">
        <BarChart v-if="loadedUpchart" :chartdata="chartdata"></BarChart>
      </div>
    </div>
    <Footer></Footer>
  </main>
</template>

<script>
import Header from "./Header.vue";
import Footer from "./Footer.vue";
import BarChart from "./BarChart.vue";
export default {
  name: "Statistics",
  components: {
    Header,
    Footer,
    BarChart,
  },
  data: () => ({
    loadedUpchart: true,
    chartdata: {
      labels: [
        "Domingo",
        "Segunda",
        "Terça",
        "Quarta",
        "Quinta",
        "Sexta",
        "Sábado",
      ],
      datasets: [
        {
          label: "Upvotes",
          data: [65, 59, 80, 81, 56, 55, 40],
          backgroundColor: "#8B5CF6",
        },
      ],
    },
  }),
  mounted() {
   console.log('teste')
  },
};
</script>

<style>
</style>