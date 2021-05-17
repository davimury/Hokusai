<template>
  <div>
    <Header></Header>
    <main class="flex justify-between container h-screen w-full mx-auto">
      <div class="w-1/3 h-screen hidden lg:block"></div>

      <div
        id="posts"
        class="w-full md:w-4/5 lg:w-3/5 h-screen overflow-y-scroll p-3"
      >
        <div class="w-full flex flex-col">
          <Post
            v-for="postData in postsData"
            :key="postData.username"
            :postData="postData"
          ></Post>
        </div>
      </div>

      <div id="right-bar" class="w-1/3 md:2/4 hidden lg:block h-screen p-3">
        <SuggestedConection></SuggestedConection>
      </div>
    </main>
    <Footer></Footer>
  </div>
</template>

<script>
import { directive as onClickaway } from "vue-clickaway";
import Post from "./Post.vue";
import SuggestedConection from "./SuggestedConection.vue";
import axios from 'axios';

import Header from "./Header.vue";
import Footer from "./Footer.vue";
export default {
  name: "Feed",
  components: {
    Post,
    SuggestedConection,
    Header,
    Footer
  },
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      postsData: []
    };
  },
  mounted () {
    axios.get('/v1/posts/').then( response => {
      this.postsData = response['data']
    })
  },
  methods: {
    logout: async function () {
      await this.$store.dispatch("LogOut");
      this.$router.push("/login");
    },
  },
};
</script>

<style>
#dropBodyMenu {
  animation-duration: 0.5s;
}
#left-bar::-webkit-scrollbar {
  width: 0px;
  background: transparent; /* make scrollbar transparent */
}
#posts::-webkit-scrollbar {
  width: 0px;
  background: transparent; /* make scrollbar transparent */
}
#right-bar::-webkit-scrollbar {
  width: 0px;
  background: transparent; /* make scrollbar transparent */
}
</style>
