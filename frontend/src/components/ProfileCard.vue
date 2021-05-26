<template>
  <div
    class="bg-lightgray text-white pb-6 justify-center items-center overflow-hidden w-full sm:w-1/3 lg:w-1/4 rounded-lg shadow-sm"
  >
    <div class="relative h-20">
      <img
        class="absolute h-full w-full object-cover"
        :src="cardData.backgroundPicture"
      />
    </div>
    <div
      class="relative shadow mx-auto h-24 w-24 -my-12 border-lightgray rounded-full overflow-hidden border-4"
    >
      <img
        class="object-cover w-full h-full"
        :src="cardData.profilePicture"
      />
    </div>
    <div class="flex justify-center ml-11 mt-6 relative"></div>
    <div class="mt-5">
      <h1 class="text-lg text-center font-semibold">{{ cardData.name }}</h1>
      <div class="flex justify-center text-gray-500">
        <button
          class="rounded-lg bg-purple-500 hover:bg-purple-600 focus:outline-none text-white p-2 mx-1 mt-2"
        >
          Conectar
        </button>
        <button
          class="rounded-lg bg-purple-500 hover:bg-purple-600 focus:outline-none text-white p-2 mx-1 mt-2"
        >
          Mensagem
        </button>
      </div>
    </div>
    <div class="mt-5 pt-3 flex flex-wrap mx-6 border-t border-lightergray">
      <div
        class="text-xs mr-2 my-1 uppercase tracking-wider border px-2 text-purple-500 border-purple-500 hover:text-purple-600 hover:border-purple-600 cursor-pointer"
        v-for="userTag in cardData.userTags"
        :key="userTag"
      >
        {{ userTag }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProfileCard",
  props: ["cardData"],
};
</script>

<style>
</style>