<template>
  <div
    class="
      bg-lightergray
      text-white
      pb-6
      justify-center
      items-center
      overflow-hidden
      w-full
      sm:w-1/3
      lg:w-1/4
      rounded-lg
      shadow-sm
      m-2
    "
  >
    <div class="relative h-20">
      <img
        class="absolute h-full w-full object-cover"
        :src="getHeader(cardData.userId)"
      />
    </div>
    <div
      class="
        relative
        shadow
        mx-auto
        h-24
        w-24
        -my-12
        border-lightgray
        rounded-full
        overflow-hidden
        border-4
      "
    >
      <img class="object-cover w-full h-full" :src="getProfilePic(cardData.userId)" />
    </div>
    <div class="flex justify-center ml-11 mt-6 relative"></div>
    <div class="mt-8">
      <a :href="'/'+cardData.username">
        <h1 class="text-lg text-center font-semibold">{{ cardData.name }}</h1>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileCard",
  props: ["cardData"],

  methods: {
      getProfilePic(user_id) {
        try {
          console.log(user_id)
          return require(`@/assets/img/profile/${user_id}.jpg`);
        } catch {
          return require("@/assets/img/profile/default.jpg");
        }
      },
      getHeader(user_id) {
        try {
          return require(`@/assets/img/header/${user_id}.jpg`);
        } catch {
          return require("@/assets/img/header/default.jpg");
        }
      },
  },
};
</script>

<style>
</style>