<template>
  <div>
    <span
      class="
        material-icons
        md-18
        text-gray-400
        cursor-pointer
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
        v-if="query.length > 0 && searchResultsVisible"
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
          overflow-y-auto
          max-h-70h
          sm:max-h-30vh
          px-3
          text-left
          block
        "
      >
        <ul class="text-left">
          <li
            class="my-1 px-3 py-1 hover:bg-lightgray rounded-lg cursor-pointer"
          >
            <div class="flex items-center">
              <img
                class="h-12 w-12 rounded-full"
                src="https://images.unsplash.com/photo-1464802686167-b939a6910659?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1033&q=80"
              />
              <div class="ml-3">
                <a href="/">
                  <span
                    class="
                      text-sm
                      font-semibold
                      antialiased
                      block
                      leading-tight
                    "
                    >chris_</span
                  >
                  <h2 class="text-base">Chris</h2>
                </a>
              </div>
            </div>
          </li>
        </ul>
        <h2 v-if="searchResults.length === 0" class="text-center">
          Nenhum resultado foi encontrado para '{{ query }}'
        </h2>
        <div class="pt-2 mt-1">
          <a
            class="px-3 text-purple-500 hover:text-purple-600 font-semibold"
            href="/search"
            >Pesquisar em Tags</a
          >
        </div>
        <div class="border-t border-lightergray pt-2 mt-1">
          <a
            class="px-3 text-purple-500 hover:text-purple-600 font-semibold"
            href="/search"
            >Ver Mais</a
          >
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: "SearchBar",
  data() {
    return {
      searchResults: "c",
      query: "",
      searchResultsVisible: false,
    };
  },
};
</script>

<style>
</style>