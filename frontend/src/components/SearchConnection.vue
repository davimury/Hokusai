<template>
  <div class="h-screen">
    <Header></Header>
    <main class="flex h-content">
      <div
        class="card w-96 hover:shadow-none relative flex flex-col mx-auto shadow-lg m-5 rounded-lg bg-lightgray"
      >
        <img
          class="max-h-20 w-full  absolute top-0 rounded-t-lg"
          
          src="https://unsplash.com/photos/h0Vxgz5tyXA/download?force=true&w=640"
          alt=""
        />
        <div class="profile relative w-full flex m-3 ml-4 text-white">
          <img
            class="w-28 h-28 p-1 bg-lightgray rounded-full "
            src="https://images.pexels.com/photos/61100/pexels-photo-61100.jpeg?crop=faces&fit=crop&h=200&w=200&auto=compress&cs=tinysrgb"
            alt=""
          />
          <div class="title mt-11 ml-3 font-semibold flex flex-col">
            <div class="name break-words">Sarah</div>
          </div>
        </div>
      </div>
    </main>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "./Header.vue";
import Footer from "./Footer.vue";
export default {
  name: "Chat",
  components: {
    Header,
    Footer,
  },
};
</script>

<style>
</style>