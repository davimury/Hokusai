<template>
  <div class="h-screen ">
    <Header></Header>
    <main class="flex h-content">
      <div id="contactsSidebar"></div>
      
      <div class="h-full flex flex-col md:max-w-4xl bg-lightgray text-white">
        <div class="flex items-center px-4 py-3">
          <img
            class="h-12 w-12 rounded-full"
            src="https://picsum.photos/id/1027/150/150"
          />
          <div class="ml-3">
            <span class="text-lg font-semibold">Chris</span>
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