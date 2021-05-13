<template>
  <div
    class="bg-lightgray border border-lightgray rounded-lg block w-full mb-16 text-white"
  >
    <div class="flex items-center px-4 py-3">
      <img
        class="h-8 w-8 rounded-full"
        :src="postData.profile_picture"
      />
      <div class="ml-3 ">
        <span class="text-sm font-semibold antialiased block leading-tight"
          >{{postData.username}}</span
        >
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
        <slide v-for="(slide, index) in postData.slides" :key="slide[index]" class="m-auto">
          <img :src="slide" />
        </slide>
        
      </carousel>
    </div>
    <div class="flex items-center justify-between mx-3 -mt-7 text-purple-500">
      <div class=" relative flex -ml-2">
        <transition
          mode="out-in"
          enter-active-class="animate__animated animate__flipInX"
          leave-active-class="animate__animated animate__flipOutX"
        >
          <div
            class="z-10 absolute -mt-14 bg-lightergray rounded-lg p-0 "
            v-if="isEmojis"
          >
            <vue-feedback-reaction v-model="feedback" />
          </div>
        </transition>
        <vue-reaction-emoji
          @mouseover.native="isEmojis = true"
          v-on-clickaway="awayEmojis"
          :reaction="reaction"
          :is-active="isActive"
          :is-disabled="isDisabled"
          :height="40"
        />
      </div>
      <div class="flex ">
        <span class="material-icons text-3xl">
          bookmark_border
        </span>
      </div>
    </div>

    <div class="mx-4 mt-2 mb-4 text-left">
      <span class="text-sm font-semibold antialiased leading-tight"
        >{{postData.username}}
      </span>
      <span
        ><span class="text-sm antialiased leading-tight"
          >{{postData.description}}</span
        ></span
      >
    </div>
  </div>
</template>

<script>
import { VueFeedbackReaction, VueReactionEmoji } from "vue-feedback-reaction";
import { directive as onClickaway } from "vue-clickaway";
export default {
  name: "Post",
  props: ['postData'],
  components: {
    VueFeedbackReaction,
    VueReactionEmoji,
  },
  directives: {
    onClickaway: onClickaway,
  },
  data: () => ({
    feedback: " ",
    reaction: "good",
    isActive: true,
    isDisabled: false,
    isEmojis: false,
  }),
  methods: {
    awayEmojis: function() {
      this.isEmojis = false;
    },
  },
};
</script>

<style>
.vue-feedback-reaction {
  margin: 0 !important;
  transition: none;
}
.vue-feedback-reaction .reaction {
  padding: 0;
}
</style>
