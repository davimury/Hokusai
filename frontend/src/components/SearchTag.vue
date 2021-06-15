<template>
  <div class="h-screen" @mousemove="mouseMove">
    <Header></Header>
    <main class="h-content" >
      <div class="w-full md:max-w-4xl mx-auto p-3">
        <div class="block sm:hidden relative w-full mb-4">
          <SearchBar></SearchBar>
        </div>
        <section class="mt-5">
          <div
            v-if="posts.length > 0"
            class="
              pb-6
              mt-6
              w-full
              justify-center
              items-center
              mx-auto
              grid grid-cols-3
              gap-3
            "
          >
            <div
              v-for="post in posts"
              :key="post.post_id"
              class="bg-lightgray post-card cursor-pointer"
              @click="showPost(post)"
            >
              <img
                :src="thumbsData[post['post_id']]"
                class="media"
              />
            </div>
          </div>
          <div
            v-else
          >
            <NotFoundGhost :xAxis="this.xAxis" :yAxis="this.yAxis"></NotFoundGhost>
          </div>
          <transition
            mode="out-in"
            enter-active-class="animate__animated animate__fadeIn"
            leave-active-class="animate__animated animate__fadeOut"
          >
            <div
              class="fixed z-10 inset-0 overflow-y-auto"
              aria-labelledby="modal-title"
              role="dialog"
              aria-modal="true"
              v-if="showModalPost"
            >
              <div
                class="
                  flex
                  items-end
                  justify-center
                  min-h-screen
                  pt-4
                  px-4
                  pb-20
                  text-center
                  sm:block
                  sm:p-0
                "
              >
                <div
                  class="
                    fixed
                    inset-0
                    bg-gray-900 bg-opacity-75
                    transition-opacity
                  "
                  aria-hidden="true"
                ></div>

                <span
                  class="hidden sm:inline-block sm:align-middle sm:h-screen"
                  aria-hidden="true"
                  >&#8203;</span
                >
                <div
                  class="
                    inline-block
                    align-bottom
                    overflow-hidden
                    transform
                    transition-all
                    sm:my-8
                    sm:align-middle
                    sm:max-w-lg
                    sm:w-full
                  "
                  v-on-clickaway="awayModalPost"
                >
                  <Post :postData="this.postData"></Post>
                </div>
              </div>
            </div>
          </transition>
        </section>
      </div>
    </main>
    <Footer></Footer>
  </div>
</template>

<script>
import Header from "./Header.vue";
import Footer from "./Footer.vue";
import NotFoundGhost from "./NotFoundGhost.vue"
import { directive as onClickaway } from "vue-clickaway";
import Post from "./Post.vue";
import SearchBar from "./SearchBar.vue";
import axios from "axios";
import * as htmlToImage from 'html-to-image';

export default {
  name: "SearchConnection",
  components: {
    Header,
    Footer,
    NotFoundGhost,
    Post,
    SearchBar
  },
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      showModalPost: false,
      tag: this.$route.params.tag,
      thumbsData: {},
      posts: [],
      postData: {},
      windowWidth: window.innerWidth,
      windowHeight: window.innerHeight,
      xAxis: 0,
      yAxis: 0,
      globalSkipCounter: 0,
      globalSkipRate: 5
    };
  },
  mounted: async function () {
    axios.get(`/posts/by_tag/${this.tag.toLowerCase()}`)
    .then(async response => {
      if( response != undefined && response["data"].length > 0){
        await this.generateThumbs(response["data"])
        this.posts = response['data']
      }
    })
    
  },
  methods: {
    generateThumbs: async function(posts){
      for (let i = 0; i < posts.length; i++) {
        if (posts[i]['postType'] == 0){
          this.thumbsData[posts[i]['post_id']] = require(`@/assets/img/posts/${posts[i]['slides'][0]}`);
        } else {
          var div = document.createElement('div');
          div.style.backgroundColor = 'white';
          div.innerHTML = posts[i]['body'].trim();
          
          const img = await htmlToImage.toJpeg(div, {width: 300, height: 300})
          this.thumbsData[posts[i]['post_id']] = img
        }
      }
    },
    awayModalPost: function () {
      this.showModalPost = false;
    },
    showPost: function (post) {
      this.postData = post;
      this.showModalPost = true;
    },
    mouseMove: function (event) {
      let pageX = window.innerWidth;
      let pageY = window.innerHeight;
      let mouseY = 0;
      let mouseX = 0;

      if (this.globalSkipCounter >= this.globalSkipRate){
        //verticalAxis
        mouseY = event.clientY;
        this.yAxis = ((pageY - mouseY) / pageY) * 100;

        //horizontalAxis
        mouseX = event.clientX / -pageX;
        this.xAxis = -mouseX * 50 - 50;

        this.globalSkipCounter = 0;
      } else {
        this.globalSkipCounter += 1;
      }
    },
  },
};
</script>

<style>
</style>