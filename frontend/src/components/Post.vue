<template>
  <div
    class="bg-lightgray border border-lightgray rounded-lg block w-full mb-16 text-white"
  >
    <div class="flex items-center px-4 py-3">
      <img class="h-8 w-8 rounded-full" :src="postData.profile_picture" />
      <div class="ml-3">
        <span class="text-sm font-semibold antialiased block leading-tight">{{
          postData.username
        }}</span>
      </div>
    </div>
    <div>
      <carousel
        v-if="postData.postType == 1"
        :per-page="1"
        :mouse-drag="true"
        :centerMode="true"
        :paginationPosition="'bottom'"
        :paginationActiveColor="'#8B5CF6'"
      >
        <slide
          v-for="(slide, index) in postData.slides"
          :key="slide[index]"
          class="m-auto"
        >
          <img :src="slide" />
        </slide>
      </carousel>
    </div>
    <div class="flex items-center justify-between mx-3 -mt-7 text-purple-500">
      <div class="relative flex -ml-2">
        <button class="focus:outline-none">
          <span class="material-icons text-gray-500 hover:text-purple-500" :class="vote == 0 ? 'text-purple-500':''" @click="chooseVote(0)">
            arrow_upward
          </span>
        </button>
        <span class="text-white mx-1">30k</span>
        <button class="focus:outline-none">
          <span class="material-icons text-gray-500 hover:text-red-600" :class="vote == 1 ? 'text-red-600':''" @click="chooseVote(1)">
            arrow_downward
          </span>
        </button>
      </div>
      <div class="relative flex">
        <button class="focus:outline-none" @click="isSaved()">
          <span  class="material-icons text-3xl" >
            {{bookmarkType}}
          </span>
        </button>
      </div>
    </div>

    <div class="mx-4 mt-2 mb-4 text-left">
      <span class="text-sm font-semibold antialiased leading-tight"
        >{{ postData.username }}
      </span>
      <span
        ><span class="text-sm antialiased leading-tight">{{
          postData.description
        }}</span></span
      >
    </div>
  </div>
</template>

<script>
import { directive as onClickaway } from "vue-clickaway";
import axios from "axios";
export default {
  name: "Post",
  props: ["postData"],

  directives: {
    onClickaway: onClickaway,
  },
  data: () => ({
    isActive: true,
    isDisabled: false,
    isEmojis: false,
    vote: null,
    bookmarkType: 'bookmark_border'
  }),
  methods: {
    isSaved: function () {
      this.bookmarkType == 'bookmark_border' ? this.bookmarkType = 'bookmark' : this.bookmarkType = 'bookmark_border'
    },
    chooseVote: function(voteType){
      this.vote = voteType
    },
    createPost: function () {
      axios.post(
        "/v1/new_post/",
        JSON.stringify({
          body: "NOVO",
          images: [
            "https://images.unsplash.com/photo-1619898109079-a0d36c4b35e6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1531501410720-c8d437636169?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1267&q=80",
          ],
          reactions: [0, 0, 0, 0, 0],
        })
      );
    },
  },
};
</script>

<style>
button.VueCarousel-dot:focus {
    outline: none;
}
</style>
