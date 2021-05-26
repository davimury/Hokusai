<template>
  <div class="h-screen">
    <Header></Header>
    <main class="flex h-content">
      <div
        class="w-full md:max-w-4xl mx-auto flex justify-center gap-5 flex-wrap p-3"
      >
      <ProfileCard cardData=""></ProfileCard>
      </div>
    </main>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "./Header.vue";
import Footer from "./Footer.vue";
import ProfileCard from './ProfileCard';

export default {
  name: "SearchConnection",
  components: {
    Header,
    Footer,
    ProfileCard
  },
    data() {
    return {
      cardsData: [],
      userTags: ["Teste", "Teste2"],
    };
  },
};
</script>

<style>
</style>