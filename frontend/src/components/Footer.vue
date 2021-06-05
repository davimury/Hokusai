<template>
  <footer class="block sm:hidden fixed bottom-0 w-screen z-20 px-4 bg-darkgray py-1">
    <div class="flex text-center justify-between text-purple-500">
      <div class="mr-5 hover:text-purple-600 text-3xl relative">
        <button>
          <span class="material-icons">
            notifications
            <div
              style="width: 0.5rem; height: 0.5rem"
              class="bg-red-600 rounded-full -ml-1 float-right z-10"
            ></div>
          </span>
        </button>
      </div>
      <div class="mr-5 hover:text-purple-600 text-3xl">
        <a href="#"><span class="material-icons"> search </span></a>
      </div>
      <div class="mr-5 hover:text-purple-600 text-3xl">
        <a href="#"><span class="material-icons"> queue </span></a>
      </div>
      <div class="mr-5 hover:text-purple-600 text-3xl">
        <a href="/chat"><span class="material-icons"> question_answer </span></a>
      </div>
      <div class="mr-5 hover:text-purple-600 text-3xl">
        <a href="/saved"><span class="material-icons"> bookmark </span></a>
      </div>

      <div class="relative">
        <button
          v-on-clickaway="away"
          v-on:click="show = !show"
          class="flex items-center outline-none focus:outline-none rounded-full"
          :class="{ 'focus:ring-2 focus:ring-purple-500': show === true }"
        >
          <img
            class="h-8 w-8 rounded-full"
            src="https://picsum.photos/id/1027/150/150"
          />
        </button>
        <!-- Dropdown Body -->
        <transition
          mode="out-in"
          enter-active-class="animate__animated animate__fadeInUp"
          leave-active-class="animate__animated animate__fadeOutDown"
        >
          <div
            v-if="show"
            id="dropBodyMenu"
            class=" block absolute right-0 bottom-10 w-40 mt-2 py-2 bg-lightgray border border-lightgray rounded-lg text-white"
          >
            <ul class="text-left">
              <li class="my-2 hover:text-gray-300">
                <a :href="this.username" class="px-4 py-2"> Perfil </a>
              </li>
              <li class="my-2 hover:text-gray-300">
                <a @click="logout" class="px-4 py-2"> Logout </a>
              </li>
            </ul>
          </div>
        </transition>
        <!-- // Dropdown Body -->
      </div>
    </div>
  </footer>
</template>

<script>
import { directive as onClickaway } from "vue-clickaway";
export default {
  name: "Footer",
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      show: false,
    };
  },
  methods: {
    away: function () {
      this.show = false;
    },
  },
};
</script>

<style>
</style>