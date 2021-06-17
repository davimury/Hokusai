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
        :src="`https://cdn.hokusai.codes/header/${cardData.userId}.jpg?${cacheStr}`"
        @error="$event.target.src = 'https://cdn.hokusai.codes/header/default.jpg'"
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
      <img class="object-cover w-full h-full" :src="`https://cdn.hokusai.codes/profile/${cardData.userId}.jpg?${cacheStr}`" @error="$event.target.src = 'https://cdn.hokusai.codes/profile/default.jpg'"/>
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

  data(){
    return {
      cacheStr: Math.random().toString(36).substring(7)
    }
  }
};
</script>

<style>
</style>