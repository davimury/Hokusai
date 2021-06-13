<template>
  <div>
    <span
      class="
        material-icons
        md-18
        text-gray-400
        select-none
        absolute
        sm:inset-y-0
        right-8
        sm:right-3
        mt-2
        flex
        items-center
      "
      >search</span
    >
    <input
      class="
        block
        p-2
        text-lg
        rounded-lg
        bg-black
        focus:ring-1 focus:ring-indigo-500
        w-full
        text-white
      "
      placeholder="Pesquisar"
      v-model="query"
      @input="getUsers"
      @blur="searchResultsVisible = false"
      @focus="searchResultsVisible = true"
      @keydown.esc="searchResultsVisible = false"
    />
    <transition
      mode="out-in"
      enter-active-class="animate__animated animate__fadeIn"
      leave-active-class="animate__animated animate__fadeOut"
    >
      
      <div
        v-if="query.length > 1 && searchResultsVisible"
        id="dropBodyMenu"
        class="
          z-10
          absolute
          w-11/12
          sm:w-full
          mt-2
          py-2
          bg-darkgray
          border border-lightergray
          rounded-lg
          text-white
          sm:max-h-30vh
          px-3
          text-left
          block
        "
        style="overflow-y: scroll !important; max-height: 70vh"
      >
        <ul class="text-left" v-for="user in searchResults" :key="user.user_id">
          <li
            class="my-1 px-3 py-1 hover:bg-lightgray rounded-lg cursor-pointer"
          >
            <a :href="'/' + user.username">
              <div class="flex items-center">
                <img
                  class="h-12 w-12 rounded-full"
                  :src="getProfilePic(user.user_id)"
                />
                <div class="ml-3">
                  <span
                    class="
                      text-sm
                      font-semibold
                      antialiased
                      block
                      leading-tight
                    "
                  >
                    {{ user.username }}</span
                  >
                  <h2 class="text-base">{{ user.name }}</h2>
                </div>
              </div>
            </a>
          </li>
        </ul>
        <h2 v-if="searchResults.length === 0" class="text-center">
          Nenhum usuário foi encontrado para '{{ query }}'
        </h2>
        <div class="border-t border-lightergray pt-2 mt-1">
          <a
            class="px-3 text-purple-500 hover:text-purple-600 font-semibold"
            :href="`/tag/${query}`"
            >Pesquisar em Tags</a
          >
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "SearchBar",
  data() {
    return {
      searchResults: [],
      query: "",
      searchResultsVisible: false,
    };
  },
  methods: {
    getUsers: async function () {
      if (this.query.length > 3) {
        axios.get(`/user/search/${this.query}`).then((response) => {
          this.searchResults = response["data"];
        });
      }
    },
    getProfilePic(id) {
      try {
        return require(`@/assets/img/profile/${id}.jpg`);
      } catch {
        return require("@/assets/img/profile/default.jpg");
      }
    },
  },
};
</script>

<style>
</style>