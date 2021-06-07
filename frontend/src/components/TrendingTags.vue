<template>
  <div
    class="
      bg-lightgray
      border border-lightgray
      rounded-lg
      block
      w-full
      text-white
      lg:float-left
      max-w-xs
    "
  >
    <div class="flex flex-col px-4 py-3">
      <h1 class="mb-5 text-lg font-semibold border-b border-lightergray pb-2">
        <span class="text-purple-500 frontend">#</span> Tags em alta
      </h1>
      <div class="mt-1 flex flex-col w-100">
        <div class="inline-block" v-for="(tag, index) in tags" :key="tag">
          <div class="mb-2">
            <span class="mr-4">{{ index + 1 }}</span>
            <span
              class="
                text-xs
                mr-2
                my-1
                uppercase
                tracking-wider
                border
                px-2
                text-purple-500
                border-purple-500
                hover:text-purple-600
                hover:border-purple-600
                cursor-pointer
              "
              >{{ tag }}</span
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TrendingTags",
  data() {
    return {
      tags: ["boku", "teste"],
    };
  },
  computed: {},
  methods: {},
};
</script>

<style>
</style>