<template>
  <div
    class=" sm:hidden fixed bottom-0 w-screen z-20 px-4 bg-darkgray py-1"
  >
    <div class="flex text-center justify-between text-purple-500">
      <div class="mr-5 text-3xl relative">
        <Notification></Notification>
      </div>
      <div class="mr-5 hover:text-purple-600 text-3xl">
        <a href="#"><span class="material-icons"> search </span></a>
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
          <img
            class="h-8 w-8 rounded-full"
            :src="getProfilePic"
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
                <a :href="username" class="px-4 py-2"> Perfil </a>
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
  </div>
</template>

<script>
import { directive as onClickaway } from "vue-clickaway";
import CreatePost from "./CreatePost.vue";
import Notification from "./Notification";
import SearchBar from "./SearchBar.vue";
import { mapActions } from "vuex";
export default {
  name: "Footer",
  components: {
    CreatePost,
    Notification,
    SearchBar,
  },
  directives: {
    onClickaway: onClickaway,
  },
  data() {
    return {
      show: false,
      showModal: true,
      username: this.$store.getters.Username,
      userId: this.$store.getters.UserId,
    };
  },
  methods: {
    ...mapActions(["LogOut"]),
    away: function () {
      this.show = false;
    },
    modalAway: function () {
      this.showModal = false;
    },
    logout: async function () {
      await this.$store.dispatch("LogOut");
      this.$router.push("/login");
    },
  },
  computed: {
    getProfilePic() {
      try {
        return require(`@/assets/img/profile/${this.$store.getters.UserId}.jpg`);
      } catch {
        return require("@/assets/img/profile/default.jpg");
      }
    },
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