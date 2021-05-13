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
  </div>
</template>

<script>
import { directive as onClickaway } from "vue-clickaway";
import Post from "./Post.vue";
import SuggestedConection from "./SuggestedConection.vue";
import Header from "./Header.vue";
export default {
  name: "Feed",
  components: {
    Post,
    SuggestedConection,
    Header,
  },
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      postsData: [
        {
          username: "Chris",
          description: "Isso é uma descrição",
          postType: 1,
          profile_picture: "https://picsum.photos/id/1027/150/150",
          slides: [
            "https://images.unsplash.com/photo-1619898109079-a0d36c4b35e6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1531501410720-c8d437636169?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1267&q=80",
          ],
        },
        {
          username: "Be",
          description: "Isso é uma descrição",
          postType: 1,
          profile_picture: "https://picsum.photos/id/1027/150/150",
          slides: [
            "https://images.unsplash.com/photo-1619898109079-a0d36c4b35e6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1531501410720-c8d437636169?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1267&q=80",
          ],
        },
      ],
    };
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
