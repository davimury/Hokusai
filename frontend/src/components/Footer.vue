<template>
  <div class="sm:hidden fixed bottom-0 w-screen z-20 px-4 bg-darkgray py-1">
    <div class="flex text-center justify-between text-purple-500">
      <div class="mr-5 text-3xl relative">
        <Notification></Notification>
      </div>
      <div class="mr-5 hover:text-purple-600 text-3xl">
        <span
          class="material-icons cursor-pointer"
          v-on:click="showModalSearch = !showModalSearch"
        >
          search
        </span>
      </div>
      <div class="mr-5 hover:text-purple-600 text-3xl">
        <button>
          <a href="/create-post"><span class="material-icons"> queue </span></a>
        </button>
      </div>
      <div class="mr-5 hover:text-purple-600 text-3xl">
        <a href="/chat"
          ><span class="material-icons"> question_answer </span></a
        >
      </div>

      <div class="relative">
        <button
          v-on-clickaway="away"
          v-on:click="show = !show"
          class="flex items-center outline-none focus:outline-none rounded-full"
          :class="{ 'focus:ring-2 focus:ring-purple-500': show === true }"
        >
          <img class="h-8 w-8 rounded-full" :src="`https://cdn.hokusai.codes/profile/${this.$store.getters.UserId}.jpg?${cacheStr}`" @error="$event.target.src = 'https://cdn.hokusai.codes/profile/default.jpg'"/>
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
            class="
              block
              absolute
              right-0
              bottom-10
              w-40
              mt-2
              py-2
              bg-lightgray
              border border-lightgray
              rounded-lg
              text-white
            "
          >
            <ul class="text-left">
              <li class="my-2 hover:text-gray-300">
                <a :href="'/'+username" class="px-4 py-2"> Perfil </a>
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

  <transition
          mode="out-in"
          enter-active-class="animate__animated animate__fadeIn"
          leave-active-class="animate__animated animate__fadeOut"
        >
          <div
            class="fixed z-10 inset-0 overflow-hidden"
            aria-labelledby="modal-title"
            role="dialog"
            aria-modal="true"
            v-if="showModalSearch"
          >
            <div
              class="
                flex
                items-end
                justify-center
                min-h-screen
                pt-4
                px-4
                pb-20
                text-center
              "
            >
              <div
                class="
                  fixed
                  inset-0
                  bg-gray-900 bg-opacity-75
                  transition-opacity
                "
                aria-hidden="true"
              ></div>
              <span
                class="hidden sm:inline-block sm:align-middle sm:h-screen"
                aria-hidden="true"
                >&#8203;</span
              >
              <div
                class="
                  inline-block
                  
                  transform
                  transition-all
                  align-middle
                  rounded-lg
                  p-4
                  w-full
                  h-screen
                "
               
                
              >
                <div class="" v-on-clickaway="modalsearchAway">
                  <SearchBar></SearchBar>
                </div>
              </div>
            </div>
          </div>
        </transition>

  </div>
</template>

<script>
import { directive as onClickaway } from "vue-clickaway";
import Notification from "./Notification";
import SearchBar from "./SearchBar.vue";
import { mapActions } from "vuex";
export default {
  name: "Footer",
  components: {
    Notification,
    SearchBar,
  },
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      show: false,
      showModalSearch: false,
      username: this.$store.getters.Username,
      userId: this.$store.getters.UserId,
      cacheStr: Math.random().toString(36).substring(7)
    };
  },
  methods: {
    ...mapActions(["LogOut"]),
    away: function () {
      this.show = false;
    },
    modalsearchAway: function () {
      this.showModalSearch = false;
    },
    logout: async function () {
      await this.$store.dispatch("LogOut");
      this.$router.push("/login");
    },
  },
  mounted: {
    openModal() {
      this.modalState = true;
    },
  },
};
</script>

<style scoped>
.animate__animated {
  --animate-duration: 0.3s;
}
.animate__animated {
  --animate-duration: 0.3s;
}
</style>