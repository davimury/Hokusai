<template>
  <main class="h-screen" @mousemove="mouseMove" >
    <Header></Header>
    <div >
      <NotFoundGhost :xAxis="xAxis" :yAxis="yAxis"></NotFoundGhost>
    </div>
    <Footer></Footer>
  </main>
</template>

<script>
import Header from "./Header.vue";
import NotFoundGhost from "./NotFoundGhost.vue";
import Footer from "./Footer.vue";
export default {
  name: "NotFoundPage",
  components: {
    Header,
    NotFoundGhost,
    Footer,
  },
  data() {
    return {
      xAxis: 0,
      yAxis: 0,
    };
  },
  methods: {
    mouseMove: function (event) {
      let pageX = this.windowWidth;
      let pageY = this.windowHeight;
      let mouseY = 0;
      let mouseX = 0;

      //verticalAxis
      mouseY = event.clientY;
      this.yAxis = ((pageY - mouseY) / pageY) * 100;
      //horizontalAxis
      mouseX = event.clientX / -pageX;
      this.xAxis = -mouseX * 50 - 50;
    },
  },
};
</script>

<style>
</style>