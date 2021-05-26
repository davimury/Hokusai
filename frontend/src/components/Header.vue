<template>
  <header class="sticky z-20 bg-darkgray top-0 p-2 px-2 ">
    <nav class=" flex justify-between">
      <div>
        <a href="/">
          <img class="w-48 md:w-60 inline-block" src="@/assets/img/logo-symb-nobg.svg" />
        </a>
      </div>

      <div class="hidden sm:block relative inline-block w-1/3">
        <span
          class="material-icons md-18 text-gray-400 cursor-pointer select-none absolute inset-y-0 right-3 mt-2 flex items-center"
          >search</span
        >
        <input
          class="block p-2 text-lg rounded-lg bg-black focus:ring-1 focus:ring-indigo-500 w-full text-white"
          placeholder="Pesquisar"
        />
      </div>

      <div class="hidden sm:flex text-center text-purple-500">
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
          <button v-on:click="showModal = !showModal"><span class="material-icons"> queue </span></button>
        </div>
        <div class="mr-5 hover:text-purple-600 text-3xl">
          <a href="/chat"><span class="material-icons"> question_answer </span></a>
        </div>
        <div class="mr-5 hover:text-purple-600 text-3xl">
          <a href="/saved"><span class="material-icons"> bookmark </span></a>
        </div>
        
        <div
            class="fixed z-10 inset-0 overflow-y-auto"
            aria-labelledby="modal-title"
            role="dialog"
            aria-modal="true"
            v-if="showModal"
          >
          <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
              <div class="fixed inset-0 bg-gray-900 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
              <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
              <div class="inline-block align-bottom overflow-hidden transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full" v-on-clickaway="modalAway">
                <div class="bg-lightgray border border-lightgray rounded-lg block w-full mb-16 text-white">
                  <CreatePost></CreatePost>
              </div>
            </div>
        </div>
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
              :src="getProfilePic"
            />
          </button>
          <!-- Dropdown Body -->
          <transition
            mode="out-in"
            enter-active-class="animate__animated animate__flipInX"
            leave-active-class="animate__animated animate__flipOutX"
          >
            <div
              v-if="show"
              id="dropBodyMenu"
              class="z-0 absolute right-0 w-40 mt-2 py-2 bg-lightgray border border-lightgray rounded-lg text-white"
            >
              <ul class="text-left">
                <li class="my-2 hover:text-gray-300">
                  <a href="/profile" class="px-4 py-2"> Perfil </a>
                </li>
                <li class="my-2 hover:text-gray-300">
                  <a href="#" class="px-4 py-2">Configurações</a>
                </li>
                <li class="my-2 hover:text-gray-300">
                  <a href="#" class="px-4 py-2"> Logout </a>
                </li>
              </ul>
            </div>
          </transition>
          <!-- // Dropdown Body -->
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
import { directive as onClickaway } from "vue-clickaway";
import CreatePost from "./CreatePost.vue";
export default {
  name: "Header",
  components: {
    CreatePost
  },
  directives: {
    onClickaway: onClickaway,
  },
  computed : {
    getProfilePic() { 
      return require('@/assets/img/profile/' + this.$store.getters.UserId + '.jpg')
    },
    openModal(){
      console.log('teste')
      this.modalState = true
    }
  },
  data() {
    return {
      show: false,
      showModal: false,
    };
  },
  methods: {
    away: function () {
      this.show = false;
    },
    modalAway: function () {
      this.showModal = false;
    },
  },
};
</script>

<style>
</style>