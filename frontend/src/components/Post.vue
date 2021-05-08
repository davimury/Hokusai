<template>
  <div
    class="bg-lightgray border border-lightgray rounded-lg block w-full mb-16 text-white"
  >
    <div class="flex items-center px-4 py-3">
      <img
        class="h-8 w-8 rounded-full"
        src="https://picsum.photos/id/1027/150/150"
      />
      <div class="ml-3 ">
        <span class="text-sm font-semibold antialiased block leading-tight"
          >8fact</span
        >
      </div>
    </div>
    <div>
      <carousel
        :per-page="1"
        :mouse-drag="true"
        :centerMode="true"
        :paginationPosition="'bottom'"
        :paginationActiveColor="'#8B5CF6'"
      >
        <slide class="m-auto">
          <img src="https://picsum.photos/id/244/900/900" />
        </slide>
        <slide class="m-auto">
          <img
            src="https://images.unsplash.com/photo-1619898109079-a0d36c4b35e6?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
          />
        </slide>
        <slide class="m-auto">
          <img
            src="https://images.unsplash.com/photo-1531501410720-c8d437636169?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1267&q=80"
          />
        </slide>
        <slide class="m-auto">
          Slide 4 Content
        </slide>
        <slide class="m-auto">
          Slide 5 Content
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

    <div class="mx-4 mt-2 mb-4">
      <span class="text-sm font-semibold antialiased leading-tight"
        >8fact
      </span>
      <span
        ><span class="text-sm antialiased leading-tight"
          >Testando essa legenda carai 2</span
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
