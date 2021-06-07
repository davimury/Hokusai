<template>
  <div class="h-screen">
    <Header></Header>
    <main class="h-content">
      <div class="w-full md:max-w-4xl mx-auto p-3">
        <div class="block sm:hidden relative w-full mb-4">
          <SearchBar></SearchBar>
        </div>
        <div class="w-full flex justify-center gap-5 bg-darkgray sticky top-0">
          <button
            class="
              text-white
              border-b-2
              hover:border-purple-600
              focus:outline-none
            "
            @click="changeSearchType(1)"
            :class="
              searchType == 1 ? 'border-purple-500' : 'border-lightergray'
            "
          >
            Usuários
          </button>
          <button
            class="
              text-white
              border-b-2
              hover:border-purple-600
              focus:outline-none
            "
            @click="changeSearchType(2)"
            :class="
              searchType == 2 ? 'border-purple-500' : 'border-lightergray'
            "
          >
            Tags
          </button>
        </div>
        <section v-if="searchType == 1" class="mt-5">
          <div class="h-full w-full flex flex-wrap justify-center">
            <ProfileCard
              v-for="cardData in cardsData"
              :key="cardData.username"
              :cardData="cardData"
            ></ProfileCard>
          </div>
        </section>
        <section v-if="searchType == 2" class="mt-5">
          <div
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
              :key="post.postId"
              class="bg-lightgray post-card cursor-pointer"
              @click="showPost(post.postId)"
            >
              <img :src="post.firstSlide" alt="" class="media" />
            </div>
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
                  <Post :postData="postData"></Post>
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
import ProfileCard from "./ProfileCard";
import { directive as onClickaway } from "vue-clickaway";
import Post from "./Post.vue";
import SearchBar from "./SearchBar.vue";
export default {
  name: "SearchConnection",
  components: {
    Header,
    Footer,
    ProfileCard,
    Post,
    SearchBar
  },
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      postData: {
        username: "Chris",
        description: "Isso é uma descrição",
        postType: 1,
        profile_picture: "https://picsum.photos/id/1027/150/150",
        slides: [
          "https://images.unsplash.com/photo-1619898109079-a0d36c4b35e6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
          "https://images.unsplash.com/photo-1531501410720-c8d437636169?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1267&q=80",
        ],
      },
      showModalPost: false,
      posts: [
        {
          postId: 1,
          firstSlide:
            "https://images.unsplash.com/photo-1619898109079-a0d36c4b35e6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
        },
      ],
      searchType: 1,
      cardsData: [
        {
          profilePicture:
            "https://images.unsplash.com/photo-1552058544-f2b08422138a?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=644&q=80",
          backgroundPicture:
            "https://images.unsplash.com/photo-1464802686167-b939a6910659?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1033&q=80",
          name: "Chris",
          userTags: "boku",
          username: "chris_",
        },
      ],
      userTags: [],
    };
  },
  methods: {
    changeSearchType: function (type) {
      this.searchType = type;
    },
    awayModalPost: function () {
      this.showModalPost = false;
    },
    showPost: function (id) {
      this.showModalPost = true;
      console.log(id);
      //usar id para receber do backend o post relacionado
    },
  },
};
</script>

<style>
</style>