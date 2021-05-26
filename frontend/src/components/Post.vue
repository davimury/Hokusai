<template>

  <div
    class="bg-lightgray border border-lightgray rounded-lg block w-full mb-16 text-white"
  >
    <div class="flex items-center px-4 py-3">
      <img class="h-8 w-8 rounded-full" :src="require('@/assets/img/profile/' + postData.author_id + '.jpg')" />
      <div class="ml-3">
        <span class="text-sm font-semibold antialiased block leading-tight">{{
          postData.username
        }}</span>
      </div>
    </div>
    <div>
      <carousel
        v-if="postData.postType == 0"
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
          <img :src="require(`@/assets/img/posts/${slide}`)" />
        </slide>
      </carousel>
    </div>
    <div class="flex items-center justify-between mx-3 text-purple-500">
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
            <!-- {{bookmarkType}} -->
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
  mounted(){
    console.log(this.postData)
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
    }
  },
};
</script>

<style>
button.VueCarousel-dot:focus {
    outline: none;
}
html, body {
  max-width: 100vw;
  overflow-x: hidden;
}
</style>
